"""Skill: Black-box Bayesian optimization of smart inverter Volt-VAR parameters."""
from typing import Dict, Any
from grid_optimization.advanced_engines.vizier_optimizer import VizierOptimizer

class VizierBayesianVvoTunerSkill:
    """Reusable skill: Vertex AI Vizier optimization for loss minimization and voltage flattening."""

    def __init__(self, optimizer: VizierOptimizer = None):
        self.optimizer = optimizer or VizierOptimizer()

    def execute(self, feeder_id: str, baseline_loss_mw: float = 2.45) -> Dict[str, Any]:
        res = self.optimizer.optimize_volt_var_curves(feeder_id=feeder_id, baseline_loss_mw=baseline_loss_mw)
        return {
            "skill": "skill_vizier_bayesian_vvo_tuner",
            "feeder_id": feeder_id,
            "study_id": res.study_id,
            "best_volt_var_curve": res.best_parameters,
            "baseline_loss_mw": baseline_loss_mw,
            "optimized_loss_mw": res.objective_value,
            "loss_reduction_pct": round((baseline_loss_mw - res.objective_value) / baseline_loss_mw * 100.0, 1),
            "iterations_run": res.iterations_run,
            "ansi_violations": res.constraint_violations
        }
