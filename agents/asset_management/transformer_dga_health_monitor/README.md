# ⚡ Transformer Dga Health Monitor

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of transformer dga health monitor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Transformer Dga Health Monitor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank transformer dga health monitor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.transformer_dga_health_monitor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What do the latest dissolved gas ratios for Main Transformer T-104 reveal regarding acetylene and ethylene generation?"

**Agent Response:**
### Executive Summary
**Recent Dissolved Gas Analysis (DGA) telemetry for Main Transformer T-104 reveals an acute surge in ethylene ($\text{C}_2\text{H}_4$) and a rapid emergence of acetylene ($\text{C}_2\text{H}_2$), indicating a progressive high-temperature thermal fault ($T > 700^\circ\text{C}$, IEC Fault T3) with localized electrical sparking/arcing. The sharp increase in the $\text{C}_2\text{H}_4 / \text{C}_2\text{H}_6$ ratio combined with detectable $\text{C}_2\text{H}_2$ generation elevates T-104 into IEEE C57.104 Condition 3 (High Risk), requiring immediate diagnostic re-sampling and operational derating.**

---

### DGA Telemetry & Gas Ratio Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Acetylene ($\text{C}_2\text{H}_2$)** | 9.2 ppm | < 1.0 ppm | +820.0% | **Critical** |
| **Ethylene ($\text{C}_2\text{H}_4$)** | 310.0 ppm | < 50.0 ppm | +520.0% | **Critical** |
| **Methane ($\text{CH}_4$)** | 120.0 ppm | < 40.0 ppm | +200.0% | **Warning** |
| **Ethane ($\text{C}_2\text{H}_6$)** | 55.0 ppm | < 30.0 ppm | +83.3% | **Warning** |
| **Hydrogen ($\text{H}_2$)** | 85.0 ppm | < 40.0 ppm | +112.5% | **Warning** |
| **Carbon Monoxide ($\text{CO}$)** | 480.0 ppm | < 350.0 ppm | +37.1% | **Warning** |
| **Total Dissolved Combustible Gas (TDCG)** | 579.2 ppm | < 720.0 ppm (Rate Alert) | +245.0% (30d Rate) | **Critical** |
| **Ratio $\text{C}_2\text{H}_2 / \text{C}_2\text{H}_4$** | 0.030 | < 0.010 | +200.0% | **Critical** |
| **Ratio $\text{CH}_4 / \text{H}_2$** | 1.41 | 0.10 – 1.00 | +41.0% | **Warning** |
| **Ratio $\text{C}_2\text{H}_4 / \text{C}_2\text{H}_6$** | 5.64 | < 3.00 | +88.0% | **Critical** |
| **Asset Health Index (AHI)** | 42.1 / 100 | > 85.0 / 100 | -50.5% | **Critical** |

---

### Key Engineering Findings
1. **Ethylene ($\text{C}_2\text{H}_4$) Acceleration**: The dominant gas produced is ethylene ($310\text{ ppm}$), which establishes severe, high-energy thermal decomposition of insulating mineral oil at core/winding hotspots exceeding $700^\circ\text{C}$.
2. **Emergence of Acetylene ($\text{C}_2\text{H}_2$)**: The generation of acetylene exceeding $9\text{ ppm}$ demonstrates that hot spot temperatures have localized sufficiently to cause dielectric oil breakdown and intermittent micro-arcing/sparking near contacts or circulating current loops.
3. **Duval Triangle / Rogers Ratio Diagnostic**: Ratios point directly to a combined **T3 (Thermal fault > 700°C)** with secondary **D1/D2 (Discharges of low/high energy)** pattern.

---

### Visualization Trigger

**Recommended Visualization**: Multi-Gas Time-Series Trend & Duval Triangle Coordinate Plot.

```json
{
  "chart_type": "line",
  "title": "Main Transformer T-104 DGA Key Gas Evolution (ppm)",
  "xAxis": ["2023-10-01", "2023-11-01", "2023-12-01", "2024-01-01", "2024-02-01", "2024-03-01"],
  "series": [
    {
      "name": "Acetylene (C2H2)",
      "data": [0.5, 0.8, 1.2, 2.5, 4.8, 9.2]
    },
    {
      "name": "Ethylene (C2H4)",
      "data": [45.0, 52.0, 68.0, 110.0, 185.0, 310.0]
    },
    {
      "name": "Methane (CH4)",
      "data": [30.0, 35.0, 42.0, 60.0, 85.0, 120.0]
    },
    {
      "name": "Ethane (C2H6)",
      "data": [15.0, 18.0, 22.0, 30.0, 42.0, 55.0]
    }
  ]
}
```

---

### Actionable Recommendations

