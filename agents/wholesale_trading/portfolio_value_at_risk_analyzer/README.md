# ⚡ Portfolio Value At Risk Analyzer

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of portfolio value at risk analyzer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Portfolio Value At Risk Analyzer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank portfolio value at risk analyzer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.portfolio_value_at_risk_analyzer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is our wholesale energy portfolio 99% one-day Value at Risk (VaR) under a simulated 20% natural gas price spike?"

**Agent Response:**
### Executive Summary
**Under a simulated +20% natural gas commodity price spike (from $2.75/MMBtu to $3.30/MMBtu), the wholesale energy portfolio’s 1-day 99% Value at Risk (VaR) increases from the baseline of $4.20M to $8.65M (+105.95%). The primary risk driver is the portfolio's unhedged short power exposure and variable heat rate spark-spread erosion across uncommitted gas peakers and open spot obligations. Total downside risk breaches the enterprise operational tolerance threshold ($7.50M), transitioning the risk profile to a Warning/Critical threshold.**

---

### Quantitative Risk Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **1-Day 99% VaR (Stress Scenario)** | **$8.65M** | $4.20M | +105.95% | **Warning** |
| **1-Day 95% VaR (Stress Scenario)** | **$6.12M** | $2.95M | +107.46% | **Warning** |
| **Expected Shortfall (CVaR 99%)** | **$11.40M** | $5.30M | +115.09% | **Critical** |
| **Spark Spread Margin Delta** | **-$14.20/MWh** | $0.00/MWh | -100.00% | **Critical** |
| **Short Power Position Exposure** | **1,250 MW** | 500 MW (Target Max) | +150.00% | **Warning** |
| **Gas Peaker Fleet Operating Margin** | **$3.85M** | $6.20M | -37.90% | **Warning** |

*Methodology: Parametric and Historical Monte Carlo simulation (10,000 iterations), assuming correlated Henry Hub/Regional Basis upward shift of 20% with power LMP elasticity response of 1.65x.*

---

### Visualization Trigger

**Recommended Chart Type:** Grouped Bar Chart (VaR Exposure Breakdown by Book/Asset Class)

```json
{
  "chart_type": "bar",
  "title": "Portfolio VaR Sensitivity by Asset Class under +20% Gas Spike Scenario",
  "categories": [
    "Combined Cycle Gas Turbines (CCGT)",
    "Gas Peakers (CT)",
    "Purchased Power Agreements (PPA)",
    "Wholesale Power Short Positions",
    "Net Generation & Trading Book"
  ],
  "series": [
    {
      "name": "Baseline 1-Day 99% VaR ($M)",
      "data": [1.45, 0.85, 0.60, 2.10, 4.20]
    },
    {
      "name": "Stress (+20% Gas Spike) 1-Day 99% VaR ($M)",
      "data": [2.85, 1.75, 0.95, 4.35, 8.65]
    }
  ],
  "units": "$ Millions USD"
}
```

---

### Actionable Recommendations

1. **Implement Financial Gas Call Options / Swaps:** Execute prompt-month financial call options on Henry Hub/regional gas hubs to cap fuel input costs for uncommitted thermal generation.
2. **Rebalance Spot-to-Term Generation Bids:** Reallocate 450 MW of merchant CCGT capacity into Day-Ahead LMP forward hedges to insulate revenue against fuel price volatility.
3. **Adjust Peaker Unit Dispatch Thresholds:** Recalculate heat-rate strike prices and reserve shutdown parameters across CT units to mitigate negative operating margin risks during high fuel cost intervals.
4. **Tighten Daily Enterprise VaR Limits:** Notify the Risk Management Committee (RMC) of the stress threshold breach and enforce temporary position sizing restrictions on wholesale spot power desk operations.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "HEDGE_EXECUTION_AND_LIMIT_ADJUSTMENT",
  "domain": "wholesale_trading",
  "requester": "portfolio_value_at_risk_analyzer",
  "details": {
    "proposed_action": "Execute prompt-month natural gas swap purchase of 50,000 MMBtu/day and adjust Day-Ahead power hedge coverage from 60% to 80%",
    "financial_exposure": "$3,850,000",
    "risk_reduction_impact": "Reduces 1-Day 99% VaR from $8.65M down to $4.95M (-42.8%)",
    "required_approver": "Head of Energy Trading / Chief Risk Officer (CRO)"
  },
  "status": "AWAITING_HUMAN_IN_THE_LOOP_CONFIRMATION"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Run 10,000 Monte Carlo iterations combining correlated forward power price volatility, heat rates, and plant forced outage probabilities."

