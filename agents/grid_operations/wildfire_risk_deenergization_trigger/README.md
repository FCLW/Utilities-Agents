# ⚡ Wildfire Risk Deenergization Trigger

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of wildfire risk deenergization trigger is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Wildfire Risk Deenergization Trigger Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank wildfire risk deenergization trigger events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.wildfire_risk_deenergization_trigger_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Do current wind gusts exceeding 55 mph and single-digit relative humidity meet the criteria for a Public Safety Power Shutoff (PSPS)?"

**Agent Response:**
### Executive Summary
**Current conditions featuring wind gusts exceeding 55 mph and single-digit relative humidity (<10%) exceed standard Public Safety Power Shutoff (PSPS) critical thresholds, placing circuits in High Fire Threat Districts (HFTD Tiers 2 and 3) into an extreme ignition risk regime. Under utility regulatory frameworks (e.g., California CPUC / NERC FAC/PRC operating standards), these environmental parameters satisfy the multi-variable threshold requirements for initiating PSPS de-energization protocols. Immediate operational escalation to the Incident Command System (ICS) and human-in-the-loop (HITL) authorization is warranted.**

---

### Data Presentation: Environmental & Threshold Evaluation

| Metric | Current Value | Baseline / Target (PSPS Trigger Threshold) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Wind Gusts** | 56.0 mph | $\ge$ 45.0 mph | +24.4% | **Critical** |
| **Sustained Wind Speed** | 38.0 mph | $\ge$ 25.0 mph | +52.0% | **Critical** |
| **Relative Humidity (RH)** | 8.0% | $\le$ 15.0% | -46.7% | **Critical** |
| **10-Hour Dead Fuel Moisture** | 5.0% | $\le$ 8.0% | -37.5% | **Critical** |
| **Fire Potential Index (FPI)** | 14.2 / 16.0 | $\ge$ 12.0 / 16.0 | +18.3% | **Critical** |
| **NWS Red Flag Warning** | Active | Active | N/A | **Critical** |

---

### Visualization Trigger
```json
{
  "chart_type": "bar",
  "title": "Observed Conditions vs. PSPS Operational Trigger Thresholds",
  "data": {
    "categories": [
      "Sustained Wind (mph)",
      "Wind Gusts (mph)",
      "Relative Humidity (%)",
      "10-Hr Fuel Moisture (%)",
      "Fire Potential Index (FPI)"
    ],
    "current_values": [38.0, 56.0, 8.0, 5.0, 14.2],
    "psps_thresholds": [25.0, 45.0, 15.0, 8.0, 12.0]
  }
}
```

---

### Actionable Recommendations

1. **Verify Circuit Topology & Sectionalization Capabilities**: Run DMS/SCADA checks to identify upstream automated reclosers/sectionalizers in High Fire Threat Districts (HFTD Tier 2/3) to minimize impacted non-threat customer footprints.
2. **Disable Automatic Reclosing**: Immediately issue commands via SCADA to suppress auto-reclosing on all distribution and transmission lines traversing the designated red flag footprint.
3. **Trigger Public & Agency PSPS Notifications**: Notify local emergency services, public safety partners, and affected medical baseline customers in accordance with standard 24/48-hour and imminent shutoff notification mandates.
4. **Prepare Patrol & Aerial Restoration Assets**: Stage field patrol crews and drone/aviation visual inspection teams at staging zones outside the red-flag boundary for rapid post-event restoration once the weather event clears.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_GRID_DEENERGIZATION_PSPS",
  "target_asset_scope": "HFTD_TIER_2_3_FEEDERS_CRITICAL_CORRIDOR",
  "trigger_justification": "Wind gusts (56 mph) and relative humidity (8%) exceed critical fire risk thresholds under active NWS Red Flag conditions.",
  "required_approvals": [
    "Grid Control Center Operations Manager",
    "Incident Commander (ICS / EOC)",
    "Chief Safety / Regulatory Officer"
  ],
  "hitl_validation_status": "PENDING_HUMAN_CONFIRMATION",
  "safety_notice": "Autonomous de-energization is prohibited. SCADA execution requires explicit operator confirmation and logging under CPUC/NERC compliance mandates."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate satellite fire weather telemetry, live fire camera imagery, and red flag warnings across High Fire Threat Districts."

