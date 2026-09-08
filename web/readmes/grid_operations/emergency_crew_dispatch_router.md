# ⚡ Emergency Crew Dispatch Router

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of emergency crew dispatch router is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Emergency Crew Dispatch Router Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank emergency crew dispatch router events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.emergency_crew_dispatch_router_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which line crews with certified live-line barehand qualifications are closest to the emergency wire-down incident on Main St?"

**Agent Response:**
### Executive Summary
**Emergency routing analysis has identified Crew LL-04 as the closest operational unit holding active Certified Live-Line Barehand (LL-BH) qualifications, located 2.4 miles (8-minute ETA) from the Main St wire-down incident. Secondary backup is Crew LL-02 at 5.1 miles (16-minute ETA), currently available in staged status. Dispatching physical field resources to an energized wire-down hazard constitutes a Tier 2 physical grid action requiring human operator confirmation.**

---

### Crew Proximity & Qualification Assessment

| Metric / Crew ID | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary: Crew LL-04 Distance** | 2.4 miles (8 min ETA) | < 15 min Target | -46.7% | **Normal** (Optimal) |
| **Primary: Crew LL-04 Certification** | LL-BH Certified (Active) | IEEE 516 / OSHA 1910.269 | 0.0% | **Normal** (Qualified) |
| **Secondary: Crew LL-02 Distance** | 5.1 miles (16 min ETA) | < 20 min Target | -20.0% | **Normal** (Available) |
| **Secondary: Crew LL-02 Certification**| LL-BH Certified (Active) | IEEE 516 / OSHA 1910.269 | 0.0% | **Normal** (Qualified) |
| **Tertiary: Crew LL-09 Distance** | 8.7 miles (25 min ETA) | < 30 min Target | -16.7% | **Warning** (Transit Delay) |
| **Public Safety Hazard Index** | Level 1 (Downed Conductor) | Level 0 (Safe) | +100.0% | **Critical** (Immediate Isolation Req.) |

---

### Visualization Trigger
```json
{
  "chart_type": "bar",
  "data": {
    "title": "Live-Line Barehand Crew Proximity to Main St Incident",
    "categories": ["Crew LL-04", "Crew LL-02", "Crew LL-09"],
    "series": [
      {
        "name": "Distance (miles)",
        "data": [2.4, 5.1, 8.7]
      },
      {
        "name": "ETA (minutes)",
        "data": [8, 16, 25]
      }
    ]
  }
}
```

---

### Actionable Recommendations
1. **Immediate Dispatch Authorization**: Request immediate operator approval to dispatch **Crew LL-04** to establish physical perimeter safety and assess conductor tension/energization state at Main St.
2. **First Responder Coordination**: Maintain automated dispatch link with local emergency services (Fire/Police) to hold traffic control on Main St until Crew LL-04 establishes on-scene isolation.
3. **Standby Designation**: Place **Crew LL-02** on secondary standby in the OMS/DMS queue should bucket truck positioning or structural rigging require multi-crew execution.
4. **Upstream Protection Check**: Verify upstream recloser/sectionalizer telemetry on Feeder MS-12 to ensure auto-reclosing is locked out prior to physical contact.

---

### [TIER 2 ACTION REQUIRED]
```yaml
Operation: FIELD_CREW_EMERGENCY_DISPATCH
Incident_Type: ENERGIZED_WIRE_DOWN
Incident_Location: Main St (Feeder MS-12 / Substation 4)
Target_Crew_ID: CREW-LL-04
Crew_Lead: J. Vance
Qualifications_Verified: Live-Line Barehand (IEEE 516 compliant)
Current_Location: Sector 4 North (2.4 miles away)
Estimated_Arrival_Time: 8 minutes
Action_Requested: Roll emergency bucket truck and authorize high-priority transit.
Operator_Authorization_Required: TRUE
```

### Example 2: Trend & Comparative Analysis
**User:** "Analyze real-time GPS locations, drive times, and remaining allowable crew shift hours under federal rest regulations."

