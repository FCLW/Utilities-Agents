# ⚡ Capital Replacement Simulator

![Domain](https://img.shields.io/badge/Domain-asset%20management-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of capital replacement simulator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Capital Replacement Simulator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank capital replacement simulator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_asset_management.capital_replacement_simulator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which aging 230kV substation transformers have crossed the 35-year threshold and qualify for immediate capital replacement?"

**Agent Response:**
### Executive Summary
**A fleet assessment of 230kV substation power transformers identified 4 critical units exceeding the 35-year operational design threshold, representing elevated risk of dielectric failure and forced outages.** **Among these, 2 units exhibit advanced dissolved gas analysis (DGA) degradation and asset health index (AHI) scores below 45, requiring prioritized capital replacement authorization.** **Immediate procurement lead-time mitigation and capital allocation of approximately $18.4M are recommended to prevent unserved energy events across critical bulk electric system transmission corridors.**

---

### Data Presentation

#### Asset Fleet Replacement Summary
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Units Exceeding Threshold (≥35 Yrs)** | 4 Units | 0 Units (>35 Yrs) | +100.0% | **Critical** |
| **Average Age of Flagged Fleet** | 38.5 Years | 35.0 Years Max | +10.0% | **Critical** |
| **Average Asset Health Index (AHI)** | 48.0 / 100 | ≥ 70.0 / 100 | -31.4% | **Critical** |
| **Combined Critical DGA Acetylene ($C_2H_2$)** | 3.8 ppm | < 1.0 ppm | +280.0% | **Critical** |
| **Total Estimated Replacement CapEx** | $18.4M | $15.0M CapEx Reserve | +22.7% | **Warning** |

#### Detailed Asset Breakdown (230kV Transformers ≥ 35 Years)

| Asset ID | Substation / Bay | Age (Yrs) | Health Index (0-100) | DGA Condition | Criticality Rating | Est. Lead Time | Est. CapEx ($M) | Qualification Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **XFMR-230-0101** | Riverside Substation (Bay 1) | 42 | 38 | High Acetylene / Thermal Overheating | High (Bulk Grid Tier 1) | 18 Months | $4.8M | **Immediate Replacement** |
| **XFMR-230-0144** | Westlake Substation (Bay 2) | 39 | 44 | Severe Furans / Paper Degradation | High (Bulk Grid Tier 1) | 16 Months | $4.6M | **Immediate Replacement** |
| **XFMR-230-0209** | Oakhaven Substation (Bay 1) | 37 | 52 | Elevated Hydrogen & Methane | Medium (Transmission Tier 2) | 14 Months | $4.5M | **Planned Replacement (FY26)** |
| **XFMR-230-0312** | Pinecrest Substation (Bay 3) | 36 | 58 | Moderate Arcing Trace | Medium (Transmission Tier 2) | 14 Months | $4.5M | **Planned Replacement (FY26)** |

---

### Visualization Trigger
- **Recommended Chart**: Categorical Bar Chart / Risk Matrix (Asset Age & Health Score vs. Regulatory Baseline).
- **Backend Configuration**:

```json
{
  "chart_type": "bar",
  "title": "230kV Transformer Fleet Age vs Replacement Threshold",
  "xAxis": "Transformer Unit / Substation",
  "yAxis": "Age (Years)",
  "threshold": 35,
  "series": [
    {
      "name": "Unit Age",
      "data": [
        {"substation": "Riverside Sub 230kV - T1", "age": 42, "health_index": 38, "status": "Critical"},
        {"substation": "Westlake Sub 230kV - T2", "age": 39, "health_index": 44, "status": "Critical"},
        {"substation": "Oakhaven Sub 230kV - T1", "age": 37, "health_index": 52, "status": "Warning"},
        {"substation": "Pinecrest Sub 230kV - T3", "age": 36, "health_index": 58, "status": "Warning"}
      ]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Expedite Procurement Requisitions**: Initiate long-lead capital procurement for **XFMR-230-0101** (Riverside Substation) and **XFMR-230-0144** (Westlake Substation) due to critical paper insulation decay and high thermal stress.
2. **Implement Interim N-1 Redundancy Protocols**: Increase DGA dissolved gas monitoring from semi-annual to bi-weekly automated online monitoring for the 4 identified units.
3. **Engineering Outage Scheduling**: Coordinate with the Transmission System Operator (TSO) to schedule standard clearance windows in Q1/Q2 of next fiscal year to execute physical civil work and unit swap.
4. **Capital Budget Adjustment**: Request an allocation adjustment from the Capital Planning Committee to cover the $9.4M immediate commitment for Phase 1 replacement.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CAPITAL_ASSET_REPLACEMENT_AUTHORIZATION",
  "scope": "230kV_BULK_TRANSMISSION_TRANSFORMERS",
  "affected_assets": [
    "XFMR-230-0101 (Riverside Substation - 230kV)",
    "XFMR-230-0144 (Westlake Substation - 230kV)"
  ],
  "total_capex_commitment_usd": 9400000,
  "action_description": "Authorize formal capital project initiation and advance manufacturing reservation for two (2) 230kV/115kV autotransformers exceeding the 35-year operational lifecycle limit.",
  "approval_required": true,
  "approver_role": "Director of Substation Engineering & Transmission Capital Asset Planning"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Compare the 10-year lifecycle replacement cost of SF6 gas-insulated breakers versus vacuum circuit breakers."

**Agent Response:**
### Executive Summary
**A 10-year Total Cost of Ownership (TCO) simulation indicates that Vacuum Circuit Breakers (VCBs) deliver a ~37.5% net lifecycle cost reduction compared to equivalent $\text{SF}_6$ gas-insulated circuit breakers in medium-voltage and sub-transmission classes ($15\text{ kV} - 38\text{ kV}$). While initial procurement and commissioning costs are comparable, $\text{SF}_6$ technology incurs substantial operational premiums due to mandated fugitive emissions monitoring (EPA 40 CFR Part 98 Subpart DD), specialized gas handling/cart certification, and end-of-life degasification/disposal liabilities.**

---

### Data Presentation

The table below summarizes the standardized per-unit 10-year lifecycle cost simulation model evaluated under utility fleet asset management parameters (discount rate / WACC: $6.5\%$).

| Metric | Current Value ($\text{SF}_6$ Baseline) | Baseline / Target (Vacuum Alternative) | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Initial CapEx & Installation** | $\$45,000$ | $\$42,000$ | $-6.67\%$ | Normal |
| **10-Yr Routine Maintenance & Testing** | $\$18,000$ | $\$9,000$ | $-50.00\%$ | Warning |
| **$\text{SF}_6$ Gas Leak Management & Compliance** | $\$14,500$ | $\$0$ | $-100.00\%$ | Critical |
| **Decommissioning & Reclamation Provision** | $\$6,500$ | $\$1,500$ | $-76.92\%$ | Warning |
| **10-Year Cumulative Lifecycle Cost** | $\$84,000$ | $\$52,500$ | $-37.50\%$ | Warning |
| **Annual Failure Probability ($P_f$)** | $0.85\%$ | $0.42\%$ | $-50.59\%$ | Normal |
| **Scope 1 GHG Direct Liability ($\text{tCO}_2\text{e}$)** | $47.8\text{ tCO}_2\text{e}$ | $0.0\text{ tCO}_2\text{e}$ | $-100.00\%$ | Critical |

*Analytical Assumptions:* 
- Voltage Class: $15\text{ kV} - 38\text{ kV}$ outdoor substation class breakers.
- $\text{SF}_6$ Global Warming Potential (GWP): $23,500 \times \text{CO}_2$.
- Annualized $\text{SF}_6$ leak rate modeled at standard utility industry average of $0.5\% - 1.0\%$ per annum under IEEE C37 and EPA GHG guidelines.

---

### Visualization Triggers

**Recommended Visualization:** Grouped Bar Chart / Cumulative Cost-Over-Time Step Chart comparing initial CapEx, OpEx maintenance intervals, regulatory burden, and residual salvage/decommissioning cost trajectories.

```json
{
  "chart_type": "bar",
  "title": "10-Year Lifecycle Cost Breakdown: SF6 vs. Vacuum Circuit Breakers (Per Unit)",
  "categories": [
    "Initial CapEx & Install",
    "Routine Maintenance & Testing",
    "SF6 Gas Compliance & Leak Management",
    "Decommissioning & Disposal Reserve",
    "Total 10-Year Lifecycle Cost"
  ],
  "series": [
    {
      "name": "SF6 Gas-Insulated Breaker ($k)",
      "data": [45.0, 18.0, 14.5, 6.5, 84.0]
    },
    {
      "name": "Vacuum Circuit Breaker ($k)",
      "data": [42.0, 9.0, 0.0, 1.5, 52.5]
    }
  ],
  "units": "Thousands USD ($k)"
}
```

---

### Actionable Recommendations

- **Standardize Procurement Specifications to Vacuum Interrupters:** Transition utility capital standards for all planned medium-voltage ($\le 38\text{ kV}$) and applicable sub-transmission replacement programs to vacuum interrupter technology (or dry-air/clean-air eco-GIS where GIS footprint constraints exist).
- **Accelerate $\text{SF}_6$ Phase-Out Prioritization:** Run asset health indices (AHI) across existing substation $\text{SF}_6$ inventory; prioritize units showing micro-leaks or nearing major 10-to-15 year seal-overhaul milestones for complete vacuum replacement rather than life-extension rebuilds.
- **Update Depreciation & Decommissioning Reserves:** Re-evaluate utility salvage and retirement reserves for active $\text{SF}_6$ inventory to account for escalating certified gas recovery, destruction, and regulatory reporting costs.
- **Execute Fleet-Wide Breaker Portfolio Simulation:** Ingest substation-specific telemetry from BigQuery to generate feeder-by-feeder multi-year capital replacement schedules.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "CAPITAL_ALLOCATION_POLICY_MODIFICATION",
  "scope": "Substation Fleet Asset Management",
  "proposed_change": "Update 5-Year Capital Replacement Plan standard to mandate Vacuum Circuit Breakers across all 15 kV-38 kV distribution/sub-transmission substations, restricting SF6 procurement to exception-only high-voltage applications (>72.5 kV).",
  "financial_impact_estimate": "Estimated 10-year net fleet OpEx/CapEx savings of $31,500 per replaced breaker unit across fleet replacement candidates.",
  "approval_level_required": "VP of Grid Engineering / Chief Asset Officer (HITL Approval Required)"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Stage a prioritized FY27 capital asset replacement schedule for board review and regulatory rate case inclusion."

**Agent Response:**
### Executive Summary
**The FY27 Capital Asset Replacement Simulation has prioritized $150.0M across 2,135 high-criticality grid assets reaching end-of-life (EOL) or severe degradation thresholds (Health Index < 40). Implementing this replacement schedule will mitigate an estimated $412M in potential unserved energy, environmental liability, and catastrophic failure penalties across transmission and distribution nodes. Staging this capital expenditure fulfills IEEE C57/C37 reliability requirements and provides defensible actuarial-backed justification for inclusion in the upcoming General Rate Case (GRC) filing.**

---

### Key Program Metrics & Baseline Performance

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Simulated FY27 Replacement Capex** | $150.0M | $135.0M | +11.1% | **Warning** (Budget Adjustment Required) |
| **Substation Power Transformers Health (<40 HI)** | 38 units | 15 units | +153.3% | **Critical** |
| **Circuit Breakers (SF6 / Vacuum EOL)** | 142 units | 60 units | +136.7% | **Critical** |
| **Underground PILC/Direct-Burial XLPE Cable** | 210 miles | 120 miles | +75.0% | **Warning** |
| **Wood Utility Poles (Class 1-4 Structural Defect)**| 1,250 poles | 800 poles | +56.3% | **Warning** |
| **Electromechanical P&C Relay Modernization** | 315 packages | 300 packages | +5.0% | **Normal** |
| **SAIDI Risk Reduction Benefit** | 18.4 min/cust/yr | 12.0 min/cust/yr | +53.3% | **Normal** (Positive Impact) |

---

### FY27 Asset Replacement Prioritization Portfolio (Board & Rate Case Staging)

| Asset Category | Target Units | Avg. Asset Age (Yrs) | Avg. Health Index (0-100) | Failure Prob. (5-Yr) | Estimated Capex ($M) | Regulatory Justification (FERC/PUC Account) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Substation Transformers (115kV/230kV)** | 38 | 47.8 | 32.4 | 42.1% | $48.5M | FERC Acct 353 (Station Equipment / NERC TPL-001) |
| **High-Voltage Circuit Breakers** | 142 | 41.2 | 36.1 | 38.4% | $32.4M | FERC Acct 353 (F-Gas Reduction & Arc Safety) |
| **Underground Cable (PILC/Vintage XLPE)** | 210 mi | 39.5 | 38.0 | 31.2% | $28.8M | FERC Acct 367 (Distribution Reliability / IEEE 400) |
| **Structural Distribution Poles & Crossarms** | 1,250 | 52.1 | 34.7 | 27.5% | $19.2M | FERC Acct 364 (GO 95 / NESC Structural Compliance) |
| **Microprocessor P&C Relay Upgrades** | 315 | 34.0 | 39.8 | 29.0% | $12.6M | FERC Acct 353 (CIP-005/007 & NERC PRC-005) |
| **Automated Reclosers & Sectionalizers** | 180 | 28.5 | 44.0 | 22.0% | $8.5M | FERC Acct 368 (Grid Modernization / FLISR Enablement) |
| **Total** | **2,135** | — | — | — | **$150.0M** | **Rate Base Capital Addition** |

---

### Visualization Trigger: FY27 Capital Replacement Allocation

```json
{
  "chart_type": "bar",
  "title": "FY27 Capital Asset Replacement Capex Allocation & Risk Priority",
  "categories": [
    "Substation Power Transformers",
    "SF6 & Vacuum Circuit Breakers",
    "Underground Cable & Conduits (PILC/XLPE)",
    "Wood Utility Poles & Crossarms",
    "Protection & Control (P&C) Relays",
    "Distribution Automation Reclosers"
  ],
  "series": [
    {
      "name": "Target Replacement Capex ($M)",
      "data": [48.5, 32.4, 28.8, 19.2, 12.6, 8.5]
    },
    {
      "name": "High-Risk Asset Units (Count)",
      "data": [38, 142, 210, 1250, 315, 180]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Board Review Dossier Assembly**: Submit the prioritized schedule alongside DGA (Dissolved Gas Analysis) histories and Weibull asset survival curves to validate the 38 transformer replacements.
2. **Rate Case Testimony Preparation**: Structure capital additions under FERC Accounts 353, 364, and 367 with explicit ties to NERC reliability criteria (PRC-005, TPL-001) and state-mandated wildfire/storm hardening metrics.
3. **Long-Lead Procurement Staging**: Initiate preliminary RFP specifications for EHV substation power transformers (lead times currently exceeding 96–120 weeks) to lock in production queue slots.
4. **Coordination with Outage Planning**: Sequence circuit breaker and relay replacements during shoulder months (Q2/Q4 FY27) to maintain N-1 system security without derating adjacent transmission corridors.

---

### [TIER 2 ACTION REQUIRED]

```yaml
action_type: "CAPITAL_BUDGET_AUTHORIZATION_AND_RATE_CASE_FILING"
target_fiscal_year: 2027
total_capex_staged_usd: 150000000.00
impacted_accounts:
  - "FERC 353: Transmission Station Equipment"
  - "FERC 364: Distribution Poles, Towers & Fixtures"
  - "FERC 367: Underground Conductors & Devices"
critical_approvals_required:
  - "Chief Financial Officer (CFO)"
  - "VP of Asset Management & Grid Engineering"
  - "Regulatory Affairs Director"
confirmation_status: "PENDING_HUMAN_IN_THE_LOOP_APPROVAL"
description: "Authorizes the finalization of the FY27 Capital Asset Replacement portfolio for board sign-off and inclusion in the upcoming jurisdictional Rate Case Filing."
```
