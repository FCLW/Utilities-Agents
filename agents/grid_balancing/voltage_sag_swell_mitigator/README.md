# ⚡ Voltage Sag Swell Mitigator

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of voltage sag swell mitigator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Voltage Sag Swell Mitigator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank voltage sag swell mitigator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.voltage_sag_swell_mitigator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did the industrial park on Feeder 8 experience an ITIC-curve violating voltage sag during the transmission fault at 03:14?"

**Agent Response:**
### Executive Summary
**Yes, the industrial park on Feeder 8 experienced an ITIC (Information Technology Industry Council) curve-violating voltage sag during the transmission fault at 03:14:22 UTC.** The line-to-ground fault caused the RMS voltage at Feeder 8 substation bus to drop to **0.68 pu (68% of nominal)** for a duration of **140 ms (8.4 cycles)** before clearing. Because the retained voltage fell below the 0.70 pu ITIC lower tolerance boundary for durations between 20 ms and 500 ms, the event entered the "No Damage / Tripping Likely" prohibited region.

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Minimum RMS Voltage** | 0.68 pu (8.43 kV L-L) | 1.00 pu (12.47 kV L-L) | -32.0% | **Critical** |
| **Sag Duration** | 140 ms (8.4 cycles) | < 20 ms (Instantaneous) | +600.0% | **Critical** |
| **ITIC Lower Bound at 140 ms** | 0.70 pu | 0.70 pu | -2.86% below limit | **Critical (Violation)** |
| **Phase Imbalance (V2/V1)** | 14.8% | < 2.0% (IEEE 1159) | +640.0% | **Critical** |
| **Fault Clearing Time** | 140 ms | 100 ms (Primary Breaker Target) | +40.0% | **Warning** |
| **Post-Fault Recovery Voltage**| 0.99 pu | 0.95 – 1.05 pu | -1.0% | **Normal** |

---

### Visualization Triggers
- **Recommended Chart**: **ITIC (CBEMA) Curve Overlay with Time-Series RMS Voltage Profile** to demonstrate the magnitude-duration trajectory relative to standard ITIC equipment ride-through boundaries.

```json
{
  "chart_type": "line",
  "title": "Feeder 8 Industrial Park - Voltage Sag vs. ITIC Ride-Through Curve",
  "xAxis": {
    "name": "Duration (ms)",
    "type": "logarithmic",
    "data": [1, 10, 20, 50, 100, 140, 200, 500, 1000, 3000]
  },
  "yAxis": {
    "name": "Voltage (pu)",
    "min": 0.0,
    "max": 1.4
  },
  "series": [
    {
      "name": "Measured Event Trajectory",
      "data": [1.0, 1.0, 0.68, 0.68, 0.68, 0.68, 0.98, 1.0, 1.0, 1.0]
    },
    {
      "name": "ITIC Lower Boundary (Ride-Through Limit)",
      "data": [0.0, 0.0, 0.70, 0.70, 0.70, 0.70, 0.80, 0.80, 0.90, 0.90]
    },
    {
      "name": "ITIC Upper Boundary (Overvoltage Limit)",
      "data": [1.2, 1.2, 1.2, 1.2, 1.15, 1.15, 1.10, 1.10, 1.06, 1.06]
    }
  ]
}
```

---

### Actionable Recommendations
- **Industrial Customer Notification**: Proactively alert Key Account managers for the Feeder 8 industrial customers (e.g., precision manufacturing, data facilities) regarding potential equipment dropouts (VFDs, PLCs, sensitive contactors) triggered during the 03:14 event.
- **Protection Coordination Audit**: Review transmission Zone 1 clearing time and Feeder 8 breaker operating time; investigate why fault clearing took 140 ms against the 100 ms target.
- **Mitigation Assessment**: Evaluate deployment of Dynamic Voltage Restorers (DVR) or fast-acting D-STATCOM support at the Feeder 8 industrial node to maintain voltage ride-through compliance during adjacent transmission disturbances.

### Example 2: Trend & Comparative Analysis
**User:** "Examine the high-speed power quality meter waveforms to classify the sag duration, depth, and point-on-wave initiation."

