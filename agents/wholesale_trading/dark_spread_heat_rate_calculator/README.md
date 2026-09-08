# ⚡ Dark Spread Heat Rate Calculator

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of dark spread heat rate calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Dark Spread Heat Rate Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank dark spread heat rate calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.dark_spread_heat_rate_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the current dark spread ($/MWh) for our 600 MW supercritical coal plant given wholesale power and delivered coal costs?"

**Agent Response:**
### Executive Summary
**The gross dark spread for the 600 MW supercritical coal generating unit currently stands at $26.94/MWh based on an on-peak wholesale power LMP of $48.50/MWh and a delivered fuel cost of $21.56/MWh (8.80 MMBtu/MWh heat rate @ $2.45/MMBtu). Factoring in regional carbon allowance pricing ($10.00/ton @ 0.88 ton/MWh emission intensity) and Variable O&M ($4.50/MWh), the Net Clean Dark Spread is $13.64/MWh, maintaining positive operating margin across all standard on-peak hours.**

---

### Quantitative Performance Metrics

$$\text{Gross Dark Spread } (\$/\text{MWh}) = \text{Power LMP} - (\text{Delivered Coal Price } [\$/\text{MMBtu}] \times \text{Heat Rate } [\text{MMBtu/MWh}])$$

$$\text{Clean Dark Spread } (\$/\text{MWh}) = \text{Gross Dark Spread} - (\text{Carbon Price} \times \text{CO}_2 \text{ Emission Factor}) - \text{VOM}$$

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Wholesale Day-Ahead LMP (On-Peak)** | $48.50/MWh | $45.00/MWh | +7.78% | Normal |
| **Delivered Coal Cost** | $2.45/MMBtu | $2.30/MMBtu | +6.52% | Normal |
| **Supercritical Net Heat Rate** | 8.80 MMBtu/MWh | 8.75 MMBtu/MWh | +0.57% | Normal |
| **Fuel Component Cost** | $21.56/MWh | $20.13/MWh | +7.10% | Normal |
| **Gross Dark Spread** | **$26.94/MWh** | **$24.87/MWh** | **+8.32%** | Normal |
| **Variable O&M (VOM)** | $4.50/MWh | $4.20/MWh | +7.14% | Normal |
| **$\text{CO}_2$ Compliance Cost** (0.88 t/MWh @ $10/t) | $8.80/MWh | $8.00/MWh | +10.00% | Warning |
| **Net Clean Dark Spread (CDS)** | **$13.64/MWh** | **$12.67/MWh** | **+7.66%** | Normal |
| **Unit Output (Economic Dispatch)** | 540 MW (90% Cap) | 480 MW (80% Cap) | +12.50% | Normal |

---

### Visualization: Dark Spread Dispatch Breakdown

```json
{
  "chart_type": "bar",
  "title": "Dark Spread & Margin Breakdown Across Market Blocks ($/MWh)",
  "labels": ["Off-Peak (Base)", "On-Peak (Standard)", "Super-Peak (High Demand)"],
  "datasets": [
    {
      "label": "Wholesale Power LMP ($/MWh)",
      "data": [34.50, 48.50, 72.00]
    },
    {
      "label": "Fuel Cost ($/MWh)",
      "data": [21.56, 21.56, 21.56]
    },
    {
      "label": "Gross Dark Spread ($/MWh)",
      "data": [12.94, 26.94, 50.44]
    },
    {
      "label": "Net Clean Dark Spread ($/MWh)",
      "data": [-0.36, 13.64, 37.14]
    }
  ]
}
```

---

### Actionable Recommendations

- **Dispatch Bidding Optimization**: Submit Day-Ahead physical offers targeting full economic maximum (600 MW) during the HE 07:00–22:00 on-peak window where the Net CDS exceeds the $10.00/MWh hurdle threshold.
- **Off-Peak Cycling Assessment**: With off-peak Net Clean Dark Spread at -$0.36/MWh, evaluate reducing generation to the plant's minimum stable load (Pmin: 240 MW) rather than taking unit offline to avoid startup/shutdown thermal stress cycles.
- **Fuel & Allowance Hedging**: Execute forward coal purchase contracts for Q3/Q4 if rail transportation surcharges rise, locking in spark/dark spread hedges on Intercontinental Exchange (ICE) for expected baseload generation tranches.

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate plant operational heat rates (Btu/kWh) across partial loading points to determine minimum profitable generation thresholds."

