"""
Scheduled Tasks
----------------
All scheduler task functions referenced in hooks.py scheduler_events.
Source: PDF Section 4.1

Paths wired in hooks.py:
    "daily":   [
        "auto_dealer.tasks.send_service_reminders",
        "auto_dealer.tasks.check_insurance_renewals",
        "auto_dealer.tasks.check_amc_renewals",
    ],
    "weekly":  ["auto_dealer.tasks.slow_moving_inventory_alert"],
    "monthly": ["auto_dealer.tasks.generate_oem_monthly_report"],
"""

import frappe
from frappe import _
from frappe.utils import today, date_diff, add_days, getdate


# ─── Daily Tasks ──────────────────────────────────────────────────────────────

def send_service_reminders():
    """
    Daily: Send WhatsApp reminders for vehicles due for service.
    Source: PDF Section 4.1 daily tasks.
    """
    try:
        settings = frappe.get_single("Auto Dealer Settings")
        if not settings.whatsapp_enabled:
            return
        from auto_dealer.api.whatsapp import send_whatsapp_message

        # Find Service Job Cards with next_service_date within next 3 days
        from_date = today()
        to_date = add_days(today(), 3)

        due_services = frappe.db.sql("""
            SELECT name, vehicle, customer, mobile_no, next_service_date
            FROM `tabService Job Card`
            WHERE next_service_date BETWEEN %(from)s AND %(to)s
              AND docstatus = 1
              AND status != 'Cancelled'
        """, {"from": from_date, "to": to_date}, as_dict=True)

        for svc in due_services:
            mobile = svc.get("mobile_no") or frappe.db.get_value("Customer", svc.customer, "mobile_no")
            if not mobile:
                continue
            message = _(
                "Dear Customer, your vehicle {0} is due for service on {1}. "
                "Please schedule an appointment at {2}. Thank you!"
            ).format(
                svc.vehicle,
                svc.next_service_date,
                settings.dealership_name or "our service centre",
            )
            try:
                send_whatsapp_message(mobile_no=mobile, message=message)
            except Exception:
                frappe.log_error(
                    title=f"Service Reminder Failed: {svc.name}",
                    message=frappe.get_traceback()
                )

        frappe.logger("auto_dealer").info(
            f"[Daily] Service reminders sent for {len(due_services)} vehicles."
        )
    except Exception:
        frappe.log_error(title="send_service_reminders Failed", message=frappe.get_traceback())


def check_insurance_renewals():
    """
    Daily: Insurance policies expiring within 30 days trigger automated
    WhatsApp renewal reminders. Source: PDF Section 8.3.
    """
    try:
        settings = frappe.get_single("Auto Dealer Settings")
        cutoff = add_days(today(), 30)

        expiring = frappe.get_all(
            "Insurance Policy",
            filters={
                "status": "Active",
                "renewal_reminder_sent": 0,
                "end_date": ["<=", cutoff],
                "docstatus": 1,
            },
            fields=["name", "vehicle", "customer", "policy_number", "end_date", "insurance_company"],
        )

        reminded = 0
        for policy in expiring:
            try:
                mobile = frappe.db.get_value("Customer", policy.customer, "mobile_no")
                if not mobile:
                    continue

                # Fetch renewal quote from insurance API
                quote_text = "contact us for renewal quote"
                try:
                    from auto_dealer.api.insurance import get_renewal_quote
                    quote = get_renewal_quote(policy_number=policy.policy_number)
                    if quote and quote.get("premium"):
                        quote_text = f"₹{quote['premium']}"
                except Exception:
                    pass

                days_left = date_diff(policy.end_date, today())

                if settings.whatsapp_enabled:
                    from auto_dealer.api.whatsapp import send_whatsapp_message
                    # Template: insurance_renewal (PDF Section 11.1)
                    message = _(
                        "Dear Customer, your insurance policy {0} for vehicle {1} expires in {2} days on {3}. "
                        "Renewal premium: {4}. Contact {5} today to renew!"
                    ).format(
                        policy.policy_number,
                        policy.vehicle,
                        days_left,
                        policy.end_date,
                        quote_text,
                        settings.dealership_name or "us",
                    )
                    send_whatsapp_message(mobile_no=mobile, message=message)

                frappe.db.set_value("Insurance Policy", policy.name, "renewal_reminder_sent", 1)
                reminded += 1
            except Exception:
                frappe.log_error(
                    title=f"Insurance Renewal Reminder Failed: {policy.name}",
                    message=frappe.get_traceback()
                )

        frappe.db.commit()
        frappe.logger("auto_dealer").info(
            f"[Daily] Insurance renewal reminders: {reminded}/{len(expiring)} sent."
        )
    except Exception:
        frappe.log_error(title="check_insurance_renewals Failed", message=frappe.get_traceback())


