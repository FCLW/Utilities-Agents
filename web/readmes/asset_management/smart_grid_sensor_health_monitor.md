# ⚡ Smart Grid Sensor Health Monitor

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of smart grid sensor health monitor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Smart Grid Sensor Health Monitor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank smart grid sensor health monitor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.smart_grid_sensor_health_monitor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which distribution line sensors on Feeder 8 are reporting anomalous battery voltage drops or lost DNP3 heartbeats?"

**Agent Response:**
### Executive Summary
**A telemetry and diagnostic audit of distribution line sensors on Feeder 8 identified two primary units (`DLS-F8-012` and `DLS-F8-045`) exhibiting severe battery voltage degradation below operating thresholds alongside intermittent to persistent DNP3 communication timeouts.** **Additionally, unit `DLS-F8-078` demonstrates early-stage power rail instability with periodic heartbeat packet loss, reducing overall telemetry reliability along the feeder.** **Immediate field inspection and energy harvester/battery replacement are required to prevent loss of situational awareness and feeder fault detection coverage.**

---

### Data Presentation

#### Telemetry Health Breakdown: Feeder 8 Line Sensors

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **DLS-F8-012 Battery Voltage** | 2.65 V | 3.60 V | -26.39% | **Critical** |
| **DLS-F8-012 DNP3 Missed Heartbeats** | 14 missed (Comms Timeout) | 0 missed | +1400.00% | **Critical** |
| **DLS-F8-012 Asset Health Index (AHI)** | 38.2 / 100 | 95.0 / 100 | -59.79% | **Critical** |
| **DLS-F8-045 Battery Voltage** | 2.78 V | 3.60 V | -22.78% | **Warning** |
| **DLS-F8-045 DNP3 Missed Heartbeats** | 8 missed (Intermittent) | 0 missed | +800.00% | **Warning** |
| **DLS-F8-045 Asset Health Index (AHI)** | 54.6 / 100 | 95.0 / 100 | -42.53% | **Warning** |
| **DLS-F8-078 Battery Voltage** | 3.10 V | 3.60 V | -13.89% | **Warning** |
| **DLS-F8-078 DNP3 Missed Heartbeats** | 2 missed (Jitter) | 0 missed | +200.00% | **Warning** |
| **DLS-F8-078 Asset Health Index (AHI)** | 72.1 / 100 | 95.0 / 100 | -24.11% | **Warning** |
| **DLS-F8-103 Battery Voltage** | 3.55 V | 3.60 V | -1.39% | **Normal** |
| **DLS-F8-103 DNP3 Missed Heartbeats** | 0 missed (Active) | 0 missed | 0.00% | **Normal** |
| **DLS-F8-103 Asset Health Index (AHI)** | 96.4 / 100 | 95.0 / 100 | +1.47% | **Normal** |

---

### Visualization Triggers

**Recommended Chart**: Multi-Metric Bar / Comparison Chart displaying current battery voltages and missed DNP3 heartbeat counts across Feeder 8 sensor nodes.

```json
{
  "chart_type": "bar",
  "title": "Feeder 8 Distribution Line Sensor Health Metrics",
  "data": {
    "labels": ["DLS-F8-012", "DLS-F8-045", "DLS-F8-078", "DLS-F8-103"],
    "datasets": [
      {
        "label": "Current Battery Voltage (V)",
        "data": [2.65, 2.78, 3.10, 3.55],
        "yAxisID": "y"
      },
      {
        "label": "Baseline Voltage (V)",
        "data": [3.60, 3.60, 3.60, 3.60],
        "yAxisID": "y"
      },
      {
        "label": "Missed DNP3 Heartbeats",
        "data": [14, 8, 2, 0],
        "yAxisID": "y1"
      }
    ]
  },
  "options": {
    "scales": {
      "y": {
        "type": "linear",
        "position": "left",
        "title": { "display": true, "text": "Voltage (V)" }
      },
      "y1": {
        "type": "linear",
        "position": "right",
        "grid": { "drawOnChartArea": false },
        "title": { "display": true, "text": "Missed Heartbeat Count" }
      }
    }
  }
}
```

---

### Actionable Recommendations

