# ⚡ Extreme Weather Anomaly Alert Bot

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of extreme weather anomaly alert bot is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Extreme Weather Anomaly Alert Bot Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank extreme weather anomaly alert bot events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.extreme_weather_anomaly_alert_bot_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Is there a polar vortex or atmospheric river event forecasted to impact power supply reliability over the next 7 days?"

**Agent Response:**
### Executive Summary
**A major Arctic Polar Vortex anomaly is forecasted to impact system operating zones between Day 3 and Day 5, driving ambient temperatures down to -22°C with severe wind chill effects. This extreme cold front will cause peak winter electrical heating demand to surge while simultaneously introducing thermal plant de-rate and gas supply freeze-off risks. System reserve margins are projected to fall significantly below the NERC reliability threshold of 15.0%, dipping to a critical minimum of 4.3% on Day 4.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Minimum Temperature (Arctic Front Peak)** | -22.0 °C | -4.5 °C (Seasonal Norm) | -388.9% | **Critical** |
| **Sustained Wind Speed / Gusts** | 58.0 km/h (Gusts: 85 km/h) | 22.0 km/h | +163.6% | **Warning** |
| **Forecasted Peak Coincident Demand** | 44,850 MW | 36,200 MW | +23.9% | **Critical** |
| **Available Generation Capacity (Thermal/Renewable)** | 46,780 MW | 51,500 MW (Nameplate Net) | -9.2% | **Warning** |
| **Projected Operating Reserve Margin (Day 4 Peak)** | 4.30% | 15.00% (Mandated Minimum) | -71.3% | **Critical** |
| **Natural Gas Delivery Curtailment Risk** | High (Pipeline Pressure Alerts) | Nominal | N/A | **Warning** |

---

### Visualization Triggers
**Recommended Visualization:** Multi-Axis Time-Series Line Chart correlating 7-day projected ambient temperatures against forecast grid operating reserve margins across all bulk transmission zones.

```json
{
  "chart_type": "line",
  "title": "7-Day Extreme Weather Impact on Power Supply Reliability",
  "xAxis": {
    "categories": ["Day 1 (+24h)", "Day 2 (+48h)", "Day 3 (+72h)", "Day 4 (+96h)", "Day 5 (+120h)", "Day 6 (+144h)", "Day 7 (+168h)"]
  },
  "yAxes": [
    {
      "title": "Temperature (°C)",
      "opposite": false
    },
    {
      "title": "Operating Reserve Margin (%)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Forecasted Min Temperature (°C)",
      "yAxis": 0,
      "data": [-4.0, -9.0, -18.0, -22.0, -19.0, -11.0, -3.0]
    },
    {
      "name": "Operating Reserve Margin (%)",
      "yAxis": 1,
      "data": [18.5, 14.2, 8.1, 4.3, 6.8, 12.5, 17.0]
    },
    {
      "name": "NERC Minimum Threshold (15%)",
      "yAxis": 1,
      "type": "dash",
      "data": [15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0]
    }
  ]
}
```

---

### Actionable Recommendations
- **Pre-warming & Freeze Protection**: Direct all thermal asset operators to execute freeze-protection procedures, verify heat trace circuit continuity, and ensure fuel-oil backup systems are fully prepped and tested.
- **Gas-Electric Coordination**: Coordinate immediately with pipeline operators to secure firm transportation nominations and verify gas pipeline pressure adequacy ahead of Day 3 morning ramp.
- **Demand Response Activation Readiness**: Place commercial and industrial (C&I) demand response aggregators on 24-hour advance notice for potential dispatch during Day 4 morning and evening peaks.
- **Outage Rescheduling**: Suspend all non-critical generator and transmission maintenance outages across the intertie corridors to maximize import capability.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_RESERVE_COMMITMENT_AND_EEA1_NOTIFICATION",
  "risk_level": "CRITICAL",
  "target_nodes": ["ALL_SYSTEM_ZONES"],
  "effective_window": "Day 3 00:00 UTC to Day 5 23:59 UTC",
  "proposed_actions": [
    "Commit 2,800 MW long-lead cold-start thermal generating units.",
    "Issue Energy Emergency Alert Level 1 (EEA1) pre-warning to Regional Reliability Coordinator.",
    "Issue Fuel Supply Alert to all dual-fuel generation resources."
  ],
  "requires_approval": true,
  "approver_role": "Shift Operations Manager / Chief Dispatcher"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Examine historical weather anomaly analogues and thermal generator freeze-off probabilities under -20°F temperatures."

