# ⚡ Water Usage Discharge Reporter

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of water usage discharge reporter is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Water Usage Discharge Reporter Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank water usage discharge reporter events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.water_usage_discharge_reporter_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did thermal cooling water discharge temperatures at River Generating Plant comply with NPDES permit environmental limits today?"

**Agent Response:**
### Executive Summary
**Thermal cooling water discharge temperatures at River Generating Plant remained in full compliance with National Pollutant Discharge Elimination System (NPDES) permit environmental limits throughout today's monitoring cycles.** **The maximum recorded effluent discharge temperature reached 84.1°F against the regulatory ceiling of 90.0°F, while the maximum thermal rise ($\Delta T$) reached 14.2°F against the allowable permit threshold of 15.0°F.** **Continuous CEMS/telemetry monitoring confirmed zero exceedance events and a 100% environmental compliance record for the 24-hour reporting window.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Discharge Temp** | 84.1 °F | 90.0 °F (Max Limit) | -6.56% | **Normal** |
| **Average Discharge Temp** | 79.8 °F | 90.0 °F (Max Limit) | -11.33% | **Normal** |
| **Max Thermal Rise ($\Delta T$)** | 14.2 °F | 15.0 °F (Max Limit) | -5.33% | **Warning** *(Approaching limit at peak load)* |
| **Intake Water Temp (Ambient)** | 69.9 °F | N/A (Baseline) | N/A | **Normal** |
| **Average Discharge Flow Rate** | 412 MGD | 450 MGD (Permit Cap) | -8.44% | **Normal** |
| **NPDES Exceedance Count** | 0 events | 0 events | 0.00% | **Normal** |
| **Telemetry VEE Success Rate** | 100.0% | 99.5% | +0.50% | **Normal** |

---

### Visualization Trigger

**Recommended Visualization:** Time-Series Line Chart illustrating hourly effluent discharge temperature and thermal rise ($\Delta T$) alongside NPDES regulatory permit caps.

```json
{
  "title": "River Generating Plant - Daily Thermal Discharge vs NPDES Limits",
  "chart_type": "line",
  "xAxis": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "23:00"],
  "series": [
    {
      "name": "Discharge Temp (°F)",
      "data": [76.4, 75.8, 79.2, 83.5, 84.1, 81.6, 78.3]
    },
    {
      "name": "NPDES Max Temp Limit (°F)",
      "data": [90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0]
    },
    {
      "name": "Thermal Delta-T (°F)",
      "data": [8.2, 7.9, 11.4, 13.8, 14.2, 12.1, 9.5]
    },
    {
      "name": "NPDES Max Delta-T Limit (°F)",
      "data": [15.0, 15.0, 15.0, 15.0, 15.0, 15.0, 15.0]
    }
  ]
}
```

---

### Actionable Recommendations

- **Thermal Rise Monitoring**: Note that peak thermal rise ($\Delta T$) approached within 0.8°F of the 15.0°F permit threshold between 15:00 and 17:00 during peak generation. Maintain cooling tower auxiliary fan readiness if ambient river intake temperatures increase tomorrow.
- **Automated DMR Archiving**: Log today's telemetry payload into the monthly Discharge Monitoring Report (DMR) database for automated submission to the EPA / State Department of Environmental Protection.
- **Intake Sensor Calibration**: Schedule routine bi-weekly calibration of intake and discharge thermistors to maintain telemetry validation accuracy above 99.5%.

### Example 2: Trend & Comparative Analysis
**User:** "Track consumptive water withdrawal volumes and effluent pH/chlorine levels against state Department of Environmental Protection rules."

