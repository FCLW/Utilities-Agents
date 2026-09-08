# ⚡ Grid Frequency Deviation Monitor

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of grid frequency deviation monitor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Grid Frequency Deviation Monitor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank grid frequency deviation monitor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.grid_frequency_deviation_monitor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did the bulk power system frequency drop below the 59.95 Hz Governor Deadband threshold during the generator trip event?"

**Agent Response:**
### Executive Summary
**A query against real-time telemetry and historian records returned `INSUFFICIENT DATA` to verify the exact millihertz frequency excursion nadir for the specific generator trip event. In accordance with NERC BAL-003-2 standards, a drop below the 59.95 Hz Governor Deadband (±0.05 Hz / ±50 mHz threshold from 60.000 Hz nominal) requires mandatory Primary Frequency Response (PFR) governor deployment. High-speed Phasor Measurement Unit (PMU) and Substation Fault Recorder telemetry must be ingested to validate if the frequency nadir breached 59.95 Hz and evaluate subsequent governor response.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Grid Frequency Nadir ($f_{nadir}$)** | **INSUFFICIENT DATA** | $60.000\text{ Hz}$ | N/A | **Warning** |
| **Governor Deadband Threshold** | $59.950\text{ Hz}$ | $59.950\text{ Hz}$ | $0.00\%$ | **Critical** (Trigger Threshold) |
| **Primary Frequency Response (PFR)** | **INSUFFICIENT DATA** | Active past deadband | N/A | **Warning** |
| **Rate of Change of Frequency (RoCoF)** | **INSUFFICIENT DATA** | $< 0.100\text{ Hz/s}$ | N/A | **Warning** |
| **Asset Health Index (AHI)** | $88.50$ | $100.00$ | $-11.50\%$ | **Normal** |

---

### Visualization Triggers
A **Time-Series Line Chart** is recommended to plot the high-resolution (30–60 samples/sec PMU) frequency trajectory against the 59.95 Hz Governor Deadband threshold and the nominal 60.00 Hz baseline.

```json
{
  "chart_type": "line",
  "title": "BPS Frequency Trajectory vs. Governor Deadband (59.95 Hz)",
  "xAxis": {
    "label": "Time (Seconds Relative to Event t=0)",
    "unit": "s"
  },
  "yAxis": {
    "label": "Frequency",
    "unit": "Hz",
    "min": 59.85,
    "max": 60.05
  },
  "thresholds": [
    { "name": "Nominal Target", "value": 60.00, "color": "#2ECC71" },
    { "name": "Governor Deadband (59.95 Hz)", "value": 59.95, "color": "#E74C3C" },
    { "name": "UFLS Stage 1 Threshold", "value": 59.50, "color": "#9B59B6" }
  ]
}
```

---

### Actionable Recommendations
- **Ingest PMU/Synchrophasor Event Data**: Extract synchronous sub-second PMU archives (IEEE C37.118 format) for the 60-second window encompassing the generator trip to definitively determine if frequency breached 59.95 Hz.
- **Audit Governor Response (NERC BAL-003)**: If the frequency dropped below 59.95 Hz, calculate the Frequency Response Measure (FRM) and verify that all online generating units delivered their required droop curve response (3–5% droop setting).
- **Coordinate with Balancing Authority (BA)**: Review Area Control Error (ACE) and Spinning Reserve deployment times to ensure secondary frequency control (AGC) restored the system back within normal operating limits (60.000 Hz ± 0.020 Hz).

### Example 2: Trend & Comparative Analysis
**User:** "Analyze the rate of change of frequency (RoCoF) over the first 500 milliseconds following the 1,200 MW nuclear plant trip."

**Agent Response:**
### 1. Executive Summary
**Following the sudden loss of 1,200 MW from the nuclear unit trip, the grid experienced an initial Rate of Change of Frequency (RoCoF) of -0.240 Hz/s over the critical 0–500 ms inertial extraction window, driving system frequency from 60.000 Hz down to 59.880 Hz.** **Synchronous system inertia ($H_{sys} \approx 3.5\text{ s}$) arrested immediate frequency collapse prior to the onset of primary governor response, preventing premature Under-Frequency Load Shedding (UFLS Stage 1: 59.500 Hz).** **Fast Frequency Response (FFR) and synthetic inertia resources must maintain immediate readiness to arrest frequency nadir degradation before secondary contingency reserve exhaustion.**

