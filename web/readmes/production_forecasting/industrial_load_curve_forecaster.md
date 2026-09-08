# ⚡ Industrial Load Curve Forecaster

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of industrial load curve forecaster is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Industrial Load Curve Forecaster Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank industrial load curve forecaster events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.industrial_load_curve_forecaster_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the forecasted 15-minute peak electric demand for the steel mill and heavy manufacturing park tomorrow afternoon?"

**Agent Response:**
### Executive Summary
**The aggregate forecasted 15-minute peak electric demand for the steel mill and heavy manufacturing park tomorrow afternoon is projected to reach 239.40 MW at 13:30 (1:30 PM). The steel mill's Electric Arc Furnace (EAF) batch cycle accounts for 148.20 MW (61.9% of total), while the heavy manufacturing park peaks at 96.10 MW at 14:15. Both facilities remain within scheduled nodal capacity limits, with model forecast confidence validated at a 95% Confidence Interval (±3.82% MAPE).**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Combined 15-Min Peak Demand (13:30)** | 239.40 MW | 225.00 MW | +6.40% | Warning |
| **Steel Mill Peak Demand (13:30)** | 148.20 MW | 140.00 MW | +5.86% | Warning |
| **Manufacturing Park Peak Demand (14:15)** | 96.10 MW | 92.00 MW | +4.46% | Normal |
| **Coincident Peak Demand (13:45)** | 238.80 MW | 225.00 MW | +6.13% | Warning |
| **Afternoon Energy Consumption (12:00–18:00)** | 1,248.65 MWh | 1,200.00 MWh | +4.05% | Normal |
| **Forecast Model Accuracy (MAPE)** | 3.82% | < 5.00% | -23.60% | Normal |
| **95% Confidence Interval Band** | ±9.15 MW | ±11.25 MW | -18.67% | Normal |

---

### Visualization Triggers

**Recommended Chart Type:** Time-Series Interval Line Chart (15-minute resolution across the afternoon peak window, 12:00–18:00).

```json
{
  "chart_type": "line",
  "title": "Tomorrow Afternoon 15-Minute Load Curve Forecast (MW)",
  "xAxis": [
    "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45",
    "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45",
    "16:00", "16:15", "16:30", "16:45", "17:00", "17:15", "17:30", "17:45", "18:00"
  ],
  "series": [
    {
      "name": "Steel Mill (EAF Melt Cycle)",
      "data": [112.4, 115.1, 118.0, 122.3, 134.8, 142.5, 148.2, 145.0, 138.6, 129.4, 124.0, 130.5, 141.0, 146.8, 144.2, 137.5, 128.0, 121.3, 118.5, 115.0, 110.2, 108.4, 106.0, 104.5, 102.0]
    },
    {
      "name": "Heavy Manufacturing Park",
      "data": [78.5, 79.2, 81.0, 83.4, 86.0, 88.5, 91.2, 93.8, 95.4, 96.1, 94.8, 93.0, 91.5, 89.0, 87.2, 85.0, 83.1, 80.5, 78.0, 76.2, 74.5, 72.0, 70.4, 68.8, 67.5]
    },
    {
      "name": "Combined Nodal Demand",
      "data": [190.9, 194.3, 199.0, 205.7, 220.8, 231.0, 239.4, 238.8, 234.0, 225.5, 218.8, 223.5, 232.5, 235.8, 231.4, 222.5, 211.1, 201.8, 196.5, 191.2, 184.7, 180.4, 176.4, 173.3, 169.5]
    }
  ]
}
```

---

### Actionable Recommendations
- **Pre-Position Spinning Reserves:** Coordinate with Generation Dispatch to allocate 15 MW of supplemental ramping reserves between 13:00 and 15:30 to accommodate steel mill EAF tap-to-tap thermal transitions.
- **Demand Response (DR) Pre-Notification:** Issue an informational advisory to the industrial park coordinator regarding the elevated peak between 13:15 and 14:00, evaluating potential voluntary peak-shaving credits.
- **Substation Thermal Monitoring:** Verify that feeder thermal ratings at the primary interconnecting 230/115 kV transformation bank have sufficient cooling headroom for the forecasted 239.4 MW load.
- **Continuous Telemetry Tracking:** Monitor real-time SCADA interval feeds against the 95% confidence interval band; re-run intra-day forecasts if variance exceeds 5% at 11:00 AM tomorrow.

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate factory production shift schedules and arc furnace operational cycles to detect demand spike correlations."

