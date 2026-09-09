#!/usr/bin/env python3
"""
Fleet-Wide Test Runner for Utilities-Agents
Discovers and executes pytest suites across all 113 specialized utility agents,
providing structured test reporting, failure diagnostics, and domain-level aggregation.
"""

import sys
import os
import argparse
import subprocess
import time
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_DIR = REPO_ROOT / "agents"
VENV_PYTEST = REPO_ROOT / ".venv" / "bin" / "pytest"

def get_pytest_bin():
    if VENV_PYTEST.exists():
        return str(VENV_PYTEST)
    return "pytest"

def discover_agents(domain_filter=None, agent_filter=None):
    agent_dirs = []
    for domain_dir in sorted(AGENTS_DIR.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith("_") or domain_dir.name == "__pycache__":
            continue
        if domain_filter and domain_dir.name != domain_filter:
            continue
        for agent_dir in sorted(domain_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith("_") or agent_dir.name == "__pycache__":
                continue
            if agent_filter and agent_dir.name != agent_filter:
                continue
            tests_dir = agent_dir / "tests"
            if tests_dir.exists():
                agent_dirs.append((domain_dir.name, agent_dir.name, tests_dir))
    return agent_dirs

def run_tests_for_agents(agent_list, verbose=False):
    pytest_bin = get_pytest_bin()
    passed = []
    failed = []
    total = len(agent_list)
    
    print(f"\n=======================================================")
    print(f"  Fleet Test Runner: Executing across {total} agents")
    print(f"=======================================================\n")
    
    start_time = time.time()
    
    for i, (domain, agent, tests_path) in enumerate(agent_list, 1):
        rel_path = tests_path.relative_to(REPO_ROOT)
        cmd = [pytest_bin, "-q", str(tests_path)]
        
        proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
        
        if proc.returncode == 0:
            status = "PASS"
            passed.append((domain, agent))
            print(f"[{i:03d}/{total:03d}] [PASS] {domain}/{agent}")
        else:
            status = "FAIL"
            failed.append((domain, agent, proc.stdout + "\n" + proc.stderr))
            print(f"[{i:03d}/{total:03d}] [FAIL] {domain}/{agent}")
            if verbose:
                print(proc.stdout)
                print(proc.stderr)
    
    elapsed = time.time() - start_time
    print(f"\n=======================================================")
    print(f"  Test Execution Summary")
    print(f"=======================================================")
    print(f"  Total Agents Tested: {total}")
    print(f"  Passed:              {len(passed)} ({len(passed)/total*100:.1f}%)")
    print(f"  Failed:              {len(failed)}")
    print(f"  Elapsed Time:        {elapsed:.2f}s")
    print(f"=======================================================\n")
    
    if failed:
        print("Failures:")
        for domain, agent, output in failed:
            print(f"\n--- {domain}/{agent} ---")
            print(output[:500])
        return 1
    return 0

def main():
    parser = argparse.ArgumentParser(description="Fleet-Wide Test Runner for Utilities-Agents")
    parser.add_argument("--domain", type=str, help="Filter by specific sub-domain (e.g. asset_management)")
    parser.add_argument("--agent", type=str, help="Filter by specific agent name")
    parser.add_argument("--sample", type=int, help="Run only first N agents across each domain")
    parser.add_argument("--all", action="store_true", help="Run across all agents")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose test outputs")
    args = parser.parse_args()

    agents = discover_agents(domain_filter=args.domain, agent_filter=args.agent)
    
    if args.sample and not args.agent:
        # Group by domain and sample
        from collections import defaultdict
        grouped = defaultdict(list)
        for d, a, t in agents:
            grouped[d].append((d, a, t))
        sampled = []
        for d, items in grouped.items():
            sampled.extend(items[:args.sample])
        agents = sampled

    if not agents:
        print("No matching agents found.")
        sys.exit(1)

    exit_code = run_tests_for_agents(agents, verbose=args.verbose)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
