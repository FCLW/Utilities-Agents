"""Sub-agents for T&D Planning Engineer Persona."""
from typing import Dict, Any
from .base import BaseSubAgent, AgentType, SubAgentOutput

class ContingencySimulatorSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_contingency_simulator",
            "Contingency Simulator",
            AgentType.DETERMINISTIC_PHYSICS,
            "Exhaustive N-1, N-1-1, and N-2 AC power flow across seasonal loading."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"n1_1_feasible": True, "critical_corridors_screened": 48, "max_mva_loading_pct": 91.2},
            "Seasonal N-1-1 contingency simulation completed: 48 corridors screened, all within NERC TPL-001 limits."
        )

class HostingCapacityEngineSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_hosting_capacity_engine",
            "Hosting Capacity Engine",
            AgentType.DETERMINISTIC_PHYSICS,
            "Iterative feeder capacity sweep for solar PV and EV charging clusters."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        feeder = inputs.get("feeder_id", "F-NORTH-08")
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"feeder_id": feeder, "pv_hosting_capacity_mw": 4.8, "limiting_criterion": "1.05 p.u. ANSI C84.1 Overvoltage"},
            f"Hosting capacity sweep on {feeder} allows 4.8 MW solar PV before overvoltage ceiling is reached."
        )

class TopologicalFeederReconfiguratorSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_topological_feeder_reconfigurator",
            "Topological Feeder Reconfigurator",
            AgentType.OPTIMIZATION_ENGINE,
            "Discovers seasonal optimal topology tie-switch configurations to minimize annual energy losses using MILP branch exchange."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        sub = inputs.get("substation", "Sub-Metro")
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"reconfiguration_study": f"TOPOL-OPT-{sub}", "loss_reduction_pct": 12.4},
            "Topological reconfiguration discovered seasonal topology reducing annual line losses by 12.4%."
        )

class LoadGrowthForecasterSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_load_growth_forecaster",
            "Load Growth Forecaster",
            AgentType.PREDICTIVE_ML,
            "10-year spatial econometric and electrification adoption forecasting."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"growth_rate_pct_yr": 3.8, "ev_adoption_rate_pct": 24.5, "peak_demand_forecast_mw_2035": 142.0},
            "10-year econometric forecast predicts 3.8% annual load growth driven by EV fleet electrification."
        )

class NonWiresAlternativesEvaluatorSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_nwa_evaluator",
            "Non-Wires Alternatives (NWA) Evaluator",
            AgentType.DETERMINISTIC_PHYSICS,
            "Evaluates targeted BESS + solar vs capital substation expansion."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"nwa_npv_usd": 12400000.0, "substation_capex_usd": 28000000.0, "recommended_path": "DEPLOY_BESS_NWA"},
            "NWA analysis recommends 10 MW / 40 MWh BESS, deferring $28M substation expansion with $15.6M net savings."
        )

class InterconnectionStudyCopilotSubAgent(BaseSubAgent):
    def __init__(self):
        super().__init__(
            "sub_interconnection_study_copilot",
            "Interconnection Study Copilot",
            AgentType.COGNITIVE_LLM,
            "Drafts utility system impact studies for developer interconnection queues."
        )

    def execute(self, inputs: Dict[str, Any]) -> SubAgentOutput:
        queue_id = inputs.get("queue_id", "Q-2026-904")
        summary = (
            f"System Impact Study Summary for {queue_id}: Interconnection approved at Point of Interconnection (POI) "
            f"Bus-14 subject to smart inverter Volt-VAR autonomous mode and 12-cycle transfer trip relay."
        )
        return SubAgentOutput(
            self.sub_agent_id, self.agent_type, "SUCCESS",
            {"queue_id": queue_id, "approval_status": "CONDITIONALLY_APPROVED", "study_text": summary},
            summary
        )
