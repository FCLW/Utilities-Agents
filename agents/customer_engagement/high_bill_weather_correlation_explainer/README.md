# ⚡ High Bill Weather Correlation Explainer

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of high bill weather correlation explainer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — High Bill Weather Correlation Explainer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank high bill weather correlation explainer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.high_bill_weather_correlation_explainer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Why was my electric bill $140 higher this January compared to the previous month?"

**Agent Response:**
### Executive Summary
**Your January bill increase of $140 was primarily driven by a 64.3% surge in Heating Degree Days (HDDs) caused by sustained sub-freezing temperatures, which substantially increased space heating load.** **This extreme cold triggered supplemental electric resistance heat strips and extended HVAC compressor cycles, driving daily consumption from an average of 36.8 kWh/day in December to 61.6 kWh/day in January.** **Additionally, increased volumetric consumption pushed a higher proportion of energy usage into your utility tariff's higher marginal rate tier.**

---

### Quantitative Weather & Billing Correlation Analysis

| Metric | Current Value (Jan) | Baseline / Target (Dec) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Billed Amount** | $325.00 | $185.00 | +75.7% (+$140.00) | **Warning** |
| **Total Consumption** | 1,910 kWh | 1,140 kWh | +67.5% (+770 kWh) | **Warning** |
| **Average Daily Consumption** | 61.6 kWh/day | 36.8 kWh/day | +67.4% | **Warning** |
| **Heating Degree Days (HDD, Base 65°F)** | 1,185 HDD | 721 HDD | +64.3% (+464 HDD) | **Critical** |
| **Average Ambient Temperature** | 24.3°F | 43.0°F | -43.5% (-18.7°F) | **Critical** |
| **Billing Cycle Duration** | 31 Days | 31 Days | 0.0% | **Normal** |
| **Effective Marginal Rate Tier Shift** | Tier 2 Marginal Rate ($0.175/kWh) | Tier 1 Base Rate ($0.145/kWh) | +20.7% | **Normal** |

---

### Root-Cause Breakdown
1. **HVAC Heating & Auxiliary Strip Engagement (~72% of increase / ~$101)**:
   - When ambient temperatures drop below the thermal balance point (typically ~32°F to 35°F for air-source heat pumps), high-draw auxiliary electric resistance heat (5–10 kW) automatically engages to meet thermostat setpoints.
   - Prolonged freezing intervals during January accounted for approximately 554 additional kWh.
2. **Thermal Envelope Loss & Water Heating Overhead (~18% of increase / ~$25)**:
   - Larger indoor-to-outdoor temperature deltas ($\Delta T$) accelerate conductive heat loss through windows, attics, and exterior walls.
   - Water heaters consume significantly more energy to heat colder incoming ground water (approx. 42°F in January vs. 52°F in December).
3. **Marginal Rate Tier Progression (~10% of increase / ~$14)**:
   - Consumption exceeding the baseline Tier 1 threshold (1,000 kWh) was billed at the higher Tier 2 marginal rate, compounding the weather-driven kWh increase.

---

### Visualization Trigger: Dual-Axis Consumption vs. Temperature

Recommended visualization: **Dual-Axis Time-Series Line & Column Chart** to demonstrate the direct inverse correlation between declining daily outdoor temperatures and spiking daily kWh usage.

```json
{
  "chart_type": "dual_axis_line",
  "title": "Daily Electric Consumption (kWh) vs. Mean Temperature (°F)",
  "categories": [
    "Week 1 Dec", "Week 2 Dec", "Week 3 Dec", "Week 4 Dec",
    "Week 1 Jan", "Week 2 Jan", "Week 3 Jan", "Week 4 Jan"
  ],
  "series": [
    {
      "name": "Electricity Consumption (kWh/day)",
      "type": "column",
      "data": [32.4, 34.1, 38.5, 42.0, 58.6, 68.2, 64.1, 55.3],
      "unit": "kWh"
    },
    {
      "name": "Average Temperature (°F)",
      "type": "line",
      "data": [48.0, 45.0, 41.0, 38.0, 26.0, 18.0, 22.0, 31.0],
      "unit": "°F"
    }
  ]
}
```

---

### Actionable Recommendations

- **Audit Thermostat Setpoints & Emergency Heat**: Verify smart thermostat schedules; lowering nighttime heating setpoints from 72°F to 68°F can reduce space heating consumption by up to 10–12%.
- **Enroll in Budget Billing / Levelized Payment Plan**: Smooth out seasonal winter heating and summer cooling spikes into predictable, equal monthly billing installments.
- **Inspect Heat Pump Defrost & Auxiliary Lockout Settings**: Schedule an HVAC maintenance inspection to ensure heat pump compressor stages are operating optimally before auxiliary resistance elements kick in.
- **Utilize High-Usage Alerts**: Subscribe to mid-cycle AMI threshold alerts to receive notifications via SMS or email when daily consumption trends exceed typical baselines.

