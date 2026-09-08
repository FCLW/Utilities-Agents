# ⚡ Hydro Inflow Snowpack Estimator

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of hydro inflow snowpack estimator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Hydro Inflow Snowpack Estimator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank hydro inflow snowpack estimator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.hydro_inflow_snowpack_estimator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How will current mountain snowpack water equivalent (SWE) levels translate into reservoir inflow volumes during spring runoff?"

**Agent Response:**
### Executive Summary
**Current basin-wide Snow Water Equivalent (SWE) levels are tracking at 118.4% of the historical median across primary high-elevation catchment zones, yielding a projected cumulative spring runoff volume of 1,245.8 Thousand Acre-Feet (kAF) into the reservoir system between April and July. Antecedent fall soil moisture saturation levels (84.2%) and below-average sublimation loss indicators suggest high runoff efficiency (~76.5%), shifting the projected peak inflow window forward to late May/early June. Generation dispatch and spillway management protocols must account for elevated crest inflow rates reaching 8,400 cfs under baseline temperature melt degree-day trajectories.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Basin-Wide Mean SWE** | 28.3 in | 23.9 in (30-Yr Median) | +18.4% | Normal |
| **High-Elevation SWE (>8,500 ft)** | 34.6 in | 28.1 in | +23.1% | Warning |
| **Antecedent Soil Moisture Saturation** | 84.2% | 71.0% | +18.6% | Normal |
| **Runoff Conversion Efficiency Index** | 76.5% | 68.0% | +12.5% | Normal |
| **Apr–Jul Forecasted Inflow Volume** | 1,245.8 kAF | 1,050.0 kAF | +18.6% | Warning |
| **Peak Inflow Rate (95% CI Midpoint)** | 8,400 cfs | 6,800 cfs | +23.5% | Warning |
| **Model Mean Absolute Percentage Error (MAPE)** | 3.8% | < 5.0% Target | -24.0% | Normal |

*Analytical Assumptions & Modeling Context:*
- Conversion modeling applies degree-day melt factors calibrated with SNOTEL telemetry and high-resolution spatial SWE interpolations.
- Net runoff volume accounts for a baseline evaporation/sublimation deduction of 11.2% and groundwater recharge retention of 12.3%.
- Confidence intervals are computed at the 95% level ($\pm 620\text{ cfs}$ peak window variability) assuming standard climatological temperature deviations ($\pm 1.5^\circ\text{C}$).

---

### Visualization Triggers
**Recommended Chart Type:** **Time-Series Multi-Line Chart** (Forecasted Hydrograph with 95% Confidence Intervals vs. 30-Year Historical Median).

```json
{
  "title": "Spring Runoff Inflow Forecast vs. Historical Median (April - July)",
  "xAxis": {
    "type": "category",
    "data": ["Apr 01", "Apr 15", "May 01", "May 15", "Jun 01", "Jun 15", "Jul 01", "Jul 15", "Jul 31"]
  },
  "yAxis": {
    "type": "value",
    "name": "Inflow Rate (cfs)"
  },
  "series": [
    {
      "name": "Forecasted Inflow (cfs)",
      "data": [1450, 2100, 3850, 6200, 8400, 7100, 4300, 2400, 1550]
    },
    {
      "name": "Historical Median Inflow (cfs)",
      "data": [1300, 1850, 3200, 4900, 6800, 5900, 3600, 2100, 1400]
    },
    {
      "name": "95% Upper Bound (cfs)",
      "data": [1600, 2350, 4300, 6900, 9300, 7900, 4800, 2700, 1750]
    },
    {
      "name": "95% Lower Bound (cfs)",
      "data": [1300, 1850, 3400, 5500, 7500, 6300, 3800, 2100, 1350]
    }
  ]
}
```

---

### Actionable Recommendations

- **Hydroelectric Generation Pre-Draft Planning:** Coordinate with Short-Term Generation Planning to ramp baseline hydro unit dispatch during late April to establish adequate reservoir flood control buffer headroom without triggering bypass spill events.
- **Continuous SNOTEL & Temperature Tracking:** Ingest daily isothermal melt layer tracking and freezing level elevation telemetry to detect early rain-on-snow event triggers that could accelerate peak inflows into mid-May.
- **Wholesale Market Integration:** Feed updated monthly volume schedules (+195.8 kAF above median) to Production Cost Modeling and Trading Desks to optimize scheduled maintenance outages and baseload thermal dispatch profiles.
- **Spillway & Dam Safety Coordination:** Maintain notification readiness with Dam Safety engineering for reservoir surface elevation targets approaching the seasonal rule curve upper margin between May 20 and June 10.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze satellite snow cover extent and degree-day snowmelt models to predict peak reservoir spill dates for Dam Beta."

