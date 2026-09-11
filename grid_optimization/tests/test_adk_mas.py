"""Comprehensive ADK integration test suite for Grid Optimization MAS.

Tests each component locally through ADK (Agent Development Kit) v2:
- ADK AgentLoader discovery of root_agent
- ADK Agent tools and attributes
- 8 Business Personas and 48 Sub-Agents via ADK dispatch tool
- 6 Collaborative Workflows via ADK workflow tool
- 3 Advanced Engines (WeatherNext, Vizier, PdM) via ADK engine tool
- 12 Abstracted Skills via ADK skill tool
- Validation Harness and HITL Gateway governance via ADK safety tools
- Multi-Dataset BigQuery access via ADK telemetry tool
- ADK Runner and InMemorySessionService execution
"""

import json
import pytest
import pytest_asyncio
from pathlib import Path

from google.adk.cli.utils.agent_loader import AgentLoader
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from grid_optimization.agent import (
    root_agent,
    get_grid_fleet_status,
    dispatch_persona_task,
    run_collaborative_workflow,
    run_advanced_optimization_engine,
    execute_abstracted_skill,
    validate_grid_constraints,
    manage_hitl_ticket,
    query_grid_telemetry,
    orchestrator,
)


class TestADKMasComponents:
    """Test every Grid Optimization MAS component through ADK interfaces."""

    def test_01_adk_agent_loader_discovery(self):
        """Verify ADK CLI agent loader discovers and loads root_agent."""
        repo_root = Path(__file__).resolve().parents[2]
        loader = AgentLoader(agents_dir=str(repo_root))
        loaded_agent = loader.load_agent("grid_optimization")

        assert loaded_agent is not None
        assert loaded_agent.name == "grid_optimization_orchestrator"
        assert len(loaded_agent.tools) == 8
        assert "Grid Optimization Master Orchestrator" in loaded_agent.instruction

    def test_02_adk_fleet_status_tool(self):
        """Verify get_grid_fleet_status tool exposes complete system inventory."""
        res = get_grid_fleet_status()
        assert res["status"] == "ONLINE"
        summary = res["fleet_summary"]
        assert summary["persona_count"] == 8
        assert summary["sub_agent_count"] == 48
        assert summary["skill_count"] == 12
        assert summary["workflow_count"] == 6
        assert len(summary["advanced_engines"]) == 3
        assert "AlphaEvolve" not in str(summary)

    @pytest.mark.parametrize(
        "persona_id,task_name",
        [
            ("grid_dispatcher_agent", "volt_var_optimization"),
            ("derms_manager_agent", "vpp_aggregation"),
            ("planning_engineer_agent", "hosting_capacity_study"),
            ("asset_reliability_agent", "transformer_dga_assessment"),
            ("protection_control_agent", "relay_coordination_check"),
            ("field_operations_tech_agent", "crew_dispatch_planning"),
            ("grid_analytics_data_scientist_agent", "scada_telemetry_anomaly_scan"),
            ("regulatory_compliance_officer_agent", "reliability_metrics_compilation"),
        ],
    )
    def test_03_dispatch_all_8_personas(self, persona_id, task_name):
        """Verify dispatch_persona_task successfully routes to all 8 business personas."""
        payload = json.dumps({"circuit_id": "CKT-WEST-01", "substation": "SUB-42"})
        res = dispatch_persona_task(persona_id=persona_id, task_name=task_name, payload_json=payload)
        assert res["status"] == "SUCCESS", f"Failed for {persona_id}: {res.get('error')}"
        assert res["persona_id"] == persona_id
        assert "result" in res

    @pytest.mark.parametrize(
        "workflow_name",
        [
            "flisr_restoration",
            "dynamic_vvo",
            "hosting_capacity",
            "predictive_maintenance",
            "dynamic_line_rating",
            "vpp_market_dispatch",
        ],
    )
    def test_04_run_all_6_collaborative_workflows(self, workflow_name):
        """Verify run_collaborative_workflow executes all 6 multi-persona workflows."""
        payload = json.dumps({"feeder_id": "FEEDER-WEST-01", "operator_id": "OP-104"})
        res = run_collaborative_workflow(workflow_name=workflow_name, payload_json=payload)
        assert res["status"] == "SUCCESS", f"Workflow {workflow_name} failed: {res.get('error')}"
        assert res["workflow"] == workflow_name
        assert "result" in res

    @pytest.mark.parametrize(
        "engine_name,params",
        [
            ("weathernext", {"lat": 37.77, "lon": -122.42, "horizon_hours": 24}),
            ("vizier", {"feeder_id": "FEEDER-NORTH-04"}),
            ("predictive_maintenance", {"dga_sample": {"methane_ch4": 40.0, "ethylene_c2h4": 80.0, "acetylene_c2h2": 15.0}}),
        ],
    )
    def test_05_run_all_3_advanced_engines(self, engine_name, params):
        """Verify direct invocation of all 3 advanced optimization engines."""
        payload = json.dumps(params)
        res = run_advanced_optimization_engine(engine_name=engine_name, parameters_json=payload)
        assert res["status"] == "SUCCESS", f"Engine {engine_name} failed: {res.get('error')}"
        assert "output" in res

    @pytest.mark.parametrize(
        "skill_key",
        [
            "skill_topological_flisr_reconfigurator",
            "skill_vizier_bayesian_vvo_tuner",
            "skill_weathernext_telemetry_correlator",
            "skill_predictive_maintenance_health_scorer",
            "skill_power_flow_simulation",
            "skill_contingency_constraint_checker",
            "skill_hosting_capacity_evaluator",
            "skill_dynamic_line_rating_calculator",
            "skill_automated_switching_planner",
            "skill_der_vpp_co_optimizer",
            "skill_scada_ami_anomaly_detector",
            "skill_regulatory_audit_reporter",
        ],
    )
    def test_06_execute_all_12_abstracted_skills(self, skill_key):
        """Verify each of the 12 abstracted skills executes and returns validated output."""
        sample_params = json.dumps({
            "circuit_id": "CKT-01",
            "feeder_id": "FEEDER-01",
            "weather_forecast": {"wind_speed_mps": 12.0, "ambient_temp_c": 24.0, "solar_irradiance_wm2": 850.0},
            "breaker_tripped": "CB-101",
            "isolated_segment": "SEG-03",
            "der_candidates_mw": 5.0,
            "dga_sample": {"methane_ch4": 30.0, "ethylene_c2h4": 60.0, "acetylene_c2h2": 10.0},
        })
        res = execute_abstracted_skill(skill_name=skill_key, parameters_json=sample_params)
        assert res["status"] == "SUCCESS", f"Skill {skill_key} failed: {res.get('error')}"
        assert "output" in res

    def test_07_validation_harness_safe_and_unsafe_checks(self):
        """Verify validation_harness enforces ANSI C84.1, thermal ampacity, and anti-islanding."""
        # Case A: Safe operation within limits
        safe_res = validate_grid_constraints(
            proposed_action="CLOSE_TIE_CB_102",
            voltage_pu=1.02,
            line_loading_pct=75.0,
            reverse_power_kw=100.0,
            anti_islanding_certified=True,
        )
        assert safe_res["status"] == "SUCCESS"
        assert safe_res["is_safe"] is True
        assert len(safe_res["violations"]) == 0

        # Case B: Unsafe operation violating all 3 safety thresholds
        unsafe_res = validate_grid_constraints(
            proposed_action="OVERLOAD_FEEDER_TRANSFER",
            voltage_pu=1.09,          # Violates ANSI C84.1 (> 1.05 p.u.)
            line_loading_pct=125.0,    # Violates thermal rating (> 100%)
            reverse_power_kw=650.0,    # Violates reverse power limit (> 500 kW)
            anti_islanding_certified=False,  # Violates IEEE 1547 anti-islanding
        )
        assert unsafe_res["status"] == "SUCCESS"
        assert unsafe_res["is_safe"] is False
        assert len(unsafe_res["violations"]) >= 3

    def test_08_hitl_gateway_ticket_lifecycle(self):
        """Verify HITL gateway ticket listing, approval, and rejection through ADK tools."""
        # 1. Trigger a high-risk action to generate a pending ticket
        flisr_res = run_collaborative_workflow("flisr_restoration")
        assert flisr_res["status"] == "SUCCESS"

        # 2. List pending tickets
        list_res = manage_hitl_ticket(action="list")
        assert list_res["status"] == "SUCCESS"
        tickets = list_res["tickets"]
        assert len(tickets) > 0

        target_ticket = tickets[0]
        ticket_id = target_ticket["ticket_id"]

        # 3. Approve ticket with operator signature
        appr_res = manage_hitl_ticket(
            action="approve",
            ticket_id=ticket_id,
            operator_id="DISPATCHER-LEAD-402",
            override_reason="Critical service restoration to regional hospital",
        )
        assert appr_res["status"] == "SUCCESS"
        assert appr_res["approved"] is True
        assert "digital_signature" in appr_res

    def test_09_query_grid_telemetry_tool(self):
        """Verify query_grid_telemetry accesses BigQuery datasets."""
        res = query_grid_telemetry(
            dataset_name="utilities_grid_operations",
            query="SELECT timestamp, voltage_pu, frequency_hz FROM feeder_telemetry LIMIT 5",
        )
        assert res["status"] == "SUCCESS"
        assert res["dataset"] == "utilities_grid_operations"
        assert "rows" in res
        assert res["total_rows"] > 0

    @pytest.mark.asyncio
    async def test_10_adk_runner_in_memory_session(self):
        """Verify ADK Runner executes queries using InMemorySessionService."""
        session_service = InMemorySessionService()
        session = await session_service.create_session(
            app_name="grid_optimization", user_id="test_operator"
        )
        runner = Runner(
            agent=root_agent,
            app_name="grid_optimization",
            session_service=session_service,
        )

        message = types.Content(
            parts=[types.Part.from_text(text="What is the grid fleet status?")]
        )

        events = []
        async for event in runner.run_async(
            session_id=session.id,
            user_id="test_operator",
            new_message=message,
        ):
            events.append(event)

        assert len(events) > 0
        # Verify event stream produced content
        has_content = any(hasattr(e, "content") and e.content for e in events)
        assert has_content

    def test_11_weathernext_malaysia_and_subagents_integration(self):
        """Verify WeatherNext engine resolves Malaysian locations and executes all 4 integrated subagents."""
        # 1. Klang Valley TNB Supergrid Hub
        payload_klang = json.dumps({
            "substation": "Klang Valley / Selangor (500kV Supergrid Hub)",
            "horizon_hours": 14,
            "include_subagents": True
        })
        res_klang = run_advanced_optimization_engine("weathernext", payload_klang)
        assert res_klang["status"] == "SUCCESS"
        assert res_klang["engine"] == "WeatherNext"
        output_kl = res_klang["output"]
        assert "Klang Valley" in output_kl["substation_or_region"]
        assert output_kl["solar_ghi_wm2"] >= 0.0
        assert output_kl["relative_humidity_pct"] >= 50.0

        # Verify all 4 integrated WeatherNext subagents executed
        subagents = res_klang["subagents_telemetry"]
        assert "storm_tracker" in subagents
        assert "forecast_consumer" in subagents
        assert "der_predictor" in subagents
        assert "dlr_solver" in subagents

        assert subagents["storm_tracker"]["status"] == "SUCCESS"
        assert subagents["forecast_consumer"]["status"] == "SUCCESS"
        assert subagents["der_predictor"]["status"] == "SUCCESS"
        assert subagents["dlr_solver"]["status"] == "SUCCESS"

        # 2. East Malaysia / Sarawak Energy Grid (Bakun Hydro)
        payload_bakun = json.dumps({
            "substation": "Bakun Hydro Terminal (500kV Hydro Complex)",
            "horizon_hours": 6,
            "include_subagents": True
        })
        res_bakun = run_advanced_optimization_engine("weathernext", payload_bakun)
        assert res_bakun["status"] == "SUCCESS"
        assert "Bakun" in res_bakun["output"]["substation_or_region"]
        assert res_bakun["subagents_telemetry"]["dlr_solver"]["data"]["voltage_kv"] == 500

