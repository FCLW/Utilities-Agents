# ⚡ Power Purchase Agreement Legal Reviewer

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of power purchase agreement legal reviewer is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Power Purchase Agreement Legal Reviewer Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank power purchase agreement legal reviewer events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.power_purchase_agreement_legal_reviewer_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Does the commercial solar Power Purchase Agreement (PPA) include standard clauses for curtailment risk and negative pricing indemnity?"

**Agent Response:**
### Executive Summary
**A standard, commercially bankable commercial solar Power Purchase Agreement (PPA) must explicitly address economic and grid-directed curtailment as well as negative pricing risk allocation.** **Market-standard terms distinguish between Buyer-directed/Economic curtailment (which requires Deemed Generation compensation to the Seller) and System Emergency/RTO curtailment (which typically has an uncompensated annual cap before relief applies).** **Without affirmative negative pricing indemnity and economic curtailment compensation clauses, the project risks unhedged revenue erosion during negative wholesale LMP hours and high renewable penetration periods.**

---

### Contract Clause Review & Risk Matrix

| Metric / Clause Area | Current Standard Term | Baseline / Industry Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Economic Curtailment Settlement** | Compensated as Deemed Generation at Contract PPA Price | 100% Deemed Energy Compensation above Annual Cap | 0.0% | **Normal** |
| **Negative Pricing Floor Exposure** | Buyer absorbs negative LMP or pays floor price ($0/MWh) | Seller indemnified against negative settlement spread | 0.0% | **Normal** |
| **Emergency / RTO Curtailment Cap** | Uncompensated up to 50–100 hrs/yr (Buyer/RTO safe harbor) | Max 50 hrs/yr uncompensated threshold | +0.0% | **Warning** |
| **Environmental Attributes (RECs) on Curtailment** | Deemed REC value credit included in economic curtailment | 100% REC replacement/credit for Buyer-directed actions | 0.0% | **Normal** |
| **Interconnection / Force Majeure Curtailment** | Excused event without monetary compensation | Non-compensable, subject to COD/availability tolling | 0.0% | **Normal** |

---

### Detailed Legal & Commercial Analysis

#### 1. Curtailment Risk Allocation
* **Buyer-Directed / Economic Curtailment**: When the Buyer (or offtaker) orders the project to reduce or cease generation due to unfavorable wholesale market conditions, standard PPAs treat the foregone energy as **"Deemed Generation."** The Buyer pays the Seller the contract PPA rate for the estimated energy that would have been generated based on real-time solar irradiance telemetry minus actual delivered energy.
* **Emergency / ISO / RTO Curtailment**: Reductions ordered by the Regional Transmission Organization / Balancing Authority (e.g., CAISO, ERCOT, PJM) for grid stability or transmission congestion:
  * Standard clauses provide an **uncompensated annual allowance** (typically 50 to 100 equivalent full-capacity hours per contract year).
  * Any grid curtailment exceeding the agreed threshold is either treated as Deemed Generation or triggers contract availability relief to prevent Seller default under minimum generation guarantees.

#### 2. Negative Pricing Indemnity
* **Settlement Mechanism**: In wholesale nodal markets (Day-Ahead or Real-Time LMP), generation during negative price events incurs a settlement charge.
* **Standard Allocation**:
  * **Fixed-for-Floating / Virtual PPA**: The PPA price is fixed; if the nodal hub/bus settles below $0.00/MWh, the contract typically stipulates that the Buyer either indemnifies the Seller for negative nodal settlements, or the settlement calculation floors the market price at $0.00/MWh unless economic curtailment was ordered.
  * **Economic Turn-Down Protocol**: The PPA should define clear automated protocol instructions allowing the asset owner to automatically curtail inverter output when real-time LMP is below a contractually agreed negative threshold, preserving project economics.

---

### Actionable Recommendations

* **Audit Contractual Deemed Energy Formula**: Ensure the mathematical formulation for Deemed Generation utilizes calibrated on-site pyranometers/meteorological stations and the pre-agreed degradation curve rather than theoretical P50 estimates.
* **Define Specific Negative Pricing Thresholds**: Incorporate an express clause setting the negative LMP trigger point (e.g., `< -$0.00/MWh` or contract price differential) where automated inverter shutdown is authorized without violating availability guarantees.
* **Standardize RTO Curtailment Safe Harbors**: Limit uncompensated RTO/Reliability curtailment to no more than 50 hours per contract year to preserve project debt service coverage ratios (DSCR).
* **Legal Counsel Verification**: Submit revised contract schedules to outside energy regulatory counsel to confirm compliance with FERC Order 888 open-access rules and relevant RTO market tariff updates.

### Example 2: Trend & Comparative Analysis
**User:** "Analyze contractual availability guarantees, heat rate degradation terms, and environmental attribute transfer rules."

