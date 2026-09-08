# ⚡ Solar Panel Installation Advisor

![Domain](https://img.shields.io/badge/Domain-customer%20engagement-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of solar panel installation advisor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Solar Panel Installation Advisor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank solar panel installation advisor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_customer_engagement.solar_panel_installation_advisor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can you estimate the solar generation potential and payback period for a 2,200 sq ft residential rooftop in Zip Code 94107?"

**Agent Response:**
### 1. Executive Summary
**A 2,200 sq ft residential rooftop in Zip Code 94107 (San Francisco, CA) provides an estimated technical generation capacity of 8.80 kW DC, yielding approximately 13,094 kWh of clean electricity annually under local solar irradiance conditions (5.1 Peak Sun Hours/day). With a net turnkey installation cost of $17,556 (reflecting the 30% Federal Section 25D Investment Tax Credit), the project demonstrates robust economics with an estimated simple payback period of 4.56 years against regional Tier 1/TOU electric utility tariffs. Over a 25-year operational lifecycle, the system delivers an estimated Levelized Cost of Energy (LCOE) of $0.072/kWh compared to the prevailing utility grid baseline of $0.360/kWh.**

---

### 2. Data Presentation

**Analytical Assumptions**:
- **Usable Solar Area**: 1,320 sq ft (~60% of total roof footprint to accommodate fire setbacks, vents, and shading).
- **Module Rating**: 400W Monocrystalline PV Modules (22 panels total).
- **Inverter & System Derate Factor**: 0.80 (accounting for DC-to-AC conversion, thermal losses, soiling, and wiring).
- **Utility Tariff Benchmark**: $0.360/kWh baseline blended TOU rate with an annual utility inflation rate of 3.0%.
- **Incentive Framework**: 30% Federal Residential Clean Energy Credit (ITC).

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Usable Rooftop Area** | 1,320 sq ft | 2,200 sq ft (Total) | -40.0% | Normal |
| **System DC Nameplate Capacity** | 8.80 kW DC | 8.00 kW DC | +10.0% | Normal |
| **Annual Generation Potential (Year 1)** | 13,094 kWh | 10,500 kWh (Avg SF Usage) | +24.7% | Normal |
| **Gross Installation Cost ($2.85/W)** | $25,080 | $28,000 (Market Avg) | -10.4% | Normal |
| **Federal ITC Tax Credit (30%)** | -$7,524 | $0 | N/A | Normal |
| **Net Capital Expenditure** | $17,556 | $25,080 | -30.0% | Normal |
| **Annual Electricity Bill Savings** | $3,850 / year | $0 / year | N/A | Normal |
| **Estimated Simple Payback Period** | 4.56 Years | 7.00 Years | -34.9% | Normal |
| **25-Year Levelized Cost of Energy (LCOE)**| $0.072 / kWh | $0.360 / kWh (Grid Rate) | -80.0% | Normal |

---

### 3. Visualization Triggers

**Recommended Visualization**: **Cumulative Net Cash Flow & Break-Even Trajectory (15-Year Time-Series Line Chart)**.  
This visualization illustrates the initial capital investment breakeven milestone occurring midway through Year 5, transitioning into sustained cumulative positive net returns.

```json
{
  "chart_type": "line",
  "title": "Cumulative Net Cash Flow & Payback Trajectory (94107)",
  "xAxis": {
    "type": "category",
    "data": ["Year 0", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6", "Year 7", "Year 8", "Year 9", "Year 10", "Year 12", "Year 15"]
  },
  "yAxis": {
    "type": "value",
    "name": "Cumulative Net Position ($)"
  },
  "series": [
    {
      "name": "Net Cumulative Savings",
      "data": [-17556, -13706, -9775, -5762, -1665, 2514, 6777, 11126, 15562, 20087, 24703, 34215, 49102],
      "type": "line"
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Site & Shading Survey**: Conduct a detailed LiDAR/drone shading analysis and structural roof integrity inspection prior to final engineering approval.
- **Interconnection & Net Billing Tariff (NEM 3.0 / Solar Billing)**: Evaluate paired Battery Energy Storage System (BESS) sizing (e.g., 10–13.5 kWh) to maximize self-consumption and capture peak-period TOU export credits.
- **Permitting & Utility Interconnection**: Coordinate with the local Authority Having Jurisdiction (AHJ) for Rule 21 simplified interconnection and building/electrical permits.
- **Contractor Procurement**: Request three competitive, itemized bids adhering to NABCEP standards to verify local balance-of-system (BOS) pricing.

### Example 2: Trend & Comparative Analysis
**User:** "Compare the annual kWh yield of a south-facing 8 kW system with battery storage versus a standalone solar array."

**Agent Response:**
### Executive Summary
**A south-facing 8.0 kW DC standalone solar array generates an estimated net annual yield of 11,600 kWh AC under standard utility irradiance assumptions (1,450 kWh/kWp specific yield). Integrating an energy storage system (e.g., 10–13.5 kWh battery) reduces the net delivered annual AC volume by approximately 4.1% (to ~11,120 kWh AC) due to storage round-trip efficiency (RTE) and inverter conversion losses. However, the solar-plus-storage configuration substantially enhances economic utility value by shifting off-peak daytime production into high-value on-peak billing windows and providing local grid resilience.**

---

### Data Presentation

The table below benchmarks the operational performance parameters between a baseline Standalone PV Array (8 kW DC, Azimuth 180°, 25°–30° Tilt) and an identical 8 kW DC PV Array coupled with an AC/DC Battery Storage System (13.5 kWh, 88% Round-Trip Efficiency, ~3,800–4,000 kWh annual cycling).

| Metric | Current Value (Solar + Battery) | Baseline / Target (Standalone PV) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Gross PV DC Output** | 13,488 kWh/yr | 13,488 kWh/yr | 0.00% | Normal |
| **Standard Balance-of-System (BOS) Losses** | 14.00% (Thermal, Soiling, Wiring) | 14.00% (Thermal, Soiling, Wiring) | 0.00% | Normal |
| **Inverter Efficiency Rating** | 97.00% | 97.00% | 0.00% | Normal |
| **Storage Round-Trip Efficiency (RTE)** | 88.00% | N/A (100% direct grid/load path) | -12.00% | Warning |
| **Annual Storage Conversion Losses** | 480 kWh/yr | 0 kWh/yr | N/A | Normal |
| **Total Net Usable AC Yield** | **11,120 kWh/yr** | **11,600 kWh/yr** | **-4.14%** | Normal |
| **Direct Self-Consumption Rate** | ~72.00% | ~32.00% | +125.00% | Normal |
| **Grid Export Ratio** | ~28.00% | ~68.00% | -58.82% | Normal |

*Analytical Assumptions: Standard Test Conditions (STC) derate factor of 0.86, southern orientation (180° azimuth), average 4.8 Peak Sun Hours (PSH)/day, time-of-use (TOU) arbitrage cycling profile.*

---

### Visualization Triggers

**Recommended Chart Type:** Dual-Dataset Grouped Bar Chart (Monthly Usable AC Generation Profile)

```json
{
  "chart_type": "bar",
  "title": "Monthly Usable AC Generation: Standalone Solar vs. Solar + Battery (8 kW DC System)",
  "x_axis_label": "Billing Month",
  "y_axis_label": "Net Energy Yield (kWh)",
  "labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  "datasets": [
    {
      "name": "Standalone Solar AC Yield (kWh)",
      "data": [620, 740, 980, 1150, 1280, 1310, 1300, 1220, 1050, 880, 610, 460]
    },
    {
      "name": "Solar + Battery Net Usable Yield (kWh)",
      "data": [595, 710, 940, 1102, 1226, 1255, 1245, 1169, 1006, 843, 585, 444]
    }
  ]
}
```

---

### Actionable Recommendations

- **Tariff & Net Energy Metering (NEM) Evaluation**: Under traditional flat 1:1 Net Metering (NEM 1.0/2.0), deploy standalone PV for maximum raw kWh throughput and lowest Levelized Cost of Energy (LCOE). Under avoided-cost export structures (e.g., NEM 3.0 or extreme TOU spreads), configure solar-plus-storage to capture on-peak premium dispatch despite the 4.1% RTE thermodynamic loss.
- **Inverter Architecture Selection**: Specify DC-coupled hybrid inverters over AC-coupled retrofits where possible to improve solar-to-battery charging efficiency by 2.5% to 4.0%, mitigating conversion loss.
- **Interconnection & Feeder Capacity Check**: Review local substation feeder hosting capacity to determine whether battery peak shaving can circumvent dynamic grid export limits or anti-islanding constraints.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate a pre-interconnection feasibility score and dispatch the solar customer application packet to the homeowner."

**Agent Response:**
### Executive Summary
**The preliminary technical screening yields a Pre-Interconnection Feasibility Score of 88/100, placing the requested residential solar system in the Fast-Track interconnection tier.** **Local distribution feeder hosting capacity and service transformer headroom are within compliant thermal and voltage thresholds under IEEE 1547 and Rule 21 standards.** **Dispatching the formal customer application packet requires Human-in-the-Loop (HITL) authorization prior to outbound transmission.**

---

### Pre-Interconnection Feasibility Assessment

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Feeder Hosting Capacity Margin** | 3.42 MW Available | ≥ 1.50 MW | +128.0% | Normal |
| **Transformer Thermal Headroom** | 42.5 kVA | ≥ 25.0 kVA | +70.0% | Normal |
| **Steady-State Voltage Impact ($\Delta V$)** | 1.15% | ≤ 2.50% | -54.0% | Normal |
| **Reverse Power Flow Risk** | 8.2% of Feeder Minimum Load | ≤ 15.0% | -45.3% | Normal |
| **Composite Feasibility Score** | **88 / 100** | ≥ 75 / 100 | +17.3% | **Normal (Eligible for Fast-Track)** |

---

### Visualization Triggers

- **Recommended Visualization**: Feasibility Component Breakdown (Bar Chart) illustrating individual dimensional scores across key engineering and grid constraints.

```json
{
  "chart_type": "bar",
  "title": "Solar Pre-Interconnection Feasibility Component Breakdown",
  "categories": [
    "Hosting Capacity Margin",
    "Transformer Headroom",
    "Voltage Stability",
    "Protection Coordination",
    "Feeder Peak Offset"
  ],
  "series": [
    {
      "name": "Score Contribution (Max 20 pts)",
      "data": [18, 17, 19, 16, 18]
    }
  ]
}
```

---

### Actionable Recommendations

- **Fast-Track Routing**: Assign application to Streamlined Tier 1 Interconnection Workflow based on composite score > 75 and absence of thermal violations.
- **Inverter Smart Settings**: Require UL 1741-SB / IEEE 1547-2018 compliant default Volt-VAR curves to maintain localized voltage profile stability.
- **Contract Validation**: Verify meter configuration (bi-directional Net Energy Metering setup required prior to Permission to Operate).

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "CUSTOMER_APPLICATION_PACKET_DISPATCH",
  "target_program": "Residential Solar Fast-Track Interconnection",
  "feasibility_score": 88,
  "dispatch_channel": "Secure Omnichannel Portal / Automated Email",
  "documents_included": [
    "Standardized_Interconnection_Agreement_Form.pdf",
    "Technical_Screening_Summary_Report.pdf",
    "NEM_Tariff_Schedule_Information.pdf"
  ],
  "approval_status": "PENDING_OPERATOR_CONFIRMATION",
  "compliance_audit_logged": true
}
```

*Operator confirmation is required to release and dispatch the legal Interconnection Application Packet to the customer.*
