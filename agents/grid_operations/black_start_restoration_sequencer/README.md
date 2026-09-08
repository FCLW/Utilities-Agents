# ⚡ Black Start Restoration Sequencer

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of black start restoration sequencer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Black Start Restoration Sequencer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank black start restoration sequencer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.black_start_restoration_sequencer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the prioritized restoration path from the Black Start Hydro Station to energize the auxiliary loads of Plant Bravo?"

**Agent Response:**
### Executive Summary
**The primary cranking path from Black Start Hydro Station to Plant Bravo is validated and clear for auxiliary load energization.** **System frequency stability and reactive power margins (MVAR absorption limits) on the intermediate 230kV/115kV transmission corridors are within NERC EOP-005 operating criteria.** **Immediate human-in-the-loop (HITL) authorization is required to initiate sequential line charging and breaker closure across designated substations.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Black Start Source Capacity (Hydro)** | 120.0 MW | 100.0 MW (Min Required) | +20.0% | Normal |
| **Plant Bravo Cranking Power Demand** | 35.0 MW | 35.0 MW | 0.0% | Normal |
| **Path Line Charging Reactive Power** | 22.4 MVAR | < 30.0 MVAR (Hydro Limit) | -25.3% | Normal |
| **Voltage Profile (230kV / 115kV Segments)** | 1.02 p.u. | 0.95 – 1.05 p.u. | 0.0% | Normal |
| **Isochronous Governor Frequency Buffer** | 60.05 Hz | 59.80 – 60.20 Hz | +0.08% | Normal |
| **Estimated Time to Auxiliary Energization** | 24.0 min | 30.0 min (Max Threshold) | -20.0% | Normal |

---

### Prioritized Restoration Sequence

1. **Step 1: Island Generation Stabilization (Black Start Hydro Station)**
   - Verify Black Start Hydro Unit 1 is running in isochronous control mode at 1.0 p.u. terminal voltage and 60.0 Hz.
   - Confirm hydro station house load is fully supported.
2. **Step 2: Energize 230kV Transmission Bus & Line Segments**
   - Connect line reactor shunt banks at Substation Alpha to mitigate Ferranti effect voltage rise.
   - Close Breaker `CB-2301` at Hydro Station to energize Corridor `TL-230-HB` to Substation Alpha.
3. **Step 3: Substation Alpha Step-Down Transformation**
   - Energize 230/115kV Transformer Bank `T-1` at Substation Alpha on open-circuit secondary.
   - Confirm 115kV bus voltage is regulated within 0.98–1.02 p.u.
4. **Step 4: Energize 115kV Cranking Tie to Plant Bravo**
   - Close Breaker `CB-1154` at Substation Alpha to energize radial feeder `TL-115-PB` into Plant Bravo switchyard.
   - Verify sync check and dead-bus interlocks are satisfied.
5. **Step 5: Pick Up Plant Bravo Auxiliary Loads**
   - Energize Plant Bravo Station Service Transformer `SST-1`.
   - Step-pick high-priority thermal auxiliaries (boiler feed pumps, lube oil systems, draft fans) in staged blocks (< 8 MW increments) to prevent frequency excursions beyond ±0.5 Hz.

---

### Visualization

```json
{
  "chart_type": "bar",
  "title": "Black Start Cranking Path Power & Dynamic Capability",
  "labels": [
    "Hydro Gen Available",
    "TL-230-HB Path Loss/Margin",
    "Substation Alpha Bus",
    "TL-115-PB Cranking Path",
    "Plant Bravo Aux Load Target"
  ],
  "datasets": [
    {
      "label": "MW Capacity / Load Requirement",
      "data": [120, 115, 110, 105, 35]
    }
  ]
}
```

---

### Actionable Recommendations

- **Confirm Shunt Reactor Readiness**: Ensure inductive compensation at Substation Alpha is in service prior to energizing `TL-230-HB` to prevent overvoltage tripping.
- **Enforce Block Loading Constraints**: Coordinate with Plant Bravo operations to stage auxiliary load pickup in increments not exceeding 8.0 MW with 90-second settling intervals.
- **Maintain Telemetry Vigilance**: Continuously poll SCADA telemetry along the hydro-to-thermal corridor for Phase Angle, Frequency, and Voltage limits per NERC EOP-005.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "GRID_SWITCHING_EXECUTION",
  "authorization_level": "TIER_2_OPERATOR_DISPATCH",
  "protocol": "NERC_EOP_005_BLACK_START",
  "target_assets": [
    {"asset_id": "CB-2301", "location": "BS_Hydro_Station", "command": "CLOSE", "description": "Energize 230kV Corridor TL-230-HB"},
    {"asset_id": "XFMR-T1", "location": "Substation_Alpha", "command": "ENERGIZE", "description": "Energize 230/115kV Transformer Bank"},
    {"asset_id": "CB-1154", "location": "Substation_Alpha", "command": "CLOSE", "description": "Energize Cranking Line TL-115-PB to Plant Bravo"},
    {"asset_id": "CB-SST1", "location": "Plant_Bravo", "command": "CLOSE", "description": "Energize Station Service Transformer SST-1"}
  ],
  "requires_hitl_approval": true,
  "safety_interlocks_verified": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Simulate crank path transmission line energization to verify that capacitive Ferranti rise does not cause overvoltage flashovers."

