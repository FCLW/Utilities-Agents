# ⚡ Storm Damage Prediction Modeler

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of storm damage prediction modeler is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Storm Damage Prediction Modeler Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank storm damage prediction modeler events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.storm_damage_prediction_modeler_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many broken poles and downed distribution wire spans will the incoming Category 2 hurricane cause in Coastal Division?"

**Agent Response:**
### Executive Summary
**Based on predictive damage modeling for an incoming Category 2 Hurricane (sustained winds 96–110 mph, gusts up to 120 mph) across Coastal Division, the model forecasts a mean of 485 broken poles (95% CI: 410–560) and 1,420 downed distribution wire spans (95% CI: 1,210–1,630). High-risk asset exposure is concentrated along the Barrier Islands and Metro Coastal districts, driven by saturated soil conditions, elevated tree canopy density, and sustained aerodynamic loading.**

---

### Data Presentation: Storm Damage & Asset Impact Forecast

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Predicted Broken Distribution Poles (Mean)** | **485 poles** (95% CI: 410–560) | 12 poles (Blue Sky baseline) | +3,941.7% | **Critical** |
| **Predicted Downed Wire Spans (Mean)** | **1,420 spans** (95% CI: 1,210–1,630) | 28 spans (Blue Sky baseline) | +4,971.4% | **Critical** |
| **Damaged Distribution Transformers** | **118 units** (95% CI: 95–142) | 4 units (Blue Sky baseline) | +2,850.0% | **Critical** |
| **Feeder Lockout Probability (>75% risk)** | **86 feeders** (out of 320 feeders) | 0 feeders | N/A | **Critical** |
| **Model Mean Absolute Percentage Error (MAPE)** | **4.2%** | < 5.0% (Operational threshold) | -16.0% | **Normal** |
| **Customer Interruption Exposure** | **148,500 customers** (64.5% of Division) | < 1,500 customers | +9,800.0% | **Critical** |

---

### Geographic & Feeder-Level Damage Breakdown

```json
{
  "chart_type": "bar",
  "title": "Coastal Division - Category 2 Hurricane Damage Prediction by District",
  "data": {
    "categories": ["Barrier Islands", "Metro Coastal", "Bayfront North", "Harbor South", "Inland Estuary"],
    "series": [
      {
        "name": "Broken Poles (Mean)",
        "data": [125, 135, 110, 75, 40]
      },
      {
        "name": "Downed Wire Spans (Mean)",
        "data": [410, 390, 320, 200, 100]
      },
      {
        "name": "Exposed Feeder Circuits",
        "data": [42, 98, 76, 64, 40]
      }
    ]
  }
}
```

*Visualization Recommendation: Stacked Bar Chart & Spatial GIS Heatmap overlaying circuit-level wind vector paths and tree canopy failure risks.*

---

### Actionable Recommendations

1. **Pre-Staging Staging Areas (Incident Command)**: Immediately mobilize mutual aid logistics to pre-stage at Central Staging Site A (Inland Base) and Site B (Harbor North), outside the primary storm surge inundation zones.
2. **Material Inventory Allocation**: Release and stage a minimum buffer inventory of 550 Class 3/4 distribution poles (35ft/40ft/45ft), 1,600 crossarms, 45 miles of ACSR conductor (1/0 and 4/0 AWG), and 140 overhead distribution transformers.
3. **Vegetation Management Rapid Response**: Dispatch tree-trimming rapid clearing crews along critical backbone feeder three-phase trunks feeding regional hospitals, water treatment plants, and emergency shelters.
4. **SCADA / FLISR Configuration**: Transition automated FLISR loops in Barrier Islands to manual confirmation mode 2 hours prior to tropical storm force wind arrival (to prevent closing onto hard pole ground faults).

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_action_request:
  action_type: "EMERGENCY_LOGISTICS_AND_MUTUAL_AID_MOBILIZATION"
  target_division: "Coastal Division"
  justification: "Category 2 hurricane asset damage threshold exceeded (485 broken poles, 1,420 downed wire spans predicted)."
  required_approvals:
    - role: "Grid Operations Incident Commander"
    - role: "Vice President of Distribution Operations"
  actions_to_execute:
    - "Authorize immediate call-out of 65 external mutual aid distribution line crews and 30 vegetation crews."
    - "Issue automated warehouse pick-list for 550 distribution poles and 45 miles of conductor stock to Inland Staging Depot."
    - "Authorize DMS operational override to pre-isolate non-essential barrier island water crossing interties upon sustained wind speeds exceeding 75 mph."
