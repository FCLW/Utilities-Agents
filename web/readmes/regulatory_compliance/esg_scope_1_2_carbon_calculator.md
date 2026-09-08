# ⚡ Esg Scope 1 2 Carbon Calculator

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of esg scope 1 2 carbon calculator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Esg Scope 1 2 Carbon Calculator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank esg scope 1 2 carbon calculator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.esg_scope_1_2_carbon_calculator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What are our utility's total Scope 1 direct greenhouse gas emissions from fossil generation and SF6 circuit breaker leakages this year?"

**Agent Response:**
### Executive Summary
**Our utility's YTD Scope 1 direct greenhouse gas emissions total 1,596,350 Metric Tons of $\text{CO}_2\text{e}$ ($\text{MT CO}_2\text{e}$), driven predominantly by stationary fossil-fuel generation ($1,557,500\text{ MT CO}_2\text{e}$) and $\text{SF}_6$ switchgear insulation leakage ($24,650\text{ MT CO}_2\text{e}$). While combined-cycle generation and $\text{SF}_6$ transmission leak rates remain within EPA Subpart DD compliance margins (leak rate at $1.18\%$ vs. the $1.5\%$ federal threshold), simple-cycle peaking units experienced a $+7.76\%$ overshoot above target baselines due to unforecasted summer grid heat events.**

---

### Data Presentation: Scope 1 Direct Emissions Breakdown

The following quantitative inventory represents direct emissions calculated in accordance with the **GHG Protocol Corporate Accounting and Reporting Standard** and **EPA 40 CFR Part 98 (Subparts C, D, and DD)**.

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Natural Gas Combined Cycle (CCGT) Generation** | $1,245,000\text{ MT CO}_2\text{e}$ | $1,350,000\text{ MT CO}_2\text{e}$ | $-7.78\%$ | **Normal** |
| **Simple-Cycle Peaker Turbines (SCGT)** | $312,500\text{ MT CO}_2\text{e}$ | $290,000\text{ MT CO}_2\text{e}$ | $+7.76\%$ | **Warning** |
| **$\text{SF}_6$ Transmission Breakers ($>115\text{ kV}$ Leakage)** | $18,450\text{ MT CO}_2\text{e}$ | $22,000\text{ MT CO}_2\text{e}$ | $-16.14\%$ | **Normal** |
| **$\text{SF}_6$ Substation Distribution Breakers ($<69\text{ kV}$ Leakage)** | $6,200\text{ MT CO}_2\text{e}$ | $7,500\text{ MT CO}_2\text{e}$ | $-17.33\%$ | **Normal** |
| **Station Auxiliary & Fleet Operations** | $14,200\text{ MT CO}_2\text{e}$ | $15,000\text{ MT CO}_2\text{e}$ | $-5.33\%$ | **Normal** |
| **Total Scope 1 Direct GHG Inventory** | **$1,596,350\text{ MT CO}_2\text{e}$** | **$1,684,500\text{ MT CO}_2\text{e}$** | **$-5.23\%$** | **Normal** |

*Note: $\text{SF}_6$ emissions are calculated using a Global Warming Potential (GWP) of $23,500$ (IPCC Fifth Assessment Report / AR5 100-year horizon) under EPA Subpart DD mass-balance methodology.*

---

### Visualization Configuration

A grouped bar chart has been generated to visualize emissions performance across Scope 1 source categories against targeted baseline ceilings:

```json
{
  "chart_type": "bar",
  "title": "YTD Scope 1 Direct GHG Emissions Breakdown (MT CO2e)",
  "categories": [
    "Natural Gas CCGT Generation",
    "Peaker Simple-Cycle Generation",
    "SF6 Transmission Breakers (Leakage)",
    "SF6 Substation Distribution Breakers",
    "Fleet & Auxiliary Operations"
  ],
  "series": [
    {
      "name": "Current YTD (MT CO2e)",
      "data": [1245000, 312500, 18450, 6200, 14200]
    },
    {
      "name": "Target Baseline (MT CO2e)",
      "data": [1350000, 290000, 22000, 7500, 15000]
    }
  ],
  "unit": "MT CO2e"
}
```

---

### Actionable Recommendations

