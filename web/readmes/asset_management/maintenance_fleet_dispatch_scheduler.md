# ⚡ Maintenance Fleet Dispatch Scheduler

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of maintenance fleet dispatch scheduler is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Maintenance Fleet Dispatch Scheduler Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank maintenance fleet dispatch scheduler events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.maintenance_fleet_dispatch_scheduler_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which aerial bucket trucks and digger derricks are closest to the reported pole fire on Highway 101?"

**Agent Response:**
### 1. Executive Summary
**A critical pole fire incident on Highway 101 (Grid Zone: North Corridor / Feeder 101-B) requires immediate structural replacement and overhead line repair. Telematics analysis identifies Aerial Bucket Truck BT-402 (4.2 miles, ETA 8 mins) and Digger Derrick DD-108 (5.8 miles, ETA 12 mins) as the closest available certified units with available 2-man qualified electrical worker (QEW) crews. Dispatching these physical fleet assets requires mandatory operator authorization under utility Tier 2 safety protocols.**

---

### 2. Data Presentation

#### Candidate Fleet Units (Proximity to Highway 101 Incident)
| Vehicle ID | Asset Class | Current Status | Assigned Crew | Current Location / Staging | Distance to Scene | Estimated Transit Time (ETA) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BT-402** | 55ft Aerial Bucket Truck | Available / Staged | Crew 14 (QEW x2) | Service Center North (Yard 3) | 4.2 miles | 8 mins |
| **DD-108** | 45ft Digger Derrick | Available / Staged | Crew 09 (QEW x2, Op x1) | Substation West Staging | 5.8 miles | 12 mins |
| **BT-415** | 60ft Aerial Bucket Truck | In Transit (Routine Maint) | Crew 22 (QEW x2) | Sector 4 Junction | 8.1 miles | 16 mins |
| **DD-112** | 50ft Digger Derrick | Available / Staged | Crew 03 (QEW x2, Op x1) | Central Ops Yard | 11.4 miles | 22 mins |

#### Operational & Fleet Dispatch Metrics
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Nearest Bucket Truck ETA** | 8.0 mins | ≤ 15.0 mins | -46.7% | Normal |
| **Nearest Digger Derrick ETA** | 12.0 mins | ≤ 20.0 mins | -40.0% | Normal |
| **Combined Crew Availability** | 100% (Certified) | 100% | 0.0% | Normal |
| **Feeder SAIDI Impact Risk** | 3.4 mins/customer | ≤ 1.5 mins/customer | +126.7% | Critical |
| **Asset Replacement Readiness** | Class 2 Pole & Crossarms Ready | Staged for Loading | 0.0% | Normal |

---

### 3. Visualization Triggers
- **Recommended Chart**: Proximity & Estimated Transit Time Comparison (Bar Chart)
- **JSON Payload**:
```json
{
  "chart_type": "bar",
  "title": "Proximity & ETA to Highway 101 Pole Fire Incident",
  "categories": ["Bucket Truck BT-402", "Digger Derrick DD-108", "Bucket Truck BT-415", "Digger Derrick DD-112"],
  "series": [
    {
      "name": "Distance (miles)",
      "data": [4.2, 5.8, 8.1, 11.4]
    },
    {
      "name": "Estimated Transit Time (mins)",
      "data": [8, 12, 16, 22]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Primary Dispatch Plan**: Assign **Bucket Truck BT-402 (Crew 14)** for immediate de-energization verification, framing, and line clearance, and **Digger Derrick DD-108 (Crew 09)** for replacement pole setting and auger operations.
- **Secondary / Backup Reservation**: Place **BT-415** on standby divert status if initial damage assessment confirms crossarm or multi-span conductor damage requiring dual-bucket support.
- **Traffic Control & First Responder Coordination**: Coordinate with CHP and local fire authorities to establish a Highway 101 lane closure buffer prior to heavy digger outrigger deployment.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation: Physical Fleet Truck Roll & Emergency Dispatch
incident_id: INC-HWAY101-POLEFIRE-01
grid_zone_id: GZ-NORTH-101B
target_assets:
  - vehicle_id: "BT-402"
    type: "Aerial Bucket Truck"
    crew_id: "CREW-14"
    eta_minutes: 8
  - vehicle_id: "DD-108"
    type: "Digger Derrick"
    crew_id: "CREW-09"
    eta_minutes: 12
destination: "Highway 101 Mile Marker 42.4 (Pole #P-99214)"
dispatch_reason: "Emergency pole structural failure / active pole fire remediation"
authorization_required: "Dispatcher / Grid Operations Supervisor Approval Required to Commit Fleet Units"
```

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate crew route efficiency and overtime hours across regional service depots during yesterday's lightning storm."