**Agent Response:**
### Executive Summary
**Thermal efficiency deteriorates significantly at low operating points, where unit heat rates increase from a baseline of 9,050 Btu/kWh at 100% Maximum Continuous Rating (MCR) to 12,450 Btu/kWh at 25% minimum stable generation ($P_{min}$), a +37.57% heat rate penalty.** **To maintain a positive Clean Dark Spread under benchmark delivered coal pricing ($2.75/MMBtu) and variable environmental/O&M costs ($7.75/MWh), the minimum profitable Locational Marginal Price (LMP) threshold escalates from $32.64/MWh at full output to $41.99/MWh at $P_{min}$.** **Operating below 40% loading (240 MW) exposes the asset to negative operating margins if clearing LMPs fall below $37.59/MWh, requiring multi-part bid curve segmentation to ensure startup, no-load, and incremental energy costs are fully recovered.**

---

### Quantitative Evaluation: Heat Rate & Generation Thresholds

The table below details thermal efficiency, short-run marginal cost (SRMC), and break-even generation thresholds across discrete plant loading increments for a reference 600 MW subcritical/supercritical coal unit:

$$\text{SRMC } (\$/\text{MWh}) = \left(\text{Heat Rate } \left[\frac{\text{Btu}}{\text{kWh}}\right] \times 10^{-3} \times \text{Delivered Coal Price } \left[\frac{\$}{\text{MMBtu}}\right]\right) + \text{VOM} + \text{Emission Costs}$$

$$\text{Clean Dark Spread (CDS) } (\$/\text{MWh}) = \text{LMP} - \text{SRMC}$$

*Parameters: Delivered Coal Price = $2.75/MMBtu; Variable O&M (VOM) = $4.50/MWh; Emissions Allowance Cost ($\text{SO}_2, \text{NO}_x, \text{CO}_2$) = $3.25/MWh; Market LMP Reference = $42.50/MWh.*

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **100% Load (600 MW) Heat Rate** | 9,050 Btu/kWh | 9,050 Btu/kWh | 0.00% | Normal |
| **100% Load Break-Even LMP** | $32.64 / MWh | $32.64 / MWh | 0.00% | Normal |
| **100% Load Clean Dark Spread** | +$9.86 / MWh | +$10.00 / MWh | -1.40% | Normal |
| **80% Load (480 MW) Heat Rate** | 9,350 Btu/kWh | 9,050 Btu/kWh | +3.31% | Normal |
| **80% Load Break-Even LMP** | $33.46 / MWh | $32.64 / MWh | +2.51% | Normal |
| **60% Load (360 MW) Heat Rate** | 9,850 Btu/kWh | 9,050 Btu/kWh | +8.84% | Normal |
| **60% Load Break-Even LMP** | $34.84 / MWh | $32.64 / MWh | +6.74% | Normal |
| **40% Load (240 MW) Heat Rate** | 10,850 Btu/kWh | 9,050 Btu/kWh | +19.89% | Warning |
| **40% Load Break-Even LMP** | $37.59 / MWh | $32.64 / MWh | +15.17% | Warning |
| **25% Load ($P_{min}$ 150 MW) Heat Rate** | 12,450 Btu/kWh | 9,050 Btu/kWh | +37.57% | Critical |
| **25% Load Break-Even LMP** | $41.99 / MWh | $32.64 / MWh | +28.65% | Critical |
| **25% Load Clean Dark Spread** | +$0.51 / MWh | +$10.00 / MWh | -94.90% | Critical |

---

### Visualization Configuration

