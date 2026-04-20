"""
Periodic Tasks (Cron-based, every N hours)
-------------------------------------------
Tasks:
  1. sync_loan_status — Poll DSA API for pending loan application updates
"""

import frappe


def sync_loan_status():
	"""Sync loan application statuses from the DSA API (runs every 4 hours)."""
	from auto_dealer.auto_dealer.api.loan_dsa import sync_all_pending_applications
	result = sync_all_pending_applications()
	frappe.logger("auto_dealer").info(f"[Periodic Task] Loan DSA sync result: {result}")
