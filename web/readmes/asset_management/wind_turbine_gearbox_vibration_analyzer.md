# ⚡ Wind Turbine Gearbox Vibration Analyzer

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of wind turbine gearbox vibration analyzer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Wind Turbine Gearbox Vibration Analyzer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank wind turbine gearbox vibration analyzer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.wind_turbine_gearbox_vibration_analyzer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are planetary gear bearing acceleration spectra on Wind Turbine WTG-09 exhibiting high-frequency crest factor anomalies?"

**Agent Response:**
### Executive Summary
**Telemetry and acceleration spectral analysis for Wind Turbine WTG-09 confirm severe high-frequency Crest Factor anomalies in the planetary gear stage bearing assembly.** **The high-frequency (2 kHz – 10 kHz) Crest Factor has spiked to 7.20 (nominal baseline: 3.20 to 3.50), driven by repetitive, transient high-amplitude shock pulses indicative of localized bearing raceway micro-spalling and sub-surface fatigue.** **Immediate operational de-rating and an endoscopic borescope inspection are recommended to prevent catastrophic gearbox stage failure.**

---

### Quantitative Vibration Spectrum & Telemetry Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **High-Frequency Crest Factor (CF)** | **7.20** | **3.40** | **+111.76%** | **Critical** |
| **Planetary Bearing Peak Acceleration ($g_{pk}$)** | **14.22 g** | **4.10 g** | **+246.83%** | **Critical** |
| **Planetary Bearing RMS Acceleration ($g_{rms}$)** | **1.98 g** | **1.21 g** | **+63.64%** | **Warning** |
| **High-Frequency Envelope Energy (HFE, 2–10 kHz)** | **8.64 gE** | **2.10 gE** | **+311.43%** | **Critical** |
| **Planetary Bearing Outer Race Defect Freq (BPFO)** | **114.6 Hz (7.8× harmonic energy)** | **< 1.0× baseline noise** | **+680.00%** | **Critical** |
| **Gearbox Sump Oil Temperature** | **78.4 °C** | **68.0 °C** | **+15.29%** | **Warning** |
| **ISO 20816-21 / VDI 3834 Velocity RMS** | **4.85 mm/s** | **2.80 mm/s** | **+73.21%** | **Warning** |

---

### Spectral Diagnostics & Fault Mechanism

1. **High Crest Factor Divergence**: The sharp divergence between Peak Acceleration ($14.22\text{ g}$) and RMS Acceleration ($1.98\text{ g}$) indicates discrete, high-energy, short-duration impact events rather than generalized gear mesh distributed wear.
2. **Demodulation & Envelope Spectrum**: High-frequency bandpass filtering (2 kHz to 10 kHz) demonstrates distinct amplitude-modulated spectral peaks centered at the Ball Pass Frequency Outer Race (BPFO) harmonics ($114.6\text{ Hz}$, $229.2\text{ Hz}$, $343.8\text{ Hz}$), sideband-modulated by planet carrier rotational frequency ($0.38\text{ Hz}$).
3. **Failure Mode**: Stage 2/Stage 3 bearing subsurface shear fatigue and raceway spalling on the planetary wheel/carrier bearings.

---

### Visualization Trigger

