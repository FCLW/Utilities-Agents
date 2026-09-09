#!/usr/bin/env python3
"""
Batch Redeployment and Registration Script for Utilities-Agents
Deploys all agents with Model Armor guardrails to Vertex AI Agent Engine
and updates registrations in Gemini Enterprise.
"""

import os
import sys
import json
import time
import shutil
import subprocess
import concurrent.futures
from pathlib import Path
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings

def get_adk_binary() -> str:
    local_adk = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".venv", "bin", "adk"))
    if os.path.exists(local_adk):
        return local_adk
    if os.path.exists(".venv/bin/adk"):
        return os.path.abspath(".venv/bin/adk")
    which_adk = shutil.which("adk")
    if which_adk:
        return which_adk
    return "adk"


def get_auth_token() -> str:
    return subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()

def fetch_existing_reasoning_engines(project_id: str, regions: list[str]) -> dict:
    token = get_auth_token()
    headers = {'Authorization': f'Bearer {token}'}
    engines = {}
    for loc in regions:
        page_token = ''
        while True:
            url = f'https://{loc}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{loc}/reasoningEngines?pageSize=100'
            if page_token:
                url += f'&pageToken={page_token}'
            resp = requests.get(url, headers=headers).json()
            for re in resp.get('reasoningEngines', []):
                disp = re.get('displayName', '')
                re_id = re.get('name', '').split('/')[-1]
                update_time = re.get('updateTime', '')
                key = disp.lower().replace(' ', '_').replace('-', '_')
                engines[key] = {
                    'region': loc,
                    're_id': re_id,
                    'display_name': disp,
                    'update_time': update_time,
                    'resource_name': re.get('name')
                }
            page_token = resp.get('nextPageToken', '')
            if not page_token:
                break
    return engines

PROGRESS_FILE = Path("deploy_progress.json")

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_progress(progress: dict):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f, indent=2)

