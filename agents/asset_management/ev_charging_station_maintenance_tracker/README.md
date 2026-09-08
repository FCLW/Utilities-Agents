# ⚡ Ev Charging Station Maintenance Tracker

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of ev charging station maintenance tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Ev Charging Station Maintenance Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank ev charging station maintenance tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.ev_charging_station_maintenance_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which DC fast chargers in the municipal fleet hub are reporting ground fault errors or cable overheating?"

**Agent Response:**
### Executive Summary
**Telemetry analysis for the Municipal Fleet Hub identified two DC Fast Chargers exhibiting active ground fault alarms (DCFC-MFH-03 and DCFC-MFH-07) and two units experiencing critical liquid-cooled cable overheating exceeding thermal thresholds (DCFC-MFH-01 and DCFC-MFH-07). Station DCFC-MFH-07 represents a compound high-risk failure with simultaneous ground insulation breakdown and thermal runaway at 84.6°C. Immediate remote de-energization and field technician dispatch are recommended to mitigate insulation degradation and electrical hazard risks.**

---

### Key Operational Metrics & Status Overview

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Max Cable Operating Temp (DCFC-MFH-07)** | 84.6 °C | ≤ 65.0 °C | +30.15% | **Critical** |
| **Max Cable Operating Temp (DCFC-MFH-01)** | 78.4 °C | ≤ 65.0 °C | +20.62% | **Critical** |
| **Ground Insulation Resistance (DCFC-MFH-03)** | 0.08 MΩ | ≥ 1.00 MΩ | -92.00% | **Critical** |
| **Ground Insulation Resistance (DCFC-MFH-07)** | 0.03 MΩ | ≥ 1.00 MΩ | -97.00% | **Critical** |
| **Hub Asset Health Index (AHI)** | 62.4 / 100 | ≥ 85.0 / 100 | -26.59% | **Warning** |
| **Active DCFC Availability** | 66.7% (8/12 Online) | ≥ 95.0% | -29.79% | **Warning** |

---

### Asset Exception Breakdown: Municipal Fleet Hub

| Charger Unit ID | Asset ID | Fault / Telemetry Anomaly | Telemetry Value | Limit / Threshold | Asset Health Index (AHI) | Operational Impact |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **DCFC-MFH-01** | `EVSE-MFH-101` | Liquid-Cooled Cable Overheat | 78.4 °C | Max 65.0 °C | 54.0 | Derated (Power Throttled) |
| **DCFC-MFH-03** | `EVSE-MFH-103` | Ground Fault (Isolation Low) | 0.08 MΩ | Min 1.00 MΩ | 42.0 | Auto-Tripped / Interlocked |
| **DCFC-MFH-07** | `EVSE-MFH-107` | Ground Fault & Cable Overheat | 84.6 °C / 0.03 MΩ | 65.0 °C / 1.00 MΩ | 28.5 | Emergency Locked Out |
| **DCFC-MFH-12** | `EVSE-MFH-112` | Pre-Trip Thermal Warning | 63.8 °C | Warning @ 60.0 °C | 71.0 | Monitored Under Load |

---

### Visualization Trigger

