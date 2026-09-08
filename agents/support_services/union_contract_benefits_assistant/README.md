# ⚡ Union Contract Benefits Assistant

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of union contract benefits assistant is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Union Contract Benefits Assistant Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank union contract benefits assistant events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.union_contract_benefits_assistant_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What are the collective bargaining agreement rules regarding storm standby pay, call-out minimums, and meal allowances for IBEW linemen?"

**Agent Response:**
### Executive Summary
**Under standard utility IBEW Collective Bargaining Agreements (CBAs), storm standby, call-out minimums, and meal allowances are governed by strict operational and fatigue-management safety clauses. Lineworkers placed on designated standby receive a minimum daily standby stipend (typically 2.0 hours straight-time base pay per 24-hour cycle) until activated, after which emergency premium overtime rates apply. Call-outs enforce a mandatory minimum guarantee of 3.0 to 4.0 hours at premium pay (1.5x to 2.0x), accompanied by contractual meal stipends or hot meals provided at recurring 4-to-5-hour operational intervals.**

---

### Data Presentation: CBA Standard Provisions & Compliance Benchmarks

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Storm Standby Pay (per 24-hr window)** | 2.0 hrs Straight-Time Base | 2.0 hrs Base Rate | 0.0% | Normal |
| **Call-Out Minimum Guarantee** | 4.0 hrs at 1.5x (or 2.0x Sunday/Holiday) | 4.0 hrs Overtime | 0.0% | Normal |
| **Meal Allowance Stipend ($/meal)** | $22.50 / eligible meal | $20.00 Base Baseline | +12.5% | Normal |
| **Meal Timing Interval** | Every 4.5 hrs of continuous duty | $\le$ 5.0 hrs Interval | -10.0% | Normal |
| **Fatigue Rest Trigger (Consecutive Hours)** | 16.0 continuous hrs | 16.0 hrs Max Shift | 0.0% | Normal |
| **Mandatory Rest Period** | 8.0 consecutive hrs | 8.0 hrs Off-Duty | 0.0% | Normal |

---

### Detailed Contractual Breakdown

#### 1. Storm Standby (On-Call / Readiness)
* **Designation & Availability:** Linemen scheduled on pre-storm standby must remain fit for duty and within a 45-minute response radius to the reporting operating center.
* **Compensation:** Credited with **2.0 hours of straight-time base pay** per 24-hour standby period when not mobilized. 
* **Transition to Active Duty:** The moment an employee reports or is dispatched, standby pay terminates and active storm compensation shifts immediately to the applicable overtime multiplier (1.5x base hourly rate, escalating to 2.0x for Sundays, designated holidays, or hours exceeding 16 consecutive hours).

#### 2. Call-Out Minimums & Fatigue Rules
* **Guaranteed Minimum:** A minimum of **4.0 hours of compensation at the applicable overtime rate** applies to any emergency call-out outside regular shift hours, regardless of whether actual restoration takes less time.
* **Continuous Call-Out Window:** If a second call-out occurs within the original 4-hour window, it is considered part of the initial call-out block. Calls occurring after the initial window trigger a new call-out minimum.
* **16-Hour Rest Rule (Fatigue Management):** Linemen working 16 or more hours in a 24-hour period must receive a mandatory **8-hour uninterrupted rest period**. If this rest window extends into their regular scheduled shift, they receive regular straight-time pay for overlapping hours without performing field labor.

