# ⚡ Dynamic Real Time Pricing Biller

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of dynamic real time pricing biller is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Dynamic Real Time Pricing Biller Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank dynamic real time pricing biller events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.dynamic_real_time_pricing_biller_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How do five-minute wholesale LMP spot prices map to large industrial customer bills for yesterday's afternoon price spike?"

**Agent Response:**
### Executive Summary
**Five-minute wholesale Locational Marginal Pricing (LMP) spot prices are mapped directly to large industrial accounts through interval meter telemetry adjusted for nodal marginal loss factors (MLF), ancillary service allocations, and capacity adders.** **During yesterday’s peak afternoon spike (14:30–16:30), wholesale nodal prices surged from \$42.50/MWh to a peak of \$2,100.00/MWh, driving the fully bundled dynamic Real-Time Pricing (RTP) rate to \$2,241.50/MWh.** **Industrial customers with automated demand response curtailed load by 54.6% during the top pricing intervals, successfully avoiding over \$142,800 in volumetric energy charges.**

---

### LMP-to-RTP Billing Transformation Architecture

To settle large industrial accounts on 5-minute dynamic pricing, the billing engine executes a multi-stage interval calculation:

1. **Telemetry & VEE Alignment**: 
   $$\text{Interval Energy } (E_t \text{ in MWh}) = \frac{\text{AMI Pulse/kW Accumulator}_t}{12}$$
   *Raw 5-minute interval kW telemetry passes through Validation, Estimation, and Editing (VEE) prior to financial settlement.*

2. **Wholesale-to-Retail Bundled Rate Formulation**:
   $$\text{RTP Rate}_t (\$/\text{MWh}) = \Big( \text{LMP}_{\text{node}, t} \times (1 + \text{MLF}_{\text{feeder}}) \Big) + \text{Ancillary Adder}_t + \text{Capacity Adder}_t + \text{T\&D Delivery} + \text{Retail Admin Margin}$$
   * *Nodal LMP*: Five-minute Real-Time Settlement Point Price ($/MWh).
   * *Marginal Loss Factor (MLF)*: Dynamic or static expansion factor compensating for transmission/distribution losses (typically $1.035 - 1.065$).
   * *Ancillary & Reserve Adders*: Operating reserves (Spinning/Non-spinning) and Frequency Regulation charges allocated per interval.
   * *Delivery & Administrative Adders*: Fixed per-MWh distribution/transmission wheeling fees.

3. **Interval Financial Settlement**:
   $$\text{Total Dynamic Energy Charge} = \sum_{t=1}^{N} \Big( E_t \times \text{RTP Rate}_t \Big)$$

---

### Data Presentation: Afternoon Spike Settlement Metrics (14:00 – 17:00 Event Window)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Wholesale Peak LMP (5-min)** | \$2,100.00 / MWh | \$45.00 / MWh | +4,566.7% | **Critical** |
| **Billed Dynamic RTP Rate (Peak)** | \$2,241.50 / MWh | \$65.00 / MWh | +3,348.5% | **Critical** |
| **Average Event LMP (14:00–17:00)** | \$583.76 / MWh | \$42.00 / MWh | +1,289.9% | **Critical** |
| **Industrial Class Load Response** | 8.40 MW (Min Load) | 18.50 MW (Baseline) | -54.6% | **Normal** |
| **VEE Interval Success Rate** | 99.94% | 99.90% | +0.04% | **Normal** |
| **Total Event Revenue Billed** | \$186,430.50 | \$32,250.00 | +478.1% | **Warning** |
| **Unhedged Value-at-Risk (VaR 95%)** | \$18,200.00 | < \$25,000.00 | -27.2% | **Normal** |

---

### Visualization Triggers

**Recommended Visualization:** *Dual-Axis Time-Series Line Chart* plotting 5-minute Wholesale LMP vs. Fully Loaded RTP Customer Rate vs. Aggregate Industrial Customer Load Profile (MW).

```json
{
  "chart_type": "line",
  "title": "5-Minute Wholesale LMP vs. Realized RTP Billing Rate & Load Curtailment",
  "intervals": ["14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45", "16:00", "16:15", "16:30", "16:45", "17:00"],
  "series": [
    {
      "name": "Wholesale LMP ($/MWh)",
      "data": [42.50, 55.10, 120.40, 480.00, 1250.00, 2100.00, 1850.00, 920.00, 340.00, 110.00, 65.00, 48.00, 45.00],
      "axis": "y1"
    },
    {
      "name": "Customer Billed RTP Rate ($/MWh)",
      "data": [61.25, 74.60, 144.02, 525.60, 1341.50, 2241.50, 1976.00, 991.20, 377.00, 132.80, 85.20, 67.10, 63.90],
      "axis": "y1"
    },
    {
      "name": "Industrial Load Demand (MW)",
      "data": [18.5, 18.2, 17.9, 15.1, 11.2, 8.4, 9.1, 12.0, 15.8, 17.4, 18.1, 18.4, 18.5],
      "axis": "y2"
    }
  ]
}
```

