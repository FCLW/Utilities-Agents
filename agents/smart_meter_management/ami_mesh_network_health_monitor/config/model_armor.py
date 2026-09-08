"""Centralized Google Cloud Model Armor Guardrail Integration for ADK Agents.

Provides seamless prompt injection defense, sensitive data protection (SDP),
and model response sanitization for all enterprise agents in Utilities-Agents.
Complies with ADK v2 guidelines.
"""

from __future__ import annotations

import os
import logging
import asyncio
from typing import Any, Optional, Dict, List
from functools import lru_cache


try:
    from config.settings import settings
except ImportError:
    import os
    class DummySettings:
        model_armor_enabled = os.getenv("MODEL_ARMOR_ENABLED", "true").lower() in ("true", "1", "yes")
        gcp_project_id = os.getenv("GCP_PROJECT_ID", "utilities-agents")
        model_armor_location = os.getenv("MODEL_ARMOR_LOCATION", "us")
        default_template = f"projects/{gcp_project_id}/locations/{model_armor_location}/templates/utilities-agent-guardrails"
        model_armor_prompt_template = os.getenv("MODEL_ARMOR_PROMPT_TEMPLATE", default_template)
        model_armor_response_template = os.getenv("MODEL_ARMOR_RESPONSE_TEMPLATE", default_template)
        model_armor_input_blocked_message = os.getenv(
            "MODEL_ARMOR_INPUT_BLOCKED_MESSAGE",
            "Request blocked by Model Armor security policy: prompt injection or safety risk detected."
        )
        model_armor_output_blocked_message = os.getenv(
            "MODEL_ARMOR_OUTPUT_BLOCKED_MESSAGE",
            "Response blocked by Model Armor security policy: sensitive data or safety risk detected."
        )
        model_armor_block_on_failure = os.getenv("MODEL_ARMOR_BLOCK_ON_FAILURE", "false").lower() in ("true", "1", "yes")
    settings = DummySettings()

logger = logging.getLogger(__name__)

# State keys for turn deduplication between App plugins and Agent callbacks
_INPUT_SCREENED_KEY = "_model_armor_screened_input"
_OUTPUT_SCREENED_KEY = "_model_armor_screened_output"

_plugin_instance: Any = None
_plugin_initialized: bool = False


def get_model_armor_config():
    """Builds and returns the ModelArmorConfig if enabled."""
    model_armor_enabled = getattr(settings, "model_armor_enabled", None)
    if model_armor_enabled is None:
        model_armor_enabled = os.getenv("MODEL_ARMOR_ENABLED", "true").lower() in ("true", "1", "yes")
    if not model_armor_enabled:
        return None

    try:
        from google.adk.integrations.model_armor import ModelArmorConfig
    except ImportError:
        logger.warning(
            "google.adk.integrations.model_armor is not available. "
            "Model Armor guardrails are inactive."
        )
        return None

    proj = getattr(settings, "gcp_project_id", os.getenv("GCP_PROJECT_ID", "utilities-agents"))
    loc = getattr(settings, "model_armor_location", os.getenv("MODEL_ARMOR_LOCATION", "us"))
    tmpl_id = getattr(settings, "model_armor_template_id", os.getenv("MODEL_ARMOR_TEMPLATE_ID", "utilities-agent-guardrails"))
    default_template = f"projects/{proj}/locations/{loc}/templates/{tmpl_id}"

    prompt_template = getattr(settings, "model_armor_prompt_template", None) or os.getenv("MODEL_ARMOR_PROMPT_TEMPLATE", default_template)
    response_template = getattr(settings, "model_armor_response_template", None) or os.getenv("MODEL_ARMOR_RESPONSE_TEMPLATE", default_template)


    return ModelArmorConfig(
        prompt_template_name=prompt_template or None,
        response_template_name=response_template or None,
        input_blocked_message=getattr(
            settings,
            "model_armor_input_blocked_message",
            "Request blocked by Model Armor security policy: prompt injection or safety risk detected."
        ),
        output_blocked_message=getattr(
            settings,
            "model_armor_output_blocked_message",
            "Response blocked by Model Armor security policy: sensitive data or safety risk detected."
        ),
        block_on_screening_failure=getattr(
            settings, "model_armor_block_on_failure", False
        ),
    )


def get_model_armor_credentials():
    """Returns valid Google credentials for Model Armor.
    Prefers Application Default Credentials (ADC), but seamlessly falls back
    to gcloud access token if ADC refresh tokens have expired in local dev environments.
    """
    try:
        import google.auth
        from google.auth.transport.requests import Request
        creds, _ = google.auth.default()
        creds.refresh(Request())
        return creds
    except Exception:
        pass

    try:
        import subprocess
        import google.oauth2.credentials
        token = subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()
        if token:
            return google.oauth2.credentials.Credentials(token)
    except Exception:
        pass

    return None


