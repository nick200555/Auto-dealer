"""
Service Job Card Event Handlers
---------------------------------
Wired by hooks.py doc_events exactly as per PDF Section 4.1:

    "Service Job Card": {
        "on_submit": "auto_dealer.events.service_job_card.on_submit",
    },

On submit actions (PDF Section 9.1 + 9.2):
  - Check stock for required parts → auto-create Material Request if below required qty
  - WhatsApp notification to customer that job has started
"""

import frappe
from frappe import _
from frappe.utils import flt


def on_submit(doc, method=None):
    """
    On submit: check parts stock and auto-create Material Request if needed.
    Source: PDF Section 9.2.
    """
    _check_parts_and_create_material_request(doc)
    _send_job_started_whatsapp(doc)


def _check_parts_and_create_material_request(doc):
    """
    When a Service Job Card is submitted, check stock for each required part.
    If any part's quantity in the Service Warehouse is below the required amount,
    a Material Request is auto-created and assigned to the Parts Incharge.
    Source: PDF Section 9.2.
    """
    if not doc.get("service_items"):
        return

    items_to_request = []
    service_warehouse = frappe.db.get_single_value("Auto Dealer Settings", "service_warehouse") or "Stores - AD"

    for item in doc.service_items:
        if not item.item_code:
            continue
        actual_qty = flt(frappe.db.get_value(
            "Bin",
            {"item_code": item.item_code, "warehouse": service_warehouse},
            "actual_qty"
        ) or 0)
        required_qty = flt(item.qty or 1)
        if actual_qty < required_qty:
            items_to_request.append({
                "item_code": item.item_code,
                "qty": required_qty - actual_qty,
                "schedule_date": frappe.utils.today(),
                "warehouse": service_warehouse,
                "description": f"Auto-requested for Service Job Card {doc.name}",
            })

    if items_to_request:
        try:
            mr = frappe.get_doc({
                "doctype": "Material Request",
                "material_request_type": "Purchase",
                "transaction_date": frappe.utils.today(),
                "items": items_to_request,
            })
            mr.insert(ignore_permissions=True)
            frappe.msgprint(
                _("Material Request {0} auto-created for short-stock parts.").format(mr.name),
                alert=True, indicator="orange"
            )
        except Exception:
            frappe.log_error(
                title="Material Request Auto-Creation Failed",
                message=frappe.get_traceback()
            )


def _send_job_started_whatsapp(doc):
    """
    Send WhatsApp to customer that service has started.
    Template: service_started — name, job_card, vehicle, advisor (PDF Section 11.1).
    """
    try:
        settings = frappe.get_single("Auto Dealer Settings")
        if not settings.whatsapp_enabled:
            return
        from auto_dealer.api.whatsapp import send_whatsapp_message
        mobile = doc.get("mobile_no") or frappe.db.get_value("Customer", doc.customer, "mobile_no")
        if not mobile:
            return
        message = _(
            "Dear {0}, your vehicle {1} has been assigned to our workshop. "
            "Service Advisor: {2}. Job Card: {3}. "
            "We will notify you when your vehicle is ready."
        ).format(
            doc.customer_name or doc.customer,
            doc.vehicle,
            doc.service_advisor or "our team",
            doc.name,
        )
        send_whatsapp_message(mobile_no=mobile, message=message)
    except Exception:
        frappe.log_error(
            title="WhatsApp Service Started Notification Failed",
            message=frappe.get_traceback()
        )
