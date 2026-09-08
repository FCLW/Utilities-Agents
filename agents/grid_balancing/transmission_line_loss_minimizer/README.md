# ⚡ Transmission Line Loss Minimizer

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of transmission line loss minimizer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Transmission Line Loss Minimizer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank transmission line loss minimizer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.transmission_line_loss_minimizer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What percentage of bulk generation is currently dissipated as I²R resistive thermal losses across the 345kV backbone?"

**Agent Response:**
### 1. Executive Summary
**Current real-time telemetry indicates that $I^2R$ resistive thermal losses across the 345kV transmission backbone account for 2.31% (385.8 MW) of total bulk generation (16,700 MW). This represents an elevated dissipation rate exceeding the seasonal target baseline of 1.85% (+24.86% delta) due to heavy corridor loading and reactive power circulating currents. Immediate voltage support and VAR optimization are recommended to bring backbone dissipation within nominal operational boundaries.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Bulk Generation Injected** | 16,700 MW | 16,500 MW | +1.21% | Normal |
| **345kV $I^2R$ Thermal Loss Dissipation** | 385.8 MW | 305.2 MW | +26.41% | Warning |
| **Backbone Loss Percentage** | 2.31% | 1.85% | +24.86% | Warning |
| **Average 345kV Backbone Voltage** | 338.2 kV (0.980 p.u.) | 345.0 kV (1.000 p.u.) | -1.97% | Warning |
| **Average Backbone Conductor Temp** | 68.4 °C | 55.0 °C | +24.36% | Warning |
| **System MVAR Imbalance** | +412 MVAR (Lagging) | 0 ± 50 MVAR | +724.0% | Critical |

---

### 3. Visualization Triggers

- **Recommended Visualization**: Time-Series Line Chart illustrating the 60-minute trajectory of 345kV backbone $I^2R$ loss percentage against baseline thresholds.

