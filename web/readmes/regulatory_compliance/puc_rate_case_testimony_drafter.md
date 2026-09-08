# ⚡ Puc Rate Case Testimony Drafter

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of puc rate case testimony drafter is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Puc Rate Case Testimony Drafter Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank puc rate case testimony drafter events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.puc_rate_case_testimony_drafter_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What capital investments in grid modernization and wildfire hardening must be justified in our upcoming state PUC General Rate Case?"

**Agent Response:**
### Executive Summary
**For the upcoming state Public Utilities Commission (PUC) General Rate Case (GRC), the enterprise must justify $1,356.9M in cumulative capital expenditures (CapEx) focused on High Fire-Threat District (HFTD) grid hardening and digital modernization.** **Prudence justification requires demonstrating direct risk-spend efficiency (RSE), verified reductions in ignition probability, and compliance with state Wildfire Mitigation Plan (WMP) mandates.** **Substantiating these investments is vital to defending rate base inclusion, preventing disallowances, and sustaining safe, reliable grid operations under increasing climate exposure.**

---

### Data Presentation

The table below outlines the core grid modernization and wildfire hardening capital programs requiring direct testimony justification for the upcoming Test Year (TY) GRC filing:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Targeted Undergrounding (Circuit Miles)** | 260.0 mi ($520.0M) | 90.0 mi ($180.0M) | +188.9% | **Warning** |
| **Covered Conductor Retrofit (Circuit Miles)** | 691.0 mi ($345.5M) | 240.0 mi ($120.0M) | +187.9% | **Warning** |
| **ADMS / DERMS Grid Modernization ($M)** | $185.0M | $75.0M | +146.7% | **Normal** |
| **Microgrids & Substation Hardening ($M)** | $165.8M | $80.0M | +107.3% | **Normal** |
| **Fast-Trip Reclosers & Sectionalizers (Units)** | 1,155 units ($92.4M) | 560 units ($45.0M) | +105.3% | **Normal** |
| **LiDAR, HD Cameras & AI Inspection ($M)** | $48.2M | $22.0M | +119.1% | **Normal** |
| **Total Hardening & Modernization Rate Base** | **$1,356.9M** | **$522.0M** | **+159.9%** | **Warning** |

*Note: Baseline reflects the prior approved GRC cycle rate-base authorized spend. Deltas reflect incremental capital required to address elevated risk scoring and revised state fire-threat mapping.*

---

### Visualization Triggers

**Recommended Chart Type:** Grouped Bar Chart (Programmatic Capital Allocation: Proposed vs. Baseline)

```json
{
  "chart_type": "bar",
  "title": "PUC GRC Capital Hardening & Modernization Request vs. Authorized Baseline",
  "data_json": {
    "categories": [
      "Covered Conductor Retrofit",
      "Undergrounding High-Risk Circuits",
      "Advanced Distribution Mgmt (ADMS/DERMS)",
      "Automated Reclosers & Sectionalizing",
      "Vegetation LiDAR & AI Inspection",
      "Substation Hardening & Microgrids"
    ],
    "series": [
      {
        "name": "Proposed GRC Capex ($M)",
        "data": [345.5, 520.0, 185.0, 92.4, 48.2, 165.8]
      },
      {
        "name": "Historical Baseline ($M)",
        "data": [120.0, 180.0, 75.0, 45.0, 22.0, 80.0]
      }
    ]
  }
}
```

---

### Key Program Testimonial Justifications

1. **Covered Conductor Installation (Overhead Hardening)**
   - *Testimony Focus:* Evidence of 90%+ contact-from-object ignition risk reduction in Tier 2/Tier 3 High Fire Threat Districts; life-cycle cost-benefit analysis against full undergrounding.
2. **Targeted Undergrounding in Extreme Threat Corridors**
   - *Testimony Focus:* Justification of high-cost corridors based on topography, egress constraints, and severe wind-loading zones where overhead mitigation fails to achieve safety margins.
3. **Advanced Protection (Fast-Trip / Enhanced Powerline Safety Settings - EPSS)**
   - *Testimony Focus:* Deployment of microsecond-sensing reclosers and sectionalizers that extinguish faults before ground arcing can trigger ignitions.
