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
Centralized Google Cloud Native Telemetry & Observability Module.

Provides seamless integration with:
- Google Cloud Trace (via OpenTelemetry CloudTraceSpanExporter and ADK GCP exporters)
- Google Cloud Logging (via StructuredLogHandler and GCP JSON format with trace correlation)
- Google Cloud Monitoring (via GCP metric readers)
- Google GenAI SDK (via GoogleGenAiSdkInstrumentor)
- ADK Application & Agent Lifecycle Logging & Tracing Plugins
"""

import asyncio
import inspect
import logging
import os
import sys
import time
from typing import Any, Callable, Dict, List, Optional

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Import configuration
try:
    from .settings import settings
except ImportError:
    try:
        from config.settings import settings
    except ImportError:
        class SettingsFallback:
            gcp_project_id = os.getenv("GCP_PROJECT_ID", "utilities-agents")
            gcp_region = os.getenv("GCP_REGION", "us-central1")
            telemetry_enabled = os.getenv("TELEMETRY_ENABLED", "true").lower() in ("true", "1", "yes")
            cloud_trace_enabled = os.getenv("CLOUD_TRACE_ENABLED", "true").lower() in ("true", "1", "yes")
            cloud_logging_enabled = os.getenv("CLOUD_LOGGING_ENABLED", "true").lower() in ("true", "1", "yes")
            cloud_metrics_enabled = os.getenv("CLOUD_METRICS_ENABLED", "true").lower() in ("true", "1", "yes")
            log_level = os.getenv("LOG_LEVEL", "INFO").upper()
            capture_message_content = os.getenv("OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "NO_CONTENT")
        settings = SettingsFallback()

logger = logging.getLogger("utilities_agents.telemetry")

_telemetry_initialized = False


def get_telemetry_credentials() -> tuple[Optional[Any], str]:
    """Returns valid Google credentials and project ID for Google Cloud Trace & Logging.
    Prefers Application Default Credentials (ADC), falling back to gcloud access
    tokens in local development environments.
    """
    project_id = getattr(settings, "gcp_project_id", os.getenv("GCP_PROJECT_ID", "utilities-agents"))

    # 1. Try ADC
    try:
        import google.auth
        from google.auth.transport.requests import Request
        creds, detected_proj = google.auth.default()
        creds.refresh(Request())
        return creds, detected_proj or project_id
    except Exception:
        pass

    # 2. Try gcloud access token
    try:
        import subprocess
        import google.oauth2.credentials
        token = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"],
            text=True,
            timeout=5
        ).strip()
        if token:
            return google.oauth2.credentials.Credentials(token), project_id
    except Exception:
        pass

    return None, project_id


def setup_telemetry(agent_name: str = "utilities_agent") -> None:
    """Sets up Google Cloud Native Logging and Distributed Tracing.

    Configures:
    1. Python logging with Google Cloud StructuredLogHandler (JSON on stdout with trace correlation).
    2. OpenTelemetry TracerProvider with Google Cloud Trace exporter.
    3. Google GenAI SDK instrumentation for Gemini calls.
    """
    global _telemetry_initialized
    if _telemetry_initialized:
        return

    # Check if telemetry is enabled
    if not getattr(settings, "telemetry_enabled", True):
        return

    log_level = getattr(logging, getattr(settings, "log_level", "INFO"), logging.INFO)

    # 1. Setup Google Cloud Native Structured Logging
    if getattr(settings, "cloud_logging_enabled", True):
        try:
            from google.cloud.logging.handlers import StructuredLogHandler
            root_logger = logging.getLogger()
            root_logger.setLevel(log_level)

            # Check if StructuredLogHandler is already attached
            has_structured_handler = any(
                isinstance(h, StructuredLogHandler) for h in root_logger.handlers
            )
            if not has_structured_handler:
                project_id = getattr(settings, "gcp_project_id", "utilities-agents")
                structured_handler = StructuredLogHandler(project_id=project_id)
                structured_handler.setLevel(log_level)
                root_logger.addHandler(structured_handler)
        except Exception:
            logging.basicConfig(
                level=log_level,
                format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )

    # 2. Setup Google Cloud Distributed Tracing
    if getattr(settings, "cloud_trace_enabled", True):
        try:
            from google.adk.telemetry.google_cloud import get_gcp_exporters, get_gcp_resource
            from google.adk.telemetry.setup import maybe_set_otel_providers

            current_provider = trace.get_tracer_provider()
            if not isinstance(current_provider, TracerProvider):
                creds, proj = get_telemetry_credentials()
                hooks = get_gcp_exporters(
                    enable_cloud_tracing=True,
                    enable_cloud_metrics=getattr(settings, "cloud_metrics_enabled", False),
                    enable_cloud_logging=getattr(settings, "cloud_logging_enabled", True),
                    google_auth=(creds, proj) if creds else None,
                )
                otel_resource = get_gcp_resource(proj)
                maybe_set_otel_providers([hooks], otel_resource=otel_resource)
        except Exception as e:
            logger.warning(f"Could not initialize Google Cloud Trace exporter: {e}")

    # 3. Setup GenAI SDK Instrumentation
    try:
        from opentelemetry.instrumentation.google_genai import GoogleGenAiSdkInstrumentor
        GoogleGenAiSdkInstrumentor().instrument()
    except Exception:
        pass

    _telemetry_initialized = True


# ============================================================================
# Google Cloud Native ADK Logging & Tracing Plugin
# ============================================================================

try:
    from google.adk.plugins.base_plugin import BasePlugin
    from google.adk.agents.invocation_context import InvocationContext
    from google.adk.agents.callback_context import CallbackContext
    from google.adk.agents.base_agent import BaseAgent
    from google.adk.models.llm_request import LlmRequest
    from google.adk.models.llm_response import LlmResponse
    from google.adk.tools.base_tool import BaseTool
    from google.adk.tools.tool_context import ToolContext
    from google.genai import types

    class GcpCloudLoggingPlugin(BasePlugin):
        """Google Cloud native logging and tracing plugin for ADK.

        Logs structured JSON entries to Google Cloud Logging for:
        - Invocations (start, completion, duration)
        - Sub-agent executions
        - LLM requests and responses (with model name, token usage)
        - Tool executions (arguments, execution duration, status)
        - Errors and exceptions with stack traces

        When Google Cloud Trace is active, all log lines automatically correlate
        with the active trace span in the Cloud Trace Explorer.
        """

        def __init__(self, name: str = "gcp_cloud_logging_plugin", agent_name: str = "utilities_agent"):
            super().__init__(name=name)
            self._agent_name = agent_name
            self._log_level = getattr(logging, getattr(settings, "log_level", "INFO"), logging.INFO)
            self._plugin_logger = logging.getLogger(f"utilities.{agent_name}")

        async def before_run_callback(
            self, *, invocation_context: InvocationContext
        ) -> Optional[None]:
            self._plugin_logger.info(
                f"Agent invocation started: {self._agent_name}",
                extra={
                    "agent_name": self._agent_name,
                    "event_type": "invocation_start",
                    "invocation_id": getattr(invocation_context, "invocation_id", "unknown"),
                    "session_id": getattr(invocation_context, "session_id", "unknown"),
                }
            )
            return None

        async def after_run_callback(
            self, *, invocation_context: InvocationContext
        ) -> Optional[None]:
            self._plugin_logger.info(
                f"Agent invocation completed: {self._agent_name}",
                extra={
                    "agent_name": self._agent_name,
                    "event_type": "invocation_complete",
                    "invocation_id": getattr(invocation_context, "invocation_id", "unknown"),
                    "session_id": getattr(invocation_context, "session_id", "unknown"),
                }
            )
            return None

        async def before_agent_callback(
            self, *, agent: BaseAgent, callback_context: CallbackContext
        ) -> Optional[types.Content]:
            sub_name = getattr(agent, "name", "unknown")
            self._plugin_logger.info(
                f"Executing agent step: {sub_name}",
                extra={
                    "agent_name": self._agent_name,
                    "sub_agent": sub_name,
                    "event_type": "agent_start",
                    "invocation_id": getattr(callback_context, "invocation_id", "unknown"),
                }
            )
            return None

        async def after_agent_callback(
            self, *, agent: BaseAgent, callback_context: CallbackContext
        ) -> Optional[types.Content]:
            sub_name = getattr(agent, "name", "unknown")
            self._plugin_logger.info(
                f"Completed agent step: {sub_name}",
                extra={
                    "agent_name": self._agent_name,
                    "sub_agent": sub_name,
                    "event_type": "agent_complete",
                    "invocation_id": getattr(callback_context, "invocation_id", "unknown"),
                }
            )
            return None

        async def before_model_callback(
            self, *, callback_context: CallbackContext, llm_request: LlmRequest
        ) -> Optional[LlmResponse]:
            model = getattr(llm_request, "model", "default")
            tools = list(llm_request.tools_dict.keys()) if getattr(llm_request, "tools_dict", None) else []
            self._plugin_logger.info(
                f"LLM request dispatched to {model}",
                extra={
                    "agent_name": self._agent_name,
                    "model": model,
                    "tools_count": len(tools),
                    "event_type": "model_request",
                }
            )
            return None

        async def after_model_callback(
            self, *, callback_context: CallbackContext, llm_response: LlmResponse
        ) -> Optional[LlmResponse]:
            tokens = getattr(llm_response, "usage_metadata", None)
            token_dict = {}
            if tokens:
                token_dict = {
                    "prompt_tokens": getattr(tokens, "prompt_token_count", None),
                    "candidates_tokens": getattr(tokens, "candidates_token_count", None),
                    "total_tokens": getattr(tokens, "total_token_count", None),
                }

            self._plugin_logger.info(
                f"LLM response received from {self._agent_name}",
                extra={
                    "agent_name": self._agent_name,
                    "event_type": "model_response",
                    "tokens": token_dict,
                }
            )
            return None

        async def before_tool_callback(
            self, *, tool: BaseTool, tool_args: Dict[str, Any], tool_context: ToolContext
        ) -> Optional[Dict[str, Any]]:
            self._plugin_logger.info(
                f"Tool invocation starting: {tool.name}",
                extra={
                    "agent_name": self._agent_name,
                    "tool_name": tool.name,
                    "event_type": "tool_start",
                    "function_call_id": getattr(tool_context, "function_call_id", None),
                }
            )
            return None

        async def after_tool_callback(
            self, *, tool: BaseTool, tool_args: Dict[str, Any], tool_context: ToolContext, result: Dict[str, Any]
        ) -> Optional[Dict[str, Any]]:
            self._plugin_logger.info(
                f"Tool invocation completed: {tool.name}",
                extra={
                    "agent_name": self._agent_name,
                    "tool_name": tool.name,
                    "event_type": "tool_complete",
                    "function_call_id": getattr(tool_context, "function_call_id", None),
                }
            )
            return None

        async def on_model_error_callback(
            self, *, callback_context: CallbackContext, llm_request: LlmRequest, error: Exception
        ) -> Optional[LlmResponse]:
            self._plugin_logger.error(
                f"LLM error in {self._agent_name}: {error}",
                exc_info=True,
                extra={
                    "agent_name": self._agent_name,
                    "event_type": "model_error",
                    "error": str(error),
                }
            )
            return None

        async def on_tool_error_callback(
            self, *, tool: BaseTool, tool_args: Dict[str, Any], tool_context: ToolContext, error: Exception
        ) -> Optional[Dict[str, Any]]:
            self._plugin_logger.error(
                f"Tool error in {tool.name}: {error}",
                exc_info=True,
                extra={
                    "agent_name": self._agent_name,
                    "tool_name": tool.name,
                    "event_type": "tool_error",
                    "error": str(error),
                }
            )
            return None

except ImportError:
    class GcpCloudLoggingPlugin:  # type: ignore
        def __init__(self, *args, **kwargs):
            pass


def get_telemetry_plugins(agent_name: str = "utilities_agent") -> list:
    """Returns telemetry and logging plugins for ADK App registration."""
    if not getattr(settings, "telemetry_enabled", True):
        return []

    plugins = []
    # 1. Google Cloud Native Structured Logging Plugin
    try:
        plugins.append(GcpCloudLoggingPlugin(
            name=f"{agent_name}_cloud_logging",
            agent_name=agent_name
        ))
    except Exception as e:
        logger.debug(f"Could not load GcpCloudLoggingPlugin: {e}")

    # 2. ADK Built-in LoggingPlugin (stdout visual logger)
    try:
        from google.adk.plugins.logging_plugin import LoggingPlugin
        plugins.append(LoggingPlugin(name=f"{agent_name}_adk_logging"))
    except Exception:
        pass

    return plugins


def get_telemetry_callbacks(agent_name: str = "utilities_agent") -> dict[str, Callable]:
    """Returns agent-level telemetry callbacks for timing, tracing, and logging."""
    if not getattr(settings, "telemetry_enabled", True):
        return {}

    tracer = trace.get_tracer(f"utilities.{agent_name}")
    agent_logger = logging.getLogger(f"utilities.{agent_name}")

    async def before_agent(callback_context: Any = None, *args, **kwargs):
        agent_logger.info(
            f"Agent activated: {agent_name}",
            extra={"agent_name": agent_name, "event_type": "agent_activated"}
        )
        return None

    async def after_agent(callback_context: Any = None, *args, **kwargs):
        agent_logger.info(
            f"Agent finished: {agent_name}",
            extra={"agent_name": agent_name, "event_type": "agent_finished"}
        )
        return None

    async def before_tool(tool: Any = None, args: Any = None, tool_context: Any = None, *a, **kwargs):
        tool_name = getattr(tool, "name", str(tool)) if tool is not None else "unknown"
        agent_logger.debug(
            f"Executing tool {tool_name}",
            extra={"agent_name": agent_name, "tool_name": tool_name, "event_type": "tool_call"}
        )
        return None

    async def after_tool(tool: Any = None, args: Any = None, tool_context: Any = None, tool_response: Any = None, *a, **kwargs):
        tool_name = getattr(tool, "name", str(tool)) if tool is not None else "unknown"
        agent_logger.debug(
            f"Executed tool {tool_name}",
            extra={"agent_name": agent_name, "tool_name": tool_name, "event_type": "tool_result"}
        )
        return None

    return {
        "before_agent_callback": before_agent,
        "after_agent_callback": after_agent,
        "before_tool_callback": before_tool,
        "after_tool_callback": after_tool,
    }


def combine_agent_callbacks(*callback_dicts: dict[str, Callable]) -> dict[str, Callable]:
    """Merges multiple callback dictionaries (e.g. Model Armor + Telemetry).
    Chains functions for the same hook in execution order. If any callback
    returns a non-None value (e.g. Model Armor blocking an injection), that
    value is immediately returned.
    """
    combined: dict[str, Callable] = {}
    all_keys = set()
    for d in callback_dicts:
        if d:
            all_keys.update(d.keys())

    for key in all_keys:
        funcs = [d[key] for d in callback_dicts if d and key in d]
        if len(funcs) == 1:
            combined[key] = funcs[0]
        else:
            def make_chained(fn_name: str, fn_list: list[Callable]) -> Callable:
                async def chained(*args, **kwargs):
                    for fn in fn_list:
                        try:
                            res = fn(*args, **kwargs)
                        except TypeError:
                            import inspect
                            try:
                                sig = inspect.signature(fn)
                                bound_args = {}
                                pos_idx = 0
                                for param_name in sig.parameters:
                                    if param_name in kwargs:
                                        bound_args[param_name] = kwargs[param_name]
                                    elif pos_idx < len(args):
                                        bound_args[param_name] = args[pos_idx]
                                        pos_idx += 1
                                res = fn(**bound_args)
                            except Exception:
                                res = None
                        if asyncio.iscoroutine(res):
                            res = await res
                        if res is not None:
                            return res
                    return None
                return chained

            combined[key] = make_chained(key, funcs)

    return combined

