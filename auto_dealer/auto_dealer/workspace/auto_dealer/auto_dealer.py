import frappe
from frappe import _

def get_data():
	"""
	Return context data for the Auto Dealer workspace.
	"""
	return {
		"roles": get_workspace_roles(),
		"onboarding": get_onboarding_data()
	}

def get_workspace_roles():
	"""
	Role visibility helpers to determine who can access the workspace.
	"""
	return [
		"System Manager",
		"Dealership Manager",
		"Sales Executive",
		"Service Advisor",
		"Finance Officer",
		"Inventory Manager"
	]

def get_onboarding_data():
	"""
	Onboarding helper methods to guide new users.
	"""
	return {
		"title": _("Welcome to the Auto Dealer System"),
		"subtitle": _("Complete these steps to set up your dealership."),
		"success_message": _("Dealership setup completed successfully."),
		"items": [
			{
				"title": _("Update Settings"),
				"description": _("Configure basic Auto Dealer settings like default warehouse and branch."),
				"route": ["Form", "Auto Dealer Settings"],
				"status": is_settings_configured()
			},
			{
				"title": _("Add Vehicle Master"),
				"description": _("Create your first vehicle model."),
				"route": ["List", "Vehicle Master"],
				"status": has_records("Vehicle Master")
			}
		]
	}

def is_settings_configured():
	"""
	Dashboard utility to check if settings exist.
	"""
	if frappe.db.exists("Auto Dealer Settings"):
		doc = frappe.get_doc("Auto Dealer Settings")
		if doc.default_company:
			return 1
	return 0

def has_records(doctype):
	"""
	Helper utility to check records for onboarding
	"""
	if frappe.db.exists("DocType", doctype):
		return 1 if frappe.db.count(doctype) > 0 else 0
	return 0
