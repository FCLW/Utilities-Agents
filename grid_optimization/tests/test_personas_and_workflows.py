import pytest
from grid_optimization.orchestrator import GridOptimizationOrchestrator

def test_orchestrator_fleet_summary():
    orchestrator = GridOptimizationOrchestrator()
    summary = orchestrator.get_system_fleet_summary()
    assert summary["personas_count"] == 8
    assert summary["sub_agents_count"] >= 40
    assert summary["workflows_count"] == 6

def test_collaborative_workflows():
    orchestrator = GridOptimizationOrchestrator()

    # Dynamic VVO with Vizier
    w1 = orchestrator.run_workflow("dynamic_vvo", feeder_id="F-401")
    assert w1["status"] == "VVO_OPTIMIZATION_SUCCESSFUL"

    # Hosting Capacity with WeatherNext
    w2 = orchestrator.run_workflow("hosting_capacity", feeder_id="F-NORTH-08")
    assert w2["status"] == "STUDY_COMPLETED"

    # Dynamic Line Rating with WeatherNext
    w3 = orchestrator.run_workflow("dynamic_line_rating", corridor_id="LINE-NORTH-230")
    assert w3["status"] == "CONGESTION_RELIEVED"

    # FLISR with Topological Reconfiguration & Mandatory HITL
    w4 = orchestrator.run_workflow("flisr_restoration", faulted_feeder="F-102")
    assert w4["requires_hitl_approval"] is True
    ticket_id = w4["hitl_ticket_id"]

    # Review HITL ticket (Approve)
    review_res = orchestrator.review_hitl_ticket(
        ticket_id=ticket_id,
        approve=True,
        operator_id="OPERATOR-7741",
        notes="Dual-operator field authorization granted."
    )
    assert review_res["status"] == "SUCCESS"
    assert review_res["ticket"]["status"] == "APPROVED"

    # Predictive Maintenance Workflow
    w5 = orchestrator.run_workflow("predictive_maintenance", asset_id="XFMR-SUB-44")
    assert w5["status"] == "FIELD_WORK_ORDER_DISPATCHED"

    # VPP Market Dispatch Workflow
    w6 = orchestrator.run_workflow("vpp_market_dispatch", vpp_id="VPP-METRO-01")
    assert w6["dispatched_capacity_mw"] > 0


def test_fastapi_fleet_and_step_endpoints():
    from fastapi.testclient import TestClient
    from grid_optimization.fast_api_app import app

    client = TestClient(app)

    # Health check
    res_health = client.get("/healthz")
    assert res_health.status_code == 200
    assert res_health.json()["status"] == "ok"

    # Fleet endpoint
    res_fleet = client.get("/api/fleet")
    assert res_fleet.status_code == 200
    assert res_fleet.json()["persona_count"] == 8

    # Test all 6 workflows, all 4 steps each
    workflows = ["flisr", "vvo", "pdm", "dlr", "hosting", "vpp"]
    for wf in workflows:
        for step_idx in range(4):
            res_step = client.post(
                "/api/workflow/step",
                json={
                    "workflow_key": wf,
                    "step_index": step_idx,
                    "parameters": {"feeder_id": "FEEDER-TEST-01", "voltage_pu": 0.96},
                    "custom_prompt": "Verify voltage headroom and thermal rating"
                }
            )
            assert res_step.status_code == 200
            data = res_step.json()
            assert data["status"] == "SUCCESS", f"Failed for {wf} step {step_idx}: {data}"
            assert data["workflow_key"] == wf
            assert data["step_index"] == step_idx
            assert "persona_name" in data
            assert len(data["tools_invoked"]) > 0

    # Persona interaction endpoint
    res_interact = client.post(
        "/api/persona/interact",
        json={
            "persona_id": "grid_dispatcher_agent",
            "task_name": "MONITOR_AND_DISPATCH",
            "prompt": "Evaluate voltage sag on West Feeder",
            "payload": {"feeder_id": "WEST-01"}
        }
    )
    assert res_interact.status_code == 200
    assert res_interact.json()["status"] == "SUCCESS"

