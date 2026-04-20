"""
Weekly Scheduled Tasks
-----------------------
Executed once per week by the Frappe scheduler.
Tasks:
  1. slow_moving_inventory_report — Flag vehicles in stock > 60 days
  2. oem_stock_report             — Generate OEM reconciliation report
"""

import frappe
from frappe.utils import today, date_diff


SLOW_MOVING_THRESHOLD_DAYS = 60


def slow_moving_inventory_report():
	"""
	Identify and report vehicles that have been in stock for more than 60 days.
	Creates a frappe.log_error / notification for Sales Manager.
	"""
	slow_vehicles = frappe.get_all(
		"Vehicle",
		filters={
			"status": "Available",
			"days_in_stock": [">", SLOW_MOVING_THRESHOLD_DAYS],
			"docstatus": 1,
		},
		fields=["name", "vin", "make", "model", "variant", "days_in_stock", "branch", "ex_showroom_price"],
		order_by="days_in_stock desc",
	)

	if not slow_vehicles:
		frappe.logger("auto_dealer").info("[Weekly Task] No slow-moving vehicles found.")
		return

	report_lines = [
		f"⚠️ Slow-Moving Inventory Report ({today()}) — {len(slow_vehicles)} vehicles over {SLOW_MOVING_THRESHOLD_DAYS} days:"
	]
	for v in slow_vehicles:
		report_lines.append(
			f"  • {v['vin']} | {v['make']} {v['model']} {v.get('variant', '')} | "
			f"{v['days_in_stock']} days | Branch: {v['branch']} | ₹{v['ex_showroom_price']:,.0f}"
		)

	report_text = "\n".join(report_lines)

	# Send in-app notification to Sales Manager role
	frappe.sendmail(
		recipients=_get_role_emails("Sales Manager"),
		subject=f"[Auto Dealer] Slow-Moving Inventory Report — {today()}",
		message=report_text.replace("\n", "<br>"),
		now=False,
	)

	frappe.logger("auto_dealer").info(
		f"[Weekly Task] Slow-moving report: {len(slow_vehicles)} vehicles flagged."
	)


def oem_stock_report():
	"""
	Generate OEM stock reconciliation: lists all inventory by make/model/variant
	with quantities and average days in stock.
	Emails report to Dealer Principal role.
	"""
	stock_summary = frappe.db.sql(
		"""
		SELECT make, model, variant,
		       COUNT(*) AS units,
		       AVG(days_in_stock) AS avg_days,
		       MIN(days_in_stock) AS min_days,
		       MAX(days_in_stock) AS max_days,
		       SUM(ex_showroom_price) AS total_value
		FROM `tabVehicle`
		WHERE status NOT IN ('Sold', 'Scrap') AND docstatus = 1
		GROUP BY make, model, variant
		ORDER BY make, model, variant
		""",
		as_dict=True,
	)

	if not stock_summary:
		frappe.logger("auto_dealer").info("[Weekly Task] OEM stock report: No inventory found.")
		return

	rows = []
	for row in stock_summary:
		rows.append(
			f"  {row['make']} {row['model']} {row.get('variant', '')} | "
			f"Units: {row['units']} | Avg Days: {row['avg_days']:.0f} | "
			f"Value: ₹{row['total_value']:,.0f}"
		)

	report_text = f"OEM Stock Reconciliation Report — {today()}\n\n" + "\n".join(rows)

	frappe.sendmail(
		recipients=_get_role_emails("Dealer Principal"),
		subject=f"[Auto Dealer] OEM Stock Reconciliation — {today()}",
		message=report_text.replace("\n", "<br>"),
		now=False,
	)

	frappe.logger("auto_dealer").info("[Weekly Task] OEM stock report sent.")


def _get_role_emails(role: str) -> list:
	"""Fetch email addresses of all users with a given role."""
	users = frappe.get_all(
		"Has Role",
		filters={"role": role, "parenttype": "User"},
		fields=["parent"],
	)
	emails = []
	for u in users:
		email = frappe.db.get_value("User", u["parent"], "email")
		if email and email != "Administrator":
			emails.append(email)
	return emails or ["admin@example.com"]