```json
{
  "chart_type": "line_column_combination",
  "title": "Thermal Heat Rate vs. Minimum Profitable Generation Threshold (SRMC)",
  "xAxis": {
    "name": "Loading Level (% / MW)",
    "categories": ["25% (150 MW)", "40% (240 MW)", "60% (360 MW)", "80% (480 MW)", "100% (600 MW)"]
  },
  "yAxis": [
    {
      "name": "Heat Rate (Btu/kWh)",
      "min": 8000,
      "max": 14000
    },
    {
      "name": "Break-Even LMP / SRMC ($/MWh)",
      "min": 25,
      "max": 50,
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Operational Heat Rate (Btu/kWh)",
      "type": "line",
      "yAxis": 0,
      "data": [12450, 10850, 9850, 9350, 9050]
    },
    {
      "name": "Break-Even Threshold / SRMC ($/MWh)",
      "type": "column",
      "yAxis": 1,
      "data": [41.99, 37.59, 34.84, 33.46, 32.64]
    },
    {
      "name": "Clean Dark Spread @ $42.50 LMP ($/MWh)",
      "type": "line",
      "yAxis": 1,
      "data": [0.51, 4.91, 7.66, 9.04, 9.86]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Segmented Multi-Part Offer Curves**:
   - Construct Day-Ahead and Real-Time offer curves with monotonically increasing piecewise segments reflecting the incremental heat rate (IHR), rather than an average unit heat rate.
   - Price Block 1 (0 to 150 MW, $P_{min}$) at **$41.99/MWh** minimum to prevent unrecovered fixed/no-load fuel penalties.
   - Price Incremental Blocks (150–360 MW, 360–480 MW, 480–600 MW) at **$30.55/MWh**, **$30.93/MWh**, and **$30.82/MWh** incremental SRMC respectively.

2. **Economic Turndown vs. Cycling Evaluation**:
   - When off-peak LMPs fall between **$33.00/MWh and $41.00/MWh**, maintain unit online at $P_{min}$ only if expected day-ahead restart/shutdown cycle costs (boiler stress, startup fuel, aux power) exceed the intra-day Clean Dark Spread operating deficit.
   - For sustained multi-day pricing forecasts $< \$37.00/\text{MWh}$, transition asset status to economic decommit.

3. **Fuel & Heat Rate Telemetry Integration**:
   - Continuously update boiler efficiency coefficients from plant distributed control systems (DCS) using as-burned coal calorific value (HHV/LHV) and ambient condenser backpressure data to avoid miscalculated dark spreads during ambient temperature swings.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit a generation commitment schedule to the ISO when dark spread margins exceed the $12.50/MWh hurdle rate."

**Agent Response:**
### Executive Summary
**The Dark Spread margin analysis indicates that peak operating hours (HE09–HE20) clear the hurdle rate at an average of $16.83/MWh, surpassing the defined $12.50/MWh threshold by +34.6%. In accordance with utility safety and market governance protocols, autonomous submission of generation commitment schedules to the Independent System Operator (ISO) constitutes a Tier 2 physical/financial market action. A finalized commitment schedule has been calculated and staged for mandatory Human-in-the-Loop (HITL) approval prior to ISO market clearing submission.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Dark Spread (HE09–HE20)** | $16.83/MWh | $12.50/MWh (Hurdle Rate) | +34.64% | Normal (Profitable) |
| **Off-Peak Dark Spread (HE01–08, 21–24)** | $8.83/MWh | $12.50/MWh (Hurdle Rate) | -29.36% | Warning (Sub-Hurdle) |
| **Full Day 24-Hr Average LMP** | $47.50/MWh | $41.00/MWh | +15.85% | Normal |
| **Delivered Fuel Cost (Coal)** | $2.65/MMBtu | $2.60/MMBtu | +1.92% | Normal |
| **Operating Heat Rate (Average)** | 9,800 Btu/kWh | 9,750 Btu/kWh | +0.51% | Normal |
| **Variable O&M + Emissions** | $7.60/MWh | $7.50/MWh | +1.33% | Normal |
| **Projected Peak Operating P&L** | +$78,500 | $0.00 | N/A | Normal |

---

### Visualization Triggers

**Recommended Visualization:** Time-Series Line Chart illustrating hourly Day-Ahead Dark Spread against the $12.50/MWh hurdle rate threshold.

```json
{
  "chart_type": "line",
  "title": "Day-Ahead Dark Spread vs. Hurdle Rate ($12.50/MWh)",
  "xAxis": ["HE01-04", "HE05-08", "HE09-12", "HE13-16", "HE17-20", "HE21-24"],
  "series": [
    {
      "name": "Dark Spread ($/MWh)",
      "data": [6.40, 11.20, 16.80, 18.50, 15.20, 8.90]
    },
    {
      "name": "Hurdle Rate Threshold ($/MWh)",
      "data": [12.50, 12.50, 12.50, 12.50, 12.50, 12.50]
    }
  ]
}
```

---

### Actionable Recommendations

- **Peak Dispatch Commitment**: Authorize the economic commitment for Unit 1 across hours ending 09:00 through 20:00 (12 consecutive operating hours) to capture the positive spread margin above the $12.50/MWh hurdle rate.
- **Off-Peak De-Commitment / Min-Gen**: Maintain minimum generation or de-commit during off-peak hours (HE01–08 and HE21–24) to avoid margin erosion where spreads drop to $6.40–$8.90/MWh.
- **Fuel & Emissions Hedging**: Lock in matching daily coal delivery nominations and verify adequate SO₂/NOx/CO₂ allowance coverage to prevent marginal cost drift.
- **Market Settlement Tracking**: Monitor real-time LMP divergence relative to Day-Ahead clearing to evaluate risk exposure on virtual or physical imbalance settlements.

---

### [TIER 2 ACTION REQUIRED]

```yaml
action_type: "ISO_GENERATION_COMMITMENT_SUBMISSION"
risk_level: "Tier 2 - High Financial & Physical Grid Impact"
asset_id: "GEN_UNIT_COAL_01"
market: "Day-Ahead Wholesale Energy Market"
commitment_parameters:
  operating_hours: "HE09 - HE20 (12 Hours)"
  capacity_committed_mw: 350
  economic_max_mw: 350
  economic_min_mw: 120
  dispatch_price_offer_mwh: 33.57
  projected_net_margin: "$16.83/MWh ($70,686 total for block)"
iso_payload_status: "STAGED - AWAITING HUMAN TRADER CONFIRMATION"
instruction: "Please confirm or reject the commitment schedule submission before the Day-Ahead Market bid close deadline."
```
