import json
import re
from pathlib import Path
import yaml

def get_actual_agent_model(agent_id, domain_id, fallback="gemini-3.7-flash"):
    """Determines actual LLM model used by inspecting manifest.yaml, agent.py, and settings.py."""
    candidates = [
        Path(f"agents/{domain_id}/{agent_id}/manifest.yaml"),
        Path(f"agents/{domain_id}/{agent_id}/agent.py"),
        Path(f"agents/{domain_id}/{agent_id}/config/settings.py")
    ]
    # Check domain folder first
    if candidates[0].exists():
        try:
            with open(candidates[0], "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                m = data.get("target_model") or data.get("model")
                if m:
                    return m
        except Exception:
            pass

    if candidates[1].exists():
        try:
            with open(candidates[1], "r", encoding="utf-8") as f:
                content = f.read()
                m = re.search(r'model\s*=\s*["\']([^"\']+)["\']', content)
                if m:
                    return m.group(1)
        except Exception:
            pass

    if candidates[2].exists():
        try:
            with open(candidates[2], "r", encoding="utf-8") as f:
                content = f.read()
                m = re.search(r'llm_model_name\s*=\s*os\.getenv\([^,]+,\s*["\']([^"\']+)["\']\)', content)
                if m:
                    return m.group(1)
        except Exception:
            pass

    # Search anywhere in agents/ for this agent_id
    for mp in Path("agents").glob(f"*/{agent_id}/manifest.yaml"):
        try:
            with open(mp, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                m = data.get("target_model") or data.get("model")
                if m:
                    return m
        except Exception:
            pass

    for ap in Path("agents").glob(f"*/{agent_id}/agent.py"):
        try:
            with open(ap, "r", encoding="utf-8") as f:
                content = f.read()
                m = re.search(r'model\s*=\s*["\']([^"\']+)["\']', content)
                if m:
                    return m.group(1)
        except Exception:
            pass

    # If fallback is a valid gemini model
    if fallback and fallback in ("gemini-3.7-flash", "gemini-3.1-pro"):
        return fallback
    return "gemini-3.7-flash"

# 1. Parse AGENTS.md
with open("AGENTS.md", "r", encoding="utf-8") as f:
    agents_md = f.read()

# Load existing catalog.json for live_urls
catalog_file = Path("web/catalog.json")
existing_catalog = []
if catalog_file.exists():
    with open(catalog_file, "r", encoding="utf-8") as f:
        try:
            existing_catalog = json.load(f)
        except Exception:
            existing_catalog = []
cat_by_id = {a.get("id"): a for a in existing_catalog if isinstance(a, dict)}

sections = re.split(r"\n##\s+", agents_md)
domain_map = {
    "Master Orchestrator": ("master_orchestrator", "Master Orchestrator", "🎯"),
    "Asset Management": ("asset_management", "Asset Management", "🏗️"),
    "Billing And Invoicing": ("billing_and_invoicing", "Billing & Invoicing", "💳"),
    "Customer Engagement": ("customer_engagement", "Customer Engagement", "👥"),
    "Grid Balancing": ("grid_balancing", "Grid Balancing", "⚖️"),
    "Grid Operations": ("grid_operations", "Grid Operations", "⚡"),
    "Production Forecasting": ("production_forecasting", "Production Forecasting", "📈"),
    "Regulatory Compliance": ("regulatory_compliance", "Regulatory Compliance", "📋"),
    "Smart Meter Management": ("smart_meter_management", "Smart Meter Management", "📟"),
    "Support Services": ("support_services", "Support Services", "🛠️"),
    "Wholesale Trading": ("wholesale_trading", "Wholesale Trading", "💹")
}

east4_agents = {
    "ancillary_services_bid_optimizer",
    "carbon_allowance_market_tracker",
    "coal_inventory_burn_rate_advisor",
    "dark_spread_heat_rate_calculator",
    "day_ahead_lmp_forecaster",
    "financial_transmission_right_copilot",
    "iso_rto_bidding_curve_generator",
    "natural_gas_pipeline_constraint_analyzer",
    "portfolio_value_at_risk_analyzer",
    "real_time_lmp_tracker",
    "renewable_energy_certificate_trader",
    "spark_spread_heat_rate_calculator",
    "warehouse_inventory_drone_auditor"
}

ge_ids_path = Path("web/ge_agent_ids.json")
ge_ids = {}
if ge_ids_path.exists():
    with open(ge_ids_path) as f:
        ge_ids = json.load(f)

agents_data = []
domain_counts = {}

for sec in sections[1:]:
    lines = sec.strip().split("\n")
    domain_header = lines[0].strip()
    if domain_header not in domain_map:
        continue
    domain_id, domain_title, icon = domain_map[domain_header]
    rows = re.findall(r"\|\s*\*\*([^*]+)\*\*<br>`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|", sec)
    domain_counts[domain_id] = len(rows)
    for r in rows:
        name = r[0].strip()
        agent_id = r[1].strip()
        persona = r[2].strip()
        problem_solution = r[3].strip()
        
        prob_match = re.search(r"\*\*Problem:\*\*\s*(.*?)(?:\<br\>|\n|$)", problem_solution)
        sol_match = re.search(r"\*\*Solution:\*\*\s*(.*?)(?:\<br\>|\n|$)", problem_solution)
        problem_text = prob_match.group(1).strip() if prob_match else ""
        solution_text = sol_match.group(1).strip() if sol_match else ""
        
        kpis_raw = r[4].strip()
        kpis = [k.strip() for k in kpis_raw.split(",") if k.strip()]
        
        tables_raw = r[5].strip().replace("`", "")
        tables = [t.strip() for t in tables_raw.split(",") if t.strip()]
        
        raw_model = r[6].strip().replace("`", "")
        model = get_actual_agent_model(agent_id, domain_id, raw_model)
        
        prompt_yaml_path = Path(f"agents/{domain_id}/{agent_id}/instructions/sample_prompts.yaml")
        prompts = []
        if prompt_yaml_path.exists():
            try:
                with open(prompt_yaml_path, "r", encoding="utf-8") as pyf:
                    pydata = yaml.safe_load(pyf) or {}
                    prompts = pydata.get("prompts", []) or pydata.get("sample_prompts", [])
            except Exception:
                pass
        if not prompts:
            cat_entry = cat_by_id.get(agent_id, {})
            prompts = cat_entry.get("prompts", [])
        if not prompts:
            prompts = [
                f"Run an operational diagnostic analysis for {name}.",
                f"Identify active anomalies and degradation trends in {domain_title}.",
                f"Generate executive briefing and recommended remediation actions for {name}."
            ]
        cat_entry = cat_by_id.get(agent_id, {})
            
        location = "us-east4" if agent_id in east4_agents else "us-central1"
        live_url = ""
            
        ge_agent_id = ge_ids.get(agent_id, "")
        if ge_agent_id:
            ge_url = f"https://vertexaisearch.cloud.google.com/home/cid/4d886c3b-e9e0-419c-a168-d25114e2dad6/r/agent/{ge_agent_id}/session/-"
        else:
            ge_url = "https://vertexaisearch.cloud.google.com/home/cid/4d886c3b-e9e0-419c-a168-d25114e2dad6/r/agent/10424690685175366976/session/-session/-"
        
        agents_data.append({
            "id": agent_id,
            "name": name,
            "display_name": name,
            "domain": domain_id,
            "domain_display": domain_title,
            "icon": icon,
            "location": location,
            "persona": persona,
            "problem": problem_text,
            "solution": solution_text,
            "description": f"Problem: {problem_text} Solution: {solution_text}",
            "kpis": kpis,
            "tables": tables,
            "model": model,
            "prompts": prompts,
            "demo_html": f"demos/{domain_id}/{agent_id}.html",
            "spec_url": f"readmes/{domain_id}/{agent_id}.md",
            "live_url": live_url,
            "ge_agent_id": ge_agent_id,
            "ge_url": ge_url
        })

print(f"Total agents processed: {len(agents_data)}")

# Save updated catalog.json
with open("web/catalog.json", "w", encoding="utf-8") as f:
    json.dump(agents_data, f, indent=2, ensure_ascii=False)
print("Updated web/catalog.json successfully.")

# Prepare domain pills HTML
domain_pills_html = [
    f'<button class="domain-btn active" data-domain="all"><span>🌐</span> All Domains <span class="domain-count">{len(agents_data)}</span></button>'
]
for d_header, (d_id, d_title, d_icon) in domain_map.items():
    count = domain_counts.get(d_id, 0)
    domain_pills_html.append(
        f'<button class="domain-btn" data-domain="{d_id}"><span>{d_icon}</span> {d_title} <span class="domain-count">{count}</span></button>'
    )
domain_pills_block = "\n        ".join(domain_pills_html)

agents_json_str = json.dumps(agents_data, indent=2, ensure_ascii=False)

template = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gemini Enterprise Agents for Utilities — 113 Multi-Agent Catalog</title>
  <meta name="description" content="Explore 113 specialized Gemini Enterprise Agents for energy & utilities operations, built on Google ADK, Gemini Enterprise, and BigQuery Conversational Analytics.">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <script>
    (function() {
      const savedTheme = localStorage.getItem('utilities_agents_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', savedTheme);
    })();
  </script>

  <style>
    :root {
      --bg-primary: #0b1120;
      --bg-secondary: #131d31;
      --bg-card: #182339;
      --bg-card-hover: #243248;
      --bg-surface: #0f172a;
      --bg-input: #0f172a;
      --border-color: #334155;
      --border-faint: rgba(255, 255, 255, 0.14);
      --border-subtle: #1e293b;
      --border-focus: #38bdf8;
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --accent-blue: #38bdf8;
      --accent-blue-hover: #0284c7;
      --accent-indigo: #818cf8;
      --accent-emerald: #34d399;
      --accent-amber: #fbbf24;
      --badge-bg: rgba(56, 189, 248, 0.12);
      --badge-border: rgba(56, 189, 248, 0.28);
      --badge-text: #38bdf8;
      --badge-model-bg: rgba(52, 211, 153, 0.12);
      --badge-model-border: rgba(52, 211, 153, 0.3);
      --badge-model-text: #34d399;
      --kpi-bg: rgba(52, 211, 153, 0.1);
      --kpi-border: rgba(52, 211, 153, 0.25);
      --kpi-text: #34d399;
      --region-bg: rgba(129, 140, 248, 0.12);
      --region-border: rgba(129, 140, 248, 0.28);
      --region-text: #a5b4fc;
      --shadow-card: 0 10px 25px -5px rgba(0, 0, 0, 0.4), 0 8px 10px -6px rgba(0, 0, 0, 0.4);
      --shadow-modal: 0 25px 50px -12px rgba(0, 0, 0, 0.7);
      --modal-overlay: rgba(15, 23, 42, 0.85);
    }

    [data-theme="light"] {
      --bg-primary: #f8fafc;
      --bg-secondary: #ffffff;
      --bg-card: #ffffff;
      --bg-card-hover: #f8fafc;
      --bg-surface: #f1f5f9;
      --bg-input: #ffffff;
      --border-color: #cbd5e1;
      --border-faint: #cbd5e1;
      --border-subtle: #e2e8f0;
      --border-focus: #0284c7;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-blue-hover: #0369a1;
      --accent-indigo: #6366f1;
      --accent-emerald: #059669;
      --accent-amber: #d97706;
      --badge-bg: #e0f2fe;
      --badge-border: #bae6fd;
      --badge-text: #0284c7;
      --badge-model-bg: #d1fae5;
      --badge-model-border: #a7f3d0;
      --badge-model-text: #065f46;
      --kpi-bg: #d1fae5;
      --kpi-border: #a7f3d0;
      --kpi-text: #065f46;
      --region-bg: #e0e7ff;
      --region-border: #c7d2fe;
      --region-text: #4338ca;
      --shadow-card: 0 4px 6px -1px rgba(0, 0, 0, 0.07), 0 2px 4px -2px rgba(0, 0, 0, 0.05);
      --shadow-modal: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
      --modal-overlay: rgba(15, 23, 42, 0.6);
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      line-height: 1.5;
      transition: background-color 0.2s ease, color 0.2s ease;
    }

    /* Global Header */
    .site-header {
      background: var(--bg-secondary);
      border-bottom: 1px solid var(--border-color);
      position: sticky;
      top: 0;
      z-index: 40;
      backdrop-filter: blur(8px);
    }

    .header-inner {
      max-width: 1400px;
      margin: 0 auto;
      padding: 14px 24px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 16px;
    }

    .brand-logo {
      display: flex;
      align-items: center;
      gap: 12px;
      text-decoration: none;
      color: var(--text-primary);
    }

    .brand-icon {
      font-size: 1.8rem;
      line-height: 1;
    }

    .brand-text {
      display: flex;
      flex-direction: column;
    }

    .brand-title {
      font-family: 'Google Sans', sans-serif;
      font-size: 1.2rem;
      font-weight: 700;
      letter-spacing: -0.01em;
      color: var(--text-primary);
    }

    .brand-subtitle {
      font-size: 0.76rem;
      color: var(--text-secondary);
      font-weight: 500;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .brand-subtitle::before {
      content: "";
      display: inline-block;
      width: 7px;
      height: 7px;
      background: var(--accent-emerald);
      border-radius: 50%;
    }

    .header-actions {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-header {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-primary);
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
    }

    .btn-header:hover {
      border-color: var(--border-focus);
      color: var(--accent-blue);
    }

    .btn-primary-header {
      background: var(--accent-blue);
      color: #0f172a;
      border-color: var(--accent-blue);
      font-weight: 700;
    }

    .btn-primary-header:hover {
      background: var(--accent-blue-hover);
      color: #ffffff;
      border-color: var(--accent-blue-hover);
    }

    /* Hero Section */
    .hero {
      padding: 44px 24px 32px;
      text-align: center;
      max-width: 1280px;
      margin: 0 auto;
    }

    .hero-pill {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 9999px;
      font-size: 0.82rem;
      font-weight: 600;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--accent-blue);
      margin-bottom: 18px;
    }

    .hero-title {
      font-family: 'Google Sans', sans-serif;
      font-size: 2.5rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      line-height: 1.2;
      margin-bottom: 14px;
    }

    .hero-title span {
      background: linear-gradient(135deg, #38bdf8 0%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .hero-desc {
      font-size: 1.05rem;
      color: var(--text-secondary);
      max-width: 820px;
      margin: 0 auto 32px;
      line-height: 1.6;
    }

    /* Platform Stats */
    .stat-row {
      display: grid;
      grid-template-columns: repeat(5, minmax(0, 1fr));
      gap: 14px;
      margin-bottom: 12px;
    }

    .stat-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 12px;
      padding: 16px 10px;
      text-align: center;
      transition: transform 0.15s ease, border-color 0.15s ease;
      min-width: 0;
    }

    @media (max-width: 768px) {
      .stat-row {
        overflow-x: auto;
        padding-bottom: 8px;
        -webkit-overflow-scrolling: touch;
      }
      .stat-card {
        min-width: 140px;
      }
    }

    .stat-card:hover {
      transform: translateY(-2px);
      border-color: var(--border-focus);
    }

    .stat-number {
      font-family: 'Google Sans', sans-serif;
      font-size: 2rem;
      font-weight: 800;
      color: var(--accent-blue);
      line-height: 1.1;
      margin-bottom: 4px;
    }

    .stat-label {
      font-size: 0.78rem;
      font-weight: 600;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }

    /* Main Container */
    .main-container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 12px 24px 60px;
      width: 100%;
      flex: 1;
    }

    /* Toolbar: Search & Filters */
    .toolbar {
      margin-bottom: 24px;
      display: flex;
      flex-direction: column;
      gap: 16px;
    }

    .search-row {
      display: flex;
      gap: 12px;
    }

    .search-input-wrapper {
      position: relative;
      flex: 1;
    }

    .search-icon {
      position: absolute;
      left: 14px;
      top: 50%;
      transform: translateY(-50%);
      color: var(--text-muted);
      font-size: 1rem;
      pointer-events: none;
    }

    .search-input {
      width: 100%;
      padding: 13px 40px 13px 42px;
      border-radius: 10px;
      border: 1px solid var(--border-color);
      background: var(--bg-input);
      color: var(--text-primary);
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .search-input:focus {
      border-color: var(--border-focus);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }

    .search-clear {
      position: absolute;
      right: 12px;
      top: 50%;
      transform: translateY(-50%);
      background: none;
      border: none;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 1.1rem;
      padding: 4px;
      display: none;
    }

    .search-clear:hover {
      color: var(--text-primary);
    }

    /* Domain Filter Pills */
    .domain-pills {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }

    .domain-btn {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 8px 14px;
      border-radius: 9999px;
      border: 1px solid var(--border-color);
      background: var(--bg-surface);
      color: var(--text-secondary);
      font-size: 0.84rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .domain-btn:hover {
      border-color: var(--border-focus);
      color: var(--text-primary);
    }

    .domain-btn.active {
      background: var(--accent-blue);
      border-color: var(--accent-blue);
      color: #0f172a;
      font-weight: 700;
    }

    .domain-count {
      font-size: 0.72rem;
      padding: 1px 6px;
      border-radius: 9999px;
      background: rgba(0, 0, 0, 0.15);
    }

    .domain-btn.active .domain-count {
      background: rgba(15, 23, 42, 0.25);
      color: #0f172a;
      font-weight: 800;
    }

    /* Results Header */
    .results-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 12px;
      border-bottom: 1px solid var(--border-subtle);
    }

    .results-count {
      font-size: 0.9rem;
      color: var(--text-secondary);
    }

    .results-count strong {
      color: var(--accent-blue);
      font-weight: 700;
    }

    /* Agent Grid */
    .agent-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
      gap: 20px;
    }

    @media (max-width: 640px) {
      .agent-grid {
        grid-template-columns: 1fr;
      }
    }

    /* Agent Card */
    .agent-card {
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: 14px;
      padding: 22px;
      display: flex;
      flex-direction: column;
      box-shadow: var(--shadow-card);
      transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
      position: relative;
    }

    .agent-card:hover {
      transform: translateY(-3px);
      border-color: var(--border-focus);
      box-shadow: 0 15px 30px -5px rgba(0, 0, 0, 0.45);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 12px;
    }

    .card-badges {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    .badge-domain {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.72rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.04em;
      padding: 3px 8px;
      border-radius: 6px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--badge-text);
    }

    .badge-region {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.7rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      background: var(--region-bg);
      border: 1px solid var(--region-border);
      color: var(--region-text);
      font-family: 'JetBrains Mono', monospace;
    }

    .badge-model {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      font-size: 0.68rem;
      font-weight: 700;
      padding: 3px 8px;
      border-radius: 6px;
      background: var(--badge-model-bg);
      border: 1px solid var(--badge-model-border);
      color: var(--badge-model-text);
      font-family: 'JetBrains Mono', monospace;
    }

    .card-title {
      font-family: 'Google Sans', sans-serif;
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 6px;
      line-height: 1.35;
    }

    .card-persona {
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--accent-indigo);
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .card-desc {
      font-size: 0.86rem;
      color: var(--text-secondary);
      line-height: 1.5;
      margin-bottom: 14px;
      flex: 1;
    }

    .card-desc strong {
      color: var(--text-primary);
    }

    /* KPI Tags */
    .kpi-row {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 12px;
    }

    .kpi-pill {
      font-size: 0.72rem;
      font-weight: 600;
      padding: 3px 8px;
      border-radius: 6px;
      background: var(--kpi-bg);
      border: 1px solid var(--kpi-border);
      color: var(--kpi-text);
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    /* Table Tag */
    .table-tag {
      font-size: 0.72rem;
      color: var(--text-muted);
      margin-bottom: 14px;
      display: flex;
      align-items: center;
      gap: 6px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }

    .table-tag code {
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-secondary);
      background: var(--bg-surface);
      padding: 2px 6px;
      border-radius: 4px;
      border: 1px solid var(--border-color);
      overflow: hidden;
      text-overflow: ellipsis;
    }

    /* Prompts Collapsible */
    .prompts-container {
      border-top: 1px solid var(--border-color);
      padding-top: 12px;
      margin-bottom: 16px;
    }

    .prompts-toggle {
      background: none;
      border: none;
      color: var(--text-secondary);
      font-size: 0.78rem;
      font-weight: 600;
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 100%;
      cursor: pointer;
      padding: 2px 0;
    }

    .prompts-toggle:hover {
      color: var(--accent-blue);
    }

    .prompts-list {
      margin-top: 8px;
      display: none;
      flex-direction: column;
      gap: 6px;
    }

    .prompts-list.open {
      display: flex;
    }

    .prompt-item {
      font-size: 0.78rem;
      color: var(--text-secondary);
      background: var(--bg-surface);
      padding: 6px 10px;
      border-radius: 6px;
      border-left: 3px solid var(--accent-indigo);
      line-height: 1.4;
      font-style: italic;
    }

    /* Card Actions */
    .card-actions {
      display: grid;
      grid-template-columns: 1fr auto;
      gap: 8px;
      align-items: center;
      margin-top: auto;
      padding-top: 14px;
      border-top: 1px solid var(--border-color);
    }

    .card-actions .btn-watch {
      grid-column: 1 / -1;
    }

    .btn-watch {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: var(--accent-blue);
      color: #0f172a;
      padding: 9px 14px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 700;
      border: none;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.15s ease;
    }

    .btn-watch:hover {
      background: var(--accent-blue-hover);
      color: #ffffff;
      transform: translateY(-1px);
    }

    .btn-showcase {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      background: var(--bg-surface);
      color: var(--text-primary);
      padding: 9px 16px;
      border-radius: 8px;
      font-size: 0.86rem;
      font-weight: 600;
      text-decoration: none;
      border: 1px solid var(--border-color);
      cursor: pointer;
      font-family: inherit;
      transition: all 0.15s ease;
      white-space: nowrap;
    }

    .btn-showcase:hover {
      border-color: var(--border-focus);
      color: var(--accent-blue);
    }

    .btn-doc {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 4px;
      background: var(--bg-surface);
      color: var(--text-secondary);
      padding: 9px 8px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      border: 1px solid var(--border-color);
      text-decoration: none;
      cursor: pointer;
      transition: all 0.15s ease;
      white-space: nowrap;
      width: max-content;
    }

    .btn-doc:hover {
      color: var(--text-primary);
      border-color: var(--border-focus);
    }

    /* No Results State */
    .no-results {
      grid-column: 1 / -1;
      text-align: center;
      padding: 60px 20px;
      background: var(--bg-card);
      border: 1px dashed var(--border-color);
      border-radius: 14px;
      display: none;
    }

    .no-results-icon {
      font-size: 3rem;
      margin-bottom: 12px;
    }

    .no-results-title {
      font-size: 1.2rem;
      font-weight: 700;
      margin-bottom: 6px;
      color: var(--text-primary);
    }

    .no-results-desc {
      color: var(--text-secondary);
      font-size: 0.9rem;
      margin-bottom: 16px;
    }

    /* Modals */
    .modal-backdrop {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: var(--modal-overlay);
      backdrop-filter: blur(6px);
      z-index: 100;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 20px;
      opacity: 0;
      transition: opacity 0.2s ease;
    }

    .modal-backdrop.open {
      display: flex;
      opacity: 1;
    }

    .modal-dialog {
      background: var(--bg-secondary);
      border: 1px solid var(--border-color);
      border-radius: 16px;
      width: 100%;
      max-width: 900px;
      max-height: 90vh;
      overflow-y: auto;
      box-shadow: var(--shadow-modal);
      position: relative;
      display: flex;
      flex-direction: column;
    }

    .modal-header {
      padding: 20px 24px;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .modal-title-wrap {
      display: flex;
      flex-direction: column;
      gap: 4px;
    }

    .modal-title {
      font-family: 'Google Sans', sans-serif;
      font-size: 1.3rem;
      font-weight: 700;
      color: var(--text-primary);
    }

    .modal-close {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-secondary);
      border-radius: 8px;
      width: 36px;
      height: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-size: 1.2rem;
      transition: all 0.15s ease;
    }

    .modal-close:hover {
      color: var(--text-primary);
      border-color: var(--border-focus);
    }

    .modal-body {
      padding: 24px;
      flex: 1;
    }

    .modal-meta-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
      gap: 12px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 14px;
      margin-bottom: 20px;
    }

    .modal-meta-item {
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
      word-break: break-word;
      overflow-wrap: break-word;
    }

    .modal-meta-label {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
    }

    .modal-meta-value {
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--text-primary);
      word-break: break-word;
      overflow-wrap: break-word;
    }

    .modal-section-title {
      font-size: 0.95rem;
      font-weight: 700;
      color: var(--accent-blue);
      margin-bottom: 10px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .modal-box {
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 16px;
      margin-bottom: 20px;
      font-size: 0.9rem;
      line-height: 1.6;
      color: var(--text-secondary);
    }

    .modal-box strong {
      color: var(--text-primary);
    }

    .modal-turns-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .modal-turns-list li {
      font-size: 0.86rem;
      color: var(--text-secondary);
      line-height: 1.5;
      background: var(--bg-card);
      padding: 10px 14px;
      border-radius: 8px;
      border-left: 3px solid var(--accent-indigo);
    }

    .modal-turns-list strong {
      color: var(--text-primary);
    }

    .modal-footer {
      padding: 16px 24px;
      border-top: 1px solid var(--border-color);
      display: flex;
      justify-content: flex-end;
      gap: 12px;
    }

    /* Architecture Blueprint Visual Component */
    .modal-dialog.arch-dialog {
      max-width: 1040px;
    }

    .arch-flow-container {
      display: flex;
      flex-direction: column;
      gap: 14px;
      margin-bottom: 20px;
    }

    .arch-layer-card {
      background: var(--bg-surface);
      border: 1px solid var(--border-faint);
      border-radius: 12px;
      padding: 16px 18px;
    }

    .arch-layer-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
      margin-bottom: 12px;
      flex-wrap: wrap;
      gap: 8px;
    }

    .arch-layer-title {
      font-family: 'Google Sans', sans-serif;
      font-size: 1rem;
      font-weight: 700;
      color: var(--text-primary);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .arch-layer-pill {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 8px;
      padding: 3px 10px;
      border-radius: 9999px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--accent-blue);
      font-family: 'JetBrains Mono', monospace;
    }

    .arch-layer-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 10px;
    }

    .arch-item {
      background: var(--bg-card);
      border: 1px solid var(--border-faint);
      border-radius: 8px;
      padding: 10px 12px;
      font-size: 0.8rem;
      color: var(--text-secondary);
      line-height: 1.45;
    }

    .arch-item strong {
      display: block;
      color: var(--text-primary);
      margin-bottom: 3px;
      margin-bottom: 4px;
      font-size: 0.84rem;
    }

    .arch-subagents-row {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      gap: 12px;
    }

    @media (max-width: 640px) {
    .arch-subagent-box {
      background: var(--bg-card);
      border: 1px solid var(--border-faint);
      border-radius: 8px;
      padding: 12px 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }

    .arch-subagent-tag {
      font-size: 0.84rem;
      font-weight: 700;
      font-family: 'Google Sans', sans-serif;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    @media (max-width: 680px) {
      .arch-subagents-row {
        grid-template-columns: 1fr;
      }
    }

    .arch-arrow {
      text-align: center;
      color: var(--accent-blue);
      font-size: 1.1rem;
      line-height: 1;
      margin: -6px 0;
      opacity: 0.85;
    }

    /* Footer */
    .site-footer {
      background: var(--bg-secondary);
      border-top: 1px solid var(--border-color);
      padding: 32px 24px;
      margin-top: 48px;
      text-align: center;
    }

    .footer-inner {
      max-width: 1400px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 12px;
    }

    .footer-text {
      font-size: 0.86rem;
      color: var(--text-secondary);
      max-width: 600px;
      line-height: 1.5;
    }

    .footer-links {
      display: flex;
      gap: 18px;
      margin-top: 4px;
    }

    .footer-link {
      color: var(--accent-blue);
      text-decoration: none;
      font-size: 0.84rem;
      font-weight: 500;
    }

    .footer-link:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <!-- Site Header -->
  <header class="site-header">
    <div class="header-inner">
      <a href="#" class="brand-logo">
        <span class="brand-icon">⚡</span>
        <div class="brand-text">
          <span class="brand-title">Gemini Enterprise Agents for Utilities</span>
          <span class="brand-subtitle">Google ADK & Gemini Enterprise Ready</span>
        </div>
      </a>
      <div class="header-actions">
        <button id="archBtn" class="btn-header" aria-label="View Architecture Blueprint">
          <span>📐</span> Architecture Blueprint
        </button>
        <button id="themeToggleBtn" class="btn-header" aria-label="Toggle Light/Dark Theme">
          <span id="themeIcon">☀️</span> <span id="themeText">Light</span>
        </button>
        <a href="https://github.com/FCLW/Utilities-Agents" target="_blank" rel="noopener noreferrer" class="btn-header" aria-label="View GitHub Repository">
          <svg width="15" height="15" viewBox="0 0 24 24" fill="currentColor" style="vertical-align: -2px; margin-right: 4px;"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg> GitHub
        </a>
        <a href="https://vertexaisearch.cloud.google.com/home/cid/4d886c3b-e9e0-419c-a168-d25114e2dad6" target="_blank" rel="noopener noreferrer" class="btn-header btn-primary-header">
          <span>✨</span> Gemini App (GE access required)
        </a>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="hero">
    <div class="hero-pill">
      <span>🚀</span> 113 Enterprise Agents Fully Deployed across 11 Utilities Domains
    </div>
    <h1 class="hero-title">
      Gemini Enterprise Agents for <span>Utilities</span>
    </h1>
    <p class="hero-desc">
      A declarative, multi-agent platform powered by Google Agent Development Kit (ADK), Gemini Enterprise, and BigQuery Conversational Analytics. Real-time quantitative querying against enterprise utility datasets, grounded with external Google Search market intelligence.
    </p>

    <!-- Platform Stats -->
    <div class="stat-row">
      <div class="stat-card">
        <div class="stat-number">113</div>
        <div class="stat-label">Gemini Enterprise Agents</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">11</div>
        <div class="stat-label">Utilities Sub-Domains</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">113+</div>
        <div class="stat-label">BigQuery Datasets & Tables</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">2</div>
        <div class="stat-label">GCP Regions (us-central1, us-east4)</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">100%</div>
        <div class="stat-label">Production Ready (ADK v2)</div>
      </div>
    </div>
  </section>

  <!-- Main Content Area -->
  <main class="main-container">
    
    <!-- Toolbar: Search & Domain Filters -->
    <section class="toolbar">
      <div class="search-row">
        <div class="search-input-wrapper">
          <span class="search-icon">🔍</span>
          <input type="text" id="searchInput" class="search-input" placeholder="Search 113 agents by name, KPI (e.g. AHI, RUL, SAIDI, VaR), persona, business question, or BigQuery table..." autocomplete="off">
          <button id="searchClear" class="search-clear" aria-label="Clear search">✕</button>
        </div>
      </div>

      <!-- Domain Pills -->
      <div class="domain-pills" id="domainPills">
        __DOMAIN_PILLS__
      </div>
    </section>

    <!-- Results Header -->
    <div class="results-bar">
      <div class="results-count" id="resultsCount">
        Showing <strong>113</strong> of 113 enterprise agents
      </div>
    </div>

    <!-- Agent Grid -->
    <div class="agent-grid" id="agentGrid">
      <!-- Injected via JavaScript -->
    </div>

    <!-- No Results Fallback -->
    <div class="no-results" id="noResults">
      <div class="no-results-icon">🔎</div>
      <div class="no-results-title">No Matching Enterprise Agents Found</div>
      <p class="no-results-desc">Try refining your search keyword or switching domain filter tabs.</p>
      <button class="btn-header" onclick="resetFilters()">Reset All Filters</button>
    </div>

  </main>

  <!-- Agent Details Modal -->
  <div class="modal-backdrop" id="agentModal">
    <div class="modal-dialog">
      <div class="modal-header">
        <div class="modal-title-wrap">
          <div style="display:flex; gap:8px; align-items:center; margin-bottom:4px;">
            <span id="modalDomainBadge" class="badge-domain">Domain</span>
            <span id="modalRegionBadge" class="badge-region">us-central1</span>
            <span id="modalModelBadge" class="badge-model">gemini-3.7-flash</span>
          </div>
          <h2 id="modalAgentTitle" class="modal-title">Agent Title</h2>
        </div>
        <button class="modal-close" id="modalCloseBtn" aria-label="Close modal">✕</button>
      </div>
      <div class="modal-body">

        <div class="modal-meta-grid">
          <div class="modal-meta-item">
            <span class="modal-meta-label">Target Persona</span>
            <span class="modal-meta-value" id="modalPersona">Reliability Engineer</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Reasoning Engine</span>
            <span class="modal-meta-value" id="modalReasoningEngine">Vertex AI (Live)</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Primary KPI</span>
            <span class="modal-meta-value" id="modalKpi">Asset Health Index (AHI)</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">BigQuery Table</span>
            <span class="modal-meta-value" id="modalTable" style="font-family:'JetBrains Mono',monospace; font-size:0.8rem; word-break: break-all; overflow-wrap: anywhere;">utilities.table</span>
          </div>
          <div class="modal-meta-item">
            <span class="modal-meta-label">Gemini Agent ID</span>
            <span class="modal-meta-value" id="modalGeAgentId" style="font-family:'JetBrains Mono',monospace; font-size:0.8rem;">10424690685175366976</span>
          </div>
        </div>

        <div class="modal-section-title">
          <span>🎯</span> Business Problem & Solution
        </div>
        <div class="modal-box" id="modalProblemSolution">
          Problem and solution description.
        </div>

        <div class="modal-section-title" id="modalDemoTitle">
          <span>💬</span> Sample Business Questions
        </div>
        <ul class="modal-turns-list" id="modalTurnsList">
          <!-- Populated dynamically -->
        </ul>

      </div>
      <div class="modal-footer">
        <a id="modalGeBtn" href="#" target="_blank" rel="noopener noreferrer" class="btn-watch" style="text-decoration:none;">
          <span>✨</span> Launch in Gemini Enterprise (GE access required)
        </a>
        <a id="modalDemoBtn" href="#" target="_blank" rel="noopener noreferrer" class="btn-showcase">
          <span>🎬</span> Watch Demo
        </a>
        <a id="modalSpecBtn" href="#" target="_blank" rel="noopener noreferrer" class="btn-doc" style="text-decoration:none;">
          <span>🔍</span> View Spec
        </a>
        <button class="btn-header" id="modalDismissBtn">Close</button>
      </div>
    </div>
  </div>

  <!-- Architecture Modal -->
  <div class="modal-backdrop" id="archModal">
    <div class="modal-dialog">
    <div class="modal-dialog arch-dialog">
      <div class="modal-header">
        <div class="modal-title-wrap">
          <div style="display:flex; gap:8px; align-items:center; margin-bottom:4px;">
            <span class="badge-domain">Architecture Spec</span>
            <span class="badge-region">Global & Multi-Region</span>
          <div style="display:flex; gap:8px; align-items:center; margin-bottom:6px; flex-wrap:wrap;">
            <span class="badge-domain">Google ADK v2.0 Enterprise</span>
            <span class="badge-region">113 Production Agents (11 Domains)</span>
            <span class="badge-model">Vertex AI & Cloud Run (us-central1)</span>
          </div>
          <h2 class="modal-title">📐 Utilities Enterprise Multi-Agent Architecture</h2>
          <h2 class="modal-title">📐 Utilities Enterprise 4-Tier ADK Architecture Blueprint</h2>
        </div>
        <button class="modal-close" id="archCloseBtn" aria-label="Close modal">✕</button>
      </div>
      <div class="modal-body">
        <p style="color:var(--text-secondary); margin-bottom:20px; font-size:0.9rem; line-height:1.5;">
          End-to-end architecture blueprint connecting 113 specialized Energy & Utilities agents across 11 core sub-domains, orchestrating real-time BigQuery telemetry queries and grounded industry intelligence via Google Agent Development Kit (ADK) and Gemini Enterprise.
        <p style="color:var(--text-secondary); margin-bottom:20px; font-size:0.92rem; line-height:1.55;">
          End-to-end multi-agent system architecture connecting <strong>113 specialized Energy & Utilities agents</strong> across <strong>11 core sub-domains</strong>, orchestrating real-time BigQuery telemetry queries, dynamic visual charting, and grounded industry intelligence via Google Agent Development Kit (ADK), Gemini Enterprise, and Cloud Run.
        </p>

        <div class="arch-flow-container">
          <!-- Tier 1 -->
          <div class="arch-layer-card" style="border-top: 3px solid var(--accent-blue);">
            <div class="arch-layer-header">
              <div class="arch-layer-title">
                <span>🖥️</span> Tier 1: Gemini Enterprise Natural Language Workspace
                <span>🖥️</span> Tier 1: Experience & Delivery Layer
              </div>
              <span class="arch-layer-pill">Gemini Enterprise App</span>
              <span class="arch-layer-pill">Gemini Enterprise + Cloud Run (IAP)</span>
            </div>
            <div class="arch-layer-grid">
              <div class="arch-item">
                <strong>Natural Language Chat Interface</strong>
                Unified conversational UI for utility executives, dispatchers & engineers
                <strong>Gemini Enterprise (GE) Workspace App</strong>
                Conversational UI integrated into Google Workspace with dedicated agent personas, direct chat, and @-mentions.
              </div>
              <div class="arch-item">
                <strong>Enterprise Search & Agent Gateway</strong>
                113 Registered Enterprise Agents searchable via natural language chat
                <strong>Interactive Cloud Run Web Showcase</strong>
                Containerized Nginx portal (`utilities-agents-portal`) secured by Identity-Aware Proxy (IAP) for `@google.com` users with faceted domain filtering.
              </div>
              <div class="arch-item">
                <strong>Gemini Canvas Workspace</strong>
                Artifact rendering, dynamic operational dashboards & executive briefing export
                <strong>Dual-Streaming Video Engine</strong>
                High-throughput same-origin HTTP 206 byte-range streaming bundled directly into Cloud Run behind IAP, plus authenticated GCS Console fallback.
              </div>
              <div class="arch-item">
                <strong>Inline Markdown Technical Specs</strong>
                All 113 agent READMEs served locally from `/readmes/` with UTF-8 markdown MIME typing for seamless in-browser viewing.
              </div>
            </div>
          </div>

          <div class="arch-arrow">▼</div>

          <!-- Tier 2 -->
          <div class="arch-layer-card" style="border-top: 3px solid var(--accent-amber);">
            <div class="arch-layer-header">
              <div class="arch-layer-title">
                <span>🎯</span> Tier 2: Master Orchestrator & Domain Lead Agents
                <span>🎯</span> Tier 2: Agent Orchestration & Master Router
              </div>
              <span class="arch-layer-pill">ADK v2.0 Multi-Agent Router</span>
              <span class="arch-layer-pill" style="color:var(--accent-amber); border-color:var(--accent-amber);">Vertex AI Reasoning Engine</span>
            </div>
            <div class="arch-layer-grid">
              <div class="arch-item">
                <strong>Intent Classification Router</strong>
                Routes incoming utility inquiries to the exact sub-domain lead
                <strong>Utilities Master Orchestrator</strong>
                Universal entrypoint (`utilities_master_orchestrator`) handling global natural language intent triage and multi-agent decomposition.
              </div>
              <div class="arch-item">
                <strong>Global Model Inference</strong>
                `gemini-3.7-flash` & `gemini-3.1-pro` for reasoning and rapid triage
                <strong>Agent-to-Agent (A2A) Protocol</strong>
                Autonomous routing to downstream domain agents across Asset Management, Grid Balancing, Trading, Outage Ops, etc.
              </div>
              <div class="arch-item">
                <strong>Lifecycle Callbacks</strong>
                IAM token scoping, grid zone injection & dataset context binding
                <strong>Dual Model Inference Fleet</strong>
                High-velocity real-time triage via `gemini-3.7-flash` and deep analytical reasoning via `gemini-3.1-pro`.
              </div>
              <div class="arch-item">
                <strong>Shared Session State & Observability</strong>
                Propagates `customer_id`, `grid_zone_id`, `operating_mode`, and `alert_level` with OpenTelemetry and Cloud Trace distributed spans.
              </div>
            </div>
          </div>

          <div class="arch-arrow">▼</div>

          <!-- Tier 3: Parallel Sub-Agents -->
          <div class="arch-subagents-row">
            <div class="arch-layer-card" style="border-top: 3px solid var(--accent-emerald);">
              <div class="arch-layer-header">
                <div class="arch-layer-title" style="font-size:0.95rem;">
                  <span>📊</span> Sub-Agent 3A: BigQuery Telemetry & Data Insights
          <!-- Tier 3: Parallel Sub-Agents & Tools -->
          <div class="arch-layer-card" style="border-top: 3px solid var(--accent-emerald);">
            <div class="arch-layer-header">
              <div class="arch-layer-title">
                <span>⚙️</span> Tier 3: Specialist Sub-Agents & Tool Suite
              </div>
              <span class="arch-layer-pill" style="color:var(--accent-emerald); border-color:var(--accent-emerald);">ADK Task Lead: Worker + Critic Gate</span>
            </div>
            
            <div class="arch-subagents-row" style="margin-bottom: 12px;">
              <div class="arch-subagent-box">
                <div class="arch-subagent-tag" style="color:var(--accent-emerald);">⚡ Execution Sub-Agent (Worker)</div>
                <div class="arch-item" style="border:none; padding:4px 0 0 0; background:transparent;">
                  Executes specialized domain algorithms, scenario modeling, load curve forecasting, and read-only parameterized BigQuery SQL queries.
                </div>
                <span class="arch-layer-pill" style="color:var(--accent-emerald); background:var(--kpi-bg); border-color:var(--kpi-border);">Conversational Analytics</span>
              </div>
              <div style="display:flex; flex-direction:column; gap:8px;">
                <div class="arch-item">
                  <strong>Natural Language to SQL Engine</strong>
                  Conversational Analytics executes parameterized BigQuery SQL directly
              <div class="arch-subagent-box">
                <div class="arch-subagent-tag" style="color:var(--accent-amber);">🛡️ Critic Sub-Agent (Safety Gatekeeper)</div>
                <div class="arch-item" style="border:none; padding:4px 0 0 0; background:transparent;">
                  Mandatory evaluator. Intercepts outputs, validates against `safety_guardrails.md`, checks for hallucinations or PII leaks, and formats structured Markdown tables before returning control.
                </div>
                <div class="arch-item">
                  <strong>Built-in ML Models</strong>
                  BigQuery forecasting, anomaly detection & asset health trend analysis
                </div>
                <div class="arch-item">
                  <strong>Telemetry Aggregator</strong>
                  Smart meter AMI, SCADA, sensor, and grid telemetry correlation
                </div>
              </div>
            </div>

            <div class="arch-layer-card" style="border-top: 3px solid var(--accent-blue);">
              <div class="arch-layer-header">
                <div class="arch-layer-title" style="font-size:0.95rem;">
                  <span>🌐</span> Sub-Agent 3B: Industry & Regulatory Grounding
                </div>
                <span class="arch-layer-pill">Google Search Grounding</span>
            <div class="arch-layer-grid">
              <div class="arch-item">
                <strong>BigQuery Tool (`bigquery_tool.py`)</strong>
                Parameterized read-only SQL with regex validation blocking mutative DDL/DML (`DROP`, `DELETE`, `INSERT`, `ALTER`, `TRUNCATE`).
              </div>
              <div style="display:flex; flex-direction:column; gap:8px;">
                <div class="arch-item">
                  <strong>Real-Time Web Grounding</strong>
                  Live Google Search verification for fresh energy market prices & weather
                </div>
                <div class="arch-item">
                  <strong>Regulatory Standards</strong>
                  FERC, NERC, IEEE, OSHA compliance rules & regional reliability benchmarks
                </div>
                <div class="arch-item">
                  <strong>Wholesale Market Intelligence</strong>
                  ISO/RTO real-time LMP, spark spreads, REC, and carbon allowance trading
                </div>
              <div class="arch-item">
                <strong>Search Grounding (`search_tool.py`)</strong>
                Live Google Search verification for fresh energy market prices (LMP, spark spreads, REC), weather forecasts, and regulatory rules.
              </div>
              <div class="arch-item">
                <strong>Visualizer Tool (`visualizer.py`)</strong>
                Dynamic Matplotlib chart generator rendering operational graphs, load curves, heat rates, and asset health diagrams.
              </div>
              <div class="arch-item">
                <strong>Delegation Tool (`delegation_tool.py`)</strong>
                A2A protocol dispatcher executing synchronous and asynchronous sub-task handoffs between domain specialists.
              </div>
            </div>
          </div>

          <div class="arch-arrow">▼</div>

          <!-- Tier 4 -->
          <div class="arch-layer-card" style="border-top: 3px solid var(--accent-indigo);">
            <div class="arch-layer-header">
              <div class="arch-layer-title">
                <span>🗄️</span> Tier 4: Enterprise Utilities BigQuery Lakehouse
              </div>
              <span class="arch-layer-pill" style="color:var(--region-text); background:var(--region-bg); border-color:var(--region-border);">Google Cloud BigQuery</span>
              <span class="arch-layer-pill" style="color:var(--accent-indigo); border-color:var(--accent-indigo);">Google Cloud BigQuery</span>
            </div>
            <div class="arch-layer-grid">
              <div class="arch-item">
                <strong>Enterprise Dataset</strong>
                `utilities_agents` multi-tenant energy & utilities schema
                <strong>113 Partitioned & Clustered Tables</strong>
                Governed by `table_registry.yaml`, covering SCADA telemetry, AMI interval VEE, asset health DGA, and wholesale trading logs.
              </div>
              <div class="arch-item">
                <strong>113+ Partitioned Tables</strong>
                Structured telemetry namespace across all 11 sub-domains
                <strong>Least-Privilege Security Isolation</strong>
                Dedicated IAM service account per agent (`<agent>@utilities-agents.iam.gserviceaccount.com`) granted strictly `roles/bigquery.dataViewer` and `roles/bigquery.jobUser`.
              </div>
              <div class="arch-item">
                <strong>IAM Table Allowlisting</strong>
                Strict per-agent service account dataset authorization & row-level security
                <strong>Synthetic Data & Schema Pipeline</strong>
                Dedicated DDL schemas (`schema.sql`), seed data (`seed_data.sql`), and sample CSV fixtures (`mock_records.csv`) per agent.
              </div>
              <div class="arch-item">
                <strong>Tiered Authorization (HITL)</strong>
                Autonomous execution for read/simulate analytics; physical grid state changes (e.g., FLISR) or financial bids require human-in-the-loop operator confirmation.
              </div>
            </div>
          </div>
        </div>

        <div class="modal-turns">
        <div class="modal-turns" style="margin-top:20px;">
          <div class="modal-section-title">
            <span>🚀</span> Key Architectural Pillars
          </div>
          <ul class="modal-turns-list">
            <li><strong>Declarative ADK Architecture:</strong> Zero-code orchestrator models bind BigQuery tools and Google Search tools with strict sub-domain boundaries.</li>
            <li><strong>Distributed Vertex AI Hosting:</strong> High-density reasoning engine deployment across `us-central1` and `us-east4` ensures zero quota bottlenecks.</li>
            <li><strong>Dual Sub-Agent Pattern:</strong> Quantitative BigQuery queries and qualitative market grounding execute in specialized sub-agent contexts for hallucination-free answers.</li>
            <li><strong>Strict Single-Purpose Scope (113 Production Agents across 11 Domains):</strong> Universal Master Orchestrator + 10 specialized industry sub-domains ensuring atomic responsibilities, zero bloat, and low cognitive load.</li>
            <li><strong>The Critic Protocol (Automated Gatekeeper + HITL):</strong> Every specialized agent contains an internal Critic sub-agent that audits safety guardrails and prevents hallucinated metrics before any response leaves the agent boundary.</li>
            <li><strong>Modular Prompt Composition:</strong> Dynamic runtime assembly of 4 modular prompt layers (`persona.md`, `business_rules.md`, `output_format.md`, and `safety_guardrails.md`) for maintainable governance.</li>
            <li><strong>Dual-Tier High-Performance Video Delivery:</strong> Native byte-range streaming bundled into Cloud Run Nginx behind Google IAP eliminates cross-origin cookie friction for corporate `@google.com` users, backed by authenticated GCS fallback.</li>
          </ul>
        </div>
      </div>
      <div class="modal-footer">
        <button class="btn-header btn-primary-header" id="archOkBtn">Close Blueprint</button>
      </div>
    </div>
  </div>

  <!-- Site Footer -->
  <footer class="site-footer">
    <div class="footer-inner">
      <div class="brand-logo" style="justify-content: center;">
        <span class="brand-icon">⚡</span>
        <span class="brand-title">Gemini Enterprise Agents for Utilities</span>
      </div>
      <p class="footer-text">
        113 Enterprise Agents across 11 Strategic Utilities Domains. Powered by Google ADK, Gemini Enterprise, and BigQuery.
      </p>
      <div class="footer-links">
        <a href="https://vertexaisearch.cloud.google.com/home/cid/4d886c3b-e9e0-419c-a168-d25114e2dad6" target="_blank" rel="noopener noreferrer" class="footer-link">Gemini Enterprise App</a>
        <a href="https://github.com/FCLW/Utilities-Agents" target="_blank" rel="noopener noreferrer" class="footer-link">GitHub Repository</a>
        <a href="#" id="archFooterLink" class="footer-link">Architecture Blueprint</a>
      </div>
    </div>
  </footer>

  <!-- Embedded JSON Data & Client Application Script -->
  <script>
    const AGENTS_DATA = __AGENTS_JSON__;

    // State Variables
    let activeDomain = 'all';
    let searchQuery = '';

    // DOM Elements
    const agentGrid = document.getElementById('agentGrid');
    const resultsCount = document.getElementById('resultsCount');
    const noResults = document.getElementById('noResults');
    const searchInput = document.getElementById('searchInput');
    const searchClear = document.getElementById('searchClear');
    const domainPills = document.getElementById('domainPills');
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const themeText = document.getElementById('themeText');

    // Agent Details Modal Elements
    const agentModal = document.getElementById('agentModal');
    const modalAgentTitle = document.getElementById('modalAgentTitle');
    const modalDomainBadge = document.getElementById('modalDomainBadge');
    const modalRegionBadge = document.getElementById('modalRegionBadge');
    const modalModelBadge = document.getElementById('modalModelBadge');
    const modalPersona = document.getElementById('modalPersona');
    const modalReasoningEngine = document.getElementById('modalReasoningEngine');
    const modalKpi = document.getElementById('modalKpi');
    const modalTable = document.getElementById('modalTable');
    const modalGeAgentId = document.getElementById('modalGeAgentId');
    const modalProblemSolution = document.getElementById('modalProblemSolution');
    const modalTurnsList = document.getElementById('modalTurnsList');
    const modalGeBtn = document.getElementById('modalGeBtn');
    const modalDemoBtn = document.getElementById('modalDemoBtn');
    const modalSpecBtn = document.getElementById('modalSpecBtn');
    const modalCloseBtn = document.getElementById('modalCloseBtn');
    const modalDismissBtn = document.getElementById('modalDismissBtn');

    // Architecture Modal Elements
    const archBtn = document.getElementById('archBtn');
    const archModal = document.getElementById('archModal');
    const archCloseBtn = document.getElementById('archCloseBtn');
    const archOkBtn = document.getElementById('archOkBtn');
    const archFooterLink = document.getElementById('archFooterLink');

    // Theme Management
    function initTheme() {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      updateThemeUI(current);
    }

    function updateThemeUI(theme) {
      if (theme === 'light') {
        themeIcon.textContent = '🌙';
        themeText.textContent = 'Dark';
      } else {
        themeIcon.textContent = '☀️';
        themeText.textContent = 'Light';
      }
    }

    themeToggleBtn.addEventListener('click', () => {
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('utilities_agents_theme', next);
      updateThemeUI(next);
    });

    // Render Cards
    function renderAgents() {
      const query = searchQuery.toLowerCase().trim();
      
      const filtered = AGENTS_DATA.filter(agent => {
        const matchesDomain = activeDomain === 'all' || agent.domain === activeDomain;
        if (!matchesDomain) return false;

        if (!query) return true;

        const textPool = [
          agent.display_name,
          agent.name,
          agent.id,
          agent.domain_display,
          agent.persona,
          agent.problem,
          agent.solution,
          agent.description,
          agent.location,
          agent.model,
          ...(agent.kpis || []),
          ...(agent.prompts || []),
          ...(agent.tables || [])
        ].join(' ').toLowerCase();

        return textPool.includes(query);
      });

      resultsCount.innerHTML = `Showing <strong>${filtered.length}</strong> of ${AGENTS_DATA.length} enterprise agents`;

      if (filtered.length === 0) {
        agentGrid.innerHTML = '';
        noResults.style.display = 'block';
        return;
      }

      noResults.style.display = 'none';

      agentGrid.innerHTML = filtered.map(agent => {
        const kpiPills = (agent.kpis || []).map(kpi => 
          `<span class="kpi-pill">🎯 ${htmlEscape(kpi)}</span>`
        ).join('');

        const promptItems = (agent.prompts || []).map((prompt, idx) => 
          `<div class="prompt-item">"${htmlEscape(prompt)}"</div>`
        ).join('');

        const tablePill = (agent.tables && agent.tables.length > 0) ?
          `<div class="table-tag" title="${htmlEscape(agent.tables[0])}">🗄️ <code>${htmlEscape(agent.tables[0])}</code></div>` : '';

        return `
          <div class="agent-card" data-agent-id="${agent.id}">
            <div class="card-top">
              <div class="card-badges">
                <span class="badge-domain">${agent.icon} ${htmlEscape(agent.domain_display)}</span>
                <span class="badge-region">${agent.location}</span>
                <span class="badge-model">${agent.model}</span>
              </div>
            </div>
            <h3 class="card-title" onclick="openAgentModal('${agent.id}', 'spec')" style="cursor:pointer;" title="View Details">${htmlEscape(agent.display_name)}</h3>
            <div class="card-persona">👤 ${htmlEscape(agent.persona)}</div>
            <p class="card-desc">
              <strong>Problem:</strong> ${htmlEscape(agent.problem)}<br>
              <strong>Solution:</strong> ${htmlEscape(agent.solution)}
            </p>

            ${kpiPills ? `<div class="kpi-row">${kpiPills}</div>` : ''}
            ${tablePill}

            ${promptItems ? `
              <div class="prompts-container">
                <button class="prompts-toggle" onclick="togglePrompts(this)">
                  <span>💬 Sample Business Questions (${agent.prompts.length})</span>
                  <span class="toggle-icon">▼</span>
                </button>
                <div class="prompts-list">
                  ${promptItems}
                </div>
              </div>
            ` : ''}

            <div class="card-actions">
              <a href="${agent.ge_url}" target="_blank" rel="noopener noreferrer" class="btn-watch" title="Launch in Gemini Enterprise App">
                <span>✨</span> Gemini App (GE access required)
              </a>
              <a href="${agent.demo_html}" target="_blank" rel="noopener noreferrer" class="btn-showcase" title="Watch Multi-Turn Conversation Demo">
                <span>🎬</span> Watch Demo
              </a>
              <a href="${agent.spec_url}" target="_blank" rel="noopener noreferrer" class="btn-doc" title="View Technical Spec (Markdown)">
                <span>🔍</span> Spec
              </a>
            </div>
          </div>
        `;
      }).join('');
    }

    function togglePrompts(btn) {
      const list = btn.nextElementSibling;
      const icon = btn.querySelector('.toggle-icon');
      if (list.classList.contains('open')) {
        list.classList.remove('open');
        icon.textContent = '▼';
      } else {
        list.classList.add('open');
        icon.textContent = '▲';
      }
    }

    function htmlEscape(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
    }

    // Search input handler
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      searchClear.style.display = searchQuery ? 'block' : 'none';
      renderAgents();
    });

    searchClear.addEventListener('click', () => {
      searchInput.value = '';
      searchQuery = '';
      searchClear.style.display = 'none';
      renderAgents();
      searchInput.focus();
    });

    // Domain Filter Handler
    domainPills.addEventListener('click', (e) => {
      const btn = e.target.closest('.domain-btn');
      if (!btn) return;

      document.querySelectorAll('.domain-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      activeDomain = btn.dataset.domain;
      renderAgents();
    });

    function resetFilters() {
      searchInput.value = '';
      searchQuery = '';
      searchClear.style.display = 'none';
      activeDomain = 'all';
      document.querySelectorAll('.domain-btn').forEach(b => {
        b.classList.toggle('active', b.dataset.domain === 'all');
      });
      renderAgents();
    }

    // Agent Details Modal
    function openAgentModal(agentId, section = 'spec') {
      const agent = AGENTS_DATA.find(a => a.id === agentId);
      if (!agent) return;

      modalAgentTitle.textContent = agent.display_name;
      modalDomainBadge.innerHTML = `${agent.icon} ${agent.domain_display}`;
      modalRegionBadge.textContent = agent.location;
      modalModelBadge.textContent = agent.model;
      modalPersona.textContent = agent.persona || 'Energy & Utilities Specialist';
      modalReasoningEngine.textContent = `Vertex AI (${agent.location})`;
      modalKpi.textContent = (agent.kpis && agent.kpis.length > 0) ? agent.kpis.join(', ') : 'Asset Health & Reliability';
      modalTable.textContent = (agent.tables && agent.tables.length > 0) ? agent.tables[0] : 'utilities_agents.logs';
      if (modalGeAgentId) modalGeAgentId.textContent = agent.ge_agent_id || 'N/A';
      
      modalProblemSolution.innerHTML = `
        <div style="margin-bottom:8px;"><strong>⚠️ Primary Business Problem:</strong> ${htmlEscape(agent.problem)}</div>
        <div><strong>💡 Autonomous Solution:</strong> ${htmlEscape(agent.solution)}</div>
      `;

      if (agent.prompts && agent.prompts.length > 0) {
        modalTurnsList.innerHTML = agent.prompts.map((p, idx) => `
          <li><strong>Question ${idx + 1}:</strong> "${htmlEscape(p)}"</li>
        `).join('');
      } else {
        modalTurnsList.innerHTML = `<li><strong>Question 1:</strong> "Analyze active anomalies and recommend operational next steps."</li>`;
      }

      modalGeBtn.href = agent.ge_url;
      modalDemoBtn.href = agent.demo_html;
      if (modalSpecBtn) modalSpecBtn.href = agent.spec_url;

      agentModal.classList.add('open');
      document.body.style.overflow = 'hidden';

      const modalBody = agentModal.querySelector('.modal-body');
      if (section === 'demo') {
        const demoTitle = document.getElementById('modalDemoTitle');
        if (demoTitle) {
          setTimeout(() => {
            demoTitle.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }, 80);
        }
      } else {
        if (modalBody) modalBody.scrollTop = 0;
      }
    }

    function closeAgentModal() {
      agentModal.classList.remove('open');
      document.body.style.overflow = '';
    }

    modalCloseBtn.addEventListener('click', closeAgentModal);
    modalDismissBtn.addEventListener('click', closeAgentModal);
    agentModal.addEventListener('click', (e) => {
      if (e.target === agentModal) closeAgentModal();
    });

    // Architecture Modal Handlers
    function openArchModal() {
      archModal.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeArchModal() {
      archModal.classList.remove('open');
      document.body.style.overflow = '';
    }

    archBtn.addEventListener('click', openArchModal);
    if (archFooterLink) {
      archFooterLink.addEventListener('click', (e) => {
        e.preventDefault();
        openArchModal();
      });
    }
    archCloseBtn.addEventListener('click', closeArchModal);
    archOkBtn.addEventListener('click', closeArchModal);
    archModal.addEventListener('click', (e) => {
      if (e.target === archModal) closeArchModal();
    });

    // ESC key listener for modals
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') {
        if (agentModal.classList.contains('open')) closeAgentModal();
        if (archModal.classList.contains('open')) closeArchModal();
      }
    });

    // Initial Load
    initTheme();
    renderAgents();
  </script>
</body>
</html>
"""

final_html = template.replace("__DOMAIN_PILLS__", domain_pills_block).replace("__AGENTS_JSON__", agents_json_str)

with open("web/index.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("Generated web/index.html with all 113 agents and 11 sub-domains successfully.")
