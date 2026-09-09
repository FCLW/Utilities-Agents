#!/usr/bin/env python3
"""
Synthetic data generator for wildfire_risk_deenergization_trigger grounded in golden-dataset.json.
Temporal coverage: 2025-09-09 to 2026-10-09.
"""
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(root_dir))

from scripts.generate_golden_synthetic_data import (
    extract_entities_from_golden,
    generate_agent_timeseries,
    ROOT_DIR
)

def generate_data():
    agent_dir = Path(__file__).resolve().parent.parent
    domain_name = "grid_operations"
    agent_name = "wildfire_risk_deenergization_trigger"
    golden_path = agent_dir / "tests" / "eval" / "datasets" / "golden-dataset.json"
    entities = extract_entities_from_golden(golden_path, domain_name)
    schema = {"cols": ['timestamp_column', 'feeder_id', 'voltage_kv', 'status_flag', 'anomaly_score', 'entity_name', 'metric_name', 'current_value', 'baseline_target', 'delta_pct', 'substation_or_region', 'details_json']}
    df = generate_agent_timeseries(agent_name, domain_name, entities, schema)
    out_csv = agent_dir / "synthetic_data" / "mock_records.csv"
    df.to_csv(out_csv, index=False)
    print(f"Generated {len(df)} golden-grounded records at {out_csv}")

if __name__ == "__main__":
    generate_data()
