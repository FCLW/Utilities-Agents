# ⚡ Thermal Plant Outage Availability Tracker

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of thermal plant outage availability tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Thermal Plant Outage Availability Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank thermal plant outage availability tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.thermal_plant_outage_availability_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which combined-cycle natural gas turbine units are currently on forced outage or scheduled maintenance turnaround?"

**Agent Response:**
### Executive Summary
**A total of four (4) Combined-Cycle Gas Turbine (CCGT) units are currently unavailable, accounting for 1,560 MW of offline generation capacity across the fleet. Two units are undergoing unplanned forced outages due to mechanical/thermal trip events (770 MW offline), while two units are progressing through scheduled major maintenance turnarounds (790 MW offline). Overall fleet thermal equivalent availability factor (EAF) has dropped to 87.2%, requiring production forecasting adjustments to maintain reserve margins.**

---

### Data Presentation

#### 1. Fleet Availability & Performance Metrics
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total CCGT Capacity on Outage** | 1,560 MW | 650 MW | +140.0% | **Critical** |
| **Forced Outage Rate (CCGT EFOR)** | 6.8% | ≤ 2.5% | +172.0% | **Critical** |
| **Scheduled Maintenance Outage** | 790 MW | 800 MW | -1.25% | **Normal** |
| **ETR Prediction Deviation** | 3.2 hrs | < 2.0 hrs | +60.0% | **Warning** |
| **Fleet Equivalent Availability Factor (EAF)** | 87.2% | ≥ 94.0% | -7.23% | **Warning** |

#### 2. Active CCGT Unit Outage Inventory
| Plant / Unit ID | Unit Configuration | Outage Classification | Root Cause / Scope | Offline (MW) | Total Capacity (MW) | Start Timestamp | Estimated Time to Restoration (ETR) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Clear Creek CCGT - Unit 1** | 2x1 CCGT (F-Class) | **Forced Outage (Unplanned)** | Gas Turbine Vibration Trip / Bearing Temp Exceedance | 450 MW | 450 MW | 2025-05-18 04:15 UTC | 2025-05-20 18:00 UTC |
| **Bayou Bend CCGT - Unit 2** | 1x1 CCGT (H-Class) | **Forced Outage (Unplanned)** | HRSG Economizer Tube Leak | 320 MW | 320 MW | 2025-05-19 11:30 UTC | 2025-05-22 06:00 UTC |
| **Pine Valley CCGT - Unit 3** | 2x1 CCGT (G-Class) | **Scheduled Maintenance** | Combustion Inspection (CI) & Hot Gas Path | 280 MW | 560 MW | 2025-05-10 00:00 UTC | 2025-05-25 23:59 UTC |
| **Delta Ridge CCGT - Unit 1** | 2x1 CCGT (J-Class) | **Scheduled Maintenance** | Major Turnaround / Steam Turbine Overhaul | 510 MW | 510 MW | 2025-05-01 00:00 UTC | 2025-05-31 23:59 UTC |

---

### Visualization Triggers
**Recommended Chart**: Stacked Bar Chart & Outage Timeline showing offline capacity distribution by outage classification and unit.

```json
{
  "chart_type": "bar",
  "title": "CCGT Outage Capacity by Unit and Classification",
  "categories": [
    "Clear Creek CCGT Unit 1 (Forced)",
    "Bayou Bend CCGT Unit 2 (Forced)",
    "Pine Valley CCGT Unit 3 (Scheduled)",
    "Delta Ridge CCGT Unit 1 (Scheduled)"
  ],
  "series": [
    {
      "name": "Offline Outage Capacity (MW)",
      "data": [450, 320, 280, 510]
    },
    {
      "name": "Available Capacity (MW)",
      "data": [0, 0, 280, 0]
    }
  ]
}
```

---