**Agent Response:**
### Executive Summary
**Historical meteorological analogues (notably Winter Storms Uri and Elliott) indicate that sustained ambient temperatures of -20°F introduce non-linear, catastrophic freeze-off risks for thermal generation assets lacking complete thermal enclosures. Unenclosed natural gas combined-cycle (CCGT) and simple-cycle (SCGT) units exhibit freeze-off probabilities exceeding 62% to 74% due to instrument air desiccant saturation, impulse sensing line freezing, and mechanical valve seizing. Immediate deployment of enhanced winterization protocols, dual-fuel readiness verification, and cold-start pre-heating procedures is mandatory under NERC EOP-011-2 and EOP-012-1 standards.**

---

### Thermal Generator Freeze-Off & Anomaly Metrics (-20°F Analogue Analysis)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Unenclosed CCGT Freeze-Off Probability** | 74.2% | 8.5% | +772.9% | Critical |
| **Weatherized/Enclosed CCGT Failure Rate** | 18.5% | 4.2% | +340.5% | Warning |
| **Simple Cycle Gas Turbine (SCGT) Trip Probability** | 62.8% | 7.1% | +784.5% | Critical |
| **Supercritical Coal Intake & Handling Freeze Risk** | 38.4% | 5.8% | +562.1% | Warning |
| **Instrument Air System Dew Point Exceedance Risk** | 81.0% | 5.0% | +1520.0% | Critical |
| **Natural Gas Wellhead/Pipeline Supply Derate** | 42.5% | 3.0% | +1316.7% | Critical |
| **Minimum Ambient Design Temperature (MADT) Margin** | -12.0°F (Deficit) | 0.0°F Margin | -100.0% | Critical |

---

### Visualization Triggers

A bar chart comparing freeze-off failure probabilities across generation asset classes against historical baseline outage rates is rendered below:

```json
{
  "chart_type": "bar",
  "title": "Thermal Generator Freeze-Off Risk Probability at -20°F by Technology Subtype",
  "xAxis": {
    "categories": [
      "Combined Cycle (CCGT) - Unenclosed",
      "CCGT - Weatherized Enclosure",
      "Simple Cycle Gas Turbine (SCGT)",
      "Supercritical Coal",
      "Subcritical Coal",
      "Nuclear Steam Balance-of-Plant"
    ]
  },
  "yAxis": {
    "title": "Probability / Outage Rate (%)",
    "min": 0,
    "max": 100
  },
  "series": [
    {
      "name": "Freeze-Off Probability (-20°F)",
      "data": [74.2, 18.5, 62.8, 38.4, 46.1, 12.0]
    },
    {
      "name": "Baseline Cold Weather Outage Rate",
      "data": [8.5, 4.2, 7.1, 5.8, 6.4, 2.1]
    }
  ]
}
```

---

### Actionable Recommendations

- **Critical Sensing Line Heat Trace Verification**: Verify operational status and continuity of electric heat tracing (EHT) and thermal lagging across all turbine pressure transducers, drum level indicators, and water line sensing lines prior to temperature falling below 32°F.
- **Instrument Air System Purge & Desiccant Replacement**: Cycle desiccant air dryers to ensure pressure dew points remain at or below -40°F, preventing regulator freezing and turbine trip-to-safe-state failures.
- **Continuous Circulation & Warm-Standby Cycling**: Institute minimum fuel burn / warm-standby operational modes for critical peaking and intermediate units to prevent stagnant line freezing.
- **Fuel Switching & Secondary Reserve Staging**: Confirm on-site distillate oil inventory and operational readiness for dual-fuel units to hedge against anticipated upstream pipeline hydraulic freeze-offs and pressure curtailments.
- **Feedwater & Demineralized Water Line Recirculation**: Maintain continuous recirculation flows in external condensate lines, cooling tower freeze protection systems, and fire protection headers.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "tier_2_operation": "DISPATCH_EMERGENCY_COLD_WEATHER_DERATE_AND_PREHEAT_ORDER",
  "risk_level": "HIGH",
  "governing_standard": "NERC EOP-011-2 / EOP-012-1",
  "target_units": ["ALL_UNENCLOSED_CCGT_FLEET", "SCGT_PEAKING_FLEET"],
  "actions_requiring_human_approval": [
    "Commit off-line thermal units to minimum stable generation (Pmin) 12 hours ahead of -20°F temperature threshold",
    "Authorize secondary fuel oil blending/switching for gas turbines experiencing pipeline pressure drop warnings",
    "Issue operational derates to generation scheduler across non-weatherized balance-of-plant assets"
  ],
  "hitl_approval_status": "PENDING_OPERATOR_CONFIRMATION"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue an extreme weather emergency alert to power generation plant managers to activate winterization freeze protection protocols."

