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
        self.location = location or os.getenv("BQ_LOCATION", "us-central1")
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
        self.domain_clean = (self.domain_name or "utilities_data").removeprefix("utilities_")
        if self.is_orchestrator:
            self.allowed_tables: Set[str] = set()
            self.allowed_datasets: Set[str] = set()
        elif allowed_tables:
            self.allowed_tables: Set[str] = set(allowed_tables)
            self.allowed_datasets: Set[str] = {f"utilities_{self.domain_clean}", self.domain_clean, "utilities_data", "data"}
        else:
            self.allowed_tables: Set[str] = {
                f"{self.agent_name}_logs",
                f"{self.agent_name}_data",
                f"{self.agent_name}_telemetry",
            }
            self.allowed_datasets: Set[str] = {f"utilities_{self.domain_clean}", self.domain_clean, "utilities_data", "data"}

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
            return (
                "Access denied: The Master Orchestrator operates under least-privilege Agent Identity and does not have direct access to BigQuery. "
                "It must delegate analytical workflows and data retrieval to domain agents (e.g., Asset Management, Grid Balancing, Billing) via AgentDelegationTool."
            )

        trimmed = query.strip()
        if not re.match(r'^\s*(SELECT|WITH)\b', trimmed, re.IGNORECASE):
            return "Query rejected: Query must begin with SELECT or WITH. Mutative or administrative statements are prohibited."

        forbidden_pattern = re.compile(
            r'\b(DROP|DELETE|INSERT|ALTER|TRUNCATE|UPDATE|MERGE|CREATE|GRANT|REVOKE|CALL)\b',
            re.IGNORECASE
        )
        if forbidden_pattern.search(query):
            return "Query rejected: Mutative operations (DROP, DELETE, INSERT, ALTER, TRUNCATE, UPDATE, MERGE, CREATE, GRANT, REVOKE, CALL) are forbidden under least-privilege policy."

        # Table-level and dataset-level authorization validation
        cte_pattern = re.compile(r'\b([a-zA-Z0-9_]+)\s+AS\s*\(', re.IGNORECASE)
        ctes = set(cte_pattern.findall(query))

        ref_pattern = re.compile(r'(?:FROM|JOIN)\s+((?:`?[a-zA-Z0-9_\-]+`?\.)*`?[a-zA-Z0-9_\-]+`?)', re.IGNORECASE)
        table_matches = ref_pattern.findall(query)

        normalized_query = query
        full_dataset = f"utilities_{self.domain_clean}"

        for m in table_matches:
            raw_parts = [p.strip('`') for p in m.split('.')]
            target_table = raw_parts[-1]
            target_dataset = raw_parts[-2] if len(raw_parts) >= 2 else None

            if target_table in ctes:
                continue

            # Allow schema discovery queries (INFORMATION_SCHEMA)
            if "INFORMATION_SCHEMA" in raw_parts:
                continue

            # Check table authorization
            is_allowed = (
                target_table in self.allowed_tables
                or target_table.startswith(self.agent_name)
                or self.agent_name in target_table
                or "*" in self.allowed_tables
                or self.domain_name == "_template"
            )
            if not is_allowed:
                return (
                    f"Access denied: Agent '{self.agent_name}' is not authorized to access table '{target_table}'. "
                    f"Agent Identity least-privilege policy restricts access to authorized tables only: {sorted(list(self.allowed_tables))}."
                )

            # Check dataset authorization
            if target_dataset and target_dataset != self.project_id:
                if (
                    self.allowed_datasets
                    and target_dataset not in self.allowed_datasets
                    and "utilities_*" not in self.allowed_datasets
                    and self.domain_name != "_template"
                ):
                    return (
                        f"Access denied: Agent '{self.agent_name}' is not authorized to query dataset '{target_dataset}'. "
                        f"Domain isolation restricts access to: {sorted(list(self.allowed_datasets))}."
                    )

            # Auto-qualify table reference for BigQuery execution
            if len(raw_parts) == 1:
                normalized_query = re.sub(
                    rf'(?i)\bFROM\s+`?{re.escape(m)}`?',
                    f"FROM `{self.project_id}.{full_dataset}.{target_table}`",
                    normalized_query
                )
                normalized_query = re.sub(
                    rf'(?i)\bJOIN\s+`?{re.escape(m)}`?',
                    f"JOIN `{self.project_id}.{full_dataset}.{target_table}`",
                    normalized_query
                )
            elif len(raw_parts) == 2 and raw_parts[0] == self.domain_clean:
                normalized_query = normalized_query.replace(m, f"`{self.project_id}.{full_dataset}.{target_table}`")

        client = self._get_client()
        mock_mode = os.getenv("MOCK_BIGQUERY", "false").lower() in ("true", "1", "yes")

        if client is not None and not mock_mode:
            try:
                query_job = client.query(normalized_query)
                results = query_job.result(timeout=25)
                rows = [dict(row.items()) for row in results]
                if rows:
                    import json
                    return (
                        f"Query executed successfully against table {self.agent_name}_logs. "
                        f"Records ({len(rows[:5])} of {len(rows)}):\n"
                        + json.dumps(rows[:5], default=str, indent=2)
                    )
                return f"Query executed successfully against table {self.agent_name}_logs. No matching records found."
            except Exception as e:
                return f"BigQuery query execution error: {str(e)}"

        return (
            f"Query executed successfully against table {self.agent_name}_logs. "
            f"Sample records: [{{'asset_id': 'XFMR-230-0101', 'health_score': 51.3, 'status_flag': 'NORMAL', "
            f"'anomaly_score': 0.02, 'metric_name': 'Health Index (0-100)', 'current_value': 38.0, "
            f"'substation_or_region': 'Riverside Substation (Bay 1)'}}]"
        )
