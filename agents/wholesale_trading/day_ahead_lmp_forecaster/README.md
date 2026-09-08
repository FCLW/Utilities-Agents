# ⚡ Day Ahead Lmp Forecaster

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of day ahead lmp forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Day Ahead Lmp Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank day ahead lmp forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.day_ahead_lmp_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the forecasted 24-hour Day-Ahead Locational Marginal Price (LMP) profile across all commercial trading hubs tomorrow?"

**Agent Response:**
### Executive Summary
**Day-Ahead Locational Marginal Prices (LMPs) for tomorrow's operating day are forecasted to exhibit a standard dual-peak load curve across all major commercial trading hubs, driven by morning ramp (HE07–HE08) and evening peak demand (HE18–HE20). The East Hub and South Hub show elevated peak pricing reaching $85.60/MWh and $79.80/MWh respectively during HE19 due to localized transmission binding constraints and elevated net load. Forecast accuracy across all hubs remains well within regulatory and operational thresholds, maintaining a 24-hour Mean Absolute Percentage Error (MAPE) of 3.42%.**

---

### Key Market Metrics & Hub Forecast Summary

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **System On-Peak Average LMP (HE07–HE22)** | $53.64/MWh | $48.50/MWh | +10.60% | Normal |
| **System Off-Peak Average LMP (HE01–06, 23–24)** | $28.18/MWh | $27.50/MWh | +2.47% | Normal |
| **System Peak Price (HE19 - East Hub)** | $85.60/MWh | $72.00/MWh | +18.89% | Warning |
| **System Minimum Price (HE04 - West Hub)** | $22.00/MWh | $21.50/MWh | +2.33% | Normal |
| **East-to-West Hub Peak Congestion Spread (HE19)** | $19.10/MWh | $12.00/MWh | +59.17% | Warning |
| **Forecast Model Accuracy (24h MAPE)** | 3.42% | < 5.00% | -31.60% | Normal |
| **95% Confidence Interval Band (System Avg)** | ±$4.15/MWh | ±$5.50/MWh | -24.55% | Normal |
| **Portfolio Value at Risk (VaR - 95% 1-Day)** | $142,500 | $250,000 | -43.00% | Normal |

---

### 24-Hour Forecast Profile by Trading Hub ($/MWh)

| Hour Ending (HE) | North Hub ($/MWh) | South Hub ($/MWh) | West Hub ($/MWh) | East Hub ($/MWh) | Congestion Component (Avg $/MWh) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **HE01** | $28.50 | $29.80 | $26.10 | $31.20 | $1.40 |
| **HE02** | $26.20 | $27.50 | $24.30 | $28.90 | $1.10 |
| **HE03** | $24.80 | $25.90 | $22.80 | $27.40 | $0.90 |
| **HE04 (Min)** | $23.90 | $25.10 | **$22.00** | $26.50 | $0.80 |
| **HE05** | $25.10 | $26.40 | $23.20 | $27.80 | $1.00 |
| **HE06** | $31.40 | $33.10 | $28.90 | $35.20 | $2.10 |
| **HE07** | $42.80 | $44.60 | $38.40 | $46.90 | $3.50 |
| **HE08 (Morning Peak)** | $48.50 | $51.20 | $43.70 | $53.80 | $4.20 |
| **HE09** | $45.20 | $47.80 | $40.50 | $50.10 | $3.80 |
| **HE10** | $41.00 | $43.50 | $36.80 | $45.80 | $3.20 |
| **HE11** | $38.50 | $40.90 | $33.90 | $43.10 | $2.90 |
| **HE12** | $37.20 | $39.40 | $32.50 | $41.70 | $2.70 |
| **HE13** | $36.80 | $39.10 | $31.80 | $41.30 | $2.60 |
| **HE14** | $38.10 | $40.60 | $33.00 | $42.90 | $2.80 |
| **HE15** | $42.50 | $45.30 | $37.20 | $48.00 | $3.40 |
| **HE16** | $49.30 | $52.80 | $44.10 | $56.20 | $4.60 |
| **HE17** | $58.70 | $63.10 | $52.60 | $67.40 | $6.10 |
| **HE18** | $68.40 | $73.50 | $61.20 | $78.90 | $7.80 |
| **HE19 (Evening Peak)**| **$74.20** | **$79.80** | **$66.50** | **$85.60** | **$9.40** |
| **HE20** | $69.80 | $75.10 | $62.30 | $80.70 | $8.20 |
| **HE21** | $56.40 | $60.50 | $50.10 | $64.90 | $5.30 |
| **HE22** | $44.10 | $47.30 | $39.60 | $50.80 | $3.70 |
| **HE23** | $35.80 | $38.20 | $32.40 | $40.70 | $2.30 |
| **HE24** | $30.20 | $32.10 | $27.90 | $34.50 | $1.60 |

