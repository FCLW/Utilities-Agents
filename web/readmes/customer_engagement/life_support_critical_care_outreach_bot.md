# ⚡ Life Support Critical Care Outreach Bot

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of life support critical care outreach bot is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Life Support Critical Care Outreach Bot Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank life support critical care outreach bot events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.life_support_critical_care_outreach_bot_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are there any registered medical life-support customers residing in the projected footprint of Outage Event #402?"

**Agent Response:**
### Executive Summary
**A total of 14 registered Medical Life-Support and Critical Care customers have been identified within the projected impact footprint of Outage Event #402 across Feeders 12A, 12B, and 14C. Immediate high-priority outreach protocols must be initiated to verify customer backup power systems, provide estimated times to restoration (ETR), and offer emergency welfare dispatch for uncontacted accounts. Adherence to state Public Utilities Commission (PUC) Medical Baseline mandates requires mandatory contact confirmation or field safety checks for all unverified accounts within 60 minutes of outage confirmation.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Impacted Life-Support Customers** | 14 accounts | 0 accounts | +100.0% | **Critical** |
| **Automated Contact Verification Rate** | 64.3% (9/14) | 100.0% | -35.7% | **Warning** |
| **Uncontacted / Escalated Accounts** | 5 accounts | 0 accounts | +100.0% | **Critical** |
| **Battery/Generator Backup Confirmed** | 7 accounts | 14 accounts | -50.0% | **Warning** |
| **Critical Care Triage SLA Remaining** | 38 mins | 60 mins | -36.7% | **Warning** |

---

### Visualization Triggers
**Recommended Chart Type:** Grouped Bar Chart (Outage Footprint Life-Support Breakdown by Feeder)

```json
{
  "chart_type": "bar",
  "title": "Life Support Customer Impact - Outage Event #402",
  "categories": ["Feeder 12A", "Feeder 12B", "Feeder 14C"],
  "series": [
    {
      "name": "Total Registered Medical Accounts",
      "data": [8, 4, 2]
    },
    {
      "name": "Contact Verified / Backup Ready",
      "data": [6, 3, 0]
    },
    {
      "name": "Pending Outreach / Welfare Escalation",
      "data": [2, 1, 2]
    }
  ]
}
```

---

### Actionable Recommendations
- **Omnichannel Broadcast Dispatch:** Trigger Tier 1 automated IVR voice calls, high-priority SMS, and email notifications to the 5 uncontacted accounts with primary medical device dependencies (e.g., oxygen concentrators, ventilators).
- **Secondary Live Agent Escalation:** Route unacknowledged records after 15 minutes to the Critical Care Customer Support queue for manual operator outreach.
- **Emergency Field Welfare Coordination:** If two-way communication is not established within 45 minutes, coordinate with local emergency dispatch / first responders for physical welfare checks per PUC Emergency Preparedness Rule requirements.
- **Restoration Prioritization:** Notify Distribution Grid Operations (DMS/OMS) to prioritize feeder restoration and mobile generation dispatch toward Substation Feeder 14C and Feeder 12A.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_CUSTOMER_OUTREACH_DISPATCH",
  "event_id": "OUTAGE-EVENT-402",
  "affected_feeders": ["FDR-12A", "FDR-12B", "FDR-14C"],
  "target_population": "Medical Life Support & Critical Care Customers",
  "recipient_count": 14,
  "channels": ["PRIORITY_VOICE_IVR", "SMS_DIRECT", "EMAIL_SECURE"],
  "message_template_id": "CRITICAL_CARE_OUTAGE_ALERT_V4",
  "requires_hitl_approval": true,
  "approval_role": "Customer Operations Duty Officer / Master Orchestrator"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Verify emergency backup generator availability and confirmed contact phone numbers for vulnerable residents in Zone 6."

**Agent Response:**
### Executive Summary
**Zone 6 critical care registry analysis confirms that 118 of 142 registered life support accounts (83.1%) have verified operational emergency backup generation on site, while 24 accounts require immediate generator status resolution. Primary and secondary emergency contact phone numbers are verified active for 131 accounts (92.3%), leaving 11 unconfirmed records flagged for prioritized omni-channel contact verification. Outreach protocols dictate immediate escalation for the 24 generator-deficient and 11 unverified contact accounts ahead of potential grid disruptions.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Registered Critical Care Accounts** | 142 | 142 | 0.0% | Normal |
| **Verified Operational Backup Generators** | 118 (83.1%) | 142 (100.0%) | -16.9% | Warning |
| **Deficient / Unverified Backup Generators** | 24 (16.9%) | 0 (0.0%) | +16.9% | Critical |
| **Confirmed Active Contact Numbers (<30 Days)** | 131 (92.3%) | 142 (100.0%) | -7.7% | Warning |
| **Unverified / Outdated Contact Records** | 11 (7.7%) | 0 (0.0%) | +7.7% | Critical |
| **Dual-Deficiency Accounts (No Gen + No Phone)** | 4 (2.8%) | 0 (0.0%) | +2.8% | Critical |

---

### Visualization Triggers
**Recommended Chart:** Categorical Bar Chart depicting emergency readiness compliance across Zone 6 vulnerable customer cohorts.

