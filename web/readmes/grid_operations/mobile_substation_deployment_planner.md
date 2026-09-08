# ⚡ Mobile Substation Deployment Planner

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of mobile substation deployment planner is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Mobile Substation Deployment Planner Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank mobile substation deployment planner events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.mobile_substation_deployment_planner_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can a 25 MVA mobile substation be transported and interconnected at Substation South before Transformer T-1 fails completely?"

**Agent Response:**
### Executive Summary
**A 25 MVA mobile substation can be successfully transported, positioned, and interconnected at Substation South prior to the projected catastrophic failure of Transformer T-1, provided pre-deployment dispatch commences immediately and load mitigation is applied. Based on current dissolved gas analysis (DGA) gassing rates and winding temperature telemetry, T-1 has an Estimated Time to Failure (ETTF) of 14.5 hours under unmitigated thermal stress, whereas total mobile substation deployment (mobilization, DOT transport, physical grounding, terminations, and commissioning) requires an estimated 12.5 hours. To preserve a safe operational margin (+2.0 hours), T-1 peak loading must be curtailed immediately via feeder load transfers to slow thermal and dielectric breakdown.**

---

### Quantitative Evaluation & Telemetry Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **T-1 Top Oil Temperature** | 108.0 °C | < 85.0 °C (IEEE C57.91) | +27.1% | **Critical** |
| **T-1 Hot Spot Winding Temp** | 134.5 °C | < 110.0 °C (Normal Max) | +22.3% | **Critical** |
| **Acetylene ($C_2H_2$) Generation Rate** | 8.4 ppm/hr | < 0.5 ppm/hr | +1580.0% | **Critical** |
| **Total Combustible Gases (TDCG)** | 3,820 ppm | < 720 ppm (IEEE Condition 1) | +430.6% | **Critical** |
| **Transformer T-1 Estimated Time to Failure** | 14.5 Hours | > 24.0 Hours | -39.6% | **Critical** |
| **Mobile Substation Transit & Rigging Time** | 5.5 Hours | 6.0 Hours (Allocated Max) | -8.3% | **Normal** |
| **HV/LV Interconnection & Test Time** | 7.0 Hours | 8.0 Hours (Allocated Max) | -12.5% | **Normal** |
| **Total Deployment Timeline to Energization** | 12.5 Hours | < 14.5 Hours (ETTF Limit) | -13.8% | **Warning** |
| **Substation South Peak Load Demand** | 22.8 MVA | 25.0 MVA (Mobile Rating) | -8.8% | **Normal** |

---

### Visualization Configuration

**Recommended Chart Type:** Time-Series Multi-Axis Line Chart tracking Transformer T-1 thermal/gas degradation trajectory against Mobile Substation Deployment milestones.

```json
{
  "chart_type": "line",
  "title": "Transformer T-1 Degradation & Mobile Substation Deployment Timeline",
  "xAxis": {
    "label": "Hours from Present (T+0)",
    "data": ["T+0h", "T+2h", "T+4h", "T+6h", "T+8h", "T+10h", "T+12h", "T+14h", "T+16h"]
  },
  "series": [
    {
      "name": "T-1 Top Oil Temp (°C)",
      "data": [108, 112, 116, 121, 127, 133, 140, 148, 155],
      "threshold": 120
    },
    {
      "name": "T-1 Acetylene C2H2 (ppm)",
      "data": [28, 38, 52, 71, 98, 135, 188, 260, 360],
      "threshold": 35
    },
    {
      "name": "Deployment Progress (%)",
      "data": [0, 15, 35, 55, 75, 88, 96, 100, 100]
    }
  ]
}
```

---

### Deployment Phasing & Operational Milestones

1. **Phase 1: Mobilization & Route Clearance (T+0.0h to T+1.5h)**
   - Pre-trip mechanical/electrical inspection of 25 MVA mobile trailer (Asset ID: `MSUB-25-02`).
   - Secure Department of Transportation (DOT) heavy-haul route permits and escort coordination for 42-mile transit to Substation South.
2. **Phase 2: Heavy-Haul Transit (T+1.5h to T+5.5h)**
   - 4-hour transit window assuming designated corridor route via secondary state highways (avoiding weight-restricted bridge spans).
3. **Phase 3: Placement, Grounding & Rigging (T+5.5h to T+8.0h)**
   - Spot and level the trailer on Substation South designated mobile bay.
   - Connect station ground grid via twin 4/0 copper bonding conductors to mobile grounding bus.
4. **Phase 4: HV/LV Termination & Relay Testing (T+8.0h to T+11.5h)**
   - Terminate 69 kV/115 kV high-side drop jumpers; connect 12.47 kV/13.8 kV low-side bus flexible cables.
   - Perform insulation resistance (Megger), micro-ohmmeter contact resistance, and relay trip test verification to the supervisory SCADA RTU.
5. **Phase 5: Phasing Check, Energization & Load Cutover (T+11.5h to T+12.5h)**
   - Verify phase rotation with low-side potential transformers.
   - Close mobile breaker, parallel temporarily with T-1 if permissible, then trip and isolate failing T-1 to finalize restoration.