**Agent Response:**
### Executive Summary
**During yesterday's convective lightning storm event, regional maintenance fleet performance exhibited significant variance, with overall route efficiency dropping to 80.8% against an operational baseline of 88.0%. Overtime hours surged across storm-impacted corridors, accumulating 439.5 total crew overtime hours with the North and East Depots bearing 59.3% of the overtime load due to road obstructions and clustered feeder lockouts. Dispatch routing adjustments and re-staging of standby crews are required to mitigate ongoing restoration delays and normalize crew fatigue cycles.**

---

### Quantitative Performance Metrics

The table below summarizes fleet dispatch efficiency, travel metrics, and overtime distribution across regional service depots during yesterday's storm window.

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Route Efficiency (System-wide)** | 80.8% | 88.0% | -8.18% | **Warning** |
| **Total Crew Overtime Hours** | 439.5 hrs | 180.0 hrs | +144.17% | **Critical** |
| **North Depot Route Efficiency** | 68.4% | 88.0% | -22.27% | **Critical** |
| **East Depot Route Efficiency** | 72.1% | 88.0% | -18.07% | **Warning** |
| **Metro Central Route Efficiency** | 84.5% | 88.0% | -3.98% | **Normal** |
| **South Depot Route Efficiency** | 88.2% | 88.0% | +0.23% | **Normal** |
| **West Valley Route Efficiency** | 91.0% | 88.0% | +3.41% | **Normal** |
| **Average Travel Time per Work Order** | 38.4 min | 25.0 min | +53.60% | **Critical** |
| **Average ETR Restoration Deviation** | +24.6 min | ≤ ±10.0 min | +146.00% | **Critical** |
| **Total Feeder Outage Dispatches** | 184 dispatches | 65 dispatches | +183.08% | **Critical** |

---

### Visualization Trigger: Route Efficiency vs. Overtime Hours

```json
{
  "chart_type": "bar",
  "title": "Depot Route Efficiency vs. Overtime Hours (Yesterday's Storm)",
  "xAxis": {
    "title": "Regional Service Depot",
    "categories": [
      "North Depot (Zone 1)",
      "East Depot (Zone 4)",
      "Metro Central Depot (Zone 2)",
      "South Depot (Zone 3)",
      "West Valley Depot (Zone 5)"
    ]
  },
  "yAxis": [
    {
      "title": "Route Efficiency (%)",
      "min": 0,
      "max": 100
    },
    {
      "title": "Overtime Hours (hrs)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Route Efficiency (%)",
      "type": "column",
      "data": [68.4, 72.1, 84.5, 88.2, 91.0],
      "unit": "%"
    },
    {
      "name": "Overtime Hours",
      "type": "line",
      "yAxis": 1,
      "data": [142.5, 118.0, 86.5, 54.0, 38.5],
      "unit": "hrs"
    }
  ]
}
```

---

### Root Cause Analysis & Engineering Findings

1. **North & East Depot Congestion**: Route efficiency at the North (68.4%) and East (72.1%) depots suffered primarily from road washouts and fallen vegetation along radial feeder spans, causing an average travel latency increase of 18.2 minutes per ticket.
2. **Back-to-Back Dispatch Sequencing**: Dispatch routing engines assigned tickets sequentially rather than clustering by substation feeder heads, leading to redundant inter-zone travel across Zone 1 and Zone 4.
3. **Crew Fatigue & Overtime Exposure**: Overtime exceeded critical thresholds in the North Depot (142.5 hrs across 12 line crews), triggering mandatory rest period protocols under utility labor compliance rules.

---

### Actionable Recommendations

