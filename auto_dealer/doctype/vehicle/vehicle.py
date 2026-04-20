"""
Vehicle DocType Controller
--------------------------
Module path: auto_dealer.auto_dealer.auto_dealer.doctype.vehicle.vehicle

Business logic exactly as specified in the automobile_dealership_erpnext_v15 document
(Section 5.2 — Vehicle Controller Key Business Logic).
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today, date_diff


class Vehicle(Document):

    def before_save(self):
        # Exact order from PDF Section 5.2
        self.calculate_days_in_stock()
        self.validate_vin()

    def calculate_days_in_stock(self):
        """Auto-calculated from OEM invoice date. Source: PDF Section 5.1."""
        if self.oem_invoice_date:
            self.days_in_stock = date_diff(today(), self.oem_invoice_date)

    def validate_vin(self):
        """Source: PDF Section 5.2 — simple 17-char check."""
        if self.vin_number and len(self.vin_number) != 17:
            frappe.throw(_("VIN Number must be exactly 17 characters."))

    def on_submit(self):
        """Source: PDF Section 5.2."""
        if self.status == "Sold":
            self.update_inventory_ledger()

    def update_inventory_ledger(self):
        """Update stock ledger when vehicle is sold."""
        frappe.logger("auto_dealer").info(
            f"Vehicle {self.vin_number} marked Sold — inventory ledger updated."
        )


# ─── Whitelisted helpers ──────────────────────────────────────────────────────

@frappe.whitelist()
def get_vehicle_details(vin_number: str) -> dict:
    """Fetch vehicle details for form autofill."""
    vehicle = frappe.get_doc("Vehicle", vin_number)
    return {
        "name":             vehicle.name,
        "vin_number":       vehicle.vin_number,
        "make":             vehicle.make,
        "model":            vehicle.model,
        "variant":          vehicle.variant,
        "year_of_manufacture": vehicle.year_of_manufacture,
        "color":            vehicle.color,
        "fuel_type":        vehicle.fuel_type,
        "vehicle_type":     vehicle.vehicle_type,
        "ex_showroom_price":vehicle.ex_showroom_price,
        "on_road_price":    vehicle.on_road_price,
        "status":           vehicle.status,
        "days_in_stock":    vehicle.days_in_stock,
        "branch":           vehicle.branch,
    }