4. **Digital Grid Modernization (ADMS, FLISR, & DERMS)**
   - *Testimony Focus:* Real-time fault location, isolation, and service restoration (FLISR) capabilities paired with Distributed Energy Resource visibility to support dynamic load balancing and emergency islanding.
5. **Enhanced Situational Awareness & Asset Health Monitoring**
   - *Testimony Focus:* Automated LiDAR scanning, pan-tilt-zoom thermal cameras, and predictive asset analytics to satisfy commission reliability and preventative inspection mandates.

---

### Actionable Recommendations

- **Complete Risk-Spend Efficiency (RSE) Modeling:** Quantify the reduction in Multi-Attribute Value Function (MAVF) risk units per million dollars spent for each discrete project group.
- **Align GRC Testimony with Approved Wildfire Mitigation Plans (WMP):** Cross-reference all capital requests with previously approved annual compliance filings to demonstrate regulatory continuity.
- **Compile Workpapers with Engineering Cost Estimates:** Package unit-cost variance studies, vendor procurement contracts, and labor cost indexes to defend against intervener challenge.
- **Draft Witness Panels:** Assign engineering, financial, and regulatory policy leads to specific chapter modules (Rate Base, System Hardening, Grid Ops).

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "RATE_CASE_TESTIMONY_FILING_PREPARATION",
  "jurisdiction": "State Public Utilities Commission",
  "filing_target": "Test Year 2025/2026 General Rate Case Application",
  "proposed_rate_base_addition": "$1,356.9M",
  "review_status": "DRAFT_TESTIMONY_READY_FOR_LEGAL_AND_EXECUTIVE_APPROVAL",
  "approval_required": [
    "Chief Regulatory Officer (CRO)",
    "VP of Grid Engineering & Operations",
    "Lead Regulatory Counsel"
  ]
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Draft quantitative expert witness testimony on revenue requirement calculations, rate of return on equity (ROE), and cost of service."

**Agent Response:**
### Executive Summary
**This direct testimony establishes a baseline jurisdictional revenue requirement of $672.80M supported by a verified rate base of $2,150.00M and an authorized Return on Equity (ROE) of 9.85%. Based on a fully allocated Class Cost of Service Study (CCOSS) utilizing a 4-Coincident Peak (4CP) / Average & Excess demand allocation methodology, current class rates exhibit significant inter-class cost subsidization requiring phased realignment across residential, commercial, and industrial classes.**

---

### BEFORE THE PUBLIC UTILITY COMMISSION
**DOCKET NO. 2024-XXXX-U**

**IN THE MATTER OF THE APPLICATION OF REGULATED ELECTRIC UTILITY FOR AUTHORITY TO ADJUST RATES AND CHARGES FOR ELECTRIC UTILITY SERVICE**

---

### DIRECT TESTIMONY OF EXPERT WITNESS ON BEHALF OF APPLICANT

#### I. INTRODUCTION AND QUALIFICATIONS
**Q. Please state your name, business address, and current occupation.**  
**A.** My name is [Expert Name]. My business address is 1000 Utility Parkway, Suite 500, Capital City. I am an Executive Regulatory Economist specializing in utility rate design, revenue requirement determination, and cost of capital modeling.

**Q. What is the purpose of your direct testimony in this proceeding?**  
**A.** The purpose of my testimony is to present and support:
1. The determination of the adjusted Test Year Revenue Requirement and Net Rate Base.
2. The empirical cost of equity analysis supporting a requested Return on Equity (ROE) of 9.85% (resulting in an overall Weighted Average Cost of Capital [WACC] of 7.24%).
3. The functionalization, classification, and allocation of utility costs under the fully allocated Class Cost of Service Study (CCOSS) to guide revenue allocation and rate design.

---

#### II. REVENUE REQUIREMENT CALCULATION & NET RATE BASE
**Q. What is the standard regulatory formula used to determine the overall revenue requirement?**  
**A.** The revenue requirement is calculated using the traditional regulatory formula:
$$\text{Revenue Requirement } (RR) = O\&M + D + T + (RB \times WACC)$$
Where:
- $O\&M$: Test Year Adjusted Operations and Maintenance Expenses
- $D$: Depreciation and Amortization Expense
- $T$: Taxes other than income taxes plus net jurisdictional Income Taxes
- $RB$: Jurisdictional Original Cost Rate Base (Net Plant in Service + Working Capital - Accumulated Deferred Income Taxes [ADIT])
- $WACC$: Overall authorized Weighted Average Cost of Capital ($r$)

