# ⚡ Solar Inverter String Fault Detector

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of solar inverter string fault detector is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Solar Inverter String Fault Detector Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank solar inverter string fault detector events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.solar_inverter_string_fault_detector_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which PV inverter strings in Solar Farm Bravo are exhibiting DC clipping or ground fault insulation breakdown?"

**Agent Response:**
### Executive Summary
**Telemetry analysis for Solar Farm Bravo indicates severe ground fault insulation breakdown on Inverter `INV-B02` (Strings 1 through 4) with isolation resistance dropping to critical levels below 50 kΩ against the 1,000 kΩ baseline. Concurrently, Inverter `INV-B01` (Strings 1–4) and `INV-B03` (Strings 1–4) are operating under persistent DC power saturation exceeding inverter AC nameplate thresholds by up to +12.4%, confirming active DC peak clipping during peak irradiance windows. Immediate field dispatch is required to mitigate fire and dielectric breakdown risks on `INV-B02`, while clipping profiles on `INV-B01` and `INV-B03` remain within designed thermal limits but require DC/AC oversizing re-benchmarking.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **INV-B02 Strings 1–2 Insulation Resistance ($R_{iso}$)** | 42.0 kΩ | ≥ 1,000.0 kΩ | -95.8% | **Critical** (Ground Fault Breakdown) |
| **INV-B02 Strings 3–4 Insulation Resistance ($R_{iso}$)** | 38.0 kΩ | ≥ 1,000.0 kΩ | -96.2% | **Critical** (Ground Fault Breakdown) |
| **INV-B01 Strings 1–4 DC/AC Power Ratio** | 108.5% | ≤ 100.0% | +8.5% | **Warning** (DC Peak Clipping) |
| **INV-B03 Strings 1–4 DC/AC Power Ratio** | 112.4% | ≤ 100.0% | +12.4% | **Warning** (DC Peak Clipping) |
| **INV-B04 Strings 1–2 Insulation Resistance ($R_{iso}$)** | 1,050.0 kΩ | ≥ 1,000.0 kΩ | +5.0% | **Normal** |
| **INV-B04 Strings 3–4 DC/AC Power Ratio** | 89.5% | ≤ 100.0% | -10.5% | **Normal** |

---

### Inverter Telemetry & Fault Signature Breakdown

1. **Ground Fault Insulation Degradation (`INV-B02`)**:
   - **Affected Strings**: String 1, String 2, String 3, String 4.
   - **Fault Mode**: Dielectric breakdown of PV DC conductor jackets or junction box moisture ingress leading to leakage currents ($I_{leak} > 300\text{ mA}$) and low $R_{iso}$ ($< 50\text{ k}\Omega$).
   - **Compliance/Safety Risk**: IEEE 1547 / NEC 690.41 compliance breach; elevated arc-fault and DC ground fault fire risk.

2. **DC Clipping / Power Saturation (`INV-B01` & `INV-B03`)**:
   - **Affected Strings**: `INV-B01` (Strings 1–4) and `INV-B03` (Strings 1–4).
   - **Operating Behavior**: DC input power exceeds the rated inverter AC inverter output capacity ($P_{DC} > P_{AC,max}$) during peak irradiance periods (> 850 W/m²), driving the Maximum Power Point Tracking (MPPT) algorithm to increase array voltage ($V_{mp} \rightarrow V_{oc}$) to throttle output power.

---

### Visualization Triggers

- **Recommended Visualization**: **Grouped Bar Chart / Inverter Diagnostics Heatmap** comparing Insulation Resistance ($R_{iso}$) against the safety threshold (1,000 kΩ) and DC/AC loading ratio (%) against clipping limits.

