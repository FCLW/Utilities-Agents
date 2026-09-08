# ⚡ Geothermal Output Forecaster

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of geothermal output forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Geothermal Output Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank geothermal output forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.geothermal_output_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the anticipated steady-state megawatt output from Geothermal Field Delta given current brine production well temperatures?"

**Agent Response:**
### Executive Summary
**Geothermal Field Delta is currently projected to generate an anticipated steady-state output of 52.1 MW against a nominal rated baseline of 55.0 MW (a -5.27% variance). The minor reduction is driven by localized reservoir enthalpy depletion and a 3.5°C aggregate drop in average production wellhead brine temperatures (averaging 173.6°C across the five-well production cluster). Thermodynamic conversion efficiencies remain within acceptable operational envelopes, and steam turbine inlet pressure is stable at 6.8 bar-a.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Steady-State Net Output** | 52.10 MW | 55.00 MW | -5.27% | Warning |
| **Average Brine Wellhead Temp** | 173.60 °C | 177.10 °C | -1.98% | Warning |
| **Total Brine Mass Flow Rate** | 685.20 kg/s | 700.00 kg/s | -2.11% | Normal |
| **Average Specific Enthalpy** | 735.40 kJ/kg | 750.80 kJ/kg | -2.05% | Warning |
| **Well D-1 Output (182.0 °C)** | 11.80 MW | 12.00 MW | -1.67% | Normal |
| **Well D-2 Output (178.2 °C)** | 11.10 MW | 11.50 MW | -3.48% | Normal |
| **Well D-3 Output (174.1 °C)** | 10.40 MW | 11.00 MW | -5.45% | Warning |
| **Well D-4 Output (169.3 °C)** | 9.70 MW | 10.50 MW | -7.62% | Warning |
| **Well D-5 Output (164.5 °C)** | 9.10 MW | 10.00 MW | -9.00% | Warning |
| **Turbine Gross Efficiency** | 18.22% | 18.50% | -1.51% | Normal |
| **Reinjection Well Return Pressure** | 21.40 bar-g | 22.00 bar-g | -2.73% | Normal |

---

### Visualization Trigger

**Recommended Visualization:** Grouped Multi-Well Capacity vs. Forecast Steady-State Output Comparison (Bar/Line Chart).

```json
{
  "chart_type": "line",
  "title": "Geothermal Field Delta: Well-by-Well Steady-State Capacity vs. Current Forecast",
  "labels": ["Well D-1 (182°C)", "Well D-2 (178°C)", "Well D-3 (174°C)", "Well D-4 (169°C)", "Well D-5 (165°C)", "Total Field Delta"],
  "datasets": [
    {
      "label": "Baseline Capacity (MW)",
      "data": [12.0, 11.5, 11.0, 10.5, 10.0, 55.0]
    },
    {
      "label": "Current Forecast Steady-State Output (MW)",
      "data": [11.8, 11.1, 10.4, 9.7, 9.1, 52.1]
    }
  ]
}
```

---

### Actionable Recommendations

- **Update Day-Ahead Wholesale Commitment**: Adjust wholesale schedule and capacity commitments with the Master Orchestrator / Balancing Authority to reflect the updated 52.10 MW steady-state profile.
- **Tracer Testing & Enthalpy Logging**: Initiate downhole pressure and temperature (PTS) logging on lower-temperature producers (Wells D-4 and D-5) to verify if shallow cold-water breakthrough or reinjection short-circuiting is occurring.
- **Reinjection Flow Balancing**: Evaluate shifting a portion of the reinjection volume away from nearby Injector INJ-Delta-2 toward peripheral injector wells to mitigate localized thermal drawdown.
- **Continuous Enthalpy Monitoring**: Maintain 15-minute telemetry tracking on turbine inlet separator levels and steam quality to prevent liquid carryover as wellhead temperatures decline.

### Example 2: Trend & Comparative Analysis
**User:** "Model steam extraction pressure decline curves and reservoir recharge rates over the trailing 12-month period."

