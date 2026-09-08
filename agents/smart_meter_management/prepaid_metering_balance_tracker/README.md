# ⚡ Prepaid Metering Balance Tracker

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of prepaid metering balance tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Prepaid Metering Balance Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank prepaid metering balance tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.prepaid_metering_balance_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many prepaid electric service customers currently have account balances below the $10 low-balance threshold?"

**Agent Response:**
### Executive Summary
**A total of 1,530 active prepaid electric service customers currently have balances below the standard $10.00 low-balance threshold, representing 10.77% of the total active prepaid portfolio.** **Within this group, 312 accounts have entered negative balance territory (<$0.00) and are subject to immediate regulatory disconnection moratorium checks and automated recharge reminders.** **AMI interval consumption tracking indicates an average daily burn rate of $4.15 per account across this cohort, giving sub-$10 customers an estimated remaining runtime of under 48 hours without replenishment.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Accounts Below $10.00 Threshold** | 1,530 accounts | 1,200 accounts (Max Target) | +27.50% | **Warning** |
| **Negative Balance Accounts (<$0.00)** | 312 accounts | 150 accounts (Max Target) | +108.00% | **Critical** |
| **Active Prepaid Electric Base** | 14,202 accounts | 14,000 accounts | +1.44% | **Normal** |
| **Portfolio Low-Balance Ratio** | 10.77% | < 8.50% | +26.71% | **Warning** |
| **Average Daily Burn Rate (Low-Balance Cohort)** | $4.15 / day | $3.90 / day | +6.41% | **Normal** |
| **Prepaid VEE Success Rate (5-min intervals)** | 99.82% | 99.50% | +0.32% | **Normal** |

---

### Visualization Triggers

**Recommended Chart**: Account Balance Distribution (Horizontal Bar / Tiered Segmentation)

```json
{
  "chart_type": "bar",
  "title": "Prepaid Electric Service Account Balance Distribution",
  "data": {
    "labels": [
      "Negative Balance (<$0.00)",
      "Critical Low ($0.00 - $4.99)",
      "Low Balance ($5.00 - $9.99)",
      "Moderate Balance ($10.00 - $24.99)",
      "Healthy Balance ($25.00+)"
    ],
    "datasets": [
      {
        "label": "Number of Accounts",
        "data": [312, 548, 982, 3410, 8950],
        "backgroundColor": [
          "#D32F2F",
          "#F57C00",
          "#FBC02D",
          "#1976D2",
          "#388E3C"
        ]
      }
    ]
  },
  "options": {
    "responsive": true,
    "scales": {
      "x": {
        "title": { "display": true, "text": "Customer Account Count" }
      },
      "y": {
        "title": { "display": true, "text": "Balance Tier" }
      }
    }
  }
}
```

---

### Actionable Recommendations

- **Automate Low-Balance AMI Notifications**: Trigger automated SMS/Email/IVR balance alerts for the 1,530 accounts below $10.00, providing localized direct-pay digital links.
- **Cross-Reference Extreme Weather / Moratorium Protocols**: Verify all 312 negative-balance meters against state PUC extreme weather protection rules (heat/cold index) and critical medical care registry prior to scheduling remote service suspension workflows.
- **Evaluate Load-Limiting Mode**: For accounts in negative balance where full disconnection is restricted by policy, evaluate configuring the AMI smart meters to soft load-limiting mode (e.g., 15A threshold) to prevent complete blackout while mitigating utility revenue leakage.
- **Engage Orchestrator for Financial Assistance Integration**: Route eligible low-income accounts within the critical bracket to the Customer Care & Billing Agent for automated Low Income Home Energy Assistance Program (LIHEAP) grant matching.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "REMOTE_SERVICE_DISCONNECT_PREPARATION",
  "affected_meters_count": 312,
  "service_type": "PREPAID_ELECTRIC",
  "threshold_breach": "NEGATIVE_BALANCE",
  "regulatory_review_status": "PENDING_HUMAN_APPROVAL",
  "description": "Mass remote disconnection batching requires Human-In-The-Loop (HITL) authorization per NERC/PUC customer protection guidelines. No autonomous disconnection commands have been executed."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Track daily consumption burn rates and predict which accounts will exhaust prepaid balances before the weekend."

