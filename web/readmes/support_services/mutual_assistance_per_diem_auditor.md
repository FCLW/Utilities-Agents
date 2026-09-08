# ⚡ Mutual Assistance Per Diem Auditor

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of mutual assistance per diem auditor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Mutual Assistance Per Diem Auditor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank mutual assistance per diem auditor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.mutual_assistance_per_diem_auditor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Do the hotel, meal, and fuel expense claims submitted by visiting mutual aid contractor crews match established utility rate caps?"

**Agent Response:**
### Executive Summary
**Audit analysis reveals that submitted mutual aid contractor expense claims exceed established utility per diem and reimbursement rate caps across lodging, meals, and fuel categories by an average variance of +25.4%. While baseline contractual allowances are indexed to standard GSA/PUC emergency mobilization rates, multiple contractor invoices reflect unapproved surge pricing and unitemized incidental surcharges. Immediate clawback adjustments and exception reconciliation are required prior to final invoice settlement and FEMA/regulatory cost-recovery filing.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Lodging / Hotel Rate (per room/night)** | $245.00 | $185.00 | +32.43% | **Critical** |
| **Meals & Per Diem (per person/day)** | $82.50 | $69.00 | +19.57% | **Warning** |
| **Fleet Fuel Reimbursement (per gal equiv.)** | $4.85 | $3.95 | +22.78% | **Critical** |
| **Staging Site Catering (per head/meal)** | $38.00 | $30.00 | +26.67% | **Warning** |
| **Itemized Receipt Compliance Rate** | 81.2% | 100.0% | -18.80% | **Critical** |
| **Audit Compliance Rate (Overall Invoices)** | 74.6% | 98.0% | -23.88% | **Critical** |

---

### Visualization Triggers
**Recommended Visualization:** Grouped Bar Chart comparing submitted contractor expense claims against utility/GSA rate caps across expense categories to highlight rate variance hotspots.

```json
{
  "chart_type": "bar",
  "title": "Mutual Aid Expense Claims vs. Established Rate Caps",
  "data": {
    "categories": [
      "Lodging / Hotel (per room/night)",
      "Meals & Incidentals (per person/day)",
      "Fleet Fuel Reimbursement (per gal)",
      "Staging Site Catering (per head)"
    ],
    "series": [
      {
        "name": "Submitted Claim Avg ($)",
        "values": [245.00, 82.50, 4.85, 38.00]
      },
      {
        "name": "Utility Rate Cap ($)",
        "values": [185.00, 69.00, 3.95, 30.00]
      }
    ]
  },
  "unit": "USD ($)"
}
```

---

### Actionable Recommendations
- **Invoice Line-Item Adjustments**: Issue formal billing dispute notices to visiting mutual aid contractors whose lodging and meal per diems exceed standard Regional Mutual Assistance Group (RMAG) schedule caps without pre-authorized emergency deviation waivers.
- **Enforce Fuel Card Indexing**: Mandate that fuel reconciliations adhere strictly to the localized OPIS (Oil Price Information Service) rack average plus contractually approved handling markups.
- **Receipt Reconciliation Mandate**: Require contractor administrative leads to submit itemized folio receipts for all lodging charges exceeding $185/night to verify whether hotel taxes/fees or unallowable ancillary charges caused the discrepancy.
- **Regulatory Cost-Recovery Documentation**: Archive all rate cap variance justifications and settlement audit trails to preserve eligibility for state public utility commission (PUC) prudency reviews and FEMA Category F/G public assistance reimbursements.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MUTUAL_AID_INVOICE_ADJUSTMENT",
  "description": "Approve systemic line-item reduction and payment hold on contractor mutual aid expense invoices exceeding authorized utility per diem rate caps pending itemized audit reconciliation.",
  "parameters": {
    "total_disputed_variance": "$184,250.00",
    "affected_contractor_count": 4,
    "target_settlement_basis": "RMAG_Standard_Schedule_A",
    "clawback_mechanism": "Net_Remittance_Reduction"
  },
  "authorization_required": "Human-In-The-Loop (HITL) - Support Services Operations Lead & Accounts Payable Controller"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Audit travel expense receipts, mileage logs, and daily per-diem submissions against FEMA disaster reimbursement guidelines."