**Agent Response:**
### Executive Summary
**Consumptive water withdrawal volumes and effluent water quality parameters are currently tracking within state Department of Environmental Protection (DEP) National Pollutant Discharge Elimination System (NPDES) permit limits across all monitored outfalls. Daily consumptive withdrawal is operating at 14.8 MGD against an authorized cap of 18.0 MGD, while continuous effluent telemetry indicates compliant pH (7.3 s.u.) and Total Residual Chlorine (0.031 mg/L). Outfall 002 peak chlorine concentrations reached 96% of the regulatory threshold during thermal cooling cycles, warranting ongoing telemetry surveillance and biocide dosing adjustments.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target Limit | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Intake Volume** | 42.6 MGD | 50.0 MGD (Max Authorized) | -14.8% | Normal |
| **Consumptive Water Loss** | 14.8 MGD | 18.0 MGD (Daily Cap) | -17.8% | Normal |
| **Effluent Discharge Flow** | 27.8 MGD | 32.0 MGD (Baseline) | -13.1% | Normal |
| **Effluent pH (Outfall 001)** | 7.3 s.u. | 6.0 – 9.0 s.u. (Permit Band) | 0.0% (In-Band) | Normal |
| **Effluent pH (Outfall 002)** | 8.1 s.u. | 6.0 – 9.0 s.u. (Permit Band) | +10.0% vs Midpoint | Normal |
| **Total Residual Chlorine (TRC - Outfall 001)** | 0.031 mg/L | 0.050 mg/L (Max Daily) | -38.0% | Normal |
| **Total Residual Chlorine (TRC - Outfall 002 Peak)** | 0.048 mg/L | 0.050 mg/L (Max Daily) | -4.0% | Warning |
| **Effluent Temperature ($\Delta T$)** | 3.4 °F | 5.0 °F (Mixing Zone Max) | -32.0% | Normal |

---

### Visualization Triggers

A **Multi-Axis Time-Series Line Chart** is recommended to track hourly effluent pH and Total Residual Chlorine fluctuations alongside consumptive withdrawal volumes against state DEP regulatory ceilings.

```json
{
  "chart_type": "line",
  "title": "Consumptive Water Withdrawal & Effluent Compliance (24-Hour Telemetry)",
  "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
  "datasets": [
    {
      "label": "Consumptive Withdrawal (MGD)",
      "data": [14.2, 14.5, 15.8, 16.4, 15.9, 14.8, 14.1],
      "unit": "MGD",
      "regulatory_threshold": 18.0,
      "color": "#1f77b4"
    },
    {
      "label": "Effluent pH (s.u.)",
      "data": [7.2, 7.4, 7.6, 8.1, 7.8, 7.3, 7.1],
      "unit": "pH",
      "regulatory_min": 6.0,
      "regulatory_max": 9.0,
      "color": "#2ca02c"
    },
    {
      "label": "Total Residual Chlorine (mg/L)",
      "data": [0.028, 0.035, 0.042, 0.048, 0.039, 0.031, 0.025],
      "unit": "mg/L",
      "regulatory_threshold": 0.050,
      "color": "#d62728"
    }
  ]
}
```

---

### Actionable Recommendations

- **Chlorine Dechlorination Feed Optimization**: Trim the sodium bisulfite dechlorination feed rates at Outfall 002 during mid-day peak chlorination cycles to widen the margin below the 0.050 mg/L TRC regulatory cap.
- **Automate Monthly DEP DMR Compilation**: Queue the validated 15-minute telemetry intervals for automated population of the State DEP monthly Discharge Monitoring Report (DMR / eDMR).
- **Consumptive Use Metering Calibration**: Schedule quarterly verification of acoustic flow meters on primary intake and cooling tower blowdown lines to maintain strict VEE compliance.
- **pH Sensor Redundancy Check**: Perform routine 2-point buffer calibration on the dual-redundant pH probes at Outfall 002 following elevated afternoon readings.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate the monthly National Pollutant Discharge Elimination System (NPDES) discharge monitoring report for regulatory filing."

**Agent Response:**
### Executive Summary
**The monthly National Pollutant Discharge Elimination System (NPDES) compliance assessment confirms zero permit exceedances across all active industrial outfalls during the reporting period. All key effluent metrics—including Total Suspended Solids (TSS), Oil & Grease, Biochemical Oxygen Demand (BOD₅), Total Residual Chlorine, and thermal discharge differential ($\Delta T$)—remained well within Clean Water Act (CWA) and state regulatory limits. Overall discharge audit compliance stands at 100%, with telemetry continuous-monitoring data achieving a 99.8% VEE (Validation, Estimation, and Editing) pass rate.**

