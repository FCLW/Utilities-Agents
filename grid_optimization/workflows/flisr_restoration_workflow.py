"""Collaborative Workflow: FLISR Restoration with Topological Optimization & Mandatory HITL."""
from typing import Dict, Any
from grid_optimization.personas.grid_dispatcher import GridDispatcherPersona
from grid_optimization.personas.field_operations_tech import FieldOperationsTechPersona
from grid_optimization.personas.protection_control import ProtectionControlPersona
from grid_optimization.safety.hitl_gateway import HITLGateway

class FlisrRestorationWorkflow:
    def __init__(self, hitl: HITLGateway = None):
        self.hitl = hitl or HITLGateway()
        self.dispatcher = GridDispatcherPersona(hitl=self.hitl)
        self.field_tech = FieldOperationsTechPersona(hitl=self.hitl)
        self.protection = ProtectionControlPersona(hitl=self.hitl)

    def run(self, faulted_feeder: str = "F-102", substation: str = "Sub-Metro") -> Dict[str, Any]:
        # Step 1: Dispatcher initiates FLISR via Topological Reconfiguration
        disp_out = self.dispatcher.execute_task("TRIGGER_FLISR_SWITCHING", {
            "feeder_id": faulted_feeder,
            "substation": substation,
            "voltage_pu": 0.94, # Sag caused by fault
            "frequency_hz": 59.94
        })

        ticket = disp_out["approval_ticket"]
        return {
            "workflow_name": "Automated FLISR Restoration with Topological Reconfiguration",
            "faulted_feeder": faulted_feeder,
            "substation": substation,
            "requires_hitl_approval": True,
            "hitl_ticket_id": ticket["ticket_id"],
            "proposed_switching_order": ticket["proposed_command"],
            "risk_tier": ticket["risk_tier"],
            "status": "PAUSED_AWAITING_OPERATOR_SIGNOFF"
        }
