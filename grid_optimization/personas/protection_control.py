"""Persona 4: Protection & Control (P&C) Engineer."""
from typing import Dict, Any
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.protection_sub_agents import (
    RelayCoordinationEngineSubAgent,
    AdaptiveProtectionDiscoverySubAgent,
    BidirectionalFaultAnalyzerSubAgent,
    AntiIslandingValidatorSubAgent,
    OscillographyFaultDiagnosticSubAgent,
    RelaySettingCopilotSubAgent
)

class ProtectionControlPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "protection_control_agent"
        self.name = "Protection & Control (P&C) Engineer"
        self.horizon = "Lifecycle & Event Analysis"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "coordination": RelayCoordinationEngineSubAgent(),
            "adaptive_protection": AdaptiveProtectionDiscoverySubAgent(),
            "fault_analyzer": BidirectionalFaultAnalyzerSubAgent(),
            "anti_islanding": AntiIslandingValidatorSubAgent(),
            "oscillography": OscillographyFaultDiagnosticSubAgent(),
            "copilot": RelaySettingCopilotSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sub_results = {}
        if task_type == "ADAPTIVE_RELAY_STUDY":
            sub_results["fault"] = self.sub_agents["fault_analyzer"].execute(payload).data
            sub_results["adaptive_protection"] = self.sub_agents["adaptive_protection"].execute(payload).data
            sub_results["anti_islanding"] = self.sub_agents["anti_islanding"].execute(payload).data
            sub_results["copilot"] = self.sub_agents["copilot"].execute(payload).data
            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "results": sub_results,
                "status": "COMPLETED"
            }
        return {"persona": self.persona_id, "error": f"Unknown task type {task_type}"}
