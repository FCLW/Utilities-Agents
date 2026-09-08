# ⚡ Outage Footprint Topology Mapper

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of outage footprint topology mapper is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Outage Footprint Topology Mapper Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank outage footprint topology mapper events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.outage_footprint_topology_mapper_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which upstream protective device opened to cause the sudden loss of 3,200 smart meters in the Oakridge subdivision?"

**Agent Response:**
### Executive Summary
**Topology correlation and SCADA telemetry trace confirm that mid-feeder automatic recloser `REC-4412` (located on Feeder 14-4 downstream of Oakridge Substation) operated to lockout due to a sustained overcurrent fault. This protective operation isolated the entire downstream Oakridge radial segment, resulting in the sudden loss of telemetry from 3,200 smart meters. Substation breaker `CB-104` remains closed, confirming the fault is localized exclusively downstream of `REC-4412`.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Operating Device State** | `REC-4412` (Open / Lockout) | Closed (Normal) | N/A | **Critical** |
| **Impacted AMI Meters** | 3,200 Meters | 0 Meters | +100.0% | **Critical** |
| **Upstream Substation Breaker (`CB-104`)** | Closed (Active) | Closed (Normal) | 0.0% | **Normal** |
| **Feeder SAIDI Impact (Projected)** | 18.4 min | < 5.0 min | +268.0% | **Warning** |
| **Estimated Time to Restoration (ETR)** | 65 min | 45 min | +44.4% | **Warning** |

---

### Outage Footprint Topology Visualization

```json
{
  "chart_type": "bar",
  "title": "Outage Impact by Upstream Protective Hierarchy",
  "xAxis": {
    "categories": [
      "Substation Feeder Breaker CB-104",
      "Recloser REC-4412 (Tripped)",
      "Sectionalizer SEC-203",
      "Lateral Fuse F-881"
    ],
    "title": "Protective Device"
  },
  "yAxis": {
    "title": "Connected / Downstream Meters"
  },
  "series": [
    {
      "name": "De-energized Meters",
      "data": [0, 3200, 1100, 450]
    },
    {
      "name": "Energized Meters",
      "data": [2600, 0, 0, 0]
    }
  ]
}
```

---

### Actionable Recommendations
- **FLISR Sequence Execution**: Validate topology boundary conditions to execute an automated Fault Location, Isolation, and Service Restoration (FLISR) switching sequence via tie switch `SW-5519` to restore 1,900 unfaulted customers on the healthy loop.
- **Field Patrol Dispatch**: Direct Trouble Truck Crew #4 to patrol the 1.8-mile line segment between Recloser `REC-4412` and Sectionalizer `SEC-203` to inspect for physical line contact (e.g., vegetation or equipment failure).
- **SCADA Fault Data Extraction**: Retrieve digital fault recorder (DFR) oscillography and sequence-of-events (SOE) logs from `REC-4412` to evaluate fault type (Phase-to-Ground vs. Phase-to-Phase) and calculated fault impedance.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "GRID_SWITCHING_OPERATION",
  "device_id": "REC-4412",
  "feeder_id": "FDR-14-4",
  "substation_id": "SUB-OAKRIDGE-01",
  "target_state": "OPEN_ISOLATE_AND_TRANSFER",
  "tie_switch_id": "SW-5519",
  "transfer_load_kVA": 4200,
  "affected_customers": 3200,
  "restoration_path_customers": 1900,
  "requires_hitl_approval": true,
  "operator_prompt": "Confirm execution of FLISR switching plan: Open sectionalizing disconnect SEC-203 and close normally-open tie switch SW-5519 to backfeed 1,900 customers from adjacent Feeder 14-5."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Trace the GIS network connectivity model from reporting meter 'last-gasp' alerts to identify the common protective device."

**Agent Response:**
### Executive Summary
**Topology trace analysis across the GIS network connectivity model has successfully mapped 142 Advanced Metering Infrastructure (AMI) 'last-gasp' alert transmissions to their nearest upstream common protective device: Lateral Fuse `FUSE-4028A` on Feeder `FDR-08` (Substation `SUB-CEDAR-13.8kV`). Upstream automated recloser `REC-1204` remains closed and fully energized with normal phase currents, isolating the physical outage footprint strictly to lateral branch node `LAT-4028`. The correlated outage impact spans 142 metered endpoints with an estimated 0.42 customer-hours contribution toward localized SAIDI.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Correlated AMI Last-Gasps** | 142 Endpoints | 0 Normal State | +100.0% | **Critical** |
| **Identified Protective Device** | `FUSE-4028A` (65T Fuse Link) | Fully Closed (Normal) | N/A | **Critical** |
| **Upstream Recloser Status (`REC-1204`)** | Closed / 3-Phase Normal | Closed | 0.0% | **Normal** |
| **Downstream Unserved Demand** | 486 kW | 0 kW | +100.0% | **Warning** |
| **Affected Feeder Topology Reach** | Lateral Branch `LAT-4028` (1.4 km) | 0 km Interrupted | +100.0% | **Warning** |
| **Estimated Restoration Time (ETR)** | 75 min | 60 min Target | +25.0% | **Warning** |

---