- **Diagnostic Verification**: Perform an immediate confirmatory laboratory oil sample verification (ASTM D3612) and configure the online DGA monitor to 4-hour sampling cycles.
- **Acoustic / PD Monitoring**: Deploy acoustic and UHF partial discharge telemetry to isolate the physical source of the thermal/arcing hotspot within the tank.
- **Thermal & Load Management**: Restrict transformer loading to $<70\%$ MVA rating to suppress gas generation rate acceleration.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "LOAD_DERATE_AND_OUTAGE_SCHEDULING"
  asset_id: "Main Transformer T-104"
  recommended_action: "Derate T-104 capacity to 65% nominal rating and schedule forced diagnostic outage within 72 hours for internal inspection and SFRA/dielectric testing."
  risk_assessment: "High risk of catastrophic tank/bushing failure if high-temperature arcing continues under peak load conditions."
  operator_confirmation_required: true
```

### Example 2: Trend & Comparative Analysis
**User:** "Examine the historical Duval triangle trajectory for Substation North to determine if active thermal arcing is accelerating."

**Agent Response:**
### Executive Summary
**Dissolved Gas Analysis (DGA) telemetry for Substation North indicates an accelerating transition from high-temperature thermal degradation ($T3$) into severe high-energy arcing ($D2$). Acetylene ($C_2H_2$) concentration has surged by +437.0% over the last 30 days alongside elevated Ethylene ($C_2H_4$), confirming active, uncontained electrical arcing within the main winding or tap-changer compartment. Immediate operational intervention is required to prevent catastrophic dielectric breakdown and tank failure.**

---

### Data Presentation (DGA & Duval Triangle Telemetry)

| Metric | Current Value | Baseline / Target (IEEE C57.104) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Acetylene ($C_2H_2$)** | 145.0 ppm | < 1.0 ppm (Condition 1) | +14,400.0% | **Critical** |
| **Ethylene ($C_2H_4$)** | 264.0 ppm | < 50.0 ppm | +428.0% | **Critical** |
| **Methane ($CH_4$)** | 91.0 ppm | < 40.0 ppm | +127.5% | **Warning** |
| **Hydrogen ($H_2$)** | 380.0 ppm | < 100.0 ppm | +280.0% | **Critical** |
| **Total Combustible Gases (TDCG)** | 880.0 ppm | < 720.0 ppm | +22.2% | **Critical** |
| **$C_2H_2$ Rate of Generation** | 12.8 ppm/day | < 0.5 ppm/day | +2,460.0% | **Critical** |
| **Duval Triangle 1 Coordinates** | %$CH_4$: 18.2%, %$C_2H_4$: 52.8%, %$C_2H_2$: 29.0% | Baseline: Zone T2 | Trajectory $\to$ Zone D2 | **Critical** |
| **Asset Health Index (AHI)** | 32.4 / 100 | $\ge$ 80.0 | -59.5% | **Critical** |

---

### Visualization Triggers
**Recommended Chart Type:** **Duval Triangle 1 Ternary Plot / Multi-Interval Trajectory Plot**  
*Visualizes the migration of gas percentage ratios across diagnostic zones over the past 30 days.*

```json
{
  "chart_type": "ternary_scatter",
  "title": "Substation North Historical Duval Triangle 1 Fault Trajectory",
  "data_points": [
    {
      "interval": "T-30 Days",
      "ch4_pct": 58.4,
      "c2h4_pct": 36.2,
      "c2h2_pct": 5.4,
      "zone": "T2 (Thermal Fault 300°C - 700°C)"
    },
    {
      "interval": "T-14 Days",
      "ch4_pct": 42.1,
      "c2h4_pct": 49.3,
      "c2h2_pct": 8.6,
      "zone": "T3 (Thermal Fault > 700°C)"
    },
    {
      "interval": "T-7 Days",
      "ch4_pct": 28.5,
      "c2h4_pct": 54.0,
      "c2h2_pct": 17.5,
      "zone": "DT (Thermal & Electrical Fault)"
    },
    {
      "interval": "Current Telemetry",
      "ch4_pct": 18.2,
      "c2h4_pct": 52.8,
      "c2h2_pct": 29.0,
      "zone": "D2 (High Energy Arcing)"
    }
  ]
}
```

---

### Actionable Recommendations
- **Dynamic Load Curtailment / Transfer:** Immediately shed or reroute load from Substation North to adjacent feeders/substations to minimize dielectric and thermal stress.
- **Continuous Gas Monitoring:** Increase online DGA sampling frequency to real-time 1-hour intervals and dispatch an emergency field sampling crew for gas chromatography verification.
- **Acoustic / UHF Partial Discharge Testing:** Perform emergency acoustic partial discharge triangulation to pinpoint the physical fault coordinates within the transformer tank.
- **Tier 2 Escalation:** Initiate controlled de-energization and inspection protocol before a violent dielectric puncture occurs.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "CONTROLLED_ASSET_DE_ENERGIZATION_AND_LOAD_TRANSFER"
  asset_id: "XFRM-SUB-NORTH-01"
  substation_id: "Substation North"
  grid_zone_id: "ZONE_NORTH_TX"
  urgency: "HIGH"
  justification: "Accelerating Duval Triangle D2 (High Energy Arcing) trajectory with Acetylene generation rate at 12.8 ppm/day, indicating imminent catastrophic winding flashover."
  target_load_transfer_bus: "SUB-NORTH-BUS-B / TIE-FEEDER-402"
  required_approvals:
    - "Grid Operations Dispatch Supervisor"
    - "Transmission Asset Health Lead"
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Issue an immediate transformer load derate directive and schedule emergency oil degasification treatment."

**Agent Response:**
### Executive Summary
**Direct autonomous execution of a transformer load derate and emergency oil degasification constitutes a Tier 2 physical grid modification and field maintenance dispatch, which requires Human-in-the-Loop (HITL) engineering approval. Telemetry and specific asset identifiers for the target transformer were not specified in the request, precluding autonomous fault classification under IEEE C57.104 standards. A formal confirmation payload has been generated for operator review and asset binding.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Asset Identifier** | *INSUFFICIENT DATA* | Valid Equipment ID | N/A | **Warning** |
| **Total Dissolved Combustible Gas (TDCG)** | *INSUFFICIENT DATA* | < 720 ppm (IEEE Condition 1) | N/A | **Warning** |
| **Acetylene ($\text{C}_2\text{H}_2$)** | *INSUFFICIENT DATA* | < 1 ppm | N/A | **Warning** |
| **Hydrogen ($\text{H}_2$)** | *INSUFFICIENT DATA* | < 100 ppm | N/A | **Warning** |
| **Ethylene ($\text{C}_2\text{H}_4$)** | *INSUFFICIENT DATA* | < 50 ppm | N/A | **Warning** |
| **Asset Health Index (AHI)** | *INSUFFICIENT DATA* | $\ge 85.0$ | N/A | **Warning** |

---

### Visualization Trigger

```json
{
  "chart_type": "bar",
  "title": "Dissolved Gas Analysis (DGA) Key Gas Concentrations vs IEEE C57.104 Limits",
  "data": [
    {"gas": "H2", "measured_ppm": 0, "threshold_ppm": 100},
    {"gas": "CH4", "measured_ppm": 0, "threshold_ppm": 120},
    {"gas": "C2H2", "measured_ppm": 0, "threshold_ppm": 1},
    {"gas": "C2H4", "measured_ppm": 0, "threshold_ppm": 50},
    {"gas": "C2H6", "measured_ppm": 0, "threshold_ppm": 65},
    {"gas": "CO", "measured_ppm": 0, "threshold_ppm": 350},
    {"gas": "CO2", "measured_ppm": 0, "threshold_ppm": 2500}
  ],
  "note": "Awaiting asset-specific telemetry ingestion to populate measured PPM values."
}
```

---

### Actionable Recommendations
- **Identify Asset Context**: Provide the specific `substation_id`, `transformer_id`, and recent laboratory or online DGA monitor (photoacoustic/GC) telemetry.
- **DGA Diagnostic Assessment**: Upon ingestion of gas values, evaluate fault types using Duval Triangle / Pentagon methods and rate of gas generation ($\Delta\text{ppm}/\text{day}$) per IEEE C57.104-2019.
- **Operational Verification**: Coordinate with Transmission/Distribution System Operations to evaluate grid contingency ($N-1$) impacts prior to executing any capacity curtailment or derate.
- **Operator Approval**: Authorize the physical maintenance work order and SCADA load limit adjustment via the Tier 2 confirmation workflow below.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_GRID_LOAD_DERATE_AND_OIL_TREATMENT",
  "approval_status": "PENDING_OPERATOR_APPROVAL",
  "safety_level": "TIER_2",
  "parameters": {
    "target_asset_id": "UNSPECIFIED (Awaiting Operator Input)",
    "requested_actions": [
      "SCADA Operational Capacity Derate Directive",
      "Field Dispatch: Emergency Mobile Oil Degasification / Dehydration Unit"
    ],
    "governing_standard": "IEEE C57.104 / IEEE C57.91",
    "required_operator_inputs": [
      "asset_id",
      "derate_percentage_or_mva_limit",
      "outage_schedule_window_utc"
    ]
  },
  "critic_validation": "APPROVED_FOR_HITL_ESCALATION"
}
```
