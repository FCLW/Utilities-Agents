# ⚡ System Inertia Tracker

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of system inertia tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — System Inertia Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank system inertia tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.system_inertia_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the real-time synchronous grid inertia level in megawatt-seconds across the interconnect, and does it exceed NERC safety floors?"

**Agent Response:**
### Executive Summary
**Real-time synchronous grid inertia across the Interconnect is currently operating at 151,200 MW·s, which remains 16.31% above the NERC Minimum Safety Floor of 130,000 MW·s and well above the Critical Floor threshold of 100,000 MW·s.** **While current inertia levels comply with mandatory NERC BAL-003 frequency response and reliability standards, a negative rate of change (-10.27% over the past 60 minutes) has been detected due to midday thermal de-commitments and high inverter-based resource (IBR) penetration.** **System stability margins remain adequate, but proactive monitoring of the Rate of Change of Frequency (RoCoF) is warranted as peak solar displacement continues.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Synchronous Inertia ($H_{sys}$)** | 151,200 MW·s | 175,000 MW·s (Nominal Target) | -13.60% | **Normal** |
| **NERC Minimum Safety Floor** | 151,200 MW·s | 130,000 MW·s (NERC Threshold) | +16.31% | **Normal** |
| **NERC Critical Floor Limit** | 151,200 MW·s | 100,000 MW·s (Critical Min) | +51.20% | **Normal** |
| **Estimated System RoCoF (N-1 Loss of 2.7 GW)** | 0.178 Hz/s | < 0.250 Hz/s (Reliability Limit) | -28.80% | **Normal** |
| **Synchronous Kinetic Energy Ratio** | 68.4% | > 60.0% (Operational Rule) | +14.00% | **Normal** |
| **Inverter-Based Resource (IBR) Share** | 41.2% | < 50.0% (Dynamic Margin) | -17.60% | **Warning** |

---

### Visualization Triggers
**Recommended Chart**: Time-Series Multi-Line Chart tracking real-time synchronous inertia against NERC alert and trip thresholds over the past 60 minutes.

```json
{
  "chart_type": "line",
  "title": "Real-Time Interconnect Inertia vs NERC Safety Floors",
  "labels": ["T-60m", "T-45m", "T-30m", "T-15m", "Current (T-0)"],
  "datasets": [
    {
      "label": "Synchronous Grid Inertia (MW-s)",
      "data": [168500, 164200, 159800, 154100, 151200],
      "borderColor": "#2563EB",
      "fill": false
    },
    {
      "label": "NERC Minimum Safety Floor (MW-s)",
      "data": [130000, 130000, 130000, 130000, 130000],
      "borderColor": "#F59E0B",
      "borderDash": [5, 5],
      "fill": false
    },
    {
      "label": "NERC Critical Floor (MW-s)",
      "data": [100000, 100000, 100000, 100000, 100000],
      "borderColor": "#DC2626",
      "borderDash": [3, 3],
      "fill": false
    }
  ]
}
```

---

### Actionable Recommendations

* **Maintain Continuous Telemetry Polling**: Maintain 1-second PMU (Phasor Measurement Unit) telemetry streams across regional balancing authorities to detect any localized RoCoF spikes or sub-synchronous oscillations.
* **Fast Frequency Response (FFR) Readiness**: Verify that Battery Energy Storage Systems (BESS) and synthetic inertia resources with droop settings $\le 3\%$ are armed for sub-second primary frequency response in case of a largest single contingency (N-1) trip.
* **Synchronous Condenser Pre-Arming**: If synchronous inertia drops below 140,000 MW·s during afternoon peak IBR generation, pre-dispatch designated offline thermal units in synchronous condenser mode.
* **A2A Hand-off**: Forward real-time headroom and frequency damping metrics to the **Fast Frequency Response Dispatcher** and the **Dynamic Contingency Analyzer**.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze the reduction in system kinetic energy resulting from the seasonal retirement of thermal synchronous generators."

**Agent Response:**
### 1. Executive Summary
**Seasonal retirement and decommitment of thermal synchronous generation have reduced total system kinetic energy from a baseline of 224.50 GW·s to 142.80 GW·s, representing an aggregate decline of -36.39%. This reduction elevates the worst-case Rate of Change of Frequency (RoCoF) under the single largest contingency (N-1 loss of 2,750 MW) from 0.32 Hz/s to 0.64 Hz/s, narrowing the operational margin above the critical inertia floor (135.00 GW·s) to just +5.78%. Urgent deployment of synchronous condensers and Fast Frequency Response (FFR) / Grid-Forming (GFM) inverter reserves is required to prevent frequency nadir violations prior to the activation of Under-Frequency Load Shedding (UFLS) Step 1.**

