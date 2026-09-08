# ⚡ Scada Vpn Access Helpdesk Bot

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of scada vpn access helpdesk bot is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Scada Vpn Access Helpdesk Bot Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank scada vpn access helpdesk bot events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.scada_vpn_access_helpdesk_bot_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Why is an authorized control center operator's hardware security token failing authentication for SCADA network access?"

**Agent Response:**
### Executive Summary
**Hardware security token authentication failures for authorized SCADA control center operators typically stem from internal clock drift on the physical token, expired security certificates/seed records, or account lockout thresholds triggered per NERC CIP-007 access control policies.** **Additional potential failure modes include RADIUS/TACACS+ authentication server synchronization timeouts across the Electronic Security Perimeter (ESP) or desynchronized token seed databases.** **Immediate diagnostic steps require verifying token drift windows, auditing Electronic Access Points (EAP/VPN concentrator) logs, and validating multi-factor authentication (MFA) server reachability.**

---

### Diagnostic Telemetry & Metric Evaluation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Token Clock Drift Window** | $\pm 180\text{ sec}$ | $\le \pm 30\text{ sec}$ | $+500.0\%$ | **Critical** |
| **RADIUS/MFA Round-Trip Latency** | $4,250\text{ ms}$ | $\le 500\text{ ms}$ | $+750.0\%$ | **Critical** |
| **Consecutive Failed Auth Attempts** | $5\text{ attempts}$ | $< 3\text{ attempts}$ | $+66.7\%$ | **Warning** |
| **Token Certificate / Seed Validity** | Active (142 days remaining) | $> 30\text{ days}$ | $0.0\%$ | **Normal** |
| **IAM Group / NERC CIP Role Match** | `SCADA-OPS-ZONE1` | `SCADA-OPS-ZONE1` | $0.0\%$ | **Normal** |

---

### Common Root Causes & Technical Breakdown

1. **Hardware Token Clock Drift (TOTP Desynchronization):**
   - Time-based One-Time Password (TOTP) hardware tokens rely on an internal quartz crystal clock. Over time or through thermal variance, the token clock drifts outside the authentication server's allowable time-step acceptance window (typically $\pm 1$ step / 30–60 seconds).
2. **Account Lockout Policy (NERC CIP-007 R5 Enforcement):**
   - If the operator repeatedly entered the rolling passcode without the PIN (or vice versa), the identity provider (IdP) or RADIUS/PAM server locks the account after 3 to 5 failed attempts to prevent brute-force attacks on the Electronic Access Point (EAP).
3. **EAP to RADIUS/LDAP Communication Timeout:**
   - VPN concentrators routing requests through intermediate firewalls to the SCADA Identity Server may drop UDP packets or exceed authentication timeout thresholds ($>4.0\text{ s}$), resulting in a generic "Authentication Failed" response on the client side.
4. **Token Revocation / Seed Expiration:**
   - The token serial number assignment may have expired, been de-provisioned during a security credential refresh cycle, or had its seed database corrupted on the secondary redundant AAA cluster.

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "data_json": "{\"title\": \"SCADA Remote Access Authentication Failure Breakdown (Last 24h)\", \"categories\": [\"Token Clock Drift\", \"MFA/RADIUS Timeout\", \"Account Lockout (Failed Attempts)\", \"Invalid PIN Entry\", \"Token Expired/De-assigned\"], \"series\": [{\"name\": \"Incident Count\", \"data\": [14, 8, 6, 4, 1]}]}"
}
```

---

### Actionable Recommendations

- **Step 1: Perform Token Resynchronization in MFA Admin Console:**
  - Execute a manual 2-passcode resynchronization (prompt operator for two consecutive rolling codes) via the Identity/MFA Manager to recalculate and store the token offset.
- **Step 2: Check Electronic Access Point (EAP) Audit Logs:**
  - Query VPN Gateway and AAA logs for error codes: `ERR_AUTH_REJECT_CLOCK_SKEW`, `ERR_USER_LOCKED`, or `RADIUS_TIMEOUT`.
- **Step 3: Verify Active Directory & Role-Based Access Control (RBAC):**
  - Confirm the operator's account has not been disabled by scheduled credential rotation or NERC CIP annual training compliance holds.
- **Step 4: Issue Hardware Token Replacement (If Drift > Threshold):**
  - If the token internal clock drift exceeds recovery parameters ($> \pm 5\text{ minutes}$), retire the physical fob and bind a replacement token via dual-custody verification.

---

### [TIER 2 ACTION REQUIRED]
```yaml
Operation: SCADA_ACCOUNT_UNLOCK_AND_TOKEN_RESYNC
Target Account: Operator ID (Redacted per CIP-004)
Target Device: SCADA-VPN-EAP-01 / Identity Provider Cluster
Trigger Condition: Consecutive Auth Failures / Token Resync Request
HITL Approval Required: Control Center Security Administrator (Tier 2 Sign-off)
Compliance Standard: NERC CIP-005-7 (Electronic Security Perimeter) & NERC CIP-007-6 (Access Management)
```

### Example 2: Trend & Comparative Analysis
**User:** "Audit VPN connection logs, source IP geolocations, and dual-custody access policies against NERC CIP-005 requirements."

**Agent Response:**
### Executive Summary
**The comprehensive audit of SCADA VPN connection telemetry against NERC CIP-005-6/7 requirements identified a 98.48% total compliance posture across 1,759 Interactive Remote Access (IRA) sessions.** **While dual-custody authorization and Intermediate System (Jump Host) routing remained strictly enforced for critical Bulk Electric System (BES) cyber assets, 18 inbound connection attempts from unauthorized non-domestic geolocations and 9 single-custody authorization failures were intercepted at the electronic perimeter.** **Immediate containment rules and credential reviews have been initiated to prevent potential unauthorized access pathways into high-impact substation control zones.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **NERC CIP-005 Compliant IRA Sessions** | 1,732 sessions | 1,759 (100%) | -1.53% | **Warning** |
| **Dual-Custody Policy Adherence Rate** | 99.49% | 100.00% | -0.51% | **Warning** |
| **Intermediate System (Jump Host) Compliance** | 100.00% | 100.00% | 0.00% | **Normal** |
| **Non-Whitelisted Geo-IP Connection Attempts** | 18 attempts | 0 attempts | +100.00% | **Critical** |
| **Failed MFA / Dual-Custody Escalations** | 9 attempts | 0 attempts | +100.00% | **Warning** |
| **Egress / Ingress Port Hardening Non-Conformances** | 0 instances | 0 instances | 0.00% | **Normal** |

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "SCADA VPN Inbound Connection Compliance Audit (NERC CIP-005)",
  "categories": [
    "Domestic Authorized (Dual-Custody)",
    "Remote Field Substation (Authorized)",
    "Unapproved Geolocation (Blocked)",
    "Single-Factor / Failed Dual-Custody",
    "Intermediate System Bypass Attempt"
  ],
  "series": [
    {
      "name": "Audited Sessions",
      "data": [1420, 312, 18, 9, 0]
    }
  ],
  "y_axis_label": "Session Count",
  "notes": "Data filtered across high-impact and medium-impact BES Cyber Systems (BCS) over the 30-day trailing audit period."
}
```

