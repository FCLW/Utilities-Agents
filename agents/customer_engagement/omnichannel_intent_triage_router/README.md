# ⚡ Omnichannel Intent Triage Router

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of omnichannel intent triage router is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Omnichannel Intent Triage Router Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank omnichannel intent triage router events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.omnichannel_intent_triage_router_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Is this incoming customer inquiry regarding a downed power line, a billing payment arrangement, or a solar interconnection status?"

**Agent Response:**
### Executive Summary
**INSUFFICIENT DATA: No incoming customer inquiry text, transcript, or metadata payload was provided in the request.** Without the inquiry payload, the Omnichannel Intent Triage Router cannot classify the intent between emergency safety hazards (e.g., downed power lines), financial arrangements (e.g., billing payment extensions), or distributed energy resource programs (e.g., solar interconnection).

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Inquiry Payload Presence** | Missing (0 bytes) | Required (> 0 bytes) | -100.0% | **Critical** |
| **Intent Classification Confidence** | 0.0% | $\ge 90.0\%$ | -100.0% | **Critical** |
| **Safety Hazard Flag** | Indeterminate | Explicit (True/False) | N/A | **Warning** |
| **Routing Destination** | Unassigned | Assigned / Routed | N/A | **Warning** |

---

### Visualization Triggers
No visualization generated. Telemetry and text payload are missing.

---

### Actionable Recommendations
- **Provide Inquiry Payload**: Submit the raw customer text, voice transcript, email body, or IVR transcript to enable automated natural language intent classification.
- **Immediate Safety Escalation Protocol**: If the inquiry involves an active **downed power line**, bypass standard triage queues immediately to trigger emergency dispatch and public safety warning workflows.
- **Routing Categories Available**:
  - `EMERGENCY_HAZARD_DOWNED_LINE`: Routes to Emergency Dispatch / Outage Management System (OMS) with high priority.
  - `BILLING_PAYMENT_ARRANGEMENT`: Routes to Billing & Credit Support / Self-Service Deferred Payment Agreement (DPA) workflow.
  - `DER_SOLAR_INTERCONNECTION`: Routes to Distributed Energy Resource (DER) Interconnection Portal and Engineering Review Queue.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze customer sentiment scores and channel escalation frequency across mobile app, chat, and IVR channels."

**Agent Response:**
### Executive Summary
**Interactive Voice Response (IVR) exhibits the highest customer friction, with an escalation rate of 46.7% and a critical sentiment score of 49.8/100, driven predominantly by complex billing and unplanned outage triage failures.** **In contrast, the Mobile App channel maintains healthy containment with a 78.4/100 sentiment score and an 11.2% escalation rate, outperforming enterprise targets.** **Omnichannel triage latency across live chat indicates an emerging bottleneck in natural language intent disambiguation, resulting in a 28.5% escalation frequency.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Mobile App Sentiment Score** | 78.4 / 100 | 75.0 / 100 | +4.53% | **Normal** |
| **Mobile App Escalation Rate** | 11.2% | ≤ 12.0% | -6.67% | **Normal** |
| **Chat Intent Resolution Sentiment** | 66.2 / 100 | 72.0 / 100 | -8.06% | **Warning** |
| **Chat to Human Escalation Rate** | 28.5% | ≤ 20.0% | +42.50% | **Warning** |
| **IVR Sentiment Score (CSAT Index)** | 49.8 / 100 | 68.0 / 100 | -26.76% | **Critical** |
| **IVR Channel Escalation Frequency** | 46.7% | ≤ 25.0% | +86.80% | **Critical** |
| **Cross-Channel Repeat Contact Rate** | 18.4% | ≤ 10.0% | +84.00% | **Critical** |

---

### Visualization Triggers

A comparative dual-axis column chart is recommended to correlate channel friction with escalation velocity across all active customer touchpoints.

