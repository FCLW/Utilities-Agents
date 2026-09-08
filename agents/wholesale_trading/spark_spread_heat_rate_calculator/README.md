# ⚡ Spark Spread Heat Rate Calculator

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of spark spread heat rate calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Spark Spread Heat Rate Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank spark spread heat rate calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.spark_spread_heat_rate_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the real-time clean spark spread ($/MWh) for Combined Cycle Gas Turbine 1 based on spot electricity and Henry Hub gas prices?"

**Agent Response:**
### Executive Summary
**The real-time Clean Spark Spread (CSS) for Combined Cycle Gas Turbine 1 (CCGT-1) is currently calculated at +$26.50/MWh, reflecting strong dispatch economics above the plant's operational profitability threshold.** **With real-time spot electricity clearing at $48.50/MWh and Henry Hub spot natural gas at $2.45/MMBtu across a baseload heat rate of 7,000 Btu/kWh (7.00 MMBtu/MWh), unit margins remain robust after accounting for carbon compliance and variable operating costs.**

---

### Data Presentation

$$\text{Clean Spark Spread (\$/MWh)} = \text{Spot LMP} - (\text{Heat Rate} \times P_{\text{gas}}) - (\text{Emissions Intensity} \times P_{\text{CO}_2}) - \text{VOM}$$

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Spot Electricity LMP** | $48.50 / MWh | $42.00 / MWh | +15.48% | Normal |
| **Henry Hub Spot Gas Price** | $2.45 / MMBtu | $2.60 / MMBtu | -5.77% | Normal |
| **CCGT-1 Operating Heat Rate** | 7,000 Btu/kWh (7.00 MMBtu/MWh) | 6,950 Btu/kWh | +0.72% | Normal |
| **Fuel Component Cost** | $17.15 / MWh | $18.07 / MWh | -5.09% | Normal |
| **Emissions Cost (CO₂ @ $5.00/MT)** | $1.85 / MWh | $1.85 / MWh | 0.00% | Normal |
| **Variable O&M (VOM)** | $3.00 / MWh | $3.00 / MWh | 0.00% | Normal |
| **Gross Spark Spread** | $31.35 / MWh | $23.93 / MWh | +31.01% | Normal |
| **Clean Spark Spread (Net Margin)** | **$26.50 / MWh** | **$19.08 / MWh** | **+38.89%** | **Normal** |

---

### Visualization Configuration

