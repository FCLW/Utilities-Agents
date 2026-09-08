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
Unit and integration tests for Google Cloud Native Telemetry and Logging.
"""

import io
import json
import logging
import os
import sys
from pathlib import Path
import pytest
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import settings
from config.telemetry import (
    setup_telemetry,
    get_telemetry_credentials,
    get_telemetry_plugins,
    get_telemetry_callbacks,
    combine_agent_callbacks,
    GcpCloudLoggingPlugin,
)
from config.model_armor import get_model_armor_callbacks, get_model_armor_plugins
from google.adk import Agent
from google.adk.apps.app import App


def test_telemetry_settings():
    """Verify Google Cloud native telemetry settings exist and have valid defaults."""
    assert settings.telemetry_enabled is True
    assert settings.cloud_trace_enabled is True
    assert settings.cloud_logging_enabled is True
    assert settings.log_level in ("INFO", "DEBUG", "WARNING", "ERROR")
    assert settings.capture_message_content == "NO_CONTENT"


def test_telemetry_credentials():
    """Verify credential resolution succeeds without throwing unhandled exceptions."""
    creds, project_id = get_telemetry_credentials()
    assert project_id == "utilities-agents"


def test_setup_telemetry():
    """Verify setup_telemetry initializes OpenTelemetry and logging handlers."""
    setup_telemetry("test_unit_agent")
    provider = trace.get_tracer_provider()
    assert provider is not None


def test_structured_cloud_logging_trace_correlation():
    """Verify StructuredLogHandler injects Cloud Trace and Span IDs into logs."""
    from google.cloud.logging.handlers import StructuredLogHandler

    stream = io.StringIO()
    handler = StructuredLogHandler(stream=stream, project_id="utilities-agents")
    test_logger = logging.getLogger("test_trace_correlation")
    test_logger.addHandler(handler)
    test_logger.setLevel(logging.INFO)

    tracer = trace.get_tracer("test_tracer")
    with tracer.start_as_current_span("test_operational_span") as span:
        ctx = span.get_span_context()
        expected_trace_id = format(ctx.trace_id, "032x")
        expected_span_id = format(ctx.span_id, "016x")

        test_logger.info("Operational event in grid balancing", extra={"grid_substation": "sub_104"})

    output = stream.getvalue()
    lines = [line for line in output.strip().split("\n") if line.strip()]
    assert len(lines) >= 1

    # Find the operational event line
    event_entry = None
    for line in lines:
        try:
            data = json.loads(line)
            if data.get("message") == "Operational event in grid balancing":
                event_entry = data
                break
        except Exception:
            continue

    assert event_entry is not None, f"Could not find event line in output: {output}"
    assert event_entry.get("severity") == "INFO"
    assert "logging.googleapis.com/trace" in event_entry
    assert expected_trace_id in event_entry["logging.googleapis.com/trace"]
    assert event_entry.get("logging.googleapis.com/spanId") == expected_span_id


@pytest.mark.asyncio
async def test_combine_agent_callbacks():
    """Verify callback combination preserves Model Armor security blocking while chaining telemetry."""
    telemetry_called = False

    async def sample_telemetry_cb(ctx, req):
        nonlocal telemetry_called
        telemetry_called = True
        return None

    # Get real Model Armor callbacks
    armor_callbacks = get_model_armor_callbacks()
    telemetry_callbacks = {"before_model_callback": sample_telemetry_cb}

    combined = combine_agent_callbacks(armor_callbacks, telemetry_callbacks)
    assert "before_model_callback" in combined

    # Test clean prompt: both Model Armor and telemetry should execute
    from google.adk.models.llm_request import LlmRequest
    from google.genai import types

    class MockCallbackContext:
        agent_name = "test_agent"
        state = {}

    req = LlmRequest(
        contents=[
            types.Content(
                role="user",
                parts=[types.Part.from_text(text="Check transformer oil temperature.")]
            )
        ]
    )

    res = await combined["before_model_callback"](MockCallbackContext(), req)
    assert res is None  # Not blocked
    assert telemetry_called is True


def test_agent_and_app_initialization_with_telemetry():
    """Verify Agent and App initialize cleanly with both Model Armor and Telemetry plugins."""
    armor_callbacks = get_model_armor_callbacks()
    telemetry_callbacks = get_telemetry_callbacks("test_agent")
    callbacks = combine_agent_callbacks(armor_callbacks, telemetry_callbacks)

    agent = Agent(
        name="test_agent",
        model="gemini-2.5-flash",
        instruction="Test agent",
        **callbacks
    )
    assert agent.name == "test_agent"

    armor_plugins = get_model_armor_plugins()
    telemetry_plugins = get_telemetry_plugins("test_agent")
    all_plugins = armor_plugins + telemetry_plugins

    app = App(
        name="test_app",
        root_agent=agent,
        plugins=all_plugins
    )
    assert app.name == "test_app"
    assert len(app.plugins) >= 2
