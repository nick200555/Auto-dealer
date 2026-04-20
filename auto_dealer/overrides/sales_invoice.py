"""
Custom Sales Invoice Override
-------------------------------
Extends ERPNext Sales Invoice to:
  - Log vehicle sale revenue for KPI dashboard
  - Trigger post-sale notifications
"""

import frappe
from frappe import _

try:
	from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
except ImportError:
	from frappe.model.document import Document as SalesInvoice


class CustomSalesInvoice(SalesInvoice):

	def on_submit(self):
		super().on_submit()
		self._log_vehicle_revenue()

	def _log_vehicle_revenue(self):
		"""Log revenue for reporting purposes."""
		frappe.logger("auto_dealer").info(
			f"Sales Invoice {self.name}: Revenue ₹{self.grand_total} logged for {self.customer}."
		)


# ── Standalone events (wired via hooks.py) ────────────────────────────────────

def on_submit(doc, method=None):
	frappe.logger("auto_dealer").info(
		f"Sales Invoice submitted: {doc.name} | Customer: {doc.customer} | Amount: {doc.grand_total}"
	)


def on_cancel(doc, method=None):
	frappe.logger("auto_dealer").info(
		f"Sales Invoice cancelled: {doc.name}"
	)
