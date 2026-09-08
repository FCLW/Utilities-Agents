# ⚡ Transmission Tower Corrosion Analyzer

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of transmission tower corrosion analyzer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Transmission Tower Corrosion Analyzer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank transmission tower corrosion analyzer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.transmission_tower_corrosion_analyzer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which lattice steel towers along Coastal Line 230-1 show severe galvanic zinc loss or pack rust on structural footings?"

**Agent Response:**
### Executive Summary
**Condition assessment for Coastal Line 230-1 reveals severe galvanic zinc coating degradation (>80% loss) and critical pack rust ("rust jacking") on structural footing members across 6 lattice steel structures (Towers 230-1-042, 058, 077, 089, 104, and 112). Marine atmospheric exposure and soil-grade moisture accumulation have accelerated base metal oxidation, compromising structural load capacities and driving Asset Health Index (AHI) scores into Critical status. Immediate structural remediation and metallurgical mitigation are required to avoid mechanical footing displacement under maximum wind-loading scenarios.**

---

### Data Presentation

#### 1. Aggregate Corrosion Telemetry & Metrics (Coastal Line 230-1)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Mean Galvanic Zinc Loss (Critical Sub-segment)** | 88.0% | < 20.0% | +340.0% | **Critical** |
| **Structural Pack Rust Severity (Max Index 1–5)** | 4.8 / 5.0 | < 1.5 / 5.0 | +220.0% | **Critical** |
| **Average Base Metal Section Loss (Leg Members)** | 2.8 mm (18.6%) | 0.0 mm | +100.0% | **Critical** |
| **Mean Asset Health Index (AHI)** | 31.4 / 100 | > 80.0 / 100 | -60.8% | **Critical** |
| **Remaining Useful Life (RUL - Unmitigated)** | 2.1 Years | 35.0 Years | -94.0% | **Critical** |

---

#### 2. Specific Tower Identification & Footing Condition Breakdown

| Tower ID | Structure Type | Micro-Environment Zone | Zinc Loss (%) | Pack Rust Severity | Section Loss (%) | AHI Score | Condition Classification |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Tower 230-1-089** | 230kV Lattice Suspension | Salt Spray / Marsh Border | 95% | Critical (Level 5) | 22.4% | 24.1 | **Critical** |
| **Tower 230-1-058** | 230kV Lattice Strain/Deadend | Intertidal Buffer (<500m) | 92% | Critical (Level 5) | 19.8% | 26.5 | **Critical** |
| **Tower 230-1-112** | 230kV Lattice Suspension | Marine Atmospheric | 91% | Severe (Level 5) | 18.2% | 29.0 | **Critical** |
| **Tower 230-1-042** | 230kV Lattice Suspension | Marine Atmospheric | 88% | Severe (Level 4.5) | 17.5% | 32.8 | **Critical** |
| **Tower 230-1-104** | 230kV Lattice Tension Angle | Wetland Basin | 84% | Severe (Level 4.2) | 15.1% | 36.2 | **Critical** |
| **Tower 230-1-077** | 230kV Lattice Suspension | Coastal Bluffs | 78% | Moderate/Severe (3.8) | 12.0% | 40.0 | **Warning** |

---

### Visualization Triggers

**Recommended Visualization:** Grouped Multi-Metric Bar Chart comparing Galvanic Zinc Depletion vs. Structural Footing Pack Rust Index across all impacted lattice structures on Coastal Line 230-1.

