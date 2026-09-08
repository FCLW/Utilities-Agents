# ⚡ Distribution Phase Imbalance Detector

![Domain](https://img.shields.io/badge/Domain-grid%20balancing-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of distribution phase imbalance detector is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Distribution Phase Imbalance Detector Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank distribution phase imbalance detector events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_balancing.distribution_phase_imbalance_detector_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are Phase A, B, and C current loadings on Feeder 14 balanced, or is the neutral current exceeding the 15% threshold?"

**Agent Response:**
### Executive Summary
**Feeder 14 is experiencing severe phase current imbalance, with Phase A carrying disproportionately high loading compared to Phase B and Phase C.** **The calculated neutral current stands at 117.2 A (46.9% of average phase loading), substantially exceeding the utility operating threshold of 15.0%.** **Immediate phase load rebalancing and supervisory field intervention are required to prevent neutral conductor thermal degradation and ground fault false-tripping.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Phase A Current ($I_A$)** | 320.0 A | 250.0 A ($I_{\text{avg}}$) | +28.0% | **Warning** |
| **Phase B Current ($I_B$)** | 245.0 A | 250.0 A ($I_{\text{avg}}$) | -2.0% | **Normal** |
| **Phase C Current ($I_C$)** | 185.0 A | 250.0 A ($I_{\text{avg}}$) | -26.0% | **Warning** |
| **Current Unbalance (IEEE 141)** | 28.0% | $\le 10.0\%$ | +180.0% | **Critical** |
| **Neutral Return Current ($I_N$)** | 117.2 A | $\le 37.5\text{ A}$ (15% $I_{\text{avg}}$) | +212.5% | **Critical** |
| **Neutral-to-Average Ratio** | 46.9% | $\le 15.0\%$ | +212.7% | **Critical** |

*Calculation Assumptions:*
- $I_{\text{avg}} = \frac{I_A + I_B + I_C}{3} = 250.0\text{ A}$
- Max Phase Current Deviation = $|320.0 - 250.0| = 70.0\text{ A}$
- Neutral current $I_N$ calculated via symmetrical sequence vector summation: $\vec{I}_N = -(\vec{I}_A + \vec{I}_B + \vec{I}_C) = 117.2\angle 153.7^\circ\text{ A}$.

---

### Visualization Triggers

```json
{
  "chart_type": "bar",
  "title": "Feeder 14 Phase Loadings vs. Neutral Current & Limits",
  "xAxis": {
    "categories": ["Phase A", "Phase B", "Phase C", "Neutral Current (Actual)", "Neutral Current Limit (15%)"]
  },
  "yAxis": {
    "title": "Current (Amperes)"
  },
  "series": [
    {
      "name": "Current (A)",
      "data": [320.0, 245.0, 185.0, 117.2, 37.5]
    }
  ]
}
```

---

### Actionable Recommendations

- **Dispatch Field Engineering Crew**: Investigate lateral takeoffs on Feeder 14 to identify heavily single-phased residential/commercial loads on Phase A.
- **Phase Reconfiguration**: Transfer approximately 65–70 A of single-phase load from Phase A to Phase C across distribution transformers DT-1404 through DT-1409.
- **Protection Coordination Check**: Verify that neutral overcurrent (50N/51N) relay pickup settings on Feeder 14 breaker are not at imminent risk of false tripping during peak demand.

---

### [TIER 2 ACTION REQUIRED]

```yaml
Tier_2_Operation:
  Feeder_ID: "Feeder 14"
  Substation_ID: "SUB-04"
  Operation_Type: "Automated/Manual Load Transfer & Phase Balancing"
  Proposed_Action: "Execute lateral phase transfer switching sequence to shift 65 A load from Phase A to Phase C"
  Safety_Impact: "Modifies physical grid topology and single-phase distribution routing"
  Prerequisites: "Distribution System Operator (DSO) clearance, verified open-point interlocking, zero active downstream work permits"
  Requires_Approval: true
```

### Example 2: Trend & Comparative Analysis
**User:** "Track the historical voltage unbalance factor (VUF) on lateral taps with heavy single-phase rooftop solar concentrations."

**Agent Response:**
### 1. Executive Summary
**Analysis of lateral taps with heavy single-phase rooftop solar PV concentrations (>35% penetration) reveals severe mid-day Voltage Unbalance Factor (VUF) excursions peaking at 2.82%, directly breaching the IEEE 1159 and ANSI C84.1 standard threshold of 2.0%. Asymmetric active power injection into single-phase tap takeoffs (predominantly Phase A and Phase B) during peak solar irradiance hours (11:00–14:00) is driving negative-sequence voltage amplification across downstream 3-phase trunk sections. Immediate automated phase balancing reconfiguration and smart inverter volt-var curve harmonization are required to prevent induction motor derating and transformer neutral overheating.**

---

### 2. Data Presentation: Historical VUF & Phase Imbalance Telemetry

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak VUF ($V_2 / V_1$) (LAT-7042)** | 2.82% | $\le$ 2.00% (ANSI C84.1) | +41.0% | **Critical** |
| **Mean Daytime VUF (High-PV Laterals)** | 2.15% | $\le$ 1.00% (IEEE Recommended) | +115.0% | **Warning** |
| **Phase-to-Neutral Voltage Spread ($\Delta V_{A-C}$)** | 0.082 p.u. (9.84 V) | $\le$ 0.030 p.u. (3.60 V) | +173.3% | **Critical** |
| **Negative Sequence Voltage ($V_2$)** | 2.95 V | $\le$ 1.20 V | +145.8% | **Critical** |
| **Neutral Return Current ($I_N$) Peak** | 68.4 A | $\le$ 25.0 A | +173.6% | **Warning** |
| **DER Active Reverse Power Flow (Phase A)** | 420 kW | 0 kW (Net Forward Load) | N/A | **Warning** |

---

### 3. Visualization Trigger

```json
{
  "chart_type": "line",
  "title": "Historical Voltage Unbalance Factor (VUF) vs. Solar Peak Hours on High-DER Lateral Taps",
  "xAxis": {
    "title": "Diurnal Profile Interval",
    "categories": ["00:00", "04:00", "08:00", "11:00", "13:00", "15:00", "18:00", "22:00"]
  },
  "yAxis": {
    "title": "Voltage Unbalance Factor (%)",
    "threshold": 2.0,
    "threshold_label": "IEEE 1159 / ANSI C84.1 Limit (2.0%)"
  },
  "series": [
    {
      "name": "Lateral LAT-7042 (Phase A: 65% PV Penetration)",
      "data": [0.62, 0.58, 1.15, 2.45, 2.82, 2.10, 0.95, 0.60]
    },
    {
      "name": "Lateral LAT-3118 (Phase B: 52% PV Penetration)",
      "data": [0.48, 0.45, 0.92, 1.88, 2.25, 1.70, 0.80, 0.52]
    },
    {
      "name": "Lateral LAT-5091 (Phase C: 44% PV Penetration)",
      "data": [0.55, 0.50, 0.85, 1.62, 1.95, 1.45, 0.78, 0.54]
    },
    {
      "name": "Balanced Feeder Baseline (<10% PV)",
      "data": [0.35, 0.32, 0.40, 0.48, 0.52, 0.45, 0.42, 0.36]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Dynamic Phase Reconnection / Swapping**: Dispatch field operations to roll high-generation single-phase solar customer connections from heavily loaded Phase A onto underutilized Phase C on Lateral `LAT-7042` and `LAT-3118`.
- **Smart Inverter Volt-Var Optimization**: Broadcast updated IEEE 1547-2018 Volt-Var / Volt-Watt setpoints via DERMS to single-phase PV inverters on over-voltage phases to mitigate localized voltage rise during 11:00–14:00 peak solar irradiance.
- **Automated Capacitor & Regulator Control**: Lock step-voltage regulator (SVR) independent single-phase regulation mode on upstream main-line autotransformers to prevent hunting caused by reverse power flow.
- **Continuous Negative-Sequence Telemetry Monitoring**: Deploy high-resolution micro-PMU / power quality sensor triggers at lateral fuse cutouts to flag any persistent $V_2 > 2.0\%$ lasting longer than 15 consecutive minutes.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "operation_type": "GRID_SWITCHING_DERMS_DISPATCH",
  "feeder_id": "FDR-SUB12-04",
  "impacted_laterals": ["LAT-7042", "LAT-3118"],
  "proposed_action": "Execute remote smart inverter active power curtailment (15%) and Volt-Var curve Q(V) steepening on Phase A single-phase PV clusters to bring VUF below the 2.0% compliance limit.",
  "risk_assessment": "Low risk of localized DER revenue loss (<$45.00 aggregate); eliminates high risk of commercial 3-phase customer motor thermal trips and distribution transformer degradation.",
  "requires_hitl_approval": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Stage a phase-swap switching recommendation to transfer three lateral taps from overloaded Phase A to underloaded Phase C."

**Agent Response:**
### 1. Executive Summary
**Feeder Phase Imbalance analysis indicates Phase A is operating at an elevated 412 A (40.9% imbalance), violating IEEE 141 / ANSI C84.1 phase balance guidelines and driving excessive neutral return current (142 A). Transferring Lateral Taps L-104, L-112, and L-128 totaling ~117 A from Phase A to underloaded Phase C (178 A) will equalize feeder loading to approximately 295 A per phase and reduce neutral current by 87.3%. This staged switching plan requires physical crew field re-termination and distribution control operator approval prior to execution.**

---

### 2. Data Presentation (Markdown Tables)

#### Feeder Phase & Neutral Current Metrics (Pre vs. Post Stage)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Phase A Current ($I_A$)** | 412 A | 290 A | +42.1% | Critical |
| **Phase B Current ($I_B$)** | 285 A | 290 A | -1.7% | Normal |
| **Phase C Current ($I_C$)** | 178 A | 290 A | -38.6% | Warning |
| **Current Imbalance ($\% I_{unbal}$)** | 40.9% | $\le 10.0\%$ | +309.0% | Critical |
| **Neutral Current ($I_N$)** | 142 A | $\le 25.0\text{ A}$ | +468.0% | Critical |
| **Projected Post-Swap $I_A$** | 295 A | 290 A | +1.7% | Normal |
| **Projected Post-Swap $I_C$** | 295 A | 290 A | +1.7% | Normal |
| **Projected Post-Swap $I_N$** | 18 A | $\le 25.0\text{ A}$ | -87.3% | Normal |

#### Lateral Tap Switching Matrix

| Lateral Tap ID | Location / Structure Pole | Transferred Load (A) | Source Phase | Target Phase | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Tap L-104** | Pole #P-44029 / Node N-302 | 42 A | Phase A | Phase C | Staged |
| **Tap L-112** | Pole #P-44180 / Node N-318 | 38 A | Phase A | Phase C | Staged |
| **Tap L-128** | Pole #P-44315 / Node N-345 | 37 A | Phase A | Phase C | Staged |
| **Total Transfer** | **Cumulative Load** | **117 A** | **Phase A** | **Phase C** | **Staged** |

---

### 3. Visualization Triggers

**Chart Reference:** Grouped Bar Chart comparing Pre-Switching vs. Post-Switching phase loading ($I_A, I_B, I_C, I_N$).

```json
{
  "chart_type": "bar",
  "title": "Phase Loading Before vs. After Proposed Lateral Tap Transfer",
  "categories": ["Phase A", "Phase B", "Phase C", "Neutral Current (In)"],
  "series": [
    {
      "name": "Pre-Switching Current (A)",
      "data": [412, 285, 178, 142]
    },
    {
      "name": "Post-Switching Current (A) [Estimated]",
      "data": [295, 285, 295, 18]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Switching Order Verification**: Forward the staged phase-swap switching sequence (L-104, L-112, L-128) to the Distribution System Operator (DSO) and Outage Management System (OMS) for pre-work clearance review.
- **Field Crew Dispatch**: Issue work orders for line crews to inspect cutout switches, phase-identification markers, and secondary drop balance at structures P-44029, P-44180, and P-44315.
- **SCADA Telemetry Baseline**: Set temporary SCADA alarms to monitor feeder head current transformers (CTs) and feeder end-of-line voltage sensors immediately following cutover to confirm balanced voltage profile.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PHYSICAL_GRID_SWITCHING_ORDER",
  "feeder_id": "FDR-DIST-7120",
  "substation_id": "SUB-WEST-04",
  "work_order_type": "LATERAL_PHASE_SWAP",
  "tap_operations": [
    {
      "lateral_id": "L-104",
      "pole_number": "P-44029",
      "action": "DISCONNECT_PHASE_A_CONNECT_PHASE_C",
      "expected_load_shift_amperes": 42.0
    },
    {
      "lateral_id": "L-112",
      "pole_number": "P-44180",
      "action": "DISCONNECT_PHASE_A_CONNECT_PHASE_C",
      "expected_load_shift_amperes": 38.0
    },
    {
      "lateral_id": "L-128",
      "pole_number": "P-44315",
      "action": "DISCONNECT_PHASE_A_CONNECT_PHASE_C",
      "expected_load_shift_amperes": 37.0
    }
  ],
  "safety_clearance_required": true,
  "human_in_the_loop_approval_required": true
}
```
