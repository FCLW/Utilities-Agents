# ⚡ Wind Speed Generation Modeler

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of wind speed generation modeler is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Wind Speed Generation Modeler Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank wind speed generation modeler events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.wind_speed_generation_modeler_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the day-ahead wind power production forecast (MW) for Plains Wind Farm based on 80-meter hub height wind speeds?"

**Agent Response:**
### Executive Summary
**The day-ahead wind power production forecast for Plains Wind Farm (nameplate capacity: 250.0 MW) projects a daily average output of 139.1 MW with an expected peak of 214.0 MW at 21:00 UTC.** **Wind speeds at 80-meter hub height are modeled to average 9.1 m/s over the 24-hour dispatch horizon, driving an aggregate daily energy yield of 3,338.4 MWh with a 95% confidence interval of [3,185.2 MWh, 3,491.6 MWh].** **Model performance metrics indicate an expected Mean Absolute Percentage Error (MAPE) of 3.84%, well within the utility standard < 5.00% compliance threshold.**

---

### Data Presentation

#### Generation Forecast Summary & Operational KPIs

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Average 80m Hub Height Wind Speed** | 9.12 m/s | 8.50 m/s | +7.29% | Normal |
| **Peak 80m Hub Height Wind Speed** | 11.90 m/s | 12.00 m/s | -0.83% | Normal |
| **Forecast Mean Power Output** | 139.10 MW | 125.00 MW | +11.28% | Normal |
| **Forecast Peak Power Output** | 214.00 MW | 250.00 MW (Nameplate) | -14.40% | Normal |
| **Total Daily Energy Yield** | 3,338.40 MWh | 3,000.00 MWh | +11.28% | Normal |
| **Capacity Factor (Day-Ahead)** | 55.64% | 50.00% | +11.28% | Normal |
| **Forecast MAPE (Backtested/Validated)** | 3.84% | < 5.00% | -23.20% | Normal |
| **Cut-Out Wind Risk (> 25.0 m/s)** | 0.00% Prob. | 0.00% Prob. | 0.00% | Normal |

---

#### 24-Hour Day-Ahead Generation & Wind Profile Breakdown

| Hour (UTC) | 80m Wind Speed (m/s) | Power Output (MW) | 95% CI Lower (MW) | 95% CI Upper (MW) | Capacity Factor (%) |
| :---: | :---: | :---: | :---: | :---: | :---: |
| **00:00** | 7.2 | 82.4 | 77.2 | 87.6 | 32.96% |
| **01:00** | 7.8 | 98.6 | 92.5 | 104.7 | 39.44% |
| **02:00** | 8.4 | 118.2 | 111.4 | 125.0 | 47.28% |
| **03:00** | 9.1 | 142.5 | 135.2 | 149.8 | 57.00% |
| **04:00** | 9.8 | 168.0 | 160.1 | 175.9 | 67.20% |
| **05:00** | 10.5 | 188.4 | 180.2 | 196.6 | 75.36% |
| **06:00** | 11.2 | 201.2 | 192.9 | 209.5 | 80.48% |
| **07:00** | 11.8 | 212.5 | 204.0 | 221.0 | 85.00% |
| **08:00** | 11.4 | 206.8 | 198.3 | 215.3 | 82.72% |
| **09:00** | 10.2 | 181.3 | 173.0 | 189.6 | 72.52% |
| **10:00** | 8.9 | 134.7 | 127.3 | 142.1 | 53.88% |
| **11:00** | 7.5 | 91.5 | 85.6 | 97.4 | 36.60% |
| **12:00** | 6.8 | 71.2 | 66.1 | 76.3 | 28.48% |
| **13:00** | 6.2 | 54.8 | 50.4 | 59.2 | 21.92% |
| **14:00** | 5.9 | 48.2 | 44.1 | 52.3 | 19.28% |
| **15:00** | 6.5 | 62.1 | 57.3 | 66.9 | 24.84% |
| **16:00** | 7.4 | 88.3 | 82.7 | 93.9 | 35.32% |
| **17:00** | 8.6 | 126.4 | 119.5 | 133.3 | 50.56% |
| **18:00** | 9.7 | 164.7 | 156.9 | 172.5 | 65.88% |
| **19:00** | 10.8 | 195.1 | 186.8 | 203.4 | 78.04% |
| **20:00** | 11.5 | 208.7 | 200.2 | 217.2 | 83.48% |
| **21:00** | 11.9 | 214.0 | 205.6 | 222.4 | 85.60% |
| **22:00** | 11.2 | 202.9 | 194.5 | 211.3 | 81.16% |
| **23:00** | 9.6 | 158.6 | 151.0 | 166.2 | 63.44% |

