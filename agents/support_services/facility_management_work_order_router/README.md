# ⚡ Facility Management Work Order Router

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of facility management work order router is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Facility Management Work Order Router Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank facility management work order router events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.facility_management_work_order_router_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which building maintenance work orders for emergency HVAC failures in the primary grid control center are currently unassigned?"

**Agent Response:**
### 1. Executive Summary
**A telemetry and work order audit of the Primary Grid Control Center (PGCC) identifies two unassigned emergency HVAC failure work orders requiring immediate dispatch.** **Due to the mission-critical status of the control room environment and server racks, unassigned thermal regulation tickets present an operational risk to grid reliability and operator safety.** **Immediate Human-In-The-Loop (HITL) authorization is required to route these priority work orders to on-call certified critical-facility HVAC technicians.**

---

### 2. Data Presentation

#### Facility Performance & Queue Status
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Unassigned Emergency HVAC Work Orders** | 2 Tickets | 0 Tickets | +100.0% | **Critical** |
| **Control Room Ambient Temperature** | 76.8 °F | 68.0 - 72.0 °F | +6.7% | **Warning** |
| **Server Room CRAC Unit 1 & 3 Redundancy** | N+0 (Degraded) | N+1 (Redundant) | -100.0% | **Critical** |
| **Emergency Dispatch Lead Time** | 38 min (Queue) | < 15 min | +153.3% | **Critical** |

#### Unassigned Emergency HVAC Work Orders Detail
| Work Order ID | Facility / Location | Asset Tag / Equipment | Issue Description | Priority | Assignment Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **WO-FAC-2024-8841** | Primary Grid Control Center (Zone 1 - Server Pod B) | CRAC-02 (Downflow Chilled Water) | Dual compressor lockout / High head pressure alarm | **Emergency (P1)** | **Unassigned** |
| **WO-FAC-2024-8845** | Primary Grid Control Center (Main Dispatch Floor) | AHU-01 (Variable Air Volume) | Supply blower motor shaft failure / zero airflow | **Emergency (P1)** | **Unassigned** |

---

### 3. Visualization Triggers
**Recommended Visualization:** Horizontal Bar Chart tracking active facility maintenance ticket counts by urgency and assignment state across grid control facilities.

```json
{
  "chart_type": "bar",
  "title": "Primary Grid Control Center - Work Order Distribution by Priority",
  "categories": [
    "HVAC Emergency (Unassigned)",
    "HVAC Priority (Assigned)",
    "Electrical Backup (Assigned)",
    "General Facility Maintenance (Queued)"
  ],
  "series": [
    {
      "name": "Work Order Count",
      "data": [2, 4, 3, 5]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Immediate Routing:** Direct dispatch of `WO-FAC-2024-8841` to Tier-1 Critical Facility Thermal Contractor (Vendor ID: `VEND-HVAC-CRIT-01`).
- **Secondary Crew Dispatch:** Route `WO-FAC-2024-8845` to Internal Support Services Mechanical Crew Lead (Unit #4).
- **Environmental Safeguard:** Activate auxiliary spot-coolers in PGCC Server Pod B if ambient temperatures breach 78.0 °F prior to contractor arrival.
- **CIP/FERC Compliance Audit:** Log incident ticket in Support Services Compliance Register per NERC CIP-005/006 physical security and environmental mandates.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_CREW_DISPATCH",
  "facility_id": "PGCC-MAIN-01",
  "target_work_orders": [
    "WO-FAC-2024-8841",
    "WO-FAC-2024-8845"
  ],
  "dispatch_targets": [
    {
      "crew_type": "External Specialized HVAC Contractor",
      "vendor_contract_id": "VEND-HVAC-CRIT-01",
      "assigned_order": "WO-FAC-2024-8841",
      "priority": "P1_EMERGENCY"
    },
    {
      "crew_type": "Internal Facilities Mechanical Crew",
      "crew_id": "CREW-FAC-MECH-04",
      "assigned_order": "WO-FAC-2024-8845",
      "priority": "P1_EMERGENCY"
    }
  ],
  "estimated_response_time": "30 minutes",
  "requires_hitl_approval": true
}
```
*Awaiting human operator sign-off to execute physical crew dispatch and notify site building security for high-security control room access.*

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate contractor response times and service level agreements (SLAs) for critical utility administrative and warehouse facilities."

**Agent Response:**
### Executive Summary
**Contractor response times across critical administrative facilities currently maintain strong overall SLA compliance at 95.8%, driven by prioritized dispatch protocols for Control Center and Data Center environmental systems.** **However, warehouse and logistics facility maintenance—specifically Fire/Life Safety and Plumbing/Mechanical trades—exhibits noticeable SLA slippage (84.6% to 88.0% compliance) due to extended off-peak transit times and parts staging delays.** **Remediation requires dynamic routing adjustments, automated pre-authorization for critical spare dispatches, and contractual penalty enforcement for persistent vendor latency.**

---

### Data Presentation: Contractor Performance & SLA Evaluation

The following table evaluates contractor response times, SLA adherence, and resolution metrics across critical utility administrative headquarters, regional operations centers, and central material warehouses:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **P1 Critical Environmental (Control Center / Data Hub)** | 0.85 hrs | 1.00 hr | -15.0% | **Normal** |
| **P1 Emergency Generator & ATS Maintenance** | 0.90 hrs | 1.00 hr | -10.0% | **Normal** |
| **P1 Admin HQ HVAC & Critical Cooling** | 1.40 hrs | 2.00 hrs | -30.0% | **Normal** |
| **P1 Warehouse Fire Suppression & Life Safety** | 1.10 hrs | 1.00 hr | +10.0% | **Warning** |
| **P2 Warehouse Electrical Distribution & Crane Power** | 4.20 hrs | 4.00 hrs | +5.0% | **Warning** |
| **P2 General Building Plumbing & Utility Support** | 5.10 hrs | 4.00 hrs | +27.5% | **Critical** |
| **Aggregate Facility SLA Compliance Rate** | 92.9% | 98.0% | -5.2% | **Warning** |
| **Overall Mean Time to Resolution (MTTR)** | 6.4 hrs | 6.0 hrs | +6.7% | **Warning** |
| **First-Time Fix Rate (FTFR) - Critical Facilities** | 91.2% | 90.0% | +1.3% | **Normal** |

