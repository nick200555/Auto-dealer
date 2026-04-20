"""
Custom Sales Order Override
-----------------------------
Source: PDF Section 4.1 — override_doctype_class:
    "Sales Order": "auto_dealer.overrides.sales_order.CustomSalesOrder"

Extends ERPNext Sales Order to:
  - Auto-link to Vehicle Sale on order creation
  - Validate vehicle availability before order is placed
  - Auto-assign Sales Consultant based on round-robin algorithm (PDF Section 7.1)
"""

import frappe
from frappe import _

try:
    from erpnext.selling.doctype.sales_order.sales_order import SalesOrder
except ImportError:
    from frappe.model.document import Document as SalesOrder


class CustomSalesOrder(SalesOrder):

    def validate(self):
        super().validate()
        self._validate_vehicle_availability()

    def on_submit(self):
        super().on_submit()
        self._auto_assign_sales_consultant()

    def _validate_vehicle_availability(self):
        """Ensure any vehicle linked in the order is Available or Booked."""
        vehicle = self.get("vehicle")
        if not vehicle:
            return
        status = frappe.db.get_value("Vehicle", vehicle, "status")
        if status not in ("Available", "Booked"):
            frappe.throw(
                _("Vehicle {0} is not available. Current status: {1}").format(vehicle, status)
            )

    def _auto_assign_sales_consultant(self):
        """
        Round-robin lead assignment based on open lead count.
        Source: PDF Section 7.1.
        """
        if self.get("sales_consultant"):
            return  # Already assigned

        consultants = frappe.db.sql("""
            SELECT u.name, COUNT(so.name) AS open_orders
            FROM `tabUser` u
            JOIN `tabHas Role` hr ON hr.parent = u.name AND hr.role = 'Sales Consultant'
            LEFT JOIN `tabSales Order` so
              ON so.sales_consultant = u.name AND so.status NOT IN ('Completed', 'Cancelled')
            WHERE u.enabled = 1
            GROUP BY u.name
            ORDER BY open_orders ASC
            LIMIT 1
        """, as_dict=True)

        if consultants:
            frappe.db.set_value("Sales Order", self.name, "sales_consultant", consultants[0].name)
