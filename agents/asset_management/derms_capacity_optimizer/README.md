# ⚡ Derms Capacity Optimizer

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of derms capacity optimizer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Derms Capacity Optimizer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank derms capacity optimizer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.derms_capacity_optimizer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What is the aggregate flexible curtailment capacity available from residential battery and solar DERs on Feeder 12?"

**Agent Response:**
### Executive Summary
**The aggregate flexible curtailment capacity available from residential battery energy storage systems (BESS) and solar photovoltaics (PV) on Feeder 12 is currently calculated at 1,490.0 kW (1.49 MW). Residential solar PV provides 1,150.0 kW of dynamic inverter-based curtailment headroom, while co-located and standalone residential battery assets offer 340.0 kW of flexible charging/discharge modulation under IEEE 1547-2018 / IEEE 2030.5 interoperability standards. This resource envelope provides sufficient flexible headroom to mitigate local thermal constraints and reverse power flow without breaching customer reliability compacts.**

---

### DERMS Capacity & Flexibility Telemetry: Feeder 12

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Residential Solar PV Curtailment Capacity** | 1,150.0 kW | 1,000.0 kW | +15.0% | Normal |
| **Residential BESS Flexible Capacity (Charge/Modulation)** | 340.0 kW | 300.0 kW | +13.3% | Normal |
| **Total Aggregate Flexible Curtailment Headroom** | 1,490.0 kW | 1,300.0 kW | +14.6% | Normal |
| **Active Feeder Reverse Power Flow** | 820.0 kW | 1,200.0 kW (Limit) | -31.7% | Normal |
| **Average Residential BESS State of Charge (SoC)** | 78.4% | 50.0% (Min Reserve) | +56.8% | Normal |
| **Telemetry & Inverter Control Availability** | 98.2% | 95.0% | +3.4% | Normal |

---

### Visualization Triggers

**Recommended Chart**: Clustered Bar Chart / Stacked Flexibility Profile  
**Rendering Configuration**:

```json
{
  "chart_type": "bar",
  "title": "Feeder 12 DER Flexible Curtailment Capacity Breakdown",
  "categories": [
    "Residential Solar PV",
    "Residential Battery Storage (BESS)",
    "Aggregate Total"
  ],
  "series": [
    {
      "name": "Current Active Output (kW)",
      "data": [1420.0, 380.0, 1800.0]
    },
    {
      "name": "Flexible Curtailment Available (kW)",
      "data": [1150.0, 340.0, 1490.0]
    },
    {
      "name": "Reserve Floor / Non-Curtailable (kW)",
      "data": [270.0, 40.0, 310.0]
    }
  ]
}
```

---

### Actionable Recommendations

- **Prioritize Solar Inverter Real Power Curtailment**: Dispatch solar PV active power limit (P-limit) commands first via IEEE 2030.5 / OpenADR to preserve customer battery energy reserves for peak net-load evening hours.
- **Maintain Battery State of Charge (SoC) Buffers**: Constrain residential BESS absorption/charging modulation to avoid exceeding customer upper SoC thresholds (95% max) during solar peak hours.
- **Feeder Thermal Headroom Monitoring**: Continuously track Feeder 12 substation transformer loading; if reverse power exceeds 1,100 kW, trigger staged group curtailment signals across Aggregation Groups A & B.
- **Human-In-The-Loop Approval for Physical Dispatch**: If operational grid constraints necessitate active dispatch or automated bulk curtailment commands exceeding 500 kW, submit a Tier 2 dispatch request for Distribution Dispatcher authorization.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze the reverse power flow and voltage rise profile along Circuit 4B during peak PV generation hours."

**Agent Response:**
### Executive Summary
**Circuit 4B exhibits severe reverse power flow of up to -3.85 MW backfeeding into the substation during peak solar generation hours (11:00–14:00). Downstream feeder nodes (Node 4B-06 through 4B-10) breach the ANSI C84.1 Range A upper voltage limit (1.050 p.u.), peaking at 1.068 p.u. at the feeder terminus. DERMS Volt-VAR control and autonomous active power curtailment scheduling are required to mitigate thermal loading on the substation regulator and restore compliant voltage profiles.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Substation Reverse Flow** | -3,850 kW | 0 kW (Net Forward) | N/A | **Critical** |
| **Feeder Head Voltage (Node 4B-00)** | 1.015 p.u. | 1.000 p.u. | +1.50% | **Normal** |
| **Mid-Feeder Voltage (Node 4B-04)** | 1.042 p.u. | 1.000–1.050 p.u. | +4.20% | **Warning** |
| **Feeder Tail Voltage (Node 4B-10)** | 1.068 p.u. | ≤ 1.050 p.u. | +1.71% above limit | **Critical** |
| **LTC Tap Operations (Daily Cycle)** | 48 operations | ≤ 24 operations/day | +100.0% | **Warning** |
| **DER PV Capacity Online** | 6.20 MW | 4.50 MW Hosting Cap | +37.78% | **Critical** |

---

### Visualization Trigger
- **Recommended Chart**: Multi-Axis Line Chart (Voltage Profile vs. Feeder Distance with ANSI Limits & Reverse Flow Profile)