**Agent Response:**
### 1. Executive Summary
**A predictive burn-rate evaluation across 14,850 active prepaid metering accounts identified 157 accounts at critical risk of balance exhaustion (< 24 hours) and 329 accounts at high risk (< 48 hours) prior to the upcoming weekend cutoff.** **With current mean daily burn rates averaging $4.82/day and forecast weather-adjusted load projections indicating an 8.4% surge in weekend cooling demand, proactive notification and disconnect-suppression protocols must be initiated immediately.** **All predictive burn-rate models operated within standard utility compliance, maintaining a forecast Mean Absolute Percentage Error (MAPE) of 3.42% under a 95% confidence interval.**

---

### 2. Data Presentation

#### High-Level Fleet & Metric Performance
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Monitored Prepaid Accounts** | 14,850 | 14,800 | +0.34% | Normal |
| **Accounts Depleting < 24 Hours** | 157 | < 50 | +214.00% | Critical |
| **Accounts Depleting 24–72 Hours (Pre-Weekend)** | 775 | < 300 | +158.33% | Warning |
| **Fleet Mean Daily Burn Rate** | $4.82 / day | $4.45 / day | +8.31% | Warning |
| **Forecast Model Accuracy (MAPE)** | 3.42% | < 5.00% | -31.60% (Favorable) | Normal |
| **Interval VEE Success Rate** | 99.84% | ≥ 99.50% | +0.34% | Normal |
| **Potential Unbilled Revenue at Risk** | $4,120.50 | < $1,500.00 | +174.70% | Critical |

---

#### Grid Zone & Feeder Risk Aggregation
*Accounts tokenized and aggregated by Grid Zone and Primary Substation to ensure CIP/PII compliance:*

| Grid Zone ID | Substation / Feeder Ref | Monitored Accounts | Avg Daily Burn Rate | Accts Depleting < 24h | Accts Depleting 24–48h | Pre-Weekend Exhaustion Risk |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **ZONE-METRO-01** | Sub-08 / Feeder-804 | 4,920 | $5.35 / day | 68 | 142 | **Critical** |
| **ZONE-NORTH-02** | Sub-14 / Feeder-142 | 3,840 | $4.78 / day | 42 | 87 | **Critical** |
| **ZONE-SOUTH-03** | Sub-22 / Feeder-221 | 3,450 | $4.40 / day | 29 | 61 | **Warning** |
| **ZONE-EAST-04** | Sub-03 / Feeder-032 | 2,640 | $4.15 / day | 18 | 39 | **Warning** |

---

### 3. Visualization Triggers
- **Recommended Chart**: Multi-Series Bar Chart / Risk Distribution by Grid Zone.
- **Rendering Configuration**:

```json
{
  "title": "Prepaid Accounts Balance Runout Risk Distribution by Grid Zone",
  "chart_type": "bar",
  "xAxis": "Grid Zone",
  "yAxis": "Number of Accounts < 72h Balance",
  "data": [
    {"grid_zone": "Zone-North (Sub-14)", "critical_under_24h": 42, "warning_24_48h": 87, "elevated_48_72h": 115},
    {"grid_zone": "Zone-Metro (Sub-08)", "critical_under_24h": 68, "warning_24_48h": 142, "elevated_48_72h": 194},
    {"grid_zone": "Zone-South (Sub-22)", "critical_under_24h": 29, "warning_24_48h": 61, "elevated_48_72h": 83},
    {"grid_zone": "Zone-East (Sub-03)", "critical_under_24h": 18, "warning_24_48h": 39, "elevated_48_72h": 54}
  ]
}
```

---

### 4. Actionable Recommendations

1. **Automated Low-Balance Omnichannel Alerts**:
   - Dispatch immediate SMS/Email/IVR push notifications to the 157 accounts with < 24-hour balance margins with real-time balance calculations and instant payment gateway links.
2. **Weekend Disconnection Moratorium Enforcement**:
   - In accordance with jurisdictional Public Utility Commission (PUC) standards prohibiting utility service shutoffs during non-business hours/weekends, apply a temporary disconnection lock across the Head-End System (HES) starting Friday at 12:00 PM through Monday at 08:00 AM.
3. **Courtesy Credit / Bridge Reserve Buffer**:
   - Flag qualifying critical accounts for temporary courtesy credit extensions ($10.00 bridge buffer) to prevent mid-weekend service interruption while preserving interval revenue tracking.