---

### Actionable Recommendations

- **Geo-Fencing Rule Hardening**: Enforce strict upstream BGP/IP-reputation and geo-fencing drop rules at the Electronic Security Perimeter (ESP) perimeter firewalls to reject unauthorized foreign and non-whitelisted ASN traffic before reaching the VPN concentrator.
- **Dual-Custody Protocol Review**: Re-certify all 9 user accounts associated with incomplete or mismatched dual-custody MFA handshakes to ensure both operator and supervisor cryptographic keys are validated.
- **Evidence Dossier Generation**: Compile signed syslog audit trails, radius authentication dumps, and intermediate jump box access logs into the NERC CIP Compliance Evidence Locker for annual audit readiness.
- **Automated Revocation**: Immediately revoke expired contractor access profiles associated with completed substation maintenance tickets.

---

### Tier 2 Human-in-the-Loop Payload

```json
[TIER 2 ACTION REQUIRED]
{
  "action_type": "FIREWALL_ACL_UPDATE_AND_CREDENTIAL_ISOLATION",
  "authority_reference": "NERC_CIP_005_R2_R3",
  "target_assets": [
    "ESP-VPN-GW-01",
    "ESP-VPN-GW-02",
    "SUBSTATION-BCS-ZONE-4"
  ],
  "parameters": {
    "quarantine_user_ids": ["USR-SCADA-8842", "USR-CTR-9913"],
    "ip_blacklist_cidrs": ["185.220.101.0/24", "194.26.29.0/24"],
    "enforce_strict_dual_custody": true
  },
  "required_approver": "Chief Information Security Officer / SCADA Operations Manager"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Reset multi-factor authentication credentials for Dispatcher User #D-902 after confirming out-of-band identity verification."

**Agent Response:**
### 1. Executive Summary
**Dispatcher User #D-902 has successfully passed out-of-band (OOB) identity verification for SCADA VPN multi-factor authentication (MFA) remediation.** **In accordance with NERC CIP-005/CIP-007 Electronic Security Perimeter access standards, the active MFA token revocation and enrollment key regeneration are staged and awaiting mandatory Human-in-the-Loop (HITL) authorization.** **No unauthorized or autonomous credential modifications have been executed prior to supervisor sign-off.**

---

### 2. Identity Verification & Access Status

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **User Identity Validation** | Verified (OOB Callback) | 100% Verified | 0.0% | **Normal** |
| **Active Session State** | Terminated / Locked | Terminated | 0.0% | **Normal** |
| **Failed Auth Attempts (24h)** | 5 | < 3 | +66.7% | **Warning** |
| **Role-Based Access Level** | SCADA Tier-1 Dispatcher | SCADA Tier-1 Dispatcher | 0.0% | **Normal** |
| **NERC CIP Background Clearance**| Active / Valid | Active | 0.0% | **Normal** |

---

### 3. Visualization Trigger

```json
{
  "chart_type": "bar",
  "data": {
    "labels": ["OOB Voice Callback", "Manager Approval", "CIP Clearance Check", "Token Revocation Staging", "HITL Authorization"],
    "datasets": [
      {
        "label": "MFA Reset Workflow Progress (%)",
        "data": [100, 100, 100, 100, 0]
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations
- **Complete HITL Approval**: Authorize the credential reset payload below to invalidate the compromised/locked hardware/software token and generate a one-time activation seed.
- **Enforce Secure Re-Enrollment**: Mandate that User #D-902 complete enrollment within a 15-minute temporary provisioning window from an authorized corporate IP.
- **Audit Logging**: Ensure the complete event trail, including the out-of-band verification recording ID, is archived to the security information and event management (SIEM) log repository.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "SCADA_VPN_MFA_RESET",
  "target_user_id": "D-902",
  "user_role": "Dispatcher",
  "verification_method": "Out-of-Band Phone Verification (Ref: OOB-2023-8821)",
  "compliance_framework": "NERC CIP-005-6 / CIP-007-6",
  "staged_operations": [
    "REVOKE_EXISTING_MFA_TOKEN",
    "CLEAR_FAILED_LOGIN_COUNTER",
    "ISSUE_TIMED_REGISTRATION_SEED"
  ],
  "requires_approval": true,
  "approver_role": "SCADA Security Administrator / Operations Duty Manager"
}
```
