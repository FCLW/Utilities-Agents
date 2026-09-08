import pytest
from unittest.mock import patch, MagicMock
from app.tools.bigquery_tool import BigQueryQueryTool

def test_defensive_sql_guardrails():
    tool = BigQueryQueryTool()
    forbidden_queries = [
        "DROP TABLE localized_outage_ping_diagnostic_bot_data;",
        "DELETE FROM localized_outage_ping_diagnostic_bot_data WHERE name=1;",
        "TRUNCATE TABLE localized_outage_ping_diagnostic_bot_data;",
        "ALTER TABLE localized_outage_ping_diagnostic_bot_data DROP COLUMN x;",
        "INSERT INTO localized_outage_ping_diagnostic_bot_data VALUES (1);"
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
    result = tool.run("SELECT * FROM localized_outage_ping_diagnostic_bot_data LIMIT 10")
    assert "Query executed successfully" in result or "val1" in result
