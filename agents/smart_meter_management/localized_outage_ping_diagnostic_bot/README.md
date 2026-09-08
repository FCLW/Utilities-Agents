# ⚡ Localized Outage Ping Diagnostic Bot

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of localized outage ping diagnostic bot is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Localized Outage Ping Diagnostic Bot Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank localized outage ping diagnostic bot events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.localized_outage_ping_diagnostic_bot_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can you send high-speed AMI pings to meters downstream of Fuse F-12 to confirm whether customer power has been restored?"

**Agent Response:**
### 1. Executive Summary
**A targeted high-speed AMI ping diagnostic sweep was initiated for all 42 meters downstream of lateral Fuse F-12 to verify power restoration following the reported interruption. Telemetry returns confirm that 38 meters (90.5%) are fully restored with nominal voltage, 2 meters report low voltage conditions, and 2 meters remain unresponsive. Full lateral energization cannot be marked as complete until nested outage verification and manual inspection on the 2 unresponsive endpoints are performed.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Ping Response Rate** | 95.2% (40/42) | 100.0% | -4.8% | **Warning** |
| **Fully Restored (Nominal RMS V)** | 38 meters (241.2 V avg) | 240.0 V (±5%) | +0.5% | **Normal** |
| **Voltage Sag Endpoints (<216 V)** | 2 meters (208.4 V avg) | 0 meters | N/A | **Warning** |
| **Unresponsive / Sustained Outage** | 2 meters | 0 meters | N/A | **Critical** |
| **Mesh Ping Latency (Round-Trip)** | 480 ms | < 750 ms | -36.0% | **Normal** |

---

### 3. Visualization Triggers

**Recommended Visualization:** Categorical Bar Chart illustrating downstream meter restoration status following the ping sweep across lateral F-12.

```json
{
  "chart_type": "bar",
  "title": "Downstream Fuse F-12 Meter Ping Restoration Status",
  "data": {
    "categories": [
      "Total Downstream Meters",
      "Restored (Nominal 240V)",
      "Low Voltage / Sag (<216V)",
      "Unresponsive (Nested Outage)"
    ],
    "values": [42, 38, 2, 2],
    "unit": "Endpoints"
  }
}
```

---

### 4. Actionable Recommendations

* **Dispatch Secondary Ping Wave**: Execute an isolated, high-retry ping cycle targeted specifically at the 2 unresponsive endpoints to confirm whether physical service drops or transformer-level secondary fuses are open.
* **Review Voltage Sag Log**: Escalate the 2 low-voltage endpoints (averaging 208.4 V) to Distribution Operations to check for loose neutral connections or phase imbalances.
* **Hold Outage Ticket Closure**: Maintain the active OMS outage ticket for lateral F-12 in "Partially Restored / Investigating" status until field verification confirms whether a nested outage exists.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "HIGH_SPEED_HEADEND_PING_SWEEP_OVERRIDE",
  "target_asset": "LATERAL_FUSE_F-12",
  "substation_feeder": "SUB_04_FEEDER_12",
  "affected_meter_count": 42,
  "execution_scope": "Continuous 60-second AMI mesh diagnostic polling and secondary re-ping loop",
  "required_authorization": "Distribution Operations Center (DOC) / Human-in-the-Loop Operator",
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate smart meter 'last-gasp' power failure power-off notifications against SCADA breaker open indications."

**Agent Response:**
### Executive Summary
**Cross-validation between smart meter AMI 'last-gasp' power failure notifications and SCADA feeder breaker open telemetry indicates an overall 98.2% correlation for primary mainline events, confirming widespread de-energization across affected feeders. However, targeted AMI on-demand ping sweeps identified 60 isolated 'nested outages' and lateral fuse clearings that were bypassed by SCADA breaker status indications. Immediate downstream crew dispatch is required for verified lateral line trips to mitigate extended customer interruption duration and prevent SAIDI penalties.**

---

### Data Presentation

The table below summarizes the diagnostic correlation between AMI last-gasp notifications, on-demand meter diagnostic pings, and SCADA breaker telemetry across monitored distribution circuits:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **AMI Last-Gasp Delivery Latency** | 18.4 s | $\le$ 30.0 s | -38.7% | Normal |
| **SCADA vs. Last-Gasp Mainline Correlation** | 98.2% | $\ge$ 95.0% | +3.4% | Normal |
| **Uncorrelated Last-Gasps (Nested/Lateral Outages)** | 60 units | $\le$ 15 units | +300.0% | Warning |
| **AMI Ping Diagnostic Failure Rate (No Response)** | 3.8% | $\le$ 2.0% | +90.0% | Warning |
| **False Positive Last-Gasp Rate (Transient Sags)** | 0.6% | $\le$ 1.5% | -60.0% | Normal |
| **ETR Calculation Variance (Nested Outages)** | +42.0 min | $\le$ 15.0 min | +180.0% | Critical |

---

### Visualization Triggers

* **Recommended Visualization:** Grouped Bar Chart / Outage Verification Profile per Feeder Node.
* **Purpose:** Correlating SCADA-reported open breaker load zones against received last-gasp clusters and localized ping diagnostic failures to differentiate mainline lockouts from downstream transformer/lateral fuse events.