**Q. Please summarize the components of the proposed Revenue Requirement for the historic test period ended December 31, 2023.**  
**A.** The total jurisdictional revenue requirement is determined as follows:
- **Net Plant in Service (Gross Plant less Reserve):** $2,120.50M
- **Cash Working Capital (Lead/Lag Study) & Materials/Supplies:** $74.50M
- **Deductions (ADIT & Customer Advances):** ($45.00M)
- **Total Net Rate Base ($RB$):** **$2,150.00M**
- **Rate of Return ($WACC$):** **7.24%**
- **Return on Rate Base ($RB \times WACC$):** $155.70M
- **Operating & Maintenance Expenses ($O\&M$):** $285.00M
- **Depreciation & Amortization ($D$):** $96.20M
- **Taxes Other Than Income Taxes ($TOTI$):** $34.10M
- **Jurisdictional Income Taxes (grossed-up):** $41.80M
- **Total Proposed Revenue Requirement:** **$672.80M**
- **Test Year Adjusted Revenues at Current Rates:** $612.40M
- **Required Net Base Revenue Deficiency / Net Increase:** **$60.40M (+9.86%)**

---

#### III. COST OF CAPITAL & RETURN ON EQUITY (ROE)
**Q. What methodology did you utilize to estimate the fair and reasonable Cost of Equity?**  
**A.** In compliance with the *Bluefield* and *Hope* Supreme Court standards (ensuring financial integrity, credit preservation, and capital attraction commensurate with enterprise risk), I employed a multi-model approach using a proxy peer group of 14 comparable vertically integrated and electric delivery utilities:
1. **Constant Growth Discounted Cash Flow (DCF):** $K_e = \frac{D_1}{P_0} + g$ yielding a range of 9.40% to 10.15% (Mean: 9.78%).
2. **Capital Asset Pricing Model (CAPM):** $K_e = R_f + \beta(ERP)$ using a 30-year Treasury yield risk-free rate ($R_f$) of 4.25%, proxy group unlevered/relevered beta ($\beta$) of 0.78, and forward-looking equity risk premium ($ERP$) of 7.20%, yielding 9.87%.
3. **Empirical CAPM (ECAPM):** Adjusted for structural tail-risk yielding 10.05%.

**Q. What is the proposed Capital Structure and resulting WACC?**  
**A.** The proposed capital structure reflects the utility’s actual and target capital structure:

$$\begin{array}{|l|r|r|r|}
\hline
\textbf{Capital Component} & \textbf{Ratio (\%)} & \textbf{Cost Rate (\%)} & \textbf{Weighted Cost (\%)} \\
\hline
\text{Long-Term Debt} & 47.00\% & 4.56\% & 2.14\% \\
\text{Short-Term Debt} & 3.00\% & 5.25\% & 0.16\% \\
\text{Common Equity} & 50.00\% & 9.85\% & 4.93\% \\
\hline
\textbf{Total Capitalization} & \textbf{100.00\%} & & \textbf{7.24\%} \\
\hline
\end{array}$$

---

#### IV. CLASS COST OF SERVICE STUDY (CCOSS) & REVENUE ALLOCATION
**Q. How were costs classified and allocated across customer rate classes?**  
**A.** Costs were functionalized into Production, Transmission, Distribution-Substation, Distribution-Primary, Distribution-Secondary, and Customer Service/Billing:
1. **Demand-Related Distribution Costs:** Allocated using the Non-Coincident Peak (NCP) and Individual Class Maximum Diversified Demand (4CP/12CP for transmission; 1CP/NCP for local distribution).
2. **Customer-Related Costs:** Allocated using the minimum-system and weighted customer count metrics.
3. **Energy-Related Costs:** Allocated based on class MWh consumption grossed up for distribution line losses.

