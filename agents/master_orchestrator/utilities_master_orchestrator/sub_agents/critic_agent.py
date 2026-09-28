import os
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"
os.environ["GOOGLE_API_USE_CLIENT_CERTIFICATE"] = "false"
os.environ["GOOGLE_API_USE_MTLS_ENDPOINT"] = "never"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "true"

from google.adk import Agent
from ..app_utils.prompt_loader import load_prompt_layer

try:
    from config.settings import settings
except ImportError:
    class Settings:
        reasoning_model_name = os.getenv("REASONING_MODEL_NAME", "gemini-3.7-flash")
    settings = Settings()

instruction = load_prompt_layer("critic_agent")

critic_agent = Agent(
    name="utilities_master_orchestrator_critic",
    model=getattr(settings, "reasoning_model_name", "gemini-3.7-flash"),
    instruction=instruction
)