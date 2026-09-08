# ⚡ Zero Consumption Anomaly Flag

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of zero consumption anomaly flag is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Zero Consumption Anomaly Flag Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank zero consumption anomaly flag events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.zero_consumption_anomaly_flag_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which commercial smart meters have reported continuous zero kWh consumption for the past 14 days despite active account status?"

**Agent Response:**
### Executive Summary
**A total of 31 commercial smart meters across 5 operational grid zones have exhibited continuous 0.00 kWh energy consumption over the preceding 14 consecutive billing days despite maintaining an active account status. Telemetry health checks indicate active AMI mesh network connectivity with no reported communication dropouts, establishing a high probability of potential current transformer (CT) bypass, potential meter tampering, phase disconnection, or silent hardware failure. Prompt localized dispatch and automated meter diagnostics are required to mitigate unbilled commercial load and revenue leakage.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Active Commercial Meters Flagged (Zero kWh)** | 31 Meters | 0 Meters | +100.0% | **Critical** |
| **14-Day Cumulative Flagged Consumption** | 0.00 kWh | 186,450.00 kWh (Hist. Avg) | -100.0% | **Critical** |
| **Average AMI Ping Success Rate** | 99.4% | ≥ 98.0% | +1.4% | **Normal** |
| **Unbilled Revenue Exposure (Est.)** | $27,967.50 | $0.00 | +100.0% | **Critical** |
| **Tamper / Inversion Flags Logged** | 8 Flags | 0 Flags | +100.0% | **Warning** |

#### Segmented Meter Exception Breakdown (Top Grid Zones)

| Meter ID | Account Ref (Masked) | Grid Zone ID | Feeder ID | Consecutive 0 kWh Days | Tamper Sensor State | Hardware / Firmware |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `MTR-COM-88214` | `ACC-***4892` | `Zone-Central-04` | `FDR-CN-12A` | 14 | Closed / No Flag | FW v4.12.1 |
| `MTR-COM-88309` | `ACC-***1143` | `Zone-Central-04` | `FDR-CN-12A` | 14 | Inversion Alert | FW v4.12.1 |
| `MTR-COM-74102` | `ACC-***9820` | `Zone-North-02` | `FDR-NO-04C` | 14 | Terminal Cover Open | FW v3.98.0 |
| `MTR-COM-74188` | `ACC-***3321` | `Zone-North-02` | `FDR-NO-04C` | 14 | Closed / No Flag | FW v4.12.1 |
| `MTR-COM-91045` | `ACC-***6501` | `Zone-South-02` | `FDR-SO-08B` | 14 | Closed / No Flag | FW v4.10.4 |
| `MTR-COM-63201` | `ACC-***7719` | `Zone-East-03` | `FDR-EA-01A` | 14 | Phase Loss Flag | FW v4.12.1 |
| `MTR-COM-55190` | `ACC-***0087` | `Zone-North-01` | `FDR-NO-02A` | 14 | Closed / No Flag | FW v4.10.4 |

---

### Visualization Trigger
**Recommended Chart**: Clustered Bar Chart illustrating zero-consumption commercial anomalies across operational grid zones.

