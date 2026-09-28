import os
import json
import yaml
import pytest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

@pytest.fixture(autouse=True)
def mock_bigquery_env(monkeypatch):
    """Enables mock BigQuery mode to test table authorization logic deterministically without live GCP tokens."""
    monkeypatch.setenv("MOCK_BIGQUERY", "true")
    monkeypatch.setenv("IDENTITY_TYPE", "AGENT_IDENTITY")

def test_orchestrator_agent_tools_configuration():
    """Verify Master Orchestrator agent has no BigQueryQueryTool in tools and has AgentDelegationTool."""
    from agents.master_orchestrator.utilities_master_orchestrator.agent import agent as orch_agent
    tool_names = [getattr(t, "name", type(t).__name__) for t in orch_agent.tools]
    assert "BigQueryQueryTool" not in tool_names, "Master Orchestrator should not have direct BigQueryQueryTool in active tools"
    assert "AgentDelegationTool" in tool_names, "Master Orchestrator must have AgentDelegationTool for A2A routing"

def test_orchestrator_bigquery_direct_access_denied():
    """Verify Master Orchestrator BigQueryQueryTool strictly denies execution with Access Denied message."""
    from agents.master_orchestrator.utilities_master_orchestrator.tools.bigquery_tool import BigQueryQueryTool
    orch_bq = BigQueryQueryTool()
    assert orch_bq.is_orchestrator is True
    assert orch_bq.get_effective_identity() == "principal://master-orchestrator-no-direct-bq-access"
    
    result = orch_bq.run("SELECT * FROM utilities_asset_management.capital_replacement_simulator_logs")
    assert "Access denied: The Master Orchestrator operates under least-privilege Agent Identity and does not have direct access to BigQuery" in result
    assert "AgentDelegationTool" in result

def test_orchestrator_registry_has_no_bigquery_datasets():
    """Verify table_registry.yaml defines 0 BigQuery datasets for utilities_master_orchestrator."""
    reg_file = REPO_ROOT / "table_registry.yaml"
    assert reg_file.exists(), "table_registry.yaml missing"
    with open(reg_file, "r") as f:
        data = yaml.safe_load(f).get("agents", {})
    orch_entry = data.get("utilities_master_orchestrator", {})
    datasets = orch_entry.get("datasets", [])
    assert datasets == [] or datasets is None, f"Orchestrator must have no datasets assigned, found {datasets}"

@pytest.mark.parametrize("domain,agent_name", [
    ("asset_management", "capital_replacement_simulator"),
    ("asset_management", "circuit_breaker_wear_analyzer"),
    ("billing_and_invoicing", "budget_billing_levelization_calculator"),
    ("grid_balancing", "battery_storage_discharge_optimizer"),
])
def test_domain_agents_can_query_authorized_tables(domain, agent_name):
    """Verify domain agents can query their own assigned tables and datasets."""
    from agents.asset_management.capital_replacement_simulator.tools.bigquery_tool import BigQueryQueryTool
    tool = BigQueryQueryTool(agent_name=agent_name, domain_name=domain)
    assert f"{agent_name}_logs" in tool.allowed_tables
    
    # Authorized queries
    result = tool.run(f"SELECT * FROM {agent_name}_logs LIMIT 5")
    assert "Query executed successfully" in result

    result_dataset = tool.run(f"SELECT * FROM utilities_{domain}.{agent_name}_data LIMIT 5")
    assert "Query executed successfully" in result_dataset

def test_domain_agent_cross_agent_table_access_blocked():
    """Verify domain agents are strictly blocked from querying other agents' tables within the same domain."""
    from agents.asset_management.capital_replacement_simulator.tools.bigquery_tool import BigQueryQueryTool
    tool = BigQueryQueryTool(agent_name="capital_replacement_simulator")
    
    # Attempting to access another asset management agent's table
    res = tool.run("SELECT * FROM utilities_asset_management.circuit_breaker_wear_analyzer_logs LIMIT 5")
    assert "Access denied: Agent 'capital_replacement_simulator' is not authorized to access table 'circuit_breaker_wear_analyzer_logs'" in res

def test_domain_agent_cross_domain_dataset_access_blocked():
    """Verify domain agents are strictly blocked from querying datasets belonging to other operational domains."""
    from agents.asset_management.capital_replacement_simulator.tools.bigquery_tool import BigQueryQueryTool
    tool = BigQueryQueryTool(agent_name="capital_replacement_simulator")
    
    # Attempting to access billing dataset
    res = tool.run("SELECT * FROM utilities_billing_and_invoicing.budget_billing_levelization_calculator_logs LIMIT 5")
    assert "Access denied: Agent 'capital_replacement_simulator' is not authorized to access table 'budget_billing_levelization_calculator_logs'" in res

def test_domain_agent_mutative_sql_guardrail():
    """Verify SQL safety guardrails reject mutative statements before table checks."""
    from agents.asset_management.capital_replacement_simulator.tools.bigquery_tool import BigQueryQueryTool
    tool = BigQueryQueryTool(agent_name="capital_replacement_simulator")
    
    mutative_queries = [
        "DROP TABLE capital_replacement_simulator_logs",
        "DELETE FROM capital_replacement_simulator_logs WHERE id = 1",
        "TRUNCATE TABLE capital_replacement_simulator_logs",
        "ALTER TABLE capital_replacement_simulator_logs ADD COLUMN extra STRING",
        "INSERT INTO capital_replacement_simulator_logs VALUES ('1')",
        "UPDATE capital_replacement_simulator_logs SET status = 'Inactive'"
    ]
    for q in mutative_queries:
        res = tool.run(q)
        assert "Query rejected" in res or "Mutative or administrative statements are prohibited" in res

def test_all_agent_packages_have_agent_identity_config():
    """Verify all 113 agents in agents/ have .agent_engine_config.json with identity_type=AGENT_IDENTITY."""
    agents_dir = REPO_ROOT / "agents"
    agent_count = 0
    for domain_dir in agents_dir.iterdir():
        if not domain_dir.is_dir() or domain_dir.name.startswith("_") or domain_dir.name == "__pycache__":
            continue
        for agent_dir in domain_dir.iterdir():
            if not agent_dir.is_dir() or agent_dir.name.startswith("_") or agent_dir.name == "__pycache__":
                continue
            agent_count += 1
            cfg_file = agent_dir / ".agent_engine_config.json"
            assert cfg_file.exists(), f"Agent {agent_dir.name} is missing .agent_engine_config.json"
            with open(cfg_file, "r") as f:
                data = json.load(f)
            assert data.get("identity_type") == "AGENT_IDENTITY", f"Agent {agent_dir.name} does not have identity_type=AGENT_IDENTITY"
    
    assert agent_count == 113, f"Expected 113 agents, found {agent_count}"
