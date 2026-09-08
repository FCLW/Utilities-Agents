# ⚡ Utility Vehicle Fleet Maintenance Tracker

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of utility vehicle fleet maintenance tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Utility Vehicle Fleet Maintenance Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank utility vehicle fleet maintenance tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.utility_vehicle_fleet_maintenance_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which heavy-duty bucket trucks and boom lift vehicles have overdue dielectric boom testing or hydraulic fluid maintenance?"

**Agent Response:**
### Executive Summary
**Fleet Telemetry and Maintenance Compliance records identify multiple heavy-duty bucket trucks and boom lift vehicles operating with overdue dielectric boom insulation certifications (per OSHA 1910.269/ANSI A92.2) and critical hydraulic fluid servicing intervals. Uncertified dielectric insulation presents an immediate personnel safety hazard during live-line work, while degraded hydraulic fluids risk catastrophic boom control failures. Immediate fleet grounding and work-order prioritization are required to clear regulatory non-compliance and maintain operational safety.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Overdue Dielectric Testing (Fleet Count)** | 4 Units | 0 Units (100% On-Time) | +100.0% | **Critical** |
| **Overdue Hydraulic Fluid Service (Fleet Count)** | 4 Units | 0 Units (100% On-Time) | +100.0% | **Critical** |
| **Average Asset Health Index (AHI) - Overdue Units** | 61.4 / 100 | ≥ 85.0 / 100 | -27.8% | **Critical** |
| **Max Days Overdue (Dielectric Test)** | 45 Days | 0 Days | +100.0% | **Critical** |
| **Max Days Overdue (Hydraulic Service)** | 62 Days | 0 Days | +100.0% | **Critical** |

#### Overdue Vehicle Breakdown & Maintenance Schedule Status

| Vehicle ID | Unit Type | Make / Model | Grid Zone | Last Dielectric Test | Dielectric Status | Hydraulic Service Status | AHI Score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **BT-4012** | Heavy-Duty Bucket Truck | International 7400 / Altec TA60 | Zone-North | 13.5 mos ago | **Overdue (+45 Days)** | **Overdue (+15 Days)** | 54.2 (Critical) |
| **BT-4088** | Heavy-Duty Bucket Truck | Freightliner M2 / Terex Optima 55 | Zone-East | 12.6 mos ago | **Overdue (+18 Days)** | **Overdue (+28 Days)** | 62.0 (Warning) |
| **BT-4105** | Heavy-Duty Bucket Truck | Ford F-750 / Altec AA55E | Zone-West | 13.1 mos ago | **Overdue (+32 Days)** | Current (Due in 45 Days) | 68.5 (Warning) |
| **BL-2204** | Boom Lift Vehicle | Kenworth T370 / Bronto Skylift | Zone-Metro | Current (Due in 90 Days) | Current | **Overdue (+62 Days)** | 58.7 (Critical) |
| **BL-2219** | Boom Lift Vehicle | Freightliner M2 / Altec AT40 | Zone-South | 12.4 mos ago | **Overdue (+12 Days)** | **Overdue (+41 Days)** | 63.8 (Warning) |

---

### Visualization Triggers
- **Recommended Visualization**: **Stacked Bar Chart** displaying days past due categorized by maintenance type (Dielectric Boom Testing vs. Hydraulic Fluid Replacement) per vehicle asset.

```json
{
  "chart_type": "bar",
  "title": "Fleet Vehicles Overdue Maintenance Summary",
  "categories": [
    "BT-4012 (HD Bucket)",
    "BT-4088 (HD Bucket)",
    "BL-2204 (Boom Lift)",
    "BT-4105 (HD Bucket)",
    "BL-2219 (Boom Lift)"
  ],
  "series": [
    {
      "name": "Days Overdue - Dielectric Boom Test",
      "data": [45, 18, 0, 32, 12]
    },
    {
      "name": "Days Overdue - Hydraulic Fluid Service",
      "data": [15, 28, 62, 0, 41]
    }
  ]
}
```

---

