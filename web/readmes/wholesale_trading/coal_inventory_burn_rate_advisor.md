# ⚡ Coal Inventory Burn Rate Advisor

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of coal inventory burn rate advisor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Coal Inventory Burn Rate Advisor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank coal inventory burn rate advisor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.coal_inventory_burn_rate_advisor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How many days of full-load coal burn inventory remain in the stockpile at Mohave Generating Station based on current rail deliveries?"

**Agent Response:**
### Executive Summary
**Mohave Generating Station is permanently decommissioned and dismantled, resulting in an active coal inventory stockpile of 0 tons and 0 remaining days of full-load burn capacity.** **Additionally, enterprise fuel telemetry confirms no active rail delivery contracts or scheduled receipts for this retired asset.** **Consequently, fuel inventory metrics reflect INSUFFICIENT DATA / Retired Asset status with zero generation availability.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Active Stockpile Level** | 0 Tons | N/A (Decommissioned) | 0.0% | Normal (Retired) |
| **Daily Full-Load Burn Rate** | 0 Tons/day | 0 Tons/day | 0.0% | Normal (Retired) |
| **Active Rail Delivery Inflow** | 0 Tons/day | 0 Tons/day | 0.0% | Normal (Retired) |
| **Days of Full-Load Inventory** | 0 Days | N/A | 0.0% | Normal (Retired) |
| **Active Asset Operational Status** | Decommissioned | Active Fleet | -100.0% | Warning |

*Note: Telemetry queries confirm no active rail delivery streams or stockpile sensors. Pursuant to regulatory and safety standards, decommissioned assets are flagged as non-operational.*

---

### Visualization Triggers

- **Recommended Chart Type**: Single-Series Bar Chart / Asset Status Gauge
- **Chart Configuration Data (JSON)**:
```json
{
  "chart_type": "bar",
  "title": "Mohave Generating Station - Coal Inventory & Burn Parameters",
  "data": {
    "categories": [
      "Current Stockpile (Tons)",
      "Daily Full-Load Burn (Tons/Day)",
      "Rail Deliveries (Tons/Day)",
      "Days of Inventory Remaining"
    ],
    "series": [
      {
        "name": "Mohave Generating Station",
        "values": [0, 0, 0, 0]
      }
    ]
  },
  "status": "ASSET_DECOMMISSIONED"
}
```

---

### Actionable Recommendations

- **Asset Registry Verification**: Confirm the target generating station identifier with the Master Orchestrator to ensure the query was not intended for an active operating coal asset (e.g., Four Corners, Coronado, or Springerville).
- **Trading Portfolio Exclusion**: Verify that Mohave Generating Station remains excluded from active day-ahead LMP bidding, thermal unit commitment stacks, and wholesale replacement reserve models.
- **Data Pipeline Audit**: Ensure downstream automated fuel inventory telemetry models do not generate false supply alarms for retired generation facilities.

### Example 2: Trend & Comparative Analysis
**User:** "Model coal rail delivery cycle times, stockpile coal density, and forecasted generation run-hours over the winter quarter."

**Agent Response:**
### Executive Summary
**Winter quarter peak generation forecasts indicate an aggregate burn requirement of 672.5 ktons against scheduled rail deliveries of 500.0 ktons, resulting in a net stockpile draw of 172.5 ktons.** **Rail cycle turnaround times are projected to expand by +28.6% from 14.0 to 18.0 days due to winter corridor congestion and weather-related switching delays.** **Under projected peak dark-spread dispatch, site inventory reaches a minimum reserve depth of 15.9 Days of Burn (DOB) in late January, breaching the 20.0 DOB operational safety threshold and requiring immediate train set acceleration or market re-bidding adjustments.**

---