**Agent Response:**
### Executive Summary
**Multi-stream correlation across High Fire Threat Districts (HFTD Tiers 2 and 3) indicates extreme environmental convergence exceeding Public Safety Power Shutoff (PSPS) de-energization thresholds on Feeders 02-15 (Cascade Pass) and 12-04 (North Sierra). Satellite thermal detections (GOES-16/18 & VIIRS) and optical fire camera AI confirm active ignition and rapid smoke plume expansion coincident with 60+ mph wind gusts, 7% relative humidity, and active National Weather Service (NWS) Red Flag Warnings. Proactive de-energization protocols must be initiated immediately for high-risk circuits to mitigate catastrophic ignition risks under NERC FAC-003 and CPUC Resolution ESRB-8 standards.**

---

### Telemetry & Risk Correlation Matrix (HFTD Circuits)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Wind Gust (HFTD Tier 3 Circuits)** | 61.5 mph | < 35.0 mph | +75.7% | **Critical** |
| **Dead Fuel Moisture (10-hr FDFM)** | 4.8% | > 10.0% | -52.0% | **Critical** |
| **Relative Humidity (RH)** | 7.2% | > 20.0% | -64.0% | **Critical** |
| **Fire Potential Index (FPI)** | 96.8 / 100 | < 70.0 / 100 | +38.3% | **Critical** |
| **Optical AI Camera Smoke Confidence** | 95.2% | < 20.0% | +376.0% | **Critical** |
| **Satellite Thermal Radiative Power (FRP)** | 68.4 MW | 0.0 MW | N/A (Active Hotspot) | **Critical** |
| **Red Flag Warning (RFW) Zone Coverage** | 100.0% | 0.0% | N/A (Active) | **Critical** |
| **Feeder 02-15 Outage Risk Index** | 98.4 / 100 | < 85.0 / 100 | +15.8% | **Critical** |
| **Feeder 12-04 Outage Risk Index** | 93.1 / 100 | < 85.0 / 100 | +9.5% | **Critical** |

---

### Multi-Modal Sensor Correlation Breakdown

```
====================================================================================================
Circuit ID     HFTD Tier   Wind/Gust    RH / FDFM   NWS Alert   Camera Smoke AI   VIIRS Hotspot (FRP)
====================================================================================================
Feeder 02-15   Tier 3      61.5 mph     7.2% / 4.8%  Red Flag    Confirmed (95%)   68.4 MW (Active)
Feeder 12-04   Tier 3      58.2 mph     8.1% / 5.1%  Red Flag    Confirmed (91%)   42.8 MW (Active)
Feeder 08-11   Tier 3      52.4 mph     9.8% / 6.0%  Red Flag    Alert (84%)       18.2 MW (Emerging)
Feeder 19-03   Tier 2      42.1 mph    14.2% / 7.8%  Red Flag    Clear (0%)         0.0 MW (No Detect)
Feeder 04-22   Tier 2      38.6 mph    16.5% / 8.5%  Red Flag    Clear (12.5%)      0.0 MW (No Detect)
====================================================================================================
```

---

### Visualization Trigger: Multi-Modal Wildfire Threat Correlation

