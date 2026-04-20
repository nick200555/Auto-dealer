"""
Daily Scheduled Tasks
----------------------
Wired from hooks.py scheduler_events → auto_dealer.tasks.daily.*

Tasks:
  1. update_days_in_stock   — Refresh days_in_stock for all active vehicles
  2. check_insurance_renewals — Notify expiring Insurance Policies (≤ 30 days)
  3. sync_marketplace_inventory — Push inventory to CarDekho
  4. send_emi_reminders     — WhatsApp reminders for EMI due in next 3 days
"""

import frappe
from frappe.utils import today, date_diff, add_days


def update_days_in_stock():
	"""Recalculate days_in_stock for every non-Sold/Scrap vehicle."""
	vehicles = frappe.get_all(
		"Vehicle",
		filters={"status": ["not in", ["Sold", "Scrap"]], "docstatus": 1},
		fields=["name", "purchase_date"],
	)
	updated = 0
	for v in vehicles:
		if v.get("purchase_date"):
			days = date_diff(today(), v["purchase_date"])
			frappe.db.set_value("Vehicle", v["name"], "days_in_stock", days, update_modified=False)
			updated += 1
	frappe.db.commit()
	frappe.logger("auto_dealer").info(f"[Daily] Updated days_in_stock for {updated} vehicles.")


def check_insurance_renewals():
	"""
	Find active Insurance Policies expiring within 30 days.
	Send WhatsApp renewal reminders for those not yet reminded.
	"""
	cutoff_date = add_days(today(), 30)
	expiring = frappe.get_all(
		"Insurance Policy",
		filters={"status": "Active", "renewal_reminder_sent": 0, "end_date": ["<=", cutoff_date], "docstatus": 1},
		fields=["name"],
	)
	reminded = 0
	for rec in expiring:
		try:
			doc = frappe.get_doc("Insurance Policy", rec["name"])
			doc.send_renewal_reminder()
			reminded += 1
		except Exception:
			frappe.log_error(title=f"Renewal Reminder Failed: {rec['name']}", message=frappe.get_traceback())
	frappe.logger("auto_dealer").info(f"[Daily] Insurance renewal reminders sent: {reminded}/{len(expiring)}")


def sync_marketplace_inventory():
	"""Push all Available vehicles to CarDekho marketplace."""
	from auto_dealer.api.marketplace_sync import sync_all_inventory
	result = sync_all_inventory()
	frappe.logger("auto_dealer").info(f"[Daily] Marketplace sync: {result}")


def send_emi_reminders():
	"""WhatsApp reminders for EMI instalments due within 3 days or overdue."""
	due_cutoff = add_days(today(), 3)
	due_instalments = frappe.get_all(
		"EMI Schedule",
		filters={"status": ["in", ["Pending", "Partial", "Overdue"]], "due_date": ["<=", due_cutoff]},
		fields=["name"],
	)
	reminded = 0
	for rec in due_instalments:
		try:
			doc = frappe.get_doc("EMI Schedule", rec["name"])
			doc.send_due_reminder()
			reminded += 1
		except Exception:
			frappe.log_error(title=f"EMI Reminder Failed: {rec['name']}", message=frappe.get_traceback())
	frappe.logger("auto_dealer").info(f"[Daily] EMI reminders sent: {reminded}/{len(due_instalments)}")
