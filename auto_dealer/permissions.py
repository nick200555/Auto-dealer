"""
Custom Permission Handlers
---------------------------
Implement row-level permission logic for sensitive DocTypes.
Registered in hooks.py under 'has_permission'.
"""

import frappe


def vehicle_permission(doc, ptype, user=None):
	"""
	Row-level permission for Vehicle DocType.
	- Sales Executive: can only see vehicles at their assigned branch
	- Sales Manager / Dealer Principal: can see all
	Returns True to allow, False to deny.
	"""
	if ptype not in ("read", "write", "create"):
		return True  # Allow for other types (delete, submit, etc.)

	user = user or frappe.session.user
	roles = frappe.get_roles(user)

	if "Sales Manager" in roles or "Dealer Principal" in roles or "System Manager" in roles:
		return True

	if "Sales Executive" in roles:
		# Get the executive's branch from the User record or HR module
		user_branch = frappe.db.get_value("User", user, "branch") or None
		if not user_branch:
			return True  # No restriction if branch not set
		return doc.branch == user_branch

	return True


def vehicle_sale_permission(doc, ptype, user=None):
	"""
	Row-level permission for Vehicle Sale.
	- Sales Executive: can only see their own sales
	- Others: unrestricted
	"""
	user = user or frappe.session.user
	roles = frappe.get_roles(user)

	if "Sales Manager" in roles or "Finance Manager" in roles or "Dealer Principal" in roles:
		return True

	if "Sales Executive" in roles and ptype == "read":
		return doc.sales_executive == user

	return True
