# ⚡ Net Metering Export Credit Processor

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of net metering export credit processor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Net Metering Export Credit Processor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank net metering export credit processor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.net_metering_export_credit_processor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the total dollar credit owed to residential rooftop solar owners for surplus energy exported to the grid last billing cycle?"

**Agent Response:**
### 1. Executive Summary
**For the most recent billing cycle, total surplus energy exported by residential rooftop solar participants across all operating zones reached 11,152.20 MWh, resulting in a total net metering export credit owed of $892,176.00.** **This represents a +6.4% increase in surplus export volume compared to the historical baseline, driven by favorable irradiance conditions and higher residential PV interconnection capacity.** **All export intervals have successfully passed Validation, Estimation, and Editing (VEE) checks with zero unbilled leakage detected across all feeder nodes.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Export Credit Owed ($)** | $892,176.00 | $838,500.00 | +6.40% | Normal |
| **Total Surplus Energy Exported (MWh)** | 11,152.20 MWh | 10,481.25 MWh | +6.40% | Normal |
| **Active Residential Solar Accounts** | 18,420 accounts | 17,950 accounts | +2.62% | Normal |
| **Effective Weighted Export Rate ($/kWh)** | $0.0800 / kWh | $0.0800 / kWh | 0.00% | Normal |
| **VEE Validation Pass Rate (%)** | 99.98% | 99.50% | +0.48% | Normal |
| **Revenue / Credit Leakage Anomaly Rate** | 0.00% | < 0.05% | 0.00% | Normal |

---

### 3. Visualization Triggers

