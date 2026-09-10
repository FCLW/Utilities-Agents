import pytest
from grid_optimization.skills import (
    WeatherNextTelemetryCorrelatorSkill,
    VizierBayesianVvoTunerSkill,
    TopologicalFlisrReconfiguratorSkill,
    PredictiveMaintenanceHealthScorerSkill,
    PowerFlowSimulationSkill,
    ContingencyConstraintCheckerSkill,
    HostingCapacityEvaluatorSkill,
    DynamicLineRatingCalculatorSkill,
    AutomatedSwitchingPlannerSkill,
    DerVppCoOptimizerSkill,
    ScadaAmiAnomalyDetectorSkill,
    RegulatoryAuditReporterSkill
)

def test_all_12_skills():
    # 1. WeatherNext correlator
    s1 = WeatherNextTelemetryCorrelatorSkill().execute("Sub-North")
    assert "ambient_temp_c" in s1

    # 2. Vizier VVO tuner
    s2 = VizierBayesianVvoTunerSkill().execute("F-101")
    assert s2["loss_reduction_pct"] > 0

    # 3. Topological FLISR reconfigurator
    s3 = TopologicalFlisrReconfiguratorSkill().execute("Sub-Metro")
    assert s3["optimal_loss_mw"] < s3["baseline_loss_mw"]

    # 4. PdM health scorer
    s4 = PredictiveMaintenanceHealthScorerSkill().execute("XFMR-01", "TRANSFORMER", "Sub-1", {"ch4_ppm": 90.0, "c2h4_ppm": 170.0, "c2h2_ppm": 1.0})
    assert s4["risk_priority_number"] > 0

    # 5. Power flow
    s5 = PowerFlowSimulationSkill().execute()
    assert s5["convergence_status"] == "CONVERGED_4_ITERATIONS"

    # 6. Constraint checker
    s6 = ContingencyConstraintCheckerSkill().execute({"voltage_pu": 1.01, "frequency_hz": 60.0})
    assert s6["is_valid"] is True

    # 7. Hosting capacity
    s7 = HostingCapacityEvaluatorSkill().execute("F-101", "Sub-1")
    assert s7["max_hosting_capacity_mw"] > 0

    # 8. Dynamic line rating
    s8 = DynamicLineRatingCalculatorSkill().execute("LINE-01")
    assert s8["dynamic_rating_amps"] > 0

    # 9. Automated switching planner
    s9 = AutomatedSwitchingPlannerSkill().execute("ZONE-A")
    assert s9["switching_steps_count"] > 0

    # 10. DER VPP co-optimizer
    s10 = DerVppCoOptimizerSkill().execute("VPP-01")
    assert s10["hourly_market_revenue_usd"] > 0

    # 11. SCADA anomaly detector
    s11 = ScadaAmiAnomalyDetectorSkill().execute([1.0, 1.01, 1.0, 0.75, 1.0])
    assert s11["anomalies_detected"] >= 1

    # 12. Regulatory audit reporter
    s12 = RegulatoryAuditReporterSkill().execute()
    assert s12["compliance_status"] == "COMPLIANT"