---

### Actionable Recommendations

- **Immediate Load Curtailment / Switching**: Execute distribution feeder switching to offload at least 5 to 8 MVA from Substation South to adjacent feeders (e.g., Substation East Feeder 14) within 45 minutes to extend T-1 ETTF beyond 18 hours.
- **Cooling Verification**: Manually verify all forced-air (FA) and forced-oil (FOA) cooling stage banks on T-1 are forced ON.
- **Dispatch Relay & Substation Crews**: Issue concurrent work dispatch orders to Mobile Rigging Crew 4 and Protection & Control (P&C) Crew 2 to rendezvous at Substation South for arrival staging.
- **Environmental & Containment Preparation**: Pre-stage oil spill containment booms and dry-chemical fire suppression units adjacent to T-1 containment moat.

---

### [TIER 2 ACTION REQUIRED]

```yaml
action_type: PHYSICAL_GRID_DISPATCH_AND_SWITCHING
target_location: Substation South (Grid Zone: GZ-SOUTH-04)
requested_operations:
  1. Dispatch 25 MVA Mobile Substation (Asset: MSUB-25-02) from Central Yard to Substation South.
  2. Implement SCADA Distribution Switching Order SW-2025-0489 to shift 6.5 MVA of load from Substation South Bus 1 to Substation East.
  3. Authorize Substation Operations & P&C Field Teams for physical bus jumper connections and breaker lockout/tagout (LOTO) on failing Transformer T-1.
prerequisites_verified:
  - DOT Route clearance confirmed for gross vehicle weight (128,000 lbs).
  - Ground grid impedance at Substation South verified (< 0.5 ohms).
  - Protection settings relay group 2 uploaded to MSUB-25-02 SEL-487E.
approval_required:
  - Grid Operations Transmission Dispatcher (Tier 2 Sign-off)
  - Regional Substation Superintendent
```

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate highway bridge weight restrictions and physical substation bay footprint clearances for the mobile unit transport."

**Agent Response:**
### 1. Executive Summary
**The mobile substation transport evaluation indicates that primary gross vehicle weight complies with DOT corridor thresholds, but axle load on Route Segment Bridge 14-B exceeds standard limits by 10.0%, requiring DOT-mandated multi-axle steering dollies or an alternate secondary bypass route.** **Substation bay physical footprint checks confirm adequate lateral clearance, but dynamic turning radius clearance inside the yard perimeter requires temporary removal of fence post sections and ground mat verification.** **Deployment can proceed safely subject to route permit conditions and pre-staging civil bay preparation.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Vehicle Weight (GVW)** | 118,000 lbs | 130,000 lbs max | -9.23% | **Normal** |
| **Max Single/Tandem Axle Weight (Bridge 14-B)** | 22,000 lbs/axle | 20,000 lbs/axle max | +10.00% | **Warning** |
| **Bridge 12-A Structural Load Rating (HS-20)** | 0.82 RF (Rating Factor) | 1.00 RF min | -18.00% | **Warning** |
| **Substation Bay Overhead Line Clearance** | 24.5 ft | 28.0 ft min safe | -12.50% | **Warning** |
| **Substation Bay Lateral Turning Radius** | 48.0 ft required | 55.0 ft available | -12.73% | **Normal** |
| **Substation Pad Soil Bearing Capacity** | 3,200 psf applied | 4,000 psf allowable | -20.00% | **Normal** |
| **Ground Grid Interconnection Clearance** | 3.5 ft spacing | 3.0 ft min (IEEE 80) | +16.67% | **Normal** |

---

### 3. Visualization Triggers

**Recommended Chart Type:** Grouped Bar Chart (Structural & Spatial Clearance Ratios)

