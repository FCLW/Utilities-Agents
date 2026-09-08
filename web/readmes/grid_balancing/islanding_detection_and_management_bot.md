# ⚡ Islanding Detection And Management Bot

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of islanding detection and management bot is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Islanding Detection And Management Bot Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank islanding detection and management bot events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.islanding_detection_and_management_bot_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Has an unintentional island formed on Distribution Substation 6 following the upstream transmission breaker lockout?"

**Agent Response:**
### Executive Summary
**Telemetry confirms that an active unintentional island has formed on Distribution Substation 6 following the upstream transmission breaker lockout.** **Local distributed energy resources (DERs) are sustaining energized bus voltage and frequency without utility grid synchronization, exceeding IEEE 1547 clearing time thresholds.** **Immediate intervention is required to prevent out-of-phase reclosing and equipment damage, as active anti-islanding mechanisms have failed to clear the islanded section within the mandatory 2.0-second window.**

---

### Quantitative Telemetry & Islanding Assessment

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Upstream Interconnect Status** | OPEN / 86 Lockout | CLOSED | N/A | **Critical** |
| **Substation Bus Voltage** | 1.14 p.u. (14.25 kV) | 1.00 p.u. (12.47 kV) | +14.0% | **Critical** |
| **System Frequency** | 61.35 Hz | 60.00 Hz | +2.25% | **Critical** |
| **Rate of Change of Frequency (ROCOF)** | +0.68 Hz/s | 0.00 Hz/s | N/A | **Critical** |
| **Synchrophasor Phase Angle Shift ($\Delta \delta$)** | 42.6° | 0.0° | N/A | **Critical** |
| **DER Active Generation Output** | 8.42 MW | 0.00 MW (Islanded) | N/A | **Critical** |
| **Feeder Aggregate Load** | 7.95 MW | 8.10 MW | -1.85% | **Warning** |
| **Active Power Mismatch ($\Delta P$)** | +0.47 MW (Surplus) | 0.00 MW | N/A | **Critical** |
| **Islanding Duration (Post-Lockout)** | > 2.85 s | < 2.00 s (IEEE 1547) | +42.5% | **Critical** |

---

### Visualization Triggers

A **Time-Series Multi-Axis Line Chart** is recommended to evaluate the post-lockout frequency and voltage divergence leading to the runaway island condition.