**Agent Response:**
### 1. Executive Summary
**Steady-state and electromagnetic transient simulation of the 120-mile, 230 kV primary crank path reveals that uncompensated no-load energization generates a severe Ferranti voltage rise of 1.134 pu (260.8 kV), exceeding the 1.10 pu temporary overvoltage (TOV) threshold and threatening insulation flashover at the target cranking terminal. By placing the 35 MVAR line-end shunt reactor into service prior to breaker closure, the receiving-end voltage rise is suppressed to 1.032 pu (237.4 kV), safely within the 1.05 pu continuous operating limit. Black start generator reactive power absorption is maintained at 9.8 MVAR, well within the 30.0 MVAR underexcited stability limit required under NERC EOP-005 restoration protocols.**

---

### 2. Data Presentation: Crank Path Energization & Ferranti Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Sending End Bus Voltage ($V_s$)** | 1.000 pu (230.0 kV) | 1.000 pu (230.0 kV) | 0.0% | Normal |
| **Uncompensated Open-End Voltage ($V_r$)** | 1.134 pu (260.8 kV) | 1.050 pu (241.5 kV) | +8.0% | Critical |
| **Compensated Open-End Voltage ($V_r$)** | 1.032 pu (237.4 kV) | 1.050 pu (241.5 kV) | -1.7% | Normal |
| **Line Charging Reactive Power ($Q_c$)** | 44.8 MVAR | 30.0 MVAR (BS Unit Cap) | +49.3% | Critical |
| **Net BS Unit Reactive Burden (Compensated)** | 9.8 MVAR (Absorption) | 30.0 MVAR (Absorption Limit) | -67.3% | Normal |
| **Peak Switching Surge Overvoltage ($V_{peak}$)** | 1.220 pu (280.6 kV) | 1.450 pu (TOV/BIL Limit) | -15.9% | Normal |
| **Frequency Stability Impact ($\Delta f$)** | +0.08 Hz | $\pm 0.50$ Hz Limit | -84.0% | Normal |

---

### 3. Visualization Triggers
- **Recommended Chart**: Multi-Series Time/Distance Voltage Profile Line Chart.
- **Rendered Output**:

```json
{
  "title": "Crank Path Voltage Profile vs Distance (Ferranti Effect)",
  "xAxis": {
    "name": "Distance from Black Start Source (miles)",
    "categories": [
      "0 mi (BS Source)",
      "30 mi (Sub Alpha)",
      "60 mi (Tap 1)",
      "75 mi (Sub Beta)",
      "100 mi (Tap 2)",
      "120 mi (Crank Target Bus)"
    ]
  },
  "series": [
    {
      "name": "Uncompensated Voltage (pu)",
      "data": [1.000, 1.018, 1.045, 1.062, 1.095, 1.134]
    },
    {
      "name": "Compensated w/ 35 MVAR Shunt Reactor (pu)",
      "data": [1.000, 1.005, 1.012, 1.018, 1.025, 1.032]
    },
    {
      "name": "Continuous Voltage Limit (1.05 pu)",
      "data": [1.050, 1.050, 1.050, 1.050, 1.050, 1.050]
    },
    {
      "name": "Temporary Overvoltage Limit (1.10 pu)",
      "data": [1.100, 1.100, 1.100, 1.100, 1.100, 1.100]
    }
  ]
}
```

---

### 4. Actionable Recommendations

1. **Pre-Energization Reactor Staging**: Lock in the 35 MVAR tertiary/bus shunt reactor at the target cranking terminal before closing the primary transmission line breaker at the Black Start source.
2. **AVR Setpoint Pre-Adjustment**: Adjust the Black Start excitation system Automatic Voltage Regulator (AVR) setpoint to 0.980 pu (225.4 kV) prior to line closure to introduce additional voltage headroom during initial charging.
3. **Synchronous Breaker Closing**: Ensure point-on-wave (POW) switching or pre-insertion resistors (PIR) are active on Breaker `CB-230-01` to mitigate transient switching overvoltage peaks below 1.25 pu.
4. **Intermediate Section Energization**: If the shunt reactor is unavailable, segment energization via Substation Alpha (30 mi) and Substation Beta (75 mi) to energize localized station service auxiliary loads before extending the path.

---

### 5. Tier 2 Human-in-the-Loop Payload

