"""
OEM Target DocType Controller
--------------------------------
Module path: auto_dealer.auto_dealer.auto_dealer.doctype.oem_target.oem_target

Tracks OEM-allocated targets vs actual sales achievement:
  - Pulls real data from Vehicle Sale for the month/executive
  - Calculates achievement percentages across all KPIs
  - Applies tiered incentive slabs
  - Supports OEM-model level allocation tracking
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint
import calendar


MONTH_MAP = {
	"January": 1, "February": 2, "March": 3, "April": 4,
	"May": 5, "June": 6, "July": 7, "August": 8,
	"September": 9, "October": 10, "November": 11, "December": 12,
}

# Incentive slabs: (min_achievement_%, incentive_% of revenue_achieved)
INCENTIVE_SLABS = [
	(100, 0.05),
	(90,  0.03),
	(75,  0.015),
	(50,  0.005),
]


class OEMTarget(Document):

	def validate(self):
		self.fetch_actual_achievement()
		self.calculate_achievement_percentages()
		self.calculate_incentive()

	def before_save(self):
		self.fetch_actual_achievement()
		self.calculate_achievement_percentages()
		self.calculate_incentive()

	def on_submit(self):
		frappe.msgprint(
			_("OEM Target confirmed. Overall Achievement: {0}% | Incentive: ₹{1}").format(
				self.overall_achievement_pct, self.incentive_amount
			),
			alert=True, indicator="blue",
		)

	# ── Data Fetching ─────────────────────────────────────────────────────────

	def fetch_actual_achievement(self):
		"""Pull actuals from Vehicle Sale (submitted) for this month/executive."""
		month_no = MONTH_MAP.get(self.month, 1)
		year = cint(self.year)
		last_day = calendar.monthrange(year, month_no)[1]
		from_date = f"{year}-{month_no:02d}-01"
		to_date = f"{year}-{month_no:02d}-{last_day}"

		sales_data = frappe.db.sql(
			"""
			SELECT COUNT(*) AS units,
			       COALESCE(SUM(total_amount), 0) AS revenue,
			       SUM(CASE WHEN finance_type = 'Loan' THEN 1 ELSE 0 END) AS finance_cases
			FROM `tabVehicle Sale`
			WHERE sales_executive = %(executive)s
			  AND sale_date BETWEEN %(from_date)s AND %(to_date)s
			  AND docstatus = 1
			""",
			{"executive": self.sales_executive, "from_date": from_date, "to_date": to_date},
			as_dict=True,
		)
		if sales_data:
			row = sales_data[0]
			self.vehicle_achieved = cint(row.get("units") or 0)
			self.revenue_achieved = flt(row.get("revenue") or 0)
			self.finance_achieved = cint(row.get("finance_cases") or 0)

		# Count insurance policies for this executive this month
		ins_count = frappe.db.sql(
			"""
			SELECT COUNT(*) AS cnt
			FROM `tabInsurance Policy` ip
			JOIN `tabVehicle Sale` vs ON vs.name = ip.vehicle_sale
			WHERE vs.sales_executive = %(executive)s
			  AND ip.start_date BETWEEN %(from_date)s AND %(to_date)s
			  AND ip.docstatus = 1
			""",
			{"executive": self.sales_executive, "from_date": from_date, "to_date": to_date},
			as_dict=True,
		)
		if ins_count:
			self.insurance_achieved = cint(ins_count[0].get("cnt") or 0)

	# ── Calculations ──────────────────────────────────────────────────────────

	def calculate_achievement_percentages(self):
		if cint(self.vehicle_target) > 0:
			self.vehicle_achievement_pct = round(cint(self.vehicle_achieved) / cint(self.vehicle_target) * 100, 2)
		else:
			self.vehicle_achievement_pct = 0

		if flt(self.revenue_target) > 0:
			self.revenue_achievement_pct = round(flt(self.revenue_achieved) / flt(self.revenue_target) * 100, 2)
		else:
			self.revenue_achievement_pct = 0

		# Overall = average of vehicle % and revenue %
		self.overall_achievement_pct = round(
			(flt(self.vehicle_achievement_pct) + flt(self.revenue_achievement_pct)) / 2, 2
		)

	def calculate_incentive(self):
		"""Apply tiered slab on overall_achievement_pct."""
		overall = flt(self.overall_achievement_pct)
		incentive_pct = 0.0
		for threshold, pct in INCENTIVE_SLABS:
			if overall >= threshold:
				incentive_pct = pct
				break
		self.incentive_amount = round(flt(self.revenue_achieved) * incentive_pct, 2)


# ── Standalone event handlers (wired via hooks.py doc_events) ─────────────────

def before_save(doc, method=None):
	doc.fetch_actual_achievement()
	doc.calculate_achievement_percentages()
	doc.calculate_incentive()


def on_submit(doc, method=None):
	pass
