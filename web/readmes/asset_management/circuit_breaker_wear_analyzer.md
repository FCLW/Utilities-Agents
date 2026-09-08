# ⚡ Circuit Breaker Wear Analyzer

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of circuit breaker wear analyzer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Circuit Breaker Wear Analyzer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank circuit breaker wear analyzer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.circuit_breaker_wear_analyzer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many fault interruptions has Breaker CB-104 cleared since its last overhaul, and what is its remaining contact wear percentage?"

**Agent Response:**
### Executive Summary
**Circuit Breaker CB-104 has logged a cumulative total of 14 fault interruptions since its last major overhaul, contributing to accelerated contact erosion based on accumulated $I^2t$ thermal energy dissipation. The asset retains a Remaining Contact Wear of 48.5%, indicating that it has consumed 51.5% of its usable contact mass relative to the baseline manufacturer specification. The overall Asset Health Index (AHI) stands at 68.2 (Warning status), requiring condition-based maintenance scheduling before reaching the 20.0% critical threshold.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fault Interruptions Cleared** | 14 ops | 0 ops (Post-Overhaul) | +1400.0% | Warning |
| **Remaining Contact Wear** | 48.5% | 100.0% (New/Refurbished) | -51.5% | Warning |
| **Accumulated Interruption Energy ($\Sigma I^2t$)** | 1.82 × $10^9\text{ A}^2\text{s}$ | 3.50 × $10^9\text{ A}^2\text{s}$ (Max Rating) | -48.0% | Warning |
| **Asset Health Index (AHI)** | 68.2 / 100 | 100.0 / 100 | -31.8% | Warning |
| **Estimated Remaining Useful Life (RUL)** | 380 Days / ~8 Faults | 1,825 Days (5-Year Cycle) | -79.2% | Warning |
| **Mechanism Total Operations** | 142 ops | 2,000 ops (Class M2 Limit) | -92.9% | Normal |

*Analytical Note: Calculations comply with IEEE C37.09 / IEC 62271-100 standards for cumulative contact wear modeling derived from fault clearing currents, arc duration telemetry, and dynamic contact resistance benchmarks.*

---

### Visualization Triggers

**Recommended Visualization**: **Time-Series Line Chart** tracking cumulative fault clearing events against remaining contact wear percentage and wear warning thresholds.

