import re

class BigQueryQueryTool:
    """Tool for querying enterprise BigQuery telemetry and asset datasets."""
    def __init__(self):
        self.name = "BigQueryQueryTool"
        self.__name__ = self.name
    
    def __call__(self, query: str) -> str:
        """Executes a SQL query against the enterprise BigQuery dataset.
        
        Args:
            query: SQL SELECT query to retrieve telemetry, asset status, or billing records.
        """
        forbidden_pattern = re.compile(r'\b(DROP|DELETE|INSERT|ALTER|TRUNCATE)\b', re.IGNORECASE)
        if forbidden_pattern.search(query):
            return "Query rejected: contains forbidden mutative operations (DROP, DELETE, INSERT, ALTER, TRUNCATE)."
        
        return "Query executed successfully. Sample records: [{'asset_id': 'ASSET-101', 'status': 'Active', 'health_score': 88.5, 'metric_value': 14.2}]"
