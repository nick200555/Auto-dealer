"""
Daily Scheduled Tasks
----------------------
Wired from hooks.py scheduler_events → auto_dealer.tasks.daily.*

Tasks:
  1. update_days_in_stock     — Refresh days_in_stock for all active vehicles
  2. check_insurance_renewals — Notify expiring Insurance Policies (≤ 30 days)
  3. sync_marketplace_inventory — Push inventory to CarDekho
  4. send_emi_reminders       — WhatsApp reminders for EMI due in next 3 days
  5. send_service_reminders   — WhatsApp reminders for vehicles due for service
  6. check_amc_renewals       — Multi-stage AMC renewal reminders
"""

import frappe
from frappe import _
from frappe.utils import today, date_diff, add_days, getdate


def update_days_in_stock():
	"""Recalculate days_in_stock for every non-Sold/Scrap vehicle."""
	vehicles = frappe.get_all(
		"Vehicle",
		filters={"status": ["not in", ["Sold", "Scrap"]], "docstatus": 1},
		fields=["name", "purchase_date"],
	)
	updated = 0
	for v in vehicles:
		if v.get("purchase_date"):
			days = date_diff(today(), v["purchase_date"])
			frappe.db.set_value("Vehicle", v["name"], "days_in_stock", days, update_modified=False)
			updated += 1
	frappe.db.commit()
	frappe.logger("auto_dealer").info(f"[Daily] Updated days_in_stock for {updated} vehicles.")


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


def sync_marketplace_inventory():
	"""Push all Available vehicles to CarDekho marketplace."""
	try:
		from auto_dealer.api.marketplace_sync import sync_all_inventory
		result = sync_all_inventory()
		frappe.logger("auto_dealer").info(f"[Daily] Marketplace sync: {result}")
	except Exception:
		frappe.log_error(title="sync_marketplace_inventory Failed", message=frappe.get_traceback())


def send_emi_reminders():
	"""WhatsApp reminders for EMI instalments due within 3 days or overdue."""
	due_cutoff = add_days(today(), 3)
	due_instalments = frappe.get_all(
		"EMI Schedule",
		filters={"status": ["in", ["Pending", "Partial", "Overdue"]], "due_date": ["<=", due_cutoff]},
		fields=["name"],
	)
	reminded = 0
	for rec in due_instalments:
		try:
			doc = frappe.get_doc("EMI Schedule", rec["name"])
			doc.send_due_reminder()
			reminded += 1
		except Exception:
			frappe.log_error(title=f"EMI Reminder Failed: {rec['name']}", message=frappe.get_traceback())
	frappe.logger("auto_dealer").info(f"[Daily] EMI reminders sent: {reminded}/{len(due_instalments)}")


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
