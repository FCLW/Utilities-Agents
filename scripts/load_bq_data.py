import os
import sys
import subprocess
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import settings
from google.cloud import bigquery

def load_data():
    client = bigquery.Client(project=settings.gcp_project_id)
    
    # User requested to load all data into a single dataset: utilities-data
    # BigQuery dataset IDs only support alphanumeric and underscores, so we use utilities_data
    dataset_name = "utilities_data"
    dataset_id = f"{settings.gcp_project_id}.{dataset_name}"
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = settings.gcp_location
    
    try:
        client.create_dataset(dataset, exists_ok=True)
        print(f"Dataset {dataset_id} created or already exists.")
    except Exception as e:
        print(f"Dataset {dataset_name} creation error: {e}")

    agents_dir = Path("agents")
    if not agents_dir.exists():
        return

    load_jobs = []

    for domain_dir in agents_dir.iterdir():
        if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
            continue
        for agent_dir in domain_dir.iterdir():
            if not agent_dir.is_dir():
                continue
            
            sync_data_dir = agent_dir / "synthetic_data"
            if not sync_data_dir.exists():
                sync_data_dir = agent_dir / "app" / "synthetic_data"
            if not sync_data_dir.exists():
                continue

            print(f"Processing data for {agent_dir.name}...")
            
            # Generate the data first
            gen_script = sync_data_dir / "generate_mock_data.py"
            if gen_script.exists():
                print(f"  Running generate_mock_data.py")
                try:
                    subprocess.run([sys.executable, str(gen_script)], check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    print(f"  Error generating data: {e.stderr.decode()}")
                    continue

            # Load CSVs
            for csv_file in sync_data_dir.glob("*.csv"):
                print(f"  Queueing load for {csv_file.name}")
                table_name = f'{agent_dir.name}_logs' if csv_file.stem == 'mock_records' else csv_file.stem
                table_full_id = f'{settings.gcp_project_id}.{dataset_name}.{table_name}'
                
                job_config = bigquery.LoadJobConfig(
                    source_format=bigquery.SourceFormat.CSV,
                    skip_leading_rows=1,
                    autodetect=True,
                    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE
                )
                
                try:
                    with open(csv_file, "rb") as source_file:
                        job = client.load_table_from_file(source_file, table_full_id, job_config=job_config)
                        load_jobs.append((table_full_id, job))
                except Exception as e:
                    print(f"  -> Failed to queue {csv_file.name}: {e}")

    print(f"Waiting for {len(load_jobs)} BigQuery load jobs to complete...")
    for table_full_id, job in load_jobs:
        try:
            job.result()
            print(f"  -> Successfully loaded into {table_full_id}")
        except Exception as e:
            print(f"  -> Failed to load into {table_full_id}: {e}")

    print("BigQuery data load complete.")

if __name__ == "__main__":
    load_data()
