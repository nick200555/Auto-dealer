"""
Monthly Scheduled Tasks
------------------------
Executed once per month by the Frappe scheduler.
Tasks:
  1. calculate_incentives        — Auto-populate Target vs Achievement and compute incentives
  2. rollover_targets           — Create next month's target records for each executive
  3. generate_oem_monthly_report — Generate OEM Monthly Sales Report
"""

import frappe
from frappe.utils import today, getdate
from datetime import date


MONTH_NAMES = [
	"", "January", "February", "March", "April", "May", "June",
	"July", "August", "September", "October", "November", "December",
]


def calculate_incentives():
	"""
	For the current month that just ended, trigger recalculation in all
	Target vs Achievement records.
	"""
	today_date = getdate(today())
	# Run on the 1st of each month for the previous month
	prev_month = today_date.month - 1 or 12
	prev_year = today_date.year if today_date.month > 1 else today_date.year - 1

	records = frappe.get_all(
		"Target vs Achievement",
		filters={
			"month": MONTH_NAMES[prev_month],
			"year": prev_year,
			"status": "Draft",
			"docstatus": 0,
		},
		fields=["name"],
	)

	updated = 0
	for rec in records:
		try:
			doc = frappe.get_doc("Target vs Achievement", rec["name"])
			doc.fetch_actual_achievement()
			doc.calculate_achievement_percentages()
			doc.calculate_incentive()
			doc.save(ignore_permissions=True)
			updated += 1
		except Exception:
			frappe.log_error(
				title=f"Incentive Calculation Failed: {rec['name']}",
				message=frappe.get_traceback(),
			)

	frappe.db.commit()
	frappe.logger("auto_dealer").info(
		f"[Monthly Task] Incentives calculated for {updated} records."
	)


def rollover_targets():
	"""
	On the 1st of each month, create new Target vs Achievement records
	for the current month by copying targets from the previous month.
	"""
	today_date = getdate(today())
	current_month = MONTH_NAMES[today_date.month]
	current_year = today_date.year

	prev_month = today_date.month - 1 or 12
	prev_year = today_date.year if today_date.month > 1 else today_date.year - 1

	prev_records = frappe.get_all(
		"Target vs Achievement",
		filters={"month": MONTH_NAMES[prev_month], "year": prev_year},
		fields=["name", "sales_executive", "branch", "vehicle_target", "revenue_target",
		        "insurance_target", "finance_target"],
	)

	created = 0
	for rec in prev_records:
		# Skip if already exists for current month
		exists = frappe.db.exists(
			"Target vs Achievement",
			{"sales_executive": rec["sales_executive"], "month": current_month, "year": current_year},
		)
		if exists:
			continue

		try:
			new_doc = frappe.get_doc({
				"doctype": "Target vs Achievement",
				"sales_executive": rec["sales_executive"],
				"month": current_month,
				"year": current_year,
				"branch": rec["branch"],
				"vehicle_target": rec["vehicle_target"],
				"revenue_target": rec["revenue_target"],
				"insurance_target": rec["insurance_target"],
				"finance_target": rec["finance_target"],
			})
			new_doc.insert(ignore_permissions=True)
			created += 1
		except Exception:
			frappe.log_error(
				title=f"Target Rollover Failed for {rec['sales_executive']}",
				message=frappe.get_traceback(),
			)

	frappe.db.commit()
	frappe.logger("auto_dealer").info(
		f"[Monthly Task] Target rollover: {created} records created for {current_month} {current_year}."
	)


def generate_oem_monthly_report():
    """
    Monthly: Generate OEM Monthly Sales Report.
    Source: PDF Section 12.2 — model/variant sold, units, revenue, finance %, insurance %.
    """
    try:
        import calendar

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
            f"<td>{round((r.finance_count / r.units_sold) * 100, 1) if r.units_sold > 0 else 0}%</td>"
            f"<td>{round((r.insurance_count / r.units_sold) * 100, 1) if r.units_sold > 0 else 0}%</td>"
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


def _get_role_emails(roles) -> list:
    """Fetch email addresses of users with any of the given roles."""
    if isinstance(roles, str):
        roles = [roles]
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
