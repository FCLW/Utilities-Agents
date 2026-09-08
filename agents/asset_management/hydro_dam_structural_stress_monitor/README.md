# ⚡ Hydro Dam Structural Stress Monitor

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of hydro dam structural stress monitor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Hydro Dam Structural Stress Monitor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank hydro dam structural stress monitor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.hydro_dam_structural_stress_monitor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are piezometer hydrostatic uplift pressures on the spillway foundation of Dam Unit 2 within FERC safety margins?"

**Agent Response:**
### Executive Summary
**Hydrostatic uplift pressures across all piezometric monitoring nodes on the Dam Unit 2 spillway foundation currently register within established Federal Energy Regulatory Commission (FERC) Engineering Guidelines (Chapter 5 - Foundation Uplift & Seepage).** **The foundation drainage gallery and pressure relief line efficiency remain at 92.4%, keeping effective uplift gradients well below design-basis stability thresholds.** **No critical anomalous differential pressures, foundation unbonding indications, or hydraulic fracture propagation signatures are observed at this time.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Heel Uplift Pressure (PZ-SP2-01)** | 18.5 psi (42.7 ft H₂O) | ≤ 24.0 psi (FERC Limit) | -22.9% | **Normal** |
| **Mid-Chute Uplift Pressure (PZ-SP2-02)** | 14.2 psi (32.8 ft H₂O) | ≤ 19.5 psi (FERC Limit) | -27.2% | **Normal** |
| **Toe / Still Basin Apron Uplift (PZ-SP2-03)** | 8.0 psi (18.5 ft H₂O) | ≤ 12.0 psi (FERC Limit) | -33.3% | **Normal** |
| **Drainage Curtain Flow Rate** | 38.4 gpm | 35.0 – 45.0 gpm | +9.7% | **Normal** |
| **Foundation Uplift Reduction Efficiency** | 92.4% | ≥ 85.0% | +8.7% | **Normal** |
| **Spillway Monolith Sliding Factor of Safety (FS)** | 1.84 | ≥ 1.50 (FERC Standard) | +22.7% | **Normal** |

---

### Visualization Triggers

**Recommended Visualization:** Time-Series Multi-Line Chart comparing real-time piezometric hydraulic head vs. FERC allowable uplift envelope across foundation cross-sections.

```json
{
  "chart_type": "line",
  "title": "Dam Unit 2 Spillway Foundation Piezometer Hydrostatic Uplift Pressures vs. FERC Limits",
  "xAxis": {
    "title": "Monitoring Interval",
    "categories": ["T-4h", "T-3h", "T-2h", "T-1h", "Current"]
  },
  "yAxis": {
    "title": "Uplift Pressure (psi)",
    "min": 0,
    "max": 30
  },
  "series": [
    {
      "name": "PZ-SP2-01 (Upstream Heel)",
      "data": [18.2, 18.4, 18.5, 18.6, 18.5]
    },
    {
      "name": "PZ-SP2-02 (Mid-Chute Foundation)",
      "data": [14.1, 14.3, 14.2, 14.4, 14.2]
    },
    {
      "name": "PZ-SP2-03 (Downstream Toe / Apron)",
      "data": [7.8, 8.0, 7.9, 8.1, 8.0]
    },
    {
      "name": "FERC Max Threshold (PZ-SP2-01)",
      "data": [24.0, 24.0, 24.0, 24.0, 24.0],
      "dashStyle": "Dash"
    },
    {
      "name": "FERC Max Threshold (PZ-SP2-02)",
      "data": [19.5, 19.5, 19.5, 19.5, 19.5],
      "dashStyle": "Dash"
    },
    {
      "name": "FERC Max Threshold (PZ-SP2-03)",
      "data": [12.0, 12.0, 12.0, 12.0, 12.0],
      "dashStyle": "Dash"
    }
  ]
}
```

---

### Actionable Recommendations

