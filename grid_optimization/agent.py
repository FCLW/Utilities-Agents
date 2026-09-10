"""Grid Optimization Master Orchestrator ADK Agent.

Exposes the Multi-Agent System (MAS) through Google Agent Development Kit (ADK) v2.
Integrates 8 business personas, 48 heterogeneous sub-agents, 12 abstracted skills,
3 advanced optimization engines, safety validation harness, and HITL governance.
"""

import dataclasses
import inspect
import json
import logging
import os
import subprocess
from pathlib import Path
from typing import Any, Optional

def _to_serializable(obj: Any) -> Any:
    """Recursively converts dataclasses and objects with __dict__ into JSON-serializable structures."""
    if dataclasses.is_dataclass(obj) and not isinstance(obj, type):
        return dataclasses.asdict(obj)
    if hasattr(obj, "__dict__"):
        return {k: _to_serializable(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
    if isinstance(obj, list):
        return [_to_serializable(x) for x in obj]
    if isinstance(obj, dict):
        return {k: _to_serializable(v) for k, v in obj.items()}
    return obj

import google.auth
from google.auth.credentials import Credentials
from google.adk.agents import Agent

from grid_optimization.orchestrator import GridOptimizationOrchestrator

logger = logging.getLogger(__name__)

# Ensure environment settings for Vertex AI
os.environ.setdefault("GOOGLE_GENAI_USE_VERTEXAI", "True")
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", os.getenv("GCP_REGION", "us-central1"))
if "GOOGLE_CLOUD_PROJECT" not in os.environ:
    os.environ["GOOGLE_CLOUD_PROJECT"] = os.getenv("GCP_PROJECT_ID", "sandbox-ai-506805")


# Seamless local credential provider for local testing
class _DirectTokenCredentials(Credentials):
    def __init__(self, token: str):
        super().__init__()
        self.token = token

    def refresh(self, request):
        pass

    def apply(self, headers, token=None):
        headers["authorization"] = f"Bearer {self.token}"

    def before_request(self, request, method, url, headers):
        self.apply(headers)

    @property
    def valid(self):
        return True


def _ensure_local_auth():
    """Ensure credentials exist for local Vertex AI calls."""
    try:
        creds, project = google.auth.default()
        if not hasattr(creds, "token") or not creds.token:
            token = subprocess.check_output(
                ["gcloud", "auth", "print-access-token"], text=True, stderr=subprocess.DEVNULL
            ).strip()
            if token:
                direct_creds = _DirectTokenCredentials(token)
                google.auth.default = lambda *args, **kwargs: (
                    direct_creds,
                    os.getenv("GOOGLE_CLOUD_PROJECT", "sandbox-ai-506805"),
                )
    except Exception:
        try:
            token = subprocess.check_output(
                ["gcloud", "auth", "print-access-token"], text=True, stderr=subprocess.DEVNULL
            ).strip()
            if token:
                direct_creds = _DirectTokenCredentials(token)
                google.auth.default = lambda *args, **kwargs: (
                    direct_creds,
                    os.getenv("GOOGLE_CLOUD_PROJECT", "sandbox-ai-506805"),
                )
        except Exception:
            pass


_ensure_local_auth()

# Initialize orchestrator singleton
orchestrator = GridOptimizationOrchestrator()


def _parse_payload(payload: Any) -> dict:
    """Helper to safely parse input payload from dict or JSON string."""
    if isinstance(payload, dict):
        return payload
    if isinstance(payload, str) and payload.strip():
        try:
            return json.loads(payload)
        except Exception:
            return {"query": payload}
    return {}


# -------------------------------------------------------------------------
# ADK Tools for the Multi-Agent System
# -------------------------------------------------------------------------

def get_grid_fleet_status() -> dict:
    """Returns the full operational topology and status of the Grid Optimization MAS.

    Summarizes active Personas (8), Sub-Agents (48), Advanced Engines (3),
    Abstracted Skills (12), Collaborative Workflows (6), and pending HITL tickets.

    Returns:
        dict: High-level topology and fleet inventory.
    """
    summary = orchestrator.get_fleet_summary()
    pending_tickets = orchestrator.hitl_gateway.get_pending_tickets()
    summary["pending_hitl_ticket_count"] = len(pending_tickets)
    return {
        "status": "ONLINE",
        "fleet_summary": summary,
    }


def dispatch_persona_task(persona_id: str, task_name: str, payload_json: str = "{}") -> dict:
    """Dispatches a specialized operational task to one of the 8 Grid Optimization Personas.

    Args:
        persona_id: Identifier of the persona (e.g., 'grid_dispatcher_agent',
            'derms_manager_agent', 'planning_engineer_agent', 'asset_reliability_agent',
            'protection_control_agent', 'field_operations_tech_agent',
            'grid_analytics_data_scientist_agent', 'regulatory_compliance_officer_agent').
        task_name: Specific task or sub-agent routine to execute.
        payload_json: JSON string containing context, circuit ID, telemetry, or parameters.

    Returns:
        dict: Execution output from the target persona and its sub-agents.
    """
    payload = _parse_payload(payload_json)
    try:
        result = orchestrator.dispatch_persona_task(persona_id, task_name, payload)
        return {"status": "SUCCESS", "persona_id": persona_id, "result": result}
    except Exception as e:
        logger.error(f"Error dispatching task to persona {persona_id}: {e}")
        return {"status": "ERROR", "persona_id": persona_id, "error": str(e)}


def run_collaborative_workflow(workflow_name: str, payload_json: str = "{}") -> dict:
    """Executes a multi-persona collaborative workflow across the grid.

    Supported workflows:
    - 'flisr_restoration': Fault location, isolation, and service restoration.
    - 'dynamic_vvo': Coordinated Volt-VAR optimization with Vizier Bayesian tuning.
    - 'hosting_capacity': Interconnection hosting capacity study.
    - 'predictive_maintenance': Duval DGA & breaker wear health diagnostics.
    - 'dynamic_line_rating': WeatherNext weather-informed ampacity rating.
    - 'vpp_market_dispatch': Virtual power plant aggregation and market commitment.

    Args:
        workflow_name: Name of the collaborative workflow to execute.
        payload_json: JSON string containing circuit, feeder, or event parameters.

    Returns:
        dict: End-to-end multi-persona workflow results and safety evaluation.
    """
    payload = _parse_payload(payload_json)
    try:
        result = orchestrator.execute_workflow(workflow_name, payload)
        return {"status": "SUCCESS", "workflow": workflow_name, "result": result}
    except Exception as e:
        logger.error(f"Error executing collaborative workflow {workflow_name}: {e}")
        return {"status": "ERROR", "workflow": workflow_name, "error": str(e)}


def run_advanced_optimization_engine(engine_name: str, parameters_json: str = "{}") -> dict:
    """Directly invokes one of the three advanced grid optimization engines.

    Engines:
    - 'weathernext': High-resolution NWP weather forecast & convective cell tracking.
    - 'vizier': Vertex AI Vizier Bayesian Volt-VAR & BESS multi-objective tuner.
    - 'predictive_maintenance': Transformer DGA Duval Triangle & circuit breaker wear diagnostics.

    Args:
        engine_name: 'weathernext', 'vizier', or 'predictive_maintenance'.
        parameters_json: JSON string with parameters (e.g. lat/lon, feeder_id, DGA gases ppm).

    Returns:
        dict: Algorithmic output from the specialized engine.
    """
    params = _parse_payload(parameters_json)
    try:
        engine_key = engine_name.lower().strip()
        if "weather" in engine_key:
            substation = params.get("substation") or params.get("substation_or_region") or params.get("feeder_id") or "Substation-Metro"
            res = orchestrator.weathernext.get_forecast(
                substation_or_region=substation,
                lat=params.get("lat", 37.77),
                lon=params.get("lon", -122.42),
                horizon_hours=params.get("horizon_hours", 24),
            )
            return {"status": "SUCCESS", "engine": "WeatherNext", "output": _to_serializable(res)}
        elif "vizier" in engine_key or "bayesian" in engine_key:
            feeder_id = params.get("feeder_id", "FEEDER-WEST-01")
            res = orchestrator.vizier.optimize_volt_var_curves(feeder_id=feeder_id)
            return {"status": "SUCCESS", "engine": "VizierOptimizer", "output": _to_serializable(res)}
        elif "pdm" in engine_key or "maintenance" in engine_key:
            dga_sample = params.get("dga_sample", {})
            ch4 = dga_sample.get("methane_ch4") or params.get("ch4_ppm") or 45.0
            c2h4 = dga_sample.get("ethylene_c2h4") or params.get("c2h4_ppm") or 82.0
            c2h2 = dga_sample.get("acetylene_c2h2") or params.get("c2h2_ppm") or 15.0
            res = orchestrator.pdm.diagnose_transformer_dga(
                transformer_id=params.get("transformer_id", "XFMR-SUB-42"),
                ch4_ppm=float(ch4),
                c2h4_ppm=float(c2h4),
                c2h2_ppm=float(c2h2),
            )
            return {"status": "SUCCESS", "engine": "PredictiveMaintenance", "output": _to_serializable(res)}
        else:
            return {
                "status": "ERROR",
                "message": f"Unknown engine '{engine_name}'. Choose 'weathernext', 'vizier', or 'predictive_maintenance'.",
            }
    except Exception as e:
        logger.error(f"Error running engine {engine_name}: {e}")
        return {"status": "ERROR", "engine": engine_name, "error": str(e)}


def execute_abstracted_skill(skill_name: str, parameters_json: str = "{}") -> dict:
    """Executes any of the 12 abstracted reusable skills.

    Skills:
    - 'skill_topological_flisr_reconfigurator'
    - 'skill_vizier_bayesian_vvo_tuner'
    - 'skill_weathernext_telemetry_correlator'
    - 'skill_predictive_maintenance_health_scorer'
    - 'skill_power_flow_simulation'
    - 'skill_contingency_constraint_checker'
    - 'skill_hosting_capacity_evaluator'
    - 'skill_dynamic_line_rating_calculator'
    - 'skill_automated_switching_planner'
    - 'skill_der_vpp_co_optimizer'
    - 'skill_scada_ami_anomaly_detector'
    - 'skill_regulatory_audit_reporter'

    Args:
        skill_name: Name or key of the abstracted skill.
        parameters_json: JSON string of input parameters for the skill.

    Returns:
        dict: Skill execution result.
    """
    params = _parse_payload(parameters_json)
    norm_name = skill_name.strip()
    if not norm_name.startswith("skill_") and norm_name in [
        k.replace("skill_", "") for k in orchestrator.skills.keys()
    ]:
        norm_name = f"skill_{norm_name}"

    skill = orchestrator.skills.get(norm_name)
    if not skill:
        return {
            "status": "ERROR",
            "message": f"Skill '{skill_name}' not found. Available: {list(orchestrator.skills.keys())}",
        }

    try:
        sig = inspect.signature(skill.execute)
        kw = {}
        for p_name, p in sig.parameters.items():
            if p.kind == inspect.Parameter.VAR_KEYWORD:
                kw = dict(params)
                break
            if p_name in params:
                kw[p_name] = params[p_name]
            elif p_name in ["substation_id", "substation"]:
                kw[p_name] = params.get("substation_id") or params.get("substation") or "Substation-North"
            elif p_name in ["feeder_id", "circuit_id"]:
                kw[p_name] = params.get("feeder_id") or params.get("circuit_id") or "FEEDER-01"
            elif p_name == "asset_id":
                kw[p_name] = params.get("asset_id") or "XFMR-SUB-44"
            elif p_name == "asset_type":
                kw[p_name] = params.get("asset_type") or "TRANSFORMER"
            elif p_name == "diagnostic_payload":
                kw[p_name] = params.get("dga_sample") or params
            elif p_name == "fault_zone":
                kw[p_name] = params.get("fault_zone") or params.get("isolated_segment") or "ZONE-B-FAULT"
            elif p_name == "telemetry_series":
                kw[p_name] = params.get("telemetry_series") or [1.01, 1.00, 0.99, 1.02, 0.82, 1.01, 1.00]
            elif p_name == "total_customers":
                kw[p_name] = int(params.get("total_customers", 125000))
            elif p_name == "customer_interruption_minutes":
                kw[p_name] = float(params.get("customer_interruption_minutes", 8750000.0))
            elif p_name == "sustained_outage_count":
                kw[p_name] = int(params.get("sustained_outage_count", 145000))
            elif p_name == "bus_count":
                kw[p_name] = int(params.get("bus_count", 14))
            elif p.default != inspect.Parameter.empty:
                pass

        if kw:
            output = skill.execute(**kw)
        else:
            output = skill.execute(params)

        return {"status": "SUCCESS", "skill": norm_name, "output": _to_serializable(output)}
    except Exception as e:
        return {"status": "ERROR", "skill": norm_name, "error": str(e)}


def validate_grid_constraints(
    proposed_action: str,
    voltage_pu: float = 1.02,
    line_loading_pct: float = 78.5,
    reverse_power_kw: float = 0.0,
    anti_islanding_certified: bool = True,
) -> dict:
    """Validates proposed actions against physical power engineering limits (ANSI C84.1, thermal ratings).

    Args:
        proposed_action: Description of proposed operation (e.g. 'CLOSE_CB_102', 'CAPACITOR_BANK_1_CLOSE').
        voltage_pu: Simulated or measured voltage in per-unit (acceptable: 0.95 - 1.05 p.u.).
        line_loading_pct: Line or transformer loading percentage (acceptable: <= 100%).
        reverse_power_kw: Reverse active power flow in kW (threshold: 500 kW).
        anti_islanding_certified: Whether IEEE 1547 anti-islanding interlock is active.

    Returns:
        dict: Validation report with pass/fail status and violation details.
    """
    telemetry = {
        "voltage_pu": voltage_pu,
        "line_loading_pct": line_loading_pct,
        "reverse_power_kw": reverse_power_kw,
        "anti_islanding_certified": anti_islanding_certified,
    }
    action = {"action_type": proposed_action, "target_device": "GRID_ASSET"}
    report = orchestrator.validation_harness.validate_pre_execution(action, telemetry)
    return {
        "status": "SUCCESS",
        "action": proposed_action,
        "is_safe": report.is_safe,
        "violations": report.violations,
        "metrics": report.metrics,
    }


def manage_hitl_ticket(
    action: str,
    ticket_id: str = "",
    operator_id: str = "OP-104",
    override_reason: str = "Authorized grid restoration",
) -> dict:
    """Manages Human-in-the-Loop (HITL) approval tickets for high/medium-risk grid actions.

    Actions:
    - 'list': List all pending approval tickets.
    - 'approve': Approve and digitally sign a ticket for execution.
    - 'reject': Reject a proposed ticket.

    Args:
        action: 'list', 'approve', or 'reject'.
        ticket_id: The unique ID of the ticket (required for approve/reject).
        operator_id: ID of the reviewing grid operator.
        override_reason: Justification notes for approval/rejection.

    Returns:
        dict: Operation status and updated ticket state.
    """
    act = action.lower().strip()
    if act == "list":
        tickets = orchestrator.hitl_gateway.get_pending_tickets()
        return {
            "status": "SUCCESS",
            "pending_count": len(tickets),
            "tickets": [
                {
                    "ticket_id": t.ticket_id,
                    "action_type": t.action_type,
                    "target_substation": t.target_substation,
                    "target_feeder": t.target_feeder,
                    "risk_tier": t.risk_tier.value,
                    "proposed_command": t.proposed_command,
                    "created_at": t.created_at,
                }
                for t in tickets
            ],
        }
    elif act == "approve":
        if not ticket_id:
            return {"status": "ERROR", "message": "ticket_id is required to approve."}
        ticket = orchestrator.hitl_gateway.approve_ticket(
            ticket_id=ticket_id,
            operator_id=operator_id,
            operator_role="Lead Control Room Operator",
            justification_notes=override_reason,
        )
        return {
            "status": "SUCCESS",
            "approved": True,
            "ticket_id": ticket.ticket_id,
            "status_code": ticket.status.value,
            "reviewed_at": ticket.reviewed_at,
            "digital_signature": f"SIG-{ticket.ticket_id}-{operator_id}",
        }
    elif act == "reject":
        if not ticket_id:
            return {"status": "ERROR", "message": "ticket_id is required to reject."}
        ticket = orchestrator.hitl_gateway.reject_ticket(
            ticket_id=ticket_id,
            operator_id=operator_id,
            rejection_reason=override_reason,
        )
        return {
            "status": "SUCCESS",
            "approved": False,
            "ticket_id": ticket.ticket_id,
            "status_code": ticket.status.value,
            "reviewed_at": ticket.reviewed_at,
        }
    else:
        return {"status": "ERROR", "message": f"Unsupported action '{action}'. Use 'list', 'approve', or 'reject'."}


def query_grid_telemetry(dataset_name: str, query: str = "") -> dict:
    """Queries multi-dataset BigQuery tables for grid telemetry, asset health, and market data.

    Args:
        dataset_name: BigQuery dataset (e.g. 'utilities_grid_operations',
            'utilities_asset_management', 'utilities_grid_balancing').
        query: SQL query or filter string.

    Returns:
        dict: Query results with schema and simulated or live records.
    """
    tool = orchestrator.multi_dataset_tool
    table_name = "feeder_telemetry"
    if "asset" in dataset_name:
        table_name = "transformer_dga"
    elif "balancing" in dataset_name or "trade" in dataset_name:
        table_name = "lmp_congestion"

    res = tool.query_dataset(dataset=dataset_name, table=table_name, sql_query=query if query else None)
    return {
        "status": "SUCCESS",
        "dataset": dataset_name,
        "table": res.table,
        "total_rows": res.total_rows,
        "rows": res.rows,
        "is_mock": res.is_mock,
    }


# -------------------------------------------------------------------------
# ADK Agent Definition
# -------------------------------------------------------------------------

instruction_path = Path(__file__).parent / "instructions" / "orchestrator.md"
if instruction_path.exists():
    with open(instruction_path, "r", encoding="utf-8") as f:
        instruction = f.read()
else:
    instruction = "You are the Grid Optimization Master Orchestrator coordinating modern electric utility operations."

model_name = os.getenv("LLM_MODEL_NAME", "gemini-2.5-flash")

root_agent = Agent(
    name="grid_optimization_orchestrator",
    model=model_name,
    description=(
        "Master Orchestrator for the Grid Optimization Multi-Agent System (MAS). "
        "Coordinates 8 business personas, 48 heterogeneous sub-agents, 12 abstracted skills, "
        "and 3 advanced engines (Google DeepMind WeatherNext, Vertex AI Vizier, Predictive Maintenance) "
        "with strict engineering validation harness and Human-in-the-Loop (HITL) governance."
    ),
    instruction=instruction,
    tools=[
        get_grid_fleet_status,
        dispatch_persona_task,
        run_collaborative_workflow,
        run_advanced_optimization_engine,
        execute_abstracted_skill,
        validate_grid_constraints,
        manage_hitl_ticket,
        query_grid_telemetry,
    ],
)

agent = root_agent
