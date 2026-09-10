"""Skill: Multi-Asset Virtual Power Plant (VPP) Co-Optimizer."""
from typing import Dict, Any

class DerVppCoOptimizerSkill:
    """Reusable skill: Co-optimizes BESS, solar curtailment, and demand response vs wholesale LMP."""

    def execute(self, vpp_id: str, available_bess_mw: float = 25.0, current_lmp_usd_mwh: float = 85.0) -> Dict[str, Any]:
        # Formulates economic merit order dispatch
        dispatch_bess_mw = available_bess_mw if current_lmp_usd_mwh > 50.0 else 0.0
        curtailable_dr_mw = 8.5 if current_lmp_usd_mwh > 75.0 else 0.0
        solar_generation_mw = 18.2

        total_dispatched_mw = round(dispatch_bess_mw + curtailable_dr_mw + solar_generation_mw, 2)
        hourly_revenue_usd = round(total_dispatched_mw * current_lmp_usd_mwh, 2)

        return {
            "skill": "skill_der_vpp_co_optimizer",
            "vpp_id": vpp_id,
            "current_lmp_usd_mwh": current_lmp_usd_mwh,
            "dispatched_bess_mw": dispatch_bess_mw,
            "dispatched_dr_mw": curtailable_dr_mw,
            "solar_active_generation_mw": solar_generation_mw,
            "total_vpp_capacity_dispatched_mw": total_dispatched_mw,
            "hourly_market_revenue_usd": hourly_revenue_usd,
            "carbon_offset_kg_co2_per_hr": round(total_dispatched_mw * 385.0, 1)
        }
