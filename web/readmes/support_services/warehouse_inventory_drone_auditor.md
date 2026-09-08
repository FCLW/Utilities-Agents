# ⚡ Warehouse Inventory Drone Auditor

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of warehouse inventory drone auditor is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Warehouse Inventory Drone Auditor Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank warehouse inventory drone auditor events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.warehouse_inventory_drone_auditor_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Did last night's autonomous warehouse drone LiDAR scan detect any inventory discrepancies for 15kV distribution cable spools?"

**Agent Response:**
### 1. Executive Summary
**Last night's autonomous warehouse drone LiDAR audit detected a localized inventory discrepancy for 15kV distribution cable spools in Central Yard (Bay A4). While 3 of the 4 storage locations matched ERP inventory records with 100% volumetric and barcode accuracy, Bay A4 registered an unrecorded variance of -3 spools (39 physically verified vs. 42 ERP ledger count). The remaining storage zones (Bay A5, Bay B2, and Rack 12) exhibited zero discrepancy.**

---

### 2. Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Central Yard Bay A4 Spools** | 39 units | 42 units | -7.14% | **Warning** |
| **Central Yard Bay A5 Spools** | 35 units | 35 units | 0.00% | **Normal** |
| **West Yard Bay B2 Spools** | 28 units | 28 units | 0.00% | **Normal** |
| **North Storage Rack 12 Spools** | 15 units | 15 units | 0.00% | **Normal** |
| **Total 15kV Cable Inventory** | 117 spools | 120 spools | -2.50% | **Warning** |
| **LiDAR Point Cloud Confidence** | 99.4% | ≥ 98.0% | +1.43% | **Normal** |
| **Volumetric Surface Tolerance** | ±1.2 cm | ≤ ±2.5 cm | -52.00% | **Normal** |

---

### 3. Visualization Triggers

**Recommended Visualization:** Grouped Bar Chart comparing ERP recorded inventory against drone LiDAR point-cloud detected spools across warehouse yard zones.

```json
{
  "chart_type": "bar",
  "title": "15kV Distribution Cable Spool Inventory: ERP vs. LiDAR Scan",
  "xAxis": {
    "categories": [
      "Central Yard Bay A4",
      "Central Yard Bay A5",
      "West Yard Bay B2",
      "North Storage Rack 12"
    ]
  },
  "yAxis": {
    "title": "Spool Count (Units)"
  },
  "series": [
    {
      "name": "ERP Ledger Count",
      "data": [42, 35, 28, 15]
    },
    {
      "name": "LiDAR Verified Count",
      "data": [39, 35, 28, 15]
    }
  ]
}
```

---

### 4. Actionable Recommendations

- **Cross-Reference Work Orders & Dispatch Logs**: Audit recent field crew checkouts from the past 24 hours to verify if the 3 missing 15kV spools in Bay A4 were issued to emergency distribution line crews without completed ERP barcode scans.
- **Physical Yard Marshall Inspection**: Dispatch a warehouse technician to Bay A4 to confirm whether spools were temporarily staged in an unmapped staging buffer or obstructed by heavy rigging equipment.
- **Drone Re-flight Path Verification**: Re-task the next scheduled aerial scan route to include high-resolution optical zoom confirmation over Bay A4's perimeter.

---

### 5. HITL / Tier 2 Notification

```markdown
[TIER 2 ACTION REQUIRED]
- Action: ERP Inventory Ledger Write-Down / Reclassification
- Asset Category: 15kV Distribution Cable Spools (SKU: CBL-15KV-AL-500)
- Location: Central Yard, Bay A4
- Proposed Adjustment: -3 Spools (Estimated Asset Value: $18,450.00)
- Confirmation Requirement: Requires Human Warehouse Operations Lead sign-off prior to executing ERP ledger balance adjustment.
```

### Example 2: Trend & Comparative Analysis
**User:** "Reconcile drone RFID scanner inventory counts against SAP enterprise resource planning (ERP) inventory ledger records."

**Agent Response:**
### Executive Summary
**Autonomous warehouse inventory drone RFID scanning sweeps across Central Logistics Depot (Zone Alpha & Beta) detected a 97.8% overall reconciliation accuracy against the active SAP S/4HANA ERP inventory ledger.** **Critical variances were identified in smart meter lots (-350 units) and pad-mounted distribution transformers (-7 units), indicating staging unrecorded in ERP post-kitting and potential unassigned yard movements.** **Total net unadjusted financial ledger variance is valued at -$184,250 USD, necessitating immediate supervisor-gated inventory adjustments and manual bin verification before cycle lock.**

---

