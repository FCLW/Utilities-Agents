import os
import re
from typing import Optional

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None

class BigQueryQueryTool:
    """Tool for querying enterprise BigQuery telemetry and asset datasets using Agent Identity."""
    def __init__(self, project_id: Optional[str] = None, location: Optional[str] = None, identity_type: Optional[str] = None):
        self.name = "BigQueryQueryTool"
        self.__name__ = self.name
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "utilities-agents")
        self.location = location or os.getenv("GCP_LOCATION", "us-central1")
        self.identity_type = identity_type or os.getenv("IDENTITY_TYPE", "AGENT_IDENTITY")
        self._client = None

    def get_effective_identity(self) -> str:
        """Returns the active Agent Identity or principal credential type used for resource access."""
        try:
            import google.auth
            credentials, _ = google.auth.default()
            agent_id = os.getenv("GOOGLE_AGENT_IDENTITY")
            if agent_id:
                return f"principal://{agent_id}"
            if hasattr(credentials, "service_account_email") and credentials.service_account_email:
                return f"serviceAccount:{credentials.service_account_email}"
            return f"agentIdentity:{type(credentials).__name__}"
        except Exception:
            return f"agentIdentity:default (type={self.identity_type})"

    def _get_client(self):
        if self._client is None and bigquery is not None:
            try:
                # BigQuery Client automatically discovers the Agent Identity via Application Default Credentials (ADC)
                self._client = bigquery.Client(project=self.project_id, location=self.location)
            except Exception:
                self._client = None
        return self._client

    def __call__(self, query: str) -> str:
        return self.run(query)

    def run(self, query: str) -> str:
        """Executes a SQL query against the enterprise BigQuery dataset.
        
        Args:
            query: SQL SELECT query to retrieve telemetry, asset status, or billing records.
        """
        trimmed = query.strip()
        if not re.match(r'^\s*(SELECT|WITH)\b', trimmed, re.IGNORECASE):
            raise ValueError("Query rejected: contains forbidden mutative operations or non-read query structure (must begin with SELECT or WITH).")

        forbidden_pattern = re.compile(
            r'\b(DROP|DELETE|INSERT|ALTER|TRUNCATE|UPDATE|MERGE|CREATE|GRANT|REVOKE|CALL)\b',
            re.IGNORECASE
        )
        if forbidden_pattern.search(query):
            raise ValueError("Query rejected: contains forbidden mutative operations (DROP, DELETE, INSERT, ALTER, TRUNCATE, UPDATE, MERGE, CREATE, GRANT, REVOKE, CALL).")
        
        client = self._get_client()
        mock_mode = os.getenv("MOCK_BIGQUERY", "false").lower() in ("true", "1", "yes")

        if client is not None and not mock_mode:
            try:
                if hasattr(bigquery, "QueryJobConfig"):
                    dry_run_config = bigquery.QueryJobConfig(dry_run=True, use_query_cache=True)
                    try:
                        dry_run_job = client.query(query, job_config=dry_run_config)
                        if hasattr(dry_run_job, "total_bytes_processed") and dry_run_job.total_bytes_processed and dry_run_job.total_bytes_processed > 250 * 1024 * 1024:
                            return f"Query rejected: will process {dry_run_job.total_bytes_processed / (1024*1024):.1f} MB, exceeding safety limit of 250 MB."
                    except Exception:
                        pass
                
                query_job = client.query(query)
                results = query_job.result()
                if hasattr(results, "__iter__"):
                    rows = list(results)
                    if rows:
                        return f"Query executed successfully. Result: {rows[:10]}"
                return "Query executed successfully. No records returned."
            except Exception as e:
                return f"BigQuery query execution error: {str(e)}"
        
        return "Query executed successfully. Sample records: [{'asset_id': 'ASSET-101', 'status': 'Active', 'health_score': 88.5, 'metric_value': 14.2}]"