---

### Visualizer Telemetry Trigger

```json
{
  "chart_type": "bar",
  "title": "Contractor Response Time vs SLA Target by Facility & Trade",
  "categories": [
    "HVAC - Admin HQ (P1)",
    "Emergency Power - Control Ctr (P1)",
    "Fire/Life Safety - Central Warehouse (P1)",
    "Electrical - Logistics Depot (P2)",
    "Critical Cooling - Data Ctr / Sub Ctr (P1)",
    "Plumbing / Utilities - Admin Hub (P2)"
  ],
  "series": [
    {
      "name": "Actual Avg Response Time (Hrs)",
      "data": [1.4, 0.9, 1.1, 4.2, 0.8, 5.1]
    },
    {
      "name": "SLA Target Response Time (Hrs)",
      "data": [2.0, 1.0, 1.0, 4.0, 1.0, 4.0]
    },
    {
      "name": "SLA Compliance (%)",
      "data": [96.2, 98.5, 88.0, 91.4, 99.1, 84.6]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Dynamic Re-Routing for Warehouse Work Orders**: Reconfigure automated work order dispatch rules to route secondary contractor providers when primary vendors exceed 75% of their allowable SLA response window.
2. **On-Site Spare Parts Consignment**: Implement dedicated on-premise safety stock for critical warehouse switchgear components and plumbing repair kits to reduce Mean Time to Resolution (MTTR).
3. **Vendor SLA Review & Liquidated Damages**: Trigger formal contract reviews for low-compliance mechanical and plumbing contractors operating under 90% SLA adherence across utility administrative facilities.
4. **Geofenced Automated Arrival Verification**: Integrate GPS and contractor portal check-ins to eliminate manual time logging discrepancies and obtain accurate gate-to-job response tracking.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch an urgent HVAC repair contract team to Data Center Room B to resolve cooling chiller redundancy loss."

**Agent Response:**
### Executive Summary
**A critical loss of HVAC cooling chiller redundancy (N+1 compromised to N-0) has been identified in Data Center Room B, presenting an imminent thermal escalation risk to enterprise grid-control computing infrastructure. Automatic priority routing has prepared an urgent emergency work order (WO-DC-2023-8891) for designated mechanical contractor dispatch. In accordance with safety guardrails, physical crew dispatch constitutes a Tier 2 action and requires human-in-the-loop (HITL) authorization prior to deployment.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Active Chiller Redundancy** | N-0 (1/2 Online) | N+1 (2/2 Online) | -50.0% | **Critical** |
| **Room B Ambient Temperature** | 24.8 °C | 21.0 °C | +18.1% | **Warning** |
| **Thermal Headroom to Trip** | 3.2 °C | > 7.0 °C | -54.3% | **Critical** |
| **Contractor Response SLA** | 60 min (Pending Dispatch) | < 120 min | 0.0% | **Normal** |
| **Estimated Time to Restoration (ETR)**| 180 min | 120 min | +50.0% | **Warning** |

---

### Visualization Trigger

* **Recommended Visualization**: Time-Series Line Chart (Ambient Temperature vs. Operating Chiller Capacity).
* **Telemetry Data Payload**:
```json
{
  "chart_type": "line",
  "title": "Data Center Room B - Chiller Redundancy & Thermal Trend",
  "categories": ["10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30"],
  "series": [
    {
      "name": "Room B Temperature (°C)",
      "data": [21.0, 21.2, 21.8, 22.5, 23.4, 24.1, 24.8]
    },
    {
      "name": "Operating Chiller Capacity (%)",
      "data": [100, 100, 100, 50, 50, 50, 50]
    }
  ]
}
```

---

### Actionable Recommendations

* **Authorize Tier 2 Dispatch**: Review and approve the dispatch of the on-call master mechanical contractor team to initiate physical repair on Chiller Unit 2.
* **Activate Auxiliary Spot Cooling**: Direct on-site facility personnel to stage portable CRAC/spot-cooling units adjacent to critical server racks to arrest thermal rise.
* **Monitor Load Shedding Triggers**: Inform IT/Grid Operations if Room B exceeds 26.5 °C to prepare non-critical workload migration.
* **Escalate Contract Performance**: Log vendor arrival timestamps against the Master Service Agreement (MSA) SLA to enforce performance credits if response exceeds 60 minutes.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PHYSICAL_CREW_DISPATCH",
  "work_order_id": "WO-DC-2023-8891",
  "asset_id": "HVAC-CHILLER-ROOM-B-02",
  "facility_location": "Enterprise Primary Data Center - Room B",
  "assigned_vendor": "Carrier Commercial Service Response Team",
  "priority": "P1_URGENT",
  "scope_of_work": "Emergency diagnostics and repair of compressor failure on Chiller Unit 2 to restore N+1 cooling redundancy.",
  "estimated_cost_limit": "$5,000.00 USD (Emergency SLA Tier)",
  "safety_and_compliance": "NERC CIP-005 / CIP-007 Physical Security Escort Required for Data Center Access",
  "requires_approval": true,
  "approval_status": "PENDING_OPERATOR_CONFIRMATION"
}
```

*Please confirm approval to transmit this dispatch instruction to the contractor response network.*
