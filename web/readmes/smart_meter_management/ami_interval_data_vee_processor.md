# ⚡ Ami Interval Data Vee Processor

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of ami interval data vee processor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Ami Interval Data Vee Processor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank ami interval data vee processor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.ami_interval_data_vee_processor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many 15-minute smart meter interval reads failed automated Validation, Editing, and Estimation (VEE) checks today?"

**Agent Response:**
### Executive Summary
**A total of 11,687 fifteen-minute smart meter interval reads failed automated Validation, Editing, and Estimation (VEE) checks across the enterprise grid footprint today, representing an overall failure rate of 0.81% against 1,440,000 processed intervals.** **The primary driver of failures is localized high/low threshold boundary violations in Grid Zone 4, followed by frozen meter zero-consumption exceptions.** **Automated secondary estimation algorithms have successfully backfilled 8,920 records, leaving 2,767 unresolved exceptions requiring manual exception queue remediation or field verification.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total 15-Min Intervals Processed** | 1,440,000 | 1,440,000 | 0.00% | Normal |
| **Total VEE Exception Failures** | 11,687 | < 7,200 (< 0.50%) | +62.32% | Warning |
| **Spike / High-Low Threshold Violations** | 4,820 | 2,500 | +92.80% | Warning |
| **Zero Consumption / Frozen Meter Reads** | 3,140 | 2,000 | +57.00% | Warning |
| **Missing Intervals / Pulse Drop** | 2,415 | 1,800 | +34.17% | Normal |
| **Negative Consumption Anomalies** | 890 | < 200 | +345.00% | Critical |
| **Sum Check / Register Discrepancies** | 422 | < 700 | -39.71% | Normal |
| **Automated VEE Estimation Success Rate** | 76.33% (8,920) | > 85.00% | -10.20% | Warning |
| **Unresolved Manual Queue Records** | 2,767 | < 1,000 | +176.70% | Warning |

---

### Visualization Triggers

**Recommended Visualization**: Horizontal Bar Chart / Categorical Breakdown showing VEE Exception Types.

```json
{
  "chart_type": "bar",
  "title": "VEE Interval Exception Breakdown by Rule (Today)",
  "categories": [
    "Spike / High-Low Limit Failures",
    "Zero Consumption / Frozen Meter",
    "Missing Intervals / Pulse Count",
    "Negative Consumption Anomaly",
    "Sum Check / Register Discrepancy"
  ],
  "series": [
    {
      "name": "Failed Reads",
      "data": [4820, 3140, 2415, 890, 422]
    }
  ]
}
```

---

### Actionable Recommendations

- **Prioritize Negative Consumption Anomalies**: Dispatch the top 890 negative consumption exception records to the Tamper & Revenue Protection queue to inspect for meter inversion, reverse wiring, or unregistered distributed energy resource (DER/solar) backfeeds.
- **Run Historical Proxy Backfill on Missing Intervals**: Trigger secondary historical-matching estimation models (same-day-of-week 4-week average) for the 2,415 missing interval reads before billing cycle cutoff.
- **Review Grid Zone 4 High-Low Limits**: Coordinate with the Distribution Operations team to adjust seasonal peak threshold multipliers for commercial feeders experiencing valid heat-index load surges.
- **Target Mesh Collector Diagnostic**: Investigate Collector Unit DC-04 in Grid Zone 4, which accounts for 43% of all dropped packet and missing interval flags today.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze continuous spike and flatline data gaps across residential meters caused by mesh network collector dropouts."

**Agent Response:**
### 1. Executive Summary
**Mesh network collector dropout events have generated severe telemetry discontinuities across residential interval data streams, manifesting as sustained zero-consumption flatlines during backhaul link severed periods followed by artificial interval demand spikes upon bulk buffer re-transmission. The Validation, Estimation, and Editing (VEE) pipeline has automatically flagged 14,600 missing or corrupted 15-minute intervals, triggering standard high-delta and failover validation rules across 480 meters connected via Collector Substation Hubs C-04 and C-07. Automated linear and historical proxy estimation algorithms are actively staging corrected profiles to prevent downstream billing inaccuracies, wholesale settlement distortions, and false customer outage flags.**

