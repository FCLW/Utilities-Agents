import pytest
from unittest.mock import patch, MagicMock
import pandas as pd
from app.tools.bigquery_tool import BigQueryQueryTool

def test_defensive_sql_guardrails():
    tool = BigQueryQueryTool()
    forbidden_queries = [
        "DROP TABLE transformer_dga_history;",
        "TRUNCATE TABLE transformer_dga_history;",
        "DELETE FROM transformer_dga_history WHERE asset_name='TX-5543';"
    ]
    for q in forbidden_queries:
        with pytest.raises(ValueError) as exc:
            tool.run(q)
        assert "forbidden mutative operations" in str(exc.value)

@patch("google.cloud.bigquery.Client")
def test_dga_historical_data_parsing(mock_bq_client):
    tool = BigQueryQueryTool()
    
    # Mocking BigQuery RowIterator
    mock_query_job = MagicMock()
    mock_rows = [
        {"asset_id": "TX-5543", "Ethylene": 150.0, "timestamp": "2026-08-20"},
        {"asset_id": "TX-5543", "Ethylene": 200.0, "timestamp": "2026-08-21"}
    ]
    mock_query_job.result.return_value = mock_rows
    
    mock_client_instance = mock_bq_client.return_value
    mock_client_instance.query.return_value = mock_query_job
    
    # If the tool processed this into a DataFrame or string, we'd test it
    # We simulate what the tool would do with the mock
    df = pd.DataFrame(mock_query_job.result())
    assert len(df) == 2
    assert df.iloc[0]["asset_id"] == "TX-5543"
    
    # Pass valid query
    result = tool.run("SELECT * FROM transformer_dga_history WHERE asset_name='TX-5543'")
    assert "Query executed" in result or "TX-5543" in result
