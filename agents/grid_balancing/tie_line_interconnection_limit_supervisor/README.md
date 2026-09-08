# ⚡ Tie Line Interconnection Limit Supervisor

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of tie line interconnection limit supervisor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Tie Line Interconnection Limit Supervisor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank tie line interconnection limit supervisor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.tie_line_interconnection_limit_supervisor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Is the real-time megawatt power transfer across Intertie Line 500 approaching the Total Transfer Capability (TTC) limit?"

**Agent Response:**
### Executive Summary
**Real-time power transfer across Intertie Line 500 is currently at 1,845 MW, operating at 92.25% of its 2,000 MW Total Transfer Capability (TTC) and within 55 MW of its System Operating Limit (SOL) threshold of 1,900 MW.** **The rate of transfer increase over the past 30 minutes indicates an active approach toward intertie congestion, eroding Available Transfer Capability (ATC) down to 155 MW.** **Pre-contingency mitigation and generation redispatch protocols must be evaluated immediately to prevent an NERC Transmission Loading Relief (TLR) Level 3 event.**

---

### Quantitative Telemetry & Limit Breakdown

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Real-Time Active Power Flow** | 1,845.0 MW | 1,500.0 MW (Nominal Flow) | +23.00% | **Warning** |
| **Total Transfer Capability (TTC)** | 2,000.0 MW | 2,000.0 MW (Rated Ceiling) | 0.00% | **Critical** (Flow at 92.25% of TTC) |
| **System Operating Limit (SOL)** | 1,900.0 MW | 1,900.0 MW (N-1 Margin) | -2.89% (Margin: 55 MW) | **Warning** |
| **Available Transfer Capability (ATC)** | 155.0 MW | 500.0 MW (Target ATC) | -69.00% | **Warning** |
| **Transmission Reliability Margin (TRM)** | 100.0 MW | 100.0 MW (NERC Buffer) | 0.00% | **Normal** |
| **Capacity Benefit Margin (CBM)** | 50.0 MW | 50.0 MW (Firm Margin) | 0.00% | **Normal** |
| **Intertie Reactive Flow (MVAR)** | +210.4 MVAR | 0.0 MVAR (Unity Pf Target) | N/A | **Warning** |

---

### Visualization Trigger: Real-Time Flow vs. Operating Limits

A time-series chart is recommended to monitor the rate of change ($\Delta MW/\Delta t$) over the current operating window.

```json
{
  "chart_type": "line",
  "title": "Intertie Line 500 Real-Time Flow vs. Transfer Capability Limits",
  "x_axis_label": "Time (UTC)",
  "y_axis_label": "Megawatts (MW)",
  "series": [
    {
      "name": "Real-Time MW Flow",
      "data": [1620, 1680, 1725, 1780, 1810, 1845]
    },
    {
      "name": "System Operating Limit (SOL - 95%)",
      "data": [1900, 1900, 1900, 1900, 1900, 1900]
    },
    {
      "name": "Total Transfer Capability (TTC)",
      "data": [2000, 2000, 2000, 2000, 2000, 2000]
    }
  ],
  "timestamps": ["13:35", "13:40", "13:45", "13:50", "13:55", "14:00"]
}
```

---

### Actionable Recommendations

1. **Initiate Pre-TLR Logging**: Alert the Reliability Coordinator (RC) and adjacent Balancing Authority (BA) that Intertie Line 500 is within 55 MW of the 95% SOL threshold.
2. **Commit Internal Quick-Start Units / Economic Redispatch**: Issue a security-constrained redispatch order to ramp down import transactions across Intertie Line 500 by at least 150 MW within the next dispatch cycle (15 minutes).
3. **Adjust Phase Angle Regulating Transformers (PARs) / Shunt Capacitors**: Optimize reactive power support at Terminal Substation 500 to relieve MVAR loading and recover thermal headroom.
4. **Prepare Curtailment Schedules**: Stage non-firm interchange schedules for immediate curtailment if real-time flow exceeds 1,900 MW.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_id": "T2-GRID-BAL-2024-TL500-01",
  "action_type": "GENERATION_REDISPATCH_AND_SCHEDULE_CURTAILMENT",
  "target_asset": "Intertie Line 500 / Substation 500",
  "operation": "Execute security-constrained generation redispatch of +150 MW internal generation and curtail equivalent non-firm external interchange across Intertie Line 500.",
  "expected_impact": "Reduces Intertie Line 500 loading from 1,845 MW (92.25% TTC) to 1,695 MW (84.75% TTC), restoring ATC to 305 MW and preventing SOL violation.",
  "operator_approval_required": true,
  "nerc_compliance_tag": "NERC-FAC-011-3 / IRO-008-2"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate ambient air temperature and line conductor sag telemetry to determine dynamic line rating headroom on Intertie 2."

