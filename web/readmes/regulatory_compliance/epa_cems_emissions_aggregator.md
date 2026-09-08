# ⚡ Epa Cems Emissions Aggregator

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of epa cems emissions aggregator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Epa Cems Emissions Aggregator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank epa cems emissions aggregator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.epa_cems_emissions_aggregator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did NOx or SO2 continuous emissions monitoring (CEMS) readings at Generating Station Unit 1 exceed EPA 40 CFR Part 75 hourly limits?"

**Agent Response:**
### Executive Summary
**A comprehensive review of the Continuous Emissions Monitoring System (CEMS) telemetry for Generating Station Unit 1 indicates that neither $\text{NO}_x$ emission rates nor $\text{SO}_2$ mass emission rates exceeded EPA 40 CFR Part 75 hourly compliance thresholds during the evaluated operational period.** **Peak hourly $\text{NO}_x$ reached $0.145\text{ lb/MMBtu}$ against the regulatory limit of $0.150\text{ lb/MMBtu}$ ($96.7\%$ of limit), while peak hourly $\text{SO}_2$ mass rate reached $188.0\text{ lb/hr}$ against the standard threshold of $200.0\text{ lb/hr}$ ($94.0\%$ of limit).** **All primary analyzer calibrations, daily zero/span drift checks, and data acquisition handling system (DAHS) data validation checks remain compliant with Part 75 QA/QC standards.**

---

### Data Presentation (EPA 40 CFR Part 75 Compliance Aggregation)

| Metric | Current Value (Peak / Avg) | Baseline / Target (Part 75 Limit) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **$\text{NO}_x$ Emission Rate (Peak)** | $0.145\text{ lb/MMBtu}$ | $0.150\text{ lb/MMBtu}$ | $-3.33\%$ | **Warning** |
| **$\text{NO}_x$ Emission Rate (24-Hr Avg)** | $0.131\text{ lb/MMBtu}$ | $0.150\text{ lb/MMBtu}$ | $-12.67\%$ | **Normal** |
| **$\text{SO}_2$ Mass Emission Rate (Peak)** | $188.00\text{ lb/hr}$ | $200.00\text{ lb/hr}$ | $-6.00\%$ | **Warning** |
| **$\text{SO}_2$ Mass Emission Rate (24-Hr Avg)** | $163.00\text{ lb/hr}$ | $200.00\text{ lb/hr}$ | $-18.50\%$ | **Normal** |
| **Diluent $\text{CO}_2$ Concentration** | $12.4\%$ | $11.5\% - 14.0\%$ | $0.00\%$ | **Normal** |
| **Stack Volumetric Flow Rate** | $1,240,000\text{ SCFH}$ | $1,350,000\text{ SCFH}$ | $-8.15\%$ | **Normal** |
| **CEMS Data Availability (Quarter-to-Date)** | $99.4\%$ | $\ge 95.0\%$ | $+4.63\%$ | **Normal** |
| **Daily Zero/Span Calibration Drift ($\text{NO}_x/\text{SO}_2$)** | $< 1.2\%$ of Span | $\le 2.5\%$ of Span | $-52.00\%$ | **Normal** |

---

### Visualization Trigger

**Recommended Chart Type**: Time-Series Multi-Axis Line Chart (24-Hour Emissions Profile vs. EPA Limits)

```json
{
  "chart_type": "line",
  "title": "Generating Station Unit 1 - 24-Hour CEMS NOx and SO2 vs EPA Part 75 Limits",
  "labels": ["00:00", "02:00", "04:00", "06:00", "08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"],
  "datasets": [
    {
      "label": "NOx Emission Rate (lb/MMBtu)",
      "data": [0.118, 0.115, 0.122, 0.134, 0.141, 0.139, 0.145, 0.142, 0.138, 0.131, 0.125, 0.120],
      "borderColor": "#3b82f6",
      "fill": false
    },
    {
      "label": "NOx Part 75 Limit (lb/MMBtu)",
      "data": [0.150, 0.150, 0.150, 0.150, 0.150, 0.150, 0.150, 0.150, 0.150, 0.150, 0.150, 0.150],
      "borderColor": "#ef4444",
      "borderDash": [5, 5],
      "fill": false
    },
    {
      "label": "SO2 Mass Rate (lb/hr)",
      "data": [142.5, 138.2, 145.0, 168.4, 182.1, 179.5, 188.0, 181.2, 174.6, 162.0, 150.3, 144.1],
      "borderColor": "#10b981",
      "fill": false
    },
    {
      "label": "SO2 Part 75 Limit (lb/hr)",
      "data": [200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0, 200.0],
      "borderColor": "#f59e0b",
      "borderDash": [5, 5],
      "fill": false
    }
  ]
}
```

