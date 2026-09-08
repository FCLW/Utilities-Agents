# ⚡ Residential Load Curve Forecaster

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of residential load curve forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Residential Load Curve Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank residential load curve forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.residential_load_curve_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How will the forecasted 98°F heatwave impact suburban residential air conditioning load across the metropolitan service territory?"

**Agent Response:**
### Executive Summary
**The forecasted 98°F heatwave will drive an estimated +59.3% increase in suburban residential peak demand across the metropolitan territory, peaking at 3,250 MW between 17:00 and 18:00 (HE18). Residential air conditioning (HVAC) duty cycles will account for 76.3% (2,480 MW) of the total zone peak load due to sustained thermal inertia and residential occupancy patterns. System model variance indicates high forecast reliability with a Mean Absolute Percentage Error (MAPE) of 2.14% and a 95% Confidence Interval upper bound of 3,365 MW.**

---

### Data Presentation

The table below summarizes the projected impact on suburban residential load dynamics during the peak heatwave interval compared against seasonal normal baselines (82°F base design condition):

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Residential Load (HE18)** | 3,250 MW | 2,040 MW | +59.31% | **Warning** |
| **AC / Cooling Load Component** | 2,480 MW | 1,220 MW | +103.28% | **Critical** |
| **Thermal Sensitivity Gradient** | 78.4 MW / °F | 42.1 MW / °F | +86.22% | **Warning** |
| **Cooling Degree Days (CDD, base 65°F)** | 33.0 CDD | 17.0 CDD | +94.12% | **Warning** |
| **After-Diversity Maximum Demand (ADMD)** | 5.82 kW / premise | 3.65 kW / premise | +59.45% | **Warning** |
| **Forecast Accuracy (Backtested MAPE)** | 2.14% | < 5.00% | -57.20% | **Normal** |
| **95% Confidence Interval (Upper Bound)** | 3,365 MW | 2,120 MW | +58.73% | **Warning** |
| **Suburban Substation Transformer Loading (Avg)** | 88.6% MVA | 58.2% MVA | +52.23% | **Warning** |

*Note: Baseline reflects typical seasonal operating conditions at 82°F dry-bulb ambient temperature. Projections aggregate suburban residential feeders within Grid Zone Metro-Suburban (IEEE/NERC load classification).*

---

### Visualization Triggers

**Recommended Chart Type**: Multi-Series Time-Series Line Chart (24-Hour Diurnal Load Profile) comparing baseline demand, forecasted heatwave load, and explicit HVAC cooling components.

