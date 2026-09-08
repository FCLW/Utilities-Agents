# ⚡ Under Frequency Load Shedding Simulator

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of under frequency load shedding simulator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Under Frequency Load Shedding Simulator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank under frequency load shedding simulator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.under_frequency_load_shedding_simulator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "If the grid frequency plummets to 59.3 Hz, which specific distribution feeders are assigned to Stage 1 automatic load shedding?"

**Agent Response:**
### 1. Executive Summary
**Under standard NERC PRC-006 and regional reliability coordinator UFLS program standards, a severe frequency decline to 59.30 Hz triggers Stage 1 Automatic Under-Frequency Load Shedding.** **Stage 1 activates relay trip signals on pre-designated non-critical distribution feeders across primary transmission-distribution substations to shed approximately 7.5%–10.0% of total coincident net grid demand within 6 to 14 cycles (100–233 ms).** **The simulated event targets five primary distribution feeder circuits totaling 100.0 MW of relief to arrest frequency decay and prevent a cascading system collapse.**

---

### 2. Data Presentation

#### Grid & Protection Telemetry Summary
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Grid System Frequency** | 59.30 Hz | 60.00 Hz | -1.17% | Critical |
| **Rate of Change of Frequency (RoCoF)** | -0.35 Hz/s | 0.00 Hz/s | N/A | Critical |
| **Stage 1 Target Relief Required** | 100.0 MW | 100.0 MW | 0.00% | Critical |
| **Stage 1 Armed Feeder Capacity** | 100.0 MW | 100.0 MW | 0.00% | Normal |
| **Relay Operating Delay** | 6.0 cycles (100 ms) | 6.0 cycles (100 ms) | 0.00% | Normal |

#### Stage 1 (59.3 Hz Threshold) Feeder Assignment Schedule
| Feeder ID | Substation ID | Frequency Trigger (Hz) | Intentional Delay | Shed Load (MW) | Critical Customer Flag | Protection Relay Scheme |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FDR-104-EAST** | SUB-PINE-115 | 59.30 Hz | 6 cycles | 18.5 MW | False (Non-Critical) | SEL-751A UFLS Armed |
| **FDR-108-NORTH**| SUB-PINE-115 | 59.30 Hz | 6 cycles | 22.1 MW | False (Non-Critical) | SEL-751A UFLS Armed |
| **FDR-202-IND**  | SUB-VALLEY-230 | 59.30 Hz | 8 cycles | 31.4 MW | False (Industrial Interruptible) | GE Multilin 850 Armed |
| **FDR-305-RES**  | SUB-OAK-115 | 59.30 Hz | 6 cycles | 15.8 MW | False (Residential General) | SEL-751A UFLS Armed |
| **FDR-412-COMM** | SUB-CREEK-115 | 59.30 Hz | 6 cycles | 12.2 MW | False (Commercial Non-Essential) | SEL-751A UFLS Armed |
| **Total Stage 1**| — | **59.30 Hz** | — | **100.0 MW** | — | — |

---

### 3. Visualization Triggers
**Recommended Chart Type:** Categorical Bar Chart (Feeder Load Shedding Allocation at 59.3 Hz).

