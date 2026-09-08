# ⚡ Real Time Lmp Tracker

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of real time lmp tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Real Time Lmp Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank real time lmp tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.real_time_lmp_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Why did the real-time five-minute LMP spike to $1,800/MWh at Substation Node 402 during the last dispatch interval?"

**Agent Response:**
### Executive Summary
**The real-time five-minute Locational Marginal Price (LMP) at Substation Node 402 escalated to $1,800.00/MWh during the most recent dispatch interval due to severe transmission branch thermal overloading and the activation of a transmission constraint penalty factor. Marginal Congestion Component (MCC) accounted for $1,582.50/MWh (87.9%) of the total price due to an N-1 contingency trip on the 230kV tie-line feeding the local load pocket, exhausting local fast-start ramping capability.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total LMP** | $1,800.00/MWh | $45.00/MWh | +3,900.0% | **Critical** |
| **Marginal Energy Component (MEC)** | $210.00/MWh | $38.50/MWh | +445.5% | **Warning** |
| **Marginal Congestion Component (MCC)** | $1,582.50/MWh | $4.80/MWh | +32,868.8% | **Critical** |
| **Marginal Loss Component (MLC)** | $7.50/MWh | $1.70/MWh | +341.2% | **Warning** |
| **Branch Line 402-A Loading** | 104.8% (MVA) | < 90.0% | +16.4% | **Critical** |
| **Local Fast-Start Ramp Available** | 0.0 MW | 45.0 MW | -100.0% | **Critical** |
| **Intra-Hour Value at Risk (VaR 95%)** | $142,500 | $15,000 | +850.0% | **Critical** |

---

### Root Cause Decomposition

1. **N-1 Contingency & Transmission Congestion**: 
   - The primary driver was a forced outage on the parallel 230kV corridor, shifting 185 MW of power flow onto the 115kV Substation Node 402 supply line.
   - The line reached 104.8% of its STE (Short-Term Emergency) thermal rating, triggering the security-constrained economic dispatch (SCED) transmission shadow price limit / relaxation penalty parameter ($1,500+/MWh).
2. **Local Ramp Scarcity**:
   - Downstream generation within the load pocket was fully ramp-constrained and unable to provide incremental sub-5-minute relief.
   - Marginal dispatch required clearing peaker units and activating demand-side emergency response tiers.

---

### Visualization

```json
{
  "chart_type": "line",
  "title": "Real-Time 5-Minute LMP Decomposition - Substation Node 402",
  "xAxis": "Interval",
  "yAxis": "$/MWh",
  "series": [
    {"name": "Total LMP", "data": [42.50, 45.10, 52.80, 68.20, 1800.00]},
    {"name": "Marginal Energy Component (MEC)", "data": [38.00, 40.20, 44.50, 55.00, 210.00]},
    {"name": "Marginal Congestion Component (MCC)", "data": [3.20, 3.50, 6.80, 11.40, 1582.50]},
    {"name": "Marginal Loss Component (MLC)", "data": [1.30, 1.40, 1.50, 1.80, 7.50]}
  ],
  "categories": ["T-20m", "T-15m", "T-10m", "T-5m", "Current (T-0)"]
}
```

---

### Actionable Recommendations

- **Desk Real-Time Hedge Optimization**: Evaluate virtual/financial trade unwinds or real-time swap rebalancing on unhedged load exposure at Node 402 to mitigate intra-hour spot settlement liability.
- **Demand Response / BESS Dispatch Evaluation**: Review battery storage dispatch schedules (BESS Unit 12) at the adjacent bus to provide counter-flow congestion relief.
- **Coordination with Transmission Operations**: Monitor the ISO/RTO re-dispatch directives and transmission switching validation to verify when the thermal overload constraint is expected to unbind.

---

### Human-in-the-Loop Confirmation Required

**[TIER 2 ACTION REQUIRED]**
* **Action Description**: Execute financial real-time physical-hedge position adjustment (> $100,000 VaR threshold) and initiate BESS counter-congestion discharge request for Node 402.
* **Impacted Assets / Portfolios**: Substation Node 402 Wholesale Settlement Account & BESS Unit 12.
* **Financial Exposure**: Estimated $142,500 VaR over the next 3 dispatch intervals.
* **Required Approval**: Wholesale Trading Desk Operator / Shift Manager sign-off before submission to ISO/RTO dispatch interface.

### Example 2: Trend & Comparative Analysis
**User:** "Correlate transmission line thermal overloads, generator ramp rate limitations, and real-time dispatch (RTD) ex-post price corrections."

