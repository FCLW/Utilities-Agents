#!/usr/bin/env python3
import os
import re
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
AGENTS_DIR = BASE_DIR / "agents"
CONFIG_DIR = BASE_DIR / "config"

REQUIREMENTS_CONTENT = """google-cloud-aiplatform>=1.126.1
google-adk>=1.18.0
google-cloud-modelarmor>=0.7.0
google-cloud-logging>=3.11.0
google-cloud-trace>=1.15.0
google-cloud-monitoring>=2.21.0
opentelemetry-api>=1.25.0
opentelemetry-sdk>=1.25.0
opentelemetry-exporter-otlp-proto-http>=1.25.0
opentelemetry-exporter-gcp-trace>=1.7.0
opentelemetry-instrumentation-fastapi>=0.46b0
"""

ENV_CONTENT = """GOOGLE_CLOUD_AGENT_ENGINE_ENABLE_TELEMETRY=true
ADK_CAPTURE_MESSAGE_CONTENT_IN_SPANS=false
OTEL_INSTRUMENTATION_GENAI_CAPTURE_MESSAGE_CONTENT=NO_CONTENT
LOG_LEVEL=INFO
"""

def process_agent(agent_dir: Path):
    agent_name = agent_dir.name
    agent_config_dir = agent_dir / "config"
    agent_config_dir.mkdir(parents=True, exist_ok=True)

    # 1. Copy config files
    shutil.copy2(CONFIG_DIR / "settings.py", agent_config_dir / "settings.py")
    shutil.copy2(CONFIG_DIR / "model_armor.py", agent_config_dir / "model_armor.py")
    shutil.copy2(CONFIG_DIR / "telemetry.py", agent_config_dir / "telemetry.py")

    # 2. Update requirements.txt
    (agent_dir / "requirements.txt").write_text(REQUIREMENTS_CONTENT)

    # 3. Update .env
    (agent_dir / ".env").write_text(ENV_CONTENT)

    # 4. Update agent.py
    agent_file = agent_dir / "agent.py"
    if agent_file.exists():
        content = agent_file.read_text()
        
        # Check if telemetry already added
        if "get_telemetry_callbacks" not in content:
            # Locate armor_callbacks block
            old_block = """except ImportError:
        armor_callbacks = {}"""
            new_block = """except ImportError:
        armor_callbacks = {}

try:
    from .config.telemetry import get_telemetry_callbacks, combine_agent_callbacks
except ImportError:
    try:
        from config.telemetry import get_telemetry_callbacks, combine_agent_callbacks
    except ImportError:
        def get_telemetry_callbacks(name): return {}
        def combine_agent_callbacks(*dicts):
            c = {}
            for d in dicts:
                if d: c.update(d)
            return c

telemetry_callbacks = get_telemetry_callbacks(agent_name=""" + f'"{agent_name}")' + """
callbacks = combine_agent_callbacks(armor_callbacks, telemetry_callbacks)"""
            
            if old_block in content:
                content = content.replace(old_block, new_block, 1)
                # Replace **armor_callbacks with **callbacks
                content = content.replace("**armor_callbacks", "**callbacks")
                agent_file.write_text(content)

    # 5. Update fast_api_app.py
    fastapi_file = agent_dir / "fast_api_app.py"
    if fastapi_file.exists():
        content = fastapi_file.read_text()
        if "setup_telemetry" not in content:
            old_block = """try:
    from .config.model_armor import get_model_armor_plugins
    plugins = get_model_armor_plugins()
except ImportError:
    try:
        from config.model_armor import get_model_armor_plugins
        plugins = get_model_armor_plugins()
    except ImportError:
        plugins = []"""
            
            new_block = """try:
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

plugins = armor_plugins + telemetry_plugins"""
            if old_block in content:
                content = content.replace(old_block, new_block, 1)
                fastapi_file.write_text(content)

def main(target_agent=None):
    count = 0
    for domain_dir in sorted(AGENTS_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith(('.', '_')):
            continue
        for agent_dir in sorted(domain_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith(('.', '_')):
                continue
            if target_agent and agent_dir.name != target_agent:
                continue
            process_agent(agent_dir)
            count += 1
    print(f"Processed {count} agents successfully.")

if __name__ == '__main__':
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else None
    main(target)
