# ⚡ Mutual Assistance Resource Allocator

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of mutual assistance resource allocator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Mutual Assistance Resource Allocator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank mutual assistance resource allocator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.mutual_assistance_resource_allocator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many external mutual assistance line contractor crews should we request through the Regional Mutual Assistance Group (RMAG)?"

**Agent Response:**
### Executive Summary
**Based on current grid damage modeling, outage density, and target Estimated Time to Restoration (ETR) of 72 hours, an operational deficit of 108 crews exists against native resource capacity. It is recommended to formally request 125 external mutual assistance line contractor crews (approximately 500 FTE lineworkers) through the Regional Mutual Assistance Group (RMAG), supplemented by 20 vegetation management crews and 10 safety/damage assessment leads. This allocation accounts for travel transit times, staging operational buffers, and structural rebuild complexity.**

---

### Quantitative Resource Sizing & Capacity Evaluation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Estimated Restoration Work-Hours** | 182,400 hrs | 62,400 hrs | +192.3% | **Critical** |
| **Native Internal Line Crews Available** | 85 crews | 85 crews | 0.0% | **Normal** |
| **Retained Native Contractor Line Crews** | 45 crews | 45 crews | 0.0% | **Normal** |
| **Total Native Crew Capacity** | 130 crews | 238 crews | -45.4% | **Critical** |
| **Net Operational Crew Deficit** | 108 crews | 0 crews | N/A | **Critical** |
| **Recommended RMAG Request (Incl. +15% Buffer)** | **125 crews** | **0 crews** | **N/A** | **Warning** |
| **Target ETR Completion Window** | 72.0 hrs | 72.0 hrs | 0.0% | **Normal** |
| **Vegetation Management / Tree Trimming Crews Required** | 20 crews | 8 crews | +150.0% | **Warning** |

---

### Visualization Recommendation

A **Grouped Bar / Ramp-Up Waterfall Chart** is recommended to visualize native vs. mutual assistance mobilization against the required restoration resource curve.