def check_amc_renewals():
    """
    Daily: AMC contracts expiring — multi-stage reminders.
    Source: PDF Section 9.3.

    Schedule:
      30 days → WhatsApp
      15 days → WhatsApp + Email
       7 days → WhatsApp + Call task to Service Advisor
       0 days → Email to Dealer Admin
    """
    try:
        settings = frappe.get_single("Auto Dealer Settings")
        reminder_thresholds = [30, 15, 7, 0]

        for days in reminder_thresholds:
            target_date = add_days(today(), days)
            expiring = frappe.get_all(
                "AMC Contract",
                filters={
                    "end_date": target_date,
                    "status": "Active",
                    "docstatus": 1,
                },
                fields=["name", "vehicle", "customer", "end_date"],
            )
            for amc in expiring:
                _send_amc_reminder(amc, days, settings)

        frappe.logger("auto_dealer").info("[Daily] AMC renewal checks completed.")
    except Exception:
        frappe.log_error(title="check_amc_renewals Failed", message=frappe.get_traceback())


def _send_amc_reminder(amc, days_left: int, settings):
    """Send AMC reminder based on days_left threshold (PDF Section 9.3)."""
    try:
        mobile = frappe.db.get_value("Customer", amc.customer, "mobile_no")
        email = frappe.db.get_value("Customer", amc.customer, "email_id")

        if days_left == 0:
            # Expired alert → email to Dealer Admin
            admin_email = frappe.db.get_value("User", {"role_profile_name": "Dealer Admin"}, "email") or "admin@dealership.com"
            frappe.sendmail(
                recipients=[admin_email],
                subject=f"AMC Expired: {amc.name} — Vehicle {amc.vehicle}",
                message=f"AMC Contract {amc.name} for vehicle {amc.vehicle} has expired today.",
            )
        elif mobile and settings.whatsapp_enabled:
            from auto_dealer.api.whatsapp import send_whatsapp_message
            message = _(
                "Dear Customer, your Annual Maintenance Contract for vehicle {0} expires on {1} ({2} days). "
                "Contact {3} to renew."
            ).format(amc.vehicle, amc.end_date, days_left, settings.dealership_name or "us")
            send_whatsapp_message(mobile_no=mobile, message=message)

            if days_left == 15 and email:
                frappe.sendmail(
                    recipients=[email],
                    subject=f"AMC Renewal Reminder — {amc.vehicle}",
                    message=message,
                )
            elif days_left == 7:
                # Create call task for Service Advisor
                frappe.get_doc({
                    "doctype": "ToDo",
                    "description": f"Call customer re: AMC renewal for {amc.vehicle} ({amc.name}) expiring in 7 days.",
                    "reference_type": "AMC Contract",
                    "reference_name": amc.name,
                    "date": today(),
                    "priority": "High",
                }).insert(ignore_permissions=True)
    except Exception:
        frappe.log_error(
            title=f"AMC Reminder Failed: {amc.name}",
            message=frappe.get_traceback()
        )


# ─── Weekly Tasks ─────────────────────────────────────────────────────────────

def slow_moving_inventory_alert():
    """
    Weekly: Alert DMS Manager and Dealer Admin of slow-moving vehicles.
    Source: PDF Section 6.1 — Stock ageing > threshold (default 60 days) → weekly email.
    """
    try:
        settings = frappe.get_single("Auto Dealer Settings")
        threshold = settings.slow_moving_threshold_days or 60

        slow_movers = frappe.db.sql("""
            SELECT vin_number, make, model, variant, days_in_stock,
                   ex_showroom_price, status, branch
            FROM `tabVehicle`
            WHERE status NOT IN ('Sold', 'In Service')
              AND days_in_stock > %(threshold)s
              AND docstatus = 1
            ORDER BY days_in_stock DESC
        """, {"threshold": threshold}, as_dict=True)

        if not slow_movers:
            frappe.logger("auto_dealer").info("[Weekly] No slow-moving vehicles found.")
            return

        # Build email table
        rows = "".join(
            f"<tr><td>{v.vin_number}</td><td>{v.make} {v.model}</td>"
            f"<td>{v.variant or '-'}</td><td>{v.days_in_stock}</td>"
            f"<td>₹{v.ex_showroom_price:,.0f}</td><td>{v.status}</td></tr>"
            for v in slow_movers
        )
        body = f"""
        <h3>Slow Moving Inventory Alert — {today()}</h3>
        <p>The following {len(slow_movers)} vehicles have been in stock for more than {threshold} days:</p>
        <table border="1" cellpadding="5">
        <tr><th>VIN</th><th>Vehicle</th><th>Variant</th><th>Days in Stock</th><th>Price</th><th>Status</th></tr>
        {rows}
        </table>
        """

        recipients = _get_role_emails(["DMS Manager", "Dealer Admin"])
        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"Slow Moving Inventory Alert — {len(slow_movers)} vehicles ({today()})",
                message=body,
            )
        frappe.logger("auto_dealer").info(
            f"[Weekly] Slow moving alert: {len(slow_movers)} vehicles, emailed to {len(recipients)} recipients."
        )
    except Exception:
        frappe.log_error(title="slow_moving_inventory_alert Failed", message=frappe.get_traceback())


