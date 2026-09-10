"""Collaborative Workflow: Dynamic Line Rating (DLR) with WeatherNext."""
from typing import Dict, Any
from grid_optimization.personas.asset_reliability import AssetReliabilityPersona
from grid_optimization.personas.grid_dispatcher import GridDispatcherPersona
from grid_optimization.personas.grid_analytics_data_scientist import GridAnalyticsDataScientistPersona

class DynamicLineRatingWorkflow:
    def __init__(self):
        self.asset_engineer = AssetReliabilityPersona()
        self.dispatcher = GridDispatcherPersona()
        self.data_scientist = GridAnalyticsDataScientistPersona()

    def run(self, corridor_id: str = "LINE-NORTH-230") -> Dict[str, Any]:
        dlr_out = self.asset_engineer.execute_task("SOLVE_DYNAMIC_LINE_RATING", {"line_id": corridor_id})
        return {
            "workflow_name": "Dynamic Line Rating (DLR) Deployment with WeatherNext",
            "corridor_id": corridor_id,
            "ampacity_gain_pct": dlr_out["results"]["dlr"]["ampacity_gain_pct"],
            "crosswind_cooling_ms": dlr_out["results"]["dlr"]["effective_crosswind_ms"],
            "status": "CONGESTION_RELIEVED"
        }
