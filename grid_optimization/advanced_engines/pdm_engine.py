"""Predictive Maintenance (PdM) Engine for Power Grid Assets."""
import math
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

@dataclass
class DgaDiagnosis:
    transformer_id: str
    methane_ch4_ppm: float
    ethylene_c2h4_ppm: float
    acetylene_c2h2_ppm: float
    hydrogen_h2_ppm: float
    carbon_monoxide_co_ppm: float
    total_dissolved_gas_ppm: float
    duval_triangle_coords: Dict[str, float]  # %CH4, %C2H4, %C2H2
    fault_classification: str                # e.g., "T3: Severe Thermal Fault > 700C"
    severity_level: str                      # "NORMAL", "CAUTION", "ALARM", "CRITICAL"
    recommended_action: str

@dataclass
class BreakerWearMetric:
    breaker_id: str
    cumulative_i2t_wear_pct: float     # Percentage of rated fault interruption capability consumed
    operations_count: int
    sf6_pressure_bar: float            # Nominal ~6.0 bar
    mechanism_timing_deviation_ms: float
    predicted_contact_erosion_pct: float
    health_index_pct: float            # 100% = pristine, <40% = urgent overhaul

@dataclass
class AssetHealthDossier:
    asset_id: str
    asset_type: str                    # "TRANSFORMER", "CIRCUIT_BREAKER", "SUBSTATION_BATTERY"
    substation: str
    health_index: float                # 0 - 100 AHI
    failure_probability_1yr_pct: float
    remaining_useful_life_days: int
    risk_priority_number: int          # RPN: Probability * Criticality * Severity (1 - 1000)
    diagnostic_details: Dict[str, Any]
    work_order_required: bool
    work_order_priority: str           # "ROUTINE", "EXPEDITED", "EMERGENCY_INTERVENTION"

