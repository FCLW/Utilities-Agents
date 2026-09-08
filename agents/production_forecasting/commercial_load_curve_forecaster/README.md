# ⚡ Commercial Load Curve Forecaster

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of commercial load curve forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Commercial Load Curve Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank commercial load curve forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.commercial_load_curve_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the day-ahead hourly megawatt demand forecast for the downtown commercial office district tomorrow?"

**Agent Response:**
### 1. Executive Summary
**The day-ahead hourly demand forecast for the Downtown Commercial Office District predicts a peak coincident load of 136.8 MW occurring at Hour Ending (HE) 14:00, driven by commercial HVAC cooling loads and standard business-hours office occupancy.** **Overall daily energy consumption is projected at 2,046.7 MWh, representing a +4.0% variance over the 30-day baseline average.** **Model uncertainty remains well within operational reliability standards with an estimated Mean Absolute Percentage Error (MAPE) of 2.85% and a 95% confidence band spanning 128.6 MW to 145.0 MW during peak hours.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Demand (HE 14:00)** | 136.8 MW | 131.5 MW | +4.03% | Normal |
| **Base / Minimum Load (HE 04:00)** | 38.2 MW | 36.8 MW | +3.80% | Normal |
| **Total Daily Energy Consumption** | 2,046.7 MWh | 1,968.1 MWh | +3.99% | Normal |
| **Morning Ramp Rate (06:00–09:00)** | +22.1 MW/hr avg | +21.3 MW/hr avg | +3.76% | Normal |
| **Evening Coincident Ramp (-)** | -21.8 MW/hr avg | -21.2 MW/hr avg | +2.83% | Normal |
| **Forecast Model Accuracy (MAPE)** | 2.85% | < 5.00% (Target) | -43.00% | Normal |
| **95% Confidence Peak Upper Bound** | 145.0 MW | 140.0 MW | +3.57% | Normal |
| **95% Confidence Peak Lower Bound** | 128.6 MW | 123.0 MW | +4.55% | Normal |
| **Peak Substation Thermal Loading** | 76.0% | 85.0% (Limit) | -10.59% | Normal |

#### Hourly Commercial Load Profile (24-Hour Schedule)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **HE 01:00 Demand** | 42.1 MW | 40.5 MW | +3.95% | Normal |
| **HE 02:00 Demand** | 39.8 MW | 38.2 MW | +4.19% | Normal |
| **HE 03:00 Demand** | 38.5 MW | 37.0 MW | +4.05% | Normal |
| **HE 04:00 Demand** | 38.2 MW | 36.8 MW | +3.80% | Normal |
| **HE 05:00 Demand** | 40.6 MW | 39.0 MW | +4.10% | Normal |
| **HE 06:00 Demand** | 52.3 MW | 50.1 MW | +4.39% | Normal |
| **HE 07:00 Demand** | 78.4 MW | 75.0 MW | +4.53% | Normal |
| **HE 08:00 Demand** | 102.6 MW | 99.2 MW | +3.43% | Normal |
| **HE 09:00 Demand** | 118.5 MW | 114.0 MW | +3.95% | Normal |
| **HE 10:00 Demand** | 126.4 MW | 121.5 MW | +4.03% | Normal |
| **HE 11:00 Demand** | 129.8 MW | 125.0 MW | +3.84% | Normal |
| **HE 12:00 Demand** | 132.5 MW | 127.8 MW | +3.68% | Normal |
| **HE 13:00 Demand** | 134.1 MW | 129.0 MW | +3.95% | Normal |
| **HE 14:00 Demand (Peak)** | 136.8 MW | 131.5 MW | +4.03% | Normal |
| **HE 15:00 Demand** | 135.2 MW | 130.0 MW | +4.00% | Normal |
| **HE 16:00 Demand** | 131.0 MW | 126.2 MW | +3.80% | Normal |
| **HE 17:00 Demand** | 118.4 MW | 114.0 MW | +3.86% | Normal |
| **HE 18:00 Demand** | 95.2 MW | 91.5 MW | +4.04% | Normal |
| **HE 19:00 Demand** | 74.6 MW | 71.8 MW | +3.90% | Normal |
| **HE 20:00 Demand** | 61.8 MW | 59.5 MW | +3.87% | Normal |
| **HE 21:00 Demand** | 53.4 MW | 51.2 MW | +4.30% | Normal |
| **HE 22:00 Demand** | 48.2 MW | 46.5 MW | +3.66% | Normal |
| **HE 23:00 Demand** | 45.0 MW | 43.5 MW | +3.45% | Normal |
| **HE 24:00 Demand** | 43.2 MW | 41.8 MW | +3.35% | Normal |

---

### 3. Visualization Triggers
**Recommended Visualization**: **Time-Series Multi-Line Chart with Confidence Bands** (Displaying Day-Ahead Point Forecast, Historical Baseline, 95% Confidence Upper/Lower Intervals).

