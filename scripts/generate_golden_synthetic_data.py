#!/usr/bin/env python3
"""
Enterprise Golden Synthetic Data Generator
Generates high-fidelity 13-month synthetic timeseries datasets (-1 year historical to +1 month future)
grounded directly in the entities, KPIs, breakdown tables, and chart series of all 113 utility agents'
golden-dataset.json files.
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

# Root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Temporal Horizon
ANCHOR_DATE = pd.Timestamp("2026-09-09 12:00:00", tz="UTC")
HISTORICAL_START = pd.Timestamp("2025-09-09 00:00:00", tz="UTC")
FORECAST_END = pd.Timestamp("2026-10-09 23:59:59", tz="UTC")

# Fallback domain column mappings
DOMAIN_SCHEMAS = {
    "asset_management": ("asset_id", "health_score"),
    "billing_and_invoicing": ("customer_id", "amount_billed"),
    "customer_engagement": ("customer_id", "metric_value"),
    "grid_balancing": ("node_id", "frequency_hz"),
    "grid_operations": ("feeder_id", "voltage_kv"),
    "master_orchestrator": ("id", "value"),
    "production_forecasting": ("plant_id", "generation_mw"),
    "regulatory_compliance": ("record_id", "metric_value"),
    "smart_meter_management": ("meter_id", "consumption_kwh"),
    "support_services": ("record_id", "metric_value"),
    "wholesale_trading": ("node_id", "price_usd_mwh"),
}

def clean_str(s):
    if s is None:
        return ""
    return re.sub(r"[\*`\$\\\{\}]", "", str(s)).strip()

def parse_num(val_str):
    if val_str is None:
        return None
    val_clean = str(val_str).replace(",", "").replace("$", "").replace("\\$", "").strip()
    
    # Check millions (e.g. $4.8M, 150.0M)
    m = re.search(r"([-+]?\d*\.?\d+)\s*[Mm](?:illion)?\b", val_clean)
    if m:
        return float(m.group(1)) * 1_000_000
    # Check thousands (e.g. 45k, $18k)
    k = re.search(r"([-+]?\d*\.?\d+)\s*[Kk]\b", val_clean)
    if k:
        return float(k.group(1)) * 1_000
    # Check standard floats / integers / percentages / fractions
    nums = re.findall(r"[-+]?\d*\.?\d+", val_clean)
    if nums:
        return float(nums[0])
    return None

def find_primary_metric(headers, vals, domain_name):
    """
    Intelligently identifies the core numerical metric column and its value from a table row.
    """
    domain_keywords = {
        "asset_management": ["health", "ahi", "wear", "score", "index", "condition", "fault", "energy", "age", "capex"],
        "billing_and_invoicing": ["billed", "amount", "charge", "bill", "cost", "total", "kwh", "credit", "rate"],
        "customer_engagement": ["csat", "score", "count", "time", "rate", "value", "bill", "savings"],
        "grid_balancing": ["freq", "hz", "soc", "mw", "mvar", "inertia", "price", "loss", "capacity"],
        "grid_operations": ["voltage", "kv", "time", "eta", "etr", "customers", "outage", "duration", "load"],
        "production_forecasting": ["generation", "mw", "mwh", "output", "forecast", "irradiance", "speed", "load"],
        "regulatory_compliance": ["saidi", "saifi", "metric", "emissions", "tons", "score", "rate", "incidents"],
        "smart_meter_management": ["consumption", "kwh", "ping", "temp", "rssi", "hops", "reads", "tamper"],
        "wholesale_trading": ["price", "lmp", "spread", "var", "heat", "bid", "mw", "cost"],
        "support_services": ["incident", "hours", "score", "mttr", "cost", "count", "compliance"]
    }
    keywords = domain_keywords.get(domain_name, []) + ["value", "score", "amount", "rate", "index"]
    
    # 1. Look for matching header with a parseable number
    for kw in keywords:
        for idx, (h, v) in enumerate(zip(headers[1:], vals[1:]), start=1):
            if kw in h.lower():
                num = parse_num(v)
                if num is not None:
                    return h, num
                    
    # 2. Fallback: find any column (excluding location/id/name/status) with a number
    for idx, (h, v) in enumerate(zip(headers[1:], vals[1:]), start=1):
        if any(ign in h.lower() for ign in ["substation", "bay", "id", "name", "status", "criticality", "zone", "qualification"]):
            continue
        num = parse_num(v)
        if num is not None:
            return h, num
            
    # 3. Last fallback
    return (headers[1] if len(headers) > 1 else "Metric"), (parse_num(vals[1]) if len(vals) > 1 else 75.0)

def extract_entities_from_golden(golden_file_path, domain_name):
    """
    Parses an agent golden-dataset.json and returns a list of unique structured entity/metric records.
    """
    with open(golden_file_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    extracted_entities = {}
    extracted_kpis = {}

    for case_idx, case in enumerate(cases):
        inp = case.get("input", "")
        out = case.get("expected_output", "")

        # Look for explicit entity codes in prompt (e.g., CB-104, XFMR-230-0101, BESS-20MW)
        prompt_entities = re.findall(r"\b([A-Z0-9]{2,10}(?:-[A-Z0-9]+)+)\b", inp)
        for pe in prompt_entities:
            key = f"PROMPT_{pe}"
            if key not in extracted_entities:
                extracted_entities[key] = {
                    "entity_id": pe,
                    "entity_name": pe,
                    "metric_name": "Telemetry Health Score",
                    "current_val_num": 50.0,
                    "baseline_val_num": 75.0,
                    "delta_pct_num": -33.3,
                    "status": "WARNING",
                    "substation_or_region": None,
                    "details": {"source": "test_prompt", "prompt": inp}
                }

        # 1. Parse markdown tables
        lines = out.split("\n")
        table_lines = []
        for line in lines:
            if line.strip().startswith("|") and line.strip().endswith("|"):
                table_lines.append(line.strip())
            else:
                if len(table_lines) >= 3:
                    headers = [clean_str(c) for c in table_lines[0].strip("|").split("|")]
                    for row_str in table_lines[2:]:
                        vals = [clean_str(c) for c in row_str.strip("|").split("|")]
                        if len(vals) == len(headers):
                            row_dict = dict(zip(headers, vals))
                            first_col = headers[0]
                            first_val = vals[0]

                            if "Metric" in headers and any("Current" in h for h in headers):
                                # KPI summary table row
                                m_name = row_dict.get("Metric", first_val)
                                cur_val_raw = None
                                base_val_raw = None
                                for k, v in row_dict.items():
                                    if "Current" in k:
                                        cur_val_raw = v
                                    elif "Baseline" in k or "Target" in k:
                                        base_val_raw = v
                                delta_raw = row_dict.get("Delta (%)", "")
                                status_raw = row_dict.get("Status (Normal/Warning/Critical)", row_dict.get("Status", "NORMAL")).upper()
                                if "CRITICAL" in status_raw:
                                    status = "CRITICAL"
                                elif "WARN" in status_raw:
                                    status = "WARNING"
                                else:
                                    status = "NORMAL"

                                key = f"KPI_{m_name}"
                                extracted_kpis[key] = {
                                    "entity_id": m_name,
                                    "entity_name": m_name,
                                    "metric_name": m_name,
                                    "current_val_num": parse_num(cur_val_raw) or 50.0,
                                    "baseline_val_num": parse_num(base_val_raw),
                                    "delta_pct_num": parse_num(delta_raw),
                                    "status": status,
                                    "substation_or_region": None,
                                    "details": row_dict
                                }
                            else:
                                # Entity breakdown table row
                                eid = first_val
                                sub = None
                                for h in headers:
                                    if any(w in h.lower() for w in ["substation", "bay", "region", "division", "node", "feeder", "zone", "corridor"]):
                                        sub = row_dict[h]
                                        break
                                
                                val_col, cur_val_num = find_primary_metric(headers, vals, domain_name)

                                row_status = "NORMAL"
                                for k, v in row_dict.items():
                                    v_upper = str(v).upper()
                                    if "CRITICAL" in v_upper or "IMMEDIATE" in v_upper or "HIGH RISK" in v_upper:
                                        row_status = "CRITICAL"
                                        break
                                    elif "WARN" in v_upper or "PLANNED" in v_upper or "MEDIUM" in v_upper:
                                        row_status = "WARNING"

                                key = f"ENTITY_{eid}"
                                extracted_entities[key] = {
                                    "entity_id": eid,
                                    "entity_name": f"{sub} - {eid}" if sub and sub != eid else eid,
                                    "metric_name": val_col,
                                    "current_val_num": cur_val_num if cur_val_num is not None else 75.0,
                                    "baseline_val_num": None,
                                    "delta_pct_num": None,
                                    "status": row_status,
                                    "substation_or_region": sub,
                                    "details": row_dict
                                }
                table_lines = []

        # 2. Parse JSON charts
        for jm in re.findall(r"```json\s*(\{[\s\S]*?\})\s*```", out):
            try:
                cd = json.loads(jm)
                if "series" in cd and isinstance(cd["series"], list):
                    for s in cd["series"]:
                        sname = s.get("name")
                        sdata = s.get("data")
                        if sname and isinstance(sdata, list):
                            for idx, pt in enumerate(sdata):
                                if isinstance(pt, dict):
                                    pt_id = pt.get("substation") or pt.get("asset_id") or pt.get("name") or pt.get("id") or f"{sname}_{idx}"
                                    val = pt.get("health_index") or pt.get("value") or pt.get("age") or pt.get("y")
                                    st = "NORMAL"
                                    if pt.get("status"):
                                        st = str(pt["status"]).upper()
                                    key = f"CHART_{pt_id}"
                                    if key not in extracted_entities:
                                        extracted_entities[key] = {
                                            "entity_id": pt_id,
                                            "entity_name": pt_id,
                                            "metric_name": sname,
                                            "current_val_num": parse_num(val) or 50.0,
                                            "baseline_val_num": None,
                                            "delta_pct_num": None,
                                            "status": st if st in ["NORMAL", "WARNING", "CRITICAL"] else "NORMAL",
                                            "substation_or_region": pt.get("substation"),
                                            "details": pt
                                        }
            except Exception:
                pass

    # Prioritize entities first, then KPIs
    combined = list(extracted_entities.values()) + list(extracted_kpis.values())
    return combined

def generate_agent_timeseries(agent_name, domain_name, entities, existing_schema):
    """
    Generates a 13-month timeseries dataframe grounded in the extracted entities.
    """
    np.random.seed(42)

    cols = existing_schema.get("cols", [])
    if cols and len(cols) >= 3:
        if cols[0] == "id" and cols[1] == "value":
            id_col = "id"
            metric_col = "value"
        else:
            id_col = cols[1]
            metric_col = cols[2]
    else:
        id_col, metric_col = DOMAIN_SCHEMAS.get(domain_name, ("asset_id", "health_score"))

    if not entities:
        entities = [{
            "entity_id": f"{agent_name.upper()}-01",
            "entity_name": f"{agent_name.replace('_', ' ').title()} Unit 01",
            "metric_name": "Operational Health Score",
            "current_val_num": 85.0,
            "baseline_val_num": 80.0,
            "delta_pct_num": 6.25,
            "status": "NORMAL",
            "substation_or_region": "Main Grid Zone",
            "details": {"status": "Nominal"}
        }]

    # Cap entities to top 25 to provide dense, relevant coverage
    selected_entities = entities[:25]

    # Sample dates: 13 months total
    # Weekly intervals historically from 2025-09-09 to 2026-08-10, plus daily for last 30 days and 30 days forecast
    dates_hist_weekly = pd.date_range(start=HISTORICAL_START, end=ANCHOR_DATE - pd.Timedelta(days=30), freq="7D", tz="UTC")
    dates_recent_daily = pd.date_range(start=ANCHOR_DATE - pd.Timedelta(days=30), end=FORECAST_END, freq="1D", tz="UTC")
    all_dates = dates_hist_weekly.union(dates_recent_daily).sort_values()

    if ANCHOR_DATE not in all_dates:
        all_dates = all_dates.insert(0, ANCHOR_DATE).sort_values()

    records = []

    for ent_idx, ent in enumerate(selected_entities):
        eid = ent["entity_id"]
        ename = ent["entity_name"]
        mname = ent["metric_name"]
        cur_val = ent["current_val_num"]
        base_val = ent["baseline_val_num"]
        delta_pct = ent["delta_pct_num"]
        final_status = ent["status"]
        sub = ent["substation_or_region"]
        details_str = json.dumps(ent["details"])

        if cur_val is None:
            cur_val = 75.0

        n_points = len(all_dates)
        anchor_idx = int(np.argmin(np.abs(all_dates - ANCHOR_DATE)))

        if "wear" in mname.lower() or "fault" in mname.lower() or "cost" in mname.lower() or "outage" in mname.lower():
            hist_start_val = cur_val * 0.45
            trend_hist = np.linspace(hist_start_val, cur_val, anchor_idx + 1)
            forecast_end_val = cur_val * 1.05
            trend_forecast = np.linspace(cur_val, forecast_end_val, n_points - anchor_idx)[1:]
            vals = np.concatenate([trend_hist, trend_forecast])
        elif "health" in mname.lower() or "score" in mname.lower() or "index" in mname.lower() or "ahi" in mname.lower():
            hist_start_val = min(100.0, cur_val * 1.35)
            trend_hist = np.linspace(hist_start_val, cur_val, anchor_idx + 1)
            forecast_end_val = max(5.0, cur_val * 0.96)
            trend_forecast = np.linspace(cur_val, forecast_end_val, n_points - anchor_idx)[1:]
            vals = np.concatenate([trend_hist, trend_forecast])
        elif "lmp" in mname.lower() or "price" in mname.lower() or "generation" in mname.lower() or "load" in mname.lower():
            base = cur_val * 0.85
            month_factors = [1.0 + 0.3 * np.sin((d.month - 3) * np.pi / 6) for d in all_dates]
            noise = np.random.normal(0, 0.05 * abs(cur_val) if cur_val != 0 else 1.0, n_points)
            vals = base * np.array(month_factors) + noise
            vals[anchor_idx] = cur_val
        else:
            noise = np.random.normal(0, 0.03 * abs(cur_val) if cur_val != 0 else 1.0, n_points)
            vals = cur_val + noise
            vals[anchor_idx] = cur_val

        for i, dt in enumerate(all_dates):
            is_anchor = (i == anchor_idx)
            is_forecast = (dt > ANCHOR_DATE)
            val_at_t = float(round(vals[i], 2))

            if is_anchor:
                st = final_status
                anom = 0.95 if st == "CRITICAL" else (0.65 if st == "WARNING" else 0.02)
            elif is_forecast:
                st = "FORECAST"
                anom = 0.50 if final_status in ["CRITICAL", "WARNING"] else 0.05
            else:
                if final_status == "CRITICAL":
                    st = "NORMAL" if i < anchor_idx * 0.5 else "WARNING" if i < anchor_idx * 0.85 else "CRITICAL"
                elif final_status == "WARNING":
                    st = "NORMAL" if i < anchor_idx * 0.7 else "WARNING"
                else:
                    st = "NORMAL"
                anom = 0.88 if st == "CRITICAL" else (0.60 if st == "WARNING" else 0.02)

            rec = {
                "timestamp_column": dt.strftime("%Y-%m-%d %H:%M:%S UTC"),
                id_col: ent_idx + 1 if id_col == "id" else eid,
                metric_col: val_at_t,
                "status_flag": st,
                "anomaly_score": round(anom, 4),
                "entity_name": ename,
                "metric_name": mname,
                "current_value": cur_val,
                "baseline_target": base_val,
                "delta_pct": delta_pct,
                "substation_or_region": sub or "Enterprise Grid",
                "details_json": details_str
            }
            records.append(rec)

    df = pd.DataFrame(records)
    return df

def generate_all():
    print(f"=== Starting Golden Synthetic Data Generation ===")
    print(f"Anchor Date: {ANCHOR_DATE}")
    print(f"Historical Start: {HISTORICAL_START} (-1 year)")
    print(f"Forecast End: {FORECAST_END} (+1 month)")

    agents_dir = ROOT_DIR / "agents"
    schema_cache = {}
    schema_cache_file = ROOT_DIR / "scripts" / "existing_agent_schemas.json"
    if schema_cache_file.exists():
        with open(schema_cache_file) as f:
            schema_cache = json.load(f)

    processed_count = 0
    total_rows = 0

    for domain_dir in sorted(agents_dir.iterdir()):
        if not domain_dir.is_dir() or domain_dir.name.startswith("_"):
            continue
        domain_name = domain_dir.name

        for agent_dir in sorted(domain_dir.iterdir()):
            if not agent_dir.is_dir() or agent_dir.name.startswith("_"):
                continue
            agent_name = agent_dir.name

            golden_path = agent_dir / "tests" / "eval" / "datasets" / "golden-dataset.json"
            if not golden_path.exists():
                print(f"Skipping {agent_name}: golden-dataset.json not found")
                continue

            entities = extract_entities_from_golden(golden_path, domain_name)
            existing_schema = schema_cache.get(agent_name, {})
            df = generate_agent_timeseries(agent_name, domain_name, entities, existing_schema)

            sync_data_dir = agent_dir / "synthetic_data"
            sync_data_dir.mkdir(parents=True, exist_ok=True)
            csv_path = sync_data_dir / "mock_records.csv"
            df.to_csv(csv_path, index=False)

            gen_script = sync_data_dir / "generate_mock_data.py"
            gen_script_code = f'''#!/usr/bin/env python3
"""
Synthetic data generator for {agent_name} grounded in golden-dataset.json.
Temporal coverage: {HISTORICAL_START.strftime("%Y-%m-%d")} to {FORECAST_END.strftime("%Y-%m-%d")}.
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
    domain_name = "{domain_name}"
    agent_name = "{agent_name}"
    golden_path = agent_dir / "tests" / "eval" / "datasets" / "golden-dataset.json"
    entities = extract_entities_from_golden(golden_path, domain_name)
    schema = {{"cols": {df.columns.tolist()}}}
    df = generate_agent_timeseries(agent_name, domain_name, entities, schema)
    out_csv = agent_dir / "synthetic_data" / "mock_records.csv"
    df.to_csv(out_csv, index=False)
    print(f"Generated {{len(df)}} golden-grounded records at {{out_csv}}")

if __name__ == "__main__":
    generate_data()
'''
            with open(gen_script, "w") as f:
                f.write(gen_script_code)

            processed_count += 1
            total_rows += len(df)
            print(f"[{processed_count:3d}/113] Generated {agent_name}: {len(df)} rows across {len(entities)} entities ({domain_name})")

    print(f"\nCompleted! Generated {total_rows:,} records across {processed_count} agents.")

if __name__ == "__main__":
    generate_all()