```json
{
  "chart_type": "bar",
  "title": "Residential Solar Export Credit Settlement by Zone - Last Billing Cycle",
  "xAxis": {
    "title": "Grid Operating Zone",
    "categories": ["Zone A (North)", "Zone B (Central)", "Zone C (South)", "Zone D (Metro)", "Zone E (Coastal)"]
  },
  "yAxis": [
    {
      "title": "Dollar Credit Owed ($)",
      "format": "currency"
    },
    {
      "title": "Exported Energy (MWh)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Dollar Credit Owed ($)",
      "type": "column",
      "data": [113640.00, 174424.00, 244064.00, 151216.00, 208832.00]
    },
    {
      "name": "Exported Energy (MWh)",
      "type": "line",
      "yAxis": 1,
      "data": [1420.50, 2180.30, 3050.80, 1890.20, 2610.40]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Post Bill Ledger Credits**: Disburse the validated $892,176.00 net metering export credits to the customer billing accounts for the current billing run in accordance with State PUC net billing tariffs.
- **Review High-Export Feeders in Zone C**: Zone C accounted for 27.35% ($244,064.00) of all residential export credits; ensure bi-directional voltage regulation telemetry is continuously monitored during peak solar hours (11:00–15:00).
- **Tariff True-Up Reconciliation**: Track cumulative annual credits for accounts approaching their annual net metering true-up date to process excess generation cash-outs or rollovers according to approved rate schedules.

---

### 5. HITL / Tier 2 Action Required

```yaml
[TIER 2 ACTION REQUIRED]
operation: POST_FINANCIAL_SETTLEMENT_CREDIT_BATCH
target_domain: Billing And Invoicing
total_accounts_impacted: 18420
total_financial_credit_amount: "$892,176.00"
billing_cycle_id: "BILL-CYCLE-2024-M09"
tariff_schedule: "NEM-2.0-RESIDENTIAL"
audit_validation: "VEE Verified (99.98% pass rate, 0 unbilled intervals)"
confirmation_required: "Approve ledger posting of export credits to customer statements."
```

### Example 2: Trend & Comparative Analysis
**User:** "Reconcile customer solar export kWh credits calculated at avoided-cost tariff rates versus full retail net metering rules."

**Agent Response:**
### 1. Executive Summary
**Reconciliation of customer solar generation export data indicates a significant financial credit divergence between Full Retail Net Energy Metering (NEM 1.0/2.0) and the Avoided-Cost Tariff (NEM 3.0/Net Billing) framework. For a standardized 620 kWh monthly export profile, the avoided-cost credit yields $36.60 compared to $173.60 under full retail 1:1 offsetting, representing a -78.92% net reduction in bill credits. Transitioning rate structures eliminates a cross-subsidization cost shift of $137.00 per customer-cycle while properly aligning customer remuneration with real-time wholesale energy and marginal grid capacity values.**

---

### 2. Data Presentation

The table below details the billing interval reconciliation, comparing Full Retail Net Metering baseline credits against hourly/TOU Avoided-Cost Calculator (ACC) tariff rates across representative TOU export intervals.

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Solar Export Volume** | 620.00 kWh | 620.00 kWh | 0.00% | `Normal` |
| **On-Peak Export Credit Value** | $13.80 ($0.115/kWh) | $45.60 ($0.380/kWh) | -69.74% | `Warning` |
| **Mid-Peak (Solar Noon) Credit Value** | $18.24 ($0.048/kWh) | $106.40 ($0.280/kWh) | -82.86% | `Critical` |
| **Off-Peak Export Credit Value** | $4.56 ($0.038/kWh) | $21.60 ($0.180/kWh) | -78.89% | `Warning` |
| **Total Gross Export Credit** | **$36.60** (Avoided-Cost) | **$173.60** (Retail NEM) | **-78.92%** | `Critical` |
| **Effective Weighted Export Rate** | $0.0590 / kWh | $0.2800 / kWh | -78.93% | `Critical` |
| **Fixed Customer & Grid Access Charge** | $15.00 / month | $0.00 / month | +100.00% | `Normal` |
| **Net Customer Monthly Bill Impact** | $188.40 due | $51.40 due | +266.54% | `Warning` |
| **Interval VEE Validation Rate** | 100.00% | 99.85% | +0.15% | `Normal` |

*Assumptions: Gross Consumption = 850 kWh; Gross Generation = 1,120 kWh; Net Import = 350 kWh ($110.00); Net Export = 620 kWh. Retail TOU import rates: On-Peak $0.38/kWh, Mid-Peak $0.28/kWh, Off-Peak $0.18/kWh. Avoided-Cost values derive from hourly marginal energy + deferred generation/distribution capacity metrics.*

---

### 3. Visualization Trigger

**Recommended Chart Type:** Grouped Bar Chart / Stacked Interval Delta  
**Purpose:** Illustrates credit breakdown and valuation divergence by TOU bin between full retail net metering rates and avoided-cost valuation schedules.

```json
{
  "chart_type": "bar",
  "title": "Solar Export Credit Reconciliation: Full Retail NEM vs. Avoided-Cost Tariff",
  "data": {
    "categories": [
      "On-Peak Export (120 kWh)",
      "Mid-Peak Export (380 kWh)",
      "Off-Peak Export (120 kWh)",
      "Total Billing Cycle (620 kWh)"
    ],
    "series": [
      {
        "name": "Full Retail NEM Credit ($)",
        "data": [45.60, 106.40, 21.60, 173.60]
      },
      {
        "name": "Avoided-Cost Tariff Credit ($)",
        "data": [13.80, 18.24, 4.56, 36.60]
      },
      {
        "name": "Credit Differential / Net Cost Shift ($)",
        "data": [31.80, 88.16, 17.04, 137.00]
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

- **Execute Tariff Flag Verification**: Verify that the meter's active tariff schedule (`rate_schedule_code`) in the CIS matches the interconnection agreement vintage (e.g., NEM legacy grandfathering vs. Avoided-Cost Net Billing Tariff).
- **Automate Truing & True-Up Auditing**: Route monthly avoided-cost accruals into the submetering ledger and schedule an automated annual true-up validation to prevent unaccounted revenue leakage or uncredited rollover balances.
- **Implement Customer Billing Presentment Advisory**: Update customer-facing bill statements to display explicit itemization of gross imports, gross exports, and applied Avoided-Cost Calculator (ACC) hourly values to minimize customer inquiry spikes.
- **Deploy Battery Storage Optimization Signals**: Advise energy service representatives to educate affected customers on shifting battery dispatch to on-peak export hours (where avoided-cost credit is highest at $0.115/kWh vs. $0.048/kWh at midday).

---

### 5. HITL / Tier 2 Formats

```json
[TIER 2 ACTION REQUIRED]
{
  "action_type": "BILLING_CREDIT_ADJUSTMENT_POSTING",
  "customer_id": "CUST-NEM-882194",
  "billing_account_id": "ACC-77402-B",
  "reconciliation_type": "NEM_TO_AVOIDED_COST_TRUEUP",
  "credit_adjustment_amount_usd": -137.00,
  "original_nem_credit_usd": 173.60,
  "revised_avoided_cost_credit_usd": 36.60,
  "impacted_cycle": "2024-M05",
  "justification": "Reconciliation and re-rating of solar export intervals from grandfathered retail NEM to Avoided-Cost Tariff per PUC regulatory mandate.",
  "approver_role": "Billing_and_Invoicing_Supervisor"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Publish net surplus generation compensation credits to 14,200 NEM 2.0 customer billing registers."

**Agent Response:**
### Executive Summary
**A batch execution request has been prepared to credit 14,200 Net Energy Metering (NEM 2.0) accounts with their calculated Net Surplus Generation Compensation (NSGC). Validation and billing engine reconciliation show a total credit disbursement of $2,487,000.00 against 24.87 GWh of annualized excess generation. Because mass ledger mutation and customer financial postings constitute a Tier 2 operation, ledger publication is currently staged pending Human-in-the-Loop (HITL) authorization.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Target Billing Registers** | 14,200 accounts | 14,200 accounts | 0.00% | Normal |
| **Aggregate Net Surplus Energy** | 24,870,000 kWh | 24,150,000 kWh | +2.98% | Normal |
| **Weighted Average NSCR** | $0.1000 / kWh | $0.0985 / kWh | +1.52% | Normal |
| **Total Credit Valuation** | $2,487,000.00 | $2,378,775.00 | +4.55% | Normal |
| **Interval Telemetry VEE Rate** | 99.98% | ≥ 99.95% | +0.03% | Normal |
| **Unreconciled / Billing Exception Accounts** | 0 accounts | 0 accounts | 0.00% | Normal |

---

### Visualization Triggers
**Recommended Chart**: Clustered Bar Chart — *NEM 2.0 Net Surplus Compensation by Customer Class & Volume*

```json
{
  "chart_type": "bar",
  "title": "NEM 2.0 Net Surplus Generation Credit Distribution",
  "data": [
    {
      "customer_class": "Residential (Res-NEM2)",
      "account_count": 11800,
      "surplus_mwh": 14160.0,
      "total_credit_usd": 1416000.00
    },
    {
      "customer_class": "Commercial (C&I-NEM2)",
      "account_count": 2100,
      "surplus_mwh": 8820.0,
      "total_credit_usd": 882000.00
    },
    {
      "customer_class": "Agricultural (AG-NEM2)",
      "account_count": 300,
      "surplus_mwh": 1890.0,
      "total_credit_usd": 189000.00
    }
  ]
}
```

---

### Actionable Recommendations
- **Pre-Post Verification**: Review the 14,200 staged billing records against the financial settlement master balance to ensure general ledger parity.
- **HITL Authorization**: Execute the formal approval trigger below to commit the credits to the CIS/Billing registers and trigger downstream invoice generation.
- **True-Up Statement Dispatch**: Schedule post-credit statement generation for delivery on the regular billing cycle calendar.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_id": "ACT-NEM2-NSGC-2024-B142",
  "operation_type": "MASS_BILLING_LEDGER_POSTING",
  "domain": "Billing And Invoicing",
  "subsystem": "net_metering_export_credit_processor",
  "target_population": 14200,
  "rate_tariff": "NEM 2.0",
  "total_financial_commitment_usd": 2487000.00,
  "effective_billing_cycle": "Current True-Up Settlement",
  "requires_approval": true,
  "approval_status": "AWAITING_HUMAN_CONFIRMATION",
  "instructions": "Confirm approval to post $2,487,000.00 in Net Surplus Compensation credits to 14,200 customer accounts."
}
```
