import subprocess
import os
import sys
from pathlib import Path
import concurrent.futures

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings

import shutil

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


def deploy_agent(domain_name, agent_name, project_id, region):
    agent_path = f"agents/{domain_name}/{agent_name}"
    display_name = agent_name.replace("_", " ").title()
    adk_bin = get_adk_binary()
    
    print(f"Deploying {agent_name} to Agent Engine...")
    try:
        # Run adk deploy agent_engine
        subprocess.run([
            adk_bin, "deploy", "agent_engine", agent_path,
            "--project", project_id,
            "--region", region,
            "--display_name", display_name,
            "--extra_packages", "config"
        ], check=True, capture_output=True)
        print(f"✅ Successfully deployed {agent_name} to Agent Engine")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to deploy {agent_name}: {e.stderr.decode() if e.stderr else str(e)}")


def deploy_agents():
    project_id = settings.gcp_project_id
    region = settings.gcp_region
    
    agents_dir = Path("agents")
    if not agents_dir.exists():
        return
        
    tasks = []
    # Test on just one agent first to verify it works without blowing up the project quota
    # with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    #     for domain_dir in agents_dir.iterdir():
    #         if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
    #             continue
    #         for agent_dir in domain_dir.iterdir():
    #             if not agent_dir.is_dir():
    #                 continue
    #             
    #             tasks.append(executor.submit(
    #                 deploy_agent, domain_dir.name, agent_dir.name, project_id, region
    #             ))
    #             
    #     concurrent.futures.wait(tasks)

if __name__ == "__main__":
    deploy_agents()
