"""Skill: AlphaEvolve evolutionary network reconfiguration to minimize line losses."""
from typing import Dict, List, Any
from grid_optimization.advanced_engines.alphaevolve_engine import AlphaEvolveEngine

class AlphaEvolveReconfiguratorSkill:
    """Reusable skill: Evolutionary topology optimization discovered by AlphaEvolve."""

    def __init__(self, engine: AlphaEvolveEngine = None):
        self.engine = engine or AlphaEvolveEngine()

    def execute(self, substation_id: str, feeder_ids: List[str] = None, baseline_loss_mw: float = 3.85) -> Dict[str, Any]:
        feeders = feeder_ids or ["F-101", "F-102", "F-103"]
        switches = [f"SW-SEC-{i}" for i in range(10, 30)] + [f"SW-TIE-{i}" for i in [44, 89, 102]]
        res = self.engine.reconfigure_distribution_network(substation_id, feeders, switches, baseline_loss_mw)
        return {
            "skill": "skill_alphaevolve_reconfigurator",
            "substation_id": substation_id,
            "study_id": res.study_id,
            "baseline_loss_mw": res.baseline_loss_mw,
            "optimal_loss_mw": res.optimal_loss_mw,
            "loss_reduction_pct": res.loss_reduction_pct,
            "optimal_normally_open_switches": res.optimal_topology.normally_open_switches,
            "reconfiguration_switching_steps": res.reconfiguration_switching_steps,
            "generations_evolved": res.generations_evolved
        }