---

### 2. Data Presentation (VEE & Mesh Telemetry Metrics)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Mesh Packet Delivery Success Rate** | 65.8% | ≥ 98.5% | -33.2% | **Critical** |
| **Collector Backhaul Availability (C-04 & C-07)** | 72.4% | ≥ 99.9% | -27.5% | **Critical** |
| **Flatline Anomaly Rate (Consecutive Zero kWh Intervals)** | 12.8% | ≤ 0.5% | +2460.0% | **Critical** |
| **Post-Reconnection Accumulated Spike Rate** | 8.9% | ≤ 0.2% | +4350.0% | **Critical** |
| **Total VEE Disqualified / Flagged Intervals** | 14,600 | < 500 | +2820.0% | **Critical** |
| **Automated VEE Estimation Coverage Ratio** | 88.2% | ≥ 99.0% | -10.9% | **Warning** |
| **Mean Time to Telemetry Restoration (MTTR)** | 3.8 hrs | < 1.0 hr | +280.0% | **Warning** |

---

### 3. Root Cause & VEE Rule Engine Analysis

1. **Collector Dropout Mechanism (Flatline Phase)**:
   - When mesh access point/collector backhaul drops (e.g., cellular/fiber link loss at hub), meters store cumulative register pulses locally in volatile memory. 
   - Polling failures produce consecutive empty intervals or zero-delta reads (`FLATLINE_FAIL_RULE_04`), triggering false zero-usage flags.

2. **Re-synchronization Burst Dynamics (Spike Phase)**:
   - Upon collector re-association, accumulated energy register differentials are dumped in the initial reconnect interval rather than being evenly parsed across the dropped time window.
   - This causes an artificial demand spike exceeding physical service capacity (e.g., >200 A residential limit or >400% maximum historical demand check via `SPIKE_MAX_DELTA_RULE_01`).

3. **VEE Algorithmic Correction Pathway**:
   - **Step 1 (Spike De-accumulation)**: Subtract register start/end reads across the gap and unbundle single-interval peak spikes.
   - **Step 2 (Linear & Profile Interpolation)**: Disperse aggregate energy consumption across missing intervals utilizing meter-specific Historical Proxy Day matching (same Day-of-Week / Temperature-normalized load shape).
   - **Step 3 (Status Code Tagging)**: Append VEE Status Flags (`EST_HIST_PROXY` / `CORR_MESH_BURST`) to ensure clear regulatory audit trails for wholesale settlement and customer billing.

---

### 4. Visualization Configuration

Recommended Chart: **Time-Series Line Chart** tracking packet delivery failure rates against VEE estimation volume, flatline meter counts, and post-restoration spike anomalies.

```json
{
  "chart_type": "line",
  "title": "AMI Mesh Collector Telemetry & VEE Anomaly Timeline (Last 24 Hours)",
  "timestamps": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
  "series": [
    {
      "name": "Mesh Packet Delivery Failure Rate (%)",
      "values": [3.2, 4.1, 18.5, 34.2, 28.1, 12.4, 4.0]
    },
    {
      "name": "VEE Estimation & Substitution Volume (k-Intervals)",
      "values": [1.1, 1.4, 7.8, 14.6, 11.2, 4.9, 1.5]
    },
    {
      "name": "Post-Restoration Burst Spikes (Flagged VEE)",
      "values": [0.2, 0.1, 3.4, 8.9, 6.1, 1.8, 0.3]
    },
    {
      "name": "Zero-Delta / Flatline Meter Count",
      "values": [45, 52, 210, 480, 395, 160, 58]
    }
  ]
}
```

---

### 5. Actionable Recommendations

