# Auto Dealer ERP — ERPNext v15+ Custom App

A comprehensive Frappe/ERPNext custom application for automobile dealership management.

## Features

- **🚗 Vehicle Inventory Management** — Full lifecycle tracking with VIN validation, days-in-stock, and status management
- **🧪 Test Drive Management** — Schedule, validate conflicts, capture feedback, and create follow-up tasks
- **💰 Vehicle Sale** — Complete sale workflow with EMI calculation (reducing-balance PMT formula), finance, and delivery
- **🔧 Service Job Card** — Workshop management with parts/labour billing, GST calculation, and next-service reminders
- **📋 Insurance Tracking** — Policy lifecycle management with automated renewal reminders
- **📊 EMI Schedule** — Auto-generated instalment tracking with overdue detection
- **🎯 Target vs Achievement** — Monthly sales targets with auto-fetched actuals and tiered incentive calculation
- **📡 API Integrations** — WhatsApp (Meta Cloud / MSG91 / WATI), Insurance provider, Loan DSA, CarDekho marketplace
- **📈 Reports** — Slow-Moving Inventory, OEM Stock Reconciliation, Sales vs Target
- **⚙️ Workflows** — Vehicle Sale (Draft → Booked → Finance → Delivery → Delivered), Service Job Card

## Directory Structure

```
auto_dealer/                  ← Frappe app root
├── setup.py
├── requirements.txt
├── pyproject.toml
└── auto_dealer/              ← Python package
    ├── __init__.py           ← Version string
    ├── hooks.py              ← App configuration hub
    ├── modules.txt
    ├── patches.txt
    ├── utils.py              ← Shared utilities + dashboard KPIs
    ├── permissions.py        ← Row-level permission handlers
    │
    ├── api/                  ← External API integrations
    │   ├── whatsapp.py       ← Meta / MSG91 / WATI
    │   ├── insurance.py      ← Insurance provider REST API
    │   ├── loan_dsa.py       ← Loan DSA partner API
    │   └── marketplace_sync.py ← CarDekho dealer API
    │
    ├── doctype/              ← Custom DocTypes
    │   ├── vehicle/
    │   ├── test_drive/
    │   ├── vehicle_sale/
    │   ├── service_job_card/
    │   ├── service_job_card_item/   ← Child table
    │   ├── service_job_card_labour/ ← Child table
    │   ├── vehicle_insurance/
    │   ├── emi_schedule/
    │   └── target_vs_achievement/
    │
    ├── report/               ← Script Reports
    │   ├── slow_moving_inventory/
    │   ├── oem_stock_report/
    │   └── sales_vs_target/
    │
    ├── workflow/             ← Workflow JSON fixtures
    │   ├── vehicle_sale_workflow.json
    │   └── service_job_card_workflow.json
    │
    ├── overrides/            ← ERPNext DocType class overrides
    │   ├── delivery_note.py
    │   ├── sales_invoice.py
    │   └── payment_entry.py
    │
    ├── events/               ← Doc event handler dispatchers
    │   ├── delivery_note.py
    │   ├── sales_invoice.py
    │   └── payment_entry.py
    │
    └── tasks/                ← Scheduled tasks
        ├── daily.py
        ├── weekly.py
        ├── monthly.py
        └── periodic.py

public/
├── js/
│   ├── auto_dealer.js        ← Global Desk JS (EMI calc, KPI helpers)
│   ├── vehicle.js
│   ├── test_drive.js
│   ├── vehicle_sale.js
│   └── service_job_card.js
└── css/
    └── auto_dealer.css       ← Status badges, KPI cards, EMI colours
```

## Installation

```bash
# Inside your Frappe bench directory
bench get-app auto_dealer /path/to/this/repo
bench --site your.site.name install-app auto_dealer
bench --site your.site.name migrate
```

## Configuration (site_config.json)

```json
{
  "whatsapp_provider": "meta",
  "whatsapp_api_token": "YOUR_META_TOKEN",
  "whatsapp_phone_number_id": "YOUR_PHONE_ID",

  "insurance_api_base_url": "https://api.insurer.com/v1",
  "insurance_api_key": "YOUR_KEY",
  "insurance_dealer_code": "DEALER001",

  "loan_dsa_api_url": "https://api.lender.com/v1",
  "loan_dsa_api_key": "YOUR_KEY",
  "loan_dsa_dealer_id": "DEALER001",

  "cardekho_api_url": "https://api.cardekho.com/dealer/v2",
  "cardekho_api_key": "YOUR_KEY",
  "cardekho_dealer_code": "CD001"
}
```

## Roles Required

| Role | Access |
|------|--------|
| Sales Executive | Create/edit vehicles, test drives, sales (own) |
| Sales Manager | Full sales access, reports, workflows |
| Service Advisor | Service job cards |
| Finance Manager | EMI schedules, loan approval |
| Insurance Manager | Insurance records |
| Dealer Principal | All reports, full read access |

## License

MIT