**Agent Response:**
### 1. Executive Summary
**A severe polar vortex cold front is forecasted to cross the operational balancing footprint within the next 3 to 6 hours, dropping ambient temperatures well below critical freezing thresholds (4°F min, -12°F wind chill). This extreme temperature anomaly presents immediate risks of instrument line freezing, cooling tower icing, and fuel supply derates across conventional and renewable generation units. Autonomous dispatch of mass emergency operational directives constitutes a Tier 2 action, requiring human operator authorization before transmitting formal compliance mandates to plant managers.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Forecasted Min Ambient Temp** | 4.0 °F | 32.0 °F (Freezing Datum) | -87.5% | **Critical** |
| **Peak Sustained Wind Chill** | -12.0 °F | 20.0 °F (Advisory Limit) | -160.0% | **Critical** |
| **Rate of Temperature Drop** | -4.8 °F/hr | -1.5 °F/hr (Standard Ramp) | +220.0% | **Critical** |
| **At-Risk Thermal Generation Fleet** | 14,250 MW | 0 MW | N/A | **Critical** |
| **Combustion Turbine Intake Icing Risk** | 88.4% Probability | < 10.0% Nominal | +784.0% | **Critical** |
| **Gas Pipeline Delivery Pressure Index**| 580 psig | 750 psig (Nominal Firm) | -22.7% | **Warning** |

---

### 3. Visualization Triggers
- **Recommended Visualization**: **Time-Series Line Chart** showing the 24-hour lookahead temperature drop and wind chill trajectory against the critical 32°F winterization threshold.

```json
{
  "chart_type": "line",
  "title": "Sub-Freezing Ambient Temperature & Wind Chill Trajectory",
  "xAxis": ["T-0h (Current)", "T+3h", "T+6h", "T+12h", "T+18h", "T+24h"],
  "series": [
    {
      "name": "Ambient Temperature (°F)",
      "data": [34, 28, 19, 11, 7, 4]
    },
    {
      "name": "Freeze Protection Threshold (°F)",
      "data": [32, 32, 32, 32, 32, 32]
    },
    {
      "name": "Wind Chill (°F)",
      "data": [29, 21, 8, -2, -8, -12]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Engage Heat Tracing & Enclosure Heating**: Verify and energize all critical instrument line heat tracing, transmitter enclosures, and boiler drum level sensing lines across all thermal assets.
- **Implement Fluid Circulation & Drainage Protocols**: Maintain continuous flow across dormant cooling loops and drain non-essential, out-of-service low-point piping to prevent structural freeze fractures.
- **Activate Dual-Fuel Switching Readiness**: Place secondary fuel oil storage heating, atomizing steam, and transfer pump skids on standby in anticipation of potential natural gas curtailments or low pipeline pressure.
- **Renewable Asset Winterization**: Set wind turbine blades to anti-icing/de-icing rotation modes and schedule high-frequency inverter enclosure heater checks for solar PV balance-of-plant systems.
- **Authorize Transmission of Mass Emergency Directive**: Approve the Tier 2 emergency dispatch payload below to trigger the plant management notification tree.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "MASS_OPERATIONAL_DIRECTIVE_DISPATCH",
  "priority": "EMERGENCY",
  "target_audience": "Generation Plant Managers & Lead Operations Engineers",
  "target_zones": ["ALL_GRID_ZONES", "NORTH_BALANCING_AREA", "CENTRAL_BASIN"],
  "protocol_id": "NERC-EOP-011-WINTERIZATION-LEVEL-3",
  "mandatory_actions": [
    "Activate full Winterization & Freeze Protection Checklist",
    "Inspect and log critical heat tracing and instrument enclosure statuses every 2 hours",
    "Confirm dual-fuel backup inventory and switchover readiness",
    "Report any weather-related capability derates (>10 MW) to Production Scheduling immediately"
  ],
  "hitl_approval_required": true,
  "requested_by": "extreme_weather_anomaly_alert_bot",
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```
