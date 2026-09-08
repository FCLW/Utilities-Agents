# ⚡ Smart Home Device Integration Helper

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of smart home device integration helper is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Smart Home Device Integration Helper Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank smart home device integration helper events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.smart_home_device_integration_helper_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How does a customer pair their ecobee or Nest smart thermostat with our utility Demand Response rewards program?"

**Agent Response:**
### Executive Summary
**Customer pairing for ecobee and Google Nest thermostats into the utility Demand Response (BYOT) rewards program is executed via direct Cloud-to-Cloud (C2C) OAuth 2.0 integration with our Distributed Energy Resource Management System (DERMS). Customers can initiate enrollment either directly within their OEM mobile application (ecobee eco+ or Google Home/Nest app) or via the Utility Customer Engagement Portal using their utility account number and OEM credentials. Once authenticated, the DERMS establishes an automated OpenADR 2.0b telemetry bridge to dispatch precooling and peak-shed events while crediting annual DR reward incentives.**

---

### Step-by-Step Device Pairing Protocols

```
[Customer OEM App / Web Portal]
               │
               ▼
   [OAuth 2.0 Authentication]
   (Google / ecobee API Token)
               │
               ▼
[Utility Account Number Validation]
               │
               ▼
   [DERMS Virtual Power Plant] <─── OpenADR 2.0b Telemetry Bridge
               │
               ▼
 [Active DR Program Enrollment]
```

#### 1. Google Nest Pairing Workflow
1. **Initiate via Google Home App or Web Portal**:
   * Open the **Google Home** app, navigate to **Settings** > **Features** > **Nest Renew / Energy**.
   * Alternatively, access the Utility Marketplace DR Onboarding Portal and select **Google Nest**.
2. **Authorize OEM Access**:
   * Sign in using your Google account linked to the active Nest thermostat.
   * Consent to share device telemetry (runtime, setpoint, temperature data) with the utility DERMS.
3. **Utility Verification**:
   * Enter the 10-digit utility account number and service address zip code to verify active residential rate tier eligibility.
4. **Handshake & Confirmation**:
   * Google passes a cryptographically signed OAuth refresh token to the utility DERMS. The thermostat receives an on-screen notification confirming enrollment in "Utility Peak Savings Rewards."

#### 2. ecobee Pairing Workflow
1. **Initiate via ecobee App**:
   * Open the **ecobee** app, select the target thermostat, and tap the **eco+** settings icon.
   * Select **Community Energy Savings** > **Find Your Utility**.
2. **Select Utility & Authorize**:
   * Search for and select the utility provider from the authorized partner list.
   * Review and accept the program terms of service (allowing automated event temperature setpoint offsets of ±2°F to ±4°F during peak events).
3. **Account Association**:
   * Provide the utility customer account number for automated service address matching against the Customer Information System (CIS).
4. **DERMS Registration**:
   * ecobee’s API registers the unique Thermostat Identifier (TID) to the utility’s virtual power plant (VPP) demand flexibility group.

---

### Integration Performance & Program Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **API Token Exchange Latency** | 1.82 s | < 3.00 s | -39.3% | Normal |
| **First-Time Match Success Rate** | 94.2% | ≥ 90.0% | +4.7% | Normal |
| **Telemetry Sync Heartbeat (Ping)** | 5 min | 5 min | 0.0% | Normal |
| **Customer Drop-off at OAuth Step** | 5.8% | ≤ 8.0% | -27.5% | Normal |
| **DERMS Device Dispatch Readiness** | 98.4% | ≥ 95.0% | +3.6% | Normal |

---

### Visualization Triggers

**Recommended Chart**: Funnel / Progression Bar Chart depicting the enrollment conversion pipeline from initial eligibility verification to active DERMS registration.