---

### Actionable Recommendations

- **Selective Catalytic Reduction (SCR) Tuning**: Although no regulatory exceedance occurred, $\text{NO}_x$ peaked at $96.7\%$ of the hourly threshold during peak load hours ($12:00\text{--}14:00$). Recommend inspecting ammonia injection grid (AIG) flow distribution and optimizing reagent dosing ahead of peak dispatch.
- **Flue Gas Desulfurization (FGD) Reagent Feed Check**: Ensure limestone/lime slurry feed rates and absorber recirculation pumps are operating at optimal stoichiometry during ramp-up periods to increase $\text{SO}_2$ operating margin.
- **Part 75 Missing Data Substitution Audit**: Verify that DAHS has not triggered standard Part 75 missing data substitution routines during calibration windows, ensuring raw analyzer values maintain verified certification flags.
- **Quarterly Electronic Data Reporting (EDR)**: Archive validated hourly CEMS emission logs for upcoming EPA Clean Air Markets Division (CAMD) XML file compilation.

### Example 2: Trend & Comparative Analysis
**User:** "Audit daily CEMS calibration drift test logs and relative accuracy test audits (RATA) across fossil generation smokestacks."

**Agent Response:**
### Executive Summary
**A comprehensive EPA 40 CFR Part 75/60 compliance audit of Continuous Emission Monitoring Systems (CEMS) was completed across all active fossil generation smokestacks, evaluating daily zero/span calibration drift logs and annual Relative Accuracy Test Audits (RATA). Stack 4 NOx analyzer exhibited an "Out-of-Control" condition exceeding the daily calibration drift limit (>5.0% span) and failing the RATA relative accuracy benchmark at 11.8% (threshold $\le$ 10.0%), invalidating hourly emissions data substitution. Immediate physical recalibration and recertification scheduling are required under Tier 2 environmental compliance protocols to avoid regulatory non-compliance and reporting penalties.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Stack 1 - NOx Daily Calibration Drift** | 1.40% span | $\le$ 2.50% span | -44.00% | Normal |
| **Stack 1 - SO₂ Daily Calibration Drift** | 1.80% span | $\le$ 2.50% span | -28.00% | Normal |
| **Stack 1 - Combined RATA Relative Accuracy** | 7.10% | $\le$ 10.00% RA | -29.00% | Normal |
| **Stack 2 - NOx Daily Calibration Drift** | 4.60% span | $\le$ 2.50% span | +84.00% | Warning |
| **Stack 2 - CO₂ Daily Calibration Drift** | 2.10% span | $\le$ 2.50% span | -16.00% | Normal |
| **Stack 2 - Combined RATA Relative Accuracy** | 9.20% | $\le$ 10.00% RA | -8.00% | Warning |
| **Stack 3 - NOx Daily Calibration Drift** | 1.20% span | $\le$ 2.50% span | -52.00% | Normal |
| **Stack 3 - Stack Flow Monitor Drift** | 2.30% span | $\le$ 3.00% span | -23.33% | Normal |
| **Stack 3 - Combined RATA Relative Accuracy** | 5.90% | $\le$ 10.00% RA | -41.00% | Normal |
| **Stack 4 - NOx Daily Calibration Drift** | 5.20% span | $\le$ 2.50% span | +108.00% | Critical |
| **Stack 4 - SO₂ Daily Calibration Drift** | 1.90% span | $\le$ 2.50% span | -24.00% | Normal |
| **Stack 4 - NOx RATA Relative Accuracy** | 11.80% | $\le$ 10.00% RA | +18.00% | Critical |
| **Fleetwide CEMS Data Availability Rate** | 97.42% | $\ge$ 95.00% | +2.55% | Normal |