```json
[TIER 2 ACTION REQUIRED]
{
  "operation_type": "GRID_SWITCHING_EXECUTION",
  "authority_level": "TRANSMISSION_DISPATCHER_APPROVAL",
  "compliance_standard": "NERC EOP-005-3 / System Restoration",
  "actions": [
    {
      "step": 1,
      "device_id": "RE-230-01",
      "location": "Target Cranking Station Substation",
      "action": "CLOSE",
      "target_state": "35 MVAR Shunt Reactor IN_SERVICE"
    },
    {
      "step": 2,
      "device_id": "BS-AVR-01",
      "location": "Black Start Generation Facility",
      "action": "SET_VOLTAGE_REFERENCE",
      "target_state": "0.980 pu (225.4 kV)"
    },
    {
      "step": 3,
      "device_id": "CB-230-01",
      "location": "Black Start Switchyard 230 kV",
      "action": "CLOSE",
      "target_state": "LINE_ENERGIZED_TO_TARGET_BUS"
    }
  ],
  "safety_interlocks_verified": true,
  "ferranti_mitigation_verified": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Authorize energization of the 138kV Black Start crank path from Unit 1 to Substation Center under strict island control."

**Agent Response:**
### Executive Summary
**The 138kV Black Start crank path from Unit 1 to Substation Center has undergone automated pre-energization electrical validation and line-charging reactive power balance checks. All pre-conditions for dead-bus energization under island control are technically verified within NERC EOP-005 and IEEE restoration standards. Because closing transmission breakers into a de-energized crank path alters the physical state of the bulk electric system, this operation cannot be executed autonomously and requires mandatory Human-in-the-Loop (HITL) Tier 2 authorization.**

---

### Data Presentation (Crank Path & Island Telemetry Verification)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Unit 1 Terminal Voltage** | 13.80 kV | 13.80 kV | 0.00% | Normal |
| **Isochronous Island Frequency** | 60.01 Hz | 60.00 Hz | +0.02% | Normal |
| **138kV Crank Path Charging MVAR** | 14.20 MVAR | 15.00 MVAR (Max absorption limit: 28 MVAR) | -5.33% | Normal |
| **Substation Center Bus Voltage (Pre-close)**| 0.00 kV (Dead-Bus) | 0.00 kV (Dead-Bus) | 0.00% | Normal |
| **Ferranti Voltage Rise Margin** | 1.04 p.u. | ≤ 1.05 p.u. | -0.95% | Normal |
| **Available Unit 1 Spinning Reserve** | 45.0 MW | ≥ 25.0 MW (Step load buffer) | +80.00% | Normal |

---

### Visualization Trigger
**Recommended Visualization:** Time-Series Profile — *Restoration Step Transient Dynamics (Voltage, Frequency, and Reactive Loading)*

```json
{
  "chart_type": "line",
  "title": "Crank Path Energization Sequence Transient Profile",
  "data": {
    "labels": ["T+0s (Unit 1 Idle)", "T+30s (Field Flash/Gen 13.8kV)", "T+60s (GSU Energization)", "T+90s (138kV Line Charging)", "T+120s (Sub Center Dead-Bus Close)"],
    "datasets": [
      {
        "label": "Voltage (p.u.)",
        "data": [0.0, 1.0, 0.98, 1.04, 1.02]
      },
      {
        "label": "Frequency (Hz)",
        "data": [0.0, 60.0, 59.95, 60.05, 60.01]
      },
      {
        "label": "Reactive Power (MVAR Charging)",
        "data": [0.0, 0.0, 2.1, 14.2, 14.5]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Maintain Isochronous Control:** Verify Unit 1 governor is locked in Isochronous mode with fast-valving response active to absorb line-charging transient capacitive surges.
- **Verify Breaker Disconnects:** Confirm Substation Center radial feeder breakers (Breakers 102, 104, 106) remain physically open and tagged out prior to main line breaker closure to prevent cold load pickup surge.
- **Arm Synchronism/Dead-Bus Check Relay:** Set Substation Center Breaker 100 to "Dead-Bus / Live-Line" close permission mode.
- **Execute Step 1 Switching via HITL Approval:** Submit and authorize the Tier 2 switching command payload below to initiate physical close.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_GRID_SWITCHING",
  "path_id": "PATH-138KV-UNIT1-SUBCENTER",
  "substation_id": "SUB-CENTER-138",
  "target_device": "BREAKER-138-100",
  "command": "CLOSE_DEAD_BUS",
  "interlocks_cleared": true,
  "telemetry_synced": true,
  "required_approver": "Transmission Dispatcher / Senior Grid Operator",
  "compliance_reference": "NERC EOP-005-3 / Black Start Restoration Plan Section 4.2",
  "safety_status": "PENDING_OPERATOR_CONFIRMATION"
}
```
