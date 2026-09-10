import pytest
from grid_optimization.advanced_engines.weathernext_engine import WeatherNextEngine
from grid_optimization.advanced_engines.vizier_optimizer import VizierOptimizer
from grid_optimization.advanced_engines.pdm_engine import PredictiveMaintenanceEngine

def test_weathernext_engine():
    wx = WeatherNextEngine()
    fc = wx.get_forecast("Substation-North")
    assert fc.solar_ghi_wm2 >= 0.0
    assert fc.ambient_temp_c > -50.0
    assert fc.wind_speed_10m_ms >= 0.0
    assert fc.convective_storm_risk in ["LOW", "MODERATE", "SEVERE", "EXTREME"]

    dlr = wx.compute_dlr_microclimate("SPAN-230-01")
    assert dlr["effective_crosswind_ms"] >= 0.5
    assert dlr["convective_cooling_factor"] >= 1.0

def test_vizier_optimizer():
    opt = VizierOptimizer()
    # Volt-VAR curve optimization
    vvo_res = opt.optimize_volt_var_curves("F-101", baseline_loss_mw=3.0)
    assert vvo_res.objective_value < 3.0
    assert "v1_pu" in vvo_res.best_parameters
    assert vvo_res.constraint_violations == 0

    # BESS arbitrage vs degradation
    bess_res = opt.optimize_bess_arbitrage_envelope("BESS-01", rated_capacity_mwh=40.0)
    assert bess_res.objective_value > 0.0
    assert bess_res.best_parameters["min_soc_pct"] >= 15.0

def test_pdm_engine():
    pdm = PredictiveMaintenanceEngine()
    # DGA with high ethylene -> T3 thermal fault
    dga_t3 = pdm.diagnose_transformer_dga("XFMR-01", ch4_ppm=80.0, c2h4_ppm=180.0, c2h2_ppm=2.0)
    assert "T3" in dga_t3.fault_classification
    assert dga_t3.severity_level == "ALARM"

    # DGA with high acetylene -> D2 arcing
    dga_d2 = pdm.diagnose_transformer_dga("XFMR-02", ch4_ppm=20.0, c2h4_ppm=60.0, c2h2_ppm=80.0)
    assert "D2" in dga_d2.fault_classification
    assert dga_d2.severity_level == "CRITICAL"

    # Circuit breaker wear
    cb = pdm.evaluate_circuit_breaker_wear("CB-01", cumulative_fault_mva_interrupted=12500.0, rated_interrupting_mva=25000.0)
    assert cb.cumulative_i2t_wear_pct == 50.0
    assert cb.health_index_pct > 0.0

    # Asset health dossier & RPN
    dossier = pdm.build_asset_health_dossier("XFMR-01", "TRANSFORMER", "Sub-01", {"ch4_ppm": 80.0, "c2h4_ppm": 180.0, "c2h2_ppm": 2.0})
    assert dossier.risk_priority_number > 0
    assert dossier.work_order_required is True
