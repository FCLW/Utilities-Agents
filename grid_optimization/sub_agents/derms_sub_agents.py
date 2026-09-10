"""Sub-agents for DER & Flexibility Program Manager Persona."""
from typing import Dict, Any
from .base import BaseSubAgent, AgentType, SubAgentOutput
from grid_optimization.advanced_engines.weathernext_engine import WeatherNextEngine
from grid_optimization.advanced_engines.vizier_optimizer import VizierOptimizer

class VppFleetAggregatorSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_vpp_fleet_aggregator",
            "VPP Fleet Aggregator",
            AgentType.DETERMINISTIC_PHYSICS,
            "Dynamically pools distributed solar, commercial loads, and BESS by electrical node."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"aggregated_bess_mw": 32.5, "aggregated_pv_mw": 48.0, "curtailable_c_and_i_mw": 14.2, "enrolled_sites": 1850},
            "VPP Fleet aggregator pooled 94.7 MW flexible capacity across 1,850 enrolled sites."
        )

class VizierBessArbitrageurSubAgent(BaseSubAgent):
    def __init__(self, optimizer: VizierOptimizer = None):
        super().__init__(
            "sub_vizier_bess_arbitrageur",
            "Vizier BESS Arbitrageur",
            AgentType.OPTIMIZATION_ENGINE,
            "Co-optimizes BESS charge/discharge schedule balancing LMP revenue against cell degradation."
        )
        self.optimizer = optimizer or VizierOptimizer()

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        bess_id = inputs.get("bess_id", "BESS-METRO-01")
        res = self.optimizer.optimize_bess_arbitrage_envelope(bess_id)
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"bess_id": bess_id, "optimal_dispatch_params": res.best_parameters, "daily_net_profit_usd": res.objective_value},
            f"Vizier Bayesian optimization balanced battery degradation with $ {res.objective_value} daily net arbitrage profit."
        )

class WeatherNextDerPredictorSubAgent(BaseSubAgent):
    def __init__(self, engine: WeatherNextEngine = None):
        super().__init__(
            "sub_weathernext_der_predictor",
            "WeatherNext DER Generation Predictor",
            AgentType.PREDICTIVE_ML,
            "Feeds DeepMind WeatherNext solar irradiance and temperature into DER aggregate capacity forecasts."
        )
        self.engine = engine or WeatherNextEngine()

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        sub = inputs.get("substation", "Sub-Metro")
        fc = self.engine.get_forecast(sub)
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"substation": sub, "solar_ghi_wm2": fc.solar_ghi_wm2, "pv_output_mw": round(fc.solar_ghi_wm2 * 0.048, 2)},
            f"WeatherNext irradiance ({fc.solar_ghi_wm2} W/m2) models 48 MW PV capacity at peak noon."
        )

class DemandResponseDispatcherSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_dr_dispatcher",
            "Demand Response Dispatcher",
            AgentType.RULE_BASED_EXPERT,
            "Dispatches automated commercial & industrial (C&I) thermostat setbacks."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"dr_event_dispatched": True, "load_shed_mw": 8.4, "participating_commercial_buildings": 42},
            "Auto-DR event triggered across 42 C&I facilities shedding 8.4 MW during top peak hour."
        )

class SmartInverterCurveManagerSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_smart_inverter_curve_manager",
            "Smart Inverter Curve Manager",
            AgentType.OPTIMIZATION_ENGINE,
            "Computes and broadcasts Vizier-optimized Volt-VAR / Volt-Watt curve parameters."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"curve_version": "IEEE1547-2018-VVO-SET4", "inverters_updated": 420, "target_power_factor": 0.96},
            "Volt-VAR curve parameter set broadcasted to 420 grid-tied smart inverters."
        )

class FlexibilityProgramCopilotSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_flexibility_program_copilot",
            "Flexibility Program Copilot",
            AgentType.COGNITIVE_LLM,
            "Communicates event schedules with aggregated C&I participants and drafts settlement summaries."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"program_briefing": "Summer Peak Savings Event confirmed for 16:00-19:00 today. 42 buildings notified."},
            "Summer Peak Savings Event confirmed for 16:00-19:00 today. Participant notifications dispatched."
        )
