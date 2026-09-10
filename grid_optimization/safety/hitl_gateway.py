"""Human-In-The-Loop (HITL) 3-Tier Approval Gateway and Safety Governance."""
import uuid
import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

class ActionRiskTier(str, Enum):
    TIER_1_AUTONOMOUS = "TIER_1_AUTONOMOUS"          # Read-only, forecasting, monitoring
    TIER_2_ADVISORY = "TIER_2_ADVISORY"              # Parametric tuning within pre-approved bounds
    TIER_3_PHYSICAL_CHANGE = "TIER_3_PHYSICAL_CHANGE"# Physical switching, breaker toggle, curtailment

class ApprovalStatus(str, Enum):
    AUTO_APPROVED = "AUTO_APPROVED"
    PENDING_APPROVAL = "PENDING_APPROVAL"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ROLLED_BACK = "ROLLED_BACK"

@dataclass
class ApprovalTicket:
    ticket_id: str
    risk_tier: ActionRiskTier
    requesting_agent: str
    target_substation: str
    target_feeder: str
    target_equipment: str
    action_type: str
    proposed_command: str
    safety_dossier: Dict[str, Any]
    status: ApprovalStatus
    created_at: str
    reviewed_at: Optional[str] = None
    operator_id: Optional[str] = None
    operator_role: Optional[str] = None
    justification_notes: Optional[str] = None
    rollback_command: Optional[str] = None

class HITLGateway:
    """Enterprise Human-In-The-Loop gateway enforcing operator authorization for grid changes."""

    def __init__(self):
        self._tickets: Dict[str, ApprovalTicket] = {}
        self._audit_trail: List[Dict[str, Any]] = []

    def evaluate_and_ticket(
        self,
        requesting_agent: str,
        target_substation: str,
        target_feeder: str,
        target_equipment: str,
        action_type: str,
        proposed_command: str,
        safety_dossier: Dict[str, Any],
        rollback_command: Optional[str] = None,
    ) -> ApprovalTicket:
        """Classifies action risk tier and creates an approval ticket."""
        ticket_id = f"TICK-{uuid.uuid4().hex[:8].upper()}"
        now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

        # Classify Risk Tier
        tier_3_actions = {
            "BREAKER_TOGGLE", "SWITCHING_ORDER", "FLISR_RESTORATION",
            "CAPACITOR_SWITCH", "RELAY_SETTING_UPDATE", "FEEDER_CURTAILMENT",
            "BLACK_START_CRANK", "SUBSTATION_ISOLATION"
        }
        tier_2_actions = {
            "INVERTER_CURVE_UPDATE", "BESS_SCHEDULE_SHIFT", "TAP_CHANGER_BIAS",
            "DEMAND_RESPONSE_ALERT", "DYNAMIC_LINE_RATING_UPDATE"
        }

        if action_type in tier_3_actions:
            tier = ActionRiskTier.TIER_3_PHYSICAL_CHANGE
            status = ApprovalStatus.PENDING_APPROVAL
        elif action_type in tier_2_actions:
            tier = ActionRiskTier.TIER_2_ADVISORY
            status = ApprovalStatus.PENDING_APPROVAL
        else:
            tier = ActionRiskTier.TIER_1_AUTONOMOUS
            status = ApprovalStatus.AUTO_APPROVED

        ticket = ApprovalTicket(
            ticket_id=ticket_id,
            risk_tier=tier,
            requesting_agent=requesting_agent,
            target_substation=target_substation,
            target_feeder=target_feeder,
            target_equipment=target_equipment,
            action_type=action_type,
            proposed_command=proposed_command,
            safety_dossier=safety_dossier,
            status=status,
            created_at=now_iso,
            rollback_command=rollback_command
        )

        self._tickets[ticket_id] = ticket
        self._log_audit(ticket, "TICKET_CREATED", "Automated classification based on action risk tier")
        return ticket

    def approve_ticket(
        self,
        ticket_id: str,
        operator_id: str,
        operator_role: str,
        justification_notes: str
    ) -> ApprovalTicket:
        """Applies human approval to a pending change ticket."""
        if ticket_id not in self._tickets:
            raise ValueError(f"Approval ticket {ticket_id} not found")

        ticket = self._tickets[ticket_id]
        if ticket.status != ApprovalStatus.PENDING_APPROVAL:
            raise ValueError(f"Ticket {ticket_id} is in status {ticket.status}, cannot approve")

        # In production, Tier 3 could verify dual-operator authorization
        ticket.status = ApprovalStatus.APPROVED
        ticket.reviewed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        ticket.operator_id = operator_id
        ticket.operator_role = operator_role
        ticket.justification_notes = justification_notes

        self._log_audit(ticket, "OPERATOR_APPROVED", f"Signed off by {operator_id} ({operator_role}): {justification_notes}")
        return ticket

    def reject_ticket(
        self,
        ticket_id: str,
        operator_id: str,
        rejection_reason: str
    ) -> ApprovalTicket:
        """Rejects a pending change ticket, keeping grid state unaltered."""
        if ticket_id not in self._tickets:
            raise ValueError(f"Approval ticket {ticket_id} not found")

        ticket = self._tickets[ticket_id]
        ticket.status = ApprovalStatus.REJECTED
        ticket.reviewed_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
        ticket.operator_id = operator_id
        ticket.justification_notes = f"REJECTED: {rejection_reason}"

        self._log_audit(ticket, "OPERATOR_REJECTED", rejection_reason)
        return ticket

    def get_pending_tickets(self) -> List[ApprovalTicket]:
        """Returns all tickets currently awaiting human operator action."""
        return [t for t in self._tickets.values() if t.status == ApprovalStatus.PENDING_APPROVAL]

    def get_ticket(self, ticket_id: str) -> Optional[ApprovalTicket]:
        return self._tickets.get(ticket_id)

    def get_audit_trail(self) -> List[Dict[str, Any]]:
        return list(self._audit_trail)

    def _log_audit(self, ticket: ApprovalTicket, event_type: str, details: str):
        self._audit_trail.append({
            "audit_id": f"AUD-{uuid.uuid4().hex[:6].upper()}",
            "ticket_id": ticket.ticket_id,
            "event_type": event_type,
            "risk_tier": ticket.risk_tier.value,
            "action_type": ticket.action_type,
            "substation": ticket.target_substation,
            "equipment": ticket.target_equipment,
            "status": ticket.status.value,
            "operator_id": ticket.operator_id or "SYSTEM_AUTO",
            "details": details,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        })