---

### Visualization Trigger: Multi-Hub Hourly LMP Curve

```json
{
  "chart_type": "line",
  "title": "24-Hour Day-Ahead Forecasted LMP Profile by Commercial Trading Hub ($/MWh)",
  "xAxis": {
    "title": "Hour Ending (HE)",
    "categories": ["HE01","HE02","HE03","HE04","HE05","HE06","HE07","HE08","HE09","HE10","HE11","HE12","HE13","HE14","HE15","HE16","HE17","HE18","HE19","HE20","HE21","HE22","HE23","HE24"]
  },
  "yAxis": {
    "title": "LMP ($/MWh)"
  },
  "series": [
    {
      "name": "North Hub",
      "data": [28.50, 26.20, 24.80, 23.90, 25.10, 31.40, 42.80, 48.50, 45.20, 41.00, 38.50, 37.20, 36.80, 38.10, 42.50, 49.30, 58.70, 68.40, 74.20, 69.80, 56.40, 44.10, 35.80, 30.20]
    },
    {
      "name": "South Hub",
      "data": [29.80, 27.50, 25.90, 25.10, 26.40, 33.10, 44.60, 51.20, 47.80, 43.50, 40.90, 39.40, 39.10, 40.60, 45.30, 52.80, 63.10, 73.50, 79.80, 75.10, 60.50, 47.30, 38.20, 32.10]
    },
    {
      "name": "West Hub",
      "data": [26.10, 24.30, 22.80, 22.00, 23.20, 28.90, 38.40, 43.70, 40.50, 36.80, 33.90, 32.50, 31.80, 33.00, 37.20, 44.10, 52.60, 61.20, 66.50, 62.30, 50.10, 39.60, 32.40, 27.90]
    },
    {
      "name": "East Hub",
      "data": [31.20, 28.90, 27.40, 26.50, 27.80, 35.20, 46.90, 53.80, 50.10, 45.80, 43.10, 41.70, 41.30, 42.90, 48.00, 56.20, 67.40, 78.90, 85.60, 80.70, 64.90, 50.80, 40.70, 34.50]
    }
  ]
}
```

---

### Actionable Recommendations

- **Thermal & Storage Asset Bidding Strategy**: Target dispatch of flexible peaker units and battery energy storage system (BESS) discharges during HE18–HE20 to capture the premium evening spread ($66.50 to $85.60/MWh).
- **Virtual Bid / Congestion Hedging**: Implement East-West Financial Transmission Rights (FTR) or Virtual Spread Bids to hedge the forecasted $19.10/MWh congestion delta across the eastern corridor during HE18–HE20.
- **BESS Charging Optimization**: Schedule storage charging cycles during the lowest marginal cost window between HE02 and HE05 ($22.00–$25.10/MWh) to maximize round-trip arbitrage efficiency.
- **Portfolio Risk Monitoring**: Maintain active surveillance on ambient temperature updates for tomorrow afternoon; if peak thermal forecasts shift by >2°F, re-run intraday LMP sensitivity.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze generation supply stack bids, forecasted regional load, and planned transmission outages driving day-ahead clearing prices."

**Agent Response:**
### Executive Summary
**Day-Ahead Locational Marginal Prices (LMP) are projected to peak at \$114.20/MWh during Hour Ending (HE) 18 due to a combined 51.2 GW regional peak load and a critical 345 kV transmission outage on the West-to-East corridor. Generation supply stack bids indicate marginal gas peakers (Heat Rate $\ge 11,200\text{ Btu/kWh}$) will clear between HE 16 and HE 20, driving an estimated 38.4% congestion cost premium in eastern delivery nodes. The overall 24-hour forecast model maintains a backtested Mean Absolute Percentage Error (MAPE) of 3.82% within a 95% Confidence Interval.**

---

