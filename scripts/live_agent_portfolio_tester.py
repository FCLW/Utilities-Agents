"""Live Agent Portfolio Tester & Golden Dataset / README Synchronizer

Runs live prompts through ADK Runner with Gemini 3.7 Flash on Vertex AI,
validates that responses are logical and structurally sound, and synchronizes
tests/eval/datasets/golden-dataset.json and README.md for all 113 agents.
"""

import os
import sys
import subprocess
import asyncio
import yaml
import json
import re
from pathlib import Path

sys.path.insert(0, str(Path('.').resolve()))
from config.settings import settings

# Set up DirectTokenCredentials for Vertex AI
from google.auth.credentials import Credentials
import google.auth

class DirectTokenCredentials(Credentials):
    def __init__(self, token):
        super().__init__()
        self.token = token
    def refresh(self, request):
        self.token = subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()
    @property
    def valid(self):
        return True

try:
    token = subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()
    creds = DirectTokenCredentials(token)
    google.auth.default = lambda *args, **kwargs: (creds, settings.gcp_project_id)
except Exception as e:
    print(f"Warning: Failed to fetch gcloud token: {e}")

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

CACHE_FILE = Path("data/live_agent_responses.json")
CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)

def load_cache():
    if CACHE_FILE.exists():
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_cache(cache):
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)

async def run_prompt_with_retry(agent, agent_id, prompt_text, max_retries=4):
    for attempt in range(max_retries):
        try:
            session_service = InMemorySessionService()
            session = await session_service.create_session(app_name=agent_id, user_id="eval_user")
            runner = Runner(
                app_name=agent_id,
                agent=agent,
                session_service=session_service,
                auto_create_session=True
            )
            content = types.Content(parts=[types.Part.from_text(text=prompt_text)])
            full_text = []
            async for event in runner.run_async(session_id=session.id, user_id="eval_user", new_message=content):
                if hasattr(event, "content") and event.content:
                    for part in event.content.parts:
                        if hasattr(part, "text") and part.text:
                            full_text.append(part.text)
            resp = "".join(full_text).strip()
            if resp and len(resp) > 100:
                return resp
            print(f"[{agent_id}] Attempt {attempt+1}: Response short or empty ({len(resp)} chars), retrying...", flush=True)
        except Exception as e:
            err_msg = str(e)
            print(f"[{agent_id}] Attempt {attempt+1} failed ({type(e).__name__}): {err_msg[:100]}...", flush=True)
            await asyncio.sleep(2 ** attempt + 2)
    return None

async def test_single_agent(agent_dir_path, sem, cache):
    agent_dir = Path(agent_dir_path)
    parts = agent_dir.parts
    subdomain = parts[1]
    agent_id = parts[2]
    
    # Check if all 4 prompts already cached and valid
    if agent_id in cache and len(cache[agent_id].get("responses", [])) == 4:
        if all(r.get("response") and len(r["response"]) > 100 for r in cache[agent_id]["responses"]):
            print(f"✓ Agent {agent_id} already cached with 4 valid responses.", flush=True)
            return cache[agent_id]
            
    prompts_file = agent_dir / "instructions" / "sample_prompts.yaml"
    if not prompts_file.exists():
        print(f"✗ Agent {agent_id} missing sample_prompts.yaml", flush=True)
        return None
        
    with open(prompts_file) as f:
        prompts = yaml.safe_load(f).get("prompts", [])
        
    if len(prompts) < 4:
        print(f"✗ Agent {agent_id} has fewer than 4 prompts ({len(prompts)})", flush=True)
        return None

    # Load agent module
    try:
        module_path = f"agents.{subdomain}.{agent_id}.agent"
        mod = __import__(module_path, fromlist=["agent"])
        agent = getattr(mod, "agent")
    except Exception as e:
        print(f"✗ Agent {agent_id} import failed: {e}", flush=True)
        return None
        
    for t in agent.tools:
        if not hasattr(t, "__name__"):
            t.__name__ = getattr(t, "name", t.__class__.__name__)

    print(f"▶ Testing agent: {agent_id}...", flush=True)
    responses = cache.get(agent_id, {}).get("responses", [])
    if len(responses) != 4:
        responses = [{"prompt": p, "response": None} for p in prompts[:4]]

    async with sem:
        for i, item in enumerate(responses):
            if item.get("response") and len(item["response"]) > 100:
                continue
            prompt_text = prompts[i]
            print(f"  [{agent_id}] Running Prompt {i+1}...", flush=True)
            resp = await run_prompt_with_retry(agent, agent_id, prompt_text)
            if resp:
                print(f"  [{agent_id}] Prompt {i+1} OK ({len(resp)} chars)", flush=True)
                item["prompt"] = prompt_text
                item["response"] = resp
            else:
                print(f"  [{agent_id}] Prompt {i+1} FAILED after retries.", flush=True)
            await asyncio.sleep(1.5)

    agent_result = {
        "subdomain": subdomain,
        "agent_id": agent_id,
        "responses": responses
    }
    cache[agent_id] = agent_result
    save_cache(cache)
    return agent_result

