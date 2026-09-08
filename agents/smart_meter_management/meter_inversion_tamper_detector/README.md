# ⚡ Meter Inversion Tamper Detector

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of meter inversion tamper detector is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Meter Inversion Tamper Detector Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank meter inversion tamper detector events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.meter_inversion_tamper_detector_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which smart meters have reported reverse energy flow or physical tilt tamper switch triggers without approved solar generation interconnection?"

**Agent Response:**
### Executive Summary
**A total of five smart meter clusters have been identified exhibiting physical tilt tamper switch triggers and significant reverse energy flow without an approved Net Energy Metering (NEM) or Distributed Energy Resource (DER) solar interconnection agreement.** **Telemetry indicates physical meter inversion—a method where the meter is physically inverted in the socket to run dials/registers in reverse—resulting in an estimated unmetered diversion of 1,235.2 kWh across affected feeders.** **Immediate field inspection and revenue protection containment protocols are recommended to mitigate revenue leakage and eliminate grid safety hazards associated with unapproved backfeed.**

---

### Quantitative Findings & Metric Overview

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Unapproved Reverse Energy Flow** | 1,235.2 kWh | 0.00 kWh | +100.0% | **Critical** |
| **Active Tilt Tamper Switch Triggers** | 22 Events | 0 Events | +100.0% | **Critical** |
| **Non-Solar Reverse Flow Flags** | 5 Meters | 0 Meters | +100.0% | **Critical** |
| **Estimated Revenue Leakage** | $271.74 | $0.00 | +100.0% | **Warning** |
| **Tamper Alarm Acknowledgment Rate** | 100.0% | 100.0% | 0.0% | **Normal** |

---

### Detailed Tamper & Inversion Audit Log

| Meter Identifier | Grid Zone / Feeder ID | Approved Solar Interconnection | Reverse Flow (kWh) | Tilt Switch Trigger Count | Tamper Severity |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `MTR-8842-INV` | `GZ-EAST-F01` | **FALSE** | 412.5 kWh | 8 | **Critical (Inversion Suspected)** |
| `MTR-4419-INV` | `GZ-NORTH-F04` | **FALSE** | 328.0 kWh | 5 | **Critical (Inversion Suspected)** |
| `MTR-9021-INV` | `GZ-SOUTH-F02` | **FALSE** | 215.4 kWh | 4 | **Critical (Inversion Suspected)** |
| `MTR-1193-INV` | `GZ-WEST-F09` | **FALSE** | 184.2 kWh | 3 | **Warning (Tilt / Backfeed)** |
| `MTR-6730-INV` | `GZ-CENTRAL-F03` | **FALSE** | 95.1 kWh | 2 | **Warning (Tilt / Backfeed)** |

