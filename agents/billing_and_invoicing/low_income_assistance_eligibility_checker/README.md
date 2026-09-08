# ⚡ Low Income Assistance Eligibility Checker

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of low income assistance eligibility checker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Low Income Assistance Eligibility Checker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank low income assistance eligibility checker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.low_income_assistance_eligibility_checker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Does customer account #901284 qualify for the state CARE or LIHEAP utility discount based on verified income thresholds?"

**Agent Response:**
### 1. Executive Summary
**Evaluation of customer account #901284 for California Alternate Rates for Energy (CARE) and the Low Income Home Energy Assistance Program (LIHEAP) reveals INSUFFICIENT DATA in the enterprise billing repository for verified annual household income and household occupant count. Without verified income documentation or cross-system categorical eligibility verification (e.g., CalFresh, Medi-Cal/Medicaid, SSI), a definitive eligibility determination cannot be executed autonomously. Manual income verification or automated state data-exchange validation is required prior to applying any rate discount tariff.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Account #901284 Status** | Active (Standard Residential) | Standard Residential Rate | 0.00% | Normal |
| **Verified Gross Annual Income** | **INSUFFICIENT DATA** | ≤ $39,440 (1–2 person CARE) / ≤ $60,000 (4-person) | N/A | Warning |
| **Documented Household Size** | Unspecified / Pending | 1–4 Persons Baseline | N/A | Warning |
| **Categorical Assistance Flags** | None Logged | Active Public Assistance Record | -100.00% | Warning |
| **LIHEAP Direct Benefit Eligibility** | Unverified | ≤ 60% State Median Income (SMI) | N/A | Warning |

*Regulatory Baseline Note: Program thresholds reflect standard PUC CARE guidelines (200% of Federal Poverty Guidelines) and State Energy Department LIHEAP eligibility limits.*

---

### 3. Visualization Triggers

A comparative **Grouped Bar Chart** illustrates the statutory annual gross income qualification ceilings for CARE vs. LIHEAP across household sizes (1–6 persons).

```json
{
  "chart_type": "bar",
  "title": "Utility Assistance Income Ceilings: CARE vs. LIHEAP",
  "categories": [
    "Household 1-2",
    "Household 3",
    "Household 4",
    "Household 5",
    "Household 6"
  ],
  "series": [
    {
      "name": "CARE Max Income ($)",
      "data": [39440, 49720, 60000, 70280, 80560]
    },
    {
      "name": "LIHEAP Max Income ($)",
      "data": [43850, 55280, 66710, 78140, 89570]
    }
  ],
  "units": "USD ($)"
}
```

---

### 4. Actionable Recommendations

* **Transmit Income Verification Request:** Dispatch an automated income documentation notice (Form 1040, W-2, pay stubs, or state benefit verification letter) to the primary account holder on Account #901284.
* **Execute Categorical Data Match:** Run a secure batch inquiry against state health and human services categorical eligibility databases (e.g., SNAP/CalFresh, SSI, TANF) to check for automatic enrollment qualification.
* **Assess FERA Secondary Eligibility:** If the customer’s verified income marginally exceeds CARE limits (200% FPL) but remains within 250% FPL for households of 3+, evaluate eligibility for the Family Electric Rate Assistance (FERA) program.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "TARIFF_OVERRIDE_AND_DISCOUNT_ENROLLMENT",
  "target_account_id": "901284",
  "requested_rate_schedule": "RESIDENTIAL_CARE_DISCOUNT (20-35% bill reduction)",
  "compliance_gate": "PENDING_INCOME_VERIFICATION",
  "reason": "Automated rate reclassification and financial discount application requires human approval and completed proof of income/categorical eligibility under State PUC Rule 19.",
  "hitl_approval_required": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Track the processing throughput and verification latency for low-income discount applications received this month."

**Agent Response:**
### Executive Summary
**Month-to-date (MTD) processing throughput for low-income discount assistance applications has reached an average of 478 applications/day, representing an 11.2% increase over baseline capacity.** **Mean verification latency has decreased significantly to 11.98 hours against the regulatory target threshold of ≤ 24.00 hours, driven by automated API data-matching with state social services and income registries.** **Backlog volume remains well within operational tolerance limits with a 96.4% on-time verification rate across all grid zones.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Applications Received (MTD)** | 10,516 | 9,800 | +7.31% | Normal |
| **Average Daily Processing Throughput** | 478 apps/day | 430 apps/day | +11.16% | Normal |
| **Mean Verification Latency** | 11.98 hrs | ≤ 24.00 hrs | -50.08% | Normal |
| **P95 Verification Latency** | 21.40 hrs | ≤ 36.00 hrs | -40.56% | Normal |
| **Automated Verification Pass Rate** | 82.40% | 75.00% | +9.87% | Normal |
| **Manual Exception / Audit Queue Volume** | 378 apps | ≤ 500 apps | -24.40% | Normal |
| **SLA Compliance Rate (≤ 48 hr resolution)**| 98.65% | 95.00% | +3.84% | Normal |

