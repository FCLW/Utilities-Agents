# ⚡ Iso Rto Bidding Curve Generator

![Domain](https://img.shields.io/badge/Domain-wholesale%20trading-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of iso rto bidding curve generator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Iso Rto Bidding Curve Generator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank iso rto bidding curve generator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_wholesale_trading.iso_rto_bidding_curve_generator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can you construct the piecewise linear three-part energy bid curve for Combined Cycle Unit 2 for tomorrow's market auction?"

**Agent Response:**
### Executive Summary
**The Three-Part Energy Bid Curve for Combined Cycle Unit 2 (CCGT-2, rated capacity 500 MW) has been successfully generated for tomorrow's Day-Ahead Market auction based on current delivered gas index pricing ($3.25/MMBtu), variable O&M, and tested incremental heat rates.** 
**The unit's economic operating band is structured across five piecewise linear segments from EcoMin ($150\text{ MW}$) to EcoMax ($500\text{ MW}$), incorporating updated cold/warm/hot startup cost profiles and no-load allocations.** 
**Submitting this market offer constitutes a Tier 2 financial market commitment and requires formal trading desk verification before submission to the ISO/RTO portal.**

---

### Unit Operating & Cost Baseline

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Delivered Fuel Price ($/MMBtu)** | $3.25 | $3.10 | +4.84% | Normal |
| **Variable O&M ($/MWh)** | $2.85 | $2.75 | +3.64% | Normal |
| **No-Load Fuel Burn (MMBtu/hr)** | 620.00 | 615.00 | +0.81% | Normal |
| **Minimum Generation (EcoMin)** | 150.00 MW | 150.00 MW | 0.00% | Normal |
| **Maximum Capacity (EcoMax)** | 500.00 MW | 500.00 MW | 0.00% | Normal |
| **Hot Startup Cost ($/Start)** | $12,450.00 | $12,000.00 | +3.75% | Normal |
| **Cold Startup Cost ($/Start)** | $38,200.00 | $37,500.00 | +1.87% | Normal |

---

### Three-Part Bid Curve Structure

#### Part 1: Startup Offers
* **Hot Start (Offline $< 8\text{ hrs}$):** $\$12,450.00$
* **Intermediate/Warm Start (Offline $8 - 24\text{ hrs}$):** $\$21,800.00$
* **Cold Start (Offline $> 24\text{ hrs}$):** $\$38,200.00$

#### Part 2: No-Load Cost
* **No-Load / Min-Gen Hourly Cost:** $\$4,862.50\text{/hr}$
  $$\text{No-Load Cost} = (620.00\text{ MMBtu/hr} \times \$3.25/\text{MMBtu}) + (150\text{ MW} \times \$2.85/\text{MWh} \times 0.20) + \text{Base Ancillary Aux Power Allocation}$$

#### Part 3: Piecewise Linear Incremental Energy Offer Segments

| Segment | MW Range | Incremental Heat Rate (Btu/kWh) | Marginal Fuel Cost ($/MWh) | VOM + Adder ($/MWh) | Total Incremental Bid ($/MWh) | Status (Normal/Warning/Critical) |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Seg 1 (Min-Gen)** | $150 - 220\text{ MW}$ | 9,108 | $29.60 | $2.85 | **$32.45** | Normal |
| **Seg 2** | $220 - 300\text{ MW}$ | 9,615 | $31.25 | $2.85 | **$34.10** | Normal |
| **Seg 3** | $300 - 380\text{ MW}$ | 10,462 | $34.00 | $2.85 | **$36.85** | Normal |
| **Seg 4 (Duct Firing)** | $380 - 450\text{ MW}$ | 11,800 | $38.35 | $2.85 | **$41.20** | Normal |
| **Seg 5 (Peak Duct Firing)** | $450 - 500\text{ MW}$ | 14,123 | $45.90 | $2.85 | **$48.75** | Normal |

---

### Visualization Trigger
A piecewise linear step-chart representation of the incremental energy curve has been compiled for ISO offer visualization:

```json
{
  "title": "Combined Cycle Unit 2 - Piecewise Linear Energy Bid Curve ($/MWh vs MW)",
  "xAxis": {
    "name": "Output (MW)",
    "type": "category",
    "data": [150, 220, 300, 380, 450, 500]
  },
  "yAxis": {
    "name": "Marginal Cost / Offer ($/MWh)",
    "type": "value"
  },
  "series": [
    {
      "name": "Incremental Energy Bid ($/MWh)",
      "type": "line",
      "step": "end",
      "data": [32.45, 34.10, 36.85, 41.20, 48.75, 54.30]
    }
  ]
}
```

---

### Actionable Recommendations
- **Fuel Basis Check:** Validate the intra-day pipeline imbalance fee status before the Day-Ahead Market bidding deadline (10:00 AM Prevailing Market Time).
- **Ramp Constraints:** Ensure the unit profile includes a $12.5\text{ MW/min}$ normal ramp rate and a minimum run time requirement of $4\text{ hours}$.
- **Ancillary Service Linkage:** In the event of spinning reserve co-optimization, restrict Segments 4–5 to energy-only dispatch due to duct-firing thermal stress limits.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_action:
  operation_type: "MARKET_BID_SUBMISSION"
  market: "ISO_RTO_DAY_AHEAD_ENERGY_MARKET"
  asset_id: "CCGT_UNIT_2"
  effective_trade_date: "TOMORROW_AUCTION_CYCLE"
  bid_parameters:
    eco_min_mw: 150.0
    eco_max_mw: 500.0
    startup_costs:
      hot_usd: 12450.00
      intermediate_usd: 21800.00
      cold_usd: 38200.00
    no_load_cost_usd_per_hr: 4862.50
    incremental_curve:
      - {mw_end: 220, offer_usd_mwh: 32.45}
      - {mw_end: 300, offer_usd_mwh: 34.10}
      - {mw_end: 380, offer_usd_mwh: 36.85}
      - {mw_end: 450, offer_usd_mwh: 41.20}
      - {mw_end: 500, offer_usd_mwh: 48.75}
  requires_hitl_approval: true
  confirmation_deadline: "10:00 AM EPT (Market Gate Closure)"
```

### Example 2: Trend & Comparative Analysis
**User:** "Calculate no-load costs, start-up cost profiles, and incremental heat rate curves based on latest spot natural gas index prices."

**Agent Response:**
### Executive Summary
**Day-Ahead ISO/RTO three-part bidding curves have been recalculated using the latest spot natural gas index price of $3.20/MMBtu delivered ($2.85/MMBtu Henry Hub index + $0.35/MMBtu basis/transport) and applicable environmental/VOM adders. The resulting portfolio marginal cost structures reflect an average incremental energy offer range of $28.56/MWh to $33.19/MWh across operating segments for Combined Cycle assets, with no-load costs settling at $1,801.20/hr. All calculated parameter curves comply with FERC Order 831 verification standards and regional market mitigation cost-based offer guidelines.**

---

### Data Presentation

#### Wholesale Generation Cost Metrics & ISO Parameter Summary

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Delivered Gas Index Price** | $3.20 / MMBtu | $3.05 / MMBtu | +4.92% | Normal |
| **CCGT No-Load Cost** | $1,801.20 / hr | $1,720.00 / hr | +4.72% | Normal |
| **CT Peaker No-Load Cost** | $712.60 / hr | $685.00 / hr | +4.03% | Normal |
| **CCGT Cold Start Cost** | $11,920.00 / start | $11,450.00 / start | +4.10% | Normal |
| **CCGT Warm Start Cost** | $6,780.00 / start | $6,520.00 / start | +3.99% | Normal |
| **CCGT Hot Start Cost** | $4,150.00 / start | $4,010.00 / start | +3.49% | Normal |
| **CT Cold Start Cost** | $3,480.00 / start | $3,350.00 / start | +3.88% | Normal |
| **CCGT Marginal Heat Rate (EcoMax)** | 7,950 Btu / kWh | 7,920 Btu / kWh | +0.38% | Normal |
| **CCGT Top-Segment Marginal Cost** | $33.19 / MWh | $31.95 / MWh | +3.88% | Normal |
| **CT Top-Segment Marginal Cost** | $61.30 / MWh | $58.90 / MWh | +4.07% | Normal |

---

#### Detailed Segmented Incremental Energy Curve Breakdown

| Asset ID | Segment (MW Range) | Incremental Heat Rate (Btu/kWh) | Fuel & Emission Cost ($/MWh) | Variable O&M ($/MWh) | Adjusted Offer Price ($/MWh) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CCGT-Unit-1** | 150 – 250 (EcoMin) | 6,750 | $26.06 | $2.50 | **$28.56** |
| **CCGT-Unit-1** | 250 – 350 | 6,980 | $26.94 | $2.50 | **$29.44** |
| **CCGT-Unit-1** | 350 – 450 | 7,320 | $28.26 | $2.50 | **$30.76** |
| **CCGT-Unit-1** | 450 – 520 (EcoMax) | 7,950 | $30.69 | $2.50 | **$33.19** |
| **CT-Peaker-2** | 40 – 75 (EcoMin) | 9,800 | $37.83 | $4.25 | **$42.08** |
| **CT-Peaker-2** | 75 – 120 | 11,200 | $43.23 | $4.25 | **$47.48** |
| **CT-Peaker-2** | 120 – 160 (EcoMax) | 14,780 | $57.05 | $4.25 | **$61.30** |

*Formulation: $\text{Offer Price} = (\text{Incremental Heat Rate} \times (\text{Gas Index} + \text{CO}_2 \text{ Adder})) + \text{VOM}$*

---

### Visualization Triggers
**Recommended Chart**: Stepwise Incremental Energy Bidding Curve (Line / Step Curve) displaying segment capacity (MW) versus offer price ($/MWh).

```json
{
  "chart_type": "line",
  "title": "ISO/RTO Incremental Supply Offer Bidding Curves",
  "xAxis": {
    "name": "Unit Output (MW)",
    "data": [150, 250, 350, 450, 520]
  },
  "yAxis": {
    "name": "Offer Price ($/MWh)"
  },
  "series": [
    {
      "name": "CCGT-Unit-1 ($/MWh)",
      "step": "start",
      "data": [28.56, 29.44, 30.76, 33.19, 33.19]
    },
    {
      "name": "CT-Peaker-2 ($/MWh)",
      "step": "start",
      "data": [42.08, 47.48, 61.30, 61.30, 61.30]
    }
  ]
}
```

---

### Actionable Recommendations
- **Validate Fuel Index Timing**: Ensure gas index intraday balancing tariffs and weekend pipeline scheduling balancing terms match the ISO Day-Ahead trading timeline.
- **Synchronize Mitigated Cost-Based Offer Caps**: Submit updated fuel price index justification to the Market Monitoring Unit (MMU) portal to prevent automated reference level offer mitigation.
- **Review Ramping Multi-Interval Constraints**: Verify unit commitment start-up ramp rates and minimum down-time parameters alongside updated start cost tables.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "ISO_RTO_DAY_AHEAD_BID_SUBMISSION",
  "market_target": "Day-Ahead Energy & Operating Reserves",
  "units_affected": ["CCGT-Unit-1", "CT-Peaker-2"],
  "effective_operating_day": "Tomorrow (Next Trading Day - 24hr)",
  "three_part_offer_payload": {
    "gas_index_applied_usd_mmbtu": 3.20,
    "CCGT-Unit-1": {
      "no_load_cost_usd_hr": 1801.20,
      "hot_start_usd": 4150.00,
      "warm_start_usd": 6780.00,
      "cold_start_usd": 11920.00,
      "energy_curve_mw_usd": [[150, 28.56], [250, 29.44], [350, 30.76], [520, 33.19]]
    },
    "CT-Peaker-2": {
      "no_load_cost_usd_hr": 712.60,
      "start_cost_usd": 3480.00,
      "energy_curve_mw_usd": [[40, 42.08], [75, 47.48], [160, 61.30]]
    }
  },
  "human_approval_required": true,
  "action_status": "PENDING_OPERATOR_APPROVAL"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Transmit the validated generation supply offer curves to PJM / CAISO market scheduling systems before gate closure."

**Agent Response:**
### Executive Summary
**Generation supply offer curves for PJM and CAISO Day-Ahead and Real-Time market intervals have been generated and validated against portfolio heat rates, fuel index pricing, and operating limits.** In accordance with safety and compliance guardrails, direct transmission of market bids constitutes a Tier 2 financial and physical commodity commitment that cannot be executed autonomously. **The complete offer stack is staged and pending mandatory Human-In-The-Loop (HITL) authorization prior to gate closure transmission.**

---

### Data Presentation: Supply Offer Curve Summary

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Staged Capacity (PJM)** | 1,450 MW | 1,450 MW | 0.00% | Normal |
| **Total Staged Capacity (CAISO)** | 820 MW | 820 MW | 0.00% | Normal |
| **Weighted Average Offer Price (PJM)** | $42.15 / MWh | $40.50 / MWh | +4.07% | Normal |
| **Weighted Average Offer Price (CAISO)**| $58.30 / MWh | $55.00 / MWh | +6.00% | Normal |
| **Portfolio Value at Risk (95% VaR)** | $128,400 | $150,000 | -14.40% | Normal |
| **PJM Market Gate Closure T-Minus** | 42 min | N/A | N/A | Warning |
| **CAISO Market Gate Closure T-Minus** | 72 min | N/A | N/A | Normal |

---

### Visualization Trigger: Marginal Cost Supply Stack

```json
{
  "chart_type": "step-line",
  "data": {
    "PJM_Segments": [
      {"mw_block": 200, "offer_price_usd_mwh": 28.50, "unit_type": "Nuclear/Base"},
      {"mw_block": 750, "offer_price_usd_mwh": 38.20, "unit_type": "CCGT Block 1"},
      {"mw_block": 1200, "offer_price_usd_mwh": 46.80, "unit_type": "CCGT Block 2"},
      {"mw_block": 1450, "offer_price_usd_mwh": 68.00, "unit_type": "Peaker Segment"}
    ],
    "CAISO_Segments": [
      {"mw_block": 300, "offer_price_usd_mwh": 32.00, "unit_type": "Hydro / Solar Hybrid"},
      {"mw_block": 650, "offer_price_usd_mwh": 54.10, "unit_type": "CCGT Flex"},
      {"mw_block": 820, "offer_price_usd_mwh": 89.50, "unit_type": "Fast-Start Peaker"}
    ]
  }
}
```

---

### Actionable Recommendations
- **Desk Trader Review**: Verify marginal heat rate indexing against morning Henry Hub / SoCal Border gas settlements.
- **Ramp & Ancillary Service Checks**: Confirm spinning reserve and regulation-up allocations on CCGT Block 2 prior to submission.
- **Authorization Execution**: Execute the approval signature block below to release the automated payload transmission via the secure ISO/RTO API endpoints.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "tier_level": 2,
  "action_type": "SUBMIT_WHOLESALE_MARKET_BIDS",
  "submitting_agent": "iso_rto_bidding_curve_generator",
  "approval_required": true,
  "target_markets": ["PJM Interconnection", "CAISO"],
  "payload_summary": {
    "PJM_Payload_ID": "BID-PJM-20250220-DA-V4",
    "PJM_Capacity_MW": 1450,
    "CAISO_Payload_ID": "BID-CAISO-20250220-DA-V2",
    "CAISO_Capacity_MW": 820,
    "Market_Product": "Energy + Ancillary Services (DA)",
    "Execution_Protocol": "OASIS / Web Services API (Encrypted E-Tag/PKI)"
  },
  "compliance_certifications": [
    "FERC Order 831 / 764 compliance verified",
    "PJM Market Rule Section 11 verified",
    "No predatory/anti-competitive step pricing detected"
  ],
  "hitl_status": "AWAITING_OPERATOR_CONFIRMATION"
}
```
