"""
Auto Dealer Settings Controller
---------------------------------
Single DocType for all dealership configuration.
Source: PDF Section 13.1 — Auto Dealer Settings Configuration Fields.
"""

import frappe
from frappe.model.document import Document


class AutoDealerSettings(Document):

    def validate(self):
        if self.slow_moving_threshold_days and self.slow_moving_threshold_days < 1:
            frappe.throw(frappe._("Slow Moving Threshold must be at least 1 day."))
        if self.accessories_commission_pct and (
            self.accessories_commission_pct < 0 or self.accessories_commission_pct > 100
        ):
            frappe.throw(frappe._("Accessories Commission % must be between 0 and 100."))
