# ⚡ Saidi Saifi Reliability Metric Tracker

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of saidi saifi reliability metric tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Saidi Saifi Reliability Metric Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank saidi saifi reliability metric tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.saidi_saifi_reliability_metric_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What are our year-to-date System Average Interruption Duration Index (SAIDI) and Frequency Index (SAIFI) numbers across all districts?"

**Agent Response:**
### Executive Summary
**Year-to-Date (YTD) system-wide reliability performance stands at a SAIDI of 56.96 minutes and a SAIFI of 0.770 interruptions per customer (calculated per IEEE 1366 standards, excluding qualifying Major Event Days). While Central Metro, Southern Coastal, and Western Plains remain well within annual regulatory reliability thresholds, Northern Valley and Eastern Highlands are currently tracking above performance targets due to severe convective weather and vegetation-related feeder trip events.**

---

### Quantitative Performance Breakdown

#### System & District Reliability Metrics (YTD)

| Metric / District | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **System-Wide SAIDI** | **56.96 min** | **57.00 min** | **-0.07%** | **Normal** |
| **System-Wide SAIFI** | **0.770 int/cust** | **0.750 int/cust** | **+2.67%** | **Warning** |
| Central Metro - SAIDI | 42.50 min | 50.00 min | -15.00% | Normal |
| Central Metro - SAIFI | 0.580 int/cust | 0.650 int/cust | -10.77% | Normal |
| Northern Valley - SAIDI | 68.20 min | 60.00 min | +13.67% | Warning |
| Northern Valley - SAIFI | 0.920 int/cust | 0.800 int/cust | +15.00% | Warning |
| Eastern Highlands - SAIDI | 84.10 min | 75.00 min | +12.13% | Critical |
| Eastern Highlands - SAIFI | 1.150 int/cust | 0.950 int/cust | +21.05% | Critical |
| Southern Coastal - SAIDI | 51.30 min | 55.00 min | -6.73% | Normal |
| Southern Coastal - SAIFI | 0.710 int/cust | 0.750 int/cust | -5.33% | Normal |
| Western Plains - SAIDI | 38.70 min | 45.00 min | -14.00% | Normal |
| Western Plains - SAIFI | 0.490 int/cust | 0.600 int/cust | -18.33% | Normal |

---

### Visualization Configuration

**Recommended Chart Type:** Grouped Bar Chart (District SAIDI & SAIFI Performance vs. Regulatory Targets)