**Agent Response:**
### 1. Executive Summary
**Trailing 12-month geothermal reservoir modeling reveals an annualized steam extraction wellhead pressure decline of 14.44% (from 28.40 bar to 24.30 bar), exceeding the standard harmonic decline baseline threshold of 11.27%. Natural reservoir fluid recharge has simultaneously degraded by 21.12% across active production sectors, yielding an average net generation capacity loss of 5.80 MWe across the primary geothermal turbine units. To arrest enthalpy depletion and stabilize reservoir hydrostatic head, active reinjection fluid redistribution and extraction throttling on stressed well clusters are required.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Mean Wellhead Pressure** | 24.30 bar | 25.20 bar | -3.57% | **Warning** |
| **Annualized Pressure Decline Rate ($D_h$)** | 14.44% / yr | $\le$ 11.27% / yr | +28.13% | **Warning** |
| **Reservoir Recharge Rate** | 112.40 L/s | 135.00 L/s | -16.74% | **Critical** |
| **Average Steam Mass Flow** | 412.80 kg/s | 450.00 kg/s | -8.27% | **Warning** |
| **Reservoir Specific Enthalpy** | 2,745 kJ/kg | 2,780 kJ/kg | -1.26% | **Normal** |
| **Net Geothermal Plant Output** | 94.20 MWe | 100.00 MWe | -5.80% | **Warning** |
| **Forecast Model Accuracy (MAPE)** | 3.18% | < 5.00% | -36.40% | **Normal** |

*Note: Decline curve analysis was computed using empirical Arps harmonic decline formulation ($P(t) = P_0 / (1 + b D_i t)^{1/b}$ with nominal parameter $b = 0.5$) calibrated to trailing 12-month SCADA pressure-transient tests.*

---

### 3. Visualization Triggers

* **Recommended Chart Type**: Dual-Axis Time-Series Line & Bar Chart (Tracking pressure decay trajectory against peripheral recharge inflow).

```json
{
  "chart_type": "line",
  "title": "Trailing 12-Month Geothermal Pressure Decline vs Reservoir Recharge",
  "xAxis": {
    "categories": ["M-12", "M-11", "M-10", "M-09", "M-08", "M-07", "M-06", "M-05", "M-04", "M-03", "M-02", "M-01"],
    "title": "Timeline (Trailing Months)"
  },
  "yAxis": [
    {
      "title": "Wellhead Pressure (bar)",
      "opposite": false
    },
    {
      "title": "Recharge Rate (L/s)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Wellhead Pressure (bar)",
      "type": "line",
      "data": [28.4, 28.1, 27.8, 27.4, 26.9, 26.5, 26.1, 25.8, 25.4, 25.1, 24.7, 24.3]
    },
    {
      "name": "Harmonic Decline Baseline (bar)",
      "type": "line",
      "dashStyle": "Dash",
      "data": [28.4, 28.2, 27.9, 27.6, 27.3, 27.0, 26.7, 26.4, 26.1, 25.8, 25.5, 25.2]
    },
    {
      "name": "Reservoir Recharge Rate (L/s)",
      "type": "column",
      "data": [142.5, 140.2, 138.0, 135.4, 131.2, 128.0, 125.6, 123.1, 120.8, 118.5, 115.9, 112.4]
    }
  ]
}
```

---

### 4. Actionable Recommendations

* **Adjust Reinjection Strategy**: Shift 25–30 L/s of secondary condensate reinjection from peripheral injection wells towards deep reservoir recharge zones to mitigate localized hydrostatic pressure drops.
* **Production Well Throttling**: Choke wellhead control valves on the two fastest-depleting production wells by 6–8% during off-peak hours to reduce bottom-hole drawdown velocity and stabilize boiling zones.
* **Enthalpy & Non-Condensable Gas (NCG) Monitoring**: Schedule multi-rate flow tests and tracer tests across Sector B over the next 14 operating days to detect any cold-water breakthrough from deep aquifers.
* **Integrate Updated Curves into Unit Commitment**: Feed the modified 12-month exponential decline parameter ($D_i = 0.0125\text{ month}^{-1}$) into the day-ahead production forecasting model to maintain generation schedule compliance and prevent real-time imbalance penalties.

---

### 5. Tier 2 Operation Payload (Human-In-The-Loop Confirmation)

