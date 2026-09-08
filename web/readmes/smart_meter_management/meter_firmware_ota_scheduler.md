# ⚡ Meter Firmware Ota Scheduler

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of meter firmware ota scheduler is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Meter Firmware Ota Scheduler Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank meter firmware ota scheduler events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.meter_firmware_ota_scheduler_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the progress of the over-the-air (OTA) firmware upgrade across our 150,000 Gen-5 smart meters?"

**Agent Response:**
### 1. Executive Summary
**The over-the-air (OTA) firmware upgrade (v4.12) across the 150,000 Gen-5 smart meter fleet has reached 79.0% completion (118,500 meters successfully upgraded and verified). An additional 18,750 meters (12.5%) are currently in staging or broadcast transfer across the AMI mesh network, with a 1.7% failure rate (2,550 meters) flagged for mesh hop path optimization and targeted retry schedules.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Completed & Verified Upgrades** | 118,500 units (79.0%) | 150,000 units (100.0%) | -21.0% | Normal |
| **In-Progress / Mesh Transfer** | 18,750 units (12.5%) | 0 units (0.0%) | N/A | Normal |
| **Pending / Queued for Push** | 10,200 units (6.8%) | 0 units (0.0%) | N/A | Normal |
| **Failed Broadcast / CRC Mismatch** | 2,550 units (1.7%) | < 2.0% fleet target | -0.3% | Warning |
| **VEE Telemetry Ingestion Rate** | 99.4% | 99.0% minimum | +0.4% | Normal |
| **Average Mesh Latency (OTA window)** | 142 ms | < 250 ms | -43.2% | Normal |

---

### 3. Visualization Triggers
**Recommended Chart**: Stacked Bar / Milestone Progress Chart detailing batch distribution and mesh propagation health.

