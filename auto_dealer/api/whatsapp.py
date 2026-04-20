"""
WhatsApp Integration
---------------------
Reads configuration from Auto Dealer Settings Single DocType.
Source: PDF Sections 11.1, 13.1, 13.2.

Provider options (PDF Section 13.2): Interakt, Wati, AiSensy, Gupshup

WhatsApp Templates (PDF Section 11.1):
  - lead_acknowledgement     → New lead created
  - test_drive_confirmation  → Test drive submitted
  - service_started          → Job card submitted
  - vehicle_ready            → Job card completed
  - amc_renewal_reminder     → 30/15/7 days before AMC expiry
  - insurance_renewal        → 30 days before policy expiry
"""

import frappe
from frappe import _
import requests


def get_whatsapp_config() -> dict:
    """Fetch WhatsApp config from Auto Dealer Settings (PDF Section 13.1)."""
    settings = frappe.get_single("Auto Dealer Settings")
    return {
        "enabled": bool(settings.whatsapp_enabled),
        "api_key": settings.whatsapp_api_key,
        "dealership_name": settings.dealership_name,
    }


def send_whatsapp_message(mobile_no: str, message: str) -> dict:
    """
    Send a WhatsApp message via the configured provider.
    Config comes from Auto Dealer Settings (PDF Section 13.1).

    Raises an exception on HTTP error so callers can handle/log.
    Returns the provider API response dict.
    """
    if not mobile_no:
        frappe.throw(_("Mobile number is required for WhatsApp messaging."))

    config = get_whatsapp_config()
    if not config["enabled"]:
        frappe.logger("auto_dealer").info(
            f"WhatsApp disabled in Auto Dealer Settings — message not sent to {mobile_no}."
        )
        return {"status": "skipped", "reason": "WhatsApp disabled"}

    if not config["api_key"]:
        frappe.throw(_("WhatsApp API key not configured in Auto Dealer Settings."))

    # Normalise mobile number — ensure 91 country code prefix for India
    mobile = str(mobile_no).strip().replace(" ", "").replace("-", "")
    if not mobile.startswith("+") and len(mobile) == 10:
        mobile = f"+91{mobile}"

    # Interakt API format (primary provider per PDF Section 13.2)
    payload = {
        "fullPhoneNumber": mobile,
        "callbackData": f"auto_dealer_{frappe.session.user}",
        "type": "text",
        "message": {"text": message},
    }

    try:
        response = requests.post(
            "https://api.interakt.ai/v1/public/message/",
            json=payload,
            headers={
                "Authorization": f"Basic {config['api_key']}",
                "Content-Type": "application/json",
            },
            timeout=15,
        )
        response.raise_for_status()
        frappe.logger("auto_dealer").info(f"WhatsApp sent to {mobile}: {message[:60]}…")
        return response.json()
    except requests.HTTPError as e:
        frappe.log_error(
            title=f"WhatsApp API Error (HTTP {e.response.status_code})",
            message=f"Mobile: {mobile}\nMessage: {message}\nResponse: {e.response.text}"
        )
        raise
    except Exception:
        frappe.log_error(title="WhatsApp Send Failed", message=frappe.get_traceback())
        raise


@frappe.whitelist()
def send_test_message(mobile_no: str) -> dict:
    """Whitelisted: send a test WhatsApp message from Auto Dealer Settings page."""
    settings = frappe.get_single("Auto Dealer Settings")
    return send_whatsapp_message(
        mobile_no=mobile_no,
        message=f"This is a test message from {settings.dealership_name or 'Auto Dealer ERP'}. WhatsApp is configured correctly.",
    )
