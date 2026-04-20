"""
Monthly Scheduled Tasks
------------------------
Executed once per month by the Frappe scheduler.
Tasks:
  1. calculate_incentives  — Auto-populate Target vs Achievement and compute incentives
  2. rollover_targets      — Create next month's target records for each executive
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
