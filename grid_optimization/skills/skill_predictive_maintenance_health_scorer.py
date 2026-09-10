"""Skill: Predictive Maintenance Asset Health Index (AHI) and RUL scoring."""
from typing import Dict, Any
from grid_optimization.advanced_engines.pdm_engine import PredictiveMaintenanceEngine

class PredictiveMaintenanceHealthScorerSkill:
    """Reusable skill: Evaluates DGA, breaker wear, and schedules preventative work orders."""

    def __init__(self, engine: PredictiveMaintenanceEngine = None):
        self.engine = engine or PredictiveMaintenanceEngine()

    def execute(self, asset_id: str, asset_type: str, substation: str, diagnostic_payload: Dict[str, Any]) -> Dict[str, Any]:
        dossier = self.engine.build_asset_health_dossier(asset_id, asset_type, substation, diagnostic_payload)
        return {
            "skill": "skill_predictive_maintenance_health_scorer",
            "asset_id": dossier.asset_id,
            "asset_type": dossier.asset_type,
            "substation": dossier.substation,
            "health_index_ahi": dossier.health_index,
            "failure_probability_1yr_pct": dossier.failure_probability_1yr_pct,
            "remaining_useful_life_days": dossier.remaining_useful_life_days,
            "risk_priority_number": dossier.risk_priority_number,
            "work_order_required": dossier.work_order_required,
            "work_order_priority": dossier.work_order_priority,
            "diagnostic_details": dossier.diagnostic_details
        }
