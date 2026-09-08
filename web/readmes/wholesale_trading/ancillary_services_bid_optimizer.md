# ⚡ Ancillary Services Bid Optimizer

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of ancillary services bid optimizer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Ancillary Services Bid Optimizer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank ancillary services bid optimizer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.ancillary_services_bid_optimizer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How should we allocate our 100 MW flexible gas turbine capacity between Regulation Up, Spinning Reserve, and Day-Ahead Energy?"

**Agent Response:**
### Executive Summary
**Optimal allocation of the 100 MW flexible gas turbine between Day-Ahead (DA) Energy, Regulation Up (Reg-Up), and Spinning Reserve requires a dynamic co-optimization model driven by the spread between Locational Marginal Prices (LMP) and Ancillary Service Market Clearing Prices (MCP). Because flexible gas turbines possess high ramp rates ($>10\text{ MW/min}$) and fast start capabilities, maximizing margin requires allocating upper capacity headroom to high-value Reg-Up and Spinning Reserve during tight regulation hours, while committing base capacity to DA Energy when spark spreads exceed ancillary opportunity costs. Operating at $P_{min}$ (e.g., 40 MW) base energy with 30 MW Reg-Up and 30 MW Spinning Reserve yields the highest risk-adjusted net margin during volatile grid intervals.**

---

### 1. Capacity Allocation Framework & Physical Constraints

To co-optimize the 100 MW asset without violating physical operating parameters or NERC/ISO market rules:

$$\max \Pi = (LMP - \text{Marginal Cost}) \cdot P_{\text{DA}} + MCP_{\text{RegUp}} \cdot C_{\text{RegUp}} + MCP_{\text{Spin}} \cdot C_{\text{Spin}} - \text{Mileage Degradation Cost}$$

$$\text{Subject to:}$$
$$P_{\text{DA}} + C_{\text{RegUp}} + C_{\text{Spin}} \le 100\text{ MW } (P_{\max})$$
$$P_{\text{DA}} - C_{\text{RegDown}} \ge P_{\min} \quad (\approx 40\text{ MW if online})$$
$$C_{\text{RegUp}} \le \text{Ramp Rate} \times 5\text{ min} \quad (\le 50\text{ MW at } 10\text{ MW/min})$$
$$C_{\text{Spin}} \le \text{Ramp Rate} \times 10\text{ min} \quad (\le 100\text{ MW at } 10\text{ MW/min})$$

---

### 2. Market Metric Benchmarks & Optimization Performance

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Qualified Capacity** | 100.0 MW | 100.0 MW | 0.0% | **Normal** |
| **Max 5-Min Reg-Up Capability** | 50.0 MW | 50.0 MW | 0.0% | **Normal** |
| **Max 10-Min Spin Capability** | 100.0 MW | 100.0 MW | 0.0% | **Normal** |
| **Reg-Up / DA Energy Price Ratio** | 1.38 | 0.85 | +62.4% | **Warning** |
| **Spinning / DA Energy Price Ratio**| 0.72 | 0.45 | +60.0% | **Normal** |
| **Expected Net Margin ($/hr)** | $4,850.00 | $3,620.00 | +34.0% | **Normal** |
| **Heat Rate Degradation Penalty** | $185.00/hr | $150.00/hr | +23.3% | **Normal** |

---

### 3. Recommended Allocation Matrix by Market Regime

1. **High Renewable Ramp / Morning & Evening Duck Curve (Recommended Base Case)**:
   * **DA Energy Commitment**: 40 MW (Set at $P_{\min}$ to maintain online status).
   * **Regulation Up Bid**: 30 MW (Captures elevated 5-minute regulation mileage clearing prices).
   * **Spinning Reserve Bid**: 30 MW (Synchronized headroom monetized with zero incremental fuel burn).
   * *Net Headroom Utilization*: 100% (40 MW Energy + 30 MW RegUp + 30 MW Spin = 100 MW).

2. **Scarcity / High LMP Events ($LMP > \text{Heat Rate} \times \text{Fuel} + \$80/\text{MWh}$)**:
   * **DA Energy Commitment**: 75 MW.
   * **Regulation Up Bid**: 0 MW (Avoid de-rating base generation during price spikes).
   * **Spinning Reserve Bid**: 25 MW (Top 25 MW headroom delivered as contingency spin).

