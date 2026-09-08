# ⚡ Employee Fatigue Risk Monitor

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of employee fatigue risk monitor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Employee Fatigue Risk Monitor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank employee fatigue risk monitor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.employee_fatigue_risk_monitor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which emergency restoration line workers have exceeded 16 consecutive hours on duty or 60 hours over the rolling 7-day storm window?"

**Agent Response:**
### Executive Summary
**A total of 6 emergency restoration line workers across 4 active storm restoration crews have breached enterprise utility fatigue safety thresholds by exceeding either the 16.0 consecutive duty hour limit or the 60.0 cumulative hour threshold over the rolling 7-day storm window. Critical fatigue exposure is most pronounced in Grid Zone 3 (Substation Delta-9 Feeder 12) and Grid Zone 1 (Substation Alpha-4), where sustained outage restoration operations have driven maximum continuous duty times up to 18.0 hours. Immediate operational intervention is required to mandate rest cycles and transition replacement crews to avert high-risk safety incidents and maintain compliance with utility labor standards.**

---

### Data Presentation

#### Enterprise Fatigue & Duty Threshold Compliance Overview
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Consecutive Duty Hours** | 18.0 hrs | ≤ 16.0 hrs | +12.5% | **Critical** |
| **Max Rolling 7-Day Storm Hours** | 68.5 hrs | ≤ 60.0 hrs | +14.2% | **Critical** |
| **Workers Exceeding Consecutive Limit (>16h)** | 4 Workers | 0 Workers | N/A | **Critical** |
| **Workers Exceeding 7-Day Window (>60h)** | 5 Workers | 0 Workers | N/A | **Critical** |
| **Dual-Threshold Violations (>16h & >60h)** | 3 Workers | 0 Workers | N/A | **Critical** |
| **Average Rest Gap Pre-Shift** | 6.2 hrs | ≥ 8.0 hrs | -22.5% | **Warning** |

#### Line Workers Exceeding Fatigue Thresholds (Detailed Breakdown)
*Note: Personal Identifiable Information (PII) is masked in accordance with enterprise data protection protocols; operational identifiers are retained for dispatch reconciliation.*

| Line Worker Identifier | Crew ID | Operating Grid Zone | Feeder / Substation ID | Consecutive Hours on Duty | Rolling 7-Day Storm Hours | Rule Violation Type | Fatigue Risk Score (1–100) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **LW-5128** | Crew B-1 | Zone 3 (Metro East) | Substation Delta-9 (F-12) | **18.0 hrs** | **68.5 hrs** | Dual Violation (>16h & >60h) | **96 (Severe)** |
| **LW-4091** | Crew A-2 | Zone 1 (North Ridge) | Substation Alpha-4 (F-02) | **17.5 hrs** | **64.0 hrs** | Dual Violation (>16h & >60h) | **93 (Severe)** |
| **LW-3312** | Crew B-1 | Zone 3 (Metro East) | Substation Delta-9 (F-12) | **16.5 hrs** | **61.5 hrs** | Dual Violation (>16h & >60h) | **89 (High)** |
| **LW-2219** | Crew A-2 | Zone 1 (North Ridge) | Substation Alpha-4 (F-02) | **16.5 hrs** | 58.0 hrs | Consecutive Violation (>16h) | **84 (High)** |
| **LW-8834** | Crew C-4 | Zone 2 (Central Valley) | Substation Beta-1 (F-07) | 15.0 hrs | **63.5 hrs** | 7-Day Rolling Violation (>60h) | **82 (High)** |
| **LW-7705** | Crew D-3 | Zone 4 (Harbor South) | Substation Gamma-6 (F-18) | 14.0 hrs | **62.0 hrs** | 7-Day Rolling Violation (>60h) | **79 (Elevated)** |

---

### Visualization Triggers
- **Recommended Chart**: Grouped Bar Chart displaying Consecutive Hours on Duty vs. Rolling 7-Day Storm Hours against regulatory ceiling thresholds for impacted personnel.

