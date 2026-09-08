# ⚡ Osha Safety Incident Classifier

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of osha safety incident classifier is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Osha Safety Incident Classifier Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank osha safety incident classifier events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.osha_safety_incident_classifier_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Does the electrical flash burn suffered by a line technician during cable splicing meet the criteria for an OSHA Recordable Incident?"

**Agent Response:**
### Executive Summary
**Under 29 CFR 1904.7 and 1904.39, an electrical flash burn sustained during cable splicing is classified as an OSHA Recordable Incident if it results in medical treatment beyond first aid, days away from work, restricted duty/job transfer, loss of consciousness, or is diagnosed as a significant burn injury by a licensed healthcare professional.** **Furthermore, if the incident resulted in an in-patient hospitalization, it triggers mandatory direct reporting to OSHA within 24 hours under 29 CFR 1904.39.** **A formal determination requires assessing the specific treatment administered (e.g., prescription silvadene/debridement vs. over-the-counter first aid topical application) and any resulting duty limitations.**

---

### Regulatory Classification Matrix (29 CFR Part 1904)

| Metric / Criteria | Incident Evaluation Baseline | Compliance Threshold / Reference | OSHA Recordability Impact | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Work-Relatedness** | Event occurred during cable splicing on duty | 29 CFR 1904.5 (Work Environment) | Established Work-Related | **Critical** |
| **Medical Treatment vs. First Aid** | Prescription meds (e.g., Silver Sulfadiazine), debridement, specialized burn care | 29 CFR 1904.7(b)(5) (First Aid definition list) | Recordable if treatment exceeds first aid | **Critical** |
| **Days Away / Work Restriction** | Missed shifts or assignment to light duty | 29 CFR 1904.7(b)(3) & (b)(4) | Recordable upon $\ge 1$ lost/restricted day | **Warning** |
| **Significant Diagnosed Injury** | 2nd or 3rd degree burns diagnosed by PLHCP | 29 CFR 1904.7(b)(7) (Significant Injuries) | Recordable even without treatment/lost time | **Warning** |
| **Direct Reporting Mandate** | Formal in-patient admission to hospital/burn center | 29 CFR 1904.39 (Severe Injury Reporting) | 24-Hour OSHA Notification required | **Critical** |

---

### OSHA Recordability Decision Breakdown

1. **First Aid Exclusions (Non-Recordable if SOLE treatment):**
   - Application of non-prescription ointments/creams at non-prescription strength.
   - Cleaning, flushing, or soaking wounds on the skin surface.
   - Use of non-rigid wound coverings (gauze pads, bandages).
   - Tetanus immunization alone.

2. **Triggers for Mandatory OSHA Form 300 Logging:**
   - **Medical Treatment Beyond First Aid:** Use of prescription-strength burn dressings/antibiotics, surgical debridement, IV hydration therapy, or dermabrasion.
   - **Work Restrictions / Job Transfer:** Inability of the line technician to perform one or more routine functions of their splicing role or work full scheduled days.
   - **Days Away from Work:** Physician-directed removal from work starting the calendar day *after* the incident.
   - **Diagnosis:** Full-thickness (3rd degree) or severe partial-thickness (2nd degree) burns diagnosed by a Physician or Licensed Healthcare Professional (PLHCP).

---

### Visualization Trigger: Incident Classification Workflow

```json
{
  "chart_type": "decision_matrix",
  "data_json": {
    "nodes": [
      {"id": "A", "label": "Work-Related Electrical Flash Burn", "status": "Confirmed"},
      {"id": "B", "label": "In-Patient Hospitalization?", "outcomes": {"Yes": "24h OSHA Direct Notification (1904.39)", "No": "Evaluate Recordability"}},
      {"id": "C", "label": "Medical Treatment Beyond First Aid?", "outcomes": {"Yes": "OSHA 300 Log Recordable", "No": "Evaluate Lost/Restricted Time"}},
      {"id": "D", "label": "Days Away or Restricted Duty?", "outcomes": {"Yes": "OSHA 300 Log Recordable", "No": "PLHCP Diagnosis Check"}},
      {"id": "E", "label": "Significant Injury Diagnosed (e.g., 2nd/3rd Deg)?", "outcomes": {"Yes": "OSHA 300 Log Recordable", "No": "Non-Recordable First Aid"}}
    ]
  }
}
```

---

### Actionable Recommendations

