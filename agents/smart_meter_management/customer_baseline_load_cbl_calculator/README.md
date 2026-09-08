# ⚡ Customer Baseline Load Cbl Calculator

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of customer baseline load cbl calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Customer Baseline Load Cbl Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank customer baseline load cbl calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.customer_baseline_load_cbl_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the calculated Customer Baseline Load (CBL) for commercial accounts participating in tomorrow's demand response event?"

**Agent Response:**
### Executive Summary
**The aggregated Customer Baseline Load (CBL) for the 142 commercial accounts enrolled in tomorrow’s peak Demand Response (DR) event (14:00–18:00 EST) is calculated at 50.48 MW average across event hours using the standard 10-in-10 baseline methodology with symmetric additive weather adjustment.** **Total nominated curtailment commitment stands at 10.10 MW (20.0% reduction), bringing target load during peak dispatch to 40.38 MW.** **All AMI interval telemetry and VEE (Validation, Editing, and Estimation) processes have achieved 99.8% data completeness across participating commercial meters.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Aggregated Peak Event CBL** | 52.10 MW (at 15:00) | 52.10 MW (10-in-10 CBL) | 0.00% | **Normal** |
| **Event Average CBL (14:00–18:00)** | 50.48 MW | 50.48 MW | 0.00% | **Normal** |
| **Nominated Target Load (Post-Curtailment)** | 40.38 MW | 50.48 MW (Baseline) | -20.01% | **Normal** |
| **Forecasted Unconstrained Load** | 51.93 MW avg | 50.48 MW (Baseline) | +2.87% | **Normal** |
| **Commercial Account Enrollment** | 142 Accounts | 145 Eligible Accounts | -2.07% | **Normal** |
| **Telemetry & VEE Data Quality Score** | 99.82% complete | 98.00% (Threshold) | +1.86% | **Normal** |

#### Segment-Level CBL Breakdown (Peak Event Hour 15:00–16:00)

| Commercial Sector | Participating Meters | Calculated CBL (MW) | Target Curtailment (MW) | Target Load (MW) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Large Commercial & Office Towers** | 48 | 21.45 | 4.30 | 17.15 | **Normal** |
| **Light Industrial & Manufacturing** | 31 | 16.80 | 3.55 | 13.25 | **Normal** |
| **Retail & Supermarket Chains** | 38 | 8.95 | 1.45 | 7.50 | **Normal** |
| **Data Centers & Tech Facilities** | 25 | 4.90 | 0.80 | 4.10 | **Normal** |
| **Total Commercial Portfolio** | **142** | **52.10** | **10.10** | **42.00** | **Normal** |

---

### Visualization Triggers

A **Time-Series Line Chart** is recommended to compare the hourly baseline profile against forecasted unconstrained demand and target curtailed demand over the operational window (12:00 PM – 07:00 PM).

```json
{
  "chart_type": "line",
  "title": "Tomorrow's Demand Response Event - Commercial CBL Profile vs Expected Load",
  "xAxis": {
    "categories": ["12:00 PM", "01:00 PM", "02:00 PM", "03:00 PM", "04:00 PM", "05:00 PM", "06:00 PM", "07:00 PM"]
  },
  "yAxis": {
    "title": "Aggregated Demand (MW)"
  },
  "series": [
    {
      "name": "Customer Baseline Load (CBL 10-in-10 Adjusted)",
      "data": [42.8, 45.3, 49.6, 52.1, 51.8, 48.4, 44.2, 39.5]
    },
    {
      "name": "Forecasted Unconstrained Load",
      "data": [43.5, 46.2, 51.0, 53.8, 53.2, 49.7, 45.1, 40.2]
    },
    {
      "name": "Committed Target Load (Post-Curtailment)",
      "data": [34.2, 36.2, 39.7, 41.7, 41.4, 38.7, 35.4, 31.6]
    }
  ]
}
```

---

### Actionable Recommendations

- **Day-of Weather Adjustment**: Execute the 2-hour pre-event baseline calibration at 12:00 PM tomorrow to compute the final additive day-of adjustment factor based on real-time temperature telemetry.
- **AMI Polling Priority**: Increase 15-minute interval read priority across the 142 commercial meter endpoints during the event window (13:00–19:00) to ensure zero interval data latency.
- **Underperformance Alerting**: Configure real-time variance alarms to trigger if any commercial participant deviates >15% above their target post-curtailment trajectory during the first 30 minutes of dispatch.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "DR_EVENT_DISPATCH_NOTIFICATION",
  "scope": "Commercial Demand Response Portfolio",
  "event_date": "Tomorrow",
  "event_window": "14:00 - 18:00 EST",
  "target_curtailment_mw": 10.10,
  "recipient_count": 142,
  "notification_channel": "Automated DR Portal & OpenADR 2.0b Signal",
  "requires_hitl_approval": true,
  "status": "AWAITING_OPERATOR_CONFIRMATION"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Compare the 'High 4-in-5' baseline methodology against weather-adjusted baseline algorithms for commercial refrigerating facilities."

