# ⚡ Dynamic Etr Calculator

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of dynamic etr calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Dynamic Etr Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank dynamic etr calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.dynamic_etr_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the predicted Estimated Time of Restoration (ETR) for Outage Ticket #9921 with 3 downed spans and broken crossarms?"

**Agent Response:**
### Executive Summary
**Outage Ticket #9921 has a dynamically calculated Estimated Time to Restoration (ETR) of 4 hours and 40 minutes (280 minutes) from crew arrival on-site.** **The repair scope involves extensive structural and conductor remediation, including replacement of broken overhead crossarms and re-stringing/tensioning 3 downed spans.** **Calculated confidence interval is 95% within a range of 250 to 310 minutes, assuming standard single-bucket line crew deployment with no adverse access impediments.**

---

### Dynamic ETR & Work Breakdown Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Site Safety & LOTO Grounding** | 35 min | 30 min | +16.7% | Normal |
| **Crossarm Removal & Replacement** | 75 min | 60 min | +25.0% | Warning |
| **3-Span Conductor Re-stringing/Sagging** | 140 min | 120 min | +16.7% | Warning |
| **Pre-Energization Inspection & Switching** | 30 min | 30 min | 0.0% | Normal |
| **Total Dynamic Repair Duration (ETR)** | **280 min (4h 40m)** | **240 min (4h 00m)** | **+16.7%** | **Warning** |
| **ETR Confidence Interval (P95)** | 250 – 310 min | ±15 min | — | Normal |
| **SAIDI Impact Risk Contribution** | Moderate | Low | — | Warning |

---

### Visualization Trigger: Restoration Phase Breakdown

```json
{
  "chart_type": "bar",
  "title": "Restoration Phase Duration Breakdown (Ticket #9921)",
  "phases": [
    {"phase": "Safety, Assessment & Grounding", "duration_min": 35},
    {"phase": "Crossarm Replacement & Hardware", "duration_min": 75},
    {"phase": "3-Span Conductor Stringing & Tensioning", "duration_min": 140},
    {"phase": "Inspection, De-grounding & Switching", "duration_min": 30}
  ],
  "total_predicted_duration_min": 280,
  "confidence_interval_min": [250, 310]
}
```

---

### Actionable Recommendations

- **Crew Dispatch & Material Verification**: Verify line crew is equipped with appropriate conductor splicing sleeves, tensioning grips/come-alongs, replacement crossarms (e.g., standard 8 ft or 10 ft tangent/deadend wood or fiberglass), and post/pin insulators prior to arrival.
- **Upstream Isolation Confirmation**: Confirm SCADA lock-out/tag-out (LOTO) isolation boundaries and verify downstream zero-voltage detection before grounds are applied.
- **OMS / CIS Update**: Push the dynamic ETR window of `Current Time + 280 min` to the Outage Management System (OMS) to keep affected customers and dispatch operators synchronized.
- **Dynamic Recalculation Trigger**: Re-evaluate ETR dynamically upon crew arrival confirmation (`On-Scene` milestone) and after conductor tensioning completion.

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate historical crew repair durations and traffic congestion models to refine restoration estimates for rural sectors."

**Agent Response:**
### 1. Executive Summary
**Historical repair duration analytics and rural ingress routing models indicate an average ETR underestimation of 24.6% across rural operating zones, primarily driven by unmodeled unimproved road transit delays and complex off-road asset staging.** **Integrating dynamic traffic congestion coefficients and multi-variable damage repair curves adjusts the baseline rural Mean Time to Restore (MTTR) upward from 165 minutes to 207 minutes.** **This calibration improves ETR 95th-percentile accuracy by 38.2%, mitigating regulatory non-compliance risks and customer broadcast discrepancies under IEEE 1366 standards.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Rural Travel Time Bias (Transit Ingress)** | 56.2 min | 35.0 min | +60.6% | **Warning** |
| **Mean Physical Repair Duration (MTTR)** | 148.0 min | 130.0 min | +13.8% | **Normal** |
| **ETR Prediction Error (Rural Sectors)** | +42.0 min | < 15.0 min | +180.0% | **Critical** |
| **SAIDI Impact (ETR Latency Contrib.)** | 4.82 min/cust | 3.50 min/cust | +37.7% | **Warning** |
| **Dynamic Model ETR Accuracy (Post-Cal)** | 91.4% | 90.0% | +1.6% | **Normal** |

---

