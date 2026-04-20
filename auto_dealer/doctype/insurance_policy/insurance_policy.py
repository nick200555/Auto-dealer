"""
Insurance Policy DocType Controller
--------------------------------------
Module path: auto_dealer.auto_dealer.auto_dealer.doctype.insurance_policy.insurance_policy

Tracks insurance policy lifecycle:
  - Validates policy date range
  - Auto-expires policies past end_date
  - Links to Vehicle Sale on creation
  - Triggers renewal reminders via WhatsApp + insurance API
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, date_diff, getdate, add_days


RENEWAL_REMINDER_DAYS = 30


class InsurancePolicy(Document):

	def validate(self):
		self.validate_dates()

	def before_save(self):
		self.update_status_based_on_dates()

	def on_submit(self):
		self.notify_insurance_company()

	# ── Validation ────────────────────────────────────────────────────────────

	def validate_dates(self):
		if self.start_date and self.end_date:
			if getdate(self.end_date) <= getdate(self.start_date):
				frappe.throw(_("Policy End Date must be after Start Date."))

	def update_status_based_on_dates(self):
		if self.end_date and getdate(self.end_date) < getdate(today()):
			if self.status == "Active":
				self.status = "Expired"

	# ── Business Logic ────────────────────────────────────────────────────────

	def days_to_expiry(self) -> int:
		if self.end_date:
			return date_diff(self.end_date, today())
		return 0

	def send_renewal_reminder(self):
		"""Send WhatsApp renewal reminder. Called from daily scheduler."""
		days_left = self.days_to_expiry()
		if days_left <= 0:
			return
		try:
			from auto_dealer.api.whatsapp import send_whatsapp_message
			from auto_dealer.api.insurance import get_renewal_quote
			quote = get_renewal_quote(policy_number=self.policy_number)
			quote_text = f"₹{quote.get('premium', 'N/A')}" if quote else "please contact us"
			mobile = frappe.db.get_value("Customer", self.customer, "mobile_no")
			message = _(
				"Dear Customer, your insurance policy {0} for vehicle {1} expires in {2} days ({3}). "
				"Renew for {4}. Contact us today!"
			).format(self.policy_number, self.vehicle, days_left, self.end_date, quote_text)
			send_whatsapp_message(mobile_no=mobile, message=message)
			frappe.db.set_value("Insurance Policy", self.name, "renewal_reminder_sent", 1)
		except Exception:
			frappe.log_error(title="Insurance Renewal Reminder Failed", message=frappe.get_traceback())

	def notify_insurance_company(self):
		try:
			from auto_dealer.api.insurance import notify_new_policy
			notify_new_policy(
				policy_number=self.policy_number,
				vehicle_vin=self.vehicle,
				customer=self.customer,
				start_date=str(self.start_date),
				end_date=str(self.end_date),
				premium=self.premium_amount,
			)
		except Exception:
			frappe.log_error(title="Insurance Company Notification Failed", message=frappe.get_traceback())


# ── Standalone event handlers (wired via hooks.py doc_events) ─────────────────

def before_save(doc, method=None):
	doc.update_status_based_on_dates()


def on_submit(doc, method=None):
	doc.notify_insurance_company()
