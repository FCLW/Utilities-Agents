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

app = FastAPI(title="Omnichannel Intent Triage Router")
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

import json
import asyncio

@app.post("/chat/stream")
async def chat_stream(request: dict):
    """Streams agent responses formatted as Server-Sent Events (SSE)."""
    message = request.get("message") or request.get("prompt") or request.get("query") or ""
    session_state = request.get("session_state") or {}

    async def event_generator():
        try:
            yield f"event: open
data: {json.dumps({'agent': task_lead_agent.name})}

"
            from .agent import workflow_router
            result = await workflow_router(message, session_state)
            
            chunk_size = 64
            for i in range(0, len(result), chunk_size):
                chunk = result[i:i + chunk_size]
                payload = json.dumps({"delta": chunk, "agent": task_lead_agent.name})
                yield f"event: message
data: {payload}

"
                await asyncio.sleep(0.01)
            
            yield f"event: done
data: {json.dumps({'status': 'completed'})}

"
        except Exception as e:
            err_payload = json.dumps({"error": str(e)})
            yield f"event: error
data: {err_payload}

"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
