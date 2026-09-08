# ⚡ Battery Storage Discharge Optimizer

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of battery storage discharge optimizer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Battery Storage Discharge Optimizer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank battery storage discharge optimizer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.battery_storage_discharge_optimizer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the optimal state-of-charge schedule to maximize revenue for our 20 MW / 80 MWh battery during evening peak LMP spikes?"

**Agent Response:**
### Executive Summary
**To maximize wholesale arbitrage revenue for the 20 MW / 80 MWh Battery Energy Storage System (BESS), the asset must be fully charged to its operational ceiling of 95% State of Charge (SoC) during the midday solar trough (12:00–15:00) at an average LMP of $19.95/MWh.** **The optimal discharge sequence executes across the 4-hour evening super-peak window (17:00–21:00) when LMPs peak at $425.00/MWh, targeting a terminal floor of 10% SoC to preserve cell degradation limits while capturing a net daily spread of $17,980.00.** **This dynamic schedule delivers an estimated 38.4% revenue uplift over a standard baseload 4-hour discharge strategy by concentrating maximum continuous 20 MW discharge during the top two pricing intervals (18:00–20:00).**

---

### Key Operational Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Available Usable Energy** | 68.0 MWh | 68.0 MWh (10%–95% SoC) | 0.0% | **Normal** |
| **Round-Trip Efficiency (RTE)** | 86.5% | 85.0% | +1.76% | **Normal** |
| **Average Charging Cost** | $19.95 / MWh | $25.00 / MWh | -20.20% | **Normal** |
| **Weighted Peak Discharge LMP** | $302.21 / MWh | $215.00 / MWh | +40.56% | **Normal** |
| **Expected Net Arbitrage Revenue** | $17,980.00 / cycle | $12,990.00 / cycle | +38.41% | **Normal** |
| **Cell Degradation Index (DoD)** | 85.0% Max DoD | 85.0% Allowable DoD | 0.0% | **Normal** |
| **Inverter Thermal Reserve Margin** | 14.2% | > 10.0% Threshold | +42.00% | **Normal** |

---

### Optimized Hourly Dispatch & State-of-Charge Schedule

| Operating Hour (HE) | Target SoC (%) | Active Power (MW) | Mode | Forecasted LMP ($/MWh) | Gross Interval Cashflow ($) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **12:00 – 13:00** | 25.0% $\rightarrow$ 50.0% | -20.0 MW | Charging | $24.50 | -$490.00 |
| **13:00 – 14:00** | 50.0% $\rightarrow$ 75.0% | -20.0 MW | Charging | $18.20 | -$364.00 |
| **14:00 – 15:00** | 75.0% $\rightarrow$ 95.0% | -16.0 MW | Charging | $15.10 | -$241.60 |
| **15:00 – 16:00** | 95.0% | 0.0 MW | Standby / Floating | $22.00 | $0.00 |
| **16:00 – 17:00** | 95.0% | 0.0 MW | Standby / Spinning | $48.30 | $0.00 |
| **17:00 – 18:00** | 95.0% $\rightarrow$ 80.0% | +12.0 MW | Partial Discharge | $142.50 | +$1,710.00 |
| **18:00 – 19:00** | 80.0% $\rightarrow$ 55.0% | +20.0 MW | Full Discharge | $310.00 | +$6,200.00 |
| **19:00 – 20:00** | 55.0% $\rightarrow$ 30.0% | +20.0 MW | Full Discharge | $425.00 | +$8,500.00 |
| **20:00 – 21:00** | 30.0% $\rightarrow$ 10.0% | +16.0 MW | Partial Discharge | $280.00 | +$4,480.00 |
| **21:00 – 22:00** | 10.0% | 0.0 MW | Standby | $95.00 | $0.00 |

*Negative active power indicates energy imported (charging); positive indicates energy injected into the grid (discharging).*

---

### Visualization: SoC Trajectory vs. Evening LMP Spikes

```json
{
  "chart_type": "line",
  "title": "20 MW / 80 MWh BESS Optimal SoC & Dispatch Schedule vs LMP",
  "categories": ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
  "series": [
    {
      "name": "LMP ($/MWh)",
      "type": "line",
      "data": [24.50, 18.20, 15.10, 22.00, 48.30, 142.50, 310.00, 425.00, 280.00, 95.00, 42.00, 31.00]
    },
    {
      "name": "State of Charge (%)",
      "type": "line",
      "data": [25.0, 50.0, 75.0, 95.0, 95.0, 80.0, 55.0, 30.0, 10.0, 10.0, 10.0, 10.0]
    },
    {
      "name": "Discharge Power (MW)",
      "type": "column",
      "data": [-20.0, -20.0, -16.0, 0.0, 0.0, 12.0, 20.0, 20.0, 16.0, 0.0, 0.0, 0.0]
    }
  ]
}
```

---

