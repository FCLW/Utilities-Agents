from google.adk import Agent
from pathlib import Path
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
from config.settings import settings
from .tools.bigquery_tool import BigQueryQueryTool
from .tools.search_tool import GoogleSearchTool
from .tools.visualizer import render_chart

instructions_dir = Path(__file__).parent / "instructions"

agent = Agent(
    name="{{agent_name}}",
    model=settings.llm_model_name,
    persona=instructions_dir / "persona.md",
    business_rules=instructions_dir / "business_rules.md",
    output_format=instructions_dir / "output_format.md",
    safety_guardrails=instructions_dir / "safety_guardrails.md",
    tools=[BigQueryQueryTool(), GoogleSearchTool(), render_chart],