class PredictiveMaintenanceEngine:
    """Predictive Health Monitoring and Failure Prevention for Substation Assets."""

    def diagnose_transformer_dga(
        self,
        transformer_id: str,
        ch4_ppm: float,
        c2h4_ppm: float,
        c2h2_ppm: float,
        h2_ppm: float = 45.0,
        co_ppm: float = 280.0
    ) -> DgaDiagnosis:
        """Applies IEEE C57.104 and Duval Triangle 1 to classify transformer internal faults."""
        total_duval = max(0.1, ch4_ppm + c2h4_ppm + c2h2_ppm)
        pct_ch4 = round((ch4_ppm / total_duval) * 100.0, 1)
        pct_c2h4 = round((c2h4_ppm / total_duval) * 100.0, 1)
        pct_c2h2 = round((c2h2_ppm / total_duval) * 100.0, 1)

        # Duval Triangle 1 zoning logic
        if pct_c2h2 >= 13.0 and pct_c2h4 >= 23.0:
            fault = "D2: High Energy Arcing Discharge"
            severity = "CRITICAL"
            action = "Immediate de-energization and internal inspection; catastrophic flashover risk"
        elif pct_c2h2 >= 4.0 and pct_c2h4 < 23.0:
            fault = "D1: Low Energy Sparking / Partial Breakdown"
            severity = "ALARM"
            action = "Perform acoustic emission PD testing and increase gas sampling to 48h intervals"
        elif pct_c2h4 >= 50.0:
            fault = "T3: Thermal Fault > 700°C (Heavy Oil Carbonization)"
            severity = "ALARM"
            action = "Inspect load tap changer contactors and core grounding strap"
        elif pct_c2h4 >= 20.0 and pct_ch4 >= 50.0:
            fault = "T2: Thermal Fault 300°C - 700°C"
            severity = "CAUTION"
            action = "Thermal imaging scan on bushings and oil cooler radiator banks"
        elif pct_ch4 >= 98.0:
            fault = "PD: Partial Discharge"
            severity = "CAUTION"
            action = "Degas oil dielectric and check paper moisture content"
        else:
            fault = "Normal Aging (No Active Fault Zone)"
            severity = "NORMAL"
            action = "Continue standard quarterly gas chromatography"

        total_gas = ch4_ppm + c2h4_ppm + c2h2_ppm + h2_ppm + co_ppm

        return DgaDiagnosis(
            transformer_id=transformer_id,
            methane_ch4_ppm=ch4_ppm,
            ethylene_c2h4_ppm=c2h4_ppm,
            acetylene_c2h2_ppm=c2h2_ppm,
            hydrogen_h2_ppm=h2_ppm,
            carbon_monoxide_co_ppm=co_ppm,
            total_dissolved_gas_ppm=round(total_gas, 1),
            duval_triangle_coords={"pct_ch4": pct_ch4, "pct_c2h4": pct_c2h4, "pct_c2h2": pct_c2h2},
            fault_classification=fault,
            severity_level=severity,
            recommended_action=action
        )

    def evaluate_circuit_breaker_wear(
        self,
        breaker_id: str,
        cumulative_fault_mva_interrupted: float = 12500.0,
        rated_interrupting_mva: float = 25000.0,
        sf6_pressure_bar: float = 5.8,
        operations_count: int = 1420
    ) -> BreakerWearMetric:
        """Evaluates accumulated arcing contact wear and SF6 gas density."""
        wear_pct = round((cumulative_fault_mva_interrupted / rated_interrupting_mva) * 100.0, 1)
        sf6_nominal = 6.0
        sf6_health = max(0.0, min(100.0, (sf6_pressure_bar / sf6_nominal) * 100.0))

        # Health index composite: 60% contact wear, 25% SF6 gas, 15% operation count
        health_index = round(100.0 - (wear_pct * 0.60) - ((100.0 - sf6_health) * 0.25) - (min(3000, operations_count) / 3000.0 * 15.0), 1)

        return BreakerWearMetric(
            breaker_id=breaker_id,
            cumulative_i2t_wear_pct=wear_pct,
            operations_count=operations_count,
            sf6_pressure_bar=sf6_pressure_bar,
            mechanism_timing_deviation_ms=4.2,
            predicted_contact_erosion_pct=round(wear_pct * 0.85, 1),
            health_index_pct=max(0.0, health_index)
        )

    def build_asset_health_dossier(
        self,
        asset_id: str,
        asset_type: str,
        substation: str,
        diagnostic_payload: Dict[str, Any]
    ) -> AssetHealthDossier:
        """Generates comprehensive asset health, RUL, and RPN work orders."""
        if asset_type == "TRANSFORMER":
            dga = self.diagnose_transformer_dga(
                transformer_id=asset_id,
                ch4_ppm=diagnostic_payload.get("ch4_ppm", 85.0),
                c2h4_ppm=diagnostic_payload.get("c2h4_ppm", 145.0),
                c2h2_ppm=diagnostic_payload.get("c2h2_ppm", 2.5)
            )
            # RUL calculation based on Duval severity
            if dga.severity_level == "CRITICAL":
                ahi = 32.0
                rul_days = 28
                prob = 78.5
                priority = "EMERGENCY_INTERVENTION"
            elif dga.severity_level == "ALARM":
                ahi = 58.0
                rul_days = 180
                prob = 34.0
                priority = "EXPEDITED"
            else:
                ahi = 88.0
                rul_days = 1450
                prob = 4.2
                priority = "ROUTINE"

            rpn = int(round(prob * 0.1 * 8.5 * (100.0 - ahi) * 0.1))
            return AssetHealthDossier(
                asset_id=asset_id,
                asset_type=asset_type,
                substation=substation,
                health_index=ahi,
                failure_probability_1yr_pct=prob,
                remaining_useful_life_days=rul_days,
                risk_priority_number=min(1000, max(1, rpn)),
                diagnostic_details={"dga": dga.__dict__},
                work_order_required=(dga.severity_level in ["ALARM", "CRITICAL"]),
                work_order_priority=priority
            )
        else: # CIRCUIT_BREAKER
            cb = self.evaluate_circuit_breaker_wear(
                breaker_id=asset_id,
                cumulative_fault_mva_interrupted=diagnostic_payload.get("cumulative_fault_mva", 16800.0)
            )
            prob = round(100.0 - cb.health_index_pct, 1)
            rul_days = int(round(max(15, (cb.health_index_pct / 100.0) * 850)))
            priority = "EXPEDITED" if cb.health_index_pct < 50.0 else "ROUTINE"
            rpn = int(round(prob * 0.1 * 7.5 * 8.0))

            return AssetHealthDossier(
                asset_id=asset_id,
                asset_type=asset_type,
                substation=substation,
                health_index=cb.health_index_pct,
                failure_probability_1yr_pct=prob,
                remaining_useful_life_days=rul_days,
                risk_priority_number=min(1000, max(1, rpn)),
                diagnostic_details={"breaker_metrics": cb.__dict__},
                work_order_required=(cb.health_index_pct < 60.0),
                work_order_priority=priority
            )
