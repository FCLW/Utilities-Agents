"""Skill: IEEE 738 Dynamic Line Rating (DLR) Ampacity Calculator."""
from typing import Dict, Any
from grid_optimization.advanced_engines.weathernext_engine import WeatherNextEngine

class DynamicLineRatingCalculatorSkill:
    """Reusable skill: Calculates real-time dynamic ampacity using WeatherNext microclimate."""

    def __init__(self, weather_engine: WeatherNextEngine = None):
        self.weather_engine = weather_engine or WeatherNextEngine()

    def execute(self, line_id: str, static_rating_amps: float = 650.0) -> Dict[str, Any]:
        microclimate = self.weather_engine.compute_dlr_microclimate(span_id=line_id)
        # IEEE 738 thermal balance approximation: Ampacity ~ sqrt(Cooling / Resistance)
        cooling_factor = microclimate["convective_cooling_factor"]
        # Ambient temperature derating factor
        temp_factor = max(0.85, 1.0 - (microclimate["ambient_temp_c"] - 25.0) * 0.005)

        dynamic_amps = round(static_rating_amps * cooling_factor * temp_factor, 1)
        capacity_gain_pct = round(((dynamic_amps - static_rating_amps) / static_rating_amps) * 100.0, 1)

        return {
            "skill": "skill_dynamic_line_rating_calculator",
            "line_id": line_id,
            "static_rating_amps": static_rating_amps,
            "dynamic_rating_amps": dynamic_amps,
            "capacity_gain_pct": capacity_gain_pct,
            "microclimate": microclimate,
            "operational_status": "CONGESTION_UNLOCKED" if capacity_gain_pct > 15.0 else "NOMINAL_GAIN"
        }
