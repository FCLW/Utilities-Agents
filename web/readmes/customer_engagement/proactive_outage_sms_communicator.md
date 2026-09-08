# ⚡ Proactive Outage Sms Communicator

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of proactive outage sms communicator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Proactive Outage Sms Communicator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank proactive outage sms communicator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.proactive_outage_sms_communicator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which customers on Feeder 4 should receive proactive SMS notifications about the tree-related power outage?"

**Agent Response:**
### Executive Summary
**A total of 1,180 active customer accounts downstream of Feeder 4 are impacted by the verified tree-related fault event and qualify for proactive SMS notifications.** **Priority messaging is partitioned across Medical/Life Support accounts (18), Key Commercial/Industrial accounts (42), and standard Residential opt-ins (1,120), with an initial Estimated Time to Restoration (ETR) set to 120 minutes.** **In accordance with utility regulatory mandates and safety protocols, all customer PII has been redacted and mass SMS broadcast requires Human-In-The-Loop (HITL) authorization prior to dispatch.**

---

### Quantitative Evaluation & Customer Cohort Breakdown

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Feeder 4 Meter Points** | 1,425 meters | 1,425 meters | 0.0% | Normal |
| **De-energized Meters (Impacted)** | 1,180 meters | 0 meters | N/A | **Critical** |
| **SMS Opt-In Coverage** | 94.9% (1,120 res / 1,180) | 85.0% target | +11.6% | Normal |
| **Critical Care / Life Support Accounts** | 18 accounts | 0 baseline | N/A | **Critical** |
| **Commercial / Essential Accounts** | 42 accounts | 0 baseline | N/A | **Warning** |
| **Predicted SAIDI Impact (Feeder 4)** | 99.3 min | < 60.0 min target | +65.5% | **Warning** |
| **Initial Dispatch ETR Accuracy Target** | 120 min | ± 15 min tolerance | 0.0% | Normal |

---

### Notification Cohort Segmentation & Payload Configuration

1. **Cohort 1: Critical Care / Medical Baseline (18 Accounts)**
   - **Channel Priority**: High-priority SMS + Automated Voice Escalation fallback.
   - **Template Payload**: `[UTILITY ALERT] Service interruption detected on Feeder 4 affecting your address. Cause: Tree on lines. Crew dispatched. Initial ETR: 2 hrs. If you require emergency medical life support power assistance, please execute your emergency backup plan or call emergency services.`

2. **Cohort 2: Key Commercial & Industrial (42 Accounts)**
   - **Channel Priority**: SMS + Designated Key Account Representative Notification.
   - **Template Payload**: `[UTILITY COMMERCE ALERT] Outage detected at Feeder 4 service drop. Vegetation management & line crews are en route. Current ETR: 2 hours. Account rep notification initiated.`

