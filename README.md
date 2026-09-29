# ⚡ Gemini Enterprise Agents for Utilities

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-v2.0-orange.svg)](https://cloud.google.com/vertex-ai)
[![Gemini](https://img.shields.io/badge/Model-Gemini%203.7%20Flash-8E7CC3.svg)](https://ai.google.dev/)
[![Vertex AI](https://img.shields.io/badge/Agent%20Engine-Reasoning%20Engines-4285F4.svg)](https://cloud.google.com/vertex-ai)
[![Cloud Run](https://img.shields.io/badge/Web%20Portal-Cloud%20Run-4285F4.svg)](https://cloud.google.com/run)
[![BigQuery](https://img.shields.io/badge/Lakehouse-BigQuery-669DF6.svg)](https://cloud.google.com/bigquery)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

A production-ready enterprise multi-agent fleet comprising **113 specialized autonomous agents** across **10 business domains** (coordinated by the Universal Master Orchestrator). Built on the **Google Agent Development Kit (ADK) v2.0** and powered by Gemini models, the fleet orchestrates real-time BigQuery telemetry queries, dynamic visual charting, automated regulatory audits, and grounded industry intelligence.

---

## 🏛️ 4-Tier ADK Enterprise Architecture

The architecture enforces strict separation of concerns, defense-in-depth safety checks, and zero-trust data access:

```
┌────────────────────────────────────────────────────────────────────────┐
│               TIER 1: Experience & Delivery Layer                      │
│  • Gemini Enterprise (GE) App: Workspace Natural Language Chat & @-mentions
│  • Cloud Run Portal: Interactive Showcase secured by Google IAP        │
│  • Native Video Streaming: Same-origin HTTP 206 byte-range engine      │
│  • Inline Technical Specs: 113 Agent READMEs served via UTF-8 Markdown │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│             TIER 2: Agent Orchestration & Master Router                │
│  • Utilities Master Orchestrator (`utilities_master_orchestrator`)     │
│  • Zero-Direct-BigQuery Architecture: Pure A2A Intent Delegation       │
│  • Reasoning Model Fleet: `gemini-3.7-flash` (Global Vertex AI Routing)│
│  • Shared `UtilitiesSessionState` & OpenTelemetry / Cloud Trace Spans  │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│          TIER 3: Specialist Sub-Agents & Tool Suite                    │
│  ┌──────────────────────────────┐     ┌─────────────────────────────┐  │
│  │ Execution Sub-Agent (Worker) │ ──► │ Critic Sub-Agent (Safety)   │  │
│  │ Specialized logic & SQL      │     │ Audits guardrails & formats │  │
│  └──────────────────────────────┘     └─────────────────────────────┘  │
│  • BigQueryTool: Parameterized read-only SQL with table-level scoping  │
│  • SearchTool: Google Search Grounding for live LMP, weather & rules   │
│  • VisualizerTool: Dynamic Matplotlib charts & heat rate curves        │
│  • DelegationTool: Synchronous and asynchronous A2A handoffs           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              TIER 4: Enterprise BigQuery Lakehouse                     │
│  • 113 Partitioned & Clustered Tables across 10 Domain Datasets        │
│  • Cryptographic Agent Identity Principals (SPIFFE Authentication)     │
│  • Zero Static Service Account Keys (Compute Engine SA for Portal only)│
│  • Granular Table-Level Least-Privilege Access Controls                │
│  • Synthetic Data & DDL Schemas (`schema.sql`, `mock_records.csv`)     │
│  • Tiered Authorization: Autonomous Read/Simulate + HITL Action Gates   │
└────────────────────────────────────────────────────────────────────────┘
```

For complete technical specifications, see [ARCHITECTURE.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/ARCHITECTURE.md).

---

## 📊 Fleet Portfolio (113 Agents Across 10 Business Domains + Master Orchestrator)

| Sub-Domain | Count | Primary Focus | Key KPIs |
| :--- | :---: | :--- | :--- |
| **[Master Orchestrator](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/master_orchestrator)** | 1 | Global intent triage, cross-domain multi-agent routing | Routing Accuracy, Triage Latency |
| **[Asset Management](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/asset_management)** | 14 | Predictive maintenance, transformer DGA, wind/solar health | Asset Health Index (AHI), RUL |
| **[Billing & Invoicing](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/billing_and_invoicing)** | 11 | TOU billing, net metering, EV submetering, spike anomalies | Revenue Leakage, VEE Accuracy |
| **[Customer Engagement](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/customer_engagement)** | 11 | Outage notifications, high-bill weather explainer, EV plans | First-Contact Resolution, CSAT |
| **[Grid Balancing](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/grid_balancing)** | 11 | Frequency deviations, battery storage dispatch, islanding | Frequency Recovery Time, Loss % |
| **[Grid Operations](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/grid_operations)** | 11 | FLISR switching, black start restoration, wildfire mitigation | SAIDI, SAIFI, CAIDI, ETR Accuracy |
| **[Production Forecasting](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/production_forecasting)** | 12 | Solar/wind output, hydro snowpack, thermal availability | MAPE (<5%), Confidence Interval |
| **[Regulatory Compliance](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/regulatory_compliance)** | 10 | FERC Form 1, NERC CIP cybersecurity, EPA CEMS emissions | Filing Accuracy, Compliance Rate |
| **[Smart Meter Management](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/smart_meter_management)** | 10 | AMI interval VEE, tamper detection, demand response | VEE Clean Rate, Tamper Detection |
| **[Support Services](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/support_services)** | 10 | Arc flash safety (LOTO), PPA contract review, fleet repair | Safety Incident Rate, Order MTTR |
| **[Wholesale Trading](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/agents/wholesale_trading)** | 12 | Real-time LMP, spark spreads, FTR co-pilot, VaR analysis | Value at Risk (VaR), Sharpe Ratio |
| **Total Fleet** | **113** | **End-to-End Energy & Utilities Ecosystem** | **Production Grade** |

For the complete catalog of individual agent capabilities, datasets, and reasoning models, see [AGENTS.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/AGENTS.md) and [Utilities.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/Utilities.md).

---

## 📁 Repository Directory Structure

```
.
├── agents/                       # 113 Production Agent implementations
│   ├── asset_management/         # 14 Asset management agents
│   ├── billing_and_invoicing/    # 11 Billing & settlement agents
│   ├── customer_engagement/      # 11 Customer outreach & advisory agents
│   ├── grid_balancing/           # 11 Frequency & storage balancing agents
│   ├── grid_operations/          # 11 Outage & restoration agents
│   ├── master_orchestrator/       # 1 Universal master orchestrator
│   ├── production_forecasting/   # 12 Generation & load forecasting agents
│   ├── regulatory_compliance/    # 10 FERC, NERC, EPA compliance agents
│   ├── smart_meter_management/   # 10 AMI & meter operations agents
│   ├── support_services/         # 10 Safety, legal & enterprise agents
│   └── wholesale_trading/        # 12 LMP, spark spread & trading agents
│       └── <agent_name>/
│           ├── agent.py          # ADK agent declaration & callbacks
│           ├── fast_api_app.py   # Standalone HTTP service wrapper
│           ├── manifest.yaml     # Metadata, description & tool specs
│           ├── README.md         # Detailed agent technical specification
│           ├── app_utils/        # Modular prompt loaders
│           ├── instructions/     # 4-layer modular prompts
│           ├── sub_agents/       # Worker and Critic sub-agents
│           ├── tools/            # BigQuery, Search & Visualizer tools
│           ├── synthetic_data/   # SQL DDL schemas & mock generator
│           └── tests/            # Golden eval datasets & tests
├── grid_optimization/            # Autonomous ADK Multi-Agent System (8 Personas Swarm)
│   ├── agent.py                  # Root Orchestrator Agent (ADK Agent Identity & Routing)
│   ├── orchestrator.py           # Dynamic Workflow Dispatch & State Aggregator
│   ├── fast_api_app.py           # FastAPI service with telemetry endpoints
│   ├── telemetry.py              # OpenTelemetry Cloud Trace & Structured Logging
│   ├── .agent_engine_config.json # Native Agent Identity specification
│   ├── advanced_engines/         # WeatherNext 3, Vizier Bayesian VVO, PdM Health Engines
│   ├── personas/                 # 8 Specialized Grid Personas
│   ├── skills/                   # 12 Abstracted Grid Skills
│   ├── sub_agents/               # Execution & Critic Sub-Agents
│   ├── workflows/                # 6 Collaborative Multi-Agent Workflows
│   ├── safety/                   # Physics Validator & Tiered HITL Approval Gateway
│   ├── instructions/             # Modular system prompt layers
│   ├── tools/                    # Multi-dataset BigQuery tools with least-privilege scoping
│   └── tests/                    # Comprehensive pytest test suite (50 tests passing)
├── config/                       # Centralized settings & Pydantic models
├── data/                         # Verified live agent evaluation responses
├── scripts/                      # Automated management & deployment scripts
│   ├── build_catalog_json.py     # Aggregates metadata into web catalog
│   ├── deploy_agent_engine.py    # Deploys individual agent to Vertex AI Reasoning Engine
│   ├── deploy_all_and_register.py # Fleet deploy to Vertex AI Reasoning Engine & GE registration
│   ├── deploy_web_portal.py      # Cloud Build + Cloud Run deployment
│   ├── generate_web_portal.py    # Generates interactive web showcase
│   ├── load_bq_data.py           # BigQuery table initialization
│   ├── register_to_gemini_enterprise.py # Discovery Engine API registration
│   ├── setup_iam_permissions.py  # Agent Identity SPIFFE IAM configuration & validation
│   └── ...                       # Prompts, eval sync, and test tools
├── web/                          # Containerized web showcase (Cloud Run)
│   ├── catalog.json              # Structured fleet metadata
│   ├── index.html                # Interactive portal UI with emphasized MAS launch banner
│   ├── persona/                  # Grid Optimization Multi-Agent System Studio
│   │   ├── index.html            # Standalone Grid Optimization Studio entry point (served at /persona/)
│   │   ├── grid_optimization.html # Interactive MAS persona dashboard & simulation UI
│   │   ├── charts.js             # High-performance grid telemetry & waveform charts
│   │   ├── weathernext_data.js   # Live NWP & DLR for West and East Malaysia fleets
│   │   └── vizier_vvo_engine.js  # Vertex AI Vizier Bayesian Volt-VAR Optimization engine
│   ├── readmes/                  # All 113 Agent technical specifications
│   └── demos/                    # High-performance local demo assets bundled in container
├── AGENTS.md                     # Comprehensive agent reference catalog
├── ARCHITECTURE.md               # 4-Tier ADK architecture & sequence diagram
├── CONTRIBUTING.md               # Contribution guidelines & code standards
├── Dockerfile                    # Container definition for ADK agent runtime
├── Makefile                      # Standard developer command automation
├── pyproject.toml                # Dependencies and project metadata
├── REGISTRATION_GUIDE.md         # Gemini Enterprise registration manual
├── table_registry.yaml           # Schema registry for all 113 BigQuery tables
└── Utilities.md                  # Executive portfolio summary
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.11+
- Google Cloud SDK (`gcloud`) authenticated to a GCP project with BigQuery, Vertex AI, and Cloud Run APIs enabled.

### 2. Clone Repository & Setup Environment
```bash
git clone https://github.com/FCLW/Utilities-Agents.git
cd Utilities-Agents

# Copy environment template
cp .env.example .env
```
Configure your GCP project and BigQuery parameters:
```ini
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GCP_LOCATION=global
LLM_MODEL_NAME=gemini-3.7-flash
REASONING_MODEL_NAME=gemini-3.7-flash
```

### 3. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 4. Seed BigQuery Lakehouse & Provision Agent Identity
```bash
# Provision Agent Identity SPIFFE principals and domain-level dataset permissions
python3 scripts/setup_iam_permissions.py

# Audit Agent Identity security boundaries and table-level least privilege
python3 scripts/setup_iam_permissions.py --validate

# Initialize datasets, tables, and seed synthetic data
python3 scripts/load_bq_data.py
```

### 5. Local Web Portal Preview
```bash
# Rebuild metadata catalog and portal
make build

# Launch local preview server (port 8080)
make web
```

---

## ⚡ Grid Optimization Multi-Agent System (Persona MAS Studio)

The repository includes an autonomous, persona-driven **Grid Optimization Multi-Agent System (MAS)** designed for real-time electrical grid stability, automated switching, and predictive asset reliability:

### Key Features & Specialized Personas
- **8 Collaborative Grid Personas**: Grid Dispatcher, Protection & Control Engineer, Asset Reliability Specialist, DERMS Manager, Planning Engineer, Grid Analytics Data Scientist, Field Operations Tech, and Regulatory Compliance Officer.
- **6 Autonomous Collaborative Workflows**: Automated FLISR (Fault Location, Isolation, and Service Restoration), Dynamic Volt-VAR Optimization (VVO), N-1 Contingency Analysis, DER Hosting Capacity Evaluation, Predictive Maintenance Health Scoring, and Virtual Power Plant (VPP) Market Dispatch.
- **Google DeepMind WeatherNext 3 Live NWP & DLR**: Integrates 1-hour temporal resolution numerical weather prediction (temperature, wind speed, solar DNI, precipitation) mapped to IEEE Std 738 Dynamic Line Rating (DLR) across dedicated regional substation fleets in **West Malaysia** and **East Malaysia**.
- **Vertex AI Vizier Bayesian Volt-VAR Optimization**: Autonomous closed-loop Bayesian optimization adjusting substation transformer load-tap changers (LTC) and capacitor banks to minimize active power losses ($I^2R$) and eliminate reactive power violations along the Pareto frontier.
- **Multi-Modal Predictive Maintenance (PdM)**: Analyzes high-frequency acoustic emissions, Dissolved Gas Analysis (DGA Duval Triangle / Roger's Ratios), and tri-axial vibration FFT spectrograms to predict Remaining Useful Life (RUL) and prevent catastrophic substation asset failures.
- **ANSI C84.1 Physics Validation & Tiered HITL Gateway**: Enforces strict operational voltage bands ($0.95 \le V \le 1.05$ p.u.), transformer thermal limits, and IEEE 1547 anti-islanding safety with Human-in-the-Loop approval required for all physical grid mutative actions.
- **Native Google Cloud Agent Identity**: Executes under cryptographic SPIFFE tokens (`identity_type: "AGENT_IDENTITY"`) with direct least-privilege BigQuery lakehouse access.
- **Full Agent Platform Telemetry & Observability**: Complete OpenTelemetry Cloud Trace instrumentation (`--otel_to_cloud`), distributed trace context propagation, and Google Cloud structured logging.

### Access & Deployment
- **Deployed Reasoning Engine**: `projects/1032317060288/locations/us-east4/reasoningEngines/4768577531618000896`
- **Cloud Console Playground**: [Vertex AI Agent Engine Console](https://console.cloud.google.com/vertex-ai/agents/agent-engines/locations/us-east4/agent-engines/4768577531618000896/playground?project=1032317060288)
- **Web Portal Persona Studio**: `https://utilities-agents-portal-1032317060288.us-central1.run.app/persona/` (directly accessible via the **⚡ Grid Optimization MAS** button on the portal header).
- **Run Tests Locally**:
  ```bash
  pytest grid_optimization/tests/
  ```

---

## 🚢 Deployment & Production Operations

### Deploy Reasoning Engines (Vertex AI Agent Engine)
Deploy the 114 Reasoning Engines (113 specialized agents + Master Orchestrator) under native Agent Identity:
```bash
python3 scripts/deploy_all_and_register.py
```

### Deploy Web Portal to Cloud Run
The showcase web portal runs on Cloud Run, authenticated via Google Identity-Aware Proxy (IAP) and operating under the Compute Engine default service account:
```bash
make deploy-portal
# Or directly:
python3 scripts/deploy_web_portal.py
```

### Register Fleet with Gemini Enterprise
Register all deployed agents with the Discovery Engine Agent Registry:
```bash
python3 scripts/register_to_gemini_enterprise.py
```
For manual Workspace Admin Console binding, consult the [REGISTRATION_GUIDE.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/REGISTRATION_GUIDE.md).

---

## 🔒 Security, Safety & Governance

- **Native Cryptographic Agent Identity:** Every agent reasoning engine runs under first-class Google Cloud **Agent Identity** (`identity_type: "AGENT_IDENTITY"`), using SPIFFE-verifiable tokens (`principal://agents.global.project-...`) with dynamic workload identity federation. All legacy static per-agent and domain service account keys have been completely decommissioned.
- **Compute Engine Default Service Account:** The single remaining service account in the GCP project is `1032317060288-compute@developer.gserviceaccount.com`, used exclusively for Cloud Run web hosting and Cloud Build execution.
- **Zero-Direct BigQuery Access for Master Orchestrator:** Under defense-in-depth rules, the `utilities_master_orchestrator` has no direct BigQuery tools or dataset permissions. It purely performs intent classification and delegates queries to domain specialists via `AgentDelegationTool`.
- **Granular Table-Level Least Privilege:** Domain agents have access restricted strictly to their designated analytical tables within their domain dataset (`utilities_{domain}`). Cross-domain and unauthorized table queries are strictly blocked.
- **Defense-in-Depth SQL Safety:** BigQuery tools enforce parameterized read-only queries. Regex guards immediately reject any destructive SQL (`DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `TRUNCATE`).
- **The Critic Protocol:** Every agent contains a dedicated `CriticSubAgent` that intercepts model outputs and verifies compliance against `safety_guardrails.md` before returning responses to callers.
- **Identity-Aware Proxy (IAP):** Web portal access is gated to authenticated corporate identity domains (`@google.com`).

---

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

