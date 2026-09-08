# ⚡ Congestion Node Price Mapper

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of congestion node price mapper is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Congestion Node Price Mapper Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank congestion node price mapper events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.congestion_node_price_mapper_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which transmission interfaces and flowgates are currently driving Locational Marginal Price (LMP) congestion over $250/MWh?"

**Agent Response:**
### Executive Summary
**Real-time market dispatch telemetry indicates that four key transmission interfaces and flowgates are currently binding, driving Locational Marginal Price (LMP) congestion components well above the $250.00/MWh threshold. The primary driver is severe thermal loading across the West-Central 500kV Corridor (FG-7022), which has reached a shadow price of $412.00/MW and an LMP congestion adder of $384.50/MWh due to localized generation outages and high transfer import schedules. Immediate transmission loading relief (TLR) protocols and targeted security-constrained economic dispatch (SCED) adjustments are required to mitigate escalating settlement exposure and localized reliability risks.**

---

### Quantitative Congestion & LMP Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **FG-7022 (West-Central 500kV) Congestion Adder** | $384.50/MWh | $35.00/MWh | +998.6% | **Critical** |
| **INT-104 (Northern Intertie Path 66) Congestion Adder** | $312.80/MWh | $28.00/MWh | +1,017.1% | **Critical** |
| **FG-4419 (South-East Valley Cutplane) Congestion Adder** | $276.40/MWh | $45.00/MWh | +514.2% | **Critical** |
| **INT-308 (Crosstown 345kV Corridor) Congestion Adder** | $258.10/MWh | $20.00/MWh | +1,190.5% | **Critical** |
| **Total Realized Congestion Rent (Active Market Interval)** | $1,842,500/hr | $180,000/hr | +923.6% | **Critical** |
| **Average System Nodal VaR (95% Confidence, 1-hr)** | $4,120,000 | $650,000 | +533.8% | **Critical** |

---

### Visualization Trigger: Real-Time Flowgate Congestion Profiles

**Recommended Chart Type:** `Bar Chart / Heatmap`

