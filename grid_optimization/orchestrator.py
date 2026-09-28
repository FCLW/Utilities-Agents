import inspect
from typing import Dict, List, Any, Optional
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway, ApprovalStatus
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.advanced_engines import (
    WeatherNextEngine,
    VizierOptimizer,
    PredictiveMaintenanceEngine
)
from grid_optimization.skills import (
    WeatherNextTelemetryCorrelatorSkill,
    VizierBayesianVvoTunerSkill,
    TopologicalFlisrReconfiguratorSkill,
    PredictiveMaintenanceHealthScorerSkill,
    PowerFlowSimulationSkill,
    ContingencyConstraintCheckerSkill,
    HostingCapacityEvaluatorSkill,
    DynamicLineRatingCalculatorSkill,
    AutomatedSwitchingPlannerSkill,
    DerVppCoOptimizerSkill,
    ScadaAmiAnomalyDetectorSkill,
    RegulatoryAuditReporterSkill
)
from grid_optimization.personas import (
    GridDispatcherPersona,
    PlanningEngineerPersona,
    DermsManagerPersona,
    ProtectionControlPersona,
    AssetReliabilityPersona,
    GridAnalyticsDataScientistPersona,
    FieldOperationsTechPersona,
    RegulatoryComplianceOfficerPersona
)
from grid_optimization.workflows import (
    DynamicVvoWorkflow,
    HostingCapacityWorkflow,
    DynamicLineRatingWorkflow,
    FlisrRestorationWorkflow,
    PredictiveMaintenanceWorkflow,
    VppMarketDispatchWorkflow
)

