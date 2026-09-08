from google.adk.apps.app import App
from .agent import task_lead_agent

app = App(name=task_lead_agent.name, root_agent=task_lead_agent)
