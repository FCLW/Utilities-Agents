# ⚡ Ev Charging Load Spike Predictor

![Domain](https://img.shields.io/badge/Domain-production%20forecasting-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of ev charging load spike predictor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Ev Charging Load Spike Predictor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank ev charging load spike predictor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_production_forecasting.ev_charging_load_spike_predictor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Will fast-charging demand at fleet depot stations create an unmanageable evening distribution peak between 18:00 and 21:00?"

**Agent Response:**
### 1. Executive Summary
**Uncontrolled fast-charging demand at fleet depot stations between 18:00 and 21:00 will create a critical distribution overload exceeding feeder continuous ratings by up to 17.1% and breaching emergency thermal limits at peak hour (19:00). Without active managed charging (smart sequencing or local Battery Energy Storage System dispatch), the coincidence of residential evening ramp with commercial fleet plug-in creates an unmanageable peak spike reaching 41.0 MW against a 35.0 MW normal feeder rating. Immediate mitigation through automated managed charging (V1G) curtailment and peak-shaving dispatch is required to maintain system reliability within NERC/IEEE standards.**

---

### 2. Quantitative Assessment & Loading Analysis

| Metric | Current Forecast Peak (19:00) | Baseline / Target Rating | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Fleet Depot EV Charging Demand** | 14.20 MW | 4.50 MW (Target Managed) | +215.6% | **Critical** |
| **Feeder Aggregate Load** | 41.00 MW | 35.00 MW (Continuous Limit) | +17.1% | **Critical** |
| **Feeder Emergency Thermal Limit** | 41.00 MW | 40.00 MW (STE Limit) | +2.5% | **Critical** |
| **Peak Substation Transformer Loading** | 108.4% | 85.0% (Operational Limit) | +23.4% | **Critical** |
| **Distribution Feeder Voltage Drop** | 0.928 p.u. | 0.950 p.u. (ANSI C84.1 Min) | -2.3% | **Warning** |
| **Forecast Mean Absolute Percentage Error (MAPE)** | 3.42% | < 5.00% (Target) | -1.58% | **Normal** |
| **95% Confidence Interval Peak Band** | 39.4 MW – 42.6 MW | ≤ 35.0 MW | +12.6% to +21.7% | **Critical** |

---

### 3. Visualization Configuration

```json
{
  "chart_type": "line",
  "title": "Evening Feeder Load Profile vs. Fleet EV Charging (16:00 - 23:00)",
  "labels": ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00"],
  "datasets": [
    {
      "name": "Baseline Non-EV Load (MW)",
      "data": [18.2, 21.5, 25.1, 26.8, 26.2, 23.4, 20.1, 17.5]
    },
    {
      "name": "Fleet Depot Fast-Charging Load (MW)",
      "data": [3.4, 6.8, 12.5, 14.2, 13.1, 9.8, 5.2, 2.1]
    },
    {
      "name": "Total Aggregate Load (MW)",
      "data": [21.6, 28.3, 37.6, 41.0, 39.3, 33.2, 25.3, 19.6]
    },
    {
      "name": "Feeder Normal Rating (MW)",
      "data": [35.0, 35.0, 35.0, 35.0, 35.0, 35.0, 35.0, 35.0]
    },
    {
      "name": "Feeder Emergency Thermal Limit (MW)",
      "data": [40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0, 40.0]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Implement Managed Charging Sequencing (V1G)**: Throttle fleet DC fast chargers (DCFC) to a maximum aggregated ceiling of 5.5 MW during the 18:00–21:00 window, shifting bulk fleet replenishment cycles to the off-peak overnight block (23:00–05:00).
- **Dispatch Co-located Fleet Energy Storage (BESS)**: Signal on-site 4 MW / 16 MWh storage assets at the depot interconnect to discharge at full capacity between 18:00 and 21:00, capping net feeder export demand.
- **Dynamic Capacity Allocation**: Trigger time-of-use or automated demand response (ADR) pricing/curtailment signals via OpenADR 2.0b protocols to depot energy management systems (EMS).
- **Substation Load Tap Changer (LTC) & Capacitor Optimization**: Pre-stage voltage regulation assets by 17:30 to mitigate projected ANSI C84.1 voltage sag below 0.93 p.u.

---

### 5. Tier 2 Human-in-the-Loop Notification

```text
[TIER 2 ACTION REQUIRED]
- Action Type: Fleet Depot Interconnection Curtailment & Demand Response Trigger
- Affected Feeders: Feeder-04B / Substation-12 (North Industrial Zone)
- Execution Window: 18:00 - 21:00
- Proposed Command: Throttle aggregate fleet fast-charging capacity from 14.2 MW to 5.5 MW (61.3% curtailment) and initiate 4.0 MW BESS local discharge.
- Risk Analysis: Prevents feeder thermal excursion >117% and avoiding transformer protection trip.
- Approval Required: Distribution Grid Operator / Transmission Operations Task Lead
```

### Example 2: Trend & Comparative Analysis
**User:** "Model the coincidence factor of 10,000 residential EV owners plugging in simultaneously upon arriving home from work."

**Agent Response:**
### Executive Summary
**A simultaneous unmanaged plug-in event of 10,000 residential electric vehicles (EVs) at 7.2 kW Level 2 capacity creates a peak coincidence factor of 0.65, injecting an instantaneous demand spike of 46.8 MW into the distribution network between 18:30 and 19:30.** **This acute coincidence coincides directly with the base residential evening peak, risking severe thermal overloading on local substation transformers and secondary feeder lines.** **Implementing randomized algorithmic charging dispatch mitigates peak coincidence to 0.23 (16.5 MW), reducing asset stress by 64.7% without compromising next-day range requirements.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Connected Fleet Nameplate Capacity** | 72.0 MW (10,000 × 7.2 kW) | 72.0 MW | 0.0% | Normal |
| **Unmanaged Peak Coincidence Factor ($CF_{peak}$)** | 0.65 (65% concurrent) | 0.20 (Managed Target) | +225.0% | **Critical** |
| **Aggregate EV Peak Load Spike (Unmanaged)** | 46.8 MW (at 19:00) | 14.4 MW (Grid Target) | +225.0% | **Critical** |
| **Timer-Cliff Spike (Un-randomized TOU at 21:00)** | 57.6 MW ($CF = 0.80$) | 14.4 MW (Grid Target) | +300.0% | **Critical** |
| **Managed Peak Coincidence Factor ($CF_{opt}$)** | 0.23 (Randomized delay) | 0.20 (Target) | +15.0% | Normal |
| **Distribution Transformer Loading Utilization** | 128.4% of Rated MVA | < 90.0% MVA Rating | +42.7% | **Critical** |
| **Feeder Voltage Drop ($\Delta V$) at Terminal Nodes** | -6.8% ($0.932\text{ p.u.}$) | $\pm 5.0\%$ (ANSI C84.1 Range A) | -36.0% | **Warning** |

*Assumptions: Standard 7.2 kW Level 2 (240V, 30A), commuter arrival distribution $\mathcal{N}(\mu=18:15, \sigma=45\text{ min})$, average daily recharge energy demand = $21.6\text{ kWh}$ ($3.0\text{ hours}$ duration per vehicle).*

---

### Visualization Triggers
- **Recommended Chart**: Multi-Series Time-Series Line Chart (Coincidence Factor & MW Load vs. Time of Day).

```json
{
  "title": "10,000 Residential EV Unmanaged vs. Managed Charging Load Profile (16:00 - 02:00)",
  "chart_type": "line",
  "xAxis": {
    "name": "Time of Day",
    "categories": ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00", "01:00", "02:00"]
  },
  "yAxis": {
    "name": "Aggregate Load (MW)"
  },
  "series": [
    {
      "name": "Unmanaged Evening Plug-in (MW)",
      "data": [3.6, 14.4, 36.0, 46.8, 39.6, 25.2, 12.6, 5.4, 2.2, 0.7, 0.0]
    },
    {
      "name": "Un-randomized TOU Timer Spike (MW)",
      "data": [1.4, 3.6, 7.2, 7.2, 10.8, 57.6, 43.2, 21.6, 7.2, 2.2, 0.0]
    },
    {
      "name": "Optimized Staggered / Smart Charging (MW)",
      "data": [3.6, 7.2, 12.0, 15.8, 16.5, 16.2, 15.5, 14.4, 13.0, 9.5, 4.0]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Deploy Distributed Randomized Delay Algorithm (RDA)**:
   - Configure utility-connected smart EVSEs (OCPP 1.6J/2.0.1) to inject a randomized start-time offset ($\Delta t \in [0, 120]\text{ minutes}$) upon TOU rate triggers to avoid secondary timer cliff spikes.
2. **Dynamic Feeder Headroom Curtailment**:
   - Establish automated local DERMS/ADMS setpoint modulation that throttles charging rates from 7.2 kW down to 3.6 kW (16A) per vehicle when distribution substation transformer thermal capacity reaches 85%.
3. **Targeted Feeder Reinforcement & Phase Balancing**:
   - Audit cluster distributions on residential feeders with high EV penetration to balance single-phase Level 2 connections across phases A, B, and C, preventing neutral conductor overcurrent and voltage unbalance (> 2%).
4. **Demand Response Event Signal Staging**:
   - In the event of system peak alerts, stage localized EV flex-demand curtailment signals to pre-emptively shift ~30 MW of flexible demand into off-peak valley hours (00:00 - 05:00).

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Trigger an automated off-peak charging price signal and demand response advisory to enrolled EV fleet operators."

**Agent Response:**
### 1. Executive Summary
**A major EV charging load spike is forecasted across Substation Clusters North-4 and Metro-East between 17:00 and 21:00 UTC, projected to exceed feeder capacity thresholds by up to +75.4%. To mitigate localized distribution transformer overloading and maintain NERC/FERC reliability margins, an off-peak dynamic pricing incentive coupled with an automated Demand Response (DR) advisory has been prepared. Because dispatching dynamic price signals and broadcasting mass DR events to external commercial fleet operators constitutes a Tier 2 operation, this action requires explicit Human-In-The-Loop (HITL) authorization prior to execution.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Peak EV Load Forecast (18:00–20:00)** | 34.20 MW | 19.50 MW | +75.38% | **Critical** |
| **Target Feeder Capacity Utilization** | 94.80% | 75.00% | +26.40% | **Critical** |
| **Forecast Model MAPE (Last 24h)** | 3.12% | < 5.00% | -37.60% | **Normal** |
| **Enrolled Fleet Shiftable Capacity** | 12.80 MW | 10.00 MW | +28.00% | **Normal** |
| **Off-Peak Incentive Shift Potential** | 8.50 MW | 6.00 MW | +41.67% | **Normal** |

---

### 3. Visualization Triggers
**Recommended Chart**: Time-Series Line Chart (Hourly Load Forecast vs. Baseline & Shift Target)

```json
{
  "chart_type": "line",
  "title": "EV Charging Load Spike & DR Shift Profile",
  "xAxis": {
    "title": "Time Interval (UTC)",
    "categories": ["16:00", "17:00", "18:00", "19:00", "20:00", "21:00", "22:00", "23:00", "00:00"]
  },
  "yAxis": {
    "title": "Megawatts (MW)"
  },
  "series": [
    {
      "name": "Baseline EV Load (MW)",
      "data": [12.4, 15.1, 18.2, 19.5, 17.0, 14.2, 10.5, 8.1, 6.0]
    },
    {
      "name": "Predicted Peak Load Spike (MW)",
      "data": [14.0, 22.8, 31.5, 34.2, 28.6, 21.0, 12.0, 8.5, 6.1]
    },
    {
      "name": "Post-Advisory Target Load (MW)",
      "data": [13.0, 16.5, 19.0, 20.0, 18.0, 15.0, 12.5, 11.0, 9.5]
    }
  ]
}
```

---

### 4. Actionable Recommendations
- **Approve Tier 2 Demand Response Dispatch**: Confirm the outbound dispatch payload to transmit dynamic off-peak tariff signals ($0.06/kWh off-peak credit vs. $0.38/kWh on-peak surcharge) to registered Commercial & Industrial (C&I) EV fleet aggregators.
- **Feeder-Level Rebalancing**: Instruct Grid Operations to monitor Feeder 14-B and Feeder 22-A closely during the ramp period (17:00–18:30 UTC).
- **Post-Event Model Verification**: Compare telemetry metering logs at 22:00 UTC against the 95% Confidence Interval bounds to assess fleet compliance rate and load drop fidelity.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "DISPATCH_DEMAND_RESPONSE_PRICING_ADVISORY",
  "agent": "ev_charging_load_spike_predictor",
  "target_entities": [
    "EV_FLEET_AGGREGATOR_GROUP_A",
    "METRO_DEPOT_CHARGING_HUBS"
  ],
  "grid_zones": ["ZONE-NORTH-4", "ZONE-METRO-EAST"],
  "event_window": {
    "start_utc": "2025-01-15T17:00:00Z",
    "end_utc": "2025-01-15T21:00:00Z"
  },
  "price_signal": {
    "rate_structure": "CRITICAL_PEAK_OFF_PEAK_REBATE",
    "peak_curtailment_incentive_mwh": 140.00,
    "off_peak_shift_credit_mwh": 60.00
  },
  "expected_load_shed_mw": 11.4,
  "requires_operator_approval": true,
  "status": "AWAITING_HUMAN_CONFIRMATION"
}
```
