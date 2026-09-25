"""
BigQuery Query Tool - Master Orchestrator (Access Restricted).

The Master Orchestrator operates as a universal entry point and router. Under the
Agent Identity least-privilege security model, the Orchestrator has NO direct
access to BigQuery datasets or tables. All analytical queries and data retrieval
must be routed to specialized domain agents via AgentDelegationTool.
"""
from typing import Optional

class BigQueryQueryTool:
    """Disabled BigQuery tool for Master Orchestrator to enforce least privilege."""

    def __init__(
        self,
        project_id: Optional[str] = None,
        location: Optional[str] = None,
        identity_type: Optional[str] = None,
        agent_name: str = "utilities_master_orchestrator"
    ):
        self.name = "BigQueryQueryTool"
        self.__name__ = self.name
        self.agent_name = agent_name
        self.is_orchestrator = True
        self.allowed_tables = set()

    def get_effective_identity(self) -> str:
        return "principal://master-orchestrator-no-direct-bq-access"

    def __call__(self, query: str) -> str:
        return self.run(query)

    def run(self, query: str) -> str:
        """Denies execution and instructs the caller to use AgentDelegationTool."""
        raise PermissionError(
            "Access denied: The Master Orchestrator does not have direct access to BigQuery. "
            "It must delegate data retrieval to specialized domain agents (e.g., Asset Management, "
            "Grid Balancing, Smart Metering, Billing) via AgentDelegationTool."
        )
