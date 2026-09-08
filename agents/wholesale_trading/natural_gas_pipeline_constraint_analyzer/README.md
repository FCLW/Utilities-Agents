# ⚡ Natural Gas Pipeline Constraint Analyzer

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of natural gas pipeline constraint analyzer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Natural Gas Pipeline Constraint Analyzer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank natural gas pipeline constraint analyzer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.natural_gas_pipeline_constraint_analyzer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are there any Critical Notices or Operational Flow Orders (OFO) declared on major interstate natural gas pipelines feeding our plants?"

**Agent Response:**
### Executive Summary
**A critical Operational Flow Order (OFO) Type 6 (Under-Performance / Short Imbalance) has been issued on Transcontinental Gas Pipe Line (Transco) Zone 5/6 and Algonquin Gas Transmission due to severe cold weather-driven demand spikes and compressor station constraints. Additionally, Texas Eastern Transmission (TETCO) M3 has issued a Critical Notice restricting secondary firm and interruptible transportation (IT) services. All gas-fired generation units interconnected to these paths face strict non-compliance balancing penalties ($25.00/MMBtu + index) and must balance intraday burn within a tight ±3% tolerance band.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Transco Zone 5/6 OFO Imbalance Tolerance** | `±3.0%` | `±10.0%` (Nominal) | `-70.0%` | **Critical** |
| **Algonquin Gas Transmission Scheduled Load** | `98.4% Capacity` | `85.0% Baseline` | `+15.76%` | **Critical** |
| **TETCO M3 Available Capacity (Secondary/IT)** | `0.0 kDth/d (Cut to 0)`| `45.0 kDth/d Nominations`| `-100.0%` | **Critical** |
| **Dominion South Constraint Index** | `82.0% Capacity` | `85.0% Baseline` | `-3.53%` | **Normal** |
| **Columbia Gas (TCO) Operating Pressure** | `76.8% Max MOP` | `85.0% Baseline` | `-9.65%` | **Normal** |
| **Non-Compliance Imbalance Penalty Surcharge** | `$25.00 / MMBtu` | `$0.00 / MMBtu` (Zero Penalty) | `+100.0%` | **Warning** |

---

### Visualization Triggers

* **Recommended Chart Type**: Horizontal / Clustered Bar Chart illustrating real-time pipeline utilization vs. OFO threshold limits across key supply interconnects.

```json
{
  "chart_type": "bar",
  "title": "Pipeline Capacity Utilization vs. OFO Alert Thresholds",
  "xAxis": {
    "categories": [
      "Transco Zone 5/6",
      "Algonquin Citygate",
      "TETCO M3",
      "Dominion South",
      "Columbia Gas (TCO)"
    ],
    "title": "Pipeline / Zone Interconnect"
  },
  "yAxis": {
    "title": "Capacity Utilization (%)",
    "min": 0,
    "max": 110
  },
  "series": [
    {
      "name": "Current Scheduled Flow (%)",
      "data": [96.5, 98.4, 94.2, 82.0, 76.8],
      "color": "#d9534f"
    },
    {
      "name": "OFO Alert Threshold (%)",
      "data": [90.0, 92.0, 90.0, 85.0, 85.0],
      "color": "#f0ad4e"
    }
  ]
}
```

---

### Actionable Recommendations

