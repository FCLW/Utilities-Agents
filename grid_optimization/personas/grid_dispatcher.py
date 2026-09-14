"""Persona 1: Grid Operations Dispatcher / Real-Time Operator."""
from typing import Dict, List, Any, Optional
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.dispatcher_sub_agents import (
    ScadaTelemetryMonitorSubAgent,
    WeatherNextStormTrackerSubAgent,
    StateEstimationEngineSubAgent,
    VoltVarDispatchOptimizerSubAgent,
    TopologicalSwitchingCoordinatorSubAgent,
    ContingencyScreenerSubAgent,
    DispatcherCopilotReasonerSubAgent
)

class GridDispatcherPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "grid_dispatcher_agent"
        self.name = "Grid Operations Dispatcher / Real-Time Operator"
        self.horizon = "Real-Time (Seconds to Hours)"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "scada_monitor": ScadaTelemetryMonitorSubAgent(),
            "weathernext_storm": WeatherNextStormTrackerSubAgent(),
            "state_estimation": StateEstimationEngineSubAgent(),
            "vvo_optimizer": VoltVarDispatchOptimizerSubAgent(),
            "topological_switching": TopologicalSwitchingCoordinatorSubAgent(),
            "contingency_screener": ContingencyScreenerSubAgent(),
            "copilot": DispatcherCopilotReasonerSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        val = self.harness.validate_input_telemetry(payload)
        sub_results = {}
        task_norm = (task_type or "").upper().strip()

        if task_norm in ("TRIGGER_FLISR_SWITCHING", "FLISR", "SWITCHING", "FLISR_RESTORATION"):
            sub_results["switching"] = self.sub_agents["topological_switching"].execute(payload).data
            ticket = self.hitl.evaluate_and_ticket(
                requesting_agent=self.persona_id,
                target_substation=payload.get("substation", "Sub-Metro"),
                target_feeder=payload.get("feeder_id", "F-102"),
                target_equipment="TIE_SWITCH_SW-TIE-44",
                action_type="FLISR_RESTORATION",
                proposed_command="CLOSE SW-TIE-44 AND OPEN SW-SEC-23",
                safety_dossier={"validation": val.__dict__, "loss_reduction_pct": sub_results["switching"].get("loss_reduction_pct")}
            )
            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "approval_ticket": ticket.__dict__,
                "results": sub_results,
                "status": "AWAITING_OPERATOR_APPROVAL"
            }
        else:
            sub_results["scada"] = self.sub_agents["scada_monitor"].execute(payload).data
            sub_results["weather"] = self.sub_agents["weathernext_storm"].execute(payload).data
            sub_results["state_est"] = self.sub_agents["state_estimation"].execute(payload).data
            sub_results["vvo"] = self.sub_agents["vvo_optimizer"].execute(payload).data
            copilot_out = self.sub_agents["copilot"].execute(payload).data
            sub_results["briefing"] = copilot_out

            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "validation": val.__dict__,
                "results": sub_results,
                "status": "COMPLETED"
            }