**Agent Response:**
### Executive Summary
**High-speed power quality meter waveform analysis identified an instantaneous, asymmetrical Phase A-to-Ground voltage sag originating at Substation-14 (Feeder 12kV-4). The disturbance exhibited a maximum depth of 58.0% (residual voltage of 0.42 p.u.) with a total clearing duration of 80.0 ms (4.8 cycles) and a point-on-wave initiation angle of 48.5° on the positive half-cycle slope. The event breaches ITI (CBEMA) curve and SEMI-F47 ride-through envelopes, requiring dynamic reactive compensation response verification and protective relay clearing validation.**

---

### Quantitative Event Classification & Telemetry Analysis

The high-resolution point-by-point waveform capture (sampled at 256 samples/cycle) was processed against IEEE 1159 and IEEE 1564 standards:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Residual Voltage ($V_{res}$)** | `0.420 p.u.` | `1.000 p.u.` (Nominal) | -58.00% | **Critical** |
| **Sag Depth ($\Delta V$)** | `58.00%` | `< 10.00%` (IEEE 1159) | +480.00% | **Critical** |
| **Event Duration ($\Delta t$)** | `80.00 ms (4.80 cycles)` | `< 20.00 ms` | +300.00% | **Warning** |
| **Point-on-Wave Inception Angle** | `48.50°` | `0.00° - 360.00°` | N/A | **Normal** |
| **Point-on-Wave Recovery Angle** | `138.20°` | `0.00° - 360.00°` | N/A | **Normal** |
| **Phase Angle Jump ($\Delta \theta$)**| `-14.30°` | `< ±5.00°` | +186.00% | **Warning** |
| **Voltage Unbalance (VUF %)** | `18.40%` | `< 2.00%` (IEC 61000-4-30) | +820.00% | **Critical** |
| **ITI (CBEMA) / SEMI F47 Curve** | `Non-Compliant (Trip Region)`| `Ride-Through / No Interruption`| N/A | **Critical** |

---

### Waveform Envelope Visualization

```json
{
  "chart_type": "line",
  "title": "High-Speed PQ Waveform Envelope (Phase A, B, C)",
  "xAxis": {
    "type": "category",
    "name": "Time (ms)",
    "data": ["0ms", "10ms", "20ms (Inception)", "40ms", "60ms", "80ms", "100ms (Clearing)", "120ms", "140ms"]
  },
  "yAxis": {
    "name": "Voltage (p.u.)",
    "min": 0.0,
    "max": 1.2
  },
  "series": [
    {
      "name": "Phase A (Faulted)",
      "data": [1.00, 0.99, 0.42, 0.41, 0.43, 0.42, 0.98, 1.00, 1.00]
    },
    {
      "name": "Phase B",
      "data": [0.99, 1.00, 0.88, 0.87, 0.89, 0.88, 0.99, 1.00, 1.00]
    },
    {
      "name": "Phase C",
      "data": [1.00, 1.00, 0.91, 0.90, 0.90, 0.91, 1.00, 1.00, 1.00]
    }
  ]
}
```

---

### Engineering Classification Findings
1. **Sag Type & Mechanism**: Asymmetrical Type B (Single Line-to-Ground, SLG) sag on Phase A. The 48.5° initiation angle indicates insulation breakdown or lightning flashover near peak dielectric stress.
2. **Protection Response Time**: Total clearance time of 4.8 cycles is consistent with high-speed microprocessor distance/overcurrent relay trip plus a 3-cycle vacuum circuit breaker clearing time.
3. **Phase-Angle Jump Effect**: The $-14.30^\circ$ phase shift introduces transient zero-crossing displacement, impacting sensitive power electronic converters and PLL (Phase-Locked Loop) synchronization on connected inverter-based resources (IBRs).

---

### Actionable Recommendations

