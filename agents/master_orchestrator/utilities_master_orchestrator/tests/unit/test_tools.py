import pytest
from pathlib import Path
import sys

# Ensure repository root is on sys.path
repo_root = Path(__file__).resolve().parents[5]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from agents.master_orchestrator.utilities_master_orchestrator.agent import agent
from agents.master_orchestrator.utilities_master_orchestrator.tools.bigquery_tool import BigQueryQueryTool
from agents.master_orchestrator.utilities_master_orchestrator.tools.delegation_tool import AgentDelegationTool

def test_orchestrator_has_no_bigquery_access():
    """Verify Master Orchestrator raises PermissionError on any direct BigQuery query attempt."""
    bq_tool = BigQueryQueryTool()
    with pytest.raises(PermissionError) as exc_info:
        bq_tool.run("SELECT * FROM utilities_asset_management.capital_replacement_simulator_logs")
    assert "Master Orchestrator does not have direct access to BigQuery" in str(exc_info.value)
    assert "delegate" in str(exc_info.value)

def test_orchestrator_tools_configuration():
    """Verify Master Orchestrator agent does not include BigQuery tool and includes AgentDelegationTool."""
    tool_names = [getattr(t, "name", type(t).__name__) for t in agent.tools]
    assert "BigQueryQueryTool" not in tool_names, "Master Orchestrator must NOT have BigQueryQueryTool in its active tools!"
    assert "AgentDelegationTool" in tool_names, "Master Orchestrator MUST have AgentDelegationTool to route to domain agents!"

def test_delegation_tool_discovery():
    """Verify AgentDelegationTool discovers registered domain agents."""
    delegation_tool = AgentDelegationTool()
    found = delegation_tool._find_agent_module("capital_replacement_simulator")
    assert found is not None
    domain, name, mod = found
    assert domain == "asset_management"
    assert name == "capital_replacement_simulator"