```json
{
  "chart_type": "bar",
  "title": "YTD District Reliability Metrics vs. Regulatory Baselines",
  "categories": [
    "Central Metro",
    "Northern Valley",
    "Eastern Highlands",
    "Southern Coastal",
    "Western Plains"
  ],
  "series": [
    {
      "name": "YTD SAIDI (Minutes)",
      "data": [42.5, 68.2, 84.1, 51.3, 38.7]
    },
    {
      "name": "Target SAIDI (Minutes)",
      "data": [50.0, 60.0, 75.0, 55.0, 45.0]
    },
    {
      "name": "YTD SAIFI (Outages/Customer)",
      "data": [0.58, 0.92, 1.15, 0.71, 0.49]
    },
    {
      "name": "Target SAIFI (Outages/Customer)",
      "data": [0.65, 0.8, 0.95, 0.75, 0.6]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Targeted Feeder Hardening in Eastern Highlands**: Prioritize inspection and recloser coordination reviews on the top 5 worst-performing distribution feeders (contributing to >40% of the district's SAIDI).
2. **Vegetation Management Rescheduling**: Expedite cycle trimming programs in Northern Valley and Eastern Highlands to mitigate repeat storm and momentary-to-sustained trip conversions.
3. **Automated Restoration (FLISR) Verification**: Audit automated sectionalizing switch performance across Southern Coastal and Northern Valley to ensure faulted segment isolation times remain under the 5-minute IEEE sustained threshold.
4. **Regulatory Reporting Alignment**: Document all IEEE 1366 Major Event Day (MED) exclusion calculations with underlying $T_{\text{MED}}$ daily threshold justifications for upcoming PUC quarterly compliance filings.

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate the reliability impact of Major Event Days (MED) excluded under IEEE 1366 2.5-Beta methodology versus normal storm days."

**Agent Response:**
### 1. Executive Summary
**Under the IEEE Std 1366™ 2.5-Beta methodology, Major Event Days (MEDs) represent statistically anomalous operating conditions exceeding the catastrophic threshold ($T_{MED} = e^{\alpha + 2.5\beta}$), isolating extreme exogenous shocks from baseline utility performance. Normal storm days that fall below $T_{MED}$ remain fully included in regulatory reliability reporting, accounting for over 34% of standard baseline SAIDI despite localized severe weather impacts. Excluding MEDs prevents distortion of underlying capital asset performance trends while preserving regulatory accountability for routine storm hardening and operational resilience.**

---

### 2. Data Presentation

The comparative analysis below reflects an annualized reliability evaluation comparing **Underlying Routine Operations**, **Non-MED Storm Days (Included)**, and **Major Event Days (Excluded via 2.5-Beta)** against typical PUC/Regulatory compliance baselines.

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Daily SAIDI Threshold ($T_{MED}$)** | 4.82 min/day | 4.50 min/day (5-yr rolling) | +7.11% | Normal |
| **Annual Reported SAIDI (w/ MED Excluded)** | 112.40 min | 120.00 min | -6.33% | Normal |
| **Non-MED Storm SAIDI Contribution** | 38.60 min | 30.00 min | +28.67% | Warning |
| **Excluded MED SAIDI Impact** | 485.20 min | N/A (Exogenous) | N/A | Critical |
| **Total Unadjusted SAIDI (All-In)** | 597.60 min | 120.00 min | +398.00% | Critical |
| **Annual Reported SAIFI (w/ MED Excluded)** | 1.05 int/cust | 1.15 int/cust | -8.70% | Normal |
| **Excluded MED SAIFI Impact** | 0.82 int/cust | N/A (Exogenous) | N/A | Critical |
| **CAIDI (Reported vs. MED Events)** | 107.0 min (137.9 storm / 591.7 MED) | 104.3 min | +2.59% | Normal |

#### Key Analytical Findings:
* **Log-Normal Distribution Shift**: The $T_{MED}$ threshold calculation utilizes a 5-year rolling natural logarithmic distribution ($\ln(\text{Daily SAIDI})$) of non-zero outage days. A standard 2.5-Beta cutoff statistically isolates the upper ~0.62% of operational days.
* **Normal Storms vs. MED Masking**: "Normal storm days" (convective storms, moderate wind events) that do not breach the $T_{MED}$ threshold drive a +28.67% variance above typical storm-budgeted SAIDI, demonstrating that routine weather exposure remains tightly scrutinized within utility regulatory caps.
* **Restoration Duration Variance**: Excluded MED events exhibit a CAIDI of 591.7 minutes (extensive physical asset destruction and multi-stage mutual assistance), whereas routine storm days maintain a CAIDI of 137.9 minutes.

---

### 3. Visualization Triggers

**Recommended Visualization**: Stacked / Grouped Bar Chart comparing Adjusted vs. Unadjusted Reliability Metrics to illustrate the exact slice of outage minutes removed under IEEE 1366 compliance filings.

```json
{
  "chart_type": "bar",
  "title": "IEEE 1366 Reliability Metrics: Reported Baseline vs. Excluded MED Impacts",
  "data": {
    "labels": ["SAIDI (minutes)", "SAIFI (interruptions)", "CAIDI (minutes)"],
    "datasets": [
      {
        "label": "Reported (IEEE 1366 Excluded)",
        "data": [112.4, 1.05, 107.0],
        "backgroundColor": "#2563EB"
      },
      {
        "label": "Non-MED Storm Impact (Included)",
        "data": [38.6, 0.28, 137.9],
        "backgroundColor": "#F59E0B"
      },
      {
        "label": "MED Impact (Excluded from Compliance)",
        "data": [485.2, 0.82, 591.7],
        "backgroundColor": "#DC2626"
      },
      {
        "label": "Total Unadjusted (All-In)",
        "data": [597.6, 1.87, 319.6],
        "backgroundColor": "#6B7280"
      }
    ]
  },
  "options": {
    "responsive": true,
    "scales": {
      "y": {
        "beginAtZero": true,
        "title": { "display": true, "text": "Metric Units (Minutes / Frequency)" }
      }
    }
  }
}
```

---

### 4. Actionable Recommendations

* **Recalibrate 5-Year Rolling $T_{MED}$ Baseline**: Execute annual re-baselining of the 5-year rolling daily SAIDI dataset to capture changes in grid topology and hardening investments prior to the next annual PUC reliability filing.
* **Target Non-MED Storm Feeder Hardening**: Prioritize targeted vegetation management and lateral recloser automation on the top 10 worst-performing feeders contributing to the 38.60-minute non-MED storm SAIDI.
* **Audit MED Boundary Timestamps**: Review Outage Management System (OMS) timestamps for storm start/stop definitions to ensure that MED declaration boundaries strictly follow the 24-hour UTC/local operating day rules specified by IEEE Std 1366 Section 4.5.
* **Regulatory Compliance Documentation**: Maintain auditable workpapers detailing outage cause codes, mutual aid mobilization logs, and chronological ETR curves for all days exceeding $T_{MED}$ to satisfy state commission audit requirements.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Publish the official monthly distribution reliability scorecard to grid operations leadership and regulatory compliance teams."

**Agent Response:**
### Executive Summary
**The enterprise distribution system operated within IEEE Std 1366 and state regulatory reliability thresholds for the current monthly reporting cycle, posting an operational SAIDI (excluding Major Event Days) of 8.45 minutes against a regulatory cap of 9.50 minutes (-11.05% favorable). System SAIFI recorded at 0.082 interruptions per customer against the 0.090 baseline (-8.89% favorable), driven by accelerated automated feeder switching and sectionalizing programs. However, localized tree-wire contact in Grid Zone 4 has elevated momentary interruptions (MAIFI at 0.240), warranting prioritized vegetation trimming ahead of quarterly PUC submittals.**

---

### Distribution Reliability Scorecard (IEEE 1366 / PUC Standard)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **SAIDI (Non-MED)** | 8.45 minutes | 9.50 minutes | -11.05% | **Normal** |
| **SAIDI (Including MED)** | 14.20 minutes | 15.00 minutes | -5.33% | **Normal** |
| **SAIFI (Non-MED)** | 0.082 interruptions | 0.090 interruptions | -8.89% | **Normal** |
| **SAIFI (Including MED)** | 0.115 interruptions | 0.125 interruptions | -8.00% | **Normal** |
| **CAIDI** | 103.05 minutes | 105.56 minutes | -2.38% | **Normal** |
| **MAIFI** | 0.240 events | 0.280 events | -14.29% | **Normal** |
| **CEMI-4 (% Customers $\ge$ 4 Outages)** | 2.10% | 2.50% | -16.00% | **Normal** |
| **Worst-Performing Feeder Outage Count** | 7 events | 5 events | +40.00% | **Warning** |

---

### Visualization: Monthly Reliability Indices vs. Regulatory Baselines

```json
{
  "chart_type": "bar",
  "title": "Monthly Distribution Reliability Indices vs. IEEE 1366 Baselines",
  "categories": [
    "SAIDI (Med. Excl.) [min]",
    "SAIDI (Med. Incl.) [min]",
    "SAIFI (Med. Excl.) [int]",
    "SAIFI (Med. Incl.) [int]",
    "CAIDI [min]",
    "MAIFI [events]",
    "CEMI-4 [%]"
  ],
  "series": [
    {"name": "Actual", "data": [8.45, 14.20, 0.082, 0.115, 103.05, 0.240, 2.1]},
    {"name": "Target Baseline", "data": [9.50, 15.00, 0.090, 0.125, 105.56, 0.280, 2.5]}
  ]
}
```

---

### Actionable Recommendations

1. **Worst-Performing Feeder Mitigation (Feeder WF-402)**: Dispatch distribution engineering field inspection to Feeder WF-402 in Grid Zone 4 to investigate recurring momentary trips (MAIFI contribution) and execute hot-spot vegetation management.
2. **Major Event Day (MED) Classification Verification**: Validate the $T_{\text{MED}}$ statistical boundary threshold calculations under IEEE 1366 2.5 Beta method with the regulatory filings working group prior to final PUC docket inclusion.
3. **FLISR Telemetry Calibration**: Audit restoration timestamp latency across automated reclosers in Substation S-12 to maintain Estimated Time to Restoration (ETR) accuracy within regulatory confidence intervals ($\pm 5\%$).

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "OFFICIAL_SCORECARD_PUBLICATION",
  "approval_level": "HUMAN_IN_THE_LOOP",
  "payload": {
    "document_title": "Monthly Distribution Reliability & IEEE 1366 Compliance Scorecard",
    "recipients": [
      "grid_operations_leadership@enterprise.utility.internal",
      "regulatory_compliance_officers@enterprise.utility.internal"
    ],
    "reporting_period": "Current Month",
    "compliance_mandates": ["IEEE Std 1366-2022", "FERC Reliability Reporting", "State PUC Distribution Service Quality Standards"],
    "summary_metrics": {
      "saidi_non_med_min": 8.45,
      "saifi_non_med_int": 0.082,
      "caidi_min": 103.05,
      "compliance_posture": "FULLY_COMPLIANT"
    }
  },
  "confirmation_prompt": "Confirm official dispatch and archiving of the Monthly Distribution Reliability Scorecard to Grid Operations Leadership and Regulatory Compliance."
}
```
