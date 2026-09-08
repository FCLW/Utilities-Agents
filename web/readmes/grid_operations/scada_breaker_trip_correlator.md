# ⚡ Scada Breaker Trip Correlator

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of scada breaker trip correlator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Scada Breaker Trip Correlator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank scada breaker trip correlator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.scada_breaker_trip_correlator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did the 115kV breaker trip at Substation West coincide with the fault event reported by digital protective relay Relay-21?"

**Agent Response:**
### Executive Summary
**Yes, the 115kV breaker trip at Substation West directly coincided with the Phase-A-to-Ground (AG) fault detected by digital protective relay Relay-21.** **Sequence of Events (SOE) telemetry confirms Relay-21 initiated a Zone 1 trip signal at T+18ms following fault inception (8.4 kA peak), with the 115kV breaker auxiliary contacts (52a) clearing the fault within 45ms (2.7 cycles).** **Total clearing time complied with IEEE C37.04/NERC PRC standards with zero breaker failure or coordination anomalies detected.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fault Event Correlation Delta** | **0.00 ms (Direct Coincidence)** | $\le 5.0\text{ ms}$ (Time-sync error) | $0.0\%$ | **Normal** |
| **Relay Operating Time (Relay-21 Zone 1)** | **18.0 ms (1.08 cycles)** | $< 20.0\text{ ms}$ | $-10.0\%$ | **Normal** |
| **115kV Breaker Interrupting Time** | **27.0 ms (1.62 cycles)** | $< 33.3\text{ ms}$ (2.0 cycles) | $-18.9\%$ | **Normal** |
| **Total Fault Clearing Time** | **45.0 ms (2.70 cycles)** | $\le 50.0\text{ ms}$ (3.0 cycles) | $-10.0\%$ | **Normal** |
| **Peak Fault Current ($I_{fault}$)** | **8.40 kA** | $40.0\text{ kA}$ (Interrupting Rating) | $-79.0\%$ | **Normal** |
| **SAIDI Impact (Substation West Bus/Feeder)** | **0.00 min** (Automated bus transfer held) | $0.00\text{ min}$ | $0.0\%$ | **Normal** |

---

### Visualization Triggers
- **Recommended Visualization**: High-Resolution Sequence of Events (SOE) Time-Series Line Chart.
- **Chart Data Payload (JSON)**:
```json
{
  "chart_type": "line",
  "title": "Substation West 115kV Breaker Trip & Relay-21 Fault Oscillography",
  "data": [
    {
      "timestamp_ms": 0,
      "event": "Fault Inception (AG Phase-to-Ground)",
      "current_kA": 8.4,
      "relay_trip_signal": 0,
      "breaker_state": "Closed"
    },
    {
      "timestamp_ms": 18,
      "event": "Relay-21 Zone 1 Trip Output Asserted",
      "current_kA": 8.4,
      "relay_trip_signal": 1,
      "breaker_state": "Closed"
    },
    {
      "timestamp_ms": 45,
      "event": "115kV Breaker Main Contacts Part / Arc Extinguished",
      "current_kA": 0.0,
      "relay_trip_signal": 1,
      "breaker_state": "Open"
    },
    {
      "timestamp_ms": 52,
      "event": "SCADA 52a Auxiliary Switch Open Status Recorded",
      "current_kA": 0.0,
      "relay_trip_signal": 0,
      "breaker_state": "Open"
    }
  ]
}
```

---

### Actionable Recommendations
- **Download Oscillography & COMTRADE Records**: Retrieve the high-speed disturbance recording from Relay-21 to verify fault distance estimation (impedance calculation).
- **Physical Line Patrol**: Dispatch a field inspection crew to the calculated line distance (~4.2 miles on Line 115-4) to check for vegetation contact, lightning arrestor failure, or mechanical line damage prior to re-energization.
- **Breaker Duty Monitoring**: Log the accumulated interrupted duty ($8.4\text{ kA}$) into the asset health management system for Substation West 115kV Breaker maintenance scheduling.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "SCADA_LINE_RECLOSE_EXECUTION",
  "substation_id": "SUB_WEST_115KV",
  "device_id": "BKR_115_4",
  "associated_relay": "RELAY_21",
  "target_state": "CLOSE",
  "interlocks_verified": [
    "Sync_Check_25_Valid",
    "Line_Dead_Bus_Live",
    "Relay_Trip_Contact_Reset"
  ],
  "hitl_approval_required": true,
  "operator_prompt": "Confirm manual SCADA supervisory close command for Substation West 115kV Breaker BKR_115_4 following visual line clearance confirmation."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate SCADA sequence of events (SOE) millisecond logs with distance relay zone-1 trip signals and fault recorders."