**Agent Response:**
### 1. Executive Summary
**Real-time GPS telemetry and telematics analysis across 5 active field units indicates that 2 crews (CREW-E401 and CREW-C512) are approaching mandatory Federal Motor Carrier Safety Administration (FMCSA § 395.1 / OSHA) 14-hour on-duty thresholds with under 1.5 hours of allowable work remaining.** **Average transit time across priority feeder outage tickets is currently 26.6 minutes, with severe route congestion affecting Sector-C.** **Immediate relief dispatch and dynamic rerouting are required to prevent regulatory rest violations while safeguarding target Estimated Time to Restoration (ETR) and minimizing customer SAIDI impact.**

---

### 2. Data Presentation: Crew Telematics & Federal Rest Compliance

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Average Transit Time** | 26.6 min | $\le$ 20.0 min | +33.0% | **Warning** |
| **Max Shift Utilization (Crew E401 / C512)** | 13.0 hrs elapsed | $\le$ 11.0 hrs (nominal) | +18.2% | **Critical** |
| **Fleet Minimum Remaining Duty Window** | 1.0 hr | $\ge$ 4.0 hrs buffer | -75.0% | **Critical** |
| **Mandatory 10-Hr Rest Compliance Rate** | 100% | 100% (Mandate) | 0.0% | **Normal** |
| **Feeder Incident Coverage Ratio** | 80% (4/5 target nodes) | 100% | -20.0% | **Warning** |
| **Predicted SAIDI Impact (ETR Delay)** | +1.85 min/customer | $\le$ 0.50 min/customer | +270.0% | **Critical** |

#### Real-Time Crew Status & Routing Matrix
| Crew ID | Grid Zone / Feeder ID | GPS Coord (Lat, Lon) | Est. Drive Time | Shift Elapsed | Allowable Remaining | Compliance Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CREW-E401** | Zone East (F-104) | 39.7589, -104.9812 | 18 min | 12.5 hrs | 1.5 hrs | **Critical (Near Timeout)** |
| **CREW-N202** | Zone North (F-302) | 39.8102, -105.0124 | 24 min | 10.2 hrs | 3.8 hrs | **Warning** |
| **CREW-S108** | Zone South (F-019) | 39.6890, -104.9450 | 32 min | 6.0 hrs | 8.0 hrs | **Normal** |
| **CREW-W305** | Zone West (F-221) | 39.7420, -105.1055 | 14 min | 4.5 hrs | 9.5 hrs | **Normal** |
| **CREW-C512** | Zone Central (F-508) | 39.7392, -104.9903 | 45 min | 13.0 hrs | 1.0 hr | **Critical (Imminent Rest Mandate)** |

---

### 3. Visualization Triggers
- **Recommended Chart**: Shift Duty Utilization vs. Allowable Remaining Window (Bar Chart).
- **Telemetry Breakdown JSON**:
```json
[
  {"crew_id": "CREW-E401", "drive_time_min": 18, "shift_elapsed_hrs": 12.5, "remaining_duty_hrs": 1.5, "status": "Critical"},
  {"crew_id": "CREW-N202", "drive_time_min": 24, "shift_elapsed_hrs": 10.2, "remaining_duty_hrs": 3.8, "status": "Warning"},
  {"crew_id": "CREW-S108", "drive_time_min": 32, "shift_elapsed_hrs": 6.0, "remaining_duty_hrs": 8.0, "status": "Normal"},
  {"crew_id": "CREW-W305", "drive_time_min": 14, "shift_elapsed_hrs": 4.5, "remaining_duty_hrs": 9.5, "status": "Normal"},
  {"crew_id": "CREW-C512", "drive_time_min": 45, "shift_elapsed_hrs": 13.0, "remaining_duty_hrs": 1.0, "status": "Critical"}
]
```

---

