# ⚡ Ami Mesh Network Health Monitor

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of ami mesh network health monitor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Ami Mesh Network Health Monitor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank ami mesh network health monitor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.ami_mesh_network_health_monitor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which RF mesh collectors in the downtown district are experiencing buffer overruns or high packet retransmission rates?"

**Agent Response:**
### Executive Summary
**A network telemetry audit of the Downtown District RF Mesh network identified two collectors (`COL-DT-104` and `COL-DT-108`) operating in Critical status due to severe buffer overruns and packet retransmission rates exceeding 14%. An additional two collectors (`COL-DT-101` and `COL-DT-112`) exhibit moderate congestion (Warning status) driven by high node-to-collector parent routing density. Without dynamic route rebalancing and queue optimization, head-end interval data ingestion latency and missed VEE read cycles will escalate.**

---

### Data Presentation

#### Aggregate Mesh Health Metrics: Downtown District

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Collector Buffer Overruns (DT-104)** | 142 events/hr | ≤ 5 events/hr | +2,740.0% | **Critical** |
| **Packet Retransmission Rate (DT-104)** | 18.4% | ≤ 3.0% | +513.3% | **Critical** |
| **Collector Buffer Overruns (DT-108)** | 98 events/hr | ≤ 5 events/hr | +1,860.0% | **Critical** |
| **Packet Retransmission Rate (DT-108)** | 14.1% | ≤ 3.0% | +370.0% | **Critical** |
| **Packet Retransmission Rate (DT-101)** | 8.7% | ≤ 3.0% | +190.0% | **Warning** |
| **Average Mesh Hop Latency (District)** | 480 ms | ≤ 250 ms | +92.0% | **Warning** |
| **Overall Interval Read Success Rate** | 94.2% | ≥ 99.5% | -5.3% | **Warning** |

#### Downtown Collector Telemetry Breakdown

| Collector ID | Grid Zone / Feeder | Active Connected Nodes | Buffer Overruns (24h) | Retransmission Rate (%) | AHI Score | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **COL-DT-104** | DT-Sub01 / Feeder-4 | 1,842 | 142 | 18.4% | 48.2 | **Critical** |
| **COL-DT-108** | DT-Sub02 / Feeder-2 | 1,620 | 98 | 14.1% | 56.0 | **Critical** |
| **COL-DT-101** | DT-Sub01 / Feeder-1 | 1,210 | 45 | 8.7% | 72.4 | **Warning** |
| **COL-DT-112** | DT-Sub03 / Feeder-5 | 1,180 | 32 | 7.2% | 75.1 | **Warning** |
| **COL-DT-103** | DT-Sub02 / Feeder-3 | 740 | 6 | 2.1% | 94.8 | **Normal** |
| **COL-DT-106** | DT-Sub01 / Feeder-2 | 680 | 2 | 1.5% | 97.2 | **Normal** |

---

### Visualization Triggers

- **Recommended Visualization**: **Grouped Bar Chart & Heatmap** comparing Buffer Overrun Counts against Retransmission Rates across all Downtown Collectors to visualize parent-node saturation.

```json
{
  "chart_type": "bar",
  "title": "Downtown RF Mesh Collector Performance & Congestion",
  "xAxis": "collector_id",
  "series": [
    {
      "name": "Buffer Overruns (Events/hr)",
      "data": [
        {"collector_id": "COL-DT-104", "value": 142},
        {"collector_id": "COL-DT-108", "value": 98},
        {"collector_id": "COL-DT-101", "value": 45},
        {"collector_id": "COL-DT-112", "value": 32},
        {"collector_id": "COL-DT-103", "value": 6},
        {"collector_id": "COL-DT-106", "value": 2}
      ]
    },
    {
      "name": "Retransmission Rate (%)",
      "data": [
        {"collector_id": "COL-DT-104", "value": 18.4},
        {"collector_id": "COL-DT-108", "value": 14.1},
        {"collector_id": "COL-DT-101", "value": 8.7},
        {"collector_id": "COL-DT-112", "value": 7.2},
        {"collector_id": "COL-DT-103", "value": 2.1},
        {"collector_id": "COL-DT-106", "value": 1.5}
      ]
    }
  ]
}
```

---

### Actionable Recommendations

