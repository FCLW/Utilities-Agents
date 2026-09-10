import pytest
from grid_optimization.safety.hitl_gateway import HITLGateway, ActionRiskTier, ApprovalStatus

def test_hitl_risk_tier_classification():
    hitl = HITLGateway()

    # Tier 1: Read-only / monitoring
    t1 = hitl.evaluate_and_ticket(
        requesting_agent="grid_dispatcher_agent",
        target_substation="Sub-01",
        target_feeder="F-10",
        target_equipment="METRIC_READER",
        action_type="STATE_ESTIMATION_RUN",
        proposed_command="RUN_WLS",
        safety_dossier={}
    )
    assert t1.risk_tier == ActionRiskTier.TIER_1_AUTONOMOUS
    assert t1.status == ApprovalStatus.AUTO_APPROVED

    # Tier 2: Advisory / curve update
    t2 = hitl.evaluate_and_ticket(
        requesting_agent="derms_manager_agent",
        target_substation="Sub-01",
        target_feeder="F-10",
        target_equipment="INVERTER_CLUSTER",
        action_type="INVERTER_CURVE_UPDATE",
        proposed_command="UPDATE_VVO_CURVE",
        safety_dossier={}
    )
    assert t2.risk_tier == ActionRiskTier.TIER_2_ADVISORY
    assert t2.status == ApprovalStatus.PENDING_APPROVAL

    # Tier 3: Physical change / breaker toggle
    t3 = hitl.evaluate_and_ticket(
        requesting_agent="grid_dispatcher_agent",
        target_substation="Sub-01",
        target_feeder="F-10",
        target_equipment="CB-101",
        action_type="BREAKER_TOGGLE",
        proposed_command="OPEN CB-101",
        safety_dossier={"pre_voltage": 0.94}
    )
    assert t3.risk_tier == ActionRiskTier.TIER_3_PHYSICAL_CHANGE
    assert t3.status == ApprovalStatus.PENDING_APPROVAL

def test_hitl_approval_and_rejection():
    hitl = HITLGateway()
    ticket = hitl.evaluate_and_ticket(
        requesting_agent="grid_dispatcher_agent",
        target_substation="Sub-Metro",
        target_feeder="F-102",
        target_equipment="SW-TIE-44",
        action_type="SWITCHING_ORDER",
        proposed_command="CLOSE SW-TIE-44",
        safety_dossier={}
    )

    # Approve
    approved = hitl.approve_ticket(
        ticket.ticket_id,
        operator_id="OPERATOR-8812",
        operator_role="Senior Grid Controller",
        justification_notes="Verified load transfer capacity."
    )
    assert approved.status == ApprovalStatus.APPROVED
    assert approved.operator_id == "OPERATOR-8812"

    # Verify audit trail
    audit = hitl.get_audit_trail()
    assert len(audit) >= 2
    assert any(a["event_type"] == "OPERATOR_APPROVED" for a in audit)
