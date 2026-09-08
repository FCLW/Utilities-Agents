# ⚡ Budget Billing Levelization Calculator

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of budget billing levelization calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Budget Billing Levelization Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank budget billing levelization calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.budget_billing_levelization_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How large is the cumulative settlement balance variance across residential budget billing participants after the winter polar vortex?"

**Agent Response:**
### Executive Summary
**Following the extreme heating degree day (HDD) anomalies associated with the winter polar vortex, the cumulative residential budget billing settlement balance has accumulated a net deferred under-collection of $16.60M across 142,500 active participants.** **This represents an average deferred balance variance of +$116.49 per participant above normalized seasonal baselines, exceeding the allowable financial levelization tolerance threshold (+15.00%) by +28.20%.** **Without mid-cycle levelization recalculation or rolling-twelve amortizations, end-of-cycle true-up reconciliation will present severe customer bill shock and heightened bad debt / working capital exposure.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Cumulative Settlement Balance Under-Collection** | $16.60M | $4.20M | +295.24% | **Critical** |
| **Average Settlement Variance per Participant** | +$116.49 | $29.47 | +295.28% | **Critical** |
| **Participant Rolling Variance Ratio** | +43.20% | ±15.00% | +28.20% | **Critical** |
| **Aggregate Energy Consumption Deviation (HDD Surge)** | 188.45 GWh | 132.80 GWh | +41.91% | **Warning** |
| **Value at Risk (VaR - 95% Confidence, 60-Day Cash Flow)** | $4.15M | $1.10M | +277.27% | **Critical** |
| **Billing VEE Interval Data Success Rate** | 99.82% | 99.50% | +0.32% | **Normal** |

---

### Visualization Triggers

A **Grouped Bar / Distribution Chart** is recommended to evaluate geographic nodal distribution across operational zones to pinpoint feeder areas experiencing the highest under-recovery.

```json
{
  "chart_type": "bar",
  "title": "Post-Polar Vortex Budget Billing Variance by Operating Zone",
  "xAxis": "Zone",
  "yAxis": "Cumulative Under-Collection ($M)",
  "series": [
    {
      "name": "Actual Under-Collection Variance",
      "data": [4.82, 3.91, 5.14, 2.73]
    },
    {
      "name": "Allowable Variance Threshold",
      "data": [1.50, 1.50, 1.50, 1.50]
    }
  ],
  "categories": [
    "Zone North (Feeder 1-4)",
    "Zone Central (Feeder 5-8)",
    "Zone East (Feeder 9-12)",
    "Zone West (Feeder 13-16)"
  ]
}
```

---

### Actionable Recommendations

- **Execute Mid-Cycle Levelization Recalibration**: Transition affected participants from standard annual settlement true-ups to a dynamic 12-month rolling recalculation model to smooth the +$116.49 average variance across remaining bill cycles.
- **Implement Nodal Risk Stratification**: Target customer outreach and mitigation programs in **Zone East** and **Zone North**, where space-heating load concentrations drove 60% of total under-collections.
- **PUC / Regulatory Compliance Alignment**: Verify that amortization adjustments comply with state Public Utility Commission (PUC) consumer protection caps on mid-year budget payment increases (e.g., max allowable monthly budget adjustment ceiling of 20–25%).

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FINANCIAL_BILLING_RECALCULATION",
  "target_population": "Residential Budget Billing Accounts (n=142,500)",
  "total_variance_to_amortize": 16600000.00,
  "proposed_mechanism": "12-Month Rolling Levelized Amortization Adjustment",
  "average_monthly_payment_delta": "+$9.71/month",
  "approval_required_from": "Billing Operations Lead & Regulatory Compliance Director",
  "status": "AWAITING_HUMAN_CONFIRMATION"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Compare the annualized rolling monthly energy spend versus actual billed amounts for customer tier R-1."

**Agent Response:**
### Executive Summary
**Customer Tier R-1 demonstrates an annualized rolling average monthly energy spend of $163.03 compared to an actual trailing 12-month average volumetric billed amount of $164.70, resulting in a tight levelization variance of -$1.67 (-1.01%). The current cumulative true-up settlement balance stands at an under-recovered +$38.17 per customer across the cohort due to elevated summer and winter peak demand intervals. Budget billing levelization algorithms are maintaining revenue stability within authorized PUC tariff thresholds (±5%), with an annual settlement adjustment scheduled for the upcoming reconciliation cycle.**

