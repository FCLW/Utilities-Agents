"""Collaborative Workflow: VPP Market Dispatch with WeatherNext & Vizier."""
from typing import Dict, Any
from grid_optimization.personas.derms_manager import DermsManagerPersona
from grid_optimization.personas.regulatory_compliance_officer import RegulatoryComplianceOfficerPersona
from grid_optimization.personas.grid_dispatcher import GridDispatcherPersona

class VppMarketDispatchWorkflow:
    def __init__(self):
        self.derms = DermsManagerPersona()
        self.regulatory = RegulatoryComplianceOfficerPersona()
        self.dispatcher = GridDispatcherPersona()

    def run(self, vpp_id: str = "VPP-METRO-01", substation: str = "Sub-Metro") -> Dict[str, Any]:
        derms_out = self.derms.execute_task("OPTIMIZE_VPP_SCHEDULE", {
            "vpp_id": vpp_id,
            "substation": substation
        })

        return {
            "workflow_name": "Virtual Power Plant (VPP) Market Dispatch with WeatherNext & Vizier",
            "vpp_id": vpp_id,
            "substation": substation,
            "dispatched_capacity_mw": derms_out["results"]["vpp"]["aggregated_bess_mw"] + derms_out["results"]["vpp"]["aggregated_pv_mw"],
            "daily_net_arbitrage_profit_usd": derms_out["results"]["vizier_bess"]["daily_net_profit_usd"],
            "approval_status": derms_out["status"]
        }
