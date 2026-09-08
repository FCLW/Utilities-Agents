# ⚡ Critical Peak Pricing Calculator

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of critical peak pricing calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Critical Peak Pricing Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank critical peak pricing calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.critical_peak_pricing_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What were the total kilowatt-hour consumption charges billed during yesterday's 4-hour Critical Peak Pricing event in Zone 1?"

**Agent Response:**
### Executive Summary
**During yesterday's 4-hour Critical Peak Pricing (CPP) event (14:00 – 18:00) in Zone 1, total energy consumption billed across 12,450 participating accounts was 166.60 MWh (166,600 kWh). Total critical peak consumption charges amounted to $149,940.00 at an effective CPP tariff rate of $0.900/kWh. This reflects an 18.2% peak load reduction relative to the 10-day baseline average, generating $124,950.00 in incremental CPP demand response revenue.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Consumption Billed** | 166,600 kWh | 203,668 kWh | -18.20% | Normal |
| **Total CPP Charges Billed** | $149,940.00 | $24,990.00 (Standard TOU) | +500.00% | Normal |
| **Effective Rate per kWh** | $0.9000/kWh | $0.1500/kWh | +500.00% | Normal |
| **Average Hourly Demand** | 41.65 MW | 50.92 MW | -18.21% | Normal |
| **Peak Interval Demand (Hour 3)** | 45.10 MW | 54.20 MW | -16.79% | Normal |
| **Total Billable Accounts** | 12,450 | 12,450 | 0.00% | Normal |
| **Billing Exception / Re-read Rate** | 0.12% (15 meters) | < 0.50% | -76.00% | Normal |

---

### Hourly Event Breakdown

| Event Interval | Billed Volume (kWh) | CPP Rate ($/kWh) | Billed Charges ($) | Baseline Volume (kWh) | Load Reduction (kWh) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **14:00 – 15:00** | 38,200 | $0.90 | $34,380.00 | 48,100 | 9,900 (-20.58%) |
| **15:00 – 16:00** | 42,500 | $0.90 | $38,250.00 | 51,300 | 8,800 (-17.15%) |
| **16:00 – 17:00** | 45,100 | $0.90 | $40,590.00 | 54,200 | 9,100 (-16.79%) |
| **17:00 – 18:00** | 40,800 | $0.90 | $36,720.00 | 50,068 | 9,268 (-18.51%) |
| **Total (4 Hours)** | **166,600** | **$0.90** | **$149,940.00** | **203,668** | **37,068 (-18.20%)** |

---

### Visualization Triggers
**Recommended Visualization:** Grouped Interval Bar Chart comparing hourly consumption, actual billed charges, and baseline charges.

```json
{
  "chart_type": "bar",
  "title": "Zone 1 Critical Peak Pricing (CPP) Event - Hourly Billed Charges & Consumption",
  "categories": [
    "Hour 1 (14:00-15:00)",
    "Hour 2 (15:00-16:00)",
    "Hour 3 (16:00-17:00)",
    "Hour 4 (17:00-18:00)"
  ],
  "series": [
    {
      "name": "Consumption Billed (MWh)",
      "data": [38.2, 42.5, 45.1, 40.8]
    },
    {
      "name": "Charges Billed ($k)",
      "data": [34.38, 38.25, 40.59, 36.72]
    },
    {
      "name": "Baseline Billed ($k)",
      "data": [5.73, 6.38, 6.77, 6.12]
    }
  ]
}
```

---

### Actionable Recommendations
- **Automated Billing Invoicing Pass**: Release the 12,435 validated interval settlements into the overnight billing batch cycle for normal invoice generation.
- **AMI Telemetry Re-query**: Route the 15 meter exceptions with missing interval packets to the Meter Data Management System (MDMS) for automated VEE (Validation, Editing, and Estimation) retry.
- **Demand Response Settlement Notification**: Transmit aggregate demand reduction figures (37.07 MWh net curtailment) to the Wholesale Settlement & Settlement Reconciliation module to true-up wholesale nodal margin credits.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze customer load reduction elasticity and price responsiveness across commercial accounts under the $1.50/kWh peak rate."

**Agent Response:**
### Executive Summary
**Under the $1.50/kWh Critical Peak Pricing (CPP) rate event structure, commercial accounts demonstrate an aggregate peak load curtailment of 15.6% across monitored grid zones, corresponding to an average price elasticity of demand ($\varepsilon_d$) of -0.115. Cold Storage/Warehousing and Manufacturing accounts exhibit the highest price responsiveness (up to 24.8% load shed), whereas Mission-Critical Data Centers and Healthcare segments show severe inelasticity ($\varepsilon_d > -0.065$). The program delivers substantial peak shaving value, though target shortfalls in inelastic commercial clusters indicate the need for dual-tariff structuring or automated demand response (Auto-DR) integration.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Aggregate Commercial Load Curtailment** | 148.2 MW | 175.0 MW Target | -15.31% | **Warning** |
| **Average Commercial Price Elasticity ($\varepsilon_d$)** | -0.115 | -0.140 Target | -17.86% | **Warning** |
| **Cold Storage & Logistics Load Shed** | 24.8% (38.4 MW) | 20.0% Target | +24.00% | **Normal** |
| **Heavy Commercial / Light Industrial Shed** | 19.5% (44.2 MW) | 18.0% Target | +8.33% | **Normal** |
| **Commercial Real Estate (Office / HVAC)** | 16.7% (28.6 MW) | 15.0% Target | +11.33% | **Normal** |
| **Retail & Food Distribution Shed** | 14.1% (18.5 MW) | 15.0% Target | -6.00% | **Normal** |
| **Data Centers & Tech Infrastructure Shed** | 6.2% (11.3 MW) | 12.0% Target | -48.33% | **Critical** |
| **Healthcare & Hospitality Shed** | 8.4% (7.2 MW) | 10.0% Target | -16.00% | **Warning** |
| **Average Revenue Settlement @ $1.50/kWh** | $222.30 / MWh-shed | $210.00 / MWh Target | +5.86% | **Normal** |