```json
{
  "chart_type": "bar",
  "title": "Mutual Assistance Crew Requirement & Mobilization Capacity",
  "xAxis": {
    "categories": [
      "Internal Utility Crews",
      "Native Retained Contractors",
      "Total Native Availability",
      "RMAG Mutual Assistance Request",
      "Total Mobilized Capacity",
      "Target Operational Requirement"
    ]
  },
  "yAxis": {
    "title": "Number of Line Crews (4-Person FTE Equivalent)"
  },
  "series": [
    {
      "name": "Allocated Line Crews",
      "data": [85, 45, 130, 125, 255, 238]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Submit RMAG Sourcing Request**: Transmit the formal requisition for **125 distribution line crews (4-person units)**, **20 bucket-equipped tree/vegetation crews**, and **10 safety assessors** through the designated RMAG portal.
2. **Activate Regional Staging Sites**: Open Primary Staging Base (Central Fairgrounds/Logistics Yard) to support crew onboarding, fuel bunkering, vehicle inspection, and automated field dispatch integration.
3. **Establish Flight Coordination & Material Kitting**: Pre-stage 45-foot Class 2 poles, distribution crossarms, 1/0 and 4/0 ACSR conductors, and 25kVA/50kVA overhead transformers matching the requested crew throughput.
4. **Onboarding & Safety Sync**: Enforce RMAG crew credentialing, distribution system safety rules (lockout/tagout, grounding requirements), and digital work packet assignment in the Mobile Outage Management System (OMS/ADMS).

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "RMAG_RESOURCE_REQUISITION",
  "approval_level": "Human-In-The-Loop (Incident Commander / Grid Operations Director)",
  "payload": {
    "target_rmag_consortium": "Great Lakes Mutual Assistance Group (GLMAG) / SEE-MAG",
    "requested_resources": {
      "line_contractor_crews": 125,
      "crew_composition": "4-Person Line Crew with Bucket/Digger Derrick",
      "vegetation_crews": 20,
      "damage_assessors": 10
    },
    "estimated_commitment_duration_days": 4,
    "primary_staging_area_id": "STAGING-CAMP-NORTH-01",
    "financial_liability_authorization": "APPROVED_STORM_OPEX_RECOVERY",
    "execution_status": "PENDING_INCIDENT_COMMANDER_SIGN_OFF"
  }
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Track contractor staging yard logistics, hotel accommodations, and fuel supply allocations for 250 incoming utility personnel."

**Agent Response:**
### Executive Summary
**Mutual Assistance logistics mobilization for 250 incoming utility personnel has been planned and mapped across primary staging yards, regional hotel room blocks, and dedicated fuel supply chains.** **All key resource constraints—including 135 secured hotel rooms, 75 heavy-equipment staging slots, and 4,500 gallons/day mobile fueling capacity—meet or exceed baseline deployment thresholds.** **Execution of binding vendor agreements and fuel replenishment contracts requires immediate human-in-the-loop authorization to maintain zero-hour onboarding readiness.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Incoming Mutual Aid Headcount** | 250 FTE | 250 FTE | 0.0% | Normal |
| **Hotel Accommodations (Rooms Blocked)** | 135 Rooms | 125 Rooms (2:1 / Superv.) | +8.0% | Normal |
| **Staging Yard Vehicle Capacity** | 75 Bays | 70 Bays | +7.1% | Normal |
| **Daily Diesel Fuel Allocation** | 4,500 Gal/day | 4,200 Gal/day | +7.1% | Normal |
| **Daily Unleaded Fuel Allocation** | 1,200 Gal/day | 1,000 Gal/day | +20.0% | Normal |
| **Daily Catering / Meals Provision** | 750 Meals/day | 750 Meals/day | 0.0% | Normal |
| **Laydown Material Kits (Poles/Transformers)** | 60 Kits | 50 Kits | +20.0% | Normal |
| **Transit Radius (Staging Yard to Hotels)** | 18 Minutes | ≤ 30 Minutes | -40.0% | Normal |

---

### Visualization Triggers

**Recommended Visualization:** Grouped Bar Chart — *Mutual Assistance Logistics Allocation vs. Target Capacity*

```json
{
  "chart_type": "bar",
  "title": "Mutual Assistance Logistics Readiness & Resource Burn Rate (250 FTE)",
  "categories": [
    "Lodging Rooms (Nights)",
    "Daily Diesel Fuel (Gal)",
    "Daily Gasoline (Gal)",
    "Staging Yard Slots (Bays)",
    "Meal Allocations (Units/Day)",
    "Material Kits (Laydown)"
  ],
  "series": [
    {
      "name": "Secured / Allocated",
      "data": [135, 4500, 1200, 75, 750, 60]
    },
    {
      "name": "Baseline Target",
      "data": [125, 4200, 1000, 70, 750, 50]
    }
  ]
}
```

---

### Actionable Recommendations

- **Staging Yard Ingress/Egress**: Establish designated heavy equipment lanes at Staging Yard Alpha to prevent bottlenecking during morning tailboard briefings and 06:00 dispatch.
- **Mobile Wet-Hosing Protocol**: Schedule dedicated mobile fuel tank truck wet-hosing operations between 20:00 and 04:00 to ensure all bucket trucks and digger derricks are 100% fueled prior to morning shift kick-off.
- **Badging & Onboarding**: Pre-print contractor credential packets and field safety compliance manifests to minimize staging yard check-in processing to < 10 minutes per crew.
- **Material Pre-Kitting**: Stage cross-arms, conductors, transformers, and cutouts in palletized storm kits directly adjacent to crew staging lanes.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "CONTRACT_AND_FINANCIAL_COMMITMENT",
  "domain": "Grid Operations - Mutual Assistance",
  "personnel_count": 250,
  "staging_location": "Staging Yard Alpha (Zone 4)",
  "commitments_requiring_authorization": {
    "hotel_lodging_block": {
      "provider_group": "Regional Lodging Consortium (3 Properties)",
      "total_rooms": 135,
      "duration_nights": 7,
      "estimated_cost_usd": 141750.00
    },
    "fuel_delivery_contract": {
      "vendor": "FleetFuel Mobile Logistics LLC",
      "daily_volume_diesel_gal": 4500,
      "daily_volume_gasoline_gal": 1200,
      "service_type": "Overnight On-Site Wet-Hosing",
      "estimated_daily_cost_usd": 22800.00
    },
    "catering_services": {
      "daily_meals": 750,
      "estimated_daily_cost_usd": 18750.00
    }
  },
  "compliance_check": "NERC EOP-011 / IEEE Emergency Operations Standard",
  "approval_status": "PENDING_HUMAN_OPERATOR_CONFIRMATION"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit formal RMAG mutual aid mobilization request for 40 bucket trucks, 15 digger derricks, and 80 qualified linemen."

**Agent Response:**
### 1. Executive Summary
**A formal Regional Mutual Assistance Group (RMAG) mobilization request package has been generated for 80 qualified journeyman linemen, 40 aerial bucket trucks, and 15 digger derricks to support large-scale emergency grid restoration.** **Internal staging site logistics, onboarding packets, and preliminary safety alignment protocols have been matched to incoming mutual aid allocations.** **Because formal RMAG mobilization triggers binding inter-utility operational and financial commitments, final dispatch transmission requires Incident Commander (IC) / Operations Section Chief authorization.**

---

### 2. Data Presentation: Resource Mobilization Requirements

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Qualified Journeyman Linemen (JL)** | 80 FTE | 80 FTE | 0.0% | **Normal** |
| **Aerial Lift Devices (Bucket Trucks - 45'+)** | 40 Units | 40 Units | 0.0% | **Normal** |
| **Digger Derricks (Pole Setting / Heavy Class)** | 15 Units | 15 Units | 0.0% | **Normal** |
| **Internal Crew Guides ("Bird Dogs") Allocated** | 20 FTE | 20 FTE (1 per 2 crews) | 0.0% | **Normal** |
| **Dedicated Staging Site Capacity (Base Camp)** | 120 Units / 180 Beds | 95 Units / 120 Beds | +26.3% | **Normal** |
| **Fuel & Fleet Maintenance Readiness** | 100% Ready | 100% Ready | 0.0% | **Normal** |
| **RMAG Daily Burn-Rate Estimate (O&M / Capital)** | $385,000 / day | $400,000 / day threshold | -3.75% | **Normal** |

---

### 3. Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "RMAG Mutual Aid Mobilization Request Breakdown",
  "data": [
    {"resource_type": "Qualified Linemen", "quantity": 80, "baseline_required": 80, "unit": "Personnel"},
    {"resource_type": "Bucket Trucks", "quantity": 40, "baseline_required": 40, "unit": "Vehicles"},
    {"resource_type": "Digger Derricks", "quantity": 15, "baseline_required": 15, "unit": "Vehicles"},
    {"resource_type": "Internal Crew Guides (Bird Dogs)", "quantity": 20, "baseline_required": 20, "unit": "Support Personnel"},
    {"resource_type": "Safety / Field Supervisors", "quantity": 8, "baseline_required": 8, "unit": "Supervisory Personnel"}
  ]
}
```