- **Peaking Plant Dispatch Optimization**: Coordinate with Generation Operations and the Energy Trading Desk to evaluate battery energy storage system (BESS) peak-shaving dispatch to mitigate further peaker turbine run-hours before Q4 reconciliation.
- **Continuous $\text{SF}_6$ Monitoring & Sealed Unit Replacement**: Prioritize non-$\text{SF}_6$ (clean air/vacuum/fluoronitrile gas mixture) breaker retrofits for aging $230\text{ kV}$ breakers showing top-quartile top-up pressure cycles.
- **EPA Subpart DD Mandatory Reporting Alignment**: Ensure mass balance logs and cylinder inventory records from field substations are synced into the enterprise ESG ledger ahead of annual FERC Form 1 and EPA Electronic Greenhouse Gas Reporting Tool (e-GGRT) filings.

### Example 2: Trend & Comparative Analysis
**User:** "Calculate Scope 2 indirect carbon emissions resulting from transmission line electrical losses and corporate facility power usage."

**Agent Response:**
### Executive Summary
**Total enterprise Scope 2 indirect greenhouse gas (GHG) emissions for the reporting period are calculated at 81,541.50 Metric Tons $\text{CO}_2\text{e}$ (Location-Based) and 74,810.80 Metric Tons $\text{CO}_2\text{e}$ (Market-Based). Grid transmission and distribution line losses account for 87.18% of total Scope 2 emissions (71,090.80 $\text{MT CO}_2\text{e}$ across 182,284 MWh of dissipation), while corporate facilities and operations centers account for the remaining 12.82% (10,450.70 $\text{MT CO}_2\text{e}$ across 26,796 MWh). Implementation of EAC/REC contractual instruments retired 6,730.70 $\text{MT CO}_2\text{e}$ from corporate facility footprints, driving a 64.4% market-based reduction in administrative facility load.**

---

### Scope 2 Carbon Emissions Quantification Methodology

Calculations adhere to the **GHG Protocol Scope 2 Guidance (amendment to the GHG Protocol Corporate Standard)**, cross-referenced with **EPA eGRID 2024 subregional emission factors** and **FERC Form 1 / Form 714 electrical delivery records**:

$$\text{Emissions } (\text{MT CO}_2\text{e}) = \text{Electricity Consumed / Lost } (\text{MWh}) \times \text{Emission Factor } \left(\frac{\text{MT CO}_2\text{e}}{\text{MWh}}\right)$$

* **Location-Based Emission Factor ($\text{EF}_{\text{loc}}$):** $0.3900\text{ MT CO}_2\text{e/MWh}$ ($859.8\text{ lb CO}_2\text{e/MWh}$ regional grid mix).
* **Market-Based Facility Residual Factor ($\text{EF}_{\text{res}}$):** $0.4120\text{ MT CO}_2\text{e/MWh}$ for unbundled load; $0.0000\text{ MT CO}_2\text{e/MWh}$ for retired Green-e certified RECs / bundled Solar PPAs.
* **T&D Loss Calculation Scope:** Utility-owned transmission and sub-transmission delivery dissipation modeled under Scope 2 Location-Based standards ($2.35\%$ HV losses, $3.42\%$ MV delivery losses).

---

### Data Presentation: Scope 2 Emissions Inventory

| Metric | Current Value | Baseline / Target | Delta (%) | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Transmission Line Losses (230kV–500kV)** | 42,150.80 $\text{MT CO}_2\text{e}$ (108,079 MWh) | 44,500.00 $\text{MT CO}_2\text{e}$ | -5.28% | **Normal** |
| **Distribution Delivery Losses (13.8kV–34.5kV)** | 28,940.00 $\text{MT CO}_2\text{e}$ (74,205 MWh) | 29,800.00 $\text{MT CO}_2\text{e}$ | -2.89% | **Normal** |
| **Corporate HQ & Regional Admin Offices** | 3,420.50 $\text{MT CO}_2\text{e}$ (8,770 MWh) | 4,100.00 $\text{MT CO}_2\text{e}$ | -16.57% | **Normal** |
| **Regional Operations & Dispatch Centers** | 2,180.00 $\text{MT CO}_2\text{e}$ (5,590 MWh) | 2,250.00 $\text{MT CO}_2\text{e}$ | -3.11% | **Normal** |
| **Substation Control & Enterprise Data Centers** | 4,850.20 $\text{MT CO}_2\text{e}$ (12,436 MWh) | 4,400.00 $\text{MT CO}_2\text{e}$ | +10.23% | **Warning** |
| **Gross Scope 2 Emissions (Location-Based)** | **81,541.50 $\text{MT CO}_2\text{e}$** | **85,050.00 $\text{MT CO}_2\text{e}$** | **-4.13%** | **Normal** |
| **Gross Scope 2 Emissions (Market-Based)** | **74,810.80 $\text{MT CO}_2\text{e}$** | **78,200.00 $\text{MT CO}_2\text{e}$** | **-4.33%** | **Normal** |
| **Contractual REC/PPA Scope 2 Offsets** | -6,730.70 $\text{MT CO}_2\text{e}$ (16,337 MWh) | -5,000.00 $\text{MT CO}_2\text{e}$ | +34.61% | **Normal** |

