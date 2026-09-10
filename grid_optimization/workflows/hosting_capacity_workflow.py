"""Collaborative Workflow: DER Hosting Capacity with WeatherNext."""
from typing import Dict, Any
from grid_optimization.personas.planning_engineer import PlanningEngineerPersona
from grid_optimization.personas.derms_manager import DermsManagerPersona
from grid_optimization.personas.grid_analytics_data_scientist import GridAnalyticsDataScientistPersona

class HostingCapacityWorkflow:
    def __init__(self):
        self.planner = PlanningEngineerPersona()
        self.derms = DermsManagerPersona()
        self.data_scientist = GridAnalyticsDataScientistPersona()

    def run(self, feeder_id: str = "F-NORTH-08", substation: str = "Sub-North") -> Dict[str, Any]:
        # Step 1: Ingest solar forecasting from WeatherNext
        wx = self.data_scientist.execute_task("INGEST_WEATHERNEXT_AND_FORECAST", {"region": substation})
        # Step 2: Evaluate hosting capacity and contingency limits
        plan = self.planner.execute_task("HOSTING_CAPACITY_STUDY", {"feeder_id": feeder_id, "substation": substation})

        return {
            "workflow_name": "DER Hosting Capacity Analysis with WeatherNext",
            "feeder_id": feeder_id,
            "substation": substation,
            "solar_dni_wm2": wx["results"]["weather"]["ghi"],
            "hosting_capacity_mw": plan["results"]["hosting"]["pv_hosting_capacity_mw"],
            "limiting_factor": plan["results"]["hosting"]["limiting_criterion"],
            "study_summary": plan["results"]["study_copilot"]["study_text"],
            "status": "STUDY_COMPLETED"
        }
