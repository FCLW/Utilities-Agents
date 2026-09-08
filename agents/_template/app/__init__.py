from google.adk.apps.app import App
from .agent import agent

try:
    from config.model_armor import get_model_armor_plugins
    plugins = get_model_armor_plugins()
except ImportError:
    plugins = []

app = App(name=agent.name, root_agent=agent, plugins=plugins)