### Key Operational Metrics & Model Parameters

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Rail Delivery Turnaround Cycle** | 18.0 days / train set | 14.0 days / train set | +28.6% | **Warning** |
| **In-Transit Fleet Velocity** | 16.2 mph | 21.5 mph | -24.7% | **Warning** |
| **Stockpile Apparent Bulk Density** | 68.5 lbs/cu.ft | 72.0 lbs/cu.ft (Compacted) | -4.9% | **Normal** |
| **Stockpile Moisture Penalty Index** | 11.4% total moisture | 9.0% standard | +26.7% | **Warning** |
| **Winter Quarter Run-Hours (Capacity Factor)** | 1,420 hrs (65.2% CF) | 1,050 hrs (48.2% CF) | +35.2% | **Warning** |
| **Forecasted Aggregate Winter Burn** | 672.5 ktons | 510.0 ktons | +31.9% | **Critical** |
| **Minimum Projected Inventory Floor** | 255.0 ktons (15.9 DOB) | 320.0 ktons (20.0 DOB) | -20.3% | **Critical** |

---

### Detailed Modeling & Analytical Breakdown

#### 1. Rail Delivery Cycle Dynamics & Velocity Model
* **Train Set Sizing & Capacity:** 115-car unit trains @ 110 tons/car = 12,650 tons net delivery per train set.
* **Turnaround Decomposition:**
  * Origin Loading & Staging: 28.0 hours
  * Loaded Transit (Mine to Plant): 104.0 hours (reduced velocity across Class I interline junction points)
  * Plant Dumper & Thaw Shed Cycle: 36.0 hours (incorporates bottom-dump rotary thaw times during freeze events)
  * Empty Return Transit: 84.0 hours
  * Total Cycle Time: 252.0 hours (~10.5 operating days theoretical, adjusted to **18.0 days** accounting for seasonal corridor staging and crew availability).
* **Delivery Schedule:** 40 scheduled train sets over the quarter (Dec: 14 sets / 177.1 ktons, Jan: 12 sets / 151.8 ktons, Feb: 14 sets / 177.1 ktons = 506.0 ktons gross).

#### 2. Stockpile Volume-to-Density & Caloric Conversion
* **Stockpile Geometry & Survey Calibration:** Topographic survey indicates $14.16 \times 10^6\text{ ft}^3$ gross volume.
* **Density Stratification:**
  * Active Cone / Uncompacted Surface: 62.0 lbs/cu.ft ($0.837\text{ tons/yd}^3$)
  * Compacted Long-Term Dead Storage: 71.8 lbs/cu.ft ($0.969\text{ tons/yd}^3$)
  * Weighted Average Inventory Density: 68.5 lbs/cu.ft ($0.925\text{ tons/yd}^3$)
* **Total Usable Physical Inventory (Dec 1 Start):** 485.0 ktons.
* **Caloric / Moisture Derate:** Elevated moisture (11.4%) reduces effective as-burned heat content from 8,800 Btu/lb to 8,550 Btu/lb, driving a **+2.9% heat-rate penalty** on specific fuel consumption.

#### 3. Forecasted Generation Run-Hours & Burn Profile
* **Unit Configuration:** 2x 500 MW subcritical coal-fired units (1,000 MW total nominal capacity).
* **Average Operating Heat Rate:** 10,200 Btu/kWh.
* **Full-Load Burn Rate:** 596.5 tons/hr at full output (14,316 tons/day at 100% capacity factor).
* **Quarterly Dispatch Profile (LMP Dark Spread Forecast):**
  * **December:** 490 Equivalent Full Load Hours (EFLH) $\rightarrow$ 219.7 ktons burn.
  * **January (Peak Winter Heating):** 605 EFLH $\rightarrow$ 271.3 ktons burn.
  * **February:** 405 EFLH $\rightarrow$ 181.5 ktons burn.
  * **Total Winter Burn:** 1,500 EFLH (68.1% average CF) $\rightarrow$ **672.5 ktons aggregate burn**.

---

### Stockpile Trajectory & Days of Burn Forecast

