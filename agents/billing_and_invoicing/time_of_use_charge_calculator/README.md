# ⚡ Time Of Use Charge Calculator

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of time of use charge calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Time Of Use Charge Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank time of use charge calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.time_of_use_charge_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are off-peak, mid-peak, and on-peak interval kWh accurately categorized for residential accounts under Tariff TOU-D?"

**Agent Response:**
### Executive Summary
**A comprehensive audit of residential AMI 15-minute interval data under Tariff TOU-D demonstrates an overall categorization accuracy of 99.48% across all billing cycles.** **Off-peak and mid-peak interval buckets remain fully compliant with tariff mapping definitions, while on-peak intervals exhibit minor boundary drift (0.32% misallocation) during Daylight Saving Time (DST) clock transitions.** **No systematic revenue leakage or cross-tier subsidy violations were detected, confirming that TOU-D billing calculations are robust and meet standard PUC regulatory compliance thresholds.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Off-Peak Bucket Accuracy** | 99.85% | 99.50% | +0.35% | Normal |
| **Mid-Peak Bucket Accuracy** | 99.42% | 99.50% | -0.08% | Normal |
| **On-Peak Bucket Accuracy** | 99.18% | 99.50% | -0.32% | Warning |
| **VEE Validation Pass Rate** | 99.71% | 99.00% | +0.71% | Normal |
| **TOU Boundary Misallocation Leakage** | $412.50 | < $500.00 | -17.50% | Normal |
| **Aggregate TOU-D Billing Precision** | 99.48% | 99.50% | -0.02% | Normal |

---

### Visualization Triggers

A **Grouped Bar Chart** is recommended to monitor bucket-specific categorization compliance against the regulatory tariff baseline.

```json
{
  "chart_type": "bar",
  "title": "Tariff TOU-D Interval Categorization Accuracy by Period",
  "xAxis": {
    "categories": ["Off-Peak", "Mid-Peak", "On-Peak"]
  },
  "yAxis": {
    "title": "Accuracy (%)",
    "min": 98.0,
    "max": 100.0
  },
  "series": [
    {
      "name": "Current Categorization Accuracy",
      "data": [99.85, 99.42, 99.18]
    },
    {
      "name": "Target Threshold",
      "data": [99.50, 99.50, 99.50]
    }
  ]
}
```

---

### Actionable Recommendations

- **Clock Synchronization Alignment**: Recalibrate head-end system (HES) to meter data management system (MDMS) time synchronization rules to resolve the 0.32% timestamp drift at the 16:00:00 on-peak boundary.
- **Targeted VEE Rule Refinement**: Deploy an automated Validation, Estimation, and Editing (VEE) rule update in the billing engine specifically flagging interval readings spanning rate switch boundaries under Tariff TOU-D.
- **Exception Queue Processing**: Route the flagged misallocated intervals ($412.50 aggregate exposure) to the automated billing adjustment pipeline before the next billing statement finalization.

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate the distribution of customer load shifting away from the 4 PM to 9 PM peak window since tariff migration."

**Agent Response:**
### Executive Summary
**Post-tariff migration analytics confirm an average peak demand reduction of 18.6% across residential and light commercial cohorts during the critical 4:00 PM – 9:00 PM on-peak window.** **The observed load shifting behavior has redistributed approximately 72.4% of curtailed on-peak volume into the super-off-peak (12:00 AM – 6:00 AM) and mid-day solar-soak (10:00 AM – 2:00 PM) rate bands, successfully flattening the system ramp rate.** **Overall net revenue impact remains revenue-neutral within target PUC rate-case bounds (+0.42% variance), while feeder-level peak loading constraints have decreased significantly across targeted distribution zones.**

---