*Note: All PII has been redacted in compliance with utility data governance and customer confidentiality mandates.*

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Unapproved Reverse Flow & Tilt Tamper Events by Feeder / Zone",
  "labels": ["GZ-EAST-F01", "GZ-NORTH-F04", "GZ-SOUTH-F02", "GZ-WEST-F09", "GZ-CENTRAL-F03"],
  "datasets": [
    {
      "label": "Reverse Flow (kWh)",
      "data": [412.5, 328.0, 215.4, 184.2, 95.1]
    },
    {
      "label": "Physical Tilt Tamper Count",
      "data": [8, 5, 4, 3, 2]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Dispatch Revenue Protection Unit (RPU) Field Crews**: Issue targeted work orders for physical site inspections and tamper seal verification on the 5 flagged meter sockets.
2. **Apply VEE Flags in MDMS**: Configure the Meter Data Management System (MDMS) to flag interval registers on these accounts to prevent erroneous negative billing credits under standard non-solar rate tariffs.
3. **Inspect for Unauthorized Generation vs. Physical Inversion**: Differentiate between unauthorized solar backfeed and physical socket inversion by cross-referencing reverse flow timestamps with solar irradiance curves (nighttime reverse flow confirms mechanical inversion).
4. **Deploy Anti-Inversion Meter Collars/Locks**: Retrofit identified socket locations with locking rings and optical tilt telemetry sensors during physical investigation.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FIELD_DISPATCH_AND_REMOTE_SERVICE_SWITCH_LOCKOUT",
  "target_meters": [
    "MTR-8842-INV",
    "MTR-4419-INV",
    "MTR-9021-INV",
    "MTR-1193-INV",
    "MTR-6730-INV"
  ],
  "reason": "Unapproved reverse energy flow combined with active tilt switch triggers indicating physical meter inversion and unmetered energy diversion.",
  "requested_operations": [
    "Issue prioritized RPU physical investigation work orders",
    "Lock MDMS billing estimation algorithms to prevent credit disbursement"
  ],
  "safety_and_compliance_impact": "Prevents unauthorized backfeed hazards to line crews and stops non-technical revenue losses.",
  "requires_human_authorization": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate meter inversion physical tilt alerts with sudden zero-consumption billing patterns to detect physical meter flipping theft."

**Agent Response:**
### Executive Summary
**Cross-correlation between AMI physical tilt/inversion sensor telemetry and high-resolution interval billing reads has identified active meter-flipping theft patterns across targeted feeder segments.** **Meters exhibiting sudden $180^\circ$ physical orientation changes or sustained tilt alarms coincide with an immediate $>98\%$ collapse in forward active energy ($kWh$) registration while maintaining active line-voltage excitation.** **Immediate dispatch of field revenue protection units is required to secure tamper evidence, prevent ongoing non-technical loss (revenue leakage), and mitigate physical socket safety hazards.**

---

### Quantitative Findings & Correlation Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Confirmed Inversion Tamper Events** | 14 Units | 0 Units | $+100.0\%$ | **CRITICAL** |
| **Post-Tilt Consumption Collapse** | 0.24 kWh/day | 38.60 kWh/day | $-99.38\%$ | **CRITICAL** |
| **Reverse Energy / Quadrant IV Flow** | 31.80 kWh/day | 0.00 kWh/day | $+100.0\%$ | **CRITICAL** |
| **Estimated Revenue Leakage (Run-Rate)**| $4,180 / month | $0 / month | $+100.0\%$ | **CRITICAL** |
| **AMI VEE Anomaly Flag Rate** | 100.0% | < 0.5% | $+19,900.0\%$ | **CRITICAL** |
| **Sustained Line Voltage (No Outage)** | 241.4 V | 240.0 V | $+0.58\%$ | **NORMAL** |

#### Cluster Breakdown by Feeder & Zone
* **Grid Zone `GZ-EAST-04` (Feeder `FDR-408`)**: 9 meters identified with simultaneous `TILT_SENSOR_ALARM` ($\Delta \theta \approx 180^\circ$) and immediate zero-consumption interval drop.
* **Grid Zone `GZ-SOUTH-11` (Feeder `FDR-112`)**: 5 meters identified with `REVERSE_ENERGY_FLOW` alarms accompanied by optical cover removal and tilt tamper logs.

---

### Visualization Triggers & Analytical Profile

```json
{
  "chart_type": "line",
  "title": "Meter Flipping Tamper Detection: Interval Consumption vs Tilt Event",
  "xAxis": {
    "categories": ["Day -7", "Day -6", "Day -5", "Day -4", "Day -3", "Day -2", "Day -1", "Event (Tilt/Invert)", "Day +1", "Day +2", "Day +3", "Day +4", "Day +5", "Day +6", "Day +7"]
  },
  "yAxis": [
    {"title": "Daily Active Energy (kWh)", "min": 0},
    {"title": "Tilt Sensor Angle (Degrees)", "opposite": true, "min": 0, "max": 180}
  ],
  "series": [
    {
      "name": "Pre/Post Inversion Active Energy (kWh)",
      "type": "line",
      "data": [38.2, 39.1, 37.8, 38.5, 40.0, 37.9, 38.4, 1.2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    },
    {
      "name": "Tilt Orientation Angle (deg)",
      "type": "column",
      "data": [0, 0, 0, 0, 0, 0, 0, 180, 180, 180, 180, 180, 180, 180, 180]
    }
  ]
}
```

---

### Actionable Recommendations

1. **VEE Engine Flagging & Estimated Billing Adjustment**:
   * Flag all intervals from the exact timestamp of the `TILT_SENSOR_ALARM` / `METER_INVERSION_ALERT` forward as `FAILED_TAMPER_SUSPECT`.
   * Apply historical baseline substitution (14-day pre-event trailing average) within the billing determinant generator to prevent unbilled revenue loss.
2. **Firmware & AMI Network Configuration**:
   * Configure the AMI Head-End System (HES) to elevate `REVERSE_POWER_FLOW` and `ACCELEROMETER_TILT` from informational status to priority-1 asynchronous push traps.
3. **Revenue Protection Field Dispatch**:
   * Deploy Revenue Protection / Meter Services field personnel with anti-tamper locking rings, digital seal verification kits, and body-worn cameras for evidence documentation.

---

### [TIER 2 ACTION REQUIRED]

```yaml
Tier_2_Operation: REVENUE_PROTECTION_FIELD_DISPATCH_AND_BILLING_HOLD
Authorization_Scope: Meter Tamper Enforcement & Work Order Generation
Impacted_Assets: 
  - MTR-88219 (Feeder FDR-408, Grid Zone GZ-EAST-04)
  - MTR-94302 (Feeder FDR-408, Grid Zone GZ-EAST-04)
  - MTR-77104 (Feeder FDR-112, Grid Zone GZ-SOUTH-11)
  - [Additional 11 flagged AMI meter endpoints]
Proposed_Actions:
  1. Generate emergency field inspection work orders for Revenue Protection & Field Metering.
  2. Place temporary administrative billing hold on accounts to prevent false $0 billing generation.
  3. Authorize physical lock-ring placement and tamper seal inspection on-site.
Safety_Risk_Assessment: Moderate (Arc flash and energized inverted socket terminal exposure hazard).
Human_Confirmation_Required: YES (Awaiting Revenue Protection Lead / Operations Supervisor Approval)
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch a revenue protection field investigator to inspect Meter #MT-90214 for unauthorized physical tampering and diversion."

**Agent Response:**
### Executive Summary
**Telemetry analysis for Meter #MT-90214 indicates sustained negative active power flow (-14.2 kW) and persistent reverse energy accumulation without an authorized distributed energy resource (DER) interconnection on file. These indicators are characteristic of a physical meter inversion tamper event, resulting in immediate revenue leakage. Autonomous field dispatch involves on-site physical inspection and regulatory engagement, requiring Human-in-the-Loop (HITL) authorization before work order issuance.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Reverse Power Flow** | -14.2 kW | 0.0 kW (Non-DER) | N/A | **Critical** |
| **Tamper Flag Count (Inversion/Tilt)** | 6 Events | 0 Events | +600.0% | **Critical** |
| **Estimated Revenue Leakage (Daily)** | $43.80 / day | $0.00 / day | N/A | **Critical** |
| **VEE Interval Validation Flag** | Failed (Rule 402) | 100% Pass | -100.0% | **Critical** |
| **Health & Integrity Score** | 18.5 / 100 | ≥ 95.0 / 100 | -80.5% | **Critical** |

---

### Visualization Trigger

* **Recommended Chart Type**: Time-Series Line Chart (Active Power & Reverse Energy Profile)
* **Description**: Displays the transition from normal forward active power draw to sustained negative power registration following suspected physical meter inversion.

```json
{
  "chart_type": "line",
  "title": "Meter #MT-90214 - Active Power Inversion Profile",
  "labels": ["Day -4", "Day -3", "Day -2", "Day -1", "Day 0"],
  "datasets": [
    {
      "label": "Active Power (kW)",
      "data": [14.2, 12.8, -8.4, -13.1, -14.2],
      "borderColor": "#FF0000",
      "fill": false
    },
    {
      "label": "Baseline / Expected (kW)",
      "data": [14.0, 13.5, 13.8, 14.1, 14.0],
      "borderColor": "#00AA00",
      "borderDash": [5, 5],
      "fill": false
    }
  ]
}
```

---

### Actionable Recommendations

* **Verify Interconnection Registry**: Confirm with GIS and DER registries that no unmapped rooftop solar or battery storage installation was commissioned at this service delivery point.
* **Freeze Billing Cycle**: Place an administrative hold on the current billing cycle for Meter #MT-90214 to prevent erroneous negative generation credits or unbilled consumption credit reconciliations.
* **Approve Field Investigation**: Authorize the Tier 2 Revenue Protection field dispatch payload below to perform a physical seal, orientation, and diversion inspection.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FIELD_DISPATCH_REVENUE_PROTECTION",
  "target_asset_id": "MT-90214",
  "priority": "HIGH",
  "dispatch_reason": "Suspected Physical Meter Inversion & Energy Diversion",
  "evidence_summary": {
    "active_power_kw": -14.2,
    "tamper_flag_count": 6,
    "unauthorized_generation_detected": true
  },
  "requested_action": "Dispatch Revenue Protection Field Investigator to inspect physical meter orientation, meter base seal integrity, and wire taps.",
  "approval_status": "PENDING_HUMAN_CONFIRMATION"
}
```