**Agent Response:**
### Executive Summary
**Thermal overloads on critical transmission corridors force Real-Time Dispatch (RTD) optimization engines to exhaust fast-ramping localized units, triggering ramp-rate constraints that decouple nodal marginal costs from system-wide energy pricing.** **When ramping shortages cause temporary infeasibilities or unphysical shadow price spikes in the ex-ante RTD run, ISO/RTO market monitors enact ex-post price corrections to recalculate LMPs based on relaxed transmission penalties or verified physical unit capability.** **This structural divergence creates settlement variance between physical telemetry, five-minute dispatch instructions, and final settled nodal prices.**

---

### Mechanics of Correlation

```
Transmission Thermal Overload (>100% MVA Rating)
   │
   ▼
Localized Counter-Flow Dispatch Required
   │
   ▼
Generator Ramp Rate Saturation (MW/min Limit Hit)
   │
   ▼
RTD Infeasibility / Scarcity Penalty Shadow Pricing ($1,000–$2,000/MWh)
   │
   ▼
Ex-Post Tariff Screening / Price Correction (Relaxation to Physical Incremental Cost)
```

1. **Thermal Line Overload & Shadow Price Dynamics**: As power flows exceed the Normal/Emergency MVA ratings of a transmission element, the Security Constrained Economic Dispatch (SCED/RTD) algorithm applies a Lagrange multiplier ($\lambda_{flow}$) to re-dispatch generation. If local effective generation is limited, the congestion component ($LMP_{cong}$) escalates non-linearly.
2. **Ramp-Rate Binding**: Fast-ramping generation becomes constrained by physical ramp limits ($\Delta MW / \Delta t$). When the marginal unit cannot ramp fast enough to relieve the transmission constraint within the 5-minute dispatch interval, the optimization hits a mathematical constraint infeasibility, imposing an administrative power balance or transmission penalty factor.
3. **Ex-Post Price Correction**: ISO/RTO market software recalculates settlement LMPs post-interval if the price spike was driven by mathematical infeasibility, transient software anomalies, or modeling artifacts rather than a true physical capacity deficit. The ex-post run recalculates LMPs with constraint relaxation parameters, resulting in substantial downward price adjustments relative to real-time ex-ante indications.

---

### Quantitative Correlation Matrix

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Monitored Branch Thermal Loading** | 107.8% MVA | $\le 100.0\%$ MVA | +7.80% | **Critical** |
| **Ramp-Constrained Capacity** | 510.0 MW | $\le 150.0$ MW | +240.00% | **Critical** |
| **RTD Ex-Ante Peak LMP** | $920.00 / MWh | $45.00 / MWh | +1,944.44% | **Critical** |
| **Ex-Post Corrected LMP** | $245.00 / MWh | $45.00 / MWh | +444.44% | **Warning** |
| **Pricing Run Correction Delta (Ex-Ante vs. Ex-Post)** | -$675.00 / MWh | $0.00 / MWh | -73.37% | **Warning** |
| **Congestion Shadow Price ($\lambda_{branch}$)** | $1,420.00 / MW | $0.00 / MW | N/A | **Critical** |

---

### Visualization Triggers

A multi-axis **Time-Series Line Chart** is recommended to track the real-time interaction between thermal line loading percentage, ramp-constrained capacity, ex-ante LMP, and ex-post corrected settlement LMP.

```json
{
  "chart_type": "line",
  "title": "Thermal Overload vs. Ramp Saturation and LMP Ex-Post Corrections",
  "data": {
    "intervals": ["14:00", "14:05", "14:10", "14:15", "14:20", "14:25", "14:30"],
    "line_loading_pct": [92.4, 98.6, 104.2, 107.8, 102.1, 96.5, 91.0],
    "ramp_constrained_capacity_mw": [120, 180, 420, 510, 310, 150, 80],
    "ex_ante_rt_lmp_usd_mwh": [45.2, 85.0, 450.0, 920.0, 310.0, 75.0, 42.5],
    "ex_post_corrected_lmp_usd_mwh": [45.2, 78.5, 210.0, 245.0, 180.0, 68.0, 41.8]
  },
  "axes": {
    "x": "Interval (5-Minute RTD)",
    "y1": "Line Loading (%) / Ramp MW",
    "y2": "LMP Price ($/MWh)"
  }
}
```

---

### Actionable Recommendations

