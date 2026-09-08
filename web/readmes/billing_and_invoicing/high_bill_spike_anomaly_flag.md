# ⚡ High Bill Spike Anomaly Flag

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of high bill spike anomaly flag is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — High Bill Spike Anomaly Flag Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank high bill spike anomaly flag events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.high_bill_spike_anomaly_flag_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which commercial accounts experienced an unexplained 300% billing increase compared to their 12-month seasonal median?"

**Agent Response:**
### Executive Summary
**Automated billing anomaly detection identified 4 commercial accounts exhibiting unexplained billing spikes exceeding +300% relative to their 12-month seasonal median.** **The cumulative anomalous revenue impact totals $129,570, driven primarily by meter multiplier misconfigurations, unresolved interval bridging errors, and unmetered phase bypasses.** **Immediate billing holds and meter validation audits have been flagged to prevent customer overbilling and regulatory non-compliance under Public Utility Commission (PUC) billing accuracy guidelines.**

---

### Data Presentation

#### Anomaly Overview Table
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **COMM-ACCT-88214 (Cold Storage Facility)** | $48,250.00 | $11,200.00 | +330.8% | **Critical** |
| **COMM-ACCT-41092 (Plastics Manufacturing)** | $36,120.00 | $8,500.00 | +324.9% | **Critical** |
| **COMM-ACCT-19305 (Retail Commercial Plaza)** | $29,800.00 | $6,800.00 | +338.2% | **Critical** |
| **COMM-ACCT-77341 (Data Processing Facility)** | $54,200.00 | $12,100.00 | +347.9% | **Critical** |
| **Total Commercial Spike Exposure** | **$168,370.00** | **$38,600.00** | **+336.2%** | **Critical** |

#### Diagnostic Breakdown

| Account ID | Rate Class | Grid Zone / Feeder | Current kWh (Prior Season kWh) | Root Cause Category | VEE Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **COMM-ACCT-88214** | Commercial TOU-3 | GZ-EAST-F14 | 386,000 kWh (89,600 kWh) | CT/PT Multiplier Error (10x vs 40x) | Validation Failed |
| **COMM-ACCT-41092** | Industrial Demand | GZ-IND-F02 | 288,960 kWh (68,000 kWh) | Unsynchronized Submeter Summation | Estimation Fallback |
| **COMM-ACCT-19305** | Commercial General | GZ-METRO-F08 | 238,400 kWh (54,400 kWh) | Ghost Interval Injection (AMI firmware glitch) | Validation Failed |
| **COMM-ACCT-77341** | Large Commercial CPP | GZ-NORTH-F19 | 433,600 kWh (96,800 kWh) | Unexplained Base Load Surge / Demand Ratchet Trigger | Failed Peak Review |

---

### Visualization Triggers
**Recommended Chart**: Grouped Bar Chart comparing Current Invoiced Amount vs. 12-Month Seasonal Median baseline across flagged commercial accounts.

```json
{
  "chart_type": "bar",
  "title": "Commercial Accounts with >300% Bill Spike vs 12-Month Seasonal Median",
  "xAxis": "Account ID",
  "yAxis": "Invoiced Total ($ USD)",
  "series": [
    {
      "name": "Current Bill Amount ($)",
      "data": [
        {"category": "COMM-ACCT-88214", "value": 48250},
        {"category": "COMM-ACCT-41092", "value": 36120},
        {"category": "COMM-ACCT-19305", "value": 29800},
        {"category": "COMM-ACCT-77341", "value": 54200}
      ]
    },
    {
      "name": "12-Month Seasonal Median ($)",
      "data": [
        {"category": "COMM-ACCT-88214", "value": 11200},
        {"category": "COMM-ACCT-41092", "value": 8500},
        {"category": "COMM-ACCT-19305", "value": 6800},
        {"category": "COMM-ACCT-77341", "value": 12100}
      ]
    }
  ]
}
```

---

### Actionable Recommendations

- **Place Pre-Issuance Billing Holds**: Intercept automated invoicing distribution for `COMM-ACCT-88214`, `COMM-ACCT-41092`, `COMM-ACCT-19305`, and `COMM-ACCT-77341` to prevent uncollectible billing disputes and customer escalations.
- **Trigger AMI Interval Data Reprocessing**: Execute VEE (Validation, Estimation, and Editing) raw packet re-runs for `COMM-ACCT-19305` and verify head-end telemetry sync.
- **Dispatch Meter Engineering Field Verification**: Issue physical work orders to inspect instrument transformer ratios (CT/PT) and phase wiring on `COMM-ACCT-88214` and `COMM-ACCT-41092`.
- **Customer Relationship Notification**: Alert assigned Key Account Managers prior to customer outbound communication with estimated resolution timelines.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "BILLING_HOLD_AND_REBILL_AUTHORIZATION",
  "target_accounts": [
    "COMM-ACCT-88214",
    "COMM-ACCT-41092",
    "COMM-ACCT-19305",
    "COMM-ACCT-77341"
  ],
  "hold_amount_total_usd": 168370.00,
  "action_description": "Supersede current billing cycle invoices with pending review status, quarantine interval telemetry, and dispatch metering technicians for onsite multiplier and hardware audit.",
  "required_approver_role": "Billing Operations Supervisor / Revenue Assurance Lead",
  "compliance_framework": "PUC Rule 17 / Revenue Protection & Meter Data Integrity"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate billing spike flags with meter multiplier errors, water heater faults, or stuck HVAC relays."

