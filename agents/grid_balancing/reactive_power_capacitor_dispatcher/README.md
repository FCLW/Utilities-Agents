# ⚡ Reactive Power Capacitor Dispatcher

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of reactive power capacitor dispatcher is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Reactive Power Capacitor Dispatcher Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank reactive power capacitor dispatcher events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.reactive_power_capacitor_dispatcher_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which distribution substations are currently exhibiting a lagging power factor below 0.92 during heavy inductive motor loading?"

**Agent Response:**
### Executive Summary
**Real-time telemetry analysis identifies four distribution substations operating below the utility target power factor threshold of 0.95 lagging, specifically falling below 0.92 lagging under heavy industrial and pumping inductive motor load profiles. Substation `SUB-402 (Oakridge Industrial)` exhibits the most severe deficit at 0.86 lagging with a 14.8 MVAR uncompensated reactive power demand. Immediate multi-stage shunt capacitor bank dispatch is required to normalize bus voltages, mitigate line losses, and restore compliance with IEEE 519 / NERC standard operational criteria.**

---

### Data Presentation

#### 1. Fleet & Substation Power Factor Assessment
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **SUB-402 (Oakridge Industrial) PF** | 0.86 Lagging | 0.95 Lagging | -9.47% | **Critical** |
| **SUB-118 (Pine Valley Mfg) PF** | 0.88 Lagging | 0.95 Lagging | -7.37% | **Critical** |
| **SUB-305 (Harbor Pumping) PF** | 0.89 Lagging | 0.95 Lagging | -6.32% | **Warning** |
| **SUB-221 (North Commercial) PF** | 0.91 Lagging | 0.95 Lagging | -4.21% | **Warning** |
| **Total System Reactive Deficit** | 38.4 MVAR | 0.0 MVAR Target | +100.0% | **Critical** |
| **Average Substation Bus Voltage** | 0.962 p.u. | 1.000 p.u. | -3.80% | **Warning** |

#### 2. Substation Telemetry & Reactive Loading Breakdown
| Substation ID | Feeder ID | Active Power (MW) | Reactive Power (MVAR) | Power Factor | Inductive Load Type | Required MVAR Compensation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SUB-402** | FDR-402-A/B | 25.2 MW | 14.8 MVAR | **0.86 Lagging** | Heavy Industrial Induction Motors | +9.6 MVAR |
| **SUB-118** | FDR-118-C | 18.5 MW | 9.9 MVAR | **0.88 Lagging** | Manufacturing / Extrusion Drives | +5.8 MVAR |
| **SUB-305** | FDR-305-1 | 14.0 MW | 7.2 MVAR | **0.89 Lagging** | Municipal Water Pumping Arrays | +4.1 MVAR |
| **SUB-221** | FDR-221-E | 21.0 MW | 9.6 MVAR | **0.91 Lagging** | Large HVAC Chiller Compressors | +3.5 MVAR |

---

### Visualization Trigger
- **Recommended Chart**: Categorical Bar Chart comparing Current Lagging Power Factor against the Operational Target (0.95) across affected substations.

