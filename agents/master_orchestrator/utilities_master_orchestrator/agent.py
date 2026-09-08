import os
# Ensure global endpoint for Gemini 3.7 Flash on Vertex AI
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

from google.adk import Agent
from pathlib import Path
from .sub_agents.execution_agent import execution_agent
from .sub_agents.critic_agent import critic_agent
from .tools.bigquery_tool import BigQueryQueryTool
from .tools.search_tool import GoogleSearchTool
from .tools.visualizer import VisualizerTool

try:
    from config.settings import settings
except ImportError:
    class Settings:
        gcp_project_id = os.getenv("GCP_PROJECT_ID", "utilities-agents")
        gcp_region = os.getenv("GCP_REGION", "us-central1")
        gcp_location = "global"
        llm_model_name = os.getenv("LLM_MODEL_NAME", "gemini-3.7-flash")
        reasoning_model_name = os.getenv("REASONING_MODEL_NAME", "gemini-3.7-flash")
        bq_dataset_name = os.getenv("BQ_DATASET_NAME", "utilities-agents")
    settings = Settings()
try:
    from .config.model_armor import get_model_armor_callbacks
    armor_callbacks = get_model_armor_callbacks()
except ImportError:
    try:
        from config.model_armor import get_model_armor_callbacks
        armor_callbacks = get_model_armor_callbacks()
    except ImportError:
        armor_callbacks = {}


agent = Agent(
    name="utilities_master_orchestrator",
    model="gemini-3.7-flash",
    instruction="You are the Utilities Master Orchestrator for Energy & Utilities workflows. You coordinate across specialized sub-agents to analyze telemetry, calculate metrics, and execute operational recommendations.",
    sub_agents=[execution_agent, critic_agent],
    tools=[BigQueryQueryTool(), GoogleSearchTool(), VisualizerTool()],
    **armor_callbacks
)

task_lead_agent = agent
root_agent = agent