**Agent Response:**
### Executive Summary
**High bill spike anomalies have been cross-correlated against advanced interval telemetry (AMI 15-minute load profiles), meter asset management (MAM) configuration logs, and disaggregation signatures. The evaluation isolates three primary mechanical and configuration failure modes: meter multiplier misconfigurations (integer-step scalar shifts), continuous water heater element energization (unmodulated ~4.5 kW baseloads), and stuck HVAC auxiliary/compressor contactors (non-cycling 5–15 kW load floors). System-wide billing reconciliation identifies 247 accounts exhibiting these specific physical and administrative failure signatures, preventing erroneous billing dispatches and regulatory non-compliance.**

---

### Quantitative Correlation & Telemetry Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Meter Multiplier Mismatches (CT/PT Scalar Errors)** | 42 Accounts | 0 Accounts | +100.0% | **Critical** |
| **Water Heater Fault Signatures (Continuous 3.5–5.0 kW)** | 118 Accounts | < 10 Accounts | +1,080.0% | **Critical** |
| **Stuck HVAC Contactors / Aux Heat Runaway** | 87 Accounts | < 15 Accounts | +480.0% | **Warning** |
| **Mean Interval Baseload Floor (Flagged Population)** | 4.82 kW | 0.65 kW | +641.5% | **Critical** |
| **VEE Interval Validation Exception Rate** | 3.42% | < 0.50% | +584.0% | **Warning** |
| **Potential Unwarranted Customer Overbill Exposure** | $146,840.10 | $0.00 | +100.0% | **Critical** |

---

### Root Cause Signature Classification

```
                          ┌─────────────────────────────────────────────────┐
                          │         High Bill Spike Anomaly Detected        │
                          │        (AMI Interval > 3σ over Baseline)        │
                          └──────────────────────┬──────────────────────────┘
                                                 │
                   ┌─────────────────────────────┼─────────────────────────────┐
                   ▼                             ▼                             ▼
       [Integer Step Multiplier]      [Flat Constant Baseload]      [High-Load Severe Floor]
                   │                             │                             │
    • Scalar jump (10x, 40x, 120x)    • 24/7 unvarying 3.5-4.5 kW   • 5.0 - 15.0+ kW continuous
    • Raw pulse unchanged             • Zero weather correlation    • High heat/cooling correlation
    • Associated with meter swap      • Diurnal cycle absent        • Stuck contactor / strip heat
                   │                             │                             │
                   ▼                             ▼                             ▼
      Meter Multiplier Config               Water Heater                  HVAC Contactor /
            Error (MAM)                     Element Fault                 Aux Relay Stuck
```

1. **Meter Multiplier Configuration Errors (MAM/Billing Engine)**:
   - **Telemetry Pattern**: Load shape retains historical residential shape (peaking at morning/evening) but displays an exact integer scalar multiplication (e.g., $10\times$, $40\times$, $80\times$, $120\times$) occurring immediately following a meter reprogram, firmware update, or physical meter exchange.
   - **Validation Check**: Meter register pulses match historical volume, but Billing Determinant Data Store shows mismatched CT/PT ratio registers.

2. **Water Heater Element / Thermostat Faults**:
   - **Telemetry Pattern**: Continuous, non-cycling flat-line demand signature of $3.8\text{ kW} - 4.5\text{ kW}$ persisting 24 hours/day ($100\%$ duty cycle, zero off-periods even during overnight trough intervals $01:00 - 05:00$).
   - **Validation Check**: Zero correlation to Heating Degree Days (HDD) or Cooling Degree Days (CDD); temperature regression $R^2 < 0.05$.

3. **Stuck HVAC Compressor / Auxiliary Heat Relays**:
   - **Telemetry Pattern**: Elevated baseload of $5.0\text{ kW} - 12.0\text{ kW}$ continuous draw with loss of standard thermostat modulation/cycling; auxiliary resistive heat bank locked in closed contact.
   - **Validation Check**: Moderate-to-high seasonal weather sensitivity with sudden transition into locked non-cycling maximum demand floor.

---

### Visualizer Telemetry Output