- **Continuous Telemetry Tracking**: Maintain 15-minute automated scanning intervals on vibrating wire piezometers `PZ-SP2-01` through `PZ-SP2-06`.
- **Drainage Gallery Inspection**: Verify during the next routine weekly physical walkdown that foundation relief drains show clean discharge without silt or precipitate clogs.
- **Reservoir Head Correlation**: Maintain automated cross-correlation between forebay pool level fluctuations and foundation pressure dissipation gradients to flag any reduction in drain efficiency.

### Example 2: Trend & Comparative Analysis
**User:** "Review the 6-month inclinometer tilt drift and seismic accelerometer readings for the main concrete gravity abutment."

**Agent Response:**
### 1. Executive Summary
**The 6-month structural telemetry review for the main concrete gravity abutment indicates steady, linear inclinometer tilt drift within design safety margins, alongside baseline micro-seismic accelerometer activity. Cumulative tilt drift has reached +3.70 arcseconds against the +5.00 arcsecond warning threshold, while seismic accelerations peaked at 0.012g following localized micro-tremor events. Overall asset structural integrity remains stable under current hydrostatic loading with an Asset Health Index (AHI) of 88.5/100.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Cumulative Inclinometer Tilt Drift** | 3.70 arcsec | 0.00 arcsec (Threshold: 5.00 arcsec) | +74.0% of Limit | **Warning** (Elevated Drift Rate) |
| **Drift Velocity (Monthly Rate)** | +0.38 arcsec/month | < 0.25 arcsec/month | +52.0% | **Warning** |
| **Peak Ground Acceleration (Seismic PGA)** | 0.012 g | < 0.050 g (Operating Basis Earthquake) | -76.0% below OBE | **Normal** |
| **Ambient Vibration Baseline (RMS)** | 0.0018 g | 0.0015 g | +20.0% | **Normal** |
| **Piezometric Uplift Pressure (Abutment Key)** | 142.3 kPa | 138.0 kPa (Max Design: 210 kPa) | +3.1% | **Normal** |
| **Asset Health Index (AHI)** | 88.5 / 100 | 100.0 / 100 | -11.5% | **Normal** |

---

### 3. Visualization Triggers

**Recommended Visualization:** Time-Series Multi-Axis Line Chart (6-Month Drift & Seismic Acceleration Profile).