**Recommended Chart**: Multi-Metric Bar & Status Chart (Cable Temperature vs. Ground Fault Isolation)

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": "Municipal Fleet Hub DCFC Fault & Thermal Distribution",
  "data": {
    "values": [
      {"charger_id": "DCFC-MFH-01", "cable_temp_c": 78.4, "insulation_mohm": 2.45, "status": "Cable Overheat"},
      {"charger_id": "DCFC-MFH-02", "cable_temp_c": 44.1, "insulation_mohm": 3.10, "status": "Normal"},
      {"charger_id": "DCFC-MFH-03", "cable_temp_c": 42.1, "insulation_mohm": 0.08, "status": "Ground Fault"},
      {"charger_id": "DCFC-MFH-07", "cable_temp_c": 84.6, "insulation_mohm": 0.03, "status": "Compound Critical"},
      {"charger_id": "DCFC-MFH-12", "cable_temp_c": 63.8, "insulation_mohm": 1.85, "status": "Thermal Warning"}
    ]
  },
  "mark": "bar",
  "encoding": {
    "x": {"field": "charger_id", "type": "nominal", "title": "Charger Asset"},
    "y": {"field": "cable_temp_c", "type": "quantitative", "title": "Cable Temperature (°C)"},
    "color": {
      "field": "status",
      "type": "nominal",
      "scale": {
        "domain": ["Normal", "Thermal Warning", "Cable Overheat", "Ground Fault", "Compound Critical"],
        "range": ["#2ecc71", "#f39c12", "#e67e22", "#e74c3c", "#8e44ad"]
      }
    }
  }
}
```

---

### Actionable Recommendations

1. **Safety Isolation**: Ensure software interlocks remain engaged for **DCFC-MFH-03** and **DCFC-MFH-07** to prevent vehicle coupler energization under low ground resistance conditions (< 1.0 MΩ).
2. **Coolant System Diagnostic**: Inspect the closed-loop glycol/chiller circulation pumps on **DCFC-MFH-01** and **DCFC-MFH-07** for flow restriction, pump cavitation, or low coolant reservoir levels.
3. **Physical Inspection**: Inspect cable harness jacket integrity, strain reliefs, and connector pins for physical damage, carbon tracking, or moisture ingress causing the ground faults.
4. **Fleet Load Balancing**: Reroute high-priority municipal fleet vehicles to chargers **DCFC-MFH-04 through DCFC-MFH-06** and **DCFC-MFH-08 through DCFC-MFH-11** to maintain required fleet state of charge (SoC) timelines.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "GRID_ASSET_ISOLATION_AND_DISPATCH",
  "authorization_level": "Tier 2 - Human Operator Approval Required",
  "target_assets": [
    {
      "asset_id": "EVSE-MFH-107",
      "charger_id": "DCFC-MFH-07",
      "location": "Municipal Fleet Hub - Bay 7",
      "action": "REMOTE_DE_ENERGIZE_LOCKOUT"
    },
    {
      "asset_id": "EVSE-MFH-103",
      "charger_id": "DCFC-MFH-03",
      "location": "Municipal Fleet Hub - Bay 3",
      "action": "REMOTE_DE_ENERGIZE_LOCKOUT"
    },
    {
      "asset_id": "EVSE-MFH-101",
      "charger_id": "DCFC-MFH-01",
      "location": "Municipal Fleet Hub - Bay 1",
      "action": "RESTRICT_OUTPUT_50KW"
    }
  ],
  "work_order": {
    "priority": "P1_CRITICAL",
    "crew_type": "EVSE_CERTIFIED_HIGH_VOLTAGE",
    "scope": "Investigate ground isolation faults, coolant flow rates, and cable insulation integrity."
  },
  "requires_confirmation": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Track the mean time between failures (MTBF) and connector wear rates for Level 3 CCS chargers over the past quarter."

**Agent Response:**
### Executive Summary
**Fleet-wide Mean Time Between Failures (MTBF) for Level 3 CCS fast chargers averaged 738 operating hours over the past quarter, representing an 8.9% decline relative to the utility benchmark target of 810 hours. Connector wear rates in high-utilization nodes (Highway Corridor and Metro Central) exceeded normal operational tolerances, with average contact degradation reaching 82.6% and contact resistance increasing to 3.8 mΩ. Immediate proactive maintenance and contact pin replacements are required for 18 identified high-wear dispensing units to avert thermal de-rating and unscheduled charger outages.**

---

### Quantitative Performance Metrics

#### Fleet Performance Overview (Past Quarter - Level 3 CCS Assets)
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Mean Time Between Failures (MTBF)** | 738.0 hrs | 810.0 hrs | -8.89% | Warning |
| **Average Connector Wear Rate** | 61.88% of rated cycle life | ≤ 50.0% | +23.76% | Warning |
| **Peak Connector Wear (Highway Corridor)** | 82.60% of rated cycle life | ≤ 50.0% | +65.20% | Critical |
| **Contact Resistance (CCS Pin Interfaces)** | 3.24 mΩ | ≤ 2.50 mΩ | +29.60% | Warning |
| **Asset Health Index (AHI)** | 78.4 / 100 | ≥ 85.0 / 100 | -7.76% | Warning |
| **Mean Time to Repair (MTTR)** | 4.1 hrs | ≤ 4.0 hrs | +2.50% | Normal |
| **Predictive Remaining Useful Life (RUL - High Wear Units)** | 42 days (95% CI: [36, 48]) | ≥ 90 days | -53.33% | Critical |

---

#### Zonal Asset Health & Connector Telemetry Breakdown
| Grid Zone ID | Active CCS L3 Units | Total Op Hours | Failure Count | Zone MTBF (hrs) | Avg Connector Wear (%) | Avg Contact Resistance (mΩ) | Zone AHI | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zone-1 (Metro Central)** | 24 | 44,640 | 72 | 620.0 | 74.20% | 3.42 | 76.8 | Warning |
| **Zone-2 (North Suburb)** | 18 | 33,600 | 40 | 840.0 | 52.80% | 2.45 | 84.1 | Normal |
| **Zone-3 (Industrial East)** | 14 | 26,390 | 29 | 910.0 | 41.50% | 2.10 | 88.5 | Normal |
| **Zone-4 (Highway Corridor)** | 30 | 59,400 | 110 | 540.0 | 82.60% | 3.80 | 71.2 | Critical |
| **Zone-5 (South Hub)** | 16 | 29,640 | 38 | 780.0 | 58.30% | 2.65 | 81.6 | Normal |

*Analytical Assumptions & Telemetry Context: Rated connector mechanical lifetime is standardized at 10,000 insertion cycles per SAE J1772/IEC 62196-3 standards. Wear rate is calculated as $(\text{Logged Ingress Cycles} / \text{Rated Design Cycles}) \times 100$. Contact resistance is sampled continuously via onboard liquid-cooled dispensing loop sensors under full 350 kW load.*

---

### Visualization: MTBF vs. Connector Wear Rate Across Zones

```json
{
  "chart_type": "bar",
  "title": "Level 3 CCS Fleet: MTBF (Hours) vs Connector Wear Rate (%) - Past Quarter",
  "xAxis": {
    "type": "category",
    "data": [
      "Zone-1 (Metro Central)",
      "Zone-2 (North Suburb)",
      "Zone-3 (Industrial East)",
      "Zone-4 (Highway Corridor)",
      "Zone-5 (South Hub)"
    ]
  },
  "yAxis": [
    {
      "type": "value",
      "name": "MTBF (Hours)",
      "min": 0,
      "max": 1200
    },
    {
      "type": "value",
      "name": "Connector Wear (%)",
      "min": 0,
      "max": 100
    }
  ],
  "series": [
    {
      "name": "MTBF (Hours)",
      "type": "bar",
      "data": [620, 840, 910, 540, 780]
    },
    {
      "name": "Avg Connector Wear (%)",
      "type": "line",
      "yAxisIndex": 1,
      "data": [74.2, 52.8, 41.5, 82.6, 58.3]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Targeted Connector Replacement**: Issue scheduled work orders for the 18 high-wear CCS connector assemblies in **Zone-4 (Highway Corridor)** and **Zone-1 (Metro Central)** that exceed the 80% wear threshold and 3.5 mΩ contact resistance.
2. **Thermal De-Rating Mitigation**: Re-calibrate liquid-cooling loop flow valves on Highway Corridor units to prevent thermal throttling until connector pin assemblies are replaced.
3. **Preventative Maintenance Interval Adjustment**: Shorten visual latch/pin inspection intervals from 90 days to 30 days on feeders experiencing > 40 daily plug-in cycles.
4. **Spare Parts Staging**: Pre-stage 25 replacement CCS liquid-cooled cable/gun assemblies in the central maintenance depot to keep Mean Time to Repair (MTTR) below the 4.0-hour SLA.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "SCHEDULE_OUTAGE_AND_DISPATCH_MAINTENANCE"
  target_assets:
    - asset_group: "Level 3 CCS Chargers - Zone-4 (Highway Corridor)"
    - high_priority_count: 12
    - expected_downtime_per_asset: "2.5 Hours"
  operation_details:
    scope: "De-energize dispenser DC bus, replace worn CCS contact pin cartridges, flush liquid cooling lines, and perform insulation resistance testing (IEEE Std 43)."
    safety_compliance: "OSHA 1910.269 / NFPA 70E Arc Flash Boundary Compliance"
    impact: "Temporary 25% capacity reduction across Highway Corridor charging plaza during off-peak window (01:00 - 05:00 UTC)."
  confirmation_status: "PENDING_OPERATOR_APPROVAL"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue a remote reboot and preventive field service dispatch for Charger Hub #14 at Airport North."

**Agent Response:**
### Executive Summary
**Charger Hub #14 at Airport North is exhibiting thermal degradation and abnormal controller latency, resulting in an Asset Health Index (AHI) drop to 54.0 (Warning/Critical). Direct autonomous execution of physical state modifications (remote reboot) and crew dispatches is restricted under utility safety guardrails and requires Human-In-The-Loop (HITL) authorization. A Tier 2 operational payload has been staged below for operator verification and confirmation.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Health Index (AHI)** | 54.0 | 90.0 | -40.0% | **Critical** |
| **Connector Thermal Sensor** | 78.5 °C | 45.0 °C | +74.4% | **Warning** |
| **Connector Isolation Resistance** | 1.2 MΩ | 10.0 MΩ | -88.0% | **Critical** |
| **Controller Latency** | 1,420 ms | 150 ms | +846.7% | **Warning** |
| **Remaining Useful Life (RUL - Power Module)** | 420 Operating Hours | 3,500 Operating Hours | -88.0% | **Critical** |

---

### Visualization Trigger
- **Recommended Chart**: Bar Comparison Chart (Current Telemetry vs. Baseline Thresholds).
```json
{
  "chart_type": "bar",
  "title": "Charger Hub #14 Telemetry vs. Baseline Target",
  "labels": ["Thermal Sensor (°C)", "Isolation Resistance (MΩ)", "Controller Latency (x10 ms)", "Asset Health Index (AHI)"],
  "datasets": [
    {
      "label": "Current Value",
      "data": [78.5, 1.2, 142.0, 54.0]
    },
    {
      "label": "Baseline Target",
      "data": [45.0, 10.0, 15.0, 90.0]
    }
  ]
}
```

---

### Actionable Recommendations
- **Authorize Staged Reboot**: Confirm the remote reboot payload to clear unresponsive controller threads and re-initialize the power electronics telemetry interface.
- **Approve Preventive Dispatch**: Approve Work Order generation for a Level 2 Field Technician to inspect isolation degradation and replace aging thermal paste/connectors at Airport North.
- **Reroute Active EV Traffic**: Temporarily de-rate or set Charger Hub #14 to "Maintenance Reserved" in the customer-facing charging availability portal to prevent stranded sessions.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_id": "ACT-EVSE-2024-0914",
  "asset_id": "EVSE-HUB-14-AIRPORT-NORTH",
  "location": "Airport North EV Plaza - Zone B",
  "operations_requested": [
    {
      "type": "REMOTE_REBOOT",
      "target_component": "OCPP_PRIMARY_CONTROLLER",
      "safety_interlock_verified": true,
      "session_active": false
    },
    {
      "type": "FIELD_SERVICE_DISPATCH",
      "work_order_type": "PREVENTIVE_MAINTENANCE",
      "priority": "HIGH",
      "skill_required": "EVSE_LVL2_CERTIFIED",
      "estimated_duration_hours": 2.5
    }
  ],
  "requires_human_approval": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```