---

### Visualization Triggers

**Recommended Visualization:** Grouped Multi-Series Bar Chart evaluating daily span drift against standard Part 75 calibration specifications and RATA Relative Accuracy percentages across individual fossil generation smokestacks.

```json
{
  "chart_type": "bar",
  "title": "CEMS Daily Calibration Drift & RATA Relative Accuracy Across Fossil Smokestacks",
  "labels": [
    "Stack-1 (NOx)",
    "Stack-1 (SO2)",
    "Stack-2 (NOx)",
    "Stack-2 (CO2)",
    "Stack-3 (NOx)",
    "Stack-3 (Flow)",
    "Stack-4 (NOx)",
    "Stack-4 (SO2)"
  ],
  "datasets": [
    {
      "label": "Daily Calibration Drift (%)",
      "data": [1.4, 1.8, 4.6, 2.1, 1.2, 2.3, 5.2, 1.9],
      "regulatory_threshold": 2.5
    },
    {
      "label": "RATA Relative Accuracy (%)",
      "data": [6.8, 7.4, 9.2, 6.1, 5.9, 8.4, 11.8, 7.1],
      "regulatory_threshold": 10.0
    }
  ]
}
```

---

### Actionable Recommendations

- **Isolate and Recalibrate Stack 4 NOx CEMS Analyzer**: Initiate immediate dual-point gas calibration (zero/high-span reference gas cylinders with certified EPA Protocol 1 standards) on Stack 4 to resolve the consecutive drift exceedance.
- **Implement Part 75 Missing Data Substitution Procedures**: Flag emissions data from Stack 4 as "Invalid/Out-of-Control" starting from the failed calibration timestamp; trigger the standard 40 CFR Part 75 Standard Missing Data Routine (maximum potential concentration / 90th percentile substitution) for regulatory reporting.
- **Schedule Immediate RATA Re-Test**: Contract an accredited source-testing firm within the mandatory 14-day compliance window to conduct a 9-run RATA re-audit on Stack 4 following instrument zero/span optical alignment and cell replacement.
- **Preventative Line Inspection for Stack 2**: Dispatch I&C technicians to inspect heated sample lines, probe filter blowback pressures, and chiller condensation traps on Stack 2 NOx line to arrest drift before crossing the out-of-control threshold.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "ENVIRONMENTAL_COMPLIANCE_INTERVENTION",
  "target_asset": "FOSSIL_GEN_STACK_4_NOX_CEMS",
  "action_details": {
    "operation": "DECLARE_OUT_OF_CONTROL_AND_APPLY_MISSING_DATA_SUBSTITUTION",
    "regulatory_framework": "40_CFR_PART_75_APPENDIX_A_AND_B",
    "justification": "Stack 4 NOx daily calibration drift at 5.20% and RATA Relative Accuracy at 11.80% exceed regulatory compliance limits.",
    "effective_period_start": "CURRENT_OPERATIONAL_INTERVAL",
    "dispatch_implication": "Unit generation derating evaluation if emissions substitution exceeds Title V hourly mass caps."
  },
  "required_approver": "Plant Environmental Compliance Manager / Chief Operations Engineer",
  "status": "PENDING_HUMAN_IN_THE_LOOP_APPROVAL"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Compile and sign the quarterly electronic EPA CEMS compliance data report for submission to the Clean Air Markets Division."

**Agent Response:**
### 1. Executive Summary
**The quarterly EPA Continuous Emission Monitoring System (CEMS) compliance aggregation has been compiled and validated against 40 CFR Part 75 quality assurance and reporting specifications.** **All generating unit primary monitoring systems maintained availability levels above the 95.0% regulatory threshold, ensuring standard missing data substitution routines remained within normal statistical bounds.** **Under EPA Clean Air Markets Division (CAMD) and ECMPS regulatory mandates, automated AI agents are strictly prohibited from applying legal electronic signatures; therefore, final certification and transmission require human authorization by the certified Designated Representative (DR).**

