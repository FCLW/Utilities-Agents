from fastapi import FastAPI
from .agent import task_lead_agent
from google.adk.apps.app import App
from fastapi.responses import StreamingResponse

app = FastAPI(title="Hazardous Waste Disposal Tracker")
adk_app = App(name=task_lead_agent.name, root_agent=task_lead_agent)

# OpenTelemetry Middleware
try:
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    FastAPIInstrumentor.instrument_app(app)
except ImportError:
    pass

@app.get("/healthz")
def healthz():
    return {"status": "ok"}

@app.post("/chat/stream")
async def chat_stream(request: dict):
    # Process with adk_app and return SSE
    pass
