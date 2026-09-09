import sys
from pathlib import Path
import importlib
import pytest
import pytest_asyncio
from unittest.mock import MagicMock
import types

repo_root = Path(__file__).resolve().parents[5]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

parts = Path(__file__).resolve().parts
agent_name = parts[-4]
domain_name = parts[-5]
module_path = f"agents.{domain_name}.{agent_name}.agent"
worker_path = f"agents.{domain_name}.{agent_name}.sub_agents.worker_agent"

agent_mod = importlib.import_module(module_path)
worker_mod = importlib.import_module(worker_path)

if 'app' not in sys.modules:
    sys.modules['app'] = types.ModuleType('app')
if 'app.sub_agents' not in sys.modules:
    sys.modules['app.sub_agents'] = types.ModuleType('app.sub_agents')
sys.modules['app.agent'] = agent_mod
sys.modules['app.sub_agents.worker_agent'] = worker_mod

workflow_router = getattr(agent_mod, 'workflow_router', None)

@pytest.mark.asyncio
async def test_a2a_workflow_critic_gate(monkeypatch):
    class MockResponse:
        def __init__(self, content):
            self.content = content
            
    mock_worker = MagicMock(return_value=MockResponse("Customer John Doe at 123 Main St has a bad meter. I think we should replace it."))
    sanitized_table = "| Metric | Status |\n|---|---|\n| Meter Issue | Bad Meter |"
    mock_critic = MagicMock(return_value=MockResponse(sanitized_table))
    
    monkeypatch.setattr(agent_mod, "worker_agent", mock_worker)
    monkeypatch.setattr(agent_mod, "critic_agent", mock_critic)
    if 'app.agent' in sys.modules:
        monkeypatch.setattr(sys.modules['app.agent'], "worker_agent", mock_worker)
        monkeypatch.setattr(sys.modules['app.agent'], "critic_agent", mock_critic)
    
    result = workflow_router("Check meter status for customer CUST-1000")
    if hasattr(result, '__await__'):
        result = await result
    
    mock_worker.assert_called_once()
    mock_critic.assert_called_once()
    assert "John Doe" not in result
    assert "123 Main St" not in result
    assert "Markdown" in mock_critic.call_args[0][0] or "format this" in mock_critic.call_args[0][0]
    assert result == sanitized_table

@pytest.mark.asyncio
async def test_context_passing():
    from app.sub_agents.worker_agent import worker_agent
    assert worker_agent is not None
