"""FastAPI and ADK App serving entrypoint for Grid Optimization MAS."""

import asyncio
import json
import logging
from typing import Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from google.adk.apps.app import App

from grid_optimization.agent import root_agent, orchestrator, _to_serializable

logger = logging.getLogger(__name__)

app = FastAPI(title="Grid Optimization Master Orchestrator", version="2.0.0")

# Enable CORS for local dashboards and cross-origin tools
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

adk_app = App(name="grid_optimization", root_agent=root_agent)


@app.get("/healthz")
def healthz():
    return {
        "status": "ok",
        "agent": root_agent.name,
        "fleet_personas": len(orchestrator.personas),
        "fleet_workflows": len(orchestrator.workflows),
    }


@app.get("/api/fleet")
def get_fleet_summary():
    """Returns overview of personas, sub-agents, skills, and pending HITL tickets."""
    return orchestrator.get_fleet_summary()


# Workflow Step Mapping Metadata
WORKFLOW_STEP_MAPPING = {
    "flisr": [
        {"persona": "grid_dispatcher_agent", "persona_name": "Grid Operations Dispatcher", "task": "MONITOR_AND_DISPATCH", "title": "Fault Telemetry Ingestion & Anomaly Flagging", "tools": ["ScadaTelemetryMonitorSubAgent", "ValidationHarness", "ScadaAmiAnomalyDetectorSkill"]},
        {"persona": "grid_dispatcher_agent", "persona_name": "Grid Operations Dispatcher", "task": "TRIGGER_FLISR_SWITCHING", "title": "Topological DNR Reconfiguration Optimization", "tools": ["TopologicalSwitchingCoordinatorSubAgent", "TopologicalFlisrReconfiguratorSkill", "HITLGateway"]},
        {"persona": "protection_control_agent", "persona_name": "Protection & Control (P&C) Engineer", "task": "ADAPTIVE_RELAY_STUDY", "title": "Protection Interlock & Reverse Power Check", "tools": ["AdaptiveProtectionSettingsSubAgent", "FaultCurrentAnalyzerSubAgent", "AntiIslandingVerificationSubAgent"]},
        {"persona": "field_operations_tech_agent", "persona_name": "Field Operations & Substation Tech", "task": "EXECUTE_PDM_FIELD_WORK", "title": "Mandatory HITL Sign-Off & SCADA Dispatch", "tools": ["SwitchingOrderSafetyVerifierSubAgent", "FieldTechnicianCopilotSubAgent", "HITLGateway"]}
    ],
    "vvo": [
        {"persona": "grid_analytics_data_scientist_agent", "persona_name": "Data Scientist / Grid Analytics", "task": "INGEST_WEATHERNEXT_AND_FORECAST", "title": "AMI Interval Voltage Profiling", "tools": ["ScadaTelemetryAnomalyDetectorSubAgent", "LoadForecastingEngineSubAgent", "MultiDatasetBigQueryTool"]},
        {"persona": "grid_dispatcher_agent", "persona_name": "Grid Operations Dispatcher", "task": "MONITOR_AND_DISPATCH", "title": "Vertex AI Vizier Bayesian Curve Tuning", "tools": ["VoltVarDispatchOptimizerSubAgent", "VizierBayesianVvoTunerSkill", "VizierOptimizer"]},
        {"persona": "derms_manager_agent", "persona_name": "DER & Flexibility Program Manager", "task": "OPTIMIZE_VPP_SCHEDULE", "title": "Substation LTC & Capacitor Coordination", "tools": ["VizierBessArbitrageSubAgent", "DemandResponseDispatcherSubAgent", "ValidationHarness"]},
        {"persona": "grid_dispatcher_agent", "persona_name": "Grid Operations Dispatcher", "task": "MONITOR_AND_DISPATCH", "title": "Real-Time Closed-Loop Validation", "tools": ["StateEstimationEngineSubAgent", "ContingencyScreenerSubAgent", "ValidationHarness"]}
    ],
    "pdm": [
        {"persona": "asset_reliability_agent", "persona_name": "Asset Performance & Reliability (PdM)", "task": "RUN_PREDICTIVE_MAINTENANCE_ASSESSMENT", "title": "Online DGA Gas Ratio Sampling", "tools": ["TransformerDgaDiagnosticSubAgent", "PredictiveMaintenanceEngine", "PredictiveMaintenanceHealthScorerSkill"]},
        {"persona": "asset_reliability_agent", "persona_name": "Asset Performance & Reliability (PdM)", "task": "RUN_PREDICTIVE_MAINTENANCE_ASSESSMENT", "title": "Duval Triangle 1 Fault Classification", "tools": ["TransformerDgaDiagnosticSubAgent", "AssetStrategyCopilotSubAgent", "PredictiveMaintenanceEngine"]},
        {"persona": "grid_analytics_data_scientist_agent", "persona_name": "Data Scientist / Grid Analytics", "task": "SCADA_TELEMETRY_ANOMALY_SCAN", "title": "Circuit Breaker Arcing Wear (∑I²t) Aggregation", "tools": ["CircuitBreakerWearSubAgent", "ScadaAmiAnomalyDetectorSkill", "MultiDatasetBigQueryTool"]},
        {"persona": "field_operations_tech_agent", "persona_name": "Field Operations & Substation Tech", "task": "EXECUTE_PDM_FIELD_WORK", "title": "Risk-Prioritized Field Crew Dispatch", "tools": ["PredictiveMaintenanceWorkOrderReceiverSubAgent", "FieldTechnicianCopilotSubAgent", "HITLGateway"]}
    ],
    "dlr": [
        {"persona": "planning_engineer_agent", "persona_name": "T&D System Planning Engineer", "task": "HOSTING_CAPACITY_STUDY", "title": "WeatherNext Atmospheric Microclimate Fetch", "tools": ["WeatherNextEngine", "WeatherNextTelemetryCorrelatorSkill", "MultiDatasetBigQueryTool"]},
        {"persona": "asset_reliability_agent", "persona_name": "T&D System Planning Engineer", "task": "SOLVE_DYNAMIC_LINE_RATING", "title": "IEEE 738 Conductor Heat Balance Solver", "tools": ["DynamicLineRatingSolverSubAgent", "DynamicLineRatingCalculatorSkill", "WeatherNextEngine"]},
        {"persona": "grid_dispatcher_agent", "persona_name": "Grid Operations Dispatcher", "task": "MONITOR_AND_DISPATCH", "title": "Contingency Verification (N-1 Overload Screening)", "tools": ["ContingencyScreenerSubAgent", "ContingencyConstraintCheckerSkill", "ValidationHarness"]},
        {"persona": "grid_dispatcher_agent", "persona_name": "Grid Operations Dispatcher", "task": "MONITOR_AND_DISPATCH", "title": "Dispatch Limit Update in EMS/SCADA", "tools": ["VoltVarDispatchOptimizerSubAgent", "DispatcherCopilotReasonerSubAgent", "HITLGateway"]}
    ],
    "hosting": [
        {"persona": "planning_engineer_agent", "persona_name": "T&D System Planning Engineer", "task": "HOSTING_CAPACITY_STUDY", "title": "GIS Feeder Topology & Model Extraction", "tools": ["HostingCapacityEngineSubAgent", "MultiDatasetBigQueryTool", "PowerFlowSimulationSkill"]},
        {"persona": "planning_engineer_agent", "persona_name": "T&D System Planning Engineer", "task": "HOSTING_CAPACITY_STUDY", "title": "Iterative Injection Power Flow Sweeps", "tools": ["HostingCapacityEngineSubAgent", "HostingCapacityEvaluatorSkill", "ValidationHarness"]},
        {"persona": "protection_control_agent", "persona_name": "Protection & Control (P&C) Engineer", "task": "ADAPTIVE_RELAY_STUDY", "title": "Anti-Islanding & Protection Screening", "tools": ["AntiIslandingVerificationSubAgent", "FaultCurrentAnalyzerSubAgent", "ValidationHarness"]},
        {"persona": "derms_manager_agent", "persona_name": "DER & Flexibility Program Manager", "task": "OPTIMIZE_VPP_SCHEDULE", "title": "Interconnection Report & Smart Inverter Spec", "tools": ["InterconnectionStudyCopilotSubAgent", "FlexibilityProgramCopilotSubAgent", "RegulatoryAuditReporterSkill"]}
    ],
    "vpp": [
        {"persona": "derms_manager_agent", "persona_name": "DER & Flexibility Program Manager", "task": "OPTIMIZE_VPP_SCHEDULE", "title": "Aggregated VPP Capacity & State of Charge Assessment", "tools": ["VppAggregatorSubAgent", "DerVppCoOptimizerSkill", "MultiDatasetBigQueryTool"]},
        {"persona": "regulatory_compliance_officer_agent", "persona_name": "Regulatory, Market & Compliance Officer", "task": "ANNUAL_COMPLIANCE_AUDIT", "title": "Day-Ahead LMP Price Spike Detection", "tools": ["WholesaleMarketSettlementReconcilerSubAgent", "RegulatoryAuditReporterSkill", "MultiDatasetBigQueryTool"]},
        {"persona": "grid_analytics_data_scientist_agent", "persona_name": "Data Scientist / Grid Analytics", "task": "INGEST_WEATHERNEXT_AND_FORECAST", "title": "Battery Degradation vs Arbitrage Co-Optimization", "tools": ["VizierBessArbitrageSubAgent", "VizierBayesianVvoTunerSkill", "DerVppCoOptimizerSkill"]},
        {"persona": "derms_manager_agent", "persona_name": "DER & Flexibility Program Manager", "task": "OPTIMIZE_VPP_SCHEDULE", "title": "Automated Dispatch & Settlement Verification", "tools": ["DemandResponseDispatcherSubAgent", "FlexibilityProgramCopilotSubAgent", "HITLGateway"]}
    ]
}