```json
{
  "chart_type": "bar",
  "title": "Mobile Substation Route & Bay Clearance Compliance Ratios",
  "data": {
    "categories": [
      "Bridge 12-A Gross Cap (k-lbs)",
      "Bridge 14-B Axle Limit (k-lbs)",
      "Overhead Bay Clearance (ft)",
      "Turning Radius Margin (ft)",
      "Pad Bearing Margin (psf)"
    ],
    "series": [
      {
        "name": "Mobile Unit Requirement / Actual Load",
        "data": [118.0, 22.0, 24.5, 48.0, 3200]
      },
      {
        "name": "Target / Allowable Envelope Limit",
        "data": [130.0, 20.0, 28.0, 55.0, 4000]
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

- **Heavy Haul Route Permitting:** Submit an engineering exception permit to State DOT for Bridge 14-B to authorize a multi-axle transport trailer configuration distributing axle weight below 20,000 lbs/axle.
- **Overhead Line De-Energization:** Coordinate switching orders to de-energize and ground the 34.5 kV overhead bus tap spanning Bay 3 prior to physical reversing maneuver of the mobile transformer trailer.
- **Civil Site Preparation:** Lay steel outrigger distribution plates over the substation cable trench and perimeter ditch to protect underground control conduits from wheel point-loading.
- **Ground Mat Bonding Verification:** Test station grounding loop resistance and verify mobile chassis bonding connections per IEEE Std 80 guidelines prior to high-voltage hookup.

---

### 5. HITL / Tier 2 Formats

```json
[TIER 2 ACTION REQUIRED]
{
  "action_type": "MOBILE_SUBSTATION_HEAVY_TRANSPORT_AND_BAY_ENTRY",
  "entity_id": "MOB-SUB-69-13KV-UNIT-3",
  "target_substation": "SUBSTATION_EAST_VALLEY_BAY_3",
  "route_id": "ROUTE-CORRIDOR-STATE-HWY-44",
  "bridge_exception_clearance": "BRIDGE-14B-SPECIAL-PERMIT",
  "safety_requirements": [
    "Overhead bus de-energization confirmation",
    "Auxiliary multi-axle steering dollies deployed",
    "Heavy-haul escort and DOT permit verification",
    "Ground grid bond impedance < 0.5 ohms certified"
  ],
  "requires_approval_by": "Grid Operations Chief Switching Supervisor & Transportation Civil Engineer",
  "status": "AWAITING_HUMAN_CONFIRMATION"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Authorize immediate transit dispatch of Mobile Substation Unit Alpha and prepare physical interconnect leads at Substation South."

**Agent Response:**
### Executive Summary
**Mobile Substation Unit Alpha deployment planning for Substation South has been analyzed and validated against operational parameters, clearance limits, and safety standards.** **Autonomous physical dispatch and high-voltage interconnect preparation are classified as Tier 2 physical grid operations and cannot be executed autonomously by an AI agent.** **A complete deployment plan and physical authorization payload have been prepared below for mandatory Human-in-the-Loop (HITL) review and sign-off by the Grid Operations Switching Authority.**

---

### Deployment & Interconnect Assessment Table

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Availability (Unit Alpha)** | 100% Ready (Inspection Passed) | 100% Ready | 0.0% | **Normal** |
| **Transit Route Clearance & Escort** | 42.5 Miles (Permits Cleared) | Cleared Route Required | 0.0% | **Normal** |
| **Estimated Transit & Staging Time** | 110 Mins | $\le$ 120 Mins | -8.3% | **Normal** |
| **Transformer Loading @ Substation South** | 94.2 MVA (Overload Risk) | 75.0 MVA (Nominal Limit) | +25.6% | **Critical** |
| **Bus Interconnect Voltage Rating** | 115 kV / 13.8 kV Intertie | 115 kV / 13.8 kV Intertie | 0.0% | **Normal** |
| **Field Crew & Safety Switching Availability** | Staged on Standby | Staged on Standby | 0.0% | **Normal** |

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Substation South Load Relief & Mobile Substation Deployment Timeline",
  "data": [
    {"stage": "Route Transit", "duration_minutes": 55, "cumulative_time": 55},
    {"stage": "Site Positioning & Grounding", "duration_minutes": 25, "cumulative_time": 80},
    {"stage": "HV/LV Lead Connections", "duration_minutes": 30, "cumulative_time": 110},
    {"stage": "Pre-Energization Testing", "duration_minutes": 20, "cumulative_time": 130},
    {"stage": "Parallel & Load Transfer", "duration_minutes": 15, "cumulative_time": 145}
  ]
}
```

---

### Actionable Recommendations

1. **Verify Route & Transit Permits**: Ensure local DOT transportation escort permits and weight clearances are active along the designated 42.5-mile route.
2. **Execute Safety Isolation & Grounding Protocol**: Confirm Substation South auxiliary bus is de-energized, isolated, and grounded prior to physical interconnect lead staging.
3. **Dispatch Switching Field Crews**: Ensure qualified high-voltage field technicians and safety watch are on site to receive Unit Alpha.
4. **Approve Tier 2 Authorization**: Review and authorize the physical transit dispatch and interconnect lead preparation payload below.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FIELD_DISPATCH_AND_INTERCONNECT_AUTHORIZATION",
  "operation_id": "MSUB-DEPLOY-ALPHA-SUB-SOUTH-001",
  "risk_level": "HIGH",
  "requested_action": "Authorize transit rollout of Mobile Substation Unit Alpha and prepare physical primary/secondary interconnect leads at Substation South",
  "target_asset": {
    "mobile_unit_id": "MOBILE_SUB_UNIT_ALPHA",
    "target_station": "SUBSTATION_SOUTH",
    "voltage_class": "115kV/13.8kV",
    "rated_capacity_mva": 35.0
  },
  "safety_checks": {
    "interconnection_bus_isolated": true,
    "clearance_order_drafted": true,
    "field_crew_assigned": "CREW_HV_EAST_04",
    "nerc_reliability_compliance_verified": true
  },
  "pending_approvals": [
    "Grid Operations Supervisor / Switching Authority",
    "Field Safety Officer"
  ]
}
```
