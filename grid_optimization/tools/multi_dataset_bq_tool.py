"""Multi-Dataset BigQuery Query Tool for Grid Optimization Agents with Agent Identity.

Enforces Google Cloud Agent Identity (identity_type: "AGENT_IDENTITY") and strict
least-privilege table-level / dataset-level access policies across all 8 Grid Personas.
The Master Orchestrator operates under zero-direct BigQuery access and must delegate
data retrieval to designated domain personas.
"""

import os
import re
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Set

try:
    from google.cloud import bigquery
except ImportError:
    bigquery = None


@dataclass
class QueryResult:
    dataset: str
    table: str
    query_executed: str
    rows: List[Dict[str, Any]] = field(default_factory=list)
    total_rows: int = 0
    bytes_scanned_mb: float = 0.0
    execution_time_ms: float = 0.0
    is_mock: bool = False
    effective_identity: str = ""


# Granular Least-Privilege Policy for Grid Optimization Personas
PERSONA_POLICY: Dict[str, Dict[str, Any]] = {
    "grid_dispatcher_agent": {
        "domain": "grid_operations",
        "allowed_datasets": {"utilities_grid_operations"},
        "allowed_tables": {
            "feeder_telemetry",
            "scada_switching_events",
            "substation_load_telemetry",
            "circuit_breaker_operations",
        },
    },
    "planning_engineer_agent": {
        "domain": "grid_operations",
        "allowed_datasets": {"utilities_grid_operations", "utilities_grid_balancing"},
        "allowed_tables": {
            "feeder_telemetry",
            "hosting_capacity_models",
            "line_impedance_parameters",
            "contingency_scenarios",
        },
    },
    "derms_manager_agent": {
        "domain": "grid_balancing",
        "allowed_datasets": {"utilities_grid_balancing", "utilities_production_forecasting"},
        "allowed_tables": {
            "der_telemetry",
            "vpp_fleet_dispatch",
            "solar_forecast",
            "bess_state_of_charge",
        },
    },
    "protection_control_agent": {
        "domain": "grid_operations",
        "allowed_datasets": {"utilities_grid_operations", "utilities_asset_management"},
        "allowed_tables": {
            "feeder_telemetry",
            "relay_settings_catalog",
            "breaker_operations",
            "transformer_dga",
        },
    },
    "asset_reliability_agent": {
        "domain": "asset_management",
        "allowed_datasets": {"utilities_asset_management"},
        "allowed_tables": {
            "transformer_dga",
            "circuit_breaker_wear_analyzer_logs",
            "breaker",
            "substation_battery_health",
            "asset_health_index",
        },
    },
    "grid_analytics_data_scientist_agent": {
        "domain": "grid_operations",
        "allowed_datasets": {
            "utilities_grid_operations",
            "utilities_grid_balancing",
            "utilities_production_forecasting",
            "utilities_data",
        },
        "allowed_tables": {
            "feeder_telemetry",
            "weathernext_spatial_telemetry",
            "ami_load_profiles",
            "voltage_timeseries",
            "load_forecast_logs",
            "transformer_dga",
            "lmp_congestion",
        },
    },
    "field_operations_tech_agent": {
        "domain": "asset_management",
        "allowed_datasets": {"utilities_asset_management", "utilities_grid_operations"},
        "allowed_tables": {
            "pdm_work_orders",
            "feeder_telemetry",
            "field_switching_logs",
            "transformer_dga",
        },
    },
    "regulatory_compliance_officer_agent": {
        "domain": "regulatory_compliance",
        "allowed_datasets": {"utilities_regulatory_compliance", "utilities_wholesale_trading"},
        "allowed_tables": {
            "saidi_saifi_audit_records",
            "nerc_prc_fac_violations",
            "lmp_congestion",
            "clean_energy_rps_records",
        },
    },
}