```json
{
  "chart_type": "bar",
  "title": "Commercial Meters with 14-Day Zero Consumption by Grid Zone",
  "xaxis": {
    "categories": ["Zone-Central-04", "Zone-North-02", "Zone-South-02", "Zone-North-01", "Zone-East-03"],
    "title": "Grid Zone"
  },
  "yaxis": {
    "title": "Number of Flagged Meters"
  },
  "series": [
    {
      "name": "Zero-Consumption Meters",
      "data": [12, 7, 5, 4, 3]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Initiate Remote Phase Voltage & Current Diagnostics**: Execute on-demand high-resolution waveform polling across the 31 flagged meters to verify whether line voltage is present with zero secondary current (indicating open CT or physical disconnect).
2. **Prioritize Physical Field Audits**: Schedule priority field inspections for the 8 meters presenting concurrent tamper or terminal cover status flags.
3. **Trigger VEE (Validation, Editing, and Estimation) Estimation Pipeline**: Queue estimated baseline billing profiles in the meter data management system (MDMS) pursuant to applicable state PUC estimation guidelines for commercial classes.
4. **Firmware Integrity Check**: Audit `FW v3.98.0` endpoints in `Zone-North-02` for register lockup vulnerabilities.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FIELD_INVESTIGATION_AND_METER_AUDIT_DISPATCH",
  "domain": "Smart Meter Management",
  "impact_scope": {
    "total_meters": 31,
    "customer_class": "Commercial",
    "affected_grid_zones": ["Zone-Central-04", "Zone-North-02", "Zone-South-02", "Zone-North-01", "Zone-East-03"],
    "estimated_revenue_at_risk_per_month": "$59,930.00"
  },
  "proposed_operation": "Issue Field Service Orders (FSO) for physical onsite tamper/CT inspection and apply MDMS VEE baseline estimation flags to billing accounts.",
  "approval_required_from": "Meter Operations Supervisor / Lead Revenue Protection Officer",
  "safety_and_compliance_verification": "IEEE C12.1 / ANSI C12.20 accuracy and safety standards verified. No direct load interruption will occur during initial inspection."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Filter zero-read accounts against move-out records, seasonal vacation properties, and potential current transformer (CT) failures."

**Agent Response:**
### Executive Summary
**A total of 2,590 zero-consumption meter accounts were processed through the multi-stage VEE (Validation, Editing, and Estimation) filtration engine.** **Cross-referencing against CIS billing states and AMI electrical telemetry isolated 1,420 authorized move-out/vacant accounts (54.8%) and 865 seasonal/vacation properties (33.4%), eliminating 88.2% of false positives.** **A critical subset of 142 meters exhibited nominal line voltage (>118V per phase) alongside persistent zero-current register reads, flagging confirmed Potential Current Transformer (CT) secondary open-circuit or wiring failures requiring immediate field remediation.**

---

### Quantitative Evaluation & Anomaly Classification

The table below summarizes the key performance indicators and classification metrics for the evaluated zero-read population:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Zero-Read AMI Endpoints** | 2,590 meters | 2,450 meters | +5.71% | Warning |
| **Validated Move-Out / Vacant Accounts** | 1,420 accounts | 1,380 accounts | +2.90% | Normal |
| **Seasonal / Vacation Premises Flagged** | 865 accounts | 850 accounts | +1.76% | Normal |
| **Potential CT / Transducer Failures** | 142 meters | < 25 meters | +468.0% | **Critical** |
| **Suspected Meter Tamper / Bypass** | 48 meters | < 15 meters | +220.0% | **Critical** |
| **True Low/Zero Standby Usage** | 115 accounts | 180 accounts | -36.11% | Normal |
| **VEE False-Positive Suppression Rate** | 88.22% | > 85.00% | +3.79% | Normal |

---

### Detailed Filtering Logic & Root-Cause Breakdown

```
[Total Zero-Read Accounts (2,590)]
   │
   ├──► CIS State = "Inactive / Move-Out / Final Read" ─────────► [1,420 Accounts] Filtered: Expected Inactivity
   │
   ├──► Tariff/Historical = "Seasonal / Vacation Profile" ──────► [865 Accounts] Filtered: Normal Low-Load Season
   │
   └──► Active Premise & Non-Seasonal (305 Accounts)
         │
         ├──► Nominal Voltage + Zero Current + Polyphase CT/PT ─► [142 Accounts] Flagged: Potential CT Circuit Failure
         ├──► Phase Imbalance / Open Neutral / Reverse Energy ──► [48 Accounts]  Flagged: Tamper / Metrology Bypass
         └──► Zero Real Power (Active Substation/Feeder Flow) ──► [115 Accounts] Filtered: True Standby / Solar Offset
```

1. **Move-Out / Vacancy Validation**: Accounts matched against Customer Information System (CIS) service status `INACT` / `MOVE_OUT` with pending final billing. Remote disconnect state confirmed where applicable.
2. **Seasonal / Vacation Profiling**: Identified via 24-month historical interval regression (winter/summer occupancy patterns), primary residence codes, and vacation-rate classes.
3. **Current Transformer (CT) Failure Logic**: Flagged commercial and industrial (C&I) / polyphase installations where Phase A/B/C voltages are active ($\pm 3\%$ of nominal 120/240V or 277/480V), while $I_{rms} = 0.00\text{ A}$ alongside feeder-level load persistence or CT ratio mismatch telemetry.

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "data_json": {
    "title": "Zero-Consumption Account Categorization & Root-Cause Filtering",
    "categories": [
      "Move-Out / Vacant Premises",
      "Seasonal / Vacation Rate Class",
      "Potential CT / Meter Hardware Failure",
      "Tamper / Unmetered Load Suspect",
      "True Zero Low-Usage / Standby"
    ],
    "series": [
      {
        "name": "Meter Count",
        "data": [1420, 865, 142, 48, 115]
      }
    ]
  }
}
```