---

### Actionable Recommendations

1. **Execute Shadow Settlement Audit**: Reconcile interval billing determinants against ISO/RTO final real-time market settlement statements (Day + 2 / Day + 5) to capture any ex-post market price corrections.
2. **Review Demand Response Performance**: Quantify industrial baseline compliance to calculate applicable capacity credits or demand-side management (DSM) performance rebates.
3. **Flag Interval Meter Telemetry Outliers**: Run specialized VEE estimation routines on the 0.06% unvalidated intervals before preliminary bill ledger finalization.
4. **Issue Financial Advisory Summaries**: Provide participating industrial accounts with their localized cost-avoidance statements showing realized bill savings from automated curtailment.

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate the bill savings achieved by metallurgical facilities that curtailed load when spot prices exceeded $300/MWh."

**Agent Response:**
### Executive Summary
**During critical wholesale pricing events where real-time spot prices exceeded $300/MWh, participating metallurgical and heavy smelting facilities achieved a cumulative bill savings of $2,291,500 by actively curtailing 4,812.50 MWh of demand across 38 peak settlement intervals.** **Aggregate load across the five primary metallurgical nodes dropped by 58.42% relative to their unconstrained baseline profiles, mitigating severe peak exposure and grid congestion in high-priced zones.** **Interval settlement validation confirms full meter-to-cash reconciliation compliance under dynamic RTP tariff schedules with zero critical revenue leakage or VEE anomalies.**

---

### Quantitative Evaluation & Performance Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Realized Bill Savings** | $2,291,500 | $0.00 (Uncurtailed Baseline) | +100.00% | Normal |
| **Total Energy Consumed during >$300/MWh** | 3,425.20 MWh | 8,237.70 MWh (Baseline Load) | -58.42% | Normal |
| **Total Demand Curtailed** | 4,812.50 MWh | 0.00 MWh | +100.00% | Normal |
| **Weighted Average Spot Settlement Price** | $476.15/MWh | $300.00/MWh (Threshold) | +58.72% | Warning |
| **Total Actual Energy Charges Incurred** | $1,630,500 | $3,922,000 (Avoided Baseline Cost) | -58.43% | Normal |
| **VEE Interval Validation Success Rate** | 100.00% | 99.50% | +0.50% | Normal |
| **Peak Demand Excursion / Non-Compliance** | 0.00 MWh | < 50.00 MWh | -100.00% | Normal |

---

### Facility-by-Facility Dynamic RTP Curtailment Breakdown

| Customer Account / Facility | Grid Zone ID | Peak Intervals (> $300/MWh) | Baseline Demand (MWh) | Actual Metered (MWh) | Curtailed Volume (MWh) | Effective Billed Cost ($) | Avoided Cost / Savings ($) | Savings (%) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Alloy Smelter Alpha** | `ZONE-NORTH-EHV` | 38 | 2,698.00 | 1,012.00 | 1,686.00 | $482,100 | $803,300 | 62.50% |
| **Arc Furnace Metro-East** | `ZONE-EAST-138KV` | 38 | 2,024.50 | 830.00 | 1,194.50 | $395,300 | $568,900 | 59.00% |
| **Heavy Forging South** | `ZONE-SOUTH-230KV` | 38 | 1,558.20 | 654.50 | 903.70 | $311,700 | $430,400 | 57.99% |
| **Precision Casting West** | `ZONE-WEST-115KV` | 38 | 1,088.00 | 511.20 | 576.80 | $243,600 | $274,700 | 52.99% |
| **Industrial Refining Central**| `ZONE-CENTRAL-230KV`| 38 | 869.00 | 417.50 | 451.50 | $197,800 | $214,200 | 51.99% |
| **Total / Weighted Avg** | **Portfolio-Wide** | **38** | **8,237.70** | **3,425.20** | **4,812.50** | **$1,630,500** | **$2,291,500** | **58.42%** |

---

### Visualization Configuration

A grouped comparative bar chart renders the financial delta between uncurtailed baseline obligations, actual billed costs, and net realized savings across each metallurgical facility.

```json
{
  "chart_type": "bar",
  "title": "Metallurgical Facilities: Real-Time Pricing (RTP) Curtailment Bill Savings (> $300/MWh Intervals)",
  "xAxis": {
    "type": "category",
    "data": [
      "Alloy Smelter Alpha",
      "Arc Furnace Metro-East",
      "Heavy Forging South",
      "Precision Casting West",
      "Industrial Refining Central"
    ]
  },
  "yAxis": {
    "type": "value",
    "name": "USD ($)"
  },
  "series": [
    {
      "name": "Baseline Uncurtailed Cost ($)",
      "type": "bar",
      "data": [1285400, 964200, 742100, 518300, 412000]
    },
    {
      "name": "Actual Realized Billed Cost ($)",
      "type": "bar",
      "data": [482100, 395300, 311700, 243600, 197800]
    },
    {
      "name": "Net Avoided Cost / Savings ($)",
      "type": "bar",
      "data": [803300, 568900, 430400, 274700, 214200]
    }
  ]
}
```