- **Immediate Review**: Verify whether Static Synchronous Compensator (STATCOM) or Dynamic Voltage Restorer (DVR) fast-VAR injection triggered within the first $0.5\text{ cycles}$ to support localized voltage.
- **Relay Coordination**: Cross-reference digital fault recorder (DFR) sequence-of-events (SOE) logs at Feeder 12kV-4 breaker to confirm correct primary protection operation without breaker failure timer pickup.
- **Customer Impact Notification**: Alert critical industrial and sensitive manufacturing accounts on Feeder 12kV-4 regarding potential SEMI-F47/CBEMA curve boundary excursion.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "RESTORATION_SWITCHING_VALIDATION"
  asset_target: "Substation-14 / Feeder-12kV-4"
  description: "Automated FLISR / SCADA reconfiguration to isolate faulted section and normalize voltage regulation settings."
  risk_assessment: "Potential transient disturbance on adjacent feeder ties if load transfer occurs prior to fault clearing verification."
  operator_action: "Manual confirmation required in SCADA OMS/DMS to authorize feeder reconfiguration and enable fast-VAR voltage support bank."
  safety_status: "PENDING_HUMAN_CONFIRMATION"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Trigger dynamic voltage restorer (DVR) fast-injection and adjust Substation Load Tap Changer (LTC) by two steps."

**Agent Response:**
### Executive Summary
**A request to trigger Dynamic Voltage Restorer (DVR) fast-injection and adjust Substation Load Tap Changer (LTC) positions by +2 steps has been staged for mitigation of local voltage deviation.** **In compliance with utility grid safety guardrails, autonomous execution of physical SCADA switching and voltage regulation assets is strictly prohibited without operator approval.** **A Tier 2 Human-In-The-Loop (HITL) authorization payload has been generated for supervisory dispatcher confirmation.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Bus Voltage (RMS)** | 0.88 p.u. | 1.00 p.u. (ANSI C84.1 Range A) | -12.0% | **Critical** (Sag Condition) |
| **DVR Energy Storage SOC** | 94.5% | ≥ 85.0% | +11.2% | **Normal** (Ready for Injection) |
| **Substation LTC Position** | Tap 0 (Neutral) | Target: Tap +2 | +2 steps | **Warning** (Adjustment Staged) |
| **Total Harmonic Distortion (THDv)** | 2.1% | < 5.0% (IEEE 519) | -58.0% | **Normal** |
| **Voltage Unbalance Factor (VUF)** | 1.8% | < 2.0% (ANSI C84.1) | -10.0% | **Normal** |

---

### Visualization Triggers

**Recommended Chart**: Time-Series Line Chart illustrating the instantaneous Phase RMS voltage profile relative to IEEE 1159 sag thresholds and ANSI C84.1 limits.

```json
{
  "chart_type": "line",
  "title": "Substation Bus Voltage Profile & Mitigation Thresholds",
  "data": {
    "timestamps": ["T-30s", "T-20s", "T-10s", "T-0s", "T+10s (Projected)"],
    "measured_voltage_pu": [0.99, 0.98, 0.88, 0.88, 1.00],
    "ansi_nominal_min_pu": [0.95, 0.95, 0.95, 0.95, 0.95],
    "ansi_nominal_max_pu": [1.05, 1.05, 1.05, 1.05, 1.05]
  }
}
```

---

### Actionable Recommendations
- **Telemetry Verification**: Validate that the observed 0.88 p.u. sag is localized to the target feeder bus before committing persistent mechanical LTC tap movements.
- **Dynamic Compensation Sequence**: Execute DVR series fast-injection immediately upon approval to provide instantaneous sub-cycle voltage support while the mechanical LTC transitions steps (approx. 3–5 seconds mechanical travel time).
- **SCADA Interlocking Check**: Ensure downstream switched capacitor banks and distributed energy resources (DERs) do not counter-react to the tap adjustment.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "SCADA_VOLTAGE_CONTROL_EXECUTION",
  "tier_level": 2,
  "status": "PENDING_OPERATOR_APPROVAL",
  "target_assets": {
    "substation_id": "SUB-BAL-04",
    "feeder_id": "FDR-402",
    "ltc_controller_id": "LTC-TR-01",
    "dvr_unit_id": "DVR-FDR-402-A"
  },
  "proposed_operations": [
    {
      "sequence": 1,
      "device": "DVR-FDR-402-A",
      "command": "ENABLE_FAST_INJECTION",
      "magnitude_pu": 0.12,
      "duration_cycles": 120
    },
    {
      "sequence": 2,
      "device": "LTC-TR-01",
      "command": "STEP_CHANGE",
      "direction": "RAISE",
      "step_count": 2,
      "resulting_tap": "+2"
    }
  ],
  "safety_interlocks_cleared": true,
  "requires_hitl_confirmation": true
}
```
