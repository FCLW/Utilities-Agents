"""Collaborative Workflow: Dynamic Volt-VAR Optimization with Vertex AI Vizier."""
from typing import Dict, Any
from grid_optimization.personas.grid_dispatcher import GridDispatcherPersona
from grid_optimization.personas.protection_control import ProtectionControlPersona
from grid_optimization.personas.grid_analytics_data_scientist import GridAnalyticsDataScientistPersona
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway

class DynamicVvoWorkflow:
    """Coordinates Dispatcher (Owner), P&C Engineer, and Data Scientist for VVO."""

    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None):
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.dispatcher = GridDispatcherPersona(self.harness, self.hitl)
        self.pc = ProtectionControlPersona(self.harness, self.hitl)
        self.data_scientist = GridAnalyticsDataScientistPersona(self.harness, self.hitl)

    def run(self, feeder_id: str = "F-401", substation: str = "Sub-Metro") -> Dict[str, Any]:
        # Step 1: Data Scientist ingests WeatherNext and predicts 15-min loading
        ds_out = self.data_scientist.execute_task("INGEST_WEATHERNEXT_AND_FORECAST", {"region": substation})
        # Step 2: Protection Engineer verifies bidirectional settings
        pc_out = self.pc.execute_task("ADAPTIVE_RELAY_STUDY", {"relay_id": f"RELAY-{feeder_id}"})
        # Step 3: Dispatcher runs Vizier Volt-VAR optimization
        disp_out = self.dispatcher.execute_task("MONITOR_AND_DISPATCH", {
            "feeder_id": feeder_id,
            "substation": substation,
            "voltage_pu": 0.985,
            "frequency_hz": 60.0
        })

        return {
            "workflow_name": "Dynamic Volt-VAR Optimization (VVO) with Vizier",
            "feeder_id": feeder_id,
            "substation": substation,
            "data_scientist_phase": ds_out["results"]["weather"],
            "protection_phase": pc_out["results"]["fault"],
            "dispatcher_vvo_phase": disp_out["results"]["vvo"],
            "operator_briefing": disp_out["results"]["briefing"]["briefing_memo"],
            "status": "VVO_OPTIMIZATION_SUCCESSFUL"
        }
