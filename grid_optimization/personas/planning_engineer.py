"""Persona 2: Transmission & Distribution (T&D) Planning Engineer."""
from typing import Dict, Any
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.planning_sub_agents import (
    ContingencySimulatorSubAgent,
    HostingCapacityEngineSubAgent,
    AlphaEvolveFeederReconfiguratorSubAgent,
    LoadGrowthForecasterSubAgent,
    NonWiresAlternativesEvaluatorSubAgent,
    InterconnectionStudyCopilotSubAgent
)

class PlanningEngineerPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "planning_engineer_agent"
        self.name = "T&D System Planning Engineer"
        self.horizon = "Near-Term to Long-Term (Months to Years)"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "contingency": ContingencySimulatorSubAgent(),
            "hosting_capacity": HostingCapacityEngineSubAgent(),
            "alphaevolve_feeder": AlphaEvolveFeederReconfiguratorSubAgent(),
            "load_growth": LoadGrowthForecasterSubAgent(),
            "nwa_evaluator": NonWiresAlternativesEvaluatorSubAgent(),
            "interconnection": InterconnectionStudyCopilotSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sub_results = {}
        if task_type == "HOSTING_CAPACITY_STUDY":
            sub_results["hosting"] = self.sub_agents["hosting_capacity"].execute(payload).data
            sub_results["contingency"] = self.sub_agents["contingency"].execute(payload).data
            sub_results["study_copilot"] = self.sub_agents["interconnection"].execute(payload).data
            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "results": sub_results,
                "status": "COMPLETED"
            }
        elif task_type == "SEASONAL_TOPOLOGY_OPTIMIZATION":
            sub_results["evolved_topology"] = self.sub_agents["alphaevolve_feeder"].execute(payload).data
            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "results": sub_results,
                "status": "COMPLETED"
            }
        return {"persona": self.persona_id, "error": f"Unknown task type {task_type}"}
