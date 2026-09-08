# ⚡ Estimated Bill Fallback Generator

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of estimated bill fallback generator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Estimated Bill Fallback Generator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank estimated bill fallback generator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.estimated_bill_fallback_generator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many customer bills in District 4 required estimation due to cellular AMI collector outages during the ice storm?"

**Agent Response:**
### Executive Summary
**During the recent ice storm, a total of 12,450 customer bills in District 4 required automated estimation due to prolonged cellular AMI collector tower outages.** **The Validation, Estimation, and Editing (VEE) fallback engine successfully applied historical weather-normalized load profiles (similar-day/proxy-meter baseline algorithms) to prevent billing cycle delays.** **Revenue exposure for unvalidated intervals remains within controlled variance parameters pending collector backhaul restoration and true-up reconciliations.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **District 4 Estimated Bills (AMI Outage)** | 12,450 accounts | < 250 accounts | +4,880.0% | **Critical** |
| **District 4 Cellular AMI Collector Availability** | 41.2% | ≥ 99.5% | -58.6% | **Critical** |
| **VEE Estimation Success Rate** | 98.6% | ≥ 98.0% | +0.6% | **Normal** |
| **Estimated Energy Volume (District 4)** | 14.82 GWh | 14.20 GWh (Hist.) | +4.37% | **Normal** |
| **Unreconciled Interval Revenue Exposure** | $1.86M | < $50.0k | +3,620.0% | **Warning** |

---

### Visualization Trigger

- **Recommended Chart**: Categorical Bar Chart / Spatial Node Breakdown by Substation Service Area in District 4.

```json
{
  "chart_type": "bar",
  "title": "District 4 Estimated Bills by Substation Feeder Group (Cellular Outage)",
  "data": {
    "categories": ["Substation 4A", "Substation 4B", "Substation 4C", "Substation 4D"],
    "series": [
      {
        "name": "Estimated Bills (Cellular AMI Outage)",
        "data": [4120, 3850, 2940, 1540]
      }
    ]
  }
}
```

---

### Actionable Recommendations

* **Initiate AMI Head-End Polling Queue Priority**: Coordinate with Telecom/Field Operations to prioritize battery/generator backup deployment to the offline District 4 cellular collector towers.
* **Configure Automatic True-Up Reconciliation**: Lock estimated accounts for automated Delta-True-Up billing upon the resumption of raw interval packet uploads from AMI collectors.
* **Flag High-Variance Commercial/Industrial Meters**: Manually review top 20 Tier-1 commercial accounts (>50 kW peak demand) prior to final bill delivery to mitigate dispute risks under Time-Of-Use (TOU) tariffs.
* **Regulatory Compliance Log**: Archive VEE estimation audit logs and proxy-meter baseline assumptions to comply with state PUC storm billing guidelines.

### Example 2: Trend & Comparative Analysis
**User:** "Compare heating degree-day regression estimates against subsequent actual meter read true-ups for estimated accounts."

**Agent Response:**
### Executive Summary
**Heating Degree-Day (HDD) regression fallback models demonstrated robust estimation fidelity during the winter evaluation cycle, yielding an overall aggregate volume estimation error of under 2.8% against subsequent actual meter read true-ups.** **While residential space-heating cohorts exhibited minimal net settlement adjustments ($12.40 average variance per account), commercial space-heating intervals in northern sub-zones experienced localized under-estimation (+3.12% variance) driven by sub-zero peak-load cold snaps.** **Post-cycle true-up variance reconciliations have been completed, confirming that fallback parameters remain compliant with Public Utility Commission (PUC) estimation tolerances (< ±5.0% error band).**

---

### Data Presentation: HDD Regression vs. Actual True-Up Analysis

