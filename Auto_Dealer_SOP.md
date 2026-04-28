# 📘 Auto_Dealer — Standard Operating Procedure (SOP)
### Functional Guide for Automotive Dealership, Vehicle Sales & Service Operations

---

> **Document Version:** 1.0  
> **Application:** Auto_Dealer on ERPNext v15  
> **Audience:** Dealership Owners, Showroom Managers, Sales Executives, CRM Teams, Service Advisors, Finance Teams, Inventory Managers, Insurance Coordinators  
> **Support:** support@autodealer.com

---

## 📋 Table of Contents

1. [Getting Started — First Login](#1-getting-started--first-login)
2. [Module 1 — Vehicle Inventory & Showroom Management](#2-module-1--vehicle-inventory--showroom-management)
3. [Module 2 — Lead & Customer Relationship Management](#3-module-2--lead--customer-relationship-management)
4. [Module 3 — Vehicle Sales & Booking Management](#4-module-3--vehicle-sales--booking-management)
5. [Module 4 — Service & Workshop Operations](#5-module-4--service--workshop-operations)
6. [Module 5 — Finance, Insurance & Loan Management](#6-module-5--finance-insurance--loan-management)
7. [Module 6 — Spare Parts & Inventory Control](#7-module-6--spare-parts--inventory-control)
8. [Module 7 — Reports & Analytics](#8-module-7--reports--analytics)
9. [Daily / Weekly / Monthly Operating Checklist](#9-daily--weekly--monthly--quarterly--annual-operating-checklists)
10. [User Roles & Who Does What](#10-user-roles--who-does-what)
11. [Frequently Asked Questions](#11-frequently-asked-questions)
12. [Support & Contact](#12-support--contact)

---

## 1. Getting Started — First Login

### 1.1 Access the Application

1. Open your browser and go to your Auto_Dealer URL:  
   `https://dealer.yourdomain.com`
2. Login with your ERPNext credentials (provided by your administrator).
3. On the left sidebar, click the **Auto_Dealer** workspace.
4. You will see the **Dealership Dashboard** with 4 quick-access shortcuts at the top:
   - 🟠 Showroom Inventory
   - 🔵 Sales Pipeline & Leads
   - 🟢 Active Workshop Jobs
   - 🟣 Financial Overview

---

### 1.2 Initial Dealership Setup (One-Time — Admin Only)

> **Who does this:** System Administrator or Dealership Owner (first time only)

| Step | Action | Where |
|---|---|---|
| 1 | Create your Dealership Company | ERPNext → Accounting → Company |
| 2 | Add Showroom Locations (Branches) | Auto_Dealer → Setup → Branch Setting |
| 3 | Define Storage / Showroom Bins | ERPNext → Stock → Warehouse |
| 4 | Assign Shift Types / Schedulers | ERPNext → HR → Shift Type |
| 5 | Run Demo Data (optional) | `bench execute auto_dealer.setup.demo.run` |

---

### 1.3 Assign User Roles

> **Who does this:** Administrator

Go to **ERPNext → HR → User** and assign each person their role:

| Role | Assign To |
|---|---|
| Dealership Owner | CEO / Dealership Managing Director |
| Showroom Manager | Branch Manager / Showroom Lead |
| Sales Executive | Vehicle Sales Associates |
| CRM Executive | Front Desk / Telecallers / Relationship Managers |
| Service Advisor | Workshop Advisors / Service Consultants |
| Workshop Technician | Mechanics / Floor Technicians |
| Inventory Manager | Stock Yard Supervisors / Spare Parts Head |
| Finance Executive | Cashiers / Loan Coordinators |
| Insurance Coordinator| Dedicated Insurance Desk Staff |
| Customer Portal User | Customers (portal access only) |

---

## 2. Module 1 — Vehicle Inventory & Showroom Management

> **Purpose:** Maintain total control over vehicles in your inventory. Track chassis/VIN numbers, showroom allocations, demo cars, and transfer stock seamlessly across branches.

---

### 2.1 SOP — Create a Vehicle Master Entry

**Who:** Inventory Manager / Admin  
**When:** When a new vehicle model/variant is introduced by the manufacturer

| Step | Action |
|---|---|
| 1 | Go to **Vehicle Inventory → Vehicle Master** |
| 2 | Click **+ New** |
| 3 | Enter **Make** (e.g., Toyota), **Model** (e.g., Innova Crysta), and **Variant** (e.g., 2.4G AT) |
| 4 | Fill in Specifications (Engine CC, Fuel Type, Transmission) |
| 5 | Upload Vehicle Images |
| 6 | Set default pricing / ex-showroom values |
| 7 | Click **Save** |

✅ **Expected Result:** Vehicle Master is available for sales booking, test drives, and stock receipt.

---

### 2.2 SOP — Receive Vehicle / VIN Registration

**Who:** Inventory Manager  
**When:** Physical vehicles arrive from the OEM manufacturer at the stockyard

| Step | Action |
|---|---|
| 1 | Go to **Vehicle Inventory → Vehicle Inventory** |
| 2 | Click **+ New** |
| 3 | Select the mapped **Vehicle Master** |
| 4 | Scan or Enter the **VIN/Chassis Number** and **Engine Number** |
| 5 | Select current **Warehouse / Branch Allocation** |
| 6 | Enter **Color** and **Manufacture Year/Month** |
| 7 | Set **Status** = "In Stock" |
| 8 | Click **Save** and **Submit** |

✅ **Expected Result:** Vehicle is officially added to stock. Dealership stock count increases.

---

### 2.3 SOP — Allocate Showroom & Demo Vehicles

**Who:** Showroom Manager  
**When:** Moving stock from main yard to showroom floor display or marking as demo

| Step | Action |
|---|---|
| 1 | Go to **Vehicle Inventory → Showroom Allocation** |
| 2 | Click **+ New** |
| 3 | Select the target **VIN/Chassis Number** |
| 4 | Set Allocation Type: "Display Module" or "Demo/Test Drive" |
| 5 | Set the target **Showroom/Location** |
| 6 | Approver: **Showroom Manager** approves |
| 7 | Click **Save** and **Submit** |

✅ **Expected Result:** Vehicle is restricted from immediate sale and marked specifically for display or testing.

---

### 2.4 SOP — Inter-Branch Vehicle Transfer

**Who:** Inventory Manager / Showroom Manager  
**When:** Moving a specific car from Branch A to Branch B for an urgent customer delivery

| Step | Action |
|---|---|
| 1 | Go to **Vehicle Inventory → Vehicle Status Tracking** |
| 2 | Locate the VIN and click **Initiate Transfer** (creates Stock Entry) |
| 3 | Set Source Branch and Destination Branch |
| 4 | Attach transfer out / gate pass documentation |
| 5 | Click **Submit** |

✅ **Expected Result:** Destination branch assumes ownership of the vehicle inventory.

---

### 2.5 SOP — Test-Drive Vehicle Handling

**Who:** Showroom Manager / CRM Executive  
**When:** Registering a new Test Drive vehicle to the fleet

| Step | Action |
|---|---|
| 1 | Go to **Vehicle Inventory → Test Drive Vehicle** |
| 2 | Click **+ New** |
| 3 | Link existing VIN or add Temporary Registration Number |
| 4 | Input current Odometer Reading |
| 5 | Set **Status** = "Available" |
| 6 | Click **Save** |

---

## 3. Module 2 — Lead & Customer Relationship Management

> **Purpose:** Capture inquiries, assign leads to sales executives, schedule test drives, track exchange vehicles, and maximize conversion rates.

---

### 3.1 SOP — Capture a New Lead (Enquiry Registration)

**Who:** CRM Executive / Reception Desk  
**When:** A walk-in, phone call, or website inquiry occurs

| Step | Action |
|---|---|
| 1 | Go to **CRM → Sales Lead** |
| 2 | Click **+ New** |
| 3 | Enter Customer Name, Mobile, and Email |
| 4 | Select **Interested Vehicle** (from Vehicle Master) |
| 5 | Set Lead Source (Walk-in / Facebook / Referral / etc.) |
| 6 | Add **Follow-up Date** and interaction notes |
| 7 | Click **Save** |

✅ **Expected Result:** Lead added to Pipeline. Dashboard alerts prompt next actions.

---

### 3.2 SOP — Schedule a Test Drive

**Who:** Sales Executive / CRM  
**When:** Customer requests to test drive a vehicle

| Step | Action |
|---|---|
| 1 | From the **Sales Lead** record, click **Create → Test Drive Schedule** |
| 2 | Select the designated **Test Drive Vehicle** |
| 3 | Enter **Date and Time Slot** |
| 4 | Allocate a **Driver / Sales Executive** |
| 5 | Ask Customer for Driving License details & upload scan |
| 6 | Update **Status** = "Scheduled" → "Completed" (after drive) |
| 7 | Collect and enter customer feedback/rating |

---

### 3.3 SOP — Exchange Vehicle Evaluation

**Who:** Sales Executive / Evaluator  
**When:** The customer wishes to trade in their existing car

| Step | Action |
|---|---|
| 1 | From the **Sales Lead** record, click **Create → Exchange Evaluation** |
| 2 | Enter Old Car details (Make, Model, Year, Mileage) |
| 3 | Enter Evaluator's inspection notes (Body condition, Engine tech, Tires) |
| 4 | Specify **Expected Price (Customer)** vs **Offered Price (Dealership)** |
| 5 | Once negotiated, Update Status = "Accepted" |
| 6 | Click **Submit** |

✅ **Expected Result:** The offered exchange bonus is computed into their new vehicle quotation automatically.

---

### 3.4 SOP — Generate a Vehicle Quotation

**Who:** Sales Executive  
**When:** Presenting the pricing breakdown to the prospect

| Step | Action |
|---|---|
| 1 | From **Sales Lead**, click **Create → Vehicle Quotation** |
| 2 | Select the exact **Variant** and **Color Preference** |
| 3 | Add standard pricing: Ex-Showroom, RTO/Registration, Insurance |
| 4 | Add optional **Accessory Package**, Extended Warranty, AMC |
| 5 | Apply Exchange Discount (if applicable) & Corporate Bonus |
| 6 | Print generating the standard Dealership PDF |
| 7 | Handover or Email quotation directly to the Customer |

---

## 4. Module 3 — Vehicle Sales & Booking Management

> **Purpose:** Convert leads to bookings, handle payments, assign specific chassis numbers, attach accessories, inspect vehicles (PDI), and execute successful deliveries.

---

### 4.1 SOP — Process a Vehicle Booking

**Workflow:** Customer Enquiry → Test Drive → Quotation → **Vehicle Booking**

**Who:** Sales Executive / Cashier  
**When:** Customer pays the booking token advance

| Step | Action |
|---|---|
| 1 | Go to **Sales → Vehicle Booking** |
| 2 | Click **+ New** |
| 3 | Link the **Sales Lead** / **Customer** |
| 4 | Select the promised **Vehicle Master** variant and color |
| 5 | Capture **Booking Amount** received (e.g., ₹50,000) & Payment Mode |
| 6 | Generate the Booking Receipt (Advance Payment Entry) |
| 7 | Set **Status** = "Booked" |
| 8 | Click **Submit** |

✅ **Expected Result:** Vehicle Booking record is confirmed. Lead converts to Customer automatically. SMS/Email confirmation triggered.

---

### 4.2 SOP — Assing a VIN / Chassis to a Booking

**Who:** Showroom Manager / Sales Exec  
**When:** Matching a customer's booking to physical vehicle availability

| Step | Action |
|---|---|
| 1 | Open the **Vehicle Booking** |
| 2 | Go to the **Chassis Assignment** section |
| 3 | Click **Fetch Available VINs** |
| 4 | Select the exact physical **Vehicle Inventory** (VIN) from the yard |
| 5 | Click **Update & Lock Chassis** |

✅ **Expected Result:** The selected VIN is removed from general sale availability and reserved specifically for this customer.

---

### 4.3 SOP — Perform PDI (Pre-Delivery Inspection)

**Who:** Workshop Technician / Showroom Manager  
**When:** 24–48 hours prior to delivery to ensure vehicle quality

| Step | Action |
|---|---|
| 1 | Go to **Sales → PDI Checklist** |
| 2 | Click **+ New** |
| 3 | Select the allocated **VIN** |
| 4 | Check off standard items (Electricals, Fluids, Scratches, Tools, Documents) |
| 5 | Note any defects. If defects exist, Status = "Failed / Sent to Workshop" |
| 6 | Once resolved, set Status = "Passed" |
| 7 | Sign and **Submit** |

---

### 4.4 SOP — Accessory Package Assignment

**Who:** Sales Executive / Parts Team  
**When:** Adding customer’s requested floor mats, alloys, stereo before delivery

| Step | Action |
|---|---|
| 1 | Go to **Sales → Accessory Package** |
| 2 | Select the **Customer & Booking** |
| 3 | Choose standard kits or add individual spare parts (Seat covers, mud flaps) |
| 4 | Issue materials from the Spare Parts Warehouse |
| 5 | Associate labor costs for fitting |
| 6 | **Save and Submit** |

✅ **Expected Result:** Accessory stock is reduced. Accessory amounts are added to the final Sales Invoice.

---

### 4.5 SOP — Execute Vehicle Delivery

**Who:** Sales Executive / Showroom Manager  
**When:** Balance payment is clear, Registration/RTO is done, car is ready

| Step | Action |
|---|---|
| 1 | Go to **Sales → Vehicle Delivery** |
| 2 | Click **+ New** |
| 3 | Link the **Vehicle Booking** |
| 4 | Ensure Pre-conditions show green (Fully Paid, PDI Passed, Insurance active) |
| 5 | Upload gate pass, delivery photo, and RTO receipt/RC copy |
| 6 | Generate Delivery Challan (Sales Invoice) |
| 7 | Set **Status** = "Delivered" |
| 8 | Click **Submit** |

✅ **Expected Result:** The VIN status officially updates to "Sold". Guarantee/Warranty records are auto-created.

---

### 4.6 SOP — Cancel a Booking & Refund

**Who:** Showroom Manager / Finance  
**When:** A customer cancels their intent to purchase

| Step | Action |
|---|---|
| 1 | Open the **Vehicle Booking** |
| 2 | Click **Cancel Booking** button |
| 3 | Enter Cancellation Reason (Finance Rejected, Changed Mind, Delayed) |
| 4 | Release the associated VIN back into stock |
| 5 | Finance Team processes the **Refund Handling** (minus any cancellation fee) |
| 6 | Complete negative Payment Entry. |

---

## 5. Module 4 — Service & Workshop Operations

> **Purpose:** Run the garage efficiently—manage service appointments, open job cards, assign mechanics, process warranty claims, and manage AMC service packages.

---

### 5.1 SOP — Book a Service Appointment

**Who:** Service Advisor / CRM  
**When:** Customer calls or uses portal to schedule maintenance

| Step | Action |
|---|---|
| 1 | Go to **Workshop → Workshop Queue / Appointments** |
| 2 | Select Customer and Vehicle (Previous VIN search or License Plate) |
| 3 | Log the exact **Customer Complaint / Service Request** |
| 4 | Assign preferred Date and Time slot |
| 5 | Save Appointment |

---

### 5.2 SOP — Open a Service Job Card

**Workflow:** Appointment → Job Card → Investigation → Approvals → Execution

**Who:** Service Advisor  
**When:** Vehicle physically arrives at the workshop

| Step | Action |
|---|---|
| 1 | Go to **Workshop → Service Job Card** |
| 2 | Click **+ New** (Or fetch from Appointment) |
| 3 | Capture **Odometer In**, **Fuel Level**, and **Visual Inspection** damages |
| 4 | Add standard labor operations / complaint resolutions |
| 5 | Estimate Parts & Labor costs |
| 6 | Provide **Service Estimate Approval** directly to Customer (SMS/WhatsApp link) |
| 7 | Set Status = "Open" |

---

### 5.3 SOP — Manage Workshop Floor & Assign Technician

**Who:** Workshop Manager  
**When:** Handing out daily service jobs to mechanics

| Step | Action |
|---|---|
| 1 | Open **Service Job Card** |
| 2 | Go to Technician Assignment section |
| 3 | Assign specific **Workshop Technician** name |
| 4 | Track time log if required |
| 5 | The Technician physically requests parts to complete the job |

✅ **Expected Result:** Workshop dashboard correctly maps efficiency and load across all bays/mechanics.

---

### 5.4 SOP — Warranty Claim Handling

**Who:** Service Advisor / Warranty Manager  
**When:** Replacing a defective part covered under OEM warranty

| Step | Action |
|---|---|
| 1 | Go to **Workshop → Warranty Claim** |
| 2 | Click **+ New** |
| 3 | Enter **VIN**, **Customer**, and exact **Failed Part Number** |
| 4 | Attach diagnostic evidence / photos required by Manufacturer |
| 5 | Set Status = "Pending Approval" (Waits for OEM system response) |
| 6 | Upon OEM approval, update Status = "Approved" |
| 7 | Replace part free of cost on Job Card; bill cost directly to OEM (Journal Entry) |

---

### 5.5 SOP — Complete Service & Invoicing

**Who:** Service Advisor / Cashier  
**When:** Mechanic completes work, ready for car to be washed / delivered

| Step | Action |
|---|---|
| 1 | Technician marks tasks = "Completed" |
| 2 | Service Advisor updates **Service Job Card** to "Completed" |
| 3 | Verify all parts issued have been accurately tallied |
| 4 | Click **Create Sales Invoice** |
| 5 | Receive Payment. Attach gate pass |
| 6 | Hand over keys. Submit Job Card |

✅ **Expected Result:** Vehicle service history tracking automatically updates with the latest services performed.

---

## 6. Module 5 — Finance, Insurance & Loan Management

> **Purpose:** Secure funding for vehicle purchases, map out EMI strategies with finance partners, and maintain an active insurance policy ledger with renewal alerts.

---

### 6.1 SOP — Process a Vehicle Loan Application

**Who:** Finance Executive  
**When:** Customer finances their new vehicle instead of direct cash payment

| Step | Action |
|---|---|
| 1 | Go to **Finance & Insurance → Vehicle Loan Application** |
| 2 | Select the **Customer / Vehicle Booking** |
| 3 | Enter Total Loan Required |
| 4 | Select **Finance Partner** (e.g., HDFC Auto Loan, SBI, Bajaj Finance) |
| 5 | Upload CIBIL / KYC docs via the document uploader |
| 6 | Set workflow: "Application Logged" → "Approved/Sanctioned" |
| 7 | Once sanctioned, enter the Disbursement DO (Delivery Order) Receipt |

---

### 6.2 SOP — Issue a New Insurance Policy

**Who:** Insurance Coordinator  
**When:** Car is sold and must be insured before hitting the road

| Step | Action |
|---|---|
| 1 | Go to **Finance & Insurance → Insurance Policy** |
| 2 | Link to the **Vehicle Inventory (VIN)** and Customer |
| 3 | Select Insurance Provider (e.g., ICICI Lombard, Tata AIG) |
| 4 | Enter **Policy Number**, Premium Amount, Deductible limits |
| 5 | Set **Start Date** and **Expiry Date** |
| 6 | Attach final policy schedule PDF |
| 7 | Save & Submit |

✅ **Expected Result:** Policy active. Alerts will automatically generate 30/15 days before the expiration date for follow-up.

---

## 7. Module 6 — Spare Parts & Inventory Control

> **Purpose:** Never let a repair pause due to lack of spare parts. Centralize part procurement, warranty stocking, batch tracking, and internal garage issuance.

---

### 7.1 SOP — SPARE PART ISSUE (Internal Consumption)

**Who:** Store Manager  
**When:** Technician urgently needs a component for an active Job Card

| Step | Action |
|---|---|
| 1 | Go to **Inventory → Spare Part Issue** |
| 2 | Click **+ New** |
| 3 | Link the specific **Service Job Card** |
| 4 | Scan or select the **Spare Part Master** item |
| 5 | Deduct Quantity |
| 6 | Select target technician |
| 7 | Submit form |

✅ **Expected Result:** Stock natively deducts. Value is linked back to the customer's repair invoice automatically.

---

### 7.2 SOP — Inward Supplier Stock / Low Stock Replenishment

**Who:** Inventory Manager  
**When:** Receiving monthly OEM spare part deliveries

| Step | Action |
|---|---|
| 1 | Review **Low Stock Alerts** dashboard |
| 2 | Issue Purchase Receipt against the OEM Purchase Order |
| 3 | Update **Supplier Parts Mapping** if a local vendor is substituted |
| 4 | Ensure correct valuation rates are entered |
| 5 | Submit to accept into current warehouse |

---

## 8. Module 7 — Reports & Analytics

> **Purpose:** Gain deep visibility into branch-wise performance, technician efficiency, aging inventory, and profitability. Use ERPNext dashboards dynamically.

**Standard Reports Included:**

- **Vehicle Sales Dashboard:** Monthly sales tracking separated by Model/Variant, Branch, and Executive performance.
- **Showroom Performance Analytics:** Walk-in traffic matched to conversion ratios for the month.
- **Lead Conversion Report:** Sales funnels showing Drop-offs, Test-Drive conversions, and Win rates.
- **Service Revenue Dashboard:** Parts vs Labor split, daily RO (Repair Order) volume, total revenue per bay.
- **Technician Productivity Report:** Time logged per mechanic vs cars dispatched on time (First-time-fix ratio).
- **Insurance Renewal Tracker:** List of all policies expiring next month categorized by probability of closure.
- **Branch-Wise Profitability Dashboard:** Compare revenue drivers (Sale + Spares + Labor) vs overhead inputs.

**To Run a Report:**  
Navigate to the specified Module, locate the `Reports` section at the bottom, configure date filters and branch filters, then export to PDF/CSV.

---

## 9. Daily / Weekly / Monthly / Quarterly / Annual Operating Checklists

### 9.1 Daily Checklist
| Task | Who | Where |
|---|---|---|
| ☐ Showroom inventory physical count & visual review | Showroom Mgr | Vehicle Inventory |
| ☐ Review pending lead follow-ups & missed calls | CRM Exec | CRM Pipeline |
| ☐ Review daily service appointments & check-ins | Service Advisor | Workshop Queue |
| ☐ Monitor workshop queue load vs current capacity | Workshop Mgr | Service Job Card |
| ☐ Audit pending deliveries & accessory fittings | Sales Exec | Vehicle Delivery |

### 9.2 Weekly Checklist
| Task | Who | Where |
|---|---|---|
| ☐ Vehicle stock ageing review (identifying 60+ days) | Inventory Mgr | Ageing Report |
| ☐ Lead conversion & lost-sale analysis | Sales Mgr | Lead Report |
| ☐ Technician efficiency and productivity review | Workshop Mgr | Productivity Report |
| ☐ Spare parts low-stock checks & purchase orders | Inventory Mgr | Parts Dashboard |
| ☐ Insurance renewal follow-up calling blitz | Insurance Rep | Renewal Tracker |

### 9.3 Monthly Checklist
| Task | Who | Where |
|---|---|---|
| ☐ Revenue reconciliation vs accounts & bank stmts | Finance / Owner| Financial Dashboards |
| ☐ Branch sales analytics vs monthly targets | Dealership Owner| Performance Analytics |
| ☐ Workshop profitability (Labor vs Parts margins) | Dealership Owner| Service Dashboard |
| ☐ Physical spot inventory audit (Cars & Main parts) | Inventory Mgr | Inventory Audit |
| ☐ Total outstanding finance/EMI status tracking | Finance Exec | Loan Ledger |

### 9.4 Quarterly Checklist
| Task | Who | Where |
|---|---|---|
| ☐ Complete physical vehicle & key audit | Inventory Mgr | Audit Module |
| ☐ Spare parts expiry / warranty claim clearance | Parts Mgr | Warranty / Returns |
| ☐ Strategic branch performance review | Owner | Analytics |
| ☐ Service SLA / Customer ratings audit | CRM Mgr | Support Dashboards |

### 9.5 Annual Checklist
| Task | Who | Where |
|---|---|---|
| ☐ Annual Sales & Margin review | Dealership Owner| Full Dashboard |
| ☐ Vendor & finance partner renegotiation | Owner / Finance | Vendor Master |
| ☐ Insurance policy global audit & commissions | Finance | Insurance Module |
| ☐ Dead-stock vehicle & parts liquidation planning | Inventory Mgr | Stock Ledger |

---

## 10. User Roles & Who Does What

| Feature | Dealership Owner | Showroom Manager | Sales Exec | Service Advisor | Finance Exec | Inventory Mgr |
|---|---|---|---|---|---|---|
| **Vehicle Master** | 👁 Read | 👁 Read | 👁 Read | 👁 Read | 👁 Read | ✅ Full |
| **Sales Leads** | 👁 Read | ✅ Full | ✅ Own Leads | ❌ | ❌ | ❌ |
| **Vehicle Booking** | 👁 Read | ✅ Full | ✅ Own Booking| ❌ | 👁 Read | 👁 Read |
| **PDI Checklist** | 👁 Read | ✅ Approve | 👁 Read | ✅ Action | ❌ | ❌ |
| **Service Job Card** | 👁 Read | ❌ | ❌ | ✅ Full | 👁 Read | 👁 Read |
| **Warranty Claims** | 👁 Read | ❌ | ❌ | ✅ Verify | ❌ | ✅ Process |
| **Spare Parts Issue**| 👁 Read | ❌ | ❌ | 👁 Read | ❌ | ✅ Full |
| **Vehicle Loan** | 👁 Read | 👁 Read | 👁 Read | ❌ | ✅ Full | ❌ |
| **Profitability DB** | ✅ Full | 👁 Branch Only| ❌ | ❌ | 👁 Read | ❌ |

---

## 11. Frequently Asked Questions

**Q1: A new vehicle arrived, but it is not showing up in stock for booking. Why?**  
A: Ensure the "Vehicle Inventory" entry for that VIN was completely Saved AND Submitted. If left in draft mode or if the status wasn't set to "In Stock", it won't appear on the showroom floor.

**Q2: The Customer paid their booking token, but the booking still shows 'Pending'.**  
A: A payment entry must be explicitly linked to the Vehicle Booking record. Go to Bookings, ensure "Advance Payment Received" is checked, and verify with the cashier that the receipt was matched.

**Q3: We need to swap a Test-Drive vehicle to a different sales executive schedule.**  
A: Navigate to **Test Drive Schedule**, open the pending drive, and alter the "Driver / Sales Executive" drop-down. It will push an alert to the new executive automatically.

**Q4: Our automated Insurance Renewal Reminders are not sending to customers.**  
A: Verify that the ERPNext email domain and scheduler hooks are active. Check the **Insurance Policy** expiry date ensuring it's exactly 15/30 days out. Also ensure the associated Customer has a valid Email ID configured.

**Q5: The Service Estimate was created, but I cannot start work on the Job Card.**  
A: The Job Card is gated by customer approval. Send the estimate via SMS/Email; once the customer clicks "Approve Estimate" (or you manually toggle it if they gave verbal approval), the Job Card moves to "In Progress".

**Q6: A workshop job is taking 3 days longer than expected. How do I reflect this?**  
A: Open the **Service Job Card**, edit the "Estimated Completion Time" field, and add notes to the "Delay Reason" dialogue. This updates SLA tracking and triggers an apology text to the customer.

**Q7: EMI payments are mismatched from the bank drop.**  
A: Cross-reference the **EMI Schedule** within the **Vehicle Loan Application** with the uploaded bank statement in ERPNext's Bank Reconciliation tool. 

**Q8: Issued spare parts are not tallying with inventory deductions.**  
A: Make sure you are using **Spare Part Issue** (which consumes stock natively to the Job Card) rather than a general manual stock entry, which lacks the relationship tie to the specific vehicle.

**Q9: The manufacturer rejected a warranty claim. How do I recover the cost?**  
A: Change the **Warranty Claim** Status to "Rejected". You must re-open the Invoice or generate an independent Sales Invoice directly billing the customer for the replaced parts if they still intend to accept the repair.

**Q10: Customer wants to cancel their vehicle purchase after booking. How do I process this?**  
A: Open the **Vehicle Booking** and click "Cancel Booking." This automatically unlocks the assigned VIN/Chassis back to available stock. The Cashier will then handle the refund payment via a contra journal entry to close it out.

**Q11: We have a cash buyer. How do I skip the vehicle loan step?**  
A: The **Vehicle Loan Application** is strictly optional. During **Vehicle Booking** / **Vehicle Delivery**, simply process standard Payment Entries for the total amount directly against the Sales Invoice.

**Q12: How do I assign a specific chassis (VIN) to an impatient customer?**  
A: Within the **Vehicle Booking** document, use the "Fetch Available VINs" function under the Chassis Assignment tab. Selecting one will instantly lock it from other sales agents.

**Q13: How do I update showroom stock availability?**  
A: The showroom stock count updates automatically whenever a new VIN is registered, transferred in via **Inter-Branch Vehicle Transfer**, or removed via **Vehicle Delivery**. Check the "Showroom Allocation" doc for display vehicles.

**Q14: How can I export dealership profitability and analytics to give to the owner?**  
A: Any ERPNext analytic dashboard can be exported by navigating to the report, setting filters (e.g., this month, branch=South), and clicking the PDF/Excel/CSV export icon located natively in the top right corner.

**Q15: How do I process an exchange vehicle valuation against a new sale?**  
A: Use the **Exchange Evaluation** Doctype to record the old vehicle specs. The "Offered Price" from this evaluation acts as a discount/contra entry when building the final **Vehicle Quotation**.

---

## 12. Support & Contact

| Channel | Details |
|---|---|
| 📧 Dealership Internal IT Email | it-admin@autodealer.com |
| 📖 Operational Knowledge Base | https://docs.autodealer.com |
| 🐛 Technical Bug Reports | Submit IT Tickets through ERPNext Internal Issues |
| 📱 Direct ERP Helpdesk | +91-XXXXXXXXXX (Central Support) |

---

*© 2026 Auto_Dealer Management Systems — Complete Dealership ERP Solution*  
*Powered by Frappe Framework & ERPNext v15*