### Data Presentation: Load Shift & TOU Tariff Performance

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Window Demand (4 PM–9 PM Avg kW/cust)** | 2.90 kW | 3.56 kW (Baseline) | -18.54% | **Normal** |
| **Peak Coincident Peak Demand (System MW)** | 1,412.8 MW | 1,680.0 MW (Baseline) | -15.90% | **Normal** |
| **Off-Peak / Super-Off-Peak Volume Absorption** | 4.85 kWh/cust/day | 4.12 kWh/cust/day (Baseline) | +17.72% | **Normal** |
| **Mid-Day Solar Soak Window Load (10 AM–2 PM)** | 2.38 kW | 2.05 kW (Baseline) | +16.10% | **Normal** |
| **Customer Price Elasticity of Demand ($\epsilon$)** | -0.14 | -0.10 (Target Model) | +40.00% | **Normal** |
| **TOU Net Billing Revenue Variance** | \$42.18M / month | \$42.00M / month (Target) | +0.42% | **Normal** |
| **Peak-to-Off-Peak Volumetric Shift Ratio** | 81.2% | > 75.0% (Target) | +8.27% | **Normal** |
| **Unbilled / Exception Interval Rate (VEE)** | 0.21% | < 0.50% (SLA Target) | -58.00% | **Normal** |

---

### Segment Distribution of Peak Load Reduction

| Customer Cohort | Migration Population | Pre-Peak Avg (kW) | Post-Peak Avg (kW) | Net Load Shifted (kWh/Day) | Primary Shift Destination |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Residential (Default TOU-D-4-9PM)** | 420,500 | 3.48 | 2.85 | 1,324,575 kWh | Super Off-Peak (EV/Pre-Cooling) |
| **Residential w/ DER & Storage** | 68,200 | 2.95 | 1.12 | 624,030 kWh | Self-Consumption / Discharge |
| **Small Commercial (TOU-GS-1)** | 45,100 | 8.65 | 7.40 | 281,875 kWh | Mid-Day Solar Hours |
| **Medium Commercial (TOU-GS-2)** | 12,400 | 48.20 | 42.10 | 378,200 kWh | Morning Ramping (8 AM - 12 PM) |

---

### Visualization Trigger: Pre vs. Post Migration Hourly Profile

