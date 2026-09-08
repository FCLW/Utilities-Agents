import os
import shutil
import argparse
from pathlib import Path

def scaffold_agent(domain: str, agent_id: str, agent_name: str):
    base_dir = Path("agents") / domain / agent_id
    template_dir = Path("agents") / "_template"
    
    if not template_dir.exists():
        print(f"Error: Template directory {template_dir} does not exist.")
        return

    if base_dir.exists():
        print(f"Warning: Directory {base_dir} already exists. Overwriting...")
        shutil.rmtree(base_dir)
        
    shutil.copytree(template_dir, base_dir)
    
    # Walk through the copied directory and replace template variables
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            file_path = Path(root) / file
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                new_content = content.replace("{{AGENT_ID}}", agent_id)
                new_content = new_content.replace("{{AGENT_NAME}}", agent_name)
                new_content = new_content.replace("{{DOMAIN}}", domain)
                
                if content != new_content:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_content)
            except UnicodeDecodeError:
                pass # Skip non-text files

    print(f"✅ Scaffolded agent '{agent_name}' ({agent_id}) in {base_dir} from template")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scaffold a new enterprise agent.")
    parser.add_argument("domain", help="The industry domain (e.g., energy, retail)")
    parser.add_argument("agent_id", help="The unique agent ID (e.g., energy-grid-ops-01)")
    parser.add_argument("agent_name", help="The human-readable agent name (e.g., 'Grid Operations Agent')")
    
    args = parser.parse_args()
    scaffold_agent(args.domain, args.agent_id, args.agent_name)
