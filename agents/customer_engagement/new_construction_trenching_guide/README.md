# ⚡ New Construction Trenching Guide

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of new construction trenching guide is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — New Construction Trenching Guide Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank new construction trenching guide events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.new_construction_trenching_guide_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What are the minimum trench depth and conduit separation clearances required for joint electric and gas utility lines?"

**Agent Response:**
### Executive Summary
**Joint trenching for electric and natural gas utilities requires strict adherence to vertical depth of cover and horizontal/radial separation standards to maintain public safety and grid integrity. Standard new construction design mandates a minimum depth of cover ranging between 24 and 48 inches depending on voltage class and surface loading, alongside a mandatory minimum 12-inch radial clearance between parallel electric and gas conduits. Failure to achieve these clearance thresholds requires specialized mechanical shielding or formal engineering variance approval prior to backfill inspection.**

---

### Data Presentation

The parameters below reflect standard utility engineering specifications (NESC Rule 353 / 49 CFR Part 192 / IEEE standards) for joint electric and gas service/distribution trenching:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Electric Secondary (<600V) Minimum Cover** | 24.0 inches | 24.0 inches | 0.0% | Normal |
| **Electric Primary (600V–35kV) Minimum Cover** | 36.0 inches | 36.0 inches | 0.0% | Normal |
| **Natural Gas Main/Service Minimum Cover** | 24.0 inches | 24.0 inches | 0.0% | Normal |
| **Electric-to-Gas Parallel Separation** | 12.0 inches | 12.0 inches (min) | 0.0% | Normal |
| **Electric-to-Gas Crossing Clearance** | 6.0 – 12.0 inches | 12.0 inches (recommended) | 0.0% | Normal |
| **Trench Bedding Sand Cushion** | 4.0 inches | 4.0 inches (clean fill) | 0.0% | Normal |
| **Warning Ribbon Depth (Below Grade)** | 12.0 inches | 12.0 inches | 0.0% | Normal |

---

### Visualization Triggers

```json
{
  "chart_type": "bar",
  "title": "Joint Utility Trench Depth and Clearance Specifications (Inches)",
  "data_json": [
    {"utility_layer": "Warning Tape Depth", "depth_inches": 12, "standard_type": "Safety Marker"},
    {"utility_layer": "Gas Service Line Depth", "depth_inches": 24, "standard_type": "Minimum Cover"},
    {"utility_layer": "Secondary Electric (<600V) Depth", "depth_inches": 24, "standard_type": "Minimum Cover"},
    {"utility_layer": "Primary Electric (>600V) Depth", "depth_inches": 36, "standard_type": "Minimum Cover"},
    {"utility_layer": "Total Joint Trench Cut (Roadway/Primary)", "depth_inches": 48, "standard_type": "Total Trench Depth"},
    {"utility_layer": "Parallel Radial Clearance (Gas-Electric)", "depth_inches": 12, "standard_type": "Separation Clearance"}
  ]
}
```

---

### Actionable Recommendations

- **Pre-Excavation Verification (811 Call)**: Verify that the 811 underground utility locator ticket is active and positive responses are logged before mechanical trenching begins.
- **Trench Separation Verification**: Ensure a minimum of **12 inches** of well-tamped, rock-free backfill or certified clean bedding sand between electric conduits and polyethylene/steel gas pipes.
- **Conduit Shoring & Shading**: Apply a minimum 4-inch bedding of select aggregate/sand beneath conduits and 12 inches of shaded sand above conduits before native soil backfill and compaction.
- **Warning Tape & Tracer Wire**: Install yellow magnetic tracer wire on all non-metallic gas lines, and place high-visibility warning ribbon 12 inches below finished grade directly above each utility run.
- **Pre-Backfill Joint Inspection**: Schedule the mandatory joint trench field inspection with municipal and utility field inspectors before placing final backfill lifts.

### Example 2: Trend & Comparative Analysis
**User:** "Review the developer trenching blueprint for Green Valley Subdivision Phase 2 against municipal electrical safety codes."

**Agent Response:**
### Executive Summary
**The technical blueprint review for Green Valley Subdivision Phase 2 identifies two non-compliant clearance deviations against Municipal Electrical Safety Codes and Utility Joint Trench Standards (NEC 300.5 & NESC Rule 353). While primary 15kV distribution trench depths meet the required 42-inch cover specification, secondary low-voltage depths and gas-to-electric radial separation fall below mandatory safety thresholds. Formal engineering plan approval must be withheld until the developer submits revised construction drawings correcting trench profiles in Segments B and D.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary (15kV) Conduit Depth of Cover** | 42.0 in | 42.0 in | 0.0% | Normal |
| **Secondary (120/240V) Depth of Cover** | 24.0 in | 30.0 in | -20.0% | Warning |
| **Gas-to-Electric Radial Separation** | 8.0 in | 12.0 in | -33.3% | Critical |
| **Telecom-to-Power Vertical Clearance** | 12.0 in | 12.0 in | 0.0% | Normal |
| **Detectable Warning Ribbon Depth** | 6.0 in | 12.0 in (below grade) | -50.0% | Warning |
| **Select Sand Bedding Thickness** | 4.0 in | 6.0 in | -33.3% | Warning |
| **Trench Sloping/Shoring Spec (>5 ft)** | 1.5:1 (Type C) | 1.5:1 (OSHA Type C) | 0.0% | Normal |

