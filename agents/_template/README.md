# ⚡ [Agent Display Name] (e.g., Substation Transformer DGA Health Monitor)

![Domain](https://img.shields.io/badge/Domain-[Sub_Domain_Name]-blue)
![ADK](https://img.shields.io/badge/Google_ADK-v2.0-orange)
![Model](https://img.shields.io/badge/Model-Gemini_2.5_Pro-green)

## 🏢 Business Problem
[Write a professional, 1-2 paragraph description. For example: In complex utility grids managing thousands of high-voltage assets, undetected insulation degradation quietly erodes capital efficiency and increases the risk of catastrophic outages. Post-failure forensics frequently discover that early warning signs in dissolved gas analysis (DGA) were overlooked for months. This autonomous agent continuously audits telemetry and maintenance logs, applying Duval Triangle rules to identify active arcing and thermal faults early, protecting grid reliability and deferring millions in replacement CapEx.]

## 🎯 What It Answers
* **Routed to Data Insights (BigQuery):**
  * **[Capability 1]** — [e.g., DGA Anomaly Detection: flags methane/ethylene spikes, match confidence scores, and historical degradation curves.]
  * **[Capability 2]** — [e.g., Asset Prioritization: cross-references thermal load history with DGA to rank transformers for immediate field inspection.]
* **Routed to External Grounding / Simulation:**
  * **[Capability 3]** — [e.g., Industry Benchmarking: retrieves standard IEEE loss-of-life calculations based on current operating temperatures.]

## ⚙️ Architecture & ADK Implementation
* **Task Lead:** `agent.py` coordinates the A2A workflow.
* **Worker Agent:** Queries the `[insert_table_name]` BigQuery table using the `BigQueryQueryTool` governed by `business_rules.md`.
* **Critic Agent:** Enforces structural formatting and scrubs PII based on `safety_guardrails.md`.

## 💬 Agent Response Examples

### Example 1: Quantitative Data Insight
**User:** "Analyze the latest DGA test results for Substation Alpha, specifically transformer TX-5543."

**Agent Response:**
Based on the August 2026 dissolved gas analysis, transformer **TX-5543** is exhibiting critical warning signs of **high-energy arcing**.

| Gas Type | Measured (ppm) | IEEE Threshold | Status |
|---|---|---|---|
| Methane (CH4) | 145 | 120 | ⚠️ High |
| Ethylene (C2H4) | 210 | 50 | 🚨 Critical |

**Recommendation:** The ratio of C2H4 to CH4 places this asset in the 'D2' zone of the Duval Triangle. I recommend immediately dispatching a field crew to perform an acoustic emission test and considering a temporary load transfer.

### Example 2: Market / Industry Grounding
**User:** "What are the typical industry benchmarks for transformer failure rates when ethylene levels exceed 200 ppm?"

**Agent Response:**
Based on external industry benchmarks and IEEE standards, when ethylene (C2H4) concentrations rapidly exceed 200 ppm without a corresponding spike in carbon monoxide, the probability of an unforced failure within 6 months increases by **400%**. 

Typical utility operational benchmarks suggest that assets in this risk tier should be deprioritized from base-load operation and scheduled for immediate oil filtration or complete unit overhaul.

