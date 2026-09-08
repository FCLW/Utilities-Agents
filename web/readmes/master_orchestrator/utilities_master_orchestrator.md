# ⚡ Utilities Master Orchestrator

![Domain](https://img.shields.io/badge/Domain-master%20orchestrator-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
In the fast-paced and highly regulated Energy & Utilities sector, manual tracking and analysis of utilities master orchestrator is inherently error-prone, fragmented, and slow. Unresolved inefficiencies in this area quietly erode capital efficiency, impact grid reliability, and increase the risk of regulatory penalties or catastrophic outages. This autonomous agent continuously audits telemetry, financial data, and maintenance logs, applying advanced analytical rules to identify active anomalies and critical faults early. By autonomously flagging these risks, the agent protects infrastructure reliability, optimizes workforce deployment, and defers millions in CapEx and OpEx.

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **Capability 1** — Utilities Master Orchestrator Anomaly Detection: flags statistical outliers, match confidence scores, and historical degradation curves.
  * **Capability 2** — Operational Prioritization: cross-references load history and risk models to rank utilities master orchestrator events for immediate action.
* **Routed to External Grounding / Simulation:**
  * **Capability 3** — Industry Benchmarking: retrieves standard IEEE/FERC compliance rules and benchmarks based on current operating metrics.

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `utilities_master_orchestrator.utilities_master_orchestrator_logs` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "Which specialized agents are currently handling active telemetry anomalies across the distribution grid?"

**Agent Response:**
In the Energy & Utilities orchestration framework, active telemetry anomalies across the distribution grid are managed and resolved through the following specialized sub-agents coordinated by the **Utilities Master Orchestrator**:

---

### 1. **Utilities Execution Agent (`utilities_master_orchestrator_execution`)**
* **Primary Role:** Operational dispatch and automated mitigation.
* **Responsibilities:**
  * Executes automated grid stabilization actions (e.g., dynamic load shedding, Volt/VAR optimization, tap-changer adjustments).
  * Generates and routes field service/crew dispatch orders for physical asset anomalies.
  * Implements corrective switching plans and recloser operational adjustments to isolate fault conditions.

---

### 2. **Utilities Critic & Validation Agent (`utilities_master_orchestrator_critic`)**
* **Primary Role:** Quality assurance, constraint validation, and safety verification.
* **Responsibilities:**
  * Verifies telemetry anomaly detections against regulatory, safety, and operating threshold constraints (NERC/FERC guidelines).
  * Critiques proposed execution plans to ensure power quality standards (IEEE 519/1547) and thermal limits are not breached.
  * Flags false positives or high-risk operational proposals before executing grid modifications.

---

### 3. **Utilities Master Orchestrator (`utilities_master_orchestrator`)**
* **Primary Role:** Central supervisory coordinator.
* **Responsibilities:**
  * Telemetry stream ingestion, cross-referencing BigQuery asset databases and external conditions (e.g., weather feeds).
  * Triages and assigns anomalies to appropriate diagnostic routines and sub-agents.
  * Synthesizes health index scores (e.g., asset operational status and telemetry variance) to maintain real-time distribution grid situational awareness.

### Example 2: Trend & Comparative Analysis
**User:** "Audit cross-agent routing latency and dispatch accuracy for storm event #2026-B."

**Agent Response:**
### Audit Report: Cross-Agent Routing Latency & Dispatch Accuracy
**Event ID:** `#2026-B`  
**Audit Status:** `COMPLETED / VERIFIED`

---

### 1. Performance & Telemetry Summary

| Event ID | Metric / Indicator | Value | Benchmark / SLA Target | Compliance Status |
| :--- | :--- | :--- | :--- | :--- |
| **2026-B** | Average Routing Latency | `14.2 ms` | < 50.0 ms | **PASS** |
| **2026-B** | Dispatch Accuracy Score | `88.5%` | > 85.0% | **PASS** |
| **2026-B** | System Operational Status | `Active` | Active | **PASS** |
| **2026-B** | Monitored Asset ID | `ASSET-101` | — | **LOGGED** |

---

### 2. Safety & Governance Review

| Verification Item | Assessment | Details |
| :--- | :--- | :--- |
| **SQL Query Safety** | **APPROVED** | Read-only queries executed (`SHOW`, `SELECT`). No DDL/DML mutations (`DROP`, `DELETE`, `INSERT`, `ALTER`, `TRUNCATE`) detected. |
| **Operation Tier Classification** | **TIER 1 (Read-Only)** | No mutative grid control or financial transactions detected. No HITL escalation required. |
| **PII & Data Leakage** | **CLEARED** | No Personally Identifiable Information (PII) identified in telemetry logs or query outputs. |
| **Data Integrity** | **VALIDATED** | Records processed and structured without hallucination or calculation anomalies. |

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "Initiate a multi-agent emergency coordination protocol across Grid Operations and Crew Dispatch."

**Agent Response:**
The multi-agent emergency coordination protocol has been successfully initiated across **Grid Operations** and **Crew Dispatch**:

### 1. Grid Operations
- **Task Initiated:** Emergency assessment, fault/outage isolation, and operational metrics analysis.
- **Status:** Completed operational assessment and established baseline metrics for dispatch coordination.

### 2. Crew Dispatch
- **Task Initiated:** Emergency crew resource allocation, route optimization, and synchronization with Grid Operations findings.
- **Status:** Emergency response crews mobilized and dispatched based on real-time grid operational status.

### Summary
Inter-agent communication and data exchange between Grid Operations and Crew Dispatch are active, enabling dynamic resource re-routing and prioritized power restoration across all critical operational zones.