- **Dynamic RPL Routing Reconfiguration**: Trigger an Over-The-Air (OTA) DODAG routing refresh to offload child nodes from overloaded collectors (`COL-DT-104`, `COL-DT-108`) toward adjacent underutilized collectors (`COL-DT-103`, `COL-DT-106`).
- **Buffer & Queue Parameter Tuning**: Remotely inspect collector memory utilization and increase queue threshold allocations for high-priority VEE alarm frames.
- **RF Interference & Spectrum Sweep**: Dispatch a field communications technician to verify if localized 900 MHz ISM band interference or physical RF path degradation is causing elevated retransmissions near `COL-DT-104`.
- **Collector Firmware & Memory Health Verification**: Check for firmware memory leaks or stuck packet buffers on `COL-DT-104` and `COL-DT-108`.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "AMI_MESH_DODAG_REBALANCING",
  "target_collectors": ["COL-DT-104", "COL-DT-108", "COL-DT-103", "COL-DT-106"],
  "district": "Downtown",
  "operation": "Execute RPL Mesh Re-parenting & Remote Collector Queue Reset",
  "estimated_affected_endpoints": 3462,
  "requires_hitl_approval": true,
  "submitted_by": "ami_mesh_network_health_monitor",
  "critic_validation_status": "PENDING_OPERATOR_CONFIRMATION"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Map cellular backhaul signal strength (RSSI) and routing hop counts across smart meter nodes in rural distribution areas."

**Agent Response:**
### Executive Summary
**Mesh network telemetry across rural distribution feeders reveals critical backhaul attenuation and extended RF routing paths in peripheral sectors.** **Collectors in Zones RUR-05, RUR-08, and RUR-09 exhibit cellular backhaul RSSI degradation below -98 dBm coupled with mesh routing hop counts exceeding 8 to 11 hops, leading to latency inflation and interval read delivery delays.** **Deploying intermediate RF range extenders and high-gain directional cellular antennas on affected collector nodes is required to prevent unbilled interval read accumulation and maintain compliance with standard 99.5% daily VEE completion targets.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Collector Backhaul RSSI (Zone Average)** | -91.2 dBm | $\ge$ -85.0 dBm | -7.29% | **Warning** |
| **Critical Collector RSSI (Worst Node: RUR-09)** | -106.0 dBm | $\ge$ -85.0 dBm | -24.71% | **Critical** |
| **Max Mesh Hop Count (Worst Feeder: 23C)** | 11 Hops | $\le$ 5 Hops | +120.00% | **Critical** |
| **Average Rural Hop Count** | 5.8 Hops | $\le$ 4.0 Hops | +45.00% | **Warning** |
| **Collector Backhaul Packet Success Rate (PSR)** | 94.10% | $\ge$ 99.00% | -4.95% | **Warning** |
| **Sub-Network Latency (Round-Trip P95)** | 4,120 ms | $\le$ 1,500 ms | +174.67% | **Critical** |
| **Asset Health Index (AHI - Rural Mesh Gateways)** | 71.4 / 100 | $\ge$ 88.0 / 100 | -18.86% | **Warning** |

---

### Visualization Trigger: Mesh Hop vs. Backhaul Signal Matrix

```json
{
  "chart_type": "scatter",
  "title": "Rural AMI Mesh Topology: Cellular Backhaul RSSI vs. Max Routing Hop Count",
  "xAxis": {
    "title": "Backhaul Signal Strength (RSSI dBm)",
    "threshold_warning": -85,
    "threshold_critical": -95
  },
  "yAxis": {
    "title": "Maximum Routing Hop Count",
    "threshold_warning": 5,
    "threshold_critical": 8
  },
  "clusters": [
    {"collector_id": "Collector-RUR-01", "feeder_id": "Feeder-12A", "rssi_dbm": -72, "max_hops": 2, "nodes": 312, "status": "Normal"},
    {"collector_id": "Collector-RUR-04", "feeder_id": "Feeder-08B", "rssi_dbm": -78, "max_hops": 3, "nodes": 280, "status": "Normal"},
    {"collector_id": "Collector-RUR-06", "feeder_id": "Feeder-04A", "rssi_dbm": -82, "max_hops": 4, "nodes": 410, "status": "Normal"},
    {"collector_id": "Collector-RUR-02", "feeder_id": "Feeder-14C", "rssi_dbm": -88, "max_hops": 5, "nodes": 540, "status": "Warning"},
    {"collector_id": "Collector-RUR-07", "feeder_id": "Feeder-09C", "rssi_dbm": -91, "max_hops": 6, "nodes": 620, "status": "Warning"},
    {"collector_id": "Collector-RUR-03", "feeder_id": "Feeder-11A", "rssi_dbm": -94, "max_hops": 7, "nodes": 490, "status": "Warning"},
    {"collector_id": "Collector-RUR-05", "feeder_id": "Feeder-17B", "rssi_dbm": -98, "max_hops": 8, "nodes": 680, "status": "Critical"},
    {"collector_id": "Collector-RUR-08", "feeder_id": "Feeder-22A", "rssi_dbm": -102, "max_hops": 9, "nodes": 750, "status": "Critical"},
    {"collector_id": "Collector-RUR-09", "feeder_id": "Feeder-23C", "rssi_dbm": -106, "max_hops": 11, "nodes": 820, "status": "Critical"}
  ]
}
```

---

### Actionable Recommendations

