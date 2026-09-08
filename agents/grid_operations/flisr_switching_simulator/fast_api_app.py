from fastapi import FastAPI
from .agent import task_lead_agent
from google.adk.apps.app import App
from fastapi.responses import StreamingResponse

try:
    from .config.model_armor import get_model_armor_plugins
    armor_plugins = get_model_armor_plugins()
except ImportError:
    try:
        from config.model_armor import get_model_armor_plugins
        armor_plugins = get_model_armor_plugins()
    except ImportError:
        armor_plugins = []

try:
    from .config.telemetry import setup_telemetry, get_telemetry_plugins
    setup_telemetry(task_lead_agent.name)
    telemetry_plugins = get_telemetry_plugins(task_lead_agent.name)
except ImportError:
    try:
        from config.telemetry import setup_telemetry, get_telemetry_plugins
        setup_telemetry(task_lead_agent.name)
        telemetry_plugins = get_telemetry_plugins(task_lead_agent.name)
    except ImportError:
        telemetry_plugins = []

plugins = armor_plugins + telemetry_plugins

app = FastAPI(title="Flisr Switching Simulator")
adk_app = App(name=task_lead_agent.name, root_agent=task_lead_agent, plugins=plugins)

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
