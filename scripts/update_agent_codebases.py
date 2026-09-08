#!/usr/bin/env python3
"""
update_agent_codebases.py

Updates manifest.yaml, agent.py, and instructions/persona.md across all 113 agents
with their tailored business-purpose descriptions from config.agent_descriptions.
"""

import json
import re
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from config.agent_descriptions import AGENT_DESCRIPTIONS

def update_agent(domain: str, agent_id: str, desc: str):
    agent_dir = REPO_ROOT / "agents" / domain / agent_id
    if not agent_dir.exists():
        print(f"⚠️ Directory not found: {agent_dir}")
        return False

    # 1. Update manifest.yaml
    m_path = agent_dir / "manifest.yaml"
    if m_path.exists():
        m_content = m_path.read_text(encoding="utf-8")
        # Escaping quotes inside desc if any
        clean_desc = desc.replace('"', '\\"')
        if "description:" in m_content:
            m_content = re.sub(r'description:\s*.*', f'description: "{clean_desc}"', m_content)
        else:
            m_content = m_content.strip() + f'\ndescription: "{clean_desc}"\n'
        m_path.write_text(m_content, encoding="utf-8")

    # 2. Update agent.py
    a_path = agent_dir / "agent.py"
    if a_path.exists():
        a_content = a_path.read_text(encoding="utf-8")
        clean_desc = desc.replace('"', '\\"')
        if "description=" in a_content:
            a_content = re.sub(r'description\s*=\s*([\"\'\w\s\.\,\-]+),', f'description="{clean_desc}",', a_content)
        else:
            a_content = re.sub(
                r'(agent = Agent\(\s*name=[\"\'\w]+,\s*model=[\"\'\-\.\w]+,)',
                f'\\1\n    description="{clean_desc}",',
                a_content
            )
        a_path.write_text(a_content, encoding="utf-8")

    # 3. Update instructions/persona.md
    p_path = agent_dir / "instructions" / "persona.md"
    if p_path.exists():
        p_content = p_path.read_text(encoding="utf-8")
        p_content = re.sub(
            r'Your primary business purpose.*',
            f'Your primary business purpose: {desc}',
            p_content
        )
        p_path.write_text(p_content, encoding="utf-8")

    return True

def main():
    cat_path = REPO_ROOT / "web" / "catalog.json"
    if not cat_path.exists():
        print("❌ web/catalog.json not found!")
        return

    with open(cat_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    updated_count = 0
    for item in catalog:
        agent_id = item["id"]
        domain = item["domain"]
        desc = AGENT_DESCRIPTIONS.get(agent_id, item.get("description", ""))
        if update_agent(domain, agent_id, desc):
            updated_count += 1

    print(f"✅ Successfully updated {updated_count}/{len(catalog)} agent codebases with business-purpose descriptions!")

if __name__ == "__main__":
    main()