| Metric / Cohort | Current Value (Actual True-Up) | Baseline / Target (HDD Est.) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Zone-North: Residential Space Heat (Avg kWh)** | 1,385 kWh | 1,420 kWh | -2.46% | **Normal** |
| **Zone-North: C&I Thermal/Heat Load (Avg kWh)** | 8,920 kWh | 8,650 kWh | +3.12% | **Normal** |
| **Zone-Central: Residential Space Heat (Avg kWh)** | 1,205 kWh | 1,180 kWh | +2.12% | **Normal** |
| **Zone-Central: C&I Thermal/Heat Load (Avg kWh)** | 7,110 kWh | 7,200 kWh | -1.25% | **Normal** |
| **Zone-South: Residential Space Heat (Avg kWh)** | 845 kWh | 890 kWh | -5.06% | **Warning** |
| **Zone-South: C&I Thermal/Heat Load (Avg kWh)** | 5,250 kWh | 5,100 kWh | +2.94% | **Normal** |
| **Overall Model Fit ($R^2$ Regression Coefficient)** | 0.934 $R^2$ | $\ge 0.900\ R^2$ | +3.78% | **Normal** |
| **VEE Interval Data Success Rate** | 98.6% | $\ge 98.0\%$ | +0.61% | **Normal** |
| **Net Financial Leakage / Variance per True-Up** | +$14.20 / acct | $\le \pm \$25.00$ | -43.20% | **Normal** |

---

### Visualization Configuration

A grouped comparative bar visualization has been generated to evaluate model divergence across geographical zones and rate classes:

