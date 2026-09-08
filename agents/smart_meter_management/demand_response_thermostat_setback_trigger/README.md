# ⚡ Demand Response Thermostat Setback Trigger

![Domain](https://img.shields.io/badge/Domain-smart%20meter%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of demand response thermostat setback trigger is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Demand Response Thermostat Setback Trigger Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank demand response thermostat setback trigger events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_smart_meter_management.demand_response_thermostat_setback_trigger_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many residential smart thermostats can we signal for a 3°F pre-cooling setback ahead of the 16:00 grid demand peak?"

**Agent Response:**
### 1. Executive Summary
**A total of 153,000 residential smart thermostats across 5 operational grid zones are fully verified, online, and eligible for the automated 3°F pre-cooling setback prior to the 16:00 grid demand peak.** Initiating pre-cooling between 14:00 and 15:45 will store thermal energy in participating homes, unlocking an estimated **191.25 MW of flexible peak demand curtailment** between 16:00 and 19:00. This action maintains an **87.4% dispatch availability rate** across enrolled residential demand response assets with zero communication gateway failures detected.

---

### 2. Fleet Availability & Impact Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Enrolled Thermostat Fleet** | 175,000 units | 175,000 units | 0.0% | Normal |
| **Active / Online AMI Connected Devices** | 161,350 units | 166,250 units (95.0%) | -2.9% | Normal |
| **Participant Opt-Out Rate (Day-Ahead)** | 8,350 units (5.2%) | < 10.0% Target | -48.0% | Normal |
| **Net Signalable Thermostats** | **153,000 units** | 140,000 units Target | **+9.3%** | **Normal** |
| **Average Indoor Baseline Temperature** | 73.4°F | 73.0°F | +0.5% | Normal |
| **Target Pre-Cooling Setpoint (3°F Setback)** | 70.4°F | 70.0°F | +0.6% | Normal |
| **Estimated Grid Curtailment Relief** | **191.25 MW** | 175.00 MW Target | **+9.3%** | **Normal** |
| **AMI Telemetry Latency (Mesh & Cellular)** | 1.42 seconds | < 5.00 seconds | -71.6% | Normal |

---

### 3. Zonal Fleet Breakdown

```json
{
  "title": "Signalable Smart Thermostats by Grid Zone (3°F Pre-Cooling Target)",
  "categories": ["North Zone", "South Metro", "West Hills", "Central Valley", "East Coastline"],
  "series": [
    {
      "name": "Signalable Devices (Online/No Opt-Out)",
      "data": [42350, 38120, 29400, 24850, 18280]
    },
    {
      "name": "Estimated Pre-Cooling Capacity (kW)",
      "data": [52937, 47650, 36750, 31062, 22850]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Stagger Pre-Cooling Dispatch (14:00 – 14:15):** Execute a ramped 3-stage dispatch (33% increments every 5 minutes) to avoid sudden local distribution feeder spikes and ramp-rate violations.
- **Set Up Real-Time Shed Telemetry:** Monitor AMI interval data and OpenADR 2.0b telemetry channels starting at 15:45 to capture initial rebound and transition dynamics at the 16:00 peak transition.
- **Maintain Hard Temperature Floors:** Enforce the 68°F lower safety limit clamp to prevent residential heat pump and compressor freezing during extended pre-cooling periods.
- **Post-Peak Ramp Recovery (19:00):** Program a staggered snapback restoration (+1°F per 30 minutes) at the event conclusion to prevent a secondary snapback demand peak.

---

### [TIER 2 ACTION REQUIRED]

```yaml
Tier_2_Operation:
  Operation_Type: "DEMAND_RESPONSE_DISPATCH_TRIGGER"
  Event_Classification: "Thermostat Pre-Cooling & Peak Setback"
  Target_Device_Count: 153000
  Target_Zones: ["North Zone", "South Metro", "West Hills", "Central Valley", "East Coastline"]
  Pre_Cooling_Window: "14:00 - 15:45"
  Setback_Delta: "-3.0°F (Pre-Cooling) -> +4.0°F (Peak Event 16:00-19:00)"
  Estimated_Peak_Load_Shed: "191.25 MW"
  Safety_Clamps_Active: true
  Min_Allowable_Temp: "68.0°F"
  Human_Approval_Required: true
  Status: "PENDING_OPERATOR_CONFIRMATION"
```

### Example 2: Trend & Comparative Analysis
**User:** "Model the expected megawatt relief curve and subsequent 'snapback' rebound demand when setback events conclude."

**Agent Response:**
### Executive Summary
**Thermostat demand response (DR) setback events deliver immediate peak curtailment but introduce a pronounced thermal-decay load reduction followed by an uncoordinated post-event "snapback" demand spike.** **Without staggered restoration staging, post-event rebound peaks at +15.4% above uncurtailed baseline load due to synchronized HVAC compressor duty cycles across the enrolled feeder population.** **Implementing a progressive 3-stage random offset restoration window flattens the rebound peak by 68%, maintaining feeder thermal constraints within NERC/utility reliability margins.**

---

### Quantitative Performance & Impact Analysis

The table below outlines the aggregate load metrics across a representative 25,000-device smart thermostat fleet during a 4-hour +3°F (+1.67°C) direct load control setback event (14:00–18:00) and the subsequent recovery window:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Initial Relief Magnitude (T+15m)** | 30.00 MW | 0.00 MW Baseline Delta | -24.00% Net Load | **Normal** |
| **Event Mid-Point Sustained Relief (T+2h)** | 24.20 MW | 28.00 MW Target | -13.57% (Thermal Drift) | **Warning** |
| **End-of-Event Relief (T+4h)** | 18.20 MW | 25.00 MW Target | -27.20% (Saturation) | **Warning** |
| **Unmitigated Post-Event Snapback Peak** | 142.50 MW | 123.50 MW (Coincident Baseline) | +15.38% (Overshoot) | **Critical** |
| **Snapback Duration to Equilibrium** | 105 Minutes | < 45 Minutes Standard | +133.33% | **Warning** |
| **Cumulative Net Energy Avoided** | 98.40 MWh | 105.00 MWh Target | -6.29% | **Normal** |

---

### Analytical Relief & Snapback Mechanics

1. **Relief Degradation (Thermal Drift)**:
   $$\Delta P_{\text{relief}}(t) = P_{\text{shed, initial}} \cdot e^{-\frac{t}{\tau_{\text{envelope}}}} + P_{\text{override}}(t)$$
   As internal building envelope temperatures rise to meet the new target setpoint, HVAC duty cycles gradually resume (cycling back on to maintain the higher limit), resulting in a natural decay of MW relief across the event duration.

2. **Thermostatic Snapback Phenomenon**:
   When the setback trigger releases simultaneously at event conclusion (18:00), 100% of enrolled units detect an immediate negative temperature error ($T_{\text{ambient}} > T_{\text{setpoint}}$), forcing continuous, simultaneous compressor run-cycles.

```
       [ Event Window: 14:00 - 18:00 ]           [ Post-Event Snapback ]
Load   
(MW)
145 |                                              /\  <-- Rebound Spike (142.5 MW)
130 | ---------------- Baseline ------------------/--\-------
115 |        \                                   /    \
100 |         \_______ Relief Profile __________-      \______ (Returns to Normal)
 85 |
     +---------+---------+---------+---------+---------+---------+---------> Time
             14:00     15:00     16:00     17:00     18:00     19:00
```

---

### Actionable Recommendations

- **Deploy Staggered Rebound Release (Ramping Logic)**: Partition the fleet into 4 randomized release cohorts (25% every 15 minutes between 18:00 and 19:00) or command a floating setpoint ramp rate of **0.5°F per 30 minutes** to eliminate the sharp coincident surge.
- **Implement Pre-Cooling Strategy**: Trigger a -2°F pre-cooling sequence 90 minutes prior to event dispatch (12:30–14:00) to flatten building thermal decay and extend sustained relief duration across the peak 4-hour window.
- **Feeder Substation Interlocking**: In the event of high local distribution transformer loading (>90% rated MVA), lock out instantaneous setpoint restoration until local telemetry drops below threshold.

---

### Human-in-the-Loop Tier 2 Operational Notice

```
[TIER 2 ACTION REQUIRED]
-------------------------------------------------------------------------
Operation: Demand Response Automatic Dispatch & Dynamic Ramping Trigger
Target Asset Group: Substation Feeder Bank 12A / 25,000 Smart Thermostats
Action: Authorize modified 4-stage staggered restoration algorithm to 
        mitigate projected 19.0 MW snapback overshoot.
Safety Status: Telemetry and AMI mesh connectivity operational.
Approval Required: Human Grid Dispatcher / Operator Confirmation.
-------------------------------------------------------------------------
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch an automated Tier 2 Demand Response event signal to 45,000 enrolled smart thermostats across Grid Zone 2."

**Agent Response:**
### Executive Summary
**A demand response setback dispatch request has been staged for 45,000 enrolled smart thermostats within Grid Zone 2 targeting an estimated peak load relief of 45.0 MW.** **In compliance with Utility Physical Grid Safety and Tier 2 Operational Guardrails, autonomous execution of load curtailment signals affecting widespread grid zones is prohibited without explicit Human-in-the-Loop (HITL) authorization.** **The event parameters, device telemetry, and communication pathway health have been verified and placed in a pending state awaiting operator sign-off.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Enrolled Thermostat Pool (Zone 2)** | 45,000 devices | 45,000 devices | 0.0% | Normal |
| **AMI/DERMS Connectivity Rate** | 98.4% (44,280 reachable) | ≥ 95.0% | +3.58% | Normal |
| **Target Setback Adjustment** | +2.5°F (Cooling Mode) | +2.0°F to +3.0°F | 0.0% | Normal |
| **Projected Demand Reduction** | 43.8 MW | 45.0 MW Target | -2.67% | Warning |
| **Grid Zone 2 Current Load** | 325.0 MW | 280.0 MW Threshold | +16.07% | Critical |
| **Event Duration** | 120 minutes | 120 minutes max | 0.0% | Normal |

---

### Visualization Triggers
**Recommended Chart Type:** Time-Series Line Chart illustrating projected load curve relief against unmitigated baseline.

```json
{
  "chart_type": "line",
  "title": "Grid Zone 2: Pre- and Post-Event Load Trajectory",
  "xAxis": ["T-60m", "T-30m", "Event Start (T0)", "T+30m", "T+60m", "T+90m", "T+120m (End)", "T+150m (Snapback)"],
  "series": [
    {
      "name": "Baseline Forecast (MW)",
      "data": [310, 318, 325, 330, 332, 328, 320, 312]
    },
    {
      "name": "Projected Curtailed Load (MW)",
      "data": [310, 318, 300, 285, 286, 284, 282, 318]
    }
  ]
}
```

---

### Actionable Recommendations
- **Verify Substation Capacity**: Cross-reference substation loading on Feeders GZ2-F101 through GZ2-F108 to ensure localized relief matches thermal congestion areas.
- **Pre-Cooling Protocol**: Ensure enrolled residential assets receive a standard 30-minute pre-cooling offset prior to trigger initiation if ambient temperatures exceed 95°F.
- **Post-Event Snapback Mitigation**: Stage a staggered 15-minute ramp-down across 4 sub-groups to avoid rebound demand spikes upon event termination.
- **Authorize Dispatch**: Review the staged Tier 2 operational payload below and approve execution via the DERMS / AMI gateway.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "TIER_2_DEMAND_RESPONSE_DISPATCH",
  "status": "PENDING_HUMAN_APPROVAL",
  "grid_zone_id": "GZ-02",
  "target_protocol": "OpenADR 2.0b / AMI Mesh Multicast",
  "device_count": 45000,
  "setback_offset_deg_f": 2.5,
  "duration_minutes": 120,
  "estimated_mw_curtailment": 43.8,
  "staggered_rebound_enabled": true,
  "requires_override_signature": true,
  "operator_prompt": "Please confirm authorization to broadcast a +2.5°F thermostat setback signal to 45,000 smart thermostats in Grid Zone 2."
}
```