```json
{
  "chart_type": "line",
  "title": "345kV Backbone I²R Thermal Loss Percentage vs. Baseline",
  "data": {
    "labels": ["T-60m", "T-45m", "T-30m", "T-15m", "Current"],
    "datasets": [
      {
        "label": "Current 345kV Loss (%)",
        "data": [1.98, 2.05, 2.12, 2.24, 2.31],
        "borderColor": "#FFA500",
        "fill": false
      },
      {
        "label": "Nominal Target (%)",
        "data": [1.85, 1.85, 1.85, 1.85, 1.85],
        "borderColor": "#00FF00",
        "borderDash": [5, 5],
        "fill": false
      },
      {
        "label": "Critical Threshold (%)",
        "data": [2.50, 2.50, 2.50, 2.50, 2.50],
        "borderColor": "#FF0000",
        "borderDash": [2, 2],
        "fill": false
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

- **Voltage Profile Elevation**: Increase terminal bus voltages across key 345kV generating stations from 0.980 p.u. to 1.025 p.u. to suppress line current magnitudes ($I$) and reduce square-law ($I^2R$) dissipation.
- **Capacitor Bank Dispatch**: Switch in localized 345kV shunt capacitor banks at major downstream load-serving substations to provide local reactive compensation and eliminate reactive loop flows.
- **Phase Angle Regulator (PAR) Optimization**: Re-dispatch power flow across parallel 345kV double-circuit lines to equalize thermal loading and avoid single-circuit overheating.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "GRID_VOLTAGE_AND_REACTIVE_DISPATCH",
  "target_assets": [
    "SUBSTATION_345KV_CAP_BANK_4A",
    "SUBSTATION_345KV_CAP_BANK_4B",
    "GEN_BUS_345KV_VOLTAGE_SETPOINT"
  ],
  "proposed_command": "ENGAGE_SHUNT_CAPACITORS_AND_RAISE_GEN_SETPOINTS_TO_1.025_PU",
  "expected_impact": "Reduces 345kV backbone line losses by ~42.3 MW (approx. 0.25% of bulk generation), restoring operation to 2.06% within 15 minutes.",
  "safety_confirmation": "NERC/FERC standard voltage stability margins remain preserved (>1.00 p.u. and <1.05 p.u.). Requires Grid Balancing Operator authorization."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Compare system technical transmission losses under optimal power flow (OPF) voltage scheduling versus nominal setpoints."

**Agent Response:**
### Executive Summary
**Implementation of Optimal Power Flow (OPF) voltage scheduling reduces active transmission line losses ($I^2R$) by an aggregate 11.52% across the system compared to flat nominal (1.00 p.u.) setpoints. By strategically optimizing reactive power dispatch (VARs), capacitor bank switching, and transformer on-load tap changer (OLTC) steps, transmission line current magnitudes are minimized while maintaining nodal voltages within standard NERC/IEEE operational bands (0.95–1.05 p.u.). Adopting OPF-driven voltage control delivers an average system-wide demand loss reduction of 21.8 MW, mitigating thermal strain and yielding substantial operational cost efficiencies.**

---

### Data Presentation

| Metric | Current Value (OPF Scheduled) | Baseline / Target (Nominal Setpoints) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Average Active Power Losses ($P_{\text{loss}}$)** | 167.50 MW | 189.30 MW | -11.52% | Normal |
| **Peak Hour Active Losses (16:00)** | 237.90 MW | 268.20 MW | -11.30% | Normal |
| **Off-Peak Active Losses (03:00)** | 98.10 MW | 112.40 MW | -12.72% | Normal |
| **System Average Voltage Magnitude** | 1.032 p.u. | 1.000 p.u. | +3.20% | Normal |
| **Reactive Power Transmission Circulation ($Q_{\text{loss}}$)** | 384.20 MVAR | 496.80 MVAR | -22.67% | Normal |
| **Critical Branch Loading (>85% MVA Rating)** | 4 Lines | 11 Lines | -63.64% | Normal |
| **Maximum Voltage Deviation ($\Delta V_{\max}$)** | 0.038 p.u. | 0.072 p.u. | -47.22% | Normal |

---

### Visualization Trigger

**Recommended Chart Type**: Multi-Series Grouped Bar Chart / Diurnal Load-Loss Curve  
*Rationale*: Displays comparative active transmission losses across diurnal load periods (Off-Peak, Ramps, Peak), highlighting intervals of highest efficiency capture.

```json
{
  "chart_type": "bar",
  "title": "Transmission System Real Power Losses: Nominal Setpoints vs. OPF Voltage Scheduling",
  "categories": [
    "Off-Peak (00:00-06:00)",
    "Morning Ramp (06:00-11:00)",
    "Afternoon Peak (11:00-18:00)",
    "Evening Peak (18:00-22:00)",
    "Night Shoulder (22:00-24:00)",
    "System Total / Avg"
  ],
  "series": [
    {
      "name": "Nominal Setpoints (1.00 p.u.) Loss (MW)",
      "data": [112.4, 185.6, 268.2, 241.5, 138.7, 189.3]
    },
    {
      "name": "OPF Optimized Voltage Loss (MW)",
      "data": [98.1, 164.2, 237.9, 214.8, 122.5, 167.5]
    },
    {
      "name": "Loss Reduction (MW)",
      "data": [14.3, 21.4, 30.3, 26.7, 16.2, 21.8]
    }
  ]
}
```

---

### Actionable Recommendations

- **Automate Real-Time Optimal Reactive Power Dispatch (ORPD)**: Deploy dynamic generator Automatic Voltage Regulator (AVR) setpoint adjustments in 15-minute intervals to follow OPF profiles.
- **Coordinate Substation Shunt Capacitors**: Stage capacitor bank switching during the morning ramp (06:00–09:00) to provide localized VAR support and prevent upstream reactive flow over transmission corridors.
- **Optimize Transformer OLTC Schedules**: Adjust high-voltage autotransformer tap positions to maintain the bulk transmission backbone near 1.03–1.04 p.u. while respecting downstream distribution interface limits.
- **Enforce Reactive Power Reserve Margins**: Maintain dynamic VAR reserves on synchronized generators and synchronous condensers to maintain N-1 contingency voltage stability margins.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "GRID_VOLTAGE_DISPATCH_OVERRIDE",
  "target_substations": ["SUB-EAST-500KV", "SUB-NORTH-230KV", "SUB-CENTRAL-500KV"],
  "operations": [
    {
      "device_type": "GENERATOR_AVR",
      "device_ids": ["GEN-UNIT-101", "GEN-UNIT-104"],
      "parameter": "V_ref",
      "target_value": "1.035 p.u.",
      "previous_value": "1.000 p.u."
    },
    {
      "device_type": "SHUNT_CAPACITOR_BANK",
      "device_ids": ["CAP-BANK-500-1", "CAP-BANK-230-3"],
      "action": "CLOSE",
      "mvar_addition": 150.0
    },
    {
      "device_type": "OLTC",
      "device_ids": ["XFRM-AUTO-01"],
      "target_tap": "+2"
    }
  ],
  "estimated_hourly_loss_savings_mwh": 21.8,
  "requires_hitl_approval": true,
  "dispatcher_confirmation_timeout_sec": 300
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Adjust transformer tap changer positions and generator reactive dispatch to minimize transmission network losses."

**Agent Response:**
### Executive Summary
**Optimal Reactive Power Dispatch (ORPD) analysis has identified actionable adjustments across on-load tap changer (OLTC) positions and generator reactive power setpoints to mitigate transmission network $I^2R$ losses. Implementing the calculated dispatch targets will reduce total transmission active power losses by 14.3% (26.2 MW reduction) across the monitored network corridors while maintaining all bus voltages within standard NERC/IEEE $\pm 5\%$ nominal operating limits (0.95–1.05 p.u.). Because tap adjustments and generator MVAr modifications alter the physical grid state, this dispatch plan requires Human-In-The-Loop (HITL) Tier 2 operator authorization prior to SCADA command issuance.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Transmission Losses ($P_{\text{loss}}$)** | 181.0 MW | 154.8 MW | -14.48% | Warning |
| **Average Bus Voltage Profile** | 0.968 p.u. | 1.012 p.u. | +4.55% | Normal |
| **Critical Branch Voltage Deviation ($\Delta V_{\text{max}}$)** | -0.048 p.u. | -0.012 p.u. | -75.00% | Warning |
| **Generator Reactive Power Reserve** | 412 MVAr | 338 MVAr | -17.96% | Normal |
| **Substation 500/230kV OLTC Tap Offset** | Tap Step 0 (Nominal) | Tap Step +2 | +2 Steps | Normal |
| **Substation 230/115kV OLTC Tap Offset** | Tap Step -1 | Tap Step +1 | +2 Steps | Normal |
| **Reactive Power Flow across Central Tie** | 185 MVAr | 62 MVAr | -66.49% | Warning |

---

### Visualization Triggers

A comparative bar chart has been generated to illustrate transmission active power loss reduction across key corridors:

```json
{
  "chart_type": "bar",
  "title": "Transmission Active Power Loss Reduction by Zone (MW)",
  "categories": [
    "North Intertie (Zone 1)",
    "Central Corridor (Zone 2)",
    "Eastern Tie (Zone 3)",
    "Southern Metro (Zone 4)"
  ],
  "series": [
    {
      "name": "Current Loss (MW)",
      "data": [42.4, 58.1, 31.6, 48.9]
    },
    {
      "name": "Optimized Loss (MW)",
      "data": [36.8, 49.5, 27.2, 41.3]
    }
  ]
}
```

---

### Actionable Recommendations
- **Adjust Transformer Tap Changers**: Step up Substation 500/230 kV autotransformers (T-101, T-102) by +2 tap positions to elevate downstream voltage profiles and reduce line current magnitude.
- **Dispatch Generator MVAr Output**: Increase lagging reactive power dispatch at Gen-Unit 3 (+45 MVAr) and Gen-Unit 5 (+30 MVAr) to supply local reactive demand natively, eliminating high-loss long-distance MVAr wheeling.
- **Backdown Over-Excited Units**: Reduce Gen-Unit 1 reactive output by 25 MVAr to alleviate reactive congestion on the Central 500 kV corridor.
- **Monitor Voltage Constraints**: Ensure all substation secondary buses remain within NERC standard operating bands ($1.00 \text{ to } 1.04\text{ p.u.}$) post-switching.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "GRID_STATE_MODIFICATION",
  "domain": "Grid Balancing - Transmission Line Loss Minimizer",
  "risk_level": "Tier 2 - Physical Grid Control",
  "target_assets": [
    {
      "asset_id": "XFMR_SUB12_T101",
      "asset_type": "OLTC_Transformer",
      "parameter": "tap_position",
      "current_value": 0,
      "recommended_value": 2
    },
    {
      "asset_id": "XFMR_SUB12_T102",
      "asset_type": "OLTC_Transformer",
      "parameter": "tap_position",
      "current_value": 0,
      "recommended_value": 2
    },
    {
      "asset_id": "GEN_PLANT_3_U1",
      "asset_type": "Synchronous_Generator",
      "parameter": "q_setpoint_mvar",
      "current_value": 110.0,
      "recommended_value": 155.0
    },
    {
      "asset_id": "GEN_PLANT_5_U2",
      "asset_type": "Synchronous_Generator",
      "parameter": "q_setpoint_mvar",
      "current_value": 65.0,
      "recommended_value": 95.0
    },
    {
      "asset_id": "GEN_PLANT_1_U1",
      "asset_type": "Synchronous_Generator",
      "parameter": "q_setpoint_mvar",
      "current_value": 140.0,
      "recommended_value": 115.0
    }
  ],
  "expected_impact": {
    "total_loss_reduction_mw": 26.2,
    "efficiency_gain_pct": 14.48,
    "voltage_compliance": "NERC_FAC_011_COMPLIANT"
  },
  "confirmation_prompt": "Operator approval required: Confirm transmission OLTC tap step changes (+2 on T101/T102) and generator VAR setpoint modifications to execute ORPD loss optimization plan."
}
```
