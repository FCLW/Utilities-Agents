# ⚡ Appliance Disaggregation Efficiency Advisor

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of appliance disaggregation efficiency advisor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Appliance Disaggregation Efficiency Advisor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank appliance disaggregation efficiency advisor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.appliance_disaggregation_efficiency_advisor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can you break down my monthly 1,450 kWh electric bill into heating, cooling, refrigeration, and EV charging categories?"

**Agent Response:**
### Executive Summary
**Exact Non-Intrusive Load Monitoring (NILM) disaggregation requires high-resolution Advanced Metering Infrastructure (AMI) interval data, which currently shows INSUFFICIENT DATA for customer-specific meter telemetry. Based on standard utility engineering end-use benchmarks (EIA RECS / EPRI load profiles) for a 1,450 kWh monthly profile with an active Electric Vehicle (EV), space conditioning (HVAC) and EV charging account for ~62% of total consumption. Baseline disaggregation indicates refrigeration operates within standard nominal parameters (~115 kWh), while seasonal HVAC and EV charging drive peak consumption.**

---

### Data Presentation: Appliance End-Use Disaggregation Baseline

The following decomposition represents estimated category allocation for a monthly total of 1,450 kWh based on standard residential customer load profiles and regional degree-day modeling:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Monthly Load** | 1,450 kWh | 1,200 kWh | +20.8% | Warning |
| **Space Conditioning (Heating/Cooling)** | 520 kWh (35.9%) | 420 kWh | +23.8% | Warning |
| **Electric Vehicle (EV Charging)** | 380 kWh (26.2%) | 350 kWh | +8.6% | Normal |
| **Refrigeration & Freezers** | 115 kWh (7.9%) | 120 kWh | -4.2% | Normal |
| **Water Heating & Heavy Appliances** | 260 kWh (17.9%) | 200 kWh | +30.0% | Warning |
| **Lighting & Always-On Baseload (Plug Loads)** | 175 kWh (12.1%) | 110 kWh | +59.1% | Warning |

*Analytical Assumptions: Baseline targets reflect an electrified single-family home with standard Level-2 EV charging (~1,000 miles/month @ 3.5 mi/kWh) and climate-adjusted heat pump/AC operation.*

---

### Visualization Triggers

**Recommended Visualization**: Category Contribution Breakdown (Bar Chart / End-Use Load Profile)

```json
{
  "chart_type": "bar",
  "data": {
    "categories": [
      "Heating & Cooling (HVAC)",
      "EV Charging (Level 2)",
      "Water Heating & Baseload",
      "Lighting & Plug Loads",
      "Refrigeration"
    ],
    "consumption_kwh": [520, 380, 260, 175, 115],
    "share_percentage": [35.9, 26.2, 17.9, 12.1, 7.9]
  },
  "metadata": {
    "total_kwh": 1450,
    "unit": "kWh",
    "disaggregation_method": "NILM Baseline Benchmark"
  }
}
```

---

### Actionable Recommendations

- **Ingest Meter Interval Telemetry**: Connect 15-minute or 60-minute AMI telemetry stream to replace estimated benchmarks with exact signature-based NILM machine learning decomposition.
- **EV Time-of-Use (TOU) Optimization**: Shift the 380 kWh EV charging demand window to off-peak utility hours (typically 11:00 PM – 6:00 AM) to capture reduced off-peak rate tiers.
- **HVAC Setpoint & Smart Thermostat Advisory**: Evaluate smart thermostat schedules to reduce HVAC consumption (520 kWh) during peak load events, targeting a 10–15% efficiency reduction.
- **Phantom Load Audit**: Investigate secondary baseload and plug load draw (175 kWh), focusing on unmanaged consumer electronics and standby power consumption.

### Example 2: Trend & Comparative Analysis
**User:** "Compare this household's HVAC runtime and baseload phantom power draw against similar homes in the neighborhood."

**Agent Response:**
### Executive Summary
**Non-Intrusive Load Monitoring (NILM) disaggregation reveals that this household operates with significantly elevated HVAC runtime (+54.1%) and excessive baseload phantom power draw (+131.0%) compared to weather-normalized neighborhood peers.** **The household draws approximately 485 W in continuous parasitic/standby load and experiences 9.4 hours of active HVAC compressor cycling per day, indicating poor thermal envelope retention, potential short-cycling, or malfunctioning standby electronics.** **Targeted behavioral and automated demand-side efficiency interventions can recover an estimated 280–350 kWh per month in preventable energy loss.**

---

### Disaggregated Appliance & Baseload Benchmark Analysis

| Metric | Current Value | Baseline / Target (Peer Avg) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **HVAC Daily Runtime** | 9.40 hrs/day | 6.10 hrs/day | +54.10% | **Warning** |
| **HVAC Cycling Frequency** | 4.20 cycles/hr | 2.10 cycles/hr | +100.00% | **Warning** |
| **Continuous Baseload (Phantom Load)** | 485 W | 210 W | +130.95% | **Critical** |
| **Baseload Daily Consumption** | 11.64 kWh/day | 5.04 kWh/day | +130.95% | **Critical** |
| **HVAC Estimated Daily Energy** | 28.20 kWh/day | 18.30 kWh/day | +54.10% | **Warning** |
| **Annualized Excess Cost Impact** | $584.20 / yr | $0.00 (Peer Baseline) | N/A | **Warning** |