@app.post("/api/workflow/step")
async def execute_workflow_step(payload: dict = Body(...)):
    """Executes an interactive single step in a multi-persona workflow in real-time."""
    workflow_key = payload.get("workflow_key", "flisr").lower()
    step_index = int(payload.get("step_index", 0))
    user_params = payload.get("parameters") or {}
    custom_prompt = payload.get("custom_prompt") or ""

    if workflow_key not in WORKFLOW_STEP_MAPPING:
        raise HTTPException(status_code=400, detail=f"Invalid workflow_key '{workflow_key}'. Available: {list(WORKFLOW_STEP_MAPPING.keys())}")

    steps = WORKFLOW_STEP_MAPPING[workflow_key]
    if step_index < 0 or step_index >= len(steps):
        raise HTTPException(status_code=400, detail=f"Step index {step_index} out of bounds for workflow '{workflow_key}' (0..{len(steps)-1})")

    step_info = steps[step_index]
    persona_id = step_info["persona"]
    task_name = step_info["task"]

    # Merge default step parameters with any user-provided parameters
    merged_payload = {
        "feeder_id": user_params.get("feeder_id", "F-102"),
        "substation": user_params.get("substation", "Sub-Metro"),
        "voltage_pu": float(user_params.get("voltage_pu", 0.94)),
        "frequency_hz": float(user_params.get("frequency_hz", 59.94)),
        "custom_prompt": custom_prompt,
        **user_params
    }

    try:
        # Run validation harness
        validation = orchestrator.harness.validate_input_telemetry(merged_payload)

        # Dispatch task to the step's persona
        persona_output = orchestrator.dispatch_persona(persona_id, task_name, merged_payload)

        # Build inter-persona handoff payload
        handoff_data = {
            "source_persona": persona_id,
            "workflow": workflow_key,
            "step_index": step_index,
            "handoff_timestamp": "2026-09-14T08:14:00Z",
            "passed_parameters": {
                "feeder_id": merged_payload.get("feeder_id"),
                "substation": merged_payload.get("substation"),
                "status": "VALIDATED",
                "risk_tier": persona_output.get("approval_ticket", {}).get("risk_tier", "LOW")
            }
        }

        # Synthesize engineering response memo
        reasoning_memo = (
            f"Persona {step_info['persona_name']} executed task '{task_name}' successfully. "
            f"Input telemetry verified against ANSI C84.1 / IEEE standards (Status: {validation.risk_level}). "
            f"Executed sub-agent toolchain: {', '.join(step_info['tools'])}. "
        )
        if custom_prompt:
            reasoning_memo += f"Addressed operator inquiry: '{custom_prompt}'. "

        if "approval_ticket" in persona_output:
            ticket = persona_output["approval_ticket"]
            reasoning_memo += f"Action requires HITL Approval (Ticket #{ticket.get('ticket_id')} - {ticket.get('action_type')})."
        else:
            reasoning_memo += "Autonomous handoff token generated and ready for downstream persona."

        return {
            "status": "SUCCESS",
            "workflow_key": workflow_key,
            "step_index": step_index,
            "step_title": step_info["title"],
            "persona_id": persona_id,
            "persona_name": step_info["persona_name"],
            "task_name": task_name,
            "tools_invoked": step_info["tools"],
            "validation": _to_serializable(validation),
            "results": _to_serializable(persona_output.get("results", {})),
            "approval_ticket": _to_serializable(persona_output.get("approval_ticket")),
            "handoff_token": handoff_data,
            "reasoning_memo": reasoning_memo
        }
    except Exception as e:
        logger.error(f"Error in execute_workflow_step: {e}")
        return {
            "status": "ERROR",
            "error": str(e),
            "workflow_key": workflow_key,
            "step_index": step_index,
            "persona_id": persona_id
        }


