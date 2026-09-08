# ⚡ Community Solar Subscription Allocator

![Domain](https://img.shields.io/badge/Domain-billing%20and%20invoicing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of community solar subscription allocator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Community Solar Subscription Allocator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank community solar subscription allocator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_billing_and_invoicing.community_solar_subscription_allocator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did the 5 MW SunRidge Community Solar garden generate enough surplus kWh to cover all 1,200 residential subscription credits this month?"

**Agent Response:**
### Executive Summary
**The 5 MW SunRidge Community Solar facility generated 745,000 kWh this billing cycle, successfully exceeding the aggregate subscription requirement of 600,000 kWh needed to cover all 1,200 residential subscribers.** **A net surplus of 145,000 kWh (24.17% above total subscriber demand) was achieved, enabling 100% on-bill credit allocation with zero curtailment or unfulfilled subscriber shares.** **Excess generation will be routed to the reserve banking pool in accordance with PUC community solar tariff provisions.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Facility Generation** | 745,000 kWh | 680,000 kWh (P50 Forecast) | +9.56% | Normal |
| **Active Residential Subscribers** | 1,200 accounts | 1,200 accounts | 0.00% | Normal |
| **Aggregate Subscriber Credit Demand** | 600,000 kWh | 600,000 kWh | 0.00% | Normal |
| **Average Allocation per Subscriber** | 500 kWh/subscriber | 500 kWh/subscriber | 0.00% | Normal |
| **Net Surplus / Banking Credit** | 145,000 kWh | 80,000 kWh | +81.25% | Normal |
| **Subscription Coverage Ratio** | 124.17% | 100.00% | +24.17% | Normal |

---

### Visualization Triggers
- **Recommended Chart**: Categorical Bar Chart illustrating Total Generation vs. Subscribed Demand Allocation vs. Net Surplus.

```json
{
  "chart_type": "bar",
  "title": "SunRidge 5 MW Community Solar Monthly Generation & Credit Distribution",
  "data": {
    "labels": ["Subscribed Demand Allocation", "Surplus / Reserve Banking", "Total Facility Generation"],
    "datasets": [
      {
        "label": "Energy (kWh)",
        "data": [600000, 145000, 745000],
        "backgroundColor": ["#2E7D32", "#0288D1", "#F57C00"]
      }
    ]
  },
  "options": {
    "responsive": true,
    "scales": {
      "y": {
        "title": { "display": true, "text": "Kilowatt-Hours (kWh)" },
        "beginAtZero": true
      }
    }
  }
}
```

---

### Actionable Recommendations
- **Execute Bill Credit Distribution**: Apply the allocated 500 kWh average credit equivalent directly to the 1,200 active residential billing profiles for the current cycle.
- **Credit Banking Allocation**: Transfer the 145,000 kWh net generation surplus into the facility's rolling subscriber credit bank to hedge against lower winter irradiance cycles.
- **Subscriber Portfolio Review**: Evaluate waitlist onboarding capacity, as consistent surplus headroom indicates potential to support an additional 200–250 residential subscriptions under standard allocation rules.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "BILLING_CREDIT_SETTLEMENT_AND_BANKING",
  "facility_id": "SOLAR-SUNRIDGE-5MW",
  "billing_cycle": "CURRENT_MONTH",
  "total_subscribers": 1200,
  "allocated_kwh": 600000,
  "banked_surplus_kwh": 145000,
  "requires_hitl_approval": true,
  "financial_impact_level": "STANDARD_BATCH_CYCLE",
  "compliance_rule": "PUC-RULE-COMMUNITY-SOLAR-TARIFF"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Reconcile customer monthly kilowatt-hour allocations against metered solar production and subscriber turnover rates."

**Agent Response:**
### Executive Summary
**Reconciliation for the current billing cycle confirms a total metered solar generation of 1,340,000 kWh against 1,285,000 kWh allocated across active subscriber accounts, yielding a 95.9% allocation efficiency.** **A monthly subscriber churn rate of 4.2% created a temporary unallocated variance of 55,000 kWh (4.1%), which has been swept into the program virtual generation bank in accordance with state tariff settlement rules.** **All submetered credits have been balanced with zero unassigned monetary leakage, though waitlist backfill throughput must be accelerated to maintain the target 98.0% subscription capacity.**

---

### Data Presentation: Monthly Reconciliation & Churn Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Metered Solar Production** | 1,340,000 kWh | 1,310,000 kWh | +2.29% | Normal |
| **Subscribed Allocation Volume** | 1,285,000 kWh | 1,283,800 kWh | +0.09% | Normal |
| **Unallocated / Banked Generation** | 55,000 kWh | 26,200 kWh | +109.92% | Warning |
| **Active Subscriber Count** | 1,820 accounts | 1,900 accounts | -4.21% | Warning |
| **Monthly Subscriber Churn Rate** | 4.20% | ≤ 2.00% | +110.00% | Warning |
| **Waitlist Auto-Onboarding Rate** | 35 accounts/mo | 75 accounts/mo | -53.33% | Warning |
| **Net Metering Credit True-Up Variance** | $0.00 | $0.00 | 0.00% | Normal |
| **Program Allocation Efficiency** | 95.90% | ≥ 98.00% | -2.14% | Warning |

---

### Visualization Configuration

A multi-series chart tracks the five-month trend of metered utility production against executed subscriber bill credits and unallocated reserve banking.

```json
{
  "chart_type": "bar",
  "title": "Monthly Community Solar Generation vs Allocation & Bank Balance (kWh)",
  "categories": ["Nov 2023", "Dec 2023", "Jan 2024", "Feb 2024", "Mar 2024"],
  "series": [
    {
      "name": "Metered Solar Production (kWh)",
      "data": [1120000, 980000, 1050000, 1180000, 1340000]
    },
    {
      "name": "Total Allocated kWh",
      "data": [1085000, 965000, 1010000, 1140000, 1285000]
    },
    {
      "name": "Unallocated / Banked Reserve (kWh)",
      "data": [35000, 15000, 40000, 40000, 55000]
    }
  ],
  "yAxis": {
    "title": "Energy (kWh)"
  }
}
```

---

### Actionable Recommendations

- **Automate Waitlist Queue Ingestion**: Trigger immediate programmatic enrollment of 80 pre-qualified residential waitlist subscribers to re-absorb the 55,000 kWh unallocated surplus before the next billing cutoff.
- **Dynamic Capacity Re-sizing**: Recalibrate subscription share sizing for anchor commercial/institutional subscribers to temporarily absorb fractional residential turnover without violating PUC caps (e.g., max 40% single-entity allocation limit).
- **True-Up Reserve Audit**: Reconcile accumulated banked generation (current balance: 185,000 kWh) against the annual forfeiture/cash-out deadline under Rule 21 / Net Energy Metering (NEM) tariff schedules.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "BATCH_BILLING_CREDIT_SETTLEMENT_AND_WAITLIST_ALLOCATION",
  "domain": "Billing And Invoicing",
  "target_program_id": "COMM_SOLAR_ZONE_4A",
  "execution_payload": {
    "billing_cycle": "2024-03",
    "total_credit_disbursement_kwh": 1285000,
    "unallocated_banked_kwh": 55000,
    "waitlist_batch_activation_count": 80,
    "financial_settlement_value_usd": 147775.00
  },
  "impact_scope": "1,820 active subscriber utility accounts + 80 onboarding accounts",
  "compliance_check": "PUC Community Solar Shared Renewables Tariff & FERC 888",
  "status": "PENDING_HUMAN_SUPERVISOR_APPROVAL"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Execute monthly subscriber credit balance distribution to the CIS billing system for the upcoming billing cycle."

**Agent Response:**
### Executive Summary
**The monthly community solar subscription credit calculation has been successfully staged and reconciled for the upcoming billing cycle across all active solar farm tranches. Total generated credits amount to $557,900 across 2,922 active subscriber accounts with an average capacity allocation factor of 98.4%. Final batch ingestion into the Customer Information System (CIS) billing ledger represents a Tier 2 financial transaction and requires explicit Human-In-The-Loop (HITL) authorization prior to ledger commit.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Distributed Generation** | 4,649,166 kWh | 4,500,000 kWh | +3.31% | **Normal** |
| **Gross Financial Credit Value** | $557,900.00 | $540,000.00 | +3.31% | **Normal** |
| **Active Subscriber Count** | 2,922 accounts | 2,900 accounts | +0.76% | **Normal** |
| **Farm Nameplate Utilization** | 98.4% | 95.0% | +3.58% | **Normal** |
| **LMI Carve-Out Credit Allocation** | $89,400.00 (16.0%) | $83,685.00 (15.0%) | +6.83% | **Normal** |
| **Unallocated Generation / Variance** | 0.42% | < 1.00% | -58.00% | **Normal** |

---

### Visualization Triggers
- **Recommended Visualization**: Stacked / Grouped Bar Chart comparing total credit value ($ USD) and subscriber count across consumer classes (Residential Standard, Low-to-Moderate Income, Small Commercial, and Municipal/Anchor Tenants).

```json
{
  "chart_type": "bar",
  "title": "Community Solar Credit Distribution by Rate Class",
  "data": {
    "categories": ["Residential Standard", "Low-to-Moderate Income (LMI)", "Small Commercial", "Municipal/Anchor Tenant"],
    "series": [
      {
        "name": "Allocated Credits ($ USD)",
        "values": [142500, 89400, 115200, 210800]
      },
      {
        "name": "Subscriber Count",
        "values": [1850, 920, 140, 12]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Audit Anchor Subscriptions**: Review municipal anchor off-taker limits against the 40% statutory cap under state public utility commission (PUC) community solar rules.
- **Verify Submeter Generation Readings**: Ensure true-up delta readings between the solar facility revenue meter and utility distribution interconnect match within the ±0.2% tolerance.
- **Authorize CIS Batch Pipeline**: Approve the Tier 2 credit distribution payload below to execute the automated batch credit transfer into CIS production accounts.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CIS_BILLING_CREDIT_POSTING",
  "tier_level": 2,
  "description": "Execute mass financial posting of solar credits to CIS subscriber accounts for the active billing cycle.",
  "payload_details": {
    "target_system": "CIS_BILLING_ENGINE",
    "billing_cycle_id": "CYCLE_2025_M04",
    "total_accounts_impacted": 2922,
    "total_credit_amount_usd": 557900.00,
    "rate_schedule_codes": ["CS-RES-01", "CS-LMI-02", "CS-COM-01", "CS-ANC-01"],
    "idempotency_key": "CS-ALLOC-202504-7F89A",
    "execution_mode": "SYNCHRONOUS_BATCH"
  },
  "compliance_verification": {
    "pu_commission_rule_check": "PASSED",
    "lmi_minimum_threshold_met": true,
    "rate_schedule_cross_validation": "PASSED"
  },
  "requires_approval_from": ["BILLING_OPERATIONS_LEAD", "REVENUE_RECONCILIATION_OFFICER"]
}
```
