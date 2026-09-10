"""Skill: Ingests and correlates Google DeepMind WeatherNext AI predictions to grid telemetry."""
from typing import Dict, Any
from grid_optimization.advanced_engines.weathernext_engine import WeatherNextEngine

class WeatherNextTelemetryCorrelatorSkill:
    """Reusable skill: spatializes WeatherNext AI forecasts to substation and feeder coordinates."""

    def __init__(self, engine: WeatherNextEngine = None):
        self.engine = engine or WeatherNextEngine()

    def execute(self, substation_id: str, horizon_hours: int = 24) -> Dict[str, Any]:
        forecast = self.engine.get_forecast(substation_or_region=substation_id, horizon_hours=horizon_hours)
        return {
            "skill": "skill_weathernext_telemetry_correlator",
            "substation_id": substation_id,
            "ambient_temp_c": forecast.ambient_temp_c,
            "solar_ghi_wm2": forecast.solar_ghi_wm2,
            "solar_dni_wm2": forecast.solar_dni_wm2,
            "wind_speed_10m_ms": forecast.wind_speed_10m_ms,
            "convective_storm_risk": forecast.convective_storm_risk,
            "storm_cells_detected": len(forecast.storm_cells),
            "cloud_cover_pct": forecast.cloud_cover_pct,
            "solar_generation_capacity_pct": round(min(100.0, (forecast.solar_ghi_wm2 / 1000.0) * 100.0), 1),
            "wind_generation_capacity_pct": round(min(100.0, (forecast.wind_speed_10m_ms / 12.0) ** 3 * 100.0), 1)
        }
