# ⚡ Nerc Cip Cybersecurity Audit Analyzer

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of nerc cip cybersecurity audit analyzer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Nerc Cip Cybersecurity Audit Analyzer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank nerc cip cybersecurity audit analyzer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.nerc_cip_cybersecurity_audit_analyzer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are all Electronic Security Perimeters (ESP) and physical access control logs for Substation Control Rooms compliant with NERC CIP-005?"

**Agent Response:**
### Executive Summary
**Current telemetry and audit log evaluations indicate that Electronic Security Perimeters (ESPs) under NERC CIP-005 maintain a 96.8% aggregate compliance rate, with minor open access remediation tickets identified at remote substation gateways. Physical access control logs for Substation Control Rooms are governed primarily under NERC CIP-006 (Physical Security of BES Cyber Systems), which currently tracks at a 97.8% logging and retention compliance rate across medium- and high-impact control rooms. Neither perimeter domain is at 100% full compliance; active non-conformance items require immediate administrative and technical remediation prior to the upcoming quarterly audit filing.**

---

### Regulatory Alignment Note
* **NERC CIP-005-6 (Electronic Security Perimeter(s))**: Governs Electronic Access Points (EAPs), External Routable Connectivity (ERC), Inbound/Outbound firewall rule sets, and Interactive Remote Access (IRA) controls for BES Cyber Systems.
* **NERC CIP-006-6 (Physical Security of BES Cyber Systems)**: Specifically mandates Physical Security Perimeters (PSPs), badge/biometric entry control, visitor escort logs, and physical access logging/monitoring for Substation Control Rooms.

---

### Quantitative Compliance Audit Results

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **CIP-005-6 R1: ESP & Inbound/Outbound Routing Rules** | 98.2% | 100.0% | -1.8% | **Warning** |
| **CIP-005-6 R2: Interactive Remote Access & MFA Enforcement** | 95.4% | 100.0% | -4.6% | **Warning** |
| **CIP-005-6 R3: Vendor Remote Access & Disconnection Controls** | 97.0% | 100.0% | -3.0% | **Warning** |
| **CIP-006-6 R1/R2: Physical Security Plan & Visitor Escort Logs** | 96.8% | 100.0% | -3.2% | **Warning** |
| **CIP-006-6 R3: Physical Access Logging & 90-Day Retention** | 97.5% | 100.0% | -2.5% | **Warning** |
| **Overall NERC CIP Audit Compliance Rate** | **96.98%** | **100.0%** | **-3.02%** | **Warning** |

---

### Visualization Trigger: CIP-005 vs. CIP-006 Compliance Distribution

```json
{
  "chart_type": "bar",
  "title": "NERC CIP-005 & CIP-006 Requirement Adherence vs Baseline",
  "data": {
    "categories": [
      "CIP-005 R1 (ESP Rules)",
      "CIP-005 R2 (Remote Access/MFA)",
      "CIP-005 R3 (Vendor IRA)",
      "CIP-006 R1/R2 (Visitor Logs)",
      "CIP-006 R3 (Access Logging)"
    ],
    "series": [
      {
        "name": "Audit Adherence Rate (%)",
        "data": [98.2, 95.4, 97.0, 96.8, 97.5]
      },
      {
        "name": "NERC Standard Baseline (%)",
        "data": [100.0, 100.0, 100.0, 100.0, 100.0]
      }
    ]
  }
}
```

---

### Findings & Actionable Recommendations

1. **Remediate Open ESP Ingress Rules (CIP-005-6 R1.2)**:
   - Review and terminate 4 stale diagnostic ports identified across Substation Intermediate Systems / Electronic Access Points (EAPs).
   - Ensure all inbound/outbound communications are restricted to documented, business-justified BES network traffic.
2. **Standardize Physical Access Control Log Ingestion (CIP-006-6 R3.1)**:
   - Resolve automated physical access log synchronization gaps detected at 3 remote substations where physical security controller telemetry is delayed beyond 24 hours.
   - Verify that all physical access event data and manual sign-in sheets maintain the mandatory 90-day continuous retention window.
3. **MFA & Intermediate System Verification (CIP-005-6 R2.1)**:
   - Audit intermediate jump-host access logs to verify that multi-factor authentication (MFA) was enforced on 100% of Interactive Remote Access sessions over the preceding 30 days.
4. **Prepare Evidence Dossier**:
   - Package all firewall configuration baselines, change tickets, and physical badging archives for Regional Entity (e.g., SERC/WECC/ReliabilityFirst) audit submission.

### Example 2: Trend & Comparative Analysis
**User:** "Audit firewall rules, open ports, and transient cyber asset (laptop) patching records against NERC CIP-007 and CIP-010 standards."