---

### 2. Data Presentation

$$\text{RoCoF } \left(\frac{df}{dt}\right) = -\frac{f_0 \cdot \Delta P_{loss}}{2 \cdot H_{sys} \cdot S_{sys}}$$

*Analysis Parameters: $f_0 = 60.00\text{ Hz}$, Contingency $\Delta P = 1,200\text{ MW}$, Interconnection Base $S_{sys} = 42,850\text{ MVA}$, Equivalent Inertia Constant $H_{sys} = 3.50\text{ s}$.*

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Initial Pre-Trip Frequency ($f_0$)** | 60.000 Hz | 60.000 Hz | 0.00% | Normal |
| **Frequency at $t = 500\text{ ms}$ ($f_{500\text{ms}}$)** | 59.880 Hz | 60.000 Hz | -0.20% | Warning |
| **Initial RoCoF (0–100 ms)** | -0.240 Hz/s | 0.000 Hz/s | N/A | Critical |
| **Average RoCoF (0–500 ms)** | -0.239 Hz/s | > -0.100 Hz/s | +139.00% | Critical |
| **System Kinetic Energy Extracted ($\Delta E_k$)** | 585.6 MJ | 0.0 MJ | N/A | Warning |
| **Frequency Margin to UFLS Stage 1 (59.50 Hz)** | +0.380 Hz | +0.500 Hz | -24.00% | Warning |
| **Area Control Error (ACE)** | -1,200 MW | 0 MW | N/A | Critical |

---

### 3. Visualization Triggers
**Recommended Visualization**: High-Resolution Time-Series Multi-Axis Line Chart (Tracking Frequency Decay vs. Instantaneous RoCoF over the 0–500 ms sub-second window).

```json
{
  "chart_type": "line",
  "title": "Sub-Second Post-Trip Frequency & RoCoF Dynamics (0 - 500 ms)",
  "xAxis": {
    "title": "Time Post-Contingency (ms)",
    "categories": ["0 ms", "100 ms", "200 ms", "300 ms", "400 ms", "500 ms"]
  },
  "yAxis": [
    {
      "title": "Frequency (Hz)",
      "min": 59.80,
      "max": 60.05
    },
    {
      "title": "RoCoF (Hz/s)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Frequency (Hz)",
      "data": [60.000, 59.976, 59.952, 59.928, 59.904, 59.880],
      "color": "#1f77b4"
    },
    {
      "name": "Instantaneous RoCoF (Hz/s)",
      "data": [-0.240, -0.240, -0.240, -0.239, -0.238, -0.235],
      "color": "#d62728"
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Verify Fast Frequency Response (FFR) & BESS Inverter Response**: Confirm immediate full-power active injection ($\le 250\text{ ms}$ response time) from grid-scale Battery Energy Storage Systems (BESS) to support inertial containment.
- **Monitor Primary Frequency Response (PFR) Delivery**: Track governor response across thermal and hydro spinning reserve assets transitioning between $t = 500\text{ ms}$ and $t = 4.0\text{ s}$ to arrest frequency nadir above 59.700 Hz.
- **Audit Distributed Energy Resource (DER) RoCoF Anti-Islanding Trip Thresholds**: Verify no inadvertent distributed solar PV/wind tripping occurred due to IEEE 1547 / NERC PRC-024 RoCoF ride-through settings ($|df/dt| \le 0.5\text{ Hz/s}$).
- **Initiate Contingency Reserve Deployment**: Deploy 1,200 MW of synchronized spinning and non-spinning reserves via Automatic Generation Control (AGC) / EMS dispatch to restore nominal 60.000 Hz within standard 15-minute NERC BAL-002 recovery limits.

---

### 5. HITL / Tier 2 Operations

```markdown
[TIER 2 ACTION REQUIRED]
- Operation Type: Manual / Secondary Contingency Reserve Activation & Fast-Start Thermal Dispatch
- Target Units: Substation Generation Fleet Balancing Group (Zones 1-4)
- Capacity to Dispatch: 1,200 MW Contingency Operating Reserves (Spinning / Quick-Start)
- Reason: Balance Area Control Error (ACE = -1,200 MW) and recover interconnection frequency back to 60.000 Hz post-nuclear trip under NERC BAL-002-3 compliance.
- Human Approval Required: Real-Time Balancing Authority Chief System Operator confirmation required to commit physical generation re-dispatch.
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Deploy 50 MW of fast frequency response from utility battery assets to arrest declining grid frequency."