**Agent Response:**
### 1. Executive Summary
**Satellite Snow Cover Extent (SCE) across the Dam Beta catchment has depleted to 62.4% following accelerated degree-day thermal accumulation, driving forecasted peak tributary inflows to 42,100 cfs between June 3 and June 7.** **Reservoir pool elevation is projected to reach maximum conservation capacity (98.6%) on June 5, initiating mandatory uncontrolled spillway engagement unless pre-spill discharge modulation is executed.** **Hydroelectric production scheduling must align turbine baseload dispatch to maximum capacity (18,500 cfs) through late May to create flood control buffer.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Catchment Snow Cover Extent (SCE)** | 62.4% | 74.0% (Historical Median) | -15.68% | Warning |
| **Snow Water Equivalent (SWE)** | 482 mm | 440 mm (Seasonal Norm) | +9.55% | Warning |
| **Degree-Day Melt Index ($\mathbf{T_{mean} > 0^\circ C}$)** | 8.4 °C-days/day | 5.2 °C-days/day | +61.54% | Critical |
| **Forecasted Peak Inflow Rate** | 42,100 cfs | 28,500 cfs (Mean Runoff) | +47.72% | Critical |
| **Reservoir Storage Capacity** | 87.8% | 78.0% (Target Rule Curve) | +12.56% | Warning |
| **Projected Peak Spill Date Window** | June 03 – June 07 | June 18 (Historical Mean) | -13 Days | Critical |
| **Inflow Model MAPE (95% CI)** | 3.82% | < 5.00% (Threshold Target) | -23.60% | Normal |

---

### 3. Visualization Triggers

A dual-axis time-series visualization has been generated to track the depletion of satellite snowpack extent alongside degree-day inflow dynamics and reservoir headroom.

