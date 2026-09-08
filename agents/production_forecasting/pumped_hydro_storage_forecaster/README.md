# ⚡ Pumped Hydro Storage Forecaster

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of pumped hydro storage forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Pumped Hydro Storage Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank pumped hydro storage forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.pumped_hydro_storage_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the optimal pumping schedule for Pumped Storage Hydro Unit 1 to take advantage of low off-peak overnight power prices?"

**Agent Response:**
### 1. Executive Summary
**Pumped Storage Hydro Unit 1 is optimized for a 6-hour overnight pumping block between 23:00 and 05:00 to capitalize on average off-peak Locational Marginal Prices (LMP) of $18.50/MWh. Dispatching at the maximum rated pumping capacity of 250 MW will restore upper reservoir head levels to 96.5% prior to the morning and evening peak spreads. This strategy achieves an estimated round-trip energy arbitrage margin of $82.40/MWh against projected evening peak generation prices of $118.07/MWh.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Off-Peak LMP Window (Avg)** | $18.50 / MWh | $24.00 / MWh | -22.92% | Normal |
| **On-Peak Generation LMP (Avg)** | $118.07 / MWh | $95.00 / MWh | +24.28% | Normal |
| **Target Pumping Capacity** | 250.0 MW | 250.0 MW | 0.00% | Normal |
| **Pumping Duration Window** | 6.0 Hours (23:00–05:00) | 6.0 Hours | 0.00% | Normal |
| **Total Energy Stored** | 1,500.0 MWh | 1,500.0 MWh | 0.00% | Normal |
| **Round-Trip Efficiency (RTE)** | 74.2% | 75.0% | -1.07% | Normal |
| **Upper Reservoir Fill Target** | 96.5% | 95.0% | +1.58% | Normal |
| **Net Arbitrage Margin** | $82.40 / MWh | $60.00 / MWh | +37.33% | Normal |
| **Forecast Error (MAPE)** | 3.12% | < 5.00% | -37.60% | Normal |

---

### 3. Visualization Triggers

**Recommended Chart Type:** Dual-Axis Time-Series Line Chart (Hourly LMP Forecast vs. Scheduled Hydro Pumping / Generation Profile).

