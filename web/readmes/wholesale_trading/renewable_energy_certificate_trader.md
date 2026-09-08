# ⚡ Renewable Energy Certificate Trader

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of renewable energy certificate trader is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Renewable Energy Certificate Trader Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank renewable energy certificate trader events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.renewable_energy_certificate_trader_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What are current compliance Class I Renewable Energy Certificates (RECs) trading for in the voluntary and compliance markets?"

**Agent Response:**
### Executive Summary
**Compliance Class I Renewable Energy Certificates (RECs) are currently trading at significant premiums across major mandatory state Renewable Portfolio Standard (RPS) markets compared to the national voluntary market.** **In strict compliance regions such as PJM, NEPOOL, and CAISO, Class I/PCC-1 contracts trade in the range of $28.00/MWh to $48.00/MWh driven by statutory annual RPS percentage escalations and Alternative Compliance Payment (ACP) price caps.** **Conversely, National Voluntary Green-e certified RECs (predominantly ERCOT/SPP wind and solar) trade at an unconstrained baseline of approximately $2.50 to $3.50/MWh due to abundant resource supply and lack of statutory retirement mandates.**

---

### REC Market Pricing & Benchmark Data

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **NEPOOL Dual-Qualified Class I (V24)** | $41.25 / MWh | $40.00 / MWh (Q1 Trailing Avg) | +3.1% | Normal |
| **PJM Tier I Compliance (V24)** | $34.50 / MWh | $32.00 / MWh (Q1 Trailing Avg) | +7.8% | Warning |
| **CAISO PCC-1 (Bundled/Class 1 RPS)** | $48.00 / MWh | $45.00 / MWh (Target ACP Hedge) | +6.7% | Warning |
| **NYISO Tier 1 (V24 NYSERDA Equivalent)** | $28.75 / MWh | $27.50 / MWh (Reference Price) | +4.5% | Normal |
| **ERCOT In-State Compliance REC** | $4.10 / MWh | $4.50 / MWh (Target) | -8.9% | Normal |
| **National Voluntary (Green-e Wind/Solar)** | $2.85 / MWh | $3.10 / MWh (Trailing Year Avg) | -8.1% | Normal |
| **Compliance/Voluntary Basis Spread** | $31.65 / MWh | $28.90 / MWh (PJM-to-Voluntary) | +9.5% | Warning |

---

### Market Dynamics & Drivers

1. **Compliance Class I Markets (PJM, NEPOOL, NYISO, CAISO)**:
   - **Regulatory Tightening**: PJM Tier I (governed by New Jersey, Maryland, Pennsylvania, and DC RPS mandates) is trending higher due to accelerated interconnection queue bottlenecks limiting new commercial online dates (COD).
   - **ACP Ceilings**: NEPOOL Class I trades closely bounded by statutory Alternative Compliance Payments ($50.00/MWh cap in Massachusetts/Connecticut), acting as an upper price resistance.
   - **PCC Classifications**: California RPS enforces strict Portfolio Content Category (PCC) rules, where PCC-1 (in-state/real-time interconnected generation) trades at a stark premium over PCC-2 (firmed/shaped) and PCC-3 (unbundled).

2. **National Voluntary Markets**:
   - **Supply Saturation**: Overwhelming capacity expansion in ERCOT and SPP utility-scale wind/solar continues to suppress unbundled voluntary REC prices.
   - **Corporate Scope 2 Demand**: Corporate buyers adhering to GHG Protocol Scope 2 guidance seek geographic and hourly matched (24/7 CFE) certificates, creating emerging bifurcations between generic unbundled RECs and time-stamped localized attributes.

---

### Visualization Configuration

```json
{
  "chart_type": "bar",
  "title": "REC Compliance vs. Voluntary Benchmark Pricing ($/MWh)",
  "categories": [
    "NEPOOL Class I",
    "PJM Tier I",
    "CAISO PCC-1",
    "NYISO Tier 1",
    "ERCOT Compliance",
    "National Voluntary"
  ],
  "series": [
    {
      "name": "Current Spot Price ($/MWh)",
      "data": [41.25, 34.50, 48.00, 28.75, 4.10, 2.85]
    },
    {
      "name": "Statutory ACP Cap / Resistance ($/MWh)",
      "data": [50.00, 45.00, 50.00, 35.00, 10.00, null]
    }
  ]
}
```

---

### Actionable Recommendations

- **Cross-Market Arbitrage & Optimization**: Evaluate options to bank qualifying multi-market certified assets (e.g., dual-certified PJM/NEPOOL assets) into higher-margin NEPOOL Class I delivery periods before the compliance retirement deadline.
- **Exposure Hedging**: With PJM Tier I approaching historical resistance levels (+7.8% delta), initiate forward strip hedges for Compliance Years 2025–2026 to lock in generation revenue against potential interconnection queue clearance surges.
- **Voluntary Portfolio Purchasing**: Leverage subdued National Voluntary pricing ($2.85/MWh) to fulfill corporate/commercial client sustainability targets requiring unbundled Green-e certification where physical RPS compliance is not legally mandated.

---