```json
{
  "chart_type": "bar",
  "data": {
    "labels": [
      "Spot Power LMP",
      "Fuel Cost (Gas)",
      "Emissions Cost (CO2)",
      "Variable O&M",
      "Clean Spark Spread (Net)"
    ],
    "datasets": [
      {
        "label": "CCGT-1 Revenue & Cost Components ($/MWh)",
        "data": [48.50, -17.15, -1.85, -3.00, 26.50],
        "backgroundColor": ["#2563EB", "#DC2626", "#F59E0B", "#6B7280", "#10B981"]
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Maintain Generation Schedule**: CCGT-1 is operating well above its minimum economic dispatch hurdle ($12.00/MWh threshold). Maintain target baseload generation profile.
- **Lock In Real-Time Spreads via Financial Hedges**: Evaluate hedging intra-day exposure by selling forward prompt-hour power and securing natural gas swing volume to lock in margins above $25.00/MWh.
- **Monitor Heat Rate Degradation**: Ambient temperature fluctuations may alter real-time heat rate curves; trigger automatic threshold alerts if heat rate rises above 7,250 Btu/kWh.

---

### [TIER 2 ACTION REQUIRED]
*If executing forward physical gas scheduling or altering real-time generation commitment schedules >50 MW, operator authorization is required before transmitting dispatch orders to the ISO/RTO portal.*

### Example 2: Trend & Comparative Analysis
**User:** "Analyze how ambient intake air temperature impacts gas turbine heat rate efficiency and power output degradation."

**Agent Response:**
### Executive Summary
**Ambient intake air temperature has an inverse relationship with gas turbine capacity and a direct degrading impact on heat rate efficiency due to air density variation.** **For standard heavy-duty combustion turbines (e.g., F- and H-Class frames), every 10°F increase in ambient temperature above ISO base conditions (59°F / 15°C) yields an estimated 3.0% to 4.5% reduction in net power output and a 1.2% to 1.8% increase (degradation) in net heat rate (Btu/kWh).** **In wholesale energy markets, this thermodynamic derate simultaneously compresses generation capacity and increases variable fuel cost, requiring dynamic adjustment of unit dispatch bids and Clean/Dark Spark Spread calculations during extreme summer peak intervals.**

---

### Thermodynamic Principles & Degradation Mechanisms

1. **Air Density & Mass Flow Rate**: Gas turbines are constant volumetric flow machines. The mass flow rate ($\dot{m} = \rho \cdot \dot{V}$) entering the axial compressor is directly proportional to intake air density ($\rho = \frac{P_{amb}}{R \cdot T_{amb}}$). Elevated ambient temperatures lower air density, reducing mass flow and limiting total expansion mass across the turbine blades.
2. **Compressor Specific Work**: Warmer intake air increases the specific compression work required per unit mass ($W_c = c_p \cdot T_1 [r_p^{(\gamma-1)/\gamma} - 1]$), consuming a higher fraction of gross turbine output.
3. **Turbine Firing Temperature & Exhaust Backpressure Limits**: Higher compressor discharge temperatures ($T_2$) restrict maximum fuel firing limits to maintain hot gas path component metallurgical integrity, worsening net thermal efficiency.

---

### Performance Sensitivity Matrix (Relative to ISO Baseline: 59°F / 15°C, 60% RH, 14.696 psia)

| Metric | Current Value (Peak Summer 105°F) | Baseline / Target (ISO 59°F) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Combustion Turbine Net Output** | 191.1 MW | 230.0 MW | -16.9% | Critical |
| **Net Heat Rate (LHV)** | 7,690 Btu/kWh | 7,050 Btu/kWh | +9.08% (Degraded) | Critical |
| **Air Mass Flow Rate** | 1,048 lb/s | 1,225 lb/s | -14.4% | Critical |
| **Compressor Power Consumption** | 134.5 MW | 126.2 MW | +6.58% | Warning |
| **Gross Thermal Efficiency (LHV)** | 44.37% | 48.40% | -8.33% | Warning |
| **Fuel Burn per MWh Generation** | 7.69 MMBtu/MWh | 7.05 MMBtu/MWh | +9.08% | Critical |

*Table: Standard representative performance impact for a 230 MW F-Class simple-cycle combustion turbine across ambient extremes.*

---

### Wholesale Trading & Spark Spread Margin Impact

The thermodynamic heat rate derate translates directly into financial exposure within real-time and day-ahead LMP markets via the **Spark Spread formula**:

$$\text{Spark Spread } (\$/\text{MWh}) = P_{\text{power}} - (\text{Heat Rate} \times P_{\text{gas}}) - \text{VOM}$$

- **Marginal Fuel Cost Shift**: At a natural gas hub price of \$3.50/MMBtu, an increase in heat rate from 7,050 to 7,690 Btu/kWh increases the unit's marginal fuel cost by **\$2.24/MWh** (\$24.68 vs. \$26.92/MWh).
- **Available Margin Compression**: Failure to update supply curves with ambient-adjusted heat rate curves risks dispatching the asset below its actual marginal cost during real-time heat waves.

---

### Visualization Configuration

```json
{
  "title": "Gas Turbine Performance vs. Ambient Intake Air Temperature",
  "chart_type": "line",
  "xAxis": {
    "name": "Ambient Temperature (°F)",
    "data": [30, 45, 59, 75, 90, 105]
  },
  "yAxis": [
    {"name": "Power Output (% ISO)", "unit": "%"},
    {"name": "Heat Rate (Btu/kWh)", "unit": "Btu/kWh"}
  ],
  "series": [
    {
      "name": "Power Output (% ISO)",
      "type": "line",
      "data": [108.5, 104.2, 100.0, 94.8, 89.2, 83.1]
    },
    {
      "name": "Heat Rate (Btu/kWh)",
      "type": "line",
      "data": [6820, 6910, 7050, 7220, 7430, 7690]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Implement Dynamic Bidding Curve Correction**:
   - Integrate day-ahead and hour-ahead ambient weather telemetry directly into the ETRM (Energy Trading and Risk Management) bidding module to dynamically adjust heat rate heat input coefficients prior to market clearing cutoff times.
2. **Inlet Cooling System Optimization**:
   - Deploy or activate inlet air evaporative cooling media, fogging systems, or mechanical inlet chillers during ambient intervals $> 75^\circ\text{F}$ to reduce intake temperature toward the wet-bulb limit, recovering up to 6–10% derated output.
3. **Portfolio VaR and Hedging Adjustments**:
   - Re-evaluate forward peak contract commitments against de-rated physical capacity limits during heat wave forecasts to avoid exposure to real-time ISO non-performance and imbalance penalties.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch Combined Cycle Unit 1 when the clean spark spread expands beyond the operational margin threshold of $8.50/MWh."

**Agent Response:**
### 1. Executive Summary
**Clean spark spread (CSS) monitoring has been configured for Combined Cycle Unit 1 against the target operational dispatch threshold of $8.50/MWh. Economic dispatch conditions are evaluated by indexing real-time Day-Ahead/Real-Time LMP power prices against unit heat rate, spot natural gas delivery, carbon allowances, and variable O&M expenses. Because initiating physical generation modifies grid injection and commits generation assets, automated physical dispatch constitutes a Tier 2 action requiring Human-in-the-Loop (HITL) authorization prior to GMS/EMS unit commitment execution.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Clean Spark Spread (CSS)** | $11.25/MWh | $8.50/MWh | +32.35% | Critical (Trigger Active) |
| **Full Load Heat Rate (HR)** | 7,150 Btu/kWh | 7,200 Btu/kWh | -0.69% | Normal |
| **Power LMP (Hub/Node)** | $48.50/MWh | $40.00/MWh | +21.25% | Normal |
| **Fuel Gas Cost (Delivered)** | $4.20/MMBtu | $3.80/MMBtu | +10.53% | Normal |
| **CO2 Emission / Allowance** | $4.75/MWh | $4.50/MWh | +5.56% | Normal |
| **Variable O&M (VOM)** | $2.50/MWh | $2.50/MWh | 0.00% | Normal |
| **Net Operational Margin** | $11.25/MWh | $8.50/MWh | +32.35% | Critical (Trigger Active) |

---

### 3. Visualization Triggers
**Recommended Visualization**: Time-Series Line Chart illustrating projected intraday Clean Spark Spread trajectory plotted against the static $8.50/MWh operational margin threshold across standard dispatch intervals (HE07–HE14).

```json
{
  "chart_type": "line",
  "title": "Clean Spark Spread vs Operational Margin Threshold ($8.50/MWh)",
  "xAxis": ["HE07", "HE08", "HE09", "HE10", "HE11", "HE12", "HE13", "HE14"],
  "series": [
    {
      "name": "Clean Spark Spread ($/MWh)",
      "data": [4.20, 6.10, 8.15, 9.40, 11.25, 10.80, 9.10, 7.80]
    },
    {
      "name": "Dispatch Threshold ($/MWh)",
      "data": [8.50, 8.50, 8.50, 8.50, 8.50, 8.50, 8.50, 8.50]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Confirm Economic Dispatch Window**: Review forward spark spread curve across HE10–HE13 where net operational margin exceeds the $8.50/MWh operational hurdle.
- **Gas Nomination & Pipeline Scheduling**: Coordinate with the fuel desk to verify intra-day gas nominations and pipeline balance to support startup and base-load MW output for CCGT Unit 1.
- **Submit Human-in-the-Loop Confirmation**: Authorize the Tier 2 unit commitment order below to release bidding parameters to the Generation Management System (GMS) / Market Operations desk.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "GENERATION_UNIT_DISPATCH_COMMITMENT",
  "asset_id": "CCGT_UNIT_1",
  "trigger_condition": "CLEAN_SPARK_SPREAD > 8.50 USD/MWh",
  "current_css_value": 11.25,
  "threshold_value": 8.50,
  "operating_mode": "ECONOMIC_DISPATCH",
  "requires_hitl_approval": true,
  "dispatch_instruction": "Commit Combined Cycle Unit 1 to Min Gen / Base Dispatch for active profitable market intervals (HE10-HE13) subject to pipeline gas availability."
}
```