```json
{
  "chart_type": "line",
  "title": "Day-Ahead Commercial Load Curve Forecast - Downtown Commercial Office District",
  "xAxisLabel": "Hour Ending (HE)",
  "yAxisLabel": "Megawatts (MW)",
  "series": [
    {
      "name": "Forecast Demand (MW)",
      "data": [42.1, 39.8, 38.5, 38.2, 40.6, 52.3, 78.4, 102.6, 118.5, 126.4, 129.8, 132.5, 134.1, 136.8, 135.2, 131.0, 118.4, 95.2, 74.6, 61.8, 53.4, 48.2, 45.0, 43.2]
    },
    {
      "name": "Baseline / Historical (MW)",
      "data": [40.5, 38.2, 37.0, 36.8, 39.0, 50.1, 75.0, 99.2, 114.0, 121.5, 125.0, 127.8, 129.0, 131.5, 130.0, 126.2, 114.0, 91.5, 71.8, 59.5, 51.2, 46.5, 43.5, 41.8]
    },
    {
      "name": "95% CI Upper (MW)",
      "data": [44.6, 42.2, 40.8, 40.5, 43.0, 55.4, 83.1, 108.8, 125.6, 134.0, 137.6, 140.5, 142.1, 145.0, 143.3, 138.9, 125.5, 100.9, 79.1, 65.5, 56.6, 51.1, 47.7, 45.8]
    },
    {
      "name": "95% CI Lower (MW)",
      "data": [39.6, 37.4, 36.2, 35.9, 38.2, 49.2, 73.7, 96.4, 111.4, 118.8, 122.0, 124.5, 126.1, 128.6, 127.1, 123.1, 111.3, 89.5, 70.1, 58.1, 50.2, 45.3, 42.3, 40.6]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Day-Ahead Generation Commitment**: Ensure committed dispatch capacity accounts for the steep morning ramp between HE 06:00 and HE 09:00 (+66.2 MW total rise over 3 hours).
- **Substation Thermal Reserve**: Downtown feeder capacity headroom is sufficient (peak loading at 76.0% vs. 85.0% operational threshold); no localized commercial demand-response curtailment calls are required at this time.
- **Intraday Telemetry Ingestion**: Continue monitoring SCADA net-metering telemetry from large commercial office cooling plant start-ups between 05:30 and 07:00 to detect any pre-cooling anomalies ahead of the afternoon peak.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze temperature sensitivity and commercial occupancy patterns driving air conditioning demand between 13:00 and 18:00."

**Agent Response:**
### 1. Executive Summary
**Commercial cooling demand between 13:00 and 18:00 exhibits a high temperature sensitivity coefficient of 18.4 MW/°F above the 72°F base temperature, driving peak HVAC demand to 498.2 MW at 16:00. While commercial building occupancy peaks early in the window (88.5% at 14:00) and declines toward 18:00 (41.5%), building thermal inertia combined with maximum ambient dry-bulb temperatures (94.1°F) shifts the coincident peak cooling load later into the 15:00–17:00 operational window. Overall commercial sector load curve forecast maintains a Mean Absolute Percentage Error (MAPE) of 2.85%, well within the utility standard <5.0% threshold at a 95% confidence interval.**

---

### 2. Data Presentation

The table below summarizes commercial sector telemetry, HVAC temperature response, and occupancy metrics across the peak demand window (13:00–18:00):

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Commercial HVAC Demand (16:00)** | 498.2 MW | 445.0 MW | +11.96% | **Warning** |
| **Aggregate Commercial Feeder Load (16:00)** | 803.3 MW | 750.1 MW | +7.09% | **Warning** |
| **Temperature Sensitivity Slope ($>72^\circ\text{F}$)** | 18.4 MW/°F | 16.2 MW/°F | +13.58% | **Warning** |
| **Peak Occupancy Index (14:00)** | 88.5% | 85.0% | +4.12% | **Normal** |
| **Late Afternoon Occupancy Index (17:00)** | 62.0% | 65.0% | -4.62% | **Normal** |
| **Mean Absolute Percentage Error (MAPE)** | 2.85% | < 5.00% | -43.00% | **Normal** |
| **Cooling Degree Hours (CDH, Base 65°F)** | 26.8 CDH | 22.1 CDH | +21.27% | **Warning** |
| **Feeder Thermal Headroom Margin** | 12.4% | > 15.0% | -17.33% | **Warning** |

---

### 3. Visualization Triggers

* **Recommended Visualization**: Dual-Axis Time-Series Line Chart (Coincident Peak HVAC Load vs. Temperature & Occupancy Trajectory).
* **Telemetry Data Payload**:

```json
{
  "chart_type": "line",
  "title": "Commercial Load & HVAC Sensitivity vs Occupancy (13:00 - 18:00)",
  "xAxis": {
    "categories": ["13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
    "title": "Hour Ending"
  },
  "yAxis": [
    {
      "title": "Load (MW)",
      "opposite": false
    },
    {
      "title": "Temperature (°F) / Occupancy (%)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Commercial HVAC Load (MW)",
      "type": "line",
      "yAxis": 0,
      "data": [412.4, 458.1, 485.6, 498.2, 472.0, 421.8]
    },
    {
      "name": "Baseline Non-HVAC Load (MW)",
      "type": "line",
      "yAxis": 0,
      "data": [310.2, 312.0, 308.5, 305.1, 290.4, 260.5]
    },
    {
      "name": "Ambient Temperature (°F)",
      "type": "line",
      "yAxis": 1,
      "data": [88.5, 91.2, 93.4, 94.1, 92.8, 89.6]
    },
    {
      "name": "Commercial Occupancy Rate (%)",
      "type": "line",
      "yAxis": 1,
      "data": [86.0, 88.5, 84.0, 78.5, 62.0, 41.5]
    }
  ]
}
```

---

### 4. Actionable Recommendations

* **Pre-Cooling Dispatch**: Recommend initiating commercial pre-cooling protocols between 10:30 and 12:30 (ramping target setpoints down by 2°F to 3°F) to leverage commercial thermal mass and flatten the 15:00–17:00 HVAC spike.
* **Commercial Demand Response (C-DR) Targeting**: Coordinate with the Demand Response aggregator to ready Stage-1 commercial curtailment (targeting 35 MW reduction between 15:30 and 17:30) if substation headroom drops below 10.0%.
* **Feeder-Level Thermal Monitoring**: Maintain 5-minute telemetry scan rates on high commercial density substations where ambient temperatures $>93^\circ\text{F}$ exacerbate transformer insulation aging.
* **Model Re-calibration**: Update the rolling regression coefficients for the 17:00–18:00 egress window, incorporating occupancy decay rates to optimize evening ramp-down forecasting.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Commit the revised 24-hour commercial load forecast to the day-ahead energy trading and procurement scheduling system."

**Agent Response:**
### Executive Summary
**The revised 24-hour commercial load curve forecast indicates a peak commercial demand of 1,248.5 MW across active grid zones, representing a +3.2% deviation from the day-ahead baseline due to updated cooling degree day (CDD) models. Model validation confirms a forecast Mean Absolute Percentage Error (MAPE) of 2.14%, well within the operational threshold of < 5.0%. Autonomous commit to the day-ahead procurement scheduling system constitutes a Tier 2 financial and market commitment operation and requires Human-in-the-Loop (HITL) operator confirmation.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Commercial Load** | 1,248.5 MW | 1,209.8 MW | +3.20% | Normal |
| **Total 24-Hour Energy Volume** | 24,860 MWh | 24,150 MWh | +2.94% | Normal |
| **Forecast Model MAPE** | 2.14% | < 5.00% | -57.20% | Normal |
| **95% CI Lower Bound (Off-Peak)** | 710.2 MW | 705.0 MW | +0.74% | Normal |
| **95% CI Upper Bound (Peak Hour)** | 1,298.4 MW | 1,250.0 MW | +3.87% | Warning |

---

### Visualization Trigger

```json
{
  "chart_type": "line",
  "title": "24-Hour Commercial Load Curve: Baseline vs Revised Forecast",
  "data": [
    {"hour": "00:00", "baseline_mw": 720, "revised_mw": 728},
    {"hour": "04:00", "baseline_mw": 695, "revised_mw": 702},
    {"hour": "08:00", "baseline_mw": 980, "revised_mw": 1010},
    {"hour": "12:00", "baseline_mw": 1180, "revised_mw": 1220},
    {"hour": "16:00", "baseline_mw": 1210, "revised_mw": 1248},
    {"hour": "20:00", "baseline_mw": 950, "revised_mw": 980},
    {"hour": "23:00", "baseline_mw": 780, "revised_mw": 795}
  ]
}
```

---

### Actionable Recommendations
- **Market Scheduling Review**: Verify day-ahead wholesale procurement positions against the +710 MWh net increase across the 24-hour dispatch cycle.
- **Substation Headroom Verification**: Confirm that primary commercial feeders in Grid Zones 2 and 4 maintain adequate transformer thermal margin during the 14:00–17:00 peak window.
- **Operator Authorization**: Review and authorize the Tier 2 commitment payload below to transmit the updated hourly schedule to the wholesale day-ahead market portal.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_id": "COMM_LOAD_COMMIT_DA_20241024",
  "action_type": "DAY_AHEAD_PROCUREMENT_SCHEDULE_COMMIT",
  "agent": "commercial_load_curve_forecaster",
  "target_system": "Energy Trading & Risk Management (ETRM) / Day-Ahead Scheduling System",
  "parameters": {
    "schedule_horizon": "24_HOURS",
    "total_mwh": 24860.0,
    "peak_load_mw": 1248.5,
    "peak_interval": "16:00-17:00",
    "mape_score": 0.0214,
    "financial_impact_level": "TIER_2_WHOLESALE_TRANSACTION"
  },
  "status": "AWAITING_OPERATOR_APPROVAL",
  "instructions": "Confirm to execute automated transmission of the revised 24-hour hourly load curve to the day-ahead procurement scheduling engine."
}
```