---

### Data Presentation

#### Budget Billing KPI & Levelization Summary (Tier R-1 Residential)
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Annualized Rolling Spend (Monthly Levelized)** | $163.03 | $164.70 | -1.01% | **Normal** |
| **Actual Volumetric Monthly Spend (Avg)** | $164.70 | $158.00 | +4.24% | **Normal** |
| **Average True-Up Variance Reserve** | +$38.17 | $0.00 | N/A | **Warning** |
| **VEE Interval Data Success Rate** | 99.82% | 99.50% | +0.32% | **Normal** |
| **Revenue Leakage / Unbilled Interval Rate** | 0.04% | < 0.10% | -60.00% | **Normal** |
| **Value at Risk (VaR - 95% Confidence, 30-Day)** | $42,350 | $50,000 | -15.30% | **Normal** |

#### Monthly Breakdown: Trailing 12-Month Levelization vs. Actual Billed (Tier R-1)
| Billing Month | Actual Billed ($) | Rolling Levelized Billed ($) | Monthly Variance ($) | Cumulative Settlement Balance ($) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **May 2023** | $118.40 | $154.20 | -$35.80 | -$35.80 | **Normal** |
| **Jun 2023** | $162.10 | $155.80 | +$6.30 | -$29.50 | **Normal** |
| **Jul 2023** | $214.80 | $158.40 | +$56.40 | +$26.90 | **Normal** |
| **Aug 2023** | $228.50 | $162.10 | +$66.40 | +$93.30 | **Warning** |
| **Sep 2023** | $178.20 | $163.50 | +$14.70 | +$108.00 | **Warning** |
| **Oct 2023** | $112.30 | $161.90 | -$49.60 | +$58.40 | **Normal** |
| **Nov 2023** | $125.60 | $160.70 | -$35.10 | +$23.30 | **Normal** |
| **Dec 2023** | $184.70 | $162.30 | +$22.40 | +$45.70 | **Normal** |
| **Jan 2024** | $209.40 | $165.10 | +$44.30 | +$90.00 | **Warning** |
| **Feb 2024** | $192.10 | $166.40 | +$25.70 | +$115.70 | **Warning** |
| **Mar 2024** | $134.50 | $164.80 | -$30.30 | +$85.40 | **Normal** |
| **Apr 2024** | $115.80 | $163.03 | -$47.23 | +$38.17 | **Normal** |

---

### Visualization Triggers
- **Recommended Chart**: Time-Series Line Chart with Dual-Axis True-Up Reserve Area overlay.
- **Chart Description**: Compares actual volumetric energy billing against the 12-month rolling budget billing levelization curve, illustrating seasonal smoothing across summer and winter weather peaks.

```json
{
  "chart_type": "line",
  "title": "Customer Tier R-1: Actual Billed vs. Annualized Rolling Levelized Spend (12-Month Trajectory)",
  "xAxis": {
    "categories": ["May-23", "Jun-23", "Jul-23", "Aug-23", "Sep-23", "Oct-23", "Nov-23", "Dec-23", "Jan-24", "Feb-24", "Mar-24", "Apr-24"],
    "title": "Billing Month"
  },
  "yAxis": {
    "title": "Average Monthly Spend ($/Customer)"
  },
  "series": [
    {
      "name": "Actual Volumetric Billed Amount ($)",
      "data": [118.40, 162.10, 214.80, 228.50, 178.20, 112.30, 125.60, 184.70, 209.40, 192.10, 134.50, 115.80]
    },
    {
      "name": "Annualized Rolling Levelized Amount ($)",
      "data": [154.20, 155.80, 158.40, 162.10, 163.50, 161.90, 160.70, 162.30, 165.10, 166.40, 164.80, 163.03]
    },
    {
      "name": "Cumulative True-Up Balance ($)",
      "data": [-35.80, -29.50, 26.90, 93.30, 108.00, 58.40, 23.30, 45.70, 90.00, 115.70, 85.40, 38.17]
    }
  ]
}
```

---

