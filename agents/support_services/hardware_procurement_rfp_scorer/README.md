# ⚡ Hardware Procurement Rfp Scorer

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of hardware procurement rfp scorer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Hardware Procurement Rfp Scorer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank hardware procurement rfp scorer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.hardware_procurement_rfp_scorer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "How do the three vendor competitive proposals for our 500kV optical ground wire (OPGW) procurement rank against technical criteria?"

**Agent Response:**
### 1. Executive Summary
**Vendor Alpha ranks 1st in technical scoring with an aggregate score of 96.2/100, demonstrating superior short-circuit fault current withstand margin (120 kA²·s vs. 105 kA²·s requirement) and lowest optical attenuation across 72-fiber single-mode cores.** **Vendor Beta ranks 2nd at 86.6/100, meeting baseline IEEE 1138 standards but offering narrower mechanical loading margins under extreme NERC Heavy loading zones.** **Vendor Gamma ranks 3rd (Non-Compliant) at 67.0/100 due to failing thermal short-circuit criteria and exceeding maximum allowable optical attenuation limits at 1550 nm.**

---

### 2. Data Presentation (Markdown Tables)

The competitive technical evaluation evaluated three submitted vendor proposals against utility engineering specifications for 500kV Optical Ground Wire (OPGW) installations under IEEE 1138, IEEE 1222, and IEC 60794 standards.

#### Table 1: Technical Criteria & Parameter Comparison by Vendor

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Vendor Alpha: Rated Tensile Strength (RTS)** | 145.2 kN | 130.0 kN (Min) | +11.69% | Normal |
| **Vendor Alpha: Short-Circuit Capacity (I²t @ 1s)** | 120.5 kA²·s | 105.0 kA²·s (Min) | +14.76% | Normal |
| **Vendor Alpha: Optical Attenuation (@ 1550 nm)** | 0.188 dB/km | 0.200 dB/km (Max) | -6.00% | Normal |
| **Vendor Alpha: Max Fiber Temp Under Fault** | 162.0 °C | 200.0 °C (Max) | -19.00% | Normal |
| **Vendor Alpha: Overall Technical Score** | 96.2 / 100 | 80.0 / 100 | +20.25% | Normal |
| **Vendor Beta: Rated Tensile Strength (RTS)** | 135.0 kN | 130.0 kN (Min) | +3.85% | Normal |
| **Vendor Beta: Short-Circuit Capacity (I²t @ 1s)** | 108.2 kA²·s | 105.0 kA²·s (Min) | +3.05% | Normal |
| **Vendor Beta: Optical Attenuation (@ 1550 nm)** | 0.195 dB/km | 0.200 dB/km (Max) | -2.50% | Normal |
| **Vendor Beta: Max Fiber Temp Under Fault** | 188.5 °C | 200.0 °C (Max) | -5.75% | Warning |
| **Vendor Beta: Overall Technical Score** | 86.6 / 100 | 80.0 / 100 | +8.25% | Normal |
| **Vendor Gamma: Rated Tensile Strength (RTS)** | 128.4 kN | 130.0 kN (Min) | -1.23% | Warning |
| **Vendor Gamma: Short-Circuit Capacity (I²t @ 1s)** | 97.8 kA²·s | 105.0 kA²·s (Min) | -6.86% | Critical |
| **Vendor Gamma: Optical Attenuation (@ 1550 nm)** | 0.215 dB/km | 0.200 dB/km (Max) | +7.50% | Critical |
| **Vendor Gamma: Max Fiber Temp Under Fault** | 218.0 °C | 200.0 °C (Max) | +9.00% | Critical |
| **Vendor Gamma: Overall Technical Score** | 67.0 / 100 | 80.0 / 100 | -16.25% | Critical |

---

### 3. Visualization Triggers

**Recommended Visualization**: Stacked Bar Chart & Multi-Attribute Radar Chart to compare technical capability domains across mechanical loading, electrical thermal capacity, optical transport performance, and standard compliance.

```json
{
  "chart_type": "bar",
  "title": "500kV OPGW Vendor Technical Scoring Breakdown (100-Point Scale)",
  "categories": [
    "Vendor Alpha (Apex)",
    "Vendor Beta (Lumina)",
    "Vendor Gamma (ElectroWire)"
  ],
  "series": [
    {
      "name": "Mechanical & Structural (30%)",
      "data": [28.5, 25.8, 20.1]
    },
    {
      "name": "Electrical & Short-Circuit (30%)",
      "data": [29.1, 25.2, 18.5]
    },
    {
      "name": "Optical Performance (25%)",
      "data": [24.0, 22.0, 17.2]
    },
    {
      "name": "Compliance & QA/QC (15%)",
      "data": [14.6, 13.6, 11.2]
    }
  ]
}
```

