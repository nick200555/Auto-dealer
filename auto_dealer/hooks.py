from . import __version__ as app_version

# ─── App Identity ─────────────────────────────────────────────────────────────
app_name        = "auto_dealer"
app_title       = "Auto Dealer"
app_publisher   = "Your Company Name"
app_description = "Automobile Dealership Management for ERPNext"
app_email       = "admin@yourdealership.com"
app_license     = "MIT"
app_version     = app_version

required_apps = ["frappe", "erpnext"]

# ─── Override existing ERPNext DocTypes ───────────────────────────────────────
# Source: Section 4.1 of automobile_dealership_erpnext_v15 document
override_doctype_class = {
    "Sales Order": "auto_dealer.overrides.sales_order.CustomSalesOrder",
    "Customer":    "auto_dealer.overrides.customer.CustomCustomer",
}

# ─── Scheduled Tasks ──────────────────────────────────────────────────────────
# Source: Section 4.1 — hooks.py scheduler_events
scheduler_events = {
    "daily": [
        "auto_dealer.tasks.send_service_reminders",
        "auto_dealer.tasks.check_insurance_renewals",
        "auto_dealer.tasks.check_amc_renewals",
    ],
    "weekly":  ["auto_dealer.tasks.slow_moving_inventory_alert"],
    "monthly": ["auto_dealer.tasks.generate_oem_monthly_report"],
}

# ─── Document Events ──────────────────────────────────────────────────────────
# Source: Section 4.1 — hooks.py doc_events
doc_events = {
    "Vehicle Sale": {
        "on_submit": [
            "auto_dealer.events.vehicle_sale.on_submit",
            "auto_dealer.events.vehicle_sale.trigger_whatsapp_confirmation",
        ],
    },
    "Service Job Card": {
        "on_submit": "auto_dealer.events.service_job_card.on_submit",
    },
}

# ─── Fixtures ─────────────────────────────────────────────────────────────────
# Source: Section 4.1 — hooks.py fixtures
fixtures = [
    {"dt": "Role", "filters": [["name", "in", [
        "Dealer Admin",
        "DMS Manager",
        "Sales Consultant",
        "Service Advisor",
        "Workshop Technician",
        "Finance Executive",
    ]]]},
    {"dt": "Workflow"},
    {"dt": "Print Format"},
    {"dt": "Custom Field"},
]

# ─── Desk / App UI ────────────────────────────────────────────────────────────
app_include_js  = ["/assets/auto_dealer/js/auto_dealer.js"]
app_include_css = ["/assets/auto_dealer/css/auto_dealer.css"]

doctype_js = {
    "Vehicle":          "public/js/vehicle.js",
    "Test Drive":       "public/js/test_drive.js",
    "Vehicle Sale":     "public/js/vehicle_sale.js",
    "Service Job Card": "public/js/service_job_card.js",
}

# ─── Jinja Filters ────────────────────────────────────────────────────────────
jinja = {
    "methods": [
        "auto_dealer.utils.format_vin",
    ]
}
