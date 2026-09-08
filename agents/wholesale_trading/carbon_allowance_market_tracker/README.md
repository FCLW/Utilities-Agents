# ⚡ Carbon Allowance Market Tracker

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of carbon allowance market tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Carbon Allowance Market Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank carbon allowance market tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.carbon_allowance_market_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What are California Carbon Allowance (CCA) and RGGI carbon credit contracts trading at for December forward delivery?"

**Agent Response:**
### Executive Summary
**California Carbon Allowance (CCA) December forward contracts are trading at \$40.25/MT (Prompt Dec-24 delivery) and \$43.10/MT (Dec-25 delivery), reflecting tightening market balances and regulatory adjustments under CARB's cap-and-trade program.** **Regional Greenhouse Gas Initiative (RGGI) December forward contracts are clearing at \$21.45/short ton (Dec-24) and \$22.80/short ton (Dec-25), continuing their steady premium above statutory auction reserve floors driven by robust compliance demand across participating Northeast power generators.**

---

### Data Presentation

The table below summarizes forward market settlement levels on the Intercontinental Exchange (ICE) and associated compliance thresholds for December prompt and forward vintages:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **CCA Vintage 2024 (Dec-24 Forward)** | \$40.25 / MT | \$24.04 / MT *(CARB Floor Price)* | +67.43% | Normal |
| **CCA Vintage 2025 (Dec-25 Forward)** | \$43.10 / MT | \$25.24 / MT *(Est. Floor Price)* | +70.76% | Normal |
| **CCA Allowance Price Containment Tier 1** | \$56.20 / MT | \$56.20 / MT *(Statutory Trigger)* | -28.38% | Normal |
| **RGGI Vintage 2024 (Dec-24 Forward)** | \$21.45 / ton | \$15.92 / ton *(Cost Containment Tier 1)* | +34.74% | Warning |
| **RGGI Vintage 2025 (Dec-25 Forward)** | \$22.80 / ton | \$16.72 / ton *(Est. Cost Containment)* | +36.36% | Warning |
| **RGGI Minimum Reserve Price (2024)** | \$2.56 / ton | \$2.56 / ton *(Statutory Floor)* | +737.89% | Normal |

*Note: CCA units are priced per Metric Ton ($/MT), while RGGI contracts are priced per Short Ton ($/ton) pursuant to jurisdictional market rules.*

---

### Visualization Triggers

**Recommended Visualization:** Grouped Bar Chart comparing current forward contract valuations against regulatory reserve price floors and cost containment triggers.

```json
{
  "chart_type": "bar",
  "title": "Carbon Allowance Forward Contract Pricing vs. Regulatory Reserve Floors",
  "categories": [
    "CCA V24 (Dec-24)",
    "CCA V25 (Dec-25)",
    "RGGI V24 (Dec-24)",
    "RGGI V25 (Dec-25)"
  ],
  "series": [
    {"name": "Current Forward Price ($/ton or MT)", "data": [40.25, 43.10, 21.45, 22.80]},
    {"name": "Regulatory Floor / Baseline ($/ton or MT)", "data": [24.04, 25.24, 2.56, 2.69]},
    {"name": "Cost Containment Trigger Level ($/ton or MT)", "data": [56.20, 59.01, 15.92, 16.72]}
  ]
}
```

---

### Actionable Recommendations

- **Hedge True-Up Evaluation**: Re-assess prompt December compliance obligations across generation assets in CAISO and PJM/NYISO/ISO-NE to verify that open surrender ratios align with targeted compliance schedules.
- **RGGI Cost Containment Trigger Monitoring**: RGGI forward trading remains above the Cost Containment Reserve (CCR) trigger price (\$15.92/ton), indicating continued auction reserve release risk; evaluate dollar-cost averaging for remaining Q4 compliance volume.
- **Forward Spread Strategy**: Monitor the CCA V24–V25 contango spread (\$2.85/MT) against the internal cost of capital to evaluate carry trade or banking optimization opportunities ahead of CARB program amendments.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action: carbon_allowance_forward_procurement
  target_portfolios:
    - CCA_Dec24_Hedge
    - RGGI_Dec24_Hedge
  proposed_execution:
    market: ICE Futures US / Energy Derivatives
    contracts:
      - instrument: California Carbon Allowance Vintage 2024 Futures
        delivery_period: December 2024
        limit_price: "$40.50 / MT"
        volume_mt: 50000
      - instrument: RGGI CO2 Allowance Vintage 2024 Futures
        delivery_period: December 2024
        limit_price: "$21.60 / short ton"
        volume_tons: 75000
  risk_validation: Passed Value-at-Risk (VaR) and Credit Threshold limits.
  approval_status: PENDING_HUMAN_OPERATOR_SIGN_OFF
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate quarterly allowance auction clearing prices with fossil generation output and state regulatory cap adjustments."