3. **Low LMP / High Regulation Value Regimes ($MCP_{\text{RegUp}} > LMP - \text{MC}$)**:
   * **DA Energy Commitment**: 40 MW ($P_{\min}$).
   * **Regulation Up Bid**: 50 MW (Ramp-limited maximum 5-minute capacity).
   * **Spinning Reserve Bid**: 10 MW.

---

### 4. Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Optimal 100 MW Capacity Allocation by Market Price Regime",
  "categories": [
    "Off-Peak / Low LMP",
    "Mid-Day / Solar Ramp",
    "Peak Hours / High LMP",
    "Grid Stress / High AS Premium"
  ],
  "series": [
    {
      "name": "Day-Ahead Energy (MW)",
      "data": [0, 40, 75, 45]
    },
    {
      "name": "Regulation Up (MW)",
      "data": [25, 30, 0, 35]
    },
    {
      "name": "Spinning Reserve (MW)",
      "data": [0, 30, 25, 20]
    },
    {
      "name": "Uncommitted / Headroom (MW)",
      "data": [75, 0, 0, 0]
    }
  ]
}
```

---

### 5. Actionable Recommendations

* **Submit Multi-Part Bid Curves**: Submit three-part bids for the Day-Ahead market specifying incremental energy curves above $P_{\min}$ (40 MW) and separate capacity offers for Reg-Up ($30 MW) and Spin ($30 MW).
* **Incorporate Regulation Mileage Cost**: Include a wear-and-tear / equipment degradation adder ($\approx \$2.50-\$4.00/\text{MW}$ of mileage) on the AGC Regulation Up offer curve to protect turbine hot-gas components from thermal cycling.
* **Enable Telemetry for Fast Response**: Ensure Automated Generation Control (AGC) tracking and 4-second DNP3/ICCP telemetry links to the ISO Balancing Authority are validated prior to operating hour submittal.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "WHOLESALE_MARKET_BID_SUBMISSION",
  "asset_id": "GT-100-UNIT1",
  "market": "DAY_AHEAD_CO_OPTIMIZED_AS",
  "bid_structure": {
    "da_energy_mw": 40.0,
    "reg_up_capacity_mw": 30.0,
    "spinning_reserve_mw": 30.0,
    "total_committed_mw": 100.0,
    "bid_period_utc": "2025-03-31T00:00:00Z_TO_2025-03-31T23:59:59Z"
  },
  "estimated_revenue_impact": "$116,400.00/day",
  "requires_human_approval": true,
  "approval_role": "Lead Real-Time / Day-Ahead Power Trader"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Analyze historical ancillary service clearing prices (ASCP) and ISO mileage multipliers across peak summer operating days."

**Agent Response:**
### Executive Summary
**Analysis of historical summer peak operating days indicates that Ancillary Service Clearing Prices (ASCP) for Regulation Up and Spinning Reserves experienced sharp premiums of up to +185.5% and +149.2% above baseline during net load ramping intervals (17:00–21:00 HE). Concurrently, ISO Regulation Mileage Multipliers increased from a seasonal baseline of 2.80 to a peak of 5.20, significantly amplifying performance-adjusted revenue capture for fast-responding battery energy storage system (BESS) and flexible thermal assets. Co-optimizing bid curves to capitalize on mileage premiums while hedging against Lost Opportunity Cost (LOC) during energy price spikes is essential to maximize net portfolio margin.**

---

### Data Presentation

The table below summarizes historical clearing metrics, mileage multipliers, and dispatch performance across peak summer operating conditions (June–August, HE 16–21):

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Regulation Up ASCP (Peak HE 18-20)** | $114.20 / MWh | $40.00 / MWh | +185.5% | Critical |
| **Regulation Down ASCP (Peak HE 12-15)** | $38.40 / MWh | $18.50 / MWh | +107.6% | Warning |
| **Spinning Reserve ASCP (Peak HE 18-21)** | $62.30 / MWh | $25.00 / MWh | +149.2% | Critical |
| **Non-Spinning Reserve ASCP** | $28.50 / MWh | $14.00 / MWh | +103.6% | Warning |
| **ISO Regulation Mileage Multiplier (Reg-Up)** | 5.20 ratio | 2.80 ratio | +85.7% | Critical |
| **Lost Opportunity Cost (LOC) Offset** | $32.80 / MWh | $12.00 / MWh | +173.3% | Warning |
| **Asset Response Accuracy Score (BESS / Gas Peaker)** | 98.4% | 95.0% | +3.6% | Normal |

---

### Visualization Triggers

A dual-axis **Time-Series Line Chart** is recommended to evaluate the co-movement between product clearing prices and the ISO mileage multiplier across summer peak operating windows.

```json
{
  "chart_type": "line",
  "title": "Summer Peak Ancillary Service Clearing Prices (ASCP) & Regulation Mileage Multipliers",
  "xAxis": {
    "categories": ["Jun Peak", "Jul Mid-Peak", "Jul Super-Peak", "Aug Super-Peak", "Aug Late-Summer"],
    "title": "Operating Timeframe"
  },
  "yAxis": [
    {
      "title": "Clearing Price ($/MWh)",
      "opposite": false
    },
    {
      "title": "Mileage Multiplier (Ratio)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Regulation Up ASCP ($/MWh)",
      "type": "line",
      "yAxis": 0,
      "data": [24.50, 42.10, 88.75, 114.20, 31.80]
    },
    {
      "name": "Spinning Reserve ASCP ($/MWh)",
      "type": "line",
      "yAxis": 0,
      "data": [12.20, 19.80, 46.50, 62.30, 16.40]
    },
    {
      "name": "Non-Spinning Reserve ASCP ($/MWh)",
      "type": "line",
      "yAxis": 0,
      "data": [6.10, 9.40, 21.00, 28.50, 7.90]
    },
    {
      "name": "Reg Mileage Multiplier",
      "type": "spline",
      "yAxis": 1,
      "data": [2.85, 3.40, 4.85, 5.20, 3.10]
    }
  ]
}
```

---

### Actionable Recommendations

- **Shift Asset Allocation in Day-Ahead Market (DAM)**: Allocate high-ramp-rate BESS capacity preferentially to Regulation Up and Regulation Mileage products during HE 17–21, capturing high performance-cleared multipliers (>4.8x).
- **Dynamic Offer Curve Adjustments**: Adjust spinning reserve offer price floors from $15.00/MWh to $45.00/MWh during heat-wave alerts to hedge against thermal trip risks and uncompensated real-time energy opportunity costs.
- **Mileage Degradation Monitoring**: Incorporate battery cell throughput cost ($/MWh equivalent cycle degradation) into the real-time regulation mileage bid price to prevent sub-economic asset wear during extreme mileage multiplier dispatch (>5.0).
- **Automated Opportunity Cost Recalibration**: Update real-time co-optimization algorithms to dynamically track the spread between Energy Locational Marginal Price (LMP) and ASCP + Mileage Settlement to prevent negative net cashflow during super-peak intervals.

---

### [TIER 2 ACTION REQUIRED]

Execution of wholesale market bid curve parameter modifications requires Human-In-The-Loop (HITL) authorization before automated submission to the ISO Market Scheduling System:

```json
{
  "action_type": "MARKET_BID_CURVE_UPDATE",
  "market_domain": "Wholesale Trading",
  "submitting_agent": "ancillary_services_bid_optimizer",
  "market_target": "ISO Day-Ahead & Real-Time Ancillary Services",
  "proposed_parameters": {
    "product_allocation": {
      "regulation_up_capacity_mw": 125.0,
      "regulation_down_capacity_mw": 50.0,
      "spinning_reserve_mw": 75.0,
      "non_spinning_reserve_mw": 30.0
    },
    "mileage_bid_adder_usd_mwh": 4.50,
    "peak_window_he": "16-21",
    "effective_operating_date": "2024-07-15"
  },
  "financial_exposure_limit_usd": 250000.00,
  "requires_approval": true,
  "approver_role": "Lead Real-Time Trader / Market Operations Lead"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit co-optimized Ancillary Services and Energy bids for Unit 1 into the ISO Day-Ahead Market before the 10:00 AM gate closure."

**Agent Response:**
### Executive Summary
**The Day-Ahead co-optimization model for Unit 1 (250 MW Net Dependable Capacity) has formulated the optimal energy and ancillary service bid stack ahead of the 10:00 AM ISO gate closure. Expected gross margin is maximized at $142,650 across all 24 market intervals by allocating 160–180 MW to Day-Ahead Energy during peak hours while reserving 50–70 MW for Regulation Up/Down and Spinning Reserves. In accordance with safety guardrails, physical submittal of financial market bids constitutes a Tier 2 action requiring Human-in-the-Loop (HITL) authorization prior to API dispatch.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Cleared Energy Capacity** | 180.0 MW | 175.0 MW | +2.86% | Normal |
| **Regulation Up/Down Offer** | 25.0 MW | 20.0 MW | +25.00% | Normal |
| **Spinning Reserve Offer** | 35.0 MW | 30.0 MW | +16.67% | Normal |
| **Supplemental / Non-Spin Offer** | 20.0 MW | 25.0 MW | -20.00% | Normal |
| **Forecasted Energy LMP (Peak Avg)** | $58.40/MWh | $52.10/MWh | +12.09% | Normal |
| **Forecasted Reg Up MCP (Peak Avg)** | $24.75/MW-h | $22.00/MW-h | +12.50% | Normal |
| **Forecasted Spin MCP (Peak Avg)** | $16.10/MW-h | $14.50/MW-h | +11.03% | Normal |
| **Total Expected DA Margin** | $142,650 | $128,500 | +11.01% | Normal |
| **Gate Closure Proximity** | 38 minutes remaining | 60 minutes target | -36.67% | Warning |

---

### Visualization Triggers

- **Recommended Chart Type**: Stacked Bar Chart (`DA Co-Optimized Capacity Allocation by Operating Period`)
- **JSON Configuration**:
```json
{
  "chart_type": "stacked_bar",
  "title": "Day-Ahead Co-Optimized Bid Allocation (Unit 1 - 250 MW Capacity)",
  "intervals": ["HE01-06 (Off-Peak)", "HE07-10 (Morning Ramp)", "HE11-18 (Peak)", "HE19-22 (Evening Peak)", "HE23-24 (Off-Peak)"],
  "series": [
    {
      "name": "Energy (MW)",
      "data": [100, 160, 180, 170, 100]
    },
    {
      "name": "Reg Up / Down (MW)",
      "data": [25, 25, 20, 20, 25]
    },
    {
      "name": "Spinning Reserve (MW)",
      "data": [35, 35, 30, 30, 35]
    },
    {
      "name": "Supplemental / Non-Spin (MW)",
      "data": [20, 10, 0, 10, 20]
    }
  ]
}
```

---

### Actionable Recommendations
- **Verify Unit Operating Limits**: Confirm Unit 1 ramp rate ($5\text{ MW/min}$) and current telemetry availability before locking in Regulation parameters.
- **Review Opportunity Cost Curves**: Validate that AS bid curves account for lost opportunity cost (LOC) during HE14–HE18 when nodal LMP is projected above $\$62/\text{MWh}$.
- **Approve Tier 2 Execution**: Provide explicit authorization on the payload block below to allow the bid dispatch API to submit files directly to the ISO Market Participant portal before the 10:00 AM cutoff.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "MARKET_BID_SUBMISSION",
  "market": "ISO_DAY_AHEAD_MARKET",
  "operating_day": "TOMORROW",
  "gate_closure": "10:00:00 EST",
  "asset_id": "UNIT_1",
  "bid_parameters": {
    "total_capacity_mw": 250.0,
    "max_energy_mw": 180.0,
    "regulation_up_mw": 25.0,
    "regulation_down_mw": 25.0,
    "spinning_reserve_mw": 35.0,
    "supplemental_reserve_mw": 20.0,
    "bid_curve_type": "CO_OPTIMIZED_PIECEWISE_LINEAR"
  },
  "estimated_financial_commitment": "$142,650 Gross Margin",
  "status": "PENDING_OPERATOR_APPROVAL"
}
```
*To authorize this market bid submission, please confirm the dispatch payload above.*
