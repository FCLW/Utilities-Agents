import os

# Ensure global endpoint for Gemini 3.7 Flash on Vertex AI
os.environ["GOOGLE_CLOUD_LOCATION"] = "global"

class Settings:
    def __init__(self):
        self.gcp_project_id = os.getenv("GCP_PROJECT_ID", "utilities-agents")
        self.gcp_region = os.getenv("GCP_REGION", "us-central1")
        self.gcp_location = "global"
        self.llm_model_name = os.getenv("LLM_MODEL_NAME", "gemini-3.7-flash")
        self.reasoning_model_name = os.getenv("REASONING_MODEL_NAME", "gemini-3.7-flash")
        self.bq_dataset_name = os.getenv("BQ_DATASET_NAME", "utilities-agents")

settings = Settings()
