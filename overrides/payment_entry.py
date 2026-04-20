"""
Custom Payment Entry Override
-------------------------------
Extends ERPNext Payment Entry to:
  - Update EMI Schedule 'Paid' status when a matched payment is received
"""

import frappe
from frappe import _
from frappe.utils import flt

try:
	from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
except ImportError:
	from frappe.model.document import Document as PaymentEntry


class CustomPaymentEntry(PaymentEntry):

	def on_submit(self):
		super().on_submit()
		self._update_emi_schedule()

	def _update_emi_schedule(self):
		"""
		If this payment matches an EMI Schedule instalment, update its paid status.
		Expects a custom field 'emi_schedule' on Payment Entry (set via custom field fixture).
		"""
		emi_name = self.get("emi_schedule")
		if not emi_name or not frappe.db.exists("EMI Schedule", emi_name):
			return

		emi = frappe.get_doc("EMI Schedule", emi_name)
		emi.paid_amount = flt(emi.paid_amount) + flt(self.paid_amount)
		emi.payment_date = self.posting_date
		emi.payment_reference = self.name
		emi.save(ignore_permissions=True)

		frappe.logger("auto_dealer").info(
			f"Payment Entry {self.name} applied to EMI {emi_name}."
		)


# ── Standalone event (wired via hooks.py) ─────────────────────────────────────

def on_submit(doc, method=None):
	emi_name = doc.get("emi_schedule")
	if emi_name and frappe.db.exists("EMI Schedule", emi_name):
		emi = frappe.get_doc("EMI Schedule", emi_name)
		emi.paid_amount = flt(emi.paid_amount) + flt(doc.paid_amount)
		emi.payment_date = doc.posting_date
		emi.payment_reference = doc.name
		emi.save(ignore_permissions=True)
		frappe.db.commit()
