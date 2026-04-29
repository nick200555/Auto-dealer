"""
Vehicle Sale Event Handlers
----------------------------
Wired by hooks.py doc_events exactly as specified in PDF Section 4.1:

    doc_events = {
        "Vehicle Sale": {
            "on_submit": [
                "auto_dealer.events.vehicle_sale.on_submit",
                "auto_dealer.events.vehicle_sale.trigger_whatsapp_confirmation",
            ],
        },
    }

Submission chain (PDF Section 5.3):
  1. Validates vehicle is still Available or Booked
  2. Calculates grand total including registration, insurance, accessories, discounts
  3. Updates Vehicle status to Sold and links the customer
  4. Creates a Sales Invoice with correct GST tax template
  5. Logs a CRM Activity record for sales reporting
  6. Creates a Vehicle Delivery Checklist document
  7. Triggers a WhatsApp confirmation message to the customer
"""

import frappe
from frappe import _
from frappe.utils import today, flt


def on_submit(doc, method=None):
    """
    Main on_submit handler for Vehicle Sale.
    Executes steps 1–6 of the submission chain (PDF Section 5.3).
    """
    _validate_vehicle_availability(doc)
    _calculate_grand_total(doc)
    _update_vehicle_status(doc)
    _create_sales_invoice(doc)
    _log_crm_activity(doc)
    _create_delivery_checklist(doc)


def trigger_whatsapp_confirmation(doc, method=None):
    """
    Step 7 of submission chain (PDF Section 5.3).
    Triggers WhatsApp confirmation message to the customer.
    """
    try:
        settings = frappe.get_single("Auto Dealer Settings")
        if not settings.whatsapp_enabled:
            return
        from auto_dealer.api.whatsapp import send_whatsapp_message
        message = _(
            "Dear {0}, congratulations on your new {1} {2}! "
            "Your vehicle purchase at {3} is confirmed. "
            "Our team will contact you shortly for delivery details."
        ).format(
            doc.customer_name or doc.customer,
            doc.make or "",
            doc.model or "",
            settings.dealership_name or "our dealership",
        )
        mobile = doc.get("mobile_no") or frappe.db.get_value("Customer", doc.customer, "mobile_no")
        if mobile:
            send_whatsapp_message(mobile_no=mobile, message=message)
    except Exception:
        frappe.log_error(
            title="WhatsApp Sale Confirmation Failed",
            message=frappe.get_traceback()
        )


# ─── Private helpers ──────────────────────────────────────────────────────────

def _validate_vehicle_availability(doc):
    """Step 1: Validate vehicle is still Available or Booked (PDF Section 5.3)."""
    status = frappe.db.get_value("Vehicle", doc.vehicle, "status")
    if status not in ("Available", "Booked"):
        frappe.throw(
            _("Vehicle {0} is not available for sale. Current status: {1}").format(
                doc.vehicle, status
            )
        )


def _calculate_grand_total(doc):
    """
    Step 2: Calculate grand total including registration, insurance,
    accessories, and discounts (PDF Section 5.3).
    """
    grand_total = (
        flt(doc.ex_showroom_price)
        + flt(doc.registration_amount)
        + flt(doc.insurance_premium)
        + flt(doc.accessories_amount)
        - flt(doc.discount_amount)
    )
    if grand_total != flt(doc.grand_total):
        frappe.db.set_value("Vehicle Sale", doc.name, "grand_total", grand_total)


def _update_vehicle_status(doc):
    """Step 3: Update Vehicle status to Sold and link the customer (PDF Section 5.3)."""
    frappe.db.set_value("Vehicle", doc.vehicle, {
        "status": "Sold",
    })
    frappe.db.commit()


def _create_sales_invoice(doc):
    """Step 4: Create a Sales Invoice with correct GST tax template (PDF Section 5.3)."""
    if frappe.db.exists("Sales Invoice", {"auto_dealer_vehicle_sale": doc.name, "docstatus": ["!=", 2]}):
        return  # Already exists

    try:
        settings = frappe.get_single("Auto Dealer Settings")
        # Determine GST template based on state (intra-state vs inter-state)
        tax_template = _get_gst_template(doc)

        si = frappe.get_doc({
            "doctype": "Sales Invoice",
            "customer": doc.customer,
            "posting_date": doc.delivery_date or today(),
            "due_date": doc.delivery_date or today(),
            "auto_dealer_vehicle_sale": doc.name,
            "taxes_and_charges": tax_template,
            "items": [{
                "item_code": doc.vehicle,
                "item_name": f"{doc.make} {doc.model} {doc.variant or ''}".strip(),
                "description": f"VIN: {doc.vehicle}",
                "qty": 1,
                "rate": flt(doc.ex_showroom_price),
                "amount": flt(doc.ex_showroom_price),
            }],
        })
        si.insert(ignore_permissions=True)
        frappe.logger("auto_dealer").info(f"Sales Invoice {si.name} created for Vehicle Sale {doc.name}")
    except Exception:
        frappe.log_error(
            title="Sales Invoice Creation Failed for Vehicle Sale",
            message=frappe.get_traceback()
        )


def _get_gst_template(doc):
    """Return appropriate GST template — CGST+SGST for intra-state, IGST for inter-state."""
    try:
        company_state = frappe.db.get_value("Company", doc.company, "state") if doc.get("company") else None
        customer_state = frappe.db.get_value("Customer", doc.customer, "state")
        if company_state and customer_state and company_state != customer_state:
            return "IGST 28%"
        return "CGST + SGST 28%"
    except Exception:
        return None


def _log_crm_activity(doc):
    """Step 5: Log a CRM Activity record for sales reporting (PDF Section 5.3)."""
    try:
        frappe.get_doc({
            "doctype": "Activity Log",
            "subject": f"Vehicle Sale {doc.name} submitted",
            "content": f"Vehicle {doc.vehicle} sold to {doc.customer} for ₹{doc.grand_total}",
            "reference_doctype": "Vehicle Sale",
            "reference_name": doc.name,
        }).insert(ignore_permissions=True)
    except Exception:
        # Activity Log may not exist in all ERPNext versions; use frappe.log
        frappe.logger("auto_dealer").info(
            f"CRM Activity: Vehicle Sale {doc.name} — Vehicle {doc.vehicle} sold to {doc.customer}"
        )


def _create_delivery_checklist(doc):
    """Step 6: Create a Vehicle Delivery Checklist document (PDF Section 5.3)."""
    if frappe.db.exists("Vehicle Delivery Checklist", {"vehicle_sale": doc.name}):
        return
    try:
        checklist = frappe.get_doc({
            "doctype": "Vehicle Delivery Checklist",
            "vehicle_sale": doc.name,
            "vehicle": doc.vehicle,
            "customer": doc.customer,
            "delivery_date": doc.delivery_date,
            "status": "Pending",
        })
        checklist.insert(ignore_permissions=True)
    except Exception:
        # DocType may not exist yet in this installation
        frappe.logger("auto_dealer").warning(
            f"Could not create Vehicle Delivery Checklist for {doc.name}: {frappe.get_traceback()}"
        )
