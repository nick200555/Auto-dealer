"""
Utility Functions
------------------
Shared helpers used across the auto_dealer app.
Also registered as Jinja filters in hooks.py.
"""

import frappe


def format_vin(vin: str) -> str:
	"""Format VIN in groups for readability: XXXX-XXXXX-XXXXXXXX."""
	if not vin or len(vin) != 17:
		return vin or ""
	return f"{vin[:4]}-{vin[4:9]}-{vin[9:]}"


def format_emi_amount(amount: float) -> str:
	"""Format a currency amount as Indian Rupee string: ₹1,23,456.78"""
	try:
		return f"₹{amount:,.2f}"
	except (TypeError, ValueError):
		return f"₹{amount}"


def get_vehicle_age_category(days_in_stock: int) -> str:
	"""
	Categorize a vehicle by how long it has been in stock.
	Returns: 'Fresh' | 'Ageing' | 'Slow Moving' | 'Critical'
	"""
	if days_in_stock <= 30:
		return "Fresh"
	elif days_in_stock <= 60:
		return "Ageing"
	elif days_in_stock <= 90:
		return "Slow Moving"
	else:
		return "Critical"


def get_dashboard_kpis() -> dict:
	"""
	Return key KPI metrics for the dashboard.
	Used by the Frappe Number Card or custom dashboard.
	"""
	total_vehicles = frappe.db.count("Vehicle", {"docstatus": 1, "status": ["not in", ["Sold", "Scrap"]]})
	total_available = frappe.db.count("Vehicle", {"docstatus": 1, "status": "Available"})
	total_booked = frappe.db.count("Vehicle", {"docstatus": 1, "status": "Booked"})
	total_sold_this_month = _count_sold_this_month()
	pending_emi = frappe.db.count("EMI Schedule", {"status": ["in", ["Pending", "Overdue"]]})
	expiring_insurance = _count_expiring_insurance()

	return {
		"total_inventory": total_vehicles,
		"available": total_available,
		"booked": total_booked,
		"sold_this_month": total_sold_this_month,
		"pending_emi_count": pending_emi,
		"expiring_insurance_30d": expiring_insurance,
	}


def _count_sold_this_month() -> int:
	from frappe.utils import getdate, today
	from datetime import date

	t = getdate(today())
	from_date = date(t.year, t.month, 1).strftime("%Y-%m-%d")
	return frappe.db.count(
		"Vehicle Sale",
		{"docstatus": 1, "sale_date": [">=", from_date], "status": "Delivered"},
	)


def _count_expiring_insurance() -> int:
	from frappe.utils import add_days, today
	cutoff = add_days(today(), 30)
	return frappe.db.count(
		"Vehicle Insurance",
		{"status": "Active", "end_date": ["<=", cutoff], "docstatus": 1},
	)


@frappe.whitelist()
def get_kpis() -> dict:
	"""Whitelisted: fetch dashboard KPIs from the client."""
	return get_dashboard_kpis()