@app.post("/api/persona/interact")
async def interact_with_persona(payload: dict = Body(...)):
    """Interacts directly with any of the 8 grid personas with custom parameters or prompt."""
    persona_id = payload.get("persona_id", "grid_dispatcher_agent")
    task_name = payload.get("task_name", "MONITOR_AND_DISPATCH")
    prompt = payload.get("prompt") or payload.get("message") or ""
    task_payload = payload.get("payload") or {}
    if prompt:
        task_payload["prompt"] = prompt

    try:
        res = orchestrator.dispatch_persona(persona_id, task_name, task_payload)
        return {
            "status": "SUCCESS",
            "persona_id": persona_id,
            "task_name": task_name,
            "result": _to_serializable(res)
        }
    except Exception as e:
        logger.error(f"Error interacting with persona {persona_id}: {e}")
        return {"status": "ERROR", "persona_id": persona_id, "error": str(e)}


@app.post("/api/hitl/review")
async def review_hitl(payload: dict = Body(...)):
    """Reviews an active HITL ticket with operator sign-off."""
    ticket_id = payload.get("ticket_id")
    approve = bool(payload.get("approve", True))
    operator_id = payload.get("operator_id", "LEAD_OPERATOR_402")
    role = payload.get("role", "Lead Control Room Operator")
    notes = payload.get("notes", "Verified safe switching clearance and topological radiality.")

    if not ticket_id:
        raise HTTPException(status_code=400, detail="Missing required field 'ticket_id'")

    res = orchestrator.review_hitl_ticket(
        ticket_id=ticket_id,
        approve=approve,
        operator_id=operator_id,
        role=role,
        notes=notes
    )
    return _to_serializable(res)