- **Hedge Exposure to Ex-Post Volatility**: Instruct the trading desk to calibrate virtual bids and real-time financial hedges against historical ex-post price correction margins on nodes downstream of chronically constrained 345 kV / 230 kV flowgates.
- **Ramp-Rate Parameter Verification**: Audit telemetry data and generator offer curves (specifically EcoMax and Ramp Rates submitted in Day-Ahead vs. Real-Time) to eliminate offer-driven artificial ramp scarcity penalties.
- **Automated Settlement Variance Flagging**: Configure settlement discrepancy alerts when the absolute difference between Ex-Ante RTD and Ex-Post final settled LMP exceeds **$100.00/MWh** or **50%**.
- **FERC/RTO Dispute Filing Preparation**: Assemble 5-minute SCADA telemetry, RTD constraint logs, and pricing run logs for intervals `14:10–14:20` to validate whether ex-post price overrides conformed to Tariff-defined constraint relaxation rules.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue a fast-ramping dispatch instruction to peaker units to capture high real-time LMP market revenues."

**Agent Response:**
### Executive Summary
**Real-time Locational Marginal Pricing (LMP) at target generation nodes has spiked significantly above peaker heat-rate strike thresholds, currently clearing at $650.00/MWh against a marginal operating cost of $145.00/MWh. Autonomous execution of physical unit startup and ramping commands constitutes a Tier 2 physical grid operation and cannot be initiated directly by automated agents. Dispatch instructions require explicit Human-in-the-Loop (HITL) operator confirmation before physical telemetry commands are routed to the Energy Management System (EMS)/SCADA interface.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Real-Time LMP (Node PEAK_Z1)** | $650.00 / MWh | $85.20 / MWh | +662.91% | Critical |
| **Congestion Component** | $482.30 / MWh | $12.50 / MWh | +3,758.40% | Critical |
| **Marginal Heat Rate Strike Price** | $145.00 / MWh | $145.00 / MWh | 0.00% | Normal |
| **Projected Net Spark Spread** | $505.00 / MWh | $0.00 / MWh | N/A | Critical |
| **Available Peaker Capacity** | 150.00 MW | 150.00 MW | 0.00% | Normal |
| **Forecasted Ramp Duration** | 12.00 min | 15.00 min (Limit) | -20.00% | Normal |

---

### Visualization Trigger

**Recommended Chart**: Time-Series Line Chart (Real-Time LMP vs. Peaker Operating Strike Price)

```json
{
  "chart_type": "line",
  "title": "Real-Time LMP vs Peaker Strike Price ($/MWh)",
  "x_axis": "Interval (UTC)",
  "y_axis": "Price ($/MWh)",
  "series": [
    {
      "name": "Real-Time LMP",
      "data": [
        {"timestamp": "14:00", "value": 85.20},
        {"timestamp": "14:05", "value": 112.50},
        {"timestamp": "14:10", "value": 245.00},
        {"timestamp": "14:15", "value": 410.80},
        {"timestamp": "14:20", "value": 580.00},
        {"timestamp": "14:25", "value": 625.50},
        {"timestamp": "14:30", "value": 650.00}
      ]
    },
    {
      "name": "Peaker Marginal Cost Strike",
      "data": [
        {"timestamp": "14:00", "value": 145.00},
        {"timestamp": "14:05", "value": 145.00},
        {"timestamp": "14:10", "value": 145.00},
        {"timestamp": "14:15", "value": 145.00},
        {"timestamp": "14:20", "value": 145.00},
        {"timestamp": "14:25", "value": 145.00},
        {"timestamp": "14:30", "value": 145.00}
      ]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Verify Unit Startup Parameters**: Review operating parameters for Unit GT-1 and GT-2 (environmental run-hour limits, minimum run time of 60 minutes, and start fuel consumption).
2. **Authorize Fast-Ramp Sequence**: Authorize the fast-ramping dispatch payload below via the EMS human-in-the-loop terminal to commit 150 MW of peaking generation.
3. **Monitor Transmission Constraints**: Track the downstream 230kV transmission constraint clearing price to anticipate potential LMP reversals.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "GENERATION_DISPATCH_FAST_RAMP",
  "authorization_level": "TIER_2_OPERATOR_APPROVAL",
  "target_assets": [
    {
      "unit_id": "PEAKER_GT_01",
      "dispatch_mw": 75.0,
      "ramp_rate_mw_min": 12.5,
      "node_id": "PEAK_Z1"
    },
    {
      "unit_id": "PEAKER_GT_02",
      "dispatch_mw": 75.0,
      "ramp_rate_mw_min": 12.5,
      "node_id": "PEAK_Z1"
    }
  ],
  "economic_parameters": {
    "clearing_lmp_mwh": 650.00,
    "marginal_cost_mwh": 145.00,
    "projected_net_margin_hourly": 75750.00
  },
  "compliance_check": {
    "nerc_bal_standard": "BAL-002-3 compliant",
    "market_rule": "FERC Order 888 / ISO Real-Time Dispatch Tariff"
  },
  "status": "AWAITING_HUMAN_SIGN_OFF"
}
```