```json
{
  "chart_type": "line",
  "title": "Suburban Residential Load Curve: Baseline vs. 98°F Heatwave Scenario",
  "xAxis": "Hour of Day (HE)",
  "yAxis": "Load (MW)",
  "series": [
    {
      "name": "Forecasted Load (98°F Heatwave)",
      "data": [
        {"x": "HE01", "y": 820}, {"x": "HE02", "y": 760}, {"x": "HE03", "y": 720}, {"x": "HE04", "y": 700},
        {"x": "HE05", "y": 730}, {"x": "HE06", "y": 810}, {"x": "HE07", "y": 940}, {"x": "HE08", "y": 1120},
        {"x": "HE09", "y": 1350}, {"x": "HE10", "y": 1620}, {"x": "HE11", "y": 1910}, {"x": "HE12", "y": 2180},
        {"x": "HE13", "y": 2420}, {"x": "HE14", "y": 2650}, {"x": "HE15", "y": 2840}, {"x": "HE16", "y": 3020},
        {"x": "HE17", "y": 3180}, {"x": "HE18", "y": 3250}, {"x": "HE19", "y": 3190}, {"x": "HE20", "y": 2980},
        {"x": "HE21", "y": 2640}, {"x": "HE22", "y": 2150}, {"x": "HE23", "y": 1600}, {"x": "HE24", "y": 1150}
      ]
    },
    {
      "name": "AC Specific Load (HVAC Component)",
      "data": [
        {"x": "HE01", "y": 260}, {"x": "HE02", "y": 220}, {"x": "HE03", "y": 200}, {"x": "HE04", "y": 190},
        {"x": "HE05", "y": 210}, {"x": "HE06", "y": 270}, {"x": "HE07", "y": 380}, {"x": "HE08", "y": 540},
        {"x": "HE09", "y": 750}, {"x": "HE10", "y": 990}, {"x": "HE11", "y": 1260}, {"x": "HE12", "y": 1510},
        {"x": "HE13", "y": 1730}, {"x": "HE14", "y": 1940}, {"x": "HE15", "y": 2110}, {"x": "HE16", "y": 2280},
        {"x": "HE17", "y": 2420}, {"x": "HE18", "y": 2480}, {"x": "HE19", "y": 2410}, {"x": "HE20", "y": 2220},
        {"x": "HE21", "y": 1910}, {"x": "HE22", "y": 1460}, {"x": "HE23", "y": 980}, {"x": "HE24", "y": 590}
      ]
    },
    {
      "name": "Baseline Load (Seasonal Normal 82°F)",
      "data": [
        {"x": "HE01", "y": 680}, {"x": "HE02", "y": 640}, {"x": "HE03", "y": 610}, {"x": "HE04", "y": 600},
        {"x": "HE05", "y": 630}, {"x": "HE06", "y": 710}, {"x": "HE07", "y": 820}, {"x": "HE08", "y": 950},
        {"x": "HE09", "y": 1080}, {"x": "HE10", "y": 1210}, {"x": "HE11", "y": 1350}, {"x": "HE12", "y": 1490},
        {"x": "HE13", "y": 1600}, {"x": "HE14", "y": 1710}, {"x": "HE15", "y": 1800}, {"x": "HE16", "y": 1890},
        {"x": "HE17", "y": 1980}, {"x": "HE18", "y": 2040}, {"x": "HE19", "y": 2010}, {"x": "HE20", "y": 1920},
        {"x": "HE21", "y": 1780}, {"x": "HE22", "y": 1520}, {"x": "HE23", "y": 1210}, {"x": "HE24", "y": 920}
      ]
    }
  ]
}
```

---

### Actionable Recommendations

- **Demand Response (DR) Pre-Cooling Activation**: Notify the Demand Side Management (DSM) agent to schedule automated residential thermostat pre-cooling between 10:00 and 13:00 to shave the anticipated 16:00–19:00 peak by an estimated 180–220 MW.
- **Generation Commitment & Peaker Readiness**: Alert Unit Commitment and Dispatch coordinators to ensure quick-start peaker capacity and operating reserves are synchronized prior to HE14 (14:00).
- **Substation Thermal Monitoring**: Request field distribution operations to monitor suburban transformer top-oil temperatures on identified high-density circuits approaching >85% nameplate capacity.
- **Continuous Weather Telemetry Refinement**: Re-run the short-term neural net load model every 60 minutes with updated NOAA/HRRR high-resolution dry-bulb and dew-point inputs to monitor for heat island amplification.

### Example 2: Trend & Comparative Analysis
**User:** "Compare cooling degree-day regressions against actual residential smart meter interval data from last year's summer peak."

**Agent Response:**
### Executive Summary
**A comparative backtest of the baseline Cooling Degree-Day (CDD) linear regression against aggregated residential smart meter interval data (AMI 15-minute telemetry) during last year's summer peak reveals a systematic underestimation of peak demand by 7.08% (120 MW) during late-afternoon ramp hours (16:00–19:00). While daily energy volume (MWh) tracked within acceptable bounds (MAPE 3.82%), standard CDD regression failed to capture non-linear thermal inertia and solar PV generation drop-off, driving localized feeder stress. Incorporating lagged temperature harmonics and solar irradiance cross-terms into the residential curve model restores hourly forecast accuracy to within target thresholds (MAPE 1.68%).**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Demand Underestimation (17:00–18:00)** | 1,575 MW (Model) | 1,695 MW (AMI Actual) | -7.08% | **Critical** |
| **Full-Day Residential MAPE** | 5.84% (Linear CDD) | < 5.00% (Target) | +16.80% | **Warning** |
| **Non-Linear Ridge/Lagged MAPE** | 1.68% (Enhanced) | < 5.00% (Target) | -66.40% | **Normal** |
| **R² Goodness-of-Fit (Peak Day 24h)** | 0.912 | ≥ 0.960 | -5.00% | **Warning** |
| **Net Evening Ramp Error (17:00 to 19:00)** | +85 MW / hr error | < 25 MW / hr error | +240.0% | **Critical** |
| **Aggregate Energy Volume Variance (24h MWh)** | 24,850 MWh | 25,837 MWh | -3.82% | **Normal** |