### 3. Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Rural Sector ETR Component Breakdown & Variance",
  "categories": [
    "Zone R-101 (Vegetation)",
    "Zone R-102 (Transformer)",
    "Zone R-103 (Downed Wire)",
    "Zone R-104 (Pole Replacement)",
    "Zone R-105 (Equipment Failure)"
  ],
  "series": [
    {
      "name": "Base Travel Time (Traffic/Distance)",
      "data": [48, 54, 62, 75, 42]
    },
    {
      "name": "Mean Repair Duration",
      "data": [115, 160, 130, 240, 95]
    },
    {
      "name": "Historical ETR Underestimation Delta",
      "data": [28, 35, 45, 60, 22]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Deploy Terrain & Traffic Penalty Weightings**: Update the Dynamic ETR algorithm with dynamic GIS-based travel coefficients ($k_{\text{road\_class}} = 1.45$ for unpaved/rural secondary roads, $k_{\text{weather}} = 1.30$ under precipitation).
- **Staging-Adjusted Repair Blocks**: Calibrate Outage Management System (OMS) base restoration curves for complex rural repair categories (e.g., pole setting in off-road terrain adjusted from 180 min to 240 min).
- **FLISR & Auto-Isolation Re-Evaluation**: Prioritize upstream SCADA recloser isolation in Rural Zones R-103 and R-104 to reduce customer counts exposed to long transit delays.
- **Continuous Parameter Refinement**: Retrain the travel time estimator bi-weekly using real-time Automatic Vehicle Location (AVL) telemetry feeds from dispatched line crews.

---

### 5. HITL / Tier 2 Confirmation Requirement

**[TIER 2 ACTION REQUIRED]**
- **Action Type**: OMS Dynamic ETR Algorithm Parameter Update & Public Threshold Publishing.
- **Target Zones**: Grid Zones R-101 through R-105 (Rural Operating Footprint).
- **Parameter Changes**:
  - Update Travel Transit Coefficient from `1.00` to `1.42`.
  - Update Base Off-Road Structural Replacement Duration from `180 min` to `240 min`.
  - Update Customer Outage Portal broadcast refresh interval to `15 minutes`.
- **System Impact**: Modifies real-time customer-facing ETRs and regulatory PUC reliability logging for approximately 42,000 rural service points.
- **Approval Path**: Requires sign-off from Grid Operations Lead and Distribution Dispatch Supervisor prior to production push.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Publish updated dynamic ETR of 18:45 to public outage dashboards and mobile subscriber notifications for Sector 4."

**Agent Response:**
### 1. Executive Summary
**The dynamic Estimated Time to Restoration (ETR) calculation for Sector 4 has been computed and updated to 18:45 based on real-time field crew telemetry, switching step progress, and current restoration velocity. Because publishing updates to public outage maps and initiating mass mobile subscriber notifications constitutes a Tier 2 mass-communication action, autonomous broadcasting is restricted pending formal operator sign-off. The staging payload has been assembled and placed in a pending state awaiting Human-In-The-Loop (HITL) authorization.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Proposed Dynamic ETR** | 18:45 UTC | 19:30 UTC (Initial Baseline) | -10.0% (-45 min) | **Normal** |
| **Model Confidence Level** | 94.2% | ≥ 90.0% | +4.7% | **Normal** |
| **Impacted Sector / Grid Zone** | Sector 4 | Sector 4 | 0.0% | **Warning** |
| **Affected Customer Count** | 14,250 | 14,250 | 0.0% | **Warning** |
| **Predicted SAIDI Impact** | 4.8 min/customer | 6.2 min/customer | -22.6% | **Normal** |

---

### 3. Visualization Triggers

```json
{
  "chart_type": "line",
  "title": "Sector 4 Restoration Progression & ETR Convergence",
  "data": [
    {"timestamp": "16:00", "predicted_etr": "19:45", "confidence_interval_low": "19:15", "confidence_interval_high": "20:15"},
    {"timestamp": "16:30", "predicted_etr": "19:30", "confidence_interval_low": "19:00", "confidence_interval_high": "20:00"},
    {"timestamp": "17:00", "predicted_etr": "19:15", "confidence_interval_low": "18:50", "confidence_interval_high": "19:40"},
    {"timestamp": "17:30", "predicted_etr": "19:00", "confidence_interval_low": "18:40", "confidence_interval_high": "19:20"},
    {"timestamp": "18:00", "predicted_etr": "18:45", "confidence_interval_low": "18:35", "confidence_interval_high": "18:55"}
  ]
}
```

---

### 4. Actionable Recommendations
- **Verify Crew Dispatch Status**: Confirm with field dispatch that the secondary feeder isolation in Sector 4 is completed before confirming broadcast.
- **Authorize Public Broadcast**: Review and approve the Tier 2 broadcast request below to push the 18:45 ETR to customer-facing channels and the OMS web portal.
- **Monitor Re-close Transients**: Maintain real-time SCADA monitoring across adjacent ties during the remaining restoration window.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MASS_PUBLIC_COMMUNICATION_DISPATCH",
  "authorization_level": "TIER_2_HITL",
  "target_channels": [
    "PUBLIC_OUTAGE_DASHBOARD",
    "MOBILE_SUBSCRIBER_NOTIFICATIONS_SMS_PUSH"
  ],
  "payload": {
    "sector_id": "Sector 4",
    "updated_etr": "18:45",
    "impacted_subscribers": 14250,
    "notification_text": "Outage Update: Crews are actively restoring power in Sector 4. The estimated time of restoration is now 6:45 PM (18:45). Thank you for your patience."
  },
  "status": "PENDING_OPERATOR_APPROVAL"
}
```