**Agent Response:**
### Executive Summary
**High-speed correlation between Substation Sequence of Events (SOE) logs, microprocessor distance relay (ANSI 21) Zone-1 trip elements, and Digital Fault Recorder (DFR) COMTRADE records confirms an instantaneous, high-confidence single-line-to-ground (SLG, A-G) fault clearance within standard clearing limits. The relay asserted an instantaneous Zone-1 trip within 14.5 ms of fault inception, and the 52kV/115kV primary vacuum breaker successfully interrupted arc current in 52.0 ms (3.12 cycles), verifying proper protection coordination without relay overreach or breaker mechanism retardation.**

---

### Quantitative Performance Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Relay Zone-1 Pickup Time** | 14.50 ms | $\le$ 16.67 ms (1.0 cycle) | -13.02% | **Normal** |
| **Total Fault Clearing Time (FCT)** | 52.00 ms | $\le$ 66.67 ms (4.0 cycles) | -22.00% | **Normal** |
| **Breaker Mechanism Travel Time (52a/52b)** | 37.50 ms | $\le$ 45.00 ms | -16.67% | **Normal** |
| **SOE-to-DFR GPS Time Sync Skew** | 0.85 ms | $\le$ 1.00 ms (IRIG-B / IEEE 1588) | -15.00% | **Normal** |
| **Calculated Fault Location Deviation** | 4.12 miles | 4.20 miles (Physical Line Tap) | -1.90% | **Normal** |
| **Arc Interruption Current Magnitude ($I_f$)**| 8.42 kA | 25.00 kA (Rated Symmetrical Breaking) | -66.32% | **Normal** |

---

### Sequence of Events (SOE) & Oscillography Correlation

```
+0.00 ms   [DFR]      Fault Inception detected (Phase A current step increase to 8.42 kA RMS).
+14.50 ms  [SEL-421]  Zone-1 Mho/Quad element (21P/21G) asserts TRIP coil output.
+16.00 ms  [DFR]      COMTRADE high-speed oscillography recording latched at 10 kHz sample rate.
+18.20 ms  [RTU-SOE]  Substation SER/SOE logs binary point change: Relay Trip Output active.
+46.50 ms  [52a AUX]  Breaker primary contact separation; 52a auxiliary contact initiates transition.
+52.00 ms  [DFR]      Primary arc extinguished at current zero crossing; line de-energized.
+56.80 ms  [52b AUX]  Breaker 52b contact closed; breaker transition state resolved to "OPEN".
+68.00 ms  [SCADA]    DNP3 Class 1 unsolicited event processed at Master Operations Console.
```

---

### Engineering Insights & Root Cause Analysis

1. **Relay Element Validation**: The distance relay operated purely on **Zone-1 (Instantaneous)** with zero intentional time delay ($T_{21} = 0.00\text{ s}$). Apparent impedance trajectory entered the characteristic boundary at $Z_{seen} = 1.28 + j3.44\ \Omega$, localizing the fault to **38.4% of total line impedance** (well within the typical 80–85% Zone-1 reach setting).
2. **Breaker Health & Clearing Dynamic**: Breaker arcing time was measured at 5.5 ms, with total operating time from coil energization to arc clearance at 37.5 ms. No contact bounce, delayed auxiliary contact transfer, or restrikes were detected on the COMTRADE current traces.
3. **Cross-System Time Synchronization**: Time divergence across GPS-synchronized IEDs (IRIG-B clock) and the RTU SOE buffer was under 0.85 ms, confirming reliable chronological causality across all protection layers.

---

### Actionable Recommendations

