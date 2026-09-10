"""Persona 5: Asset Performance & Reliability Engineer - PdM Lead."""
from typing import Dict, Any
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.asset_sub_agents import (
    TransformerDgaPdmSubAgent,
    CircuitBreakerTimingWearSubAgent,
    DynamicLineRatingSolverSubAgent,
    SubstationBatteryHealthSubAgent,
    PredictiveMaintenanceSchedulerSubAgent,
    AssetStrategyCopilotSubAgent
)

class AssetReliabilityPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "asset_reliability_agent"
        self.name = "Asset Performance & Reliability Engineer (PdM Lead)"
        self.horizon = "Medium to Long-Term (Predictive Maintenance)"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "dga_pdm": TransformerDgaPdmSubAgent(),
            "breaker_wear": CircuitBreakerTimingWearSubAgent(),
            "dlr_solver": DynamicLineRatingSolverSubAgent(),
            "battery_health": SubstationBatteryHealthSubAgent(),
            "pdm_scheduler": PredictiveMaintenanceSchedulerSubAgent(),
            "copilot": AssetStrategyCopilotSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sub_results = {}
        if task_type == "RUN_PREDICTIVE_MAINTENANCE_ASSESSMENT":
            sub_results["dga"] = self.sub_agents["dga_pdm"].execute(payload).data
            sub_results["breaker"] = self.sub_agents["breaker_wear"].execute(payload).data
            sub_results["battery"] = self.sub_agents["battery_health"].execute(payload).data
            sub_results["scheduler"] = self.sub_agents["pdm_scheduler"].execute(payload).data
            sub_results["strategy"] = self.sub_agents["copilot"].execute(payload).data
            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "results": sub_results,
                "status": "COMPLETED"
            }
        elif task_type == "SOLVE_DYNAMIC_LINE_RATING":
            sub_results["dlr"] = self.sub_agents["dlr_solver"].execute(payload).data
            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "results": sub_results,
                "status": "COMPLETED"
            }
        return {"persona": self.persona_id, "error": f"Unknown task type {task_type}"}
