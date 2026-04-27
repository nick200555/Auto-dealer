"""
OEM Stock Report — Script Report
-----------------------------------
Summarizes vehicle inventory grouped by Make / Model / Variant.
Useful for OEM reconciliation and stock reporting.

Columns: Make, Model, Variant, Count, Avg Days in Stock, Total Value
"""

import frappe
from frappe import _


def execute(filters=None):
	columns = get_columns()
	data = get_data()
	return columns, data


def get_columns():
	return [
		{"label": _("Make"), "fieldname": "make", "fieldtype": "Data", "width": 120},
		{"label": _("Model"), "fieldname": "model", "fieldtype": "Data", "width": 140},
		{"label": _("Variant"), "fieldname": "variant", "fieldtype": "Data", "width": 120},
		{"label": _("Units in Stock"), "fieldname": "units", "fieldtype": "Int", "width": 120},
		{"label": _("Avg Days in Stock"), "fieldname": "avg_days", "fieldtype": "Float", "width": 150, "precision": 1},
		{"label": _("Min Days"), "fieldname": "min_days", "fieldtype": "Int", "width": 100},
		{"label": _("Max Days"), "fieldname": "max_days", "fieldtype": "Int", "width": 100},
		{"label": _("Total Stock Value (₹)"), "fieldname": "total_value", "fieldtype": "Currency", "width": 180},
	]


def get_data() -> list:
	return frappe.db.sql(
		"""
		SELECT make, model, COALESCE(variant, '') AS variant,
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
