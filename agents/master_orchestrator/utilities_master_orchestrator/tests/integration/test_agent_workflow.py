import sys
from pathlib import Path
import importlib
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
import types

repo_root = Path(__file__).resolve().parents[5]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from agents.master_orchestrator.utilities_master_orchestrator.agent import workflow_router, agent
from config.session_state import UtilitiesSessionState

@pytest.mark.asyncio
async def test_a2a_orchestrator_critic_workflow(monkeypatch):
    class MockResponse:
        def __init__(self, content):
            self.content = content

    mock_exec = MagicMock(return_value=MockResponse("Dispatched request to grid balancing agent. Asset transformer T-42 is at 95% load."))
    mock_critic = MagicMock(return_value=MockResponse("| Asset | Load | Status |\n|---|---|---|\n| T-42 | 95% | Critical |"))

    orchestrator_mod = sys.modules["agents.master_orchestrator.utilities_master_orchestrator.agent"]
    monkeypatch.setattr(orchestrator_mod, "execution_agent", mock_exec)
    monkeypatch.setattr(orchestrator_mod, "critic_agent", mock_critic)

    result = await workflow_router("Analyze transformer load in zone 3")
    mock_exec.assert_called_once()
    mock_critic.assert_called_once()
    assert result == "| Asset | Load | Status |\n|---|---|---|\n| T-42 | 95% | Critical |"

def test_session_state_schema():
    state = UtilitiesSessionState(
        customer_id="CUST-1001",
        grid_zone_id="ZONE-NORTH",
        operating_mode="Emergency",
        active_alert_level="HIGH"
    )
    assert state.customer_id == "CUST-1001"
    assert state.operating_mode == "Emergency"
    assert state.active_alert_level == "HIGH"
