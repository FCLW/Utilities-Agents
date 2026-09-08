import os
# Ensure global endpoint for Gemini 3.7 Flash on Vertex AI
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

from google.adk import Agent
from .app_utils.prompt_loader import load_prompt_layer
from .tools.bigquery_tool import BigQueryQueryTool
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

persona = load_prompt_layer("persona")
business_rules = load_prompt_layer("business_rules")
safety_guardrails = load_prompt_layer("safety_guardrails")
output_format = load_prompt_layer("output_format")

instruction = f"{persona}\n\n{business_rules}\n\n{safety_guardrails}\n\n{output_format}"

agent = Agent(
    name="geothermal_output_forecaster",
    model="gemini-3.7-flash",
    instruction=instruction,
    tools=[BigQueryQueryTool(), VisualizerTool()]
)

task_lead_agent = agent
root_agent = agent