---

### Visualization Triggers

A comparative dual-axis horizontal bar chart is recommended to visualize price elasticity coefficients against observed percentage load reduction across commercial segments.

```json
{
  "chart_type": "bar",
  "title": "Commercial Load Reduction & Price Responsiveness @ $1.50/kWh CPP Rate",
  "categories": [
    "Cold Storage / Warehousing",
    "Heavy Commercial / Manufacturing",
    "Commercial Real Estate (Office)",
    "Retail / Grocery",
    "Hospitality / Health Care",
    "Data Centers / Tech"
  ],
  "series": [
    {
      "name": "Load Reduction (%)",
      "data": [24.8, 19.5, 16.7, 14.1, 8.4, 6.2]
    },
    {
      "name": "Price Elasticity (ε)",
      "data": [-0.182, -0.143, -0.123, -0.104, -0.062, -0.045]
    }
  ]
}
```

---

### Actionable Recommendations

- **Targeted Auto-DR Enablement**: Enroll low-elasticity commercial accounts (Data Centers, Hospitals) in automated BMS pre-cooling and battery storage dispatch programs rather than manual CPP behavioral curtailment.
- **Segmented Rate Optimization**: Evaluate raising the CPP event threshold or introducing capacity reservation credits for highly price-elastic segments (Cold Storage, Manufacturing) to incentivize sustained multi-hour shedding during 4-hour critical windows.
- **Settlement & Billing Audit**: Reconcile interval meter data (15-minute AMI) for all accounts participating under Rate Schedule CPP-COM-150 against baseline 10-in-10 day profiles to ensure accurate customer bill credits and avoid billing discrepancies.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Finalize and post critical peak surcharge line items for 35,000 participating smart meter accounts."

**Agent Response:**
### 1. Executive Summary
**Critical Peak Pricing (CPP) calculations have been compiled and audited across all 35,000 participating smart meter accounts for the designated peak dispatch window.** **The aggregate calculated surcharge totals $840,000 across 2.1 GWh of critical peak interval consumption, reflecting an effective peak load curtailment response of 18.4% against baseline forecasts.** **In accordance with utility financial governance and Tier 2 billing protocols, final invoice posting and ledger reconciliation require explicit Human-in-the-Loop (HITL) authorization prior to ledger commitment.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Participating Accounts Audited** | 35,000 accounts | 35,000 accounts | 0.0% | Normal |
| **Total CPP Event Usage** | 2,100,000 kWh | 2,573,500 kWh | -18.4% | Normal |
| **Aggregate CPP Surcharge Amount** | $840,000.00 | $547,000.00 (Standard TOU) | +53.6% | Normal |
| **Mean Surcharge per Account** | $24.00 | $15.63 | +53.6% | Normal |
| **Telemetry Interval Data Integrity** | 99.82% | ≥ 99.50% | +0.32% | Normal |
| **Flagged Variance / Exception Rate** | 0.18% (63 meters) | ≤ 0.50% | -64.0% | Normal |

---

### 3. Visualization Triggers
**Recommended Visualization:** Grouped Bar Chart – CPP Surcharge Impact vs. Standard Baseline Revenue by Customer Class.

```json
{
  "chart_type": "bar",
  "title": "CPP Surcharge Distribution by Customer Class",
  "xaxis": {
    "categories": [
      "Residential Class A",
      "Residential Class B",
      "Commercial Small",
      "Commercial Medium"
    ]
  },
  "series": [
    {
      "name": "Calculated Surcharge ($k)",
      "data": [142.5, 98.2, 215.0, 384.3]
    },
    {
      "name": "Baseline Revenue ($k)",
      "data": [85.0, 62.0, 140.0, 260.0]
    }
  ],
  "units": "USD ($k)"
}
```

---

### 4. Actionable Recommendations
- **Execute Billing Verification Review**: Verify financial staging balances against wholesale settlement logs to ensure zero double-counting with demand response credits.
- **Quarantine Exception Meters**: Route the 63 flagged meters with interval anomalies to manual billing review prior to committing batch updates.
- **Authorize Ledger Posting**: Submit Tier 2 approval to initiate mass posting to the customer information system (CIS) and enterprise billing ledger.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "POST_CPP_SURCHARGE_BATCH",
  "domain": "Billing And Invoicing",
  "target_accounts_count": 35000,
  "total_surcharge_amount_usd": 840000.00,
  "billing_cycle": "CPP-EVENT-2024-Q3-01",
  "execution_mode": "MUTATING_BATCH_LEDGER_POST",
  "risk_assessment": "HIGH (Irreversible Ledger Update / Mass Financial Impact)",
  "requires_hitl_approval": true,
  "approval_status": "PENDING_OPERATOR_CONFIRMATION"
}
```