```json
{
  "chart_type": "line",
  "title": "Unit 1 Pumping & Generation Dispatch Schedule vs. Day-Ahead LMP",
  "data_json": {
    "labels": ["00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00", "08:00", "12:00", "16:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
    "datasets": [
      {
        "label": "LMP Power Price ($/MWh)",
        "data": [22.5, 18.2, 16.4, 15.8, 17.1, 21.0, 34.5, 58.2, 65.0, 72.4, 85.0, 115.6, 128.4, 110.2, 74.5, 42.0, 28.5],
        "borderColor": "#3b82f6",
        "yAxisID": "y-price",
        "fill": false
      },
      {
        "label": "Hydro Unit 1 MW (+ Gen / - Pump)",
        "data": [-250, -250, -250, -250, -250, 0, 0, 0, 0, 0, 0, 220, 220, 220, 0, 0, -250],
        "borderColor": "#10b981",
        "yAxisID": "y-power",
        "fill": true
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

- **Commit Pumping Schedule**: Lock in Day-Ahead market bids to purchase 1,500 MWh of charging power across the optimal 23:00–05:00 window.
- **Hydraulic Head Optimization**: Verify intake gate positions and lower reservoir net head constraints at 22:30 before starting the synchronous motor startup sequence.
- **Monitor Wind Infeed Spikes**: If overnight wind generation exceeds forecasted baseload, evaluate extending pumping through 06:00 should negative pricing or deep curtailment conditions manifest.
- **Generation Preparedness**: Stage the dual-mode turbine-generator transitions for full generation dispatch across the 18:00–21:00 net-load evening peak window.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "COMMIT_PHYSICAL_DISPATCH_SCHEDULE",
  "asset_id": "PSH-UNIT-1",
  "operating_mode": "PUMPING",
  "scheduled_start": "2024-10-24T23:00:00Z",
  "scheduled_end": "2024-10-25T05:00:00Z",
  "target_capacity_mw": -250.0,
  "total_energy_mwh": 1500.0,
  "estimated_charging_cost": 27750.00,
  "projected_generation_revenue": 116889.30,
  "projected_net_margin": 89139.30,
  "human_approval_required": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Model upper reservoir hydraulic head levels, pumping round-trip efficiency (78%), and generation discharge capacity."

**Agent Response:**
### 1. Executive Summary
**Hydrodynamic and dispatch modeling of the upper reservoir indicates that at a 78.0% cycle round-trip efficiency (RTE), the facility sustains a peak generation discharge capacity of 1,000.0 MW across a maximum continuous discharge duration of 7.80 hours at nominal head. Hydraulic head variation between maximum operating elevation (378.0 m) and minimum operating elevation (340.0 m) introduces an 11.1% head-dependent modulation in instantaneous discharge power output and penstock flow velocity. Optimal off-peak pumping schedules require 10,000.0 MWh of charging energy at an aggregate pumping demand of 1,282.0 MW to restore active storage capacity from 0% to 100% State of Charge (SoC).**

---

### 2. Engineering Formulation & Telemetry Data Presentation

#### Hydro-Mechanical Governing Formulations
1. **Hydraulic Generation Power Equation:**
   $$P_{\text{gen}} = \eta_{\text{turb}} \cdot \rho \cdot g \cdot Q_{\text{gen}} \cdot \left(H_{\text{gross}} - h_{f,\text{gen}}\right)$$
   *Where $\rho = 1000\text{ kg/m}^3$, $g = 9.81\text{ m/s}^2$, $\eta_{\text{turb}} = 89.14\%$, and penstock friction head loss $h_{f,\text{gen}} = k_f \cdot Q_{\text{gen}}^2 \approx 5.0\text{ m}$ at rated $Q_{\text{gen}} = 320.0\text{ m}^3/\text{s}$.*

2. **Hydraulic Pumping Power Equation:**
   $$P_{\text{pump}} = \frac{\rho \cdot g \cdot Q_{\text{pump}} \cdot \left(H_{\text{gross}} + h_{f,\text{pump}}\right)}{\eta_{\text{pump}}}$$
   *Where $\eta_{\text{pump}} = 87.50\%$, yielding an aggregate cycle RTE: $\eta_{\text{RTE}} = \eta_{\text{turb}} \cdot \eta_{\text{pump}} = 0.8914 \times 0.8750 = 78.00\%$.*

3. **Upper Reservoir Mass Balance:**
   $$\frac{dH_{\text{upper}}}{dt} = \frac{Q_{\text{pump}}(t) - Q_{\text{gen}}(t) + Q_{\text{inflow}}(t) - Q_{\text{spill}}(t) - Q_{\text{evap}}(t)}{A_{\text{reservoir}}(H)}$$

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Upper Reservoir Gross Head ($H_{\text{gross}}$)** | 358.50 m | 360.00 m | -0.42% | Normal |
| **Active Storage Usable Volume ($V_{\text{active}}$)** | 15.00 MCM | 15.00 MCM | 0.00% | Normal |
| **Pumping Round-Trip Efficiency ($\eta_{\text{RTE}}$)** | 78.00% | 78.50% | -0.64% | Normal |
| **Pumping Mode Electromechanical Efficiency ($\eta_{\text{pump}}$)** | 87.50% | 88.00% | -0.57% | Normal |
| **Generating Mode Efficiency ($\eta_{\text{turb}}$)** | 89.14% | 89.20% | -0.07% | Normal |
| **Max Generation Discharge Capacity ($P_{\text{gen,max}}$)** | 1,000.00 MW | 1,000.00 MW | 0.00% | Normal |
| **Max Pumping Consumption Load ($P_{\text{pump,max}}$)** | 1,282.05 MW | 1,273.88 MW | +0.64% | Normal |
| **Rated Generation Penstock Flow ($Q_{\text{gen}}$)** | 320.00 m³/s | 320.00 m³/s | 0.00% | Normal |
| **Rated Pumping Flow ($Q_{\text{pump}}$)** | 270.00 m³/s | 270.00 m³/s | 0.00% | Normal |
| **Available Generation Energy Equivalent** | 7,800.00 MWh | 7,850.00 MWh | -0.64% | Normal |
| **Required Pumping Recharge Energy** | 10,000.00 MWh | 10,000.00 MWh | 0.00% | Normal |
| **Penstock Head Loss Coefficient ($k_f$)** | $4.88 \times 10^{-5}\text{ s}^2/\text{m}^5$ | $4.85 \times 10^{-5}\text{ s}^2/\text{m}^5$ | +0.62% | Normal |

---

### 3. Visualization Recommendation & Data Trigger

**Recommended Visualization:** 24-Hour Dual-Axis Time-Series Line & Dispatch Curve depicting Upper Reservoir Head (m), Generation Discharge Capacity / Pumping Load (MW), and Storage State of Charge (SoC %).

```json
{
  "chart_type": "line",
  "title": "24-Hour Pumped Storage Dispatch, Hydraulic Head & Generation Profile",
  "x_axis": [
    "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", "06:00", "07:00",
    "08:00", "09:00", "10:00", "11:00", "12:00", "13:00", "14:00", "15:00",
    "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
  ],
  "series": [
    {
      "name": "Upper Reservoir Head (m)",
      "data": [
        352.0, 356.5, 361.0, 365.2, 369.8, 374.1, 377.5, 378.0, 
        378.0, 374.2, 369.5, 364.8, 360.1, 356.4, 352.0, 348.5, 
        345.2, 342.0, 340.5, 340.0, 340.0, 343.8, 348.0, 352.0
      ]
    },
    {
      "name": "Net Generation / Pumping (MW)",
      "data": [
        -1280.0, -1280.0, -1280.0, -1280.0, -1280.0, -1280.0, -640.0, 0.0,
        0.0, 520.0, 780.0, 950.0, 1000.0, 980.0, 940.0, 910.0,
        880.0, 850.0, 500.0, 0.0, 0.0, -1280.0, -1280.0, -1280.0
      ]
    },
    {
      "name": "State of Charge (%)",
      "data": [
        31.6, 43.4, 55.3, 66.3, 78.4, 89.7, 98.7, 100.0,
        100.0, 90.0, 77.6, 65.3, 52.9, 43.2, 31.6, 22.4,
        13.7, 5.3, 1.3, 0.0, 0.0, 10.0, 20.5, 31.6
      ]
    }
  ],
  "unit": "MW / m / %"
}
```

---

### 4. Actionable Recommendations

- **Head-Dependent Derating Adjustment**: Update the Energy Management System (EMS) dynamic unit commitment curves to account for the -150 MW (15.0%) generation derate when reservoir head approaches the lower limit ($H_{\text{gross}} = 340.0\text{ m}$).
- **Pumping Co-Optimization**: Lock off-peak pumping intervals between 22:00 and 06:00 to capitalize on low-cost renewable surplus, ensuring the full 10,000.0 MWh recharge window is met prior to morning peak ramp.
- **Vibration & Cavitation Boundary Enforcement**: Restrict prolonged turbine operation between 40% and 65% discharge gate openings during low-head regimes to prevent draft tube cavitation and mechanical fatigue.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_action_request:
  action_id: ACT-PHS-DISPATCH-2024-001
  operation_type: DISPATCH_SCHEDULE_MODIFICATION
  affected_asset: Pumped_Hydro_Storage_Plant_1
  target_grid_zone: GRID_ZONE_NORTH_01
  parameters:
    pumping_commitment_target_mw: 1282.00
    generation_capacity_cap_mw: 1000.00
    modeled_rte_factor: 0.7800
    min_head_limit_m: 340.00
    max_head_limit_m: 378.00
    dispatch_window: "2024-11-01T00:00:00Z to 2024-11-01T23:59:59Z"
  operator_confirmation_required: true
  compliance_reference: "NERC BAL-005-1 / Hydro Operating Directive Sec 4.2"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit day-ahead pumping and generation bid schedules for the 600 MW pumped storage plant to the regional market operator."

**Agent Response:**
### 1. Executive Summary
**The optimal Day-Ahead pumping and generation schedule for the 600 MW Pumped Storage Plant has been formulated based on forecasted locational marginal pricing (LMP), net load curves, and reservoir head constraints. Submitting binding market bids directly to the Regional Transmission Operator (RTO/ISO) is classified as a Tier 2 financial and grid-commitment operation requiring human verification. The proposed schedule maximizes energy arbitrage across off-peak pumping (01:00–05:00) and peak generation (17:00–21:00) while maintaining required minimum head and reserve margins.**

---

### 2. Operational Metrics & Schedule Summary

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Generation Capacity** | 600.0 MW | 600.0 MW | 0.0% | Normal |
| **Max Pumping Demand** | 550.0 MW | 550.0 MW | 0.0% | Normal |
| **Planned Pumping Volume (Off-Peak)** | 2,200 MWh (4.0 hrs @ 550 MW) | 2,200 MWh | 0.0% | Normal |
| **Planned Generation Volume (On-Peak)** | 1,760 MWh (3.5 hrs @ ~503 MW avg) | 1,760 MWh | 0.0% | Normal |
| **Round-Trip Efficiency (RTE)** | 80.0% | 78.5% | +1.9% | Normal |
| **Forecasted Net Arbitrage Spread** | $84.20 / MWh | $65.00 / MWh | +29.5% | Normal |
| **Day-Ahead Forecast MAPE** | 3.42% | < 5.00% | -31.6% | Normal |
| **Upper Reservoir Usable Head (Start)** | 92.4% | > 85.0% | +8.7% | Normal |

---

### 3. Visualization Trigger & Profile

**Recommended Chart Type:** Dual-Axis Time-Series Area/Line Chart (Scheduled MW Dispatch vs. Forecasted LMP $/MWh)

```json
{
  "chart_type": "line",
  "title": "Day-Ahead 24-Hour Pumped Hydro Schedule & Price Forecast",
  "xAxis": {
    "categories": [
      "00:00", "01:00", "02:00", "03:00", "04:00", "05:00", 
      "06:00", "07:00", "08:00", "09:00", "10:00", "11:00", 
      "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", 
      "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"
    ],
    "title": "Hour of Day"
  },
  "yAxis": [
    { "title": "Dispatch (MW)", "opposite": false },
    { "title": "Forecasted LMP ($/MWh)", "opposite": true }
  ],
  "series": [
    {
      "name": "Scheduled Dispatch (MW)",
      "type": "column",
      "data": [
        0, -550, -550, -550, -550, 0,
        0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 600,
        600, 400, 160, 0, 0, 0
      ]
    },
    {
      "name": "Forecasted LMP ($/MWh)",
      "type": "line",
      "yAxis": 1,
      "data": [
        28.5, 19.2, 17.5, 18.0, 21.4, 32.1,
        45.0, 58.2, 52.0, 48.6, 44.1, 42.0,
        38.5, 39.0, 43.2, 51.0, 68.4, 112.5,
        138.0, 124.2, 95.8, 62.1, 41.0, 31.5
      ]
    }
  ]
}
```

---

### 4. Actionable Recommendations
* **Review Arbitrage Spread:** Verify the off-peak charging window (01:00–05:00 at ~$19.03/MWh average) against peak discharge (17:00–20:30 at ~$118.60/MWh average).
* **Confirm Spinning Reserve Allocation:** Ensure 100 MW of head-room during partial-load discharge blocks is registered for synchronized spinning reserve participation where applicable.
* **Execute Tier 2 Authorization:** A human market operator must approve the payload below to authorize transmission to the market operator's programmatic bidding portal (e.g., API/E-Tag gateway).

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MARKET_BID_SUBMISSION",
  "facility_id": "PHS-600MW-PLANT-01",
  "asset_name": "600 MW Pumped Hydro Storage Facility",
  "target_market_operator": "REGIONAL_ISO_RTO",
  "market_horizon": "DAY_AHEAD",
  "trading_date": "2025-05-19",
  "financial_exposure_usd": 328400.00,
  "pumping_blocks": [
    {"hours": "01:00-05:00", "bid_type": "PRICE_TAKER_LOAD", "mw": 550.0, "total_mwh": 2200.0}
  ],
  "generation_blocks": [
    {"hours": "17:00-19:00", "bid_type": "ECONOMIC_GENERATION", "mw": 600.0, "min_price_floor_usd": 85.00},
    {"hours": "19:00-20:00", "bid_type": "ECONOMIC_GENERATION", "mw": 400.0, "min_price_floor_usd": 90.00},
    {"hours": "20:00-21:00", "bid_type": "ECONOMIC_GENERATION", "mw": 160.0, "min_price_floor_usd": 75.00}
  ],
  "requires_hitl_approval": true,
  "approval_status": "PENDING_OPERATOR_SIGN_OFF"
}
```
