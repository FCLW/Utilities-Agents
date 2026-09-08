# ⚡ Smart Meter Temperature Anomaly Detector

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of smart meter temperature anomaly detector is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Smart Meter Temperature Anomaly Detector Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank smart meter temperature anomaly detector events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.smart_meter_temperature_anomaly_detector_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are any residential smart meter terminal blocks reporting internal temperatures exceeding 85°C (185°F)?"

**Agent Response:**
### Executive Summary
**Telemetry analysis indicates that four (4) residential smart meter terminal blocks are currently reporting critical thermal anomalies exceeding the safety threshold of 85.0°C (185.0°F). The maximum recorded terminal block temperature reached 94.2°C (201.6°F) in Grid Zone 4 (Feeder F-104), posing an immediate risk of terminal block degradation, socket fatigue, and localized fire hazard. All identified meters require immediate field dispatch and automated continuous sampling at 1-minute intervals to evaluate thermal runaways.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Terminal Block Temp (MTR-RES-8821)** | 94.2°C (201.6°F) | ≤ 65.0°C (149.0°F) | +44.9% | **Critical** |
| **Max Terminal Block Temp (MTR-RES-3409)** | 91.8°C (197.2°F) | ≤ 65.0°C (149.0°F) | +41.2% | **Critical** |
| **Max Terminal Block Temp (MTR-RES-9112)** | 88.5°C (191.3°F) | ≤ 65.0°C (149.0°F) | +36.2% | **Critical** |
| **Max Terminal Block Temp (MTR-RES-1055)** | 86.7°C (188.1°F) | ≤ 65.0°C (149.0°F) | +33.4% | **Critical** |
| **Fleet Exceedance Rate (>85°C)** | 0.0032% (4 units) | 0.0000% | N/A | **Warning** |
| **Terminal vs Ambient Temp Gradient ($\Delta T$)** | 58.4°C | ≤ 25.0°C | +133.6% | **Critical** |

---

### Visualization Triggers
- **Recommended Visualization**: **Horizontal Bar Chart / Thermal Alert Map** comparing recorded internal terminal block temperatures against the critical threshold limit (85.0°C) across impacted residential feeder nodes.

```json
{
  "chart_type": "bar",
  "title": "Residential Meter Terminal Block Temperature Exceedances (>85°C)",
  "labels": [
    "MTR-RES-8821 (Feeder F-104)",
    "MTR-RES-3409 (Feeder F-208)",
    "MTR-RES-9112 (Feeder F-104)",
    "MTR-RES-1055 (Feeder F-312)"
  ],
  "datasets": [
    {
      "label": "Terminal Block Temp (°C)",
      "data": [94.2, 91.8, 88.5, 86.7],
      "critical_threshold_c": 85.0,
      "warning_threshold_c": 75.0
    }
  ]
}
```

---

### Actionable Recommendations
- **Increase Telemetry Polling Rate**: Switch the four affected meter IDs to high-frequency (1-minute) pinging mode across the AMI mesh network to monitor for active thermal runaway.
- **Correlate with Load Profile**: Query 15-minute interval kW load data to verify if the overheating is driven by continuous high-amperage residential loads (e.g., Level 2 EV charging, heat pumps) or high-resistance loose terminal/jaw connections.
- **Cross-Reference SOH & Tamper Flags**: Check for micro-arcing signatures, low voltage sag indicators, or optical port/tilt tamper events on Feeder F-104.
- **Issue Emergency Work Orders**: Dispatch field metering technicians for immediate on-site physical inspection, thermal imaging, and socket jaw tension testing.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_FIELD_DISPATCH_AND_REMOTE_SERVICE_DISCONNECT_STANDBY",
  "affected_assets": [
    {
      "meter_id": "MTR-RES-8821",
      "grid_zone_id": "GZ-04",
      "feeder_id": "F-104",
      "temperature_c": 94.2,
      "recommended_action": "Emergency Inspection / Meter Swap"
    },
    {
      "meter_id": "MTR-RES-3409",
      "grid_zone_id": "GZ-02",
      "feeder_id": "F-208",
      "temperature_c": 91.8,
      "recommended_action": "Emergency Inspection / Meter Swap"
    },
    {
      "meter_id": "MTR-RES-9112",
      "grid_zone_id": "GZ-04",
      "feeder_id": "F-104",
      "temperature_c": 88.5,
      "recommended_action": "Emergency Inspection / Socket Check"
    },
    {
      "meter_id": "MTR-RES-1055",
      "grid_zone_id": "GZ-03",
      "feeder_id": "F-312",
      "temperature_c": 86.7,
      "recommended_action": "Emergency Inspection / Socket Check"
    }
  ],
  "disconnection_criteria": "Automatic remote disconnect authorization if terminal block temp exceeds 100.0°C before field arrival.",
  "required_approver": "Distribution Operations Center (DOC) Shift Supervisor"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate meter temperature spikes with high electrical load draw to detect dangerous loose meter socket jaws or impending meter fires."