---

### Actionable Recommendations

- **Post-Settlement Billing Integration**: Finalize 5-minute/15-minute interval financial reconciliation records in the customer billing engine for the current billing cycle and apply the avoided spot rate credits.
- **Automated Price Signal Calibration**: Review telemetry latency on automated SCADA load reduction triggers for facilities achieving < 55% curtailment (Precision Casting West & Industrial Refining Central) to maximize response during sudden price spikes.
- **Demand Response & Capacity Co-Optimization**: Assess whether participating metallurgical accounts are eligible for supplementary ISO/RTO ancillary services or emergency demand response capacity payments during overlapping high-heat rate contingency intervals.
- **Baseline Model Recalibration**: Update rolling 10-of-10 baseline load calculations to ensure customer baseline load (CBL) accounts for post-curtailment rebound effects without distorting subsequent off-peak settlement billing.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate and dispatch dynamic interval billing statements for all Schedule RTP high-voltage customers."

**Agent Response:**
### 1. Executive Summary
**Dynamic interval settlement calculations have been compiled for all 42 primary high-voltage accounts enrolled under Schedule RTP (Real-Time Pricing) across the current billing cycle.** **Interval-level telemetry reconciliation confirms a 99.88% VEE (Validation, Estimation, and Editing) data completion rate with an aggregate dynamic energy settlement value of $14,892,340.00.** **Because statement dispatch triggers binding financial liabilities and receivables issuance, statement delivery has been staged and placed under Human-In-The-Loop (HITL) gatekeeper hold pending financial controller sign-off.**

---

### 2. Data Presentation (Markdown Tables)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Aggregated Schedule RTP-HV Energy** | 182,450.60 MWh | 178,000.00 MWh | +2.50% | Normal |
| **Volume-Weighted Average RTP Price** | $81.62 / MWh | $76.40 / MWh | +6.83% | Normal |
| **Gross Interval Billing Settlement Amount** | $14,892,340.00 | $13,599,200.00 | +9.51% | Normal |
| **Interval VEE Completion Rate** | 99.88% | 99.50% | +0.38% | Normal |
| **Coincident Peak Demand Charges (Transmission HV)** | $3,120,400.00 | $3,100,000.00 | +0.66% | Normal |
| **Unbilled / Revenue Leakage Exposure** | $0.00 (0 MWh) | < $5,000.00 | -100.00% | Normal |
| **Value at Risk (VaR - 95% Confidence Interval)** | $142,500.00 | $200,000.00 | -28.75% | Normal |

---

### 3. Visualization Triggers

```json
{
  "chart_type": "line",
  "title": "Aggregated Schedule RTP-HV Interval Load & Weighted Real-Time Price Profile",
  "data": {
    "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00"],
    "datasets": [
      {
        "name": "Aggregated HV Load (MW)",
        "data": [412.5, 385.2, 598.0, 742.6, 810.4, 620.1],
        "unit": "MW"
      },
      {
        "name": "Real-Time Locational Price ($/MWh)",
        "data": [32.40, 28.15, 64.80, 112.50, 145.20, 58.90],
        "unit": "$/MWh"
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

- **Authorize Batch Dispatch**: Review the calculated interval billing totals and authorize invoice dispatch for the 42 Schedule RTP-HV customer accounts via EDI 810 / secure customer invoicing portal.
- **Archive VEE Audit Logs**: Securely log the 5-minute interval locational marginal price (LMP) mapping and revenue meter settlement hashes into the regulatory compliance archive for FERC/PUC audit readiness.
- **Notify Key Account Managers**: Provide high-load industrial accounts that experienced peak real-time price exposure (> $140/MWh) with interval load-shifting advisories for subsequent cycles.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FINANCIAL_INVOICE_DISPATCH",
  "target_schedule": "SCHEDULE_RTP_HV",
  "customer_count": 42,
  "service_class": "High-Voltage Transmission / Primary Substation (>69 kV)",
  "total_settlement_amount_usd": 14892340.00,
  "billing_cycle_period": "2025-M03-C1",
  "vee_verification_status": "VERIFIED_PASSED",
  "delivery_channel": "EDI_810_AND_ENTERPRISE_PORTAL",
  "risk_assessment": "Irreversible financial posting and direct enterprise receivables issuance.",
  "hitl_approval_required": true
}
```
*Please provide explicit confirmation to execute the financial statement dispatch payload.*