---

### Visualization Triggers

```json
{
  "chart_type": "bar",
  "title": "Scope 2 Emissions Breakdown: Location-Based vs. Market-Based (MT CO2e)",
  "categories": [
    "Corporate HQ",
    "Regional Operations Centers",
    "Data Centers & Substation Control",
    "Transmission Line Losses (HV 230kV-500kV)",
    "Distribution Line Losses (MV 13.8kV-34.5kV)"
  ],
  "series": [
    {
      "name": "Location-Based Emissions (MT CO2e)",
      "data": [3420.5, 2180.0, 4850.2, 42150.8, 28940.0]
    },
    {
      "name": "Market-Based Emissions (MT CO2e)",
      "data": [1120.0, 950.0, 1650.0, 42150.8, 28940.0]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Mitigate Substation Data Center Load Growth (+10.23% vs Baseline):**
   * Execute immediate HVAC and compute workload consolidation audits across Tier-3 operational data centers.
   * Procure additional Green-e certified bundled renewable PPAs to bridge the 3,200.20 $\text{MT CO}_2\text{e}$ unhedged data center exposure.

2. **Transmission Efficiency & Conductor Optimization:**
   * Prioritize reconductoring on high-loss corridors (feeder segments experiencing $>3.8\%$ dissipation) with High-Temperature Low-Sag (HTLS) composite-core conductors to lower gross T&D thermal losses by an estimated $12\text{–}15\%$.
   * Dispatch static VAR compensators (SVCs) and optimize substation capacitor bank switching to improve power factor ($\ge 0.98$), reducing reactive current dissipation.

3. **Regulatory Filing Alignment (FERC Form 1 & CDP/ESG Disclosures):**
   * Synchronize the dual-reporting tables (Location vs. Market methods) directly with FERC Form 1 (Pages 401a-401b) transmission loss accounts and submit to the enterprise ESG assurance team for third-party ISO 14064-3 verification.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate the annual ESG sustainability disclosure table aligned with SASB and TCFD reporting standards for stakeholder review."

**Agent Response:**
### Executive Summary
**Annual enterprise Greenhouse Gas (GHG) accounting indicates total Scope 1 direct emissions of 1,157,000 MT $\text{CO}_2\text{e}$ and market-based Scope 2 indirect emissions of 98,500 MT $\text{CO}_2\text{e}$ for the reporting cycle, achieving an overall 24.9% reduction against the 2020 baseline.** **All evaluated categories meet or outperform SASB Electric Utilities & Power Generators standard (IF-EU-110a) and TCFD Metrics & Targets climate milestones, driven primarily by heat-rate efficiency improvements in thermal generation and increased renewable energy certificate (REC) retirements.** **Fugitive $\text{SF}_6$ switchgear leak rates decreased to 0.58%, maintaining full compliance well below regulatory threshold limits.**

---

### Data Presentation: SASB & TCFD Sustainability Disclosure

The quantitative inventory follows the **GHG Protocol Corporate Accounting and Reporting Standard**, mapped to **SASB (IF-EU-110a)** and **TCFD Climate Disclosure Metrics**:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Global Scope 1 Emissions** (*SASB IF-EU-110a.1 / TCFD Direct*) | 1,157,000 MT $\text{CO}_2\text{e}$ | 1,486,500 MT $\text{CO}_2\text{e}$ (Baseline) | -22.17% | **Normal** |
| — *Stationary Combustion (Generation Assets)* | 1,110,000 MT $\text{CO}_2\text{e}$ | 1,150,000 MT $\text{CO}_2\text{e}$ (Target) | -3.48% | **Normal** |
| — *Mobile Fleet Combustion* | 36,200 MT $\text{CO}_2\text{e}$ | 38,000 MT $\text{CO}_2\text{e}$ (Target) | -4.74% | **Normal** |
| — *Fugitive $\text{SF}_6$ Gas Insulated Switchgear* | 10,800 MT $\text{CO}_2\text{e}$ | 12,000 MT $\text{CO}_2\text{e}$ (Target) | -10.00% | **Normal** |
| **Scope 2 Indirect (Location-Based)** (*SASB IF-EU-110a.1 / TCFD Indirect*) | 142,000 MT $\text{CO}_2\text{e}$ | 150,000 MT $\text{CO}_2\text{e}$ (Target) | -5.33% | **Normal** |
| **Scope 2 Indirect (Market-Based)** (*TCFD Indirect w/ EACs/RECs*) | 98,500 MT $\text{CO}_2\text{e}$ | 110,000 MT $\text{CO}_2\text{e}$ (Target) | -10.45% | **Normal** |
| **Total Net Scope 1 & 2 Emissions (Market-Based)** | 1,255,500 MT $\text{CO}_2\text{e}$ | 1,310,000 MT $\text{CO}_2\text{e}$ (Target) | -4.16% | **Normal** |
| **GHG Intensity per Net Generation** (*SASB IF-EU-110a.1*) | 0.382 MT $\text{CO}_2\text{e}$ / MWh | 0.410 MT $\text{CO}_2\text{e}$ / MWh (Target) | -6.83% | **Normal** |
| **Fugitive $\text{SF}_6$ Leak Rate** (*EPA Subpart DD / SASB*) | 0.58% | 1.00% (Regulatory Ceiling) | -42.00% | **Normal** |
| **Covered Emissions under Cap-and-Trade / Carbon Pricing** (*SASB IF-EU-110a.2*) | 95.9% | 100.0% (Target Coverage) | -4.10% | **Normal** |

---

### Visualization Trigger: Scope 1 & 2 Emissions Profile

A **Grouped Bar Chart** compares baseline metrics, interim compliance targets, and verified operational emissions across all material scopes.

```json
{
  "chart_type": "bar",
  "title": "Annual ESG Scope 1 & 2 Carbon Inventory vs. Targets",
  "categories": [
    "Stationary Combustion (Scope 1)",
    "Fleet & Mobile (Scope 1)",
    "Fugitive SF6 Emissions (Scope 1)",
    "Scope 2 (Location-Based)",
    "Scope 2 (Market-Based)",
    "Total Net Scope 1 & 2 (Market)"
  ],
  "series": [
    {
      "name": "Baseline (2020) [MT CO2e]",
      "data": [1420000, 48000, 18500, 210000, 185000, 1671500]
    },
    {
      "name": "Target (2024) [MT CO2e]",
      "data": [1150000, 38000, 12000, 150000, 110000, 1310000]
    },
    {
      "name": "Current Reporting Period (2024) [MT CO2e]",
      "data": [1110000, 36200, 10800, 142000, 98500, 1255500]
    }
  ]
}
```

---

### Actionable Recommendations

- **Third-Party Assurance Engagement**: Submit the consolidated Scope 1 continuous emission monitoring system (CEMS) telemetry logs and Scope 2 utility billing reconciliations to the accredited external verifier for ISO 14064-3 limited assurance sign-off.
- **$\text{SF}_6$ Replacement Lifecycle Acceleration**: Maintain the substation breaker refurbishment schedule in Grid Zone 4 to replace aging high-voltage $\text{SF}_6$ equipment with vacuum and fluoronitrile-based alternatives ahead of state phasedown mandates.
- **REC Registry Retirement**: Lock the 43,500 MWh equivalent bundled renewable energy certificates (RECs) in the regional tracking system (e.g., M-RETS/WREGIS) to substantiate the market-based Scope 2 accounting adjustments.
- **Stakeholder Disclosure Publication**: Incorporate these finalized tables into the upcoming TCFD Index and SASB Performance Tables of the Enterprise Annual Sustainability Report.

---

### [TIER 2 ACTION REQUIRED]
Formal submission and public filing of ESG regulatory disclosures with external governing bodies (e.g., EPA e-GGRT, state public utility commissions, or published investor decks) require human authorization.

```json
{
  "tier_2_action": "ESG_ANNUAL_DISCLOSURE_SUBMISSION",
  "disclosure_year": 2024,
  "scope_1_mt_co2e": 1157000,
  "scope_2_market_mt_co2e": 98500,
  "verification_status": "PENDING_AUDIT_SIGN_OFF",
  "requires_approval_by": ["Director_Environmental_Compliance", "Chief_Sustainability_Officer"]
}
```
