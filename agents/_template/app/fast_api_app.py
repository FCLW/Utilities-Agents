from fastapi import FastAPI
from .agent import agent
from google.adk.apps.app import App
from fastapi.responses import StreamingResponse

app = FastAPI(title="{{AGENT_NAME}}")
adk_app = App(name=agent.name, root_agent=agent)

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