*Note: Baseline is calibrated against 120 thermally matched peer homes within the same distribution feeder zone under identical degree-day (CDD/HDD) weather conditions.*

---

### Visualization Configuration

```json
{
  "chart_type": "bar",
  "title": "Household Disaggregation vs. Neighborhood Peer Benchmark",
  "categories": [
    "HVAC Daily Runtime (hrs)",
    "HVAC Cycling Rate (cycles/hr)",
    "Baseload Phantom Power (W / 10)",
    "Baseload Daily Energy (kWh)"
  ],
  "series": [
    {
      "name": "Target Household",
      "data": [9.4, 4.2, 48.5, 11.64]
    },
    {
      "name": "Neighborhood Peer Baseline",
      "data": [6.1, 2.1, 21.0, 5.04]
    }
  ]
}
```

---

### Actionable Recommendations

- **Smart Thermostat & Short-Cycling Diagnostics**:
  - Deploy an automated diagnostic test on the HVAC system to evaluate compressor short-cycling (currently 4.2 cycles/hr vs. 2.1 standard), which indicates possible refrigerant under-charge, dirty filter/coil restriction, or oversized tonnage.
  - Recommend adjusting minimum compressor runtime settings and deadband parameters via smart thermostat integration.
- **Parasitic / Standby Power Mitigation**:
  - Dispatch a personalized Home Energy Report (HER) identifying high always-on baseload (485 W continuous), pinpointing common culprits (unmanaged media centers, secondary refrigeration, pool pump timers, or recirculating domestic hot water pumps).
  - Enroll customer in a Smart Strip / Home Energy Management System (HEMS) rebate program.
- **Customer Omnichannel Triage & Engagement**:
  - Route efficiency insights to the customer portal and utility mobile app with estimated bill savings of ~$48.60/month upon achieving peer parity.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Dispatch a personalized Home Energy Audit report with tailored heat pump rebate incentives to Customer #10294."

**Agent Response:**
### Executive Summary
**Appliance disaggregation telemetry for Customer #10294 reveals legacy resistive heating and cooling systems account for 47.6% of total annual consumption (6,850 kWh/yr), presenting a prime conversion opportunity.** **Deploying an ENERGY STAR® Cold-Climate Heat Pump with Hybrid Water Heating is modeled to reduce net household consumption by 4,770 kWh/yr (-33.1%), saving an estimated $858 annually.** **A personalized Home Energy Audit report with an eligible utility rebate package of up to $2,500 has been compiled for targeted dispatch.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **HVAC Annual Load** | 6,850 kWh | 3,750 kWh | +82.7% | Critical |
| **Water Heating Load** | 3,120 kWh | 1,450 kWh | +115.2% | Warning |
| **Baseload (Plug/Lighting)** | 3,000 kWh | 3,000 kWh | 0.0% | Normal |
| **Total Annual Consumption** | 14,400 kWh | 9,630 kWh | +49.5% | Warning |
| **Estimated Annual Energy Bill** | $2,592 | $1,734 | +49.5% | Warning |
| **Available Heat Pump Rebate** | $2,500 (Tier 3) | $0 (Standard) | N/A | Normal |

---

### Visualization Triggers
**Recommended Visualization**: Grouped Bar Chart comparing current disaggregated appliance loads against post-heat pump retrofit target loads.

```json
{
  "chart_type": "bar",
  "title": "Customer #10294: Disaggregated Energy Consumption vs. Heat Pump Post-Retrofit Target",
  "data": {
    "categories": [
      "HVAC (Space Heating/Cooling)",
      "Water Heating",
      "Refrigeration",
      "Lighting & Plug Loads",
      "Major Appliances"
    ],
    "series": [
      {
        "name": "Current Annual (kWh)",
        "values": [6850, 3120, 1150, 1850, 1430]
      },
      {
        "name": "Post-Heat Pump Target (kWh)",
        "values": [3750, 1450, 1150, 1850, 1430]
      }
    ]
  },
  "unit": "kWh/year"
}
```

---

### Actionable Recommendations
- **Deliver Personalized Report**: Transmit the generated Home Energy Audit detailing the seasonal disaggregation breakdown and 3-year payback horizon.
- **Pre-Approve Incentive Package**: Apply the $2,000 Heat Pump HVAC Rebate (Program Code: `HP-RES-2024`) and $500 Heat Pump Water Heater Rebate (Program Code: `HPWH-500`).
- **Omnichannel Triage**: Queue outbound email dispatch with SMS follow-up alert, providing a 1-click link to certified local installation contractors.
- **Demand Response (DR) Program Enrollment**: Bundle an optional pre-enrollment offer for the Connected Thermostat Peak Savings Program upon equipment commissioning.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CUSTOMER_OUTBOUND_DISPATCH",
  "target_customer_id": "10294",
  "document_type": "Home_Energy_Audit_Report",
  "incentive_payload": {
    "program_id": "ENERGY_EFF_REBATE_2024",
    "rebate_amount_usd": 2500.00,
    "eligible_measures": [
      "Cold-Climate Air-Source Heat Pump (SEER2 >= 16, HSPF2 >= 9.0)",
      "Hybrid Electric Heat Pump Water Heater (UEF >= 3.3)"
    ]
  },
  "dispatch_channel": "EMAIL_AND_CUSTOMER_PORTAL",
  "approval_status": "PENDING_HUMAN_CONFIRMATION",
  "compliance_check": "PUC_RESIDENTIAL_COMMUNICATION_PASSED"
}
```
