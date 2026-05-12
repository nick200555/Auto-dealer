# 📘 StartupOS — Standard Operating Procedure (SOP)
### Functional Guide for Indian Startup Founders

---

> **Document Version:** 1.0  
> **Application:** StartupOS on ERPNext v15  
> **Audience:** Startup Founders, CFOs, Legal Teams, Operators  
> **Support:** support@startupos.in

---

## 📋 Table of Contents

1. [Getting Started — First Login](#1-getting-started--first-login)
2. [Module 1 — Compliance Hub](#2-module-1--compliance-hub)
3. [Module 2 — Fundraising OS](#3-module-2--fundraising-os)
4. [Module 3 — Cap Table Management](#4-module-3--cap-table-management)
5. [Module 4 — Financial & Runway Intelligence](#5-module-4--financial--runway-intelligence)
6. [Module 5 — Legal & Governance](#6-module-5--legal--governance)
7. [Module 6 — AI Startup Assistant](#7-module-6--ai-startup-assistant)
8. [Daily / Weekly / Monthly Operating Checklist](#8-daily--weekly--monthly-operating-checklist)
9. [User Roles & Who Does What](#9-user-roles--who-does-what)
10. [Frequently Asked Questions](#10-frequently-asked-questions)

---

## 1. Getting Started — First Login

### 1.1 Access the Application

1. Open your browser and go to your StartupOS URL:  
   `https://startup.yourdomain.org`
2. Login with your ERPNext credentials (provided by your administrator).
3. On the left sidebar, click **StartupOS** workspace.
4. You will see the **StartupOS Dashboard** with 4 quick-access shortcuts at the top:
   - 🟠 Compliance Score
   - 🔵 Runway Model
   - 🟢 Fundraising Pipeline
   - 🟣 Cap Table

---

### 1.2 Initial Company Setup (One-Time — Admin Only)

> **Who does this:** System Administrator or Startup Founder (first time only)

| Step | Action | Where |
|---|---|---|
| 1 | Create your Company | ERPNext → Accounting → Company |
| 2 | Set your Financial Year | ERPNext → Accounting → Fiscal Year |
| 3 | Seed the Regulatory Calendar | StartupOS → Compliance Hub → Compliance Alert Setting |
| 4 | Run Demo Data (optional) | `bench execute startup_os.setup.demo.run` |

---

### 1.3 Assign User Roles

> **Who does this:** Administrator

Go to **ERPNext → HR → User** and assign each person their role:

| Role | Assign To |
|---|---|
| Startup Founder | CEO / Co-Founders |
| Startup CFO | Finance Head / CFO |
| Startup Legal | Legal Counsel / Company Secretary |
| Startup Investor | Investor (portal access only) |
| Startup Admin | IT Admin / Operations Lead |

---

## 2. Module 1 — Compliance Hub

> **Purpose:** Never miss a filing deadline. Track DPIIT recognition, ROC filings, GST, TDS, and company health score in one place.

---

### 2.1 SOP — Register DPIIT Recognition

**Who:** Founder / Legal  
**When:** At incorporation or when applying for Startup India recognition

| Step | Action |
|---|---|
| 1 | Go to **Compliance Hub → DPIIT Application** |
| 2 | Click **+ New** |
| 3 | Select your **Company** |
| 4 | Fill in **Application Number** (from DIPP portal) |
| 5 | Set **Status** = "Pending" (change to "Recognized" once certificate received) |
| 6 | Open the **Documents** tab and tick each uploaded document |
| 7 | Attach the **Recognition Certificate** in the file field |
| 8 | Click **Save** |

✅ **Expected Result:** DPIIT Application appears on your dashboard. Compliance Score auto-updates to reflect recognition (+20 points).

---

### 2.2 SOP — Complete Incorporation Checklist

**Who:** Legal / Founder  
**When:** Within first 30 days of incorporation

| Step | Action |
|---|---|
| 1 | Go to **Compliance Hub → Incorporation Checklist** |
| 2 | Click **+ New** |
| 3 | Select your **Company** |
| 4 | Tick each completed registration: PAN, TAN, INC-20A, GST, Shops & Establishment |
| 5 | Add other registrations in the text field (e.g., MSME, Startup India Portal) |
| 6 | Set **Status** = Complete |
| 7 | Click **Save** |

✅ **Expected Result:** Checklist marked complete. Compliance Hub shows green status for incorporation.

---

### 2.3 SOP — Set Up Regulatory Calendar

**Who:** Legal / Admin  
**When:** Once at setup; review quarterly

| Step | Action |
|---|---|
| 1 | Go to **Compliance Hub → Regulatory Calendar** |
| 2 | Click **+ New** for each filing event |
| 3 | Fill: Filing Name, Form Type, Due Date, Status |
| 4 | Repeat for: GST returns (monthly), TDS returns (quarterly), ITR (annual), MGT-7, AOC-4 |

> **Tip:** You can auto-seed standard filings by running:  
> `bench execute startup_os.compliance.api.seed_regulatory_calendar --kwargs '{"company": "Your Company"}'`

**Filing Calendar — Key Annual Dates:**

| Filing | Form | Typical Due Date |
|---|---|---|
| GST Return | GSTR-1 / 3B | 11th / 20th every month |
| TDS Return Q1 | 26Q / 24Q | 31st July |
| TDS Return Q2 | 26Q / 24Q | 31st October |
| TDS Return Q3 | 26Q / 24Q | 31st January |
| TDS Return Q4 | 26Q / 24Q | 31st May |
| Annual Return | MGT-7 / 7A | 60 days from AGM |
| Financial Statements | AOC-4 | 30 days from AGM |
| Auditor Appointment | ADT-1 | 15 days from AGM |
| Income Tax Return | ITR-6 | 31st October |

---

### 2.4 SOP — Mark a Filing as Complete

**Who:** Legal / CFO  
**When:** After every filing is submitted

| Step | Action |
|---|---|
| 1 | Go to **Regulatory Calendar** |
| 2 | Open the relevant filing record |
| 3 | Change **Status** from "Upcoming" → "Filed" |
| 4 | Enter **Completion Date** |
| 5 | Attach acknowledgement / receipt (optional) |
| 6 | Save |

✅ **Expected Result:** Filing marked complete. Compliance Score auto-updates. Alerts stop for that filing.

---

### 2.5 SOP — Read Your Compliance Score

**Who:** Founder / CFO  
**When:** Monthly review

1. Go to **Compliance Hub → Compliance Score**
2. Open your company's record
3. Read the **Score (0–100)** and **Score Breakdown** table

| Score Range | Status |
|---|---|
| 90–100 | 🟢 Excellent |
| 75–89 | 🟡 Good |
| 50–74 | 🟠 Needs Attention |
| Below 50 | 🔴 Critical — take action |

> **Note:** Score is auto-recomputed daily by the system scheduler.

---

## 3. Module 2 — Fundraising OS

> **Purpose:** Manage your entire investor relationship — from first email to money-in-bank — with a structured CRM pipeline.

---

### 3.1 SOP — Add a New Investor

**Who:** Founder  
**When:** Whenever you identify a new target investor

| Step | Action |
|---|---|
| 1 | Go to **Fundraising OS → Investor** |
| 2 | Click **+ New** |
| 3 | Fill Investor Name, Type (Angel / VC / PE / Family Office) |
| 4 | Enter Contact Email, Website, LinkedIn |
| 5 | Add notes about investment thesis, ticket size |
| 6 | Save |

Then add individual contacts:

| Step | Action |
|---|---|
| 1 | Go to **Investor Contact → + New** |
| 2 | Link the **Investor** (firm) |
| 3 | Add partner/associate name, email, phone |
| 4 | Tick **Lead Contact** for the primary contact |

---

### 3.2 SOP — Track a Deal in the Pipeline

**Who:** Founder  
**When:** After every investor conversation

| Step | Action |
|---|---|
| 1 | Go to **Fundraising OS → Fundraising Opportunity** |
| 2 | Click **+ New** |
| 3 | Select **Investor**, enter target **Amount (₹)** |
| 4 | Set **Stage** based on where you are |
| 5 | Enter **Close Date** (estimated) and **Probability (%)** |
| 6 | Add notes about the conversation |
| 7 | Save |

**The 7 Deal Stages:**

```
Intro ──► Meeting ──► Due Diligence ──► Term Sheet ──► Closing ──►┬── Closed Won ✅
                                                                    └── Passed ❌
```

**Update stage after every interaction:**

| Stage | When to Move |
|---|---|
| Intro | Email sent, LinkedIn connection made |
| Meeting | First call / pitch meeting done |
| Due Diligence | Investor has requested data room |
| Term Sheet | Term sheet / LOI received |
| Closing | Legals being finalized |
| Closed Won | Money received, allotment done |
| Passed | Investor declined |

---

### 3.3 SOP — Generate an Investor Update

**Who:** Founder / CFO  
**When:** Monthly (1st–5th of every month)

| Step | Action |
|---|---|
| 1 | Go to **Fundraising OS → Investor Update** |
| 2 | Click **+ New** (or system auto-creates a draft) |
| 3 | Set **Period Start** and **Period End** (last month) |
| 4 | The AI pre-fills MRR, burn rate, runway in the update text |
| 5 | Edit the narrative — add wins, challenges, ask |
| 6 | Review and change **Status** to "Sent" after distributing |

**Standard Investor Update Template:**

```
Subject: [Company Name] — Monthly Update [Month Year]

TL;DR: MRR: ₹X | Growth: Y% | Runway: Z months | Highlight

1. Key Metrics
2. Wins This Month
3. Challenges / Help Needed
4. Fundraising Update
5. Next Month Priorities
```

---

### 3.4 SOP — Store a Pitch Deck Version

**Who:** Founder  
**When:** Every time you update the deck

| Step | Action |
|---|---|
| 1 | Go to **Pitch Deck Vault → + New** |
| 2 | Enter version name (e.g., "Seed Deck v3 – April 2025") |
| 3 | Attach the PDF file |
| 4 | Add notes about what changed |
| 5 | Save |

---

## 4. Module 3 — Cap Table Management

> **Purpose:** Maintain a 100% accurate digital cap table — who owns what, what ESOP options are outstanding, and what happens to ownership after the next round.

---

### 4.1 SOP — Add Shareholders at Incorporation

**Who:** Founder / Legal  
**When:** At incorporation (one-time setup)

| Step | Action |
|---|---|
| 1 | Go to **Cap Table → Shareholder → + New** |
| 2 | Enter **Shareholder Name** (e.g., "Ravi Kumar (Founder)") |
| 3 | Set **Shareholder Type** (Founder / Investor / Employee / Company) |
| 4 | Link to **Company** |
| 5 | Save |
| 6 | Repeat for each founder and ESOP Pool |

---

### 4.2 SOP — Record an Equity Transaction

**Who:** Legal / CFO  
**When:** At incorporation, each funding round, any transfer or buyback

| Step | Action |
|---|---|
| 1 | Go to **Equity Transaction → + New** |
| 2 | Select **Company** and **Shareholder** |
| 3 | Set **Transaction Type**: Issuance / Transfer / Buyback / Cancellation |
| 4 | Set **Share Type**: Equity / CCPS / OCD / Warrants |
| 5 | Enter **Quantity** and **Price Per Share** |
| 6 | Enter **Date** of the transaction |
| 7 | Save |

✅ **Expected Result:** Ownership percentages auto-recompute for all shareholders.

**Common Transaction Types:**

| Event | Transaction Type | Share Type |
|---|---|---|
| Founders receive shares at incorporation | Issuance | Equity |
| Angel / VC invests at seed round | Issuance | CCPS |
| Founder transfers shares to trust | Transfer | Equity |
| Company buys back ESOP shares | Buyback | Equity |
| Employee exercises ESOP options | Issuance | Equity |

---

### 4.3 SOP — Create an ESOP Grant

**Who:** HR / Legal  
**When:** When giving stock options to an employee

| Step | Action |
|---|---|
| 1 | Go to **ESOP Grant → + New** |
| 2 | Select the **Employee** |
| 3 | Enter **Quantity** (number of options) |
| 4 | Set **Grant Date** |
| 5 | Set **Vesting Start Date** (usually same as grant date) |
| 6 | Set **Cliff Period** (typically 12 months) |
| 7 | Set **Vesting Period** (typically 48 months = 4 years) |
| 8 | Save |

✅ **Expected Result:** System automatically generates the full monthly vesting schedule. Employee gets options in equal monthly installments after the cliff.

**Standard ESOP Vesting (4yr / 1yr cliff):**
```
Month 0–11:   0 options vest (cliff period)
Month 12:     25% vest in one go (cliff release)
Month 13–48:  Remaining 75% vest monthly (2.08%/month)
```

---

### 4.4 SOP — Run a Dilution Scenario ("What If" Analysis)

**Who:** Founder / CFO  
**When:** Before any fundraising round to understand ownership impact

Use the API or ask your admin to run:

```
POST startup_os.cap_table.api.run_dilution_scenario
Body: {
  "company": "Your Company",
  "new_amount": 30000000,        ← New money being raised (₹3 Cr)
  "pre_money": 200000000         ← Pre-money valuation (₹20 Cr)
}
```

**Example Output:**
```
Pre-Money Valuation:  ₹2,00,00,000
New Investment:       ₹30,00,000
Post-Money:           ₹2,30,00,000
New Investor %:       13.04%

                  Before    After
Founder 1 (Ravi): 50.0%  → 43.5%
Founder 2 (Priya):40.0%  → 34.8%
Angel Investor:   10.0%  →  8.7%
New Investor:      0.0%  → 13.04%
```

---

### 4.5 SOP — Issue a Share Certificate

**Who:** Legal / Company Secretary  
**When:** After every allotment of shares

| Step | Action |
|---|---|
| 1 | Go to **Share Certificate → + New** |
| 2 | Select **Shareholder** and **Company** |
| 3 | Enter **Certificate Number** (sequential) |
| 4 | Enter **From Share No.** and **To Share No.** |
| 5 | Enter **Quantity**, **Issue Date**, **Price Per Share** |
| 6 | Attach the signed certificate PDF |
| 7 | Save |

---

## 5. Module 4 — Financial & Runway Intelligence

> **Purpose:** Know exactly how much money you have, how fast you're spending it, how long you'll last, and whether your unit economics are healthy.

---

### 5.1 SOP — Set Up Your Runway Model

**Who:** CFO / Founder  
**When:** One-time setup, then monthly sync

| Step | Action |
|---|---|
| 1 | Go to **Financial & Runway → Runway Model → + New** |
| 2 | Select **Company** |
| 3 | Enter **Cash Balance** (total cash in bank today, ₹) |
| 4 | Enter **Base Burn** (average monthly expenses, ₹) |
| 5 | System auto-calculates Base Runway |
| 6 | Save |

✅ **Expected Result:** System calculates 3 scenarios:

| Scenario | Formula | Meaning |
|---|---|---|
| Base Runway | Cash ÷ Base Burn | At current spending pace |
| Optimistic | Cash ÷ (Burn × 0.75) | If you cut costs by 25% |
| Pessimistic | Cash ÷ (Burn × 1.30) | If costs rise by 30% |

> **Sync with GL:** To auto-pull burn from ERPNext accounting ledger, run:  
> `bench execute startup_os.financial.api.sync_burn_rate --kwargs '{"company": "Your Company"}'`

---

### 5.2 SOP — Update Unit Economics (SaaS / Subscription)

**Who:** CFO  
**When:** Monthly or quarterly

| Step | Action |
|---|---|
| 1 | Go to **Financial & Runway → Unit Economics → + New (or open existing)** |
| 2 | Enter **ARPU** (Average Revenue Per User per month, ₹) |
| 3 | Enter **CAC** (Customer Acquisition Cost, ₹) |
| 4 | Enter **Churn Rate** (% of customers lost each month) |
| 5 | System auto-calculates: LTV, Payback Period, LTV:CAC ratio |
| 6 | Save |

**Key Benchmarks for Indian SaaS / B2B:**

| Metric | Healthy | Warning |
|---|---|---|
| Monthly Churn | < 2% | > 5% |
| LTV:CAC | > 3x | < 1.5x |
| Payback Period | < 12 months | > 18 months |
| Magic Number | > 0.75 | < 0.5 |

---

### 5.3 SOP — Create a Budget Plan

**Who:** CFO  
**When:** Start of each quarter / financial year

| Step | Action |
|---|---|
| 1 | Go to **Budget Plan → + New** |
| 2 | Enter **Company** and **Budget Period** (e.g., "Q1 FY2025-26") |
| 3 | In the **Budget Line Items** table, add each category |
| 4 | Enter **Budgeted Amount** for each category |
| 5 | Fill **Actual Amount** monthly as actuals come in |
| 6 | System auto-calculates **Variance** |
| 7 | Save |

**Standard Budget Categories:**

| Category | Examples |
|---|---|
| Payroll | Salaries, PF, ESIC, bonuses |
| Technology | AWS, SaaS tools, GitHub, Zoho |
| Sales & Marketing | Ads, events, content |
| Office & Admin | Rent, utilities, housekeeping |
| Legal & Compliance | CA, CS, lawyer fees |
| Travel | Client visits, conferences |
| Miscellaneous | Other expenses |

---

## 6. Module 5 — Legal & Governance

> **Purpose:** Run board meetings properly, track all legal agreements, protect your IP, and stay compliant with FEMA for foreign investments.

---

### 6.1 SOP — Schedule and Run a Board Meeting

**Who:** Founder / Company Secretary  
**When:** Minimum 4 times a year (Companies Act requirement)

**Step A — Schedule the Meeting:**

| Step | Action |
|---|---|
| 1 | Go to **Legal & Governance → Board Meeting → + New** |
| 2 | Select **Company** |
| 3 | Set **Meeting Date** (give 7-day notice to directors) |
| 4 | Write the **Agenda** in the rich text field |
| 5 | Set **Status** = "Scheduled" |
| 6 | Save and share the agenda with board members |

**Step B — Record Minutes After Meeting:**

| Step | Action |
|---|---|
| 1 | Go to **Board Minutes → + New** |
| 2 | Link to the **Board Meeting** |
| 3 | Fill in **Minutes** (what was discussed) |
| 4 | Fill in **Resolutions** (formal decisions taken) |
| 5 | Change Meeting status to "Completed" |
| 6 | Save |

> **Important:** Include at minimum — quorum confirmation, agenda items discussed, resolutions passed, and next meeting date.

---

### 6.2 SOP — Store a Contract

**Who:** Legal / Founder  
**When:** When signing any agreement

| Step | Action |
|---|---|
| 1 | Go to **Contract Document → + New** |
| 2 | Enter **Contract Name** (e.g., "NDA – Blume Ventures") |
| 3 | Select **Company** and enter **Party** (counterparty name) |
| 4 | Enter **Expiry Date** |
| 5 | Set **Status** = Active / Expired / Terminated |
| 6 | Attach the signed contract PDF |
| 7 | Save |

✅ System will alert you 30 days before expiry.

**Types of Contracts to Track:**

| Contract Type | Key Party |
|---|---|
| Shareholders Agreement (SHA) | All investors + founders |
| Investor Rights Agreement (IRA) | Lead investor |
| NDA | Potential investors, vendors |
| Employment Agreements | Key hires |
| Vendor / SaaS Agreements | AWS, Zoho, etc. |
| Office Lease | Landlord |
| Client Agreements | Customers |
| Co-founder Agreement | Co-founders |

---

### 6.3 SOP — Track Intellectual Property

**Who:** Legal  
**When:** When filing or receiving any IP registration

| Step | Action |
|---|---|
| 1 | Go to **IP Tracker → + New** |
| 2 | Enter **IP Name** (e.g., "BizAxl") |
| 3 | Select **IP Type**: Patent / Trademark / Copyright / Design |
| 4 | Set **Status**: Pending / Registered / Expired |
| 5 | Enter **Application Number** and **Filing Date** |
| 6 | Enter **Expiry Date** (10 years for TM from filing) |
| 7 | Attach certificate when received |

---

### 6.4 SOP — Track Foreign Investment Compliance (FEMA)

**Who:** Legal / CFO  
**When:** Every time you receive foreign investment

> **Required for all FDI under FEMA 20R — file FC-GPR within 30 days of allotment**

| Step | Action |
|---|---|
| 1 | Go to **FEMA FDI Tracker → + New** |
| 2 | Select **Company** and **Investor** |
| 3 | Enter **Round Name** and **Amount (INR equivalent)** |
| 4 | Set **FC-GPR Filing Status** = Pending → Filed → Acknowledged |
| 5 | Set **RBI Approval Required** (Yes for restricted sectors) |
| 6 | Attach the **Valuation Report** (CA certificate mandatory for FDI) |
| 7 | Update status as filings progress |

**FC-GPR Filing Timeline:**

```
Day 0:   Shares allotted to foreign investor
Day 1–30: File FC-GPR on RBI FIRMS portal
Day 30:  Acknowledgement received from authorized dealer
```

---

## 7. Module 6 — AI Startup Assistant

> **Purpose:** Get instant answers to Indian startup law, compliance, finance, and fundraising questions — powered by AI trained on Indian regulatory documents.

---

### 7.1 SOP — Ask the AI Assistant

**Who:** Any user  
**When:** Anytime you have a compliance, financial, or legal question

| Step | Action |
|---|---|
| 1 | Go to **AI Assistant → AI Chat Session → + New** |
| 2 | Type your question in plain English |
| 3 | The AI responds with context from your live company data |
| 4 | Previous chat history is saved per session |

**Sample Questions You Can Ask:**

```
🏛  Compliance
"When is my next ROC filing due?"
"Am I eligible for 80-IAC income tax exemption?"
"What documents do I need for DPIIT recognition?"
"Has my GST return been filed this month?"

💰  Fundraising
"What is the difference between CCPS and Equity shares?"
"What should I check before signing a term sheet?"
"What is a drag-along right?"

📊  Cap Table
"What will Priya's ownership be after we raise ₹5 Cr at ₹20 Cr pre-money?"
"How many options has Ravi vested so far?"

💸  Finance
"What is our current runway?"
"What is our LTV:CAC ratio?"
"Is our burn rate healthy for our stage?"

📄  Legal
"What is the lock-in period for foreign investment under FEMA?"
"What mandatory items must be in board meeting minutes?"
```

> **Note:** The AI Assistant requires OpenAI or Anthropic API key configured by your administrator. Contact support@startupos.in for setup.

---

## 8. Daily / Weekly / Monthly Operating Checklist

### 8.1 Daily (5 minutes)

| Task | Who | Where |
|---|---|---|
| ☐ Check compliance alerts in email/WhatsApp | Legal | Inbox |
| ☐ Update any deal stage that changed | Founder | Fundraising Pipeline |
| ☐ Log any new investor conversation | Founder | Fundraising Opportunity |

---

### 8.2 Weekly (15 minutes)

| Task | Who | Where |
|---|---|---|
| ☐ Review upcoming filing deadlines (next 30 days) | Legal | Regulatory Calendar |
| ☐ Update fundraising deal notes | Founder | Fundraising Opportunity |
| ☐ Check for expiring contracts | Legal | Contract Document |
| ☐ Review open ESOP vesting events | HR | ESOP Grant |

---

### 8.3 Monthly (1–2 hours)

| Task | Who | Where |
|---|---|---|
| ☐ Update cash balance in Runway Model | CFO | Runway Model |
| ☐ Sync burn rate from accounting | CFO | `sync_burn_rate` API |
| ☐ Update Unit Economics (MRR, churn, CAC) | CFO | Unit Economics |
| ☐ Update Budget Plan actuals | CFO | Budget Plan |
| ☐ Draft and send Investor Update | Founder | Investor Update |
| ☐ Mark filed compliance items as Complete | Legal | Regulatory Calendar |
| ☐ Review Compliance Score | Founder | Compliance Score |
| ☐ Issue share certificates if applicable | Legal | Share Certificate |

---

### 8.4 Quarterly (Half day)

| Task | Who | Where |
|---|---|---|
| ☐ Schedule Board Meeting (7-day notice) | CS / Founder | Board Meeting |
| ☐ Prepare board pack (financial summary, compliance, fundraising update) | CFO | All modules |
| ☐ File TDS Return | CFO | External |
| ☐ Update ESOP vested amounts | HR | ESOP Grant |
| ☐ Review cap table for accuracy | Legal | Equity Transaction |
| ☐ Verify all FEMA filings are acknowledged | Legal | FEMA FDI Tracker |

---

### 8.5 Annually (Full day)

| Task | Who | Where |
|---|---|---|
| ☐ File Annual Return MGT-7 / MGT-7A | CS | Regulatory Calendar |
| ☐ File Financial Statements AOC-4 | CS + CA | Regulatory Calendar |
| ☐ File Income Tax Return ITR-6 | CA | Regulatory Calendar |
| ☐ Appoint/Reappoint Auditor ADT-1 | CS | Regulatory Calendar |
| ☐ Renew DPIIT Recognition (if expired) | Founder | DPIIT Application |
| ☐ Update IP Tracker for renewals | Legal | IP Tracker |
| ☐ Archive old pitch deck versions | Founder | Pitch Deck Vault |

---

## 9. User Roles & Who Does What

| Feature | Founder | CFO | Legal | Investor | Admin |
|---|---|---|---|---|---|
| DPIIT Application | ✅ Full | 👁 Read | ✅ Full | ❌ | ✅ Full |
| Regulatory Calendar | ✅ Full | 👁 Read | ✅ Full | ❌ | ✅ Full |
| Compliance Score | 👁 Read | 👁 Read | 👁 Read | ❌ | ✅ Full |
| Investor CRM | ✅ Full | 👁 Read | ❌ | ❌ | ✅ Full |
| Fundraising Pipeline | ✅ Full | ✅ Full | ❌ | ❌ | ✅ Full |
| Investor Update | ✅ Full | ✅ Full | ❌ | 👁 Own | ✅ Full |
| Cap Table | 👁 Read | 👁 Read | ✅ Full | 👁 Own row | ✅ Full |
| Equity Transaction | ✅ Create | 👁 Read | ✅ Full | ❌ | ✅ Full |
| ESOP Grant | 👁 Read | 👁 Read | ✅ Full | ❌ | ✅ Full |
| Runway Model | 👁 Read | ✅ Full | ❌ | ❌ | ✅ Full |
| Unit Economics | 👁 Read | ✅ Full | ❌ | ❌ | ✅ Full |
| Budget Plan | 👁 Read | ✅ Full | ❌ | ❌ | ✅ Full |
| Board Meeting | ✅ Full | 👁 Read | ✅ Full | ❌ | ✅ Full |
| Contract Document | 👁 Read | ❌ | ✅ Full | ❌ | ✅ Full |
| FEMA FDI Tracker | 👁 Read | 👁 Read | ✅ Full | ❌ | ✅ Full |
| AI Assistant | ✅ Full | ✅ Full | ✅ Full | ❌ | ✅ Full |

---

## 10. Frequently Asked Questions

**Q1: I filed a GST return but compliance score didn't update. What do I do?**  
A: Open the Regulatory Calendar entry for that filing, change Status to "Filed", add the completion date, and save. The score updates automatically overnight or you can force it via `bench execute startup_os.compliance.utils.compute_compliance_scores`.

---

**Q2: My Runway Model shows wrong burn. How do I fix it?**  
A: The burn rate auto-syncs from ERPNext's GL entries daily. Make sure all expenses are booked in ERPNext Accounting. You can also manually edit the **Base Burn** field in Runway Model for an immediate override.

---

**Q3: A new investor joined. How do I update the cap table?**  
A: Create a new **Shareholder** record for the investor, then create an **Equity Transaction** (type: Issuance, share type: CCPS or Equity) for the shares allotted. Ownership percentages auto-recalculate.

---

**Q4: How do I give an investor access to see their shareholding?**  
A: Create a User account in ERPNext for the investor, assign the **Startup Investor** role. They will see only their own rows in the cap table.

---

**Q5: The AI Assistant isn't responding. What's wrong?**  
A: This usually means the OpenAI API key is not configured. Ask your system admin to run:  
`bench --site yoursite.org set-config openai_api_key "sk-..."`  
Then restart bench.

---

**Q6: How do I know when an ESOP cliff date has passed for an employee?**  
A: Go to **ESOP Grant** and open the employee's grant. The vesting schedule table will show which months have status "Vested" vs "Pending". You can also ask the AI: *"Has [Employee Name]'s ESOP cliff date passed?"*

---

**Q7: Our DPIIT recognition is expiring. What do I do?**  
A: Open the **DPIIT Application** record, change Status to "Renewal Pending", and start the renewal process on the Startup India portal. Upload the renewal certificate once received and update the status to "Recognized".

---

**Q8: Board meeting minutes — what's mandatory?**  
A: Per Companies Act 2013, board minutes must include:
- Date, time, and venue
- Directors in attendance (quorum confirmed)
- Resolutions passed (with For/Against count)
- Signature of Chairman

Store all of this in the **Board Minutes** DocType.

---

**Q9: When do I need RBI approval for foreign investment?**  
A: You need prior RBI approval only for sectors on the Government Route (e.g., defense, media, banking). For most tech/SaaS startups under Automatic Route, you only need to file FC-GPR within 30 days — no prior approval needed. Always consult your CA/lawyer.

---

**Q10: How do I export the cap table as a PDF for investors?**  
A: Go to **Equity Transaction** list view, use the print format or contact your admin to run the cap table export API. A formatted PDF cap table is available via:  
`startup_os.cap_table.api.get_fully_diluted?company=YourCompany`

---

## 📞 Support & Contact

| Channel | Details |
|---|---|
| 📧 Email | support@startupos.in |
| 📖 Documentation | https://docs.startupos.in |
| 🐛 Bug Reports | https://github.com/balaji-001-gif/startups/issues |
| 📱 WhatsApp | +91-XXXXXXXXXX (BizAxl Support) |

---

*© 2024 StartupOS — Built with ❤️ for Indian Startup Founders*  
*Powered by Frappe Framework & ERPNext*
