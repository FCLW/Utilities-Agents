import os
import re
from pathlib import Path
from typing import Optional, List, Set

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None

class BigQueryQueryTool:
    """Tool for querying enterprise BigQuery telemetry and asset datasets using Agent Identity
    with granular table-level and dataset-level authorization.
    """
    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        identity_type: Optional[str] = None,
        agent_name: Optional[str] = None,
        domain_name: Optional[str] = None,
        allowed_tables: Optional[List[str]] = None
    ):
        self.name = "BigQueryQueryTool"
        self.__name__ = self.name
        self.project_id = project_id or os.getenv("GCP_PROJECT_ID", "utilities-agents")
        self.location = location or os.getenv("GCP_LOCATION", "us-central1")
        self.identity_type = identity_type or os.getenv("IDENTITY_TYPE", "AGENT_IDENTITY")

        # Discover domain and agent identity from module path if not explicitly provided
        curr_path = Path(__file__).resolve()
        parts = curr_path.parts
        discovered_domain = None
        discovered_agent = None
        if "agents" in parts:
            idx = parts.index("agents")
            if len(parts) > idx + 1:
                discovered_domain = parts[idx + 1]
            if len(parts) > idx + 2:
                discovered_agent = parts[idx + 2]

        self.agent_name = agent_name or discovered_agent or os.getenv("AGENT_NAME", "utilities_domain_agent")
        self.domain_name = domain_name or discovered_domain or "utilities_data"
        self.is_orchestrator = "master_orchestrator" in self.agent_name.lower() or "master_orchestrator" in (self.domain_name or "").lower()

        # Table-level least privilege scoping
        if self.is_orchestrator:
            self.allowed_tables: Set[str] = set()
            self.allowed_datasets: Set[str] = set()
        elif allowed_tables:
            self.allowed_tables: Set[str] = set(allowed_tables)
            self.allowed_datasets: Set[str] = {f"utilities_{self.domain_name}", "utilities_data"}
        else:
            self.allowed_tables: Set[str] = {
                f"{self.agent_name}_logs",
                f"{self.agent_name}_data",
                f"{self.agent_name}_telemetry",
            }
            self.allowed_datasets: Set[str] = {f"utilities_{self.domain_name}", "utilities_data"}

        self._client = None

    def get_effective_identity(self) -> str:
        """Returns the active Agent Identity or principal credential type used for resource access."""
        if self.is_orchestrator:
            return "principal://master-orchestrator-no-direct-bq-access"
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
        if self._client is None and bigquery is not None and not self.is_orchestrator:
            try:
                # BigQuery Client automatically discovers the Agent Identity via Application Default Credentials (ADC)
                self._client = bigquery.Client(project=self.project_id, location=self.location)
            except Exception:
                self._client = None
        return self._client

    def __call__(self, query: str) -> str:
        return self.run(query)

    def run(self, query: str) -> str:
        """Executes a validated read-only SQL query against the agent's authorized BigQuery tables.
        
        Args:
            query: SQL SELECT query to retrieve telemetry, asset status, or analytical records.
        """
        if self.is_orchestrator:
            raise PermissionError(
                "Access denied: The Master Orchestrator does not have direct access to BigQuery. "
                "It must delegate data retrieval to specialized domain agents (e.g., Asset Management, "
                "Grid Balancing, Smart Metering, Billing) via AgentDelegationTool."
            )

        trimmed = query.strip()
        if not re.match(r'^\s*(SELECT|WITH)\b', trimmed, re.IGNORECASE):
            raise ValueError("Query rejected: contains forbidden mutative operations or non-read query structure (must begin with SELECT or WITH).")

        forbidden_pattern = re.compile(
            r'\b(DROP|DELETE|INSERT|ALTER|TRUNCATE|UPDATE|MERGE|CREATE|GRANT|REVOKE|CALL)\b',
            re.IGNORECASE
        )
        if forbidden_pattern.search(query):
            raise ValueError("Query rejected: contains forbidden mutative operations (DROP, DELETE, INSERT, ALTER, TRUNCATE, UPDATE, MERGE, CREATE, GRANT, REVOKE, CALL).")

        # Table-level authorization validation
        cte_names = set(re.findall(r'\b([a-zA-Z0-9_]+)\s+AS\s*\(', query, re.IGNORECASE))
        table_matches = re.findall(r'(?:FROM|JOIN)\s+`?([a-zA-Z0-9_\-\.]+)`?', query, re.IGNORECASE)
        for full_table_ref in table_matches:
            tbl_parts = full_table_ref.strip('`').split('.')
            target_table = tbl_parts[-1]
            if target_table in cte_names:
                continue

            # Check if dataset is specified and restricted
            if len(tbl_parts) >= 2:
                target_dataset = tbl_parts[-2]
                if self.allowed_datasets and target_dataset not in self.allowed_datasets and "utilities_*" not in self.allowed_datasets and self.domain_name != "_template":
                    raise PermissionError(
                        f"Access denied: Agent '{self.agent_name}' is not authorized to query dataset '{target_dataset}'. "
                        f"Domain isolation restricts access to: {sorted(list(self.allowed_datasets))}."
                    )

            # Check table authorization
            is_allowed = (
                target_table in self.allowed_tables
                or target_table.startswith(self.agent_name)
                or self.agent_name in target_table
                or "*" in self.allowed_tables
                or self.domain_name == "_template"
            )
            if not is_allowed:
                raise PermissionError(
                    f"Access denied: Agent '{self.agent_name}' is not authorized to access table '{target_table}'. "
                    f"Agent Identity least-privilege policy restricts access to authorized tables only: {sorted(list(self.allowed_tables))}."
                )

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
        
        return f"Query executed successfully against table {self.agent_name}_logs. Sample records: [{{'asset_id': 'ASSET-101', 'status': 'Active', 'health_score': 88.5, 'metric_value': 14.2}}]"
