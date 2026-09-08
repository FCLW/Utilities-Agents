# ⚡ Gemini Enterprise Agents for Utilities

[![Python](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-v2.0-orange.svg)](https://cloud.google.com/vertex-ai)
[![Gemini](https://img.shields.io/badge/Model-Gemini%203.7%20Flash%20%7C%203.1%20Pro-8E7CC3.svg)](https://ai.google.dev/)
[![Cloud Run](https://img.shields.io/badge/Deployed-Cloud%20Run-4285F4.svg)](https://cloud.google.com/run)
[![BigQuery](https://img.shields.io/badge/Lakehouse-BigQuery-669DF6.svg)](https://cloud.google.com/bigquery)
[![License](https://img.shields.io/badge/License-Apache%202.0-green.svg)](LICENSE)

A production-ready enterprise multi-agent fleet comprising **113 specialized autonomous agents** across **11 core energy and utilities sub-domains**. Built on the **Google Agent Development Kit (ADK) v2.0** and powered by Gemini models, the fleet orchestrates real-time BigQuery telemetry queries, dynamic visual charting, automated regulatory audits, and grounded industry intelligence.

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
│  • Agent-to-Agent (A2A) Routing Protocol                               │
│  • Dual Model Fleet: `gemini-3.7-flash` (triage) & `gemini-3.1-pro`    │
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
│  • BigQueryTool: Parameterized read-only SQL with regex DDL/DML guards │
│  • SearchTool: Google Search Grounding for live LMP, weather & rules   │
│  • VisualizerTool: Dynamic Matplotlib charts & heat rate curves        │
│  • DelegationTool: Synchronous and asynchronous A2A handoffs           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│              TIER 4: Enterprise BigQuery Lakehouse                     │
│  • 113 Partitioned & Clustered Tables (`table_registry.yaml`)          │
│  • Dedicated Least-Privilege IAM Service Accounts per Agent            │
│  • Synthetic Data & DDL Schemas (`schema.sql`, `mock_records.csv`)     │
│  • Tiered Authorization: Autonomous Read/Simulate + HITL Action Gates   │
└────────────────────────────────────────────────────────────────────────┘
```

For complete technical specifications, see [ARCHITECTURE.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/ARCHITECTURE.md).

---

## 📊 Fleet Portfolio (113 Agents Across 11 Domains)

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
├── config/                       # Centralized settings & Pydantic models
├── data/                         # Verified live agent evaluation responses
├── scripts/                      # 17 Automated management & deployment scripts
│   ├── build_catalog_json.py     # Aggregates metadata into web catalog
│   ├── deploy_web_portal.py      # Cloud Build + Cloud Run deployment
│   ├── generate_web_portal.py    # Generates interactive web showcase
│   ├── load_bq_data.py           # BigQuery table initialization
│   ├── register_to_gemini_enterprise.py # Discovery Engine API registration
│   └── ...                       # Prompts, eval sync, and test tools
├── web/                          # Containerized web showcase
│   ├── catalog.json              # Structured fleet metadata
│   ├── index.html                # Interactive portal UI
│   └── readmes/                  # All 113 Agent technical specifications
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
- Google Cloud SDK (`gcloud`) authenticated to a GCP project with:
  - BigQuery API
  - Vertex AI API
  - Cloud Run API
  - Discovery Engine API (for Gemini Enterprise)

### 2. Environment Configuration
Copy the provided `.env.example` template:
```bash
cp .env.example .env
```
Configure your GCP project and BigQuery parameters:
```ini
GCP_PROJECT_ID=your-project-id
GCP_REGION=us-central1
GCP_LOCATION=us-central1
LLM_MODEL_NAME=gemini-3.7-flash
REASONING_MODEL_NAME=gemini-3.1-pro
BQ_DATASET_NAME=utilities_data
```

### 3. Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 4. Seed BigQuery Lakehouse
```bash
# Provision IAM service accounts with least privilege
python3 scripts/setup_iam_permissions.py

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

## 🚢 Deployment & Production Operations

### Deploy Web Portal to Cloud Run
The web portal packages Nginx with Identity-Aware Proxy (IAP) integration:
```bash
make deploy-portal
# Or directly:
python3 scripts/deploy_web_portal.py
```

### Register Fleet with Gemini Enterprise
Register all 113 agents with the Discovery Engine Agent Registry:
```bash
python3 scripts/register_to_gemini_enterprise.py
```
For manual Workspace Admin Console binding, consult the [REGISTRATION_GUIDE.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/REGISTRATION_GUIDE.md).

---

## 🔒 Security, Safety & Governance

- **Zero-Trust BigQuery Tool:** Uses parameterized read-only queries. Regex guards immediately reject any destructive SQL (`DROP`, `DELETE`, `INSERT`, `UPDATE`, `ALTER`, `TRUNCATE`).
- **The Critic Protocol:** Every agent contains a dedicated `CriticSubAgent` that intercepts model outputs and verifies compliance against `safety_guardrails.md` before returning responses to callers.
- **Identity-Aware Proxy (IAP):** Web portal access is gated to authenticated corporate identity domains (`@google.com`).
- **Least-Privilege IAM:** Dedicated per-agent service accounts with minimal `roles/bigquery.dataViewer` and `roles/bigquery.jobUser` roles.

---

## 📄 License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