- **Dispatch Line Inspection Crew**: Route patrol to mile marker **4.1 to 4.3** along the line segment to inspect Phase A insulators, cross-arms, and vegetation clearances.
- **Archive Event Records**: Automatically package COMTRADE (.CFG/.DAT) and SOE (.SER) records into the enterprise asset repository for compliance with **NERC PRC-002-2** (Disturbance Monitoring).
- **Auto-Reclose Lockout Review**: Verify whether automatic reclosing (ANSI 79) is permitted or blocked by the Protection Automation Controller based on fault impedance proximity and downstream distributed energy resource (DER) anti-islanding interlocks.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "BREAKER_AUTO_RECLOSE_OVERRIDE_OR_LINE_PATROL_HOLD",
  "affected_breaker_id": "BKR-115-SUB12-04",
  "affected_feeder": "FDR-115-LINE-42",
  "action_description": "Maintain Breaker 115-04 open in lockout status pending line patrol verification at Mile 4.12. Authorize supervisory close only after patrol reports all-clear.",
  "hitl_approval_required": true,
  "safety_risk_level": "Tier-2 Operational Grid Switching"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue a SCADA reclose supervisory permission signal after confirming line impedance has returned to normal open state."

**Agent Response:**
### Executive Summary
**Autonomous physical control and direct supervisory signal execution are strictly restricted under Grid Operations Safety Guardrails.** 
**The Scada Breaker Trip Correlator has evaluated the supervisory reclose request against nominal line impedance thresholds and classified the reclose command as a Tier 2 High-Risk Physical Grid Action.** 
**Supervisory permission cannot be executed autonomously and is queued pending mandatory Human-in-the-Loop (HITL) engineering verification and authorization.**

---

### Data Presentation (Markdown Table)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Positive Sequence Impedance ($Z_1$)** | 42.15 $\Omega$ | 42.00 $\Omega$ (Open State) | +0.36% | **Normal** |
| **Zero Sequence Impedance ($Z_0$)** | 118.40 $\Omega$ | 118.00 $\Omega$ (Open State) | +0.34% | **Normal** |
| **Line Residual Voltage ($V_{res}$)** | 0.42 kV | < 1.00 kV (De-energized) | -58.00% | **Normal** |
| **Fault Current Decay ($I_{fault}$)** | 0.00 A | 0.00 A | 0.00% | **Normal** |
| **Sync-Check Phase Angle ($\Delta \theta$)** | 3.2° | $\le 10.0^\circ$ | -68.00% | **Normal** |
| **Reclose Supervisory Token Status** | PENDING_HITL_AUTH | ARMED | N/A | **Warning** |

---

### Visualization Triggers

A **Time-Series Line Chart** is recommended to monitor the post-trip impedance recovery profile and verify that transient oscillations have settled prior to closing the breaker.

```json
{
  "chart_type": "line",
  "data": {
    "labels": ["T-5s", "T-4s", "T-3s", "T-2s", "T-1s", "T-0s (Current)"],
    "datasets": [
      {
        "label": "Measured Impedance (Ohms)",
        "data": [1.2, 4.8, 28.5, 41.8, 42.1, 42.15],
        "borderColor": "#1f77b4",
        "fill": false
      },
      {
        "label": "Normal Open Nominal Threshold (Ohms)",
        "data": [42.0, 42.0, 42.0, 42.0, 42.0, 42.0],
        "borderColor": "#2ca02c",
        "borderDash": [5, 5],
        "fill": false
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Perform Secondary Verification**: Grid Operator must confirm synchrocheck relay (25) voltage differential and phase angle alignment across the open breaker terminals.
- **Review Pre-Trip Relay Targets**: Cross-reference digital fault recorder (DFR) event logs to ensure the original trip mechanism (e.g., transient vs. permanent fault) has cleared.
- **Execute Supervisory Authorization**: A certified SCADA Dispatcher must manually authorize the staged reclose signal via the DMS/SCADA console.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "SCADA_SUPERVISORY_RECLOSE_PERMISSION",
  "classification": "TIER_2_PHYSICAL_GRID_OPERATION",
  "status": "AWAITING_HUMAN_APPROVAL",
  "target_asset": {
    "substation_id": "SUB-EAST-115KV",
    "breaker_id": "CB-115-402",
    "feeder_id": "FDR-402"
  },
  "pre_conditions_verified": {
    "line_impedance_normal_open": true,
    "residual_voltage_cleared": true,
    "lockout_relay_86_reset": true,
    "synchrocheck_permissive": true
  },
  "command_payload": {
    "control_point": "SCADA_RECLOSE_ARM_EXECUTE",
    "point_address": "DO_402_REC_PERM",
    "pulse_duration_ms": 1500
  },
  "operator_prompt": "Confirm execution of supervisory reclose permission signal for Breaker CB-115-402. Impedance telemetry indicates cleared line."
}
```