**Agent Response:**
### Executive Summary
**Mutual assistance travel and expense documentation was audited against FEMA Public Assistance Program and Policy Guide (PAPPG FP 104-009-2), GSA Federal Travel Regulations (41 CFR Chapters 300–304), and Regional Mutual Assistance Group (RMAG) governance. Of the total $1,104,400 submitted across deployed responding utility crews, $999,600 meets all statutory substantiation standards, while $104,800 in claims has been flagged for audit variance or disallowance due to missing lodging itemization, unreceipted incidentals, and per-diem rate caps exceeding local GSA thresholds. Immediate adjustment and reconciliation are required prior to final Form FF-206-FY-21-137 submission to prevent federal clawbacks.**

---

### Quantitative Audit & Compliance Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Audit Compliance Rate** | 90.51% | 100.00% | -9.49% | **Warning** |
| **Total Claimed Expenses** | $1,104,400 | $1,104,400 | 0.00% | **Normal** |
| **FEMA Allowable Amount** | $999,600 | $1,104,400 | -9.49% | **Warning** |
| **Identified Non-Compliant / Disallowed Variance** | $104,800 | $0.00 | +100.00% | **Critical** |
| **GSA M&IE Daily Rate Adherence** | 92.40% | 100.00% | -7.60% | **Warning** |
| **Mileage Log Substantiation Rate (GPS / Odometer)** | 95.72% | 100.00% | -4.28% | **Warning** |
| **Receipt Itemization & Lodging Folio Match** | 91.12% | 100.00% | -8.88% | **Critical** |

---

### Detailed Audit Breakdown by FEMA Expense Category