---

### 2. Quantitative System Inertia & Dynamic Stability Metrics

$$\text{System Kinetic Energy } (E_k) = \sum_{i=1}^{N} H_i \cdot S_{n,i} \quad \text{and} \quad \text{Initial RoCoF} = \left. \frac{df}{dt} \right|_{t=0^+} = \frac{f_0 \cdot \Delta P}{2 \cdot E_k}$$

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Online Synchronous Capacity ($S_n$)** | 34,250 MVA | 52,800 MVA | -35.13% | **Warning** |
| **System Kinetic Energy ($E_k$)** | 142.80 GW·s | 224.50 GW·s | -36.39% | **Warning** |
| **System Inertia Constant ($H_{sys}$)** | 3.12 s | 4.25 s | -26.59% | **Warning** |
| **Critical Inertia Margin Above Floor** | +7.80 GW·s | +89.50 GW·s | -91.28% | **Critical** |
| **Initial RoCoF (N-1 Contingency: 2,750 MW)** | 0.64 Hz/s | $\le$ 0.40 Hz/s | +60.00% | **Critical** |
| **Projected Frequency Nadir (N-1)** | 59.38 Hz | $\ge$ 59.50 Hz | -0.20% | **Critical** |
| **UFLS Stage 1 Clearance Margin** | 0.08 Hz | $\ge$ 0.30 Hz | -73.33% | **Critical** |

---

### 3. Visualization Configuration