**Agent Response:**
### Executive Summary
**A comprehensive legal and technical review of standard utility Power Purchase Agreement (PPA) provisions confirms that strict alignment between equivalent availability factors (EAF), thermal/efficiency heat rate degradation curves, and unencumbered title transfer of Environmental Attributes (RECs/GHG credits) is vital to risk mitigation. Non-conforming availability shortfall liquidated damages (LDs) and ambiguous heat rate test tolerances expose the off-taker to thermal dispatch cost shifting and market under-recovery. Contractual definitions must clearly establish WREGIS/NEPOOL-GIS/PJM-GATS tracking mechanisms alongside mandatory true-up settlement mechanisms to prevent double-counting and regulatory compliance exposure under FERC and state PUC mandates.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Equivalent Availability Factor (EAF) Guarantee** | 94.20% | 96.50% | -2.38% | **Warning** |
| **Availability Shortfall LD Threshold** | $45.00/MWh-shortfall | Market Replace + $15/MWh | N/A | **Warning** |
| **Heat Rate Degradation Allowance (Annual)** | 1.15%/year | 0.85%/year | +35.29% | **Critical** |
| **Heat Rate Correction Testing Margin** | ±3.50% | ±1.50% (ASME PTC 46) | +133.33% | **Critical** |
| **Environmental Attribute Title Transfer Rate** | 100% Unbundled | 100% Bundled w/ Unit | 0.00% | **Normal** |
| **REC Delivery Failure Remedy (True-Up Penalty)** | Fixed $25.00/REC | Alternative Compliance Payment (ACP) Equivalent | -44.44% | **Critical** |
| **Force Majeure Outage Exclusion Window** | 180 Days Max | 90 Days Max | +100.00% | **Warning** |

---

### Key Contractual Review Dimensions

#### 1. Contractual Availability Guarantees & Liquidated Damages
* **Measurement Standard**: Governed by IEEE Standard 762 definitions for Equivalent Availability Factor (EAF) and Equivalent Forced Outage Rate (EFOR).
* **Planned Outage Windows**: Restrict major overhauls and planned outages to low-demand off-peak shoulder months (typically March–May, September–November) with a 60-day advance scheduling notice.
* **Liquidated Damages Mechanism**: Availability shortfalls below the guaranteed baseline must be calculated on an hourly replacement power cost basis ($\max(0, \text{Real-Time LMP} - \text{PPA Strike Price}) \times \text{Shortfall MWh}$) plus capacity deficiency penalties rather than fixed nominal rates.

#### 2. Heat Rate Degradation Terms & Efficiency Benchmarks
* **Degradation Profiles**: Ensure heat rate degradation schedules follow manufacturer warranty curves (e.g., OEM degradation curves) rather than linear over-approximations. Cumulative degradation caps must be enforced (e.g., maximum allowable heat rate increase not to exceed $4.5\%$ over a 20-year term).
* **Performance Testing Protocol**: Mandate annual heat rate performance verification conducted in accordance with ASME PTC 46 (Overall Plant Performance) under ISO standard ambient conditions (59°F, 14.7 psia, 60% relative humidity), disallowing excessive contractual deadbands.
* **Fuel Pass-Through Protection**: Where fuel costs are passed through to the off-taker, the heat rate used for settlement billing must be capped at the lesser of the actual tested heat rate or the contractually guaranteed degradation curve.

#### 3. Environmental Attribute Transfer Rules & Regulatory Title
* **Bundled Transfer Scope**: Legal definitions must grant the buyer 100% right, title, and interest in all current and future Environmental Attributes, including Renewable Energy Certificates (RECs), carbon offsets, capacity rights, Clean Air Act Section 111 credits, and avoided GHG emissions associated with net generation.
* **Tracking System Conveyance**: Expressly obligate the seller to register, transfer, and deliver certificates through the designated regional tracking system (e.g., WREGIS, PJM-GATS, NEPOOL-GIS, ERCOT REC) by the 15th business day of the month following the generation month.
* **Warranty of Title & Indemnification**: Seller must provide explicit representations that all attributes are transferred free and clear of all liens, encumbrances, claims, or double-selling under competing compliance regimes (e.g., RPS, Clean Energy Standard, voluntary corporate claims).

---

### Visualization Triggers

```json
{
  "chart_type": "line",
  "title": "Contractual Performance & Degradation Multi-Year Profile",
  "data": {
    "labels": ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 10", "Year 15", "Year 20"],
    "datasets": [
      {
        "label": "Contractual Availability Guarantee (%)",
        "data": [98.0, 97.5, 97.0, 96.5, 96.0, 95.0, 94.0, 93.0],
        "borderColor": "#1f77b4"
      },
      {
        "label": "Heat Rate Degradation Curve (MMBtu/MWh)",
        "data": [7.20, 7.27, 7.34, 7.42, 7.49, 7.85, 8.21, 8.57],
        "borderColor": "#ff7f0e"
      },
      {
        "label": "REC Delivery Obligation (%)",
        "data": [100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0, 100.0],
        "borderColor": "#2ca02c"
      }
    ]
  }
}
```

---

### Actionable Recommendations

