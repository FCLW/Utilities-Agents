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
try:
    from .config.model_armor import get_model_armor_callbacks
    armor_callbacks = get_model_armor_callbacks()
except ImportError:
    try:
        from config.model_armor import get_model_armor_callbacks
        armor_callbacks = get_model_armor_callbacks()
    except ImportError:
        armor_callbacks = {}

try:
    from .config.telemetry import get_telemetry_callbacks, combine_agent_callbacks
except ImportError:
    try:
        from config.telemetry import get_telemetry_callbacks, combine_agent_callbacks
    except ImportError:
        def get_telemetry_callbacks(name): return {}
        def combine_agent_callbacks(*dicts):
            c = {}
            for d in dicts:
                if d: c.update(d)
            return c

telemetry_callbacks = get_telemetry_callbacks(agent_name="scada_vpn_access_helpdesk_bot")
callbacks = combine_agent_callbacks(armor_callbacks, telemetry_callbacks)


persona = load_prompt_layer("persona")
business_rules = load_prompt_layer("business_rules")
safety_guardrails = load_prompt_layer("safety_guardrails")
output_format = load_prompt_layer("output_format")

instruction = f"{persona}\n\n{business_rules}\n\n{safety_guardrails}\n\n{output_format}"

agent = Agent(
    name="scada_vpn_access_helpdesk_bot",
    model="gemini-3.7-flash",
    description="Automates authentication troubleshooting, MFA token verification, and role-based access approval for authorized engineers accessing SCADA networks.",
    instruction=instruction,
    tools=[BigQueryQueryTool(), VisualizerTool()],
    **callbacks
)

task_lead_agent = agent
root_agent = agent