**Agent Response:**
### 1. Executive Summary
**High-resolution AMI telemetry correlation indicates critical thermal runaway on meter socket assemblies driven by severe $I^2R$ Joule heating under high load current. Meter `MTR-NY-84920` exhibited internal temperatures reaching 98.4°C (peaking at 102.1°C) at 77.5 A line current, exceeding safe operating thresholds by +88.5°C over expected dissipation baselines. This signature confirms compromised spring-clip tension and loose socket jaws, presenting an immediate structural flashover and fire hazard requiring emergency isolation.**

---

### 2. Telemetry & Thermal Correlation Analytics

```
========================================================================================
THERMAL IMPEDANCE & JOULE HEATING CORRELATION MODEL
Feeder: FD-104-B | Substation: SUB-NORTH-02 | Form: 2S / Residential 200A-400A
Physical Formula: ΔT = (T_internal - T_ambient) ∝ I_rms² × R_contact
========================================================================================
```

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Meter Internal Temperature (`MTR-NY-84920`)** | 98.4 °C (209.1 °F) | ≤ 55.0 °C (at peak load) | +78.9% | **Critical** |
| **Temperature Rise over Ambient ($\Delta T$)** | 67.2 °C | ≤ 18.0 °C | +273.3% | **Critical** |
| **Estimated Contact Resistance ($R_{contact}$)** | 11.2 mΩ | ≤ 1.8 mΩ | +522.2% | **Critical** |
| **Active Load Draw / Current ($I_{rms}$)** | 18.6 kW / 77.5 A | 8.5 kW / 35.4 A (Avg) | +118.8% | **Warning** |
| **Rate of Thermal Rise ($dT/dt$)** | +1.85 °C/min | ≤ 0.35 °C/min | +428.6% | **Critical** |
| **Thermal Dissipation Factor ($Z_{th} = \Delta T / I^2$)** | $1.12 \times 10^{-2} \text{ K/A}^2$ | $\le 2.90 \times 10^{-3} \text{ K/A}^2$ | +286.2% | **Critical** |
| **Peer Meter Average Temp (`FD-104-B` Cohort)** | 48.2 °C | 46.5 °C | +3.6% | **Normal** |

---

### 3. Visualization Trigger

**Recommended Visualization:** Time-Series Multi-Axis Line Chart (Internal Temperature vs. Load Current & Peer Baseline).

