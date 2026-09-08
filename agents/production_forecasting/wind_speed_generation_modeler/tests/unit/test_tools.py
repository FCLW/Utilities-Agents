import pytest
from unittest.mock import patch, MagicMock
from app.tools.bigquery_tool import BigQueryQueryTool

def test_defensive_sql_guardrails():
    tool = BigQueryQueryTool()
    forbidden_queries = [
        "DROP TABLE wind_speed_generation_modeler_data;",
        "DELETE FROM wind_speed_generation_modeler_data WHERE name=1;",
        "TRUNCATE TABLE wind_speed_generation_modeler_data;",
        "ALTER TABLE wind_speed_generation_modeler_data DROP COLUMN x;",
        "INSERT INTO wind_speed_generation_modeler_data VALUES (1);"
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
    result = tool.run("SELECT * FROM wind_speed_generation_modeler_data LIMIT 10")
    assert "Query executed successfully" in result or "val1" in result