### Data Presentation: Market Drivers & LMP Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Forecasted Load (HE 18)** | 51,200 MW | 44,500 MW | +15.06% | **Warning** |
| **Average Day-Ahead LMP** | \$53.86/MWh | \$42.10/MWh | +27.93% | **Warning** |
| **Peak LMP (HE 18, East Hub)** | \$114.20/MWh | \$68.50/MWh | +66.72% | **Critical** |
| **Marginal Congestion Component (MCC)** | \$38.60/MWh | \$6.20/MWh | +522.58% | **Critical** |
| **Marginal Loss Component (MLC)** | \$2.80/MWh | \$1.90/MWh | +47.37% | **Normal** |
| **Available Economic Generation (Stack)** | 54,800 MW | 58,200 MW | -5.84% | **Warning** |
| **Reserve Margin at Peak** | 7.03% | 12.00% | -41.42% | **Critical** |
| **Model Forecast Error (MAPE)** | 3.82% | < 5.00% | -23.60% | **Normal** |
| **Portfolio Value at Risk (VaR - 95%)** | \$1.42M | \$1.10M | +29.09% | **Warning** |

---

### Key Analytical Drivers

1. **Supply Stack Dynamics**:
   - **Base Load & Renewables**: Solar generation ramps down from 6,800 MW at HE 15 to <200 MW by HE 19.
   - **Marginal Clearing**: Sub-economic Combined Cycle Gas Turbines (CCGT) and Simple Cycle Peakers (\$75–\$110/MWh offer tranches) set the marginal energy price across HE 17–HE 20.

2. **Transmission Outages & Congestion**:
   - **Outage**: Planned outage on the 345 kV Line *Substation Alpha – Substation Delta* limits East-to-West transfer capacity by 1,450 MW.
   - **Binding Constraint**: Thermal ratings on parallel 230 kV interfaces trigger shadow prices exceeding \$210/MW, sharply diverging eastern nodal prices from western generation pockets.

---

### Visualization Configuration

- **Chart Type**: Time-Series Line & Area Composite Chart
- **Data Series Definition**:

```json
{
  "chart_type": "line",
  "title": "Day-Ahead Hourly LMP Forecast vs. Regional Net Load",
  "x_axis": {
    "label": "Hour Ending (HE)",
    "intervals": ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16","17","18","19","20","21","22","23","24"]
  },
  "series": [
    {
      "name": "Forecasted LMP ($/MWh)",
      "data": [32.4, 30.1, 28.5, 27.8, 29.2, 36.5, 48.2, 62.8, 58.4, 52.1, 49.3, 47.8, 46.2, 48.5, 54.1, 68.9, 89.4, 114.2, 98.7, 76.5, 61.2, 49.8, 41.3, 35.0]
    },
    {
      "name": "Forecasted Load (GW)",
      "data": [24.1, 22.8, 21.9, 21.4, 22.0, 25.6, 31.2, 36.8, 38.2, 39.1, 39.8, 40.2, 40.9, 41.8, 43.2, 46.5, 49.8, 51.2, 48.6, 44.1, 40.2, 35.4, 30.1, 26.5]
    }
  ]
}
```

---

### Actionable Recommendations

- **Energy Offer Adjustments**: Re-parameterize offer curves for fast-start peaking units in Zone East to clear in the Day-Ahead Market ahead of the 10:30 AM market gate closure.
- **Congestion Revenue Rights (CRR) / FTR Allocation**: Execute hedge overlays on the East-West transfer path to offset projected \$38.60/MWh Congestion Component exposure.
- **Demand Response Dispatch**: Pre-schedule Tier-1 commercial demand-response blocks for HE 17–HE 19 to mitigate spot real-time market price exposure.

---

### Human-In-The-Loop Confirmation

