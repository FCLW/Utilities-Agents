"""Master Grid Optimization Orchestrator coordinating all personas, workflows, engines, and HITL governance."""
from typing import Dict, List, Any, Optional
from grid_optimization.safety.validation_harness import ValidationHarness
from grid_optimization.safety.hitl_gateway import HITLGateway, ApprovalStatus
from grid_optimization.tools.multi_dataset_bq_tool import MultiDatasetBigQueryTool
from grid_optimization.advanced_engines import (
    WeatherNextEngine,
    VizierOptimizer,
    PredictiveMaintenanceEngine
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
        self.bq = MultiDatasetBigQueryTool()

        # Advanced Technology Engines
        self.weathernext = WeatherNextEngine()
        self.vizier = VizierOptimizer()
        self.pdm = PredictiveMaintenanceEngine()

        # 8 Core Personas
        self.personas = {
            "grid_dispatcher_agent": GridDispatcherPersona(self.harness, self.hitl, self.bq),
            "planning_engineer_agent": PlanningEngineerPersona(self.harness, self.hitl, self.bq),
            "derms_manager_agent": DermsManagerPersona(self.harness, self.hitl, self.bq),
            "protection_control_agent": ProtectionControlPersona(self.harness, self.hitl, self.bq),
            "asset_reliability_agent": AssetReliabilityPersona(self.harness, self.hitl, self.bq),
            "grid_analytics_data_scientist_agent": GridAnalyticsDataScientistPersona(self.harness, self.hitl, self.bq),
            "field_operations_tech_agent": FieldOperationsTechPersona(self.harness, self.hitl, self.bq),
            "regulatory_compliance_officer_agent": RegulatoryComplianceOfficerPersona(self.harness, self.hitl, self.bq),
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
        return self.workflows[workflow_name].run(**kwargs)

    def dispatch_persona(self, persona_id: str, task_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Dispatches a task directly to a persona agent."""
        if persona_id not in self.personas:
            raise ValueError(f"Persona '{persona_id}' not found. Available: {list(self.personas.keys())}")
        return self.personas[persona_id].execute_task(task_type, payload)

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

    def get_system_fleet_summary(self) -> Dict[str, Any]:
        """Returns overview of personas, sub-agents, skills, and pending HITL tickets."""
        total_sub_agents = sum(len(p.sub_agents) for p in self.personas.values())
        return {
            "fleet_name": "Utilities Grid Optimization Multi-Agent System",
            "personas_count": len(self.personas),
            "sub_agents_count": total_sub_agents,
            "workflows_count": len(self.workflows),
            "pending_hitl_tickets": len(self.hitl.get_pending_tickets()),
            "advanced_engines": ["Google DeepMind WeatherNext", "Vertex AI Vizier", "Predictive Maintenance (PdM)"],
            "operational_horizons": [
                "Real-Time Operations (Seconds to Hours)",
                "Intraday to Day-Ahead",
                "Medium to Long-Term Planning & Asset Management",
                "Periodic Governance & Regulatory Audit"
            ]
        }