```json
{
  "chart_type": "line",
  "title": "Breaker CB-104 Contact Wear Degradation vs. Fault Interruptions",
  "data": {
    "labels": [
      "Overhaul Baseline",
      "Fault Ops 1-4",
      "Fault Ops 5-8",
      "Fault Ops 9-11",
      "Fault Ops 12-14 (Current)"
    ],
    "datasets": [
      {
        "label": "Remaining Contact Wear (%)",
        "data": [100.0, 88.5, 74.0, 61.2, 48.5],
        "borderColor": "#FFA500",
        "fill": false
      },
      {
        "label": "Warning Threshold (%)",
        "data": [40.0, 40.0, 40.0, 40.0, 40.0],
        "borderColor": "#FF4500",
        "borderDash": [5, 5],
        "fill": false
      },
      {
        "label": "Critical Replacement Threshold (%)",
        "data": [20.0, 20.0, 20.0, 20.0, 20.0],
        "borderColor": "#DC143C",
        "borderDash": [2, 2],
        "fill": false
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Schedule Dynamic Contact Resistance Measurement (DCRM)**: Plan micro-ohm resistance testing during the next scheduled substation outage window to validate telemetry-derived wear estimates against physical contact erosion.
- **Adjust Recloser / Protection Settings**: Review feeder protection coordination upstream and downstream of CB-104 to minimize unnecessary high-current fault duty cycles while wear is elevated.
- **Stage Replacement Arcing Contacts**: Initiate procurement and staging of OEM contact kits (or vacuum/SF6 interrupter bottles) within the maintenance management system to prepare for overhaul prior to breaching the 40.0% warning threshold.
- **Continuous Monitoring**: Keep telemetry polling active on SOE (Sequence of Events) digital fault recorders (DFR) to capture exact clearing times ($t_{arc}$) and peak current ($I_{peak}$) on any subsequent trip events.

### Example 2: Trend & Comparative Analysis
**User:** "Plot the cumulative I²t fault energy curve for feeder breakers in Substation Alpha over the past 24 months."

**Agent Response:**
### Executive Summary
**Cumulative $I^2t$ fault energy analysis for Substation Alpha indicates critical contact erosion on Feeder Breaker CB-101 (Feeder F-01), which has reached 98.7% of its rated fault interruption capability following multiple high-magnitude through-fault interruptions over the past 24 months.** **Breaker CB-104 exhibits moderate contact wear at 61.3% of rated capacity, while breakers CB-102 and CB-103 remain well within operational safety limits.** **Immediate maintenance overhaul and interrupter bottle replacement are required for CB-101 to avoid catastrophic dielectric breakdown or failure-to-interrupt under subsequent short-circuit conditions.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **CB-101 (Feeder F-01) Cumulative $I^2t$** | 1,480 kA²·s (98.7% wear) | < 1,200 kA²·s (80% threshold) | +23.3% | **Critical** |
| **CB-101 Asset Health Index (AHI)** | 24.5 / 100 | ≥ 80.0 / 100 | -69.4% | **Critical** |
| **CB-104 (Feeder F-04) Cumulative $I^2t$** | 920 kA²·s (61.3% wear) | < 1,200 kA²·s (80% threshold) | -23.3% | **Warning** |
| **CB-104 Asset Health Index (AHI)** | 68.2 / 100 | ≥ 80.0 / 100 | -14.8% | **Normal** |
| **CB-102 (Feeder F-02) Cumulative $I^2t$** | 460 kA²·s (30.7% wear) | < 1,200 kA²·s (80% threshold) | -61.7% | **Normal** |
| **CB-102 Asset Health Index (AHI)** | 88.5 / 100 | ≥ 80.0 / 100 | +10.6% | **Normal** |
| **CB-103 (Feeder F-03) Cumulative $I^2t$** | 280 kA²·s (18.7% wear) | < 1,200 kA²·s (80% threshold) | -76.7% | **Normal** |
| **CB-103 Asset Health Index (AHI)** | 94.1 / 100 | ≥ 80.0 / 100 | +17.6% | **Normal** |

---

### Visualization Triggers

**Recommended Chart**: Multi-Series Time-Series Line Chart illustrating the 24-month cumulative $I^2t$ wear accumulation against the IEEE/Manufacturer 80% maintenance trigger and 100% rated rupture capacity.

```json
{
  "chart_type": "line",
  "title": "Cumulative I²t Interruption Energy Wear Curve (24-Month Trajectory) - Substation Alpha",
  "xAxis": {
    "label": "Timeline (Months)",
    "categories": [
      "M-24", "M-22", "M-20", "M-18", "M-16", "M-14", "M-12", "M-10", "M-08", "M-06", "M-04", "M-02", "Current"
    ]
  },
  "yAxis": {
    "label": "Cumulative I²t Fault Energy (kA²·s)",
    "unit": "kA²·s"
  },
  "series": [
    {
      "name": "CB-101 (Feeder F-01)",
      "data": [120, 180, 240, 310, 420, 510, 680, 750, 890, 1020, 1180, 1340, 1480],
      "color": "#e74c3c"
    },
    {
      "name": "CB-104 (Feeder F-04)",
      "data": [90, 130, 170, 220, 280, 340, 420, 490, 580, 670, 760, 850, 920],
      "color": "#f39c12"
    },
    {
      "name": "CB-102 (Feeder F-02)",
      "data": [80, 95, 110, 140, 160, 200, 230, 260, 290, 320, 370, 410, 460],
      "color": "#3498db"
    },
    {
      "name": "CB-103 (Feeder F-03)",
      "data": [50, 60, 75, 90, 110, 130, 150, 170, 190, 210, 230, 250, 280],
      "color": "#2ecc71"
    },
    {
      "name": "Maintenance Threshold (80% Limit - 1,200 kA²·s)",
      "data": [1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200, 1200],
      "type": "dashed",
      "color": "#e67e22"
    },
    {
      "name": "Nameplate Rating (100% Limit - 1,500 kA²·s)",
      "data": [1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500, 1500],
      "type": "dashed",
      "color": "#c0392b"
    }
  ]
}
```

---

### Actionable Recommendations

1. **Immediate Outage & Overhaul Scheduling**: Dispatch Substation Maintenance to inspect breaker CB-101 contacts, perform dynamic contact resistance measurement (DCRM), and replace vacuum/SF6 interrupter bottles.
2. **Protection Coordination Review**: Coordinate with Protection & Controls Engineering to investigate high fault frequency on Feeder F-01 (e.g., vegetation encroachment, recurring animal contact, reclosing sequence tuning).
3. **Condition-Based Monitoring (CBM)**: Re-evaluate breaker CB-104 inspection intervals given its steady climb past 60% rated $I^2t$ accumulation.
4. **Load / Feeder Transfer Consideration**: Consider transferring Feeder F-01 critical load to adjacent tie-feeders during scheduled maintenance to minimize customer interruption duration (SAIDI impact).

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action: SCADA_LOAD_TRANSFER_AND_BREAKER_ISOLATION
  substation_id: "SUB_ALPHA"
  target_asset: "CB-101"
  feeder_id: "F-01"
  reason: "Cumulative I²t contact wear at 98.7% of rating; mandatory maintenance isolation."
  safety_protocol: "IEEE C37.09 / OSHA 1910.269"
  requires_human_approval: true
  authorization_roles: ["Substation Operations Lead", "Grid Dispatch Supervisor"]
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Flag Breaker CB-104 for emergency contact inspection and temporarily reduce recloser shot attempts."

**Agent Response:**
### Executive Summary
**Circuit Breaker CB-104 has been flagged for prioritized emergency physical contact inspection due to cumulative $I^2t$ thermal-mechanical contact erosion exceeding safe operating limits.** **Telemetry indicates severe wear degradation, lowering the Asset Health Index (AHI) to critical levels and accelerating Remaining Useful Life (RUL) consumption.** **A temporary de-rating of the recloser auto-reclose sequence (reducing shot attempts from 3 to 1) has been staged to mitigate risk of catastrophic phase-to-ground or interrupter failure pending operator authorization.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Cumulative $I^2t$ Wear** | 94.8% | < 80.0% | +18.5% | **Critical** |
| **Asset Health Index (AHI)** | 28.5 / 100 | > 75.0 / 100 | -62.0% | **Critical** |
| **Remaining Useful Life (RUL)** | 12 Operations | > 150 Operations | -92.0% | **Critical** |
| **Contact Resistance ($R_{\mu\Omega}$)** | 62.4 $\mu\Omega$ | 25.0 $\mu\Omega$ | +149.6% | **Critical** |
| **Reclose Shot Cycle Limit** | 3 Shots | 1 Shot (Target De-rate) | -66.7% | **Warning** |

---

### Visualization Triggers

**Recommended Visualization:** Time-Series Line Chart illustrating cumulative contact wear accumulation ($I^2t$) leading to threshold breach across recent fault clearing events.

```json
{
  "chart_type": "line",
  "title": "Breaker CB-104 Cumulative Contact Wear Trajectory",
  "data": {
    "labels": ["T-5", "T-4", "T-3", "T-2", "T-1", "Current"],
    "datasets": [
      {
        "label": "Cumulative I²t Contact Wear (%)",
        "data": [62.0, 68.5, 74.2, 81.0, 89.4, 94.8],
        "borderColor": "#FF4C4C",
        "fill": false
      },
      {
        "label": "Wear Alarm Threshold (%)",
        "data": [80.0, 80.0, 80.0, 80.0, 80.0, 80.0],
        "borderColor": "#FFA500",
        "borderDash": [5, 5],
        "fill": false
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Immediate Work Order Generation**: Issue an urgent Field Maintenance Work Order for CB-104 interrupter chamber opening, contact erosion depth measurement, and SF6/oil dielectric integrity check.
- **Dynamic Protection Coordination**: Temporarily disable multi-shot auto-reclosing sequences on the associated protection relay to prevent re-strikes under heavy fault currents.
- **Continuous Thermal & Vibration Monitoring**: Maintain high-frequency acoustic/DGA monitoring on adjacent substation bays until physical inspection is complete.
- **HITL Approval Routing**: Escalate the protection setting modification to the SCADA Operations Engineer for execution.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PROTECTION_SETTING_MODIFICATION",
  "asset_id": "CB-104",
  "substation_id": "SUB-EAST-12",
  "parameters": {
    "setting_parameter": "AUTO_RECLOSE_SHOT_COUNT",
    "current_setting": 3,
    "proposed_setting": 1,
    "reclose_interval_override": "BLOCK_RAPID_AUTO_RECLOSE"
  },
  "justification": "Contact wear index at 94.8% exceeding IEEE C37.09 safety criteria. Multi-shot fault interrupter duty poses imminent failure risk.",
  "hitl_approval_required": true,
  "target_authority": "SCADA_OPERATIONS_DESK"
}
```
