# ⚡ Wholesale Vendor Payment Reconciler

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of wholesale vendor payment reconciler is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Wholesale Vendor Payment Reconciler Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank wholesale vendor payment reconciler events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.wholesale_vendor_payment_reconciler_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Do our monthly transmission wheeling fee invoices from Regional Grid Operator match internal SCADA interchange logs?"

**Agent Response:**
### Executive Summary
**A systematic reconciliation of the past six billing cycles reveals a significant billing mismatch between the Regional Grid Operator (RGO) monthly transmission wheeling fee invoices and internal SCADA tie-line interchange logs.** **While shoulder months remain within the standard ±0.5% telemetry tolerance band, winter peak months (December and January) exhibit unexplained positive billing variances of +3.01% and +3.74% (totaling 32,600 MWh / $348,820 over-invoiced).** **The discrepancy is traced to unadjusted tie-line meter drift at Substation Interconnection East and an erroneous loss multiplier applied during RGO peak settlement runs.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Invoiced Wheeling Volume (6-Mo Sum)** | 2,777,100 MWh | 2,739,200 MWh (SCADA) | +1.38% | **Warning** |
| **Peak Month Variance (Jan 2024)** | 510,400 MWh | 492,000 MWh (SCADA) | +3.74% | **Critical** |
| **High Winter Variance (Dec 2023)** | 485,200 MWh | 471,000 MWh (SCADA) | +3.01% | **Critical** |
| **Shoulder Month Avg Variance (Oct–Nov, Feb–Mar)** | +0.31% | < ±0.50% (FERC/NERC Band) | +0.31% | **Normal** |
| **Net Financial Discrepancy (Over-Billed)** | $387,420 | $0.00 (Zero Tolerance) | N/A | **Critical** |
| **Tie-Line VEE Completeness Rate** | 99.94% | 99.90% Target | +0.04% | **Normal** |

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Monthly Transmission Wheeling: RGO Invoiced vs. SCADA Interchange (MWh)",
  "categories": ["Oct 2023", "Nov 2023", "Dec 2023", "Jan 2024", "Feb 2024", "Mar 2024"],
  "series": [
    {
      "name": "RGO Invoiced (MWh)",
      "data": [412500, 428000, 485200, 510400, 462100, 478900]
    },
    {
      "name": "SCADA Logged (MWh)",
      "data": [411900, 427400, 471000, 492000, 459800, 477100]
    },
    {
      "name": "Variance (MWh)",
      "data": [600, 600, 14200, 18400, 2300, 1800]
    }
  ]
}
```

---

### Actionable Recommendations

- **Formal Billing Dispute Initiation**: Issue a formal FERC Open Access Transmission Tariff (OATT) settlement dispute for the December 2023 and January 2024 billing cycles seeking a credit adjustment of **$348,820**.
- **Tie-Line Meter Calibration Review**: Dispatch substation protection and metering technicians to verify primary/secondary revenue meters at Tie-Line Interconnection East (Node TL-E301).
- **RGO Loss Factor Reconciliation**: Request RGO's settlement engineering team provide hourly marginal transmission loss coefficients and interval settlement files for peak flow hours.
- **Automate Monthly Ingestion**: Configure automated daily tie-line settlement delta alerts to flag any variance exceeding ±0.5% prior to monthly invoice receipt.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "operation_type": "WHOLESALE_DISPUTE_AND_FINANCIAL_ADJUSTMENT",
  "vendor_name": "Regional Grid Operator (RGO)",
  "settlement_period": "2023-12-01 to 2024-01-31",
  "disputed_amount_usd": 348820.00,
  "disputed_volume_mwh": 32600.00,
  "dispute_grounds": "OATT Schedule 7 / 8 Over-billing vs SCADA Revenue Tie-Line Meters",
  "impact": "Initiates formal commercial dispute, places hold on disputed balance, triggers joint engineering meter audit",
  "requires_hitl_approval": true,
  "authorized_approver_role": "Director of Wholesale Settlements & Energy Accounting"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Reconcile disputed line-item billing variances on fuel transport contracts with pipeline operators for Q3."

**Agent Response:**
### Executive Summary
**Q3 wholesale fuel transport billing reconciliation identified a net overcharge variance of $511,900 across five major interstate pipeline operators, driven predominantly by unauthorized fuel shrinkage retention rate adjustments and misapplied operational balancing agreement (OBA) cash-out penalty tiers. Contractual baseline audits established valid payable charges of $15,710,000 against gross vendor billings of $16,221,900, resulting in an aggregate 3.26% variance. A formal dispute withholding protocol is initiated pursuant to FERC Part 284 and standard NAESB contract dispute provisions.**

---

### Data Presentation: High-Level Q3 Fuel Transport Reconciliation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Invoiced Amount** | $16,221,900 | $15,710,000 | +3.26% | **Warning** |
| **Disputed Variance Total** | $511,900 | $0.00 | +100.00% | **Critical** |
| **Fuel Retainage / Shrinkage Charges** | $1,845,200 | $1,620,000 | +13.90% | **Critical** |
| **Firm Reservation (Demand) Fees** | $11,250,000 | $11,250,000 | 0.00% | **Normal** |
| **Volumetric Commodity / Transport Surcharges** | $2,185,500 | $2,125,000 | +2.85% | **Warning** |
| **OBA Imbalance Cash-Out Penalties** | $941,200 | $715,000 | +31.64% | **Critical** |
| **VEE Telemetry / Flow Meter Alignment Rate** | 97.10% | 99.50% | -2.41% | **Warning** |

---

### Granular Line-Item Variance Breakdown by Pipeline Operator

| Pipeline Operator | Contract ID | Invoiced Amount ($) | Verified Baseline ($) | Net Disputed ($) | Primary Dispute Root Cause |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Transcontinental Gas Pipe Line (Transco)** | FT-TR-8841 | $4,850,400 | $4,620,000 | **+$230,400** | Applied off-peak fuel retention rate (2.1%) to peak firm deliveries instead of tariff-indexed rate (1.45%); meter station flow discrepancy at Zone 4 receipt point. |
| **Kinder Morgan Texas Pipeline (KMTP)** | IT-KM-2093 | $3,920,800 | $3,810,000 | **+$110,800** | Erroneous Tier-3 cash-out multiplier applied to daily cumulative imbalance despite scheduled nomination matches confirmed via Electronic Data Interchange (EDI 214). |
| **Tennessee Gas Pipeline (TGP)** | FT-TG-5120 | $3,110,500 | $2,985,000 | **+$125,500** | Unwarranted Electric Power Cost Recovery (EPCR) and ACA surcharges added to exempt firm storage withdrawal transport. |
| **Enbridge Texas Eastern (TETCO)** | FT-EN-3309 | $2,450,200 | $2,445,000 | **+$5,200** | Minor rounding variance on ACA administrative rate (within allowable tolerance threshold). |
| **Columbia Gulf Transmission (CGT)** | FT-CG-7721 | $1,890,000 | $1,850,000 | **+$40,000** | Failure to credit scheduled overrun volume credits during August curtailment declaration event. |

---

### Visualization Triggers

```json
{
  "chart_type": "bar",
  "data_json": {
    "title": "Q3 Fuel Transport Invoiced vs Contracted Variances by Pipeline Operator",
    "labels": [
      "Transcontinental Gas Pipe Line",
      "Kinder Morgan Texas Pipeline",
      "Tennessee Gas Pipeline",
      "Enbridge Texas Eastern",
      "Columbia Gulf Transmission"
    ],
    "datasets": [
      {
        "label": "Invoiced Amount ($k)",
        "data": [4850.4, 3920.8, 3110.5, 2450.2, 1890.0]
      },
      {
        "label": "Contract Baseline Amount ($k)",
        "data": [4620.0, 3810.0, 2985.0, 2445.0, 1850.0]
      },
      {
        "label": "Disputed Variance ($k)",
        "data": [230.4, 110.8, 125.5, 5.2, 40.0]
      }
    ]
  }
}
```

---

### Actionable Recommendations

1. **Escrow Disputed Balances**: Authorize immediate short-pay release of the undisputed baseline balance ($15,710,000) and withhold the disputed aggregate of $511,900 into the designated wholesale settlement escrow account.
2. **Issue Formal NAESB Dispute Notices**:
   - Transco: Demand recalculation of fuel retainage based on FERC Docket Tariff sheets and station SCADA flow telemetry.
   - KMTP: Submit EDI 214 nomination audit logs to void non-compliant Tier-3 imbalance cash-out multipliers.
   - TGP: Request revised billing excluding exempt firm storage transport surcharges.
   - CGT: Enforce contractual curtailment overrun credits for August generation dispatch.
3. **Internal SCADA & EBB Alignment**: Re-synchronize electronic bulletin board (EBB) pipeline flow telemetry with enterprise SCADA energy management data to eliminate meter telemetry drift prior to Q4 true-up.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "WHOLESALE_DISPUTE_SHORT_PAY_AUTHORIZATION",
  "approval_level": "Tier 2 - Treasury & Wholesale Settlements Lead Approval Required",
  "details": {
    "quarter": "Q3",
    "undisputed_payable_total_usd": 15710000.00,
    "withheld_disputed_total_usd": 511900.00,
    "counterparties": [
      {
        "operator": "Transcontinental Gas Pipe Line",
        "contract_id": "FT-TR-8841",
        "dispute_amount_usd": 230400.00,
        "action": "WITHHOLD_AND_ISSUE_DISPUTE_LETTER"
      },
      {
        "operator": "Kinder Morgan Texas Pipeline",
        "contract_id": "IT-KM-2093",
        "dispute_amount_usd": 110800.00,
        "action": "WITHHOLD_AND_ISSUE_DISPUTE_LETTER"
      },
      {
        "operator": "Tennessee Gas Pipeline",
        "contract_id": "FT-TG-5120",
        "dispute_amount_usd": 125500.00,
        "action": "WITHHOLD_AND_ISSUE_DISPUTE_LETTER"
      },
      {
        "operator": "Columbia Gulf Transmission",
        "contract_id": "FT-CG-7721",
        "dispute_amount_usd": 40000.00,
        "action": "WITHHOLD_AND_ISSUE_DISPUTE_LETTER"
      },
      {
        "operator": "Enbridge Texas Eastern",
        "contract_id": "FT-EN-3309",
        "dispute_amount_usd": 5200.00,
        "action": "APPROVE_FULL_PAYMENT_DE_MINIMIS"
      }
    ],
    "regulatory_framework": "FERC Part 284 / NAESB WGQ Standard Contract Terms",
    "timestamp_utc": "2023-10-24T12:00:00Z"
  }
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Authorize scheduled wire settlement for wholesale power supplier invoices matching contract settlement tolerance."

**Agent Response:**
### Executive Summary
**A comprehensive multi-counterparty wholesale settlement reconciliation has been completed for the current billing cycle, validating five major power supplier invoices against internal shadow settlement calculations. All five supplier settlement packages fall within the contractual variance tolerance threshold of $\pm 0.25\%$, with a total net variance of $+0.04\%$ ($\$25,000$ on $\$59.90\text{ M}$ gross invoiced). Per enterprise safety guardrails, scheduled wire authorization constitutes a Tier 2 financial operation requiring Human-in-the-Loop (HITL) approval prior to execution.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Invoiced Settlement Amount** | $\$59,900,000.00$ | $\$59,875,000.00$ | $+0.04\%$ | **Normal** |
| **Contract Tolerance Threshold** | $0.04\%$ | $\le \pm 0.25\%$ | $-84.00\%$ | **Normal** |
| **Matched Invoice Count** | $5$ of $5$ | $5$ ($100\%$) | $0.00\%$ | **Normal** |
| **Disputed / Unreconciled Line Items** | $0$ | $0$ | $0.00\%$ | **Normal** |
| **VEE Interval Data Integrity Rate** | $99.98\%$ | $\ge 99.50\%$ | $+0.48\%$ | **Normal** |

---

### Visualization

```json
{
  "chart_type": "bar",
  "title": "Wholesale Invoiced vs. Shadow Settlement by Counterparty ($M)",
  "categories": [
    "NextEra Energy",
    "Calpine Power",
    "Constellation",
    "Vistra Corp",
    "Invenergy Wind"
  ],
  "series": [
    {"name": "Invoiced ($M)", "data": [14.25, 9.80, 18.10, 11.45, 6.30]},
    {"name": "Shadow Settlement ($M)", "data": [14.23, 9.81, 18.08, 11.46, 6.29]}
  ]
}
```

---

### Actionable Recommendations

- **Review Counterparty Batch Details**: Verify that the five scheduled recipient accounts match the designated Fedwire/CHIPS routing instructions on file in the Treasury settlement register.
- **Enforce Single-Day Value Cutoff**: Ensure human sign-off is submitted prior to the 14:00 EST Federal Reserve wire cut-off to avoid late settlement interest accruals under FERC standard tariffs.
- **Archive Shadow Run Telemetry**: Commit interval settlement logs, ISO/RTO nodal price lookups, and bilateral contract indices to the audit-compliant immutable financial ledger.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FINANCIAL_WIRE_SETTLEMENT_AUTHORIZATION",
  "domain": "Billing And Invoicing",
  "subdomain": "Wholesale Vendor Payment Reconciliation",
  "status": "PENDING_HUMAN_APPROVAL",
  "execution_payload": {
    "settlement_cycle_id": "ST-2025-W12-004",
    "total_settlement_amount_usd": 59900000.00,
    "payment_channel": "Fedwire_Direct",
    "counterparties": [
      {"name": "NextEra Energy", "vendor_id": "VEND-NE-881", "authorized_amount": 14250000.00, "variance": "+0.14%"},
      {"name": "Calpine Power", "vendor_id": "VEND-CP-412", "authorized_amount": 9800000.00, "variance": "-0.10%"},
      {"name": "Constellation", "vendor_id": "VEND-CE-109", "authorized_amount": 18100000.00, "variance": "+0.11%"},
      {"name": "Vistra Corp", "vendor_id": "VEND-VC-774", "authorized_amount": 11450000.00, "variance": "-0.09%"},
      {"name": "Invenergy Wind", "vendor_id": "VEND-IW-305", "authorized_amount": 6300000.00, "variance": "+0.16%"}
    ],
    "tolerance_rule_verified": true,
    "max_allowed_tolerance_pct": 0.25,
    "actual_max_tolerance_pct": 0.16
  },
  "required_approver_role": "Treasury Operations Manager / Settlement Lead"
}
```