### Actionable Recommendations
1. **Pre-Charge Staging**: Lock in Day-Ahead / Real-Time charging schedules between 12:00 and 15:00 to achieve 95% SoC (76 MWh total stored energy) before the evening ramp.
2. **Thermal Conditioning**: Enable auxiliary HVAC pre-cooling 30 minutes prior to the 18:00 full 20 MW discharge block to avoid high-temperature derating during peak ambient conditions.
3. **Co-Optimization Monitoring**: Monitor real-time contingency spinning reserve clearing prices; if spinning reserve margins exceed $450/MWh during HE 19:00, co-optimize the inverter capacity between 10 MW energy discharge and 10 MW ancillary reserves.
4. **Execution Safeguards**: Maintain the 10% minimum SoC reserve limit (8 MWh) to comply with warranty obligations and provide emergency response buffer.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_DISPATCH_SCHEDULE_SUBMISSION",
  "target_asset": "BESS-20MW-80MWH-01",
  "operating_horizon": "12:00 - 22:00",
  "parameters": {
    "charge_window": "12:00-15:00 @ up to -20 MW",
    "discharge_window": "17:00-21:00 @ up to +20 MW",
    "max_soc_limit_pct": 95.0,
    "min_soc_limit_pct": 10.0,
    "projected_net_revenue_usd": 17980.00
  },
  "safety_checks_passed": true,
  "requires_human_approval": true,
  "approval_role": "Lead Generation / Market Dispatch Operator"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Analyze battery degradation cost per equivalent full cycle under aggressive frequency regulation versus energy arbitrage."

**Agent Response:**
### Executive Summary
**Aggressive frequency regulation accelerates solid electrolyte interphase (SEI) growth and localized thermal cycling, elevating battery degradation cost to \$81.25/MWh-throughput (\$32.50/EFC per installed MWh) compared to \$48.50/MWh-throughput (\$19.40/EFC per installed MWh) under energy arbitrage.** **While frequency regulation yields higher gross market clearing revenues, high C-rate micro-cycling (1.0C–2.0C) reduces total asset cycle life from 5,200 to 3,100 Equivalent Full Cycles (EFC) before reaching 80% State of Health (SoH).** **Dynamic dispatch optimization requires co-optimizing regulation mileage multipliers against cell replacement capital expenditure amortization.**

---

### Data Presentation

The comparative assessment below models a utility-scale Grid Balancing Battery Energy Storage System (BESS) (Utility Baseline: Lithium Iron Phosphate / LFP, \$140/kWh cell replacement cost, 4-hour system) operating across both duty cycle regimes:

| Metric | Current Value (Frequency Regulation) | Baseline / Target (Energy Arbitrage) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Degradation Cost per EFC (\$/MWh-cap)** | \$32.50 | \$19.40 | +67.53% | **Warning** |
| **Degradation Cost per Throughput (\$/MWh)** | \$81.25 | \$48.50 | +67.53% | **Warning** |
| **Operational C-Rate (Peak Burst)** | 1.80 C | 0.50 C | +260.00% | **Critical** |
| **Average Operational Depth of Discharge (DoD)** | 22.0% | 85.0% | -74.12% | **Normal** |
| **Cell Life Expectancy (Total EFC to 80% SoH)** | 3,100 EFC | 5,200 EFC | -40.38% | **Critical** |
| **Thermal Dissipation Load (Avg Cell Temp Rise)**| +6.8 °C | +2.2 °C | +209.09% | **Warning** |
| **VEE Telemetry Reliability Index** | 99.85% | 99.90% | -0.05% | **Normal** |

---

### Visualization Triggers

- **Recommended Visualization**: **Grouped Bar Chart & Multi-Interval Degradation Trajectory Curve** comparing marginal cell aging kinetics, thermal degradation multipliers, and unit degradation costs across duty-cycle profiles.

```json
{
  "chart_type": "bar",
  "title": "BESS Degradation Cost and Operational Stress Comparison",
  "xAxis": {
    "categories": [
      "Depth of Discharge (Avg %)",
      "Peak Operating C-Rate",
      "Cycle Life Expectancy (EFC x100)",
      "Degradation Cost ($/MWh-throughput)",
      "Degradation Cost per EFC ($/EFC-MWh cap)"
    ]
  },
  "series": [
    {
      "name": "Energy Arbitrage (Base DoD 85%, 0.5C)",
      "data": [85.0, 0.5, 52.0, 48.50, 19.40]
    },
    {
      "name": "Aggressive Frequency Regulation (Reg-D/Fast Response)",
      "data": [22.0, 1.8, 31.0, 81.25, 32.50]
    }
  ]
}
```

---

### Actionable Recommendations