```json
{
  "chart_type": "line",
  "title": "Circuit 4B Voltage Rise & Reverse Flow Profile (11:00 - 14:00)",
  "x_axis": {
    "label": "Distance from Substation (km)",
    "data": ["0.0 km (4B-00)", "1.8 km (4B-02)", "3.5 km (4B-04)", "5.2 km (4B-06)", "6.9 km (4B-08)", "8.5 km (4B-10)"]
  },
  "series": [
    {
      "name": "Voltage Profile (p.u.)",
      "type": "line",
      "data": [1.015, 1.028, 1.042, 1.054, 1.062, 1.068],
      "y_axis_index": 0
    },
    {
      "name": "ANSI C84.1 Upper Limit (p.u.)",
      "type": "line",
      "data": [1.050, 1.050, 1.050, 1.050, 1.050, 1.050],
      "y_axis_index": 0
    },
    {
      "name": "Net Power Flow (kW)",
      "type": "bar",
      "data": [-3850, -2900, -1850, -950, -320, 45],
      "y_axis_index": 1
    }
  ]
}
```

---

### Actionable Recommendations
- **Dispatch Smart Inverter Volt-VAR Curves (IEEE 1547-2018)**: Enable reactive power absorption ($Q_{\text{inj}} < 0$) on aggregated commercial PV inverters connected between Nodes 4B-06 and 4B-10.
- **Dynamic Hosting Capacity Derating**: Dynamically adjust DER operating envelopes via IEEE 2030.5 / OpenADR during 11:30–13:30 to cap peak solar injection below the 4.50 MW circuit threshold.
- **Substation LTC & Switched Capacitor Coordination**: Lock or down-tap the substation Load Tap Changer (LTC) to nominal minus 2 steps (0.9875 p.u. base) and ensure mid-line capacitor bank `CAP-4B-1` is de-energized during peak irradiance.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "GRID_DER_DISPATCH_AND_TAP_LOCK",
  "target_circuit": "Circuit 4B",
  "substation_id": "SUB-NORTH-04",
  "dispatch_parameters": {
    "smart_inverter_mode": "VOLT_VAR_ABSORPTION",
    "reactive_power_target_kvar": -650,
    "active_power_curtailment_percent": 12.5,
    "ltc_tap_step_adjustment": -2,
    "effective_window": "11:00:00Z to 14:30:00Z"
  },
  "safety_validation": {
    "ansi_c84_1_compliant_projected": true,
    "max_projected_voltage_pu": 1.044,
    "reverse_flow_headroom_kw": 850
  },
  "requires_hitl_approval": true,
  "approver_role": "Distribution System Operator / DERMS Grid Engineer"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch a dynamic 1.5 MW reactive power absorption setpoint to connected commercial smart inverters in West Ridge."

**Agent Response:**
### Executive Summary
**The DERMS Capacity Optimizer has modeled and staged the dynamic reactive power absorption setpoint for commercial smart inverters across the West Ridge feeder network.** **Executing this dispatch will absorb dynamic reactive power (1.50 MVAr equivalent) to mitigate localized over-voltage and optimize feeder head power factor within IEEE 1547 standards.** **As this constitutes a direct physical grid setpoint modification, execution is staged pending Human-In-The-Loop (HITL) Tier 2 authorization.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Feeder Voltage Profile** | 1.042 p.u. | 1.000 p.u. | +4.20% | Warning |
| **Reactive Power Absorption** | 0.00 MVAr | 1.50 MVAr | -100.00% | Warning |
| **Feeder Power Factor (West Ridge)** | 0.92 Leading | 0.98 Lagging/Unity | -6.12% | Warning |
| **Total Inverter Nameplate Available** | 2.40 MVA | 1.50 MVA Target | +60.00% | Normal |
| **Asset Thermal Headroom** | 88.5% | > 80.0% | +10.63% | Normal |

---

### Visualization Triggers
**Recommended Chart Type:** Bar Chart — Feeder Group Allocation Profile

```json
{
  "chart_type": "bar",
  "title": "West Ridge Smart Inverter Reactive Power Dispatch Allocation",
  "xaxis": {
    "categories": ["Inverter Group WR-01", "Inverter Group WR-02", "Inverter Group WR-03", "Inverter Group WR-04"]
  },
  "yaxis": {
    "title": "Reactive Power Absorption (MVAr)"
  },
  "series": [
    {
      "name": "Target Absorption Setpoint",
      "data": [0.45, 0.40, 0.35, 0.30]
    }
  ]
}
```

---

### Actionable Recommendations
- **Authorize Dispatch**: Review the staged Tier 2 payload below to broadcast Volt-VAr curve setpoints via DNP3/IEEE 2030.5 to the West Ridge commercial aggregators.
- **Post-Dispatch Verification**: Monitor SCADA telemetry for feeder head voltage dampening toward nominal 1.005–1.015 p.u. within 60 seconds of command execution.
- **Feeder Balance Validation**: Ensure phase-level reactive power absorption remains balanced across all three phases (A, B, C) to avoid neutral current escalation.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_id": "ACT-DERMS-WR-2024-0891",
  "action_type": "GRID_DISPATCH_SETPOINT",
  "target_asset_group": "West Ridge Commercial Smart Inverters (WR-01 through WR-04)",
  "substation_id": "SUB-WEST-RIDGE-12",
  "feeder_id": "FDR-WR-4kV-01",
  "parameters": {
    "mode": "DYNAMIC_REACTIVE_POWER_ABSORPTION",
    "total_setpoint_mvar": 1.50,
    "ramp_rate_mvar_per_sec": 0.25,
    "duration_minutes": 120,
    "protocol": "IEEE 2030.5 / DNP3 Profile"
  },
  "safety_checks": {
    "thermal_overload_risk": "LOW",
    "voltage_violation_risk": "MITIGATED",
    "nerc_cip_compliant": true
  },
  "approval_required": "Grid Operations Supervisor / Human-In-The-Loop Confirmation"
}
```
