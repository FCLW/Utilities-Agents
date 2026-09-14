"""Persona 6: Data Scientist / Grid Analytics Engineer."""
from typing import Dict, Any
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.sub_agents.analytics_sub_agents import (
    WeatherNextForecastConsumerSubAgent,
    ShortTermLoadForecasterSubAgent,
    SolarWindGenerationForecasterSubAgent,
    SpatialGisAmiFusionPipelineSubAgent,
    ScadaAmiAnomalyDetectorSubAgent,
    GridAnalyticsCopilotSubAgent
)

class GridAnalyticsDataScientistPersona:
    def __init__(self, harness: ValidationHarness = None, hitl: HITLGateway = None, bq: MultiDatasetBigQueryTool = None):
        self.persona_id = "grid_analytics_data_scientist_agent"
        self.name = "Data Scientist / Grid Analytics Engineer"
        self.horizon = "Continuous / MLOps"
        self.harness = harness or ValidationHarness()
        self.hitl = hitl or HITLGateway()
        self.bq = bq or MultiDatasetBigQueryTool()

        self.sub_agents = {
            "weathernext_consumer": WeatherNextForecastConsumerSubAgent(),
            "load_forecaster": ShortTermLoadForecasterSubAgent(),
            "renewable_forecaster": SolarWindGenerationForecasterSubAgent(),
            "gis_ami_fusion": SpatialGisAmiFusionPipelineSubAgent(),
            "anomaly_detector": ScadaAmiAnomalyDetectorSubAgent(),
            "copilot": GridAnalyticsCopilotSubAgent()
        }

    def execute_task(self, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        sub_results = {}
        sub_results["weather"] = self.sub_agents["weathernext_consumer"].execute(payload).data
        sub_results["load"] = self.sub_agents["load_forecaster"].execute(payload).data
        sub_results["renewables"] = self.sub_agents["renewable_forecaster"].execute(payload).data
        sub_results["anomalies"] = self.sub_agents["anomaly_detector"].execute(payload).data
        sub_results["copilot"] = self.sub_agents["copilot"].execute(payload).data
        return {
            "persona": self.persona_id,
            "task_type": task_type,
            "results": sub_results,
            "status": "COMPLETED"
        }
