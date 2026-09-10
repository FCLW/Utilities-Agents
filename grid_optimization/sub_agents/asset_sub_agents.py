"""Sub-agents for Asset Performance & Reliability Engineer - PdM Lead Persona."""
from typing import Dict, Any
from .base import BaseSubAgent, AgentType, SubAgentOutput
from grid_optimization.advanced_engines.pdm_engine import PredictiveMaintenanceEngine
from grid_optimization.advanced_engines.weathernext_engine import WeatherNextEngine

class TransformerDgaPdmSubAgent(BaseSubAgent):
    def __init__(self, pdm_engine: PredictiveMaintenanceEngine = None):
        super().__init__(
            "sub_transformer_dga_pdm",
            "Transformer DGA PdM Analyzer",
            AgentType.PREDICTIVE_ML,
            "Evaluates Duval Triangle 1, Rogers Ratios, and moisture-in-oil degradation trends."
        )
        self.pdm_engine = pdm_engine or PredictiveMaintenanceEngine()

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        xfmr_id = inputs.get("transformer_id", "XFMR-SUB-44")
        diag = self.pdm_engine.diagnose_transformer_dga(
            xfmr_id,
            ch4_ppm=inputs.get("ch4_ppm", 92.0),
            c2h4_ppm=inputs.get("c2h4_ppm", 164.0),
            c2h2_ppm=inputs.get("c2h2_ppm", 3.1)
        )
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"dga_diagnosis": diag.__dict__},
            f"Duval Triangle diagnosed {diag.fault_classification} (Severity: {diag.severity_level}). {diag.recommended_action}"
        )

class CircuitBreakerTimingWearSubAgent(BaseSubAgent):
    def __init__(self, pdm_engine: PredictiveMaintenanceEngine = None):
        super().__init__(
            "sub_circuit_breaker_timing_wear",
            "Circuit Breaker Wear & Timing Analyzer",
            AgentType.EVENT_DRIVEN_REFLEX,
            "Tracks cumulative interrupted fault energy (sum I2t) and SF6 gas density decay."
        )
        self.pdm_engine = pdm_engine or PredictiveMaintenanceEngine()

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        cb_id = inputs.get("breaker_id", "CB-230-01")
        wear = self.pdm_engine.evaluate_circuit_breaker_wear(cb_id, cumulative_fault_mva_interrupted=inputs.get("cumulative_fault_mva", 14200.0))
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"breaker_metrics": wear.__dict__},
            f"Breaker {cb_id} arcing wear at {wear.cumulative_i2t_wear_pct}%, health index: {wear.health_index_pct}%."
        )

class DynamicLineRatingSolverSubAgent(BaseSubAgent):
    def __init__(self, wx_engine: WeatherNextEngine = None):
        super().__init__(
            "sub_dynamic_line_rating_solver",
            "Dynamic Line Rating (DLR) Solver",
            AgentType.DETERMINISTIC_PHYSICS,
            "Ingests WeatherNext local wind velocity and ambient temp for IEEE 738 dynamic ampacity ratings."
        )
        self.wx_engine = wx_engine or WeatherNextEngine()

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        line_id = inputs.get("line_id", "LINE-NORTH-230")
        dlr = self.wx_engine.compute_dlr_microclimate(line_id)
        cooling = dlr["convective_cooling_factor"]
        dynamic_gain_pct = round((cooling - 1.0) * 100.0 * 0.7, 1)
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"line_id": line_id, "effective_crosswind_ms": dlr["effective_crosswind_ms"], "ampacity_gain_pct": dynamic_gain_pct},
            f"WeatherNext crosswind ({dlr['effective_crosswind_ms']} m/s) delivers +{dynamic_gain_pct}% dynamic line capacity headroom."
        )

class SubstationBatteryHealthSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_substation_battery_health",
            "Substation Battery Health Tracker",
            AgentType.PREDICTIVE_ML,
            "Models internal cell resistance (mOhm) and battery remaining useful life (RUL)."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"battery_bank_id": "BATT-SUB-04", "internal_resistance_mohm": 1.42, "float_voltage_v": 134.8, "rul_days": 820},
            "Substation DC 125V battery bank health nominal (1.42 mOhm internal impedance, 820 days RUL)."
        )

class PredictiveMaintenanceSchedulerSubAgent(BaseSubAgent):
    def __init__(self, pdm_engine: PredictiveMaintenanceEngine = None):
        super().__init__(
            "sub_pdm_scheduler",
            "PdM Risk-Ranked Scheduler",
            AgentType.OPTIMIZATION_ENGINE,
            "Ranks equipment by Risk Priority Number (RPN) and generates preventative work orders."
        )
        self.pdm_engine = pdm_engine or PredictiveMaintenanceEngine()

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        dossier = self.pdm_engine.build_asset_health_dossier(
            asset_id=inputs.get("asset_id", "XFMR-SUB-44"),
            asset_type=inputs.get("asset_type", "TRANSFORMER"),
            substation=inputs.get("substation", "Sub-North"),
            diagnostic_payload={"ch4_ppm": 92.0, "c2h4_ppm": 164.0, "c2h2_ppm": 3.1}
        )
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"asset_dossier": dossier.__dict__},
            f"Risk Prioritization: Asset {dossier.asset_id} ranked RPN={dossier.risk_priority_number}. Work Order: {dossier.work_order_priority}."
        )

class AssetStrategyCopilotSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_asset_strategy_copilot",
            "Asset Strategy Copilot",
            AgentType.COGNITIVE_LLM,
            "Synthesizes multi-sensor PdM health indices into capital replacement justification memos."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"strategy_memo": "Asset replacement prioritization memo drafted for FY2027 Capital Budget."},
            "Asset replacement prioritization memo drafted for FY2027 Capital Budget."
        )
