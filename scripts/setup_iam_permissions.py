import subprocess
import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings

try:
    from google.cloud import bigquery
except ImportError:
    class MockClient:
        def __init__(self, **kwargs): pass
    "master_orchestrator": "orchestrator-sa",
    "asset_management": "asset-mgmt-sa",
    "billing_and_invoicing": "billing-sa",
    "customer_engagement": "customer-eng-sa",
    "grid_balancing": "grid-balance-sa",
    "grid_operations": "grid-ops-sa",
    "production_forecasting": "prod-forecast-sa",
    "regulatory_compliance": "compliance-sa",
    "smart_meter_management": "smart-meter-sa",
    "support_services": "support-sa",
    "wholesale_trading": "wholesale-sa"
}

def setup_iam():
    project_id = settings.gcp_project_id
    client = bigquery.Client(project=project_id)

    for domain, sa_name in DOMAIN_SA_MAP.items():
        sa_email = f"{sa_name}@{project_id}.iam.gserviceaccount.com"
        print(f"\n--- Processing Domain: {domain} ---")
        
        # 1. Create Service Account
        print(f"Creating SA: {sa_email}")
        subprocess.run([
            "gcloud", "iam", "service-accounts", "create", sa_name,
            "--project", project_id,
            "--display-name", f"{domain} Domain SA"
        ], check=False)

        # 2. Grant Project-Level Compute/Job Roles
        project_roles = ["roles/bigquery.jobUser", "roles/aiplatform.user"]
        for role in project_roles:
            subprocess.run([
                "gcloud", "projects", "add-iam-policy-binding", project_id,
                "--member", f"serviceAccount:{sa_email}",
                "--role", role,
                "--condition=None",
                "--quiet"
            ], check=False)
            
        # 3. Grant Strict Dataset-Level Access
        dataset_id = f"utilities_{domain}"
        try:
            dataset_ref = client.dataset(dataset_id)
            dataset = client.get_dataset(dataset_ref)
            
            entries = list(dataset.access_entries)
            # Check if already exists to avoid duplicates
            if not any(entry.entity_id == sa_email for entry in entries):
                entries.append(bigquery.AccessEntry(role="roles/bigquery.dataViewer", entity_type="userByEmail", entity_id=sa_email))
                dataset.access_entries = entries
                client.update_dataset(dataset, ["access_entries"])
                print(f"Granted exclusive dataset dataViewer access on {dataset_id}")
            else:
                print(f"Dataset access already granted for {dataset_id}")
        except Exception as e:
            print(f"Notice: Dataset {dataset_id} does not exist yet or error: {e}")

    print("\nDomain-Level IAM isolation setup complete.")

if __name__ == "__main__":
    setup_iam()