- **Implement Dynamic Degradation-Adder Bidding**: Update wholesale market dispatch models to inject a dynamic degradation floor price of **\$81.25/MWh** during fast frequency response intervals to prevent sub-marginal revenue capture.
- **Enforce State of Charge (SoC) Band Clamping**: Constrain the regulation resting target to **45%–55% SoC** to minimize high-voltage calendar aging combined with dynamic high-C thermal spikes.
- **Activate Thermal Management Pre-Cooling**: Pre-condition liquid-cooling chiller loops 10 minutes prior to scheduled high-mileage regulation blocks to restrict cell junction temperatures under 32°C.
- **Rebalance Revenue-Degradation Co-Optimization**: Transition up to 40% of peak-hour BESS capacity into stacked Energy Arbitrage + Spinning Reserve when frequency regulation clearing prices fall below \$35.00/MW-h.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "UPDATE_DISPATCH_COST_CURVE",
  "target_asset_id": "BESS_GRID_BALANCING_CLUSTER_01",
  "parameter": "marginal_degradation_adder_frequency_reg",
  "current_setpoint": "$52.00/MWh",
  "proposed_setpoint": "$81.25/MWh",
  "economic_impact": "Prevents estimated $1.2M annual premature cell replacement liability",
  "requires_hitl_approval": true,
  "approver_role": "Lead Grid Balancing & Market Dispatch Engineer"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Commit an automated 15 MW discharge dispatch order to CAISO real-time market for BESS Unit 1 starting at 17:30."

**Agent Response:**
### Executive Summary
**Autonomous market commitment and physical dispatch execution cannot be initiated without Human-in-the-Loop (HITL) authorization under NERC/FERC and Grid Balancing safety compliance. An optimized 15 MW discharge dispatch schedule for BESS Unit 1 starting at 17:30 PPT has been staged and evaluated against CAISO real-time market (RTM) parameters and battery state-of-charge limits. Operator review and manual confirmation are required before this Tier 2 physical and market action can be committed.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Requested Discharge Capacity** | 15.0 MW | 15.0 MW Max Continuous | 0.0% | Normal |
| **BESS Unit 1 Current State of Charge (SoC)** | 88.5% | 20.0% Min Operating Reserve | +68.5% | Normal |
| **Projected Duration at 15 MW** | 3.5 Hours | 2.0 Hours Market Block | +75.0% | Normal |
| **Projected CAISO Real-Time LMP** | $142.50 / MWh | $65.00 / MWh Day-Ahead | +119.2% | Normal |
| **Cell Core Temperature (Max)** | 28.4 °C | 35.0 °C Thermal Limit | -18.9% | Normal |

---

### Visualization Trigger

```json
{
  "chart_type": "line",
  "title": "BESS Unit 1 - Scheduled Discharge Profile & SoC Depletion",
  "data": [
    {"timestamp": "17:00", "soc_percent": 88.5, "dispatch_mw": 0.0, "rtm_lmp_usd_mwh": 85.20},
    {"timestamp": "17:30", "soc_percent": 88.5, "dispatch_mw": 15.0, "rtm_lmp_usd_mwh": 135.40},
    {"timestamp": "18:00", "soc_percent": 74.5, "dispatch_mw": 15.0, "rtm_lmp_usd_mwh": 148.10},
    {"timestamp": "18:30", "soc_percent": 60.5, "dispatch_mw": 15.0, "rtm_lmp_usd_mwh": 152.00},
    {"timestamp": "19:00", "soc_percent": 46.5, "dispatch_mw": 15.0, "rtm_lmp_usd_mwh": 142.50},
    {"timestamp": "19:30", "soc_percent": 32.5, "dispatch_mw": 15.0, "rtm_lmp_usd_mwh": 110.30},
    {"timestamp": "20:00", "soc_percent": 32.5, "dispatch_mw": 0.0, "rtm_lmp_usd_mwh": 78.00}
  ]
}
```

---

### Actionable Recommendations
- **Validate Inverter and Thermal Limits**: Verify that BESS Unit 1 HVAC and thermal management systems remain in nominal range prior to step-up transformer energization.
- **Confirm Market Clearing Gate Closure**: Ensure CAISO real-time market bid submission occurs prior to the T-75 minute gate closure window for the target operating interval.
- **Review Ramp-Rate Settings**: Ensure the 15 MW ramp trajectory conforms to CAISO telemetry protocol (standard ramp rate ≤ 5 MW/min unless frequency regulation is engaged).

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CAISO_RTM_DISPATCH_COMMITMENT",
  "resource_id": "BESS_UNIT_1",
  "grid_zone": "CAISO_SP15",
  "target_mw": 15.0,
  "start_time": "17:30 PPT",
  "duration_hours": 2.0,
  "estimated_gross_revenue_usd": 4275.00,
  "safety_interlock_status": "PASS",
  "confirmation_required": true,
  "instruction": "A certified grid balancing operator must approve this order to transmit the physical dispatch instruction to CAISO telemetry and the plant controller."
}
```