* **Re-align Generation Dispatch**: Notify real-time trading and plant dispatch to strictly track scheduled Intraday 1 and Intraday 2 gas burn rates to avoid severe unauthorized overrun penalties on Transco and Algonquin.
* **Assess Dual-Fuel Switching**: Evaluate switching dual-fuel combined cycle (CCGT) units in affected zones from natural gas to Ultra-Low Sulfur Diesel (ULSD) / backup fuel oil where spark/dark spreads and emission limits permit.
* **Firm Transport Prioritization**: Verify that all scheduled volumes are nominated under Firm Transportation (FT-1) contracts; re-route any remaining Secondary Firm or IT nominations on TETCO M3 to secondary interconnects or storage withdrawals.
* **Coordinate with RTO/ISO**: Alert the Regional Transmission Organization (e.g., PJM / ISO-NE) of fuel supply limitations and potential maximum generation derates ahead of the next day-ahead market clearing.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_approval_request:
  action_type: "FUEL_SWITCH_AND_INTRA_DAY_GAS_NOMINATION"
  target_assets:
    - "Plant_Bravo_CCGT_Unit_1_2 (Transco Zone 5)"
    - "Plant_Yankee_Peaker_GT (Algonquin Path)"
  proposed_operations:
    - "Switch 420 MW generation load to on-site liquid secondary fuel reserves effective 18:00 EST."
    - "Submit Intraday 3 Gas Re-nomination derating gas intake to 0 MMBtu/h to prevent out-of-balance penalty exposure ($25/MMBtu penalty mitigation)."
  estimated_financial_impact: "$142,500 net operational cost delta vs. estimated penalty exposure of $480,000"
  compliance_basis: "NERC Standard TOP-002-4 / FERC Gas-Electric Reliability Coordination Guidelines"
  requires_human_approval: true