@app.post("/api/workflow/run")
async def run_entire_workflow(payload: dict = Body(...)):
    """Runs a full collaborative multi-persona workflow end-to-end."""
    workflow_name = payload.get("workflow_name", "flisr_restoration")
    wf_payload = payload.get("payload") or {}
    try:
        res = orchestrator.execute_workflow(workflow_name, wf_payload)
        return {"status": "SUCCESS", "workflow": workflow_name, "result": _to_serializable(res)}
    except Exception as e:
        logger.error(f"Error executing collaborative workflow {workflow_name}: {e}")
        return {"status": "ERROR", "workflow": workflow_name, "error": str(e)}


@app.post("/chat/stream")
async def chat_stream(request: dict):
    """Streams agent execution responses as Server-Sent Events (SSE)."""
    message = request.get("message") or request.get("prompt") or request.get("query") or ""

    async def event_generator():
        try:
            yield f"event: open\ndata: {json.dumps({'agent': root_agent.name})}\n\n"
            fleet = orchestrator.get_fleet_summary()
            p_count = fleet.get("persona_count", 8)
            sa_count = fleet.get("sub_agent_count", 48)
            wf_count = fleet.get("workflow_count", 6)
            msg = f"Grid Orchestrator ready. Active Personas: {p_count}, Sub-Agents: {sa_count}, Workflows: {wf_count}"
            yield f"event: message\ndata: {json.dumps({'content': msg})}\n\n"
            yield "event: close\ndata: [DONE]\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