**Agent Response:**
### 1. Executive Summary
**A strong positive correlation ($r = 0.94$) has been identified between facility shift changeover cycles (06:00, 14:00, 22:00) and high-magnitude Electric Arc Furnace (EAF) scrap meltdown sequences.** **Coincident energization of auxiliary melting equipment and bore-in arcing cycles produces uncoordinated peak ramp rates reaching 3.2 MW/min, breaching the 115.0 MW feeder thermal threshold by up to 20.2%.** **Staggering furnace tap-to-tap charge cycles by 35 minutes post-shift handover mitigates coincident demand spikes below critical limits without compromising overall plant throughput.**

---

### 2. Quantitative Telemetry & Correlation Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Coincident Demand (MW)** | 138.20 MW | 115.00 MW | +20.17% | **Critical** |
| **Shift 1/2 Ramp Rate ($\Delta$MW/min)** | 3.20 MW/min | 1.50 MW/min | +113.33% | **Warning** |
| **Meltdown Stage Mean Power** | 132.80 MW | 80.00 MW | +66.00% | **Critical** |
| **Refining Stage Mean Power** | 69.85 MW | 66.50 MW | +5.04% | **Normal** |
| **Power Factor (Arc Ignition Phase)** | 0.78 lagging | 0.92 lagging | -15.22% | **Warning** |
| **Forecast Model MAPE (24h Interval)**| 3.82% | < 5.00% | -23.60% | **Normal** |

---

### 3. Visualization Trigger

**Recommended Chart:** Time-Series Multi-Line Chart tracking diurnal factory load curves against furnace cycle milestones and feeder threshold limits.