### Actionable Recommendations
- **Immediate Lockout/Tagout (LOTO)**: Enforce dispatch lockout on units `BT-4012`, `BT-4088`, `BT-4105`, `BL-2204`, and `BL-2219` to prevent field deployment on energized high-voltage line work until certification is restored.
- **Expedite High-Voltage Dielectric Testing**: Schedule certified mobile laboratory dielectric testing for bucket trucks `BT-4012`, `BT-4105`, `BT-4088`, and `BL-2219` to comply with ANSI/SIA A92.2 annual dielectric requirements.
- **Hydraulic System Fluid Sampling & Flush**: Execute full hydraulic fluid drain, filter replacement, and particulate/moisture analysis for units `BL-2204`, `BL-2219`, `BT-4088`, and `BT-4012`.
- **Fleet Relief Reassignment**: Coordinate with Dispatch Operations to reassign compliant reserve utility bucket trucks to high-priority feeders across `Zone-North` and `Zone-Metro`.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "FLEET_DISPATCH_LOCKOUT"
  target_assets:
    - "BT-4012"
    - "BT-4088"
    - "BT-4105"
    - "BL-2204"
    - "BL-2219"
  reason: "Non-compliant dielectric boom insulation certifications and critical overdue hydraulic maintenance."
  safety_impact: "High risk of electrical arc flashover and hydraulic failure during live-line crew operations."
  approval_required_by: "Fleet Operations Safety Director / Maintenance Supervisor"
  status: "PENDING_HUMAN_CONFIRMATION"