---

### 2. Data Presentation (Markdown Table)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Gross Generation (Gross Load)** | 1,420,580 MWh | 1,380,000 MWh | +2.94% | Normal |
| **Cumulative Total Heat Input** | 13,850,200 MMBtu | 13,500,000 MMBtu | +2.59% | Normal |
| **$\text{SO}_2$ Mass Emissions** | 412.80 Tons | 450.00 Tons (Allowance Cap) | -8.27% | Normal |
| **$\text{NO}_x$ Mass Emissions** | 682.40 Tons | 720.00 Tons (Program Limit) | -5.22% | Normal |
| **$\text{CO}_2$ Mass Emissions** | 1,412,720 Tons | 1,377,000 Tons (Projected) | +2.59% | Normal |
| **$\text{SO}_2$ CEMS Monitor Availability** | 98.65% | $\ge$ 95.00% (EPA Threshold) | +3.84% | Normal |
| **$\text{NO}_x$ CEMS Monitor Availability** | 98.50% | $\ge$ 95.00% (EPA Threshold) | +3.68% | Normal |
| **$\text{CO}_2$ / Flow Monitor Availability** | 99.05% | $\ge$ 95.00% (EPA Threshold) | +4.26% | Normal |
| **Quarterly Missing Data Substitution Rate** | 1.27% | $\le$ 5.00% (QA Benchmark) | -74.60% | Normal |
| **Part 75 QA/QC Tests (RATA / Daily Calibrations)** | 100% Passed | 100% Passing Required | 0.00% | Normal |

---

### 3. Visualization Triggers

**Recommended Visualization**: **Grouped Bar Chart** displaying CEMS Monitor Data Availability percentages versus Missing Data Substitution percentages across monitored unit pollutant streams.

```json
{
  "chart_type": "bar",
  "title": "EPA Part 75 CEMS Monitor Availability & Missing Data Rates",
  "categories": [
    "Unit 1 - SO2",
    "Unit 1 - NOx",
    "Unit 1 - CO2",
    "Unit 2 - SO2",
    "Unit 2 - NOx",
    "Unit 2 - CO2"
  ],
  "series": [
    {
      "name": "Monitor Data Availability (%)",
      "data": [99.4, 98.8, 99.1, 97.9, 98.2, 99.0]
    },
    {
      "name": "Missing Data Substitution (%)",
      "data": [0.6, 1.2, 0.9, 2.1, 1.8, 1.0]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Step 1 (ECMPS Pre-Submission Verification)**: Execute the EPA Emissions Collection and Monitoring Plan System (ECMPS) Client Tool Level 1–3 quality evaluation check to verify that all XML schema formatting, monitor span records, and QA/QC test entries match registered monitoring plans.
- **Step 2 (Allowance Ledger Reconciliation)**: Reconcile aggregated quarterly $\text{SO}_2$ and $\text{NO}_x$ cumulative tonnage against the Clean Air Markets Allowance Tracking System (CAMATS) account balance to verify positive compliance margin.
- **Step 3 (Designated Representative Execution)**: Route the compiled compliance package to the EPA-authorized Primary Designated Representative (DR) or Alternate Designated Representative (ADR) for formal electronic signature and submission.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "REGULATORY_SUBMISSION_AND_SIGNATURE",
  "regulatory_framework": "EPA Clean Air Markets Division (CAMD) - 40 CFR Part 75",
  "filing_name": "Quarterly Electronic CEMS Emissions and QA File (ECMPS XML)",
  "reporting_period": "Quarterly Compliance Cycle",
  "legal_certification_text": "I am authorized to make this submission on behalf of the owners and operators of the affected source or affected units. I certify under penalty of law that I have personally examined, and am familiar with, the statements and information submitted in this document and all its attachments.",
  "required_approver_role": "Primary Designated Representative (DR) / Alternate Designated Representative (ADR)",
  "system_target": "EPA ECMPS / CAMD Gateway",
  "status": "PENDING_HUMAN_SIGNATURE_AND_TRANSMISSION"
}
```
