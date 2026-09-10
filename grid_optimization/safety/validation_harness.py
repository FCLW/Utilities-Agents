"""Validation Harness and Physical Feasibility Guardrails for Grid Optimization Agents."""
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
import math

@dataclass
class SafetyBounds:
    min_voltage_pu: float = 0.95      # ANSI C84.1 Range A lower bound
    max_voltage_pu: float = 1.05      # ANSI C84.1 Range A upper bound
    max_line_loading_pct: float = 100.0  # Max thermal conductor rating %
    max_transformer_loading_pct: float = 105.0 # Max emergency transformer loading %
    min_bess_soc_pct: float = 15.0    # Minimum state-of-charge buffer
    max_bess_soc_pct: float = 95.0    # Maximum state-of-charge upper limit
    max_frequency_dev_hz: float = 0.2  # Max acceptable frequency deviation from 60Hz
    max_baseline_drift_pct: float = 10.0 # Anti-hallucination baseline drift limit

@dataclass
class ValidationResult:
    is_valid: bool
    risk_level: str  # "SAFE", "WARNING", "CRITICAL_VIOLATION"
    violations: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    safety_margins: Dict[str, float] = field(default_factory=dict)
    grounded_evidence: Dict[str, Any] = field(default_factory=dict)

    @property
    def is_safe(self) -> bool:
        return self.is_valid

    @property
    def metrics(self) -> Dict[str, float]:
        return self.safety_margins