```

### Example 2: Trend & Comparative Analysis
**User:** "Map gas pipeline compressor station outages and pipeline capacity utilization factors against electric generation fuel demand."

**Agent Response:**
### Executive Summary
**Compressor station outages on key interstate gas corridors (notably MidValley CS-12 and TransEast CS-04) have reduced total effective throughput capacity by 28.3% across high-demand delivery zones. Pipeline capacity utilization factors along constrained paths now exceed 96.0% of derated operating limits, directly clashing with a 14.8% peak hour increase in electric generation fuel demand. Without targeted fuel switching and day-ahead LMP constraint management, downstream gas-fired generation assets face severe fuel burn curtailment and high intraday basis price exposure.**

---

### Data Presentation: Operational & Market Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **System Effective Pipeline Capacity** | 8,150 MMcf/d | 9,850 MMcf/d | -17.26% | **Critical** |
| **Compressor Outage Deratings (Total)** | 1,700 MMcf/d | 250 MMcf/d | +580.00% | **Critical** |
| **Peak Pipeline Capacity Utilization** | 96.03% | 82.00% | +17.11% | **Critical** |
| **Electric Generation Gas Burn Demand** | 4,260 MMcf/d | 3,710 MMcf/d | +14.82% | **Warning** |
| **Non-Firm Secondary Transportation Curtailment** | 480 MMcf/d | 0 MMcf/d | N/A | **Critical** |
| **Downstream Citygate Basis Spread** | $2.85 / MMBtu | $0.45 / MMBtu | +533.33% | **Critical** |
| **Dual-Fuel Generation Oil Inventory Readiness** | 94.20% | 90.00% | +4.67% | **Normal** |

---

### Pipeline Segment Mapping & Generation Interconnects

| Pipeline Segment / Corridor | Interconnect Grid Zone | Active Compressor Outage Status | Derated vs. Design Capacity (MMcf/d) | Utilization Factor (post-Derate) | Electric Gen Demand (MMcf/d) | Fuel Supply Deficit Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TransEast (Segment 4B)** | Zone East (PJM/NYISO) | CS-04 (Turbine Trip / Derate) | 1,260 / 1,800 (-30%) | **96.03%** | 850 | **High / Critical** |
| **MidValley Mainline** | Zone Central (MISO) | CS-12 (Forced Outage - Valve) | 1,430 / 2,200 (-35%) | **97.20%** | 920 | **High / Critical** |
| **Gulflink North Header** | Zone South (ERCOT/SPP) | CS-02 (Nominal) | 1,500 / 1,500 (0%) | 75.00% | 610 | **Low / Normal** |
| **Appalachian Header** | Zone Mid-Atlantic | CS-08 (Nominal) | 2,400 / 2,400 (0%) | 77.08% | 1,100 | **Low / Normal** |
| **Coastal Mainline (South-to-North)** | Zone Northeast | CS-01 (Planned Maintenance) | 1,560 / 1,950 (-20%) | **91.03%** | 780 | **Moderate / Warning** |

---

### Visualization Configuration

**Recommended Chart**: Stacked/Grouped Bar Chart mapping Design Capacity, Effective Throughput post-Outage, Scheduled Volume, and Gas Generation Fuel Demand by Segment.

```json
{
  "chart_type": "bar",
  "title": "Pipeline Capacity, Effective Throughput & Gas Generation Demand by Pipeline Segment",
  "categories": [
    "TransEast - CS-04 (Derated)",
    "MidValley - CS-12 (Forced Outage)",
    "Gulflink North - CS-02 (Nominal)",
    "Appalachian Header - CS-08 (Nominal)",
    "Coastal Mainline - CS-01 (Planned Maint)"
  ],
  "series": [
    {
      "name": "Design Capacity (MMcf/d)",
      "data": [1800, 2200, 1500, 2400, 1950]
    },
    {
      "name": "Effective Capacity post-Outage (MMcf/d)",
      "data": [1260, 1430, 1500, 2400, 1560]
    },
    {
      "name": "Scheduled Throughput (MMcf/d)",
      "data": [1210, 1390, 1125, 1850, 1420]
    },
    {
      "name": "Gas-Fired Gen Fuel Demand (MMcf/d)",
      "data": [850, 920, 610, 1100, 780]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Nomination Rebalancing & Priority Scheduling**: Transition non-firm transportation (IT/Secondary) gas nominations to Primary Firm entitlements across `TransEast CS-04` and `MidValley CS-12` interconnect points to protect scheduled generation burn ahead of Timely nomination deadlines (13:00 CCT).
2. **Execute Dual-Fuel Switching Protocols**: Notify generation operations to initiate dual-fuel readiness (Ultra-Low Sulfur Diesel / Fuel Oil #2) on 380 MW of dual-fuel capable CCGT units in Zone East and Zone Central to reduce pipeline burn requirement by ~65 MMcf/d.
3. **Wholesale Trading Basis & Financial Spread Hedging**: Lock in basis hedges between Henry Hub and downstream delivery points (Zone East Citygate) to mitigate basis price spikes driven by physical capacity bottlenecks.
4. **Coordinate with Regional Transmission Operators (RTO/ISO)**: Submit updated EcoMax / EcoMin fuel constraint telemetry to the RTO to reflect localized pipeline deliverability restrictions and ensure accurate nodal pricing (LMP) and security-constrained economic dispatch (SCED).

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_action_request:
  action_type: "FUEL_SWITCH_AND_GAS_NOMINATION_REALLOCATION"
  description: "Reallocate 65 MMcf/d of firm pipeline delivery away from constrained CCGTs in Zone East to dual-fuel oil backup, and submit an adjusted Day-Ahead generation offer curve to the ISO."
  affected_assets:
    - "TransEast Segment 4B Delivery Points"
    - "CCGT Unit 1 & 2 (Zone East - 380 MW Combined)"
  operational_impact:
    - "Switches 380 MW electric capacity to secondary distillate fuel."
    - "Prevents pipeline imbalance penalties ($15.00/MMBtu overrun charges)."
    - "Estimated intraday basis risk avoidance: $185,250."
  approval_workflow: "Requires confirmation from Wholesale Trading Lead and Generation Shift Supervisor (HITL)."
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Rebalance intra-day gas nominations on Line 300 to avoid pipeline imbalance penalties and secure evening turbine fuel supply."

**Agent Response:**
### Executive Summary
**Intra-day flow telemetry on Line 300 indicates a projected evening turbine fuel deficit of 22.0 MMCFD against current scheduled nominations, risking operational curtailment and severe pipeline imbalance cash-out penalties under FERC OFO (Operational Flow Order) provisions. Rebalancing Cycle 3 (Intraday 1) and Cycle 4 (Intraday 2) nominations up to 72.0 MMCFD will align supply with peak gas turbine dispatch (18:00–22:00) while keeping pipeline utilization at 96.0% of the 75.0 MMCFD firm capacity threshold. Executing this nomination rebalance eliminates an estimated $184,500 in pipeline unbalance penalties and ensures grid reliability compliance.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Line 300 Scheduled Nomination (Cycle 2)** | 50.0 MMCFD | 72.0 MMCFD | -30.56% | **Warning** |
| **Forecasted Evening Turbine Burn (18:00-22:00)** | 72.0 MMCFD | 50.0 MMCFD | +44.00% | **Critical** |
| **Projected Cumulative Imbalance** | -22.0 MMCFD | $\pm$ 2.5 MMCFD (Tolerance) | +780.00% | **Critical** |
| **Line 300 Available Firm Capacity** | 75.0 MMCFD | 75.0 MMCFD | 0.00% | **Normal** |
| **Linepack Operating Pressure (Line 300)** | 685 PSIG | 720 PSIG (Nominal) | -4.86% | **Warning** |
| **OFO / Daily Cash-Out Penalty Exposure** | $184,500 | $0.00 | N/A | **Critical** |

---

### Visualization: Nomination vs. Burn Demand Profile

```json
{
  "chart_type": "line",
  "title": "Line 300 Intra-Day Gas Nominations vs Turbine Burn Requirement",
  "xAxis": {
    "title": "Nomination Cycle / Hour",
    "categories": [
      "Cycle 1 (Timely)",
      "Cycle 2 (Evening)",
      "Cycle 3 (ID1)",
      "Cycle 4 (ID2)",
      "Cycle 5 (ID3)",
      "Peak Evening Burn (18:00-22:00)"
    ]
  },
  "yAxis": {
    "title": "Flow / Burn Rate (MMCFD)"
  },
  "series": [
    {
      "name": "Current Scheduled Nomination",
      "data": [45.0, 48.0, 52.0, 52.0, 50.0, 50.0]
    },
    {
      "name": "Forecasted Evening Turbine Demand",
      "data": [42.0, 46.0, 64.0, 68.0, 70.0, 72.0]
    },
    {
      "name": "Proposed Rebalanced Nomination",
      "data": [45.0, 48.0, 65.0, 69.0, 71.0, 72.0]
    },
    {
      "name": "Pipeline Capacity Limit",
      "data": [75.0, 75.0, 75.0, 75.0, 75.0, 75.0]
    }
  ]
}
```

---

### Actionable Recommendations

- **Submit Intraday 1 (Cycle 3) & Intraday 2 (Cycle 4) Nominations**: Incrementally adjust scheduled receipts from 50.0 MMCFD to 72.0 MMCFD at receipt point meter `M-L300-NORTH` to cover the evening power generation ramp.
- **Utilize Secondary Storage Draw**: If Line 300 upstream receipt point cuts occur during confirmation, trigger a secondary draft from the storage header at `STRG-ZONE-B` (up to 5.0 MMCFD buffer).
- **Monitor Real-Time Pressure Drop**: Maintain minimum delivery pressure above 650 PSIG at the turbine fuel gas skid to prevent low-pressure turbine trip interlocks.
- **Reconcile Imbalance Ledger**: Verify post-cycle scheduling confirmation with pipeline gas control to confirm zero unauthorized overrun / imbalance status.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PIPELINE_NOMINATION_REBALANCE",
  "agent": "natural_gas_pipeline_constraint_analyzer",
  "pipeline_system": "Line 300",
  "receipt_meter_id": "M-L300-NORTH",
  "delivery_point_id": "DEL-TURBINE-STN1",
  "nomination_details": {
    "current_scheduled_volume_mmcfd": 50.0,
    "requested_nomination_volume_mmcfd": 72.0,
    "net_adjustment_mmcfd": 22.0,
    "effective_cycle": "Intraday 1 (ID1) / Intraday 2 (ID2)",
    "market_window_deadline_utc": "15:00 UTC",
    "financial_exposure_mitigated_usd": 184500.00
  },
  "compliance_check": {
    "within_firm_transport_rights": true,
    "ferc_ofo_compliant": true,
    "pressure_constraint_checked": true
  },
  "authorization_required": "Wholesale Gas Trading Desk Lead / Human-in-the-Loop Operator",
  "status": "PENDING_OPERATOR_APPROVAL"
}
```