```json
{
  "chart_type": "line",
  "title": "System Kinetic Energy Degradation & RoCoF Trend by Season",
  "xAxis": {
    "type": "category",
    "data": ["Pre-Retirement Base", "Spring Shoulder", "Summer Peak", "Fall Shoulder", "Winter Post-Retirement"]
  },
  "yAxis": [
    {"type": "value", "name": "Kinetic Energy (GW·s)", "min": 100, "max": 250},
    {"type": "value", "name": "Max RoCoF (Hz/s)", "min": 0.0, "max": 1.0}
  ],
  "series": [
    {
      "name": "System Kinetic Energy (GW·s)",
      "type": "line",
      "yAxisIndex": 0,
      "data": [224.5, 168.2, 192.4, 154.1, 142.8]
    },
    {
      "name": "Critical Inertia Floor (GW·s)",
      "type": "line",
      "yAxisIndex": 0,
      "data": [135.0, 135.0, 135.0, 135.0, 135.0],
      "lineStyle": {"type": "dashed", "color": "#d9534f"}
    },
    {
      "name": "Max Calculated RoCoF (Hz/s)",
      "type": "line",
      "yAxisIndex": 1,
      "data": [0.32, 0.49, 0.41, 0.58, 0.64]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Procure Fast Frequency Response (FFR)**: Contract a minimum of 450 MW of sub-second battery energy storage system (BESS) primary frequency response (droop $\le 2.0\%$, response time $\le 200\text{ ms}$) to arrest RoCoF during the initial post-contingency transient.
- **Convert Retired Units to Synchronous Condensers**: Prioritize declutched operation / synchronous condenser conversion at decommissioned high-MVA thermal stations to restore physical $H$ without generating active power ($P$).
- **Update Dynamic Stability Floor Constraints**: Enforce a minimum commitment constraint of 150.00 GW·s in day-ahead security-constrained unit commitment (SCUC) engines to maintain safe compliance under NERC BAL-003 standards.
- **Tune Synthetic Inertia / GFM Inverters**: Mandate grid-forming control modes (virtual synchronous machine / droop-based GFM) on interconnecting Inverter-Based Resources (IBRs) across low-inertia zones.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "GRID_STABILITY_COMMITMENT_OVERRIDE",
  "domain": "Grid Balancing / System Inertia Tracker",
  "payload": {
    "target_zone": "ALL_ZONES_INTERTIE",
    "action": "ENFORCE_MINIMUM_INERTIA_CONSTRAINT",
    "proposed_floor_gws": 150.0,
    "contingency_reserve_mw": 2750,
    "required_sync_condenser_starts": 2,
    "approval_required": "Chief System Operator / Human-in-the-Loop"
  }
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue a directive to synchronize two idle gas turbines in synchronous condenser mode to bolster system kinetic inertia."

**Agent Response:**
### Executive Summary
**Current system kinetic inertia has degraded to 124.8 GW·s, falling below the mandatory operational floor of 135.0 GW·s due to displacement of synchronous generation by inverter-based resources. Synchronizing two idle combustion turbines in Synchronous Condenser Mode will contribute an estimated +33.7 GW·s of physical rotational inertia ($H$-constant equivalent), successfully restoring grid stability and RoCoF containment margins. In accordance with utility safety mandates, this physical grid modification constitutes a Tier 2 action requiring Human-in-the-Loop (HITL) operator confirmation before command execution.**

---

### Quantitative Telemetry & Impact Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **System Kinetic Inertia** | 124.8 GW·s | 135.0 GW·s (Min Floor) | -7.56% | **Critical** |
| **Projected Post-Sync Inertia** | 158.5 GW·s | 135.0 GW·s (Min Floor) | +17.41% | **Normal** |
| **Max Projected RoCoF (N-1)** | 0.68 Hz/s | < 0.50 Hz/s | +36.00% | **Warning** |
| **Post-Sync RoCoF (N-1)** | 0.39 Hz/s | < 0.50 Hz/s | -22.00% | **Normal** |
| **Unit 1 Inertia Contribution** | 0.0 GW·s (Idle) | 16.8 GW·s | N/A | **Warning** |
| **Unit 2 Inertia Contribution** | 0.0 GW·s (Idle) | 16.9 GW·s | N/A | **Warning** |

---

### Visualization Trigger
**Chart Recommendation**: Time-Series Line Chart illustrating dynamic system kinetic inertia degradation against the NERC/Regional Reliability Coordinator minimum operational floor, with the projected recovery trajectory post-synchronization.

```json
{
  "chart_type": "line",
  "title": "System Kinetic Inertia Trajectory & Synchronous Condenser Impact",
  "xAxis": "Time Interval",
  "yAxis": "Kinetic Inertia (GW·s)",
  "data": {
    "labels": ["T-15m", "T-10m", "T-5m", "Current (T0)", "T+5m (Projected)", "T+10m (Post-Sync)"],
    "series": [
      {
        "name": "System Kinetic Inertia",
        "values": [142.5, 138.2, 130.4, 124.8, 124.0, 158.5]
      },
      {
        "name": "Minimum Inertia Floor",
        "values": [135.0, 135.0, 135.0, 135.0, 135.0, 135.0]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Dispatch Order Preparation**: Prepare start and clutch-engagement sequence commands for Unit GT-1 and Unit GT-2 at the designated balancing substation.
- **Auxiliary System Verification**: Confirm de-watered/de-coupled combustor state and lube oil pressure readiness prior to clutch engagement.
- **Automatic Generation Control (AGC) Coordination**: Maintain zero active power setpoint ($P = 0\text{ MW}$) while enabling Automatic Voltage Regulation (AVR) for reactive power and voltage support ($Q$ control).
- **Execution**: Await human dispatcher sign-off on the Tier 2 confirmation block below to transmit SCADA closing directives.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_GRID_DEVICE_CONTROL",
  "subsystem": "GENERATION_DISPATCH_AND_BALANCING",
  "risk_level": "TIER_2_CRITICAL",
  "target_assets": [
    {
      "asset_id": "GEN-GT-01",
      "substation_id": "SUB-NORTH-500KV",
      "target_mode": "SYNCHRONOUS_CONDENSER",
      "target_mw_setpoint": 0.0,
      "estimated_inertia_addition_gws": 16.8
    },
    {
      "asset_id": "GEN-GT-02",
      "substation_id": "SUB-NORTH-500KV",
      "target_mode": "SYNCHRONOUS_CONDENSER",
      "target_mw_setpoint": 0.0,
      "estimated_inertia_addition_gws": 16.9
    }
  ],
  "reason": "Restore total system kinetic inertia above the 135.0 GW·s reliability compliance threshold to suppress Rate of Change of Frequency (RoCoF).",
  "operator_action_required": "CONFIRM_SYNCHRONIZATION_DIRECTIVE",
  "timestamp_utc": "AUTO_SCADA_DISPATCH_PENDING_APPROVAL"
}
```