- **Audit Medical Records for Treatment Details:** Review the clinical notes from the occupational health or emergency provider to verify if prescription burn treatments (e.g., SSD cream, oral analgesics above OTC limits) or wound debridement were administered.
- **Track Work Status:** Confirm if the treating physician issued written work restrictions (e.g., "no glove use," "no high-voltage switching," "desk duty only") or scheduled days off following the date of injury.
- **Log Entry Timelines:** If recordable, enter the incident onto the enterprise **OSHA Form 300** within **7 calendar days** of receiving notice of the injury.
- **Root Cause & PPE Inspection:** Immediately secure the cable splicing toolset, arc-rated face shield/balaclava, and rubber insulating gloves for failure analysis and ASTM F855 / NFPA 70E compliance verification.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "OSHA_FORM_300_FORMAL_RECORDING",
  "trigger": "Electrical flash burn classified as Recordable Incident under 29 CFR 1904.7",
  "approval_required": "Human-In-The-Loop Safety & Regulatory Compliance Officer",
  "parameters": {
    "incident_category": "Electrical Arc Flash / Thermal Burn",
    "regulatory_standard": "29 CFR 1904.7 / 1904.39",
    "osha_300_log_deadline_days": 7,
    "osha_direct_report_deadline_hours": 24
  }
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Analyze days away, restricted, or transferred (DART) rate and Total Recordable Incident Rate (TRIR) across field operations."

**Agent Response:**
### 1. Executive Summary
**Enterprise Field Operations recorded an aggregate Total Recordable Incident Rate (TRIR) of 1.94 and a Days Away, Restricted, or Transferred (DART) rate of 0.98 per 200,000 hours worked over the trailing twelve months. While Generation & Plant Operations and Transmission & Substations remain within OSHA/BLS industry benchmarks, Vegetation Management (TRIR 3.45, DART 1.95) and Fleet & Logistics (TRIR 2.80, DART 1.45) exceed acceptable safety and compliance thresholds. Targeted ergonomic, line-clearance safety, and material handling interventions are required immediately to prevent OSHA Form 300/300A non-compliance escalations.**

---

### 2. Data Presentation

#### Enterprise Field Safety Compliance Overview
*(Formulas: $\text{TRIR} = \frac{\text{Recordable Incidents} \times 200,000}{\text{Total Hours Worked}}$, $\text{DART} = \frac{\text{DART Cases} \times 200,000}{\text{Total Hours Worked}}$)*

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Enterprise TRIR** | 1.94 incidents / 200k hrs | 1.50 (BLS Utility Benchmark) | +29.3% | **Warning** |
| **Enterprise DART Rate** | 0.98 cases / 200k hrs | 0.80 (BLS Utility Benchmark) | +22.5% | **Warning** |
| **Lost Time Severity Rate (LTSR)** | 18.4 days / 200k hrs | 12.0 days | +53.3% | **Warning** |
| **OSHA 300 Log Recordability Audit** | 98.6% compliance | 100.0% compliance | -1.4% | **Normal** |
| **Incident Classification Latency** | 14.2 hours | < 24.0 hours | -40.8% | **Normal** |

#### Operational Division Breakdown

| Operational Unit | Total Hours Worked | OSHA Recordable Cases | DART Cases | TRIR | DART Rate | Unit Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Vegetation Management** | 463,770 | 8 | 5 | **3.45** | **1.95** | **Critical** |
| **Fleet & Logistics** | 357,140 | 5 | 3 | **2.80** | **1.45** | **Critical** |
| **Distribution Line Ops** | 1,209,300 | 13 | 7 | **2.15** | **1.10** | **Warning** |
| **Gas Operations** | 744,680 | 7 | 4 | **1.88** | **0.92** | **Warning** |
| **Transmission & Substations** | 985,915 | 7 | 3 | **1.42** | **0.65** | **Normal** |
| **Generation & Plant Ops** | 842,100 | 4 | 2 | **0.95** | **0.40** | **Normal** |
| **Total / Enterprise Aggregate** | **4,602,905** | **44** | **24** | **1.94** | **0.98** | **Warning** |

---

### 3. Visualization Triggers

```json
{
  "chart_type": "bar",
  "title": "Field Operations TRIR & DART Rates vs Industry Benchmark (BLS)",
  "categories": [
    "Vegetation Management",
    "Fleet & Logistics",
    "Distribution Line Ops",
    "Gas Operations",
    "Transmission & Substations",
    "Generation & Plant Ops"
  ],
  "series": [
    {
      "name": "Actual TRIR",
      "data": [3.45, 2.80, 2.15, 1.88, 1.42, 0.95]
    },
    {
      "name": "Actual DART Rate",
      "data": [1.95, 1.45, 1.10, 0.92, 0.65, 0.40]
    },
    {
      "name": "BLS TRIR Benchmark",
      "data": [1.50, 1.50, 1.50, 1.50, 1.50, 1.50]
    },
    {
      "name": "BLS DART Benchmark",
      "data": [0.80, 0.80, 0.80, 0.80, 0.80, 0.80]
    }
  ],
  "xAxisLabel": "Field Operations Division",
  "yAxisLabel": "Rate per 200,000 Hours Worked"
}
```