```json
{
  "chart_type": "bar",
  "data": {
    "categories": [
      "LW-5128 (Crew B-1)",
      "LW-4091 (Crew A-2)",
      "LW-3312 (Crew B-1)",
      "LW-2219 (Crew A-2)",
      "LW-8834 (Crew C-4)",
      "LW-7705 (Crew D-3)"
    ],
    "thresholds": {
      "consecutive_limit_hrs": 16.0,
      "rolling_7day_limit_hrs": 60.0
    },
    "series": [
      {
        "name": "Consecutive Hours on Duty",
        "data": [18.0, 17.5, 16.5, 16.5, 15.0, 14.0]
      },
      {
        "name": "Rolling 7-Day Storm Hours",
        "data": [68.5, 64.0, 61.5, 58.0, 63.5, 62.0]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Mandate Immediate Rest Protocol**: Direct field supervisors for Crew A-2 and Crew B-1 to stand down workers `LW-5128`, `LW-4091`, `LW-3312`, and `LW-2219` immediately and enforce an uninterrupted 8-hour minimum rest period.
- **Dispatch Mutual Aid / Secondary Roster**: Mobilize off-duty Relief Shift Roster Tier-2 to take over active feeder energization and wire repair tasks on Substation Delta-9 (Feeder 12) and Substation Alpha-4 (Feeder 02).
- **Enforce Rolling 7-Day Cap**: Transition workers `LW-8834` and `LW-7705` to non-safety-critical ground support or staging area logistics until rolling 7-day cumulative hours fall below the 60.0-hour safety ceiling.
- **Automate Alert Escalation**: Configure real-time Dispatch Management System (DMS) telemetry to trigger an automated yellow alert at 14.0 consecutive hours and 54.0 cumulative 7-day hours during active storm operating mode.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FIELD_CREW_STAND_DOWN_AND_DISPATCH_SUBSTITUTION",
  "urgency": "IMMEDIATE",
  "affected_personnel": ["LW-5128", "LW-4091", "LW-3312", "LW-2219"],
  "target_crews": ["Crew A-2", "Crew B-1"],
  "operating_zones": ["Zone 1 (North Ridge)", "Zone 3 (Metro East)"],
  "required_actions": [
    "Execute mandatory 8-hour stand-down for flagged line workers.",
    "Assign replacement relief crew R-04 to Substation Alpha-4 and R-09 to Substation Delta-9.",
    "Reassign LW-8834 and LW-7705 to light-duty storm staging operations."
  ],
  "hitl_approval_required": true,
  "approver_roles": ["Storm Operations Director", "Safety & Compliance Officer"]
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Track crew shift rotations, rest periods, and circadian fatigue risk scores to ensure full compliance with utility labor safety rules."

**Agent Response:**
### 1. Executive Summary
**Field workforce telemetry indicates elevated circadian fatigue risk scores exceeding the safety threshold (70/100) in Grid Zones A and C following extended restoration shifts.** **Mandatory minimum rest periods (8 consecutive hours) are currently at risk of violation for 2 out of 5 active field crews without immediate schedule intervention.** **Immediate crew rotation and shift rebalancing are required to maintain strict adherence to utility labor safety regulations and OSHA 1910.269 high-voltage operational standards.**

---

### 2. Data Presentation

The table below details shift rotations, off-duty rest intervals, and circadian fatigue scoring evaluated across active service zones:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Zone C Max Fatigue Index** | `84.6 / 100` | `< 70.0 / 100` | `+20.9%` | **Critical** |
| **Zone A Max Fatigue Index** | `78.4 / 100` | `< 70.0 / 100` | `+12.0%` | **Critical** |
| **Zone E Max Fatigue Index** | `61.5 / 100` | `< 70.0 / 100` | `-12.1%` | **Warning** |
| **Zone B Max Fatigue Index** | `42.1 / 100` | `< 70.0 / 100` | `-39.9%` | **Normal** |
| **Zone D Max Fatigue Index** | `31.2 / 100` | `< 70.0 / 100` | `-55.4%` | **Normal** |
| **Crew Rest Interval (Zone C)** | `6.5 hrs` | `≥ 8.0 hrs` | `-18.8%` | **Critical** |
| **Max Consecutive Shift Days** | `6.0 days` | `≤ 5.0 days` | `+20.0%` | **Warning** |

---

### 3. Visualization Triggers

A bar chart has been generated comparing crew circadian fatigue scores against regulatory compliance thresholds across operational grid zones.

```json
{
  "chart_type": "bar",
  "title": "Crew Circadian Fatigue Risk Scores by Zone",
  "labels": ["Zone A (Feeder-12)", "Zone B (Sub-04)", "Zone C (Metro North)", "Zone D (Rural East)", "Zone E (Sub-09)"],
  "datasets": [
    {
      "label": "Current Fatigue Score (0-100)",
      "data": [78.4, 42.1, 84.6, 31.2, 61.5]
    },
    {
      "label": "OSHA/Utility Compliance Threshold",
      "data": [70.0, 70.0, 70.0, 70.0, 70.0]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Immediate Stand-Down**: Enforce an immediate mandatory 8-hour uninterrupted rest period for Zone C and Zone A line crews prior to any live-line maintenance or high-voltage dispatch.
- **Shift Reassignment**: Mobilize auxiliary crew resources from Zone D (Rural East) and Zone B (Sub-04), where fatigue scores remain low (`< 43.0`), to relieve high-risk zones.
- **Circadian Window Restriction**: Restrict switching operations and heavy energized work between 02:00 and 06:00 (circadian trough) for crews nearing 12 continuous hours on-duty.
- **Telematics & Dispatch Lock**: Integrate real-time fatigue monitoring flags into the automated dispatch queue to prevent auto-assignment of emergency tickets to fatigued crews.

---

### 5. HITL / Tier 2 Formats

```text
[TIER 2 ACTION REQUIRED]
--------------------------------------------------------------------------------
Operation: Autonomous Dispatch Suspension & Mandatory Crew Stand-Down
Affected Units: Field Crews assigned to Grid Zone A (Feeder-12) & Zone C (Metro North)
Justification: Circadian fatigue risk index exceeds safety limit (Score: 84.6 & 78.4 > Threshold: 70.0); minimum rest period non-compliance.
Required Approver: Support Services Operations Director / Safety Dispatch Supervisor
Action Needed: Confirm dispatch lock and approve mutual-aid / backup crew reassignment to cover active tickets.
--------------------------------------------------------------------------------
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue a mandatory rest stand-down order for Line Crew Bravo and assign fresh relief personnel to ongoing restoration shifts."

**Agent Response:**
### 1. Executive Summary
**Line Crew Bravo has exceeded standard allowable on-duty work duration thresholds, reaching an elevated cumulative shift fatigue index that poses immediate safety and operational risks during active restoration.** **In compliance with utility safety protocols and fatigue management standards, an immediate mandatory rest stand-down is recommended, along with the dispatch of relief personnel.** **Because initiating mandatory labor stand-down orders and crew reassignment affects physical field operations, this action requires Human-In-The-Loop (HITL) operator confirmation.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Consecutive On-Duty Hours** | 23.5 hrs | Max 16.0 hrs | +46.88% | **Critical** |
| **Fatigue Risk Score (0-100)** | 88.5 | < 50.0 | +77.00% | **Critical** |
| **Cumulative Rest Period (Past 24h)** | 0.5 hrs | Min 8.0 hrs | -93.75% | **Critical** |
| **Restoration Shift Duration** | 14.2 hrs | Max 10.0 hrs | +42.00% | **Critical** |
| **Relief Crew Bravo-2 Availability** | 100% (Available) | Ready Status | 0.00% | **Normal** |

---

### 3. Visualization Triggers
- **Recommended Visualization**: Time-Series Line Chart illustrating cumulative on-duty hours vs. the maximum continuous fatigue threshold limit (16 hrs).

```json
{
  "chart_type": "line",
  "title": "Line Crew Bravo Cumulative Work Hours vs. Fatigue Safety Limit",
  "labels": ["00:00", "04:00", "08:00", "12:00", "16:00", "20:00", "24:00"],
  "datasets": [
    {
      "label": "Cumulative Shift Hours",
      "data": [4.0, 8.0, 12.0, 16.0, 18.5, 21.0, 23.5],
      "borderColor": "#E74C3C"
    },
    {
      "label": "Safety Threshold (Max 16h)",
      "data": [16.0, 16.0, 16.0, 16.0, 16.0, 16.0, 16.0],
      "borderColor": "#F39C12",
      "borderDash": [5, 5]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Immediate Stand-Down Order**: Direct Line Crew Bravo to complete current safe isolation/tagging step and safely transition the active work zone to a secure standby state.
- **Relief Crew Deployment**: Dispatch certified Relief Crew (Bravo-2 / Relief Unit #4) to assume control of the restoration work package at the target feeder/substation.
- **Mandatory Minimum Rest**: Enforce a mandatory minimum 8-to-10 hour undisturbed rest window for all members of Line Crew Bravo prior to re-entering the dispatch queue.
- **Incident Log Recording**: Record the extended shift hours and fatigue intervention in the enterprise safety compliance management system.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MANDATORY_CREW_STAND_DOWN_AND_RELIEF_DISPATCH",
  "target_crew": "Line Crew Bravo",
  "relief_crew": "Relief Unit Bravo-2",
  "mandate_details": {
    "reason": "Exceeded continuous fatigue threshold (23.5 hours on-duty)",
    "mandatory_rest_duration_hours": 8.0,
    "active_work_order": "RESTORATION-FEEDER-ZONE-4"
  },
  "execution_impact": "Safe handoff of ongoing restoration feeder operations to relief personnel",
  "approval_required": true,
  "human_in_the_loop": "Field Dispatch Supervisor / Safety Operations Lead"
}
```