### Actionable Recommendations
- **Generation Dispatch Re-optimization**: Notify the Day-Ahead and Real-Time Production Planning desk to reallocate 770 MW of forced outage deficit to peaker assets (simple-cycle gas turbines) or evaluate wholesale market imports.
- **Root Cause & Telemetry Verification**: Dispatch field engineering to verify bearing vibration diagnostics at Clear Creek Unit 1 and monitor hydrostatic pressure testing at Bayou Bend Unit 2 HRSG.
- **NERC GADS Reporting**: Ensure all outage events and event timestamps conform strictly to NERC GADS event-reporting standards within standard filing windows.
- **ETR Tracking**: Re-evaluate restoration milestones twice daily to ensure ETR accuracy deviation remains within the < 2.0 hour target for grid reliability modeling.

### Example 2: Trend & Comparative Analysis
**User:** "Track equivalent forced outage rates (EFOR) and mean time to repair (MTTR) across the fossil generation fleet over the last year."

**Agent Response:**
### Executive Summary
**Fleet-wide Equivalent Forced Outage Rate (EFOR) over the trailing 12 months averaged 5.54%, exceeding the enterprise target baseline of 4.50% primarily driven by recurring boiler tube leaks at Prairie Coal Unit 1. Mean Time to Repair (MTTR) across the fossil generation fleet stands at 26.8 hours, reflecting an 11.7% increase against the benchmark of 24.0 hours due to supply chain procurement lead times for critical steam path components. Combined Cycle and Combustion Turbine assets continue to demonstrate top-quartile reliability with an aggregate EFOR of 3.78% and an average MTTR of 15.3 hours.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Average EFOR** | 5.54% | 4.50% | +23.11% | **Warning** |
| **Fleet Average MTTR** | 26.80 hrs | 24.00 hrs | +11.67% | **Warning** |
| **Riverside CCGT (2x1 650 MW) EFOR** | 3.42% | 3.80% | -10.00% | **Normal** |
| **Riverside CCGT MTTR** | 18.50 hrs | 20.00 hrs | -7.50% | **Normal** |
| **Blue Ridge Peaker CT (4x50 MW) EFOR** | 4.15% | 4.00% | +3.75% | **Normal** |
| **Blue Ridge Peaker CT MTTR** | 12.00 hrs | 14.00 hrs | -14.29% | **Normal** |
| **Prairie Coal Unit 1 (550 MW) EFOR** | 8.85% | 5.00% | +77.00% | **Critical** |
| **Prairie Coal Unit 1 MTTR** | 46.20 hrs | 28.00 hrs | +65.00% | **Critical** |
| **Prairie Coal Unit 2 (550 MW) EFOR** | 6.20% | 5.00% | +24.00% | **Warning** |
| **Prairie Coal Unit 2 MTTR** | 32.80 hrs | 28.00 hrs | +17.14% | **Warning** |
| **Valley Steam Station (320 MW) EFOR** | 5.10% | 4.80% | +6.25% | **Normal** |
| **Valley Steam Station MTTR** | 24.50 hrs | 22.00 hrs | +11.36% | **Warning** |
| **Equivalent Availability Factor (EAF - Fleet)** | 88.65% | 91.00% | -2.58% | **Warning** |

*Methodology Note: EFOR and MTTR calculations strictly conform to NERC Generating Availability Data System (GADS) IEEE Standard 762 definitions: $\text{EFOR} = \frac{\text{FOH} + \text{EFDH}}{\text{SH} + \text{FOH} + \text{EFDHRS}} \times 100$.*

---

### Visualization Triggers
- **Recommended Chart Type**: Dual-Axis Grouped Bar & Line Chart (EFOR % vs. MTTR Hours per Generating Unit).

```json
{
  "chart_type": "dual_axis_bar_line",
  "title": "Fossil Generation Fleet EFOR & MTTR Performance (Trailing 12 Months)",
  "categories": [
    "Riverside CCGT",
    "Blue Ridge CT",
    "Prairie Coal Unit 1",
    "Prairie Coal Unit 2",
    "Valley Steam Station"
  ],
  "series": [
    {
      "name": "EFOR (%)",
      "type": "bar",
      "data": [3.42, 4.15, 8.85, 6.20, 5.10],
      "unit": "%",
      "target": 4.50
    },
    {
      "name": "MTTR (Hours)",
      "type": "line",
      "yAxisIndex": 1,
      "data": [18.5, 12.0, 46.2, 32.8, 24.5],
      "unit": "hrs",
      "target": 24.0
    }
  ],
  "yAxis": [
    {
      "name": "EFOR (%)",
      "min": 0,
      "max": 12
    },
    {
      "name": "MTTR (Hours)",
      "min": 0,
      "max": 60
    }
  ]
}
```