```json
{
  "chart_type": "bar",
  "title": "Substations with Lagging Power Factor Below 0.92",
  "xAxisLabel": "Substation",
  "yAxisLabel": "Power Factor (Lagging)",
  "data": {
    "labels": [
      "SUB-402 (Oakridge Industrial)",
      "SUB-118 (Pine Valley Mfg)",
      "SUB-305 (Harbor Pumping Station)",
      "SUB-221 (North Heavy Commercial)"
    ],
    "datasets": [
      {
        "label": "Current Power Factor",
        "data": [0.86, 0.88, 0.89, 0.91],
        "backgroundColor": ["#D32F2F", "#D32F2F", "#F57C00", "#F57C00"]
      },
      {
        "label": "Target Threshold",
        "data": [0.95, 0.95, 0.95, 0.95],
        "borderColor": "#388E3C",
        "type": "line",
        "fill": false
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Dispatch Substation Shunt Capacitor Banks**: Close available capacitor bank steps on `SUB-402` (Steps 1 & 2: 2x 4.8 MVAR) and `SUB-118` (Step 1: 6.0 MVAR) to bring bus power factor above 0.96 lagging.
- **Engage Downstream Distribution Feeder Switched Banks**: Issue close commands to automated pole-mounted switched capacitor banks on `FDR-305-1` and `FDR-221-E` to support mid-feeder voltage profiles.
- **Monitor Tap Changer Interactions**: Verify that Load Tap Changers (LTC) and Voltage Regulators do not experience excessive tap hunting during reactive step insertion.
- **Coordination Alert**: Notify the Industrial Account Management representative if continuous uncompensated motor operation at `SUB-402` breaches contractual power factor penalty tariffs (< 0.90 lagging).

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "SCADA_CAPACITOR_BANK_SWITCHING",
  "authorization_level": "Tier 2 - Human Operator Approval Required",
  "target_assets": [
    {
      "substation_id": "SUB-402",
      "device_tag": "CAP-402-B1",
      "operation": "CLOSE",
      "nominal_rating": "4.8 MVAR",
      "voltage_level": "13.8 kV"
    },
    {
      "substation_id": "SUB-402",
      "device_tag": "CAP-402-B2",
      "operation": "CLOSE",
      "nominal_rating": "4.8 MVAR",
      "voltage_level": "13.8 kV"
    },
    {
      "substation_id": "SUB-118",
      "device_tag": "CAP-118-B1",
      "operation": "CLOSE",
      "nominal_rating": "6.0 MVAR",
      "voltage_level": "13.8 kV"
    }
  ],
  "expected_post_switching_pf": {
    "SUB-402": "0.97 Lagging",
    "SUB-118": "0.96 Lagging"
  },
  "interlock_status": "All pre-switching voltage and lockout timer interlocks clear",
  "approval_required": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate the voltage profile improvement along Circuit 7 before and after switching in the 1,200 kVar capacitor bank."

**Agent Response:**
### Executive Summary
**Switching in the 1,200 kVar shunt capacitor bank at Node 7-C resolves severe downstream undervoltage violations along Circuit 7, elevating the tail-end feeder voltage from an out-of-spec 0.922 p.u. to a compliant 0.958 p.u. (+3.90%). Feeder-head power factor improves from 0.865 lagging to 0.982 lagging, significantly reducing upstream reactive power demand and lowering circuit technical $I^2R$ line losses by 18.4%. This dispatch action successfully brings all feeder nodes within ANSI C84.1 Range A voltage requirements (0.950 – 1.050 p.u.).**

---

### Quantitative Voltage & Reactive Power Analysis

| Metric | Current Value (Post-Switch) | Baseline / Target (Pre-Switch / Spec) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Feeder End Voltage (Node 7-End)** | 0.958 p.u. | 0.922 p.u. (Target: $\ge$ 0.950 p.u.) | +3.90% | **Normal** |
| **Capacitor Bus Voltage (Node 7-C)** | 0.972 p.u. | 0.938 p.u. (Target: $\ge$ 0.950 p.u.) | +3.62% | **Normal** |
| **Mid-Feeder Voltage (Node 7-B)** | 0.981 p.u. | 0.958 p.u. (Target: 1.000 p.u.) | +2.40% | **Normal** |
| **Substation Bus Voltage** | 1.012 p.u. | 1.010 p.u. (Target: 1.015 p.u.) | +0.20% | **Normal** |
| **Feeder Power Factor (Substation Head)** | 0.982 Lagging | 0.865 Lagging (Target: $\ge$ 0.950) | +13.53% | **Normal** |
| **Feeder Reactive Power Flow ($Q_{\text{head}}$)** | 320 kVar | 1,520 kVar (Baseline) | -78.95% | **Normal** |
| **Feeder Active Line Losses ($P_{\text{loss}}$)** | 142 kW | 174 kW (Baseline) | -18.39% | **Normal** |

---

### Visualization: Feeder Voltage Profile

**Recommended Visualization Type:** Distance-to-Voltage Line Profile (p.u. vs. km)

```json
{
  "title": "Circuit 7 Voltage Profile (Pre vs. Post 1,200 kVar Capacitor Dispatch)",
  "xAxis": {
    "name": "Distance from Substation (km)",
    "categories": [
      "0.0 (Substation Bus)",
      "2.4 (Node 7-A)",
      "4.8 (Node 7-B)",
      "6.5 (Capacitor Bank 7-C)",
      "8.2 (Node 7-D)",
      "10.5 (Feeder End)"
    ]
  },
  "yAxis": {
    "name": "Voltage (p.u.)",
    "min": 0.920,
    "max": 1.040
  },
  "series": [
    {
      "name": "Pre-Switching Voltage (p.u.)",
      "data": [1.010, 0.982, 0.958, 0.938, 0.930, 0.922]
    },
    {
      "name": "Post-Switching Voltage (p.u.)",
      "data": [1.012, 0.995, 0.981, 0.972, 0.965, 0.958]
    },
    {
      "name": "ANSI C84.1 Lower Limit (p.u.)",
      "data": [0.950, 0.950, 0.950, 0.950, 0.950, 0.950]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Maintain Capacitor Bank In-Service Status**: Keep the 1,200 kVar bank closed during current load block conditions (peak/near-peak loading) to sustain tail-end ANSI C84.1 Range A compliance.
2. **Monitor Off-Peak Leading PF / High Voltage Risk**: Configure SCADA automated dispatch or VAR controller threshold to switch out the bank if feeder reactive power drops below 200 kVar inductive, preventing overvoltage ($>1.05\text{ p.u.}$) during light-load evening hours.
3. **LTC / Regulator Coordination**: Confirm substation Load Tap Changer (LTC) step positions do not hunt or interact dynamically with the switched capacitance.

---

### Tier 2 Operational Notice
*If a physical switching execution or SCADA control command needs to be sent to toggle this capacitor bank state in real-time, execute the human confirmation process below:*

```markdown
[TIER 2 ACTION REQUIRED]
- Action Type: SCADA Capacitor Bank Remote Control
- Target Asset: Circuit 7 Capacitor Bank (Asset ID: CAP-C7-1200)
- Target Operation: CLOSE / ENERGIZE (1,200 kVar)
- Justification: Mitigate ANSI C84.1 undervoltage violation at Node 7-End (pre-switch 0.922 p.u.)
- Human Approval Required: Dispatcher confirmation required prior to signal transmission.
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch a supervisory close command to Capacitor Bank C-2 at North Substation to boost feeder voltage."

**Agent Response:**
### 1. Executive Summary
**A supervisory close command request has been staged for Capacitor Bank C-2 at North Substation to correct localized bus and feeder voltage depression. In strict adherence to physical grid safety guardrails and Tier 2 SCADA operational controls, autonomous switching cannot be directly executed without human confirmation. A complete Tier 2 Human-In-The-Loop (HITL) verification payload has been prepared for operator review and SCADA dispatch authorization.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Bus Voltage (North Substation Feeder)** | 0.942 p.u. (11.68 kV) | 1.000 p.u. (12.47 kV) | -5.80% | Warning |
| **Reactive Power Demand (Q)** | +4.80 MVAR | +1.20 MVAR | +300.00% | Warning |
| **Capacitor Bank C-2 Nominal Rating** | 3.60 MVAR | 3.60 MVAR | 0.00% | Normal |
| **Post-Switching Projected Voltage** | 0.991 p.u. (12.36 kV) | 1.000 p.u. (12.47 kV) | -0.90% | Normal |
| **Interlock & Discharge Timer Status** | 312 s elapsed | > 300 s required | N/A | Normal (Ready) |

---

### 3. Visualization Triggers

**Recommended Visualization:** Time-Series Line Chart illustrating pre- and post-switching voltage trajectory relative to ANSI C84.1 Range A voltage limits (0.95 p.u. – 1.05 p.u.).

```json
{
  "chart_type": "line",
  "title": "North Substation Feeder Voltage Profile & Forecast",
  "x_axis": "Time (HH:MM)",
  "y_axis": "Voltage (p.u.)",
  "series": [
    {
      "name": "Target (1.0 p.u.)",
      "data": [
        {"x": "14:00", "y": 1.00},
        {"x": "14:15", "y": 1.00},
        {"x": "14:30", "y": 1.00},
        {"x": "14:45 (Projected)", "y": 1.00}
      ]
    },
    {
      "name": "Feeder Voltage",
      "data": [
        {"x": "14:00", "y": 0.965},
        {"x": "14:15", "y": 0.951},
        {"x": "14:30", "y": 0.942},
        {"x": "14:45 (Projected)", "y": 0.991}
      ]
    },
    {
      "name": "Lower ANSI Limit (0.95 p.u.)",
      "data": [
        {"x": "14:00", "y": 0.95},
        {"x": "14:15", "y": 0.95},
        {"x": "14:30", "y": 0.95},
        {"x": "14:45 (Projected)", "y": 0.95}
      ]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Operator Action Required:** Review the pre-switching telemetry and safety interlocks below before authorizing the supervisory close command.
- **Post-Close Monitoring:** Monitor transient overvoltage and harmonic distortion on the North Substation feeder following breaker closure.
- **Coordination:** Confirm downstream automatic voltage regulator (LTC/SVR) tap changer delay timers are coordinated to avoid hunting.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "SUPERVISORY_SWITCHING_EXECUTION",
  "substation_id": "SUB_NORTH_01",
  "feeder_id": "FDR_NORTH_1204",
  "asset_id": "CAP_BANK_C2",
  "asset_type": "Shunt Capacitor Bank",
  "command": "CLOSE",
  "capacity_mvar": 3.6,
  "safety_interlock_verification": {
    "discharge_timer_cleared": true,
    "lockout_relay_86_reset": true,
    "scada_control_permissive": true
  },
  "expected_impact": {
    "voltage_delta_pu": "+0.049 p.u.",
    "projected_feeder_voltage_pu": "0.991 p.u.",
    "reactive_power_compensation": "3.60 MVAR leading"
  },
  "status": "PENDING_OPERATOR_APPROVAL"
}
```