### Quantitative Reconciliation & KPI Metrics

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Drone RFID Scan Completion Rate** | 99.85% (18,805 / 18,838 bins) | 99.50% | +0.35% | Normal |
| **Overall SKU Match Rate** | 97.82% | 99.00% | -1.18% | Warning |
| **Gross Ledger Count Variance** | 403 units | < 50 units | +706.00% | Critical |
| **Net Financial Discrepancy** | -$184,250 USD | $0.00 USD | N/A | Critical |
| **Ghost Inventory (ERP > Drone RFID)** | 363 units | 0 units | N/A | Critical |
| **Unregistered Tag Density (Drone > ERP)** | 40 units | 0 units | N/A | Warning |
| **Audit Compliance Rate (NERC/FERC/SOX)** | 98.20% | 100.00% | -1.80% | Warning |

---

### Detailed Asset Class Reconciliation Table

| SKU / Material Description | Material Master Code | Warehouse Bin Location | Drone RFID Count | SAP ERP Ledger | Variance (Units) | Unit Cost ($) | Net Value Delta ($) | Primary Root Cause / Findings |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Pad-Mounted Transformers (50kVA)** | `MAT-TX-50-PM` | Yard Y-04 to Y-08 | 428 | 435 | -7 | $14,500 | -$101,500 | Staged on emergency storm trailers without SAP Goods Issue (Mvt 201). |
| **Substation Circuit Breakers (69kV)** | `MAT-CB-69KV-SF6` | High-Bay HB-02 | 74 | 74 | 0 | $48,000 | $0 | 100% Match; Tag orientation verified. |
| **ACSR Conductor Reels (477 kcmil)** | `MAT-CND-477-ACSR`| Yard Y-12 to Y-16 | 1,850 | 1,820 | +30 | $1,250 | +$37,500 | Returned from capital project feeder rebuild; credit not yet posted in ERP. |
| **Smart AMI Electric Meters (Single-Phase)**| `MAT-AMI-1P-LTE` | Aisle A-01 to A-06 | 12,450 | 12,800 | -350 | $165 | -$57,750 | Pallet batch #9042 issued to AMI deployment subcontractor without 261 posting. |
| **Microprocessor Protective Relays** | `MAT-REL-SEL411L`| Secure Vault SV-01 | 310 | 312 | -2 | $8,200 | -$16,400 | RFID shielding effect on lower steel racking shelf; manual verification required. |
| **Distribution Switchgear Units** | `MAT-SWG-15KV-4W`| High-Bay HB-05 | 88 | 92 | -4 | $11,500 | -$46,100 | Staged for Substation Feeder 14B upgrade; staging status pending in SAP WMS. |
| **Polymer Suspension Insulators (115kV)**| `MAT-INS-115-POLY`| Aisle B-08 to B-11 | 3,420 | 3,410 | +10 | $60 | +$600 | Supplier overage received and placed in rack before GR/IR verification. |
| **Gas Pressure Regulators (2" ANSI 300)** | `MAT-REG-2IN-300` | Aisle C-03 | 195 | 195 | 0 | $2,100 | $0 | 100% Match. |

---

### Visualization Trigger: Variance Distribution by Asset Class

Recommended Chart: **Categorical Horizontal Bar Chart / Ledger Delta Variance**

```json
{
  "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
  "title": "Drone RFID Physical Count vs. SAP ERP Ledger Variance",
  "data": {
    "values": [
      {"category": "Pad-Mounted Transformers", "variance_units": -7, "variance_cost": -101500},
      {"category": "Substation Circuit Breakers", "variance_units": 0, "variance_cost": 0},
      {"category": "Conductor Reels (ACSR)", "variance_units": 30, "variance_cost": 37500},
      {"category": "Smart AMI Meters", "variance_units": -350, "variance_cost": -57750},
      {"category": "Protective Relays & IEDs", "variance_units": -2, "variance_cost": -16400},
      {"category": "Distribution Switchgear", "variance_units": -4, "variance_cost": -46100},
      {"category": "Polymer Insulators", "variance_units": 10, "variance_cost": 600},
      {"category": "Gas Pressure Regulators", "variance_units": 0, "variance_cost": 0}
    ]
  },
  "mark": "bar",
  "encoding": {
    "y": {"field": "category", "type": "nominal", "sort": "-x", "title": "Material Class"},
    "x": {"field": "variance_cost", "type": "quantitative", "title": "Net Value Variance ($ USD)"},
    "color": {
      "field": "variance_cost",
      "type": "quantitative",
      "scale": {"scheme": "redyellowgreen", "domainMid": 0}
    }
  }
}
```

---

### Actionable Recommendations

1. **Immediate Yard Staging Trace**: Dispatch warehouse field personnel with handheld Zebra RFID scanners to staging docks Y-04 through Y-08 to physically scan the 7 missing pad-mounted transformers against active storm-response work orders.
2. **Subcontractor Outbound Reconciliation**: Reconcile SAP Outbound Delivery note `OBD-8840291` for AMI Meter Lot #9042 with the deployment contractor dispatch log to execute SAP Movement Type 261 (Goods Issue to Work Order).
3. **Restock Crediting for Field Returns**: Post SAP Movement Type 282/561 for the 30 surplus ACSR conductor reels located in Yard Y-14 to restore ledger valuation and prevent redundant procurement.
4. **Rescan Shielded Vault SV-01**: Execute a low-altitude, high-gain drone rescan on Aisle SV-01 bottom shelves to verify line-of-sight for the 2 missing protective relays before initiating loss reporting.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "tier_level": "Tier 2",
  "action_type": "ERP_INVENTORY_WRITE_OFF_AND_LEDGER_ADJUSTMENT",
  "system": "SAP S/4HANA (Warehouse Management / Material Management)",
  "details": {
    "transaction_code": "MI07 / MB1A",
    "total_financial_adjustment_usd": -184250.00,
    "affected_items": [
      {"material_code": "MAT-TX-50-PM", "qty_adjustment": -7, "mvt_type": "702 (Physical Inventory Loss)"},
      {"material_code": "MAT-CND-477-ACSR", "qty_adjustment": 30, "mvt_type": "701 (Physical Inventory Gain)"},
      {"material_code": "MAT-AMI-1P-LTE", "qty_adjustment": -350, "mvt_type": "261 (Issue to Deployment WO #44091)"},
      {"material_code": "MAT-SWG-15KV-4W", "qty_adjustment": -4, "mvt_type": "311 (Transfer to Substation Staging)"}
    ],
    "regulatory_compliance_impact": "SOX Inventory Accuracy Mandate & NERC CIP-014 Physical Asset Tracking",
    "required_approver": "Director of Supply Chain & Material Operations"
  },
  "confirmation_prompt": "Confirm execution of SAP S/4HANA inventory adjustments totaling -$184,250.00 USD across 4 material master categories? [YES / NO]"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Update the warehouse inventory database to reflect actual verified stock counts of 48 porcelain insulator bushings."

**Agent Response:**
### Executive Summary
**Autonomous drone visual telemetry and barcode scanning have completed the cycle count, verifying an actual physical inventory of 48 porcelain insulator bushings.** In accordance with read-only database guardrails and enterprise utility auditing policies, autonomous agent direct database mutations (`UPDATE`/`INSERT`) are strictly prohibited. An inventory adjustment staging payload has been prepared for Human-in-the-Loop (HITL) sign-off.

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Porcelain Insulator Bushings Count** | 48 Units | 50 Units (System ERP) | -4.00% | Warning |
| **Audit Visual Confidence Score** | 99.4% | 95.0% | +4.63% | Normal |
| **Barcode / Serial Match Rate** | 100.0% | 100.0% | 0.00% | Normal |
| **Storage Bin Discrepancy** | Bin A-14 (Zone 2) | Bin A-14 (Zone 2) | 0.00% | Normal |

---

### Visualization Triggers
- **Recommended Chart**: Categorical Bar Chart (Physical Drone Audit vs. ERP System Baseline)
- **Chart Data (JSON)**:
```json
{
  "chart_type": "bar",
  "title": "Inventory Audit Reconciliation - Porcelain Insulator Bushings",
  "data": [
    {
      "category": "ERP System Baseline",
      "quantity": 50,
      "status": "Target"
    },
    {
      "category": "Drone Audit Verified",
      "quantity": 48,
      "status": "Actual"
    },
    {
      "category": "Variance",
      "quantity": -2,
      "status": "Discrepancy"
    }
  ]
}
```

---

### Actionable Recommendations
- **Inventory Reconciliation**: Dispatch the warehouse supervisor to review the 2-unit delta against recent work orders or maintenance staging pull requests.
- **ERP Synchronization**: Approve the Tier 2 payload below to commit the audited count of 48 units into the enterprise Warehouse Management System (WMS).
- **Scheduled Re-Audit**: Re-scan Bin A-14 during the next scheduled drone flight cycle to verify physical retention.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "WAREHOUSE_INVENTORY_DATABASE_UPDATE",
  "item_description": "Porcelain Insulator Bushings (15kV / 34.5kV Substation Grade)",
  "sku_id": "INSL-PORC-0048-B",
  "location_id": "WH-CENTRAL-BIN-A14",
  "previous_system_count": 50,
  "verified_physical_count": 48,
  "variance": -2,
  "adjustment_reason": "Drone visual audit & barcode scan cycle reconciliation",
  "operator_approval_required": true,
  "audit_timestamp": "2023-10-25T14:30:00Z"
}
```