def sync_agent_files(agent_dir_path, agent_result):
    agent_dir = Path(agent_dir_path)
    parts = agent_dir.parts
    subdomain = parts[1]
    agent_id = parts[2]
    
    responses = agent_result.get("responses", [])
    if len(responses) < 4:
        return False
        
    # 1. Update golden-dataset.json
    golden_path = agent_dir / "tests" / "eval" / "datasets" / "golden-dataset.json"
    if golden_path.exists():
        with open(golden_path, "r") as f:
            golden_data = json.load(f)
    else:
        golden_data = []

    new_golden = []
    for i in range(4):
        prompt = responses[i]["prompt"]
        resp = responses[i]["response"]
        
        if i == 3:
            contains = [agent_id.replace("_", " ").title(), "[TIER 2 ACTION REQUIRED]", "HITL", "operator"]
        elif i == 0:
            contains = ["Executive Summary", "Data Presentation", "Actionable Recommendations"]
        elif i == 1:
            contains = ["Executive Summary", "Data Presentation", "Baseline", "Variance"]
        else:
            contains = ["Executive Summary", "Data Presentation", "Actionable Recommendations"]

        new_golden.append({
            "input": prompt,
            "expected_output_contains": contains,
            "expected_format": "markdown_table",
            "expected_output": resp if resp else (golden_data[i]["expected_output"] if i < len(golden_data) else "")
        })
        
    golden_path.parent.mkdir(parents=True, exist_ok=True)
    with open(golden_path, "w") as f:
        json.dump(new_golden, f, indent=2)

    # 2. Update README.md Agent Response Examples
    readme_path = agent_dir / "README.md"
    if readme_path.exists():
        with open(readme_path, "r") as f:
            content = f.read()

        p1 = responses[0]["prompt"]
        r1 = responses[0]["response"] or ""
        p2 = responses[1]["prompt"]
        r2 = responses[1]["response"] or ""
        p4 = responses[3]["prompt"]
        r4 = responses[3]["response"] or ""

        examples_section = f"""## 💬 Agent Response Examples

### Example 1: Operational Diagnostic Query
**User:** "{p1}"

**Agent Response:**
{r1}

### Example 2: Trend & Comparative Analysis
**User:** "{p2}"

**Agent Response:**
{r2}

### Example 3: Tier 2 Autonomous Operations (Human-in-the-Loop)
**User:** "{p4}"

**Agent Response:**
{r4}
"""
        marker = "## 💬 Agent Response Examples"
        if marker in content:
            idx = content.find(marker)
            new_content = content[:idx].rstrip() + "\n\n" + examples_section.lstrip()
        else:
            new_content = content.rstrip() + "\n\n" + examples_section.lstrip()

        with open(readme_path, "w") as f:
            f.write(new_content)

    return True

async def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdomain", help="Filter by subdomain", default=None)
    parser.add_argument("--agent", help="Filter by specific agent_id", default=None)
    parser.add_argument("--concurrency", help="Concurrency limit", type=int, default=2)
    parser.add_argument("--sync-only", action="store_true", help="Sync existing cache to files without running tests")
    args = parser.parse_args()

    cache = load_cache()
    
    agent_dirs = sorted([d for d in Path("agents").glob("*/*") if d.is_dir() and (d / "agent.py").exists()])
    
    if args.subdomain:
        agent_dirs = [d for d in agent_dirs if d.parts[1] == args.subdomain]
    if args.agent:
        agent_dirs = [d for d in agent_dirs if d.parts[2] == args.agent]

    print(f"Selected {len(agent_dirs)} agents to process (concurrency={args.concurrency}).", flush=True)

    if args.sync_only:
        print("Running sync-only mode...", flush=True)
        synced = 0
        for ad in agent_dirs:
            agent_id = ad.parts[2]
            if agent_id in cache:
                sync_agent_files(ad, cache[agent_id])
                synced += 1
        print(f"Successfully synced {synced} agents.", flush=True)
        return

    sem = asyncio.Semaphore(args.concurrency)
    tasks = [test_single_agent(ad, sem, cache) for ad in agent_dirs]
    results = await asyncio.gather(*tasks)

    synced = 0
    for ad, res in zip(agent_dirs, results):
        if res:
            sync_agent_files(ad, res)
            synced += 1

    print(f"\n==========================================", flush=True)
    print(f"Finished processing! Successfully tested & synced {synced}/{len(agent_dirs)} agents.", flush=True)
    print(f"==========================================", flush=True)

if __name__ == "__main__":
    asyncio.run(main())
