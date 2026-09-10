"""Collaborative Workflow: Predictive Maintenance (PdM) Health Assessment & Field Dispatch."""
from typing import Dict, Any
from grid_optimization.personas.asset_reliability import AssetReliabilityPersona
from grid_optimization.personas.field_operations_tech import FieldOperationsTechPersona
from grid_optimization.personas.grid_dispatcher import GridDispatcherPersona

class PredictiveMaintenanceWorkflow:
    def __init__(self):
        self.asset_eng = AssetReliabilityPersona()
        self.field_tech = FieldOperationsTechPersona()
        self.dispatcher = GridDispatcherPersona()

    def run(self, asset_id: str = "XFMR-SUB-44", asset_type: str = "TRANSFORMER", substation: str = "Sub-North") -> Dict[str, Any]:
        # Step 1: Asset Reliability evaluates DGA and breaker degradation
        pdm_out = self.asset_eng.execute_task("RUN_PREDICTIVE_MAINTENANCE_ASSESSMENT", {
            "asset_id": asset_id,
            "asset_type": asset_type,
            "substation": substation,
            "ch4_ppm": 92.0,
            "c2h4_ppm": 164.0,
            "c2h2_ppm": 3.1
        })
        # Step 2: Field tech queues work order with safety LOTO check
        field_out = self.field_tech.execute_task("EXECUTE_PDM_FIELD_WORK", {
            "asset_id": asset_id,
            "substation": substation
        })

        sched = pdm_out["results"]["scheduler"]["asset_dossier"]

        return {
            "workflow_name": "Predictive Maintenance (PdM) Health Assessment & Field Intervention",
            "asset_id": asset_id,
            "asset_type": asset_type,
            "substation": substation,
            "health_index_ahi": sched["health_index"],
            "failure_probability_1yr_pct": sched["failure_probability_1yr_pct"],
            "remaining_useful_life_days": sched["remaining_useful_life_days"],
            "risk_priority_number": sched["risk_priority_number"],
            "work_order_priority": sched["work_order_priority"],
            "field_loto_verified": field_out["results"]["safety_loto"]["loto_verified"],
            "status": "FIELD_WORK_ORDER_DISPATCHED"
        }
