"""Persona 7: Field Operations & Substation Technician."""
from typing import Dict, Any
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.field_sub_agents import (
    PdmWorkOrderReceiverSubAgent,
    SwitchingOrderSafetyVerifierSubAgent,
    FieldTelemetryCalibratorSubAgent,
    SmartInverterFirmwareAuditorSubAgent,
    MobileWorkforceDispatcherSubAgent,
    FieldTechnicianCopilotSubAgent
)

class FieldOperationsTechPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "field_operations_tech_agent"
        self.name = "Field Operations & Substation Technician"
        self.horizon = "Real-Time / Scheduled Field Execution"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "pdm_receiver": PdmWorkOrderReceiverSubAgent(),
            "switching_verifier": SwitchingOrderSafetyVerifierSubAgent(),
            "calibrator": FieldTelemetryCalibratorSubAgent(),
            "inverter_auditor": SmartInverterFirmwareAuditorSubAgent(),
            "workforce_dispatcher": MobileWorkforceDispatcherSubAgent(),
            "copilot": FieldTechnicianCopilotSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sub_results = {}
        if task_type == "EXECUTE_PDM_FIELD_WORK":
            sub_results["work_order"] = self.sub_agents["pdm_receiver"].execute(payload).data
            sub_results["safety_loto"] = self.sub_agents["switching_verifier"].execute(payload).data
            sub_results["copilot"] = self.sub_agents["copilot"].execute(payload).data
            return {
                "persona": self.persona_id,
                "task_type": task_type,
                "results": sub_results,
                "status": "COMPLETED"
            }
        return {"persona": self.persona_id, "error": f"Unknown task type {task_type}"}
