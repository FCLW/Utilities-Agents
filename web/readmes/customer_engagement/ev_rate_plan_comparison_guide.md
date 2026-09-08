# ⚡ Ev Rate Plan Comparison Guide

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of ev rate plan comparison guide is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Ev Rate Plan Comparison Guide Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank ev rate plan comparison guide events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.ev_rate_plan_comparison_guide_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which rate plan will minimize my monthly electric costs if I charge an EV with a 75 kWh battery exclusively overnight?"

**Agent Response:**
### Executive Summary
**For a customer charging a 75 kWh EV battery exclusively overnight, a dedicated EV Time-of-Use (EV-TOU / Super Off-Peak) rate plan delivers the lowest total monthly operating cost.** **By shifting EV charging load to the designated super off-peak hours (typically 12:00 AM – 6:00 AM), energy supply costs are reduced by approximately 57.7% compared to standard flat or tiered baseline rates.** **Customers must ensure that non-charging household load is minimized during peak demand windows (4:00 PM – 9:00 PM) to maintain net savings.**

---

### Data Presentation

The analysis models an average monthly driving requirement of ~1,100 miles (~375 kWh/month in EV charging demand) combined with an average baseline household consumption of 600 kWh/month.

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Dedicated EV-TOU Overnight Rate** | $0.11 / kWh | $0.26 / kWh (Flat Rate) | -57.7% | Normal |
| **Monthly EV Charging Cost (EV-TOU)** | $41.25 | $97.50 (Flat Baseline) | -57.7% | Normal |
| **Monthly EV Charging Cost (Standard TOU)**| $71.25 | $97.50 (Flat Baseline) | -26.9% | Normal |
| **Total Estimated Monthly Bill (EV + Home)**| $183.25 | $253.50 (Flat Baseline) | -27.7% | Normal |
| **Annualized EV Fueling Savings** | $675.00 / yr | $0.00 / yr (Baseline) | +100.0% | Normal |
| **On-Peak Price Sensitivity Exposure** | $0.54 / kWh | $0.26 / kWh (Flat Baseline) | +107.7% | Warning |

*Analytical Assumptions:*
- *EV Battery: 75 kWh nominal capacity.*
- *Charge Schedule: Managed charging scheduled via Level 2 EVSE exclusively between 12:00 AM and 6:00 AM.*
- *Household Non-EV Consumption: 600 kWh/month with standard 80% off-peak / 20% on-peak distribution.*

---

### Visualization Triggers

**Recommended Visualization:** Comparative Multi-Bar Chart displaying monthly cost components (EV Charging vs. Base Household Load) across candidate rate structures.

```json
{
  "chart_type": "bar",
  "title": "Monthly Electric Cost Comparison for Overnight EV Charging",
  "xAxis": {
    "categories": [
      "Standard Flat Rate",
      "Standard TOU Plan",
      "Dedicated EV-TOU Plan (Recommended)"
    ]
  },
  "yAxis": {
    "title": "Cost (USD)"
  },
  "series": [
    {
      "name": "EV Charging Cost ($)",
      "data": [97.50, 71.25, 41.25]
    },
    {
      "name": "Household Baseline Cost ($)",
      "data": [156.00, 148.00, 142.00]
    },
    {
      "name": "Total Monthly Bill ($)",
      "data": [253.50, 219.25, 183.25]
    }
  ]
}
```

---

### Actionable Recommendations

- **Enroll in Dedicated EV-TOU Rate**: Transition your utility tariff to the EV-specific Time-of-Use schedule to capture the super off-peak rate during overnight hours.
- **Configure Vehicle / EVSE Timer**: Program the vehicle or smart Level 2 charger schedule strictly for the Super Off-Peak window (e.g., 12:00 AM to 6:00 AM) to prevent accidental high-cost charging during peak hours (4:00 PM – 9:00 PM).
- **Audit Household Peak Consumption**: Mitigate higher on-peak energy rates by scheduling major residential appliances (dishwashers, dryers, HVAC pre-cooling) outside the 4:00 PM – 9:00 PM peak period.
- **Smart Meter Telemetry Validation**: Check the initial billing cycle following the rate change to verify that AMI interval data correctly reflects the overnight load shift.

### Example 2: Trend & Comparative Analysis
**User:** "Compare projected annual energy expenses under the Standard Residential Tier versus the EV Time-of-Use Plan."

**Agent Response:**
### Executive Summary
**Transitioning an electric vehicle (EV) owner from the Standard Residential Tier rate to a dedicated EV Time-of-Use (EV-TOU) rate plan generates projected annual net savings of $166.80 to $452.40 depending on charging automation efficiency.** **By shifting 85% or more of vehicle charging load to super off-peak hours (11:00 PM – 7:00 AM), effective EV fuel electricity costs decrease by 48.5% compared to baseline volumetric tiered pricing.** **Adoption of the EV-TOU plan significantly dampens peak grid demand during the 4:00 PM – 9:00 PM distribution system stress window.**

---

### Data Presentation

*Analytical Baseline Assumption: Standard customer profile with 7,200 kWh/year base residential load plus 3,000 kWh/year EV charging load (approx. 10,500 miles/year at 3.5 mi/kWh).*

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Annual Electricity Cost (Total)** | $2,101.20 | $2,268.00 (Std Tier) | -7.35% | Normal |
| **EV-Specific Annual Charging Cost** | $402.00 | $780.00 (Std Tier) | -48.46% | Normal |
| **Effective EV Rate ($/kWh)** | $0.134 / kWh | $0.260 / kWh (Tier 2) | -48.46% | Normal |
| **Off-Peak EV Load Concentration** | 85.0% | 20.0% (Unmanaged) | +325.00% | Normal |
| **On-Peak EV Demand Contribution** | 5.0% | 35.0% (Unmanaged) | -85.71% | Normal |
| **Gasoline Equivalent Cost ($/gal equiv.)** | $1.15 / GGE | $2.23 / GGE (Std Tier) | -48.43% | Normal |