---

### Visualization Triggers
**Recommended Visualization:** Grouped Horizontal Bar Chart comparing blueprint proposed dimensions against standard municipal trench specifications.

```json
{
  "chart_type": "bar",
  "title": "Green Valley Phase 2 Trenching Compliance vs Municipal Safety Code",
  "categories": [
    "Primary Electric Cover",
    "Secondary Electric Cover",
    "Gas-Electric Radial Clearance",
    "Telecom Vertical Separation",
    "Warning Ribbon Depth",
    "Bedding Thickness"
  ],
  "series": [
    {
      "name": "Proposed Blueprint",
      "data": [42.0, 24.0, 8.0, 12.0, 6.0, 4.0],
      "unit": "inches"
    },
    {
      "name": "Municipal/Utility Code Standard",
      "data": [42.0, 30.0, 12.0, 12.0, 12.0, 6.0],
      "unit": "inches"
    }
  ]
}
```

---

### Actionable Recommendations

- **Issue Blueprint Correction Notice**: Transmit a formal plan-check rejection for Segments B and D requiring the developer to adjust secondary trench depths to a minimum of 30 inches and restore gas-electric radial clearance to $\ge 12$ inches.
- **Enforce Sand Bedding and Ribbon Standards**: Direct the civil contractor to update trench section details to reflect 6 inches of select sand bedding (100% passing 3/8" sieve) and warning tape placement at 12 inches below finished grade.
- **Mandate Pre-Backfill Site Inspection**: Schedule an on-site utility safety inspection checkpoint prior to backfilling to verify conduit separation, sweep radius ($\ge 36$ in), and bedding compaction.
- **Cross-Utility Coordination**: Notify the municipal gas authority of joint-trench proximity conflicts along Feeder Path GV-2.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "operation_type": "DEVELOPER_PERMIT_APPROVAL_HOLD",
  "project_id": "PRJ-GV-PH2",
  "project_name": "Green Valley Subdivision Phase 2",
  "risk_level": "High (Gas-Electric Clearance Violation)",
  "action": "Transmit Official Blueprint Revision Notice and Hold Excavation Clearance Permit",
  "authorizer_required": "Lead Distribution Planning Engineer / Municipal Code Official",
  "timestamp_utc": "2023-10-24T12:00:00Z"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Approve the underground conduit trenching inspection checklist and schedule field inspector site verification."

**Agent Response:**
### Executive Summary
**The preliminary underground conduit trenching inspection checklist has been validated against standard utility electric service specifications and clearance mandates. All primary structural parameters—including trench depth, bedding thickness, and utility separation clearances—meet compliance thresholds for pre-pour and backfill inspection readiness. Formal sign-off and dispatch of field inspection personnel constitute a Tier 2 operational trigger requiring Human-In-The-Loop (HITL) authorization prior to work order execution.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary/Secondary Trench Depth** | 36.0 in | 36.0 in (Min. Cover) | 0.0% | Normal |
| **Trench Base Width** | 18.0 in | 12.0 in (Minimum) | +50.0% | Normal |
| **Sand Bedding / Cushion Thickness** | 4.0 in | 4.0 in (Class 1 Sand) | 0.0% | Normal |
| **Conduit Clearance to Wet Utilities** | 12.0 in | 12.0 in (Radial Min.) | 0.0% | Normal |
| **Detectable Warning Ribbon Position** | 12.0 in | 12.0 in below grade | 0.0% | Normal |
| **811 Locate Ticket Status** | Active / Valid | Active Ticket Required | 0.0% | Normal |

---

### Visualization Triggers
**Recommended Chart**: Grouped Bar Chart comparing field-submitted trench measurements against minimum utility clearance baselines.

```json
{
  "chart_type": "bar",
  "title": "Trench Dimensional Verification vs. Minimum Engineering Standards",
  "data": {
    "categories": [
      "Trench Cover Depth (in)",
      "Trench Width (in)",
      "Bedding Layer (in)",
      "Joint Trench Separation (in)",
      "Warning Ribbon Depth (in)"
    ],
    "series": [
      {
        "name": "Actual Field Measurement",
        "values": [36, 18, 4, 12, 12]
      },
      {
        "name": "Utility Baseline Requirement",
        "values": [36, 12, 4, 12, 12]
      }
    ]
  }
}
```

---

### Actionable Recommendations
* **Verify Site Readiness**: Confirm that trench spoils are set back at least 2 feet from the excavation edge in accordance with OSHA Subpart P safety standards prior to inspector arrival.
* **Open Trench Protocol**: Ensure trench shoring/sloping remains secure and no backfill is placed before physical on-site inspector verification and photo-logging.
* **Customer Communication**: Dispatch automated SMS/email notification to the primary project contractor confirming inspection window once human approval is logged.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "FIELD_DISPATCH_AND_CHECKLIST_APPROVAL",
  "domain": "Customer Engagement / Field Operations",
  "target_entity": "Underground Distribution Construction",
  "details": {
    "workflow": "New Service Trenching Verification",
    "requested_action": "Approve Checklist & Dispatch Field Inspector",
    "safety_pre_check": "811 Locate Active, Trench Open, Shoring Compliant",
    "estimated_window": "Next Business Day (08:00 - 12:00)",
    "requires_hitl_signature": true
  }
}
```
