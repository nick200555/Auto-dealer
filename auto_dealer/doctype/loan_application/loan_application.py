"""
Loan Application DocType Controller
--------------------------------------
Module path: auto_dealer.auto_dealer.doctype.loan_application.loan_application

EMI formula exactly as given in PDF Section 8.1:
    EMI = P × r × (1+r)^n / ((1+r)^n - 1)
    where r = (interest_rate / 100) / 12   (monthly rate)

All calculation fields (EMI, total_payable, total_interest) are
auto-populated on save (PDF Section 8.1).
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, cint, today


class LoanApplication(Document):

    def validate(self):
        self.calculate_emi()

    def before_save(self):
        self.calculate_emi()

    def on_submit(self):
        self._submit_to_dsa()

    # ── EMI Calculation — exact PDF Section 8.1 code ─────────────────────────

    def calculate_emi(self):
        """
        Exact formula from PDF Section 8.1:
            p = self.loan_amount
            r = (self.interest_rate / 100) / 12
            n = self.tenure_months
            if r > 0:
                emi = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
                self.emi_amount    = round(emi, 2)
                self.total_payable = round(emi * n, 2)
                self.total_interest = round(self.total_payable - p, 2)
        """
        p = flt(self.loan_amount)
        r = (flt(self.interest_rate) / 100) / 12   # Monthly rate
        n = cint(self.tenure_months)

        if r > 0 and p > 0 and n > 0:
            emi = p * r * ((1 + r) ** n) / (((1 + r) ** n) - 1)
            self.emi_amount    = round(emi, 2)
            self.total_payable = round(emi * n, 2)
            self.total_interest = round(self.total_payable - p, 2)
        elif p > 0 and n > 0:
            # Zero-interest: equal instalments
            self.emi_amount    = round(p / n, 2)
            self.total_payable = round(p, 2)
            self.total_interest = 0
        else:
            self.emi_amount    = 0
            self.total_payable = 0
            self.total_interest = 0

    # ── DSA Integration ───────────────────────────────────────────────────────

    def _submit_to_dsa(self):
        """Submit to Loan DSA partner portal. Source: PDF Section 13.2."""
        if not self.get("dsa_name"):
            return
        try:
            from auto_dealer.api.loan_dsa import submit_loan_application
            result = submit_loan_application(
                vehicle_sale_name=self.vehicle_sale,
                customer=self.customer,
                loan_amount=self.loan_amount,
                tenure_months=self.tenure_months,
                vehicle_vin=self.vehicle,
            )
            if result and result.get("application_id"):
                frappe.db.set_value("Loan Application", self.name, {
                    "dsa_application_id": result["application_id"],
                    "submitted_on": today(),
                    "status": "Submitted to DSA",
                })
                frappe.db.commit()
        except Exception:
            frappe.log_error(title="Loan DSA Submission Failed", message=frappe.get_traceback())


# ── Standalone event handlers (wired via hooks.py if needed) ─────────────────

def before_save(doc, method=None):
    doc.calculate_emi()