- **Automated VEE Batch Execution**: Run the automated VEE Redistribution Algorithm across the 14,600 flagged intervals, recalculating interval kW demand based on end-of-interval cumulative kWh register differentials.
- **Mesh Topology Optimization**: Reconfigure mesh routing tables on neighbor nodes adjacent to Collector Hubs C-04 and C-07 to dynamically failover to Collectors C-02 and C-09 during backhaul latency spikes.
- **Backhaul Health Diagnostics**: Direct telecommunications field operations to inspect WAN cellular routers and backhaul modems at Substation Collector nodes C-04 and C-07.
- **Billing Hold Enforcement**: Temporarily hold billing determinant generation for the 480 affected meter accounts until automated VEE profile substitution has completed validation checks.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_approval_request:
  action: "MASS_VEE_INTERVAL_EDIT_AND_SUBSTITUTION_COMMIT"
  target_grid_zones: ["SUBSTATION_FEEDER_C04", "SUBSTATION_FEEDER_C07"]
  affected_meter_count: 480
  total_substituted_intervals: 14600
  estimation_method: "HISTORICAL_PROXY_AND_END_REGISTER_PRO_RATA"
  financial_and_settlement_impact: "Prevents false high-bill residential disputes and eliminates 3.6 MWh wholesale ISO imbalance settlement error"
  risk_assessment: "Low physical risk; mandatory compliance check for PUC interval data edit audit standards"
  required_approver: "Meter Data Management (MDM) Operations Lead / Grid Analytics Manager"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Commit validated 15-minute interval energy records for 250,000 meters to the Meter Data Management System (MDMS) for billing."

**Agent Response:**
### 1. Executive Summary
**The VEE (Validation, Estimation, and Editing) processing cycle has completed quality checks across 250,000 meters totaling 24,000,000 fifteen-minute interval energy records.** **Committing mass billing-determinant interval datasets directly impacts downstream customer billing cycles and enterprise financial settlement; therefore, this operation is classified as a Tier 2 financial action.** **Direct write/commit execution to the MDMS billing partition has been staged and paused pending mandatory Human-In-The-Loop (HITL) authorization.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Meters Processed** | 250,000 meters | 250,000 meters | 0.0% | Normal |
| **Total 15-Min Intervals** | 24,000,000 records | 24,000,000 records | 0.0% | Normal |
| **Validation Pass Rate (First Pass)** | 95.40% (238,500 meters) | ≥ 95.00% | +0.42% | Normal |
| **VEE Algorithmic Estimation Rate** | 3.56% (8,900 meters) | ≤ 4.00% | -11.00% | Normal |
| **High-Consumption / Anomaly Flags** | 0.74% (1,850 meters) | ≤ 0.80% | -7.50% | Normal |
| **Fatal Check Exceptions / Missing Telemetry** | 0.30% (750 meters) | ≤ 0.20% | +50.00% | Warning |

---

### 3. Visualization Triggers
**Recommended Visualization:** Categorical Bar Chart depicting the classification breakdown across the 250,000-meter billing batch.

```json
{
  "chart_type": "bar",
  "title": "AMI 15-Minute Interval VEE Batch Breakdown",
  "data": {
    "categories": ["Validated (Passed)", "Estimated (VEE)", "Anomalies/Flagged", "Pending Review"],
    "counts": [238500, 8900, 1850, 750],
    "percentages": [95.40, 3.56, 0.74, 0.30]
  },
  "axes": {
    "x": "Meter Classification",
    "y": "Meter Count"
  }
}
```

---

### 4. Actionable Recommendations
- **Audit Exception Queue**: Route the 750 meters failing critical zero-consumption and clock-skew validation checks to the manual VEE exception queue for billing analyst remediation.
- **Isolate Anomaly Cohort**: Hold the 1,850 anomalous spikes for automated secondary verification against temperature sensitivity indices before release.
- **Execute Staged Batch Commit**: Upon operator approval, release the 247,400 fully validated and rule-estimated meter records directly to MDMS for billing determinant aggregation.

---

### [TIER 2 ACTION REQUIRED]

```yaml
operation: MDMS_BILLING_DATASET_COMMIT
target_system: Meter Data Management System (MDMS) - Production Billing Store
scope:
  meters_queued: 250000
  interval_granularity: 15_minute
  total_interval_records: 24000000
  staged_for_commit: 247400
  held_in_exception_queue: 2600
risk_assessment: High (Direct impact on customer billing, revenue recognition, and settlement calculations)
action_required: Operator verification and digital sign-off to execute batch commit to production billing tables.
status: PENDING_HUMAN_APPROVAL
```