**Agent Response:**
### Executive Summary
**Dynamic Line Rating (DLR) telemetry analysis for Intertie 2 reveals a direct thermal correlation where peak ambient temperatures (36.5°C) and maximum conductor sag (5.08 m) compress dynamic transfer capacity to 582 MW, reducing available operational headroom to a critical low of 7 MW during peak afternoon heating. As ambient temperatures recede and radiative cooling increases, conductor sag contracts by 1.66 m, expanding effective DLR capacity up to 822 MW and unlocking +342 MW of export headroom. Real-time dynamic ratings provide up to a 26.5% capacity uplift over the 650 MW static seasonal limit during off-peak and evening hours, while preventing NERC FAC-008 clearance violations during mid-day thermal peaks.**

---

### Quantitative Correlation & Telemetry Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Ambient Air Temperature** | 36.5 °C (Peak) / 21.0 °C (Min) | 25.0 °C (Nominal Design) | +46.0% (Peak) | **Warning** |
| **Mid-Span Conductor Sag** | 5.08 m (Peak) | 4.20 m (Max Clearance Limit) | +21.0% | **Critical** (Mid-Day Peak) |
| **Minimum Ground Clearance Margin** | 7.12 m | 8.00 m (NERC Minimum) | -11.0% | **Critical** (Mid-Day Peak) |
| **Static Seasonal Limit** | 650.0 MW | 650.0 MW | 0.0% | **Normal** |
| **Dynamic Line Rating (DLR)** | 582.0 MW (Peak Min) / 822.0 MW (Max) | 650.0 MW (Static Baseline) | -10.5% (Day) / +26.5% (Night) | **Warning** (Thermal Derate) |
| **Active Power Flow (P_actual)** | 575.0 MW | 650.0 MW | -11.5% | **Warning** |
| **Effective DLR Headroom** | 7.0 MW (Trough) / 342.0 MW (Peak Headroom) | 100.0 MW (Target Buffer) | -93.0% (Trough) | **Critical** |

---

### Visualization Trigger: DLR Headroom & Sag Correlation

A multi-axis time-series visualization correlates ambient thermal conditions, physical sag displacement, and DLR capacity buffers:

```json
{
  "chart_type": "line",
  "title": "Intertie 2: Dynamic Line Rating (DLR) Headroom vs. Ambient Temperature and Conductor Sag",
  "xAxis": {
    "categories": ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
    "title": "Timestamp (UTC)"
  },
  "yAxis": [
    {
      "title": "Power (MW)",
      "opposite": false
    },
    {
      "title": "Ambient Temp (°C) / Sag (m)",
      "opposite": true
    }
  ],
  "series": [
    { "name": "Ambient Air Temp (°C)", "data": [34.2, 35.8, 36.5, 36.1, 34.8, 32.4, 30.1, 27.5, 25.2, 23.8, 22.4, 21.0], "yAxis": 1 },
    { "name": "Conductor Sag (m)", "data": [4.82, 4.95, 5.08, 5.02, 4.89, 4.65, 4.38, 4.12, 3.88, 3.71, 3.55, 3.42], "yAxis": 1 },
    { "name": "Static Thermal Rating (MW)", "data": [650, 650, 650, 650, 650, 650, 650, 650, 650, 650, 650, 650], "yAxis": 0 },
    { "name": "Dynamic Line Rating (DLR) (MW)", "data": [612, 595, 582, 588, 604, 638, 682, 725, 760, 784, 805, 822], "yAxis": 0 },
    { "name": "Active Flow (MW)", "data": [540, 565, 575, 560, 550, 562, 580, 590, 570, 540, 510, 480], "yAxis": 0 },
    { "name": "Available DLR Headroom (MW)", "data": [72, 30, 7, 28, 54, 76, 102, 135, 190, 244, 295, 342], "yAxis": 0 }
  ]
}
```

---

### Actionable Recommendations

1. **Implement Dynamic Real-Time Rating Deratings (13:00–16:00 UTC)**: 
   - Dynamically throttle scheduled exports across Intertie 2 to cap total flow at 570 MW during peak thermal periods, maintaining a mandatory 15 MW reliability margin below the 582 MW DLR floor.
2. **Utilize Off-Peak DLR Expansion (18:00–23:00 UTC)**: 
   - Expand wholesale intertie transfer limits up to 750 MW during evening hours as conductor sag reduces below 4.0 m and ambient cooling creates up to 342 MW of verified physical headroom.
