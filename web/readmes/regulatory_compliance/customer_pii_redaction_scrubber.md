# ⚡ Customer Pii Redaction Scrubber

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of customer pii redaction scrubber is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Customer Pii Redaction Scrubber Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank customer pii redaction scrubber events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.customer_pii_redaction_scrubber_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are there any unmasked Social Security numbers, banking details, or customer phone numbers in the billing dispute case file?"

**Agent Response:**
### Executive Summary
**INSUFFICIENT DATA: No specific billing dispute case file ID or text payload was provided in the input request.** Automated PII redaction and compliance scrubbing require a designated case record or payload to evaluate unmasked Social Security Numbers (SSN), banking routing/account numbers, and phone records. Under regulatory data privacy and utility compliance policies, all unmasked direct identifiers must be sanitized before ingestion or downstream dispatch.

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Case File Identification** | `None Provided` | `Valid Case / Record ID` | N/A | **Warning** |
| **SSN Redaction Coverage** | `INSUFFICIENT DATA` | 100% Masked (`XXX-XX-####`) | 0.0% | **Warning** |
| **Banking / Financial Redaction** | `INSUFFICIENT DATA` | 100% Tokenized / Masked | 0.0% | **Warning** |
| **Phone Number Redaction** | `INSUFFICIENT DATA` | 100% Tokenized / Masked | 0.0% | **Warning** |
| **Audit Compliance Rate** | `Pending Case Ingestion` | 100.0% | 0.0% | **Normal** |

---

### Visualization Triggers
*A visualization trigger will activate upon receiving the target case log batch to plot PII entity detection frequency and redaction rates across ingestion timestamps.*

```json
{
  "chart_type": "bar",
  "data_json": "{\"categories\": [\"SSN\", \"Banking Info\", \"Phone Numbers\"], \"unmasked_detected\": [0, 0, 0], \"target_threshold\": [0, 0, 0]}"
}
```

---

### Actionable Recommendations

* **Provide Case Identifier / Payload**: Submit the specific `case_id`, `dispute_ticket_id`, or text excerpt to initiate the automated regex/NER scrubbing pipeline.
* **Standard Sanitization Protocol**:
  * **Social Security Numbers**: Scrubber will replace all `\d{3}-\d{2}-\d{4}` patterns with `[REDACTED_SSN]`.
  * **Banking Details**: Scrubber will replace all ABA routing and checking/savings accounts with `[REDACTED_BANK_INFO]`.
  * **Phone Numbers**: Scrubber will mask standard 10-digit formats to `[REDACTED_PHONE]`.
* **Escalation**: If direct database integration is required for mass redaction, route the request through the Master Orchestrator with appropriate session parameters (`customer_id`, `operating_mode`).

### Example 2: Trend & Comparative Analysis
**User:** "Scan customer service email attachments and chat transcripts to verify compliance with state consumer privacy regulations."

