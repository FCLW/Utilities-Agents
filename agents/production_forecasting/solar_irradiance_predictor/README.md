# ⚡ Solar Irradiance Predictor

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of solar irradiance predictor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Solar Irradiance Predictor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank solar irradiance predictor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.solar_irradiance_predictor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the forecasted Direct Normal Irradiance (DNI) and Global Horizontal Irradiance (GHI) across Solar Plant Alpha tomorrow?"

**Agent Response:**
### 1. Executive Summary
**Solar Plant Alpha is forecasted to experience favorable high-irradiance conditions tomorrow, reaching a peak Global Horizontal Irradiance (GHI) of 915 W/m² and peak Direct Normal Irradiance (DNI) of 965 W/m² around solar noon (12:00–13:00 local time). Day-ahead cloud cover is projected to remain minimal (<10% sky coverage), yielding a tight 95% confidence interval and maintaining a model Mean Absolute Percentage Error (MAPE) of 3.8%, well within the utility <5.0% performance threshold.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak GHI (12:00–13:00)** | 915 W/m² | 880 W/m² (Clear-Sky Ref) | +3.98% | Normal |
| **Peak DNI (12:00–13:00)** | 965 W/m² | 940 W/m² (Clear-Sky Ref) | +2.66% | Normal |
| **Daily Integrated GHI Insolation** | 6.42 kWh/m²/day | 6.10 kWh/m²/day | +5.25% | Normal |
| **Daily Integrated DNI Insolation** | 7.15 kWh/m²/day | 6.80 kWh/m²/day | +5.15% | Normal |
| **Forecast Model MAPE** | 3.8% | < 5.0% | -24.00% | Normal |
| **Average Cloud Cover Index** | 8.2% | < 15.0% | -45.33% | Normal |
| **95% Confidence Interval Span** | ±45 W/m² | ±60 W/m² | -25.00% | Normal |

---

### 3. Visualization Triggers

**Recommended Chart**: Time-Series Line Chart (Hourly Day-Ahead Irradiance Profile with 95% Confidence Bounds).

