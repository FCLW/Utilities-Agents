# Contributing to Gemini Enterprise Agents for Utilities

Thank you for your interest in contributing to the **Gemini Enterprise Agents for Utilities** repository! This project delivers a suite of 113 specialized autonomous agents built on the **Google Agent Development Kit (ADK) v2.0** and powered by Google Gemini reasoning models.

---

## 1. Core Architecture & Coding Standards

All contributions must follow the repository standards defined in [GEMINI.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/GEMINI.md) and [ARCHITECTURE.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/ARCHITECTURE.md):

1. **Google ADK v2.0 Guidelines:**
   - Agents must be built using `google-adk[gcp]>=2.0.0`.
   - Use declarative tools and lifecycle callbacks (`before_model_call`, `after_model_call`).
2. **Modular Prompts (`instructions/`):**
   - **Never hardcode large prompt blocks** in Python source files.
   - Always load prompts from modular markdown templates under `instructions/`:
     - `persona.md` (Domain identity, role, and capabilities)
     - `business_rules.md` (Operational equations, thresholds, and dispatch logic)
     - `output_format.md` (Structured tables, Markdown formatting)
     - `safety_guardrails.md` (NERC/FERC compliance, PII redaction, bounds checking)
3. **Task Lead Pattern (Worker + Critic Gate):**
   - Each specialist agent must implement an internal **Critic Sub-Agent** acting as a safety gatekeeper to inspect outputs, audit guardrails, prevent hallucinations, and enforce structured formats.
4. **Environment & Secrets:**
   - **No hardcoded GCP properties** (project IDs, dataset IDs, regions, or service accounts).
   - All configuration must load dynamically via `config/settings.py` backed by environment variables (see `.env.example`).
5. **Directory Hierarchy:**
   - Follow the standardized layout: `agents/<sub_domain>/<agent_id>/`.

---

## 2. Development Setup

### Prerequisites
- Python 3.11+
- Google Cloud SDK (`gcloud`) authenticated with a project having Vertex AI & BigQuery APIs enabled.
- `uv` or `pip`

### Initializing Environment
```bash
# Clone the repository
git clone <repo-url>
cd Utilities-Agents

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -e ".[dev]"
```

---

## 3. Scaffolding a New Agent

To add a new specialist agent to the fleet:

```bash
# Run the scaffolding utility
python3 scripts/scaffold_agent.py --domain <sub_domain> --name <agent_name>
```

This generates the standard ADK layout:
```
agents/<sub_domain>/<agent_name>/
├── agent.py               # Main ADK agent entrypoint
├── fast_api_app.py        # Standalone HTTP service wrapper
├── manifest.yaml          # Agent metadata & tool declarations
├── README.md              # Technical specification
├── app_utils/             # Modular prompt loaders
├── instructions/          # 4-layer modular prompts
├── sub_agents/            # Worker and Critic sub-agents
├── tools/                 # BigQuery, Search, and Visualization tools
├── synthetic_data/        # SQL DDL schemas and mock generator
└── tests/                 # Unit, integration, and golden eval tests
```

---

## 4. Testing & Verification

Before submitting changes, run the validation test suite:

```bash
# Run all unit tests
make test

# Rebuild catalog and verify schema consistency
make build

# Launch the local web portal to preview changes
make web
```

---

## 5. Pull Request Guidelines

1. **Atomic Commits:** Make descriptive, conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`).
2. **Evaluation Datasets:** If modifying an agent's reasoning or tools, update its golden evaluation dataset in `tests/eval/datasets/golden-dataset.json`.
3. **Documentation:** Update [AGENTS.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/AGENTS.md) and [Utilities.md](file:///usr/local/google/home/xwangx/agy2-projects/Utilities-Agents/Utilities.md) if adding, renaming, or modifying agents.
4. **Clean Commits:** Do not commit `.env`, `*.csv` files, or video binaries (`demos/`).
