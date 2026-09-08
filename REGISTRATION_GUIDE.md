# Gemini Enterprise App Registration Guide

This guide explains how to make the **113 Utility Agents** (1 Master Orchestrator + 112 Specialized Domain Agents across 10 industry sub-domains) available in the Gemini Enterprise App within Google Workspace.

---

## Method 1: Automated Registration via Discovery Engine API (Recommended)

The automated script [`scripts/register_to_gemini_enterprise.py`](scripts/register_to_gemini_enterprise.py) registers deployed Vertex AI Reasoning Engines directly with the Discovery Engine Agent Registry:

```bash
# Register all deployed Reasoning Engine agents to Gemini Enterprise
python3 scripts/register_to_gemini_enterprise.py
```

This registers the agent name, description, tool declarations, and authorization bindings directly into Gemini Enterprise.

---

## Method 2: Manual Registration via Google Workspace Admin Console

If your organization manages Gemini extensions through the central Workspace Admin directory:

1. Sign in to the **Google Workspace Admin Console** ([admin.google.com](https://admin.google.com)) with Administrator privileges.
2. Navigate to **Apps** -> **Google Workspace** -> **Gemini** -> **Extensions & Agent Integrations** (or the corresponding section for your Gemini Enterprise tier).
3. Click **Add Extension** / **Register Agent** and choose **Vertex AI Reasoning Engine** as the source type.
4. When prompted for the Google Cloud Project, select **`utilities-agents`** (Project Number: `1032317060288`, Region: `us-central1`).
5. Select the Reasoning Engine instances you want to enable (such as `utilities_master_orchestrator` as the primary universal entrypoint).
6. Set organizational unit (OU) sharing rules and click **Save & Publish**.

---

## End-User Access in Gemini Enterprise

Once registered:
- **Direct Chat:** Users can select individual specialized agents from the extension list.
- **Master Orchestrator:** Users can converse directly with the **`utilities_master_orchestrator`**, which will automatically classify user intent and route tasks to downstream domain agents using the Agent-to-Agent (A2A) protocol.
- **@-Mentions:** Users can @-mention specific agents in chat prompts (e.g., `@circuit_breaker_wear_analyzer check health for Substation 4B breaker`).
