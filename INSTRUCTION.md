# Deployment Runbook

This is a comprehensive, step-by-step deployment and operational runbook for standing up the Enterprise Utilities Agents Suite.

## Prerequisites

Ensure you have the following installed on your local machine or development environment:
- **`gcloud` CLI**: Google Cloud SDK for authenticating and managing GCP infrastructure.
- **Python 3.11+**: Runtime environment for Google ADK, FastAPI, and data engineering scripts.
- **Docker**: Container engine for building and packaging the Cloud Run web showcase portal.
- **FFmpeg & Playwright (Python)**: Required for automated 1080p demo video recording (`pip install playwright && playwright install chromium`).

---

## Step 1: Clone & Configure Environment

1. Clone the repository and enter the directory:
   ```bash
   git clone https://github.com/FCLW/Utilities-Agents.git
   cd Utilities-Agents
   ```

2. Initialize your local environment file from the template:
   ```bash
   cp .env.example .env
   ```

3. Open `.env` and verify your target Google Cloud parameters:
   ```bash
   # Google Cloud Configuration
   GCP_PROJECT_ID=utilities-agents
   GCP_REGION=us-central1
   GCP_LOCATION=us-central1

   # Model Configuration
   LLM_MODEL_NAME=gemini-3.7-flash
   REASONING_MODEL_NAME=gemini-3.1-pro

   # BigQuery Configuration
   BQ_DATASET_NAME=utilities-data
   ```

---

## Step 2: Authenticate with Google Cloud

Authenticate your environment with your user credentials and Application Default Credentials (ADC):

```bash
# Authenticate gcloud CLI
gcloud auth login

# Set active project
gcloud config set project utilities-agents

# Generate Application Default Credentials for Python SDKs
gcloud auth application-default login
```

---

## Step 3: Execute Automated Provisioning Pipeline

Run the automated pipeline scripts in sequence from the project root:

```bash
# 1. Create IAM Service Accounts and grant BigQuery least-privilege roles
python3 scripts/setup_iam_permissions.py

# 2. Provision BigQuery datasets, tables, and load synthetic seed telemetry data
python3 scripts/load_bq_data.py

# 3. Deploy the 113 agents to Vertex AI Reasoning Engine and register in Gemini Enterprise
python3 scripts/deploy_all_and_register.py
```

### Video Demos & Portal Assets (Optional / Pre-Recorded)

The repository comes with pre-recorded 1080p MP4 demos for all 113 agents hosted in `gs://utilities-agents-demos/`. If you wish to regenerate demo videos or HTML players:

```bash
# Record 1080p MP4 videos using Playwright & FFmpeg
python3 scripts/record_agent_demo.py --all

# Compile standalone HTML demo players linking local & GCS video sources
python3 scripts/generate_demo_html.py
```

---

## Step 4: Build & Deploy Showcase Web Portal (Cloud Run)

1. Compile the master catalog JSON and web frontend:
   ```bash
   python3 scripts/build_catalog_json.py
   python3 scripts/generate_web_portal.py
   ```

2. Deploy the containerized Nginx portal to Cloud Run:
   ```bash
   python3 scripts/deploy_web_portal.py
   ```
   *Note: The deployment script utilizes Cloud Build to pull the 1.9 GiB MP4 video fleet directly from `gs://utilities-agents-demos` over Google's internal datacenter network and bundles them into the container with HTTP 206 byte-range streaming enabled.*

---

## Step 5: Verification & Testing

1. **Unit & Tool Tests**: Run deterministic tests on tools and SQL regex guardrails:
   ```bash
   pytest agents/
   ```

2. **Live Agent Portfolio Evaluation**: Test deployed Vertex AI Reasoning Engines across multi-turn prompts:
   ```bash
   python3 scripts/live_agent_portfolio_tester.py
   ```

3. **Explore the Showcase Portal Locally**:
   ```bash
   make web
   ```
   Open `http://localhost:8000` in your browser to test filtering, search, and Markdown specification views.

4. **Production Web Access**:
   Access the deployed Cloud Run service URL behind Identity-Aware Proxy (IAP) at:
   `https://utilities-agents-portal-ilrdua3y3q-uc.a.run.app`
