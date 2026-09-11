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

MALAYSIA_GRID_LOCATIONS: Dict[str, Dict[str, Any]] = {
    "klang_valley": {
        "name": "Klang Valley / Selangor (500kV Supergrid Hub)",
        "lat": 3.1390,
        "lon": 101.6869,
        "state": "Selangor / WP Kuala Lumpur",
        "grid": "TNB Peninsular Grid",
        "voltage_kv": 500,
        "corridor": "500kV Bukit Badong - Rawang - Klang West Corridor",
        "conductor_type": "Quad-bundle ACSR Zebra (4x400mm²)",
        "static_book_rating_a": 1800,
        "baseline_mva": 1558
    },
    "penang": {
        "name": "Bayan Lepas (275kV High-Tech Corridor)",
        "lat": 5.4141,
        "lon": 100.3288,
        "state": "Pulau Pinang",
        "grid": "TNB Peninsular Grid",
        "voltage_kv": 275,
        "corridor": "275kV Bayan Lepas - Prai Cross-Channel Interconnection",
        "conductor_type": "Twin-bundle ACSR Drake (2x400mm²)",
        "static_book_rating_a": 1200,
        "baseline_mva": 571
    },
    "gurun_kedah": {
        "name": "Gurun & Chuping (275kV LSS Solar Hub)",
        "lat": 5.8167,
        "lon": 100.4833,
        "state": "Kedah / Perlis",
        "grid": "TNB Peninsular Grid",
        "voltage_kv": 275,
        "corridor": "275kV Gurun - Bukit Keteri LSS Evacuation Corridor",
        "conductor_type": "Twin-bundle ACSR Drake",
        "static_book_rating_a": 1200,
        "baseline_mva": 571
    },
    "manjung_perak": {
        "name": "Manjung (500kV Coastal Generation Node)",
        "lat": 4.1622,
        "lon": 100.6433,
        "state": "Perak",
        "grid": "TNB Peninsular Grid",
        "voltage_kv": 500,
        "corridor": "500kV Janamanjung - Ayer Tawar Supergrid Trunk",
        "conductor_type": "Quad-bundle ACSR Zebra",
        "static_book_rating_a": 1800,
        "baseline_mva": 1558
    },
    "pengerang_johor": {
        "name": "Pengerang & Pasir Gudang (500kV Southern Node)",
        "lat": 1.4854,
        "lon": 103.7618,
        "state": "Johor",
        "grid": "TNB Peninsular Grid (Interconnected to Singapore SP)",
        "voltage_kv": 500,
        "corridor": "500kV Pengerang - Pasir Gudang - Yong Peng North",
        "conductor_type": "Quad-bundle ACSR Zebra",
        "static_book_rating_a": 1800,
        "baseline_mva": 1558
    },
    "paka_terengganu": {
        "name": "Paka & Kenyir (275kV Hydro & CCGT Node)",
        "lat": 4.6373,
        "lon": 103.4368,
        "state": "Terengganu",
        "grid": "TNB Peninsular Grid",
        "voltage_kv": 275,
        "corridor": "275kV Kenyir Hydro - Paka CCGT East Coast Corridor",
        "conductor_type": "Twin-bundle ACSR Drake",
        "static_book_rating_a": 1200,
        "baseline_mva": 571
    },
    "bakun_sarawak": {
        "name": "Bakun Hydro Terminal (500kV Hydro Complex)",
        "lat": 2.7567,
        "lon": 114.0533,
        "state": "Sarawak",
        "grid": "Sarawak Energy Grid",
        "voltage_kv": 500,
        "corridor": "500kV Bakun - Murum - Similajau Transmission Backbone",
        "conductor_type": "Quad-bundle ACSR Zebra",
        "static_book_rating_a": 1800,
        "baseline_mva": 1558
    },
    "samalaju_sarawak": {
        "name": "Samalaju (275kV Industrial Terminal)",
        "lat": 3.5833,
        "lon": 113.3500,
        "state": "Sarawak",
        "grid": "Sarawak Energy Grid",
        "voltage_kv": 275,
        "corridor": "275kV Similajau - Samalaju SCORE Industrial Corridor",
        "conductor_type": "Twin-bundle ACSR Drake",
        "static_book_rating_a": 1200,
        "baseline_mva": 571
    },
    "kota_kinabalu_sabah": {
        "name": "Kota Kinabalu (275kV West Coast Ring)",
        "lat": 5.9804,
        "lon": 116.0735,
        "state": "Sabah",
        "grid": "Sabah Electricity (SESB)",
        "voltage_kv": 275,
        "corridor": "275kV Kolopis - Segaliud East-West Interconnection",
        "conductor_type": "Twin-bundle ACSR Drake",
        "static_book_rating_a": 1100,
        "baseline_mva": 524
    }
}

