"""Persona 3: DER & Flexibility Program Manager."""
from typing import Dict, Any
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.derms_sub_agents import (
    VppFleetAggregatorSubAgent,
    VizierBessArbitrageurSubAgent,
    WeatherNextDerPredictorSubAgent,
    DemandResponseDispatcherSubAgent,
    SmartInverterCurveManagerSubAgent,
    FlexibilityProgramCopilotSubAgent
)

class DermsManagerPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "derms_manager_agent"
        self.name = "DER & Flexibility Program Manager"
        self.horizon = "Intraday to Day-Ahead"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "vpp_aggregator": VppFleetAggregatorSubAgent(),
            "vizier_bess": VizierBessArbitrageurSubAgent(),
            "weathernext_der": WeatherNextDerPredictorSubAgent(),
            "dr_dispatcher": DemandResponseDispatcherSubAgent(),
            "inverter_curves": SmartInverterCurveManagerSubAgent(),
            "copilot": FlexibilityProgramCopilotSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sub_results = {}
        sub_results["vpp"] = self.sub_agents["vpp_aggregator"].execute(payload).data
        sub_results["weather"] = self.sub_agents["weathernext_der"].execute(payload).data
        sub_results["vizier_bess"] = self.sub_agents["vizier_bess"].execute(payload).data
        sub_results["dr"] = self.sub_agents["dr_dispatcher"].execute(payload).data

        ticket = self.hitl.evaluate_and_ticket(
            requesting_agent=self.persona_id,
            target_substation=payload.get("substation", "Sub-Metro"),
            target_feeder=payload.get("feeder_id", "F-BESS-01"),
            target_equipment="BESS-METRO-01",
            action_type="BESS_SCHEDULE_SHIFT",
            proposed_command="DISPATCH BESS 25 MW DISCHARGE 16:00-19:00",
            safety_dossier={"optimal_profit": sub_results["vizier_bess"].get("daily_net_profit_usd")}
        )
        return {
            "persona": self.persona_id,
            "task_type": task_type,
            "approval_ticket": ticket.__dict__,
            "results": sub_results,
            "status": "AWAITING_ADVISORY_APPROVAL"
        }