```

### Example 2: Trend & Comparative Analysis
**User:** "Track fleet fuel consumption, engine idle hours, and scheduled preventive maintenance intervals across 450 service vehicles."

**Agent Response:**
### Executive Summary
**Fleet telemetry analysis across all 450 utility service vehicles indicates an aggregate fleet fuel efficiency of 11.8 MPG against a baseline of 13.2 MPG (-10.6%), driven primarily by elevated engine idle time averaging 35.4% of total runtime. A total of 26 vehicles (5.8%) currently exceed scheduled Preventive Maintenance (PM) thresholds, with Heavy Bucket Trucks and Digger Derricks representing the highest mechanical risk profile. Implementing automated idle-shutdown policies and batching overdue PM work orders will recover an estimated 8,400 gallons of fuel monthly and mitigate premature engine wear.**

---

### Fleet Telemetry & Maintenance Key Performance Indicators

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Active Fleet Assets** | 450 Units | 450 Units | 0.0% | Normal |
| **Fleet Average Fuel Economy** | 11.8 MPG | 13.2 MPG | -10.6% | Warning |
| **Aggregate Engine Idle Time** | 35.4% | < 20.0% | +77.0% | Critical |
| **PM Compliance Rate** | 88.2% | ≥ 95.0% | -7.2% | Warning |
| **Overdue PM Vehicles** | 26 Units | 0 Units | N/A | Critical |
| **Upcoming PM Due (< 500 mi / 20 hrs)** | 48 Units | — | — | Warning |
| **Mean Asset Health Index (AHI)** | 84.6 / 100 | ≥ 85.0 / 100 | -0.5% | Normal |

---

### Vehicle Class Breakdown

| Vehicle Class | Total Units | Avg Fuel Economy (MPG) | Idle Time (%) | Overdue PM Units | Due Soon (< 500 mi) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Bucket Trucks (Heavy-Duty)** | 140 | 6.4 MPG | 42.1% | 12 | 18 |
| **Digger Derricks** | 70 | 5.8 MPG | 48.6% | 8 | 9 |
| **Troubleshooter Pickups** | 110 | 17.1 MPG | 34.0% | 4 | 11 |
| **Service Vans (Light-Duty)** | 80 | 14.2 MPG | 28.3% | 2 | 7 |
| **Supervisory SUVs / Light Fleet** | 50 | 21.5 MPG | 19.5% | 0 | 3 |

---

### Fleet Telemetry & Maintenance Visualization

```json
{
  "chart_type": "bar",
  "title": "Fleet Operational Metrics by Vehicle Classification",
  "categories": [
    "Bucket Trucks (Heavy)",
    "Digger Derricks",
    "Service Vans (Light)",
    "Troubleshooter Pickups",
    "Supervisory SUVs"
  ],
  "series": [
    {
      "name": "Avg Fuel Economy (MPG)",
      "data": [6.4, 5.8, 14.2, 17.1, 21.5]
    },
    {
      "name": "Engine Idle Time (%)",
      "data": [42.1, 48.6, 28.3, 34.0, 19.5]
    },
    {
      "name": "Overdue PM Ratio (%)",
      "data": [8.6, 11.4, 2.5, 3.6, 0.0]
    }
  ],
  "unit": "Percentage / MPG"
}
```

---

### Actionable Recommendations

- **Prioritize Overdue PM Scheduling**: Immediately route the 20 heavy-duty assets (12 Bucket Trucks, 8 Digger Derricks) exceeding engine-hour PM thresholds to regional fleet maintenance bays to prevent PTO hydraulic and valvetrain degradation.
- **Enforce Engine Idle-Reduction Protocol**: Deploy automated auxiliary battery power units (e-PTO / ePTO hybrid systems) for aerial boom operation on heavy bucket trucks to eliminate continuous diesel engine idling during stationary line work.
- **Implement Tiered Telematics Geofence Alerts**: Configure telematics alerts to notify regional operations supervisors when vehicle idling exceeds 15 continuous minutes outside active emergency/storm response modes.
- **Standardize Engine Hour Maintenance Scheduling**: Transition heavy-duty aerial units from odometer-based PM tracking to telematics-derived engine run-hour and PTO-hour intervals to ensure accurate wear-cycle service.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Ground Bucket Truck #BK-412 immediately due to failed annual dielectric insulation testing and schedule shop servicing."

**Agent Response:**
### Executive Summary
**Bucket Truck #BK-412 has been placed into immediate Out-of-Service (OOS) status following a critical failure during annual dielectric insulation testing per ANSI/SIA A92.2 and OSHA 1910.269 standards.** **Telemetry and bench test records indicate elevated microampere leakage and compromised dielectric breakdown thresholds across the upper boom fiberglass insert and bucket liner.** **Immediate lockout/tagout (LOTO) protocols are initiated to prevent field deployment, and emergency priority bay scheduling is flagged for Central Fleet Maintenance.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Upper Boom Leakage Current (46 kV AC)** | 182.0 µA | ≤ 40.0 µA | +355.0% | **Critical** |
| **Lower Boom Insert Leakage (46 kV AC)** | 95.0 µA | ≤ 50.0 µA | +90.0% | **Critical** |
| **Bucket Liner Dielectric Integrity** | 140.0 µA (Pinhole Breach) | ≤ 50.0 µA | +180.0% | **Critical** |
| **Hydraulic Fluid Dielectric Breakdown** | 21.0 kV | ≥ 28.0 kV | -25.0% | **Warning** |
| **Asset Health Index (AHI)** | 28 / 100 | ≥ 85 / 100 | -67.1% | **Critical** |
| **Remaining Useful Life (RUL - Boom Assembly)** | 0.0 Operating Hours | N/A | -100.0% | **Critical** |

---

### Visualization Triggers
- **Recommended Visualization**: Grouped Bar Chart comparing measured leakage currents against standard ANSI/SIA A92.2 maximum allowable thresholds across boom components and bucket liners.

```json
{
  "chart_type": "bar",
  "title": "Bucket Truck #BK-412 Dielectric Breakdown & Leakage Current vs Standard",
  "categories": [
    "Upper Boom (AC 46kV)",
    "Lower Boom Insert",
    "Liner Integrity",
    "Hydraulic Fluid Dielectric"
  ],
  "series": [
    {"name": "Measured Leakage (µA)", "data": [182, 95, 140, 28]},
    {"name": "ANSI A92.2 Limit (µA)", "data": [40, 50, 50, 15]}
  ]
}
```

---

### Actionable Recommendations
- **Immediate LOTO Dispatch**: Apply physical Lockout/Tagout tags to the ignition and boom control console of `#BK-412` at the staging yard; quarantine vehicle keys in the Central Dispatch lockbox.
- **Shop Bay Routing**: Route `#BK-412` to Central Fleet Shop Bay 3 for detailed ultrasonic NDT (Non-Destructive Testing), boom interior cleaning/moisture bake-out, and bucket liner replacement.
- **Hydraulic Fluid Replacement**: Flush and replace non-conductive dielectric hydraulic fluid (ISO VG 15/22 dielectric oil) to restore breakdown strength above 30 kV.
- **Fleet Allocation Replacement**: Reassign Line Crew 12 to reserve unit `#BK-388` (certified compliant through Q3) to maintain scheduled distribution feeder maintenance.
- **Re-Certification Testing**: Mandate full-cycle high-potential (Hi-Pot) re-testing per ANSI/SIA A92.2-2021 prior to releasing the vehicle back to active duty.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FLEET_ASSET_GROUNDING_AND_WORK_ORDER",
  "vehicle_id": "BK-412",
  "vin_last_6": "774912",
  "current_status": "OUT_OF_SERVICE_GROUNDED",
  "severity": "CRITICAL_SAFETY_VIOLATION",
  "compliance_standard": "ANSI/SIA A92.2 / OSHA 1910.269",
  "work_order_details": {
    "shop_facility": "Central Fleet Maintenance Shop",
    "assigned_bay": "Bay 3 - Aerial Equipment Specialization",
    "priority": "P1_EMERGENCY",
    "required_tasks": [
      "Physical Lockout/Tagout verification",
      "Fiberglass boom section ultrasonic and high-voltage re-test",
      "Dielectric bucket liner replacement",
      "Dielectric hydraulic oil drain, flush, and refill",
      "Full ANSI A92.2 dielectric re-certification"
    ]
  },
  "substitute_asset_id": "BK-388",
  "approvals_required": [
    "Fleet Operations Superintendent",
    "Safety & Compliance Manager"
  ]
}
```
