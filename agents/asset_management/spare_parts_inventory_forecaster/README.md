# ⚡ Spare Parts Inventory Forecaster

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of spare parts inventory forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Spare Parts Inventory Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank spare parts inventory forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.spare_parts_inventory_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Do we have sufficient spare 50kVA pole-mounted distribution transformers in Central Warehouse to withstand peak storm season?"

**Agent Response:**
### Executive Summary
**Current inventory levels of 50kVA pole-mounted distribution transformers at Central Warehouse are insufficient to meet the upper-bound (P95) storm season replacement demand without triggering safety stock breaches. While on-hand physical stock currently stands at 142 units against a baseline minimum requirement of 45 units, cumulative peak storm season failure models project a replacement requirement of 234 units across the season, resulting in a forecasted deficit of 23 units below safety buffer thresholds by late September. Immediate procurement expediting and regional inventory re-allocation are required to mitigate service restoration risks.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **On-Hand Inventory (Central Warehouse)** | 142 Units | 180 Units (Pre-Storm Target) | -21.1% | **Warning** |
| **Minimum Safety Stock Threshold** | 45 Units | 45 Units | 0.0% | **Normal** |
| **P95 Peak Storm Cumulative Demand Forecast** | 234 Units | 160 Units (Historical Avg) | +46.3% | **Critical** |
| **Projected End-of-Season Stock Deficit** | 22 Units (Stock) | 45 Units (Safety Buffer) | -51.1% | **Critical** |
| **Supplier Lead Time (Standard Procurement)** | 56 Days | 30 Days (Expedited SLA) | +86.7% | **Warning** |
| **Model Accuracy (Backtested MAPE)** | 3.8% | < 5.0% Target | -24.0% | **Normal** |

*Analytical Assumptions & Modeling Parameters:*
- **Model Standard**: Probabilistic Monte Carlo storm failure simulation (10,000 runs) evaluated at 95% Confidence Interval ($Z = 1.96$) using IEEE C57.91 thermal loading and historical wind-shear failure distributions.
- **Operating Context**: Central Warehouse servicing Feeders in Grid Zones Central-North and Central-South. Lead-time supply chain constraints reflect current regional supplier capacity.

---

### Visualization Trigger

**Recommended Chart**: Time-Series Line Chart with Safety Margin Threshold Boundary.

```json
{
  "chart_type": "line",
  "title": "50kVA Pole-Mounted Transformer Stock vs Storm Demand Forecast (Central Warehouse)",
  "xAxis": ["Jun", "Jul", "Aug", "Sep", "Oct", "Nov"],
  "series": [
    {
      "name": "Projected Stock (Units)",
      "data": [142, 118, 76, 42, 28, 22]
    },
    {
      "name": "P95 Storm Demand Forecast",
      "data": [24, 42, 58, 65, 30, 15]
    },
    {
      "name": "Safety Stock Minimum",
      "data": [45, 45, 45, 45, 45, 45]
    }
  ],
  "yAxis": {
    "label": "Transformer Units",
    "min": 0,
    "max": 160
  }
}
```

---

### Actionable Recommendations

- **Execute Emergency Supplier Purchase Order**: Place an expedited procurement order for 60 units of 50kVA pole-mounted distribution transformers under utility MSA terms to bridge the projected August–September deficit before supplier lead times elapse.
- **Inter-Warehouse Stock Rebalancing**: Initiate an intra-grid transfer of 25 surplus units currently staged at the Western Logistics Depo, where storm risk vulnerability index is lower ($P < 0.12$).
- **Staging & Pre-Positioning**: Pre-allocate 30 units from Central Warehouse directly to forward operating storm staging yards (SSY-Central 1 & 2) by July 15 to reduce dispatch transit latency during severe weather events.
- **Telemetry Health Cross-Check**: Coordinate with the Predictive Maintenance agent to flag high-risk 50kVA units on overloaded feeder runs ($>110\%$ rated capacity) for proactive replacement prior to severe weather alerts.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "EMERGENCY_INVENTORY_PROCUREMENT_AND_TRANSFER",
  "asset_classification": "50kVA Pole-Mounted Distribution Transformer (120/240V)",
  "facility": "Central Warehouse (WH-01)",
  "details": {
    "expedited_purchase_order_units": 60,
    "inter_warehouse_transfer_units": 25,
    "source_facility": "Western Logistics Depo (WH-04)",
    "destination_facility": "Central Warehouse (WH-01)",
    "estimated_expedited_cost_usd": 186000.00,
    "lead_time_target_days": 14
  },
  "compliance_reference": "NERC TPL-001 / Utility Emergency Preparedness Standard",
  "authorization_required": "Human-In-The-Loop (HITL) Grid Asset Manager Approval"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Forecast the 12-month replenishment lead time and burn rate for SF6 gas cylinders and surge arresters."

