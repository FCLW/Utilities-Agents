# ⚡ Electric Vehicle Submeter Billing Processor

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of electric vehicle submeter billing processor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Electric Vehicle Submeter Billing Processor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank electric vehicle submeter billing processor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.electric_vehicle_submeter_billing_processor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did the submetered Level 2 EV charger at account #449210 properly isolate charging kWh from the main household consumption?"

**Agent Response:**
### Executive Summary
**Submetering reconciliation for Account #449210 confirmed successful load disaggregation between the Level 2 EVSE submeter and the primary utility revenue meter.** **All charging intervals were accurately isolated and netted out of the primary household consumption ($kWh_{\text{Net}} = kWh_{\text{Gross}} - kWh_{\text{EV}}$) with zero negative baseline artifacts or interval alignment mismatches.** **The EV-specific consumption has been routed to the designated EV-TOU rate schedule without double-counting or unbilled revenue leakage.**

---

### Quantitative Reconciliation & Validation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **EV Submeter Total Volume** | 324.50 kWh | 320.00 kWh (Historical Avg) | +1.41% | **Normal** |
| **Main Meter Gross Volume** | 842.10 kWh | 835.00 kWh | +0.85% | **Normal** |
| **Net Household Baseload** | 517.60 kWh | 515.00 kWh | +0.50% | **Normal** |
| **Subtractive VEE Validation Rate** | 100.0% | 99.50% | +0.50% | **Normal** |
| **Negative Interval Delta Instances** | 0 intervals | 0 intervals | 0.00% | **Normal** |
| **Timestamp Alignment Latency** | < 1.2 sec | $\le$ 15.0 sec | -92.00% | **Normal** |

---

### Subtractive Billing Analysis Details

1. **Subtractive Billing Rule Compliance**:
   - Interval-by-interval subtraction verified: $kWh_{\text{Primary Net}} = \max(0, kWh_{\text{Main Gross}} - kWh_{\text{EV Submeter}})$.
   - EV submeter consumption never exceeded gross main meter intake during any 15-minute settlement interval.
2. **TOU Disaggregation**:
   - **Super Off-Peak / Off-Peak (EV Charging Window)**: 324.50 kWh billed at EV-TOU Tier 1 rate.
   - **On-Peak / Part-Peak**: 0.00 kWh recorded on EVSE; standard residential tiered rate applied solely to baseline household load.
3. **Data Quality & Integrity**:
   - No missing intervals detected across the active settlement cycle.
   - CRC checksum validation passed for all ANSI C12.20 Class 0.5 submeter telemetry packets.

---

### Visualization

```json
{
  "title": "Account #449210 - Main Meter vs EV Submeter Load Isolation Profile",
  "chart_type": "line",
  "xAxis": {
    "categories": ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"],
    "title": "Settlement Interval (TOU Window)"
  },
  "yAxis": {
    "title": "Energy Consumption (kWh)"
  },
  "series": [
    {
      "name": "Main Meter Gross Consumption (kWh)",
      "data": [8.2, 8.5, 7.9, 2.1, 1.8, 1.5, 1.4, 1.6, 2.8, 3.4, 4.1, 8.0]
    },
    {
      "name": "EV Submeter Dedicated Load (kWh)",
      "data": [7.2, 7.2, 6.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 6.5]
    },
    {
      "name": "Net Baseline Household Load (kWh)",
      "data": [1.0, 1.3, 1.1, 2.1, 1.8, 1.5, 1.4, 1.6, 2.8, 3.4, 4.1, 1.5]
    }
  ]
}
```

---

### Actionable Recommendations

- **Post to Billing Engine**: Release the reconciled interval dataset for Account #449210 to the standard billing cycle generator for bill presentment.
- **Maintain Telemetry Sync**: Continue monitoring the 15-minute NTP timestamp synchronization between the Level 2 EVSE submeter gateway and the primary AMI headend.
- **Automated VEE Guardrail**: Retain automated threshold checks to alert if $kWh_{\text{EV Submeter}} > kWh_{\text{Main Gross}}$ in any future interval.

### Example 2: Trend & Comparative Analysis
**User:** "Audit interval charging records to ensure zero double-counting of net-metered residential solar exports against EV submeters."

**Agent Response:**
### Executive Summary
**The Electric Vehicle Submeter Billing Processor completed a comprehensive interval-level disaggregation audit across net-metered residential solar paired accounts. Submeter subtraction logic and settlement algorithms confirmed that solar export credits ($kWh_{NEM\_export}$) and EV interval consumption ($kWh_{EV\_submeter}$) remain mathematically isolated with zero double-counting anomalies detected. All interval billing calculations adhere strictly to PUC Rule 21 and applicable TOU/NEM tariff settlement protocols.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Double-Counted Solar Export Inaccuracies** | 0.00 kWh | 0.00 kWh | 0.00% | Normal |
| **VEE Interval Success Rate** | 99.94% | $\ge$ 99.50% | +0.44% | Normal |
| **Submeter Subtraction Disaggregation Precision** | 100.0% | 100.0% | 0.00% | Normal |
| **Coincident Peak TOU Alignment Accuracy** | 99.88% | $\ge$ 99.00% | +0.88% | Normal |
| **Net Unbilled Revenue Leakage Delta** | \$0.00 | \$0.00 | 0.00% | Normal |

---

### Visualization Triggers
**Recommended Visualization:** Time-Series Interval Line Chart comparing Primary Net Meter Solar Exports, EV Submeter Dedicated Charging Consumption, and Disaggregated Net Billed Quantities across 15-minute intervals.