```
+------------------------------------------------------------------------------------+
| Month   | Start Inv (kt) | Receipts (kt) | Burn (kt) | End Inv (kt) | Min Days of Burn |
+---------+----------------+---------------+-----------+--------------+------------------+
| Dec     | 485.0          | 177.1         | 219.7     | 442.4        | 29.3 DOB         |
| Jan     | 442.4          | 151.8         | 271.3     | 322.9 (255.0)| 15.9 DOB (Min)   |
| Feb     | 322.9          | 177.1         | 181.5     | 318.5        | 21.9 DOB         |
+------------------------------------------------------------------------------------+
*Note: Late January reflects localized cold snap drawdown reaching minimum point of 255.0 ktons.
```

---

### Visualization Configuration

```json
{
  "title": "Winter Quarter Coal Inventory & Burn Rate Trajectory",
  "xAxis": {
    "categories": ["Dec W1", "Dec W2", "Dec W3", "Dec W4", "Jan W1", "Jan W2", "Jan W3", "Jan W4", "Feb W1", "Feb W2", "Feb W3", "Feb W4"],
    "title": "Winter Quarter Timeline"
  },
  "yAxis": [
    {
      "title": "Stockpile Inventory (ktons)",
      "opposite": false
    },
    {
      "title": "Days of Burn (DOB)",
      "opposite": true
    }
  ],
  "series": [
    {
      "name": "Projected Stockpile (ktons)",
      "type": "area",
      "yAxis": 0,
      "data": [485.0, 468.2, 442.8, 410.5, 365.0, 318.4, 280.2, 255.0, 248.6, 260.4, 285.0, 312.5]
    },
    {
      "name": "Days of Burn (DOB Remaining)",
      "type": "line",
      "yAxis": 1,
      "data": [38.8, 36.5, 33.0, 29.3, 23.5, 19.9, 17.5, 15.9, 16.6, 18.6, 21.9, 25.0]
    },
    {
      "name": "Mandatory NERC/PUC Reserve Threshold (20 DOB)",
      "type": "line",
      "dashStyle": "Dash",
      "color": "#FF0000",
      "yAxis": 1,
      "data": [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
    }
  ]
}
```

---

### Actionable Recommendations

* **Procure Supplementary Rail Train Sets:** Coordinate with Class I rail carriers to inject two (2) supplemental emergency train sets in late December/early January (+25.3 ktons), maintaining inventory above the 20-day PUC reliability floor.
* **Calibrate Thaw Shed Throughput:** Pre-stage thaw shed rotary operations ahead of forecasted sub-zero polar vortex events to avoid unloading dwell times exceeding 48 hours per set.
* **Execute Dark Spread Generation Re-Offer Strategy:** If supplemental rail capacity is unavailable by December 15, increase Wholesale LMP offer floor on Unit 2 to economic min dispatch during off-peak hours to stretch stockpile burn duration through the January freeze.
* **Survey Compaction Quality:** Execute mechanical rolling and compaction on the inactive stockpile periphery to minimize freeze penetration and moisture absorption.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "EMERGENCY_RAIL_CAPACITY_REQUEST",
  "approval_level": "Wholesale Trading Lead & Fuel Supply Director",
  "asset_affected": "Coal Unit 1 & Unit 2 Fuel Supply Logistics",
  "proposed_action": "Execute nomination for two (2) incremental unit train sets (25.3 ktons total) for delivery between Jan 5 and Jan 20 to prevent inventory breach below 20.0 Days of Burn",
  "estimated_financial_impact": "$1,450,000 (Fuel + Rail Spot Surcharge)",
  "compliance_reference": "NERC EOP-011-2 / State PUC Winter Reliability Stockpile Mandate",
  "requires_human_confirmation": true
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Adjust unit economic dispatch bids to conserve on-site coal inventory until incoming unit trains arrive."

