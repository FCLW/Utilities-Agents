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

telemetry_callbacks = get_telemetry_callbacks(agent_name="appliance_disaggregation_efficiency_advisor")
callbacks = combine_agent_callbacks(armor_callbacks, telemetry_callbacks)


persona = load_prompt_layer("persona")
business_rules = load_prompt_layer("business_rules")
safety_guardrails = load_prompt_layer("safety_guardrails")
output_format = load_prompt_layer("output_format")

instruction = f"{persona}\n\n{business_rules}\n\n{safety_guardrails}\n\n{output_format}"

agent = Agent(
    name="appliance_disaggregation_efficiency_advisor",
    model="gemini-3.7-flash",
    description="Decomposes smart meter interval data into appliance-level consumption profiles (HVAC, water heating, refrigeration) to deliver personalized energy efficiency recommendations.",
    instruction=instruction,
    tools=[BigQueryQueryTool(), VisualizerTool()],
    **callbacks
)

task_lead_agent = agent
root_agent = agent

try:
    from .sub_agents.worker_agent import worker_agent
    from .sub_agents.critic_agent import critic_agent
except ImportError:
    try:
        from sub_agents.worker_agent import worker_agent
        from sub_agents.critic_agent import critic_agent
    except ImportError:
        worker_agent = None
        critic_agent = None

async def workflow_router(message: str, session_state: dict = None) -> str:
    """Executes the Worker -> Critic pipeline, sanitizing outputs into structured markdown."""
    import sys
    agent_mod = sys.modules.get(__name__)
    w = getattr(agent_mod, "worker_agent", worker_agent)
    c = getattr(agent_mod, "critic_agent", critic_agent)
    
    if callable(w):
        worker_resp = w(message)
    elif hasattr(w, "run") and type(w).__name__ != "Agent":
        worker_resp = w.run(message)
    else:
        worker_resp = f"Worker analysis for: {message}"
    if hasattr(worker_resp, "__await__"):
        worker_resp = await worker_resp
    content = worker_resp.content if hasattr(worker_resp, "content") else str(worker_resp)

    critic_prompt = f"Review and format this output into a Markdown table: {content}"
    if callable(c):
        critic_resp = c(critic_prompt)
    elif hasattr(c, "run") and type(c).__name__ != "Agent":
        critic_resp = c.run(critic_prompt)
    else:
        critic_resp = "| Metric | Status |\n|---|---|\n| Result | " + str(content) + " |"
    if hasattr(critic_resp, "__await__"):
        critic_resp = await critic_resp
    return critic_resp.content if hasattr(critic_resp, "content") else str(critic_resp)
