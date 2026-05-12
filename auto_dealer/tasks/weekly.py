"""
Weekly Scheduled Tasks
-----------------------
Executed once per week by the Frappe scheduler.
Tasks:
  1. slow_moving_inventory_alert — Flag vehicles in stock > 60 days
  2. oem_stock_report             — Generate OEM reconciliation report
"""

import frappe
from frappe.utils import today, date_diff


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
		recipients=_get_role_emails(["Dealer Principal"]),
		subject=f"[Auto Dealer] OEM Stock Reconciliation — {today()}",
		message=report_text.replace("\n", "<br>"),
		now=False,
	)

	frappe.logger("auto_dealer").info("[Weekly Task] OEM stock report sent.")


def _get_role_emails(roles) -> list:
	"""Fetch email addresses of all users with given roles."""
	if isinstance(roles, str):
		roles = [roles]
	
	emails = []
	for role in roles:
		users = frappe.get_all(
			"Has Role",
			filters={"role": role, "parenttype": "User"},
			fields=["parent"],
		)
		for u in users:
			email = frappe.db.get_value("User", u["parent"], "email")
			if email and email != "Administrator":
				emails.append(email)
	return list(set(emails)) or ["admin@example.com"]