**Agent Response:**
### Executive Summary
**The NERC CIP Cybersecurity Compliance Audit identified an overall compliance rating of 94.4% across CIP-007 (Systems Security Management) and CIP-010 (Configuration Change Management & TCA Security) assets.** While Electronic Security Perimeter (ESP) firewall rules and logical port restrictions demonstrate high adherence, critical compliance gaps exist in Transient Cyber Asset (TCA) laptop patch status (88.6%) and 35-calendar-day patch mitigation documentation under CIP-007 R2. Immediate remediation and formal mitigation documentation are required to prevent potential Potential Non-Compliance (PNC) findings during regional entity audits (e.g., Texas RE, WECC, SERC).

---

### Quantitative Audit Findings

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **CIP-007 R1: ESP Firewall Rule Business Justification** | 98.4% Documented | 100.0% | -1.6% | **Warning** |
| **CIP-007 R1: Unneeded Logical Ports & Services Disabled** | 95.8% Compliant | 100.0% | -4.2% | **Warning** |
| **CIP-007 R2: Patch Evaluation Cycle (35-Day Window)** | 92.1% Evaluated | 100.0% | -7.9% | **Critical** |
| **CIP-010 R1: BES Cyber System Baseline Configurations** | 97.5% Aligned | 100.0% | -2.5% | **Normal** |
| **CIP-010 R4: TCA Laptop Patch Status Prior to Connection** | 88.6% Compliant | 100.0% | -11.4% | **Critical** |
| **CIP-010 R4: TCA Antivirus Signature Currency (< 7 Days)** | 94.2% Current | 100.0% | -5.8% | **Warning** |

---

### Compliance Detail & Root Cause Analysis

1. **Firewall Rules & Logical Ports (CIP-007-6 R1)**:
   - **Finding**: 4 active firewall rules across Substation BES Cyber Asset (BCA) ingress perimeters lacked active business justifications and associated ticketing references in the Electronic Security Perimeter (ESP) rulebase.
   - **Finding**: 6 assets within Grid Zone 3 were identified with listening logical ports (TCP 21, TCP 23) that were not declared in the baseline port inventory.

2. **Patch Management & Evaluation (CIP-007-6 R2)**:
   - **Finding**: 3 critical security advisories released over 35 calendar days ago lack documented mitigation plans or dated patch evaluation records in the patch tracking registry.

3. **Transient Cyber Assets / Laptops (CIP-010-3 R4)**:
   - **Finding**: 8 field service laptops used by maintenance contractors for Relay & RTU direct connections lacked cryptographic verification and patch updates matching the authorized 30-day TCA baseline prior to physical ESP ingress.

---

### Visualization Trigger: NERC CIP Compliance Breakdown

```json
{
  "chart_type": "bar",
  "title": "NERC CIP-007 & CIP-010 Compliance Audit Status",
  "categories": [
    "Firewall Rule Justifications (CIP-007 R1)",
    "Logical Open Port Restrictions (CIP-007 R1)",
    "Patch Evaluation / 35-Day Window (CIP-007 R2)",
    "TCA Patch Baseline Adherence (CIP-010 R4)",
    "TCA Antivirus/Malware Updates (CIP-010 R4)",
    "Baseline Configuration Verification (CIP-010 R1)"
  ],
  "series": [
    {
      "name": "Compliance Rate (%)",
      "data": [98.4, 95.8, 92.1, 88.6, 94.2, 97.5]
    },
    {
      "name": "Target Threshold (%)",
      "data": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0]
    }
  ]
}
```

---

### Actionable Recommendations

- **Transient Cyber Asset (TCA) Lockdown**: Immediately revoke ESP connection tokens for non-compliant field engineering laptops until offline patch staging and malware scans (< 7 days) are verified and signed off.
- **Firewall Rulebase Cleanup**: Disable or document business justification for the 4 unjustified perimeter rules within 5 business days to satisfy CIP-007-6 R1.2 evidence requirements.
- **Patch Mitigation Filing**: Draft and approve CIP-007-6 R2.3 dated mitigation plans for the 3 overdue vendor security advisories, specifying compensating controls and target installation windows.
- **Port Remediation**: Execute configuration rollbacks on the 6 Grid Zone 3 assets to close unauthorized listening services (FTP/Telnet) and enforce encrypted protocols (SFTP/SSH).

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "COMPLIANCE_EVIDENCE_REMEDIATION_AND_RULE_MODIFICATION"
  target_assets:
    - "ESP-FW-SUB-Z3-01"
    - "ESP-FW-SUB-Z3-02"
    - "TCA-LAPTOP-POOL-MAINT"
  standards_impacted: ["NERC CIP-007-6", "NERC CIP-010-3"]
  proposed_actions:
    - "Revoke ESP physical/logical access for 8 unpatched TCA laptops"
    - "Disable undeclared listening ports (TCP 21, 23) across 6 Substation BCAs"
    - "Submit formal CIP-007 R2.3 Patch Mitigation Plan to Utility Compliance Officer"
  requires_human_approval: true
  approval_roles: ["Chief Compliance Officer", "Lead CIP Senior Manager (CSM)"]
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate an immediate mitigation ticket and revoke unapproved VPN credentials for third-party contractor accounts."

