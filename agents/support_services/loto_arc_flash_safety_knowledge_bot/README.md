# ⚡ Loto Arc Flash Safety Knowledge Bot

![Domain](https://img.shields.io/badge/Domain-support%20services-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of loto arc flash safety knowledge bot is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Loto Arc Flash Safety Knowledge Bot Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank loto arc flash safety knowledge bot events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_support_services.loto_arc_flash_safety_knowledge_bot_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "What are the mandated Lockout/Tagout (LOTO) isolation points and PPE requirements for replacing a 13.8kV breaker in Cubicle 4?"

**Agent Response:**
### Executive Summary
**Mandated Lockout/Tagout (LOTO) isolation for 13.8kV Cubicle 4 requires establishing a three-point electrical boundary encompassing upstream bus isolation, downstream load circuit opening, and auxiliary DC/AC control power disconnects. In accordance with NFPA 70E and OSHA 1910.269 standards, all personnel engaging in racking, testing, and grounding within the 13.8kV arc flash boundary must utilize minimum 40 cal/cm² (Arc Flash PPE Category 4) flash suits with Class 2 (17kV/20kV test) insulating rubber gloves. Physical work cannot commence until a calibrated Live-Dead-Live zero-energy verification is completed and protective safety grounds are secured.**

---

### Safety & Operational Boundaries: 13.8kV Switchgear Cubicle 4

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **System Voltage Rating** | 13.8 kV Line-to-Line | 13.8 kV Nominal | 0.0% | **Normal** |
| **Calculated Incident Energy** | 36.4 cal/cm² (@ 36 in) | < 40.0 cal/cm² (Cat 4 Limit) | -9.0% | **Warning** |
| **Arc Flash Boundary (AFB)** | 14.2 ft (170.4 in) | Standard Boundary Envelope | 0.0% | **Warning** |
| **Limited Approach Boundary** | 5.0 ft (60.0 in) | NFPA 70E Medium Voltage Std | 0.0% | **Normal** |
| **Restricted Approach Boundary**| 2.2 ft (26.0 in) | NFPA 70E Medium Voltage Std | 0.0% | **Critical** |
| **Control Circuit Voltage** | 125 VDC / 120 VAC | Nominal Trip/Close Supply | 0.0% | **Normal** |

---

### Mandated LOTO Isolation Sequence & Points

1. **Primary Circuit Isolation:**
   - **Primary Bus:** Trip and open 13.8kV circuit breaker in Cubicle 4.
   - **Racking Mechanism:** Rack out breaker from "Connected" to "Test" position, confirm visual separation/shutter closure, then move to "Disconnected/Fully Withdrawn" position.
   - **Upstream & Downstream Disconnects:** Open upstream bus tie/source disconnect switches and downstream feeder disconnects; attach LOTO padlocks and Danger Tags to physical mechanical locks.

2. **Secondary & Auxiliary Energy Isolation:**
   - **DC Control Power:** Open and lockout 125VDC breaker/knife switch in auxiliary control compartment to disable trip/close solenoids.
   - **AC Spring Charging:** Manually discharge breaker spring mechanism; open 120VAC motor supply circuit breaker and apply lockout hasp.
   - **PT/CT Circuits:** Isolate secondary potential transformer (PT) fuses to prevent backfeeding hazards; short-circuit secondary CT blocks prior to lead disconnection.

3. **Zero-Energy Verification (Live-Dead-Live):**
   - Perform three-point verification using an adequately rated capacitive voltage detector (rated ≥15kV):
     1. Test voltage detector against a known energized source/piezoelectric tester.
     2. Verify zero potential on all three phases ($A, B, C$) of Cubicle 4 primary stabs/bushings.
     3. Re-test voltage detector against the known source to verify proper instrument operation.
   - Install safety grounding cluster or racking ground truck to discharge residual capacitive charges.

---

### Mandated PPE Requirements (NFPA 70E / OSHA 1910.269)

* **Arc Flash Protective Equipment:** Minimum **40 cal/cm²** Arc Flash Hood with integrated face shield, multi-layer arc-rated jacket and bib overalls (or 40 cal/cm² flash suit).
* **Dielectric Protection:** ASTM D120 **Class 2 Rubber Insulating Gloves** (proof tested to 20kV AC, max use 17kV AC) with heavy-duty leather protectors.
* **Head, Eye & Hearing Protection:** Type I or II dielectric Hard Hat (Class E), safety glasses with side shields (ANSI Z87.1), and canal earplugs/hearing protection.
* **Footwear & Apparel:** ASTM F2413 dielectric/EH-rated safety boots and non-melting arc-rated base layers (100% natural fiber/cotton).

---

### Visualization Triggers

```json
{
  "chart_type": "bar",
  "title": "Cubicle 4 Incident Energy & Approach Boundaries (NFPA 70E)",
  "data": [
    {"parameter": "Restricted Approach", "distance_inches": 26, "type": "Approach Boundary"},
    {"parameter": "Limited Approach", "distance_inches": 60, "type": "Approach Boundary"},
    {"parameter": "Arc Flash Boundary", "distance_inches": 170.4, "type": "Arc Flash Envelope"},
    {"parameter": "Working Distance", "distance_inches": 36, "type": "Operating Point"}
  ]
}
```

---

### Actionable Recommendations

* **Switching Order Issuance:** Request a formal Switching Order and Clearance Authorization from the System Operating Center (SOC) before initiating breaker manipulation.
* **Remote Racking Deployment:** Utilize a motorized remote racking mechanism positioned outside the 14.2 ft Arc Flash Boundary during breaker withdrawal and insertion.
* **Calibrated Test Equipment Check:** Ensure the high-voltage phased proximity detector is within its active calibration and recertification interval prior to Live-Dead-Live verification.
* **Safety Ground Placement:** Ensure grounds are sized to withstand maximum available short-circuit current (kA) for the required clearing time.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_id": "LOTO_CUBICLE_4_CLEARANCE_APPROVAL",
  "action_type": "MEDIUM_VOLTAGE_PHYSICAL_ISOLATION",
  "target_asset": "13.8kV Switchgear Bus 2 - Cubicle 4",
  "isolation_points": [
    "Breaker 4 Racked to Disconnected Position",
    "125VDC Control Fuse Block Cubicle 4 Aux",
    "120VAC Spring Charging Disconnect SW-04",
    "Potential Transformer Secondary Disconnect Fuses"
  ],
  "ppe_mandate": "40 cal/cm2 Category 4 Suit + Class 2 Dielectric Gloves",
  "verification_required": "Live-Dead-Live Instrument Protocol + Grounding Cluster Installation",
  "status": "PENDING_OPERATOR_CONFIRMATION"
}
```

### Example 2: Trend & Comparative Analysis
**User:** "Retrieve NFPA 70E arc flash boundary calculations and incident energy ratings (cal/cm²) for Substation West switchgear."

**Agent Response:**
### Executive Summary
**Arc flash hazard analysis for Substation West switchgear indicates maximum calculated incident energy levels of 24.6 cal/cm² on the 13.8 kV Main Bus, requiring NFPA 70E PPE Category 4 protection and an established Arc Flash Boundary of 11.8 feet (141.6 inches). Clearing times governed by upstream primary protection remain within standard IEEE 1584-2018 parameters, but secondary feeder bus sections exhibit elevated thermal exposure requiring strict Lockout/Tagout (LOTO) and maintenance switch mode engagement prior to physical racking or servicing. All personnel must strictly observe the designated approach boundaries and PPE mandates prior to executing any maintenance work inside the substation envelope.**

---

### Data Presentation

The table below summarizes the calculated arc flash boundaries, incident energy ratings, working distances, and NFPA 70E compliance metrics for Substation West switchgear lineups:

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **13.8 kV Main Bus A Incident Energy** | 24.60 cal/cm² | 20.00 cal/cm² | +23.0% | **Warning** |
| **13.8 kV Main Bus A Arc Flash Boundary** | 11.80 ft (141.6 in) | 10.00 ft | +18.0% | **Warning** |
| **13.8 kV Main Bus B Incident Energy** | 22.10 cal/cm² | 20.00 cal/cm² | +10.5% | **Warning** |
| **13.8 kV Main Bus B Arc Flash Boundary** | 10.90 ft (130.8 in) | 10.00 ft | +9.0% | **Warning** |
| **Feeder Breaker 12W-01 Incident Energy** | 18.50 cal/cm² | 15.00 cal/cm² | +23.3% | **Warning** |
| **Feeder Breaker 12W-01 Arc Flash Boundary** | 9.40 ft (112.8 in) | 8.00 ft | +17.5% | **Warning** |
| **4.16 kV Aux Switchgear Incident Energy** | 8.40 cal/cm² | 8.00 cal/cm² | +5.0% | **Normal** |
| **4.16 kV Aux Switchgear Arc Flash Boundary** | 5.70 ft (68.4 in) | 5.00 ft | +14.0% | **Normal** |
| **480V Station Service SWGR Incident Energy** | 4.20 cal/cm² | 4.00 cal/cm² | +5.0% | **Normal** |
| **480V Station Service Arc Flash Boundary** | 3.20 ft (38.4 in) | 3.00 ft | +6.7% | **Normal** |
| **Breaker Clearing Time (Arcing Duration)** | 185 ms | ≤ 150 ms | +23.3% | **Warning** |
| **Working Distance (13.8 kV Switchgear)** | 36.0 in (91.4 cm) | 36.0 in | 0.0% | **Normal** |

---

### Visualization Triggers

**Recommended Visualization:** Comparative Multi-Series Bar Chart displaying Incident Energy (cal/cm²), NFPA 70E PPE category thresholds, and Arc Flash Boundaries across all Substation West switchgear sections.

```json
{
  "chart_type": "bar",
  "data": {
    "categories": [
      "13.8kV Main Bus A",
      "13.8kV Main Bus B",
      "Feeder Breaker 12W-01",
      "Feeder Breaker 12W-02",
      "4.16kV Aux Switchgear",
      "480V Station Service SWGR"
    ],
    "series": [
      {
        "name": "Incident Energy (cal/cm²)",
        "data": [24.6, 22.1, 18.5, 17.9, 8.4, 4.2]
      },
      {
        "name": "PPE Level Upper Limit (cal/cm²)",
        "data": [40.0, 40.0, 25.0, 25.0, 25.0, 8.0]
      },
      {
        "name": "Arc Flash Boundary (ft)",
        "data": [11.8, 10.9, 9.4, 9.1, 5.7, 3.2]
      }
    ]
  }
}
```

---

### Actionable Recommendations

- **PPE Compliance**: Mandate minimum Category 4 PPE (40 cal/cm² rated arc flash suit, hood with face shield, voltage-rated gloves, and safety footwear) for all personnel operating within the 11.8 ft boundary of the 13.8 kV Main Bus sections.
- **Arc Energy Reduction Maintenance Switch (ARMS)**: Enable the Maintenance Mode / Quick-Trip selector on upstream relay protection prior to any racking, door-opening, or voltage-testing procedures to reduce clearing time from 185 ms to < 50 ms (lowering incident energy below 8 cal/cm²).
- **LOTO Boundary Enforcement**: Follow utility Standard Operating Procedure (SOP) SOP-SAF-402 for establishing verified zero-energy state, including physical lockouts, visible disconnect isolation, and three-point voltage verification before removing barrier panels.
- **Labeling Audit**: Inspect and verify that all physical warning labels on Substation West switchgear cubicles reflect IEEE 1584-2018 and NFPA 70E current study dates and boundary distances.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "PROTECTION_SETTING_OVERRIDE_AND_LOTO_PERMIT",
  "asset_id": "SUB_WEST_SWGR_13_8KV",
  "location": "Substation West - 13.8 kV Switchgear Room",
  "details": {
    "operation": "Engage Arc Flash Maintenance Switch (ARMS) and issue LOTO Master Switching Order",
    "target_breakers": ["CB-12W-MAIN-A", "CB-12W-MAIN-B", "CB-12W-T1"],
    "impact": "Lowers instantaneous trip delay from 185ms to 42ms; temporary loss of downstream selective coordination",
    "required_approvals": ["Field Safety Lead", "Substation Operations Dispatcher"]
  },
  "confirmation_status": "PENDING_HUMAN_IN_THE_LOOP_APPROVAL"
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Generate a site-specific LOTO switching clearance sheet and PPE checklist for maintenance work on 115kV Transformer T-3."

**Agent Response:**
### Executive Summary
**A comprehensive Lockout/Tagout (LOTO) clearance procedure and Arc Flash Risk Assessment have been generated for scheduled maintenance on 115kV Transformer T-3 in accordance with OSHA 1910.269 and NFPA 70E standards. The high-side 115kV and low-side 13.8kV isolation boundaries establish a Zero Energy State (ZES) with an incident energy exposure rated at $28.4\text{ cal/cm}^2$ requiring Category 4 PPE prior to verification and grounding. Physical execution of field switching, lock placement, and grounding constitutes a Tier 2 physical grid operation requiring certified Dispatcher and Switching Lead authorization.**

---

### Data Presentation

#### Table 1: Safety & Arc Flash Operational Parameters
| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Primary Nominal Voltage** | 115.0 kV | 115.0 kV | 0.0% | Normal |
| **Secondary Nominal Voltage** | 13.8 kV | 13.8 kV | 0.0% | Normal |
| **Arc Flash Boundary (Primary)** | 24.5 ft | 25.0 ft max | -2.0% | Normal |
| **Calculated Incident Energy (115kV)** | $28.4\text{ cal/cm}^2$ | $< 40.0\text{ cal/cm}^2$ | -29.0% | Warning |
| **Limited Approach Boundary** | 10.0 ft | 10.0 ft | 0.0% | Normal |
| **Restricted Approach Boundary** | 3.2 ft | 3.2 ft | 0.0% | Normal |
| **Clearance Execution Time Estimate** | 45 min | 60 min | -25.0% | Normal |

---

### Site-Specific LOTO Switching Clearance Sheet: 115kV Transformer T-3

**Clearance ID:** CLR-115KV-T3-MAINT  
**Asset ID:** 115kV/13.8kV Substation Power Transformer T-3  
**Applicable Standards:** OSHA 29 CFR 1910.269, NFPA 70E (2024), IEEE 1584-2018  

#### Step-by-Step Switching & Isolation Sequence:
1. **Notification & Verification:** Notify System Operations Control Center (OCC) and Substation Switching Coordinator. Confirm no active auto-reclose or SCADA override conflicts.
2. **Trip & Open Low-Side Breaker:** Open and rack out 13.8kV Feeder Breaker 52-3L. Apply LOTO Lock & Red "DANGER - DO NOT OPERATE" Tag on the breaker cubicle mechanism.
3. **Open Low-Side Disconnect Switch:** Open Disconnect Switch 89-3L. Visually verify air-gap open on all 3 phases. Install lock and tag.
4. **Trip & Open High-Side Breaker:** Open 115kV Circuit Breaker 52-3H. Lock and tag control switch and open trip circuit isolators.
5. **Open High-Side Motor-Operated Disconnect (MOD):** Open 115kV Disconnect Switch 89-3H. Visually verify three-phase physical blade separation and mechanical lock in open position.
6. **Auxiliary & Control Isolation:** 
   - Open and lock DC control knife switches for T-3 LTC (Load Tap Changer) and sudden pressure relay trip circuits.
   - De-energize and LOTO 480V/240V AC cooling fan and oil pump auxiliary supply breaker panel (Panelboard AC-T3).
7. **Zero Energy Verification (Live-Dead-Live Test):**
   - Test voltage detector on known energized source.
   - Test 115kV bushings (H1, H2, H3) and 13.8kV bushings (X1, X2, X3) for zero voltage.
   - Retest voltage detector on known energized source to confirm detector functionality.
8. **Apply Protective Grounds:** Install approved portable personal protective grounds (minimum 4/0 AWG copper) to high-side 115kV and low-side 13.8kV terminals, ground-end connection attached first.

---

### PPE & Arc Flash Safety Checklist

| Protection Category | Required PPE Specification | Activity Phase |
| :--- | :--- | :--- |
| **Arc Flash Rating** | $\ge 40\text{ cal/cm}^2$ (Category 4 Arc Flash Suit & Hood) | Racking breakers, opening manual disconnects, Live-Dead-Live testing |
| **Head & Face** | Hard hat with full-face arc shield, balaclava / arc flash hood | All switching & testing steps |
| **Eye & Ear** | ANSI Z87.1 safety glasses with side shields, hearing protection ($\ge 25\text{ NRR}$) | All clearance steps |
| **Hand Protection** | Class 4 (36kV rated) dielectric rubber gloves with leather protectors for 115kV; Class 2 for 13.8kV | Operating switches, voltage testing, ground installation |
| **Footwear** | EH-rated dielectric safety boots (ASTM F2413) | Substation yard maintenance |
| **Tools & Equipment** | Hot sticks rated for 115kV (tested per ASTM F711), calibrated phaser/detector | Zero-energy verification & ground placement |

---

### Visualization Trigger

**Chart Type:** Bar Chart (Approach Boundaries & Flash Protection Distances)  
```json
{
  "chart_type": "bar",
  "title": "115kV Transformer T-3 Approach & Arc Flash Boundaries",
  "data": {
    "labels": [
      "Flash Protection Boundary",
      "Limited Approach Boundary (Movable)",
      "Limited Approach Boundary (Fixed)",
      "Restricted Approach Boundary"
    ],
    "datasets": [
      {
        "label": "Distance (ft)",
        "data": [24.5, 10.0, 10.0, 3.2],
        "backgroundColor": ["#FF5722", "#FFC107", "#03A9F4", "#E91E63"]
      }
    ]
  }
}
```

---

### Actionable Recommendations
- **Pre-Job Briefing (Tailboard):** Conduct mandatory safety briefing with all field crew members reviewing isolation points, clearance boundaries, and emergency contact frequencies.
- **Visual Inspection of Grounding Studs:** Inspect transformer grounding pads and structural grounds for mechanical integrity and corrosion prior to attaching portable ground clamps.
- **Transfer of Control:** Ensure the Clearance Holder retains the physical clearance master key until all work is completed, grounds are removed, and the permit is formally surrendered to Operations.

---

### [TIER 2 ACTION REQUIRED]
```json
{
  "action_type": "LOTO_SWITCHING_CLEARANCE_EXECUTION",
  "tier_level": 2,
  "substation_id": "SUB-NORTH-115",
  "target_asset": "115kV Transformer T-3",
  "operation_summary": "Initiate physical isolation, opening of breakers 52-3H/52-3L, disconnects 89-3H/89-3L, zero-energy live-dead-live testing, and placement of utility safety grounds.",
  "required_approvals": [
    "Switching Lead (Certified Qualified Electrical Worker)",
    "System Dispatcher / Operations Control Center"
  ],
  "hold_point": "DO NOT PROCEED WITH SWITCHING OR GROUNDING UNTIL WRITTEN / VERBAL OCC DISPATCH PERMIT IS LOGGED AND CONFIRMED."
}
```
