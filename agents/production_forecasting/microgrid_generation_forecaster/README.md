# ⚡ Microgrid Generation Forecaster

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of microgrid generation forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Microgrid Generation Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank microgrid generation forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.microgrid_generation_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can the Island Community microgrid maintain standalone power balance tomorrow using its local solar, wind, and battery assets?"

**Agent Response:**
### Executive Summary
**The Island Community microgrid is projected to maintain standalone power balance over tomorrow's 24-hour horizon utilizing its coordinated solar PV, wind turbine, and Battery Energy Storage System (BESS) assets.** **Total forecasted renewable generation (58.4 MWh) and available BESS capacity (15.0 MWh) are sufficient to satisfy the projected aggregate demand (104.2 MWh) when coupled with mid-day BESS charging cycles and evening discharge support.** **A constrained operating margin is identified during the evening peak (18:00–21:00 UTC), where BESS State of Charge (SoC) draws down to 18%, remaining above the critical reserve limit (15%) under the 95% confidence interval.**

---

### Data Presentation

The table below summarizes the 24-hour microgrid generation, demand, and storage forecast evaluated against standard operational baselines:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Microgrid Demand** | 5.90 MW (Hour 18) | 6.20 MW (Nameplate Limit) | -4.8% | **Normal** |
| **Total Daily Energy Demand** | 104.2 MWh | 102.0 MWh (Historical Avg) | +2.2% | **Normal** |
| **Solar PV Total Output** | 40.8 MWh | 39.5 MWh (P50 Baseline) | +3.3% | **Normal** |
| **Wind Generation Output** | 46.2 MWh | 44.0 MWh (P50 Baseline) | +5.0% | **Normal** |
| **Peak Renewable Generation** | 6.20 MW (Hour 12) | 5.80 MW (Coincident Load) | +6.9% | **Normal** |
| **BESS Minimum State of Charge (SoC)** | 18.0% (Hour 22) | 20.0% (Operational Target) | -10.0% | **Warning** |
| **Forecast Model Accuracy (MAPE)** | 3.42% | < 5.00% (Target Threshold) | -31.6% | **Normal** |
| **Loss of Load Expectation (LOLE)** | 0.00 Hours | 0.00 Hours | 0.0% | **Normal** |

---

### Visualization Trigger: 24-Hour Microgrid Power Balance & Storage Trajectory

*Recommended Chart Type*: **Time-Series Line / Area Chart** depicting hourly load profile, solar PV output, wind generation, net BESS dispatch, and battery State of Charge (SoC).

```json
{
  "chart_type": "line",
  "title": "Island Community Microgrid 24-Hour Power Balance Forecast",
  "xaxis": {
    "title": "Hour of Day (UTC)",
    "categories": ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"]
  },
  "yaxis": {
    "title": "Power (MW) / SoC (%)"
  },
  "series": [
    {
      "name": "Load Demand (MW)",
      "data": [3.2, 2.9, 2.8, 3.4, 4.8, 5.5, 5.8, 5.6, 5.1, 5.9, 5.2, 4.0]
    },
    {
      "name": "Solar PV (MW)",
      "data": [0.0, 0.0, 0.0, 0.2, 2.4, 4.6, 5.2, 4.8, 2.8, 0.4, 0.0, 0.0]
    },
    {
      "name": "Wind Generation (MW)",
      "data": [2.1, 2.4, 2.6, 2.3, 1.8, 1.2, 1.0, 1.4, 1.9, 2.5, 2.8, 2.5]
    },
    {
      "name": "BESS Net Dispatch (MW)",
      "data": [1.1, 0.5, 0.2, 0.9, 0.6, -0.3, -0.4, -0.6, 0.4, 3.0, 2.4, 1.5]
    },
    {
      "name": "BESS State of Charge (%)",
      "data": [65, 62, 60, 56, 52, 55, 59, 65, 62, 38, 22, 18]
    }
  ]
}
```

---

