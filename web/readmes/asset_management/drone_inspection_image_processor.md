# ⚡ Drone Inspection Image Processor

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of drone inspection image processor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Drone Inspection Image Processor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank drone inspection image processor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.drone_inspection_image_processor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did yesterday's autonomous drone flight over Transmission Line 502 detect any chipped ceramic insulators or frayed shield wires?"

**Agent Response:**
### Executive Summary
**Yesterday's autonomous drone flight over Transmission Line 502 (TL-502) computer vision inference pipeline identified 3 chipped ceramic insulator discs and 1 section of frayed optical ground wire (OPGW) shield wire.** **The most severe anomaly involves a high-voltage ceramic bell insulator cluster at Tower 38 exhibiting severe mechanical spalling and surface flashover risk (Confidence: 94.2%), alongside structural strand severance detected on the shield wire at Span 24 (Confidence: 91.8%).** **Both findings degrade the Asset Health Index (AHI) for the affected spans below standard operational reliability thresholds, requiring immediate targeted maintenance intervention.**

---

### Quantitative Inspection Results

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Chipped Ceramic Insulators** | 3 defects | 0 defects | +300.0% | **Critical** |
| **Frayed Shield Wire (OPGW) Strands** | 1 span (Span 24) | 0 defects | +100.0% | **Warning** |
| **Average CV Inference Confidence** | 93.0% | > 85.0% | +9.4% | **Normal** |
| **Span 38 Insulator Health Index (AHI)** | 42.0 / 100 | 85.0 / 100 | -50.6% | **Critical** |
| **Span 24 Shield Wire Remaining Useful Life** | 1.8 months | 36.0 months | -95.0% | **Warning** |

---

### Defect Localization & Classification Detail

* **Structure ID: TL502-TWR-038 (Phase B - Suspension String)**
  * *Anomaly Type*: Chipped Ceramic Insulator (2 bells showing severe skirt fractures > 25mm).
  * *Severity*: Level 3 (High dielectric breakdown risk / mechanical degradation).
* **Structure ID: TL502-TWR-012 (Phase A - Dead-End Assembly)**
  * *Anomaly Type*: Minor Ceramic Shell Chipping (1 bell, superficial edge chip < 10mm).
  * *Severity*: Level 1 (Monitor during next routine cycle).