```json
{
  "chart_type": "line",
  "title": "Dam Beta Hydro Inflow & Reservoir Spill Trajectory Forecast",
  "xAxis": {
    "type": "category",
    "data": ["May 01", "May 08", "May 15", "May 22", "May 29", "Jun 05", "Jun 12", "Jun 19", "Jun 26", "Jul 03"]
  },
  "yAxis": [
    {
      "type": "value",
      "name": "Flow Rate (cfs)",
      "position": "left"
    },
    {
      "type": "value",
      "name": "Storage / SCA (%)",
      "position": "right",
      "max": 100
    }
  ],
  "series": [
    {
      "name": "Degree-Day Snowmelt Inflow (cfs)",
      "type": "line",
      "yAxisIndex": 0,
      "data": [14200, 18500, 24600, 31200, 38500, 42100, 39400, 31800, 22100, 15400]
    },
    {
      "name": "Reservoir Storage Capacity (%)",
      "type": "line",
      "yAxisIndex": 1,
      "data": [72.4, 76.1, 81.5, 87.8, 94.2, 98.6, 99.4, 96.2, 91.5, 85.0]
    },
    {
      "name": "Satellite Snow Cover Extent (%)",
      "type": "line",
      "yAxisIndex": 1,
      "data": [86.5, 81.2, 73.8, 62.4, 48.1, 32.7, 19.5, 11.2, 5.8, 2.1]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Ramping Generation Schedule**: Coordinate with the Energy Settlement and Dispatch desk to schedule all units at Dam Beta to full generation capacity (18,500 cfs hydraulic throughput) starting May 22 to optimize water value and draft pool elevation.
- **Continuous Satellite & SNOTEL Assimilation**: Ingest daily MODIS/VIIRS fractional snow cover products and elevation-banded SNOTEL telemetry into the temperature-index melt model to refine peak timing error bounds.
- **Downstream Flood Coordination**: Notify downstream water authorities and USACE partners regarding projected spill crest window (June 03–June 07, peak volume ~42,100 cfs).

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "RESERVOIR_CONTROLLED_PRE_SPILL_RELEASE",
  "asset_id": "DAM_BETA",
  "zone_id": "HYDRO_CASCADE_ZONE_4",
  "parameters": {
    "target_pool_elevation_ft": 1242.0,
    "current_pool_elevation_ft": 1261.5,
    "recommended_spillway_gate_opening": "Gate_1_and_Gate_2_at_15_pct",
    "discharge_increase_cfs": 6500,
    "effective_start_time": "2025-05-25T06:00:00Z",
    "duration_hours": 96
  },
  "justification": "Mitigate uncontrolled spill risk during projected peak inflow surge (42,100 cfs) between June 3 and June 7 by establishing 85,000 acre-feet of flood control surcharge capacity.",
  "regulatory_framework": "FERC Project License & USACE Water Control Manual Rule Curve",
  "requires_hitl_approval": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Adjust monthly hydropower generation capacity dispatch curves to preserve mandated fish flow conservation storage."

**Agent Response:**
### Executive Summary
**Snowpack Water Equivalent (SWE) projections and seasonal inflow runoff hydrographs have been integrated to recalibrate monthly hydropower generation dispatch curves, enforcing strict compliance with regulatory environmental and fish flow conservation minimums. Baseload generation limits have been derated across Q3/Q4 summer peak drawdown intervals by an average of 14.2% to guarantee minimum downstream flow rates (1,250–2,100 cfs) and preserve active reservoir pool elevation above the critical 1,420 ft MSL threshold. Dispatch capacity envelopes now operate within a 95% confidence interval under updated IEEE/FERC biological opinion constraints without violating reservoir rule curves.**

---

### Quantitative Performance & Inflow Storage Analysis

The table below details current hydrological storage metrics, run-off projections, and revised monthly generation parameters compared against unconstrained targets:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Seasonal SWE Accumulation** | 28.4 in | 31.0 in (Historical Median) | -8.39% | Warning |
| **Projected Spring/Summer Runoff Inflow** | 2,120 TAF | 2,350 TAF | -9.79% | Warning |
| **Conservation Storage Reserve** | 845 TAF | 720 TAF (Mandated Minimum) | +17.36% | Normal |
| **Peak Summer Dispatch Capability** | 630 MW | 710 MW (Unconstrained) | -11.27% | Warning |
| **Minimum Environmental Fish Flow** | 1,850 cfs | 1,850 cfs (FERC Floor) | 0.00% | Normal |
| **Hydro Inflow Forecast MAPE** | 3.82% | < 5.00% | -23.60% | Normal |
| **Tailrace Dissolved Oxygen Compliance** | 7.6 mg/L | ≥ 6.5 mg/L | +16.92% | Normal |

---

### Inflow & Generation Capacity Trajectory

```json
{
  "chart_type": "line",
  "title": "Monthly Hydropower Generation vs. Conservation Flow & Inflow Forecast",
  "data": {
    "categories": ["Oct", "Nov", "Dec", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"],
    "series": [
      {
        "name": "Unconstrained Dispatch (MW)",
        "data": [450, 480, 520, 560, 510, 490, 620, 750, 710, 580, 440, 400]
      },
      {
        "name": "Adjusted Dispatch Curve (MW)",
        "data": [380, 410, 450, 480, 460, 470, 580, 690, 630, 490, 350, 320]
      },
      {
        "name": "Mandated Minimum Fish Flow Eqv (MW)",
        "data": [180, 180, 190, 200, 210, 220, 250, 310, 310, 260, 210, 190]
      },
      {
        "name": "SWE Runoff Inflow Forecast (TAF)",
        "data": [110, 95, 85, 90, 120, 185, 340, 520, 460, 210, 130, 105]
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Update Market Bidding & Unit Commitment**: Adjust Day-Ahead and Month-Ahead forward capacity nominations to reflect the reduced peak capacity ceiling (maximum 690 MW in May and 630 MW in June) to avoid non-compliance penalties.
- **Implement Spillway / Bypass Gate Coordination**: Coordinate low-head bypass turbine configurations during low-flow periods (July–September) to maintain mandated tailwater temperature and dissolved oxygen standards.
- **Dynamic SWE Telemetry Re-evaluation**: Ingest SNOTEL and airborne LiDAR snow depth datasets bi-weekly through May to refine runoff hydrographs and adjust dispatch headroom dynamically.
- **Coordinate with Thermal & Renewables Fleet**: Submit revised hydro dispatch limits to the Master Production Planning Orchestrator to schedule replacement CCGT and solar-plus-storage ramping during the derated late-summer window.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "DISPATCH_CURVE_OVERRIDE_COMMITMENT",
  "target_asset_group": "HYDRO_GENERATION_CASCADE_ZONE_4",
  "authorized_officer": "Generation Production Superintendent / Lead Hydro Dispatcher",
  "parameters": {
    "effective_start_date": "2025-04-01T00:00:00Z",
    "effective_end_date": "2025-09-30T23:59:59Z",
    "minimum_downstream_bypass_cfs": 1850,
    "max_monthly_energy_derate_mwh": -58400,
    "regulatory_mandate_id": "FERC-ENVR-FLOW-SEC-7"
  },
  "risk_assessment": "Reallocation of 58.4 GWh to conservation storage prevents violation of statutory fish flow mandates; necessitates market purchase or alternate thermal dispatch substitution during summer on-peak hours.",
  "approval_status": "PENDING_OPERATOR_SIGN_OFF"
}
```