**Agent Response:**
### Executive Summary
**Grid frequency telemetry indicates an active under-frequency event requiring immediate Fast Frequency Response (FFR) to stabilize the interconnection. Autonomous physical dispatch of utility Battery Energy Storage Systems (BESS) is strictly prohibited under safety guardrails without human authorization. A 50 MW FFR discharge sequence has been staged and requires immediate Human-in-the-Loop (HITL) operational sign-off.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Grid Frequency** | 59.82 Hz | 60.00 Hz | -0.30% | **Critical** |
| **Rate of Change of Frequency (RoCoF)** | -0.045 Hz/s | 0.000 Hz/s | N/A | **Critical** |
| **BESS Fleet State of Charge (SoC)** | 84.5% | ≥ 50.0% | +34.5% | **Normal** |
| **Available Fast Frequency Capacity** | 72.0 MW | 50.0 MW (Required) | +44.0% | **Normal** |
| **Fleet Inverter Response Latency** | < 120 ms | ≤ 250 ms | -52.0% | **Normal** |

---

### Visualization Triggers

**Recommended Chart Type:** Time-Series Line Chart (Frequency Trajectory vs. FFR Trigger Thresholds)

```json
{
  "chart_type": "line",
  "title": "Grid Frequency Deviation & FFR Response Profile",
  "data": [
    {"timestamp": "14:02:00", "frequency_hz": 60.00, "trigger_threshold_hz": 59.85},
    {"timestamp": "14:02:05", "frequency_hz": 59.94, "trigger_threshold_hz": 59.85},
    {"timestamp": "14:02:10", "frequency_hz": 59.88, "trigger_threshold_hz": 59.85},
    {"timestamp": "14:02:15", "frequency_hz": 59.82, "trigger_threshold_hz": 59.85},
    {"timestamp": "14:02:20", "frequency_hz": 59.82, "trigger_threshold_hz": 59.85}
  ],
  "x_axis": "timestamp",
  "y_axis": "frequency_hz"
}
```

---

### Actionable Recommendations

* **Authorize FFR Dispatch:** Human operator must review and confirm the 50 MW BESS discharge command via the HITL console.
* **Monitor RoCoF Stabilization:** Verify that frequency decay arrests within 500 ms of inverter ramp-up and recovers toward the 59.95 Hz deadband.
* **Prepare Secondary Reserves:** Alert Spinning Reserve / Automatic Generation Control (AGC) units to sustain balancing as BESS bridges the initial transient.
* **Track Inverter Thermal Loads:** Monitor battery module temperature and state-of-health metrics during the 50 MW sustained burst.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_id": "ACT-FFR-BESS-50MW-DISPATCH",
  "action_type": "PHYSICAL_GRID_CONTROL",
  "subsystem": "Fast Frequency Response / Battery Energy Storage System",
  "target_assets": [
    {
      "asset_group": "Utility BESS Fleet - Zone 1 & 2",
      "command": "DISCHARGE_ACTIVE_POWER",
      "setpoint_mw": 50.0,
      "ramp_rate_mw_per_sec": 100.0,
      "duration_minutes": 15
    }
  ],
  "safety_interlocks_verified": true,
  "requires_human_approval": true,
  "authorization_prompt": "Confirm physical execution of 50 MW Fast Frequency Response dispatch from Utility BESS assets to arrest under-frequency event (Current Frequency: 59.82 Hz)."
}
```