**Agent Response:**
### Executive Summary
**Projected 12-month demand indicates a critical supply bottleneck for SF6 gas cylinders and surge arresters driven by regulatory phase-downs and summer storm activity. SF6 supplier replenishment lead times have expanded to 180 days with an annual forecasted burn rate of 241 cylinders, while surge arrester burn rates peak sharply during Q2–Q3 storm seasons with a 90-day lead time. Immediate purchase order authorization is required to prevent inventory levels from breaching minimum safety stock thresholds by Month 4.**

---

### Data Presentation

#### Inventory Forecast & Lead Time Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **SF6 Gas Cylinder Stock** | 42 cylinders | 65 cylinders | -35.38% | **Warning** |
| **SF6 Replenishment Lead Time** | 180 days | 90 days | +100.00% | **Critical** |
| **SF6 Annual Burn Rate** | 241 cylinders/yr | 210 cylinders/yr | +14.76% | **Warning** |
| **SF6 Forecast MAPE (Backtest)** | 3.82% | < 5.00% | -23.60% | **Normal** |
| **Surge Arrester Stock (15kV–138kV)** | 35 units | 60 units | -41.67% | **Warning** |
| **Surge Arrester Replenishment Lead Time**| 90 days | 45 days | +100.00% | **Warning** |
| **Surge Arrester Annual Burn Rate** | 257 units/yr | 225 units/yr | +14.22% | **Warning** |
| **Surge Arrester Peak Burn (M5–M7 Storm Season)** | 125 units | 95 units | +31.58% | **Critical** |

---

### 12-Month Monthly Demand & Safety Stock Trajectory

```json
{
  "chart_type": "line",
  "title": "12-Month Inventory Burn Rate & Replenishment Trajectory",
  "xAxis": {
    "type": "category",
    "data": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10", "M11", "M12"]
  },
  "yAxis": {
    "type": "value",
    "name": "Units / Cylinders"
  },
  "series": [
    {
      "name": "SF6 Gas Cylinders (Monthly Demand)",
      "data": [14, 15, 18, 22, 25, 28, 30, 26, 20, 16, 14, 13],
      "type": "line"
    },
    {
      "name": "Surge Arresters (Monthly Demand)",
      "data": [8, 9, 12, 24, 38, 45, 42, 35, 20, 11, 7, 6],
      "type": "line"
    },
    {
      "name": "SF6 Safety Stock Threshold",
      "data": [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
      "type": "line",
      "lineStyle": { "type": "dashed" }
    },
    {
      "name": "Surge Arrester Safety Stock Threshold",
      "data": [15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15, 15],
      "type": "line",
      "lineStyle": { "type": "dashed" }
    }
  ]
}
```

---

### Actionable Recommendations