---

### 4. Actionable Recommendations

- **Staging Base Activation**: Confirm designated Primary Staging Site (Base Camp Alpha) with materials management for pole, crossarm, wire, and transformer pre-staging.
- **Bird Dog Assignment**: Finalize pairing of internal qualified electrical workers (Crew Guides/Bird Dogs) to incoming foreign crews for distribution switching, radio comms, and system mapping orientation.
- **Safety & Protocol Inprocessing**: Pre-load foreign crew tailboard packets, switching/tagging clearance rules, IEEE/OSHA standard PPE verification, and automated time-tracking accounts.
- **Execute RMAG Transmission**: Route the Tier 2 confirmation payload to the Incident Commander for immediate release to the regional mutual assistance roster.

---

### 5. Tier 2 Operation Approval Required

```markdown
[TIER 2 ACTION REQUIRED]
--------------------------------------------------------------------------------
ACTION TYPE: RMAG Mutual Aid Formal Mobilization Request Transmission
TRANSMISSION TARGET: Regional Mutual Assistance Group (RMAG) Coordinator / Operations Roster
REQUEST DETAILS:
  - Personnel: 80 Qualified Journeyman Linemen (40 2-person crews)
  - Fleet / Equipment: 40 Bucket Trucks, 15 Digger Derricks
  - Supervisory Support: 8 Field Safety / Line Supervisors
  - Target Staging Location: Staging Base Camp Alpha (Logistics Sector 4)
  - Estimated Mobilization Window: 12–24 Hours Travel / Reporting
  - Financial Commitment Authority: Emergency Restoration O&M / FERC Acct 593
AUTHORIZATION REQUIRED: Incident Commander / Grid Operations Section Chief
STATUS: PENDING HUMAN-IN-THE-LOOP (HITL) APPROVAL
--------------------------------------------------------------------------------
```