```json
{
  "chart_type": "bar",
  "title": "Coastal Line 230-1 Lattice Tower Corrosion Severity Assessment",
  "xAxis": [
    "Tower 230-1-042",
    "Tower 230-1-058",
    "Tower 230-1-077",
    "Tower 230-1-089",
    "Tower 230-1-104",
    "Tower 230-1-112"
  ],
  "series": [
    {
      "name": "Galvanic Zinc Loss (%)",
      "data": [88, 92, 78, 95, 84, 91]
    },
    {
      "name": "Structural Footing Pack Rust (Scale 1-5)",
      "data": [4.5, 4.8, 3.8, 5.0, 4.2, 4.9]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Immediate Non-Destructive Ultrasonic Thickness (UT) Testing**: Dispatch structural inspection crews to measure residual steel web and flange thickness at connection gusset plates on Towers `230-1-089` and `230-1-058`.
2. **Pack Rust Remediation & Joint Encapsulation**: Execute pneumatic descaling, rust-jacking separation, and installation of moisture-excluding structural elastomeric mastics / polyurethane barrier coatings on stub angles.
3. **Cathodic Protection (CP) & Galvanizing Renewal**: Install sacrificial zinc anode ground beds at concrete collar interfaces and apply high-build cold-galvanizing compound (or thermal spray zinc metallizing) to degraded lower lacing members.
4. **Structural Member Reinforcement / Sistering**: Issue engineering work packages to sister or replace heavily corroded diagonal footing angle braces exceeding 15% section loss.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_CAPITAL_MAINTENANCE_DISPATCH",
  "asset_group": "Coastal Line 230-1",
  "affected_structures": ["Tower 230-1-089", "Tower 230-1-058", "Tower 230-1-112"],
  "action_description": "Authorize high-priority structural engineering crew mobilization for footing reinforcement, bolt-pack replacement, and temporary dead-end guying under clearance conditions.",
  "risk_impact": "Loss of structural integrity under NERC heavy wind-loading threshold if left unmitigated prior to Q3 storm season.",
  "hitl_approval_required": true
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Correlate atmospheric salt spray deposition and ultrasonic steel thickness measurements from the latest inspection cycle."

**Agent Response:**
### Executive Summary
**Analysis of the latest inspection cycle indicates a strong positive correlation ($R^2 = 0.942$) between atmospheric salt spray deposition rates and ultrasonic steel thickness loss across coastal and near-coastal transmission corridors.** **Transmission structures located within 5 km of the coastline experience chloride deposition rates exceeding $250\ \text{mg/m}^2/\text{day}$, accelerating cross-sectional member thinning to an average of $0.098\ \text{mm/year}$ and driving critical Asset Health Index (AHI) degradation.** **Structures along the 500 kV Coastal Corridor require prioritized cathodic protection recoating and structural member reinforcement to prevent accelerated loss of mechanical load-bearing margin.**

---

### Data Presentation

#### Key Corrosion & Telemetry Metrics (Latest Inspection Cycle Aggregation)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Mean Atmospheric Salt Deposition (Coastal Zone 1)** | $262.4\ \text{mg/m}^2/\text{day}$ | $< 60.0\ \text{mg/m}^2/\text{day}$ | $+337.3\%$ | **Critical** |
| **Mean Atmospheric Salt Deposition (Inland Zone 2/3)** | $78.2\ \text{mg/m}^2/\text{day}$ | $< 60.0\ \text{mg/m}^2/\text{day}$ | $+30.3\%$ | **Normal** |
| **Ultrasonic Steel Thickness (Zone 1 Critical Nodes)** | $7.55\ \text{mm}$ | $10.00\ \text{mm}$ (Nominal) | $-24.5\%$ | **Critical** |
| **Corrosion Penetration Rate (Zone 1 Average)** | $0.098\ \text{mm/yr}$ | $< 0.025\ \text{mm/yr}$ | $+292.0\%$ | **Critical** |
| **Average Asset Health Index (AHI - Zone 1)** | $57.5\ / 100$ | $\ge 85.0\ / 100$ | $-32.4\%$ | **Warning** |
| **Mean Remaining Useful Life (RUL - Zone 1)** | $8.2\ \text{years}$ | $\ge 25.0\ \text{years}$ | $-67.2\%$ | **Warning** |
| **Correlation Coefficient ($r$) [Salt vs. Thickness Loss]** | $0.971$ | $0.000$ (No correlation) | $+97.1\%$ | **Critical** |

---

### Asset-Level Correlation Breakdown

| Tower ID | Grid Zone ID | Distance to Coast (km) | Salt Spray Deposition ($\text{mg/m}^2/\text{day}$) | Nominal Thickness ($\text{mm}$) | Ultrasonic Measured ($\text{mm}$) | Thickness Loss ($\text{mm}$) | AHI Score | RUL ($\text{yrs}$) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TWR-500-012** | Zone-1A | $0.8$ | $310.5$ | $10.00$ | $7.55$ | $2.45$ ($-24.5\%$) | $48.2$ | $5.4$ |
| **TWR-500-015** | Zone-1A | $1.4$ | $285.0$ | $10.00$ | $7.80$ | $2.20$ ($-22.0\%$) | $52.1$ | $6.8$ |
| **TWR-500-018** | Zone-1A | $2.1$ | $260.4$ | $10.00$ | $8.05$ | $1.95$ ($-19.5\%$) | $58.7$ | $8.1$ |
| **TWR-500-022** | Zone-1B | $3.5$ | $240.2$ | $10.00$ | $8.20$ | $1.80$ ($-18.0\%$) | $62.4$ | $9.5$ |
| **TWR-500-025** | Zone-1B | $4.8$ | $215.8$ | $10.00$ | $8.35$ | $1.65$ ($-16.5\%$) | $66.0$ | $11.0$ |
| **TWR-230-044** | Zone-2A | $9.2$ | $145.2$ | $9.50$ | $8.40$ | $1.10$ ($-11.6\%$) | $74.3$ | $16.2$ |
| **TWR-230-058** | Zone-2A | $14.6$ | $110.0$ | $9.50$ | $8.65$ | $0.85$ ($-8.9\%$) | $81.0$ | $21.5$ |
| **TWR-115-101** | Zone-3 | $32.0$ | $42.1$ | $8.00$ | $7.70$ | $0.30$ ($-3.8\%$) | $93.2$ | $38.0$ |

---

### Visualization Triggers

A **Bivariate Scatter & Linear Regression Plot** has been generated via `VisualizerTool` to model atmospheric salinity stress against metal cross-section loss:

```json
{
  "chart_type": "scatter",
  "title": "Correlation: Atmospheric Salt Spray Deposition vs. Ultrasonic Steel Thickness Loss",
  "regression_model": "y = 0.0076x + 0.038 (R² = 0.942)",
  "x_axis": "Salt Spray Deposition (mg/m²/day)",
  "y_axis": "Ultrasonic Steel Thickness Loss (mm)",
  "status": "RENDERED"
}
```

---

### Actionable Recommendations

- **Targeted Protective Coating Application**: Schedule high-build barrier coating (zinc-rich epoxy mastic/polyurethane topcoat compliant with ISO 12944 C5-M marine standard) for towers `TWR-500-012`, `TWR-500-015`, and `TWR-500-018` within 90 days.
- **Shorten Inspection Intervals**: Shift coastal structures ($< 5\ \text{km}$ from coastline) from a 36-month inspection cadence to a 12-month ultrasonic non-destructive testing (NDT) and atmospheric salt monitoring cycle.
- **Structural Leg Member Reinforcement Assessment**: Issue structural engineering evaluation orders for `TWR-500-012` where flange member thickness loss exceeds $24\%$, approaching ASCE 10 allowable structural stress limits.
- **Cathodic Ground Collar Protection**: Inspect and retrofit sacrificial zinc galvanic anode systems at ground line transitions (soil-to-air interface) where chloride leaching from sea spray accumulates in foundation soils.

---

### [TIER 2 ACTION REQUIRED]

```yaml
action_type: "CREATE_FIELD_WORK_ORDER_AND_CAPITAL_INTERVENTION"
domain: "asset_management"
sub_domain: "transmission_tower_corrosion_analyzer"
target_assets:
  - "TWR-500-012"
  - "TWR-500-015"
  - "TWR-500-018"