---

### Visualization Triggers

**Recommended Chart Type:** Time-Series Line Chart with multi-series overlay (CDD Baseline vs. AMI Actuals vs. Enhanced Non-Linear Model).

```json
{
  "title": "Last Year Summer Peak: CDD Regression Forecast vs. Actual Smart Meter Load",
  "chart_type": "line",
  "xAxis": {
    "categories": [
      "12:00 AM", "02:00 AM", "04:00 AM", "06:00 AM", "08:00 AM", "10:00 AM",
      "12:00 PM", "02:00 PM", "04:00 PM", "05:00 PM", "06:00 PM", "07:00 PM",
      "08:00 PM", "10:00 PM"
    ],
    "title": "Interval Timestamp (Hour Ending)"
  },
  "yAxis": {
    "title": "Residential Load (MW)"
  },
  "series": [
    {
      "name": "Actual Smart Meter Aggregated Load (MW)",
      "data": [680, 620, 590, 610, 750, 910, 1120, 1340, 1580, 1660, 1695, 1640, 1520, 1180]
    },
    {
      "name": "CDD Linear Regression Model (MW)",
      "data": [710, 640, 610, 630, 730, 860, 1050, 1260, 1470, 1540, 1575, 1520, 1430, 1150]
    },
    {
      "name": "Temperature / CDD Sensitive Ridge Model (MW)",
      "data": [685, 622, 595, 612, 745, 905, 1110, 1335, 1572, 1652, 1690, 1635, 1515, 1175]
    }
  ]
}
```

---

### Key Analytical Findings
1. **Thermal Building Inertia Lag**: Pure single-variable CDD (Base $65^\circ\text{F}$) lacks dynamic heat accumulation tracking. Building envelope heat soak caused peak HVAC cycling to crest at 17:30–18:30 despite maximum ambient dry-bulb temperature occurring at 15:00.
2. **Behind-the-Meter (BTM) Solar Masking**: Mid-day residential load is suppressed by residential rooftop solar generation, steepening the apparent evening net load curve as solar irradiance drops off while cooling load remains high.
3. **Model Convergence**: Applying a multi-variate polynomial model with rolling CDD lag terms ($\text{CDD}_{t}$, $\text{CDD}_{t-1}$, $\text{CDD}_{t-2}$) and solar zenith angle interaction terms reduces the peak-hour error from 120 MW down to 5 MW.

---

### Actionable Recommendations
- **Update Operational Regression Baselines**: Replace unlagged linear CDD models with a 3-hour moving CDD heat index variable to account for residential thermal retention during extreme heat waves.
- **Decompose Net Metering**: Separate gross residential load from behind-the-meter solar estimates using representative feeder telemetry to prevent evening ramp under-forecasting.
- **Calibrate Demand Response Dispatch**: Update DR trigger thresholds based on the 16:30–19:30 interval risk zone rather than standard peak CDD hours (14:00–16:00).
- **Integrate Humidity / Heat Index**: Transition standard CDD regression to Cooling Degree Hours (CDH) computed against wet-bulb/heat index for upcoming summer forecast cycles.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Publish the 48-hour forward residential load profile to the power supply procurement and balancing desk."

**Agent Response:**
### Executive Summary
**The 48-hour forward residential load forecast has been generated using calibrated neural network and ensemble gradient-boosted models, incorporating high-resolution numerical weather prediction data and localized feeder telemetry. The projected aggregate residential peak is expected to reach 2,490 MW at T+43 (Day 2 evening peak, 19:00 local time) with an overall model Mean Absolute Percentage Error (MAPE) of 2.14%, well within the operational threshold of < 5.0%. Transmission-to-distribution interface constraints remain nominal across all grid operating zones, and the forecast profile is staged for human review prior to formal publication to the Power Supply Procurement and Balancing Desk.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **48-Hour Peak Demand (MW)** | 2,490.00 MW | 2,410.00 MW | +3.32% | Normal |
| **48-Hour Minimum Off-Peak (MW)** | 1,190.00 MW | 1,150.00 MW | +3.48% | Normal |
| **Model Forecast MAPE** | 2.14% | < 5.00% | -57.20% | Normal |
| **95% Confidence Band Spread (Peak)** | ±115.00 MW (±4.62%) | ±150.00 MW | -23.33% | Normal |
| **Aggregate 48-Hr Energy Volume** | 86,470.00 MWh | 84,200.00 MWh | +2.70% | Normal |
| **Ramping Max Rate (MW/hr)** | +270.00 MW/hr | +300.00 MW/hr | -10.00% | Normal |