---

### Actionable Recommendations

1. **Suppression of Legitimate Inactivity**:
   - Auto-clear VEE exception queues for the 1,420 move-out records and 865 seasonal accounts to prevent unnecessary estimated billing adjustments.
2. **Field Meter Test Work Order Generation**:
   - Dispatch metering technicians to inspect the 142 flagged CT installations for blown secondary fuses, disconnected CT shorting blocks, or open-circuit wiring.
3. **Revenue Protection Investigation**:
   - Route the 48 suspected tamper/bypass endpoints to Revenue Protection teams for physical seal verification and phase angle validation.
4. **Interval Monitoring**:
   - Place the remaining 115 true zero standby meters under a 14-day high-frequency (15-minute interval) monitoring watch list to verify seasonal re-energization or solar generation net-zero balance.

---

### Human-In-The-Loop Confirmation

**[TIER 2 ACTION REQUIRED]**
- **Operation**: Automated Bulk Dispatch of Field Investigation Work Orders (C&I CT/PT Metering Units).
- **Target Count**: 142 High-Priority Commercial & Industrial Endpoints.
- **Estimated Operational Cost**: $18,460 ($130/site diagnostic dispatch).
- **Potential Revenue at Risk**: ~$210,000/month in unbilled energy throughput.
- **Required Approval**: Meter Operations Supervisor confirmation required prior to dispatching field work packages.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Schedule an on-site field meter technician visit to inspect Account #10492 for defective current sensors or internal meter failure."

**Agent Response:**
### Executive Summary
**Zero consumption anomaly analysis for Account #10492 indicates sustained 0.0 kWh interval registrations across consecutive billing cycles despite an active service status and continuous mesh network ping connectivity. Telemetry signatures strongly correlate with a defective current transformer (CT) sensor array or internal metrology unit failure rather than a physical vacancy. Initiating an on-site field meter technician dispatch constitutes a Tier 2 operational action and requires formal Human-in-the-Loop (HITL) authorization prior to work order execution.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Interval Energy Registration** | 0.00 kWh/day | 27.20 kWh/day | -100.0% | **Critical** |
| **AMI Mesh Communication Health** | 99.4% (Active) | ≥ 98.0% | +1.4% | **Normal** |
| **Meter Line Voltage (L1/L2)** | 240.2 V | 240.0 V | +0.08% | **Normal** |
| **Current Sensor Signal (CT Output)**| 0.00 A | 12.50 A | -100.0% | **Critical** |
| **Tamper / Inversion Flag Status** | Clear (No Flag) | Clear | 0.0% | **Normal** |
| **Meter Metrology Health Score** | 14.2 / 100 | ≥ 85.0 / 100 | -83.3% | **Critical** |

---

### Visualization Triggers
- **Recommended Chart**: Time-Series Line Chart illustrating active interval consumption drop against historical baseline.

```json
{
  "chart_type": "line",
  "title": "Account #10492 - 7-Day Interval Consumption vs Baseline",
  "labels": ["Day -6", "Day -5", "Day -4", "Day -3", "Day -2", "Day -1", "Day 0"],
  "series": [
    {
      "name": "Actual Consumption (kWh)",
      "data": [28.4, 26.1, 27.5, 0.0, 0.0, 0.0, 0.0]
    },
    {
      "name": "Expected Baseline (kWh)",
      "data": [27.0, 26.5, 27.0, 28.0, 27.5, 26.8, 27.2]
    }
  ]
}
```

---

### Actionable Recommendations
- **Authorize Field Dispatch**: Review and approve the Tier 2 payload below to generate and issue the Field Service Work Order to metering operations.
- **Run Metrology Diagnostic Protocol**: Dispatch an over-the-air (OTA) diagnostic interrogation to retrieve internal registers and firmware event logs prior to technician roll.
- **Apply Temporary VEE Billing Estimation**: Trigger automated Validation, Editing, and Estimation (VEE) rules to substitute estimated intervals based on historical load profiles until physical meter replacement or repair is verified.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FIELD_SERVICE_DISPATCH",
  "account_id": "10492",
  "asset_id": "ASSET-101",
  "work_order_type": "METER_INVESTIGATION_REPLACEMENT",
  "priority": "HIGH",
  "dispatch_reason": "Zero consumption anomaly with active voltage telemetry; suspected current sensor or internal metrology failure",
  "safety_checks_passed": true,
  "required_approval": "HUMAN_OPERATOR_CONFIRMATION",
  "status": "PENDING_APPROVAL"
}
```
