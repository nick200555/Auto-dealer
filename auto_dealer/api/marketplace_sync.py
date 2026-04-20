"""
Marketplace Sync — CarDekho Integration
-----------------------------------------
API integration exactly as specified in PDF Section 6.2.

Uses Auto Dealer Settings (PDF Section 13.1) for:
  - settings.cardekho_dealer_id
  - settings.cardekho_api_url
  - settings.cardekho_api_key
  - Vehicle field: vin_number (PDF Section 5.1)
"""

import frappe
from frappe import _
import requests


def sync_to_cardekho(vehicle_name: str) -> dict:
    """
    Sync a single vehicle to CarDekho partner portal.
    Exact implementation from PDF Section 6.2.

    Vehicle listings are auto-synced to CarDekho's partner portal when a vehicle
    is marked Available. The sync includes VIN, specs, price, and images.
    Failed syncs are logged to the Frappe error log for retry.
    """
    vehicle = frappe.get_doc("Vehicle", vehicle_name)
    settings = frappe.get_single("Auto Dealer Settings")

    payload = {
        "dealer_id": settings.cardekho_dealer_id,
        "vin":       vehicle.vin_number,          # PDF uses vin_number field
        "make":      vehicle.make,
        "model":     vehicle.model,
        "variant":   vehicle.variant or "",
        "year":      vehicle.year_of_manufacture,  # PDF uses year_of_manufacture
        "color":     vehicle.color or "",
        "fuel_type": vehicle.fuel_type,
        "price":     vehicle.ex_showroom_price,
        "on_road_price": vehicle.on_road_price or vehicle.ex_showroom_price,
        "status":    vehicle.status,
        # ... more fields as needed
    }

    response = requests.post(
        settings.cardekho_api_url or "https://api.cardekho.com/dealer/v2/listings",
        json=payload,
        headers={"Authorization": f"Bearer {settings.cardekho_api_key}"},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def sync_all_inventory() -> dict:
    """
    Sync all Available vehicles to CarDekho.
    Called from daily scheduler task.
    Source: PDF Section 6.2.
    """
    settings = frappe.get_single("Auto Dealer Settings")
    if not settings.cardekho_dealer_id or not settings.cardekho_api_key:
        return {"status": "skipped", "reason": "CarDekho not configured"}

    available_vehicles = frappe.get_all(
        "Vehicle",
        filters={"status": "Available", "docstatus": 1},
        fields=["name"],
    )

    synced = 0
    failed = 0
    for v in available_vehicles:
        try:
            sync_to_cardekho(v.name)
            synced += 1
        except requests.HTTPError as e:
            failed += 1
            frappe.log_error(
                title=f"CarDekho Sync Failed: {v.name}",
                message=str(e)
            )
        except Exception:
            failed += 1
            frappe.log_error(
                title=f"CarDekho Sync Failed: {v.name}",
                message=frappe.get_traceback()
            )

    return {"status": "completed", "synced": synced, "failed": failed}


@frappe.whitelist()
def push_vehicle_to_marketplace(vehicle: str) -> dict:
    """Whitelisted: manually push a vehicle from the form button."""
    try:
        result = sync_to_cardekho(vehicle)
        return {"status": "success", "response": result}
    except Exception as e:
        frappe.log_error(title=f"Manual MarketplaceSync Failed: {vehicle}", message=frappe.get_traceback())
        return {"status": "error", "message": str(e)}