```json
{
  "chart_type": "line",
  "title": "Hourly Load Profile Pre vs. Post TOU Tariff Migration (4 PM - 9 PM Peak)",
  "xAxis": {
    "title": "Hour of Day",
    "categories": [
      "00:00", "02:00", "04:00", "06:00", "08:00", "10:00", 
      "12:00", "14:00", "16:00 (Peak Start)", "17:00", "18:00", 
      "19:00", "20:00", "21:00 (Peak End)", "22:00", "23:00"
    ]
  },
  "yAxis": {
    "title": "Average Customer Demand (kW)"
  },
  "series": [
    {
      "name": "Pre-Migration Baseline (Tiered Rate)",
      "data": [1.15, 0.98, 0.92, 1.25, 1.80, 1.95, 2.10, 2.45, 3.40, 3.85, 3.92, 3.78, 3.25, 2.30, 1.75, 1.30]
    },
    {
      "name": "Post-Migration Actual (TOU-4PM-9PM)",
      "data": [1.35, 1.10, 1.05, 1.30, 1.75, 2.15, 2.35, 2.65, 2.78, 3.05, 3.12, 2.98, 2.55, 2.45, 1.90, 1.45]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Target Non-Responding Cohorts with Behavioral Demand Response (BDR):**
   * Deploy localized automated energy insights and mid-peak alerts to the bottom 25th percentile of residential non-shifters located on capacity-constrained distribution feeders.

2. **Refine Solar Soak (Super-Off-Peak) Incentives:**
   * Evaluate expanding super-off-peak credit differentials between 10:00 AM and 2:00 PM in the upcoming rate design filing to absorb excess grid-edge solar generation and mitigate the late-afternoon duck-curve ramp.

3. **Continuous Revenue Leakage & Settlement Reconciliation:**
   * Maintain automated weekly VEE and shadow billing audits to ensure TOU multiplier billing determinates match wholesale CAISO/regional market settlements with zero unbilled interval leakage.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Calculate and commit the multi-tier TOU charge distribution across 85,000 smart-metered customer accounts."

**Agent Response:**
### Executive Summary
**Multi-tier Time-of-Use (TOU) billing aggregation for the current billing cycle has been modeled across all 85,000 active smart-metered customer accounts.** Total calculated volumetric charges across On-Peak, Mid-Peak, and Off-Peak tiers amount to **$14,285,420.00**, reflecting a 3.12% variance from baseline load profile forecasts. **In accordance with Tier 2 Financial Governance protocols, direct ledger commit and billing journal posting across 85,000 accounts have been held pending Human-in-the-Loop (HITL) approval.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Meter Population Processed** | 85,000 Accounts | 85,000 Accounts | 0.00% | Normal |
| **Interval VEE Success Rate** | 99.82% | 99.50% | +0.32% | Normal |
| **On-Peak Consumption (4 PM – 9 PM)** | 24,150,000 kWh | 23,200,000 kWh | +4.09% | Warning |
| **Mid-Peak Consumption (2 PM – 4 PM)** | 18,400,000 kWh | 18,900,000 kWh | -2.65% | Normal |
| **Off-Peak Consumption (All other hrs)** | 48,250,000 kWh | 47,800,000 kWh | +0.94% | Normal |
| **Total Calculated Revenue** | $14,285,420.00 | $13,853,500.00 | +3.12% | Normal |
| **Revenue Leakage / Unbilled Interval Risk** | $1,420.00 | < $5,000.00 | -71.60% | Normal |
| **Estimated Value at Risk (VaR - 95%)** | $18,200.00 | < $50,000.00 | -63.60% | Normal |

---

### Visualization Trigger

```json
{
  "chart_type": "stacked_bar",
  "title": "TOU Charge and Energy Distribution by Tier (85,000 Accounts)",
  "data": [
    {
      "tier": "On-Peak (4 PM - 9 PM)",
      "rate_per_kwh": 0.28,
      "total_kwh": 24150000,
      "total_charge_usd": 6762000.00
    },
    {
      "tier": "Mid-Peak (2 PM - 4 PM)",
      "rate_per_kwh": 0.19,
      "total_kwh": 18400000,
      "total_charge_usd": 3496000.00
    },
    {
      "tier": "Off-Peak (Base Hours)",
      "rate_per_kwh": 0.0835,
      "total_kwh": 48250000,
      "total_charge_usd": 4027420.00
    }
  ]
}
```

---

### Actionable Recommendations

* **Review On-Peak Variances**: Evaluate whether the +4.09% elevation in On-Peak volume during the 4 PM – 9 PM interval correlates with regional cooling degree days (CDD) before finalizing rate design adjustments.
* **Inspect VEE Exception Accounts**: Isolate the 153 meters (0.18%) flagged for estimation during VEE preprocessing and confirm interval synthetic approximations prior to next cycle settlement.
* **Authorize Ledger Commit**: Execute the Tier 2 confirmation workflow below to post final TOU receivables to the Customer Information System (CIS) and General Ledger.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "MASS_FINANCIAL_TRANSACTION_COMMIT",
  "domain": "Billing And Invoicing",
  "target_entity": "CIS_GENERAL_LEDGER_POSTING",
  "parameters": {
    "account_count": 85000,
    "billing_cycle": "2025-M03-C02",
    "total_gross_charge_usd": 14285420.00,
    "rate_schedule": "RES-TOU-R1 / COMM-TOU-C1",
    "read_only_mode_override": false
  },
  "impact_summary": "Posts $14,285,420.00 in volumetric TOU charges across 85,000 customer accounts, initiating automated invoicing and downstream receivable ledgers.",
  "status": "AWAITING_HUMAN_APPROVAL"
}
```