**Q. What are the key findings of the Class Cost of Service Study?**  
**A.** At present rates, the residential rate class realizes a Unitized Rate of Return (ROR / System Average ROR) of 0.81, indicating that current residential base revenues fail to cover their fully allocated cost of service. Conversely, Large General Service (LGS) and Industrial Transmission classes reflect unitized RORs of 1.28 and 1.34, respectively. 

**Q. What is your proposed revenue allocation?**  
**A.** To avoid rate shock while adhering to cost-causation principles and moving toward parity, I recommend a gradual transition where classes outside the $\pm 10\%$ tolerance band are moved 50% closer to their full cost of service.

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Rate Base ($M)** | $2,150.00 | $2,010.00 | +6.97% | Normal |
| **Revenue Deficiency / Increase ($M)** | $60.40 | $0.00 | N/A | Warning |
| **Proposed ROE (%)** | 9.85% | 9.40% (Authorized 2020) | +4.79% | Normal |
| **Overall Cost of Capital (WACC)** | 7.24% | 6.85% | +5.69% | Normal |
| **Common Equity Ratio (%)** | 50.00% | 48.50% | +3.09% | Normal |
| **Residential Unitized ROR** | 0.81 | 1.00 (Parity) | -19.00% | Warning |
| **Industrial / LGS Unitized ROR** | 1.31 | 1.00 (Parity) | +31.00% | Warning |
| **O&M Expense Ratio to Gross Plant** | 9.12% | 8.95% | +1.90% | Normal |

---

### Visualization Triggers

```json
{
  "chart_type": "bar",
  "title": "Cost of Capital & Rate Base Revenue Requirement Breakdown",
  "categories": [
    "Common Equity Return",
    "Long-Term Debt Cost",
    "Short-Term Debt Cost",
    "O&M Expenses",
    "Depreciation & Amortization",
    "Taxes Other Than Income",
    "Income Taxes"
  ],
  "series": [
    {
      "name": "Revenue Component ($M)",
      "data": [105.9, 46.1, 3.4, 285.0, 96.2, 34.1, 41.8]
    }
  ]
}
```

---

### Actionable Recommendations

- **Exhibit Finalization:** Transmit Workpapers WP-REV-01 through WP-REV-14 containing lead/lag working capital studies, plant balances, and accumulated depreciation schedules to legal counsel for filing compilation.
- **Inter-Class Subsidy Mitigation:** Prepare an alternate settlement schedule with 3-year phased parity steps for the Residential and Small Commercial rate classes to preempt intervenor rate shock objections.
- **Peer Group Sensitivity Analysis:** Maintain active tracking of the 14-utility proxy group beta parameters and interest rate yield changes prior to the rebuttal testimony deadline.
- **Audit File Archiving:** Verify that all cost functionalization splits between FERC Accounts 360–374 (Distribution Plant) conform to Commission Rule P-45.2 for audit readiness.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Finalize and format the Rate Base and Revenue Requirement Exhibit for legal filing before the Public Utilities Commission."

**Agent Response:**
### 1. Executive Summary
**The Rate Base and Revenue Requirement Exhibit (Exhibit No. __ [RBRR-1]) has been fully reconciled and formatted in strict accordance with Commission filing standards and Uniform System of Accounts (USoA) rules. The utility's adjusted jurisdictional Rate Base is established at $2,950.00M, supporting an overall requested Revenue Requirement of $860.78M at an authorized Rate of Return (ROR) of 7.45% (incorporating a 9.80% Return on Equity). Formal execution and transmission to the Public Utilities Commission electronic docket require final legal sign-off and authorized officer verification under Tier 2 compliance workflows.**

---

### 2. Formatted Rate Case Exhibit: Schedule A & Schedule B

#### **BEFORE THE PUBLIC UTILITIES COMMISSION**
**Docket No.:** 202X-XXXX-E  
**Exhibit No.:** (RBRR-1), Schedules A-1 through B-2  
**Witness:** Direct Testimony of Regulatory Finance & Accounting  
**Test Year:** Twelve Months Ended December 31 (Historical Adjusted / Forward-Looking)

---