```json
{
  "chart_type": "bar",
  "title": "HDD Regression Estimates vs. Actual Meter Read True-Ups (Winter Period)",
  "categories": [
    "Zone-North (Residential Heat)",
    "Zone-North (C&I Space Heat)",
    "Zone-Central (Residential Heat)",
    "Zone-Central (C&I Space Heat)",
    "Zone-South (Residential Heat)",
    "Zone-South (C&I Space Heat)"
  ],
  "series": [
    {
      "name": "HDD Regression Estimate (kWh Avg)",
      "data": [1420, 8650, 1180, 7200, 890, 5100]
    },
    {
      "name": "Actual True-Up (kWh Avg)",
      "data": [1385, 8920, 1205, 7110, 845, 5250]
    },
    {
      "name": "Variance (%)",
      "data": [-2.46, 3.12, 2.12, -1.25, -5.06, 2.94]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Recalibrate Base Temperature Coefficients in Zone-South**: Update the HDD reference baseline temperature from $65^\circ\text{F}$ to $62^\circ\text{F}$ for Southern zone residential cohorts to eliminate the -5.06% over-estimation bias caused by higher thermal insulation thresholds.
2. **Incorporate Wind-Chill Covariates for C&I Classes**: Enhance the primary linear HDD regression model with wind-speed vectors during sustained freeze events to tighten C&I thermal variances in Zone-North.
3. **Execute Automated True-Up Ledgering**: Process standard automated financial adjustments on subsequent monthly billing statements for accounts with estimated variances within the acceptable regulatory tolerance ($\le \pm 5\%$).
4. **Flag Outliers for AMI Field Diagnostic**: Route accounts exhibiting variance exceeding $\pm 15\%$ to Advanced Metering Infrastructure (AMI) operations to check for potential meter telemetry degradation or submetering communication failures.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate automated estimated bill statements using degree-day adjusted historical profiles for missing AMI meters."

**Agent Response:**
### Executive Summary
**Automated degree-day adjusted estimated billing has been synthesized for 1,420 missing AMI meter endpoints across billing cycle 14 to prevent unbilled interval revenue leakage. Historical baselines from the corresponding prior-year billing periods were calibrated using Heating Degree Day (HDD) and Cooling Degree Day (CDD) indices (+14.2% total thermal variance), yielding an aggregate weather-adjusted billing volume of 1,842,510 kWh ($257,951.40). All fallback estimates adhere to State PUC Rule 17 standards and are staged in pending status awaiting Human-In-The-Loop (HITL) authorization prior to ledger posting.**

---

### Quantitative Performance & Estimation Summary

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Missing AMI Telemetry Count** | 1,420 meters | < 250 meters | +468.0% | **Warning** |
| **Total Estimated Energy Volume** | 1,842,510 kWh | 1,613,400 kWh (Prior Year) | +14.2% | **Normal** |
| **Estimated Billing Revenue** | $257,951.40 | $225,876.00 (Prior Year) | +14.2% | **Normal** |
| **Degree Day Variance ($\Delta$DD)** | 485 Total DD | 422 Normal DD | +14.9% | **Normal** |
| **VEE Fallback Algorithm Confidence** | 98.4% | $\ge$ 95.0% | +3.4% | **Normal** |
| **Potential Unbilled Revenue at Risk** | $0.00 (Mitigated) | $257,951.40 | -100.0% | **Normal** |

---

### Degree-Day Adjusted Profile Breakdown by Zone & Rate Class

$$\text{Estimated Usage } (kWh) = kWh_{base, baseline\_period} \times \left[ w_{base} + w_{weather} \times \left( \frac{HDD_{actual} + CDD_{actual}}{HDD_{normal} + CDD_{normal}} \right) \right]$$

| Grid Zone / Feeder ID | Rate Class | Affected Meters | Base Period Usage (kWh) | Actual / Normal DD Ratio | Weather-Adjusted Volume (kWh) | Effective Rate ($/kWh) | Total Estimated Bill Amount ($) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zone A - Feeder 101** | Res-TOU | 450 | 369,000 | 1.152 | 425,250 | $0.1500 | $63,787.50 |
| **Zone B - Feeder 204** | Res-Flat | 380 | 296,400 | 1.144 | 338,960 | $0.1500 | $50,844.00 |
| **Zone A - Feeder 103** | Comm-Small (GS-1) | 190 | 465,500 | 1.094 | 509,200 | $0.1300 | $66,196.00 |
| **Zone C - Feeder 308** | Comm-Small (GS-1) | 120 | 372,000 | 1.071 | 398,400 | $0.1300 | $51,792.00 |
| **Zone D - Feeder 412** | Res-TOU | 280 | 249,200 | 1.140 | 284,200 | $0.1500 | $42,630.00 |
| **Total / Aggregate** | — | **1,420** | **1,752,100** | **1.121 (avg)** | **1,956,010** | — | **$275,249.50** |

*Note: Calculations apply baseload weight factor $w_{base} = 0.35$ and weather-sensitive weight factor $w_{weather} = 0.65$ for residential classes ($0.55/0.45$ for commercial).*

---

### Visualization Triggers

A **Grouped Bar Chart** has been generated to benchmark Prior Year Baseline consumption against Degree-Day Weather-Adjusted Estimates and final calculated bill revenue across affected rate classes and feeder zones.

```json
{
  "chart_type": "bar",
  "title": "Historical Baseline vs. Degree-Day Adjusted Billing Estimation",
  "data": {
    "categories": [
      "Residential-North (Zone A)",
      "Residential-East (Zone B)",
      "Commercial-Small (Zone A)",
      "Commercial-Small (Zone C)",
      "Residential-West (Zone D)"
    ],
    "series": [
      {
        "name": "Prior Year Baseline (kWh)",
        "data": [820, 780, 2450, 3100, 890]
      },
      {
        "name": "Weather-Adjusted Estimate (kWh)",
        "data": [945, 892, 2680, 3320, 1015]
      },
      {
        "name": "Estimated Revenue ($)",
        "data": [141.75, 133.80, 348.40, 431.60, 152.25]
      }
    ]
  }
}
```

---

### Actionable Recommendations

1. **Authorize Billing Batch Release**: Submit the degree-day fallback batch for billing cycle 14 to prevent cycle slippage and billing delay penalties.
2. **Issue AMI Head-End Diagnostics**: Dispatch an automated diagnostic query to the AMI Head-End Network Operations Center (NOC) for Feeders 101, 204, and 412 to investigate mesh collector communication dropouts.
3. **True-Up Protocol Staging**: Flag all 1,420 meter accounts with PUC Rule 17 "Estimated Bill - Weather Adjusted" bill line disclosure, and schedule automated true-up reconciliation upon receipt of restored interval telemetry.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "POST_ESTIMATED_BILLING_BATCH",
  "domain": "Billing And Invoicing",
  "agent": "estimated_bill_fallback_generator",
  "impact_scope": {
    "affected_accounts": 1420,
    "total_billed_kwh": 1842510,
    "total_financial_amount_usd": 257951.40,
    "billing_cycle": "Cycle 14",
    "methodology": "Degree-Day Adjusted Historical VEE Profile"
  },
  "compliance_check": {
    "puc_rule_17_compliant": true,
    "max_consecutive_estimates": 1,
    "weather_station_stationarity_verified": true
  },
  "authorization_required": "Human-In-The-Loop (Billing Operations Supervisor / Financial Controller)"
}
```
