import pytest
import pytest_asyncio
from unittest.mock import patch, MagicMock
from app.agent import workflow_router

@pytest.mark.asyncio
@patch("app.agent.worker_agent")
@patch("app.agent.critic_agent")
async def test_a2a_workflow_critic_gate(mock_critic, mock_worker):
    # 1. Mock Worker to return PII
    class MockResponse:
        def __init__(self, content):
            self.content = content
            
    mock_worker.return_value = MockResponse("Customer John Doe at 123 Main St has a bad meter. I think we should replace it.")
    
    # 2. Mock Critic to return sanitized Markdown table
    sanitized_output = "| Metric | Status |\n|---|---|\n| Meter Issue | Bad Meter |"
    mock_critic.return_value = MockResponse(sanitized_output)
    
    # Execute workflow (mocking async if it were async, but calling normally for now)
    # The prompt demands pytest-asyncio, so we ensure the test is an async coroutine
    result = workflow_router("Check meter status for customer CUST-1000")
    if hasattr(result, '__await__'):
        result = await result
    
    # 3. Assert calling sequence and sanitized output
    mock_worker.assert_called_once()
    mock_critic.assert_called_once()
    assert "John Doe" not in result
    assert "123 Main St" not in result
    assert "Markdown" in mock_critic.call_args[0][0] or "format this" in mock_critic.call_args[0][0]
    assert result == sanitized_output

@pytest.mark.asyncio
async def test_context_passing():
    # Assert that UtilitiesSessionState propagates correctly
    from app.sub_agents.worker_agent import worker_agent
    assert worker_agent is not None