```json
{
  "chart_type": "bar",
  "title": "AMI Last-Gasp Telemetry vs SCADA Breaker Status",
  "categories": [
    "Feeder-04A",
    "Feeder-04B",
    "Feeder-12C",
    "Feeder-08D",
    "Feeder-15A"
  ],
  "series": [
    {
      "name": "SCADA Breaker Confirmed Outages",
      "data": [450, 0, 1200, 0, 310]
    },
    {
      "name": "AMI Last-Gasp Alarms",
      "data": [442, 18, 1185, 42, 305]
    },
    {
      "name": "Targeted Ping Failures (Nested/Lateral)",
      "data": [8, 18, 15, 42, 5]
    }
  ]
}
```

---

### Actionable Recommendations

* **Execute Localized Ping Sequences on Latched Feeders:** For `Feeder-04B` and `Feeder-08D`, where SCADA breakers show closed/energized but last-gasps and ping failures persist, initiate automated cyclic ping diagnostics to map the exact boundary of blown lateral fuses.
* **Auto-Isolate False Restorations:** Reconfigure Outage Management System (OMS) restoration verification rules so that mainline breaker reclose events do not clear customer tickets automatically if downstream meters fail ping confirmation.
* **Audit AMI Mesh Battery/Capacitor Health:** Flag the 15 non-responsive meters on `Feeder-12C` for battery health and power-off alarm capacitor diagnostic checks during routine field servicing.
* **Synchronize SCADA and Head-End Timestamps:** Calibrate SCADA sequence of events (SOE) clock with the AMI Head-End System (HES) time standard (NTP/PTP) to enhance sub-second last-gasp correlation accuracy.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "OMS_TICKET_SPLIT_AND_CREW_DISPATCH",
  "feeder_ids": ["Feeder-04B", "Feeder-08D"],
  "affected_customers": 60,
  "incident_type": "Confirmed Nested / Lateral Outage",
  "risk_level": "Medium",
  "requires_approval": true,
  "authorizer_role": "Distribution Operations Center (DOC) Operator / Dispatch Lead",
  "justification": "SCADA indicates substation breaker closed, but AMI last-gasp and ping telemetry confirms 60 downstream customers remain de-energized across two branch lateral protective devices."
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Execute automated batch ping sequence to 85 smart meters on Circuit 3 and close confirmed restored outage work tickets."

**Agent Response:**
### Executive Summary
**A localized batch diagnostic ping sequence was executed across 85 smart meters mapped to Circuit 3 to verify post-restoration status.** **Of the targeted endpoints, 79 smart meters responded with affirmative power-on acknowledgments (92.9% verified restoration), while 6 endpoints remain either unresponsive or degraded, indicating potential localized nested outages.** **In accordance with utility safety and operational compliance guardrails, automated batch closure of associated outage work tickets constitutes a Tier 2 action requiring Human-In-The-Loop (HITL) authorization prior to updating the Outage Management System (OMS).**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Meters Pinged** | 85 endpoints | 85 endpoints | 0.0% | Normal |
| **Successful Ping Responses (Restored)** | 79 endpoints | 85 endpoints | -7.1% | Normal |
| **Unresponsive Endpoints (Nested Outage Risk)** | 4 endpoints | 0 endpoints | N/A | Warning |
| **Degraded / High Latency Mesh Nodes** | 2 endpoints | 0 endpoints | N/A | Warning |
| **Ping Response Success Rate** | 92.94% | 98.00% | -5.16% | Warning |
| **Average Round-Trip Latency** | 184 ms | 120 ms | +53.33% | Warning |

---

### Visualization Trigger
**Recommended Chart Type**: Distribution / Bar Chart (Restoration & Reachability Breakdown)

```json
{
  "chart_type": "bar",
  "title": "Circuit 3 AMI Batch Ping Diagnostic Results",
  "categories": [
    "Confirmed Restored",
    "Unresponsive (Nested Outage)",
    "Degraded / High Latency"
  ],
  "series": [
    {
      "name": "Smart Meters",
      "data": [79, 4, 2]
    }
  ],
  "y_axis_label": "Meter Count"
}
```

---

### Actionable Recommendations
* **Submit for Work Ticket Closure**: Approve ticket closure for the 79 verified restored smart meter accounts on Circuit 3.
* **Isolate Unresponsive Nodes**: Dispatch targeted secondary pings and generate nested outage investigation tickets for the 4 unresponsive meters (potential line fuse or lateral drop failure).
* **Mesh Network Optimization**: Flag the 2 high-latency mesh relay nodes for routing table refresh to ensure stable automated interval telemetry.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "BATCH_WORK_TICKET_CLOSURE",
  "feeder_id": "Circuit 3",
  "target_asset_count": 79,
  "system_target": "OMS_WMS_INTEGRATION",
  "impact_scope": "Close active restoration tickets for 79 confirmed online endpoints; exclude 6 pending investigation endpoints",
  "requires_approval": true,
  "action_status": "PENDING_OPERATOR_APPROVAL"
}
```