* **Amend Section 6.2 (Availability LDs)**: Redraft liquidated damage calculation formula from the static $45/MWh rate to an indexed market-replacement cost framework incorporating applicable RTO/ISO capacity deficiency charges.
* **Tighten Heat Rate Testing Clauses (Exhibit C)**: Re-index testing tolerances to ASME PTC 46 standards (±1.5%) and cap fuel pass-through settlements at the guaranteed degradation baseline.
* **Standardize REC Default Clauses (Section 11.4)**: Require replacement of defaulted RECs with equivalent vintage/eligibility attributes within 30 days, or apply an LD benchmarked to 120% of the prevailing state RPS Alternative Compliance Payment (ACP).
* **Limit Force Majeure Extended Relief**: Reduce the unilateral Force Majeure termination threshold from 180 consecutive days to 90 cumulative days per contract year to mitigate stranded capacity obligations.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "operation": "PPA_CONTRACTUAL_AMENDMENT_SUBMISSION",
  "action_details": {
    "target_agreement": "Master Power Purchase Agreement (PPA)",
    "proposed_modifications": [
      "Update Section 6.2 Availability Liquidated Damages to RTO Index + Capacity Offset",
      "Amend Exhibit C Heat Rate Degradation cap to 0.85%/yr with ASME PTC 46 verification",
      "Update Section 11.4 REC True-Up to match 120% State PUC ACP default remedy"
    ],
    "financial_exposure_mitigation_est": "$1,420,000 / Contract Year",
    "approval_required_from": "Office of General Counsel & VP of Power Procurement"
  },
  "status": "PENDING_HUMAN_IN_THE_LOOP_CONFIRMATION"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Flag non-standard indemnification language in Section 14.2 of the Wind PPA and route to General Counsel for legal revision."

**Agent Response:**
### Executive Summary
**A legal review of Section 14.2 (Indemnification) within the proposed Wind Power Purchase Agreement (PPA) identified critical non-standard risk-allocation provisions that deviate significantly from utility procurement benchmarks.** **Specifically, the clause contains an asymmetric, uncapped indemnification burden on the buyer, lacks a mutual waiver of consequential damages, and fails to incorporate standard gross negligence/willful misconduct carve-outs.** **Immediate routing to General Counsel is required to redline Section 14.2 prior to commercial execution.**

---

### Data Presentation: Legal Risk & Clause Benchmark Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Indemnification Cap Liability** | Uncapped ($0 limit) | 100% of Contract Value Cap ($25.0M) | N/A (Infinite Exposure) | **Critical** |
| **Consequential Damages Exclusion** | Silent / Excluded from Clause | Mutual Express Waiver Required | -100.0% | **Critical** |
| **Gross Negligence / Misconduct Carve-Out** | Unilateral (Seller Only) | Mutual Standard Carve-Out | -50.0% | **Warning** |
| **Environmental & Curtailment Indemnity** | Buyer-Allocated ($4.2M est.) | Seller Responsibility ($0.0M) | +100.0% | **Critical** |
| **PPA Legal Risk Score (0-100 scale)** | 88 / 100 | ≤ 25 / 100 (Standard PPA Risk) | +252.0% | **Critical** |

---

### Visualization Trigger: Legal Risk Profile by Clause Area

```json
{
  "chart_type": "radar",
  "data_json": {
    "categories": [
      "Liability Cap Exposure",
      "Consequential Damages",
      "Environmental Indemnity",
      "IP / Grid Interconnection",
      "Mutual Gross Negligence"
    ],
    "series": [
      {
        "name": "Standard PPA Benchmark",
        "values": [20, 15, 10, 20, 15]
      },
      {
        "name": "Wind PPA Section 14.2 (Proposed)",
        "values": [95, 90, 85, 60, 80]
      }
    ]
  }
}
```

---

### Actionable Recommendations

* **Transmit Redline Draft to Legal**: Route Section 14.2 to General Counsel with proposed standard Edison Electric Institute (EEI) / utility-standard mutual indemnification language.
* **Insert Consequential Damages Waiver**: Mandate an explicit mutual waiver for special, indirect, incidental, punitive, or consequential damages (including lost profits).
* **Cap Aggregate Indemnification Liability**: Establish a strict aggregate ceiling capped at twelve (12) months of rolling contract revenue or a negotiated fixed dollar amount ($25,000,000).
* **Align Environmental & Curtailment Risk**: Reassign all environmental compliance, avian mitigation, and pre-COD grid interconnection liabilities exclusively to the Seller.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "ROUTING_TO_GENERAL_COUNSEL_FOR_PPA_REVISION",
  "document_id": "PPA-WIND-2024-SEC14.2",
  "target_recipient": "General Counsel / Support Services Legal Division",
  "flagged_provisions": [
    "Section 14.2.1: Uncapped Buyer Indemnification Obligation",
    "Section 14.2.3: Absence of Mutual Consequential Damages Waiver",
    "Section 14.2.5: Asymmetrical Environmental Liability Allocation"
  ],
  "proposed_redline_action": "Substitute with EEI Standard Form Power Purchase Agreement Mutual Indemnification Model Clause",
  "human_approval_required": true,
  "status": "PENDING_LEGAL_OFFICER_SIGN_OFF"
}
```
