import os
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", os.getenv("GCP_LOCATION", "global"))

from google.adk import Agent
from ..tools.delegation_tool import AgentDelegationTool
from ..app_utils.prompt_loader import load_prompt_layer
from pydantic import BaseModel
from typing import Optional

try:
    from config.settings import settings
except ImportError:
    class Settings:
        llm_model_name = os.getenv("LLM_MODEL_NAME", "gemini-3.7-flash")
    settings = Settings()

class UtilitiesSessionState(BaseModel):
    customer_id: Optional[str] = None
    grid_zone_id: Optional[str] = None
    operating_mode: str = "Normal"
    active_alert_level: str = "Low"

instruction = load_prompt_layer("execution_agent")

execution_agent = Agent(
    name="utilities_master_orchestrator_execution",
    model=getattr(settings, "llm_model_name", "gemini-3.7-flash"),
    instruction=instruction,
    tools=[AgentDelegationTool()]
)