---

### 4. Actionable Recommendations

1. **Shortlist Vendor Alpha and Vendor Beta for Commercial Evaluation**: Proceed with commercial phase and Total Cost of Ownership (TCO) modeling including reel optimization and hardware accessory kits (dead-ends, suspension clamps, vibration dampers).
2. **Disqualify Vendor Gamma on Technical Grounds**: Formally reject Proposal C due to non-compliance with the 500kV fault-withstand requirement (105 kA²·s minimum) and excessive optical signal attenuation.
3. **Conduct Factory Acceptance Testing (FAT) Scope Review with Vendor Alpha**: Mandate type-test verification reports under IEEE 1138 Section 6 (Aeolian vibration, gallop test, and short-circuit thermal cycling).

---

### [TIER 2 ACTION REQUIRED]

```yaml
action_type: "PROCUREMENT_TECHNICAL_AWARD_STAGE_GATE"
status: "PENDING_HITL_CONFIRMATION"
description: "Authorization to advance Vendor Alpha and Vendor Beta to Commercial RFP evaluation stage and issue technical disqualification letter for Vendor Gamma."
affected_rfp_id: "RFP-500KV-OPGW-2025-01"
grid_voltage_class: "500kV"
target_asset: "Optical Ground Wire (OPGW) Hardware"
evaluation_summary:
  rank_1: "Vendor Alpha (Score: 96.2/100 - Technologically Qualified)"
  rank_2: "Vendor Beta (Score: 86.6/100 - Technologically Qualified)"
  disqualified: "Vendor Gamma (Score: 67.0/100 - Critical Technical Deficiencies)"
approver_roles:
  - "Support Services Procurement Lead"
  - "Transmission Lines Principal Engineer"
```

### Example 2: Trend & Comparative Analysis
**User:** "Evaluate vendor manufacturing warranties, delivery lead times, price per kilometer, and cybersecurity supply chain audits."

**Agent Response:**
### Executive Summary
**The Hardware Procurement RFP evaluation has scored three shortlisted vendors across manufacturing warranty terms, delivery lead times, unit pricing ($/km), and NERC CIP-013 supply chain cybersecurity audit verifications. Vendor A (AlphaGrid) emerges as the top-ranked bidder with a composite score of 88.5/100, outperforming peers on cybersecurity provenance (full SBOM & SOC 2 Type II) and extended 10-year warranty coverage despite a 7.1% price premium over baseline. Vendor B and Vendor C present elevated risks in cyber audit compliance and lead-time volatility, respectively.**

---

### Quantitative Evaluation & RFP Scoring Matrix

| Metric / Dimension | Current Value (Vendor A / B / C) | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Manufacturing Warranty Duration** | Vendor A: 10 yrs<br>Vendor B: 5 yrs<br>Vendor C: 3 yrs | $\ge 7\text{ yrs}$ | Vendor A: $+42.9\%$<br>Vendor B: $-28.6\%$<br>Vendor C: $-57.1\%$ | **Normal** (Vendor A)<br>**Warning** (Vendor B)<br>**Critical** (Vendor C) |
| **Delivery Lead Time (Aerosol/Conductor/Cable)** | Vendor A: 16 wks<br>Vendor B: 12 wks<br>Vendor C: 26 wks | $\le 16\text{ wks}$ | Vendor A: $0.0\%$<br>Vendor B: $-25.0\%$<br>Vendor C: $+62.5\%$ | **Normal** (Vendor A)<br>**Normal** (Vendor B)<br>**Critical** (Vendor C) |
| **Price per Kilometer ($/km)** | Vendor A: \$37,500/km<br>Vendor B: \$39,200/km<br>Vendor C: \$32,800/km | \$35,000/km | Vendor A: $+7.1\%$<br>Vendor B: $+12.0\%$<br>Vendor C: $-6.3\%$ | **Normal** (Vendor A)<br>**Warning** (Vendor B)<br>**Normal** (Vendor C) |
| **Cyber Supply Chain Audit & Provenance (NERC CIP-013)** | Vendor A: Pass (100% SBOM, Level 3)<br>Vendor B: Conditional (Gap in Tier 2 microcode)<br>Vendor C: Failed (No independent audit) | 100% Third-party Audit + Verified SBOM | Vendor A: $0.0\%$<br>Vendor B: $-35.0\%$<br>Vendor C: $-75.0\%$ | **Normal** (Vendor A)<br>**Warning** (Vendor B)<br>**Critical** (Vendor C) |
| **Composite Weighted RFP Score (0–100)** | Vendor A: 88.5<br>Vendor B: 74.0<br>Vendor C: 62.5 | $\ge 80.0$ | Vendor A: $+10.6\%$<br>Vendor B: $-7.5\%$<br>Vendor C: $-21.9\%$ | **Normal** (Vendor A)<br>**Warning** (Vendor B)<br>**Critical** (Vendor C) |

