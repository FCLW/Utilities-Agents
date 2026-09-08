from google.adk import Agent
from pathlib import Path
import sys
import os

try:
    from config.settings import settings
except ImportError:
    class Settings:
        gcp_project_id = os.getenv("GCP_PROJECT_ID", "utilities-agents")
        gcp_region = os.getenv("GCP_REGION", "us-central1")
        gcp_location = os.getenv("GCP_LOCATION", "us-central1")
        llm_model_name = os.getenv("LLM_MODEL_NAME", "gemini-2.5-flash")
        reasoning_model_name = os.getenv("REASONING_MODEL_NAME", "gemini-2.5-pro")
        bq_dataset_name = os.getenv("BQ_DATASET_NAME", "utilities-agents")
    settings = Settings()
from ..app_utils.prompt_loader import load_prompt_layer

persona = load_prompt_layer("persona")
safety_guardrails = load_prompt_layer("safety_guardrails")
output_format = load_prompt_layer("output_format")

critic_instructions = f"{persona}\n\n{safety_guardrails}\n\n{output_format}\n\n" + \
    "You are the Critic. You will receive raw output from the Worker agent. You must:\n" + \
    "1) Verify no PII is leaked.\n" + \
    "2) Verify no destructive SQL was recommended.\n" + \
    "3) Format the data EXACTLY as specified in output_format.md (e.g., using Markdown tables).\n" + \
    "4) Strip out any internal 'thinking' logs."

flash_model = getattr(settings, 'llm_model_name', 'gemini-2.5-flash')

critic_agent = Agent(
    name="transformer_dga_health_monitor_critic",
    model=flash_model,
    instruction=critic_instructions,
    tools=[] # NO tools for the critic
)