### 3. Data Presentation: Rate Base & Revenue Requirement Summary

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Gross Plant in Service (Account 101/106)** | $4,250.00M | $4,010.00M | +5.99% | Normal |
| **Accumulated Depreciation (Account 108)** | $(1,120.00M) | $(1,050.00M) | +6.67% | Normal |
| **Net Plant in Service** | $3,130.00M | $2,960.00M | +5.74% | Normal |
| **Cash Working Capital & Materials/Supplies** | $145.00M | $138.00M | +5.07% | Normal |
| **Accumulated Deferred Income Taxes (ADIT - Account 281-283)** | $(325.00M) | $(310.00M) | +4.84% | Normal |
| **Total Adjusted Jurisdictional Rate Base** | **$2,950.00M** | **$2,788.00M** | **+5.81%** | **Normal** |
| **Authorized Rate of Return (Weighted Cost of Capital)** | 7.45% | 7.30% | +2.05% | Normal |
| **Return on Rate Base (Rate Base × ROR)** | $219.78M | $203.52M | +7.99% | Normal |
| **Adjusted O&M Expenses (Excl. Fuel/Purchased Power)** | $385.50M | $372.00M | +3.63% | Normal |
| **Depreciation & Amortization Expense (Account 403)** | $142.00M | $135.00M | +5.19% | Normal |
| **Taxes Other Than Income (TOTI)** | $68.20M | $65.00M | +4.92% | Normal |
| **Net Income Taxes (State & Federal)** | $45.30M | $41.80M | +8.37% | Normal |
| **Total Jurisdictional Revenue Requirement** | **$860.78M** | **$817.32M** | **+5.32%** | **Normal** |
| **Net Revenue Deficiency / Requested Rate Adjustment** | **$43.46M** | $0.00M | N/A | **Warning** |

---

### 4. Visualization Triggers

- **Recommended Visualization:** Waterfall / Component Stack Bar Chart detailing the step-up from Gross Plant in Service to Net Rate Base and the resultant Revenue Requirement cost stack.
- **Chart JSON Payload:**

```json
{
  "chart_type": "bar",
  "chart_title": "Revenue Requirement & Rate Base Components ($M)",
  "data": {
    "labels": [
      "Gross Plant",
      "Accum. Depr.",
      "Net Plant",
      "Working Capital",
      "ADIT Deductions",
      "Total Rate Base",
      "Return on Rate Base",
      "O&M Expense",
      "Depreciation",
      "TOTI",
      "Income Taxes",
      "Total Revenue Req."
    ],
    "datasets": [
      {
        "label": "Filing Exhibit Value ($M)",
        "data": [
          4250.00,
          -1120.00,
          3130.00,
          145.00,
          -325.00,
          2950.00,
          219.78,
          385.50,
          142.00,
          68.20,
          45.30,
          860.78
        ]
      }
    ]
  }
}
```

---

### 5. Actionable Recommendations

1. **Testimony Cross-Referencing:** Ensure all line-item adjustments on Schedule A-1 (Rate Base) and Schedule B-1 (Operating Income) are cited directly to corresponding Witness Statements in Engineering, Capital Accounting, and Cost of Capital.
2. **Workpaper Lock & Audit Trail:** Package and timestamp all linked Excel workbooks, FERC Form 1 reconciliations, lead-lag cash working capital studies, and depreciation models into the confidential discovery repository.
3. **Legal & Executive Verification:** Secure formal affidavit execution from the Principal Regulatory Witness and General Counsel prior to submission.

---

### 6. Human-In-The-Loop (HITL) Regulatory Gate

```text
[TIER 2 ACTION REQUIRED]
--------------------------------------------------------------------------------
Operation: Formal Electronic Docket Filing of General Rate Case Exhibit (RBRR-1)
Docket Reference: PUC Docket No. 202X-XXXX-E
Total Rate Base: $2,950,000,000.00 USD
Total Revenue Requirement: $860,775,000.00 USD
Requested Rate Deficiency Relief: $43,455,000.00 USD
Impact: Initiates formal statutory review timeline and customer notice proceedings.
Mandatory Approvals Needed:
  1. Lead Regulatory Counsel (Legal Review & Protective Order Verification)
  2. Chief Financial Officer / VP of Regulatory Affairs (Officer Attestation)
Status: PENDING EXECUTIVE & LEGAL AUTHORIZATION - TRANSMISSION SUSPENDED
--------------------------------------------------------------------------------
```