### Example 2: Trend & Comparative Analysis
**User:** "Correlate local outdoor heating degree-days and extreme sub-zero temperature spells with the customer's daily smart meter usage."

**Agent Response:**
### Executive Summary
**Customer daily interval smart meter analysis demonstrates an extremely strong positive statistical correlation ($R^2 = 0.94$) between surge electricity consumption and the multi-day polar vortex sub-zero temperature spell.** **During peak freeze events (ambient lows reaching $-15^\circ\text{F}$ and heating degree-days reaching $75\ \text{HDD}$), heating load drove daily electricity consumption from a baseline of $28.2\ \text{kWh/day}$ up to $79.1\ \text{kWh/day}$ ($+180.5\%$).** **The elevated billing cycle totals are directly attributable to continuous auxiliary/resistive space heating thermal requirements during sub-zero intervals rather than metering telemetry drift or unauthorized grid leakage.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Daily Smart Meter Usage** | $79.1\ \text{kWh/day}$ | $28.2\ \text{kWh/day}$ | $+180.5\%$ | **Critical** |
| **Average Daily Consumption (Freeze Spell)** | $69.4\ \text{kWh/day}$ | $30.1\ \text{kWh/day}$ | $+130.6\%$ | **Warning** |
| **Peak Heating Degree Days (Base $65^\circ\text{F}$)** | $75.0\ \text{HDD}$ | $32.0\ \text{HDD}$ | $+134.4\%$ | **Critical** |
| **Minimum Ambient Temperature** | $-15.0^\circ\text{F}$ | $22.0^\circ\text{F}$ | $-168.2\%$ | **Critical** |
| **Heating Load Sensitivity Coefficient** | $1.12\ \text{kWh / HDD}$ | $0.45\ \text{kWh / HDD}$ | $+148.9\%$ | **Warning** |
| **AMI Interval VEE Success Rate** | $100.0\%$ | $99.5\%$ | $+0.5\%$ | **Normal** |
| **Meter Hardware Calibration & Clock Drift** | $0.00\ \text{s / drift}$ | $\pm 15.0\ \text{s}$ | $0.0\%$ | **Normal** |

---

### Visualization Trigger: Dual-Axis Time-Series & Weather Correlation

*Recommended Chart Type:* **Dual-Axis Time-Series Line Chart with Overlay Scatter Regression**

```json
{
  "chart_type": "dual_axis_line",
  "title": "Smart Meter Daily Consumption vs. Heating Degree-Days & Minimum Temperature",
  "xAxis": {
    "title": "Date",
    "categories": ["Jan 10", "Jan 11", "Jan 12", "Jan 13", "Jan 14", "Jan 15", "Jan 16", "Jan 17", "Jan 18", "Jan 19", "Jan 20", "Jan 21", "Jan 22"]
  },
  "yAxes": [
    {
      "id": "y-kwh",
      "title": "Daily Smart Meter Usage (kWh)",
      "position": "left"
    },
    {
      "id": "y-hdd",
      "title": "Heating Degree Days (HDD Base 65°F)",
      "position": "right"
    },
    {
      "id": "y-temp",
      "title": "Min Temp (°F)",
      "position": "right",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Daily AMI Usage (kWh)",
      "type": "line",
      "yAxis": "y-kwh",
      "color": "#E65100",
      "data": [28.4, 31.2, 35.8, 58.6, 72.4, 79.1, 74.8, 61.2, 42.0, 33.5, 29.8, 27.5, 26.1]
    },
    {
      "name": "Heating Degree Days (HDD)",
      "type": "column",
      "yAxis": "y-hdd",
      "color": "#1E88E5",
      "data": [33.0, 36.0, 42.0, 62.0, 71.0, 75.0, 73.0, 63.0, 45.0, 35.0, 31.0, 28.0, 27.0]
    },
    {
      "name": "Daily Min Temperature (°F)",
      "type": "line",
      "yAxis": "y-temp",
      "color": "#5E35B1",
      "dashStyle": "Dash",
      "data": [18.0, 14.0, 8.0, -4.0, -12.0, -15.0, -11.0, -2.0, 10.0, 19.0, 24.0, 26.0, 28.0]
    }
  ],
  "correlation_metrics": {
    "pearson_r": 0.968,
    "r_squared": 0.937,
    "p_value": "< 0.0001",
    "thermostat_setpoint_estimate_f": 68.5
  }
}
```

---

### Actionable Recommendations

- **Omnichannel Customer Explanation Dispatch**: 
  - Route the automated *Weather Impact Bill Breakdown* to the customer portal and interactive voice response (IVR) profile, highlighting that $62.4\%$ of the current billing cycle total was driven strictly during the 5-day sub-zero freeze event (Jan 13–17).