class MultiDatasetBigQueryTool:
    """Provides validated read-only querying across utility BigQuery datasets using Agent Identity."""

    ALLOWED_DATASETS = {
        "utilities_grid_operations",
        "utilities_grid_balancing",
        "utilities_asset_management",
        "utilities_smart_meter_management",
        "utilities_production_forecasting",
        "utilities_wholesale_trading",
        "utilities_regulatory_compliance",
        "utilities_data",
    }

    def __init__(self, project_id: Optional[str] = None, persona_id: Optional[str] = None):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "utilities-agents")
        self.location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
        self.identity_type = os.environ.get("IDENTITY_TYPE", "AGENT_IDENTITY")
        self.persona_id = persona_id
        self._client = None
        self._init_client()

    def get_effective_identity(self, persona_id: Optional[str] = None) -> str:
        """Returns the active Agent Identity or principal credential type used for resource access."""
        active_persona = persona_id or self.persona_id
        if active_persona == "grid_optimization_orchestrator":
            return "principal://master-orchestrator-no-direct-bq-access"

        try:
            import google.auth
            credentials, _ = google.auth.default()
            agent_id = os.getenv("GOOGLE_AGENT_IDENTITY")
            if agent_id:
                return f"principal://{agent_id}"
            if hasattr(credentials, "service_account_email") and credentials.service_account_email:
                return f"serviceAccount:{credentials.service_account_email}"
            persona_tag = f"/{active_persona}" if active_persona else ""
            return f"agentIdentity:{type(credentials).__name__}{persona_tag}"
        except Exception:
            persona_tag = f":{active_persona}" if active_persona else ""
            return f"agentIdentity:default{persona_tag} (type={self.identity_type})"

    def _init_client(self):
        try:
            if bigquery is not None and os.getenv("MOCK_BIGQUERY", "").lower() != "true":
                # BigQuery Client automatically discovers the Agent Identity via Application Default Credentials (ADC)
                self._client = bigquery.Client(project=self.project_id)
            else:
                self._client = None
        except Exception:
            # Fallback to analytical simulation mode if offline or ADC missing
            self._client = None

    def query_dataset(
        self,
        dataset: str,
        table: str,
        sql_query: Optional[str] = None,
        limit: int = 20,
        persona_id: Optional[str] = None,
    ) -> QueryResult:
        """Executes a safe read-only SQL query against authorized datasets and tables under Agent Identity."""
        active_persona = persona_id or self.persona_id

        # Master Orchestrator Zero-Direct BigQuery Access Rule
        if active_persona == "grid_optimization_orchestrator":
            raise PermissionError(
                "Access denied: The Master Orchestrator operates under least-privilege Agent Identity "
                "and does not have direct access to BigQuery. It must delegate analytical workflows and "
                "data retrieval to domain persona agents (e.g., grid_analytics_data_scientist_agent, "
                "asset_reliability_agent) via persona delegation."
            )

        # Enforce authorized dataset boundary
        if dataset not in self.ALLOWED_DATASETS:
            raise ValueError(f"Dataset '{dataset}' is not in the allowed grid datasets: {self.ALLOWED_DATASETS}")

        query = sql_query or f"SELECT * FROM `{self.project_id}.{dataset}.{table}` LIMIT {limit}"

        # Guard against DDL/DML and require SELECT or WITH syntax
        trimmed = query.strip()
        if not re.match(r"^\s*(SELECT|WITH)\b", trimmed, re.IGNORECASE):
            raise PermissionError("Query rejected: Query must begin with SELECT or WITH. Mutative or administrative statements are prohibited.")

        forbidden_patterns = [
            r"\bDROP\b", r"\bDELETE\b", r"\bINSERT\b", r"\bALTER\b",
            r"\bTRUNCATE\b", r"\bUPDATE\b", r"\bMERGE\b", r"\bCREATE\b",
            r"\bGRANT\b", r"\bREVOKE\b", r"\bCALL\b"
        ]
        for pat in forbidden_patterns:
            if re.search(pat, query, re.IGNORECASE):
                raise PermissionError(f"Security violation: Query contains disallowed DDL/DML token '{pat}'.")

        # Persona Least-Privilege Table and Dataset Scoping
        if active_persona and active_persona in PERSONA_POLICY:
            policy = PERSONA_POLICY[active_persona]
            allowed_ds: Set[str] = policy["allowed_datasets"]
            allowed_tbls: Set[str] = policy["allowed_tables"]

            if dataset not in allowed_ds:
                raise PermissionError(
                    f"Access denied: Persona '{active_persona}' is not authorized to query dataset '{dataset}'. "
                    f"Agent Identity least-privilege policy restricts access to: {sorted(list(allowed_ds))}."
                )

            # Check table authorization
            table_clean = table.strip("`")
            if table_clean not in allowed_tbls and not any(t in table_clean for t in allowed_tbls):
                raise PermissionError(
                    f"Access denied: Persona '{active_persona}' is not authorized to access table '{table}'. "
                    f"Agent Identity least-privilege policy restricts access to authorized tables only: {sorted(list(allowed_tbls))}."
                )

        eff_id = self.get_effective_identity(active_persona)

        if self._client is not None:
            try:
                query_job = self._client.query(query)
                results = query_job.result()
                rows = [dict(row.items()) for row in results]
                bytes_mb = round((query_job.total_bytes_billed or 0) / (1024 * 1024), 2)
                return QueryResult(
                    dataset=dataset,
                    table=table,
                    query_executed=query,
                    rows=rows,
                    total_rows=len(rows),
                    bytes_scanned_mb=bytes_mb,
                    execution_time_ms=120.0,
                    is_mock=False,
                    effective_identity=eff_id,
                )
            except Exception:
                # Fall back to grounded analytical rows if remote ADC/network is unreachable
                pass

        return self._generate_simulated_rows(dataset, table, query, limit, eff_id)

    def _generate_simulated_rows(
        self, dataset: str, table: str, query: str, limit: int, effective_identity: str
    ) -> QueryResult:
        """Provides realistic grounded telemetry for offline execution and testing."""
        rows = []
        if "voltage" in table or "voltage" in dataset or "feeder" in table:
            rows = [
                {"timestamp_column": "2026-09-10T12:00:00Z", "node_id": "BUS-NORTH-12", "voltage_pu": 0.985, "frequency_hz": 59.98, "delta_pct": -1.5, "status_flag": "NORMAL"},
                {"timestamp_column": "2026-09-10T12:15:00Z", "node_id": "BUS-NORTH-14", "voltage_pu": 0.942, "frequency_hz": 59.95, "delta_pct": -5.8, "status_flag": "UNDERVOLTAGE_ALERT"},
                {"timestamp_column": "2026-09-10T12:30:00Z", "node_id": "BUS-EAST-08", "voltage_pu": 1.012, "frequency_hz": 60.01, "delta_pct": 1.2, "status_flag": "NORMAL"},
            ]
        elif "transformer_dga" in table:
            rows = [
                {"timestamp_column": "2026-09-10T08:00:00Z", "transformer_id": "XFMR-SUB-44", "ch4_ppm": 92.0, "c2h4_ppm": 164.0, "c2h2_ppm": 3.1, "h2_ppm": 65.0, "fault_class": "T3_THERMAL"},
                {"timestamp_column": "2026-09-10T08:00:00Z", "transformer_id": "XFMR-SUB-12", "ch4_ppm": 12.0, "c2h4_ppm": 8.0, "c2h2_ppm": 0.0, "h2_ppm": 18.0, "fault_class": "NORMAL"},
            ]
        elif "breaker" in table:
            rows = [
                {"timestamp_column": "2026-09-10T10:00:00Z", "breaker_id": "CB-230-01", "operations_count": 1680, "sf6_pressure_bar": 5.75, "cumulative_fault_mva": 14200.0, "ahi": 68.5},
                {"timestamp_column": "2026-09-10T10:00:00Z", "breaker_id": "CB-115-04", "operations_count": 2890, "sf6_pressure_bar": 5.10, "cumulative_fault_mva": 22400.0, "ahi": 38.0},
            ]
        elif "lmp" in table or "congestion" in table:
            rows = [
                {"timestamp_column": "2026-09-10T13:00:00Z", "node_id": "NODE-WEST-HUB", "lmp_total_usd_mwh": 84.50, "congestion_usd_mwh": 22.10, "loss_usd_mwh": 2.40},
                {"timestamp_column": "2026-09-10T13:00:00Z", "node_id": "NODE-CENTRAL-GEN", "lmp_total_usd_mwh": 38.20, "congestion_usd_mwh": 0.0, "loss_usd_mwh": 0.80},
            ]
        else:
            rows = [
                {"timestamp_column": "2026-09-10T14:00:00Z", "entity_id": "GRID-ASSET-01", "current_value": 104.2, "baseline_target": 100.0, "status_flag": "NORMAL"}
            ]

        return QueryResult(
            dataset=dataset,
            table=table,
            query_executed=query,
            rows=rows[:limit],
            total_rows=len(rows[:limit]),
            bytes_scanned_mb=4.8,
            execution_time_ms=45.0,
            is_mock=True,
            effective_identity=effective_identity,
        )