```yaml
[TIER 2 ACTION REQUIRED]
Action: Wholesale Market Day-Ahead Generation Bidding & Hedging Repositioning
Target Nodes: East Hub / Zone-3 Delivery Nodes
Parameters:
  - Thermal Peaker Fleet Dispatch Commitment: 650 MW (HE 17 - HE 20)
  - Financial Congestion Hedge Block: $450,000 Notional
  - Market Gate Closure: 10:30 AM EPT
Required Authorization: Wholesale Trading Floor Risk Manager / Generation Operations Lead
Impact: Prevents spot real-time market exposure and mitigates projected $1.42M Value at Risk (VaR).
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Commit day-ahead hourly price forecasts to the wholesale trading desk portfolio optimization engine."

**Agent Response:**
### Executive Summary
**The 24-hour day-ahead Locational Marginal Pricing (LMP) forecast for the upcoming operating day has been generated, validated, and staged for commitment to the wholesale trading desk portfolio optimization engine.** **The predictive model achieved an aggregate Mean Absolute Percentage Error (MAPE) of 3.42%, well within the strict < 5.0% accuracy threshold, with peak pricing projected at $92.50/MWh during Hour Ending (HE) 18.** **Because committing these price curves directly impacts day-ahead bidding, dispatch scheduling, and portfolio Value at Risk (VaR), human-in-the-loop authorization is required prior to production engine ingestion.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Model Forecast Accuracy (MAPE)** | 3.42% | < 5.00% | -31.60% | Normal |
| **Peak LMP Forecast (HE 18)** | $92.50 / MWh | $88.00 / MWh | +5.11% | Normal |
| **Off-Peak LMP Average (HE 01–06, 23–24)** | $31.46 / MWh | $30.25 / MWh | +4.00% | Normal |
| **On-Peak LMP Average (HE 07–22)** | $60.79 / MWh | $57.97 / MWh | +4.86% | Normal |
| **95% Confidence Interval Band** | ± 4.98% ($4.61/MWh) | ± 6.50% | -23.38% | Normal |
| **Portfolio 1-Day VaR (95% Conf.)** | $248,500 | $275,000 | -9.64% | Normal |
| **Projected Portfolio P&L Impact** | +$112,400 (Unrealized) | +$95,000 (Target) | +18.32% | Normal |

---

### Visualization Trigger

**Recommended Visualization**: Time-Series Line Chart (24-Hour Day-Ahead LMP Forecast with 95% Confidence Interval Upper/Lower Bands vs. Historical Baseline).

```json
{
  "chart_type": "line",
  "title": "Day-Ahead Hourly LMP Forecast vs Baseline ($/MWh)",
  "xAxis": {
    "label": "Hour Ending (HE)",
    "categories": ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24"]
  },
  "yAxis": {
    "label": "Price ($/MWh)"
  },
  "series": [
    {
      "name": "LMP Forecast ($/MWh)",
      "data": [32.4, 30.1, 28.5, 27.8, 29.2, 35.6, 48.2, 62.5, 58.0, 52.3, 49.8, 47.5, 46.2, 48.0, 54.1, 68.7, 84.3, 92.5, 86.0, 71.4, 58.2, 49.0, 41.2, 34.5]
    },
    {
      "name": "Baseline ($/MWh)",
      "data": [31.0, 29.0, 27.5, 27.0, 28.5, 34.0, 46.0, 60.0, 55.5, 50.0, 48.0, 46.0, 45.0, 46.5, 52.0, 65.0, 80.0, 88.0, 82.5, 68.0, 56.0, 47.5, 40.0, 33.0]
    },
    {
      "name": "95% Upper Bound",
      "data": [34.0, 31.6, 29.9, 29.2, 30.7, 37.4, 50.6, 65.6, 60.9, 54.9, 52.3, 49.9, 48.5, 50.4, 56.8, 72.1, 88.5, 97.1, 90.3, 75.0, 61.1, 51.5, 43.3, 36.2]
    },
    {
      "name": "95% Lower Bound",
      "data": [30.8, 28.6, 27.1, 26.4, 27.7, 33.8, 45.8, 59.4, 55.1, 49.7, 47.3, 45.1, 43.9, 45.6, 51.4, 65.3, 80.1, 87.9, 81.7, 67.8, 55.3, 46.5, 39.1, 32.8]
    }
  ]
}
```

---

### Actionable Recommendations

- **Review Peak Hour Spreads**: Note the elevated evening ramp between HE 17 and HE 19 ($84.30–$92.50/MWh); evaluate virtual bidding and flexible generation commitment schedules.
- **Execute Human Confirmation**: Review the staged dataset and approve the Tier 2 commitment payload below to release the price curves to the portfolio optimization engine.
- **Downstream Dispatch Alignment**: Once committed, notify the Generation Asset Bidding agent to re-optimize thermal and battery storage dispatch profiles against the updated price vector.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "COMMIT_PORTFOLIO_OPTIMIZATION_PRICE_CURVE",
  "target_system": "Wholesale Trading Desk Portfolio Optimization Engine",
  "execution_payload": {
    "market_run": "DAY_AHEAD",
    "delivery_date": "CURRENT_DATE + 1",
    "forecast_model_version": "LMP-DA-v4.2.1",
    "intervals_committed": 24,
    "mape_validation": 0.0342,
    "max_lmp": 92.50,
    "min_lmp": 27.80,
    "var_exposure_limit_usd": 275000,
    "status": "PENDING_OPERATOR_APPROVAL"
  },
  "impact_scope": "Initiates automated day-ahead wholesale market bid curves and co-optimized asset commitment schedules across the generation fleet.",
  "required_approver": "Lead Market Trader / Portfolio Risk Manager"
}
```
