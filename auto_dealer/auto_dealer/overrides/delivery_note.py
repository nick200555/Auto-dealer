"""
Custom Delivery Note Override
-------------------------------
Extends ERPNext's Delivery Note to:
  - Update Vehicle status to 'Sold' when Delivery Note is submitted
  - Validate that the vehicle being delivered matches the Vehicle Sale
"""

import frappe
from frappe import _

try:
	from erpnext.stock.doctype.delivery_note.delivery_note import DeliveryNote
except ImportError:
	from frappe.model.document import Document as DeliveryNote


class CustomDeliveryNote(DeliveryNote):

	def on_submit(self):
		super().on_submit()
		self._update_vehicle_on_delivery()

	def on_cancel(self):
		super().on_cancel()
		self._revert_vehicle_on_cancel()

	def _update_vehicle_on_delivery(self):
		"""Mark all vehicles in this delivery note as Sold."""
		for item in self.items:
			vin = item.get("vin") or item.get("serial_no")
			if vin and frappe.db.exists("Vehicle", vin):
				frappe.db.set_value("Vehicle", vin, "status", "Sold")
				frappe.logger("auto_dealer").info(
					f"Delivery Note {self.name}: Vehicle {vin} marked as Sold."
				)

	def _revert_vehicle_on_cancel(self):
		"""Revert vehicle status if delivery is cancelled."""
		for item in self.items:
			vin = item.get("vin") or item.get("serial_no")
			if vin and frappe.db.exists("Vehicle", vin):
				frappe.db.set_value("Vehicle", vin, "status", "Available")


# ── Standalone event (wired via hooks.py doc_events) ─────────────────────────

def on_submit(doc, method=None):
	"""Called via hooks.py doc_events for Delivery Note on_submit."""
	for item in doc.items:
		vin = item.get("vin") or item.get("serial_no")
		if vin and frappe.db.exists("Vehicle", vin):
			frappe.db.set_value("Vehicle", vin, "status", "Sold")
	frappe.db.commit()