---

### Data Presentation: Monthly NPDES Discharge Monitoring Summary

| Metric | Current Value | Baseline / Target (Permit Limit) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Effluent Flow Rate (Outfall 001)** | 18.40 MGD | 25.00 MGD (Max Daily) | -26.40% | Normal |
| **Total Suspended Solids (TSS)** | 14.80 mg/L | 30.00 mg/L (Monthly Avg) / 45.00 mg/L (Max) | -50.67% | Normal |
| **Oil & Grease** | 4.20 mg/L | 10.00 mg/L (Monthly Avg) / 15.00 mg/L (Max) | -58.00% | Normal |
| **Biochemical Oxygen Demand (BOD₅)**| 8.50 mg/L | 30.00 mg/L (Daily Max) | -71.67% | Normal |
| **Total Residual Chlorine (TRC)** | 0.018 mg/L | 0.050 mg/L (Daily Max) | -64.00% | Normal |
| **pH (Range)** | 7.10 – 7.80 S.U. | 6.00 – 9.00 S.U. (Permit Window) | In-Band | Normal |
| **Thermal Discharge ($\Delta T$)** | 3.20 °F | 5.00 °F (Mixing Zone Limit) | -36.00% | Normal |
| **Cooling Tower Blowdown Flow** | 4.10 MGD | 6.50 MGD (Permit Cap) | -36.92% | Normal |
| **Heavy Metals (Total Copper)** | 0.006 mg/L | 0.018 mg/L (Daily Max) | -66.67% | Normal |
| **Audit Compliance Rate** | 100.0% | 100.0% | 0.00% | Normal |

---

### Visualization Trigger
- **Recommended Visualization**: Multi-Parameter Grouped Bar Chart comparing observed peak values against state/EPA permit caps across all monitored outfalls.

```json
{
  "chart_type": "bar",
  "title": "NPDES Monthly Effluent Discharge Monitoring vs Permit Limits",
  "categories": [
    "Flow Rate (MGD)",
    "TSS (mg/L)",
    "Oil & Grease (mg/L)",
    "BOD5 (mg/L)",
    "Total Residual Chlorine (mg/L)",
    "pH Max (S.U.)",
    "Thermal Discharge Delta-T (°F)"
  ],
  "series": [
    {
      "name": "Permit Daily Max Limit",
      "data": [25.0, 45.0, 15.0, 30.0, 0.05, 9.0, 5.0]
    },
    {
      "name": "Reported Monthly Max Value",
      "data": [18.4, 14.8, 4.2, 8.5, 0.018, 7.8, 3.2]
    }
  ]
}
```

---

### Actionable Recommendations
1. **Prepare EPA NetDMR Electronic Submission File**: Package the validated continuous monitoring and grab-sample laboratory records into the standard XML/CSV format for electronic filing.
2. **Conduct Semi-Annual Sensor Calibration**: Verify calibration curves for Outfall 001 online pH meters, turbidimeters, and thermal differential thermocouples prior to the upcoming quarter.
3. **Archive Chain-of-Custody (CoC) Records**: Ensure certified environmental lab analytical sheets for heavy metals and BOD₅ are cross-referenced and stored in the environmental compliance archive for the mandatory 5-year retention period.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action: "SUBMIT_NPDES_ELECTRONIC_DMR"
  target_portal: "EPA NetDMR / State Environmental Protection Agency"
  reporting_period: "Monthly - Preceding Calendar Month"
  facility_id: "NPDES-FAC-004812"
  compliance_officer_signoff_required: true
  description: "Formal electronic signature and cryptographic submittal of the monthly NPDES Discharge Monitoring Report (DMR) to state and federal regulatory repositories. Requires certified Designated Representative (RO/DMR Signatory) authorization."
```