```json
{
  "chart_type": "line",
  "title": "Substation 6 Post-Lockout Frequency & Voltage Trajectory",
  "xAxis": "Time (seconds post-lockout)",
  "series": [
    {
      "name": "Bus Frequency (Hz)",
      "data": [
        {"x": "-2.0s", "y": 60.00},
        {"x": "-1.0s", "y": 60.01},
        {"x": "0.0s (Lockout)", "y": 59.98},
        {"x": "0.5s", "y": 60.42},
        {"x": "1.0s", "y": 60.85},
        {"x": "1.5s", "y": 61.12},
        {"x": "2.0s", "y": 61.35}
      ]
    },
    {
      "name": "Bus Voltage (p.u.)",
      "data": [
        {"x": "-2.0s", "y": 1.01},
        {"x": "-1.0s", "y": 1.00},
        {"x": "0.0s (Lockout)", "y": 0.98},
        {"x": "0.5s", "y": 1.05},
        {"x": "1.0s", "y": 1.08},
        {"x": "1.5s", "y": 1.11},
        {"x": "2.0s", "y": 1.14}
      ]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Block Automatic Reclosing Immediately**: Inhibit any automatic reclosing schemes on the upstream transmission line and substation feeder breakers to eliminate catastrophic out-of-phase reclosing risks.
2. **Execute Direct Transfer Trip (DTT)**: Dispatch transfer trip signals to all registered DER inverters, solar farms, and battery energy storage systems (BESS) on Feeders 601, 602, and 603.
3. **Dispatch Distribution Field Operations**: Alert local field crews that Substation 6 feeders remain energized from downstream sources despite upstream transmission isolation.
4. **Isolate Substation Feeders**: If DTT fails to decouple DER generation within standard clearing margins, sequentially open feeder circuit breakers at Substation 6 to de-energize the island safely.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_GRID_CONTROL",
  "target_substation": "Distribution Substation 6",
  "proposed_operations": [
    {
      "device_id": "RECLOSER_CTRL_T6",
      "command": "BLOCK_AUTO_RECLOSE",
      "urgency": "IMMEDIATE"
    },
    {
      "device_id": "DTT_SUB6_DER_GROUP",
      "command": "DIRECT_TRANSFER_TRIP_DISCONNECT",
      "target_assets": ["DER_SOLAR_601", "DER_BESS_602", "DER_SOLAR_603"],
      "urgency": "IMMEDIATE"
    },
    {
      "device_id": "CB_601_602_603",
      "command": "SEQUENTIAL_FEEDER_OPEN",
      "condition": "CONTINGENCY_IF_DTT_FAILS"
    }
  ],
  "safety_risk": "High - Unsynchronized island with overvoltage (1.14 p.u.) and frequency drift (61.35 Hz) risking public safety and catastrophic damage upon line re-energization.",
  "compliance_basis": "IEEE 1547.1 Anti-Islanding De-energization Mandate / NERC PRC-024-2",
  "requires_hitl_approval": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Verify that active anti-islanding relays (IEEE 1547) disconnected all distributed solar generators within 2.0 seconds."

**Agent Response:**
### Executive Summary
**Post-event telemetry verification confirms that 100% of distributed solar photovoltaic (PV) generation assets successfully detected unintentional island formation and disconnected within standard thresholds.** All active anti-islanding relays operating under IEEE 1547 standards achieved full circuit disconnection with a fleet-wide maximum clearing time of **1.82 seconds**, well below the mandatory **2.00-second (2000 ms)** clearing ceiling. No persistent energization, out-of-phase reclosure risk, or unmitigated micro-islands were detected across monitored feeder segments.

---

### Quantitative Performance & Compliance Verification

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Max DER Clearing Time** | `1.82 s` | `≤ 2.00 s (IEEE 1547)` | `-9.0%` (Safety Margin) | **Normal** |
| **Fleet Average Trip Duration** | `0.97 s` | `≤ 2.00 s` | `-51.5%` | **Normal** |
| **Active Solar Anti-Islanding Trip Rate** | `100.0%` (48/48 DERs) | `100.0%` | `0.0%` | **Normal** |
| **Feeder Residual Active Power Post-Trip** | `0.00 MW` | `0.00 MW` | `0.0%` | **Normal** |
| **Frequency Departure (df/dt) ROCOF Response** | `142 ms avg` | `≤ 500 ms` | `-71.6%` | **Normal** |
| **Phase Imbalance Post-Disconnection** | `0.0%` | `< 3.0%` | `-100.0%` | **Normal** |

---

### Trip Performance Telemetry by Feeder Node

```json
{
  "chart_type": "bar",
  "title": "IEEE 1547 Anti-Islanding Trip Time by Substation Feeder vs 2.0s Limit",
  "xAxis": {
    "categories": ["Feeder 12A-West", "Feeder 12B-East", "Feeder 14A-North", "Feeder 14C-South", "Feeder 18-Industrial"]
  },
  "yAxis": {
    "title": "Trip Time (Seconds)",
    "max": 2.5
  },
  "series": [
    {
      "name": "Average Trip Time (s)",
      "data": [0.74, 0.92, 1.15, 0.68, 1.34]
    },
    {
      "name": "Maximum Trip Time (s)",
      "data": [1.12, 1.45, 1.68, 0.95, 1.82]
    },
    {
      "name": "IEEE 1547 Threshold Limit (s)",
      "data": [2.0, 2.0, 2.0, 2.0, 2.0],
      "type": "line",
      "dashStyle": "Dash"
    }
  ]
}
```

---

### Technical Findings & Event Details
1. **Detection Mechanisms**: Interconnected inverters utilized dual active frequency drift (AFD/sandia frequency shift) combined with passive rate-of-change-of-frequency (ROCOF) and under/over-voltage (27/59) elements.
2. **Phase Clearing Integrity**: Inverter contactors and solid-state disconnect switches verified zero current flow across all phases ($I_A = I_B = I_C = 0\text{ A}$) within the 2-second compliance window.
3. **Reclose Safety**: Automatic reclosing lockouts are active on all feeders; DER reconnection is inhibited until area electric power system (EPS) voltage and frequency remain within normal operating ranges for a minimum of 300 seconds (5 minutes) per IEEE 1547-2018 §10.7.

---

### Actionable Recommendations
- **Maintain Lockout State**: Keep inverter reconnect timers active until steady-state grid synchronism ($60.0 \pm 0.05\text{ Hz}$, nominal $\text{kV} \pm 5\%$) is re-established across all affected distribution feeders.
- **Inspect Slower Performing Units**: Dispatch a diagnostic check for Feeder 18-Industrial inverters operating near the upper boundary ($1.82\text{ s}$) to verify phase-locked loop (PLL) tuning and active perturbation settings.
- **Log Compliance Record**: Archive event telemetry package in the compliance ledger for NERC PRC / PUC distributed generation reliability audits.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Trigger an emergency trip signal to all DER inverters on Feeder 6 and de-energize the islanded distribution section."

**Agent Response:**
### Executive Summary
**Islanding detection protocols have flagged an active islanding condition on Feeder 6 requiring DER disconnection and section de-energization to maintain grid safety and adhere to IEEE 1547 / NERC standards.** 
**Autonomous physical execution of breaker trips and inverter shutdowns is restricted under Tier 2 Physical Grid Safety guardrails.** 
**A Human-In-The-Loop (HITL) confirmation payload has been generated for operator approval to execute the emergency trip sequence.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Feeder 6 Frequency (ROCOF)** | 61.42 Hz (+1.8 Hz/s) | 60.00 Hz (±0.05 Hz) | +2.37% | **Critical** |
| **Voltage Deviation (Phase A-C)** | 1.18 p.u. | 1.00 p.u. (±0.05 p.u.) | +18.00% | **Critical** |
| **Active DER Capacity on Island** | 4.85 MW | 0.00 MW (Grid Tied) | N/A | **Critical** |
| **Active Island Status** | Confirmed (Loss of Mains) | Interconnected | N/A | **Critical** |
| **Target Feeder Section** | Feeder 6 - Substation Sec 3 | Closed / Interconnected | N/A | **Warning** |

---

### Actionable Recommendations
- **Operator Action**: Review and authorize the Tier 2 emergency trip signal below to disconnect all distributed energy resources (DERs) on Feeder 6 via transfer trip / DNP3 controls.
- **Islanding Verification**: Confirm anti-islanding relay pickup and loss-of-mains (LOM) telemetry at Recloser R-604.
- **Safety Protocol**: Ensure synchronous phase matching is verified prior to any future automatic reclosing attempts.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "EMERGENCY_DER_TRIP_AND_DE_ENERGIZE",
  "feeder_id": "Feeder-06",
  "substation_id": "Substation-Sec-3",
  "target_devices": [
    "DER_INV_ALL_FEEDER_6",
    "RECLOSER_R-604"
  ],
  "command": "DIRECT_TRANSFER_TRIP",
  "safety_compliance": "IEEE 1547 / NERC PRC-024",
  "risk_level": "CRITICAL_PHYSICAL_SWITCHING",
  "status": "PENDING_OPERATOR_CONFIRMATION",
  "timestamp_utc": "2025-05-20T12:00:00Z"
}
```

*Please confirm execution to dispatch direct trip controls to all DER inverters and lock out Feeder 6 section switches.*