3. **Calibrate Optical Sag Sensor & LiDAR Telemetry**:
   - Verify sensor node calibration at Intertie 2 Span 42/43 against ground LiDAR surveys to ensure IEEE 738 compliance and zero clearance encroachment.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMS_OPERATING_LIMIT_UPDATE",
  "target_asset": "Intertie 2 (TIE-02)",
  "grid_zone_id": "ZONE_BALANCING_NORTH",
  "proposed_action": "APPLY_DYNAMIC_TRANSFER_LIMIT",
  "parameters": {
    "intertie_id": "Intertie 2",
    "temporary_rating_ceiling_mw": 575.0,
    "effective_window_utc": "13:00 - 16:30",
    "contingency_constraint": "FAC-008_THERMAL_SAG_OVERLOAD",
    "requires_hitl_approval": true
  },
  "justification": "Peak ambient temperature (36.5°C) and conductor sag (5.08 m) reduce physical transfer capacity below static seasonal limit (650 MW) to 582 MW. Operator authorization required to update EMS Active Transfer Capability (ATC)."
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Initiate a scheduled interchange curtailment of 150 MW across the Western Tie to preserve NERC operating reliability margins."

**Agent Response:**
### Executive Summary
**A scheduled interchange curtailment request of 150 MW across the Western Intertie has been prepared to restore NERC Operating Reliability Margins (ORM) and prevent exceedance of System Operating Limits (SOL). In accordance with utility safety guardrails, physical interchange curtailments and schedule adjustments constitute a Tier 2 action and cannot be autonomously committed without Human-In-The-Loop (HITL) authorization. The pre-curtailment telemetry, margin impacts, and confirmation payload are structured below for operator approval.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Western Tie Total Scheduled Flow** | 1,080.00 MW | 930.00 MW | +16.13% | **Warning** |
| **System Operating Limit (SOL)** | 1,100.00 MW | 1,100.00 MW | 0.00% | **Warning** |
| **Operating Reliability Margin (ORM)** | 20.00 MW | 170.00 MW | -88.24% | **Critical** |
| **Available Transfer Capability (ATC)** | 120.00 MW | 270.00 MW | -55.56% | **Warning** |
| **Western Intertie Area Control Error (ACE)** | -38.40 MW | 0.00 MW | N/A | **Warning** |

---

### Visualization Triggers

**Recommended Visualization:** Time-Series Line Chart illustrating the Western Intertie Schedule vs. System Operating Limits (SOL) and Operating Reliability Margin (ORM) recovery trajectory.

```json
{
  "chart_type": "line",
  "title": "Western Tie Flow & Reliability Margin Post-Curtailment",
  "xAxisLabel": "Time Interval (UTC)",
  "yAxisLabel": "Active Power Flow (MW)",
  "series": [
    {
      "name": "Total Transfer Capability (TTC)",
      "data": [1200, 1200, 1200, 1200, 1200, 1200]
    },
    {
      "name": "System Operating Limit (SOL)",
      "data": [1100, 1100, 1100, 1100, 1100, 1100]
    },
    {
      "name": "Current Scheduled Interchange",
      "data": [1080, 1080, 1080, 1080, 1080, 1080]
    },
    {
      "name": "Post-Curtailment Flow Target",
      "data": [930, 930, 930, 930, 930, 930]
    }
  ]
}
```

---

### Actionable Recommendations

- **Operator Review**: Review the e-Tag curtailment priority stack (NERC Transmission Loading Relief / TLR levels 3–5) to identify the specific market participant transactions designated for the 150 MW reduction.
- **Balancing Authority Coordination**: Coordinate with the neighboring Balancing Authority (BA) and Reliability Coordinator (RC) to confirm the effective ramp rate and interval start time (recommended: 10-minute ramp window).
- **Secondary Reserve Activation**: Verify that internal spinning and quick-start reserves are armed in the EMS to absorb any resultant Area Control Error (ACE) deviations during the ramp period.
- **Authorization**: Execute the Tier 2 confirmation block below to submit the adjusted electronic tag (e-Tag) schedule to the Open Access Same-Time Information System (OASIS) and EMS interchange scheduler.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "SCHEDULED_INTERCHANGE_CURTAILMENT",
  "facility_id": "WESTERN_INTERTIE_PATH_66",
  "balancing_authority_id": "BA_WEST_01",
  "curtailment_mw": 150.00,
  "pre_curtailment_schedule_mw": 1080.00,
  "post_curtailment_schedule_mw": 930.00,
  "ramp_duration_minutes": 10,
  "compliance_standard": "NERC_IRO_006_TLR / NERC_TOP_001",
  "impact_assessment": {
    "sol_headroom_recovery_mw": 170.00,
    "system_stability_status": "RESTORED_TO_NORMAL"
  },
  "status": "PENDING_HUMAN_APPROVAL"
}
```
