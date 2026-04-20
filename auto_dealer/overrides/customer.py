"""
Custom Customer Override
--------------------------
Source: PDF Section 4.1 — override_doctype_class:
    "Customer": "auto_dealer.overrides.customer.CustomCustomer"

Extends ERPNext Customer to:
  - Initialize a Loyalty Account on customer creation (PDF Section 11.2)
  - Send WhatsApp acknowledgement on new lead/customer (PDF Section 7.1)
"""

import frappe
from frappe import _

try:
    from erpnext.selling.doctype.customer.customer import Customer
except ImportError:
    from frappe.model.document import Document as Customer


class CustomCustomer(Customer):

    def after_insert(self):
        super().after_insert()
        self._create_loyalty_account()
        self._send_lead_acknowledgement_whatsapp()

    def _create_loyalty_account(self):
        """
        Create Loyalty Account with 0 points on customer creation.
        Source: PDF Section 11.2.
        """
        if frappe.db.exists("Loyalty Account", {"customer": self.name}):
            return
        try:
            loyalty = frappe.get_doc({
                "doctype": "Loyalty Account",
                "customer": self.name,
                "customer_name": self.customer_name,
                "total_points": 0,
            })
            loyalty.insert(ignore_permissions=True)
        except Exception:
            frappe.log_error(
                title=f"Loyalty Account Creation Failed for {self.name}",
                message=frappe.get_traceback()
            )

    def _send_lead_acknowledgement_whatsapp(self):
        """
        Send WhatsApp acknowledgement immediately after lead/customer creation.
        Template: lead_acknowledgement (PDF Section 7.1 + 11.1).
        Variables: customer_name, model, dealership_name.
        """
        try:
            settings = frappe.get_single("Auto Dealer Settings")
            if not settings.whatsapp_enabled:
                return
            mobile = self.mobile_no or self.get("mobile_no")
            if not mobile:
                return
            from auto_dealer.api.whatsapp import send_whatsapp_message
            message = _(
                "Dear {0}, thank you for your interest in {1}! "
                "Our Sales Consultant will contact you shortly. "
                "We look forward to serving you."
            ).format(
                self.customer_name,
                settings.dealership_name or "our dealership",
            )
            send_whatsapp_message(mobile_no=mobile, message=message)
        except Exception:
            frappe.log_error(
                title="Lead Acknowledgement WhatsApp Failed",
                message=frappe.get_traceback()
            )
