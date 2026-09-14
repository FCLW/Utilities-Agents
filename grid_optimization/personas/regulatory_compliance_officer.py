"""Persona 8: Regulatory, Market & Compliance Officer."""
from typing import Dict, Any
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.regulatory_sub_agents import (
    NercPrcFacComplianceAuditorSubAgent,
    Ieee1366ReliabilityCalculatorSubAgent,
    CleanEnergyRpsTrackerSubAgent,
    WholesaleSettlementReconcilerSubAgent,
    RegulatoryFilingCopilotSubAgent
)

class RegulatoryComplianceOfficerPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "regulatory_compliance_officer_agent"
        self.name = "Regulatory, Market & Compliance Officer"
        self.horizon = "Periodic / Audit Cycles"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "nerc_auditor": NercPrcFacComplianceAuditorSubAgent(),
            "reliability_calc": Ieee1366ReliabilityCalculatorSubAgent(),
            "rps_tracker": CleanEnergyRpsTrackerSubAgent(),
            "settlement_reconciler": WholesaleSettlementReconcilerSubAgent(),
            "copilot": RegulatoryFilingCopilotSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sub_results = {}
        sub_results["nerc"] = self.sub_agents["nerc_auditor"].execute(payload).data
        sub_results["reliability"] = self.sub_agents["reliability_calc"].execute(payload).data
        sub_results["rps"] = self.sub_agents["rps_tracker"].execute(payload).data
        sub_results["settlement"] = self.sub_agents["settlement_reconciler"].execute(payload).data
        sub_results["copilot"] = self.sub_agents["copilot"].execute(payload).data
        return {
            "persona": self.persona_id,
            "task_type": task_type,
            "results": sub_results,
            "status": "COMPLETED"
        }