---

### Actionable Recommendations
- **Prairie Coal Unit 1 Root Cause Analysis**: Initiate an engineering root-cause failure analysis (RCFA) on the reheater and waterwall circuit tube failures responsible for 68% of the forced outage hours on Unit 1.
- **Critical Spares Staging**: Pre-stage standardized boiler tube weld sections and high-pressure steam valve packing kits at Prairie Station to compress MTTR from 46.2 hours toward the 28.0-hour design target.
- **Production Forecasting Calibration**: Adjust available thermal capacity deratings in Day-Ahead and Month-Ahead production cost models to reflect a 5.54% fleet EFOR baseline (up from 4.50%) to avoid reserve shortage penalties.
- **Predictive Maintenance Realignment**: Deploy high-frequency acoustic leak detection telemetry on Prairie Units 1 & 2 during the upcoming planned shoulder-month maintenance window.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Flag Unit 3 at Riverside Generating Station as available for commercial dispatch following successful turbine test sync."

**Agent Response:**
### Executive Summary
**Riverside Generating Station Unit 3 has completed its post-maintenance turbine synchronization test and is technically ready for return to service.** **Transitioning this asset to commercial dispatch availability represents a Tier 2 physical grid and market operation that modifies generation stack capacity and market bidding commitments.** **In accordance with grid reliability mandates and enterprise safety guardrails, human confirmation is required prior to updating the central Energy Management System (EMS) and Independent System Operator (ISO) dispatch registry.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Operational Status** | Synchronized / Testing Complete | Commercial Dispatch | N/A | Normal |
| **Available Generation Capacity** | 450.0 MW | 450.0 MW (Nameplate) | 0.0% | Normal |
| **Ramp Rate Capability** | 12.5 MW/min | 12.0 MW/min | +4.17% | Normal |
| **Vibration & Thermal Tolerances** | Nominal (Within Limits) | OEM Standard Limits | 0.0% | Normal |
| **Outage Duration vs. ETR** | 72.4 hrs | 72.0 hrs (Target ETR) | +0.56% | Normal |

---

### Visualization Triggers
- **Recommended Chart**: Unit Capacity & State Progression (Bar Chart / Step-Line) tracking transition from Outage $\rightarrow$ Synchronization Test $\rightarrow$ Commercial Availability.

```json
{
  "chart_type": "bar",
  "data": {
    "categories": ["Outage / Cold Standby", "Turbine Test Sync", "Available for Dispatch"],
    "series": [
      {
        "name": "Available Capacity (MW)",
        "data": [0, 150, 450]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- Verify synchronization telemetry records, vibration harmonics, and OEM bearing temperatures with the on-site Chief Plant Engineer.
- Transmit the verified unit status change to the Day-Ahead/Real-Time Generation Scheduling desk.
- Authorize the Tier 2 HITL payload below to update the enterprise asset registry, EMS availability status, and RTO/ISO market portal.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "UPDATE_THERMAL_ASSET_DISPATCH_AVAILABILITY",
  "plant_name": "Riverside Generating Station",
  "unit_id": "Unit 3",
  "requested_status": "AVAILABLE_FOR_COMMERCIAL_DISPATCH",
  "available_capacity_mw": 450.0,
  "sync_event_verified": true,
  "impact_scope": "ISO/RTO Market Bidding & Grid Dispatch Stack",
  "compliance_framework": "NERC GADS / IEEE 762",
  "requires_human_approval": true,
  "approver_role": "Generation Dispatch Operations Lead / Shift Supervisor"
}
```
