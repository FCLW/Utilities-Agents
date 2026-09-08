from google.adk.apps.app import App
try:
    from .config.model_armor import get_model_armor_plugins
    plugins = get_model_armor_plugins()
except ImportError:
    try:
        from config.model_armor import get_model_armor_plugins
        plugins = get_model_armor_plugins()
    except ImportError:
        plugins = []
from .agent import agent
app = App(name=agent.name, root_agent=agent, plugins=plugins)
