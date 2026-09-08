# ⚡ Financial Transmission Right Copilot

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of financial transmission right copilot is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Financial Transmission Right Copilot Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank financial transmission right copilot events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.financial_transmission_right_copilot_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which Financial Transmission Right (FTR) paths between West Hub and Load Zone 1 offer the highest expected auction payout return?"

**Agent Response:**
### 1. Executive Summary
**Analysis of historical Day-Ahead Congestion Price differentials (MCC) and current Auction Clearing Prices (ACP) indicates that the `WH_HUB -> LZ1_NORTH_SUB` and `WH_HUB -> LZ1_CENTRAL` paths deliver the highest expected return on auction investment at +69.5% and +68.1% net ROI, respectively.** 
**Transmission line derates and projected summer peak load import constraints across the West-to-East 345 kV interface drive elevated positive congestion spreads into Load Zone 1.** 
**Bidding on these specific paths provides superior risk-adjusted Value-at-Risk (VaR) efficiency compared to broad zonal aggregate paths.**

---

### 2. Data Presentation (Markdown Tables)

#### Portfolio & Market Metric Overview
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Top Path Expected Net Return (WH_HUB -> LZ1_NORTH)** | 69.5% ROI | 25.0% Target ROI | +178.0% | Normal |
| **Average LZ1 Congestion Spread (DA MCC Sink - Source)** | $6.95 / MWh | $4.50 / MWh | +54.4% | Warning |
| **Auction Clearing Price Premium / Discount** | $4.10 / MWh | $4.35 / MWh | -5.7% | Normal |
| **Portfolio 95% 1-Month Value at Risk (VaR)** | $142,000 | $250,000 Cap | -43.2% | Normal |
| **West-East Interface Constraint Probability** | 78.4% | 52.0% Historical | +50.8% | Warning |

#### Path Payout & Return Breakdown (West Hub to Load Zone 1 Delivery Points)
| Path ID | Source Node | Sink Node | Auction Clearing Price ($/MWh) | Expected DA Congestion ($/MWh) | Expected Net Payout ($/MWh) | Expected Return (%) | Risk-Adjusted Sharpe Ratio |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **FTR-LZ1-01** | `WEST_HUB` | `LZ1_NORTH_SUB` | $4.10 | $6.95 | +$2.85 | **+69.5%** | 2.41 |
| **FTR-LZ1-02** | `WEST_HUB` | `LZ1_CENTRAL` | $3.45 | $5.80 | +$2.35 | **+68.1%** | 2.35 |
| **FTR-LZ1-03** | `WEST_HUB` | `LZ1_INTERFACE` | $2.80 | $3.90 | +$1.10 | **+39.3%** | 1.62 |
| **FTR-LZ1-04** | `WEST_HUB` | `LZ1_SOUTH_345kV` | $5.25 | $7.10 | +$1.85 | **+35.2%** | 1.48 |

---

### 3. Visualization Triggers
- **Recommended Chart Type**: Grouped Bar Chart comparing Auction Clearing Price, Expected Day-Ahead Congestion Rent, and Net ROI (%) across candidate FTR paths.