```json
{
  "chart_type": "bar",
  "title": "Gen-5 Smart Meter OTA Firmware Rollout Progress (150,000 Target)",
  "labels": ["Completed (v4.12)", "In-Progress / Staged", "Pending / Queued", "Failed / Rollback Required"],
  "datasets": [
    {
      "label": "Meter Count",
      "data": [118500, 18750, 10200, 2550],
      "backgroundColor": ["#2E7D32", "#0288D1", "#F57C00", "#D32F2F"]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Execute Wave 4 Dispatch**: Queue the remaining 10,200 pending meters across Substation Feeders 12A and 14B during the scheduled low-traffic maintenance window (01:00–04:00 AM local).
- **Isolate Failed Nodes**: Direct the mesh routing diagnostic tool to analyze the 2,550 failed meters for high RF attenuation, excessive mesh hop counts (>6 hops), or transient packet collisions.
- **Throttle Concurrent Channels**: Limit simultaneous RF multicast streams to 250 nodes per collector to prevent congestion on interval meter read channels (VEE SLA preservation).

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FIRMWARE_OTA_EXECUTION",
  "target_asset_group": "Gen-5 Smart Meters (Wave 4 & Retry Queue)",
  "firmware_image_id": "FW-GEN5-v4.12.8-PROD",
  "target_meter_count": 12750,
  "affected_grid_zones": ["GZ-NORTH-SUB12", "GZ-METRO-SUB14"],
  "scheduled_window": "2025-05-18T01:00:00Z - 2025-05-18T04:00:00Z",
  "safety_checks": {
    "emergency_override_active": false,
    "battery_backup_status": "PASS",
    "crc32_checksum_verified": true,
    "rollback_image_ready": true
  },
  "requires_human_approval": true,
  "approval_role": "Lead AMI Operations Engineer"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Track download failure rates, transmission retry latency, and device battery drain during nighttime mesh broadcast windows."

**Agent Response:**
### Executive Summary
**Telemetry analysis for the nighttime mesh broadcast window (01:00–05:00) indicates an elevated peak in download failure rates (9.1%) and transmission retry latency (26.5s) between 02:30 and 03:00 due to mesh RF channel saturation. Battery-operated endpoint nodes experienced a temporary 2.2× surge in discharge rates during multihop retry cycles, exceeding standard operating envelopes. Throttling broadcast concurrency and re-indexing mesh relay routing tables is required to stabilize delivery rates before the next scheduled rollout window.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Download Failure Rate** | 5.22% (Avg) / 9.10% (Peak) | $\le$ 3.00% | +74.0% | **Warning** |
| **Transmission Retry Latency** | 15.54 s (Avg) / 26.50 s (Peak) | $\le$ 12.00 s | +29.5% | **Warning** |
| **Device Battery Drain Rate** | 0.111 %/hr (Avg) / 0.220 %/hr (Peak) | $\le$ 0.080 %/hr | +38.8% | **Warning** |
| **Multihop Retry Packet Volume** | 18,450 pkts/window | $\le$ 8,500 pkts/window | +117.1% | **Critical** |
| **Firmware Block Completion Rate** | 94.78% | $\ge$ 98.00% | -3.29% | **Warning** |

---

### Visualization Triggers
- **Recommended Chart**: Time-Series Multi-Line Chart (Tracking failure rate, retry latency, and battery drain per 30-minute interval across the 01:00–05:00 broadcast window).

```json
{
  "chart_type": "line",
  "title": "Nighttime Mesh Broadcast Window Telemetry (01:00 - 05:00)",
  "labels": ["01:00", "01:30", "02:00", "02:30", "03:00", "03:30", "04:00", "04:30", "05:00"],
  "datasets": [
    {
      "label": "Download Failure Rate (%)",
      "data": [4.2, 4.8, 6.5, 9.1, 7.3, 5.0, 3.8, 3.2, 2.9],
      "borderColor": "#FF5722",
      "yAxisID": "y"
    },
    {
      "label": "Transmission Retry Latency (s)",
      "data": [12.4, 14.1, 18.6, 26.5, 21.0, 15.2, 11.8, 10.5, 9.8],
      "borderColor": "#FFC107",
      "yAxisID": "y1"
    },
    {
      "label": "Device Battery Drain Rate (%/hr)",
      "data": [0.08, 0.09, 0.14, 0.22, 0.18, 0.11, 0.07, 0.06, 0.05],
      "borderColor": "#E91E63",
      "yAxisID": "y2"
    }
  ]
}
```

---

### Actionable Recommendations
- **Throttle Broadcast Chunk Rate**: Lower packet injection rates from collector nodes during the 02:00–03:30 congestion peak to reduce RF contention on 915 MHz channels.
- **Dynamic Hop-Limit Dampening**: Limit maximum packet hop count to 4 for battery-powered endpoints, re-routing through mains-powered router nodes to preserve endpoint battery health.
- **Selective Delta-Block Retransmission**: Implement partial-block repair instead of full image download for meters with transient link drops.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "OTA_BROADCAST_SCHEDULE_ADJUSTMENT",
  "agent": "meter_firmware_ota_scheduler",
  "target_fleet": "AMI_MESH_METERS_ZONE_EAST",
  "parameters": {
    "broadcast_window": "01:00-05:00",
    "concurrency_limit_per_collector": 250,
    "chunk_interval_ms": 750,
    "max_retries_per_block": 3,
    "battery_guard_threshold_pct": 15.0
  },
  "safety_validation": {
    "hitl_approval_required": true,
    "critic_agent_review": "PASSED_WITH_CONSTRAINTS",
    "risk_level": "MEDIUM"
  }
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Pause the OTA firmware broadcast campaign on Substation 8 cluster due to elevated packet collision rates."

**Agent Response:**
### Executive Summary
**The Over-The-Air (OTA) firmware broadcast campaign across the Substation 8 cluster is experiencing acute RF mesh saturation, with packet collision rates exceeding the critical operating threshold by +421.0%. Immediate suspension of the broadcast schedule is staged to safeguard AMI mesh stability and prevent metering telemetry dropped packets. Because modifying active OTA firmware broadcast campaigns across physical smart meter fleets constitutes a Tier 2 operation, human operator authorization is required to execute the pause command.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Mesh Packet Collision Rate** | 52.1% | < 10.0% | +421.0% | **Critical** |
| **MAC Layer Retry Rate** | 69.4% | < 15.0% | +362.7% | **Critical** |
| **Interval Data Delivery Latency** | 38.4 min | < 5.0 min | +668.0% | **Critical** |
| **Active Campaign Broadcast Rate** | 250 pkts/sec | 50 pkts/sec | +400.0% | **Warning** |
| **VEE Interval Delivery Success** | 88.2% | ≥ 99.5% | -11.4% | **Critical** |

---

### Visualization Triggers
**Recommended Chart Type:** Time-Series Line Chart  
*Visualizes RF packet collision rates, MAC retries, and network latency degradation relative to the 10.0% engineering threshold over the active broadcast window.*

```json
{
  "chart_type": "line",
  "title": "Substation 8 Cluster - Mesh Packet Collision Rate & AMI Network Saturation",
  "xAxis": {
    "label": "Time (UTC)",
    "categories": ["14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30"]
  },
  "yAxis": {
    "label": "Percentage (%)"
  },
  "series": [
    {
      "name": "Packet Collision Rate (%)",
      "data": [4.2, 5.1, 12.8, 24.6, 38.2, 47.5, 52.1]
    },
    {
      "name": "Target Threshold (%)",
      "data": [10.0, 10.0, 10.0, 10.0, 10.0, 10.0, 10.0]
    },
    {
      "name": "MAC Layer Retry Rate (%)",
      "data": [6.1, 7.8, 18.4, 33.1, 51.0, 63.8, 69.4]
    }
  ]
}
```

---

### Actionable Recommendations
- **Halt Broadcast Immediately:** Execute the staged pause on the Substation 8 OTA firmware multicast pipeline to restore 900 MHz RF mesh channel capacity.
- **Isolate Congested Nodes:** Identify routing bottleneck collector nodes and high-hop mesh repeaters within the Substation 8 feeder boundary.
- **Reschedule with Rate Throttling:** Reconfigure the OTA scheduler to broadcast in low-density off-peak windows (01:00–04:00 Local Time) with a reduced bitrate of ≤ 35 pkts/sec.
- **Monitor Telemetry Recovery:** Verify that VEE interval collection success rates return above 99.5% within 30 minutes of campaign suspension.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "tier_level": 2,
  "action_type": "OTA_CAMPAIGN_PAUSE",
  "target_cluster": "Substation_8",
  "affected_device_count": 4218,
  "firmware_package_id": "FW-v4.12.9-NIC",
  "current_state": "ACTIVE_BROADCAST",
  "requested_state": "PAUSED",
  "reason": "Packet collision rate (52.1%) exceeding critical limit (10.0%), impacting normal VEE telemetry ingestion",
  "rollback_strategy": "Maintain current operational firmware image (FW-v4.11.2); resume unicast patching during low-traffic window",
  "requires_approval_from": "AMI Operations Lead / Smart Meter Operations Center"
}
```
