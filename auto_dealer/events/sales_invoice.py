"""
Sales Invoice Event Handlers
Thin wrappers wired via hooks.py doc_events.
"""
from auto_dealer.auto_dealer.overrides.sales_invoice import on_submit, on_cancel  # noqa: F401