```json
{
  "chart_type": "bar",
  "title": "Solar Farm Bravo - String Insulation Resistance & DC Clipping Index",
  "data": {
    "labels": [
      "INV-B01 (Str 1-4)",
      "INV-B02 (Str 1-2)",
      "INV-B02 (Str 3-4)",
      "INV-B03 (Str 1-4)",
      "INV-B04 (Str 1-2)",
      "INV-B04 (Str 3-4)"
    ],
    "datasets": [
      {
        "label": "Insulation Resistance Riso (kOhm) [Threshold: 1000 kOhm]",
        "data": [1200, 42, 38, 1150, 1050, 1100],
        "unit": "kOhm"
      },
      {
        "label": "DC/AC Power Ratio (%) [Clipping Threshold: 100%]",
        "data": [108.5, 74.0, 71.5, 112.4, 91.2, 89.5],
        "unit": "%"
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Immediate Physical Isolation**: Open DC disconnect switches on `INV-B02` (Strings 1–4) to isolate degraded circuits and prevent catastrophic ground fault arcing.
- **Field Inspection & Megger Testing**: Dispatch field maintenance to perform handheld 1,000V DC insulation resistance (Megohmmeter) testing across homerun cables, module backsheets, and string combiner boxes on `INV-B02`.
- **Thermal & MPPT Audit for `INV-B01` & `INV-B03`**: Monitor IGBT junction temperatures on `INV-B01` and `INV-B03` during clipping hours to ensure inverter cooling loops maintain internal temps below 75°C.
- **Orchestration Log**: Transmit diagnostic telemetry to the Master Orchestrator for work order ticket generation in the enterprise Computerized Maintenance Management System (CMMS).

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "REMOTE_INVERTER_DC_STRING_ISOLATION",
  "site_id": "SF-BRAVO",
  "affected_units": ["INV-B02-STR01", "INV-B02-STR02", "INV-B02-STR03", "INV-B02-STR04"],
  "reason": "Critical DC ground fault insulation breakdown (Riso < 50 kOhm) posing immediate electrical fire hazard",
  "target_state": "DISENGAGED / OPEN_CIRCUIT",
  "requires_hitl_approval": true,
  "safety_standard": "IEEE 1547 / NEC 690.41",
  "confirmation_prompt": "Confirm execution of remote DC contactor trip for Inverter INV-B02 Strings 1-4 at Solar Farm Bravo."
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Compare the string-level current-voltage curves against clear-sky baseline expectations for Inverter Block 7."

**Agent Response:**
### Executive Summary
**A comparative diagnostic of Inverter Block 7 against clear-sky baseline expectations reveals localized anomalous behavior across two PV strings, while Strings 7A and 7B are operating within standard performance limits. Specifically, String 7C exhibits characteristic step-down curve deformation indicating bypass diode activation or localized module mismatch, whereas String 7D displays high series resistance ($R_s$) slope degradation resulting in an aggregate 28.6% power clipping loss. Corrective field dispatch and targeted string isolation are required to mitigate thermal stress and prevent permanent hot-spot cell degradation.**

---

### Quantitative Performance Breakdown

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Block 7 Total Active Power ($P_{mp}$)** | 28.4 kW | 34.8 kW | -18.39% | **Warning** |
| **String 7A Short-Circuit Current ($I_{sc}$)** | 9.78 A | 9.85 A | -0.71% | **Normal** |
| **String 7A Open-Circuit Voltage ($V_{oc}$)** | 948 V | 950 V | -0.21% | **Normal** |
| **String 7B Maximum Power ($P_{mp}$)** | 6.82 kW | 6.95 kW | -1.87% | **Normal** |
| **String 7C Knee-Point Voltage ($V_{mp}$)** | 610 V | 815 V | -25.15% | **Critical** |
| **String 7C Fill Factor ($FF$)** | 0.58 | 0.77 | -24.68% | **Critical** |
| **String 7D Series Resistance ($R_s$) Slope** | -0.0125 A/V | -0.0035 A/V | +257.14% | **Critical** |
| **String 7D Maximum Power ($P_{mp}$)** | 4.96 kW | 6.95 kW | -28.63% | **Critical** |
| **Block 7 Array Operating Temperature** | 48.2 °C | 44.0 °C (ambient norm) | +9.55% | **Warning** |

---

### Visualization Triggers

* **Recommended Visualization**: **Multi-Trace I-V & P-V Characteristic Curve Plot** overlaying measured string curves against irradiance-adjusted clear-sky baselines.
* **Telemetry Data JSON**:
```json
{
  "chart_type": "line",
  "title": "Inverter Block 7 - String I-V Curves vs Clear-Sky Baseline",
  "xAxis": {
    "title": "Voltage (V)",
    "data": [0, 100, 200, 300, 400, 500, 600, 700, 800, 850, 900, 920, 950]
  },
  "yAxis": {
    "title": "Current (A)"
  },
  "series": [
    {
      "name": "Clear-Sky Baseline (STC Expected)",
      "data": [9.85, 9.84, 9.82, 9.80, 9.77, 9.72, 9.60, 9.30, 8.50, 7.20, 4.00, 1.80, 0.00]
    },
    {
      "name": "String 7A (Normal)",
      "data": [9.78, 9.77, 9.75, 9.72, 9.68, 9.61, 9.48, 9.15, 8.35, 7.05, 3.85, 1.65, 0.00]
    },
    {
      "name": "String 7B (Normal)",
      "data": [9.80, 9.79, 9.76, 9.73, 9.70, 9.63, 9.50, 9.18, 8.38, 7.10, 3.90, 1.70, 0.00]
    },
    {
      "name": "String 7C (Diode Bypass / Partial Shading)",
      "data": [9.75, 9.74, 9.70, 9.65, 9.58, 9.40, 8.10, 6.20, 4.10, 2.00, 0.50, 0.00, 0.00]
    },
    {
      "name": "String 7D (High Series Resistance / Degradation)",
      "data": [9.70, 9.45, 9.10, 8.65, 8.10, 7.40, 6.50, 5.20, 3.40, 1.80, 0.40, 0.00, 0.00]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Perform Thermographic Aerial / Handheld Inspection**: Schedule an infrared (IR) scan on Strings 7C and 7D to verify if String 7C has shorted bypass diodes or severe localized soiling, and check String 7D for junction box/connector corrosion.
2. **Execute In-Situ DC Isolation & Megger Testing**: Conduct open-circuit voltage ($V_{oc}$) tests and insulation resistance measurements on String 7D to isolate high-resistance contact terminations.
3. **Firmware MPPT Tracking Verification**: Verify that Inverter Block 7's global maximum power point tracking (GMPPT) algorithm is periodically scanning to prevent sub-optimal local peak trapping caused by String 7C.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "DC_STRING_ISOLATION_AND_WORK_ORDER",
  "target_asset": "INV-BLK-07",
  "affected_circuits": ["STRING-7C", "STRING-7D"],
  "operation": "Lockout/Tagout (LOTO) & DC Disconnect for Field Diagnostic Inspection",
  "impact_assessment": "Temporary capacity derate of 11.78 kW on Inverter Block 7 during maintenance window.",
  "approval_required": "Field Operations Lead / Substation Asset Engineer"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Isolate Inverter String 14B remotely and dispatch a solar field technician with replacement bypass diodes."

**Agent Response:**
### Executive Summary
**A remote isolation command and field service dispatch request have been initiated for Inverter String 14B due to suspected bypass diode degradation. Under physical grid safety protocols and Tier 2 operational guardrails, autonomous modification of physical grid switching states and technician dispatch are restricted. A formal Human-In-The-Loop (HITL) authorization payload has been prepared for operator review and confirmation.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **String 14B DC Current Telemetry** | INSUFFICIENT DATA | 8.5 A | N/A | Warning |
| **String 14B Operating Voltage** | INSUFFICIENT DATA | 650.0 V | N/A | Warning |
| **Physical Isolation State** | Closed / Connected | Open / Isolated | N/A | Critical |
| **Technician Work Order Status** | Pending Approval | Dispatched | N/A | Warning |

*Note: Telemetry values reflect unverified runtime telemetry at the time of request. Historical baseline assumes standard operating conditions under peak irradiance.*

---

### Visualization Triggers
- **Recommended Visualization**: Multi-String I-V Curve and DC Current Time-Series Comparison.
- **Purpose**: Corroborate diode short-circuit / open-circuit conditions against adjacent strings prior to physical intervention.

```json
{
  "chart_type": "time_series_line",
  "title": "String 14B DC Current Telemetry vs Neighboring Strings",
  "series": [
    {"string_id": "String_14A", "status": "Normal"},
    {"string_id": "String_14B", "status": "Underperforming / Suspect"},
    {"string_id": "String_14C", "status": "Normal"}
  ]
}
```

---

### Actionable Recommendations
- **Telemetry Verification**: Validate inverter-level DC input alarms, string current divergence, and open-circuit voltage ($V_{oc}$) drops on String 14B before initiating isolation.
- **Safety Interlocking**: Confirm no downstream DC arc fault or ground fault interrupter (GFDI) trips are active that would present switching hazards.
- **Work Order Generation**: Stage Field Work Order specifying replacement bypass diodes, array junction box access permits, and Lockout/Tagout (LOTO) protocols.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PHYSICAL_GRID_CONTROL_AND_DISPATCH",
  "asset_id": "INV_STR_14B",
  "asset_type": "Solar_Inverter_String",
  "operations": [
    {
      "step": 1,
      "command": "REMOTE_STRING_ISOLATION",
      "target_component": "DC_DISCONNECT_STRING_14B",
      "target_state": "OPEN",
      "safety_interlock_verified": false
    },
    {
      "step": 2,
      "command": "DISPATCH_FIELD_TECHNICIAN",
      "crew_type": "Solar_Asset_Maintenance",
      "required_parts": ["Bypass Diode Module Type-A", "DC String Fuses (15A/1000V)"],
      "priority": "HIGH"
    }
  ],
  "requires_human_confirmation": true,
  "confirmation_prompt": "Confirm remote isolation of Inverter String 14B and immediate field crew dispatch for diode replacement."
}
```
