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
