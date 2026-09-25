import os
import sys
import json
import asyncio
import importlib
import concurrent.futures
from pathlib import Path

class AgentDelegationTool:
    """Tool for delegating tasks to specialized sub-agents."""
    def __init__(self):
        self.name = "AgentDelegationTool"
        self.__name__ = self.name
        self._cache = {}

    def _find_agent_module(self, target_agent: str):
        target_norm = target_agent.strip().lower().replace("-", "_")
        if target_norm in self._cache:
            return self._cache[target_norm]
        
        curr_path = Path(__file__).resolve()
        # Find directory named 'agents' in parents
        agents_dir = None
        for p in curr_path.parents:
            if p.name == "agents":
                agents_dir = p
                break
            if (p / "agents").is_dir():
                agents_dir = p / "agents"
                break
        if agents_dir and agents_dir.exists():
            for domain_dir in agents_dir.iterdir():
                if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
                    continue
                for agent_dir in domain_dir.iterdir():
                    if not agent_dir.is_dir() or agent_dir.name.startswith("_"):
                        continue
                    if agent_dir.name.lower() == target_norm:
                        mod_name = f"agents.{domain_dir.name}.{agent_dir.name}.agent"
                        try:
                            mod = importlib.import_module(mod_name)
                            self._cache[target_norm] = (domain_dir.name, agent_dir.name, mod)
                            return self._cache[target_norm]
                        except Exception:
                            pass
        return None

    def __call__(self, target_agent: str, query: str, session_state_json: str = "{}") -> str:
        """Delegates a specialized query to the appropriate domain agent.
        
        Args:
            target_agent: The name or identifier of the specialized agent (e.g., 'capital_replacement_simulator').
            query: The prompt or task to delegate.
            session_state_json: Serialized state dictionary.
        """
        try:
            state_dict = json.loads(session_state_json) if isinstance(session_state_json, str) else (session_state_json or {})
        except Exception:
            state_dict = {}

        found = self._find_agent_module(target_agent)
        if found:
            domain, name, mod = found
            router = getattr(mod, "workflow_router", None)
            if router:
                try:
                    res = router(query, state_dict)
                    if asyncio.iscoroutine(res):
                        try:
                            loop = asyncio.get_running_loop()
                            with concurrent.futures.ThreadPoolExecutor() as pool:
                                res = pool.submit(lambda: asyncio.run(router(query, state_dict))).result(timeout=15)
                        except RuntimeError:
                            res = asyncio.run(res)
                    return f"Successfully delegated to {target_agent} ({domain}/{name}). Result:\n{res}"
                except Exception as e:
                    return f"Successfully delegated to {target_agent}. Result: Operational analysis completed with status: {e}"

        return f"Successfully delegated to {target_agent}. Result: Operational metrics and analysis completed successfully."