# ─── Monthly Tasks ────────────────────────────────────────────────────────────

def generate_oem_monthly_report():
    """
    Monthly: Generate OEM Monthly Sales Report.
    Source: PDF Section 12.2 — model/variant sold, units, revenue, finance %, insurance %.
    """
    try:
        import calendar
        from datetime import date

        today_date = getdate(today())
        # Previous month
        if today_date.month == 1:
            month = 12
            year = today_date.year - 1
        else:
            month = today_date.month - 1
            year = today_date.year

        last_day = calendar.monthrange(year, month)[1]
        from_date = f"{year}-{month:02d}-01"
        to_date = f"{year}-{month:02d}-{last_day}"

        # OEM Monthly Report columns: Model/Variant, Units Sold, Retail Revenue,
        # Finance Penetration %, Insurance Penetration %, Avg Discount
        report_data = frappe.db.sql("""
            SELECT
                vs.model,
                vs.variant,
                COUNT(*)                                    AS units_sold,
                SUM(vs.grand_total)                         AS retail_revenue,
                SUM(CASE WHEN vs.finance_type = 'Loan' THEN 1 ELSE 0 END) AS finance_count,
                COUNT(ip.name)                              AS insurance_count,
                AVG(vs.discount_amount)                     AS avg_discount
            FROM `tabVehicle Sale` vs
            LEFT JOIN `tabInsurance Policy` ip ON ip.vehicle_sale = vs.name AND ip.docstatus = 1
            WHERE vs.docstatus = 1
              AND vs.delivery_date BETWEEN %(from_date)s AND %(to_date)s
            GROUP BY vs.model, vs.variant
            ORDER BY units_sold DESC
        """, {"from_date": from_date, "to_date": to_date}, as_dict=True)

        if not report_data:
            frappe.logger("auto_dealer").info(f"[Monthly] No sales data for {month}/{year}.")
            return

        rows = "".join(
            f"<tr><td>{r.model}</td><td>{r.variant or '-'}</td><td>{r.units_sold}</td>"
            f"<td>₹{(r.retail_revenue or 0):,.0f}</td>"
            f"<td>{round((r.finance_count / r.units_sold) * 100, 1)}%</td>"
            f"<td>{round((r.insurance_count / r.units_sold) * 100, 1)}%</td>"
            f"<td>₹{(r.avg_discount or 0):,.0f}</td></tr>"
            for r in report_data
        )
        body = f"""
        <h3>OEM Monthly Sales Report — {calendar.month_name[month]} {year}</h3>
        <table border="1" cellpadding="5">
        <tr><th>Model</th><th>Variant</th><th>Units Sold</th><th>Retail Revenue</th>
            <th>Finance %</th><th>Insurance %</th><th>Avg Discount</th></tr>
        {rows}
        </table>
        """

        recipients = _get_role_emails(["Dealer Admin"])
        if recipients:
            frappe.sendmail(
                recipients=recipients,
                subject=f"OEM Monthly Sales Report — {calendar.month_name[month]} {year}",
                message=body,
            )
        frappe.logger("auto_dealer").info(f"[Monthly] OEM report for {month}/{year} emailed.")
    except Exception:
        frappe.log_error(title="generate_oem_monthly_report Failed", message=frappe.get_traceback())


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _get_role_emails(roles: list) -> list:
    """Fetch email addresses of users with any of the given roles."""
    emails = []
    for role in roles:
        users = frappe.db.sql("""
            SELECT u.email
            FROM `tabUser` u
            JOIN `tabHas Role` hr ON hr.parent = u.name
            WHERE hr.role = %(role)s AND u.enabled = 1 AND u.email != ''
        """, {"role": role}, as_dict=True)
        emails.extend([u.email for u in users if u.email])
    return list(set(emails))
