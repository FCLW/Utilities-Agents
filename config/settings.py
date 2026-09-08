import os

# Ensure global endpoint for Gemini 3.7 Flash on Vertex AI
os.environ.setdefault("GOOGLE_CLOUD_LOCATION", "global")

class Settings:
    def __init__(self):
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID", "utilities-agents")
        self.gcp_region = os.getenv("GCP_REGION", "us-central1")
        self.gcp_location = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
        self.llm_model_name = os.getenv("LLM_MODEL_NAME", "gemini-3.7-flash")
        self.reasoning_model_name = os.getenv("REASONING_MODEL_NAME", "gemini-3.7-flash")
        self.bq_dataset_name = os.getenv("BQ_DATASET_NAME", "utilities-agents")

        # Google Cloud Model Armor Guardrails Configuration
        self.model_armor_enabled = os.getenv("MODEL_ARMOR_ENABLED", "true").lower() in ("true", "1", "yes")
        # Note: GEAP (Gemini Enterprise Agent Platform) assistants in location 'global' require multi-region 'us' (or 'eu')
        self.model_armor_location = os.getenv("MODEL_ARMOR_LOCATION", "us")
        self.model_armor_template_id = os.getenv("MODEL_ARMOR_TEMPLATE_ID", "utilities-agent-guardrails")
        default_template = f"projects/{self.gcp_project_id}/locations/{self.model_armor_location}/templates/{self.model_armor_template_id}"
        self.model_armor_prompt_template = os.getenv("MODEL_ARMOR_PROMPT_TEMPLATE", default_template)
        self.model_armor_response_template = os.getenv("MODEL_ARMOR_RESPONSE_TEMPLATE", default_template)

        self.model_armor_input_blocked_message = os.getenv(
            "MODEL_ARMOR_INPUT_BLOCKED_MESSAGE",
            "Request blocked by Model Armor security policy: prompt injection or safety risk detected."
        )
        self.model_armor_output_blocked_message = os.getenv(
            "MODEL_ARMOR_OUTPUT_BLOCKED_MESSAGE",
            "Response blocked by Model Armor security policy: sensitive data or safety risk detected."
        )
        self.model_armor_block_on_failure = os.getenv(
            "MODEL_ARMOR_BLOCK_ON_FAILURE", "false"
        ).lower() in ("true", "1", "yes")

        # Google Cloud Native Observability (Cloud Trace, Cloud Logging, Cloud Monitoring)
        self.telemetry_enabled = os.getenv("TELEMETRY_ENABLED", "true").lower() in ("true", "1", "yes")
        self.cloud_trace_enabled = os.getenv("CLOUD_TRACE_ENABLED", "true").lower() in ("true", "1", "yes")
        self.cloud_logging_enabled = os.getenv("CLOUD_LOGGING_ENABLED", "true").lower() in ("true", "1", "yes")
        self.cloud_metrics_enabled = os.getenv("CLOUD_METRICS_ENABLED", "true").lower() in ("true", "1", "yes")
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        self.capture_message_content = os.getenv(
            "OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT", "NO_CONTENT"
        )
        self.adk_capture_message_content_in_spans = os.getenv(
            "ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS", "false"
        ).lower() in ("true", "1", "yes")

settings = Settings()