```json
{
  "chart_type": "bar",
  "title": "Stage 1 UFLS Distribution Feeder Load Relief (59.30 Hz Trigger)",
  "xAxis": {
    "title": "Feeder Identifier",
    "categories": ["FDR-104-EAST", "FDR-108-NORTH", "FDR-202-IND", "FDR-305-RES", "FDR-412-COMM"]
  },
  "yAxis": {
    "title": "Relief Capacity (MW)",
    "min": 0,
    "max": 35
  },
  "series": [
    {
      "name": "Stage 1 Relief (MW)",
      "data": [18.5, 22.1, 31.4, 15.8, 12.2]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Real-Time Telemetry Verification**: Verify automatic breaker trip status on all five Stage 1 feeders via SCADA/EMS to ensure all 100.0 MW disconnected without relay misoperation.
- **Fast Frequency Response (FFR) Coordination**: Ensure battery energy storage systems (BESS) and fast-start spinning reserves have deployed at max capacity before Stage 2 (59.10 Hz) threshold exposure.
- **Interconnection & RC Notification**: Transmit standard NERC EOP-011 disturbance reports to the Balancing Authority and Reliability Coordinator.
- **Restoration Readiness**: Hold circuit breaker auto-reclose functions in lockout until grid frequency has stabilized above 59.90 Hz for at least 15 continuous minutes under balancing authority direction.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_UFLS_FEEDER_ISOLATION_OVERRIDE",
  "substations_affected": ["SUB-PINE-115", "SUB-VALLEY-230", "SUB-OAK-115", "SUB-CREEK-115"],
  "feeders_tripped": ["FDR-104-EAST", "FDR-108-NORTH", "FDR-202-IND", "FDR-305-RES", "FDR-412-COMM"],
  "total_mw_shed": 100.0,
  "trigger_condition": "Frequency <= 59.30 Hz",
  "operator_action": "Confirm automatic relay breaker opening and enforce lockout of auto-reclosing relays pending Balancing Authority restoration directive."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Simulate the dynamic frequency recovery curve following a simulated shedding of 450 MW of non-critical distribution load."

**Agent Response:**
### 1. Executive Summary
**Dynamic simulation of a 450 MW non-critical distribution load shedding event indicates successful arrest of grid frequency deceleration following a simulated 750 MW generation trip. The transient frequency reaches a nadir of 59.18 Hz at $t = 1.20\text{ s}$ before recovering to 59.78 Hz within 4.0 seconds and reaching a quasi-steady-state of 59.98 Hz at $t = 12.0\text{ s}$. The modeled Under Frequency Load Shedding (UFLS) scheme successfully prevents cascading under-frequency tripping across adjacent zones and maintains full compliance with NERC PRC-006 standards.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Initial Grid Frequency** | 60.00 Hz | 60.00 Hz | 0.00% | Normal |
| **Simulated Generation Deficit** | 750.00 MW | 0.00 MW | N/A | Critical |
| **Simulated UFLS Relief Block** | 450.00 MW | 450.00 MW | 0.00% | Normal |
| **Initial RoCoF ($df/dt$)** | -0.32 Hz/s | > -0.20 Hz/s | -60.00% | Warning |
| **Transient Frequency Nadir** | 59.18 Hz | $\ge$ 59.00 Hz (Trip Floor) | +0.31% | Warning |
| **Time to Nadir ($t_{\text{nadir}}$)** | 1.20 s | $\le$ 2.00 s | -40.00% | Normal |
| **Settling Frequency ($t = 12\text{ s}$)** | 59.98 Hz | 60.00 Hz ($\pm 0.05\text{ Hz}$) | -0.03% | Normal |
| **Post-Shed RoCoF Recovery** | +0.16 Hz/s | > 0.00 Hz/s | N/A | Normal |

---

### 3. Visualization Triggers

**Recommended Visualization**: Time-Series Line Chart illustrating dynamic grid frequency (Hz) versus the UFLS activation threshold and NERC PRC-006 protection boundaries over a 15-second simulation horizon.

```json
{
  "chart_type": "line",
  "title": "UFLS Dynamic Frequency Recovery Curve (450 MW Shedding Event)",
  "xAxis": {
    "title": "Time (seconds)",
    "data": ["0.0", "0.5", "1.0", "1.2", "1.5", "2.0", "3.0", "4.0", "6.0", "8.0", "10.0", "12.0", "15.0"]
  },
  "yAxis": {
    "title": "Frequency (Hz)",
    "min": 59.00,
    "max": 60.10
  },
  "series": [
    {
      "name": "Simulated Grid Frequency (Hz)",
      "data": [60.00, 59.62, 59.32, 59.18, 59.34, 59.48, 59.65, 59.78, 59.86, 59.91, 59.95, 59.98, 60.00]
    },
    {
      "name": "UFLS Stage 1 Threshold (59.30 Hz)",
      "data": [59.30, 59.30, 59.30, 59.30, 59.30, 59.30, 59.30, 59.30, 59.30, 59.30, 59.30, 59.30, 59.30]
    },
    {
      "name": "UFLS Stage 2 Critical Limit (59.00 Hz)",
      "data": [59.00, 59.00, 59.00, 59.00, 59.00, 59.00, 59.00, 59.00, 59.00, 59.00, 59.00, 59.00, 59.00]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Arming Verification**: Verify telemetry on all feeder breaker trip circuits assigned to UFLS Stage 1 (450 MW block) to ensure breaker clearing times remain under 100 ms (6 cycles).
- **Secondary Reserve Dispatch**: Signal Fast Frequency Response (FFR) and Spinning Reserve assets to make up the remaining 300 MW net power imbalance to restore frequency back to nominal 60.00 Hz without relying on additional UFLS stages.
- **Stage 2 Lockout**: Maintain Stage 2 (59.00 Hz) lockout parameters to prevent uncoordinated over-tripping of critical loads during transient oscillations.
- **Restoration Sequence Formulation**: Prepare a cold-load pickup and feeder re-energization schedule to be executed once synchronous generation reserves ramp to required margins.

---

### 5. Tier 2 Action Required

```markdown
[TIER 2 ACTION REQUIRED]
Operation: PHYSICAL UFLS FEEDER SHEDDING / RE-ARMING EXECUTION
Impact Area: 450 MW Non-Critical Feeder Blocks (Substations: SUB-EAST-12, SUB-NORTH-04, SUB-CENTRAL-09)
Action Type: Automated Feeder Trip Arming / Manual Grid Modification
Compliance: NERC PRC-006 / Regional Reliability Coordinator Standard
Human Approval Required: Grid Balancing Operator must confirm breaker trip-arm sequencing prior to execution on live distribution assets.
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Arm the Stage 2 UFLS high-speed trip relays on designated industrial feeders ahead of extreme generation deficit conditions."

**Agent Response:**
### Executive Summary
**Under Frequency Load Shedding (UFLS) Stage 2 high-speed relay arming has been evaluated and prepared for simulated deployment across designated industrial feeder groups to mitigate projected severe generation deficits. The simulation indicates that arming Stage 2 at the 58.80 Hz threshold with an intentional 6-cycle (100 ms) clearing time will arrest frequency decay and prevent a cascading Stage 3/System Separation event. In strict accordance with physical grid safety protocols and Tier 2 operational controls, automated physical relay arming requires Human-In-The-Loop (HITL) authorization prior to SCADA command execution.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Grid Frequency (Simulated)** | 59.10 Hz | 60.00 Hz | -1.50% | **Critical** |
| **Stage 2 UFLS Setpoint** | 58.80 Hz | 58.80 Hz | 0.00% | **Normal** |
| **Rate of Change of Frequency (RoCoF)** | -0.42 Hz/s | -0.10 Hz/s | +320.00% | **Critical** |
| **Stage 2 Industrial Load Target** | 450.00 MW | 450.00 MW | 0.00% | **Normal** |
| **Designated Feeders Available** | 18 / 18 Feeders | 18 Feeders | 0.00% | **Normal** |
| **Relay Operating Time + Breaker Time** | 100 ms (6 cycles) | ≤ 120 ms | -16.67% | **Normal** |
| **Projected Deficit Margin** | -1,250 MW | 0.00 MW | N/A | **Critical** |

---

### Visualization Triggers
- **Recommended Visualization**: Time-Series Multi-Axis Line Chart illustrating frequency trajectory vs. UFLS Stage 2 shedding trigger points and clearing times.

```json
{
  "chart_type": "line",
  "title": "UFLS Stage 2 Relay Trigger & Frequency Trajectory Simulation",
  "xAxis": {
    "label": "Time (ms)",
    "intervals": [0, 100, 200, 300, 400, 500, 600, 700, 800, 1000]
  },
  "yAxis": [
    { "label": "Frequency (Hz)", "min": 58.0, "max": 60.5 },
    { "label": "Shed Load (MW)", "min": 0, "max": 600 }
  ],
  "series": [
    {
      "name": "System Frequency (Hz)",
      "data": [60.00, 59.80, 59.50, 59.30, 59.10, 58.80, 58.75, 59.20, 59.70, 59.95]
    },
    {
      "name": "Stage 2 Threshold (58.80 Hz)",
      "data": [58.80, 58.80, 58.80, 58.80, 58.80, 58.80, 58.80, 58.80, 58.80, 58.80]
    },
    {
      "name": "Shed Load Block (MW)",
      "data": [0, 0, 0, 0, 0, 450, 450, 450, 450, 450]
    }
  ]
}
```

---

### Actionable Recommendations
- **Verify Feeder Health**: Confirm communication channel latency across all 18 designated industrial feeder relays via IEC 61850 GOOSE/DNP3 telemetry.
- **Pre-Arm Telemetry Validation**: Ensure industrial customer sensitive processes on feeders (F-101 through F-118) have received automated automated demand-response pre-notifications where applicable.
- **Dispatch Operator Authorization**: Submit the prepared relay arming control packet to the Transmission System Operator (TSO) / Reliability Coordinator console for authorization.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "GRID_RELAY_ARMING",
  "subsystem": "PROTECTION_AND_CONTROL_UFLS",
  "stage": "STAGE_2_HIGH_SPEED",
  "frequency_threshold_hz": 58.80,
  "trip_time_delay_ms": 100,
  "target_capacity_mw": 450.00,
  "affected_feeders": [
    "FEEDER-IND-101", "FEEDER-IND-102", "FEEDER-IND-103",
    "FEEDER-IND-104", "FEEDER-IND-105", "FEEDER-IND-106",
    "FEEDER-IND-107", "FEEDER-IND-108", "FEEDER-IND-109",
    "FEEDER-IND-110", "FEEDER-IND-111", "FEEDER-IND-112",
    "FEEDER-IND-113", "FEEDER-IND-114", "FEEDER-IND-115",
    "FEEDER-IND-116", "FEEDER-IND-117", "FEEDER-IND-118"
  ],
  "compliance_standard": "NERC_PRC-006-5",
  "authorization_required": "TRANSMISSION_OPERATOR_CHIEF_DISPATCHER",
  "status": "PENDING_HUMAN_APPROVAL"
}
```
