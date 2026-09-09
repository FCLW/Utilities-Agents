#!/usr/bin/env python3
"""
High-throughput BigQuery Loader for Enterprise Utilities Multi-Agent Fleet
Truncates and loads golden-grounded synthetic records into `utilities_data.{agent_name}_logs`
and creates domain-scoped views in `utilities_{domain_name}.{agent_name}_logs` and `orchestrator.session_state`.
"""

import os
import sys
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings
from google.cloud import bigquery

DOMAIN_DATASET_MAP = {
    "asset_management": "utilities_asset_management",
    "billing_and_invoicing": "utilities_billing_and_invoicing",
    "customer_engagement": "utilities_customer_engagement",
    "grid_balancing": "utilities_grid_balancing",
    "grid_operations": "utilities_grid_operations",
    "production_forecasting": "utilities_production_forecasting",
    "regulatory_compliance": "utilities_regulatory_compliance",
    "smart_meter_management": "utilities_smart_meter_management",
    "support_services": "utilities_support_services",
    "wholesale_trading": "utilities_wholesale_trading",
    "master_orchestrator": "orchestrator",
}

def ensure_dataset(client, dataset_id, location):
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = location
    client.create_dataset(dataset, exists_ok=True)

def load_single_table(client, csv_path, table_full_id):
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
    )
    with open(csv_path, "rb") as source_file:
        job = client.load_table_from_file(source_file, table_full_id, job_config=job_config)
        job.result() # Wait for job completion
        
    table = client.get_table(table_full_id)
    return table_full_id, table.num_rows

def create_domain_views(client, domain_tables):
    print("\n--- Creating Domain Views ---")
    view_count = 0
    for domain_name, tables in domain_tables.items():
        domain_dataset = DOMAIN_DATASET_MAP.get(domain_name)
        if not domain_dataset:
            continue
        
        for agent_name in tables:
            src_table = f"`{settings.gcp_project_id}.utilities_data.{agent_name}_logs`"
            target_view = f"`{settings.gcp_project_id}.{domain_dataset}.{agent_name}_logs`"
            
            sql = f"CREATE OR REPLACE VIEW {target_view} AS SELECT * FROM {src_table};"
            try:
                client.query(sql).result()
                view_count += 1
            except Exception as e:
                print(f"Error creating view {target_view}: {e}")
                
        # For master orchestrator, also create orchestrator.session_state
        if domain_name == "master_orchestrator":
            src_table = f"`{settings.gcp_project_id}.utilities_data.utilities_master_orchestrator_logs`"
            target_view = f"`{settings.gcp_project_id}.orchestrator.session_state`"
            sql = f"CREATE OR REPLACE VIEW {target_view} AS SELECT * FROM {src_table};"
            try:
                client.query(sql).result()
                view_count += 1
                print(f"Created view {target_view}")
            except Exception as e:
                print(f"Error creating view {target_view}: {e}")

    print(f"Successfully configured {view_count} domain views across all 10 business domains and Master Orchestrator.")

def load_data(max_workers=10):
    start_time = time.time()
    client = bigquery.Client(project=settings.gcp_project_id)
    try:
        location = client.get_dataset("utilities_data").location
    except Exception:
        location = "us-central1"
    
    print(f"Project: {settings.gcp_project_id}")
    print(f"Location: {location}")
    print("Ensuring datasets exist...")
    
    # 1. Primary dataset
    ensure_dataset(client, f"{settings.gcp_project_id}.utilities_data", location)
    
    # 2. Domain datasets
    for ds_name in DOMAIN_DATASET_MAP.values():
        ensure_dataset(client, f"{settings.gcp_project_id}.{ds_name}", location)
    
    print("Datasets initialized.")

    agents_dir = Path("agents")
    tasks = []
    domain_tables = {}

    for domain_dir in sorted(agents_dir.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
            continue
        domain_name = domain_dir.name
        domain_tables[domain_name] = []

        for agent_dir in sorted(domain_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith("_"):
                continue
            agent_name = agent_dir.name
            csv_file = agent_dir / "synthetic_data" / "mock_records.csv"
            if not csv_file.exists():
                continue

            table_full_id = f"{settings.gcp_project_id}.utilities_data.{agent_name}_logs"
            tasks.append((csv_file, table_full_id, agent_name, domain_name))
            domain_tables[domain_name].append(agent_name)

    print(f"\nDispatching {len(tasks)} parallel table load jobs (concurrency={max_workers})...")

    completed = 0
    total_rows = 0
    errors = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_task = {
            executor.submit(load_single_table, client, csv_path, table_id): (agent_name, domain_name)
            for csv_path, table_id, agent_name, domain_name in tasks
        }

        for future in as_completed(future_to_task):
            agent_name, domain_name = future_to_task[future]
            try:
                table_id, num_rows = future.result()
                completed += 1
                total_rows += num_rows
                print(f"[{completed:3d}/{len(tasks)}] Loaded {agent_name}_logs: {num_rows:,} rows")
            except Exception as e:
                print(f"[{completed:3d}/{len(tasks)}] FAILED {agent_name}: {e}")
                errors.append((agent_name, str(e)))

    duration = time.time() - start_time
    print(f"\nLoaded {total_rows:,} rows into {completed} tables in {duration:.1f}s.")
    if errors:
        print(f"Encountered {len(errors)} errors:")
        for a, err in errors:
            print(f"  - {a}: {err}")

    # Create Domain Views
    create_domain_views(client, domain_tables)
    print("\nAll BigQuery datasets and views successfully re-populated with golden-grounded data!")

if __name__ == "__main__":
    load_data()
