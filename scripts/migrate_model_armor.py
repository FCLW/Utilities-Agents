#!/usr/bin/env python3
"""Batch migration script to enable Model Armor across all 113 agents in Utilities-Agents.

Updates:
1. fast_api_app.py: Adds ModelArmorPlugin to adk_app = App(..., plugins=plugins)
2. __init__.py: Adds ModelArmorPlugin to app = App(..., plugins=plugins)
3. agent.py: Adds Model Armor before_model_callback and after_model_callback to Agent(..., **armor_callbacks)
"""

import os
import re
import py_compile
from pathlib import Path

BASE_DIR = Path("agents").resolve()

def update_fast_api_app(file_path: Path, dry_run: bool = False) -> bool:
    content = file_path.read_text(encoding="utf-8")
    if "get_model_armor_plugins" in content:
        return False  # Already updated

    # Pattern for adk_app = App(...)
    pattern = r"adk_app\s*=\s*App\(([^)]+)\)"
    match = re.search(pattern, content)
    if not match:
        print(f"  [WARN] Could not find adk_app = App(...) in {file_path}")
        return False

    orig_args = match.group(1).strip()
    if "plugins=" in orig_args:
        new_app_call = f"adk_app = App({orig_args})"
    else:
        new_app_call = f"adk_app = App({orig_args}, plugins=plugins)"

    import_block = (
        "try:\n"
        "    from config.model_armor import get_model_armor_plugins\n"
        "    plugins = get_model_armor_plugins()\n"
        "except ImportError:\n"
        "    plugins = []\n\n"
    )

    # Insert import block before app = FastAPI(...)
    if "app = FastAPI" in content:
        content = content.replace("app = FastAPI", import_block + "app = FastAPI", 1)
    else:
        content = import_block + content

    content = re.sub(pattern, new_app_call, content, count=1)

    if not dry_run:
        file_path.write_text(content, encoding="utf-8")
        py_compile.compile(str(file_path), doraise=True)
    return True


def update_init_py(file_path: Path, dry_run: bool = False) -> bool:
    content = file_path.read_text(encoding="utf-8")
    if "get_model_armor_plugins" in content:
        return False  # Already updated

    pattern = r"app\s*=\s*App\(([^)]+)\)"
    match = re.search(pattern, content)
    if not match:
        print(f"  [WARN] Could not find app = App(...) in {file_path}")
        return False

    orig_args = match.group(1).strip()
    if "plugins=" in orig_args:
        new_app_call = f"app = App({orig_args})"
    else:
        new_app_call = f"app = App({orig_args}, plugins=plugins)"

    import_block = (
        "try:\n"
        "    from config.model_armor import get_model_armor_plugins\n"
        "    plugins = get_model_armor_plugins()\n"
        "except ImportError:\n"
        "    plugins = []\n"
    )

    # Insert import block
    content = f"from google.adk.apps.app import App\n{import_block}" + re.sub(r"from google\.adk\.apps\.app import App\s*", "", content)
    content = re.sub(pattern, new_app_call, content, count=1)

    if not dry_run:
        file_path.write_text(content, encoding="utf-8")
        py_compile.compile(str(file_path), doraise=True)
    return True


def update_agent_py(file_path: Path, dry_run: bool = False) -> bool:
    content = file_path.read_text(encoding="utf-8")
    if "armor_callbacks" in content:
        return False  # Already updated

    # Insert armor_callbacks import after settings initialization
    callback_import_block = (
        "\ntry:\n"
        "    from config.model_armor import get_model_armor_callbacks\n"
        "    armor_callbacks = get_model_armor_callbacks()\n"
        "except ImportError:\n"
        "    armor_callbacks = {}\n"
    )

    if "settings = Settings()" in content:
        content = content.replace("settings = Settings()", "settings = Settings()" + callback_import_block, 1)
    else:
        content = callback_import_block + content

    # Add **armor_callbacks to agent = Agent(...)
    # Find agent = Agent(...)
    pattern = r"(agent\s*=\s*Agent\s*\([\s\S]*?)(\n\))"
    match = re.search(pattern, content)
    if match:
        prefix = match.group(1)
        suffix = match.group(2)
        if "**armor_callbacks" not in prefix:
            new_agent_block = prefix.rstrip() + ",\n    **armor_callbacks\n)"
            content = content[:match.start()] + new_agent_block + content[match.end():]
    else:
        print(f"  [WARN] Could not find agent = Agent(...) in {file_path}")
        return False

    if not dry_run:
        file_path.write_text(content, encoding="utf-8")
        py_compile.compile(str(file_path), doraise=True)
    return True


def migrate_all(dry_run: bool = False):
    print(f"Running Model Armor Migration (dry_run={dry_run})...")
    fast_api_count = 0
    init_count = 0
    agent_count = 0

    for domain_dir in sorted(BASE_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith((".", "_")):
            continue

        for agent_dir in sorted(domain_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith((".", "_")):
                continue

            # 1. fast_api_app.py
            fast_api_file = agent_dir / "fast_api_app.py"
            if fast_api_file.exists():
                if update_fast_api_app(fast_api_file, dry_run=dry_run):
                    fast_api_count += 1

            # 2. __init__.py
            init_file = agent_dir / "__init__.py"
            if init_file.exists():
                if update_init_py(init_file, dry_run=dry_run):
                    init_count += 1

            # 3. agent.py
            agent_file = agent_dir / "agent.py"
            if agent_file.exists():
                if update_agent_py(agent_file, dry_run=dry_run):
                    agent_count += 1

    print(f"\nMigration completed:")
    print(f"  fast_api_app.py updated: {fast_api_count}")
    print(f"  __init__.py updated:     {init_count}")
    print(f"  agent.py updated:        {agent_count}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    migrate_all(dry_run=args.dry_run)