class ValidationHarness:
    """Rigorous pre- and post-execution guardrail validator for all grid actions."""

    def __init__(self, bounds: Optional[SafetyBounds] = None):
        self.bounds = bounds or SafetyBounds()

    def validate_input_telemetry(self, telemetry: Dict[str, Any]) -> ValidationResult:
        """Pre-execution validation: checks data plausibility and boundary constraints."""
        violations = []
        warnings = []
        margins = {}

        # 1. Voltage validation
        voltage_pu = telemetry.get("voltage_pu")
        if voltage_pu is not None:
            if not isinstance(voltage_pu, (int, float)) or math.isnan(voltage_pu):
                violations.append("Voltage value is non-numeric or NaN")
            elif voltage_pu < 0.5 or voltage_pu > 1.5:
                violations.append(f"Physical plausibility failure: voltage_pu={voltage_pu} outside [0.5, 1.5]")
            else:
                margin_low = voltage_pu - self.bounds.min_voltage_pu
                margin_high = self.bounds.max_voltage_pu - voltage_pu
                margins["voltage_min_margin_pu"] = round(margin_low, 4)
                margins["voltage_max_margin_pu"] = round(margin_high, 4)
                if voltage_pu < self.bounds.min_voltage_pu:
                    violations.append(f"ANSI C84.1 undervoltage violation: {voltage_pu:.3f} p.u. < {self.bounds.min_voltage_pu}")
                elif voltage_pu > self.bounds.max_voltage_pu:
                    violations.append(f"ANSI C84.1 overvoltage violation: {voltage_pu:.3f} p.u. > {self.bounds.max_voltage_pu}")

        # 2. Line loading validation
        loading_pct = telemetry.get("loading_pct")
        if loading_pct is not None:
            margins["thermal_headroom_pct"] = round(self.bounds.max_line_loading_pct - loading_pct, 2)
            if loading_pct > self.bounds.max_line_loading_pct:
                violations.append(f"Thermal overload violation: {loading_pct:.1f}% exceeds 100% MVA rating")
            elif loading_pct > 90.0:
                warnings.append(f"Thermal warning: feeder at {loading_pct:.1f}% capacity (>90% threshold)")

        # 3. Frequency validation
        frequency_hz = telemetry.get("frequency_hz")
        if frequency_hz is not None:
            freq_dev = abs(frequency_hz - 60.0)
            margins["frequency_dev_hz"] = round(freq_dev, 4)
            if freq_dev > self.bounds.max_frequency_dev_hz:
                violations.append(f"NERC BAL-001 frequency deviation: {frequency_hz:.2f} Hz exceeds ±0.2 Hz tolerance")

        is_valid = len(violations) == 0
        risk_level = "CRITICAL_VIOLATION" if violations else ("WARNING" if warnings else "SAFE")

        return ValidationResult(
            is_valid=is_valid,
            risk_level=risk_level,
            violations=violations,
            warnings=warnings,
            safety_margins=margins,
            grounded_evidence={"input_checked": list(telemetry.keys())}
        )

    def validate_proposed_plan(self, action_plan: Dict[str, Any], current_state: Dict[str, Any]) -> ValidationResult:
        """Post-execution validation: validates simulated plan consequences before execution."""
        violations = []
        warnings = []
        margins = {}

        # 1. Projected voltage check
        projected_v = action_plan.get("projected_voltage_pu")
        if projected_v is not None:
            if projected_v < self.bounds.min_voltage_pu or projected_v > self.bounds.max_voltage_pu:
                violations.append(
                    f"Plan violates ANSI C84.1: projected voltage {projected_v:.3f} p.u. outside "
                    f"[{self.bounds.min_voltage_pu}, {self.bounds.max_voltage_pu}]"
                )
            margins["projected_voltage_pu"] = projected_v

        # 2. Projected thermal line loading check
        projected_loading = action_plan.get("projected_loading_pct")
        if projected_loading is not None:
            if projected_loading > self.bounds.max_line_loading_pct:
                violations.append(
                    f"Plan induces thermal violation: projected line loading {projected_loading:.1f}% > 100% MVA"
                )
            margins["projected_thermal_headroom_pct"] = round(self.bounds.max_line_loading_pct - projected_loading, 2)

        # 3. Interlocking & Anti-Islanding IEEE 1547 verification
        if action_plan.get("action_type") in ["SWITCHING_ORDER", "FLISR_RESTORATION", "BREAKER_TOGGLE"]:
            is_backfeed_isolated = action_plan.get("is_backfeed_isolated", True)
            if not is_backfeed_isolated:
                violations.append("IEEE 1547 anti-islanding failure: unisolated DER backfeed detected on isolated zone")

            zero_energy_verified = action_plan.get("zero_energy_verified", False)
            if action_plan.get("requires_clearance") and not zero_energy_verified:
                violations.append("Safety lock-out failure: zero-energy state not verified prior to close clearance")

        # 4. Anti-hallucination baseline grounding check
        baseline_diff_pct = action_plan.get("baseline_drift_pct", 0.0)
        if baseline_diff_pct > self.bounds.max_baseline_drift_pct:
            warnings.append(
                f"Statistical drift warning: projected metric differs by {baseline_diff_pct:.1f}% from BigQuery historical baseline"
            )

        is_valid = len(violations) == 0
        risk_level = "CRITICAL_VIOLATION" if violations else ("WARNING" if warnings else "SAFE")

        return ValidationResult(
            is_valid=is_valid,
            risk_level=risk_level,
            violations=violations,
            warnings=warnings,
            safety_margins=margins,
            grounded_evidence={"action_type": action_plan.get("action_type")}
        )

    def validate_pre_execution(self, action_plan: Dict[str, Any], telemetry: Dict[str, Any]) -> ValidationResult:
        """Combined pre-execution validation checking physical telemetry and action plan limits."""
        res_telemetry = self.validate_input_telemetry(telemetry)
        res_plan = self.validate_proposed_plan(action_plan, telemetry)

        all_violations = list(res_telemetry.violations) + [
            v for v in res_plan.violations if v not in res_telemetry.violations
        ]
        all_warnings = list(res_telemetry.warnings) + [
            w for w in res_plan.warnings if w not in res_telemetry.warnings
        ]
        margins = {**res_telemetry.safety_margins, **res_plan.safety_margins}

        # Check reverse power if provided
        rev_kw = telemetry.get("reverse_power_kw", 0.0)
        if rev_kw > 500.0:
            all_violations.append(f"Reverse power threshold violation: {rev_kw} kW > 500.0 kW limit")

        # Check anti-islanding certification
        if not telemetry.get("anti_islanding_certified", True):
            all_violations.append("IEEE 1547 anti-islanding interlock certification not active")

        is_valid = len(all_violations) == 0
        risk_level = "CRITICAL_VIOLATION" if all_violations else ("WARNING" if all_warnings else "SAFE")

        return ValidationResult(
            is_valid=is_valid,
            risk_level=risk_level,
            violations=all_violations,
            warnings=all_warnings,
            safety_margins=margins,
            grounded_evidence={"action_type": action_plan.get("action_type")}
        )