```json
{
  "chart_type": "line",
  "title": "6-Month Inclinometer Tilt Drift and Seismic Accelerometer Telemetry",
  "xAxis": {
    "categories": ["Month -5", "Month -4", "Month -3", "Month -2", "Month -1", "Current Month"],
    "title": "Observation Period"
  },
  "yAxes": [
    {
      "title": "Tilt Drift (arcsec)",
      "opposite": false
    },
    {
      "title": "Peak Ground Accel (g)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Tilt Drift (arcsec)",
      "data": [1.80, 2.12, 2.45, 2.88, 3.32, 3.70],
      "yAxis": 0,
      "color": "#1f77b4"
    },
    {
      "name": "Max Seismic Accel (g)",
      "data": [0.004, 0.006, 0.005, 0.012, 0.007, 0.005],
      "yAxis": 1,
      "color": "#ff7f0e"
    },
    {
      "name": "Tilt Warning Threshold",
      "data": [5.00, 5.00, 5.00, 5.00, 5.00, 5.00],
      "yAxis": 0,
      "dashStyle": "Dash",
      "color": "#d62728"
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Increase Telemetry Polling Frequency**: Transition bi-axial inclinometer logging from 1-hour intervals to 15-minute intervals to closely track drift velocity approaching the 5.00 arcsec threshold.
- **Correlate Headwater Differential**: Cross-reference piezometric uplift measurements and reservoir pool elevations against abutment tilt to isolate hydrostatic load-induced elastic strain from inelastic foundation displacement.
- **Perform Geodetic Optical Survey Verification**: Dispatch a field engineering crew to perform high-precision robotic total station and GNSS monument survey cross-checks across the abutment crest.
- **FERC/DSOD Compliance Review**: Archive the 6-month seismic and structural trend file in accordance with Part 12D dam safety surveillance and monitoring protocols.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Trigger an automated sluice gate relief sequence and alert the dam safety engineer of abnormal foundation uplift."

**Agent Response:**
### Executive Summary
**A critical uplift pressure anomaly has been detected across the hydro dam foundation piezometric array, exceeding the high-threshold safety baseline and signaling abnormal hydrostatic loading. In accordance with utility safety guardrails and FERC/NERC dam safety guidelines, physical actuation of sluice gates cannot be executed autonomously and requires mandatory Human-In-The-Loop (HITL) authorization. A high-priority emergency alert has been staged for the Dam Safety Engineer alongside a pre-configured Tier 2 gate relief actuation payload awaiting operator sign-off.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Foundation Uplift Pressure (Pz-04)** | 148.5 psi | 92.0 psi (Max Normal) | +61.4% | **Critical** |
| **Piezometric Head Level** | 412.8 ft | 385.0 ft | +7.2% | **Critical** |
| **Foundation Drainage Flow Rate** | 18.2 gpm | 45.0 gpm (Expected Relief) | -59.6% (Drain Blockage Suspected) | **Warning** |
| **Structural Crest Displacement** | 4.8 mm | < 2.5 mm | +92.0% | **Warning** |
| **Asset Health Index (AHI)** | 42.0 / 100 | > 80.0 / 100 | -47.5% | **Critical** |

---

### Visualization Trigger

```json
{
  "chart_type": "line",
  "title": "Dam Foundation Uplift Pressure vs. Baseline Thresholds",
  "data": [
    {"timestamp": "T-05h", "uplift_pressure_psi": 91.2, "critical_threshold_psi": 120.0, "normal_baseline_psi": 92.0},
    {"timestamp": "T-04h", "uplift_pressure_psi": 94.8, "critical_threshold_psi": 120.0, "normal_baseline_psi": 92.0},
    {"timestamp": "T-03h", "uplift_pressure_psi": 108.3, "critical_threshold_psi": 120.0, "normal_baseline_psi": 92.0},
    {"timestamp": "T-02h", "uplift_pressure_psi": 126.1, "critical_threshold_psi": 120.0, "normal_baseline_psi": 92.0},
    {"timestamp": "T-01h", "uplift_pressure_psi": 139.7, "critical_threshold_psi": 120.0, "normal_baseline_psi": 92.0},
    {"timestamp": "Current", "uplift_pressure_psi": 148.5, "critical_threshold_psi": 120.0, "normal_baseline_psi": 92.0}
  ]
}
```

---

### Actionable Recommendations
- **Dispatch Immediate Emergency Notification**: Transmit priority alert to the on-call Dam Safety Engineer, Lead Civil Engineer, and Grid Operations Control Center.
- **Inspect Foundation Drainage Gallery**: Deploy field personnel to verify gallery drainage headers for calcification or mechanical valve blockages contributing to reduced drain outflow.
- **Review Hydrodynamic Downstream Impact**: Validate downstream river stage gauges and spillway discharge capacity prior to manual sluice gate relief authorization.
- **Maintain High-Frequency Telemetry Ingestion**: Increase piezometer, seepage, and pendulum displacement sensor telemetry sampling rates to 1-minute intervals.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_ASSET_ACTUATION",
  "subsystem": "HYDRO_SLUICE_GATE_CONTROL",
  "action_description": "Execute automated partial sluice gate relief sequence (Gate 1 & Gate 2 open to 15% discharge rate) to mitigate foundation uplift pressure.",
  "target_asset_id": "DAM-HYDRO-SLUICE-01/02",
  "risk_classification": "CRITICAL_SAFETY_OPERATION",
  "requires_hitl_approval": true,
  "telemetry_trigger": {
    "sensor_id": "PZ-04-FOUNDATION",
    "trigger_value": "148.5 psi",
    "threshold_limit": "120.0 psi"
  },
  "compliance_framework": "FERC Hydro Dam Safety Division / NERC Standard",
  "operator_prompt": "Confirm execution of controlled sluice gate relief sequence. Awaiting manual authorization from Licensed Dam Safety Engineer."
}
```
