import os
import json
import subprocess
from pathlib import Path
import sys

try:
    import yaml
except ImportError:
    print("pyyaml is not installed. Please run: pip install pyyaml")
    sys.exit(1)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings

def build_catalog():
    agents_dir = Path("agents")
    catalog = []
    
    if not agents_dir.exists():
        print("No agents directory found.")
        return

    registry_path = Path("table_registry.yaml")
    registry = {}
    if registry_path.exists():
        with open(registry_path, 'r') as f:
            registry = yaml.safe_load(f) or {}

    for domain_dir in agents_dir.iterdir():
        if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
            continue
        for agent_dir in domain_dir.iterdir():
            if not agent_dir.is_dir():
                continue
                
            manifest_path = agent_dir / "manifest.yaml"
            prompts_path = agent_dir / "app" / "instructions" / "sample_prompts.yaml"
            readme_path = agent_dir / "README.md"
            
            if not manifest_path.exists():
                continue
                
            with open(manifest_path, 'r') as f:
                manifest = yaml.safe_load(f) or {}
                
            prompts = []
            if prompts_path.exists():
                with open(prompts_path, 'r') as f:
                    prompts_data = yaml.safe_load(f) or {}
                    prompts = prompts_data.get("prompts", [])
                    
            readme_content = ""
            if readme_path.exists():
                with open(readme_path, 'r') as f:
                    readme_content = f.read()
                    
            agent_id = manifest.get("agent_id", agent_dir.name)
            live_url = ""
            
            # Load tables from centralized registry
            agent_tables = []
            agent_reg = registry.get("agents", {}).get(agent_id, {})
            for dataset in agent_reg.get("datasets", []):
                for table in dataset.get("tables", []):
                    agent_tables.append(f"{dataset.get('dataset_id')}.{table.get('table_id')}")

            entry = {
                "id": agent_id,
                "name": manifest.get("name", agent_id),
                "display_name": manifest.get("display_name", agent_id),
                "domain": manifest.get("domain", domain_dir.name),
                "icon": manifest.get("icon", "robot"),
                "location": manifest.get("location", ""),
                "description": manifest.get("description", ""),
                "prompts": prompts,
                "tables": agent_tables if agent_tables else manifest.get("tables", []),
                "demo_mp4": f"demos/{domain_dir.name}/{agent_id}.mp4",
                "demo_html": f"demos/{domain_dir.name}/{agent_id}.html",
                "spec_url": f"readmes/{domain_dir.name}/{agent_id}.md",
                "readme": readme_content,
                "live_url": live_url
            }
            catalog.append(entry)
            
    web_dir = Path("web")
    web_dir.mkdir(exist_ok=True)
    
    out_path = web_dir / "catalog.json"
    with open(out_path, 'w') as f:
        json.dump(catalog, f, indent=2)
        
    print(f"Built catalog with {len(catalog)} agents at {out_path}")

if __name__ == "__main__":
    build_catalog()
