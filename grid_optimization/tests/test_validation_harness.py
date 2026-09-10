import pytest
from grid_optimization.safety.validation_harness import ValidationHarness, SafetyBounds

def test_validation_harness_voltage_ansi():
    harness = ValidationHarness()
    # Safe voltage
    res_safe = harness.validate_input_telemetry({"voltage_pu": 1.01, "frequency_hz": 60.0, "loading_pct": 72.0})
    assert res_safe.is_valid is True
    assert res_safe.risk_level == "SAFE"

    # Undervoltage ANSI violation (< 0.95)
    res_under = harness.validate_input_telemetry({"voltage_pu": 0.93, "frequency_hz": 60.0})
    assert res_under.is_valid is False
    assert res_under.risk_level == "CRITICAL_VIOLATION"
    assert any("undervoltage" in v.lower() for v in res_under.violations)

    # Overvoltage ANSI violation (> 1.05)
    res_over = harness.validate_input_telemetry({"voltage_pu": 1.07})
    assert res_over.is_valid is False
    assert any("overvoltage" in v.lower() for v in res_over.violations)

def test_validation_harness_thermal_and_frequency():
    harness = ValidationHarness()
    # Thermal overload
    res_thermal = harness.validate_input_telemetry({"voltage_pu": 1.0, "loading_pct": 112.5})
    assert res_thermal.is_valid is False
    assert any("thermal overload" in v.lower() for v in res_thermal.violations)

    # Frequency excursion
    res_freq = harness.validate_input_telemetry({"voltage_pu": 1.0, "frequency_hz": 59.70})
    assert res_freq.is_valid is False
    assert any("frequency" in v.lower() for v in res_freq.violations)

def test_validation_harness_plan_anti_islanding():
    harness = ValidationHarness()
    # Plan with backfeed violation
    plan = {
        "action_type": "SWITCHING_ORDER",
        "projected_voltage_pu": 1.01,
        "is_backfeed_isolated": False
    }
    res = harness.validate_proposed_plan(plan, current_state={})
    assert res.is_valid is False
    assert any("anti-islanding" in v.lower() for v in res.violations)
