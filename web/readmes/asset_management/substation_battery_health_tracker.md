# ⚡ Substation Battery Health Tracker

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of substation battery health tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Substation Battery Health Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank substation battery health tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.substation_battery_health_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are internal cell resistance and float voltages on the 125V DC control battery bank at Substation Echo within IEEE 450 specs?"

**Agent Response:**
### Executive Summary
**Telemetry and impedance diagnostic records for the 125V DC control battery bank (60-cell Vented Lead-Acid configuration) at Substation Echo confirm that overall bank float voltage and individual cell float voltages are operating well within IEEE 450 nominal limits.** **Internal cell ohmic resistance measurements show an average variance of +2.8% over commissioning baselines, with no individual cell exceeding the critical +20% / +50% degradation thresholds specified in IEEE 450 Section 5.3.** **The DC auxiliary system remains fully compliant with NERC PRC-005 reliability standards with an Asset Health Index (AHI) of 92.4/100.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Bank Float Voltage (Total)** | 133.80 V DC | 132.00 – 135.00 V DC (2.23 V/cell) | +1.36% | **Normal** |
| **Min. Cell Float Voltage** | 2.21 V DC | $\ge$ 2.14 V DC (IEEE 450 low limit) | +3.27% | **Normal** |
| **Max. Cell Float Voltage** | 2.24 V DC | $\le$ 2.28 V DC (IEEE 450 high limit) | -1.75% | **Normal** |
| **Avg. Internal Cell Resistance** | 185.0 $\mu\Omega$ | 180.0 $\mu\Omega$ (Factory Baseline) | +2.78% | **Normal** |
| **Max. Internal Resistance Delta** | +12.5% (Cell #42) | $< 20.0\%$ (Warning: $+20\%$, Action: $+50\%$) | N/A | **Normal** |
| **Intercell Connection Resistance** | 11.2 $\mu\Omega$ avg | $\le 15.0\ \mu\Omega$ ($<20\%$ above baseline) | +4.67% | **Normal** |
| **Electrolyte Temperature** | 23.8 °C (74.8 °F) | 25.0 °C (77.0 °F Nominal) | -4.80% | **Normal** |
| **Asset Health Index (AHI)** | 92.4 / 100 | $\ge 85.0$ | +8.71% | **Normal** |

---

### Visualization Configuration

A comparative cell-level baseline vs. measured distribution chart has been synthesized for telemetry visualization:

```json
{
  "chart_type": "bar",
  "title": "Substation Echo 125V DC Battery Bank - Float Voltage & Resistance Compliance (IEEE 450)",
  "labels": [
    "Bank Float Voltage (V)",
    "Min Cell Voltage (V)",
    "Max Cell Voltage (V)",
    "Avg Cell Resistance (µΩ/10)",
    "Max Cell Resistance Dev (%)"
  ],
  "datasets": [
    {
      "label": "Measured Telemetry",
      "data": [133.8, 2.21, 2.24, 18.5, 12.5],
      "backgroundColor": "rgba(54, 162, 235, 0.7)"
    },
    {
      "label": "IEEE 450 Standard / Nominal Limit",
      "data": [133.5, 2.14, 2.28, 18.0, 50.0],
      "backgroundColor": "rgba(255, 99, 132, 0.7)"
    }
  ]
}
```

---

### Actionable Recommendations

- **Quarterly Inspection Schedule**: Maintain standard quarterly visual inspection and thermal imaging scan of intercell connections in accordance with NERC PRC-005 Table 1-4b.
- **Trend Monitoring for Cell #42**: Although Cell #42 internal resistance increase (+12.5%) is within acceptable limits ($<20\%$), flag Cell #42 for automatic delta rate-of-change tracking to detect early signs of grid corrosion or sulfation.
- **Temperature Compensation Verification**: Ensure DC charger temperature compensation coefficient remains calibrated to -3.0 mV/°C/cell relative to the standard 25°C baseline.

### Example 2: Trend & Comparative Analysis
**User:** "Track the thermal runaway risk and electrolyte level degradation across lead-acid banks over the trailing 12 months."

**Agent Response:**
### Executive Summary
**Across the fleet of lead-acid substation battery banks over the trailing 12 months, thermal runaway risk peaked during high ambient summer months driven by elevated float currents and internal cell impedance buildup, while electrolyte levels exhibited a steady 26.0% degradation across unmaintained flooded cells. Fleet-wide Asset Health Index (AHI) currently averages 71.4%, with 8 banks in Warning status and 2 banks breaching Critical IEEE 450/1188 operational limits due to severe dry-out and float current instability. Immediate electrolyte replenishment, temperature-compensated charger calibration, and targeted impedance testing are required to mitigate catastrophic cell dry-out and thermal runaway.**

---

### Data Presentation: Fleet Telemetry & Degradation Summary (Trailing 12 Months)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Asset Health Index (AHI)** | 71.4 / 100 | $\ge 85.0$ / 100 | -16.0% | **Warning** |
| **Thermal Runaway Risk Index** | 19.5 / 100 *(Peak: 41.8)* | $\le 15.0$ / 100 | +30.0% | **Warning** |
| **Flooded Cell Electrolyte Level** | 71.4% of plate coverage | 100.0% (High-level line) | -28.6% | **Critical** |
| **Float Current Deviation** | +10.2 mA *(Peak: +31.0 mA)* | $\le +5.0$ mA baseline | +104.0% | **Warning** |
| **Max Pilot Cell Temperature** | 33.8 °C *(Peak: 42.1 °C)* | $\le 25.0$ °C nominal | +35.2% | **Warning** |
| **Internal Cell Resistance ($R_i$)** | 1.82 mΩ | $\le 1.25$ mΩ | +45.6% | **Critical** |
| **Float Voltage Variance ($\Delta V$)** | 0.082 V/cell | $\le 0.030$ V/cell | +173.3% | **Critical** |

#### High-Risk Substation Battery Bank Inventory
| Substation / Bank ID | Chemistry | Electrolyte Level | Max Temp (°C) | Float Current (mA) | AHI | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **SUB-042 (Bank 1)** | Flooded Lead-Acid (VLA) | 58.2% (Low Line Breached) | 39.4 °C | 82 mA | 54.1 | **Critical** |
| **SUB-118 (Bank 2)** | VRLA (AGM) | Dry-out Detected ($\Delta W$) | 42.1 °C | 115 mA | 48.3 | **Critical** |
| **SUB-087 (Bank 1)** | Flooded Lead-Acid (VLA) | 68.5% | 34.2 °C | 64 mA | 67.8 | **Warning** |
| **SUB-204 (Bank 2)** | VRLA (Gel) | Normal Seal Pressure | 31.5 °C | 45 mA | 72.0 | **Warning** |

---

### Visualization Configuration

A multi-series time-series tracking chart displaying monthly Thermal Runaway Risk Index, Average Electrolyte Level Degradation, and Float Current Deviation over the trailing 12-month window has been generated:

```json
{
  "title": "Lead-Acid Battery Health Telemetry (Trailing 12 Months)",
  "chart_type": "line",
  "labels": ["M-12", "M-11", "M-10", "M-09", "M-08", "M-07", "M-06", "M-05", "M-04", "M-03", "M-02", "M-01"],
  "datasets": [
    {
      "label": "Thermal Runaway Risk Index (0-100)",
      "data": [14.2, 15.0, 16.8, 18.2, 22.5, 34.1, 41.8, 38.6, 29.4, 24.1, 21.0, 19.5],
      "borderColor": "#e63946"
    },
    {
      "label": "Average Electrolyte Level (%)",
      "data": [96.5, 95.8, 94.2, 92.0, 89.4, 85.1, 81.3, 78.5, 76.2, 74.8, 73.1, 71.4],
      "borderColor": "#457b9d"
    },
    {
      "label": "Float Current Deviation (mA above baseline)",
      "data": [5.0, 6.2, 7.8, 9.1, 14.5, 26.3, 31.0, 28.2, 19.0, 14.3, 11.8, 10.2],
      "borderColor": "#f4a261"
    }
  ]
}
```

---

### Actionable Recommendations

1. **Immediate Field Service (IEEE 450 Dispatch)**:
   - Dispatch substation field crews to **SUB-042** and **SUB-087** for deionized water replenishment on flooded lead-acid cells below the minimum electrolyte plate coverage threshold.
   - Perform specific gravity measurements across all pilot cells to identify stratification and sulfation.
2. **Thermal Runaway Containment on VRLA Banks (IEEE 1188 / NERC PRC-005)**:
   - Perform urgent ohmic testing (internal resistance and inter-cell connection resistance) on **SUB-118 Bank 2** showing severe dry-out and thermal runaway precursor signatures (float current >100 mA).
   - Verify battery enclosure HVAC operation and ensure pilot cell temperature sensors are functioning within calibration limits.
3. **Charger Voltage Compensation Calibration**:
   - Recalibrate temperature-compensated float voltage settings across all DC systems exhibiting $>0.030\text{ V/cell}$ variance to prevent overcharging during warmer operating cycles.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_BATTERY_MAINTENANCE_AND_CHARGER_TRIM",
  "asset_ids": ["SUB-042-B1", "SUB-118-B2"],
  "target_substations": ["SUB-042", "SUB-118"],
  "standard_mandate": "NERC_PRC_005_BPS_DC_SUPPLY",
  "proposed_actions": [
    {
      "asset_id": "SUB-118-B2",
      "operation": "SET_FLOAT_VOLTAGE_REDUCTION",
      "parameters": {"trim_voltage_v": -1.5, "enable_temp_compensation": true}
    },
    {
      "asset_id": "SUB-042-B1",
      "operation": "DISPATCH_EMERGENCY_ELECTROLYTE_REFILL_WORK_ORDER",
      "priority": "HIGH_P1"
    }
  ],
  "hitl_approval_required": true,
  "critic_agent_status": "VALIDATED"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Schedule urgent cell replacement for Jar #8 in Bank 2 and trigger an automated battery discharge load test."

**Agent Response:**
### 1. Executive Summary
**A critical cell replacement request for Jar #8 (Bank 2) and an automated battery discharge load test have been staged for authorization. In accordance with utility safety mandates and NERC PRC-005 / IEEE 450/1188 compliance guidelines, physical load testing and physical asset dispatch cannot be triggered autonomously. These operations are classified as Tier 2 physical grid actions and require explicit Human-In-The-Loop (HITL) confirmation before work order issuance and test initiation.**

---

### 2. Data Presentation

Telemetry and condition assessment indicators for Bank 2, Jar #8:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Internal Cell Resistance / Impedance** | 1.85 mΩ | 1.10 mΩ | +68.18% | **Critical** |
| **Float Voltage (Jar #8)** | 2.12 Vpc | 2.25 Vpc | -5.78% | **Critical** |
| **Intercell Connection Resistance** | 18.2 µΩ | ≤ 15.0 µΩ | +21.33% | **Warning** |
| **Electrolyte / Post Temp** | 31.5 °C | 25.0 °C (Nominal) | +26.00% | **Warning** |
| **Asset Health Index (AHI)** | 34.0 / 100 | ≥ 85.0 / 100 | -60.00% | **Critical** |
| **Remaining Useful Life (RUL)** | 1.2 Months | 60.0 Months | -98.00% | **Critical** |

---

### 3. Visualization Triggers

**Recommended Visualization:** Multicell Float Voltage & Impedance Profile (Bar & Line Chart) across Bank 2 showing individual cell deviations relative to IEEE lower tolerance limits.

```json
{
  "chart_type": "bar_line_composite",
  "title": "Bank 2 Individual Cell Voltage & Internal Resistance Profile",
  "labels": ["Jar #1", "Jar #2", "Jar #3", "Jar #4", "Jar #5", "Jar #6", "Jar #7", "Jar #8 (Target)", "Jar #9", "Jar #10", "Jar #11", "Jar #12"],
  "datasets": [
    {
      "name": "Cell Float Voltage (Vpc)",
      "type": "line",
      "data": [2.26, 2.25, 2.24, 2.25, 2.26, 2.23, 2.24, 2.12, 2.25, 2.24, 2.26, 2.25],
      "threshold_low": 2.20,
      "unit": "Vpc"
    },
    {
      "name": "Internal Impedance (mΩ)",
      "type": "bar",
      "data": [1.12, 1.09, 1.11, 1.15, 1.10, 1.13, 1.12, 1.85, 1.11, 1.10, 1.14, 1.12],
      "threshold_high": 1.43,
      "unit": "mΩ"
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Human Operator Review**: Review the staged Tier 2 operational payload below to authorize the physical replacement work order and approve scheduling of the discharge capacity test.
- **Pre-Test Protocol**: Ensure Bank 1 (redundant DC string) is fully operational and supporting the DC bus prior to isolating Bank 2 for the discharge test.
- **Safety Precaution**: Execute the automated discharge test during off-peak operational hours with on-site technician supervision to monitor thermal runaway risk on degraded Jar #8.
- **Compliance Logging**: Ensure all pre-test and post-replacement ohmic measurements are logged in the enterprise asset register to maintain NERC PRC-005 audit trails.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PHYSICAL_GRID_AND_MAINTENANCE_OPERATION",
  "status": "AWAITING_OPERATOR_APPROVAL",
  "operations": [
    {
      "id": "WO-BATT-REPLACE-JAR8-B2",
      "action": "EMERGENCY_CELL_REPLACEMENT",
      "target_asset": "Station Battery Bank 2, Jar #8",
      "parameters": {
        "priority": "URGENT",
        "replacement_part": "Compatible IEEE 450/1188 Certified Cell",
        "required_crew": "Substation Electrical Maintenance (P&C / Battery Specialist)"
      }
    },
    {
      "id": "CMD-BATT-LOADTEST-B2",
      "action": "TRIGGER_AUTOMATED_DISCHARGE_TEST",
      "target_asset": "Station Battery Bank 2",
      "parameters": {
        "test_type": "Modified Performance / Capacity Discharge Test",
        "rate_duration": "3-Hour / 8-Hour Standard Profile",
        "interlock_check": "Redundant DC Bank 1 Online & Nominal (Verified)"
      }
    }
  ],
  "operator_prompt": "Please confirm authorization to dispatch Emergency Work Order WO-BATT-REPLACE-JAR8-B2 and initiate automated battery discharge sequence CMD-BATT-LOADTEST-B2."
}
```