---

### 4. Actionable Recommendations

1. **Targeted Stand-Down & Ergonomic Audits in Vegetation Management**:
   - High DART rate (1.95) is predominantly driven by acute soft tissue strains, struck-by debris, and chainsaw handling.
   - Schedule mandatory field safety audits and stand-downs across tree crew contractors and internal crews within 10 business days.

2. **Material Handling & Slip/Trip/Fall Protocols in Fleet & Logistics**:
   - Re-evaluate material handling equipment (MHE) loading docks and warehouse loading zones to mitigate non-fatal lost-workday incidents.

3. **OSHA 301 / 300A Pre-Filing Classification Review**:
   - Ensure all 44 recordable cases have completed formal root-cause evaluations (5-Why / TapRooT) and that all restricted duty days are logged accurately prior to annual OSHA Form 300A certification.

4. **Near-Miss Reporting Program Expansion in Distribution Ops**:
   - Deploy automated field near-miss reporting via mobile crew tablets to address leading indicators before they materialize into lost-time injuries.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Submit the certified OSHA 300 log entry and initiate a comprehensive root-cause safety stand-down review for District West."

**Agent Response:**
### Executive Summary
**The OSHA Safety Incident Classifier has finalized the categorization and audit verification for all pending safety records in District West, identifying 3 OSHA Recordable incidents requiring certified Form 300/300A logging. Formal submission of certified regulatory compliance logs and the operational execution of a mandatory safety stand-down constitute Tier 2 operations requiring explicit Human-in-the-Loop (HITL) authorization. All root-cause telemetry, causal factors, and regulatory reporting artifacts have been compiled and staged for executive review.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **OSHA Recordable Incident Rate (TRIR)** | 2.14 / 200k hrs | ≤ 1.20 / 200k hrs | +78.3% | **Critical** |
| **Days Away, Restricted, Transferred (DART)** | 1.07 / 200k hrs | ≤ 0.60 / 200k hrs | +78.3% | **Warning** |
| **OSHA 300 Log Classification Accuracy** | 100.0% | 100.0% | 0.0% | **Normal** |
| **Incident Reporting Latency** | 3.2 hrs | ≤ 8.0 hrs | -60.0% | **Normal** |
| **Audit Compliance Rate** | 98.6% | 100.0% | -1.4% | **Warning** |

---

### Visualization Triggers
**Recommended Chart**: Incident Severity & Recordability Distribution (District West vs. Target)

```json
{
  "chart_type": "bar",
  "title": "District West OSHA Incident Classification Breakdown",
  "xAxis": {
    "categories": [
      "Lost Time Incidents",
      "Restricted Duty / Transfer",
      "Medical Treatment Only",
      "First Aid / Non-Recordable"
    ]
  },
  "yAxis": {
    "title": "Total Incident Count (YTD)"
  },
  "series": [
    {
      "name": "District West Actual",
      "data": [3, 5, 8, 14]
    },
    {
      "name": "Enterprise Benchmark Cap",
      "data": [1, 2, 5, 12]
    }
  ]
}
```

---

### Actionable Recommendations
- **Validate Log Certification**: Verify official executive sign-off on Form 300A prior to final regulatory dispatch to federal/state OSHA reporting portals.
- **Implement Stand-Down Protocol**: Coordinate with District West Field Operations to execute the Root-Cause Safety Stand-Down schedule across line crews and substation personnel.
- **Deploy Corrective and Preventive Actions (CAPA)**: Prioritize training on high-voltage personal protective equipment (PPE) compliance and energized line work safety protocols.
- **Monitor Real-Time Exposure**: Maintain heightened surveillance on District West field work permits until the stand-down debriefing is completed.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CERTIFIED_OSHA_SUBMISSION_AND_STAND_DOWN",
  "authority_level": "Safety Director / Designated Regulatory Official",
  "parameters": {
    "district": "District West",
    "filing_target": "OSHA 300 / 300A Annual Electronic Submission",
    "recordable_events_count": 3,
    "operational_stand_down": {
      "target_scope": "District West Field Crews & Substation Ops",
      "duration_hours": 4,
      "focus_area": "High-Voltage Safe Work Practices & Root-Cause Remediation",
      "schedule_window": "Immediate Next Shift"
    }
  },
  "confirmation_status": "PENDING_HUMAN_APPROVAL",
  "required_actions": [
    "Acknowledge and sign official electronic certification for OSHA 300 log entries.",
    "Approve operational stop-work notice for District West safety stand-down."
  ]
}
```