```

### Example 2: Trend & Comparative Analysis
**User:** "Run Monte Carlo damage simulations combining 65 mph wind gust forecasts, soil moisture saturation, and tree canopy density."

**Agent Response:**
### 1. Executive Summary
**Monte Carlo probabilistic storm damage simulations ($N=10,000$ iterations) indicate high structural asset vulnerability driven by the compound interaction of 65 mph wind gusts and high soil moisture saturation (88%–94%) across heavy tree canopy corridors.** **The probabilistic model projects a mean of $135$ broken poles, $549$ tree-on-wire/downed line incidents, and approximately $104,000$ customer interruptions concentrated in Zone-North and Zone-East.** **System damage indices exceed standard operational thresholds by $+248\%$, necessitating immediate activation of Level 4 Storm Preparedness and pre-staging of mutual aid crews.**

---

### 2. Data Presentation: Simulation Results & Risk Metrics

| Metric | Simulated Mean (95% CI) | Baseline / Normal Threshold | Delta (%) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Peak Wind Gust Loading** | 65.0 mph ($61.2 - 68.8\text{ mph}$) | 35.0 mph | $+85.7\%$ | **Critical** |
| **Soil Saturation Level** | 91.4% ($86.0\% - 96.5\%$) | 45.0% | $+103.1\%$ | **Critical** |
| **Canopy Failure Probability (Per Span Mile)** | 14.8% ($12.1\% - 17.6\%$) | 1.8% | $+722.2\%$ | **Critical** |
| **Total Broken Distribution Poles** | 135 ($112 - 164$) | 12 | $+1,025.0\%$ | **Critical** |
| **Downed Conductors / Wire Strikes** | 549 ($480 - 625$) | 45 | $+1,120.0\%$ | **Critical** |
| **Predicted Transformer Lockouts** | 82 ($68 - 99$) | 15 | $+446.7\%$ | **Critical** |
| **Sustained Customer Interruptions (CI)** | 104,000 ($89,500 - 121,000$) | 8,500 | $+1,123.5\%$ | **Critical** |
| **Estimated System Restoration Time (CAIDI Target)** | 42.5 hrs ($34.0 - 54.0\text{ hrs}$) | 4.0 hrs | $+962.5\%$ | **Critical** |

---

### 3. Spatial Simulation Breakdown & Visualization

#### Zone-Level Damage Distribution

| Grid Zone | Overhead Miles | Avg Canopy Density | Soil Saturation | Predicted Pole Failures | Predicted Line Drops | Customer Impact (CI) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Zone-North** | 412 mi | 74% (Dense) | 94% | 42 | 185 | 34,500 |
| **Zone-East** | 328 mi | 62% (Moderate-High) | 96% | 35 | 142 | 26,800 |
| **Zone-West** | 290 mi | 51% (Moderate) | 88% | 28 | 110 | 19,400 |
| **Zone-South** | 245 mi | 38% (Low-Moderate) | 85% | 19 | 74 | 11,100 |
| **Zone-Central** | 180 mi | 22% (Urban/Low) | 78% | 11 | 38 | 12,200 |

```json
{
  "chart_type": "bar",
  "title": "Predicted Asset Damage & Outage Distribution (Monte Carlo N=10,000)",
  "labels": ["Zone-North (Heavy Canopy)", "Zone-East (Coastal/Wet)", "Zone-West (Suburban)", "Zone-South (Rural/Open)", "Zone-Central (Dense Urban)"],
  "datasets": [
    {
      "label": "Expected Pole Failures (Mean)",
      "data": [42, 35, 28, 19, 11]
    },
    {
      "label": "Tree-on-Wire / Line Down Incidents",
      "data": [185, 142, 110, 74, 38]
    },
    {
      "label": "Predicted Customer Interruptions (k)",
      "data": [34.5, 26.8, 19.4, 11.1, 12.2]
    }
  ]
}
```

---

### 4. Actionable Recommendations

1. **Pre-Position Line Crews & Vegetation Strike Teams**: Mobilize and stage internal restoration crews and contracted tree-trimming contractors at North Substation (Yard 4) and East Operations Depot (Yard 2) prior to T-0 storm onset.
2. **Material Inventory Verification**: Stage high-demand replacement inventory at regional staging sites, including Class 3/4 40-foot wood poles (minimum 150 units), distribution crossarms, 1/0 ACSR conductor reels, and 25–50 kVA overhead transformers.
3. **Automated Switching & FLISR Preparation**: Validate DMS/SCADA automated feeder sectionalizing schemes in Zones North and East to isolate predicted high-canopy fault segments while maintaining critical infrastructure feeds.
4. **Emergency Operating Mode Escalation**: Transition grid operations mode from *Normal* to *Level 4 Emergency Restoration Readiness* across all affected operating dispatch desks.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "EMERGENCY_CREW_PRESTAGING_AND_MUTUAL_AID_MOBILIZATION"
  target_zones: ["Zone-North", "Zone-East", "Zone-West"]
  trigger_conditions:
    wind_gust_forecast: "65 mph"
    soil_saturation: ">90%"
    predicted_pole_failures: 135
    predicted_outages: 104000
  resource_allocation:
    internal_line_crews: 45
    contract_vegetation_crews: 60
    mutual_aid_crews_requested: 30
    logistics_staging_yards: ["Yard-North-4", "Yard-East-2"]
  flisr_reconfiguration:
    disable_reclosers_high_fire_zones: false
    enable_storm_mode_recloser_blocking: true
  authorization_required: "System Operations Incident Commander / Lead Dispatcher"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Pre-stage emergency inventory materials and staging yards in District 3 based on predicted high-impact damage clusters."

**Agent Response:**
### Executive Summary
**High-impact storm damage modeling for District 3 indicates severe structural and electrical asset exposure concentrated along Coastal/Marsh Corridor (Cluster 3B) and Pine Valley (Cluster 3D), with peak wind gusts exceeding 68 mph. Predictive modeling forecasts 215 pole failures, 86 transformer replacements, and 117 k-ft of downed conductor line across four localized clusters. Pre-staging emergency inventory at Yard 3-Alpha (North/Central) and Yard 3-Bravo (South Coastal) is required prior to storm onset to reduce Mean Time to Restoration (MTTR) by an estimated 42%.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Predicted Damaged Poles (Total)** | 215 units | 35 units (Nominal Storm) | +514.3% | **Critical** |
| **Predicted Transformer Failures** | 86 units | 15 units (Nominal Storm) | +473.3% | **Critical** |
| **Damaged Conductor Span (Est.)** | 117.0 k-ft | 25.0 k-ft | +368.0% | **Critical** |
| **Model Confidence Interval (95%)** | [204, 226] poles | [190, 240] acceptable | N/A | **Normal** |
| **Model MAPE (Historical Validation)**| 3.82% | < 5.00% | -23.6% | **Normal** |
| **District 3 Available Yard Capacity**| 88.5% | > 80.0% | +10.6% | **Normal** |
| **Estimated Restoration Time Impact** | 18.4 hrs (Pre-staged) | 31.8 hrs (Reactive) | -42.1% | **Normal** |

---

### Damage Cluster Breakdown & Inventory Allocation

| Cluster Location | Primary Hazard Driver | Predicted Pole Failures | Predicted Transformer Failures | Conductor Required (k-ft) | Recommended Staging Yard |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Cluster 3A (North Ridge)** | Heavy Ice / Sleet Loading | 48 | 16 | 22.0 | Yard 3-Alpha |
| **Cluster 3B (Coastal / Marsh)**| Gale-Force Winds (>65 mph) | 85 | 34 | 45.0 | Yard 3-Bravo |
| **Cluster 3C (Metro Central)** | Flying Debris / Tree Canopy | 18 | 9 | 12.0 | Yard 3-Alpha |
| **Cluster 3D (Pine Valley)** | High Tree Density / Soil Saturation | 64 | 27 | 38.0 | Yard 3-Bravo |

---

### Visualization

```json
{
  "chart_type": "bar",
  "title": "District 3 Storm Damage Prediction & Material Staging Requirements",
  "categories": [
    "Cluster 3A - North Ridge",
    "Cluster 3B - Coastal / Marsh",
    "Cluster 3C - Metro Central",
    "Cluster 3D - Pine Valley"
  ],
  "series": [
    {
      "name": "Predicted Damaged Poles",
      "data": [48, 85, 18, 64]
    },
    {
      "name": "Predicted Damaged Transformers",
      "data": [16, 34, 9, 27]
    },
    {
      "name": "Required Conductor (k-ft)",
      "data": [22, 45, 12, 38]
    }
  ]
}
```

---

### Actionable Recommendations
- **Material Dispatch**: Issue transfer manifests to move 135 Class 2/3 distribution poles, 50 25kVA/50kVA pad/overhead transformers, and 60 k-ft ACSR conductor to **Yard 3-Bravo (South Coastal)** immediately.
- **Secondary Yard Staging**: Transfer 90 Class 3/4 poles, 40 overhead transformers, and 60 k-ft ACSR conductor to **Yard 3-Alpha (North/Central)**.
- **Mutual Assistance & Crew Marshalling**: Coordinate with Regional Dispatch to align 14 line restoration crews and 6 vegetation management units at Staging Yard 3-Bravo by T-4 hours prior to landfall/peak wind front.
- **Logistics Verification**: Validate fuel depot reserves, mobile generation units, and satellite communications kits at both designated staging yards in accordance with NERC EOP-011 guidelines.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_INVENTORY_TRANSFER_AND_STAGING",
  "approval_level": "TIER_2_OPERATIONS",
  "target_district": "District 3",
  "source_warehouse": "Central Regional Logistics Depot",
  "destination_yards": [
    {
      "yard_id": "STAGING-YARD-3-BRAVO",
      "allocation": {
        "distribution_poles_class_2_3": 135,
        "distribution_transformers": 50,
        "conductor_acsr_kft": 60,
        "hardware_crossarm_kits": 150
      }
    },
    {
      "yard_id": "STAGING-YARD-3-ALPHA",
      "allocation": {
        "distribution_poles_class_3_4": 90,
        "distribution_transformers": 40,
        "conductor_acsr_kft": 60,
        "hardware_crossarm_kits": 100
      }
    }
  ],
  "estimated_logistics_cost": "$248,500 USD",
  "status": "PENDING_HUMAN_SUPERVISOR_APPROVAL"
}
```
