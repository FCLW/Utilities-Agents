#!/usr/bin/env python3
"""
generate_demo_demo.py — Wrapper for record_agent_demo.py.
Preserves backwards compatibility for scripts invoking generate_demo_video.py.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.record_agent_demo import main

if __name__ == "__main__":
    main()