```json
{
  "chart_type": "bar",
  "title": "Smart Thermostat BYOT Enrollment Pipeline Conversion",
  "xAxis": "Stage",
  "yAxis": "Conversion Rate (%)",
  "data": [
    {"stage": "Eligibility Check", "completion_rate": 100.0},
    {"stage": "OEM OAuth Auth", "completion_rate": 94.2},
    {"stage": "DERMS Token Handshake", "completion_rate": 91.0},
    {"stage": "Baseline Verification", "completion_rate": 88.4},
    {"stage": "Active DR Registration", "completion_rate": 85.1}
  ]
}
```

---

### Actionable Recommendations

* **Self-Service Support Routing**: Direct customers experiencing pairing mismatches to verify that the primary address on their ecobee/Google profile matches the premise address in the Utility CIS database.
* **Automated Exception Handling**: Configure DERMS ingestion pipelines to flag unmatched premise accounts for asynchronous fuzzy-matching on street address and zip code within 24 hours.
* **Incentive Issuance**: Verify that the automated billing engine credits the $50 one-time enrollment bill incentive within 1 to 2 billing cycles following verified DERMS telemetry validation.
* **Firmware Compatibility Notice**: Ensure customer support agents remind end-users to keep thermostat firmware updated (ecobeeOS v4.7+ or Google Nest v5.9+) to avoid OpenADR event signal dropouts.

### Example 2: Trend & Comparative Analysis
**User:** "Audit telemetry communication success rates between the utility DERMS cloud and customer smart home smart plugs."

**Agent Response:**
### Executive Summary
**An audit of telemetry communication between the utility DERMS cloud and enrolled customer smart plugs reveals an overall communication success rate of 94.8% across 1,240,000 polling intervals.** **While the majority of operating zones exceed the 95.0% SLA threshold, Zone-West and Zone-South exhibit elevated packet drop rates and heartbeat timeouts driven by legacy firmware and mesh gateway disconnections.** **Targeted firmware updates and cloud-to-device keepalive optimizations are required to restore fleet-wide DERMS telemetry reliability to target performance levels.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Overall Success Rate** | 94.82% | 95.00% | -0.19% | Warning |
| **Zone-North Telemetry Success Rate** | 98.40% | 95.00% | +3.58% | Normal |
| **Zone-South Telemetry Success Rate** | 91.20% | 95.00% | -4.00% | Warning |
| **Zone-East Telemetry Success Rate** | 99.10% | 95.00% | +4.32% | Normal |
| **Zone-West Telemetry Success Rate** | 87.60% | 95.00% | -7.79% | Critical |
| **Zone-Central Telemetry Success Rate** | 97.80% | 95.00% | +2.95% | Normal |
| **Mean Round-Trip Latency** | 242 ms | < 200 ms | +21.00% | Warning |
| **Heartbeat Timeout / Packet Loss Rate** | 5.18% | < 5.00% | +3.60% | Warning |
| **DERMS Demand Response Ack Rate** | 93.40% | 98.00% | -4.69% | Critical |

---

### Visualization Triggers

A **Bar Chart** comparing telemetry success rates against SLA thresholds across grid zones is recommended for operational monitoring.

```json
{
  "chart_type": "bar",
  "title": "Smart Plug Telemetry Communication Success Rate by Grid Zone",
  "categories": ["Zone-North", "Zone-South", "Zone-East", "Zone-West", "Zone-Central"],
  "series": [
    {
      "name": "Success Rate (%)",
      "data": [98.4, 91.2, 99.1, 87.6, 97.8]
    },
    {
      "name": "Target SLA (%)",
      "data": [95.0, 95.0, 95.0, 95.0, 95.0]
    }
  ],
  "unit": "%"
}
```

---

### Actionable Recommendations