- **Advance Procurement Schedule**: Issue blanket purchase orders (PO) immediately for 150 SF6 cylinders and 180 surge arresters to buffer against 180-day and 90-day supply chain lead times.
- **Dynamic Safety Stock Adjustment**: Elevate Surge Arrester buffer stock by 25% across transmission and distribution depots in Grid Zones subject to high lightning flash density prior to Month 4.
- **SF6 Leak Mitigation & Non-SF6 Transition**: Deploy acoustic imaging and IR optical gas inspection crews to high-risk circuit breaker bays showing top-quartile top-up frequency to arrest leak rates ahead of regulatory reporting windows.
- **Supplier Dual-Sourcing**: Qualify secondary regional vendors for polymer-housed surge arresters to mitigate extended manufacturing queues during extreme weather events.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_id: ACT-SPARE-PARTS-REPLENISH-2024-001
  domain: Asset Management
  operation_type: Commercial / Material Procurement Authorization
  description: "Initiate blanket purchase orders for 150 SF6 gas cylinders ($185,000) and 180 multi-class surge arresters ($216,000) to meet projected 12-month burn rates and offset supply chain lead times."
  estimated_cost: "$401,000 USD"
  impacted_grid_zones: ["ALL_DEPOTS", "ZONE_NORTH", "ZONE_CENTRAL", "ZONE_COASTAL"]
  risk_assessment: "Failure to issue purchase orders within 14 calendar days will lead to stockout conditions during peak summer lightning and maintenance operations."
  human_in_the_loop_required: true
  approver_roles: ["Asset Inventory Director", "Grid Maintenance Operations Lead"]
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate an automated purchase requisition for 25 units of 15kV cutouts and distribution fuses."

**Agent Response:**
### Executive Summary
**A stock deficit analysis indicates inventory levels for 15kV distribution cutouts and fuse links have dropped below dynamic reorder thresholds due to heightened seasonal maintenance demands. Generating an automated purchase requisition for 25 units will restore inventory to target buffer capacity and prevent supply chain stockouts across operational grid zones. In accordance with utility enterprise governance, executing this financial procurement commitment requires Human-in-the-Loop (HITL) authorization prior to ERP transmission.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **15kV Cutouts In-Stock** | 18 units | 40 units (Safety Buffer) | -55.0% | Warning |
| **Distribution Fuses In-Stock** | 32 units | 75 units (Safety Buffer) | -57.3% | Warning |
| **30-Day Demand Forecast** | 22 units | 15 units (Historical Avg) | +46.7% | Warning |
| **Procurement Lead Time** | 14 Days | 10 Days | +40.0% | Normal |
| **Forecast Model Accuracy (MAPE)** | 4.1% | < 5.0% Target | -0.9% | Normal |

---

### Visualization Triggers
- **Recommended Visualization**: Bar Chart (Inventory Deficit vs. Proposed Requisition Target)
- **Chart Data Configuration**:
```json
{
  "chart_type": "bar",
  "title": "15kV Cutout & Fuse Stock vs. Requisition Level",
  "categories": ["Current Stock", "Reorder Point", "Forecasted 30-Day Demand", "Proposed Requisition Qty"],
  "series": [
    {
      "name": "Units",
      "data": [18, 40, 22, 25]
    }
  ],
  "unit": "Units"
}
```

---

### Actionable Recommendations
- **Approve Purchase Requisition**: Authorize the requisition payload below to dispatch the purchase order to certified OEM distribution suppliers.
- **Expedite Delivery Window**: Request standard 14-day delivery to align with the scheduled predictive replacement cycle in Grid Zone 4.
- **Log Reorder Parameters**: Update the dynamic safety stock baseline in the Asset Management System to reflect the increased seasonal failure rates observed in distribution feeder circuits.

---

### **[TIER 2 ACTION REQUIRED]**

```json
{
  "action_type": "PURCHASE_REQUISITION_SUBMISSION",
  "domain": "Asset Management / Supply Chain",
  "asset_type": "15kV Overhead Distribution Cutouts & Type K/T Fuse Links",
  "order_details": {
    "requisition_id": "REQ-2024-15KV-0882",
    "item_description": "15kV 100A Polymer Cutout Assembly with Distribution Fuse Links",
    "quantity": 25,
    "unit_of_measure": "EA",
    "estimated_unit_cost_usd": 245.00,
    "estimated_total_cost_usd": 6125.00,
    "target_warehouse_id": "WH-CENTRAL-02",
    "urgency_level": "Standard Replenishment"
  },
  "compliance_check": {
    "standard": "IEEE C37.41 / C37.42",
    "mape_confidence": "95.9% (MAPE: 4.1%)",
    "erp_destination": "SAP_MM_GRID_OPS"
  },
  "requires_hitl_approval": true,
  "approval_role": "Procurement Manager / Asset Operations Lead"
}
```