**Agent Response:**
### Executive Summary
**For commercial refrigeration facilities, standard "High 4-in-5" baseline calculations introduce systematic negative bias and high Mean Absolute Percentage Error (MAPE up to 18.4%) during heatwave dispatch days due to nonlinear thermodynamic lift on compressor head pressure. Weather-adjusted multi-variable regression baselines (incorporating Cooling Degree Hours and ambient enthalpy) reduce estimation error to under 3.8% MAPE, eliminating unearned financial risk and ensuring regulatory settlement accuracy under FERC/PUC standards. Adoption of weather-normalized CBL models is strongly recommended for commercial cold storage and supermarket cohorts to prevent systemic baseline degradation during grid emergencies.**

---

### Data Presentation

The comparative analysis below evaluates the performance of the **High 4-in-5 Baseline** (standard historical averaging) against a **Weather-Adjusted Multi-Variable Regression Algorithm** (using local AMI interval data paired with dry-bulb temperature and relative humidity inputs) for a representative 750 kW commercial refrigeration facility during peak summer event conditions.

| Metric | High 4-in-5 Baseline | Weather-Adjusted Baseline (Target) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Event Hour Under-Estimation (kW)** | -115.0 kW | -5.0 kW | -95.7% Error Reduction | **Critical** (High 4-in-5) / **Normal** (Weather-Adjusted) |
| **Mean Absolute Percentage Error (MAPE)** | 18.4% | 3.6% | -80.4% | **Critical** |
| **Model Mean Bias Error (MBE)** | -14.2% (Under-predicts) | +0.4% (Neutral) | -97.2% | **Warning** |
| **Goodness-of-Fit ($R^2$ on Heatwave Days)** | 0.61 | 0.94 | +54.1% | **Critical** |
| **Settlement Revenue Volatility ($/MWh)** | $142.50 / MWh (Imbalance Risk) | $8.20 / MWh (Tolerance Band) | -94.2% | **Warning** |
| **Susceptibility to Pre-Cooling Distortion** | High (Uncalibrated) | Low (Thermal Inertia Modeled) | -75.0% | **Warning** |

---

### Key Technical Findings

1. **Thermodynamic Sensitivity of Refrigeration Loads**:
   - Commercial refrigeration facilities operate with continuous 24/7 base process loads, but their energy intensity varies nonlinearly with ambient temperature due to condenser heat-rejection requirements and defrost cycles.
   - On extreme event days where temperatures exceed preceding non-event baseline days by 8°F to 15°F, the **High 4-in-5 methodology** fails to capture the elevated uncurtailed baseline counterfactual, leading to severe under-crediting of actual demand response curtailment.

2. **Same-Day Adjustment Limitations**:
   - Applying a standard additive same-day adjustment factor (e.g., 2-4 hours pre-event window) to High 4-in-5 can partially mitigate under-prediction; however, commercial refrigeration facilities frequently utilize pre-cooling or variable defrost schedules, which artificially skews pre-event calibration windows.

3. **Weather-Adjusted Multi-Variable Regression (ASHRAE / IPMVP Option C & CalTRACK Standard)**:
   - Utilizes hour-of-day fixed effects, dry-bulb temperature, Cooling Degree Hours (CDH), and enthalpy to dynamically adjust the CBL.
   - Provides consistent baselines across both moderate and extreme grid conditions without penalizing the customer during peak-stress heatwaves.

---

### Visualization Output

The chart configuration has been generated to depict the event-day divergence between unadjusted High 4-in-5 and Weather-Adjusted Regression relative to actual counterfactual consumption:

```json
{
  "title": "Hourly CBL Model Performance for Commercial Cold Storage (Event Day)",
  "xAxis": "Hour of Day (HE01 - HE24)",
  "yAxis": "Load (kW)",
  "series": [
    {
      "name": "Actual Uncurtailed Counterfactual Load (kW)",
      "data": [420, 410, 405, 400, 415, 440, 480, 520, 560, 610, 650, 690, 720, 745, 755, 740, 710, 660, 600, 540, 490, 460, 435, 425]
    },
    {
      "name": "High 4-in-5 Baseline (Standard Unadjusted) (kW)",
      "data": [415, 405, 400, 395, 405, 425, 450, 480, 510, 540, 570, 600, 620, 635, 640, 630, 610, 575, 530, 490, 460, 440, 425, 418]
    },
    {
      "name": "Weather-Adjusted Regression CBL (CDH + Enthalpy) (kW)",
      "data": [418, 408, 404, 398, 412, 438, 476, 515, 555, 605, 646, 685, 715, 740, 750, 736, 705, 655, 595, 536, 488, 458, 432, 422]
    }
  ]
}
```

---

### Actionable Recommendations

- **Transition Commercial Refrigeration Cohorts to Weather-Adjusted CBL**: Reclassify commercial cold storage and grocery refrigeration accounts under a multi-variable temperature-regression CBL model to maintain $R^2 \ge 0.90$ settlement fidelity.
- **Implement Enthalpy / Wet-Bulb Correction Factors**: For facilities using evaporative condensers, incorporate relative humidity/wet-bulb temperature into the regression equation to capture latent heat rejection dynamics.
- **Enforce Anti-Gaming Pre-Cooling Detection**: Restrict simple additive pre-event window adjustments for facilities with demonstrated pre-cooling capabilities, utilizing baseline model fits calculated over a 30-day non-event baseline pool.
- **Validate Data Streams via VEE Rules**: Ensure 15-minute AMI telemetry streams pass interval data validation, editing, and estimation (VEE) checks before executing baseline recalculations.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Publish final verified demand response curtailment performance calculations to the wholesale market settlement portal."

**Agent Response:**
### 1. Executive Summary
**Direct transmission and publication of verified Demand Response (DR) curtailment performance data to the wholesale market settlement portal constitutes a binding financial transaction.** **Under utility compliance and safety guardrails, autonomous publishing of final financial settlement records is strictly prohibited without explicit Human-in-the-Loop (HITL) review.** **To proceed with settlement submission, event identifiers, interval baseline methodologies, and aggregated performance metrics must be validated and confirmed by an authorized settlement operator.**

---

### 2. Data Presentation (Markdown Table)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Wholesale Submission Status** | Pending Operator Approval | Published / Reconciled | N/A | **Warning** |
| **Telemetry Ingestion & VEE** | Complete (100% Intervals) | 100.0% Target | 0.0% | **Normal** |
| **Baseline Methodology Audit** | Compliant (ISO/RTO 10-in-10) | Standard Approved Model | 0.0% | **Normal** |
| **Settlement Run Type** | Final True-Up Submission | Final Market Cycle | N/A | **Normal** |
| **Financial Exposure / Settlement** | Pending HITL Sign-off | Cleared Value | N/A | **Warning** |

---

### 3. Visualization Trigger

```json
{
  "chart_type": "line",
  "title": "Demand Response Event: Aggregated CBL vs. Actual Load Profile",
  "data": {
    "timestamps": ["13:00", "14:00", "15:00", "16:00", "17:00", "18:00"],
    "baseline_load_mw": [125.4, 128.2, 131.0, 134.5, 130.8, 124.1],
    "actual_load_mw": [124.9, 102.5, 98.1, 95.4, 110.2, 123.5],
    "curtailment_mw": [0.5, 25.7, 32.9, 39.1, 20.6, 0.6]
  }
}
```

---

### 4. Actionable Recommendations

* **Review Settlement Aggregations:** Validate that Customer Baseline Load (CBL) adjustments (day-of weather adjustment / symmetric additive adjustment) strictly comply with ISO/RTO tariff schedules.
* **Audit Outliers & Exclusions:** Confirm that baseline candidate days excluded due to prior event dispatch or abnormal grid conditions are documented.
* **Execute Authorization:** Submit manual authorization using the Tier 2 confirmation workflow below to initiate transmission to the wholesale settlement portal.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "WHOLESALE_MARKET_SETTLEMENT_PUBLICATION",
  "agent": "customer_baseline_load_cbl_calculator",
  "target_system": "Wholesale Market Settlement Portal (ISO/RTO Interface)",
  "details": {
    "operation": "TRANSMIT_VERIFIED_CURTAILMENT_RECORDS",
    "verification_status": "AMI_INTERVALS_VERIFIED",
    "requires_hitl_approval": true
  },
  "confirmation_prompt": "Are you sure you want to authorize the final publication and financial transmission of DR curtailment performance records to the wholesale market settlement portal?"
}
```