### 4. Actionable Recommendations
- **Reroute & Relief Staging**: Immediately reassign target Feeder `F-508` from `CREW-C512` to incoming fresh relief unit `CREW-W305` (drive time: 14 min) to prevent on-site duty timeouts during hot-line repair work.
- **Enforce Mandatory Rest Cycles**: Order `CREW-C512` and `CREW-E401` back to their primary base operating yards for mandatory 10-hour consecutive rest reset prior to the start of the next operational operational period.
- **GPS Path Optimization**: Re-calculate GIS turn-by-turn routing for `CREW-S108` via Arterial Corridor South to bypass local traffic congestion and shave 11 minutes off current estimated transit.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CREW_DISPATCH_AND_RELIEF_SWAP",
  "authorization_level": "HUMAN_OPERATOR_REQUIRED",
  "affected_units": [
    {
      "crew_id": "CREW-C512",
      "action": "STAND_DOWN_AND_BASE_RETURN",
      "reason": "FMCSA 14-Hour Duty Limit Expiration (1.0 hr remaining)",
      "target_base": "Yard-Central"
    },
    {
      "crew_id": "CREW-W305",
      "action": "REASSIGN_INCIDENT",
      "target_incident": "INC-F508-LOCKOUT",
      "estimated_eta_min": 14
    }
  ],
  "regulatory_impact": "Prevents FMCSA Part 395 and OSHA safety rest non-compliance penalties.",
  "expected_etr_delta": "-31 minutes restoration improvement on Feeder F-508"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch Crew Unit 14 to isolate the arcing primary conductor at 5th & Elm and secure the public hazard perimeter."

**Agent Response:**
### Executive Summary
**Emergency routing assessment has prepared the dispatch order for Crew Unit 14 to respond to an active arcing primary conductor hazard at 5th & Elm. Physical field crew dispatch constitutes a Tier 2 physical operation requiring mandatory Human-In-The-Loop (HITL) authorization prior to rolling units. Isolation protocols and public safety perimeter management plans are queued pending operator confirmation.**

---

### Incident & Dispatch Operational Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Hazard Severity Level** | Arcing Primary / Live Downed Conductor | Zero Hazards | N/A | **Critical** |
| **Estimated Travel Time (ETA)** | 11 mins (Crew Unit 14) | < 15 mins (Emergency ETR target) | -26.7% | **Normal** |
| **Public Perimeter Safety Radius** | 30 ft (Minimum initial clearance) | ≥ 30 ft (OSHA / IEEE 516 standard) | 0.0% | **Warning** |
| **Downstream Affected Customers** | 412 Customers | 0 (Normal state) | +100.0% | **Critical** |
| **Projected SAIDI Impact** | 0.048 mins | < 0.020 mins / event | +140.0% | **Warning** |

---

### Visualization Trigger
```json
{
  "chart_type": "bar",
  "data_json": {
    "categories": ["Crew Unit 14 (Assigned)", "Crew Unit 08", "Crew Unit 22"],
    "series": [
      {
        "name": "ETA (Minutes)",
        "data": [11, 19, 27]
      },
      {
        "name": "Distance (Miles)",
        "data": [3.4, 6.8, 9.5]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Authorize Field Crew Rollout**: Execute the HITL confirmation payload to transmit route guidance and turn-by-turn navigation directly to Crew Unit 14 Mobile Data Terminal (MDT).
- **Coordinate First Responders**: Notify local municipal 911 dispatch / Fire Department to establish a physical cordon at 5th & Elm pending Crew Unit 14 arrival.
- **SCADA Upstream Recloser Check**: Prepare switching order in DMS/OMS to de-energize or isolate lateral fuse/recloser upstream of 5th & Elm if telemetry confirms sustained arcing fault.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CREW_DISPATCH_ROLLOUT",
  "hazard_type": "ARCING_PRIMARY_CONDUCTOR",
  "target_location": "5th & Elm",
  "assigned_crew": "Crew Unit 14",
  "crew_qualifications": ["High Voltage Certified", "Live-Line Qualified"],
  "estimated_arrival_minutes": 11,
  "required_actions": [
    "Secure minimum 30-foot public hazard perimeter",
    "Perform visual line inspection and field switching/isolation",
    "Ground and tag out isolated section prior to conductor repair"
  ],
  "hitl_approval_status": "PENDING_OPERATOR_CONFIRMATION"
}
```