```
══════════════════════════════════════════════════════════════════════════════════════════════════
FEMA PAPPG / 2 CFR 200 SUBPART E AUDIT VARIANCE ANALYSIS
══════════════════════════════════════════════════════════════════════════════════════════════════
Expense Category        Claimed ($)   FEMA Cap / Allowable ($)  Variance / Disallowance ($)  Root Cause
──────────────────────────────────────────────────────────────────────────────────────────────────
Lodging Folios          $485,200      $442,100                  $43,100                      Direct room charges exceed GSA CONUS rate without prior written justification; unauthorized resort/valet fees.
M&IE Per Diem           $214,500      $198,200                  $16,300                      First/last day of travel claimed at 100% instead of statutory 75%; meals provided at staging base not deducted.
Vehicle / Fleet Mileage $168,400      $161,200                  $7,200                       Missing point-to-point transit justification; odometer variance vs. telematics log.
Commercial Airfare      $89,200       $89,200                   $0                           Coach-class compliant with Fly America Act & standard ticket receipts verified.
Staging Fuel & Tolls    $112,600      $108,900                  $3,700                       Missing automated toll receipts and duplicate fuel card entry on heavy transport unit.
Unreceipted Incidentals $34,500       $0                        $34,500                      Flat-rate incidental line items lacking source vendor receipts (ineligible under 2 CFR § 200.403).
──────────────────────────────────────────────────────────────────────────────────────────────────
TOTALS                  $1,104,400    $999,600                  $104,800                     Total Audit Disallowance Pool
══════════════════════════════════════════════════════════════════════════════════════════════════
```

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "FEMA Mutual Assistance Expense Audit: Claimed vs. Allowable Breakdown",
  "data": {
    "categories": [
      "Lodging (GSA Cap)",
      "M&IE Per Diem",
      "Vehicle Mileage",
      "Commercial Airfare",
      "Staging Fuel & Tolls",
      "Unreceipted Incidentals"
    ],
    "claimed_amount_usd": [485200, 214500, 168400, 89200, 112600, 34500],
    "fema_allowable_usd": [442100, 198200, 161200, 89200, 108900, 0],
    "variance_disallowance_usd": [43100, 16300, 7200, 0, 3700, 34500]
  }
}
```

---

### Actionable Recommendations

1. **Enforce 75% M&IE Proration for Travel Days**: Automatically recompute travel mobilization and demobilization calendar days to 75% of the applicable GSA Meals and Incidental Expenses baseline pursuant to 41 CFR § 301-11.101.
2. **Deduct Staging Site Provided Meals**: Cross-reference camp log catering rosters against daily per-diem submissions; deduct statutory meal allocations for all breakfast, lunch, and dinner services furnished by the host utility or emergency operations center.
3. **Disallow Unreceipted Incidentals**: Strip $34,500 in miscellaneous flat charges lacking line-item vendor receipts from the direct FEMA reimbursement request package, routing them to internal utility non-reimbursable accounting codes.
4. **Require Hotel Zero-Balance Folios**: Request itemized zero-balance hotel folios for the $43,100 lodging delta to substantiate non-taxable utility emergency exemptions and remove unallowable room service or discretionary fees.
5. **Reconcile Fleet GPS Telematics**: Align mileage claims with automated telematics/ELD trip logs for utility bucket trucks and digger derricks to substantiate the $7,200 delta.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "FINANCIAL_CLAIM_ADJUSTMENT"
  description: "Deduct $104,800.00 in non-compliant travel, lodging, and per-diem charges from the mutual assistance FEMA Public Assistance reimbursement filing."
  reconciliation_details:
    total_submitted: "$1,104,400.00"
    adjusted_claim_amount: "$999,600.00"
    total_disallowance: "$104,800.00"
    target_fema_form: "FEMA Form FF-206-FY-21-137 (Project Application)"
    affected_categories:
      - "Lodging: $43,100.00"
      - "M&IE Proration/Catering: $16,300.00"
      - "Unsubstantiated Mileage: $7,200.00"
      - "Fuel/Toll Exceptions: $3,700.00"
      - "Unreceipted Incidentals: $34,500.00"
  approver_role: "Finance Director / Mutual Assistance Controller"
  confirmation_status: "PENDING_HUMAN_IN_THE_LOOP_APPROVAL"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Approve verified per-diem and lodging expense disbursements for Contractor Force #402 for storm restoration services."

**Agent Response:**
### Executive Summary
**Audit verification for Contractor Force #402 storm restoration per-diem and lodging expenses has been completed against standard mutual assistance GSA/EEI rate schedules. Total audited reimbursable expenses equal $234,700 against $241,400 submitted claims, identifying $6,700 in non-qualifying or out-of-cap lodging charges. Because financial disbursement of mutual assistance funds constitutes a Tier 2 financial transaction, human authorization is required to release the approved payout.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Claimed Expenses** | $241,400 | $234,700 (Audit Cap) | +2.85% | Warning |
| **Lodging per Room/Night (Avg)** | $185.00 | $175.00 (EEI Schedule) | +5.71% | Warning |
| **M&IE Daily Rate Compliance** | 96.2% | 100.0% | -3.80% | Warning |
| **Headcount Rostering Verification** | 120 / 120 FTEs | 120 FTEs | 0.00% | Normal |
| **Audit Compliance Rate** | 97.2% | 95.0% | +2.32% | Normal |
| **Eligible Disbursement Total** | $234,700 | $234,700 | 0.00% | Normal |

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Contractor Force #402 - Claimed vs. Audited Per Diem & Lodging",
  "categories": [
    "Lodging Per Diem",
    "Meals & Incidentals (M&IE)",
    "Staging Site Stipend",
    "Mobilization Travel Allowance"
  ],
  "series": [
    {
      "name": "Claimed ($)",
      "data": [142500, 58400, 18500, 22000]
    },
    {
      "name": "Audited / Approved Cap ($)",
      "data": [138000, 56200, 18500, 22000]
    }
  ]
}
```

---

### Actionable Recommendations
- **Approve Verified Disbursement**: Disburse the verified sum of **$234,700.00** to Contractor Force #402 accounts payable profile.
- **Issue Reconciliation Notice**: Forward the itemized audit variance report ($6,700.00 deduction for unauthorized lodging surcharges and out-of-policy M&IE items) to Contractor Force #402 billing coordinators.
- **Archive Documentation**: Store signed roster manifests, timesheets, and hotel master folios in the Storm Cost Recovery repository for state PUC prudency review and FERC compliance audits.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FINANCIAL_DISBURSEMENT_APPROVAL",
  "contractor_force_id": "402",
  "vendor_name": "Contractor Force #402 (Mutual Assistance Restoration)",
  "claimed_amount_usd": 241400.00,
  "audit_deduction_usd": 6700.00,
  "net_approved_disbursement_usd": 234700.00,
  "account_code": "FERC-593-STORM-RESTORATION-MA",
  "compliance_status": "VERIFIED_WITH_ADJUSTMENTS",
  "requires_hitl_approval": true,
  "approver_role": "Support Services Operations / Financial Controller"
}
```