### Visualization Triggers
- **Recommended Chart Type**: **Topology Tree / Aggregated Device Cluster Chart**
- **Purpose**: Visualizes the nested distribution hierarchy (Substation $\rightarrow$ Feeder Breaker $\rightarrow$ Mid-Line Recloser $\rightarrow$ Lateral Fuse $\rightarrow$ Transformers $\rightarrow$ Meters) and highlights the exact point of interruption based on last-gasp density.

```json
{
  "chart_type": "bar",
  "data": {
    "title": "Meter Last-Gasp Cluster by Upstream Protective Device",
    "labels": [
      "FUSE-4028A (Lateral)",
      "REC-1204 (Mid-Feeder Recloser)",
      "CB-FDR-08 (Substation Breaker)",
      "FUSE-4028B (Adjacent Lateral)",
      "TR-7712 Downstream Group"
    ],
    "datasets": [
      {
        "name": "Reporting AMI Last-Gasps",
        "values": [142, 0, 0, 0, 142]
      },
      {
        "name": "Connected Customers",
        "values": [142, 1280, 2450, 88, 142]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Isolate & Verify**: Dispatch a trouble crew to lateral branch `LAT-4028` at pole location `P-4028-01` to inspect for physical line damage (vegetation intrusion or transformer fault downstream of `FUSE-4028A`).
- **SCADA Telemetry Check**: Maintain continuous telemetry polling on upstream recloser `REC-1204` to ensure load current stability across adjacent energized branches.
- **Outage Management System (OMS) Clustering**: Bind the 142 individual AMI incident tickets into a single parent outage event under Device ID `FUSE-4028A` to streamline dispatch and customer communication channels.
- **AMI Ping Sequence**: Initiate downstream automated AMI ping validation to detect any false positives or edge-of-footprint restoration anomalies.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action: DISPATCH_TROUBLE_CREW_AND_MANUAL_SWITCHING_ORDER
  device_id: FUSE-4028A
  feeder_id: FDR-08
  substation_id: SUB-CEDAR-13.8kV
  location_coordinates: "34.0522 N, -118.2437 W (Pole P-4028-01)"
  impact_summary: "Manual field replacement of 65T fuse link and physical line patrol on Lateral LAT-4028 (142 customers affected)."
  approval_status: PENDING_OPERATOR_CONFIRMATION
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Update the operational outage management system (OMS) map to highlight the confirmed blown transformer fuse at Pole #392."

**Agent Response:**
### Executive Summary
**Confirmed hardware fault telemetry indicates a blown transformer cutout fuse at Pole #392, isolating the downstream low-voltage lateral.** **The Outage Footprint Topology Mapper has isolated the outage footprint to 14 downstream customer meters and updated the local operational topology model.** **Operational state changes to the live Outage Management System (OMS) and crew dispatch require operator confirmation via Human-in-the-Loop (HITL) protocol.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Faulted Asset ID** | Pole #392 (Transformer Fuse) | Normal Closed State | N/A | **Critical** |
| **Direct Customer Outage Count** | 14 Meters | 0 Meters | +100% | **Critical** |
| **Feeder Head Current / Status** | 242 A (Feeder #404) | 250 A Target | -3.2% | **Normal** |
| **Upstream Recloser Status** | Closed (Active) | Closed (Active) | 0.0% | **Normal** |
| **Estimated Restoration Time (ETR)** | 75 min | 60 min Target | +25.0% | **Warning** |

---

### Visualization Triggers

- **Recommended Visualization**: **Geographic / Topology Map Chart** highlighting the fault node, upstream feeder backbone, and isolated customer footprint.
- **Topology Configuration Data**:
```json
{
  "chart_type": "topology_map",
  "data": {
    "nodes": [
      { "id": "SUB_NORTH_12", "type": "Substation", "status": "Normal" },
      { "id": "FEEDER_404", "type": "Feeder Backbone", "status": "Normal" },
      { "id": "POLE_392", "type": "Transformer Fuse Cutout", "status": "Blown_Critical", "highlight": true },
      { "id": "METER_GRP_392A", "type": "Downstream Customers", "status": "Outage", "customers_impacted": 14 }
    ],
    "edges": [
      { "source": "SUB_NORTH_12", "target": "FEEDER_404" },
      { "source": "FEEDER_404", "target": "POLE_392" },
      { "source": "POLE_392", "target": "METER_GRP_392A" }
    ]
  }
}
```

---

### Actionable Recommendations

- **Confirm Isolation Perimeter**: Verify that AMI "Last Gasp" alerts from the 14 downstream smart meters align with the topological footprint of Pole #392.
- **Dispatch Trouble Crew**: Assign a field repair crew with replacement cutout fuses (standard 25A/40A fuse link based on transformer kVA rating).
- **Notify Customer Care / IVR**: Update the automated customer messaging system with the localized outage notification and an initial ETR of 75 minutes.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "COMMIT_OMS_STATE_OVERRIDE",
  "target_asset_id": "POLE_392_FUSE",
  "proposed_state": "OPEN_BLOWN",
  "downstream_meters_affected": 14,
  "requires_hitl_approval": true,
  "dispatcher_instructions": "Authorize updating production OMS GIS topology layer to mark Pole #392 cutout fuse as OPEN/BLOWN and release ticket to Field Operations."
}
```