```json
{
  "chart_type": "line",
  "title": "Industrial Feeder Load Profile vs. Arc Furnace Meltdown Cycles",
  "data": {
    "labels": [
      "06:00 (Shift 1 Start)",
      "06:30 (Bore-in/Meltdown)",
      "07:00 (Full Melting)",
      "08:30 (Refining)",
      "14:00 (Shift 2 Start)",
      "14:30 (Bore-in/Meltdown)",
      "15:00 (Full Melting)",
      "16:30 (Refining)",
      "22:00 (Shift 3 Start)",
      "22:30 (Bore-in/Meltdown)",
      "23:00 (Full Melting)"
    ],
    "datasets": [
      {
        "label": "Aggregated Load (MW)",
        "data": [42.5, 118.4, 132.8, 68.2, 46.0, 124.6, 138.2, 71.5, 38.2, 112.0, 126.5],
        "borderColor": "#D9381E",
        "fill": false
      },
      {
        "label": "Baseline Forecast (MW)",
        "data": [40.0, 75.0, 80.0, 65.0, 42.0, 78.0, 82.0, 68.0, 36.0, 70.0, 75.0],
        "borderColor": "#1E88E5",
        "borderDash": [5, 5],
        "fill": false
      },
      {
        "label": "Feeder Coincident Threshold (MW)",
        "data": [115.0, 115.0, 115.0, 115.0, 115.0, 115.0, 115.0, 115.0, 115.0, 115.0, 115.0],
        "borderColor": "#FFA000",
        "borderDash": [2, 2],
        "fill": false
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

- **Stagger EAF Melt Sequencing**: Coordinate with the industrial facility's energy management system (EMS) to introduce a mandatory 35-minute offset between shift start times and EAF first-bucket scrap charging, smoothing coincident ramp rates below 1.5 MW/min.
- **Dynamic VAR Compensation (SVC/STATCOM)**: Verify static VAR compensator dynamic response timing during the initial bore-in phase (06:20–07:10 and 14:20–15:10) to correct sub-0.80 lagging power factor conditions and reduce feeder I²R losses.
- **Short-Term Predictive Load Model Integration**: Ingest real-time SCADA scrap basket charging signals into the 15-minute Day-Ahead/Hour-Ahead production forecasting model to keep MAPE under 4.0%.
- **Industrial Demand Response (IDR) Tier 2 Escalation**: If grid operating mode shifts to Emergency, prepare an automated DR signal dispatch payload for human-in-the-loop authorization.

---

### [TIER 2 ACTION REQUIRED]
*Any physical command dispatching automated industrial breaker trip limits, curtailment signals, or modifying contractual intertie setpoints requires explicit utility dispatcher sign-off.*

```json
{
  "action_type": "INDUSTRIAL_DEMAND_RESPONSE_DISPATCH",
  "target_substation": "SUB_138KV_IND_EAST",
  "facility_id": "FAC_STEEL_EAF_04",
  "proposed_curtailment_mw": 23.2,
  "execution_window": "14:30 - 15:30 UTC",
  "requires_hitl_approval": true,
  "dispatcher_confirmation_status": "PENDING"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue an automated peak-shaving alert to industrial customers requesting voluntary production modulation between 14:00 and 16:00."

**Agent Response:**
### **Executive Summary**
**Industrial load curve forecasting indicates a projected system peak demand exceeding nominal operating thresholds between 14:00 and 16:00.** Voluntary production modulation across major industrial feeders is projected to mitigate regional transformer overload and maintain grid reliability. **Pursuant to enterprise safety guardrails, automated mass communication to external customers constitutes a Tier 2 operation and cannot be dispatched autonomously without Human-In-The-Loop (HITL) authorization.**

---

### **Data Presentation**

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Forecasted Peak Load (14:00–16:00)** | 482.4 MW | 420.0 MW | +14.86% | **Warning** |
| **Required Peak-Shaving Relief** | 45.0 MW | 0.0 MW | N/A | **Warning** |
| **Industrial Class Contribution** | 218.6 MW | 180.0 MW | +21.44% | **Warning** |
| **Model Forecast MAPE** | 3.12% | < 5.00% | -1.88% | **Normal** |
| **95% Confidence Upper Bound** | 497.1 MW | 450.0 MW | +10.47% | **Critical** |

---

### **Visualization Trigger**

*Recommended Visualization*: **Time-Series Line Chart** displaying the baseline forecast, modulated industrial load curve, and capacity limits between 12:00 and 18:00.

```json
{
  "chart_type": "line",
  "title": "Industrial & System Load Curve Forecast (12:00 - 18:00)",
  "x_axis": {
    "label": "Time Interval",
    "categories": ["12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]
  },
  "y_axis": {
    "label": "Megawatts (MW)"
  },
  "series": [
    {
      "name": "Forecasted Total System Load",
      "data": [390.2, 435.0, 482.4, 478.1, 465.0, 410.5, 380.0]
    },
    {
      "name": "Target Threshold Capacity",
      "data": [420.0, 420.0, 420.0, 420.0, 420.0, 420.0, 420.0]
    },
    {
      "name": "Post-Modulation Estimated Load",
      "data": [390.2, 435.0, 437.4, 433.1, 420.0, 410.5, 380.0]
    }
  ]
}
```

---

### **Actionable Recommendations**
* **Approve Tier 2 Demand-Response Dispatch**: Validate the proposed peak-shaving relief envelope (45.0 MW) and authorize transmission of the voluntary curtailment notification to enrolled industrial accounts.
* **Coordinate with Grid Operations**: Confirm that industrial substations and feeder tie-lines are staged to monitor real-time telemetry starting at 13:30.
* **Review Customer Bidding/Incentive Baselines**: Ensure tariff accounting and peak-shaving event settlement windows are initialized in accordance with PUC/FERC compliance schedules.

---

### **[TIER 2 ACTION REQUIRED]**

```json
{
  "action_type": "EXTERNAL_MASS_COMMUNICATION_AND_DEMAND_RESPONSE_ALERT",
  "operating_domain": "Production Forecasting / Demand Response",
  "target_audience": "Enrolled Tier-1 & Tier-2 Industrial Customer Accounts",
  "event_window": {
    "start_time": "14:00:00Z",
    "end_time": "16:00:00Z",
    "date": "CURRENT_OPERATIONAL_DATE"
  },
  "curtailment_target_mw": 45.0,
  "execution_mode": "VOLUNTARY_MODULATION",
  "requires_hitl_approval": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```

*Please confirm approval to dispatch this notification through the Demand Response / Customer Operations system.*