**Agent Response:**
### Executive Summary
**The 10,000-iteration Monte Carlo simulation has been executed across correlated forward power curves, market implied heat rates, and plant Equivalent Forced Outage Rates (EFORd). The portfolio 95% 1-Month Value at Risk (VaR) is evaluated at -$5.12M, driven primarily by peak-hour power price volatility coupled with correlated gas spark spread compression and peak-period generator availability. Downside tail exposure (99% CVaR / Expected Shortfall) extends to -$11.45M under compound outage and price spike conditions.**

---

### Quantitative Risk Analysis (10,000 Iteration Results)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **95% Value at Risk (1-Month VaR)** | -$5.12M | -$4.00M | +28.0% | **Warning** |
| **99% Value at Risk (1-Month VaR)** | -$8.84M | -$7.00M | +26.3% | **Warning** |
| **95% Conditional VaR (Expected Shortfall)** | -$7.65M | -$5.50M | +39.1% | **Warning** |
| **99% Conditional VaR (Tail Risk)** | -$11.45M | -$9.00M | +27.2% | **Critical** |
| **Expected Mean Gross Margin (P50)** | +$14.28M | +$15.00M | -4.8% | **Normal** |
| **Simulated Fleet EFORd Impact** | -$1.85M | -$1.20M | +54.2% | **Warning** |
| **Spark Spread / Heat Rate Correlation ($\rho$)** | 0.72 | 0.65 | +10.8% | **Normal** |
| **Implied Power Volatility ($\sigma_{power}$)** | 42.5% | 35.0% | +21.4% | **Warning** |

---

### Visualization Triggers

A Monte Carlo P&L distribution chart has been compiled to visualize the distribution of outcomes across all 10,000 iterations, emphasizing the 95% and 99% VaR tail regions.

```json
{
  "chart_type": "bar",
  "title": "10,000 Iteration Monte Carlo Portfolio P&L Distribution ($M)",
  "labels": [
    "<-$12M (Tail Risk)",
    "-$12M to -$8M (99% VaR)",
    "-$8M to -$5.1M (95% VaR)",
    "-$5.1M to -$2M",
    "-$2M to $0M",
    "$0M to $3M",
    "$3M to $6M",
    "$6M to $9M",
    ">$9M"
  ],
  "datasets": [
    {
      "label": "Simulated Frequency (Count)",
      "data": [112, 388, 500, 1500, 2500, 2800, 1450, 650, 100]
    }
  ]
}
```

---

### Component Risk Decomposition
1. **Power Price Volatility Contribution (48.2%)**: On-peak forward power price swings represent the largest contributor to downside variance due to open net long/short prompt-month exposures across zonal LMP hubs.
2. **Spark Spread & Heat Rate Risk (33.7%)**: Marginal heat rate fluctuations against index gas contracts induce unhedged shape risk during sub-economic dispatch intervals.
3. **Plant Outage Volumetric Risk (18.1%)**: Coincident forced outages during high-LMP hours exacerbate replacement power costs, driving the heavy left tail beyond the 95th percentile.

---

### Actionable Recommendations

- **Execute Heat Rate / Spark Spread Hedges**: Reduce prompt-month open exposure by entering into clean spark spread options or fixed-for-floating heat rate swaps to compress the VaR back within the -$4.00M limit.
- **Implement Peak-Period Volumetric Cover**: Secure physical call options or firm transmission capacity hedges to insulate against unhedged replacement power costs in the event of forced outages at primary baseload/peaking assets.
- **Review Enterprise Risk Limits**: Present the current VaR threshold breach (+28% above risk policy target) to the Energy Risk Management Committee (ERMC) for position rebalancing approval.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "HEDGE_REBALANCING_TRANSACTION",
  "domain": "Wholesale Trading",
  "risk_impact": "Reduction of 1-Month 95% VaR from -$5.12M to -$3.85M",
  "proposed_trades": [
    {
      "instrument": "Prompt-Month On-Peak Heat Rate Swap",
      "volume_mw": 150,
      "settlement_hub": "Zonal Hub LMP",
      "action": "BUY_FLOOR / SELL_CAP (COLLAR)"
    }
  ],
  "authorization_required": "Human-In-The-Loop (HITL) Trading Desk Lead / ERMC Approval"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Recommend immediate forward hedging transactions to reduce portfolio VaR below the corporate board risk ceiling of $15M."

**Agent Response:**
### 1. Executive Summary
**The enterprise wholesale trading portfolio currently exhibits a 95% Confidence Value at Risk (VaR) of $19.80M, breaching the corporate board risk ceiling of $15.00M by $4.80M (+32.0%). To restore compliance and establish an operational buffer, an immediate forward financial swap hedging package across prompt-month peak and off-peak forward blocks is required to reduce net open position volatility. Executing the recommended 350 MW aggregate forward hedge will bring post-trade portfolio VaR down to $12.80M, successfully mitigating tail-risk exposure within mandated governance limits.**

