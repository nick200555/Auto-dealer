"""
Loan DSA (Direct Selling Agent) API Integration
-------------------------------------------------
Facilitates loan application processing with bank/NBFC DSA partners:
  - Submitting loan applications
  - Checking loan application status
  - Fetching approved loan offers
  - Syncing EMI disbursement events

Configuration stored in site_config under 'loan_dsa_*' keys.
"""

import frappe
from frappe import _
import requests
from typing import Optional


def _get_config() -> dict:
	"""Retrieve Loan DSA API configuration from site config."""
	return {
		"base_url": frappe.conf.get("loan_dsa_api_url", "https://api.loan-dsa.example.com/v1"),
		"api_key": frappe.conf.get("loan_dsa_api_key", ""),
		"dealer_id": frappe.conf.get("loan_dsa_dealer_id", ""),
	}


def _headers(config: dict) -> dict:
	return {
		"Authorization": f"Bearer {config['api_key']}",
		"X-Dealer-ID": config.get("dealer_id", ""),
		"Content-Type": "application/json",
		"Accept": "application/json",
	}


def submit_loan_application(
	vehicle_sale_name: str,
	customer: str,
	loan_amount: float,
	tenure_months: int,
	vehicle_vin: str,
) -> Optional[dict]:
	"""
	Submit a loan application to the DSA partner.

	Args:
		vehicle_sale_name: Reference to the Vehicle Sale document
		customer: Customer's name / ID
		loan_amount: Requested loan amount in INR
		tenure_months: Loan tenure in months
		vehicle_vin: VIN of the vehicle being financed

	Returns:
		dict: {'application_id': '...', 'status': 'submitted', ...}
		      or None on failure
	"""
	config = _get_config()
	if not config["api_key"]:
		frappe.logger("auto_dealer").warning(
			"Loan DSA API key not configured. Application not submitted."
		)
		return None

	# Fetch customer KYC details
	customer_doc = frappe.get_doc("Customer", customer)
	payload = {
		"reference_id": vehicle_sale_name,
		"dealer_id": config.get("dealer_id", ""),
		"customer": {
			"name": customer_doc.customer_name,
			"email": customer_doc.email_id or "",
			"mobile": customer_doc.mobile_no or "",
		},
		"vehicle_vin": vehicle_vin,
		"loan_amount": loan_amount,
		"tenure_months": tenure_months,
	}

	try:
		url = f"{config['base_url']}/loan/apply"
		response = requests.post(url, headers=_headers(config), json=payload, timeout=30)
		response.raise_for_status()
		result = response.json()
		frappe.logger("auto_dealer").info(
			f"Loan application submitted for {customer} / {vehicle_vin}. App ID: {result.get('application_id')}"
		)
		return result
	except Exception as e:
		frappe.log_error(title="Loan DSA - Application Submission Error", message=str(e))
		return None


def get_loan_status(application_id: str) -> Optional[dict]:
	"""
	Fetch the current status of a loan application from the DSA.

	Returns:
		dict: {'status': 'approved'|'rejected'|'pending', 'approved_amount': ..., ...}
		      or None on failure
	"""
	config = _get_config()
	if not config["api_key"]:
		return None

	try:
		url = f"{config['base_url']}/loan/{application_id}/status"
		response = requests.get(url, headers=_headers(config), timeout=15)
		response.raise_for_status()
		return response.json()
	except Exception as e:
		frappe.log_error(title="Loan DSA - Status Check Error", message=str(e))
		return None


def sync_all_pending_applications() -> dict:
	"""
	Called from scheduler (every 4 hours).
	Fetches status for all Vehicle Sales with pending loan applications
	and updates accordingly.

	Returns:
		dict: Summary of synced applications
	"""
	pending_sales = frappe.get_all(
		"Vehicle Sale",
		filters={"finance_type": "Loan", "status": "Finance Approved", "docstatus": 1},
		fields=["name", "customer", "vehicle", "loan_amount", "tenure_months"],
	)

	synced = 0
	errors = 0

	for sale in pending_sales:
		# In a real implementation, the DSA application ID would be stored on the sale
		app_id = frappe.db.get_value(
			"Vehicle Sale", sale["name"], "loan_dsa_application_id"
		)
		if not app_id:
			continue

		status_data = get_loan_status(app_id)
		if not status_data:
			errors += 1
			continue

		# Update vehicle sale with latest DSA status
		new_status = status_data.get("status", "").lower()
		if new_status == "approved":
			frappe.db.set_value("Vehicle Sale", sale["name"], "status", "Finance Approved")
			synced += 1
		elif new_status == "rejected":
			frappe.db.set_value("Vehicle Sale", sale["name"], "status", "Draft")
			synced += 1

	frappe.db.commit()
	return {"synced": synced, "errors": errors, "total": len(pending_sales)}


@frappe.whitelist()
def apply_for_loan(vehicle_sale: str) -> dict:
	"""
	Whitelisted endpoint to initiate a loan application from the Vehicle Sale form.
	"""
	doc = frappe.get_doc("Vehicle Sale", vehicle_sale)
	if doc.finance_type != "Loan":
		frappe.throw(_("Finance type must be Loan to apply via DSA."))

	result = submit_loan_application(
		vehicle_sale_name=vehicle_sale,
		customer=doc.customer,
		loan_amount=doc.loan_amount,
		tenure_months=doc.tenure_months,
		vehicle_vin=doc.vehicle,
	)

	if result and result.get("application_id"):
		frappe.db.set_value(
			"Vehicle Sale", vehicle_sale, "loan_dsa_application_id", result["application_id"]
		)
		return {"success": True, "application_id": result["application_id"]}

	return {"success": False, "message": _("Loan application submission failed. Check API settings.")}