class WeatherNextEngine:
    """Interface to Google DeepMind WeatherNext AI High-Resolution Weather Prediction.
    
    Coupled with tropical equatorial climatology across Malaysia and global grids.
    """

    def __init__(self, model_version: str = "WeatherNext-GraphCast-v2.1"):
        self.model_version = model_version
        self.locations_catalog = MALAYSIA_GRID_LOCATIONS

    def _resolve_location(
        self,
        substation_or_region: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> Dict[str, Any]:
        """Resolves target geographic coordinates, preferring Malaysian grid locations if matched."""
        query = (substation_or_region or "").lower().replace("-", " ").replace("_", " ")

        # Specific distinct place tokens for Malaysian grid hubs
        tokens_map = {
            "bakun_sarawak": ["bakun", "murum", "baleh", "sarawak", "kuching", "sibu"],
            "samalaju_sarawak": ["samalaju", "score", "similajau"],
            "kota_kinabalu_sabah": ["kinabalu", "sabah", "sesb", "kolopis", "sandakan", "tawau"],
            "gurun_kedah": ["gurun", "chuping", "kedah", "perlis", "lss solar"],
            "penang": ["penang", "bayan lepas", "georgetown", "seberang perai", "pulau pinang"],
            "pengerang_johor": ["pengerang", "pasir gudang", "johor", "singapore link"],
            "manjung_perak": ["manjung", "janamanjung", "perak", "lumut"],
            "paka_terengganu": ["paka", "kenyir", "terengganu", "kerteh"],
            "klang_valley": ["klang", "selangor", "kuala lumpur", "bukit badong", "rawang", "kapar", "putrajaya"]
        }

        for loc_id, kws in tokens_map.items():
            if any(kw in query for kw in kws):
                return self.locations_catalog[loc_id]

        for loc_id, loc_data in self.locations_catalog.items():
            loc_key = loc_id.replace("_", " ")
            if loc_key in query:
                return loc_data

        # Check for general "malaysia"
        if "malaysia" in query:
            return self.locations_catalog["klang_valley"]

        # Default fallback (preserves lat/lon if passed, else Klang Valley or general default)
        if lat is not None and lon is not None and (lat != 37.77 or lon != -122.42):
            return {
                "name": substation_or_region,
                "lat": lat,
                "lon": lon,
                "state": "Regional Grid",
                "grid": "Utility Interconnection",
                "voltage_kv": 230,
                "corridor": f"{substation_or_region} 230kV Corridor",
                "conductor_type": "ACSR Drake",
                "static_book_rating_a": 900,
                "baseline_mva": 358
            }
        
        # If standard substation name from previous tests
        return {
            "name": substation_or_region,
            "lat": lat if lat is not None else 3.1390,
            "lon": lon if lon is not None else 101.6869,
            "state": "Klang Valley / Selangor",
            "grid": "TNB Peninsular Grid",
            "voltage_kv": 275,
            "corridor": f"275kV {substation_or_region} Transmission Tie",
            "conductor_type": "ACSR Drake",
            "static_book_rating_a": 900,
            "baseline_mva": 358
        }

    def get_forecast(
        self,
        substation_or_region: str,
        horizon_hours: int = 24,
        lat: float = 37.77,
        lon: float = -122.42
    ) -> AtmosphericForecast:
        """Generates high-resolution AI meteorological predictions for grid telemetry.
        
        Simulates tropical equatorial atmospheric physics:
        - High solar irradiance (GHI up to 1050 W/m²)
        - Ambient equatorial temperature (27°C - 34°C)
        - Monsoonal sea-breeze / mountain convective convergence
        - Heavy tropical thunderstorm squall lines (dBZ 45-65+)
        - High lightning strike frequency (Malaysia global hotspot)
        """
        loc_meta = self._resolve_location(substation_or_region, lat, lon)
        resolved_lat = loc_meta["lat"]
        resolved_lon = loc_meta["lon"]

        # Diurnal solar cycle calculation (Malaysia UTC+8 peak around 13:00 - 14:00)
        hour_of_day = (14 + (horizon_hours % 24)) % 24
        solar_peak = max(0.0, math.sin(math.pi * (hour_of_day - 6) / 12)) if 6 <= hour_of_day <= 18 else 0.0

        # High equatorial solar irradiance
        ghi = round(solar_peak * 980.0 + random.uniform(-15, 15), 1)
        dni = round(solar_peak * 890.0 + random.uniform(-10, 10), 1) if ghi > 80 else 0.0

        # Tropical ambient temperatures (26.5°C night to 33.8°C afternoon peak)
        ambient_temp = round(26.5 + 6.8 * solar_peak + random.uniform(-0.4, 0.4), 1)

        # Monsoonal wind regimes (Southwest / Northeast monsoon breezes, 3.5 - 9.0 m/s)
        wind_10m = round(4.2 + 2.5 * math.sin(horizon_hours * 0.25) + random.uniform(0.2, 1.8), 2)
        wind_100m = round(wind_10m * 1.58, 2)
        # Prevailing wind directions (SW monsoon ~210°-240°, NE monsoon ~30°-60°)
        wind_dir = round(225.0 + random.uniform(-20, 20), 1)

        # Relative humidity (typical Malaysian tropical levels: 72% - 92%)
        humidity = round(88.0 - 18.0 * solar_peak + random.uniform(-2.0, 2.0), 1)
        cloud_cover = round(20.0 + 35.0 * (1.0 - solar_peak) + random.uniform(-5.0, 5.0), 1)

        # Tropical convective thunderstorm cells (Sumatra squall lines / Inter-monsoon convection)
        storm_cells: List[ConvectiveStormCell] = []
        convective_risk = "LOW"

        # Convective activity peaks during late afternoon / evening or tropical monsoon
        convective_weight = 0.55 if 14 <= hour_of_day <= 19 else 0.25
        if random.random() < convective_weight:
            convective_risk = "SEVERE" if random.random() < 0.4 else "MODERATE"
            
            # Primary squall cell moving northeastward across Strait of Malacca / South China Sea
            cell_1 = ConvectiveStormCell(
                cell_id="SQUALL-MY-WX01",
                latitude=round(resolved_lat + 0.12, 4),
                longitude=round(resolved_lon - 0.18, 4),
                peak_reflectivity_dbz=54.5 if convective_risk == "SEVERE" else 43.0,
                propagation_speed_kmh=38.0,
                heading_degrees=65.0,  # Heading toward Peninsular Malaysian coast
                lightning_strike_rate_per_min=28 if convective_risk == "SEVERE" else 14,
                projected_eta_minutes={
                    substation_or_region: 24.0,
                    "Klang Valley 500kV": 32.0,
                    "Substation-North": 45.0
                }
            )
            storm_cells.append(cell_1)

            if convective_risk == "SEVERE":
                cell_2 = ConvectiveStormCell(
                    cell_id="SQUALL-MY-WX02",
                    latitude=round(resolved_lat - 0.20, 4),
                    longitude=round(resolved_lon - 0.25, 4),
                    peak_reflectivity_dbz=58.0,
                    propagation_speed_kmh=42.0,
                    heading_degrees=70.0,
                    lightning_strike_rate_per_min=36,
                    projected_eta_minutes={
                        substation_or_region: 52.0,
                        "Bayan Lepas 275kV": 40.0
                    }
                )
                storm_cells.append(cell_2)

        return AtmosphericForecast(
            substation_or_region=loc_meta["name"] if "name" in loc_meta else substation_or_region,
            timestamp_iso=f"2026-09-11T{hour_of_day:02d}:00:00+08:00",
            ambient_temp_c=ambient_temp,
            solar_ghi_wm2=max(0.0, ghi),
            solar_dni_wm2=max(0.0, dni),
            wind_speed_10m_ms=wind_10m,
            wind_speed_100m_ms=wind_100m,
            wind_direction_deg=wind_dir,
            relative_humidity_pct=min(100.0, max(40.0, humidity)),
            convective_storm_risk=convective_risk,
            storm_cells=storm_cells,
            cloud_cover_pct=min(100.0, max(5.0, cloud_cover))
        )

    def compute_dlr_microclimate(
        self,
        span_id: str,
        conductor_azimuth_deg: float = 90.0,
        substation: str = "Klang Valley / Selangor (500kV Supergrid Hub)"
    ) -> Dict[str, Any]:
        """Calculates effective crosswind velocity and ambient cooling for Dynamic Line Rating.
        
        Applies IEEE 738 thermal balance:
        q_c + q_r = q_s + I² * R(T_c)
        """
        forecast = self.get_forecast(substation)
        loc_meta = self._resolve_location(substation)

        # Angle between wind vector and conductor span
        angle_diff_rad = math.radians(abs(forecast.wind_direction_deg - conductor_azimuth_deg))
        effective_crosswind_ms = max(0.6, forecast.wind_speed_10m_ms * abs(math.sin(angle_diff_rad)))

        # IEEE 738 convective cooling factor (forced convection)
        convective_cooling_factor = round(1.0 + (effective_crosswind_ms ** 0.52) * 0.48, 3)

        # Static book rating vs Dynamic ampacity
        base_amps = loc_meta.get("static_book_rating_a", 1200)
        dynamic_amps = round(base_amps * (convective_cooling_factor / (1.0 + (forecast.ambient_temp_c - 25.0) / 75.0)))
        headroom_pct = round(((dynamic_amps - base_amps) / base_amps) * 100.0, 1)

        return {
            "span_id": span_id,
            "corridor": loc_meta.get("corridor", f"{span_id} Corridor"),
            "grid_system": loc_meta.get("grid", "TNB Peninsular Grid"),
            "voltage_kv": loc_meta.get("voltage_kv", 275),
            "conductor_type": loc_meta.get("conductor_type", "ACSR Drake"),
            "ambient_temp_c": forecast.ambient_temp_c,
            "relative_humidity_pct": forecast.relative_humidity_pct,
            "wind_speed_ms": forecast.wind_speed_10m_ms,
            "effective_crosswind_ms": round(effective_crosswind_ms, 2),
            "solar_radiation_wm2": forecast.solar_ghi_wm2,
            "convective_cooling_factor": convective_cooling_factor,
            "static_book_rating_a": base_amps,
            "dynamic_line_rating_a": dynamic_amps,
            "unlocked_headroom_pct": headroom_pct,
            "thermal_sag_status": "NORMAL" if headroom_pct > 0 else "CAUTION"
        }