def deploy_single_agent(agent_info: dict, adk_bin: str, project_id: str) -> dict:
    agent_name = agent_info['agent_name']
    domain = agent_info['domain']
    region = agent_info['region']
    re_id = agent_info['re_id']
    display_name = agent_info['display_name']
    agent_path = f"agents/{domain}/{agent_name}"

    start_time = time.time()
    print(f"[{time.strftime('%X')}] 🚀 Deploying {agent_name} ({region}) [ID: {re_id}]...")

    cmd = [
        adk_bin, "deploy", "agent_engine", agent_path,
        "--project", project_id,
        "--region", region,
        "--display_name", display_name,
        "--agent_engine_id", re_id,
        "--extra_packages", "config",
        "--otel_to_cloud"
    ]

    max_attempts = 2
    for attempt in range(1, max_attempts + 1):
        try:
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0 or "Deploy failed:" in res.stdout or "Failed to deploy" in res.stdout:
                err_output = res.stderr or res.stdout or "Deployment returned non-zero or failure message"
                raise RuntimeError(err_output[-500:])
            elapsed = int(time.time() - start_time)
            print(f"[{time.strftime('%X')}] ✅ Successfully deployed {agent_name} in {elapsed}s")
            return {
                "agent_name": agent_name,
                "status": "SUCCESS",
                "region": region,
                "re_id": re_id,
                "elapsed": elapsed
            }
        except Exception as e:
            err_msg = str(e)[-500:]
            if attempt < max_attempts:
                print(f"[{time.strftime('%X')}] ⚠️ Attempt {attempt} failed for {agent_name}. Retrying in 10s... ({err_msg[:120]})")
                time.sleep(10)
            else:
                elapsed = int(time.time() - start_time)
                print(f"[{time.strftime('%X')}] ❌ Failed to deploy {agent_name} after {max_attempts} attempts: {err_msg[:200]}")
                return {
                    "agent_name": agent_name,
                    "status": "FAILED",
                    "region": region,
                    "re_id": re_id,
                    "error": err_msg,
                    "elapsed": elapsed
                }

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Batch deploy agents to Agent Engine with Model Armor")
    parser.add_argument("--workers", type=int, default=5, help="Number of concurrent deployment workers (default: 5)")
    parser.add_argument("--agent", type=str, default=None, help="Target a specific agent by name (e.g. utilities_master_orchestrator)")
    parser.add_argument("--dry-run", action="store_true", help="Print plan without executing deployments")
    parser.add_argument("--force", action="store_true", help="Redeploy all agents even if previously marked SUCCESS")
    parser.add_argument("--skip-ge-register", action="store_true", help="Skip registration to Gemini Enterprise at the end")
    args = parser.parse_args()

    project_id = settings.gcp_project_id
    regions = ["us-central1", "us-east4"]
    adk_bin = get_adk_binary()

    print(f"ADK Binary: {adk_bin}")
    print(f"Scanning GCP Reasoning Engines in {regions}...")
    gcp_engines = fetch_existing_reasoning_engines(project_id, regions)
    print(f"Found {len(gcp_engines)} Reasoning Engines in GCP.")

    # Collect local agents
    agents_dir = Path("agents")
    local_agents = []
    for root, dirs, files in os.walk(agents_dir):
        if "agent.py" in files and not root.startswith("agents/_template"):
            ag_name = os.path.basename(root)
            dom_name = os.path.basename(os.path.dirname(root))
            key = ag_name.lower().replace(" ", "_").replace("-", "_")
            if key in gcp_engines:
                info = gcp_engines[key]
                local_agents.append({
                    "agent_name": ag_name,
                    "domain": dom_name,
                    "region": info["region"],
                    "re_id": info["re_id"],
                    "display_name": info["display_name"],
                    "update_time": info["update_time"]
                })
            else:
                print(f"⚠️ Warning: Agent {ag_name} not found in GCP Reasoning Engines!")

    if args.agent:
        local_agents = [ag for ag in local_agents if ag["agent_name"] == args.agent]
        print(f"Filtered for single agent: {args.agent} (found {len(local_agents)})")

    # Sort master orchestrator first, then alphabetically
    local_agents.sort(key=lambda x: (0 if x["domain"] == "master_orchestrator" else 1, x["domain"], x["agent_name"]))

    progress = load_progress() if not args.force else {}

    # Check already deployed: if in progress and SUCCESS, or already updated today (e.g. capital_replacement_simulator)
    to_deploy = []
    already_done = []
    for ag in local_agents:
        name = ag["agent_name"]
        if name in progress and progress[name].get("status") == "SUCCESS":
            already_done.append(ag)
        else:
            to_deploy.append(ag)

    print(f"\n--- Deployment Plan ---")
    print(f"Total Agents: {len(local_agents)}")
    print(f"Already Deployed: {len(already_done)}")
    print(f"Remaining to Deploy: {len(to_deploy)}")

    if args.dry_run:
        print("\n[DRY RUN] Would deploy the following remaining agents:")
        for idx, ag in enumerate(to_deploy, 1):
            print(f"  {idx}. {ag['agent_name']} ({ag['region']}) -> ID: {ag['re_id']}")
        return

    if not to_deploy:
        print("All agents are already deployed!")
    else:
        print(f"\nLaunching parallel deployment with {args.workers} workers...")
        with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as executor:
            future_to_agent = {
                executor.submit(deploy_single_agent, ag, adk_bin, project_id): ag
                for ag in to_deploy
            }
            completed_count = 0
            for future in concurrent.futures.as_completed(future_to_agent):
                res = future.result()
                name = res["agent_name"]
                progress[name] = res
                save_progress(progress)
                completed_count += 1
                print(f"📊 Progress: [{completed_count}/{len(to_deploy)}] ({len(already_done) + completed_count}/{len(local_agents)} total)")

    if not args.skip_ge_register:
        print("\n--- Synchronizing Gemini Enterprise Registrations ---")
        python_bin = sys.executable
        res = subprocess.run([python_bin, "scripts/register_to_gemini_enterprise.py"], text=True)
        print("Registration process finished.")

    # Final summary
    successes = sum(1 for p in progress.values() if p.get("status") == "SUCCESS")
    failures = sum(1 for p in progress.values() if p.get("status") == "FAILED")
    print(f"\n=======================================================")
    print(f"Deployment Complete!")
    print(f"Total Successful: {successes} / {len(local_agents)}")
    if failures > 0:
        print(f"Failed Agents ({failures}): {[k for k, v in progress.items() if v.get('status') == 'FAILED']}")
    print(f"=======================================================")

if __name__ == "__main__":
    main()

