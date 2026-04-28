"""
Service Job Card DocType Controller
--------------------------------------
Module path: auto_dealer.auto_dealer.doctype.service_job_card.service_job_card
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

GST_RATE = 0.18


class ServiceJobCard(Document):

	def validate(self):
		self.calculate_totals()

	def before_save(self):
		self.calculate_totals()

	def on_submit(self):
		self.update_vehicle_odometer()
		self.notify_customer_vehicle_ready()
		self.schedule_next_service_reminder()

	def calculate_totals(self):
		parts_total = sum(flt(row.amount) for row in (self.service_items or []))
		labour_total = sum(flt(row.amount) for row in (self.labour_items or []))
		sub_total = parts_total + labour_total
		tax = sub_total * GST_RATE
		self.parts_total = parts_total
		self.labour_total = labour_total
		self.tax_amount = round(tax, 2)
		self.grand_total = round(sub_total + tax, 2)

	def update_vehicle_odometer(self):
		if self.odometer_at_service:
			vehicle = frappe.get_doc("Vehicle", self.vehicle)
			if flt(self.odometer_at_service) >= flt(vehicle.odometer_reading):
				vehicle.odometer_reading = self.odometer_at_service
				vehicle.save(ignore_permissions=True)

	def notify_customer_vehicle_ready(self):
		if self.status == "Completed" and self.mobile_no:
			try:
				from auto_dealer.api.whatsapp import send_whatsapp_message
				message = _(
					"Dear {0}, your vehicle (VIN: {1}) is ready for pickup. "
					"Total: ₹{2}. Thank you!"
				).format(self.customer_name or self.customer, self.vehicle, self.grand_total)
				send_whatsapp_message(mobile_no=self.mobile_no, message=message)
			except Exception:
				frappe.log_error(title="WhatsApp Service Ready Failed", message=frappe.get_traceback())

	def schedule_next_service_reminder(self):
		if self.next_service_date:
			frappe.get_doc({
				"doctype": "ToDo",
				"owner": self.service_advisor,
				"date": self.next_service_date,
				"description": _("Next service due for {0} (Customer: {1}). Next at {2} km.").format(
					self.vehicle, self.customer_name or self.customer, self.next_service_km or "N/A"
				),
				"reference_type": "Service Job Card",
				"reference_name": self.name,
				"priority": "Medium",
			}).insert(ignore_permissions=True)


# ── Standalone event handlers ─────────────────────────────────────────────────

def before_save(doc, method=None):
	doc.calculate_totals()


def on_submit(doc, method=None):
	doc.update_vehicle_odometer()
	doc.notify_customer_vehicle_ready()
	doc.schedule_next_service_reminder()