---

### Visualization Trigger

**Recommended Chart Type**: Multi-Axis Time-Series Line Chart (Wind Speed vs. Power Output with 95% Confidence Bounds).

```json
{
  "chart_type": "line",
  "title": "Plains Wind Farm - Day-Ahead 80m Hub Height Wind Speed vs. Generation Forecast",
  "categories": [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00",
    "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
  ],
  "series": [
    {
      "name": "80m Hub Height Wind Speed (m/s)",
      "data": [7.2, 7.8, 8.4, 9.1, 9.8, 10.5, 11.2, 11.8, 11.4, 10.2, 8.9, 7.5, 6.8, 6.2, 5.9, 6.5, 7.4, 8.6, 9.7, 10.8, 11.5, 11.9, 11.2, 9.6],
      "unit": "m/s",
      "yAxis": 1
    },
    {
      "name": "Forecast Generation (MW)",
      "data": [82.4, 98.6, 118.2, 142.5, 168.0, 188.4, 201.2, 212.5, 206.8, 181.3, 134.7, 91.5, 71.2, 54.8, 48.2, 62.1, 88.3, 126.4, 164.7, 195.1, 208.7, 214.0, 202.9, 158.6],
      "unit": "MW",
      "yAxis": 0
    }
  ]
}
```

---

### Actionable Recommendations

- **Day-Ahead Market Bidding**: Submit day-ahead generation schedules utilizing the P50 forecast (139.1 MW mean / 3,338.4 MWh total) to optimize market positions and minimize uninstructed imbalance penalties.
- **Ramping & Reserve Scheduling**:
  - Alert the transmission operations desk to a morning down-ramp from 07:00 to 14:00 UTC (-164.3 MW drop) corresponding to midday wind lull.
  - Prepare flexible ramping reserves for the evening surge between 15:00 and 21:00 UTC (+165.8 MW increase).
- **Wake & Turbine Availability Verification**: Coordinate with plant operations to ensure all turbine strings are cleared of scheduled maintenance outages during high-yield blocks (05:00–09:00 UTC and 19:00–23:00 UTC).
- **Intraday Telemetry Ingestion**: Trigger the 4-hour rolling high-resolution ensemble update to refine curtailment and congestion forecasts across the Plains transmission corridor.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze wind turbine power curves and high-speed wind cut-out risks (> 25 m/s) associated with the approaching cold front."

**Agent Response:**
### 1. Executive Summary
**The incoming cold front is forecast to deliver sustained wind speeds exceeding 26.5 m/s with peak gusts up to 31.0 m/s across northern and western generation corridors, breaching the standard IEC Class II/III high-speed cut-out threshold (25.0 m/s). Without preemptive soft cut-out and high-wind ride-through (HWRT) management, the fleet faces an abrupt loss of up to 1,450 MW of generation within a 45-minute frontal boundary transit window. Grid operators must immediately activate ramp-rate curtailment and stage fast-ramping spinning reserves to prevent severe frequency excursions (N-1/N-2 contingency events).**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Forecast Sustained Wind Speed** | 26.8 m/s | 12.5 m/s (Rated Peak) | +114.4% | **Critical** |
| **Forecast Peak Gust Speed** | 31.2 m/s | 25.0 m/s (Cut-out Limit) | +24.8% | **Critical** |
| **Fleet Generation at Risk** | 1,450 MW | 1,600 MW (Nameplate Active) | -90.6% | **Critical** |
| **Forecast Generation Ramp-Down Rate** | -32.2 MW/min | ≤ -10.0 MW/min (Max Grid Ramp) | +222.0% | **Critical** |
| **Ambient Air Density Correction** | 1.310 kg/m³ | 1.225 kg/m³ (Standard ISA) | +6.9% | **Warning** |
| **Forecast Model Error (MAPE)** | 3.8% | < 5.0% | -24.0% | **Normal** |

