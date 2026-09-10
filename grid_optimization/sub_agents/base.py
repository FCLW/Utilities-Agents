"""Base abstractions for heterogeneous grid sub-agents."""
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

class AgentType(str, Enum):
    COGNITIVE_LLM = "COGNITIVE_LLM"                  # Gemini reasoning, explanation, NLP synthesis
    DETERMINISTIC_PHYSICS = "DETERMINISTIC_PHYSICS"  # Exact numerical power flow, impedance matrices
    PREDICTIVE_ML = "PREDICTIVE_ML"                  # WeatherNext, LSTM load forecast, anomaly detection
    RULE_BASED_EXPERT = "RULE_BASED_EXPERT"          # Interlocking rules, NERC standards, safety tagouts
    EVENT_DRIVEN_REFLEX = "EVENT_DRIVEN_REFLEX"      # Low-latency SCADA alarm threshold triggers
    OPTIMIZATION_ENGINE = "OPTIMIZATION_ENGINE"      # Vizier Bayesian tuning, AlphaEvolve genetic search

@dataclass
class SubAgentOutput:
    sub_agent_id: str
    agent_type: AgentType
    status: str
    data: Dict[str, Any]
    reasoning_summary: str
    execution_time_ms: float = 25.0

class BaseSubAgent:
    """Base class for all heterogeneous sub-agents across operational horizons."""

    def __init__(self, sub_agent_id: str, name: str, agent_type: AgentType, role_description: str):
        self.sub_agent_id = sub_agent_id
        self.name = name
        self.agent_type = agent_type
        self.role_description = role_description

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        raise NotImplementedError("Sub-agents must implement execute()")

    def get_metadata(self) -> Dict[str, Any]:
        return {
            "sub_agent_id": self.sub_agent_id,
            "name": self.name,
            "agent_type": self.agent_type.value,
            "role_description": self.role_description
        }