---

### Visualization Triggers

A dual-axis time-series chart is recommended to track the inverse correlation between verification latency and throughput scaling over the monthly billing cycles.

```json
{
  "chart_type": "line",
  "title": "Low-Income Assistance Application Throughput & Verification Latency (MTD)",
  "labels": ["Week 1", "Week 2", "Week 3", "Week 4 (Current)"],
  "datasets": [
    {
      "label": "Daily Application Throughput (apps/day)",
      "data": [420, 485, 510, 495],
      "borderColor": "#1f77b4",
      "yAxisID": "y"
    },
    {
      "label": "Avg Verification Latency (Hours)",
      "data": [14.2, 12.8, 11.5, 9.4],
      "borderColor": "#ff7f0e",
      "yAxisID": "y1"
    }
  ]
}
```

---

### Actionable Recommendations

- **Automated Clearing Threshold Maintenance**: Maintain active automated API bridges with state categorical eligibility databases (e.g., SNAP, LIHEAP, Medicaid) to preserve the >80% automated approval rate.
- **Exception Queue Rebalancing**: Route remaining manual document verification exceptions (17.6% of intake) to Tier 1 billing caseworkers during off-peak morning processing windows (07:00–10:00 UTC).
- **Tariff Enrollment Verification**: Ensure verified applicants are systematically assigned to the subsidized rate schedule (e.g., CARE/FERA/LID rate rider) prior to the next active billing cycle cut-off date to prevent delayed discount application.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Enroll Account #901284 in the 30% monthly lifeline discount program and waive past-due late payment penalties."

**Agent Response:**
### Executive Summary
**Account #901284 has been evaluated against state and utility regulatory criteria for the 30% Monthly Lifeline Low-Income Assistance Tariff. The account meets qualifying income-verification thresholds, making it eligible for rate reclassification and past-due penalty waiver consideration. Because rate structure modifications and financial balance adjustments constitute Tier 2 financial operations, human operator confirmation is required prior to applying changes.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Household Income % of FPL** | 142% | ≤ 200% FPL | -29.0% | Normal |
| **Lifeline Discount Rate** | 0% | 30.0% | +30.0% | Normal |
| **Effective Base Tariff ($/kWh)** | $0.180 / kWh | $0.126 / kWh | -30.0% | Normal |
| **Past-Due Late Penalties Accrued** | $45.00 | $0.00 | -100.0% (Target) | Warning |
| **Arrears Balance (Excluding Penalties)** | $312.40 | $0.00 | N/A | Warning |
| **Documentation / Categorical Eligibility** | Verified (SNAP/Medicaid) | Verified | 0.0% | Normal |

---

### Visualization Triggers

**Recommended Chart Type**: **Bar Chart (Comparative Tariff & Penalty Structure)**  
*Visualizes the pre-enrollment vs. proposed post-enrollment tariff rate and fee structure for Account #901284.*

```json
{
  "chart_type": "bar",
  "title": "Account #901284 - Tariff & Late Fee Comparison",
  "data": {
    "labels": [
      "Standard Tariff Rate ($/kWh)",
      "Lifeline Discount Rate ($/kWh)",
      "Past-Due Late Penalties ($)",
      "Waived Penalty Balance ($)"
    ],
    "datasets": [
      {
        "label": "Pre-Enrollment Status",
        "data": [0.18, 0.0, 45.0, 0.0],
        "backgroundColor": "#FF6384"
      },
      {
        "label": "Proposed Lifeline Enrollment",
        "data": [0.0, 0.126, 0.0, 45.0],
        "backgroundColor": "#36A2EB"
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Authorize Tariff Enrollment**: Approve the enrollment transition from Standard Residential (`RES-STD-01`) to Lifeline Assistance Tier (`RES-LIFE-30`).
- **Execute Penalty Waiver**: Post a credit memo to extinguish the $45.00 in late payment penalties accrued during the eligibility validation window.
- **Set Up Arrears Management Plan (AMP)**: Propose a 12-month levelized payment arrangement for the remaining $312.40 balance to prevent future service interruption.
- **Schedule Annual Re-Certification**: Flag the account for automated categorical income re-verification in 12 months in compliance with Public Utility Commission (PUC) mandates.

---

### [TIER 2 ACTION REQUIRED]

```yaml
operation_type: "FINANCIAL_TARIFF_MUTATION_AND_FEE_WAIVER"
account_id: "901284"
actions:
  - action_type: "ENROLL_LIFELINE_PROGRAM"
    program_code: "LIFELINE-30"
    discount_percentage: 30.0
    effective_billing_cycle: "CURRENT"
  - action_type: "WAIVE_LATE_FEES"
    credit_amount_usd: 45.00
    credit_type: "PENALTY_FORGIVENESS"
    justification: "Low Income Assistance Program Onboarding Policy"
compliance_reference: "PUC Rule 14.1 / Lifeline Rate Order"
requested_by: "low_income_assistance_eligibility_checker"
status: "AWAITING_HUMAN_CONFIRMATION"
```
