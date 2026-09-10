"""FastAPI and ADK App serving entrypoint for Grid Optimization MAS."""

import asyncio
import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from google.adk.apps.app import App

from grid_optimization.agent import root_agent

app = FastAPI(title="Grid Optimization Master Orchestrator")
adk_app = App(name="grid_optimization", root_agent=root_agent)


@app.get("/healthz")
def healthz():
    return {"status": "ok", "agent": root_agent.name}


@app.post("/chat/stream")
async def chat_stream(request: dict):
    """Streams agent execution responses as Server-Sent Events (SSE)."""
    message = request.get("message") or request.get("prompt") or request.get("query") or ""

    async def event_generator():
        try:
            yield f"event: open\ndata: {json.dumps({'agent': root_agent.name})}\n\n"
            from grid_optimization.agent import get_grid_fleet_status
            fleet = get_grid_fleet_status()
            yield f"event: message\ndata: {json.dumps({'content': f'Grid Orchestrator ready. Active Personas: {fleet[\"fleet_summary\"][\"persona_count\"]}, Sub-Agents: {fleet[\"fleet_summary\"][\"sub_agent_count\"]}'})}\n\n"
            yield "event: close\ndata: [DONE]\n\n"
        except Exception as e:
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