---

### Evaluation Criteria Breakdown

1. **Vendor Manufacturing Warranties (Weight: 25%)**:
   - *Vendor A*: Full 10-year defect and performance warranty covering environmental degradation, dielectric breakdown, and mechanical tension failure.
   - *Vendor B*: 5-year standard warranty; prorated replacement after Year 3.
   - *Vendor C*: 3-year limited warranty; excludes thermal cycling wear and surge stress.

2. **Delivery Lead Times (Weight: 25%)**:
   - *Vendor A*: 16 weeks firm with liquidated damages clause (1.5%/week delayed).
   - *Vendor B*: 12 weeks expedited due to domestic distribution warehouse.
   - *Vendor C*: 26 weeks with offshore shipping exposure and customs clearance dependencies.

3. **Commercial Pricing per Kilometer (Weight: 25%)**:
   - *Vendor C* offers lowest capital cost (\$32,800/km), but total cost of ownership (TCO) is undermined by short warranty and freight risk.
   - *Vendor A* offers balanced volume discounts at \$37,500/km with fixed index hedging against base metals (Al/Cu).

4. **Cybersecurity & Supply Chain Integrity (Weight: 25%)**:
   - *Compliance Mandate*: Strict alignment with **NERC CIP-013-1** (Supply Chain Risk Management).
   - *Vendor A*: Delivered full Software Bill of Materials (SBOM), hardware component tracing to country of origin (NDAA compliant), and third-party ISO 27001/SOC 2 Type II attestation.
   - *Vendor B & C*: Identified Tier 2/3 sub-supplier firmware traceability gaps and non-audited microcontroller component sourcing.

---

### Actionable Recommendations

- **Award Recommendation**: Select **Vendor A (AlphaGrid)** as the primary hardware supplier based on comprehensive compliance with technical specs, NERC CIP-013 audit verifications, and superior 10-year warranty mitigation.
- **Secondary / Backup Supplier**: Place **Vendor B (VoltCore)** on conditional reserve contingent upon their submission of a certified remediation plan for Tier 2 microcode provenance within 30 business days.
- **Disqualification Notice**: Formally disqualify **Vendor C (NexLine)** due to non-conformance with CIP-013 cybersecurity baseline criteria and lead times exceeding maximum critical path thresholds (26 weeks vs. 16 weeks target).
- **Contractual Safeguards**: Integrate mandatory factory acceptance testing (FAT), milestone-based payment schedules, and index-linked price adjustments for commodity conductor metals.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PROCUREMENT_CONTRACT_INTENT_APPROVAL",
  "domain": "Support Services / Procurement",
  "contract_summary": {
    "recommended_vendor": "AlphaGrid Technologies Inc.",
    "rfp_reference": "RFP-2024-GRID-HDW-088",
    "scope": "High-Voltage Conductor & Transmission Hardware Procurement",
    "contract_value_estimated": "$18,750,000 USD (500 km baseline)",
    "unit_rate": "$37,500 / km",
    "lead_time": "16 Weeks Firm",
    "warranty_term": "10 Years Full Coverage",
    "cip_013_compliance_status": "CERTIFIED_PASS"
  },
  "required_approver": "Chief Procurement Officer / Supply Chain Director",
  "approval_status": "PENDING_HUMAN_IN_THE_LOOP_CONFIRMATION"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate the procurement bid evaluation matrix and submit the vendor award recommendation to the utility procurement committee."