3. **Cohort 3: Residential SMS Opt-In (1,120 Accounts)**
   - **Channel Priority**: Standard Omnichannel SMS.
   - **Template Payload**: `[UTILITY OUTAGE UPDATE] We are aware of a power outage in your area (Feeder 4) caused by fallen tree limbs. Repair crews have been assigned. Estimated restoration time is 2 hours. Track progress at [LINK]. Reply STOP to opt out.`

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Feeder 4 Outage Customer Notification Cohort Distribution",
  "data": {
    "labels": [
      "Critical Medical / Life Support",
      "Commercial / Essential Services",
      "Standard Residential (SMS Opt-In)",
      "Non-SMS / Backup Channels"
    ],
    "datasets": [
      {
        "label": "Number of Accounts",
        "data": [18, 42, 1120, 245]
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Immediate Broadcast**: Authorize Tier 2 execution of the outbound proactive SMS broadcast across all 1,180 validated contacts on Feeder 4.
- **Vegetation Management Telemetry Sync**: Monitor live field crew ingress (Vegetation Crew #12) and dynamically recalculate ETR if line clearing exceeds the 45-minute benchmark.
- **Cadence Frequency**: Schedule downstream interval updates every 60 minutes or immediately upon 50% restoration milestone.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "MASS_CUSTOMER_COMMUNICATION_DISPATCH",
  "feeder_id": "FEEDER-04",
  "grid_zone_id": "GZ-NORTH-04",
  "total_recipients": 1180,
  "cohort_breakdown": {
    "critical_care_sms": 18,
    "commercial_sms": 42,
    "residential_sms": 1120
  },
  "cause": "Tree contact / Vegetation fault",
  "etr_timestamp_utc": "2025-02-18T18:00:00Z",
  "requires_hitl_approval": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Track SMS delivery throughput and customer click-through rates on live outage map tracking links."

**Agent Response:**
### Executive Summary
**Proactive SMS outage delivery throughput is currently operating at an average of 425 messages/second with a 98.4% gateway delivery success rate across active outage zones.** **Customer engagement remains robust with an aggregate Click-Through Rate (CTR) of 51.2% on personalized live outage map tracking links, exceeding the operational target baseline of 40.0%.** **Telecommunications gateway latency is stable at 2.4 seconds, mitigating inbound call center load during active restoration events.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak SMS Throughput** | 510 msgs/sec | 350 msgs/sec | +45.71% | Normal |
| **SMS Gateway Delivery Rate** | 98.4% | 95.0% | +3.58% | Normal |
| **Average Delivery Latency** | 2.4 sec | < 5.0 sec | -52.00% | Normal |
| **Live Outage Map Link CTR** | 51.2% | 40.0% | +28.00% | Normal |
| **Link Bounce / 404 Error Rate** | 0.12% | < 0.50% | -76.00% | Normal |
| **Opt-Out / STOP Rate** | 0.04% | < 0.15% | -73.33% | Normal |

---

### Visualization Triggers

**Recommended Chart Type:** Dual-Axis Time-Series Line Chart (Throughput vs. CTR Over 24 Hours)

```json
{
  "chart_type": "line",
  "title": "Hourly SMS Delivery Throughput vs. Live Outage Map CTR",
  "xAxis": {
    "categories": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    "title": "Time Interval (UTC)"
  },
  "yAxis": [
    {
      "title": "Throughput (msgs/sec)",
      "opposite": false
    },
    {
      "title": "CTR (%)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "SMS Delivery Throughput (msgs/sec)",
      "data": [120, 95, 340, 510, 480, 290]
    },
    {
      "name": "Live Map CTR (%)",
      "data": [38.2, 34.5, 52.1, 58.4, 54.0, 46.8]
    }
  ]
}
```

---

### Actionable Recommendations

* **Maintain Dynamic Shortlink Tokenization:** Continue utilizing automated shortlink generation to track customer engagement at the feeder and substation level without exposing unencrypted customer identifiers or PII.
* **Carrier Gateway Bandwidth Allocation:** Keep multi-aggregator fallback routing primed in the event of upstream carrier throttling during severe weather/high-volume alert spikes.
* **ETR Refresh Synchronization:** Ensure web map landing pages dynamically cache and refresh Estimated Time to Restoration (ETR) data every 60 seconds to minimize repeat outbound SMS querying and call center deflection.
* **Monitor Opt-Out Velocity:** Maintain strict frequency capping (maximum 1 proactive update per ETR revision or milestone) to preserve low customer opt-out rates.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch an automated restoration update SMS with updated Estimated Time of Restoration (ETR) to 2,400 affected premises."

**Agent Response:**
### Executive Summary
**A batch of 2,400 automated restoration update SMS messages containing revised Estimated Time of Restoration (ETR) parameters has been staged for delivery across three impacted feeder corridors.** **Because dispatching outbound mass customer communications is classified as a Tier 2 critical operation, automated transmission is paused pending operator authorization.** **Upon Human-In-The-Loop (HITL) approval, the communication engine will broadcast through redundant carrier aggregators with standard rate-limiting controls to ensure compliance and prevent delivery bottlenecks.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Targeted Premises** | 2,400 accounts | 2,400 accounts | 0.0% | **Normal** |
| **ETR Confidence Interval** | 94.2% | ≥ 90.0% | +4.67% | **Normal** |
| **Average ETR Extension** | +35 minutes | ≤ 45 minutes | -22.2% | **Warning** |
| **SMS Queue Staging Latency** | 1.8 seconds | < 5.0 seconds | -64.0% | **Normal** |
| **TCPA / Quiet Hours Compliance** | 100% Passed | 100% Passed | 0.0% | **Normal** |

---

### Visualization Triggers
**Recommended Visualization:** *Categorical Bar Chart / Geographic Queue Distribution*
- **Chart Type:** Bar Chart
- **Description:** Staged outbound customer notifications segmented by feeder zone and corresponding revised ETR window.

```json
{
  "chart_type": "bar",
  "title": "Outage SMS Broadcast Volume by Feeder Zone",
  "x_axis_label": "Grid Zone / Feeder",
  "y_axis_label": "Impacted Premises",
  "series": [
    {
      "zone": "North Sector (Feeder N-12)",
      "premises_affected": 1100,
      "updated_etr": "18:30 EST"
    },
    {
      "zone": "Central Metro (Feeder C-04)",
      "premises_affected": 850,
      "updated_etr": "19:00 EST"
    },
    {
      "zone": "South Substation (Feeder S-09)",
      "premises_affected": 450,
      "updated_etr": "19:45 EST"
    }
  ]
}
```

---

### Actionable Recommendations
- **Validate Inbound Call Center Staffing:** Coordinate with customer service operations to ensure IVR trunks and digital triage channels can handle potential callback volume (~3–5% estimated response rate).
- **Monitor Real-Time SMS Gateway Throughput:** Track carrier delivery receipts (DLR) post-dispatch to verify delivery success rates meet the utility KPI standard of ≥ 98.5%.
- **Synchronize Digital Touchpoints:** Automatically update the public outage map and mobile application outage tracker with the identical revised ETR timestamps upon dispatch.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MASS_CUSTOMER_OUTAGE_SMS_DISPATCH",
  "target_scope": {
    "total_premises": 2400,
    "feeders_impacted": ["N-12", "C-04", "S-09"],
    "carrier_protocol": "A2P 10DLC / Shortcode 78489"
  },
  "message_template": "Utility Alert: Crews are actively working to restore power in your area. Your updated Estimated Time of Restoration (ETR) is now {UPDATED_ETR}. Track status at {PORTAL_URL} or reply STOP to opt out.",
  "risk_assessment": "Low risk of customer churn; moderate potential for inbound IVR load increase.",
  "hitl_approval_required": true,
  "execution_status": "AWAITING_OPERATOR_CONFIRMATION"
}
```