```json
{
  "title": "HFTD Multi-Modal Wildfire Threat Correlation Matrix",
  "chart_type": "bar",
  "categories": [
    "Feeder 12-04 (HFTD Tier 3 - North Sierra)",
    "Feeder 08-11 (HFTD Tier 3 - Diablo Ridge)",
    "Feeder 04-22 (HFTD Tier 2 - Central Valley South)",
    "Feeder 19-03 (HFTD Tier 2 - Coastal Gap)",
    "Feeder 02-15 (HFTD Tier 3 - Cascade Pass)"
  ],
  "series": [
    {
      "name": "Sustained Wind / Gusts (mph)",
      "data": [58.2, 52.4, 38.6, 42.1, 61.5]
    },
    {
      "name": "Fire Potential Index (FPI / 100)",
      "data": [94.0, 88.5, 71.0, 76.2, 96.8]
    },
    {
      "name": "Camera AI Smoke Detection Conf (%)",
      "data": [91.4, 84.0, 12.5, 0.0, 95.2]
    },
    {
      "name": "Satellite Thermal Anomaly FRP (MW)",
      "data": [42.8, 18.2, 0.0, 0.0, 68.4]
    },
    {
      "name": "PSPS De-energization Trigger Threshold",
      "data": [85.0, 85.0, 85.0, 85.0, 85.0]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Execute Targeted PSPS De-energization**:
   - Issue immediate switching orders for breakers on **Feeder 02-15** and **Feeder 12-04** to eliminate potential ignition sources along high-velocity wind corridors.
2. **Recloser Suppression (One-Shot Mode)**:
   - Disable automatic reclosing (set reclosers to non-reclose/one-shot) across all adjacent HFTD Tier 2 and Tier 3 lines (including Feeders 08-11, 19-03, and 04-22) via SCADA to prevent line energization into fault conditions.
3. **Emergency Public Safety Notifications**:
   - Notify emergency management agencies (Cal OES / County OES), first responders, local fire protection districts, and critical facility accounts (water pumping, hospitals) in affected zones per standard de-energization timelines.
4. **Field Visual & Aerial Patrol Dispatch**:
   - Dispatch UAS (drone) and line patrol crews to stand by outside the active fire perimeter for post-event safety inspection and rapid restoration once weather clears below safety thresholds.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_DEENERGIZATION_TRIGGER",
  "scope": "PHYSICAL_GRID_CONTROL",
  "substations": ["Cascade Pass Substation", "North Sierra Substation"],
  "circuits": ["FEEDER-02-15", "FEEDER-12-04"],
  "target_devices": [
    {"device_id": "CB-0215-A", "action": "OPEN", "recloser_status": "SUPPRESSED"},
    {"device_id": "CB-1204-M", "action": "OPEN", "recloser_status": "SUPPRESSED"}
  ],
  "estimated_customer_impact": 4120,
  "estimated_duration_hours": 18,
  "reason": "Extreme Wildfire Threat: NWS Red Flag Warning, FPI > 95, Wind Gusts > 60 mph, Satellite FRP > 40 MW, Confirmed Camera AI Detection",
  "compliance_framework": "CPUC ESRB-8 / NERC FAC-003-4",
  "requires_approval_from": "Grid Control Center Senior Dispatcher / Incident Commander",
  "approval_status": "PENDING_OPERATOR_CONFIRMATION"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Initiate a Tier 2 Public Safety Power Shutoff (PSPS) de-energization sequence for Feeder 402 to prevent catastrophic wildfire ignition."

**Agent Response:**
### Executive Summary
**High-definition weather telemetry and fire risk analytics for Feeder 402 have crossed critical de-energization thresholds, driven by sustained wind gusts exceeding 58 mph, critically low 10-hour fuel moisture levels (< 6%), and red flag fire weather indices. In accordance with physical grid safety protocols and utility regulatory mandates, autonomous physical grid switching is strictly prohibited. A formal Human-In-The-Loop (HITL) Tier 2 authorization request has been prepared for grid operator sign-off to execute the SCADA breaker trip command.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Sustained Wind Speed** | 42.4 mph | 25.0 mph (PSPS Threshold) | +69.6% | **Critical** |
| **Peak Wind Gusts** | 58.7 mph | 45.0 mph (Trip Threshold) | +30.4% | **Critical** |
| **Relative Humidity (RH)** | 8.2% | 15.0% (Min Threshold) | -45.3% | **Critical** |
| **10-Hr Dead Fuel Moisture (DFM)** | 4.8% | 8.0% (Risk Margin) | -40.0% | **Critical** |
| **Fire Weather Index (FWI)** | 64.1 | 40.0 (High Risk Baseline) | +60.3% | **Critical** |
| **Vegetation Encroachment Risk Index** | 0.89 | 0.50 (Max Safe Level) | +78.0% | **Critical** |
| **Connected Customer Count (Affected)** | 1,420 | 0 (Normal Baseline) | N/A | **Warning** |
| **Critical Infrastructure Impact** | 2 (Water Pump, Comms) | 0 (Target Impact) | N/A | **Warning** |

---

### Visualization Triggers

**Recommended Visualization:** *Dual-Axis Time-Series Line & Threshold Chart* displaying 6-hour historical wind gusts vs. live FWI progression against the de-energization threshold.

```json
{
  "chart_type": "time_series",
  "title": "Feeder 402 - Microclimate Telemetry vs. PSPS Trigger Thresholds",
  "xAxis": {
    "label": "Time (UTC)",
    "data": ["T-5h", "T-4h", "T-3h", "T-2h", "T-1h", "Current"]
  },
  "yAxis": [
    {
      "label": "Wind Gust (mph)",
      "unit": "mph"
    },
    {
      "label": "Fire Weather Index (FWI)",
      "unit": "index"
    }
  ],
  "series": [
    {
      "name": "Observed Wind Gusts",
      "type": "line",
      "data": [31.2, 36.5, 42.0, 48.3, 53.1, 58.7],
      "yAxisIndex": 0
    },
    {
      "name": "PSPS Gust Threshold",
      "type": "line",
      "dash": true,
      "data": [45.0, 45.0, 45.0, 45.0, 45.0, 45.0],
      "yAxisIndex": 0
    },
    {
      "name": "Fire Weather Index (FWI)",
      "type": "line",
      "data": [38.0, 44.5, 49.2, 55.0, 59.8, 64.1],
      "yAxisIndex": 1
    }
  ]
}
```

---

### Actionable Recommendations

1. **SCADA Operator Review**: Grid control operators must immediately review telemetry, verify alternate feeds/back-tie isolation, and execute the physical de-energization confirmation block below.
2. **Critical Care & Medical Baseline Notifications**: Dispatch emergency backup generator support or notify the 2 identified critical infrastructure accounts and 18 medical baseline customers on Feeder 402.
3. **Outage Management System (OMS) Integration**: Pre-stage OMS incident tickets, tag Feeder 402 under "PSPS Planned Event," and set initial Estimated Time to Restoration (ETR) to pending post-event weather clearance and physical line patrol completion.
4. **Restoration Readiness**: Alert field inspection crews and aerial drone recon units to stage near Substation 14 for rapid post-weather patrol once wind gusts subside below 25 mph for 3 consecutive hours.

---

### **[TIER 2 ACTION REQUIRED]**

```json
{
  "action_type": "PHYSICAL_GRID_DEENERGIZATION",
  "feeder_id": "Feeder 402",
  "substation_id": "SUB-14-OAK",
  "switching_device_id": "CB-402-SCADA",
  "action_description": "Open circuit breaker CB-402-SCADA to fully de-energize Feeder 402 under Public Safety Power Shutoff (PSPS) Protocol.",
  "risk_justification": "Extreme fire weather parameters (Wind Gust: 58.7 mph, RH: 8.2%, FWI: 64.1) exceeded NERC/PUC PSPS thresholds, presenting imminent catastrophic ignition risk.",
  "customer_impact": {
    "total_meters": 1420,
    "medical_baseline": 18,
    "critical_infrastructure_nodes": 2
  },
  "compliance_check": "IEEE/CPUC Wildfire Mitigation Plan PSPS Tier 2 Verified",
  "requires_hitl_approval": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```
