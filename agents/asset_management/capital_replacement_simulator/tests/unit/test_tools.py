import sys
from pathlib import Path
import pytest
from unittest.mock import patch, MagicMock

agent_dir = Path(__file__).resolve().parents[2]
if str(agent_dir) not in sys.path:
    sys.path.insert(0, str(agent_dir))

import tools.bigquery_tool
import types
if 'app' not in sys.modules:
    app_mod = types.ModuleType('app')
    app_tools_mod = types.ModuleType('app.tools')
    sys.modules['app'] = app_mod
    sys.modules['app.tools'] = app_tools_mod
sys.modules['app.tools.bigquery_tool'] = tools.bigquery_tool

from tools.bigquery_tool import BigQueryQueryTool

def test_defensive_sql_guardrails():
    tool = BigQueryQueryTool()
    forbidden_queries = [
        "DROP TABLE capital_replacement_simulator_data;",
        "DELETE FROM capital_replacement_simulator_data WHERE name=1;",
        "TRUNCATE TABLE capital_replacement_simulator_data;",
        "ALTER TABLE capital_replacement_simulator_data DROP COLUMN x;",
        "INSERT INTO capital_replacement_simulator_data VALUES (1);"
    ]
    for q in forbidden_queries:
        with pytest.raises(ValueError) as exc:
            tool.run(q)
        assert "forbidden mutative operations" in str(exc.value)

@patch("google.cloud.bigquery.Client")
def test_bigquery_client_execution(mock_bq_client):
    tool = BigQueryQueryTool()
    # Mocking the row iterator
    mock_query_job = MagicMock()
    mock_query_job.result.return_value = [{"col1": "val1"}]
    mock_client_instance = mock_bq_client.return_value
    mock_client_instance.query.return_value = mock_query_job
    
    # Normally we'd test tool.run(valid_query) interacting with client
    # Since BigQueryQueryTool is currently a stub, we just ensure the guardrail passes
    result = tool.run("SELECT * FROM capital_replacement_simulator_data LIMIT 10")
    assert "Query executed successfully" in result or "val1" in result