- **Dynamic Work Order Clustering**: Implement dynamic spatial grouping in the dispatch engine to bundle pending transformer and lateral fuse tickets within identical 13.8 kV feeder protection zones prior to routing.
- **Mutual Depot Shift Re-Balancing**: Temporarily reassign 4 standby bucket truck crews from West Valley Depot to North Depot to cover secondary restoration mopping and relieve fatigued crews.
- **Dynamic Routing Layer Integration**: Enable real-time municipal road closure and hazard feeds in the mobile workforce management (MWM) client to reduce in-transit navigation delays.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FLEET_CREW_REALLOCATION",
  "source_depot": "West Valley Depot (Zone 5)",
  "target_depot": "North Depot (Zone 1)",
  "crew_units_to_transfer": [
    {"crew_id": "CREW-WV-04", "type": "Overhead Line Crew (4-Man)"},
    {"crew_id": "CREW-WV-07", "type": "Overhead Line Crew (4-Man)"},
    {"crew_id": "CREW-WV-09", "type": "Troubleshooter Single Unit"},
    {"crew_id": "CREW-WV-12", "type": "Vegetation / Tree Trimming Unit"}
  ],
  "effective_shift_start": "06:00:00 UTC",
  "duration_hours": 24,
  "justification": "Mitigate severe crew overtime fatigue (>140 hrs) and restore degraded route efficiency (68.4%) in storm-damaged North Depot territory.",
  "hitl_approval_required": true,
  "dispatcher_confirmation_status": "PENDING_HUMAN_APPROVAL"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Reroute Crew Bravo from routine preventive inspection to high-priority pole replacement at Substation South."

**Agent Response:**
### Executive Summary
**Crew Bravo is currently scheduled for pre-planned routine preventive inspections; rerouting to high-priority pole replacement at Substation South will mitigate localized asset failure risk and protect feeder reliability. This reassignment represents a physical field resource redirection (Tier 2 operation) and requires Human-in-the-Loop (HITL) dispatch authorization prior to execution. Routine inspections on the originating feeder will be placed on temporary hold and queued for dynamic rescheduling.**

---

### Fleet & Dispatch Assessment

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Failure Probability (Substation South Pole)** | High (AHI < 45) | Normal (AHI > 80) | -43.75% | **Critical** |
| **Crew Bravo Availability / En-Route Feasibility** | Available (Routine Task) | Immediate Dispatch | 0% | **Normal** |
| **Estimated Travel Time to Substation South** | 18 mins | < 30 mins | -40.00% | **Normal** |
| **Estimated Time to Restoration (ETR) Impact** | -45 mins (Avoided Outage) | Baseline SAIDI Cap | N/A | **Warning** |
| **Deferred Inspection Schedule Slippage** | +1.5 Business Days | 0 Days | +150.00% | **Warning** |

---

### Visualization Trigger: Crew Reroute & Feeder Impact

```json
{
  "chart_type": "bar",
  "title": "Dispatch Priority & Risk Comparison",
  "data": [
    {
      "Task": "Routine Inspection (Feeder East)",
      "Priority_Score": 25,
      "Asset_Health_Risk": 15,
      "SAIDI_Exposure_Mins": 0
    },
    {
      "Task": "Pole Replacement (Substation South)",
      "Priority_Score": 95,
      "Asset_Health_Risk": 88,
      "SAIDI_Exposure_Mins": 62
    }
  ]
}
```

---

### Actionable Recommendations

1. **Authorize Reroute**: Confirm the immediate dispatch of Crew Bravo with bucket truck, digger derrick, and Class 2 replacement pole inventory to Substation South.
2. **Safety & Switching Clearance**: Ensure South Substation feeder switching orders, line isolation, and grounding are verified with Distribution Operations before crew arrival.
3. **Reschedule Deferred Task**: Automatically return the postponed routine preventive inspection task to the active scheduling queue with a targeted completion window within 5 business days.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FIELD_CREW_REROUTE_DISPATCH",
  "crew_id": "Crew Bravo",
  "current_assignment": {
    "task_type": "ROUTINE_PREVENTIVE_INSPECTION",
    "status": "SUSPENDED"
  },
  "target_assignment": {
    "task_type": "HIGH_PRIORITY_POLE_REPLACEMENT",
    "location": "Substation South",
    "priority": "HIGH_EMERGENCY",
    "estimated_duration_hours": 4.5
  },
  "safety_clearance_required": true,
  "requires_human_approval": true,
  "authorization_prompt": "Confirm field dispatch override to redirect Crew Bravo to Substation South for emergency pole replacement?"
}
```