```json
{
  "chart_type": "bar",
  "title": "Flowgates & Interfaces Driving LMP Congestion > $250/MWh",
  "xAxis": {
    "categories": [
      "FG-7022 (West-Central 500kV)",
      "INT-104 (Northern Intertie Path 66)",
      "FG-4419 (South-East Valley Cutplane)",
      "INT-308 (Crosstown 345kV Corridors)"
    ]
  },
  "yAxis": {
    "title": "Price ($/MWh or $/MW)"
  },
  "series": [
    {
      "name": "Congestion Component ($/MWh)",
      "data": [384.50, 312.80, 276.40, 258.10]
    },
    {
      "name": "Shadow Price ($/MW)",
      "data": [412.00, 335.50, 298.00, 275.20]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Initiate Out-of-Merit Security Constrained Dispatch (SCED):** Ramp fast-start peaker and battery energy storage system (BESS) resources downstream of FG-7022 and INT-104 to relieve line ratings and lower shadow prices.
2. **Evaluate Transmission Loading Relief (TLR Level 3a/3b):** Reallocate interchange transactions across adjacent non-congested intertie pathways to alleviate Path 66 constraint loading.
3. **Phase-Shifting Transformer (PST) Optimization:** Coordinate with regional balancing authorities to adjust tap settings on Crosstown 345kV phase angle regulators, shifting up to 140 MW away from INT-308.
4. **Demand Response Triggering:** Review non-critical industrial load curtailment programs in the South-East Valley zone to dampen peak LMP spikes.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_id": "ACT-TLR-7022-REDISPATCH",
  "action_type": "PHYSICAL_GRID_REDISPATCH_AND_TLR",
  "impact_level": "Tier 2",
  "target_interfaces": ["FG-7022", "INT-104"],
  "dispatch_adjustments": {
    "downstream_generation_increase_mw": 220.0,
    "upstream_generation_curtailment_mw": 215.0,
    "pst_angle_tap_adjustment_deg": -3.5
  },
  "estimated_congestion_reduction_mwh": "$145.00/MWh",
  "requires_hitl_approval": true,
  "human_operator_role": "Lead Balancing Authority & Transmission Operator (TOP)"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Map the historical shadow prices and shift factors on the North-South transmission tie line over the last 30 days."

**Agent Response:**
### Executive Summary
**Analysis of the North-South transmission tie line over the trailing 30-day window reveals periodic thermal constraint binding, resulting in a 30-day peak shadow price of $82.50/MWh during peak load intervals.** **The nodal Generation Shift Factor (GSF) on adjacent North injection buses increased from a baseline of 0.42 to an operational peak of 0.52, driving heightened Locational Marginal Price (LMP) congestion components across downstream pricing nodes.** **Current line loading has stabilized with an average shadow price of $24.60/MWh, maintaining a moderate alert posture requiring continuous redispatch monitoring.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Tie Line Shadow Price** | $24.60/MWh | $15.00/MWh | +64.0% | **Warning** |
| **Generation Shift Factor (GSF)** | 0.45 | 0.42 | +7.1% | **Normal** |
| **Peak 30-Day Shadow Price** | $82.50/MWh | $35.00/MWh | +135.7% | **Critical** |
| **Tie Line Flow / Rating Utilization** | 88.4% (1,326 MW / 1,500 MW) | 80.0% (1,200 MW) | +10.5% | **Warning** |
| **Cumulative 30-Day Congestion Rent** | $1,842,500 | $1,200,000 | +53.5% | **Warning** |
| **Binding Hours Count (30-Day)** | 78 hrs | 40 hrs | +95.0% | **Warning** |

---

### Visualization Trigger: Dual-Axis Time-Series Line Chart

A **Dual-Axis Time-Series Line Chart** is recommended to evaluate the co-movement between transmission constraint shadow prices and nodal shift factors.

```json
{
  "chart_type": "line",
  "title": "North-South Transmission Tie Line: 30-Day Shadow Price & Shift Factor Trend",
  "xAxis": {
    "label": "Time Interval (Trailing 30 Days)",
    "categories": ["Day -30", "Day -25", "Day -20", "Day -15", "Day -10", "Day -5", "Day 0 (Current)"]
  },
  "yAxis": [
    {
      "label": "Shadow Price ($/MWh)",
      "unit": "$/MWh",
      "position": "left"
    },
    {
      "label": "Generation Shift Factor (GSF)",
      "unit": "p.u.",
      "position": "right"
    }
  ],
  "series": [
    {
      "name": "Shadow Price ($/MWh)",
      "type": "line",
      "yAxisIndex": 0,
      "data": [12.40, 15.10, 48.75, 82.50, 34.20, 19.80, 24.60]
    },
    {
      "name": "Shift Factor (GSF)",
      "type": "line",
      "yAxisIndex": 1,
      "data": [0.42, 0.43, 0.48, 0.52, 0.46, 0.44, 0.45]
    }
  ]
}
```

---

### Actionable Recommendations

* **Security-Constrained Economic Dispatch (SCED) Adjustment**: Coordinate with the Real-Time Dispatch Desk to evaluate out-of-merit generation adjustments on the North bus to relieve persistent flow accumulation when shift factors exceed $0.45$.
* **Congestion Revenue Rights (CRR / FTR) Hedging**: Review financial transmission rights allocations and auction clearing prices along the North-to-South corridor to mitigate exposure to shadow price spikes above the $50.00/MWh threshold.
* **Topological Reconfiguration Assessment**: Evaluate dynamic line ratings (DLR) and busbar switching options with Transmission Operations to expand effective tie-line transfer capability during high thermal stress intervals.
* **Continuous Telemetry Tracking**: Maintain 5-minute interval telemetry on tie-line power flow ($MW$) and real-time LMP congestion components ($LMP_{cong} = - \sum \text{Shift Factor} \times \text{Shadow Price}$).

---

### [TIER 2 ACTION REQUIRED]
*Physical line switching, manual out-of-merit generator re-dispatch commands, or transmission topology changes require formal Human-In-The-Loop (HITL) authorization by the Reliability Coordinator / Transmission Grid Operator prior to implementation.*

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Re-optimize generator dispatch setpoints across unconstrained nodes to mitigate localized transmission congestion penalties."

**Agent Response:**
### Executive Summary
**Localized transmission interface overload along Flowgate-7 (Zone-North to Zone-Central) has driven Marginal Congestion Components (MCC) at Node-Alpha to an unsustainable peak of $142.50/MWh. By recalculating Generator Shift Factors (GSF) and re-optimizing dispatch targets across unconstrained resource nodes (Node-Gamma and Node-Delta), localized congestion penalties can be mitigated by 77.5%, yielding an estimated net operational savings of $41,200/hr. Execution of physical setpoint modifications constitutes a Tier 2 Grid Action requiring explicit operator sign-off prior to SCADA dispatch transmission.**

---

### Data Presentation

#### Key Balancing & Congestion Metrics
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Nodal LMP (Node-Alpha)** | $186.20/MWh | $45.00/MWh | +313.78% | **Critical** |
| **Max Flowgate-7 Loading** | 482.0 MVA | 450.0 MVA (N-1 Limit) | +7.11% | **Critical** |
| **Marginal Congestion Penalty** | $46,800/hr | $5,600/hr | +735.71% | **Critical** |
| **Redispatch Cost (Unconstrained Nodes)** | $0.00/hr | $5,600/hr | N/A | **Warning** |
| **Net Hourly VaR (95% Conf, 1-hr Horizon)** | $68,450 | $15,000 | +356.33% | **Critical** |
| **Projected Net P&L Savings** | +$41,200/hr | $0.00/hr | +100.00% | **Normal** |

#### Nodal Congestion & Generator Redispatch Mapping
| Node ID | Zone ID | Generator ID | Generation Shift Factor (GSF) | Current Setpoint (MW) | Proposed Setpoint (MW) | Pre-MCC ($/MWh) | Post-MCC ($/MWh) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Node-Alpha** | `GZ-NORTH-01` | `GEN-101` (CCGT) | +0.48 | 320.0 | 230.0 | +$142.50 | +$32.10 |
| **Node-Beta** | `GZ-NORTH-02` | `GEN-102` (CT) | +0.32 | 110.0 | 75.0 | +$48.20 | +$18.50 |
| **Node-Gamma** | `GZ-WEST-01` | `GEN-201` (Hydro) | -0.41 | 180.0 | 250.0 | -$12.40 | -$4.20 |
| **Node-Delta** | `GZ-SOUTH-01` | `GEN-301` (CCGT) | -0.38 | 240.0 | 295.0 | -$8.10 | -$2.50 |
| **Node-Epsilon** | `GZ-CENTRAL-01`| `REF-SLACK` | 0.00 | 500.0 | 500.0 | $0.00 | $0.00 |

*Assumptions: System losses modeled via linearized Marginal Loss Factors (MLF). Transmission thermal ratings constrained to NERC FAC-011-3 and TOP-001-4 operating limits under N-1 contingency evaluation.*

---

### Visualization Triggers
- **Recommended Chart**: Multi-Series Comparison Bar Chart (Marginal Congestion Component Shift across Monitored Busses).
- **Chart JSON**:
```json
{
  "chart_type": "bar",
  "title": "Marginal Congestion Component (MCC) Pre vs. Post Redispatch",
  "data": {
    "labels": [
      "Node-Alpha (Constrained)",
      "Node-Beta (Export Hub)",
      "Node-Gamma (Unconstrained)",
      "Node-Delta (Unconstrained)",
      "Node-Epsilon (Slack Node)"
    ],
    "datasets": [
      {
        "label": "Pre-Optimization MCC ($/MWh)",
        "data": [142.50, 48.20, -12.40, -8.10, 0.00],
        "backgroundColor": "rgba(239, 68, 68, 0.7)"
      },
      {
        "label": "Post-Optimization MCC ($/MWh)",
        "data": [32.10, 18.50, -4.20, -2.50, 0.00],
        "backgroundColor": "rgba(34, 197, 94, 0.7)"
      }
    ]
  },
  "options": {
    "scales": {
      "y": {
        "title": { "display": true, "text": "Marginal Congestion Component ($/MWh)" }
      }
    }
  }
}
```

---

### Actionable Recommendations
1. **Operator Validation**: Verify ramping limits on `GEN-201` (+70 MW at 15 MW/min) and `GEN-301` (+55 MW at 8 MW/min) to ensure dynamic stability during the redispatch trajectory.
2. **Execute Redispatch Sequence**: Issue staggered basepoint instructions to ramp down constrained high-GSF generation (`GEN-101`, `GEN-102`) concurrently with unconstrained ramp-up (`GEN-201`, `GEN-301`) to maintain active power-frequency balance ($\Delta f < 0.02\text{ Hz}$).
3. **Monitor Flowgate Shadow Price**: Track Flowgate-7 dual variable continuously in the EMS; confirm relief of line MVA below the 450 MVA continuous thermal threshold.
4. **Coordinate Settlement Adjustment**: Submit redispatch deviation flags to wholesale market accounting to capture the estimated $41,200/hr congestion reduction under FERC Order 888/890 compliance standards.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "GRID_DISPATCH_SETPOINT_OVERRIDE",
  "target_domain": "Grid Balancing / Generation Control",
  "risk_classification": "Tier 2 - Physical Generator Setpoint Modification",
  "authorization_standard": "NERC TOP-001-4 / IEEE 1547",
  "parameters": {
    "contingency_id": "FLWG-07-OVERLOAD",
    "dispatch_instructions": [
      {"asset_id": "GEN-101", "node_id": "Node-Alpha", "current_mw": 320.0, "target_mw": 230.0, "ramp_rate_mw_per_min": 10.0},
      {"asset_id": "GEN-102", "node_id": "Node-Beta", "current_mw": 110.0, "target_mw": 75.0, "ramp_rate_mw_per_min": 12.0},
      {"asset_id": "GEN-201", "node_id": "Node-Gamma", "current_mw": 180.0, "target_mw": 250.0, "ramp_rate_mw_per_min": 15.0},
      {"asset_id": "GEN-301", "node_id": "Node-Delta", "current_mw": 240.0, "target_mw": 295.0, "ramp_rate_mw_per_min": 8.0}
    ],
    "net_generation_delta_mw": 0.0,
    "financial_impact_est": "-$41,200/hr congestion penalty reduction",
    "requires_hitl_approval": true
  }
}
```
