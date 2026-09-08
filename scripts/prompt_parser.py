#!/usr/bin/env python3
"""
prompt_parser.py — Prompt Parser and Domain Resolver for Utilities Enterprise Agents.

Extracts 3 curated business prompts from an agent's README.md (from Sample Q&A or Example Questions)
or falls back to web/catalog.json.
"""

import json
from pathlib import Path
import re
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

def load_catalog_data() -> dict:
    catalog_file = REPO_ROOT / "web" / "catalog.json"
    if catalog_file.exists():
        try:
            with open(catalog_file, "r", encoding="utf-8") as f:
                agents = json.load(f)
                return {a["id"]: a for a in agents}
        except Exception:
            pass
    return {}

CATALOG_CACHE = None

def get_catalog_entry(agent_name: str) -> dict:
    global CATALOG_CACHE
    if CATALOG_CACHE is None:
        CATALOG_CACHE = load_catalog_data()
    return CATALOG_CACHE.get(agent_name, {})

def resolve_agent_domain(agent_name: str, repo_root: Path | None = None) -> str:
    """Resolves the sub-domain name for a given agent name."""
    if repo_root is None:
        repo_root = REPO_ROOT

    # 1. Try catalog entry
    entry = get_catalog_entry(agent_name)
    if entry and "domain" in entry:
        return entry["domain"]

    # 2. Try file system lookup in agents/<domain>/<agent_name>
    matching_dirs = list((repo_root / "agents").glob(f"*/{agent_name}"))
    if matching_dirs:
        return matching_dirs[0].parent.name

    raise ValueError(f"Could not find agent '{agent_name}' in repository under agents/*/{agent_name}")

def parse_agent_prompts(readme_path: Path, agent_name: str | None = None) -> list[str]:
    """Parses at least 3 curated prompts from an agent's README.md, sample_prompts.yaml, or catalog."""
    prompts = []

    if readme_path and readme_path.parent:
        yaml_p = readme_path.parent / "instructions" / "sample_prompts.yaml"
        if yaml_p.exists():
            try:
                with open(yaml_p, "r", encoding="utf-8") as yf:
                    yd = yaml.safe_load(yf) or {}
                    for p in yd.get("prompts", []) or yd.get("sample_prompts", []):
                        if p and isinstance(p, str) and p.strip() and p.strip() not in prompts:
                            prompts.append(p.strip())
            except Exception:
                pass

    if len(prompts) < 4 and readme_path.exists():
        content = readme_path.read_text(encoding="utf-8")

        # Pattern 1: **User:** "..." or **User Prompt:** "..."
        for p in re.findall(r'\*\*User(?: Prompt)?:\*\*\s*["“](.*?)["”]', content, re.MULTILINE):
            cleaned = p.strip()
            if cleaned and not cleaned.startswith("TODO") and cleaned not in prompts:
                prompts.append(cleaned)

        # Pattern 2: *Question:* "..." or **Question:** "..."
        for p in re.findall(r'[\*\_]{1,2}Question:[\*\_]{1,2}\s*["“](.*?)["”]', content, re.MULTILINE):
            cleaned = p.strip()
            if cleaned and not cleaned.startswith("TODO") and cleaned not in prompts:
                prompts.append(cleaned)

        # Pattern 3: Numbered or bulleted example questions
        ex_match = re.search(r'##\s+(?:(?:\d+\.\s+)?(?:Real\s+)?Example Questions).*?(?=\n##\s+|\Z)', content, re.DOTALL | re.IGNORECASE)
        if ex_match:
            for p in re.findall(r'(?:^\s*(?:\d+\.|\-)\s*["“](.*?)["”])', ex_match.group(0), re.MULTILINE):
                cleaned = p.strip()
                if cleaned and not cleaned.startswith("TODO") and cleaned not in prompts:
                    prompts.append(cleaned)

    # Fallback to catalog prompts if less than 4
    if len(prompts) < 4 and agent_name:
        entry = get_catalog_entry(agent_name)
        cat_prompts = entry.get("prompts", [])
        for cp in cat_prompts:
            if cp not in prompts:
                prompts.append(cp)

    # General domain-specific fallback prompts if still needed
    if len(prompts) < 4:
        clean_title = (agent_name or "Asset").replace("_", " ").title()
        prompts.extend([
            f"Analyze recent telemetry and operational performance metrics for {clean_title}.",
            f"Identify active anomalies, degradation signatures, and root-cause indicators.",
            f"Generate prioritized operational recommendations and preventive maintenance schedule.",
            f"Stage an authorized operational workflow and action plan for {clean_title}."
        ])

    return prompts[:4]

