import os
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

from google.adk import Agent
from ..tools.delegation_tool import AgentDelegationTool
from pydantic import BaseModel
from typing import Optional

class UtilitiesSessionState(BaseModel):
    customer_id: Optional[str] = None
    grid_zone_id: Optional[str] = None
    operating_mode: str = "Normal"
    active_alert_level: str = "Low"

execution_agent = Agent(
    name="utilities_master_orchestrator_execution",
    model="gemini-3.7-flash",
    instruction="""You are the Master Orchestrator execution lead. 
Your primary role is to interpret the user's intent, identify the correct specialized domain agent for the task, 
and dispatch the request using the AgentDelegationTool. 
Always serialize the current UtilitiesSessionState into JSON when delegating.""",
    tools=[AgentDelegationTool()]
)
