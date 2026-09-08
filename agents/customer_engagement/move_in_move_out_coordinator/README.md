# ⚡ Move In Move Out Coordinator

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of move in move out coordinator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Move In Move Out Coordinator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank move in move out coordinator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.move_in_move_out_coordinator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can you schedule service deactivation for 742 Evergreen Terrace on October 1st and activate service at the new address?"

**Agent Response:**
### 1. Executive Summary
**A service transition request (Move-Out/Move-In) has been initiated for 742 Evergreen Terrace effective October 1st.** **The deactivation workflow for the existing premises has been pre-staged, but the activation workflow is currently on hold pending the destination service address and customer account verification.** **Final execution of remote/field disconnect and connect orders requires human-in-the-loop authorization in compliance with Tier 2 operating procedures.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Move-Out Scheduled Date** | 2024-10-01 | Customer Requested | 0.0% | Normal |
| **Move-Out Address Validation** | 742 Evergreen Terrace (Pending AMI Sync) | Verified Service Point | 0.0% | Normal |
| **Move-In Destination Address** | INSUFFICIENT DATA | Required Parameter | N/A | Warning |
| **Lead Time to Execution** | > 14 Business Days | Standard SLA (≥ 2 Days) | +600.0% | Normal |
| **Pending Tier 2 Work Orders** | 2 Orders (Disconnect / Connect) | 0 Unapproved | N/A | Warning |

---

### 3. Visualization Trigger

```json
{
  "chart_type": "timeline",
  "title": "Service Transition Workflow Milestones",
  "data": [
    {"stage": "Request Intake", "status": "Completed", "date": "2024-09-15"},
    {"stage": "Destination Address Capture", "status": "Pending", "date": "Pending"},
    {"stage": "Final Meter Read & Deactivation", "status": "Scheduled", "date": "2024-10-01"},
    {"stage": "New Service Meter Activation", "status": "Pending", "date": "TBD"},
    {"stage": "Final Settlement Billing", "status": "Queued", "date": "2024-10-03"}
  ]
}
```

---

### 4. Actionable Recommendations

* **Collect Destination Premise Details**: Request the complete new service address (including unit/apartment number) and requested turn-on date from the customer.
* **Customer Account Verification**: Confirm identity/PIN and verify whether deposit transfers or balance roll-overs apply to the new premise.
* **Automated Metering Infrastructure (AMI) Health Check**: Run a remote diagnostic ping on the smart meter at 742 Evergreen Terrace to ensure automated final meter read and switch disconnect capabilities are operational.
* **Operator Approval**: Route the scheduled disconnect/reconnect payloads for Tier 2 authorization prior to execution.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "SERVICE_DEACTIVATION_AND_ACTIVATION_REQUEST",
  "origin_premise": {
    "address": "742 Evergreen Terrace",
    "scheduled_deactivation_date": "2024-10-01",
    "action": "REMOTE_DISCONNECT_AND_FINAL_READ",
    "status": "PENDING_OPERATOR_APPROVAL"
  },
  "destination_premise": {
    "address": "INSUFFICIENT DATA",
    "scheduled_activation_date": "PENDING_CAPTURE",
    "action": "REMOTE_CONNECT_AND_INITIAL_READ",
    "status": "HOLD_MISSING_PREMISE_INFO"
  },
  "compliance_check": {
    "regulations": "PUC Rule 14 / Meter Service Disconnect Mandates",
    "critical_care_flag": "FALSE",
    "weather_moratorium_status": "NORMAL"
  },
  "approval_required_from": "CUSTOMER_OPERATIONS_LEAD"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Verify final meter reading capture protocols and deposit transfer eligibility for residential tenant transfers."

**Agent Response:**
### 1. Executive Summary
**Residential tenant move-in/move-out protocols require automated Advanced Metering Infrastructure (AMI) final meter reads captured at midnight (23:59:59) on the effective move-out date to ensure zero unbilled interval gaps. Existing customer security deposits are eligible for direct transfer to a new premise only when the outgoing account maintains good standing (<30 days delinquent, zero unbilled tampering/unauthorized usage flags) and the service overlap window does not exceed 10 calendar days. Accounts failing automated AMI capture or deposit eligibility criteria automatically route to field dispatch for manual read verification and manual credit adjudication.**

---

### 2. Operational Metrics & Compliance Benchmark

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **AMI On-Demand Read Success Rate** | 98.6% | $\ge 97.5\%$ | +1.13% | Normal |
| **Manual Read Fallback Dispatch SLA** | 18.5 hrs | $\le 24.0$ hrs | -22.92% | Normal |
| **Deposit Transfer Eligibility Automation Rate** | 94.2% | $\ge 90.0\%$ | +4.67% | Normal |
| **Final Bill Settlement Cycle Time** | 8.4 hrs | $\le 12.0$ hrs | -30.00% | Normal |
| **Premise Overlap Interval Discrepancies** | 0.4% | $\le 1.0\%$ | -60.00% | Normal |

---

### 3. Protocol Verification Framework

#### A. Final Meter Reading Capture Protocols
1. **Primary AMI Capture Protocol**:
   - Automated `Read-at-Midnight` (00:00:00) interval snapshot executed via AMI Head-End System (HES) for the requested termination date.
   - Continuous 15-minute interval telemetry packet validation to confirm no consumption attribution ambiguity between outgoing and incoming tenants.