---

### Visualization Triggers

**Recommended Chart Type:** Grouped Bar / Monthly Expense Comparison Chart

```json
{
  "chart_type": "bar",
  "title": "Projected Monthly Energy Expense: Standard Tier vs. EV-TOU",
  "xAxis": {
    "categories": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
  },
  "yAxis": {
    "title": "Monthly Expense ($ USD)"
  },
  "series": [
    {
      "name": "Standard Residential Tier ($)",
      "data": [189.0, 182.5, 175.2, 171.0, 184.3, 212.8, 235.4, 241.2, 205.6, 178.0, 169.5, 183.5]
    },
    {
      "name": "EV Time-of-Use Plan ($)",
      "data": [174.2, 168.0, 161.8, 158.5, 169.0, 198.5, 219.0, 224.6, 192.1, 164.5, 156.2, 169.8]
    }
  ]
}
```

---

### Actionable Recommendations

- **Automated Charge Scheduling:** Configure the EV on-board timer or Level 2 EVSE (Electric Vehicle Supply Equipment) to initiate charging automatically at 11:00 PM (Super Off-Peak window) to capture the lowest tariff tier ($0.11/kWh).
- **Peak Load Shifting:** Restrict major home appliances (dryers, dishwashers, pool pumps) between 4:00 PM and 9:00 PM (On-Peak rate: $0.39/kWh) to avoid erosion of TOU rate benefits.
- **Smart Charging & Telematics Enrollment:** Enroll the customer in utility Managed Charging / Demand Response programs for additional annual grid service bill credits ($50–$100/yr).
- **Rate Switch Execution:** Offer the customer one-click migration to the EV-TOU tariff structure via the customer portal or support agent workflow.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Switch Customer Account #773829 to the EV-TOU rate schedule effective with the upcoming meter billing cycle."

**Agent Response:**
### Executive Summary
**Customer Account #773829 has been evaluated for migration from the Standard Tiered/Flat Rate (Schedule D) to the Electric Vehicle Time-of-Use (EV-TOU-2) rate plan. Based on smart meter interval data and overnight EV charging patterns (12:00 AM – 6:00 AM), transitioning to the EV-TOU rate schedule yields an estimated 25.8% reduction in total monthly energy billing costs. Executing a rate plan modification on an active utility customer account is a Tier 2 financial and administrative action requiring explicit Human-In-The-Loop (HITL) authorization prior to billing system commitment.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Off-Peak Energy Rate** | $0.150 / kWh | $0.320 / kWh (Flat) | -53.1% | Normal |
| **On-Peak Energy Rate (4–9 PM)** | $0.540 / kWh | $0.320 / kWh (Flat) | +68.8% | Warning |
| **Off-Peak EV Load Share** | 78.4% | > 70.0% (Target) | +12.0% | Normal |
| **Estimated Monthly Bill** | $182.20 | $245.50 (Baseline) | -25.8% | Normal |
| **Annualized Cost Savings** | $759.60 / yr | $0.00 / yr (Baseline) | N/A | Normal |
| **Peak Coincident Demand Risk** | 1.8 kW | < 2.5 kW (Threshold) | -28.0% | Normal |

---

### Visualization Triggers
**Recommended Chart Type:** Comparative Bar Chart (Cost & Rate Structure Comparison: Standard Tiered vs. EV-TOU Schedule)

```json
{
  "chart_type": "bar",
  "title": "Rate Plan Cost Comparison for Account #773829",
  "xAxis": {
    "title": "Period / Metric",
    "categories": [
      "Super Off-Peak Rate ($/kWh)",
      "Off-Peak Rate ($/kWh)",
      "On-Peak Rate ($/kWh)",
      "Est. Monthly Bill ($)"
    ]
  },
  "yAxis": {
    "title": "Value ($ / $/kWh)"
  },
  "series": [
    {
      "name": "Standard Rate (Current)",
      "data": [0.32, 0.32, 0.32, 245.50]
    },
    {
      "name": "EV-TOU Rate (Proposed)",
      "data": [0.15, 0.28, 0.54, 182.20]
    }
  ]
}
```

---

### Actionable Recommendations
* **Submit Schedule Change for Approval:** Authorize the Tier 2 account schedule modification to align the rate switch with the upcoming meter billing cycle anchor date.
* **Enroll Customer in Automated Off-Peak Charging Program:** Dispatch TOU schedule educational materials and offer enrollment in smart charging integration to lock in >75% off-peak charging compliance.
* **Establish Bill Protection & 90-Day Review:** Configure automated 90-day post-transition billing audit to verify anticipated savings and alert if on-peak charging exceeds 15% of total consumption.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "RATE_SCHEDULE_CHANGE",
  "account_id": "773829",
  "current_rate_schedule": "DOMESTIC_STANDARD_TIERED",
  "requested_rate_schedule": "EV_TOU_2",
  "effective_date": "NEXT_BILLING_CYCLE",
  "financial_impact_estimate_annual": "-$759.60",
  "requires_approval": true,
  "approval_role": "Customer_Engagement_Supervisor",
  "status": "PENDING_CONFIRMATION"
}
```
