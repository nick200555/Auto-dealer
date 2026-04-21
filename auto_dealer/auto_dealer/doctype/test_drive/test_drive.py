"""
Test Drive DocType Controller
-------------------------------
Module path: auto_dealer.auto_dealer.auto_dealer.doctype.test_drive.test_drive
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, getdate


class TestDrive(Document):

	def validate(self):
		self.validate_vehicle_availability()
		self.validate_schedule()
		self.calculate_distance()

	def before_save(self):
		self.calculate_distance()

	def on_submit(self):
		self.mark_vehicle_on_test_drive()
		self.schedule_follow_up()

	def on_cancel(self):
		self.release_vehicle()

	def validate_vehicle_availability(self):
		vehicle_status = frappe.db.get_value("Vehicle", self.vehicle, "status")
		if vehicle_status not in ["Available", "Demo"]:
			frappe.throw(
				_("Vehicle {0} is not available for test drive. Status: {1}").format(self.vehicle, vehicle_status)
			)

	def validate_schedule(self):
		if getdate(self.test_drive_date) < getdate(today()):
			frappe.throw(_("Test Drive date cannot be in the past."))
		conflict = frappe.db.exists(
			"Test Drive",
			{"vehicle": self.vehicle, "test_drive_date": self.test_drive_date,
			 "status": ["not in", ["Cancelled", "No Show"]], "name": ["!=", self.name], "docstatus": ["!=", 2]},
		)
		if conflict:
			frappe.throw(
				_("Vehicle {0} already has a test drive scheduled on {1}.").format(self.vehicle, self.test_drive_date)
			)

	def calculate_distance(self):
		if self.odometer_start and self.odometer_end:
			if self.odometer_end < self.odometer_start:
				frappe.throw(_("Odometer End reading cannot be less than Start reading."))
			self.distance_covered = self.odometer_end - self.odometer_start

	def mark_vehicle_on_test_drive(self):
		vehicle = frappe.get_doc("Vehicle", self.vehicle)
		if vehicle.status == "Available":
			vehicle.status = "Demo"
			vehicle.save(ignore_permissions=True)

	def release_vehicle(self):
		vehicle = frappe.get_doc("Vehicle", self.vehicle)
		if vehicle.status == "Demo":
			vehicle.status = "Available"
			vehicle.save(ignore_permissions=True)

	def schedule_follow_up(self):
		if self.follow_up_date:
			frappe.get_doc({
				"doctype": "ToDo",
				"owner": self.sales_executive,
				"date": self.follow_up_date,
				"description": _("Follow up with {0} re: test drive of {1} on {2}. Rating: {3}/5").format(
					self.customer_name or self.customer, self.vehicle, self.test_drive_date, self.rating or "N/A"
				),
				"reference_type": "Test Drive",
				"reference_name": self.name,
				"priority": "Medium",
			}).insert(ignore_permissions=True)


# ── Standalone event handlers ─────────────────────────────────────────────────

def before_save(doc, method=None):
	doc.calculate_distance()


def on_submit(doc, method=None):
	doc.mark_vehicle_on_test_drive()
	doc.schedule_follow_up()
