from .agent import agent
from google.adk.apps.app import App

app = App(name=agent.name, root_agent=agent)