```json
{
  "chart_type": "bar",
  "title": "FTR Expected Payout vs. Auction Clearing Price (West Hub -> Load Zone 1)",
  "categories": [
    "WH_HUB to LZ1_NORTH_SUB",
    "WH_HUB to LZ1_CENTRAL",
    "WH_HUB to LZ1_INTERFACE",
    "WH_HUB to LZ1_SOUTH_345kV"
  ],
  "series": [
    {
      "name": "Auction Clearing Price ($/MWh)",
      "data": [4.10, 3.45, 2.80, 5.25]
    },
    {
      "name": "Expected DA Congestion Rent ($/MWh)",
      "data": [6.95, 5.80, 3.90, 7.10]
    },
    {
      "name": "Expected Net Payout ($/MWh)",
      "data": [2.85, 2.35, 1.10, 1.85]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Priority Allocation**: Target 60% of the allocated capital tranche to `WH_HUB -> LZ1_NORTH_SUB` and 40% to `WH_HUB -> LZ1_CENTRAL` to capture peak forward congestion premia.
- **Limit Bid Strategy**: Implement a maximum limit bid cap at **$4.40/MWh** for `LZ1_NORTH_SUB` to preserve a minimum hurdle return of >50% net ROI.
- **Outage Monitoring**: Monitor scheduled 345 kV transmission line maintenance across the West-to-East corridor during upcoming monthly RTO maintenance outages.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "SUBMIT_AUCTION_BIDS",
  "domain": "Wholesale_Trading",
  "market": "ISO/RTO Financial Transmission Rights (FTR) Monthly Auction",
  "details": {
    "target_paths": [
      {
        "source": "WEST_HUB",
        "sink": "LZ1_NORTH_SUB",
        "bid_volume_mw": 50,
        "bid_price_cap": 4.40,
        "term": "Prompt_Month_Peak"
      },
      {
        "source": "WEST_HUB",
        "sink": "LZ1_CENTRAL",
        "bid_volume_mw": 35,
        "bid_price_cap": 3.75,
        "term": "Prompt_Month_Peak"
      }
    ],
    "total_capital_commitment_limit": "$255,000",
    "approver_role": "Lead FTR Trader / Risk Manager"
  },
  "status": "AWAITING_HUMAN_APPROVAL"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Analyze historical transmission congestion rent and binding constraint hours on the West-Central 500kV transmission corridor."

**Agent Response:**
### Executive Summary
**Historical congestion analysis on the West-Central 500kV corridor indicates a marked escalation in thermal loading and binding frequency over the trailing 12-month period, driven primarily by high summer transfer flows and generation retirements in the import sink. Cumulative congestion rent reached $9.79M across 1,346 binding constraint hours, representing a 34.2% increase over the trailing multi-year baseline. This structural congestion profile elevates basis risk for unhedged load obligations and justifies an optimized Financial Transmission Right (FTR) / Congestion Revenue Right (CRR) acquisition strategy in upcoming seasonal auctions.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Trailing 12-Month Congestion Rent** | $9,787,000 | $7,290,000 | +34.2% | **Warning** |
| **Total Binding Hours (L12M)** | 1,346 hrs | 980 hrs | +37.3% | **Warning** |
| **Peak Hourly Shadow Price** | $142.80/MWh | $95.00/MWh | +50.3% | **Critical** |
| **Average Binding Shadow Price** | $28.45/MWh | $22.10/MWh | +28.7% | **Warning** |
| **Binding Frequency (% of Total Hours)** | 15.36% | 11.19% | +37.3% | **Warning** |
| **FTR Hedge PnL Efficiency (Historical)** | 88.4% | 92.0% | -3.9% | **Normal** |

---

### Visualization Trigger

**Recommended Visualization:** Dual-Axis Time-Series Line & Column Chart displaying Monthly Total Congestion Rent ($k) against Binding Constraint Hours over the trailing 12 months.

```json
{
  "chart_type": "line",
  "title": "West-Central 500kV Corridor: Monthly Congestion Rent vs Binding Hours (L12M)",
  "x_axis": {
    "label": "Month",
    "categories": ["M-12", "M-11", "M-10", "M-9", "M-8", "M-7", "M-6", "M-5", "M-4", "M-3", "M-2", "M-1"]
  },
  "y_axes": [
    {
      "name": "Congestion Rent ($k)",
      "opposite": false
    },
    {
      "name": "Binding Hours",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Congestion Rent ($k)",
      "type": "column",
      "y_axis_index": 0,
      "data": [412, 385, 520, 710, 890, 1240, 1580, 1420, 960, 680, 510, 475]
    },
    {
      "name": "Binding Hours",
      "type": "line",
      "y_axis_index": 1,
      "data": [48, 42, 65, 92, 124, 186, 235, 210, 140, 88, 62, 54]
    }
  ]
}
```

---

### Actionable Recommendations

- **Hedge Allocation Strategy**: Increase seasonal FTR/CRR hedge coverage from the current 65% to 85% of peak load exposure on the West-to-Central path for Q2 and Q3 to insulate against summer peak shadow price spikes.
- **Auction Bid Price Modeling**: Calibrate clearing price bid curves to account for the elevated $28.45/MWh average shadow price during peak hours, ensuring bid competitiveness without exceeding portfolio Value-at-Risk (VaR) limits.
- **Outage & Flowgate Sensitivity Monitoring**: Track transmission outage schedules on adjacent 345kV/500kV parallel paths (e.g., North-Central bypass loops), which correlate with 72% of the binding constraint events above $100/MWh shadow price.
- **Coordinated Shift-Factor Verification**: Validate generator shift factors (GSF) across portfolio assets to evaluate potential localized counter-flow hedging opportunities.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "FTR_AUCTION_BID_SUBMISSION",
  "corridor": "West-Central 500kV",
  "target_market_period": "Upcoming Seasonal FTR Auction",
  "proposed_hedge_mw": 250.0,
  "estimated_capital_commitment_usd": 1250000.00,
  "max_clearing_price_limit_usd_per_mw_month": 1680.00,
  "human_approval_required": true,
  "sign_off_roles": ["Wholesale Trading Desk Lead", "Risk Management Officer"]
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit bids for 75 MW of Peak FTR contracts on the North-to-South corridor in the upcoming monthly ISO auction."

**Agent Response:**
### 1. Executive Summary
**The Financial Transmission Right (FTR) bid package for 75 MW Peak contracts on the North-to-South corridor has been synthesized and risk-assessed against ISO auction parameters.** **Projected monthly congestion spreads demonstrate favorable risk-adjusted returns with Portfolio Value-at-Risk (VaR) remaining within authorized trading limits.** **Because bid submission constitutes a binding financial transaction in wholesale energy markets, formal Human-in-the-Loop (HITL) authorization is required prior to ISO market submission.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **FTR Contract Volume** | 75.00 MW | 75.00 MW | 0.00% | Normal |
| **Bid Price Cap** | $4.25 / MWh | $3.80 / MWh | +11.84% | Warning |
| **Historical Congestion Spread (DA)** | $5.10 / MWh | $4.65 / MWh | +9.68% | Normal |
| **Expected Net Congestion Revenue** | $342,000 | $300,000 | +14.00% | Normal |
| **Portfolio 95% VaR (Monthly)** | $185,400 | $250,000 | -25.84% | Normal |
| **Collateral Margin Requirement** | $159,375 | $200,000 | -20.31% | Normal |

---

### 3. Visualization Triggers

- **Recommended Visualization**: **Time-Series Line Chart** showing historical Day-Ahead North-to-South congestion spreads against the proposed FTR bid cap and break-even clearing levels.

```json
{
  "chart_type": "line",
  "title": "North-to-South Congestion Price Spread & Bid Threshold",
  "labels": ["Wk 1", "Wk 2", "Wk 3", "Wk 4", "Auction Bid Cap"],
  "datasets": [
    {
      "label": "Historical Congestion Spread ($/MWh)",
      "data": [4.10, 4.65, 4.80, 5.10, null]
    },
    {
      "label": "Bid Price Cap ($/MWh)",
      "data": [null, null, null, null, 4.25]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Confirm Collateral Availability**: Verify that the trading account's available credit facility covers the $159,375 margin requirement prior to the monthly auction clearing window.
- **Review Transmission Outage Schedules**: Re-verify scheduled line maintenance along the North-to-South 500kV interface to ensure expected congestion drivers remain intact.
- **Authorize Market Submission**: Provide explicit operator sign-off via the Tier 2 confirmation workflow below to post the bid curve into the ISO Market Clearing Engine.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "WHOLESALE_TRANSACTION_SUBMISSION",
  "domain": "Wholesale Trading",
  "market": "ISO Monthly FTR/CRR Auction",
  "contract_type": "Peak Financial Transmission Right (FTR)",
  "path": "North-to-South Corridor",
  "source_node": "ZONE_NORTH_HUB",
  "sink_node": "ZONE_SOUTH_HUB",
  "volume_mw": 75.00,
  "bid_price_cap_per_mwh": 4.25,
  "total_financial_exposure_cap": 159375.00,
  "requires_approval": true,
  "status": "AWAITING_HUMAN_CONFIRMATION"
}
```
