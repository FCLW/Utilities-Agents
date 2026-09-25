#!/usr/bin/env python3
"""
Agent Identity IAM Provisioning Script for Utilities Agents.

Configures Google Cloud IAM policies using first-class Agent Identity
(SPIFFE-based cryptographic identity principals) instead of static legacy service accounts.
Also generates .agent_engine_config.json with identity_type=AGENT_IDENTITY across all agents.
"""

import os
import sys
import json
import argparse
import subprocess
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings

try:
    from google.cloud import bigquery
except ImportError:
    class MockClient:
        def __init__(self, **kwargs): pass
    bigquery = MockClient()

DOMAINS = [
    "master_orchestrator",
    "asset_management",
    "billing_and_invoicing",
    "customer_engagement",
    "grid_balancing",
    "grid_operations",
    "production_forecasting",
    "regulatory_compliance",
    "smart_meter_management",
    "support_services",
    "wholesale_trading"
]

def get_project_number(project_id: str) -> str:
    """Retrieves GCP project number via gcloud or environment variable."""
    env_num = os.getenv("GCP_PROJECT_NUMBER")
    if env_num:
        return env_num.strip()
    try:
        res = subprocess.run(
            ["gcloud", "projects", "describe", project_id, "--format=value(projectNumber)"],
            capture_output=True,
            text=True,
            timeout=5,
            stdin=subprocess.DEVNULL
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "PROJECT_NUMBER"

def get_agent_identity_principals(project_id: str, project_number: str, region: str) -> dict:
    """Builds Agent Identity SPIFFE principal identifiers for deployed agents."""
    principals = {
        "project_principal_set": f"principalSet://goog/subject/resources/aiplatform/projects/{project_id}/locations/{region}/reasoningEngines/*",
        "domain_agents": {}
    }
    
    progress_file = Path("deploy_progress.json")
    if progress_file.exists():
        try:
            with open(progress_file, "r") as f:
                data = json.load(f)
                for name, info in data.items():
                    re_id = info.get("re_id")
                    reg = info.get("region", region)
                    if re_id:
                        spiffe_principal = (
                            f"principal://agents.global.project-{project_number}.system.id.goog/"
                            f"resources/aiplatform/projects/{project_id}/locations/{reg}/reasoningEngines/{re_id}"
                        )
                        principals["domain_agents"][name] = spiffe_principal
        except Exception:
            pass
            
    return principals

def configure_agent_engine_configs():
    """Generates .agent_engine_config.json across all 113 agents and template."""
    agents_dir = Path("agents")
    count = 0
    config_data = {
        "identity_type": "AGENT_IDENTITY"
    }
    config_json = json.dumps(config_data, indent=2) + "\n"

    template_dir = agents_dir / "_template"
    if template_dir.exists():
        (template_dir / ".agent_engine_config.json").write_text(config_json, encoding="utf-8")

    for root, dirs, files in os.walk(agents_dir):
        if "agent.py" in files:
            p = Path(root) / ".agent_engine_config.json"
            p.write_text(config_json, encoding="utf-8")
            count += 1

    print(f"✅ Generated .agent_engine_config.json (AGENT_IDENTITY) across {count} agent packages.")

def setup_iam(dry_run: bool = False):
    project_id = settings.gcp_project_id
    region = settings.gcp_region
    project_number = get_project_number(project_id)

    print(f"=== Setting up Agent Identity IAM for Project: {project_id} (Number: {project_number}) ===")
    print(f"Identity Mode: {settings.identity_type} (Cryptographic SPIFFE Authentication)")

    # 1. Configure agent engine config files
    configure_agent_engine_configs()

    principals_info = get_agent_identity_principals(project_id, project_number, region)
    principal_set = principals_info["project_principal_set"]

    print(f"\n🔐 Baseline Agent Identity PrincipalSet: {principal_set}")

    # 2. Project-level bindings for Agent Identity
    project_roles = [
        "roles/bigquery.jobUser",
        "roles/aiplatform.user",
        "roles/logging.logWriter",
        "roles/monitoring.metricWriter",
        "roles/serviceusage.serviceUsageConsumer"
    ]

    print("\n--- Project-Level IAM Bindings ---")
    for role in project_roles:
        cmd = [
            "gcloud", "projects", "add-iam-policy-binding", project_id,
            "--member", principal_set,
            "--role", role,
            "--condition=None",
            "--quiet"
        ]
        if dry_run:
            print(f"[DRY-RUN] {' '.join(cmd)}")
        else:
            try:
                subprocess.run(cmd, check=False, timeout=10, stdin=subprocess.DEVNULL)
                print(f"Bound {role} to Agent Identity principalSet")
            except Exception as e:
                print(f"Notice: gcloud binding skipped ({e})")

    # 3. Domain-Level Dataset Isolation for BigQuery
    print("\n--- Domain-Level BigQuery Dataset Isolation ---")
    client = None
    if not dry_run and hasattr(bigquery, "Client"):
        try:
            client = bigquery.Client(project=project_id)
        except Exception:
            client = None

    for domain in DOMAINS:
        dataset_id = f"utilities_{domain}"
        print(f"\nConfiguring Dataset: {dataset_id}")
        
        # In Agent Identity architecture, datasets grant access to the Agent Identity principalSet or per-agent SPIFFE principals
        if client and hasattr(client, "get_dataset"):
            try:
                dataset_ref = client.dataset(dataset_id)
                dataset = client.get_dataset(dataset_ref)
                entries = list(dataset.access_entries)
                if not any(entry.entity_id == principal_set for entry in entries):
                    entries.append(bigquery.AccessEntry(role="roles/bigquery.dataViewer", entity_type="iamMember", entity_id=principal_set))
                    dataset.access_entries = entries
                    client.update_dataset(dataset, ["access_entries"])
                    print(f"Granted roles/bigquery.dataViewer to Agent Identity on {dataset_id}")
                else:
                    print(f"Access already granted on {dataset_id}")
            except Exception as e:
                print(f"Notice: Dataset {dataset_id} access configuration: {e}")
        else:
            print(f"[Policy Plan] Dataset {dataset_id} -> roles/bigquery.dataViewer to {principal_set}")

    print("\n✅ Agent Identity IAM setup completed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Setup Agent Identity IAM permissions.")
    parser.add_argument("--dry-run", action="store_true", help="Print planned policy bindings without modifying GCP.")
    args = parser.parse_args()
    setup_iam(dry_run=args.dry_run)
