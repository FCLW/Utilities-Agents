# ⚡ Flisr Switching Simulator

![Domain](https://img.shields.io/badge/Domain-grid%20operations-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of flisr switching simulator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Flisr Switching Simulator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank flisr switching simulator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_grid_operations.flisr_switching_simulator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Can Fault Location, Isolation, and Service Restoration (FLISR) automatically restore power to 1,400 customers on Feeder 12B?"

**Agent Response:**
### Executive Summary
**FLISR can automatically restore power to a substantial portion of the 1,400 customers on Feeder 12B by isolating the faulted line segment and reconfiguring healthy zones via upstream reclosing and downstream tie-switch transfers. However, full automated restoration of all 1,400 customers is physically constrained; customers located within the isolated fault zone (~300 customers) cannot be re-energized until field crews execute physical repairs. Automated backfeeding of the downstream section (~450 customers) is contingent upon reserve thermal capacity and voltage stability margins on the adjacent donor feeder.**

---

### Data Presentation

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Total Feeder 12B Customers** | 1,400 Cust | 1,400 Cust | 0.0% | Normal |
| **Upstream Zone Automated Restoration** | 650 Cust | 650 Cust | 0.0% | Normal |
| **Downstream Tie Transfer Restoration** | 450 Cust | 450 Cust | 0.0% | Normal |
| **Fault Isolation Zone (Manual Dispatch)** | 300 Cust | 0 Cust | N/A | Critical |
| **Adjacent Tie Feeder Available Capacity** | 2.4 MVA | 1.8 MVA (Req.) | +33.3% | Normal |
| **FLISR Sequence Execution Time** | 48 sec | < 60 sec | -20.0% | Normal |
| **Projected SAIDI Avoidance Impact** | 42.5 cust-hrs | 40.0 cust-hrs | +6.25% | Normal |

---

### Visualization Trigger
Recommended Chart: **Horizontal / Stacked Bar Chart** showing the customer breakdown by FLISR restoration state.

```json
{
  "chart_type": "bar",
  "title": "Feeder 12B FLISR Restoration Breakdown",
  "xAxis": {
    "categories": [
      "Upstream Healthy Zone",
      "Downstream Healthy Zone (Tie-Switch)",
      "Fault Isolation Zone (Manual Repair)",
      "Total Feeder Base"
    ]
  },
  "yAxis": {
    "title": "Number of Customers"
  },
  "series": [
    {
      "name": "Customer Count",
      "data": [650, 450, 300, 1400]
    }
  ]
}
```

---

### Actionable Recommendations

- **Arm FLISR Scheme for Automated Upstream Reclosing**: Enable the automated sectionalizing sequence to re-energize 650 upstream customers immediately following fault isolation verification.
- **Verify Tie Feeder Thermal & Voltage Margins**: Confirm that the adjacent tie feeder (e.g., Feeder 12A / Substation 4) maintains acceptable N-1 loading (< 80% thermal limit) and voltage profiles (> 0.95 p.u.) prior to closing normally open switch `NO-SW-12B-T1`.
- **Dispatch First-Response Repair Crew**: Issue an automated field work order to dispatch a line crew to the isolated section between Sectionalizer `SW-12B-3` and `SW-12B-4` for visual damage assessment and line clearance.
- **Maintain HITL Supervisory Control**: Ensure the distribution system operator validates tie-switch interlock conditions prior to autonomous remote close execution.

---

### [TIER 2 ACTION REQUIRED]
```yaml
tier_2_operation:
  action_type: "SCADA_FLISR_SWITCHING_EXECUTION"
  feeder_id: "Feeder 12B"
  substation_id: "SUB-04"
  switching_sequence:
    - step: 1
      device_id: "CB-12B-HEAD"
      operation: "TRIP_AND_LOCKOUT"
      status: "COMPLETED"
    - step: 2
      device_id: "SW-12B-3"
      operation: "OPEN"
      description: "Isolate fault upstream boundary"
    - step: 3
      device_id: "SW-12B-4"
      operation: "OPEN"
      description: "Isolate fault downstream boundary"
    - step: 4
      device_id: "CB-12B-HEAD"
      operation: "CLOSE"
      description: "Restore 650 upstream customers"
    - step: 5
      device_id: "NO-SW-12B-T1"
      operation: "CLOSE"
      description: "Tie-transfer restore 450 downstream customers"
  interlock_checks:
    thermal_overload_risk: "PASSED (Current loading at 72% post-transfer)"
    voltage_drop_check: "PASSED (0.972 p.u. at end-of-line)"
    sync_check: "NOT_REQUIRED (Radial tie transfer)"
  human_confirmation: "PENDING_OPERATOR_APPROVAL"
```

### Example 2: Trend & Comparative Analysis
**User:** "Simulate open-tie closing sequences to ensure adjacent Feeder 15 does not exceed its continuous thermal ampacity limit."

**Agent Response:**
### Executive Summary
**A power flow simulation of open-tie switching sequences was conducted to evaluate load transfer capacity into adjacent Feeder 15 while maintaining continuous thermal compliance.** **Direct execution of bulk tie switch TS-15-B would induce an overload condition of 640 A (106.7% of continuous thermal rating), violating operating limits.** **The staged multi-tie sequence (Option C) successfully restores isolated load by transferring 110 A to Feeder 15 (81.7% loading) and bifurcating remaining load to Feeder 18, preventing thermal overload and low-voltage violations.**

---

### Quantitative Simulation Analysis

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Feeder 15 Pre-Switching Load** | 380.0 A | 600.0 A Max Continuous | -36.7% | **Normal** |
| **Option A (TS-15-A Close - Zone 3 Only)** | 490.0 A | 600.0 A Max Continuous | -18.3% | **Normal** |
| **Option B (TS-15-B Close - Bulk Transfer)** | 640.0 A | 600.0 A Max Continuous | +6.7% | **Critical** |
| **Option C Feeder 15 Load (Staged Multi-Tie)** | 490.0 A | 600.0 A Max Continuous | -18.3% | **Normal** |
| **Option C Feeder 18 Load (Auxiliary Tie)** | 420.0 A | 600.0 A Max Continuous | -30.0% | **Normal** |
| **Feeder 15 End-of-Line Voltage (Option C)** | 0.962 p.u. | ≥ 0.950 p.u. (ANSI C84.1) | +1.3% | **Normal** |
| **Feeder 15 Phase Unbalance** | 2.4% | ≤ 3.0% Max Limit | -20.0% | **Normal** |

---

### Switching Sequence Telemetry & Thermal Margin Profile

```json
{
  "chart_type": "bar",
  "title": "Feeder 15 Thermal Loading Across Tie-Closing Sequences",
  "xAxis": {
    "title": "Switching Sequence Scenario",
    "categories": [
      "Pre-Switch Baseline",
      "Option A: Tie TS-15-A (Zone 3)",
      "Option B: Tie TS-15-B (Zone 2+3)",
      "Option C: Staged Multi-Tie (Optimal)"
    ]
  },
  "yAxis": {
    "title": "Current Loading (Amperes)",
    "threshold": 600
  },
  "series": [
    {
      "name": "Feeder 15 Projected Load (A)",
      "data": [380, 490, 640, 490]
    },
    {
      "name": "Continuous Thermal Rating (A)",
      "data": [600, 600, 600, 600]
    }
  ]
}
```

---

### Actionable Recommendations

1. **Reject Direct Closing of Tie Switch TS-15-B**: Block automated FLISR execution of single-point bulk transfer TS-15-B to prevent tripping Feeder 15 breaker on overcurrent.
2. **Execute Staged Multi-Tie Restoration (Option C)**:
   - **Step 1**: Open Sectionalizing Switch `SW-14-S3` to isolate downstream segment.
   - **Step 2**: Close Open-Tie Switch `TS-15-A` to restore Zone 3 via Feeder 15 (+110 A load transfer).
   - **Step 3**: Close Open-Tie Switch `TS-18-B` to restore Zone 2 via Feeder 18 (+150 A load transfer).
3. **Monitor Feeder 15 SCADA RTU Telemetry**: Verify real-time current magnitude and neutral unbalance remain below 510 A and 3.0% respectively post-transfer.

---

### [TIER 2 ACTION REQUIRED]

```json
{
  "action_type": "SCADA_FLISR_SWITCHING_EXECUTION",
  "safety_classification": "Tier 2 - Physical Grid Switching",
  "requires_hitl_approval": true,
  "execution_payload": {
    "switching_plan_id": "FLISR-PLAN-F15-OPT-C",
    "target_feeders": ["FEEDER-14", "FEEDER-15", "FEEDER-18"],
    "sequence": [
      {
        "step": 1,
        "device_id": "SW-14-S3",
        "command": "OPEN",
        "expected_state": "OPEN",
        "interlock_check": "VERIFIED_ZERO_VOLTAGE_OR_ISOLATED"
      },
      {
        "step": 2,
        "device_id": "TS-15-A",
        "command": "CLOSE",
        "expected_state": "CLOSED",
        "projected_feeder_load_amps": 490.0,
        "feeder_continuous_rating_amps": 600.0
      },
      {
        "step": 3,
        "device_id": "TS-18-B",
        "command": "CLOSE",
        "expected_state": "CLOSED",
        "projected_feeder_load_amps": 420.0,
        "feeder_continuous_rating_amps": 600.0
      }
    ]
  },
  "critic_agent_validation": {
    "status": "APPROVED_PENDING_DISPATCHER_CONFIRMATION",
    "thermal_overload_risk": "MITIGATED",
    "voltage_stability_check": "PASSED"
  }
}
```

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Execute automated FLISR switching sequence: open recloser R-3 and close mid-point tie switch TS-12 to isolate fault section."

**Agent Response:**
### 1. Executive Summary
**A FLISR automated switching simulation has been successfully generated to isolate the faulted feeder section by opening Recloser R-3 and closing Tie Switch TS-12. This reconfiguration isolates the downstream fault zone while safely backfeeding and restoring service to adjacent un-faulted segments without violating thermal or voltage limits. Per Grid Operations safety guardrails, autonomous physical SCADA execution is prohibited and requires Human-In-The-Loop (HITL) verification.**

---

### 2. Data Presentation (Simulation Metrics & Load Flow Analysis)

| Metric | Current Value | Baseline / Target | Delta (%) | Status (Normal/Warning/Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Tie Switch TS-12 Loading** | 245 A | 400 A (Continuous Rating) | -38.8% | Normal |
| **Backfeed Feeder Head Loading** | 68.4% | 85.0% (Emergency Limit) | -19.5% | Normal |
| **Minimum Node Voltage (Post-Switching)** | 0.965 p.u. | ≥ 0.950 p.u. (ANSI C84.1) | +1.58% | Normal |
| **Isolated Fault Customers** | 120 | 0 | N/A | Warning |
| **Restored Customers via TS-12** | 1,450 | 1,450 | 0.0% | Normal |
| **Estimated SAIDI Reduction** | 4.25 min | 0.0 min (Unmitigated) | -100.0% | Normal |

---

### 3. Visualization Trigger
```json
{
  "chart_type": "bar",
  "data_json": {
    "title": "FLISR Customer Restoration & Feeder Capacity Impact",
    "categories": ["Faulted Zone (Isolated)", "Restored via TS-12", "Original Healthy Zone"],
    "series": [
      {
        "name": "Customer Count",
        "data": [120, 1450, 2100]
      },
      {
        "name": "Feeder Load (A)",
        "data": [0, 245, 310]
      }
    ]
  }
}
```

---

### 4. Actionable Recommendations
- **Pre-Execution Check**: Verify that SCADA telemetry confirms zero-voltage / lock-out status on the isolated section upstream of Recloser R-3 before tie closure.
- **Operator Authorization**: Obtain formal dispatcher confirmation to proceed with remote command dispatch.
- **Field Crew Dispatch**: Automatically dispatch trouble crew to patrol and locate fault between Recloser R-3 and upstream sectionalizing points.

---

### [TIER 2 ACTION REQUIRED]
```yaml
Operation Type: SCADA Switching Execution / FLISR Restoration
Target Devices:
  - Device ID: R-3
    Action: OPEN (Isolate Downstream Fault)
    Substation/Feeder: Substation Alpha / Feeder 12B
    Current State: CLOSED (Tripped/Open pending confirmation)
  - Device ID: TS-12
    Action: CLOSE (Tie Backfeed Restoration)
    Substation/Feeder: Substation Beta / Feeder 08A
    Current State: OPEN
Interlocking Status: Interlocks Verified (Phase sync and thermal head-room validated)
Safety Level: Tier 2 - Human Confirmation Required
Action Required: Operator must review and explicitly authorize SCADA dispatch.
```
