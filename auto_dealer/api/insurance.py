"""
Insurance API Integration
--------------------------
Interfaces with insurance provider APIs for:
  - Fetching renewal premium quotes
  - Creating new policy records at the insurer
  - Checking policy status
  - Triggering claim initiation

Configuration stored in site_config or "Insurance API Settings" DocType.
"""

import frappe
from frappe import _
import requests
from typing import Optional


def _get_config() -> dict:
	"""Retrieve insurance API configuration."""
	return {
		"base_url": frappe.conf.get("insurance_api_base_url", "https://api.insurer.example.com/v1"),
		"api_key": frappe.conf.get("insurance_api_key", ""),
		"dealer_code": frappe.conf.get("insurance_dealer_code", ""),
	}


def _headers(config: dict) -> dict:
	return {
		"Authorization": f"Bearer {config['api_key']}",
		"X-Dealer-Code": config.get("dealer_code", ""),
		"Content-Type": "application/json",
		"Accept": "application/json",
	}


def get_renewal_quote(policy_number: str) -> Optional[dict]:
	"""
	Fetch a renewal premium quote for an existing policy.

	Args:
		policy_number: The existing insurance policy number

	Returns:
		dict: {'premium': float, 'valid_until': 'YYYY-MM-DD', ...}
		      or None if not available
	"""
	config = _get_config()
	if not config["api_key"]:
		frappe.logger("auto_dealer").warning("Insurance API key not configured. Skipping renewal quote.")
		return None

	try:
		url = f"{config['base_url']}/policy/{policy_number}/renewal-quote"
		response = requests.get(url, headers=_headers(config), timeout=15)
		response.raise_for_status()
		data = response.json()
		frappe.logger("auto_dealer").info(
			f"Insurance renewal quote for {policy_number}: {data}"
		)
		return data
	except requests.exceptions.HTTPError as e:
		if e.response.status_code == 404:
			frappe.logger("auto_dealer").warning(
				f"Insurance policy {policy_number} not found at provider."
			)
			return None
		frappe.log_error(title="Insurance API - Renewal Quote Error", message=str(e))
		return None
	except Exception as e:
		frappe.log_error(title="Insurance API - Renewal Quote Error", message=str(e))
		return None


def notify_new_policy(
	policy_number: str,
	vehicle_vin: str,
	customer: str,
	start_date: str,
	end_date: str,
	premium: float,
) -> Optional[dict]:
	"""
	Register a new insurance policy with the insurer's system.

	Args:
		policy_number: Policy reference number
		vehicle_vin: VIN of the insured vehicle
		customer: Customer name / ID
		start_date: Policy start date (YYYY-MM-DD)
		end_date: Policy end date (YYYY-MM-DD)
		premium: Premium amount in INR

	Returns:
		dict: Insurer's confirmation payload or None on failure
	"""
	config = _get_config()
	if not config["api_key"]:
		frappe.logger("auto_dealer").warning("Insurance API key not configured. New policy not notified.")
		return None

	payload = {
		"policy_number": policy_number,
		"vehicle_vin": vehicle_vin,
		"customer_id": customer,
		"start_date": start_date,
		"end_date": end_date,
		"premium_amount": premium,
		"dealer_code": config.get("dealer_code", ""),
	}

	try:
		url = f"{config['base_url']}/policy/create"
		response = requests.post(url, headers=_headers(config), json=payload, timeout=15)
		response.raise_for_status()
		result = response.json()
		frappe.logger("auto_dealer").info(
			f"New policy {policy_number} registered with insurer. Response: {result}"
		)
		return result
	except Exception as e:
		frappe.log_error(title="Insurance API - New Policy Notification Error", message=str(e))
		return None


def check_policy_status(policy_number: str) -> Optional[dict]:
	"""
	Check the current status of a policy at the insurer.

	Returns:
		dict: {'status': 'active'|'expired'|'cancelled', 'expiry_date': '...'}
		      or None on failure
	"""
	config = _get_config()
	if not config["api_key"]:
		return None

	try:
		url = f"{config['base_url']}/policy/{policy_number}/status"
		response = requests.get(url, headers=_headers(config), timeout=15)
		response.raise_for_status()
		return response.json()
	except Exception as e:
		frappe.log_error(title="Insurance API - Policy Status Error", message=str(e))
		return None


@frappe.whitelist()
def fetch_renewal_quote_for_policy(policy_number: str) -> dict:
	"""
	Whitelisted endpoint: Fetch renewal quote for a Vehicle Insurance record.
	Called from the form's action button or from scheduler tasks.
	"""
	quote = get_renewal_quote(policy_number=policy_number)
	if quote:
		return {"success": True, "quote": quote}
	return {"success": False, "message": _("Could not fetch renewal quote. Please check API configuration.")}