def get_model_armor_plugin():
    """Initializes and caches the singleton ModelArmorPlugin instance."""
    global _plugin_instance, _plugin_initialized
    if _plugin_initialized:
        return _plugin_instance

    _plugin_initialized = True
    config = get_model_armor_config()
    if not config:
        _plugin_instance = None
        return None

    try:
        from google.adk.integrations.model_armor import ModelArmorPlugin
        creds = get_model_armor_credentials()
        _plugin_instance = ModelArmorPlugin(
            config=config,
            name="utilities_model_armor_plugin",
            credentials=creds
        )
        logger.info(
            "Google Cloud Model Armor plugin initialized with template: %s",
            config.prompt_template_name
        )
    except Exception as e:
        logger.warning(
            "Failed to initialize ModelArmorPlugin: %s. Proceeding without Model Armor.",
            e
        )
        _plugin_instance = None

    return _plugin_instance



def _ensure_active_client(plugin: Any):
    """Ensures plugin's gRPC client is bound to the currently running asyncio event loop."""
    if plugin is None:
        return
    client = getattr(plugin, "_client", None)
    if client is not None:
        try:
            current_loop = asyncio.get_running_loop()
            transport = getattr(client, "transport", None)
            channel = getattr(transport, "grpc_channel", None)
            channel_loop = getattr(channel, "_loop", None)
            if channel_loop is None or channel_loop.is_closed() or channel_loop is not current_loop:
                plugin._client = None
        except Exception:
            plugin._client = None


def get_model_armor_plugins() -> list:
    """Returns a list containing the ModelArmorPlugin for App(plugins=[...])."""
    plugin = get_model_armor_plugin()
    return [plugin] if plugin is not None else []


async def model_armor_before_model_callback(
    *, callback_context: Any, llm_request: Any
) -> Optional[Any]:
    """Callback for Agent(before_model_callback=...).

    Screens incoming prompt against Model Armor prompt template.
    Avoids duplicate screening if App plugin already screened this turn.
    """
    if hasattr(callback_context, "state") and callback_context.state is not None:
        if callback_context.state.get(_INPUT_SCREENED_KEY):
            return None

    plugin = get_model_armor_plugin()
    if not plugin:
        return None

    _ensure_active_client(plugin)

    try:
        response = await plugin.before_model_callback(
            callback_context=callback_context,
            llm_request=llm_request,
        )
        if hasattr(callback_context, "state") and callback_context.state is not None:
            callback_context.state[_INPUT_SCREENED_KEY] = True
        return response
    except Exception as e:
        logger.error("Model Armor before_model_callback error: %s", e)
        if getattr(settings, "model_armor_block_on_failure", False):
            from google.adk.models.llm_response import LlmResponse
            from google.genai import types
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=settings.model_armor_input_blocked_message)],
                ),
                custom_metadata={"model_armor_blocked": True, "error": str(e)},
            )
        return None


async def model_armor_after_model_callback(
    *, callback_context: Any, llm_response: Any
) -> Optional[Any]:
    """Callback for Agent(after_model_callback=...).

    Screens outgoing response against Model Armor response template.
    Avoids duplicate screening if App plugin already screened this turn.
    """
    if hasattr(callback_context, "state") and callback_context.state is not None:
        if callback_context.state.get(_OUTPUT_SCREENED_KEY):
            return None

    plugin = get_model_armor_plugin()
    if not plugin:
        return None

    _ensure_active_client(plugin)


    try:
        response = await plugin.after_model_callback(
            callback_context=callback_context,
            llm_response=llm_response,
        )
        if hasattr(callback_context, "state") and callback_context.state is not None:
            callback_context.state[_OUTPUT_SCREENED_KEY] = True
        return response
    except Exception as e:
        logger.error("Model Armor after_model_callback error: %s", e)
        if getattr(settings, "model_armor_block_on_failure", False):
            from google.adk.models.llm_response import LlmResponse
            from google.genai import types
            return LlmResponse(
                content=types.Content(
                    role="model",
                    parts=[types.Part(text=settings.model_armor_output_blocked_message)],
                ),
                custom_metadata={"model_armor_blocked": True, "error": str(e)},
            )
        return None


def get_model_armor_callbacks() -> Dict[str, Any]:
    """Returns callback kwargs dictionary for Agent instantiation:

    Usage:
        Agent(
            name="...",
            model=...,
            ...,
            **get_model_armor_callbacks()
        )
    """
    if not getattr(settings, "model_armor_enabled", False):
        return {}

    return {
        "before_model_callback": model_armor_before_model_callback,
        "after_model_callback": model_armor_after_model_callback,
    }