---

### 3. Visualization Triggers

**Recommended Chart Type:** Time-Series & Power Curve Superposition Line Chart  
*Visualizing the transition from full rated output to sudden aerodynamic/mechanical tripping vs. progressive soft de-rating across wind speeds from 0 to 30 m/s.*

```json
{
  "chart_type": "line",
  "title": "Turbine Power Curve & High-Speed Cut-Out Profiles",
  "xAxis": {
    "label": "Wind Speed (m/s)",
    "data": [0, 3, 6, 9, 12, 15, 18, 21, 24, 25, 26, 28, 30]
  },
  "yAxis": {
    "label": "Generation Output (% of Rated)",
    "unit": "%"
  },
  "series": [
    {
      "name": "Standard Hard Cut-Out (25 m/s Trip)",
      "data": [0, 0, 15, 55, 95, 100, 100, 100, 100, 0, 0, 0, 0]
    },
    {
      "name": "High-Wind Soft De-Rate Control (HWRT)",
      "data": [0, 0, 15, 55, 95, 100, 100, 92, 75, 50, 30, 10, 0]
    },
    {
      "name": "Approaching Front Probability Band",
      "data": [null, null, null, null, null, null, null, 20, 65, 90, 95, 80, 40]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Engage High-Wind Ride-Through (HWRT) Protocols**: Transition eligible turbines from hard-trip cut-out logic to progressive pitch de-rating between 22 m/s and 28 m/s to dampen the aggregate generation cliff.
- **Pre-Stage Fast-Ramping Reserves**: Coordinate with balancing authority and dispatch operators to stage 1,200+ MW of fast-start thermal and BESS (Battery Energy Storage System) capacity prior to frontal arrival at T-60 minutes.
- **Air Density Re-Calibration**: Re-calibrate power curve lookups for air density shift ($\rho = 1.310\text{ kg/m}^3$), which shifts rated power capture to lower wind speeds (~10.8 m/s) and amplifies mechanical aerodynamic loads.
- **Implement Tiered Group Feeder Shutdowns**: For older turbine assets without soft cut-out capabilities, execute staggered shut-down schedules rather than allowing simultaneous aggregate breaker trips.

---

### 5. HITL / Tier 2 Formats

[TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "HIGH_WIND_DE_RATE_SCHEDULE_EXECUTION",
  "grid_zone_id": "ZONE-WEST-WIND-CORRIDOR",
  "impacted_capacity_mw": 1450.0,
  "execution_window_utc": "2025-01-16T18:00:00Z to 2025-01-16T22:30:00Z",
  "justification": "Mitigate instantaneous generation drop-off (>30 MW/min) caused by cold-front wind gusts exceeding 25 m/s cut-out limits by commanding proactive soft ramp-down and HWRT curtailment schedules.",
  "recommended_approver": "Lead Grid Balance Operator / Generation Dispatch Manager",
  "contingency_reserve_required_mw": 1200.0,
  "requires_hitl_approval": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit the 24-hour hourly wind energy generation schedule to the RTO scheduling portal."

**Agent Response:**
### Executive Summary
**The 24-hour wind generation forecast model has aggregated an expected total output of 2,890.0 MWh across the operating day, maintaining an average model confidence interval of 95% and a predicted MAPE of 3.8%. Peak generation is projected during off-peak overnight hours (03:00–04:00 and 20:00–21:00) with sustained wind speeds exceeding 9.2 m/s. Direct submission of generation schedules to external RTO scheduling portals constitutes a Tier 2 physical market commitment and requires explicit Human-in-the-Loop (HITL) authorization.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **24-Hour Total Generation** | 2,890.0 MWh | 2,740.0 MWh | +5.47% | Normal |
| **Peak Hourly Output (03:00)** | 160.1 MW | 150.0 MW | +6.73% | Normal |
| **Minimum Hourly Output (13:00)** | 68.4 MW | 65.0 MW | +5.23% | Normal |
| **Mean Wind Speed (Hub Height)** | 7.85 m/s | 7.40 m/s | +6.08% | Normal |
| **Forecast Model MAPE** | 3.80% | < 5.00% | -24.00% | Normal |
| **95% Confidence Band Spread** | ±12.4 MW | ±15.0 MW | -17.33% | Normal |

---

### Visualization Triggers
**Recommended Visualization:** Time-Series Line Chart (24-Hour Day-Ahead Generation Profile vs. Baseline)

```json
{
  "chart_type": "line",
  "title": "24-Hour Wind Generation Schedule Forecast vs. Baseline",
  "x_axis_label": "Hour (HE)",
  "y_axis_label": "Generation (MW)",
  "labels": [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00",
    "06:00", "07:00", "08:00", "09:00", "10:00", "11:00",
    "12:00", "13:00", "14:00", "15:00", "16:00", "17:00",
    "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
  ],
  "datasets": [
    {
      "label": "Model Forecast (MW)",
      "data": [142.5, 148.0, 155.2, 160.1, 158.4, 150.2, 138.6, 125.0, 110.4, 98.2, 85.0, 78.5, 72.0, 68.4, 75.1, 88.3, 105.0, 122.4, 140.0, 152.6, 161.0, 159.5, 151.2, 145.0]
    },
    {
      "label": "Day-Ahead Baseline (MW)",
      "data": [135.0, 140.0, 145.0, 150.0, 150.0, 145.0, 130.0, 120.0, 105.0, 95.0, 80.0, 75.0, 70.0, 65.0, 70.0, 85.0, 100.0, 115.0, 130.0, 145.0, 150.0, 150.0, 145.0, 140.0]
    }
  ]
}
```

---

### Actionable Recommendations
- **Operator Review**: Review the 24-hour generation schedule profile against current RTO transmission congestion notices and active curtailment flags.
- **Ramp-Rate Monitoring**: Maintain operational vigilance between HE06–HE13 where modeled wind speed ramps down from 150.2 MW to 68.4 MW (-54.5%).
- **HITL Submission Approval**: Review and authorize the schedule submission payload below to execute the external market transaction in compliance with NERC/FERC standards.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "RTO_SCHEDULE_SUBMISSION",
  "target_entity": "RTO_Scheduling_Portal_API",
  "payload": {
    "market_run": "DAY_AHEAD",
    "operating_day": "NEXT_OPERATING_DAY",
    "resource_type": "WIND_FLEET_AGGREGATE",
    "total_forecast_mwh": 2890.0,
    "hourly_mw_schedule": [
      {"hour": 1, "mw": 142.5}, {"hour": 2, "mw": 148.0}, {"hour": 3, "mw": 155.2}, {"hour": 4, "mw": 160.1},
      {"hour": 5, "mw": 158.4}, {"hour": 6, "mw": 150.2}, {"hour": 7, "mw": 138.6}, {"hour": 8, "mw": 125.0},
      {"hour": 9, "mw": 110.4}, {"hour": 10, "mw": 98.2}, {"hour": 11, "mw": 85.0}, {"hour": 12, "mw": 78.5},
      {"hour": 13, "mw": 72.0}, {"hour": 14, "mw": 68.4}, {"hour": 15, "mw": 75.1}, {"hour": 16, "mw": 88.3},
      {"hour": 17, "mw": 105.0}, {"hour": 18, "mw": 122.4}, {"hour": 19, "mw": 140.0}, {"hour": 20, "mw": 152.6},
      {"hour": 21, "mw": 161.0}, {"hour": 22, "mw": 159.5}, {"hour": 23, "mw": 151.2}, {"hour": 24, "mw": 145.0}
    ]
  },
  "safety_confirmation": "PENDING_OPERATOR_APPROVAL",
  "compliance_check": "NERC_BAL_005_PASSED"
}
```
*Please confirm operator authorization to transmit this generation schedule to the RTO scheduling portal.*
