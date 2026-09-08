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
from ..tools.bigquery_tool import BigQueryQueryTool
from ..tools.search_tool import GoogleSearchTool
from ..tools.visualizer import VisualizerTool

persona = load_prompt_layer("persona")
business_rules = load_prompt_layer("business_rules")
safety_guardrails = load_prompt_layer("safety_guardrails")

worker_instructions = f"{persona}\n\n{business_rules}\n\n{safety_guardrails}\n\n" + \
    "You are the execution worker. Use your tools to fetch data and solve the user's query. Return raw, unformatted data and your reasoning steps."

reasoning_model = getattr(settings, 'reasoning_model_name', 'gemini-2.5-pro')

worker_agent = Agent(
    name="wildfire_risk_deenergization_trigger_worker",
    model=reasoning_model,
    instruction=worker_instructions,
    tools=[BigQueryQueryTool(), GoogleSearchTool(), VisualizerTool()]
)
