# Antigravity/Agent guidance file (coding standards)

- Follow ADK v2 guidelines.
- Always use modular prompts (instructions/).
- No hardcoded GCP properties.
- Do not push to remote repo (e.g., git push) unless explicitly requested by the user.
- **Agent Identity Architecture:** All agents run under native Google Cloud Agent Identity (`identity_type: "AGENT_IDENTITY"` with `.agent_engine_config.json`) using cryptographic SPIFFE tokens. Static per-agent and per-domain service accounts are strictly prohibited.
- **Zero-Direct BigQuery Access on Orchestrator:** The Master Orchestrator (`utilities_master_orchestrator`) must never access BigQuery directly; all analytical queries and data retrieval must be delegated via `AgentDelegationTool` to domain agents.
- **Table-Level Least Privilege:** Domain agents are restricted strictly to their designated analytical tables in `utilities_{sub_domain}`.
- **Model Standardization & Routing:** Fleet standardized on `gemini-3.7-flash` with global routing (`GOOGLE_CLOUD_LOCATION="global"`).