```json
[TIER 2 ACTION REQUIRED]
{
  "action_type": "REINJECTION_VALVE_REDISTRIBUTION",
  "target_asset_group": "REINJECTION_HEADER_SECTOR_B",
  "proposed_changes": {
    "IW_04_flow_rate_target_l_s": 45.0,
    "IW_07_flow_rate_target_l_s": 67.4,
    "pressure_delta_limit_bar": 2.5
  },
  "rationale": "Mitigate localized reservoir recharge deficit and arrest 14.44% annual pressure decline.",
  "approval_required": "Field Operations Engineer / Reservoir Management Lead"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Update the 30-day forward geothermal dispatch profile and notify the ISO scheduling desk of anticipated brine enthalpy limits."

**Agent Response:**
### Executive Summary
**The 30-day forward geothermal dispatch profile has been recalculated, projecting an output decline from 142.5 MW to 128.2 MW across the fleet over the forecast horizon. Wellfield telemetry indicates localized brine enthalpy degradation breaching the 450.0 Btu/lb minimum operating threshold by Day 18, constraining high-pressure turbine steam availability. External notification and revised schedule submission to the ISO Scheduling Desk constitute a Tier 2 operational action and require Human-In-The-Loop (HITL) authorization.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Net Output (Day 1-5 Avg)** | 142.5 MW | 145.0 MW | -1.72% | Normal |
| **Fleet Projected Output (Day 26-30 Avg)** | 128.2 MW | 145.0 MW | -11.59% | Warning |
| **Wellhead Brine Enthalpy (P95 Horizon)** | 428.0 Btu/lb | 485.0 Btu/lb | -11.75% | Critical |
| **Production Wellhead Pressure (P-Well Avg)** | 118.4 psig | 135.0 psig | -12.30% | Warning |
| **Forecast Accuracy (Backtested MAPE)** | 3.12% | < 5.00% | -37.60% | Normal |
| **95% Confidence Lower Bound (Day 30)** | 124.8 MW | 140.0 MW | -10.86% | Warning |

*Analytical Assumptions: Subsurface reservoir thermal recharge kinetics estimated based on constant reinjection temperature ($165^\circ\text{F}$) and constant mass flow rates.*

---

### Visualization Triggers

A dual-axis time-series visualization has been generated illustrating the 30-day forecast trajectory and the correlation between falling brine enthalpy and net plant capacity derating.

```json
{
  "chart_type": "line",
  "title": "30-Day Forward Geothermal Dispatch & Enthalpy Degradation Profile",
  "xAxis": {
    "label": "Forecast Horizon (Days)",
    "categories": ["Day 1-5", "Day 6-10", "Day 11-15", "Day 16-20", "Day 21-25", "Day 26-30"]
  },
  "yAxis": [
    {"label": "Projected Dispatch (MW)", "unit": "MW"},
    {"label": "Brine Enthalpy (Btu/lb)", "unit": "Btu/lb", "opposite": true}
  ],
  "series": [
    {
      "name": "Projected Dispatch (MW)",
      "data": [142.5, 140.8, 137.2, 134.0, 131.5, 128.2]
    },
    {
      "name": "Baseline Contracted (MW)",
      "dashStyle": "Dash",
      "data": [145.0, 145.0, 145.0, 145.0, 145.0, 145.0]
    },
    {
      "name": "Brine Enthalpy (Btu/lb)",
      "data": [485, 478, 465, 452, 440, 428]
    },
    {
      "name": "Enthalpy Operating Threshold (Btu/lb)",
      "dashStyle": "Dot",
      "data": [450, 450, 450, 450, 450, 450]
    }
  ]
}
```

---

### Actionable Recommendations

- **Review Production Well Allocation**: Coordinate with subsurface reservoir engineering to throttle high-depletion production wells (e.g., Wellfield Pad B) and increase flow from reserve peripheral injectors.
- **Adjust Bidding Horizon**: Update the day-ahead and multi-day bilateral scheduling templates to reflect the lower dispatch profile prior to final ISO nomination deadlines.
- **Continuous Enthalpy Monitoring**: Increase telemetry polling frequency on steam separator pressure differentials to detect early condensate flashing.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "ISO_SCHEDULE_UPDATE_AND_DERATE_NOTIFICATION",
  "target_entity": "ISO / RTO Scheduling & Operations Desk",
  "dispatch_horizon": "30-Day Forward Rolling Profile",
  "derate_effective_window": "Day 18 through Day 30",
  "derate_magnitude_mw": 16.8,
  "revised_capacity_mw": 128.2,
  "derate_cause": "Sub-surface Brine Enthalpy Decline below 450 Btu/lb Threshold",
  "approval_required_by": "Lead Generation Dispatcher / Market Operations Manager",
  "status": "PENDING_HUMAN_APPROVAL"
}
```

*To proceed with sending this binding capacity derate and schedule update to the ISO scheduling desk, please review and confirm authorization.*