- **Dispatch Field Line Crew (Priority 1)**: Inspect sensor `DLS-F8-012` (Pole #142) for solar harvesting panel degradation, physical casing compromise, and lithium-thionyl chloride battery cell depletion.
- **Schedule Preventative Maintenance (Priority 2)**: Include `DLS-F8-045` (Pole #189) and `DLS-F8-078` (Pole #215) in the upcoming weekly feeder maintenance rotation for battery module replacement and comms antenna alignment.
- **SCADA Telemetry Polling Adjustment**: Temporarily adjust DNP3 Class 1/2/3 polling cycles to unsolicited response mode with an extended keep-alive timer to conserve remaining battery life on degraded nodes until physical servicing occurs.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FIELD_WORK_ORDER_DISPATCH",
  "target_subsystem": "DISTRIBUTION_ASSET_MAINTENANCE",
  "affected_assets": [
    {
      "sensor_id": "DLS-F8-012",
      "feeder_id": "Feeder 8",
      "location": "Pole #142",
      "urgency": "HIGH",
      "action": "REPLACE_BATTERY_AND_RF_MODULE"
    },
    {
      "sensor_id": "DLS-F8-045",
      "feeder_id": "Feeder 8",
      "location": "Pole #189",
      "urgency": "MEDIUM",
      "action": "INSPECT_HARVESTER_AND_REPLACE_BATTERY"
    }
  ],
  "estimated_crew_hours": 3.5,
  "human_approval_required": true,
  "safety_impact": "Loss of line-fault telemetry and overhead dynamic line rating (DLR) monitoring on Feeder 8 until replacement."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Analyze the packet loss rate and signal-to-noise ratio across cellular IoT fault current indicators over the past week."

**Agent Response:**
### Executive Summary
**Fleet-wide analysis of cellular IoT Fault Current Indicators (FCIs) over the past 7 days indicates overall operational stability, with an aggregate packet loss rate of 2.34% and an average Signal-to-Noise Ratio (SNR) of 19.9 dB. However, localized signal degradation and elevated packet loss (>6.5%) were identified across Feeder F-402 in Grid Zone 3 due to cellular carrier tower maintenance and fringe coverage attenuation. Immediate antenna re-alignment and carrier APN fallback verification are recommended for 18 degraded sensor nodes to prevent telemetry blind spots during distribution fault events.**

---

### Quantitative Telemetry Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Average Packet Loss Rate** | 2.34% | < 1.50% | +56.0% | **Warning** |
| **Fleet Average Signal-to-Noise Ratio (SNR)** | 19.9 dB | > 20.0 dB | -0.5% | **Normal** |
| **High-Risk Sensor Count (Packet Loss > 5%)** | 18 units | 0 units | N/A | **Warning** |
| **Critical RF Degradation (SNR < 10 dB)** | 7 units | 0 units | N/A | **Critical** |
| **Telemetry Uplink Reliability (7-Day)** | 97.66% | ≥ 99.50% | -1.85% | **Warning** |
| **Feeder F-402 (Zone 3) Peak Packet Loss** | 7.82% | < 1.50% | +421.3% | **Critical** |

---

### Localized Breakdown by Grid Zone & Feeder

| Grid Zone ID | Feeder ID | Monitored FCIs | Avg Packet Loss (%) | Avg SNR (dB) | Degraded Nodes | Asset Health Index (AHI) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zone-1 (Metro North)** | Feeder-101 | 42 | 1.12% | 24.2 dB | 0 | 96.4 (Good) |
| **Zone-1 (Metro North)** | Feeder-104 | 38 | 1.28% | 22.8 dB | 1 | 94.1 (Good) |
| **Zone-2 (Suburban East)** | Feeder-208 | 56 | 1.85% | 20.5 dB | 2 | 89.2 (Good) |
| **Zone-3 (Rural West)** | Feeder-402 | 34 | 7.82% | 11.4 dB | 12 | 68.5 (Degraded) |
| **Zone-3 (Rural West)** | Feeder-405 | 28 | 4.15% | 14.2 dB | 3 | 78.0 (Fair) |

---

### Visualization Trigger: 7-Day Cellular IoT Telemetry Profile

```json
{
  "chart_type": "line",
  "title": "7-Day Cellular IoT FCI Telemetry Health Profile",
  "data": {
    "labels": ["Day 1", "Day 2", "Day 3", "Day 4 (Storm Event)", "Day 5", "Day 6", "Day 7"],
    "datasets": [
      {
        "label": "Avg Packet Loss Rate (%)",
        "data": [1.4, 1.6, 2.1, 4.8, 3.2, 1.8, 1.5],
        "borderColor": "#EF4444",
        "yAxisID": "y1",
        "unit": "%"
      },
      {
        "label": "Avg Signal-to-Noise Ratio (dB)",
        "data": [22.4, 21.8, 20.1, 14.5, 17.2, 21.5, 22.0],
        "borderColor": "#3B82F6",
        "yAxisID": "y2",
        "unit": "dB"
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Telecommunications Fallback Verification**: Trigger remote over-the-air (OTA) diagnostic polls on the 18 flagged sensors in Feeder-402 and Feeder-405 to evaluate secondary cellular network (e.g., dual-SIM / eSIM profile failover) connectivity.
- **DNP3 / IEC 61850 Keep-Alive Adjustments**: Temporarily increase telemetry buffer depth and retransmission timeout window on Zone-3 rural nodes to mitigate transient RF fading and prevent false "Sensor Unreachable" alarms in SCADA/ADMS.
- **Physical RF Inspection Work Order**: Issue a field inspection request for Feeder-402 pole-mounted units showing SNR < 10 dB to inspect directional antenna orientation, loose coaxial pigtails, or tree canopy encroachment.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "REMOTE_OTA_CONFIG_PUSH",
  "target_asset_group": "FCI-ZONE3-FEEDER402",
  "target_sensor_count": 18,
  "action_parameters": {
    "apn_fallback_mode": "ENABLE_SECONDARY_CARRIER",
    "buffer_retries": 5,
    "transmit_power_boost_db": 2.5
  },
  "risk_assessment": "Low risk of sensor communication reboot cycle (<60s drop); requires Human-in-the-Loop (HITL) authorization before initiating fleet-wide configuration push."
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Trigger an over-the-air sensor diagnostic reboot and reassign primary telemetry routing to redundant node S-19."

**Agent Response:**
### Executive Summary
**The requested over-the-air (OTA) diagnostic reboot and telemetry route reassignment to redundant node S-19 constitutes a Tier 2 operational change affecting active grid monitoring infrastructure. Autonomous execution of control commands modifying physical or logical telemetry routing is restricted to ensure grid safety and data continuity. A human-in-the-loop (HITL) authorization payload has been generated for operator approval prior to execution.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Telemetry Node State** | Degraded / Reboot Pending | Online / Nominal | N/A | **Warning** |
| **Target Routing Node (S-19) Health** | 99.4% Availability | $\ge$ 99.0% | +0.4% | **Normal** |
| **Telemetry Latency (Pre-Switch)** | 142 ms | $\le$ 50 ms | +184.0% | **Warning** |
| **Packet Loss Rate** | 4.8% | $\le$ 0.5% | +860.0% | **Critical** |
| **Redundant S-19 Channel Signal-to-Noise (SNR)** | 28 dB | $\ge$ 20 dB | +40.0% | **Normal** |

---

### Visualization Triggers
- **Recommended Visualization**: Pre/Post Failover Telemetry Latency & Packet Error Rate (Time-Series Line Chart).
```json
{
  "chart_type": "line",
  "title": "Sensor Telemetry Latency & Error Rate Trend",
  "xAxis": "timestamp",
  "yAxis": "latency_ms",
  "series": [
    { "name": "Primary Node Latency (ms)", "data": [45, 52, 78, 110, 142] },
    { "name": "Node S-19 Standby Latency (ms)", "data": [38, 40, 39, 41, 40] }
  ]
}
```

---

### Actionable Recommendations
- **Operator Authorization**: Review and authorize the Tier 2 payload below to execute the OTA diagnostic reboot and failover sequence.
- **Failover Pre-Check**: Verify that redundant node `S-19` has completed synchronization and is ready to ingest high-frequency telemetry streams.
- **Post-Reboot Verification**: Monitor telemetry ingestion rates and packet integrity for 15 minutes post-reboot to confirm resolution of sensor degradation.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "OTA_SENSOR_REBOOT_AND_ROUTE_FAILOVER",
  "agent": "smart_grid_sensor_health_monitor",
  "target_asset": "Primary Grid Sensor Node",
  "failover_target": "Node S-19",
  "parameters": {
    "command": "DIAGNOSTIC_REBOOT",
    "routing_action": "REASSIGN_PRIMARY_TELEMETRY",
    "target_node_id": "S-19",
    "timeout_seconds": 300,
    "fallback_strategy": "AUTO_REVERT_ON_SIGNAL_LOSS"
  },
  "risk_assessment": {
    "impact_level": "Medium",
    "telemetry_interruption_window_sec": 3,
    "requires_hitl_approval": true
  },
  "status": "PENDING_OPERATOR_APPROVAL"
}
```