```json
{
  "chart_type": "line",
  "title": "WTG-09 Planetary Bearing Crest Factor & High-Frequency Peak Acceleration Trend",
  "data": {
    "labels": ["T-12h", "T-10h", "T-8h", "T-6h", "T-4h", "T-2h", "Current"],
    "datasets": [
      {
        "name": "High-Frequency Crest Factor",
        "data": [3.4, 3.6, 4.1, 4.8, 5.7, 6.4, 7.2],
        "unit": "ratio"
      },
      {
        "name": "Critical Alarm Threshold",
        "data": [6.0, 6.0, 6.0, 6.0, 6.0, 6.0, 6.0],
        "unit": "ratio"
      },
      {
        "name": "Warning Threshold",
        "data": [4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5],
        "unit": "ratio"
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **Immediate Power Curtailment**: Curtail WTG-09 rated active power output by 40% (curtailment to nominal torque limit $\le 60\%$) to reduce mechanical contact stresses across the planetary stage and mitigate rapid crack propagation.
- **Oil Debris & Particle Counter Verification**: Pull an inline optical particle counter (ISO 4406) log and collect an offline oil sample for Spectrometric Metals Analysis (PQ Index, Fe/Cr/Cu content).
- **Video Borescope Inspection**: Deploy field maintenance crew to perform internal video-endoscopic inspection of the planetary gear stage bearings, planet pins, and planet gear teeth within 48 operating hours.
- **Continuous Fast-Fourier Transform (FFT) Tracking**: Configure SCADA / CMS condition monitoring to high-resolution trigger mode (16 kHz raw acceleration capture every 15 minutes).

---

### [TIER 2 ACTION REQUIRED]

```yaml
operation_type: "TURBINE_OPERATIONAL_CURTAILMENT"
asset_id: "WTG-09"
substation_feeder: "FDR-WND-04"
target_action: "De-rate WTG-09 active power setpoint to 60% rated capacity and lock yaw/pitch control to prevent torque transients"
safety_criticality: "HIGH"
justification: "Planetary bearing high-frequency crest factor exceeded critical threshold (7.20 vs 6.00 limit); risk of catastrophic gearbox seizure and secondary generator/main shaft damage."
human_approval_required: true
```

### Example 2: Trend & Comparative Analysis
**User:** "Track the lubrication particle count and vibration velocity trends over the last 90 days of high wind operation."

**Agent Response:**
### Executive Summary
**Analysis of the 90-day high-wind operating period reveals a critical co-trending escalation in gearbox vibration velocity (RMS reaching 7.8 mm/s, a +151.6% increase over baseline) and high-speed stage lubrication particle concentration (ISO 4406 cleanliness rating degraded to 22/19/16). The strong statistical correlation between high-frequency mechanical vibration and ferrous particulate generation indicates accelerating intermediate-to-high-speed shaft bearing fatigue/micro-pitting under sustained aerodynamic loading. Immediate maintenance intervention is required to avoid catastrophic planetary/helical gear mesh failure and uncontained mechanical seizure.**

---

### Quantitative Analysis (90-Day High Wind Regimes: Wind Speed $\ge$ 12 m/s)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Vibration Velocity RMS (High-Speed Shaft / Bearings)** | 7.80 mm/s | 3.10 mm/s (Target < 4.50 mm/s) | +151.6% | **Critical** |
| **Peak Vibration Acceleration ($a_{peak}$)** | 4.85 g | 1.80 g (Target < 2.50 g) | +169.4% | **Critical** |
| **Lubrication Particle Count ($>4\,\mu\text{m}$ / mL)** | 4,650 particles/mL | 850 particles/mL (Target < 1,000) | +447.1% | **Critical** |
| **Ferrous Debris Index (FDI)** | 148 ppm | 22 ppm (Target < 35 ppm) | +322.9% | **Critical** |
| **Gearbox Sump / Bearing Temperature** | 81.4 °C | 62.0 °C (Target < 75.0 °C) | +31.3% | **Warning** |
| **ISO 4406 Cleanliness Code** | 22/19/16 | 17/15/12 | +5 ISO Steps | **Critical** |
| **Demodulation / PeakVue Energy (HSS Outer Race)**| 6.2 g-s | 1.1 g-s (Target < 2.0 g-s) | +463.6% | **Critical** |

---

### Visualization: 90-Day Trend Analysis

```json
{
  "chart_type": "line",
  "title": "Gearbox Vibration Velocity vs. Lubricant Particle Count (90-Day High Wind Trend)",
  "xAxis": {
    "name": "Operating Timeline (90 Days)",
    "categories": ["Day 90 (T-90)", "Day 75", "Day 60", "Day 45", "Day 30", "Day 15", "Day 1 (Current)"]
  },
  "yAxis": [
    {
      "name": "Vibration Velocity RMS (mm/s)",
      "min": 0,
      "max": 10
    },
    {
      "name": "Lube Particle Count (>4µm/mL)",
      "opposite": true,
      "min": 0,
      "max": 5000
    }
  ],
  "series": [
    {
      "name": "Vibration Velocity RMS (mm/s)",
      "data": [3.1, 3.3, 3.6, 4.2, 5.1, 6.4, 7.8],
      "yAxis": 0,
      "color": "#e74c3c"
    },
    {
      "name": "Lube Particle Count (>4µm/mL)",
      "data": [850, 920, 1150, 1680, 2450, 3400, 4650],
      "yAxis": 1,
      "color": "#f39c12"
    },
    {
      "name": "ISO 10816-21 Warning Threshold (4.5 mm/s)",
      "data": [4.5, 4.5, 4.5, 4.5, 4.5, 4.5, 4.5],
      "yAxis": 0,
      "dashStyle": "Dash",
      "color": "#7f8c8d"
    }
  ]
}
```

---

### Root Cause & Predictive Diagnosis
1. **Mechanical Signature**: High vibration velocity (7.8 mm/s) accompanied by high-frequency spectral sidebands at the Intermediate-Speed Shaft (ISS) and High-Speed Shaft (HSS) gear mesh frequencies ($f_{GMF}$) indicates advancing contact fatigue (spalling/macropitting).
2. **Tribological Synergy**: Sharp inflection at Day 45 in ferrous debris index ($>4\,\mu\text{m}$ counts $>4,600/\text{mL}$) confirms that particulate contamination is actively abrading raceways, accelerating kinematic degradation during high torque wind shear events.
3. **Thermal Feedback**: Secondary bearing temperature increase (+19.4 °C above baseline) confirms elevated friction and reduced hydrodynamic film thickness.

---

### Actionable Recommendations

- **Engineering Inspection**: Perform an immediate video borescope inspection of the High-Speed Shaft (HSS) bearings, intermediate pinions, and planet carrier bearings.
- **Filtration & Fluid Service**: Replace offline and inline lubrication filter cartridges ($3\,\mu\text{m}$ / $\beta \ge 200$) and run magnetic plug chip catch analysis for material composition (spectrometric oil analysis - SOAP).
- **Operational De-rating**: Implement temporary active power and torque de-rating (curtailment to 70% rated capacity) during high-wind gusts ($\ge 12\,\text{m/s}$) to minimize dynamic tooth impact loading until mechanical inspection is completed.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action: "EXECUTE_TURBINE_POWER_CURTAILMENT_AND_MAINTENANCE_LOCKOUT"
  target_asset: "WIND_TURBINE_ASSET_101_GEARBOX"
  operational_parameters:
    maximum_torque_limit: "70%"
    vibration_trip_threshold: "8.5 mm/s RMS"
    emergency_lockout_if_temp_exceeds: "85.0 °C"
  justification: "Critical vibration velocity (7.8 mm/s) and extreme particulate debris (4,650/mL) indicate imminent catastrophic bearing/gear mesh failure during high wind operations."
  approval_workflow: "Human-In-The-Loop (HITL) Operations Control Center Sign-Off Required"
  safety_protocol_reference: "ISO 10816-21 / AGMA 6006-A03 / Grid Asset Management Standard Ops"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Curtail Turbine WTG-09 maximum generator output to 50% and schedule an immediate borescope gearbox inspection."

**Agent Response:**
### Executive Summary
**Vibration analysis for Turbine WTG-09 indicates elevated high-frequency acceleration and crest factor anomalies across the high-speed shaft (HSS) and planetary stage bearings, signifying early mechanical degradation. Derating the turbine output by 50% mitigates immediate mechanical fatigue and dynamic loading while preventing catastrophic gear tooth/bearing spalling. In accordance with utility safety guardrails, physical generation curtailment and field maintenance dispatch represent Tier 2 operational actions and require Human-In-The-Loop (HITL) authorization prior to execution.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Gearbox HSS Bearing Vibration (RMS)** | 7.82 mm/s | 2.50 mm/s | +212.8% | **Critical** |
| **Planetary Stage Acceleration (Peak-to-Peak)** | 14.20 g | 4.80 g | +195.8% | **Critical** |
| **High-Speed Pinion Crest Factor** | 6.40 | 3.20 | +100.0% | **Warning** |
| **Gearbox Sump Oil Temperature** | 78.5 °C | 62.0 °C | +26.6% | **Warning** |
| **Active Power Output** | 2.40 MW (100%) | 2.40 MW | 0.0% | **Warning** |

---

### Visualization Triggers

**Recommended Visualization:** Time-Series Line Chart illustrating vibration velocity (RMS) and acceleration spectrum trends against ISO 10816-21 severity thresholds for WTG-09.

```json
{
  "chart_type": "line",
  "title": "WTG-09 Gearbox HSS Bearing Vibration & Temperature Trend",
  "data": {
    "timestamps": ["T-24h", "T-18h", "T-12h", "T-6h", "T-1h", "Current"],
    "hss_vibration_rms_mms": [2.6, 3.1, 4.4, 5.8, 7.1, 7.82],
    "iso_warning_threshold_mms": [4.5, 4.5, 4.5, 4.5, 4.5, 4.5],
    "iso_alarm_threshold_mms": [7.0, 7.0, 7.0, 7.0, 7.0, 7.0],
    "gearbox_oil_temp_c": [63.2, 64.8, 68.1, 72.4, 76.0, 78.5]
  }
}
```

---

### Actionable Recommendations
- **Execute Active Power Curtailment**: Limit maximum active generator setpoint to 50% (1.20 MW) to relieve dynamic tooth contact stress and thermal buildup on the high-speed pinion.
- **Dispatch Borescope Inspection**: Deploy a certified field technician team to perform an internal optical borescope inspection of the high-speed shaft bearing raceways and planetary gear mesh.
- **Lubrication Debris Analysis**: Collect an inline oil sample and inspect the magnetic chip detectors and secondary 10-micron oil filter for metallic particulate accumulation.
- **Continuous Spectrum Monitoring**: Increase vibration telemetry acquisition frequency to 1-minute intervals to detect any rapid acceleration runaway under curtailed conditions.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "ASSET_CONTROL_AND_WORK_ORDER",
  "asset_id": "WTG-09",
  "grid_zone_id": "GZ-NORTH-WIND-01",
  "curtailment_parameters": {
    "command": "SET_MAX_ACTIVE_POWER",
    "target_output_pct": 50,
    "target_output_mw": 1.20,
    "ramp_rate_mw_per_min": 0.20
  },
  "work_order_request": {
    "work_type": "EMERGENCY_INSPECTION",
    "procedure": "INTERNAL_BORESCOPE_GEARBOX_INSPECTION",
    "priority": "HIGH_P1",
    "target_subcomponents": ["HSS_BEARING", "INTERMEDIATE_STAGE", "PLANETARY_STAGE"]
  },
  "safety_confirmation_required": true,
  "requires_hitl_approval": true,
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```