```json
{
  "chart_type": "bar",
  "title": "Zone 6 Life Support Readiness & Contact Verification",
  "data": [
    {"category": "Total Registered", "count": 142},
    {"category": "Generator Verified Ready", "count": 118},
    {"category": "Generator Deficient/Unverified", "count": 24},
    {"category": "Phone Verified Active", "count": 131},
    {"category": "Phone Verification Pending", "count": 11},
    {"category": "Dual-Deficiency (Priority 1)", "count": 4}
  ]
}
```

---

### Actionable Recommendations

* **Priority 1 Field & Direct Outreach:** Dispatch customer liaison agents to conduct targeted outbound calls and in-person welfare checks for the 4 accounts flagged with both unverified phone numbers and deficient backup power.
* **Automated Multi-Channel Outreach:** Trigger IVR/SMS verification prompts for the remaining 7 accounts with pending contact verification to secure secondary and emergency caregiver contact lines.
* **Mobile Generation Staging:** Coordinate with the Regional Dispatch Operations Center to stage portable generation units and battery backup modules at the Zone 6 primary distribution substation for rapid deployment.
* **Regulatory Compliance Log:** Archive verification audit trail into the PUC Medical Baseline / Life Support compliance repository.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MASS_CUSTOMER_COMMUNICATION_DISPATCH",
  "module": "Customer_Engagement_Omnichannel_Outreach",
  "target_zone": "Zone 6",
  "target_cohort": "Life_Support_Critical_Care",
  "payload": {
    "campaign_id": "LS-Z6-EMERGENCY-VERIFY-2025",
    "contact_outreach_type": "HIGH_PRIORITY_IVR_AND_SMS",
    "affected_records": 11,
    "template_id": "CRITICAL_CARE_CONTACT_AND_GENERATOR_AUDIT_V3",
    "requires_field_dispatch_escalation": true,
    "escalation_field_count": 4
  },
  "compliance_check": {
    "puc_rule_conformance": "PASSED",
    "pii_redaction_enforced": "TRUE"
  },
  "authorization_required": "Operator confirmation required prior to initiating outbound IVR and SMS broadcast sequence."
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Trigger an automated priority voice call and SMS welfare check to all registered life-support accounts in Sector 3."

**Agent Response:**
### Executive Summary
**A prioritized welfare check sequence comprising automated IVR voice calls and SMS alerts has been prepared for all 142 registered life-support critical care accounts in Sector 3.** **Because initiating automated mass outbound communications is classified as a Tier 2 operation under utility compliance and regulatory safety standards, outbound dialing and messaging queues require explicit operator authorization prior to release.** **System telemetry indicates 100% communication channel readiness across all primary telephony and SMS gateway endpoints.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Registered Life-Support Accounts (Sector 3)** | 142 Accounts | 142 Accounts | 0.0% | **Normal** |
| **Voice / IVR Gateway Channel Availability** | 99.8% | 99.5% | +0.3% | **Normal** |
| **High-Priority SMS Gateway Throughput** | 250 msg/sec | 100 msg/sec | +150.0% | **Normal** |
| **Escalation Field Verification Standby** | 12 Units | 10 Units | +20.0% | **Normal** |
| **Contact Response SLA Target** | 15 min | 20 min | -25.0% | **Normal** |

---

### Visualization Triggers
- **Recommended Visualization**: Stacked / Category Bar Chart tracking stage progression across outbound communication channels (IVR Dialing vs. SMS Delivery vs. Unresponsive Field Escalation).

```json
{
  "chart_type": "bar",
  "title": "Sector 3 Life Support Outreach Queue Distribution",
  "categories": ["Primary Voice Call Queue", "Priority SMS Queue", "Direct Field Dispatch Backup"],
  "series": [
    {
      "name": "Target Accounts",
      "data": [142, 142, 12]
    }
  ]
}
```

---

### Actionable Recommendations
- **Operator Review**: Verify outbound campaign parameters and authorize the Tier 2 communication dispatch payload below.
- **Continuous Cadence Monitoring**: Monitor automated callback receipts and interactive response acknowledgments across the initial 15-minute contact window.
- **Field Welfare Escalation**: Automatically route any accounts with non-responsive attempts after 2 call/SMS cycles to localized emergency field response and dispatch units.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "MASS_CUSTOMER_COMMUNICATION",
  "agent": "life_support_critical_care_outreach_bot",
  "domain": "Customer Engagement",
  "target_zone": "Sector 3",
  "affected_population": 142,
  "communication_channels": [
    "PRIORITY_VOICE_IVR",
    "CRITICAL_SMS"
  ],
  "payload_details": {
    "campaign_name": "Sector_3_LifeSupport_Welfare_Check",
    "message_template_id": "LIFE_SUPPORT_WELFARE_CHECK_V2",
    "acknowledgment_required": true,
    "unresponsive_escalation_timeout_sec": 900
  },
  "compliance_check": {
    "puc_critical_care_mandate": "COMPLIANT",
    "pii_redaction_status": "ENCRYPTED_AND_TOKENIZED"
  },
  "status": "PENDING_HUMAN_APPROVAL"
}
```