- **Dynamic RF Routing Optimization**: Re-balance parent-child routing tables on Feeders 17B, 22A, and 23C to limit maximum downstream node depth to $\le 6$ hops by establishing secondary tree pathways to adjacent collectors.
- **Physical Antenna Upgrades**: Issue a work order for field technicians to install high-gain directional Yagi or panel antennas (8–11 dBi) on Collectors RUR-05, RUR-08, and RUR-09 to improve cellular RSSI above the -85 dBm threshold.
- **Micro-Repeater Placement**: Deploy pole-mounted RF mesh range extenders at nodes with hop depths $>7$ on long rural lateral lines to reduce packet loss and channel congestion.
- **Carrier Dual-SIM Failover Assessment**: For collectors experiencing persistent low SINR ($< 3\text{ dB}$) and RSSI ($< -100\text{ dBm}$), verify carrier profile configuration and initiate secondary carrier failover testing.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Rebalance mesh routing topologies by reassigning 120 isolated smart meter child nodes to adjacent high-gain Collector C-04."

**Agent Response:**
### Executive Summary
**A total of 120 isolated smart meter child nodes have been evaluated for mesh routing reassignment to high-gain Collector C-04 following link-layer degradation on their primary parent paths.** **The proposed topology migration reduces child node isolation to 0% and optimizes the collector load to 76.0% of rated capacity with an average link margin improvement of +14.2 dB.** **Because mesh routing reconfiguration executes wide-area Over-The-Air (OTA) network control commands, this action constitutes a Tier 2 operation requiring human operator authorization prior to topology commit.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Isolated Meter Node Count** | 120 Nodes | 0 Nodes | +100.0% | **Critical** |
| **Collector C-04 Connected Nodes (Pre)** | 640 Nodes | 1,000 Nodes Max | -36.0% | **Normal** |
| **Collector C-04 Connected Nodes (Post)** | 760 Nodes | 1,000 Nodes Max | -24.0% | **Normal** |
| **Average Link Margin (Isolated Nodes to C-04)** | 22.4 dB | ≥ 12.0 dB | +86.7% | **Normal** |
| **Average RPL Hop Count to Root** | 4.2 Hops | ≤ 5.0 Hops | -16.0% | **Normal** |
| **Mesh Packet Delivery Ratio (PDR)** | 78.4% | ≥ 98.5% | -20.4% | **Critical** |
| **Expected Post-Rebalance PDR** | 99.1% | ≥ 98.5% | +0.6% | **Normal** |

---

### Visualization Triggers

**Recommended Visualization:** *Collector Capacity & Node Allocation Bar Chart* (to monitor channel utilization, collector overhead, and bandwidth margins before and after reassignment).

```json
{
  "chart_type": "bar",
  "title": "Mesh Collector Node Allocation & Headroom",
  "xAxis": {
    "categories": [
      "Collector C-01",
      "Collector C-02",
      "Collector C-03",
      "Collector C-04 (Pre-Rebalance)",
      "Collector C-04 (Post-Rebalance)"
    ]
  },
  "yAxis": {
    "title": "Connected Child Nodes",
    "max": 1000
  },
  "series": [
    {
      "name": "Active Child Nodes",
      "data": [12, 850, 780, 640, 760]
    },
    {
      "name": "Provisioned Capacity Limit",
      "data": [1000, 1000, 1000, 1000, 1000]
    }
  ]
}
```

---

### Actionable Recommendations
- **Validate RF Path Quality**: Confirm that all 120 isolated nodes exhibit a minimum Received Signal Strength Indicator (RSSI) of $\ge -95\text{ dBm}$ and Signal-to-Noise Ratio (SNR) $\ge 10\text{ dB}$ relative to Collector C-04 repeaters.
- **Schedule Staged RPL Routing Updates**: Dispatch Destination-Oriented Directed Acyclic Graph (DODAG) Information Object (DIO) trickle timer resets in 3 staged batches of 40 nodes to avoid channel collision during routing convergence.
- **Post-Reassignment Audit**: Monitor 15-minute interval data delivery and VEE (Validation, Editing, and Estimation) exception rates for 2 operating cycles (30 minutes) post-migration.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MESH_TOPOLOGY_REBALANCE",
  "tier": 2,
  "execution_mode": "HUMAN_APPROVAL_REQUIRED",
  "target_entity": "Collector C-04",
  "affected_nodes_count": 120,
  "parameters": {
    "source_status": "ISOLATED_PARENT_DROPPED",
    "target_collector_id": "COLL-C04-ZN02",
    "rebalance_method": "RPL_DODAG_REPARENTING",
    "staged_batches": 3,
    "batch_size": 40,
    "trickle_timer_reset": true,
    "max_collector_capacity": 1000,
    "post_load_projected": 760
  },
  "risk_assessment": {
    "rf_collision_risk": "LOW",
    "data_loss_risk": "LOW",
    "service_interruption": "NONE"
  },
  "authorization_prompt": "Approve remote Over-The-Air (OTA) RPL routing reassignment of 120 smart meter child nodes to Collector C-04."
}
```
