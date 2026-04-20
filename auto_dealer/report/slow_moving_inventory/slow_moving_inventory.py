"""
Slow Moving Inventory — Script Report
---------------------------------------
Shows all vehicles in stock beyond a configurable threshold (default 60 days).
Columns: VIN, Make, Model, Variant, Branch, Purchase Date, Days in Stock, Ex-Showroom Price, Status
"""

import frappe
from frappe import _


def execute(filters=None):
	filters = filters or {}
	threshold = int(filters.get("days_threshold") or 60)

	columns = get_columns()
	data = get_data(threshold)
	return columns, data


def get_columns():
	return [
		{"label": _("VIN"), "fieldname": "vin", "fieldtype": "Link", "options": "Vehicle", "width": 180},
		{"label": _("Make"), "fieldname": "make", "fieldtype": "Data", "width": 100},
		{"label": _("Model"), "fieldname": "model", "fieldtype": "Data", "width": 120},
		{"label": _("Variant"), "fieldname": "variant", "fieldtype": "Data", "width": 100},
		{"label": _("Branch"), "fieldname": "branch", "fieldtype": "Link", "options": "Branch", "width": 120},
		{"label": _("Purchase Date"), "fieldname": "purchase_date", "fieldtype": "Date", "width": 110},
		{"label": _("Days in Stock"), "fieldname": "days_in_stock", "fieldtype": "Int", "width": 120},
		{"label": _("Ex-Showroom Price"), "fieldname": "ex_showroom_price", "fieldtype": "Currency", "width": 150},
		{"label": _("Status"), "fieldname": "status", "fieldtype": "Data", "width": 100},
	]


def get_data(threshold: int) -> list:
	return frappe.db.sql(
		"""
		SELECT vin, make, model, variant, branch, purchase_date,
		       days_in_stock, ex_showroom_price, status
		FROM `tabVehicle`
		WHERE status NOT IN ('Sold', 'Scrap')
		  AND days_in_stock > %(threshold)s
		  AND docstatus = 1
		ORDER BY days_in_stock DESC
		""",
		{"threshold": threshold},
		as_dict=True,
	)