**Agent Response:**
### 1. Executive Summary
**Quarterly carbon allowance auction clearing prices demonstrate a strong inverse correlation ($r = -0.91$) with annual state regulatory cap reductions, driving clearing prices up 18.4% year-over-year to $46.20/MT.** **While fossil generation exhibits high seasonal intraday volatility ($r = +0.68$ correlation to peak summer run-hours), structural multi-year cap tightenings are the primary driver of allowance scarcity and upward clearing price pressure.** **Compliance obligation ratios for the utility fossil portfolio have reached 104.2% of baseline surrender targets, necessitating immediate hedge adjustments in wholesale forward markets.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Quarterly Auction Clearing Price ($/MT)** | $46.20 | $38.45 | +20.16% | **Warning** |
| **Net Fossil Fleet Output (Q1 Trajectory - GWh)** | 13,200 GWh | 13,900 GWh | -5.04% | **Normal** |
| **Annual State Cap Allocation (MMT CO₂e)** | 62.8 MMT | 67.6 MMT | -7.10% | **Warning** |
| **Portfolio Compliance Obligation (MMT CO₂e)** | 11.25 MMT | 10.80 MMT | +4.17% | **Warning** |
| **Clean Spark Spread Compression** | $8.40/MWh | $12.50/MWh | -32.80% | **Critical** |
| **Allowance Price Cap Reserve Floor ($/MT)** | $24.60 | $22.20 | +10.81% | **Normal** |
| **Allowance Inventory Hedge Ratio** | 78.5% | 90.0% | -12.78% | **Warning** |

---

### 3. Econometric & Dispatch Correlation Analysis

1. **Regulatory Cap Step-Down Elasticity**:
   * The annual statutory cap decrease of **7.10%** (from 67.6 MMT to 62.8 MMT) has shifted auction supply-demand curves leftward, resulting in a **+$7.75/MT** structural upward price adjustment independent of weather anomalies.
2. **Fossil Fleet Volatility & Marginal Abatement**:
   * Peak summer and winter dispatch intervals continue to require peaker operations (CTs and unscrubbed CCGTs), causing non-linear surges in allowance demand during high LMP hours despite flat baseload demand.
3. **Portfolio Value at Risk (VaR)**:
   * Unhedged allowance liability exposure across the rolling 12-month window stands at **$103.95M**, exceeding risk tolerance thresholds by **$14.2M** under 95% Confidence Interval scenarios.

---

### 4. Visualization Trigger

```json
{
  "chart_type": "combo",
  "title": "Carbon Allowance Clearing Prices vs. Fossil Generation Output & Statutory Cap",
  "data_json": {
    "labels": ["Q1 2023", "Q2 2023", "Q3 2023", "Q4 2023", "Q1 2024", "Q2 2024", "Q3 2024", "Q4 2024", "Q1 2025 (Est.)"],
    "datasets": [
      {
        "name": "Clearing Price ($/MT)",
        "type": "line",
        "yAxis": "price",
        "data": [29.85, 31.20, 35.50, 36.80, 38.45, 41.10, 44.75, 42.60, 46.20]
      },
      {
        "name": "Fossil Generation (GWh)",
        "type": "bar",
        "yAxis": "generation",
        "data": [14200, 12800, 16900, 13400, 13900, 12100, 17400, 12900, 13200]
      },
      {
        "name": "Quarterly Regulatory Cap (MMT)",
        "type": "line",
        "yAxis": "cap",
        "data": [18.2, 18.2, 18.2, 18.2, 16.9, 16.9, 16.9, 16.9, 15.7]
      }
    ]
  }
}
```

---

### 5. Actionable Recommendations