---

### 2. Quantitative Risk Metrics & Exposure Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Portfolio 1-Day 95% VaR** | $19.80M | $15.00M (Board Ceiling) | +32.00% | **Critical** |
| **Conditional VaR (CVaR / Expected Shortfall)** | $26.40M | $20.00M | +32.00% | **Critical** |
| **Net Prompt-Month Open Position** | +850 MW | +500 MW (Target Net) | +70.00% | **Warning** |
| **Peak LMP Volatility Exposure** | $78.50/MWh | $52.00/MWh | +50.96% | **Warning** |
| **Post-Hedge Projected VaR** | $12.80M | $15.00M (Board Ceiling) | -14.67% | **Normal** |

---

### 3. Recommended Forward Hedging Strategy

To effectively dampen prompt-month power curve covariance and cross-zonal basis risk, the following forward financial hedging contracts are recommended for immediate block execution:

* **Tranche A (Peak Forward Financial Swap)**:
  * **Contract**: Prompt-Month Hub Peak LMP Fixed-for-Floating Swap
  * **Volume**: 150 MW (7x16 Peak Block)
  * **Tenor**: Prompt Month (30-day forward delivery)
  * **VaR Impact**: -$3.40M reduction

* **Tranche B (Off-Peak Forward Financial Swap)**:
  * **Contract**: Prompt-Month Hub Off-Peak Fixed-for-Floating Swap
  * **Volume**: 200 MW (7x8 + 2x24 Off-Peak Block)
  * **Tenor**: Prompt Month (30-day forward delivery)
  * **VaR Impact**: -$3.60M reduction

* **Combined Net Portfolio VaR Reduction**: **-$7.00M** (accounting for cross-commodity and covariance offset), yielding a final post-execution portfolio VaR of **$12.80M**.

---

### 4. Visualization Trigger

**Recommended Chart**: Risk Waterfall / Horizon Bar Chart comparing pre-hedge risk, individual hedge block risk reductions, target board threshold, and final post-hedge position.

```json
{
  "chart_type": "bar",
  "title": "Portfolio VaR Mitigation Path vs. Board Limit ($M)",
  "data": {
    "categories": [
      "Current Portfolio VaR",
      "Tranche A (Peak 150MW)",
      "Tranche B (Off-Peak 200MW)",
      "Post-Hedge Position",
      "Corporate Board Ceiling"
    ],
    "series": [
      {
        "name": "Portfolio VaR ($M, 95% Conf)",
        "values": [19.80, 16.40, 13.60, 12.80, 15.00]
      }
    ]
  }
}
```

---

### 5. Actionable Recommendations

1. **Submit Tier 2 Order Approval**: Route the forward swap package to the Chief Risk Officer (CRO) and Lead Financial Trader for formal execution authorization.
2. **Execute Staged Counterparty Allocations**: Split the 350 MW aggregate volume across bilateral ISDA counterparties and cleared exchange contracts (e.g., ICE/CME) to minimize single-clearinghouse margin call concentration.
3. **Re-evaluate Covariance Matrix Post-Settlement**: Perform real-time intra-day Monte Carlo stress-testing post-execution to confirm that correlation changes do not trigger second-order basis limit breaches.
4. **Notify Master Orchestrator**: Update the enterprise trading risk state to reflect pending execution status and expected limit re-entry.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "WHOLESALE_FINANCIAL_TRANSACTION",
  "action_description": "Execute Prompt-Month Forward Financial Swap Hedging Package to reduce Portfolio VaR from $19.80M to $12.80M below the $15.00M Board Limit.",
  "contracts": [
    {
      "instrument": "Hub Peak Fixed-for-Floating Financial Swap",
      "trade_type": "Sell / Short Hedge",
      "volume_mw": 150,
      "tenor": "Prompt-Month (Calendar Month +1)",
      "clearing_venue": "ICE/CME Cleared"
    },
    {
      "instrument": "Hub Off-Peak Fixed-for-Floating Financial Swap",
      "trade_type": "Sell / Short Hedge",
      "volume_mw": 200,
      "tenor": "Prompt-Month (Calendar Month +1)",
      "clearing_venue": "ICE/CME Cleared"
    }
  ],
  "estimated_margin_requirement_usd": 2450000.00,
  "projected_post_trade_var_usd": 12800000.00,
  "requires_approval": true,
  "approver_roles": ["Chief_Risk_Officer", "Lead_Wholesale_Trader"]
}
```
