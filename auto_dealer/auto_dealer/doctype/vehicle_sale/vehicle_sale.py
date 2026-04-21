"""
Vehicle Sale DocType Controller
--------------------------------
Module path: auto_dealer.auto_dealer.auto_dealer.doctype.vehicle_sale.vehicle_sale
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, flt, cint
import math


class VehicleSale(Document):

	def validate(self):
		self.validate_vehicle_status()
		self.calculate_total_amount()
		self.calculate_emi()

	def before_save(self):
		self.calculate_total_amount()
		self.calculate_emi()

	def on_submit(self):
		self.update_vehicle_status("Sold")
		self.create_loan_application()
		self.trigger_whatsapp_confirmation()
		self.link_insurance_policy()

	def on_cancel(self):
		self.update_vehicle_status("Available")

	# ── Validation ────────────────────────────────────────────────────────────

	def validate_vehicle_status(self):
		status = frappe.db.get_value("Vehicle", self.vehicle, "status")
		if status not in ["Available", "Booked"]:
			frappe.throw(
				_("Vehicle {0} is not available for sale. Current status: {1}").format(self.vehicle, status)
			)

	# ── Calculations ──────────────────────────────────────────────────────────

	def calculate_total_amount(self):
		self.total_amount = flt(self.agreed_price) - flt(self.discount_amount) + flt(self.accessories_amount)

	def calculate_emi(self):
		"""EMI using PMT formula: P·r·(1+r)^n / ((1+r)^n - 1)"""
		if self.finance_type != "Loan":
			self.emi_amount = 0
			return
		P = flt(self.loan_amount)
		n = cint(self.tenure_months)
		annual_rate = flt(self.interest_rate)
		if not P or not n or not annual_rate:
			self.emi_amount = 0
			return
		r = annual_rate / 12 / 100
		try:
			emi = P * r * math.pow(1 + r, n) / (math.pow(1 + r, n) - 1)
			self.emi_amount = round(emi, 2)
		except ZeroDivisionError:
			self.emi_amount = round(P / n, 2)

	# ── Business Logic ────────────────────────────────────────────────────────

	def update_vehicle_status(self, status: str):
		if self.vehicle:
			frappe.db.set_value("Vehicle", self.vehicle, "status", status)
			frappe.db.commit()

	def create_loan_application(self):
		"""Auto-create a Loan Application record if finance type is Loan."""
		if self.finance_type != "Loan" or not self.loan_amount:
			return
		if frappe.db.exists("Loan Application", {"vehicle_sale": self.name}):
			return
		loan_app = frappe.get_doc({
			"doctype": "Loan Application",
			"vehicle_sale": self.name,
			"vehicle": self.vehicle,
			"customer": self.customer,
			"mobile_no": self.mobile_no,
			"financier": self.financier,
			"loan_amount": self.loan_amount,
			"down_payment": self.down_payment,
			"tenure_months": self.tenure_months,
			"interest_rate": self.interest_rate,
			"status": "Draft",
		})
		loan_app.insert(ignore_permissions=True)
		frappe.msgprint(
			_("Loan Application {0} created automatically.").format(loan_app.name),
			alert=True, indicator="blue",
		)

	def trigger_whatsapp_confirmation(self):
		try:
			from auto_dealer.api.whatsapp import send_whatsapp_message
			message = _(
				"Dear {0}, congratulations on your new {1}! "
				"Your vehicle delivery is confirmed. Thank you for choosing us!"
			).format(self.customer_name or self.customer, self.vehicle)
			send_whatsapp_message(mobile_no=self.mobile_no, message=message)
		except Exception:
			frappe.log_error(title="WhatsApp Delivery Notification Failed", message=frappe.get_traceback())

	def link_insurance_policy(self):
		"""Auto-create an Insurance Policy record if insurance details are provided."""
		if not self.insurance_policy_no:
			return
		if frappe.db.exists("Insurance Policy", {"policy_number": self.insurance_policy_no}):
			return
		ins = frappe.get_doc({
			"doctype": "Insurance Policy",
			"vehicle": self.vehicle,
			"customer": self.customer,
			"insurance_company": self.insurance_company,
			"policy_number": self.insurance_policy_no,
			"premium_amount": self.insurance_premium,
			"start_date": self.insurance_start_date,
			"end_date": self.insurance_end_date,
			"status": "Active",
			"vehicle_sale": self.name,
		})
		ins.insert(ignore_permissions=True)


# ── Standalone event handlers (wired via hooks.py doc_events) ─────────────────

def before_save(doc, method=None):
	doc.calculate_total_amount()
	doc.calculate_emi()


def on_submit(doc, method=None):
	doc.update_vehicle_status("Sold")
	doc.create_loan_application()
	doc.trigger_whatsapp_confirmation()
	doc.link_insurance_policy()


def on_cancel(doc, method=None):
	doc.update_vehicle_status("Available")