* **Rebalance Portfolio Hedging Trajectory**: Increase Tier 1 forward allowance procurement to close the 11.5% hedge deficit prior to the Q2 secondary auction window.
* **Incorporate Carbon Floor Escalators in Day-Ahead Bidding**: Update short-run marginal cost (SRMC) offer curves for gas turbine units to embed a **$46.20/MT** marginal carbon cost adder in RTO/ISO market submissions.
* **Dispatch Displacement Optimization**: Coordinate with GMS (Generation Management Systems) to prioritize high-efficiency CCGT heat rate tiers when allowance forward curves trade above $45.00/MT.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "ALLOWANCE_FORWARD_HEDGE_ORDER",
  "status": "PENDING_HUMAN_APPROVAL",
  "details": {
    "instrument": "State Compliance Carbon Allowance (CCA) Futures / Bilateral Forwards",
    "delivery_period": "Q2/Q3 2025",
    "volume_metric_tons": 500000,
    "limit_price_usd_per_ton": 46.50,
    "notional_value_usd": 23250000.00,
    "target_counterparty_clearinghouse": "ICE / Nodal Exchange",
    "risk_mitigation_target": "Brings portfolio compliance hedge ratio from 78.5% to 89.6%"
  },
  "required_approver": "Wholesale Trading Desk Lead / Portfolio Risk Manager"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Execute a forward purchase hedge for 50,000 metric tons of compliance carbon allowances at $38.50 per ton."

**Agent Response:**
### Executive Summary
**A request has been initiated to execute a forward purchase hedge of 50,000 metric tons (MT) of compliance carbon allowances at a contract strike price of $38.50/MT, yielding a total financial commitment of $1,925,000.00. Under utility trading safety guardrails and wholesale risk policy, automated execution of commodity and financial procurement contracts is strictly classified as a Tier 2 operation and cannot be autonomously dispatched. The transaction payload has been staged and validated by the Critic Agent, requiring Human-In-The-Loop (HITL) authorization prior to market submission.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Order Volume** | 50,000 MT | 50,000 MT | 0.00% | Normal |
| **Contract Limit Price** | $38.50 / MT | $38.20 / MT (Index Reference) | +0.79% | Normal |
| **Total Notional Exposure** | $1,925,000.00 | $1,910,000.00 | +0.79% | Normal |
| **Hedge Horizon** | Forward Strip (Compliance) | Annual Compliance Target | N/A | Normal |
| **Portfolio VaR Utilization** | 68.4% | 85.00% (VaR Cap) | -16.60% | Normal |

---

### Visualization Triggers
- **Recommended Chart**: Financial Exposure and Volume Breakdown (Bar Chart).
- **Chart Data Configuration**:
```json
{
  "chart_type": "bar",
  "title": "Forward Carbon Allowance Hedge Commitment",
  "data": {
    "instruments": ["Compliance Carbon Allowance Forward"],
    "metrics": {
      "volume_mt": 50000,
      "strike_price_usd": 38.50,
      "notional_value_usd": 1925000.00
    }
  }
}
```

---

### Actionable Recommendations
- **Risk Validation**: Confirm total hedge volume is aligned with portfolio emission compliance obligations and within authorized counterparty credit lines.
- **Limit Verification**: Verify whether current market depth allows execution of 50,000 MT at or below $38.50/MT without adverse market impact.
- **Trader Authorization**: Review the staged Tier 2 transaction payload below and provide explicit operational approval to submit the order to the designated exchange/broker.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EXECUTE_FORWARD_COMMODITY_HEDGE",
  "domain": "Wholesale Trading",
  "subdomain": "Carbon Allowance Market Tracker",
  "asset_class": "Compliance Carbon Allowances (EUA/CCA)",
  "trade_parameters": {
    "volume_metric_tons": 50000,
    "limit_price_per_ton": 38.50,
    "currency": "USD",
    "total_notional": 1925000.00,
    "execution_type": "Forward Hedge",
    "settlement_type": "Physical Delivery / Registry Transfer"
  },
  "critic_agent_validation": {
    "status": "PASSED",
    "var_limit_breach": false,
    "policy_compliance": "APPROVED_STAGING"
  },
  "status": "PENDING_HUMAN_APPROVAL"
}
```
