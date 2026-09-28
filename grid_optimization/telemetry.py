# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Google Cloud Native Telemetry & Observability Manager for Grid Optimization MAS.

Provides:
- OpenTelemetry Distributed Tracing (Cloud Trace compatible spans with GenAI semantic conventions)
- Correlated Google Cloud Logging with trace IDs and Agent Identity principals
- Real-time Metrics Aggregation (latencies, token counts, BigQuery MBs, HITL lifecycle, safety checks)
- In-memory Trace and Audit Buffers accessible via REST endpoints and web portal
- Table-level and Persona-level Agent Identity authorization auditing
"""

import os
import time
import uuid
import logging
import threading
from collections import deque
from datetime import datetime, timezone
from contextlib import contextmanager
from typing import Dict, Any, List, Optional

from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode

# Import centralized settings & telemetry initialization
try:
    from config.settings import settings
except ImportError:
    class FallbackSettings:
        gcp_project_id = os.getenv("GCP_PROJECT_ID", "utilities-agents")
        gcp_region = os.getenv("GCP_REGION", "us-central1")
        telemetry_enabled = True
        cloud_trace_enabled = True
        cloud_logging_enabled = True
        cloud_metrics_enabled = True
    settings = FallbackSettings()

try:
    from config.telemetry import setup_telemetry, get_telemetry_callbacks, get_telemetry_plugins
    setup_telemetry(agent_name="grid_optimization_orchestrator")
except Exception as _e:
    pass

logger = logging.getLogger("utilities.grid_optimization.telemetry")


class GridTelemetryTracker:
    """Thread-safe telemetry collector, distributed trace recorder, and audit manager."""

    def __init__(self, max_buffer_size: int = 500):
        self._lock = threading.Lock()
        self._max_size = max_buffer_size
        self._spans: deque = deque(maxlen=max_buffer_size)
        self._audit_logs: deque = deque(maxlen=max_buffer_size)
        self._latencies: deque = deque(maxlen=200)

        # Cumulative Metrics Counters
        self._metrics: Dict[str, Any] = {
            "identity_mode": "AGENT_IDENTITY",
            "telemetry_enabled": True,
            "cloud_trace_active": True,
            "total_spans": 0,
            "total_traces": 0,
            "total_errors": 0,
            "total_requests": 0,
            "avg_latency_ms": 0.0,
            "p95_latency_ms": 0.0,
            "bq_queries_total": 0,
            "bq_bytes_scanned_mb": 0.0,
            "validation_checks_total": 0,
            "validation_violations_total": 0,
            "hitl_tickets_created": 0,
            "hitl_tickets_approved": 0,
            "hitl_tickets_rejected": 0,
            "persona_dispatches": {},
            "workflow_executions": {},
            "active_principals": set(),
        }

        self._tracer = trace.get_tracer("utilities.grid_optimization")

    @property
    def tracer(self):
        return self._tracer

    def _get_current_trace_and_span_ids(self) -> tuple[str, str]:
        """Extracts trace_id and span_id from OpenTelemetry active span, or creates UUIDs."""
        current_span = trace.get_current_span()
        if current_span and current_span.get_span_context().is_valid:
            ctx = current_span.get_span_context()
            trace_id = format(ctx.trace_id, "032x")
            span_id = format(ctx.span_id, "016x")
            return trace_id, span_id
        return uuid.uuid4().hex, uuid.uuid4().hex[:16]

    @contextmanager
    def trace_span(self, name: str, attributes: Optional[Dict[str, Any]] = None):
        """Context manager creating both an OpenTelemetry span and an in-memory trace entry."""
        attrs = attributes or {}
        # Standard OpenTelemetry & Google Cloud Agent Identity attributes
        base_attrs = {
            "service.name": "grid_optimization",
            "cloud.provider": "gcp",
            "gcp.project_id": getattr(settings, "gcp_project_id", "utilities-agents"),
            "gcp.region": getattr(settings, "gcp_region", "us-central1"),
            "identity.type": "AGENT_IDENTITY",
            "gen_ai.system": "gemini",
            "gen_ai.request.model": "gemini-3.7-flash",
        }
        all_attrs = {**base_attrs, **attrs}

        start_time_sec = time.time()
        start_iso = datetime.now(timezone.utc).isoformat()
        span_id = uuid.uuid4().hex[:16]
        trace_id = uuid.uuid4().hex

        # OpenTelemetry span invocation
        with self._tracer.start_as_current_span(name) as otel_span:
            try:
                # Set OTEL attributes
                for k, v in all_attrs.items():
                    if isinstance(v, (str, int, float, bool)):
                        otel_span.set_attribute(k, v)

                # Extract valid hex IDs if available
                if otel_span.get_span_context().is_valid:
                    ctx = otel_span.get_span_context()
                    trace_id = format(ctx.trace_id, "032x")
                    span_id = format(ctx.span_id, "016x")

                status_val = "OK"
                error_msg = None
                yield otel_span

            except Exception as e:
                status_val = "ERROR"
                error_msg = str(e)
                otel_span.set_status(Status(StatusCode.ERROR, description=str(e)))
                otel_span.record_exception(e)
                with self._lock:
                    self._metrics["total_errors"] += 1
                raise
            finally:
                duration_ms = round((time.time() - start_time_sec) * 1000.0, 2)
                end_iso = datetime.now(timezone.utc).isoformat()

                record = {
                    "trace_id": trace_id,
                    "span_id": span_id,
                    "name": name,
                    "start_time": start_iso,
                    "end_time": end_iso,
                    "duration_ms": duration_ms,
                    "status": status_val,
                    "error": error_msg,
                    "attributes": {k: str(v) if not isinstance(v, (str, int, float, bool)) else v for k, v in all_attrs.items()}
                }

                self._record_span_in_memory(record)

    def _record_span_in_memory(self, record: Dict[str, Any]):
        """Updates buffer and aggregates latency stats."""
        with self._lock:
            self._spans.append(record)
            self._latencies.append(record["duration_ms"])
            self._metrics["total_spans"] += 1

            if len(self._latencies) > 0:
                self._metrics["avg_latency_ms"] = round(sum(self._latencies) / len(self._latencies), 1)
                sorted_lats = sorted(self._latencies)
                p95_idx = int(0.95 * len(sorted_lats))
                self._metrics["p95_latency_ms"] = round(sorted_lats[min(p95_idx, len(sorted_lats) - 1)], 1)

            # Record principal if available
            p = record["attributes"].get("identity.principal")
            if p:
                self._metrics["active_principals"].add(p)

    def record_audit_event(
        self,
        persona_id: str,
        effective_identity: str,
        resource_type: str,
        resource_name: str,
        action: str,
        status: str,
        reason: str = "Authorized under Persona Least-Privilege Policy"
    ):
        """Records an Agent Identity resource access audit event."""
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "persona_id": persona_id,
            "effective_identity": effective_identity,
            "resource_type": resource_type,
            "resource_name": resource_name,
            "action": action,
            "status": status,
            "reason": reason,
        }
        with self._lock:
            self._audit_logs.append(event)
            self._metrics["active_principals"].add(effective_identity)

        log_level = logging.INFO if status in ("GRANTED", "SUCCESS") else logging.WARNING
        logger.log(
            log_level,
            f"Agent Identity Audit [{status}]: {persona_id} ({action} {resource_type}:{resource_name}) - {reason}",
            extra=event
        )

    def record_query(
        self,
        persona_id: str,
        dataset: str,
        table: str,
        query: str,
        total_rows: int,
        bytes_scanned_mb: float,
        is_mock: bool,
        effective_identity: str,
        execution_time_ms: float
    ):
        """Records BigQuery query metrics and audit event."""
        with self._lock:
            self._metrics["bq_queries_total"] += 1
            self._metrics["bq_bytes_scanned_mb"] = round(self._metrics["bq_bytes_scanned_mb"] + bytes_scanned_mb, 2)

        self.record_audit_event(
            persona_id=persona_id,
            effective_identity=effective_identity,
            resource_type="BIGQUERY_TABLE",
            resource_name=f"{dataset}.{table}",
            action="QUERY",
            status="GRANTED",
            reason=f"Scanned {bytes_scanned_mb} MB ({total_rows} rows returned in {execution_time_ms}ms)"
        )

    def record_validation(self, risk_level: str, violations: List[str], execution_time_ms: float = 0.0):
        """Records physics validation harness result metrics."""
        with self._lock:
            self._metrics["validation_checks_total"] += 1
            if violations or risk_level in ("HIGH", "CRITICAL"):
                self._metrics["validation_violations_total"] += len(violations) or 1

    def record_hitl_action(self, ticket_id: str, action: str, operator_id: str, risk_tier: str = "TIER_3"):
        """Records HITL gatekeeper ticket lifecycle transitions."""
        with self._lock:
            if action == "CREATED":
                self._metrics["hitl_tickets_created"] += 1
            elif action == "APPROVED":
                self._metrics["hitl_tickets_approved"] += 1
            elif action == "REJECTED":
                self._metrics["hitl_tickets_rejected"] += 1

        self.record_audit_event(
            persona_id="hitl_gateway",
            effective_identity="principal://iam.googleapis.com/lead_operator",
            resource_type="HITL_TICKET",
            resource_name=ticket_id,
            action=action,
            status="SUCCESS",
            reason=f"Operator '{operator_id}' executed {action} for {risk_tier} physical switching"
        )

    def record_persona_dispatch(self, persona_id: str, task_type: str, duration_ms: float, status: str = "SUCCESS"):
        """Records persona task dispatches."""
        with self._lock:
            self._metrics["total_requests"] += 1
            current = self._metrics["persona_dispatches"].get(persona_id, 0)
            self._metrics["persona_dispatches"][persona_id] = current + 1

    def record_workflow_execution(self, workflow_name: str, duration_ms: float, status: str = "SUCCESS"):
        """Records collaborative multi-persona workflow executions."""
        with self._lock:
            current = self._metrics["workflow_executions"].get(workflow_name, 0)
            self._metrics["workflow_executions"][workflow_name] = current + 1

    def get_metrics(self) -> Dict[str, Any]:
        """Returns snapshot of live telemetry and observability metrics."""
        with self._lock:
            m = dict(self._metrics)
            m["active_principals"] = sorted(list(self._metrics["active_principals"]))
            m["total_traces"] = len(set(s["trace_id"] for s in self._spans))
            m["recent_spans_count"] = len(self._spans)
            m["audit_log_count"] = len(self._audit_logs)
            return m

    def get_recent_spans(self, limit: int = 50, persona_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns most recent distributed trace spans."""
        with self._lock:
            items = list(self._spans)

        if persona_id:
            items = [s for s in items if s["attributes"].get("gen_ai.agent.name") == persona_id or s["attributes"].get("persona_id") == persona_id]

        items.reverse()
        return items[:limit]

    def get_audit_logs(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Returns most recent Agent Identity audit log entries."""
        with self._lock:
            items = list(self._audit_logs)
        items.reverse()
        return items[:limit]

    def clear(self):
        """Clears in-memory buffers (primarily for clean testing)."""
        with self._lock:
            self._spans.clear()
            self._audit_logs.clear()
            self._latencies.clear()
            self._metrics["total_spans"] = 0
            self._metrics["total_traces"] = 0
            self._metrics["total_errors"] = 0
            self._metrics["total_requests"] = 0
            self._metrics["bq_queries_total"] = 0
            self._metrics["bq_bytes_scanned_mb"] = 0.0
            self._metrics["validation_checks_total"] = 0
            self._metrics["validation_violations_total"] = 0
            self._metrics["hitl_tickets_created"] = 0
            self._metrics["hitl_tickets_approved"] = 0
            self._metrics["hitl_tickets_rejected"] = 0
            self._metrics["persona_dispatches"].clear()
            self._metrics["workflow_executions"].clear()
            self._metrics["active_principals"].clear()


# Global Singleton Instance
grid_telemetry = GridTelemetryTracker()

def get_grid_telemetry() -> GridTelemetryTracker:
    return grid_telemetry