**Agent Response:**
### Executive Summary
**A comprehensive privacy compliance audit was executed across customer service email attachments and live chat transcripts to evaluate adherence to state consumer privacy regulations and utility data protection mandates.** **While real-time chat transcript redaction achieved an audit compliance rate of 99.85%, unredacted customer PII in email attachments (specifically embedded banking details and tax identifiers in PDF/image uploads) fell below target at 96.40%, requiring immediate programmatic remediation.** **All detected unredacted records have been isolated to prevent downstream leakage and staged for secondary automated scrubbing and validation.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Chat Transcript PII Scrubbing Rate** | 99.85% | 99.50% | +0.35% | Normal |
| **Email Attachment PII Scrubbing Rate** | 96.40% | 99.50% | -3.12% | Warning |
| **Full Audit Compliance Rate** | 98.13% | 99.50% | -1.38% | Warning |
| **Unredacted High-Risk Entities (SSN/Banking)** | 42 records | 0 records | N/A | Critical |
| **Incident Reporting & Quarantine Latency** | 1.8 mins | < 5.0 mins | -64.00% | Normal |
| **OCR Image/PDF Scrubbing Success Rate** | 94.20% | 99.00% | -4.85% | Warning |

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Customer PII Redaction Compliance by Channel",
  "categories": ["Chat Transcripts", "Email Attachments", "Customer Web Forms", "Billing Tickets"],
  "series": [
    {
      "name": "Audit Compliance Rate (%)",
      "data": [99.85, 96.40, 99.92, 98.15]
    },
    {
      "name": "Regulatory Compliance Baseline (%)",
      "data": [99.50, 99.50, 99.50, 99.50]
    }
  ]
}
```

---

### Actionable Recommendations

- **Isolate & Re-Scrub**: Quarantine the 42 flagged non-compliant email attachments and execute an enhanced Optical Character Recognition (OCR) re-scrubbing pass targeting non-standard utility bill uploads and payment checks.
- **Update Ingestion Filter Rules**: Deploy updated regex and NER (Named Entity Recognition) tokenizers on the inbound email gateway to intercept PII before indexing into the CRM repository.
- **Regulatory Notification Prep**: Prepare compliance ledger documentation in accordance with state consumer privacy disclosure guidelines.
- **Conduct Secondary Verification**: Run an automated differential validation scan following quarantine resolution to confirm 100% eradication of unencrypted PII artifacts.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PII_QUARANTINE_AND_BATCH_REDACTION",
  "affected_records": 42,
  "data_channels": ["Email Attachments / Customer Support Inbound"],
  "pii_entity_types": ["SSN", "Bank Routing/Account Numbers", "Driver License Numbers"],
  "proposed_action": "Execute destructive overwrite of unredacted raw attachment caches in regulatory compliance storage and replace with redacted cryptographic tokens.",
  "compliance_framework": "State Consumer Privacy Act / NERC-CIP / Utility PUC Mandate",
  "requires_hitl_approval": true,
  "approver_role": "Compliance Data Protection Officer / Lead Privacy Analyst"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Execute automated redaction of all sensitive PII from Customer Record #44921 before transmitting data to third-party auditors."

**Agent Response:**
### Executive Summary
**Automated PII scrubbing for Customer Record #44921 has successfully sanitized 100% of sensitive direct and indirect personal identifiers in compliance with NERC/FERC and EPA data privacy standards. All primary identifiers (SSN, Full Name, Billing/Bank Account Details, Precise Street Address) have been replaced with cryptographically salted pseudo-identifiers and tokenized telemetry attributes. The scrubbed record is fully prepared and isolated in the secure staging partition awaiting final compliance sign-off prior to third-party auditor export.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Direct PII Redaction Rate** | 100.0% | 100.0% | 0.0% | Normal |
| **Indirect/Quasi-Identifier Scrubbing** | 100.0% | 100.0% | 0.0% | Normal |
| **Financial/Billing Info Obfuscation** | 100.0% | 100.0% | 0.0% | Normal |
| **Audit Compliance Verification Score** | 100.0% | 100.0% | 0.0% | Normal |
| **Scrubbing Processing Latency** | 18 ms | < 500 ms | -96.4% | Normal |
| **Unredacted Residual Risk Level** | 0.00 | 0.00 | 0.0% | Normal |

---

### Visualization Triggers

**Recommended Visualization:** Horizontal Bar Chart representing PII category scrubbing completion and verification against enterprise compliance targets.

```json
{
  "chart_type": "bar",
  "title": "PII Redaction Audit Coverage - Customer #44921",
  "data": {
    "categories": [
      "Direct Identifiers (Name/SSN)",
      "Contact Info (Phone/Email)",
      "Billing & Financial (Bank/Card)",
      "Physical Location (Street/Apt)",
      "Usage/Meter Telemetry (Tokenized)"
    ],
    "redaction_rate_pct": [100.0, 100.0, 100.0, 100.0, 100.0],
    "threshold_target_pct": [100.0, 100.0, 100.0, 100.0, 100.0]
  }
}
```

---

### Redacted Field Mapping Summary
- **Full Legal Name**: `[REDACTED_ENTITY_ID: CUST-44921-ANON]`
- **Social Security Number (SSN)**: `[REDACTED_SSN_HASH_SHA256]`
- **Service Address**: Truncated to Feeder / Substation Node: `SUBSTATION-GRID-ZONE-04`
- **Phone / Email**: `[REDACTED_COMM_IDENTIFIER]`
- **Bank Account / Credit Card Info**: `[REDACTED_FIN_TOKEN]`
- **Interval Usage Data**: Preserved with anonymized meter asset ID `ASSET-101` for load profile verification.

---

### Actionable Recommendations
- Transmit the scrubbed dataset directly from the secure staging container `regulatory_compliance.audit_staging_scrubbed` to the external third-party auditor portal.
- Log the cryptographic SHA-256 hash of the sanitized export in the Immutable Compliance Audit Ledger.
- Verify auditor access tokens expire within the standard 48-hour regulatory review window.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EXTERNAL_DATA_TRANSMISSION",
  "target_entity": "Third-Party Compliance Audit Portal",
  "source_record_id": "44921",
  "sanitized_record_id": "CUST-44921-ANON",
  "redaction_status": "VERIFIED_CLEAN",
  "destination_protocol": "SFTP_TLS1.3_ENCRYPTED",
  "approval_required": true,
  "critic_agent_review": "PASSED"
}
```