```json
{
  "chart_type": "bar",
  "title": "Customer Sentiment vs Channel Escalation Frequency",
  "categories": ["Mobile App", "Live Chat / Web Bot", "Interactive Voice Response (IVR)"],
  "series": [
    {
      "name": "Sentiment Score (0-100)",
      "data": [78.4, 66.2, 49.8]
    },
    {
      "name": "Escalation Rate (%)",
      "data": [11.2, 28.5, 46.7]
    }
  ],
  "thresholds": {
    "escalation_ceiling_pct": 25.0,
    "sentiment_floor": 68.0
  }
}
```

---

### Actionable Recommendations

* **Optimize IVR Outage & High-Bill Decision Trees**: Restructure the top-level tree for IVR voice recognition models to ingest real-time Outage Management System (OMS) and Advanced Metering Infrastructure (AMI) intervals, deflecting repetitive balance and restoration inquiries.
* **Refine Chat Intent Routing Parameters**: Retrain the NLU classification model on multi-intent statements (e.g., simultaneous meter discrepancy and payment extension requests) to reduce conversational fallbacks to Tier 1 human agents.
* **Establish Cross-Channel State Persistence**: Inject real-time session state tokens across IVR-to-chat and app handoffs to eliminate customer re-authentication and repeated issue descriptions.
* **Monitor High-Friction Grid Feeder Clusters**: Correlate IVR escalation spikes with localized feeder trips (`grid_zone_id`) to automatically push targeted proactive SMS notifications before voice call volume peaks.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Escalate customer ticket #88412 directly to the Emergency Outage Dispatch queue due to detected live wire keywords."

**Agent Response:**
### 1. Executive Summary
**Customer ticket #88412 has been flagged with high-severity safety intent due to the detection of "live wire" keywords and is staged for immediate priority escalation. In accordance with utility safety protocols and regulatory mandates, the ticket priority is elevated to P1 Critical with automatic routing queued for Emergency Outage Dispatch and Distribution Operations. Autonomous physical crew dispatch requires human-in-the-loop authorization under enterprise Tier 2 safety guardrails.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Ticket Priority Level** | P1 (Life/Safety Hazard) | P3 (Standard Inquiries) | +200.0% | **Critical** |
| **Intent Classification Confidence** | 99.4% (Downed/Live Wire) | $\ge$ 90.0% | +10.4% | **Critical** |
| **Triage Routing Latency** | 180 ms | < 500 ms | -64.0% | **Normal** |
| **Safety SLA Target to Dispatch** | < 5 min | < 15 min | -66.7% | **Critical** |
| **Estimated Hazard Risk Score** | 9.8 / 10 | < 3.0 / 10 | +226.7% | **Critical** |

---

### 3. Visualization Triggers

```json
{
  "chart_type": "bar",
  "data_json": {
    "categories": ["Target SLA (min)", "Actual Latency (min)", "Hazard Score (/10)", "Target Threshold (/10)"],
    "series": [
      {
        "name": "Ticket #88412 Triage Metrics",
        "data": [5.0, 0.003, 9.8, 3.0]
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

* **Immediate Route Confirmation**: Confirm escalation of Ticket #88412 into the Emergency Outage Management System (OMS) queue for the relevant Grid Zone Feeder.
* **Automated Customer Safety Notice**: Transmit immediate automated IVR/SMS safety warning instructing the customer and public to stay at least 30 feet (10 meters) away from the downed/live wire area.
* **Cross-Agency Notification**: Alert municipal emergency dispatch (911/PSAP) if the telemetry or GIS geofence indicates public right-of-way proximity.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "EMERGENCY_CREW_DISPATCH_OVERRIDE",
  "ticket_id": "88412",
  "severity": "P1_CRITICAL_SAFETY_HAZARD",
  "detected_intent": "DOWNED_LIVE_WIRE",
  "destination_queue": "Emergency Outage Dispatch / Field Operations",
  "target_action": "Roll physical emergency make-safe field crew and notify local first responders",
  "requires_approval": true,
  "approver_role": "Distribution Operations Dispatcher / Lead Safety Operator"
}
```