- **Auxiliary Strip Heat Audit**: 
  - The high sensitivity slope ($1.12\ \text{kWh/HDD}$) indicates heat pump auxiliary resistance heat strip lock-in below $15^\circ\text{F}$. Proactively suggest a home energy assessment or smart thermostat balance point calibration.
- **Budget Billing & Flexible Payment Terms**: 
  - Trigger downstream enrollment workflow for Levelized Budget Billing to smooth the winter heating spikes across 12 annualized billing cycles.
- **AMI Meter Telemetry Validation Confirmation**: 
  - Confirm to tier-1 customer service representatives that meter interval validation, editing, and estimation (VEE) passed with zero data gaps, ruling out meter malfunction or billing multiplier discrepancies.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate a customer-facing bill explainer graphic detailing day-by-day temperature impact for CSR agent use."

**Agent Response:**
### 1. Executive Summary
**During the 30-day billing cycle, extreme ambient temperature spikes (peaking above 100°F during two distinct heat events) directly drove an 84.4% increase in HVAC-driven daily electricity consumption. Analysis confirms a high correlation coefficient ($R^2 = 0.94$) between daily Cooling Degree Days (CDD) and peak household kWh consumption. The resulting high bill is primarily attributable to weather-induced cooling demand rather than rate changes, unbilled carryover, or metering hardware irregularities.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Cycle Consumption** | 1,288 kWh | 890 kWh | +44.7% | **Warning** |
| **Peak Daily Usage** | 62.0 kWh (Day 21) | 30.0 kWh | +106.7% | **Critical** |
| **Average Outdoor Temperature** | 84.6°F | 75.2°F | +12.5% | **Warning** |
| **Peak Day Temperature** | 104.0°F (Day 21) | 78.0°F | +33.3% | **Critical** |
| **Cooling Degree Days (CDD)** | 378 CDD | 120 CDD | +215.0% | **Critical** |
| **Weather/Usage Correlation ($R^2$)** | 0.94 | < 0.50 | +88.0% | **Normal** |
| **Interval VEE Validation Rate** | 100.0% | 99.5% | +0.5% | **Normal** |

---

### 3. Visualization Triggers & Graphic Configuration

- **Recommended Chart Type**: Dual-Axis Overlay (Daily kWh Usage Bar Chart overlaid with Mean Daily Temperature Line Chart).
- **Chart UI Payload**:

```json
{
  "chart_type": "dual_axis_line_bar",
  "title": "Daily Energy Consumption vs. Average Temperature",
  "xAxis": {
    "categories": [
      "Day 1", "Day 2", "Day 3", "Day 4", "Day 5", "Day 6", "Day 7", "Day 8", "Day 9", "Day 10",
      "Day 11", "Day 12", "Day 13", "Day 14", "Day 15", "Day 16", "Day 17", "Day 18", "Day 19", "Day 20",
      "Day 21", "Day 22", "Day 23", "Day 24", "Day 25", "Day 26", "Day 27", "Day 28", "Day 29", "Day 30"
    ],
    "title": "Billing Cycle Days"
  },
  "yAxis": [
    {
      "title": "Daily Usage (kWh)",
      "opposite": false
    },
    {
      "title": "Avg Temperature (°F)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Daily Usage (kWh)",
      "type": "column",
      "yAxis": 0,
      "data": [28, 29, 31, 30, 42, 48, 55, 58, 54, 49, 38, 32, 30, 29, 31, 33, 45, 52, 56, 59, 62, 60, 53, 41, 33, 30, 28, 29, 31, 30]
    },
    {
      "name": "Avg Outdoor Temp (°F)",
      "type": "line",
      "yAxis": 1,
      "data": [74, 75, 76, 77, 88, 93, 98, 101, 97, 92, 84, 76, 75, 74, 76, 79, 89, 95, 99, 102, 104, 101, 96, 86, 77, 75, 73, 74, 76, 75]
    },
    {
      "name": "Cooling Degree Baseline (72°F)",
      "type": "line",
      "dashStyle": "Dash",
      "yAxis": 1,
      "data": [72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72, 72]
    }
  ]
}
```

---

### 4. Actionable Recommendations for CSR Agent

- **Customer Communication Framing**:
  - Direct the customer's attention to **Days 6–9** and **Days 18–23**, pointing out that daily usage doubled specifically when temperatures exceeded 95°F–104°F.
  - Explain that for every 1°F increase above 75°F outdoor temperature, air conditioning compressor runtime increases exponentially to maintain indoor setpoints.
- **CSR Next Steps & Program Advisory**:
  - Offer enrollment in **Budget Billing / Levelized Payment Plans** to smooth out seasonal weather volatility.
  - Suggest smart thermostat optimization programs and peak-time savings rebates.
  - Confirm AMI interval telemetry passed all VEE validations (no estimated reads or meter errors).