### [TIER 2 ACTION REQUIRED]
*Financial Commodity Commitment Notice*

```yaml
Transaction_Intent: "Forward REC Procurement Hedge Execution"
Market_Segment: "PJM Tier I Compliance (Vintage 2024 / 2025)"
Volume: "50,000 MWh (RECs)"
Limit_Price: "$34.25 / REC"
Estimated_Notional_Value: "$1,712,500.00 USD"
Counterparty_Type: "Bilateral OTC / Cleared Exchange"
Compliance_Target_Jurisdiction: "PJM GATS (MD/NJ/PA RPS Portfolio Obligation)"
Approval_Protocol: "Tier 2 Wholesale Trading - Human In The Loop (HITL) Signature Required"
```
*To authorize execution of the proposed forward REC procurement contract, please confirm operator sign-off with trading floor risk parameters.*

### Example 2: Trend & Comparative Analysis
**User:** "Track our portfolio surplus REC generation inventory across wind and solar assets against state RPS compliance obligations."

**Agent Response:**
### Executive Summary
**The portfolio maintains a net positive REC surplus of +353,000 MWh across solar and wind fleets relative to current compliance year (CY2024) state RPS obligations.** **Wind generation in ERCOT and PJM Class I provides the largest surplus volume (+225,000 RECs), while high-value Solar SREC carves-outs in PJM/NJ-MD are over-hedged by +20.0% against compliance mandates.** **Current market liquidity presents an optimal window to monetize unhedged Tier 1 and SREC surplus balances via over-the-counter (OTC) bilateral transfers and spot auction clearance before vintage banking expiration.**

---

### Portfolio REC Inventory & RPS Compliance Balance

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Portfolio REC Generation (MWh)** | 1,488,000 RECs | 1,320,000 RECs | +12.7% | **Normal** |
| **Banked Carryover (Prior Vintage)** | 210,000 RECs | 180,000 RECs | +16.7% | **Normal** |
| **Total Gross REC Supply** | 1,698,000 RECs | 1,500,000 RECs | +13.2% | **Normal** |
| **Mandatory State RPS Obligations** | 1,345,000 RECs | 1,345,000 RECs | 0.0% | **Normal** |
| **Net Portfolio Surplus Balance** | **+353,000 RECs** | +155,000 RECs (Min Reserve) | +127.7% | **Normal** |
| **PJM Tier 1 / Class I Position** | +135,000 RECs | Obligation: 450,000 RECs | +30.0% | **Normal** |
| **NEPOOL Class I Position** | +55,000 RECs | Obligation: 280,000 RECs | +19.6% | **Normal** |
| **CA RPS (PCC-1 Bundle) Position** | +60,000 RECs | Obligation: 350,000 RECs | +17.1% | **Normal** |
| **ERCOT Tier 1 / Voluntary Surplus** | +90,000 RECs | Obligation: 200,000 RECs | +45.0% | **Normal** |
| **Solar SREC Carve-Out (NJ/MD/PA)** | +13,000 SRECs | Obligation: 65,000 SRECs | +20.0% | **Normal** |
| **Compliance Value-at-Risk (ACP Penalty Floor)** | $0.00 (Zero Shortfall) | $0.00 | 0.0% | **Normal** |

---

### Jurisdiction & Asset Class Breakdown

```
+----------------------------------------------------------------------------------------------------+
| Asset Class | Region / Market | RPS Tier / Carve-Out | Generation (MWh) | Banked | Obligation | Net Balance |
+----------------------------------------------------------------------------------------------------+
| Utility Wind| PJM (West/PJM-Classic)| Class I / Tier 1 |   395,000        | 80,000 |  360,000   | +115,000    |
| Utility Wind| ERCOT (Panhandle/Coast)| State Vol / Tier 1|  240,000        | 50,000 |  200,000   |  +90,000    |
| Utility Solar| PJM (DPL/PEPCO/PSEG) | Class I / SREC   |   190,000        | 30,000 |  155,000   |  +65,000    |
| Utility Solar| NEPOOL (MA/CT/RI)    | Class I RPS      |   300,000        | 35,000 |  280,000   |  +55,000    |
| Utility Solar| CAISO (SP15/NP15)    | PCC-1 (In-State) |   363,000        | 15,000 |  350,000   |  +28,000    |
+----------------------------------------------------------------------------------------------------+
```

---

### Visualization Trigger: Portfolio Obligation vs Available RECs