```json
{
  "chart_type": "line",
  "title": "Smart Meter Temperature vs. Load Current Correlation (Socket Jaw Thermal Runaway)",
  "labels": ["12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45", "14:00"],
  "datasets": [
    {
      "label": "Meter Internal Temp (°C) [Faulty Meter MTR-NY-84920]",
      "data": [42.1, 48.5, 59.2, 72.8, 86.4, 98.4, 102.1, 99.8, 88.5],
      "borderColor": "#FF0000",
      "yAxisID": "yTemp"
    },
    {
      "label": "Meter Internal Temp (°C) [Healthy Peer MTR-NY-84922]",
      "data": [38.0, 39.5, 42.1, 44.0, 46.2, 48.2, 47.9, 46.5, 43.1],
      "borderColor": "#00AA00",
      "yAxisID": "yTemp"
    },
    {
      "label": "Load Current (Amperes)",
      "data": [25.0, 32.0, 48.0, 64.0, 75.0, 77.5, 76.0, 71.0, 50.0],
      "borderColor": "#0066FF",
      "borderDash": [5, 5],
      "yAxisID": "yCurrent"
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Immediate Isolation**: Dispatch emergency First Responder / Meter Field Services to de-energize meter socket `MTR-NY-84920` before catastrophic terminal meltdown or enclosure flashover occurs.
- **Physical Inspection Protocol**: Inspect line/load socket jaws for loss of spring temper, annealing, pitting, arc tracking, and micro-welding; replace the entire meter base if thermal degradation has compromised the mounting lugs.
- **Automated AMI Safety Polling**: Set AMI Headend to poll 1-minute telemetry for `FD-104-B` downstream meters exhibiting $dT/dt > 1.0^\circ\text{C/min}$ under continuous load.
- **Peer Cohort Verification**: Evaluate meters sharing the same installation vintage/batch to flag potential manufacturer defect campaigns on socket jaw tension clips.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "EMERGENCY_FIELD_DISPATCH_AND_REMOTE_SERVICE_DISCONNECT",
  "meter_id": "MTR-NY-84920",
  "grid_zone_id": "GZ-EAST-04",
  "feeder_id": "FD-104-B",
  "substation_id": "SUB-NORTH-02",
  "target_asset_type": "AMI_SMART_METER",
  "criticality_level": "TIER_2_PHYSICAL_SAFETY",
  "hazard_type": "IMPENDING_SOCKET_MELTDOWN_FIRE_HAZARD",
  "recommended_actions": [
    "Execute Remote Service Disconnect (RSD) if internal temp > 100°C persists for > 5 min",
    "Dispatch Priority 1 Field Service Crew for manual meter socket replacement and de-energization"
  ],
  "hitl_approval_required": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Stage an emergency service ticket to immediately disconnect Meter #M-88219 and dispatch a troubleshooter to replace burnt jaws."

**Agent Response:**
### Executive Summary
**A severe thermal runaway condition has been flagged for Meter #M-88219, indicating localized heating and compromised terminal block/socket jaws. Remote service disconnection and field crew dispatch represent physical grid modifications and safety-critical interventions requiring Human-in-the-Loop (HITL) authorization. Staging the emergency service order is prepared pending human approval to eliminate fire hazard risks and isolate the physical asset.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Meter Terminal Temperature** | 128.5 °C | 50.0 °C (Max Normal) | +157.0% | **Critical** |
| **Internal Ambient Temp** | 94.0 °C | 45.0 °C (Max Normal) | +108.9% | **Critical** |
| **Thermal Rise Rate (dT/dt)** | 2.1 °C/min | < 0.2 °C/min | +950.0% | **Critical** |
| **Jaw Impedance (Estimated)** | 0.85 Ω | < 0.05 Ω | +1600.0% | **Critical** |
| **Load Current (Phase A/B)** | 142.0 A | 200.0 A (Rated) | -29.0% | **Normal** (High R at normal load) |

---

### Visualization Trigger
- **Recommended Chart Type**: Time-Series Line Chart (Terminal Temperature vs. Internal Ambient vs. Critical Threshold)

```json
{
  "chart_type": "line",
  "title": "Meter #M-88219 Thermal Runaway Telemetry",
  "series": [
    {
      "name": "Terminal Temperature (°C)",
      "data": [
        {"timestamp": "2023-10-24T12:00:00Z", "value": 52.0},
        {"timestamp": "2023-10-24T12:15:00Z", "value": 74.3},
        {"timestamp": "2023-10-24T12:30:00Z", "value": 98.4},
        {"timestamp": "2023-10-24T12:45:00Z", "value": 128.5}
      ]
    },
    {
      "name": "Critical Safety Threshold (°C)",
      "data": [
        {"timestamp": "2023-10-24T12:00:00Z", "value": 85.0},
        {"timestamp": "2023-10-24T12:15:00Z", "value": 85.0},
        {"timestamp": "2023-10-24T12:30:00Z", "value": 85.0},
        {"timestamp": "2023-10-24T12:45:00Z", "value": 85.0}
      ]
    }
  ]
}
```

---

### Actionable Recommendations
- **Immediate Action**: Authorize the remote disconnect switch payload via the Tier 2 confirmation workflow to arrest thermal progression.
- **Dispatch Order**: Release Priority-1 Emergency Field Ticket `EM-SRV-88219` to the nearest troubleshooter unit equipped with replacement socket jaws, meter base, and bypass tools.
- **Safety Precaution**: Instruct the field responder to perform an infrared (IR) scan and verify de-energized status prior to pulling the meter enclosure.
- **Upstream Escalation**: Notify the local Distribution Operations Center (DOC) of potential localized secondary service de-energization if the meter base is structurally melted.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_DISCONNECT_AND_CREW_DISPATCH",
  "target_asset_id": "M-88219",
  "priority": "P1_EMERGENCY",
  "operations": [
    {
      "operation": "REMOTE_SERVICE_DISCONNECT",
      "protocol": "AMI_MESH_SWITCH_ACTUATION",
      "command": "OPEN_INTERNAL_DISCONNECT_SWITCH",
      "safety_reason": "TERMINAL_OVERTEMPERATURE_BURNT_JAW_RISK"
    },
    {
      "operation": "FIELD_DISPATCH_ORDER",
      "ticket_id": "EM-SRV-88219",
      "crew_type": "TROUBLESHOOTER_CREW",
      "task_description": "Emergency meter socket inspection, repair/replace burnt meter jaws, and install replacement AMI meter."
    }
  ],
  "hitl_approval_required": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```