```json
{
  "chart_type": "line",
  "title": "EV Submeter vs. Solar NEM Disaggregation Audit",
  "xAxis": "interval_timestamp",
  "yAxis": "kWh",
  "series": [
    {
      "name": "Primary Meter Export (NEM)",
      "data": [
        {"x": "2023-10-24 12:00", "y": 4.2},
        {"x": "2023-10-24 13:00", "y": 5.1},
        {"x": "2023-10-24 14:00", "y": 4.8},
        {"x": "2023-10-24 15:00", "y": 3.2},
        {"x": "2023-10-24 16:00", "y": 1.5},
        {"x": "2023-10-24 17:00", "y": 0.0}
      ]
    },
    {
      "name": "EV Submeter Consumption",
      "data": [
        {"x": "2023-10-24 12:00", "y": 3.5},
        {"x": "2023-10-24 13:00", "y": 6.8},
        {"x": "2023-10-24 14:00", "y": 7.2},
        {"x": "2023-10-24 15:00", "y": 7.0},
        {"x": "2023-10-24 16:00", "y": 6.5},
        {"x": "2023-10-24 17:00", "y": 6.2}
      ]
    },
    {
      "name": "Reconciled Net Billed Baseline",
      "data": [
        {"x": "2023-10-24 12:00", "y": 3.5},
        {"x": "2023-10-24 13:00", "y": 6.8},
        {"x": "2023-10-24 14:00", "y": 7.2},
        {"x": "2023-10-24 15:00", "y": 7.0},
        {"x": "2023-10-24 16:00", "y": 6.5},
        {"x": "2023-10-24 17:00", "y": 6.2}
      ]
    }
  ]
}
```

---

### Actionable Recommendations
- **Continuous Interval Validation**: Maintain automated daily VEE validation runs matching primary meter net channel exports with secondary EV submeter consumption records.
- **Rule Verification**: Maintain the subtraction methodology: $$\text{House Net Load} = \text{Primary Meter Net} - \text{EV Submeter Load}$$ ensuring solar NEM credits are computed solely against primary export channels without double-crediting charging consumption.
- **Reconciliation Sign-Off**: Release audited interval billing runs for downstream settlement and final bill cycle processing upon human verification.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FINANCIAL_BILLING_BATCH_FINALIZATION",
  "domain": "Billing And Invoicing",
  "agent": "electric_vehicle_submeter_billing_processor",
  "audit_scope": "Residential Solar NEM & EV Submeter Interval Billing Cycle",
  "status": "AWAITING_HUMAN_APPROVAL",
  "payload": {
    "audit_verified": true,
    "double_count_delta_kwh": 0.00,
    "total_intervals_audited": 2880,
    "target_billing_cycle": "2023-M10",
    "recommended_action": "Approve final billing batch release for residential EV submeter accounts with paired solar NEM."
  }
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Apply the discounted overnight EV-9 charging tariff credit to submetered charging sessions for Account #449210."

**Agent Response:**
### 1. Executive Summary
**Submetered electric vehicle interval telemetry for Account #449210 was successfully validated and reconciled against the overnight EV-9 charging tariff schedule (23:00–06:00 window). A total of 340.50 kWh across 14 qualifying overnight charging sessions was processed with 100% VEE data validation, yielding a total gross billing credit of $40.86. Final financial settlement and ledger posting have been staged pending mandatory Human-in-the-Loop (HITL) Tier 2 approval.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Submetered Consumption** | 340.50 kWh | 325.00 kWh | +4.77% | Normal |
| **EV-9 Overnight Window Compliance** | 100.0% | ≥ 98.0% | +2.04% | Normal |
| **VEE Validation Pass Rate** | 100.0% | ≥ 99.5% | +0.50% | Normal |
| **Standard Baseline Rate (TOU-Off-Peak)** | $0.240 / kWh | $0.240 / kWh | 0.00% | Normal |
| **Discounted EV-9 Overnight Tariff** | $0.120 / kWh | $0.120 / kWh | 0.00% | Normal |
| **Net Applied Billing Credit** | -$40.86 | -$39.00 | +4.77% | Normal |
| **Revenue Leakage / Unmetered Delta** | 0.00 kWh | 0.00 kWh | 0.00% | Normal |

---

### 3. Visualization Triggers
- **Recommended Chart Type**: Stacked Bar Chart (Standard Cost vs. EV-9 Net Cost vs. Calculated Tariff Credit by Session Interval).

```json
{
  "chart_type": "bar",
  "title": "Account #449210 EV-9 Overnight Tariff Reconciliation",
  "data": {
    "labels": ["Week 1 Overnight", "Week 2 Overnight", "Week 3 Overnight", "Week 4 Overnight"],
    "datasets": [
      {
        "label": "Standard TOU Cost ($)",
        "data": [20.40, 19.80, 21.12, 20.40]
      },
      {
        "label": "EV-9 Net Billed ($)",
        "data": [10.20, 9.90, 10.56, 10.20]
      },
      {
        "label": "EV-9 Tariff Credit ($)",
        "data": [10.20, 9.90, 10.56, 10.20]
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations
- **Approve Financial Credit Posting**: Authorize the credit memo payload to post the -$40.86 line-item credit to Account #449210's pending statement cycle.
- **Maintain Automated Interval Polling**: Continue automated daily polling of Submeter ID `SM-EV-449210-01` at 15-minute interval granularity.
- **Customer Notification**: Dispatch automated billing portal notification confirming successful enrollment and credit processing under Schedule EV-9.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FINANCIAL_BILLING_CREDIT_APPLICATION",
  "account_id": "449210",
  "submeter_id": "SM-EV-449210-01",
  "tariff_code": "EV-9_OVERNIGHT",
  "billing_cycle": "2024-M03",
  "qualifying_kwh": 340.50,
  "credit_rate_per_kwh": 0.120,
  "total_credit_amount_usd": -40.86,
  "validation_status": "VEE_PASSED",
  "requires_hitl_confirmation": true
}
```