* **Span ID: TL502-SPAN-024 (Static / Shield Wire run between Towers 24 & 25)**
  * *Anomaly Type*: Outer aluminum strand fraying (2 broken outer strands near vibration damper clamp).
  * *Severity*: Level 2 (Tensile fatigue / aeolian vibration wear).

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "TL-502 Drone Image Processing Defect Tally by Span",
  "categories": [
    "Tower 12 (Span 12)",
    "Tower 24-25 (Span 24)",
    "Tower 38 (Span 38)",
    "Tower 45-46 (Span 45)"
  ],
  "series": [
    {
      "name": "Chipped Ceramic Insulators",
      "data": [1, 0, 2, 0]
    },
    {
      "name": "Frayed Shield Wires",
      "data": [0, 1, 0, 0]
    },
    {
      "name": "Baseline Anomaly Threshold",
      "data": [0, 0, 0, 0]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Schedule Hot-Stick / Outage Replacement for Tower 38**: Mobilize a transmission line crew to replace the defective Phase B ceramic insulator string before the next forecasted high-humidity/precipitation window to prevent line-to-ground flashover.
2. **Armor Rod / Shunt Installation at Span 24**: Deploy a line-repair crew to inspect the frayed shield wire at Tower 24 damper assembly and install preformed armor rods or splice sleeves to restore mechanical tensile strength.
3. **Trigger High-Resolution Thermal Telemetry**: Ingest FLIR radiometric thermal data from the drone run to verify if current leakage or localized hot spots have formed on the chipped bells at Tower 12 and Tower 38.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "TRANSMISSION_WORK_ORDER_DISPATCH",
  "asset_id": "TL-502",
  "location": {
    "grid_zone_id": "GZ-NORTH-500KV",
    "substations": ["Westlake Substation", "Midway 500kV Switching Yard"],
    "structures": ["TL502-TWR-038", "TL502-SPAN-024"]
  },
  "priority": "HIGH",
  "recommended_outage_window": "Next scheduled maintenance window (within 72 hours)",
  "work_scope": "Replace Phase B suspension ceramic insulator string on Tower 38; repair 2 frayed OPGW shield wire strands at Span 24 vibration damper.",
  "safety_clearance_required": true,
  "human_approval_required": "Transmission Operations Superintendent / Lead Asset Engineer"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate the thermal infrared hotspot severity on conductor splice joints along Tower Span 45 to 60."

**Agent Response:**
### Executive Summary
**High-resolution radiometric thermal infrared (TIR) imagery acquired via UAS payload across Tower Spans 45 to 60 identified critical thermal anomalies on mid-span compression splice joints on Spans 52–53 and 58–59. The maximum temperature gradient was detected on Splice SP-58-B ($\Delta T = +44.7^\circ\text{C}$ over reference conductor, peak temperature $104.2^\circ\text{C}$), indicating severe contact resistance degradation and impending structural annealing under current line loading. Immediate load shedding/dispatch curtailment and prioritized field repair are required to prevent mechanical splice separation and catastrophic conductor drop.**

---

### Quantitative Evaluation & Diagnostic Metrics

All thermographic data were normalized against baseline ambient conditions ($24.5^\circ\text{C}$, wind speed $1.8\text{ m/s}$) and compared against baseline conductor operating temperatures under IEEE 738 steady-state thermal rating methodology and NETA/EPRI infrared severity classification standards.

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Splice SP-45-A (Phase A, Span 45–46)** | $38.4^\circ\text{C}$ ($\Delta T: 6.4^\circ\text{C}$) | $32.0^\circ\text{C}$ | $+20.0\%$ | Normal |
| **Splice SP-48-B (Phase B, Span 48–49)** | $47.3^\circ\text{C}$ ($\Delta T: 14.8^\circ\text{C}$) | $32.5^\circ\text{C}$ | $+45.5\%$ | Warning |
| **Splice SP-52-C (Phase C, Span 52–53)** | $71.2^\circ\text{C}$ ($\Delta T: 38.2^\circ\text{C}$) | $33.0^\circ\text{C}$ | $+115.8\%$ | Warning (Elevated) |
| **Splice SP-55-A (Phase A, Span 55–56)** | $41.6^\circ\text{C}$ ($\Delta T: 9.1^\circ\text{C}$) | $32.5^\circ\text{C}$ | $+28.0\%$ | Normal |
| **Splice SP-58-B (Phase B, Span 58–59)** | $104.2^\circ\text{C}$ ($\Delta T: 44.7^\circ\text{C}$) | $33.1^\circ\text{C}$ | $+214.8\%$ | Critical |
| **Splice SP-59-C (Phase C, Span 59–60)** | $44.1^\circ\text{C}$ ($\Delta T: 11.5^\circ\text{C}$) | $32.6^\circ\text{C}$ | $+35.3\%$ | Warning |
| **Max Splice Joint Contact Resistance (SP-58-B)** | $48.2\text{ }\mu\Omega$ | $\le 15.0\text{ }\mu\Omega$ | $+221.3\%$ | Critical |
| **Span 45–60 Asset Health Index (AHI)** | $58.4\text{ / }100$ | $\ge 85.0\text{ / }100$ | $-31.3\%$ | Critical |
| **Calculated Splice RUL (SP-58-B)** | $< 72\text{ hours (at peak MVA)}$ | $> 87,600\text{ hours}$ | $-99.9\%$ | Critical |

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "data_json": {
    "title": "Conductor Splice Delta-T Distribution vs Critical Threshold (Tower Spans 45-60)",
    "labels": [
      "Span 45-46 (SP-45-A)",
      "Span 48-49 (SP-48-B)",
      "Span 52-53 (SP-52-C)",
      "Span 55-56 (SP-55-A)",
      "Span 58-59 (SP-58-B)",
      "Span 59-60 (SP-59-C)"
    ],
    "datasets": [
      {
        "label": "Measured Delta-T over Conductor Baseline (°C)",
        "data": [6.4, 14.8, 38.2, 9.1, 44.7, 11.5],
        "backgroundColor": [
          "#4CAF50",
          "#FFC107",
          "#FF9800",
          "#4CAF50",
          "#F44336",
          "#FFC107"
        ]
      },
      {
        "label": "EPRI Class 4 Critical Failure Threshold (°C)",
        "type": "line",
        "data": [40.0, 40.0, 40.0, 40.0, 40.0, 40.0],
        "borderColor": "#D32F2F",
        "borderDash": [5, 5],
        "fill": false
      }
    ]
  }
}
```

---

### Engineering Findings & Root-Cause Assessment
1. **Splice SP-58-B (Critical - EPRI Class 4 / NETA Critical):** Core temperature exceeds $100^\circ\text{C}$ with a temperature rise of $+44.7^\circ\text{C}$ relative to the adjacent ACSR conductor. High probability of strand oxidation, galvanic corrosion, or crimp relaxation causing micro-arcing and thermal runaway. Conductor aluminum strands are at immediate risk of tensile annealing.
2. **Splice SP-52-C (Warning/Elevated - EPRI Class 3):** Thermal rise of $+38.2^\circ\text{C}$ indicates high localized resistance; structural degradation is underway and will accelerate under peak thermal loading.
3. **Splice SP-48-B & SP-59-C (Warning - EPRI Class 2):** Marginal thermal delta ($\approx 11.5^\circ\text{C} - 14.8^\circ\text{C}$) indicative of early-stage joint degradation requiring scheduling during the next scheduled clearance window.

---

### Actionable Recommendations

- **Immediate Operations Action:** Execute dynamic line rating (DLR) curtailment on the circuit to limit conductor loading to $\le 60\%$ of nominal capacity until field remediation is completed.
- **Field Maintenance Dispatch:** Issue an expedited Priority 1 Work Order for hot-line clamp bypass / mechanical shunting or full compression splice replacement on Span 58–59 (Phase B) and Span 52–53 (Phase C).
- **Secondary Inspection:** Deploy follow-up optical zoom/corona imaging via drone to inspect strand fatigue, broken outer aluminum layers, and vibration damper integrity adjacent to Tower 58.
- **Asset Health Tracking:** Update enterprise transmission asset records with calculated Asset Health Index ($AHI = 58.4$) and tag Spans 45–60 for post-repair baseline thermography.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "tier_2_operation": "EMERGENCY_TRANSMISSION_DISPATCH_DERATING_AND_OUTAGE_CLEARANCE",
  "asset_group": "Transmission_Corridor_Span_45_60",
  "line_identifier": "TL-230KV-SP45-60",
  "critical_components": ["SPLICE-SP-58-B", "SPLICE-SP-52-C"],
  "requested_actions": [
    "Implement immediate 40% thermal capacity line derating with Grid Balancing Authority.",
    "Schedule emergency 8-hour line outage clearance window within 24 hours for splice replacement.",
    "Dispatch Bare-Hand / Hot-Line Transmission Line Crew with replacement two-sleeve full-tension splices."
  ],
  "safety_risk": "High - Conductor parted line drop hazard under structural annealing (>104°C).",
  "requires_human_signoff": true,
  "signoff_role": "Transmission Operations Director / Grid Reliability Coordinator"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate a high-priority work ticket for structural reinforcement on Tower #118 with embedded LiDAR coordinate tags."

**Agent Response:**
### Executive Summary
**High-resolution aerial photogrammetry and LiDAR point-cloud processing on Transmission Tower #118 have identified severe mechanical deformation and lattice buckling across the mid-to-upper mast cross-bracing.** **The Asset Health Index (AHI) for this structure has degraded to critical levels (34.2/100), exceeding allowable angular deflection thresholds by +316.3% under standard mechanical load baselines.** **Immediate field dispatch for structural reinforcement is required to mitigate catastrophic structural failure and line drop risk.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Health Index (AHI)** | 34.2 / 100 | 85.0 / 100 | -59.8% | **Critical** |
| **Max Lattice Deflection** | 145.7 mm | < 35.0 mm | +316.3% | **Critical** |
| **Angular Mast Tilt** | 3.42° | < 0.75° | +356.0% | **Critical** |
| **Member Section Loss (Corrosion/Fatigue)** | 18.5% | < 5.0% | +270.0% | **Warning** |
| **Remaining Useful Life (RUL)** | 0.8 Months | 240.0 Months | -99.7% | **Critical** |
| **LiDAR Point Cloud Density** | 1,420 pts/m² | > 800 pts/m² | +77.5% | **Normal** |

---

### Work Ticket Details: Structural Reinforcement

- **Work Order ID:** `WO-STRUC-2024-T118-001`
- **Asset ID:** `TOWER-118`
- **Asset Classification:** 500 kV Lattice Steel Suspension Tower
- **Priority Level:** **Priority 1 (Emergency / Expedited Response)**
- **Required Action:** Fabricate and bolt auxiliary structural sister-splices on primary leg member and replace buckled diagonal cross-braces.

#### Embedded LiDAR Coordinate Tags & Spatial Anomalies
```json
{
  "tower_id": "TOWER-118",
  "spatial_reference_system": "EPSG:4326 (WGS 84) / NAVD88",
  "survey_timestamp": "2024-10-24T14:22:15Z",
  "critical_defect_nodes": [
    {
      "node_id": "DEF-118-01",
      "component": "Upper Leg Joint C (Bent Web Member)",
      "latitude": 34.052235,
      "longitude": -118.243684,
      "elevation_msl_m": 312.45,
      "local_z_height_m": 22.0,
      "deflection_vector_xyz_mm": [42.1, -12.4, 145.7],
      "severity": "CRITICAL"
    },
    {
      "node_id": "DEF-118-02",
      "component": "Mid-Mast Lattice B (Sheared Fastener / Flange Gap)",
      "latitude": 34.052241,
      "longitude": -118.243679,
      "elevation_msl_m": 305.65,
      "local_z_height_m": 15.2,
      "deflection_vector_xyz_mm": [18.2, 5.1, 88.4],
      "severity": "CRITICAL"
    },
    {
      "node_id": "DEF-118-03",
      "component": "Cross-arm Joint A (Micro-cracking)",
      "latitude": 34.052228,
      "longitude": -118.243690,
      "elevation_msl_m": 300.95,
      "local_z_height_m": 10.5,
      "deflection_vector_xyz_mm": [8.5, 1.2, 42.1],
      "severity": "WARNING"
    }
  ]
}
```

---

### Visualization Trigger

**Recommended Chart:** Scatter / 3D Spatial Deflection Profile  
The UI visualizer renders structural deflection magnitude across tower elevation zones:

```json
{
  "chart_type": "scatter",
  "title": "Tower #118 LiDAR Structural Deflection Profile",
  "series": [
    {
      "name": "Deflection Amplitude (mm)",
      "data": [
        {"x": 10.5, "y": 42.1, "label": "Cross-arm Joint A"},
        {"x": 15.2, "y": 88.4, "label": "Mid-Mast Lattice B"},
        {"x": 22.0, "y": 145.7, "label": "Upper Leg Joint C (Critical)"},
        {"x": 28.4, "y": 35.2, "label": "Apex Mount D"}
      ]
    }
  ],
  "thresholds": {
    "warning_mm": 35.0,
    "critical_mm": 75.0
  }
}
```

---

### Actionable Recommendations

1. **Immediate De-rating & Clearance Control:** Notify Grid Operations to assess tension relief options and restrict live-line work around Tower #118 until structural stabilization is complete.
2. **Field Crew Staging:** Dispatch Transmission Structural Maintenance Crew equipped with heavy hydraulic clamping units and prefabricated steel angle brackets (L6x6x1/2 Grade 50).
3. **Continuous Photogrammetric Monitoring:** Schedule automated follow-up drone inspection flights at 24-hour intervals until reinforcement is verified.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "DISPATCH_EMERGENCY_FIELD_WORK_ORDER"
  work_order_id: "WO-STRUC-2024-T118-001"
  target_asset: "TOWER-118"
  grid_zone: "ZONE-TRANS-WEST-04"
  estimated_cost_usd: 28500.00
  crew_type: "TRANSMISSION_STRUCTURAL_HOT_CREW"
  clearance_permit_required: true
  hitl_approval_required: "Approve generation and automated dispatch of emergency structural reinforcement work ticket."
```