* **Initiate Cloud Adapter Reconnects for Sub-SLA Zones**: Re-authenticate and flush stale WebSocket connections for smart plugs in Zone-West and Zone-South to clear connection bottlenecks.
* **Deploy Over-the-Air (OTA) Firmware Patch**: Push the latest Matter/Zigbee bridge adapter update to resolve local Wi-Fi keepalive drops on legacy smart plug hardware batches.
* **Dynamic Heartbeat Frequency Tuning**: Adjust DERMS polling intervals from 60s to 120s dynamically during non-event baseline windows to minimize packet collisions on customer home networks.
* **Automated Customer Support Diagnostic Notification**: Trigger automated in-app diagnostics for devices offline >24 hours, guiding customers through home router/mesh node reconnection steps.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue a test demand reduction event signal to enrolled smart home devices on Circuit 9 to verify gateway responsiveness."

**Agent Response:**
### Executive Summary
**A pre-dispatch readiness evaluation was conducted for enrolled smart home telemetry gateways on Circuit 9 in preparation for a synthetic test demand reduction event. Current gateway communication availability is verified at 96.1% across 720 enrolled endpoint devices, confirming nominal readiness for test signal dispatch. Because issuing active demand reduction signals directly impacts physical load states and customer-facing premises equipment, automated execution is halted pending mandatory Tier 2 Human-In-The-Loop (HITL) authorization.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Enrolled Device Population** | 720 units | 720 units | 0.0% | Normal |
| **Gateway Online / Heartbeat Rate** | 689 units (95.7%) | 684 units (95.0%) | +0.7% | Normal |
| **Average Telemetry Latency** | 240 ms | 300 ms | -20.0% | Normal |
| **Estimated Test Shed Capacity** | 485 kW | 500 kW | -3.0% | Normal |
| **Customer Opt-Out Rate (24h)** | 1.8% | < 5.0% | -64.0% | Normal |

---

### Visualization Triggers

**Recommended Chart Type:** Grouped Bar Chart (Device Category Availability vs. Enrolled Base on Circuit 9)

```json
{
  "chart_type": "bar",
  "title": "Circuit 9 Smart Home Device Enrollment vs Online Status",
  "data": {
    "labels": [
      "Smart Thermostats",
      "Level 2 EV Chargers",
      "Home Battery Storage",
      "Smart Water Heaters"
    ],
    "datasets": [
      {
        "label": "Online / Responsive Gateways",
        "data": [412, 128, 64, 85]
      },
      {
        "label": "Total Enrolled Devices",
        "data": [430, 135, 65, 90]
      }
    ]
  },
  "options": {
    "responsive": true,
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": { "display": true, "text": "Device Count" }
      }
    }
  }
}
```

---

### Actionable Recommendations

* **Operator Approval Required:** Review the dispatch parameters in the Tier 2 payload below to approve signal injection to the OpenADR / IEEE 2030.5 Virtual Top Node (VTN).
* **Test Event Window Configuration:** Verify that the 15-minute synthetic test window does not conflict with existing scheduled high-peak event windows on Substation Feeder 9.
* **Customer Communications:** Confirm that customer in-app notifications are set to "Diagnostic Test Mode" to prevent unnecessary customer support inquiries or manual overrides.
* **Post-Event Telemetry Capture:** Upon operator execution, monitor the 1-minute interval AMI and telemetry backhaul to log real-time curtailment verification (M&V) curves.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "DEMAND_RESPONSE_TEST_EVENT_DISPATCH",
  "circuit_id": "Circuit_9",
  "target_protocol": "OpenADR_2.0b / IEEE_2030.5",
  "event_classification": "TEST_SIGNAL_NON_EMERGENCY",
  "target_device_count": 689,
  "duration_minutes": 15,
  "dispatch_payload": {
    "signal_type": "SETPOINT_MODULATION_TEST",
    "thermostat_delta_f": "+1.0",
    "evse_throttle_pct": "50%",
    "battery_mode": "IDLE_TEST",
    "override_allowed": true
  },
  "safety_check_status": "PASSED_PRE_SCREEN",
  "requires_hitl_approval": true,
  "approval_prompt": "Confirm execution of a 15-minute test demand response signal to 689 connected devices on Circuit 9."
}
```
