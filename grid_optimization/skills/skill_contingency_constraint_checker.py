"""Skill: ANSI C84.1, Thermal Ampacity, and NERC Contingency Constraint Checker."""
from typing import Dict, List, Any
from grid_optimization.safety.validation_harness import ValidationHarness

class ContingencyConstraintCheckerSkill:
    """Reusable skill: Enforces voltage, thermal, and frequency safety envelopes."""

    def __init__(self, harness: ValidationHarness = None):
        self.harness = harness or ValidationHarness()

    def execute(self, telemetry_or_plan: Dict[str, Any], is_plan: bool = False) -> Dict[str, Any]:
        if is_plan:
            res = self.harness.validate_proposed_plan(telemetry_or_plan, current_state={})
        else:
            res = self.harness.validate_input_telemetry(telemetry_or_plan)

        return {
            "skill": "skill_contingency_constraint_checker",
            "is_valid": res.is_valid,
            "risk_level": res.risk_level,
            "violations": res.violations,
            "warnings": res.warnings,
            "safety_margins": res.safety_margins
        }
