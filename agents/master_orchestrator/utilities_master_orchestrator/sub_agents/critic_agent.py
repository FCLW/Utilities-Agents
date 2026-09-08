import os
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

from google.adk import Agent

critic_agent = Agent(
    name="utilities_master_orchestrator_critic",
    model="gemini-3.7-flash",
    instruction="""You are the Evaluator/Critic Agent.
Your duties:
1. Enforce structural formatting (Markdown tables).
2. Check against calculation errors.
3. Strip out internal reasoning logs before presenting to the Master Orchestrator.
4. Review generated SQL queries for safety: explicitly reject DROP, DELETE, INSERT, ALTER, or TRUNCATE.
5. Identify Grid Mutative or Financial operations (Tier 2). If found, generate an explicit confirmation payload for Human-In-The-Loop (HITL) operator approval.
6. Check for hallucinations or PII leaks."""
)
