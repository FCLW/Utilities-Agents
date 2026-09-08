# ⚡ Hazardous Waste Disposal Tracker

![Domain](https://img.shields.io/badge/Domain-regulatory%20compliance-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of hazardous waste disposal tracker is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Hazardous Waste Disposal Tracker Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank hazardous waste disposal tracker events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_regulatory_compliance.hazardous_waste_disposal_tracker_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Are all decommissioned polychlorinated biphenyl (PCB) contaminated distribution transformers documented with EPA hazardous manifests?"

**Agent Response:**
### Executive Summary
**A comprehensive audit of the hazardous waste inventory indicates that 98.68% (225 of 228) of decommissioned PCB-contaminated distribution transformers (≥50 ppm) are documented with validated EPA Uniform Hazardous Waste Manifests (EPA Form 8700-22 / e-Manifest). Three decommissioned units currently in staging yards require immediate manifest finalization and certificate of disposal reconciliation to reach 100% TSCA compliance. All active storage facilities remain within the 30-day temporary staging and 1-year disposal timeline mandates under 40 CFR § 761.60.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Decommissioned PCB Transformers (≥50 ppm)** | 228 units | 228 units | 0.00% | Normal |
| **Documented with Verified EPA Manifests** | 225 units | 228 units (100.0%) | -1.32% | Warning |
| **Pending / In-Transit Manifest Documentation** | 3 units | 0 units | +100.00% | Warning |
| **TSCA 1-Year Disposal Rule Compliance** | 100.00% | 100.00% | 0.00% | Normal |
| **Certificates of Destruction / Disposal (COD) Logged** | 218 units | 225 manifested units | -3.11% | Warning |
| **High-Concentration PCB Units (≥500 ppm) Fully Tracked** | 100.00% (41/41) | 100.00% | 0.00% | Normal |

---

### Visualization Trigger: PCB Manifest Tracking by Grid Zone

```json
{
  "chart_type": "bar",
  "title": "PCB Transformer Manifest Compliance Status by Grid Zone",
  "xAxis": {
    "categories": ["Zone North", "Zone South", "Zone East", "Zone West", "Central Yard"]
  },
  "yAxis": {
    "title": "Transformer Units (Count)"
  },
  "series": [
    {
      "name": "Fully Manifested (EPA Form 8700-22)",
      "data": [42, 38, 55, 29, 61]
    },
    {
      "name": "Pending / Missing Manifest",
      "data": [0, 2, 0, 1, 0]
    }
  ]
}
```

---

### Actionable Recommendations

- **Reconcile Pending Manifests**: Direct field operations in **Zone South** (2 units) and **Zone West** (1 unit) to upload executed copies of EPA Form 8700-22 into the enterprise hazardous waste tracking system within 5 business days.
- **Acquire Outstanding Certificates of Disposal (COD)**: Contact permitted TSCA incinerator/chemical waste landfill facilities for the 7 outstanding CODs that are nearing the 30-day post-disposal return window.
- **Inspect Staging Labels**: Verify that all 3 un-manifested decommissioned units currently held in containment bays are marked with EPA PCB markings (ML Label) and designated out-of-service dates pursuant to 40 CFR § 761.40.
- **Automated e-Manifest Ingestion**: Enable daily webhook sync between the EPA RCRA-Info / e-Manifest system and the Environmental Compliance Registry to eliminate manual logging latency.

### Example 2: Trend & Comparative Analysis
**User:** "Track chain-of-custody disposal records, storage dwell times, and licensed hazardous waste recycling facility receipts."

**Agent Response:**
### Executive Summary
**RCRA Title 40 CFR and EPA e-Manifest compliance tracking indicates that 98.4% of utility hazardous waste streams remain strictly within allowable 90-day Large Quantity Generator (LQG) on-site accumulation limits.** **All active chain-of-custody (CoC) manifests are reconciled with Treatment, Storage, and Disposal Facility (TSDF) final certificates of destruction/recycling with zero unresolved 35-day exception notices.** **Substation decommissioned lead-acid battery inventory requires expedited off-site logistics as average dwell time has reached 68 days against the 90-day statutory threshold.**

---

### Data Presentation

#### Key Compliance & Operational Metrics
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **EPA e-Manifest Reconciliation Rate** | 100.0% | 100.0% | 0.0% | Normal |
| **Avg Substation Storage Dwell Time** | 45.4 Days | < 60.0 Days | -24.3% | Normal |
| **Lead-Acid Battery Dwell Time (Peak Zone)** | 68.0 Days | < 60.0 Days | +13.3% | Warning |
| **Unsigned TSDF Receipts (>30 Days)** | 0 Records | 0 Records | 0.0% | Normal |
| **Permitted Transporter Chain-of-Custody Integrity** | 100.0% | 100.0% | 0.0% | Normal |
| **PCB Waste Destruction Certification Rate** | 100.0% | 100.0% | 0.0% | Normal |

#### Active Manifest & Waste Stream Chain-of-Custody Tracking
| Manifest Tracking # | Waste Stream Category | Accumulation Start | Dwell Time (Days) | Transporter / TSDF Partner | TSDF EPA ID | Final Receipt Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **MAN-2024-0881** | PCB Mineral Oil (>50 ppm) | 2024-04-12 | 42 | Clean Harbors Env. Services | MAD039322250 | Certified / Incinerated |
| **MAN-2024-0894** | Substation Lead-Acid Batteries | 2024-03-15 | 68 | RSR Quemetco Metals Rec. | CAD066233966 | In Transit / Verified CoC |
| **MAN-2024-0912** | Decommissioned SF6 Gas Cylinders | 2024-04-26 | 28 | Electronic Fluorocarbons LLC | PAD982361102 | Received / Reclaimed |
| **MAN-2024-0925** | Solvent Rags & Heavy Degreasers | 2024-03-28 | 55 | Heritage Thermal Services | OHD980613541 | Certified / Energy Recovery |
| **MAN-2024-0938** | Non-PCB Contaminated Dielectric | 2024-04-20 | 34 | Hydrodec North America | OHR000142984 | Certified / Hydro-Treated |

---

### Visualization Triggers
- **Recommended Visualization**: Grouped Horizontal Bar Chart comparing current waste accumulation dwell days against statutory 90-day RCRA Large Quantity Generator limits by waste stream classification.

```json
{
  "chart_type": "bar",
  "title": "Hazardous Waste Storage Dwell Time vs. RCRA 90-Day Limit",
  "categories": [
    "PCB Transformer Oil",
    "Substation Lead-Acid Batteries",
    "SF6 Gas Cylinders (Decomm)",
    "Solvent Rags & Degreasers",
    "Contaminated Dielectric Fluid"
  ],
  "series": [
    {
      "name": "Current Storage Dwell Time (Days)",
      "data": [42, 68, 28, 55, 34]
    },
    {
      "name": "RCRA Regulatory Limit (Days)",
      "data": [90, 90, 90, 90, 90]
    }
  ],
  "threshold_warning_days": 60
}
```

---

### Actionable Recommendations

- **Expedite Pickup Schedule for Substation Lead-Acid Batteries**: Coordinate with logistics and RSR Quemetco to ensure all manifest batches exceeding 60 dwell days are transported and received well within the 90-day threshold to avoid RCRA storage permit violations.
- **Automate TSDF Receipt Exception Alerting**: Maintain automated EPA e-Manifest sync triggers to flag any manifest reaching day 35 post-shipment without a signed TSDF electronic receipt, triggering standard EPA exception filings if not closed by day 45.
- **Verify Secondary Containment Inspections**: Conduct weekly documented inspections for on-site accumulation areas at central staging yards housing PCB and solvent waste streams.
- **Maintain TSCA PCB Records**: Archive all TSDF Certificates of Disposal (COD) for PCB transformers (40 CFR Part 761) with retention periods set for minimum 3 years.

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate the certified hazardous waste shipping manifest and schedule pickup of 12 retired PCB-mineral oil transformers."

**Agent Response:**
### 1. Executive Summary
**A certified hazardous waste manifest (EPA Form 8700-22 / TSCA Manifest) has been pre-drafted for the offsite transport and incineration of 12 decommissioned PCB-contaminated mineral oil transformers (50–499 ppm PCB category). All units have undergone lab verification, containment inspection, and regulatory classification in accordance with 40 CFR Part 761 (TSCA) and state environmental standards. Final carrier dispatch, hazardous material bill of lading issuance, and physical transport execution constitute a Tier 2 physical/financial dispatch action requiring mandatory Human-In-The-Loop (HITL) sign-off.**

---

### 2. Regulatory & Manifest Tracking Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Units Prepared for Pickup** | 12 Transformers | 12 Units | 0.0% | **Normal** |
| **Total PCB Oil Volume** | 3,840 Gallons (29,568 lbs) | ≤ 4,000 Gallons capacity | -4.0% | **Normal** |
| **Max Concentration (PCB)** | 240 ppm (TSCA Contaminated) | < 500 ppm (Non-TSCA Bulk Rule) | -52.0% | **Normal** |
| **EPA 30-Day Storage Limit** | 14 Days in Yard | ≤ 30 Days (Pre-shipment) | -53.3% | **Normal** |
| **Secondary Containment Integrity**| 100% Verified Pass | 100% Pass Required | 0.0% | **Normal** |
| **Designated TSDF Acceptance** | Certified / Permitted TSDF | Active EPA ID Required | 0.0% | **Normal** |

---

### 3. Visualization Trigger

```json
{
  "chart_type": "bar",
  "data_json": {
    "title": "PCB Concentration Profile per Transformer Unit (ppm)",
    "categories": [
      "TX-01", "TX-02", "TX-03", "TX-04", "TX-05", "TX-06",
      "TX-07", "TX-08", "TX-09", "TX-10", "TX-11", "TX-12"
    ],
    "series": [
      {
        "name": "Measured PCB Level (ppm)",
        "data": [112, 145, 88, 210, 195, 74, 160, 240, 130, 95, 180, 205]
      },
      {
        "name": "TSCA Hazardous Regulatory Threshold (ppm)",
        "data": [50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations

* **Step 1: Manifest Verification**: Confirm Designated TSDF (Treatment, Storage, and Disposal Facility) EPA ID: `TXD000838896` and DOT Certified Transporter ID: `USDOT-748921`.
* **Step 2: Placarding & Marking**: Ensure all 12 units have yellow PCB `ML` (Large PCB Mark) labels affixed to both sides along with DOT Class 9 UN3432 placards on the transport trailer.
* **Step 3: Chain-of-Custody Tracking**: Require the transporter operator and utility environmental officer to execute physical wet-ink or e-Manifest signatures (EPA e-Manifest system) prior to leaving the staging yard.
* **Step 4: TSDF Certificate of Destruction**: Schedule a tracking trigger for receipt of the Certificate of Disposal / Destruction within 45 days pursuant to 40 CFR § 761.218.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "HAZARDOUS_WASTE_DISPATCH_AND_MANIFEST_EXECUTION",
  "domain": "REGULATORY_COMPLIANCE",
  "authorization_level": "TIER_2",
  "parameters": {
    "manifest_tracking_number": "019482038JJK",
    "waste_description": "UN3432, Polychlorinated biphenyls, solid / liquid mixture (Mineral Oil Decommissioned Transformers), 9, PG III, Marine Pollutant",
    "item_count": 12,
    "total_weight_lbs": 29568,
    "transporter": "CleanHarbors Environmental Services Inc.",
    "destination_tsDF": "CleanHarbors Deer Park Inc. (EPA ID: TXD000838896)",
    "pickup_window": "2025-03-05 08:00:00 UTC - 12:00:00 UTC",
    "storage_site_id": "SUB_STAGING_YARD_EAST_04"
  },
  "critic_validation": {
    "status": "AWAITING_HUMAN_SIGN_OFF",
    "safety_checks_passed": true,
    "compliance_verified": "40_CFR_761_TSCA_AND_DOT_CLASS_9"
  }
}
```