line_id: "TL-500-COASTAL-01"
grid_zone_id: "Zone-1A"
scope_of_work:
  - "Emergency surface grit blast and multi-layer C5-M compliant anti-corrosion recoating"
  - "Ultrasonic A-scan / Phased Array verification on critical base flange joints"
  - "Structural splice reinforcement plate installation on TWR-500-012"
estimated_cost_usd: 185000.00
safety_criticality: "HIGH (Structural integrity risk under peak NERC wind-load criteria)"
status: "AWAITING_HUMAN_IN_THE_LOOP_APPROVAL"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Stage a structural grit-blasting and protective recoating work order for Tower #72 before winter coastal gale season."

**Agent Response:**
### Executive Summary
**Tower #72 exhibits severe atmospheric and marine aerosol corrosion with significant galvanic coating depletion across lower lattice structural members and base foundation interfaces. Immediate staging of dry abrasive grit-blasting (SSPC-SP 10 / NACE No. 2 Near-White Metal) and application of an engineered multi-coat protective barrier system is critical prior to the onset of the coastal winter gale season. Implementing this remediation will restore structural integrity margins, arrest section thickness loss, and mitigate the risk of high-wind mechanical failure under coastal storm-loading profiles.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Health Index (AHI)** | 42.0 / 100 | $\ge$ 80.0 / 100 | -47.5% | **Critical** |
| **Dry Film Coating Thickness (Base/Lattice)** | 1.8 mils | 8.0 - 12.0 mils | -81.3% | **Critical** |
| **Sacrificial Zinc Layer Depletion** | 88.5% | $\le$ 20.0% | +342.5% | **Critical** |
| **Structural Member Section Loss (Max)** | 9.4% | $\le$ 5.0% | +88.0% | **Warning** |
| **Atmospheric Chloride Deposition Rate** | 185 mg/m²·day | $\le$ 60 mg/m²·day | +208.3% | **Critical** |
| **Remaining Useful Life (RUL) Without Action** | 2.4 Years | 25.0 Years | -90.4% | **Critical** |