### Key Analytical Findings & Technical Assumptions
1. **Mid-Day Solar Surpluses**: Between 10:00 and 14:00 UTC, solar and wind generation exceed aggregate local demand by an average of 0.4–0.6 MW, enabling the BESS to absorb up to 2.8 MWh and recharge to 65% SoC ahead of the evening peak.
2. **Evening Peak Margin**: The microgrid net peak occurs at 18:00 UTC (5.9 MW demand vs. 2.9 MW combined wind/solar generation), requiring a sustained 3.0 MW BESS discharge rate. 
3. **95% Confidence Interval Assessment**: Lower-bound P95 wind generation scenarios indicate that if wind output drops below 1.5 MW during the 18:00–21:00 window, BESS SoC could breach the 15% reserve floor.

---

### Actionable Recommendations
- **Maintain Automated Microgrid Energy Management System (EMS) Scheduling**: Retain planned BESS absorption setpoints during the 10:00–14:00 solar crest to guarantee minimum 65% pre-peak SoC.
- **Arm Non-Critical Demand Response (DR)**: Pre-stage 0.5 MW of interruptible commercial loads between 18:00 and 21:00 UTC as an operating contingency in the event wind generation underperforms P50 forecast by >15%.
- **Continuous Feeder Telemetry Monitoring**: Monitor feeder-level power quality and frequency regulation thresholds (IEEE 1547 / IEEE 2030.7 compliance) across Island Substation Bus A.

---

### [TIER 2 ACTION REQUIRED]
*Note: Any manual modification to the microgrid islanding switchgear state or battery inverter operational modes requires operator confirmation.*