class GridOptimizationOrchestrator:
    """Central Orchestrator coordinating cross-domain grid optimization workflows."""

    def __init__(self):
        self.harness = ValidationHarness()
        self.hitl = HITLGateway()
        # Multi-Dataset BigQuery Tool
        # The Master Orchestrator operates under least-privilege Agent Identity (zero direct BQ access)
        # and delegates analytical queries to domain persona agents.
        self.bq = MultiDatasetBigQueryTool(persona_id="grid_optimization_orchestrator")

        # Aliases for ADK tool consistency
        self.validation_harness = self.harness
        self.hitl_gateway = self.hitl
        self.multi_dataset_tool = self.bq

        # Advanced Technology Engines
        self.weathernext = WeatherNextEngine()
        self.vizier = VizierOptimizer()
        self.pdm = PredictiveMaintenanceEngine()

        # 12 Abstracted Reusable Skills
        self.skills = {
            "skill_weathernext_telemetry_correlator": WeatherNextTelemetryCorrelatorSkill(self.weathernext),
            "skill_vizier_bayesian_vvo_tuner": VizierBayesianVvoTunerSkill(self.vizier),
            "skill_topological_flisr_reconfigurator": TopologicalFlisrReconfiguratorSkill(),
            "skill_predictive_maintenance_health_scorer": PredictiveMaintenanceHealthScorerSkill(self.pdm),
            "skill_power_flow_simulation": PowerFlowSimulationSkill(),
            "skill_contingency_constraint_checker": ContingencyConstraintCheckerSkill(),
            "skill_hosting_capacity_evaluator": HostingCapacityEvaluatorSkill(),
            "skill_dynamic_line_rating_calculator": DynamicLineRatingCalculatorSkill(),
            "skill_automated_switching_planner": AutomatedSwitchingPlannerSkill(),
            "skill_der_vpp_co_optimizer": DerVppCoOptimizerSkill(),
            "skill_scada_ami_anomaly_detector": ScadaAmiAnomalyDetectorSkill(),
            "skill_regulatory_audit_reporter": RegulatoryAuditReporterSkill(),
        }

        # 8 Core Personas - each provisioned with persona-scoped Agent Identity
        self.personas = {
            "grid_dispatcher_agent": GridDispatcherPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="grid_dispatcher_agent")),
            "planning_engineer_agent": PlanningEngineerPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="planning_engineer_agent")),
            "derms_manager_agent": DermsManagerPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="derms_manager_agent")),
            "protection_control_agent": ProtectionControlPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="protection_control_agent")),
            "asset_reliability_agent": AssetReliabilityPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="asset_reliability_agent")),
            "grid_analytics_data_scientist_agent": GridAnalyticsDataScientistPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="grid_analytics_data_scientist_agent")),
            "field_operations_tech_agent": FieldOperationsTechPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="field_operations_tech_agent")),
            "regulatory_compliance_officer_agent": RegulatoryComplianceOfficerPersona(self.harness, self.hitl, MultiDatasetBigQueryTool(persona_id="regulatory_compliance_officer_agent")),
        }

        # 6 Collaborative Workflows
        self.workflows = {
            "dynamic_vvo": DynamicVvoWorkflow(self.harness, self.hitl),
            "hosting_capacity": HostingCapacityWorkflow(),
            "dynamic_line_rating": DynamicLineRatingWorkflow(),
            "flisr_restoration": FlisrRestorationWorkflow(self.hitl),
            "predictive_maintenance": PredictiveMaintenanceWorkflow(),
            "vpp_market_dispatch": VppMarketDispatchWorkflow(),
        }

    def run_workflow(self, workflow_name: str, **kwargs) -> Dict[str, Any]:
        """Executes a collaborative workflow across operational horizons."""
        if workflow_name not in self.workflows:
            raise ValueError(f"Workflow '{workflow_name}' not found. Available: {list(self.workflows.keys())}")
        wf = self.workflows[workflow_name]
        sig = inspect.signature(wf.run)
        valid_kwargs = {}
        for p_name, param in sig.parameters.items():
            if param.kind == inspect.Parameter.VAR_KEYWORD:
                valid_kwargs = kwargs
                break
            if p_name in kwargs:
                valid_kwargs[p_name] = kwargs[p_name]
            elif p_name == "faulted_feeder" and ("feeder_id" in kwargs or "circuit_id" in kwargs):
                valid_kwargs[p_name] = kwargs.get("feeder_id") or kwargs.get("circuit_id")
            elif p_name == "corridor_id" and ("feeder_id" in kwargs or "corridor_id" in kwargs):
                valid_kwargs[p_name] = kwargs.get("corridor_id") or kwargs.get("feeder_id")
            elif p_name == "asset_id" and ("feeder_id" in kwargs or "asset_id" in kwargs):
                valid_kwargs[p_name] = kwargs.get("asset_id") or kwargs.get("feeder_id")
            elif p_name == "vpp_id" and ("feeder_id" in kwargs or "vpp_id" in kwargs):
                valid_kwargs[p_name] = kwargs.get("vpp_id") or kwargs.get("feeder_id")
            elif p_name == "substation" and "substation_id" in kwargs:
                valid_kwargs[p_name] = kwargs["substation_id"]

        return wf.run(**valid_kwargs)

    def execute_workflow(self, workflow_name: str, payload: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes a workflow with dictionary payload."""
        payload = payload or {}
        return self.run_workflow(workflow_name, **payload)

    def dispatch_persona(self, persona_id: str, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches a task directly to a persona agent."""
        if persona_id not in self.personas:
            raise ValueError(f"Persona '{persona_id}' not found. Available: {list(self.personas.keys())}")
        return self.personas[persona_id].execute_task(task_type, payload)

    def dispatch_persona_task(self, persona_id: str, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Alias for dispatch_persona."""
        return self.dispatch_persona(persona_id, task_type, payload)

    def review_hitl_ticket(
        self,
        ticket_id: str,
        approve: bool,
        operator_id: str,
        role: str = "Lead Control Room Operator",
        notes: str = "Verified safe voltage and clearance parameters."
    ) -> Dict[str, Any]:
        """Applies human-in-the-loop sign-off or rejection to a grid action ticket."""
        if approve:
            ticket = self.hitl.approve_ticket(ticket_id, operator_id, role, notes)
            return {"status": "SUCCESS", "message": f"Ticket {ticket_id} approved. Command released to SCADA.", "ticket": ticket.__dict__}
        else:
            ticket = self.hitl.reject_ticket(ticket_id, operator_id, notes)
            return {"status": "SUCCESS", "message": f"Ticket {ticket_id} rejected. Safe state preserved.", "ticket": ticket.__dict__}

    def get_fleet_summary(self) -> Dict[str, Any]:
        """Returns overview of personas, sub-agents, skills, and pending HITL tickets."""
        total_sub_agents = sum(len(p.sub_agents) for p in self.personas.values())
        return {
            "fleet_name": "Utilities Grid Optimization Multi-Agent System",
            "persona_count": len(self.personas),
            "personas_count": len(self.personas),
            "sub_agent_count": total_sub_agents,
            "sub_agents_count": total_sub_agents,
            "skill_count": len(self.skills),
            "skills_count": len(self.skills),
            "workflow_count": len(self.workflows),
            "workflows_count": len(self.workflows),
            "personas": list(self.personas.keys()),
            "workflows": list(self.workflows.keys()),
            "skills": list(self.skills.keys()),
            "pending_hitl_tickets": len(self.hitl.get_pending_tickets()),
            "advanced_engines": ["Google DeepMind WeatherNext", "Vertex AI Vizier", "Predictive Maintenance (PdM)"],
            "operational_horizons": [
                "Real-Time Operations (Seconds to Hours)",
                "Intraday to Day-Ahead",
                "Medium to Long-Term Planning & Asset Management",
                "Periodic Governance & Regulatory Audit"
            ]
        }

    def get_system_fleet_summary(self) -> Dict[str, Any]:
        """Backward-compatible alias for get_fleet_summary."""
        return self.get_fleet_summary()