**Agent Response:**
### 1. Executive Summary
**The Hardware Procurement RFP evaluation for Grid Modernization & Substation Telemetry Hardware (RFP-2024-ENG-088) has been completed across all qualifying bidders. Vendor A (GridTech Dynamics) achieved the highest composite score of 90.35/100, outperforming competing proposals in critical technical compliance, IEEE/NERC-CIP cyber standards, and SLA reliability despite a minor initial capital premium. Final recommendation is submitted for Procurement Committee review and formal award approval subject to standard Tier 2 Human-in-the-Loop governance.**

---

### 2. RFP Scoring Matrix & Performance Summary

#### Comprehensive Bid Evaluation Scoring Table
| Bidder / Vendor | Technical & Specs (35%) | TCO / Commercial (30%) | Supply Chain & Lead Time (15%) | Warranty & SLAs (10%) | NERC CIP / Cyber (10%) | Weighted Composite Score (100%) | Bid Rank |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Vendor A (GridTech Dynamics)** | **94.00** | **82.50** | **91.00** | **95.00** | **98.00** | **90.35** | **Rank 1 (Recommended)** |
| **Vendor B (VoltPower Systems)** | 88.00 | 91.00 | 78.00 | 85.00 | 89.00 | 87.20 | Rank 2 |
| **Vendor C (Apex Substation Hardware)** | 76.50 | 95.00 | 72.00 | 80.00 | 75.00 | 81.38 | Rank 3 |

#### Target Key Performance Indicators & Benchmark Tracking
| Metric | Current Value (Vendor A) | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Evaluated TCO** | $14.28M | $15.00M Target Cap | -4.80% | **Normal** |
| **Hardware Lead Time** | 16.0 Weeks | ≤ 20.0 Weeks | -20.00% | **Normal** |
| **Technical Compliance Rate** | 98.4% | ≥ 95.0% | +3.58% | **Normal** |
| **NERC CIP-013 Supply Chain Score** | 98.0 / 100 | ≥ 85.0 / 100 | +15.29% | **Normal** |
| **Extended Warranty Duration** | 10 Years | 5 Years Baseline | +100.00% | **Normal** |
| **Spares Inventory Availability** | 99.2% | ≥ 98.0% | +1.22% | **Normal** |

---

### 3. Visualization Triggers

**Recommended Visualization:** Grouped Multi-Factor Category Bar Chart comparing vendor category scores against utility evaluation weights.

```json
{
  "chart_type": "bar",
  "title": "Hardware RFP Evaluation Factor Comparison by Vendor",
  "categories": [
    "Technical Compliance (35%)",
    "Total Cost of Ownership (30%)",
    "Delivery & Supply Chain Reliability (15%)",
    "Warranty & SLA Terms (10%)",
    "Cybersecurity & NERC CIP (10%)"
  ],
  "series": [
    {
      "name": "Vendor A (GridTech Dynamics)",
      "data": [94.0, 82.5, 91.0, 95.0, 98.0]
    },
    {
      "name": "Vendor B (VoltPower Systems)",
      "data": [88.0, 91.0, 78.0, 85.0, 89.0]
    },
    {
      "name": "Vendor C (Apex Substation Hardware)",
      "data": [76.5, 95.0, 72.0, 80.0, 75.0]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Proceed to Legal & PPA/Contract Review:** Initiate master supply agreement drafting incorporating Vendor A’s 10-year warranty, liquidated damages for delivery delays exceeding 16 weeks, and strict adherence to NERC CIP-013 supply chain verification.
- **Lock In Capital Allocation:** Reconcile the committed capital expenditure ($14.28M) against the approved annual support services capital budget.
- **Establish Vendor Key Performance Tracking:** Integrate delivery milestone tracking into the enterprise fleet/procurement monitoring system upon contract execution.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "PROCUREMENT_CONTRACT_AWARD_RECOMMENDATION",
  "approval_level": "TIER_2_PROCUREMENT_COMMITTEE",
  "rfp_reference_id": "RFP-2024-ENG-088",
  "recommended_vendor": "GridTech Dynamics, Inc.",
  "evaluated_contract_value_usd": 14280000.00,
  "budget_ceiling_usd": 15000000.00,
  "scoring_summary": {
    "composite_score": 90.35,
    "rank": 1,
    "cyber_compliance": "PASSED_NERC_CIP_013"
  },
  "required_approvers": [
    "Chief Procurement Officer",
    "VP of Power Delivery & Engineering",
    "Lead Support Services Legal Counsel"
  ],
  "action_prompt": "Confirm formal authorization to issue the Notice of Intent to Award and commence final contract execution with GridTech Dynamics, Inc."
}
```