#### 3. Meal Allowances & Field Provisions
* **First Meal Eligibility:** Linemen called out on emergency storm duty become eligible for their first meal allowance after **2.0 hours of unplanned work** beyond regular shift hours, or at the start of an unscheduled call-out exceeding 4 hours.
* **Recurring Intervals:** Additional meal stipends ($22.50/meal) or employer-provided field catering must be provided every **4.5 to 5.0 hours** of sustained emergency work thereafter.
* **Paid Meal Time:** Lineworkers are allowed **30 minutes of paid meal time** when meals are taken in the field or at staging areas.

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "data_json": {
    "title": "Storm Duty Compensation Multipliers & Minimum Thresholds",
    "categories": [
      "Standby (24-hr Inactive)",
      "Call-Out Minimum (Base Guarantee)",
      "Standard Storm Overtime",
      "Sunday / Holiday Storm Overtime",
      "Post-16hr Extended Restoration"
    ],
    "series": [
      {
        "name": "Pay Multiplier / Hours Paid",
        "data": [2.0, 4.0, 1.5, 2.0, 2.0]
      }
    ]
  }
}
```

---

### Actionable Recommendations

* **Automate ERP/Workforce Time Capture:** Ensure utility dispatch management systems (e.g., CGI/ARCOS/SAP) automatically map lineworker timesheets to the 4.0-hour minimum rule and meal allowance trigger codes during designated storm operating modes.
* **Fatigue Tracking Enforcement:** Cross-verify crew management logs with the 16-hour fatigue rule to prevent safety and NERC/OSHA violations during multi-day major weather restoration events.
* **Field Logistics Coordination:** If field staging site catering is deployed in lieu of the $22.50 cash voucher, log catering delivery times to substantiate compliance with the 4.5-to-5.0-hour meal interval mandate.

### Example 2: Trend & Comparative Analysis
**User:** "Clarify apprenticeship progression timelines and healthcare contribution rates under the ratified 2025-2028 union contract."

**Agent Response:**
### Executive Summary
**Under the ratified 2025–2028 Collective Bargaining Agreement (CBA), the apprenticeship progression is formalized into an 8-step, 48-month competency schedule requiring 7,000 on-the-job training (OJT) hours and 576 accredited classroom hours for Journeyman certification. Healthcare contribution cost-sharing transitions gradually from an 88/12 employer/employee split in 2025 to an 85/15 split by 2028, with employer-funded HSA seed amounts locked across all contract years. All step advancements remain contingent upon semi-annual Joint Apprenticeship and Training Committee (JATC) review and practical competency evaluations.**

---

### Data Presentation: Apprenticeship Progression & Healthcare Rates

#### 1. Apprenticeship Progression Timelines (4-Year / 8-Step Schedule)

| Step / Level | Timeline (Months) | Required Cumulative OJT Hours | Classroom / Related Training | Wage Rate (% of Journeyman Scale) | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Step 1 (Probationary)** | 0 – 6 Mos | 1,000 hrs | 72 hrs (Safety & Fundamentals) | 60.0% | Normal |
| **Step 2** | 7 – 12 Mos | 2,000 hrs | 144 hrs (Basic Electrical/Gas) | 65.0% | Normal |
| **Step 3** | 13 – 18 Mos | 3,000 hrs | 216 hrs (Distribution Systems I) | 70.0% | Normal |
| **Step 4** | 19 – 24 Mos | 4,000 hrs | 288 hrs (Distribution Systems II) | 75.0% | Normal |
| **Step 5** | 25 – 30 Mos | 5,000 hrs | 360 hrs (High-Voltage/Substation) | 80.0% | Normal |
| **Step 6** | 31 – 36 Mos | 6,000 hrs | 432 hrs (Hot-Line / Advanced Ops) | 85.0% | Normal |
| **Step 7** | 37 – 42 Mos | 6,500 hrs | 504 hrs (System Protection & Switching)| 90.0% | Normal |
| **Step 8 (Final Evaluation)**| 43 – 48 Mos | 7,000 hrs | 576 hrs (Final Board & Testing) | 95.0% | Normal |
| **Journeyman Classification**| Post-48 Mos | 7,000+ hrs & Board Pass | Full Certification | 100.0% | Normal |

---

#### 2. Healthcare Contribution & Benefits Summary (2025–2028 CBA Metrics)

| Metric | Current Value (2025 Ratified) | Baseline / Target (2024 CBA) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Employee Premium Share (2025)** | 12.0% | 10.0% | +20.0% | Normal |
| **Employee Premium Share (2026)** | 13.0% | 12.0% | +8.3% | Normal |
| **Employee Premium Share (2027)** | 14.0% | 13.0% | +7.7% | Normal |
| **Employee Premium Share (2028)** | 15.0% | 14.0% | +7.1% | Normal |
| **Employer HSA Contribution (Single)** | $1,000 / year | $750 / year | +33.3% | Normal |
| **Employer HSA Contribution (Family)** | $2,000 / year | $1,500 / year | +33.3% | Normal |
| **In-Network Individual Deductible (PPO)**| $750 | $750 | 0.0% | Normal |
| **In-Network Family Deductible (PPO)** | $1,500 | $1,500 | 0.0% | Normal |
| **Out-of-Pocket Max (Individual PPO)** | $3,500 | $3,500 | 0.0% | Normal |

---

### Visualization Triggers

- **Recommended Chart Type**: **Grouped Bar & Trend Line Chart** to display annual healthcare cost-share escalation alongside Journeyman baseline wage adjustments across the 4-year contract term (2025–2028).

```json
{
  "chart_type": "bar",
  "data": {
    "title": "2025-2028 Union Contract Healthcare Cost Sharing & Apprenticeship Wage Scale",
    "categories": ["2025", "2026", "2027", "2028"],
    "series": [
      {
        "name": "Employee Healthcare Contribution (%)",
        "data": [12.0, 13.0, 14.0, 15.0]
      },
      {
        "name": "Employer Healthcare Contribution (%)",
        "data": [88.0, 87.0, 86.0, 85.0]
      },
      {
        "name": "Journeyman Base Scale ($/hr)",
        "data": [52.50, 54.60, 56.78, 59.05]
      }
    ]
  }
}
```

---

### Actionable Recommendations

1. **HR/Payroll Configuration**: Update ERP and benefits administration portals to execute the progressive annual premium deduction split adjustments effective January 1 of each contract year (12% in 2025, scaling to 15% in 2028).
2. **JATC Audit Cadence**: Enforce bi-annual submission of apprentice field logs and hours tracking at each 6-month milestone to ensure automated step-rate wage increases are processed without administrative delay.
3. **Open Enrollment Briefings**: Issue clear employee benefit summaries to bargaining unit members detailing employer HSA contributions and deductible structures prior to each annual enrollment window.
4. **Apprentice Progress Reviews**: Schedule formal probationary reviews prior to Month 6 for all Step 1 apprentices to confirm retention and progression into Step 2.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Calculate retroactive standby wage adjustments for 14 union lineworkers impacted by rescheduled storm duty rotations."

**Agent Response:**
### Executive Summary
**Retroactive standby wage calculations have been finalized for all 14 union lineworkers impacted by rescheduled storm duty rotations in accordance with Article VII (Emergency Operations & Standby Premiums) of the Collective Bargaining Agreement (CBA). The total gross retroactive adjustment due across the cohort is $8,280.00, resulting from unapplied short-notice shift rescheduling penalties and mandatory 24-hour standby rate differentials. Correcting these payroll entries restores contractual compliance, eliminates grievance exposure under IBEW labor standards, and requires human payroll sign-off prior to the next pay cycle.**

---

### Data Presentation (Markdown Tables)

#### Table 1: Overall Retroactive Wage Adjustment Summary
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Impacted Lineworkers** | 14 FTE | 14 FTE | 0.0% | Normal |
| **Total Standby Hours Rescheduled** | 336.0 hrs | 0.0 hrs | +100.0% | Warning |
| **Original Standby Compensation Paid** | $6,624.00 | $14,904.00 | -55.56% | Critical |
| **Contractual CBA Total Liability** | $14,904.00 | $14,904.00 | 0.0% | Normal |
| **Total Retroactive Adjustment Owed** | **$8,280.00** | **$0.00** | **+100.0%** | **Warning** |
| **Average Adjustment per Lineworker** | $591.43 | $0.00 | +100.0% | Warning |
| **CBA Grievance Risk Score** | 0.0 / 10.0 (Post-Pay) | 8.5 / 10.0 (Pre-Pay) | -100.0% | Normal |

---

#### Table 2: Roster Classification & Wage Breakdown (14 Lineworkers)
*CBA Formula: Base Standby (2 hrs straight time/24 hr block) + Reschedule Penalty Notice Differential (<24h Notice = 4 hrs straight time differential/rotation).*

| Job Classification | Headcount | Hourly Base Rate | Original Standby Paid / Head | CBA Required Standby / Head | Retroactive Delta / Head | Group Retroactive Total |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Journeyman Lineworker** | 8 | $56.00/hr | $448.00 | $1,008.00 | +$560.00 | $4,480.00 |
| **Lead Lineworker** | 4 | $62.50/hr | $500.00 | $1,125.00 | +$625.00 | $2,500.00 |
| **Troubleman / Crew Lead** | 2 | $65.00/hr | $520.00 | $1,170.00 | +$650.00 | $1,300.00 |
| **Total Cohort** | **14** | **—** | **$6,624.00** | **$14,904.00** | **+$591.43 (avg)** | **$8,280.00** |

---

### Visualization Triggers
- **Recommended Visualization**: Grouped Bar Chart comparing Original Standby Paid vs. CBA Contractual Standby Total and Net Retroactive Adjustment by classification.

```json
{
  "chart_type": "bar",
  "title": "Retroactive Standby Wage Adjustments by Lineworker Classification",
  "categories": [
    "Journeyman Lineworker (8 FTE)",
    "Lead Lineworker (4 FTE)",
    "Troubleman / Crew Lead (2 FTE)",
    "Total Group (14 FTE)"
  ],
  "series": [
    {
      "name": "Original Standby Paid ($)",
      "data": [3584, 2000, 1040, 6624]
    },
    {
      "name": "CBA Required Standby Total ($)",
      "data": [8064, 4500, 2340, 14904]
    },
    {
      "name": "Retroactive Adjustment Due ($)",
      "data": [4480, 2500, 1300, 8280]
    }
  ]
}
```

---

### Actionable Recommendations
- **Transmit Wage Ledger**: Send the computed retroactive adjustment schedule to Utility Payroll Operations for inclusion in the upcoming bi-weekly pay cycle (Pay Period Ending: Current Cycle).
- **Notify Labor Relations & Union Shop Steward**: Issue formal confirmation of the proactive adjustment to the IBEW Local Business Representative to close open inquiries regarding the rescheduled storm duty rotation.
- **Update Dispatch Standby Logging**: Update the automated Work Management System (WMS) scheduling trigger to automatically apply the short-notice rescheduling differential whenever storm duty rotations shift within a 48-hour window.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PAYROLL_RETROACTIVE_DISBURSEMENT_AUTHORIZATION",
  "target_system": "Enterprise_HRIS_Payroll_Module",
  "impacted_personnel_count": 14,
  "financial_impact": {
    "gross_retroactive_wages": 8280.00,
    "currency": "USD",
    "cost_center": "SUPPORT_SERVICES_STORM_OPERATIONS_1042"
  },
  "cba_provision_reference": "IBEW_CBA_ART_VII_SEC_4_STANDBY_ROTATION",
  "risk_assessment": "Low risk; mandatory compliance disbursement to prevent formal labor grievance filing.",
  "approval_required": "Human-In-The-Loop (HR Director / Labor Relations Lead / Payroll Supervisor)",
  "status": "PENDING_HUMAN_APPROVAL"
}
```
