import subprocess
import os
import sys
from pathlib import Path
import concurrent.futures
import requests
import json
import time

def deploy_agent(domain_name, agent_name, project_id, region):
    agent_path = f"agents/{domain_name}/{agent_name}"
    display_name = agent_name.replace("_", " ").title()
    
    print(f"🚀 Deploying {agent_name} ({region})...")
    cmd = [
        ".venv/bin/adk", "deploy", "agent_engine", agent_path,
        "--project", project_id,
        "--region", region,
        "--display_name", display_name
    ]
    
    try:
        res = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ Successfully deployed {agent_name} ({region})")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to deploy {agent_name}: {e.stderr if e.stderr else str(e)}")
        return False

def main():
    project_id = "utilities-agents"
    agents_dir = Path("agents")
    
    # Collect all agents
    all_agents = []
    for domain_dir in sorted(agents_dir.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith(("_", ".")):
            continue
        for agent_dir in sorted(domain_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith(("_", ".")) or "tmp" in agent_dir.name:
                continue
            all_agents.append((domain_dir.name, agent_dir.name))

    # Prioritize master orchestrator first
    all_agents.sort(key=lambda x: (0 if x[0] == "master_orchestrator" else 1, x[0], x[1]))

    print(f"Starting deployment for {len(all_agents)} agents in us-central1...")
    tasks = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for idx, (dom, ag) in enumerate(all_agents):
            region = "us-central1"
            tasks.append(executor.submit(deploy_agent, dom, ag, project_id, region))
            
        concurrent.futures.wait(tasks)

    print("\n--- Deployments complete. Registering all agents to Gemini Enterprise App ---")
    subprocess.run([sys.executable, "scripts/register_to_gemini_enterprise.py"], check=False)
    print("All tasks finished successfully!")

if __name__ == "__main__":
    main()