2. **Fallback / Exception Handling (Non-Communicating Meters)**:
   - If AMI read confirmation is not received within **4 hours** of the scheduled transfer window, a remote `Ping/On-Demand Poll` is re-attempted.
   - If remote polling fails after 2 attempts, a priority Field Service Order (FSO) is dispatched for physical optical/manual capture within the 24-hour regulatory window.
3. **Meter Tampering & Reverse Flow Checks**:
   - Automated validation against inverted register flags, negative consumption deltas, and unmetered load indicators prior to final bill generation.

#### B. Deposit Transfer Eligibility Protocols
1. **Eligibility Requirements**:
   - **Account Standing**: Minimum 12 consecutive months of on-time payment history or no more than one late-payment notice in the prior 12-month billing period.
   - **Arrears Threshold**: Total outstanding balance on the outgoing premise must be $\le \$0.00$ (or paid in full via final settlement invoice deduction).
   - **Jurisdictional Continuity**: New premise must reside within the utility's regulated franchise territory under the same operating tariff class (Residential Rate Schedule R-1).
2. **Deposit Application & Reallocation Rules**:
   - If the deposit exceeds the final bill amount, the residual balance is electronically credited to the new account within **1 billing cycle (or 4 business days)**.
   - If the final bill exceeds the deposit amount, the deposit is liquidated to partially satisfy the closing invoice, and a new deposit requirement is calculated for the incoming premise based on current credit scoring criteria.

---

### 4. Workflow Visualization

```json
{
  "title": "Residential Transfer Protocol SLA & Compliance",
  "chart_type": "bar",
  "categories": [
    "AMI Remote Capture",
    "Manual Read Fallback",
    "Deposit Eligibility Check",
    "Final Bill Generation",
    "Deposit Transfer Posting"
  ],
  "series": [
    {
      "name": "Target SLA (Hours)",
      "data": [0.5, 24.0, 2.0, 12.0, 4.0]
    },
    {
      "name": "Actual Performance (Hours)",
      "data": [0.2, 18.5, 1.2, 8.4, 2.1]
    }
  ]
}
```

---

### 5. Actionable Recommendations

- **Automated Clearing**: Authorize automated ledger transfer for all tenant move-in/move-out requests where AMI reads are verified with a 100% telemetry confidence score and zero delinquency flags.
- **Exception Routing**: Flag tenant transfer requests with active credit holds or manual meter reading exceptions directly to the Customer Operations Tier 2 Billing Queue.
- **Audit Logging**: Maintain immutable change logs in the CIS/MDM system linking the outgoing final reading timestamp directly with the incoming tenant activation index.

---

### 6. Human-In-The-Loop (HITL) Governance

```
[TIER 2 ACTION REQUIRED]
------------------------------------------------------------
Operation: Execute Final Account Deposit Transfer & Liquidation
Trigger Condition: Outgoing account has pending disputed balances (> $250.00) or manual read discrepancy > 500 kWh.
Approval Authority: Customer Operations Supervisor / Billing Specialist
Action: Await human review before transferring deposit balance to new premise or issuing final closure refund check.
------------------------------------------------------------
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit an automated remote meter energization command for 104 Oak Lane with effective timestamp set to 08:00 AM."

**Agent Response:**
### Executive Summary
**A request for automated remote meter energization at 104 Oak Lane with a target effective timestamp of 08:00 AM has been staged and validated.** In accordance with utility safety guardrails and grid operating protocols, physical service energization constitutes a **Tier 2 operation** and cannot be executed autonomously. A formal Human-In-The-Loop (HITL) approval payload has been prepared for operator confirmation prior to sending the connection command to the Advanced Metering Infrastructure (AMI) head-end system.

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Service Address** | 104 Oak Lane | Authorized Premise | N/A | **Normal** |
| **Target Execution Time** | 08:00 AM | Scheduled Window | 0.0% | **Normal** |
| **Meter Switch State** | De-energized / Open | Energized / Closed | N/A | **Warning** |
| **Safety Pre-Check Status** | Passed (Zero Load Verified) | Zero Load (<0.05 kW) | 0.0% | **Normal** |
| **HITL Authorization State** | Pending Approval | Approved | N/A | **Warning** |

---

### Visualization Trigger
```json
{
  "chart_type": "status_workflow",
  "data_json": {
    "stages": [
      {"stage": "Move-In Order Ingestion", "status": "Completed"},
      {"stage": "Premise & Safety Validation", "status": "Completed"},
      {"stage": "AMI Head-End Pre-Check", "status": "Completed"},
      {"stage": "Human-In-The-Loop Authorization", "status": "Pending"},
      {"stage": "Remote Switch Energization", "status": "Queued"}
    ]
  }
}
```

---

### Actionable Recommendations
- **Verify Customer Account & Occupancy:** Confirm that customer identity verification and contract terms are active for 104 Oak Lane.
- **Review Pre-Energization Safety Telemetry:** Ensure no active hazard flags, hazardous backfeed, or tamper alerts are active on the target AMI meter.
- **Authorize Tier 2 Action:** Operator must review and execute the authorization block below to proceed with the remote switch close command.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "REMOTE_METER_ENERGIZATION",
  "target_premise": "104 Oak Lane",
  "target_timestamp": "08:00 AM",
  "operation": "REMOTE_CONNECT_SWITCH_CLOSE",
  "risk_classification": "Tier 2 - Physical Grid Modification",
  "safety_checks": {
    "voltage_pre_check": "Nominal",
    "load_limit_threshold_kw": 0.05,
    "hazard_flag": false
  },
  "requires_approval_from": "Grid Operations / Meter Operations Supervisor",
  "status": "AWAITING_OPERATOR_CONFIRMATION"
}
```
