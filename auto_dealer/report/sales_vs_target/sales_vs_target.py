"""
Sales vs Target Report — Script Report
----------------------------------------
Shows each sales executive's target vs achievement for the selected month/year.
"""

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	return [
		{"label": _("Sales Executive"), "fieldname": "sales_executive", "fieldtype": "Link", "options": "User", "width": 180},
		{"label": _("Month"), "fieldname": "month", "fieldtype": "Data", "width": 100},
		{"label": _("Year"), "fieldname": "year", "fieldtype": "Int", "width": 80},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 120},
		{"label": _("Vehicle Target"), "fieldname": "vehicle_target", "fieldtype": "Int", "width": 120},
		{"label": _("Vehicle Achieved"), "fieldname": "vehicle_achieved", "fieldtype": "Int", "width": 130},
		{"label": _("Vehicle %"), "fieldname": "vehicle_achievement_pct", "fieldtype": "Percent", "width": 100},
		{"label": _("Revenue Target (₹)"), "fieldname": "revenue_target", "fieldtype": "Currency", "width": 150},
		{"label": _("Revenue Achieved (₹)"), "fieldname": "revenue_achieved", "fieldtype": "Currency", "width": 160},
		{"label": _("Revenue %"), "fieldname": "revenue_achievement_pct", "fieldtype": "Percent", "width": 100},
		{"label": _("Incentive (₹)"), "fieldname": "incentive_amount", "fieldtype": "Currency", "width": 130},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 90},
	]


def get_data(filters: dict) -> list:
	conditions = {}
	if filters.get("month"):
		conditions["month"] = filters["month"]
	if filters.get("year"):
		conditions["year"] = filters["year"]
	if filters.get("sales_executive"):
		conditions["sales_executive"] = filters["sales_executive"]
	if filters.get("branch"):
		conditions["branch"] = filters["branch"]

	return frappe.get_all(
		"Target vs Achievement",
		filters=conditions,
		fields=[
			"sales_executive", "month", "year", "branch",
			"vehicle_target", "vehicle_achieved", "vehicle_achievement_pct",
			"revenue_target", "revenue_achieved", "revenue_achievement_pct",
			"incentive_amount", "status",
		],
		order_by="year desc, month asc, sales_executive asc",
	)