**Agent Response:**
### **Executive Summary**
**An immediate NERC CIP compliance violation (CIP-004 R4 / CIP-005 R2) has been detected involving unapproved third-party contractor VPN credentials accessing Electronic Security Perimeters (ESP). Autonomous credential revocation and active directory modification constitute Tier 2 operations requiring explicit Human-In-The-Loop (HITL) authorization before automated execution. A formal mitigation ticket draft and remediation payload have been staged for immediate operator approval and enforcement.**

---

### **Data Presentation: NERC CIP Access & Credential Audit**

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Active Unapproved Contractor Accounts** | 4 Accounts | 0 Accounts | +400.0% | **Critical** |
| **ESP Remote Access Authentication Rate (MFA/Authorized)** | 82.5% | 100.0% | -17.5% | **Critical** |
| **CIP-004 Personnel Risk Assessment (PRA) Validity** | 75.0% Valid | 100.0% Valid | -25.0% | **Warning** |
| **Quarterly Access Privilege Verification (CIP-004 R4)** | Overdue (98 Days) | ≤ 90 Days | +8.9% | **Warning** |
| **Audit Compliance Rate (Access Control)** | 68.0% | 100.0% | -32.0% | **Critical** |

---

### **Visualization Trigger**
*Recommended Chart: Categorical Bar Chart / Access Distribution Breakdown across Electronic Access Points (EAPs).*

```json
{
  "chart_type": "bar",
  "title": "Third-Party Remote Access Status by Substation/ESP Node",
  "data": [
    {"node": "EAP-North-Sub-01", "authorized_sessions": 12, "unapproved_sessions": 2},
    {"node": "EAP-South-Sub-04", "authorized_sessions": 8, "unapproved_sessions": 1},
    {"node": "EAP-ControlCenter-Primary", "authorized_sessions": 25, "unapproved_sessions": 1},
    {"node": "EAP-West-Gen-02", "authorized_sessions": 14, "unapproved_sessions": 0}
  ],
  "series": [
    {"name": "Authorized Active Sessions", "field": "authorized_sessions"},
    {"name": "Unapproved Active Sessions", "field": "unapproved_sessions"}
  ]
}
```

---

### **Actionable Recommendations**
- **Immediate Credential Isolation**: Approve the staged Tier 2 action below to lock directory objects, terminate active SSL-VPN/IPsec tunnels, and invalidate Kerberos/OAuth tokens for flagged third-party contractor accounts.
- **Log Archival & Forensics**: Isolate authentication and packet logs from Intermediate Systems and ESP border firewalls for the last 90 days to satisfy CIP-007 R5 and CIP-008 incident investigation retention rules.
- **Root Cause & Vendor Risk Review**: Initiate an emergency CIP-013 supply chain risk evaluation with vendor account sponsors to determine why access provisioning bypassed standard CIP-004 7-day termination/transfer authorization workflows.
- **Self-Report Filing Prep**: Prepare a preliminary Notice of Violation (self-log/self-report) package for the Regional Entity (e.g., WECC, SERC, Texas RE) documenting discovery time, exposure window, and remediation actions.

---

### **[TIER 2 ACTION REQUIRED]**

```json
{
  "action_type": "IAM_CREDENTIAL_REVOCATION_AND_SESSION_TERMINATION",
  "ticket_id": "INC-CIP-2025-04882",
  "severity": "CRITICAL",
  "compliance_framework": "NERC CIP-004 R4 / CIP-005 R2",
  "target_directory": "LDAP://CORP-AUTH.UTILITY.INTERNAL/OU=Contractors,OU=ThirdParty",
  "targeted_identities": [
    {
      "account_id": "ext_vendor_jdoe_91",
      "vpn_profile": "Vendor-Tier3-ESP-Access",
      "associated_esp": "ESP-Zone-A-Substations",
      "action": "REVOKE_AND_TERMINATE_SESSION"
    },
    {
      "account_id": "ext_vendor_msmith_44",
      "vpn_profile": "Vendor-Tier3-ESP-Access",
      "associated_esp": "ESP-Zone-B-ControlCenter",
      "action": "REVOKE_AND_TERMINATE_SESSION"
    },
    {
      "account_id": "ext_vendor_rgarcia_12",
      "vpn_profile": "Vendor-SCADA-Maintenance",
      "associated_esp": "ESP-Zone-A-Substations",
      "action": "REVOKE_AND_TERMINATE_SESSION"
    },
    {
      "account_id": "ext_vendor_tlee_88",
      "vpn_profile": "Vendor-EMS-Support",
      "associated_esp": "ESP-Zone-C-Generation",
      "action": "REVOKE_AND_TERMINATE_SESSION"
    }
  ],
  "hitl_approval_required": true,
  "approver_role": "CIP Senior Manager / Lead Cybersecurity Operations Engineer",
  "execution_timeout_minutes": 15
}
```

*To execute credential revocation and terminate all active sessions, confirm approval of ticket `INC-CIP-2025-04882`.*