---

### Visualization Triggers
- **Recommended Visualization**: Multi-Series Time-Series Line Chart with 95% Confidence Interval Bands and Historical Baseline Overlay.

```json
{
  "chart_type": "line",
  "title": "48-Hour Forward Residential Load Curve Forecast (MW)",
  "xAxis": {
    "label": "Forecast Horizon (Hours T+1 to T+48)",
    "interval_unit": "Hour"
  },
  "yAxis": {
    "label": "Residential Load (MW)"
  },
  "series": [
    {
      "name": "Base Forecast",
      "data": [1420, 1350, 1280, 1210, 1190, 1240, 1410, 1680, 1850, 1920, 1960, 1980, 1950, 1930, 1910, 1970, 2120, 2340, 2450, 2410, 2300, 2110, 1850, 1580, 1440, 1360, 1290, 1220, 1200, 1250, 1430, 1710, 1890, 1950, 1990, 2010, 1980, 1950, 1930, 1990, 2150, 2380, 2490, 2440, 2330, 2140, 1870, 1600]
    },
    {
      "name": "Upper 95% CI",
      "data": [1480, 1410, 1340, 1270, 1250, 1300, 1480, 1760, 1935, 2010, 2050, 2070, 2040, 2020, 2000, 2060, 2220, 2450, 2565, 2520, 2410, 2210, 1940, 1655, 1505, 1420, 1350, 1280, 1260, 1310, 1500, 1790, 1975, 2040, 2080, 2105, 2070, 2040, 2020, 2085, 2250, 2490, 2605, 2555, 2440, 2240, 1960, 1675]
    },
    {
      "name": "Lower 95% CI",
      "data": [1360, 1290, 1220, 1150, 1130, 1180, 1340, 1600, 1765, 1830, 1870, 1890, 1860, 1840, 1820, 1880, 2020, 2230, 2335, 2300, 2190, 2010, 1760, 1505, 1375, 1300, 1230, 1160, 1140, 1190, 1360, 1630, 1805, 1860, 1900, 1915, 1890, 1860, 1840, 1895, 2050, 2270, 2375, 2325, 2220, 2040, 1780, 1525]
    }
  ]
}
```

---

### Actionable Recommendations
- **Day-Ahead Balancing Adjustment**: Alert the Day-Ahead Market (DAM) desk to secure additional 80 MW of flexible peaking capacity between T+18 to T+20 and T+42 to T+44 to cover evening ramp dynamics.
- **Solar PV Offset Verification**: Cross-reference behind-the-meter (BTM) rooftop solar irradiance forecasts between 11:00 and 15:00 on Day 2 to capture duck-curve steepening before the evening net load ramp.
- **Execute Data Publication**: Authorize the release of the 48-hour forward profile dataset to the Power Supply Procurement & Balancing Desk operational message bus.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PUBLISH_FORWARD_LOAD_SCHEDULE",
  "target_system": "POWER_PROCUREMENT_BALANCING_DESK",
  "payload_metadata": {
    "forecast_horizon_hours": 48,
    "granularity": "60_min",
    "total_mwh": 86470.00,
    "peak_mw": 2490.00,
    "mape_confidence": "97.86%",
    "transmission_zones": ["ZONE_NORTH", "ZONE_CENTRAL", "ZONE_SOUTH"]
  },
  "compliance_check": {
    "nerc_bal_standards_verified": true,
    "ferc_data_protection_verified": true,
    "read_only_source_enforced": true
  },
  "authorization_required": "Human-In-The-Loop (HITL) Desk Lead Approval"
}
```