4. **VEE & AMI Mesh Monitoring**:
   - Maintain 15-minute interval validation checks over High-Burn Feeder-804 to capture sudden HVAC-driven load spikes prior to Friday evening peak demand.

---

### 5. Tier 2 Human-in-the-Loop (HITL) Action Required

```yaml
[TIER 2 ACTION REQUIRED]
Operation Type: Automated Disconnect Suppression & Batch Customer Outreach
Target Subsystems: Meter Data Management System (MDMS) / AMI Head-End System (HES) / Customer Communications Gateway
Affected Entities: 
  - Disconnect Moratorium Scope: 486 prepaid meters with < 48-hour balance
  - Notification Batch Size: 775 SMS / 612 Automated Voice Alerts
Trigger Window: Friday 12:00:00 UTC through Monday 08:00:00 UTC
Safety & Regulatory Impact: 
  - Prevents off-hours remote disconnector activation in compliance with PUC Safe Operation Mandates.
  - Mitigates physical tamper and cold/heat-stress emergency calls.
Approval Required: Utility Dispatch Supervisor / Customer Operations Lead
Confirmation Payload:
  suppress_remote_disconnect: TRUE
  moratorium_start_utc: "2024-05-17T12:00:00Z"
  moratorium_end_utc: "2024-05-20T08:00:00Z"
  enable_automated_topup_prompts: TRUE
  max_authorized_courtesy_buffer_usd: 10.00
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Send an urgent low-balance SMS warning to Account #30194 and schedule an automated grace-period extension until Monday morning."

**Agent Response:**
### Executive Summary
**Prepaid balance tracking for Account #30194 indicates a critical low-balance trajectory approaching zero balance within the next interval cycle. In accordance with safety and compliance protocols, external SMS dispatch and grace-period overrides represent sensitive customer and billing status modifications requiring authorized confirmation before execution. Automated balance tracking has flagged this account for immediate operator review.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Current Balance** | $4.10 | $25.00 (Min Target) | -83.6% | **Critical** |
| **Estimated Burn Rate** | $0.48 / hr | $0.25 / hr (Avg) | +92.0% | **Warning** |
| **Time to Depletion** | ~8.5 Hours | > 48.0 Hours | -82.3% | **Critical** |
| **Active Disconnect Protection** | None | Standard Protection | N/A | **Warning** |
| **VEE Interval Validation** | 100% Validated | 100% | 0.0% | **Normal** |

---

### Visualization Triggers
**Recommended Chart**: Time-Series Line Chart (Balance Depletion Curve & Projection)

```json
{
  "chart_type": "line",
  "data": {
    "labels": ["Day -3", "Day -2", "Day -1", "Current", "Projected Depletion"],
    "datasets": [
      {
        "label": "Account Balance ($)",
        "data": [28.50, 19.20, 9.80, 4.10, 0.00],
        "borderColor": "#FF4D4F",
        "fill": false
      },
      {
        "label": "Low-Balance Alert Threshold ($)",
        "data": [10.00, 10.00, 10.00, 10.00, 10.00],
        "borderColor": "#FAAD14",
        "borderDash": [5, 5],
        "fill": false
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Validate Contact & Channel Authorization**: Confirm mobile number on file has valid opt-in consent for automated utility notifications per regulatory guidelines.
- **Authorize Grace Period Extension**: Confirm temporary override of automated disconnect logic until Monday 08:00 AM local time.
- **Review AMI Telemetry**: Verify real-time interval load data to ensure no ongoing meter tampering or erratic load spikes contributing to rapid balance drain.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "tier_level": 2,
  "action_type": "CUSTOMER_NOTIFICATION_AND_BILLING_OVERRIDE",
  "target_account_id": "30194",
  "actions": [
    {
      "type": "OUTBOUND_SMS_ALERT",
      "template_id": "PREPAID_LOW_BALANCE_CRITICAL",
      "recipient_masked": "***-***-XXXX",
      "parameters": {
        "balance_remaining": "$4.10",
        "estimated_hours_remaining": "8.5"
      }
    },
    {
      "type": "SCHEDULE_GRACE_PERIOD_EXTENSION",
      "extension_expiry": "Monday 08:00:00 Local Time",
      "disconnect_suppression_active": true,
      "reason": "Customer Low Balance Grace Period Extension Request"
    }
  ],
  "hitl_approval_required": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```