```json
{
  "chart_type": "bar",
  "title": "Root Cause Distribution of High Bill Spike Anomalies",
  "categories": [
    "Meter Multiplier Config Error",
    "Water Heater Element Fault (Continuous Draw)",
    "Stuck HVAC Contactor / Aux Heat Relay",
    "Customer Operational / Behavioral Shift",
    "Unresolved / Pending Field Audit"
  ],
  "series": [
    {
      "name": "Flagged Account Count",
      "data": [42, 118, 87, 65, 14]
    },
    {
      "name": "Mean Bill Impact ($)",
      "data": [1280.5, 312.4, 545.8, 185.2, 420.0]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Billing Hold Placements**:
   - Immediately place automated billing holds on the 42 accounts with confirmed Meter Multiplier scalar jumps to avoid sending erroneous invoices and incurring regulatory billing dispute penalties.
2. **Customer Proactive Notification & Disaggregation Alerts**:
   - Dispatch automated AMI continuous-load notifications to the 118 accounts exhibiting water heater failure profiles ($>3.5\text{ kW}$ flat baseload for $>48\text{ hours}$) to mitigate property damage risks (e.g., T&P valve discharge).
   - Flag the 87 HVAC contactor accounts for Customer Service / Home Energy Audit outreach detailing unmodulated resistive heat consumption.
3. **MAM & Billing Determinant Audit**:
   - Re-sync Meter Asset Management (MAM) CT/PT ratio tables with the Customer Information System (CIS) billing engine for all work orders executed within the prior 60 days.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "BILLING_HOLD_AND_ADJUSTMENT_DISPATCH",
  "affected_accounts_count": 42,
  "financial_exposure": "$53,781.00",
  "description": "Approval required to place manual billing holds on 42 identified accounts with CT/PT meter multiplier configuration discrepancies, suppress automatic bill print/dispatch, and initiate CIS rate determinant re-calculation.",
  "compliance_reference": "PUC Rule 16 / ANSI C12.1 Meter Accuracy Standards",
  "requires_hitl_approval": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Place a temporary billing hold on Account #882194 to prevent auto-debit pending on-site meter re-verification."

**Agent Response:**
### Executive Summary
**A critical high bill spike anomaly has been detected on Account #882194, indicating an unexpected 330.2% variance above historical baseline consumption. To protect the customer from unauthorized or inaccurate financial deductions, a temporary billing and auto-debit hold must be placed pending physical on-site meter re-verification. Because this action alters the financial processing state and prevents automated settlement, it requires human operator confirmation.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Current Cycle Invoiced Volume** | 1,850.0 kWh | 430.0 kWh | +330.2% | **Critical** |
| **Current Cycle Billed Amount** | $518.00 | $120.40 | +330.2% | **Critical** |
| **Interval VEE Integrity Score** | 62.0% | 99.5% | -37.7% | **Critical** |
| **Peak Demand Spike** | 14.2 kW | 4.8 kW | +195.8% | **Warning** |
| **Auto-Debit Scheduled Execution** | Pending (T-24h) | Standard Schedule | N/A | **Warning** |

---

### Visualization Triggers
- **Recommended Chart Type:** Time-Series Line Chart (Multi-Cycle Comparison)
- **Visualization Payload:**
```json
{
  "chart_type": "line",
  "title": "Account #882194 Historical vs Billed Interval Trend",
  "xAxis": {
    "categories": ["Cycle -4", "Cycle -3", "Cycle -2", "Cycle -1", "Current Cycle"]
  },
  "yAxis": {
    "title": "Consumption (kWh)"
  },
  "series": [
    {
      "name": "Baseline Consumption (kWh)",
      "data": [420, 435, 410, 450, 430]
    },
    {
      "name": "Current Cycle Invoiced (kWh)",
      "data": [420, 435, 410, 450, 1850]
    }
  ]
}
```

---

### Actionable Recommendations
- **Dispatch Field Services:** Issue an automated high-priority work order for on-site physical meter verification, optical port download, and CT/PT ratio verification.
- **Suspend Collection Notices:** Ensure automated delinquency notices or late payment fees are suppressed while the billing hold is active.
- **Audit Telemetry Stream:** Validate head-end AMI interval data against substation feeder totalizers to check for potential meter multiplier/firmware mapping discrepancies.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "BILLING_HOLD_AND_AUTODEBIT_SUSPENSION",
  "tier_level": 2,
  "requires_hitl": true,
  "parameters": {
    "account_id": "882194",
    "hold_type": "TEMPORARY_DISPUTE_INVESTIGATION",
    "suspend_auto_debit": true,
    "suppress_late_fees": true,
    "trigger_reason": "High Bill Spike Anomaly (+330.2% above baseline)",
    "duration_days": 14,
    "field_investigation_required": true
  },
  "impact_assessment": {
    "financial_impact": "Prevents scheduled auto-debit of $518.00 until meter re-verification is completed.",
    "compliance_alignment": "Complies with PUC billing dispute protection standards and ratepayer protection mandates."
  },
  "status": "AWAITING_HUMAN_CONFIRMATION"
}
```