### Actionable Recommendations
- **Recalibrate Levelized Baseline**: Maintain the current levelized calculation factor at $163.03/month; the cumulative true-up delta (+$38.17) is amortized automatically over the shoulder spring months (April–May).
- **Automated Mid-Year Trigger Evaluation**: For customer accounts within Tier R-1 carrying a cumulative variance exceeding +$100.00, perform micro-level adjustments (+3.5% increment) ahead of the summer peak to mitigate year-end settlement bill shock.
- **VEE Settlement Verification**: Run automated interval anomaly checks for feeder zones showing deviations >10% between unbilled delivered energy and meter-aggregated billings before the annual true-up dispatch.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FINAL_BILLING_TRUE_UP_DISPATCH",
  "tier_level": 2,
  "affected_cohort": "Tier R-1 Residential Budget Billing",
  "parameters": {
    "proposed_adjusted_monthly_base": 163.03,
    "net_settlement_rebalance_amount_avg": 38.17,
    "amortization_period_months": 12,
    "human_in_the_loop_approval_required": true
  },
  "justification": "Finalization and customer notification dispatch for annual budget billing reconciliation schedule."
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Recalculate monthly budget installment amounts for accounts with variance exceeding ±20% and queue notification letters."

**Agent Response:**
### Executive Summary
**A mid-cycle levelization evaluation identified 1,420 accounts exceeding the ±20% budget-to-actual variance threshold, driven by seasonal cooling and heating degree day fluctuations. Recalculating monthly installments aligns unbilled settlement balances with forward consumption trends, mitigating an aggregate settlement risk of $384,200. Proposed rate adjustments and queued customer notification letters have been staged pending Human-In-The-Loop (HITL) authorization.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Accounts Exceeding ±20% Variance** | 1,420 Accounts | 0 Accounts | +100.0% | **Critical** |
| **Average Monthly Installment** | $213.00 / month | $238.00 / month | +11.74% | **Warning** |
| **Max Positive Variance (Under-billed)** | +42.50% | 0.00% | +42.50% | **Critical** |
| **Max Negative Variance (Over-billed)** | -31.20% | 0.00% | -31.20% | **Critical** |
| **Aggregate Settlement True-Up Balance** | $384,200.00 | $0.00 | N/A | **Warning** |
| **Levelization Cycle Compliance (PUC Rule 14)** | 99.8% | 100.0% | -0.20% | **Normal** |

---

### Visualization Trigger
- **Recommended Chart**: Grouped Bar Chart comparing current monthly installments against recalculated monthly installments by grid zone.

```json
{
  "chart_type": "bar",
  "title": "Budget Billing Installment Levelization Adjustments (> ±20% Variance)",
  "categories": [
    "Zone North (Over-billed)",
    "Zone Central (Under-billed)",
    "Zone South (Under-billed)",
    "Zone East (Under-billed)",
    "Zone West (Over-billed)"
  ],
  "series": [
    {
      "name": "Current Monthly Installment ($)",
      "data": [245.00, 180.00, 150.00, 210.00, 280.00]
    },
    {
      "name": "Recalculated Monthly Installment ($)",
      "data": [190.00, 225.00, 195.00, 260.00, 220.00]
    }
  ]
}
```

---

### Actionable Recommendations
- **Apply Recalculated Schedules**: Update the CIS (Customer Information System) budget billing profile schedules for the 1,420 flagged accounts to reflect the new 12-month rolling average.
- **Stage Tiered Communications**: Segment customer notification letters into two categories:
  - *Notice of Upward Adjustment* (under-billed accounts to avoid year-end settlement balloon payments).
  - *Notice of Downward Adjustment* (over-billed accounts with credit rollover options).
- **Monitor Interval Telemetry**: Track AMI interval readings across affected feeders to ensure seasonal heating/cooling normalization factors remain stable over the next billing cycle.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "operation": "DISPATCH_CUSTOMER_NOTIFICATIONS_AND_UPDATE_BILLING_SCHEDULE",
  "domain": "Billing And Invoicing",
  "action_type": "Tier 2 - Financial & Customer Communications",
  "details": {
    "target_account_count": 1420,
    "total_recalculated_delta_monthly": "$35,500.00",
    "notification_type": "Budget Billing Mid-Cycle Levelization Notice",
    "delivery_channels": ["Email", "USPS Direct Mail"],
    "effective_billing_cycle": "Next Immediate Billing Period (Cycle 02/2025)"
  },
  "review_status": "PENDING_OPERATOR_CONFIRMATION"
}
```

*Operator approval is required before dispatching mass customer notifications and committing financial installment changes to the live CIS billing ledger.*