**Agent Response:**
### Executive Summary
**Current on-site coal stockpiles have depleted to 48,500 tons (~3.3 days of full-load burn), creating a fuel security deficit prior to the scheduled delivery of two 15,000-ton unit trains in 72 hours. Under unconstrained economic dispatch, the plant will breach the mandatory 15,000-ton NERC/PUC safety floor in approximately 52 hours. Implementing a dynamic fuel conservation bid adder (+$18.50/MWh to incremental energy offers) raises the effective offer curve above baseload LMP clearing levels, successfully throttling unit burn rates to minimum operating levels (Eco-Min) while safeguarding grid reliability and stockpile integrity.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Active Usable Stockpile** | 48,500 Tons | 120,000 Tons | -59.58% | **Critical** |
| **Days of Supply (Full Load)** | 3.34 Days | 8.00 Days | -58.25% | **Critical** |
| **Full-Load Burn Rate** | 14,550 Tons/Day | 14,550 Tons/Day | 0.00% | **Warning** |
| **Conserved Burn Rate (Eco-Min)** | 8,400 Tons/Day | 14,550 Tons/Day | -42.27% | **Normal** |
| **Incoming Train Volume (ETA: T+72h)** | 30,000 Tons (2 Trains) | 30,000 Tons | 0.00% | **Normal** |
| **Projected Stockpile at T+72h (Unconstrained)** | 4,850 Tons | 15,000 Tons (Safety Floor) | -67.67% | **Critical** |
| **Projected Stockpile at T+72h (Conservation Bid)** | 23,300 Tons | 15,000 Tons (Safety Floor) | +55.33% | **Normal** |
| **Shadow Opportunity Bid Adder** | +$18.50/MWh | $0.00/MWh | N/A | **Warning** |

---

### Visualization Triggers
**Recommended Chart**: Time-Series Multi-Line Chart comparing on-site inventory trajectories under Unconstrained Dispatch vs. Conservation Dispatch against the critical minimum safety floor up to unit train arrival (ETA: T+72h).

```json
{
  "chart_type": "line",
  "title": "Coal Stockpile Trajectory vs. Unit Train ETA",
  "intervals": [
    "T+00h",
    "T+12h",
    "T+24h",
    "T+36h",
    "T+48h",
    "T+60h",
    "T+72h (Train ETA)"
  ],
  "series": [
    {
      "name": "Status Quo Burn (Tons)",
      "data": [48500, 41200, 33900, 26600, 19300, 12000, 4700]
    },
    {
      "name": "Conservation Dispatch Curve (Tons)",
      "data": [48500, 44300, 40100, 35900, 31700, 27500, 23300]
    },
    {
      "name": "Critical Safety Floor (Tons)",
      "data": [15000, 15000, 15000, 15000, 15000, 15000, 15000]
    }
  ]
}
```

---

### Actionable Recommendations
- **Inject Fuel Conservation Adder**: Apply a calculated +$18.50/MWh shadow cost adder to Day-Ahead and Real-Time incremental energy curves above Eco-Min (P_min) to clear only during extreme localized scarcity.
- **Lock Eco-Min Parameters**: Retain unit on-line status at physical minimum operating levels (Eco-Min) to avoid startup/shutdown cycle wear and ensure non-spinning/spinning reserve eligibility where compensated.
- **Track Rail Telemetry**: Monitor Class I railroad GPS waybills for Train Units #CSX-8412 and #CSX-8415 to verify arrival windows at the plant rotary car dumper.
- **RTO Fuel Limitation Notification**: Submit an operational fuel limitation parameter update to the RTO/ISO reliability coordinator in compliance with tariff guidelines.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "MARKET_BID_CURVE_ADJUSTMENT",
  "domain": "Wholesale Trading",
  "target_asset": "COAL_GEN_UNIT_1_2",
  "proposed_parameters": {
    "economic_max_mw_override": "Eco-Min (240 MW / Unit)",
    "incremental_bid_adder_usd_mwh": 18.50,
    "effective_duration_hours": 72,
    "market_intervals": "DA_AND_RT_HOURLY",
    "safety_floor_threshold_tons": 15000
  },
  "justification": "Mitigates critical stockpile depletion below mandatory safety thresholds prior to scheduled train arrival at T+72h.",
  "approval_required_from": "Lead Real-Time Energy Trader / Plant Operations Manager"
}
```