```json
{
  "chart_type": "bar",
  "title": "Portfolio RPS Obligation vs Available Inventory & Surplus",
  "xAxis": {
    "categories": [
      "PJM Class I (Wind/Solar)",
      "NEPOOL Class I",
      "CA RPS (PCC-1)",
      "ERCOT Tier 1",
      "NJ/MD Solar SREC"
    ]
  },
  "yAxis": {
    "title": "Volume (MWh / RECs)"
  },
  "series": [
    {
      "name": "Obligation (MWh/RECs)",
      "data": [450000, 280000, 350000, 200000, 65000]
    },
    {
      "name": "Total Available (Gen + Banked)",
      "data": [585000, 335000, 410000, 290000, 78000]
    },
    {
      "name": "Net Surplus (RECs)",
      "data": [135000, 55000, 60000, 90000, 13000]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Monetize Front-Month PJM SREC Surplus**: Execute bilateral sales for 10,000 NJ/MD SRECs currently trading at premium spreads ($215–$230/MWh) prior to vintage expiration windows.
2. **Execute Forward Hedging for CY2025/2026**: Lock in forward Tier 1 REC swaps for NEPOOL Class I (+35,000 RECs at ~$41.50/MWh) to de-risk future compliance cost escalations.
3. **PJM-GATS / NEPOOL-GIS Registry Reconciliation**: Finalize monthly generation certificate minting and retire compliance-matched tranches to avoid Alternative Compliance Payment (ACP) liability.
4. **Maintain Operational Banking Buffer**: Retain a 10% safety buffer (134,500 RECs) across all asset nodes to insulate against potential Q4 generation shortfalls from low wind/solar resource availability.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "REC_FORWARD_SALE_EXECUTION",
  "risk_level": "Tier 2 - Financial Market Transaction",
  "jurisdiction_registries": ["PJM-GATS", "NEPOOL-GIS"],
  "proposed_transactions": [
    {
      "contract": "NJ-SREC-CY2024-SPOT",
      "volume_recs": 10000,
      "settlement_type": "OTC Bilateral Transfer",
      "target_price_per_rec": 222.50,
      "estimated_proceeds_usd": 2225000.00
    },
    {
      "contract": "NEPOOL-CLASS1-CY2024-FWD",
      "volume_recs": 35000,
      "settlement_type": "Broker Clearance",
      "target_price_per_rec": 41.75,
      "estimated_proceeds_usd": 1461250.00
    }
  ],
  "total_estimated_gross_proceeds_usd": 3686250.00,
  "compliance_impact": "Post-execution remaining surplus maintains compliance safety margin at +208,000 RECs (15.5% above obligation).",
  "approval_required": "Human-In-The-Loop (HITL) Head of Wholesale Trading / Risk Manager confirmation required prior to order routing."
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Execute a bilateral sale contract of 25,000 Class 1 Green-e certified solar RECs at $24.50 per certificate."

**Agent Response:**
### Executive Summary
**A bilateral sale contract order for 25,000 Class 1 Green-e certified Solar Renewable Energy Certificates (RECs) at $24.50/REC (total notional value: $612,500.00) has been structured and validated against wholesale risk boundaries. In accordance with enterprise safety guardrails, physical/financial commodity contract execution is classified as a Tier 2 operation and cannot be autonomously committed. The transaction order has been staged and requires formal Human-In-The-Loop (HITL) authorization prior to clearing and registry transfer.**

---

### Transaction & Portfolio Summary

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Transaction Type** | Bilateral Spot/Forward Sale | Spot Inventory Monetization | N/A | **Normal** |
| **REC Category / Standard** | Solar Class 1 (Green-e) | PJM/NEPOOL/ERCOT Tier 1 | 0.00% | **Normal** |
| **Contract Volume** | 25,000 RECs (25,000 MWh) | 25,000 RECs | 0.00% | **Normal** |
| **Execution Price** | $24.50 / REC | $24.00 / REC (Market Mark) | +2.08% | **Normal** |
| **Gross Contract Value** | $612,500.00 | $600,000.00 | +2.08% | **Normal** |
| **Post-Trade Compliance Buffer**| 118,500 RECs | 100,000 RECs Min Mandate | +18.50% | **Normal** |

---

### Visualization Trigger
```json
{
  "chart_type": "bar",
  "data": {
    "labels": ["Execution Price ($)", "Market Mark Benchmark ($)"],
    "datasets": [
      {
        "label": "Class 1 Green-e Solar REC Pricing",
        "data": [24.50, 24.00]
      }
    ]
  }
}
```

---

### Actionable Recommendations
1. **Verify Registry Inventory**: Confirm that 25,000 unencumbered Class 1 Solar RECs are active and serialized in the designated tracking registry (e.g., PJM-GATS, NEPOOL-GIS, or WREGIS).
2. **Review Credit Exposure**: Ensure the counterparty has sufficient credit limits and active master trading agreements (e.g., EEI/ISDA REC Annex) in place.
3. **Execute HITL Approval**: Authorize the staged contract payload below to dispatch the binding trade confirmation and initiate transfer in the tracking registry.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EXECUTE_BILATERAL_REC_SALE",
  "trade_details": {
    "commodity": "Solar Renewable Energy Certificate",
    "certification": "Green-e Certified / Class 1",
    "quantity_mwh": 25000,
    "unit_price_usd": 24.50,
    "total_notional_value_usd": 612500.00,
    "settlement_type": "Bilateral Delivery vs. Payment",
    "settlement_registry": "Tracking System (GATS/GIS/WREGIS)"
  },
  "risk_validation": {
    "portfolio_var_impact": "Negligible (Long Inventory Reduction)",
    "rpo_compliance_impact": "Compliant (Maintains statutory surplus)"
  },
  "requires_hitl_confirmation": true,
  "status": "PENDING_OPERATOR_APPROVAL"
}
```