---

### Visualization Triggers

A bar chart visualizing degradation levels across structural sections of Tower #72 has been generated to prioritize surface prep and recoating passes.

```json
{
  "chart_type": "bar",
  "title": "Tower #72 Section Corrosion Degradation & Coating Thickness Loss",
  "labels": [
    "Base/Foundation Interface",
    "Lower Lattice Legs",
    "Middle Bracing",
    "Upper Crossarms",
    "Peak / Shield Wire Arm"
  ],
  "datasets": [
    {
      "label": "Observed Coating Loss (%)",
      "data": [85, 78, 62, 45, 40],
      "unit": "%"
    },
    {
      "label": "Galvanic Sacrificial Depletion (%)",
      "data": [90, 82, 65, 48, 42],
      "unit": "%"
    }
  ]
}
```

---

### Actionable Recommendations

- **Surface Preparation Specification**: Execute abrasive grit-blasting compliant with SSPC-SP 10 / NACE No. 2 (Near-White Blast Cleaning) to achieve a 2.0–3.0 mil surface profile on all degraded carbon steel members.
- **Protective Coating System**: Apply a 3-coat marine-grade system:
  1. *Primer*: Organic Zinc-Rich Epoxy Primer (3.0–4.0 mils DFT).
  2. *Intermediate*: High-Build Polyamide Epoxy (4.0–6.0 mils DFT).
  3. *Topcoat*: Aliphatic Polyurethane UV/Chloride-Resistant finish (2.0–3.0 mils DFT).
- **Environmental & Outage Coordination**: Stage containment tarps and negative-air recovery systems to adhere to environmental dust/spent abrasive capture standards; coordinate non-reclose / line de-energization windows with Transmission System Operations.
- **Pre-Storm Inspection**: Conduct dry film thickness (DFT) magnetic gauge testing (SSPC-PA 2) and holiday detection prior to final project sign-off and the commencement of seasonal high-wind gale periods.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "WORK_ORDER_CREATION",
  "asset_id": "TOWER-72",
  "grid_zone_id": "COASTAL-SECTOR-04",
  "priority": "HIGH_EXPEDITED",
  "scope_of_work": {
    "surface_prep": "SSPC-SP 10 / NACE No. 2 Abrasive Grit-Blasting",
    "coating_system": "3-Coat Zinc-Epoxy-Polyurethane System",
    "target_completion_window": "Pre-Winter Coastal Gale Season (within 30 days)",
    "environmental_containment": "Lead/Particulate Containment Level 2"
  },
  "estimated_budget_impact": "$48,500 USD",
  "requires_line_clearance": true,
  "human_in_the_loop_approval": "PENDING_ASSET_MANAGER_AUTHORIZATION"
}
```