```json
{
  "action_type": "MICROGRID_ISLANDING_SCHEDULE_CONFIRMATION",
  "target_asset": "Island_Community_Substation_BESS_Controller_01",
  "parameters": {
    "operating_mode": "ISLANDED_AUTONOMOUS",
    "bess_reserve_floor_pct": 15.0,
    "demand_response_standby_mw": 0.5,
    "effective_start_utc": "2025-01-01T00:00:00Z",
    "effective_end_utc": "2025-01-01T23:59:59Z"
  },
  "safety_checks_passed": true,
  "human_in_the_loop_approval_required": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Forecast 24-hour microgrid generation versus critical hospital and water treatment load under islanded conditions."

**Agent Response:**
### Executive Summary
**The 24-hour islanded microgrid generation forecast demonstrates 100% continuous coverage of combined critical hospital (2.30–3.80 MW) and water treatment facility (1.18–2.30 MW) loads, maintaining an average N-1 reserve margin of +2.18 MW.** **Total microgrid generation capacity peaks at 10.50 MW during peak solar irradiation (11:00) against a maximum combined critical load peak of 6.10 MW, yielding a maximum surplus generation capacity of +4.40 MW for battery storage replenishment.** **All operating parameters comply with IEEE 1547.4 islanding reliability guidelines, maintaining a forecast Mean Absolute Percentage Error (MAPE) of 3.24% and an active spinning reserve buffer exceeding 25% across all intervals.**

---

### Data Presentation: Key Forecast & Operational Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Critical Load (Hospital + Water)** | 6.10 MW | 6.50 MW (Max Rating) | -6.15% | Normal |
| **Minimum Microgrid Firm Generation** | 5.20 MW (Baseload + BESS) | 4.80 MW (Min Islanded Target) | +8.33% | Normal |
| **Peak Total Generation Capacity** | 10.50 MW | 9.80 MW (Expected) | +7.14% | Normal |
| **Minimum Hourly Operating Reserve Margin** | +1.48 MW (Hour 00:00) | $\ge$ 1.00 MW (N-1 Requirement) | +48.00% | Normal |
| **Forecast Model Accuracy (MAPE)** | 3.24% | < 5.00% (KPI Threshold) | -35.20% | Normal |
| **BESS State-of-Charge (SoC) End-of-Day** | 82.5% | $\ge$ 70.0% (Islanded Target) | +17.86% | Normal |
| **Frequency Regulation Headroom ($\pm 0.2\text{ Hz}$)** | $\pm 1.20\text{ MW}$ | $\pm 0.80\text{ MW}$ | +50.00% | Normal |

---

### 24-Hour Islanded Microgrid Generation & Load Dispatch Schedule

*All values in Megawatts (MW) unless otherwise noted.*

| Hour | Solar PV | Gas/CHP Gen | BESS Discharge / (Charge) | Total Gen Available | Hospital Load | Water Treatment | Total Critical Load | Net Reserve Margin |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **00:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.40 | 1.25 | 3.65 | **+1.55** |
| **01:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.35 | 1.20 | 3.55 | **+1.65** |
| **02:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.30 | 1.20 | 3.50 | **+1.70** |
| **03:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.30 | 1.18 | 3.48 | **+1.72** |
| **04:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.32 | 1.20 | 3.52 | **+1.68** |
| **05:00** | 0.30 | 4.50 | 0.70 | 5.50 | 2.45 | 1.30 | 3.75 | **+1.75** |
| **06:00** | 0.90 | 4.50 | 0.70 | 6.10 | 2.70 | 1.50 | 4.20 | **+1.90** |
| **07:00** | 2.20 | 4.50 | 0.70 | 7.40 | 3.10 | 1.75 | 4.85 | **+2.55** |
| **08:00** | 3.60 | 4.50 | 0.70 | 8.80 | 3.45 | 1.95 | 5.40 | **+3.40** |
| **09:00** | 4.50 | 4.50 | 0.70 | 9.70 | 3.65 | 2.10 | 5.75 | **+3.95** |
| **10:00** | 5.00 | 4.50 | 0.70 | 10.20 | 3.75 | 2.20 | 5.95 | **+4.25** |
| **11:00** | 5.30 | 4.50 | 0.70 | 10.50 | 3.80 | 2.30 | 6.10 | **+4.40** |
| **12:00** | 5.20 | 4.50 | 0.70 | 10.40 | 3.78 | 2.27 | 6.05 | **+4.35** |
| **13:00** | 4.70 | 4.50 | 0.70 | 9.90 | 3.70 | 2.20 | 5.90 | **+4.00** |
| **14:00** | 3.90 | 4.50 | 0.70 | 9.10 | 3.65 | 2.15 | 5.80 | **+3.30** |
| **15:00** | 2.80 | 4.50 | 0.70 | 8.00 | 3.55 | 2.10 | 5.65 | **+2.35** |
| **16:00** | 1.50 | 4.50 | 0.70 | 6.70 | 3.45 | 2.05 | 5.50 | **+1.20** |
| **17:00** | 0.60 | 4.50 | 0.70 | 5.80 | 3.35 | 2.00 | 5.35 | **+0.45** |
| **18:00** | 0.00 | 4.50 | 0.70 | 5.20 | 3.20 | 1.90 | 5.10 | **+0.10** |
| **19:00** | 0.00 | 4.50 | 0.70 | 5.20 | 3.05 | 1.75 | 4.80 | **+0.40** |
| **20:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.90 | 1.60 | 4.50 | **+0.70** |
| **21:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.75 | 1.45 | 4.20 | **+1.00** |
| **22:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.60 | 1.35 | 3.95 | **+1.25** |
| **23:00** | 0.00 | 4.50 | 0.70 | 5.20 | 2.45 | 1.30 | 3.75 | **+1.45** |

---

### Visualization Triggers

```json
{
  "chart_type": "line",
  "data": {
    "title": "24-Hour Islanded Microgrid Generation vs. Critical Load Profile",
    "xAxis": {
      "title": "Hour (T+00:00 to T+23:00)",
      "categories": ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"]
    },
    "yAxis": {
      "title": "Power (MW)"
    },
    "series": [
      {
        "name": "Total Generation Available (MW)",
        "data": [5.20, 5.20, 5.20, 5.20, 5.20, 5.50, 6.10, 7.40, 8.80, 9.70, 10.20, 10.50, 10.40, 9.90, 9.10, 8.00, 6.70, 5.80, 5.20, 5.20, 5.20, 5.20, 5.20, 5.20]
      },
      {
        "name": "Total Critical Load (MW)",
        "data": [3.65, 3.55, 3.50, 3.48, 3.52, 3.75, 4.20, 4.85, 5.40, 5.75, 5.95, 6.10, 6.05, 5.90, 5.80, 5.65, 5.50, 5.35, 5.10, 4.80, 4.50, 4.20, 3.95, 3.75]
      },
      {
        "name": "Hospital Critical Load (MW)",
        "data": [2.40, 2.35, 2.30, 2.30, 2.32, 2.45, 2.70, 3.10, 3.45, 3.65, 3.75, 3.80, 3.78, 3.70, 3.65, 3.55, 3.45, 3.35, 3.20, 3.05, 2.90, 2.75, 2.60, 2.45]
      },
      {
        "name": "Water Treatment Critical Load (MW)",
        "data": [1.25, 1.20, 1.20, 1.18, 1.20, 1.30, 1.50, 1.75, 1.95, 2.10, 2.20, 2.30, 2.27, 2.20, 2.15, 2.10, 2.05, 2.00, 1.90, 1.75, 1.60, 1.45, 1.35, 1.30]
      }
    ]
  }
}
```

---

### Actionable Recommendations

1. **Mid-Day Solar Excess Capture (10:00 – 14:00)**: Route surplus solar output ($\approx 3.30\text{--}4.40\text{ MW}$) into the secondary BESS charging circuit to elevate SoC above 85% prior to evening solar decay.
2. **Evening Tight Margin Mitigation (17:00 – 19:00)**: The net reserve margin narrows to +0.10 MW at 18:00. Recommend pre-pumping treated water storage between 11:00 and 14:00 to enable a 0.50 MW controllable load reduction at the water treatment plant during the 17:00–19:00 window.
3. **Firm Generation Continuity**: Maintain continuous fuel pressure telemetry and lubrication oil temp monitoring on the primary 4.50 MW reciprocating/CHP gas generator to preserve islanded grid inertia and primary voltage/frequency reference (isochronous mode).
4. **Emergency Reserve Dispatch Verification**: Keep the standby 1.50 MW backup diesel generator in hot-standby readiness should solar irradiance drop due to localized cloud cover.

---

### HITL / Tier 2 Operations

```json
[TIER 2 ACTION REQUIRED]
{
  "action_type": "MICROGRID_DISPATCH_SETPOINT_UPDATE",
  "target_asset_id": "BESS_CONTROLLER_01 & WATER_TREATMENT_PUMP_BANK_B",
  "operation": "SET_DYNAMIC_LOAD_SHIFT_AND_STORAGE_CHARGE_SCHEDULE",
  "parameters": {
    "bess_charge_window_utc": "10:00-14:00",
    "bess_charge_rate_mw": 2.50,
    "water_treatment_demand_shift_mw": -0.45,
    "shift_window_utc": "17:00-19:00",
    "operating_mode": "ISLANDED_EMERGENCY"
  },
  "rationale": "Execution of dynamic schedule shifting ensures minimum spinning reserve margin stays above 0.55 MW at 18:00 without requiring non-critical load shedding.",
  "approval_required": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Schedule microgrid battery pre-charging from surplus wind generation tonight to prepare for scheduled utility tie-line disconnection."

**Agent Response:**
### Executive Summary
**Microgrid generation forecasting indicates sustained surplus wind generation tonight between 22:00 and 05:00 UTC, peaking at 650 kW against an average critical load demand of 177 kW. The overnight surplus of 2,740 kWh provides ample clean headroom to safely pre-charge the 1.0 MWh Battery Energy Storage System (BESS) from 45% to 100% State of Charge (SoC) prior to the scheduled 06:00 UTC tie-line disconnection. Executing this physical charging dispatch sequence alters asset operating states and requires Tier 2 Human-In-The-Loop (HITL) approval.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Current BESS State of Charge (SoC)** | 45.0% (450 kWh) | 100.0% (1,000 kWh) | -55.0% | Warning |
| **Overnight Wind Generation Yield** | 4,160 kWh | 3,850 kWh | +8.05% | Normal |
| **Overnight Net Critical Load** | 1,420 kWh | 1,450 kWh | -2.07% | Normal |
| **Available Surplus Generation** | 2,740 kWh | 550 kWh (Req. for 100% SoC) | +398.18% | Normal |
| **Generation Forecast Error (MAPE)** | 3.8% | < 5.0% | -24.0% | Normal |
| **95% Confidence Interval Band** | ±4.2% | ±7.5% | -44.0% | Normal |

---

### Visualization Triggers
**Recommended Visualization:** Time-Series Multi-Variable Area/Line Chart  
*Description:* Hourly generation forecast, critical microgrid load profile, scheduled battery charging trajectory, and resultant battery SoC across the pre-islanding window (22:00 – 05:00 UTC).

```json
{
  "chart_type": "line",
  "title": "Overnight Microgrid Dispatch & Battery Pre-Charge Profile",
  "xAxis": "Time (UTC)",
  "yAxis": "Power (kW) / SoC (%)",
  "categories": ["22:00", "23:00", "00:00", "01:00", "02:00", "03:00", "04:00", "05:00"],
  "series": [
    {
      "name": "Wind Generation Forecast (kW)",
      "data": [420, 480, 550, 610, 650, 580, 490, 380]
    },
    {
      "name": "Critical Load Demand (kW)",
      "data": [180, 175, 170, 165, 160, 170, 190, 210]
    },
    {
      "name": "Surplus Wind Available (kW)",
      "data": [240, 305, 380, 445, 490, 410, 300, 170]
    },
    {
      "name": "BESS Pre-Charge Rate (kW)",
      "data": [200, 250, 300, 300, 300, 200, 50, 0]
    },
    {
      "name": "BESS State of Charge (%)",
      "data": [45, 52, 63, 76, 89, 97, 99, 100]
    }
  ]
}
```

---

### Actionable Recommendations
- **Approve Pre-Charging Dispatch**: Authorize the automated BESS inverter controller to ramp charging starting at 22:00 UTC, peaking at a 300 kW charge rate between 00:00 and 03:00 UTC.
- **Set Dynamic Reserve Margin**: Maintain a 50 kW spinning margin above local load to absorb sudden wind gust variations and avoid tie-line inadvertent export/import before the scheduled breaker opening.
- **Enable Islanding Transition Mode**: Transition the microgrid controller to grid-forming (GFM) voltage-source mode on the BESS inverter by 05:45 UTC, 15 minutes prior to tie-line breaker trip.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_action:
  action_type: "PHYSICAL_ASSET_DISPATCH_SCHEDULE"
  target_subsystem: "BESS_INVERTER_CONTROLLER"
  grid_zone_id: "ZONE_MG_04"
  scheduled_start_time: "2025-01-16T22:00:00Z"
  scheduled_end_time: "2025-01-17T05:00:00Z"
  operational_parameters:
    target_soc_percent: 100.0
    energy_to_charge_kwh: 550.0
    max_charge_rate_kw: 300.0
    primary_source: "LOCAL_WIND_SURPLUS"
    island_preparation_mode: "ENABLED"
    scheduled_islanding_time: "2025-01-17T06:00:00Z"
  safety_validation:
    thermal_runaway_interlocks: "VERIFIED_CLEAR"
    grid_voltage_regulation_limits: "COMPLIANT_IEEE_1547"
    forecast_confidence: "95_PCT_STABLE"
  required_approval: "HUMAN_OPERATOR_SIGN_OFF"
```
