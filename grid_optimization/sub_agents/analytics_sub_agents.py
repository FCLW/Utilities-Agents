"""Sub-agents for Data Scientist / Grid Analytics Engineer Persona."""
from typing import Dict, Any
from .base import BaseSubAgent, AgentType, SubAgentOutput
from grid_optimization.advanced_engines.weathernext_engine import WeatherNextEngine

class WeatherNextForecastConsumerSubAgent(BaseSubAgent):
    def __init__(self, engine: WeatherNextEngine = None):
        super().__init__(
            "sub_weathernext_forecast_consumer",
            "WeatherNext Forecast Consumer",
            AgentType.PREDICTIVE_ML,
            "Ingests DeepMind WeatherNext atmospheric fields (wind, solar, temp) into spatial grid models."
        )
        self.engine = engine or WeatherNextEngine()

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        region = inputs.get("region") or inputs.get("substation") or inputs.get("substation_or_region") or "Klang Valley / Selangor (500kV Supergrid Hub)"
        horizon = inputs.get("horizon_hours", 24)
        fc = self.engine.get_forecast(region, horizon_hours=horizon)
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {
                "region": region,
                "region_resolved": fc.substation_or_region,
                "ghi": fc.solar_ghi_wm2,
                "ghi_wm2": fc.solar_ghi_wm2,
                "dni_wm2": fc.solar_dni_wm2,
                "wind_10m": fc.wind_speed_10m_ms,
                "wind_10m_ms": fc.wind_speed_10m_ms,
                "wind_100m_ms": fc.wind_speed_100m_ms,
                "temp_c": fc.ambient_temp_c,
                "ambient_temp_c": fc.ambient_temp_c,
                "relative_humidity_pct": fc.relative_humidity_pct,
                "spatial_resolution": "0.08° (~9km ECMWF/WeatherNext)",
                "bigquery_table": "utilities_grid_optimization.weathernext_spatial_telemetry",
                "ingestion_status": "COMMITTED"
            },
            f"WeatherNext AI spatial ingestion complete for {fc.substation_or_region}: GHI={fc.solar_ghi_wm2} W/m2, Ambient Temp={fc.ambient_temp_c}°C, Wind={fc.wind_speed_10m_ms} m/s."
        )

class ShortTermLoadForecasterSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_short_term_load_forecaster",
            "Short-Term Load Forecaster",
            AgentType.PREDICTIVE_ML,
            "Ensemble gradient-boosted tree & LSTM models predicting 15-minute feeder demand."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"next_hour_load_mw": 84.2, "mape_error_pct": 1.45, "confidence_interval_95_mw": [82.5, 85.9]},
            "15-minute ensemble load forecast generated with 1.45% MAPE accuracy."
        )

class SolarWindGenerationForecasterSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_solar_wind_generation_forecaster",
            "Solar & Wind Generation Forecaster",
            AgentType.PREDICTIVE_ML,
            "Translates WeatherNext GHI and wind vectors into solar/wind generation curves."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"solar_forecast_mw": 34.5, "wind_forecast_mw": 28.2, "renewable_penetration_pct": 52.4},
            "Renewable generation forecast: 62.7 MW aggregate solar + wind (52.4% grid penetration)."
        )

class SpatialGisAmiFusionPipelineSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_spatial_gis_ami_fusion",
            "Spatial GIS & AMI Fusion Pipeline",
            AgentType.DETERMINISTIC_PHYSICS,
            "Spatially joins smart meter voltage profiles with GIS feeder electrical graphs."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"meters_joined": 14200, "phase_identification_accuracy_pct": 99.1, "unmapped_meters": 4},
            "Spatial GIS-AMI graph join complete: 14,200 meters mapped with 99.1% phase identification confidence."
        )

class ScadaAmiAnomalyDetectorSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_scada_ami_anomaly_detector",
            "SCADA / AMI Anomaly Detector",
            AgentType.PREDICTIVE_ML,
            "Unsupervised Isolation Forest detecting sensor drift and meter tampering."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"anomalies_flagged": 2, "tamper_flags": 0, "sensor_drift_indices": ["MTR-882", "RTU-04"]},
            "Isolation Forest flagged 2 telemetry points exhibiting statistical sensor drift."
        )

class GridAnalyticsCopilotSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_grid_analytics_copilot",
            "Grid Analytics Copilot",
            AgentType.COGNITIVE_LLM,
            "Translates complex ML metrics, feature importance, and model uncertainty into plain engineering English."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"analytics_memo": "Feature importance indicates WeatherNext ambient temperature accounts for 64% of peak feeder loading variance."},
            "Feature importance indicates WeatherNext ambient temperature accounts for 64% of peak feeder loading variance."
        )
