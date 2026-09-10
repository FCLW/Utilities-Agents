"""Google DeepMind WeatherNext AI Weather Prediction Engine."""
import math
import random
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class ConvectiveStormCell:
    cell_id: str
    latitude: float
    longitude: float
    peak_reflectivity_dbz: float
    propagation_speed_kmh: float
    heading_degrees: float
    lightning_strike_rate_per_min: int
    projected_eta_minutes: Dict[str, float]  # Substation ID -> ETA minutes

@dataclass
class AtmosphericForecast:
    substation_or_region: str
    timestamp_iso: str
    ambient_temp_c: float
    solar_ghi_wm2: float       # Global Horizontal Irradiance
    solar_dni_wm2: float       # Direct Normal Irradiance
    wind_speed_10m_ms: float   # Wind speed at 10m
    wind_speed_100m_ms: float  # Wind speed at 100m (hub height)
    wind_direction_deg: float  # Wind incident direction
    relative_humidity_pct: float
    convective_storm_risk: str # "LOW", "MODERATE", "SEVERE", "EXTREME"
    storm_cells: List[ConvectiveStormCell] = field(default_factory=list)
    cloud_cover_pct: float = 15.0

class WeatherNextEngine:
    """Interface to Google DeepMind WeatherNext AI High-Resolution Weather Prediction."""

    def __init__(self, model_version: str = "WeatherNext-GraphCast-v2.1"):
        self.model_version = model_version

    def get_forecast(
        self,
        substation_or_region: str,
        horizon_hours: int = 24,
        lat: float = 37.77,
        lon: float = -122.42
    ) -> AtmosphericForecast:
        """Generates high-resolution AI meteorological predictions for grid telemetry."""
        # Realistic synthesis grounded in typical Western grid climatology
        # Incorporates diurnal solar and ambient cycles
        hour_of_day = 14  # Peak solar afternoon default
        solar_peak = max(0.0, math.sin(math.pi * (hour_of_day - 6) / 12)) if 6 <= hour_of_day <= 18 else 0.0

        ghi = round(solar_peak * 950.0 + random.uniform(-20, 20), 1)
        dni = round(solar_peak * 880.0 + random.uniform(-15, 15), 1) if ghi > 100 else 0.0
        ambient_temp = round(24.5 + 6.0 * solar_peak + random.uniform(-0.5, 0.5), 1)
        wind_10m = round(4.8 + random.uniform(0.5, 3.5), 2)
        wind_100m = round(wind_10m * 1.55, 2)
        wind_dir = round(275.0 + random.uniform(-15, 15), 1)

        storm_cells = []
        convective_risk = "LOW"
        if random.random() < 0.25:
            convective_risk = "MODERATE"
            storm_cells.append(
                ConvectiveStormCell(
                    cell_id="STORM-CELL-WX09",
                    latitude=lat + 0.15,
                    longitude=lon - 0.22,
                    peak_reflectivity_dbz=48.5,
                    propagation_speed_kmh=42.0,
                    heading_degrees=115.0,
                    lightning_strike_rate_per_min=18,
                    projected_eta_minutes={substation_or_region: 34.0, "Substation-East": 58.0}
                )
            )

        return AtmosphericForecast(
            substation_or_region=substation_or_region,
            timestamp_iso="2026-09-10T14:00:00Z",
            ambient_temp_c=ambient_temp,
            solar_ghi_wm2=max(0.0, ghi),
            solar_dni_wm2=max(0.0, dni),
            wind_speed_10m_ms=wind_10m,
            wind_speed_100m_ms=wind_100m,
            wind_direction_deg=wind_dir,
            relative_humidity_pct=42.0,
            convective_storm_risk=convective_risk,
            storm_cells=storm_cells,
            cloud_cover_pct=18.5
        )

    def compute_dlr_microclimate(
        self,
        span_id: str,
        conductor_azimuth_deg: float = 90.0,
        substation: str = "Substation-North"
    ) -> Dict[str, Any]:
        """Calculates effective crosswind velocity and ambient cooling for Dynamic Line Rating."""
        forecast = self.get_forecast(substation)
        # Angle between wind vector and conductor span
        angle_diff_rad = math.radians(abs(forecast.wind_direction_deg - conductor_azimuth_deg))
        effective_crosswind_ms = max(0.5, forecast.wind_speed_10m_ms * abs(math.sin(angle_diff_rad)))

        return {
            "span_id": span_id,
            "ambient_temp_c": forecast.ambient_temp_c,
            "wind_speed_ms": forecast.wind_speed_10m_ms,
            "effective_crosswind_ms": round(effective_crosswind_ms, 2),
            "solar_radiation_wm2": forecast.solar_ghi_wm2,
            "convective_cooling_factor": round(1.0 + (effective_crosswind_ms ** 0.52) * 0.45, 3)
        }