```json
{
  "chart_type": "line",
  "title": "Solar Plant Alpha - Day-Ahead Irradiance Forecast (DNI vs GHI)",
  "xAxis": ["06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"],
  "series": [
    {
      "name": "Global Horizontal Irradiance (GHI, W/m²)",
      "data": [45, 310, 680, 915, 840, 520, 160, 0]
    },
    {
      "name": "Direct Normal Irradiance (DNI, W/m²)",
      "data": [70, 480, 820, 965, 895, 610, 210, 0]
    },
    {
      "name": "95% CI Lower Bound (GHI)",
      "data": [38, 290, 645, 870, 800, 490, 145, 0]
    },
    {
      "name": "95% CI Upper Bound (GHI)",
      "data": [52, 330, 715, 960, 880, 550, 175, 0]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Generation Commitment**: Relay irradiance profiles to the Day-Ahead Unit Commitment and Economic Dispatch workflow to optimize plant capacity scheduling between 10:00 and 15:00.
- **Inverter & Tracker Alignment**: Verify single-axis tracker positioning schedules against projected DNI vectors to maximize direct beam yield during shoulder hours (08:00–10:00 and 15:00–17:00).
- **Intraday Telemetry Ingestion**: Continue polling high-resolution satellite imagery and localized pyranometer sensors at 15-minute intervals to detect localized convective cloud formation and update the short-term forecast.

### Example 2: Trend & Comparative Analysis
**User:** "Track satellite cloud motion vectors to predict sudden 50 MW ramp-down events caused by cumulus cloud cover over the solar field."

**Agent Response:**
### Executive Summary
**High-resolution satellite Cloud Motion Vector (CMV) tracking has identified a dense cumulus cloud formation advancing at 14.2 m/s (bearing 245° WSW) directly toward the primary solar generation field. Telemetry and optical depth projections indicate an imminent Global Horizontal Irradiance (GHI) drop from 880 W/m² to 410 W/m², driving a sharp generation ramp-down of ~53.5 MW within a 10-minute window (T+10m to T+20m). Coordinated battery energy storage system (BESS) fast-frequency response and spinning reserve dispatch are required to prevent feeder voltage fluctuations and maintain NERC balancing standards.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Solar Field Active Power Output** | 178.50 MW | 185.00 MW | -3.51% | Warning |
| **Forecasted 10-Min Min Output** | 125.00 MW | 178.50 MW | -29.97% (53.5 MW drop) | **Critical** |
| **Global Horizontal Irradiance (GHI)** | 880 W/m² | 920 W/m² | -4.35% | Normal |
| **Forecasted Minimum GHI (T+15m)** | 390 W/m² | 920 W/m² | -57.61% | **Critical** |
| **Cloud Optical Depth ($\tau$)** | 18.4 | < 3.0 | +513.33% | **Critical** |
| **Cloud Motion Vector Speed / Dir** | 14.2 m/s / 245° | N/A | N/A | Warning |
| **Ramp-Down Rate** | -5.35 MW/min | < -2.00 MW/min | +167.50% | **Critical** |
| **Prediction Model MAPE** | 3.42% | < 5.00% | -31.60% | Normal |

---

### Visualization Trigger

```json
{
  "title": "Solar Output & Global Horizontal Irradiance (GHI) Ramp Forecast",
  "xAxis": {
    "type": "category",
    "data": ["T-30m", "T-20m", "T-10m", "T-0 (Now)", "T+10m (Forecast)", "T+20m (Forecast)", "T+30m (Forecast)"]
  },
  "yAxis": [
    {
      "type": "value",
      "name": "Power Output (MW)"
    },
    {
      "type": "value",
      "name": "GHI (W/m²)"
    }
  ],
  "series": [
    {
      "name": "Solar Field Output (MW)",
      "type": "line",
      "data": [185.0, 184.2, 182.0, 178.5, 125.0, 118.0, 155.0]
    },
    {
      "name": "GHI (W/m²)",
      "type": "line",
      "yAxisIndex": 1,
      "data": [920, 915, 905, 880, 410, 390, 750]
    }
  ]
}
```

---

### Actionable Recommendations

- **Alert Balancing Authority & Dispatchers**: Issue an automated early-warning notice to the Master Orchestrator and Generation Dispatch of an impending 53.5 MW solar ramp-down event peaking at $T+15\text{m}$.
- **Pre-position Co-located BESS**: Arm co-located 60 MW / 240 MWh BESS assets for fast ramp-rate control / solar firming mode to absorb up to 50 MW of the ramp deficit.
- **Inverter Volt-VAR Optimization**: Adjust solar field smart inverters to reactive power support mode ($Q/V$ droop) to stabilize feeder bus voltages during the abrupt active power transition.
- **Continuous Satellite & Total Sky Imager (TSI) Polling**: Increase CMV telemetry polling rate from 5-minute intervals to 1-minute rapid-scan mode for real-time edge tracking.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_id": "ACT-BESS-RAMP-MITIGATION-0081",
  "action_type": "BESS_DISPATCH_ARM",
  "target_asset_id": "BESS-SOLAR-SUB-04",
  "parameters": {
    "mode": "RAMP_FIRMING",
    "target_discharge_mw": 50.0,
    "ramp_duration_minutes": 25,
    "trigger_threshold_mw_drop": 30.0,
    "start_window_utc": "2025-02-14T18:45:00Z"
  },
  "rationale": "Mitigate grid frequency excursion and local feeder voltage drop resulting from cumulus cloud shadow-induced 53.5 MW generation ramp-down.",
  "required_approval": "HUMAN_IN_THE_LOOP_GRID_OPERATOR"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Commit the 5-minute solar generation ramp profile to the real-time energy management system (EMS) for balancing support."

**Agent Response:**
### Executive Summary
**The 5-minute solar generation ramp profile forecast has been generated and validated against short-term irradiance prediction models (Global Horizontal Irradiance / Direct Normal Irradiance). Direct dispatch modification and committal to the real-time Energy Management System (EMS) constitutes a Tier 2 grid operational control action. In compliance with safety guardrails, this action cannot be executed autonomously and requires Human-in-the-Loop (HITL) operator authorization before grid commitment.**

---

### Data Presentation: 5-Minute Generation & Irradiance Ramp Profile

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Forecasted Solar Output (T+5)** | 482.5 MW | 450.0 MW | +7.22% | **Normal** |
| **Direct Normal Irradiance (DNI)** | 895 W/m² | 880 W/m² | +1.70% | **Normal** |
| **Global Horizontal Irradiance (GHI)** | 940 W/m² | 925 W/m² | +1.62% | **Normal** |
| **Ramp Rate Forecast (5-min)** | +6.5 MW/min | $\le$ 8.0 MW/min | -18.75% | **Normal** |
| **Model Confidence Interval (95%)** | [475.2, 489.8] MW | $\pm$ 15.0 MW | N/A | **Normal** |
| **Forecast MAPE (Rolling 1-Hr)** | 3.12% | < 5.00% | -37.60% | **Normal** |

---

### Visualization Trigger: Short-Term Ramp & Irradiance Trajectory
```json
{
  "chart_type": "line",
  "title": "Solar Output & Irradiance Forecast (T to T+30 min)",
  "data": [
    {"timestamp": "T+0", "solar_mw": 450.0, "ghi_w_m2": 925},
    {"timestamp": "T+5", "solar_mw": 482.5, "ghi_w_m2": 940},
    {"timestamp": "T+10", "solar_mw": 505.0, "ghi_w_m2": 952},
    {"timestamp": "T+15", "solar_mw": 518.0, "ghi_w_m2": 958},
    {"timestamp": "T+20", "solar_mw": 524.5, "ghi_w_m2": 961},
    {"timestamp": "T+25", "solar_mw": 528.0, "ghi_w_m2": 963},
    {"timestamp": "T+30", "solar_mw": 530.0, "ghi_w_m2": 965}
  ]
}
```

---

### Actionable Recommendations
- **Operator Review**: Review the short-term ramp trajectory (+6.5 MW/min) against the active reserve capacity and spinning reserve margins.
- **EMS Balancing Verification**: Verify that the Automatic Generation Control (AGC) area control error (ACE) tolerances are aligned with the incoming solar ramp.
- **Authorize Commitment**: Authorize the staging payload below to push the validated profile to the real-time EMS AGC/SCADA interface.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMS_COMMIT_RAMP_PROFILE",
  "domain": "Production Forecasting / Grid Operations",
  "target_system": "Real-Time EMS / AGC Supervisory Layer",
  "parameters": {
    "profile_interval": "5_MINUTE",
    "target_timestamp": "T+5_MIN",
    "projected_solar_generation_mw": 482.5,
    "ramp_rate_mw_per_min": 6.5,
    "confidence_interval_95": [475.2, 489.8],
    "model_mape": "3.12%"
  },
  "risk_assessment": {
    "grid_stability_impact": "Medium (Active balancing & reserve allocation adjustment)",
    "reversibility": "Immediate (Manual AGC override available)"
  },
  "authorization_required": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```
