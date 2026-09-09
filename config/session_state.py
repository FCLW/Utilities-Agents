from typing import Optional, Any, Literal
from pydantic import BaseModel, Field
from pydantic.fields import FieldInfo

class UtilitiesSessionState(BaseModel):
    """Enterprise session state schema propagated across Utilities Agents."""
    customer_id: Optional[str] = Field(default=None, description="Active utility customer identifier.")
    grid_zone_id: Optional[str] = Field(default="ZONE-DEFAULT", description="Electrical grid zone or substation identifier.")
    operating_mode: Literal["Normal", "Degraded", "Emergency", "BlackStart"] = Field(
        default="Normal", description="Operational grid condition."
    )
    active_alert_level: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"] = Field(
        default="LOW", description="Current utility threat/alert severity level."
    )
    session_id: Optional[str] = Field(default=None, description="Unique telemetry session ID.")

# Declare Model Armor runtime state keys so ADK session state validation allows them
UtilitiesSessionState.model_fields["_model_armor_screened_input"] = FieldInfo(annotation=Optional[Any], default=None)
UtilitiesSessionState.model_fields["_model_armor_screened_output"] = FieldInfo(annotation=Optional[Any], default=None)
