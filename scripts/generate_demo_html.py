#!/usr/bin/env python3
"""
generate_demo_html.py — Standalone HTML Demo Video Showcase Generator for Utilities Agents

Generates high-fidelity, responsive HTML5 video showcase pages for recorded agent demo MP4s
matching the standard Gemini Enterprise demo player design (dual light/dark theme, navigation bar,
badge row, metadata grid, multi-turn conversation flow breakdown, and links).
"""

import argparse
import html
import json
from pathlib import Path
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.prompt_parser import get_catalog_entry, parse_agent_prompts, resolve_agent_domain

DOMAIN_ICONS = {
    "asset_management": "⚡",
    "billing_and_invoicing": "💳",
    "customer_engagement": "👥",
    "grid_balancing": "⚖️",
    "grid_operations": "🔌",
    "master_orchestrator": "🎯",
    "production_forecasting": "📈",
    "regulatory_compliance": "📜",
    "smart_meter_management": "📡",
    "support_services": "🛠️",
    "wholesale_trading": "📊",
}

DOMAIN_TITLES = {
    "asset_management": "Asset Management & Reliability",
    "billing_and_invoicing": "Billing & Invoicing",
    "customer_engagement": "Customer Engagement & Experience",
    "grid_balancing": "Grid Balancing & Frequency Regulation",
    "grid_operations": "Grid Operations & Outage Management",
    "master_orchestrator": "Master Orchestrator",
    "production_forecasting": "Production Forecasting & DER",
    "regulatory_compliance": "Regulatory Compliance & Audit",
    "smart_meter_management": "Smart Meter & AMI Management",
    "support_services": "Support Services & Dispatch",
    "wholesale_trading": "Wholesale Trading & Market Operations",
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{page_title}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <script>
    (function() {{
      const savedTheme = localStorage.getItem('utilities_agents_theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
      document.documentElement.setAttribute('data-theme', savedTheme);
    }})();
  </script>

  <style>
    :root, [data-theme="dark"] {{
      --bg-primary: #0b1120;
      --bg-card: #131c31;
      --bg-surface: #0f172a;
      --border-color: #27354f;
      --border-faint: rgba(255, 255, 255, 0.12);
      --text-primary: #f8fafc;
      --text-secondary: #94a3b8;
      --text-muted: #64748b;
      --accent-blue: #38bdf8;
      --accent-teal: #2dd4bf;
      --accent-indigo: #818cf8;
      --badge-bg: rgba(56, 189, 248, 0.12);
      --badge-border: rgba(56, 189, 248, 0.28);
      --badge-text: #38bdf8;
      --shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
    }}

    [data-theme="light"] {{
      --bg-primary: #f8fafc;
      --bg-card: #ffffff;
      --bg-surface: #f1f5f9;
      --border-color: #cbd5e1;
      --border-faint: #cbd5e1;
      --text-primary: #0f172a;
      --text-secondary: #475569;
      --text-muted: #64748b;
      --accent-blue: #0284c7;
      --accent-teal: #0d9488;
      --accent-indigo: #6366f1;
      --badge-bg: #e0f2fe;
      --badge-border: #bae6fd;
      --badge-text: #0284c7;
      --shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.08);
    }}

    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}

    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: var(--bg-primary);
      color: var(--text-primary);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 24px 16px 40px;
      transition: background-color 0.2s ease, color 0.2s ease;
    }}

    .container {{
      max-width: 1100px;
      width: 100%;
      background: var(--bg-card);
      border: 1px solid var(--border-faint);
      border-radius: 16px;
      padding: 28px;
      box-shadow: var(--shadow);
    }}

    .top-nav {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 1px solid var(--border-faint);
    }}

    .nav-back-link {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      color: var(--accent-blue);
      text-decoration: none;
      font-size: 0.88rem;
      font-weight: 600;
      transition: color 0.15s ease;
    }}

    .nav-back-link:hover {{
      text-decoration: underline;
    }}

    .theme-toggle-btn {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      color: var(--text-primary);
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.82rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }}

    .theme-toggle-btn:hover {{
      border-color: var(--accent-blue);
      color: var(--accent-blue);
    }}

    header {{
      margin-bottom: 20px;
    }}

    .badge-row {{
      display: flex;
      gap: 8px;
      margin-bottom: 12px;
      flex-wrap: wrap;
    }}

    .badge {{
      display: inline-flex;
      align-items: center;
      gap: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      padding: 4px 10px;
      border-radius: 9999px;
      background: var(--badge-bg);
      border: 1px solid var(--badge-border);
      color: var(--badge-text);
    }}

    .badge-model {{
      background: rgba(45, 212, 191, 0.12);
      border-color: rgba(45, 212, 191, 0.3);
      color: var(--accent-teal);
    }}

    h1 {{
      font-family: 'Google Sans', sans-serif;
      font-size: 1.7rem;
      font-weight: 700;
      color: var(--text-primary);
      margin-bottom: 6px;
      display: flex;
      align-items: center;
      gap: 10px;
    }}

    p.subtitle {{
      color: var(--text-secondary);
      font-size: 0.95rem;
      line-height: 1.5;
    }}

    .video-wrapper {{
      position: relative;
      width: 100%;
      background: #000;
      border: 1px solid var(--border-faint);
      border-radius: 12px;
      overflow: hidden;
      margin: 20px 0;
      box-shadow: 0 10px 20px -5px rgba(0, 0, 0, 0.5);
    }}

    video {{
      width: 100%;
      display: block;
      max-height: 640px;
    }}

    .meta-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 12px;
      background: var(--bg-surface);
      border: 1px solid var(--border-faint);
      border-radius: 10px;
      padding: 18px;
      margin-bottom: 24px;
    }}

    .meta-item {{
      display: flex;
      flex-direction: column;
      gap: 4px;
    }}

    .meta-label {{
      font-size: 0.75rem;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }}

    .meta-value {{
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--text-primary);
    }}

    .meta-item.full-width {{
      grid-column: 1 / -1;
    }}

    .turns-section {{
      background: var(--bg-surface);
      border: 1px solid var(--border-faint);
      border-radius: 10px;
      padding: 20px;
      margin-bottom: 24px;
    }}

    .turns-section h2 {{
      font-family: 'Google Sans', sans-serif;
      font-size: 1.15rem;
      margin-bottom: 14px;
      color: var(--accent-indigo);
    }}

    .turn-list {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }}

    .turn-list li {{
      font-size: 0.9rem;
      line-height: 1.5;
      color: var(--text-secondary);
    }}

    .turn-list strong {{
      color: var(--text-primary);
    }}

    .app-link-btn {{
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: #2563eb;
      color: #ffffff;
      padding: 8px 16px;
      border-radius: 8px;
      font-size: 0.85rem;
      font-weight: 600;
      text-decoration: none;
      margin-top: 6px;
      transition: background 0.15s ease;
    }}

    .app-link-btn:hover {{
      background: #1d4ed8;
    }}

    footer {{
      margin-top: 24px;
      text-align: center;
      font-size: 0.8rem;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>
  <div class="container">
    <nav class="top-nav">
      <a href="../../index.html" class="nav-back-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
        Back to Utilities Agents Portal
      </a>
      <button class="theme-toggle-btn" onclick="toggleTheme()">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="5"/><path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>
        Toggle Theme
      </button>
    </nav>

    <header>
      <div class="badge-row">
        <span class="badge">{domain_icon} {domain_title}</span>
        <span class="badge badge-model">🧠 {model}</span>
        <span class="badge">Google ADK v2.0</span>
      </div>
      <h1><span>{agent_icon}</span> {display_name}</h1>
      <p class="subtitle">{description}</p>
    </header>

    <div class="video-wrapper">
      <video controls autoplay loop muted playsinline poster="">
        <source src="{agent_name}.mp4" type="video/mp4">
        <source src="https://storage.cloud.google.com/utilities-agents-demos/{domain_name}/{agent_name}.mp4" type="video/mp4">
        Your browser does not support the video tag.
      </video>
    </div>
    <div style="display:flex; justify-content:space-between; align-items:center; margin-top:-10px; margin-bottom:20px; font-size:0.82rem; color:var(--text-secondary);">
      <span>📹 Hosted on Google Cloud Storage</span>
      <a href="https://storage.cloud.google.com/utilities-agents-demos/{domain_name}/{agent_name}.mp4" target="_blank" rel="noopener noreferrer" style="color:var(--accent-blue); text-decoration:none; font-weight:500;">Open in GCS (Authenticated) ↗</a>
    </div>

    <div class="meta-grid">
      <div class="meta-item">
        <span class="meta-label">Domain</span>
        <span class="meta-value">{domain_title}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Business Role</span>
        <span class="meta-value">{persona}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">Reasoning Model</span>
        <span class="meta-value">{model}</span>
      </div>
      <div class="meta-item">
        <span class="meta-label">BigQuery Datasets</span>
        <span class="meta-value" style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; word-break: break-all; overflow-wrap: anywhere; white-space: normal;">{tables}</span>
      <div class="meta-item full-width">
        <span class="meta-label">Primary Business Problem & Solution</span>
        <span class="meta-value" style="font-weight: 400; font-size: 0.88rem; line-height: 1.5; color: var(--text-secondary); margin-top: 4px;">
          <strong style="color: var(--text-primary);">Problem:</strong> {problem}<br>
          <strong style="color: var(--text-primary); display: inline-block; margin-top: 4px;">Solution:</strong> {solution}
        </span>
      </div>
      <div class="meta-item full-width">
        <span class="meta-label">Key Business KPIs</span>
        <span class="meta-value" style="font-weight: 500; font-size: 0.88rem; color: var(--accent-blue); margin-top: 2px;">{kpis}</span>
      </div>
      {app_link_section}
    </div>

    <section class="turns-section">
      <h2>🎬 Multi-Turn Conversation Flow Showcase</h2>
      <ul class="turn-list">
        <li><strong>Turn 1 (Data Insight):</strong> "{prompt_1}"</li>
        <li><strong>Turn 2 (Root Cause & Diagnostics):</strong> "{prompt_2}"</li>
        <li><strong>Turn 3 (Recommendations & Benchmarks):</strong> "{prompt_3}"</li>
        <li><strong>Turn 4 (Operational Action & Staging):</strong> "{prompt_4}"</li>
    </section>

    <footer>
      Energy & Utilities Multi-Agent Operations Platform • Google Gemini Enterprise & Vertex AI
    </footer>
  </div>

  <script>
    function toggleTheme() {{
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const next = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', next);
      localStorage.setItem('utilities_agents_theme', next);
    }}
  </script>
</body>
</html>
"""

def generate_html_showcase(agent_name: str, domain: str | None = None, output_dir: Path | None = None) -> Path:
    if output_dir is None:
        output_dir = REPO_ROOT / "demos"

    if domain is None:
        domain = resolve_agent_domain(agent_name)

    cat_entry = get_catalog_entry(agent_name)
    readme_path = REPO_ROOT / "agents" / domain / agent_name / "README.md"
    prompts = parse_agent_prompts(readme_path, agent_name)

    domain_icon = DOMAIN_ICONS.get(domain, "⚡")
    domain_title = DOMAIN_TITLES.get(domain, domain.replace("_", " ").title())
    
    display_name = cat_entry.get("name", agent_name.replace("_", " ").title())
    clean_name = display_name.split(":")[-1].strip() if ":" in display_name else display_name
    agent_icon = cat_entry.get("icon", "🤖")
    description = cat_entry.get("description", f"Specialized AI agent for {clean_name}.")
    model = cat_entry.get("model", "gemini-3.7-flash")
    persona = cat_entry.get("persona", "Utility Operations Analyst")
    problem = cat_entry.get("problem", "Manual tracking is slow and error-prone.")
    solution = cat_entry.get("solution", "Autonomous AI monitoring and workflows.")
    kpis = ", ".join(cat_entry.get("kpis", ["Process Efficiency", "Reliability Index"]))
    tables = ", ".join(cat_entry.get("tables", [f"utilities_{domain}.logs"]))
    ge_url = cat_entry.get("ge_url", "")

    app_link_section = ""
    if ge_url:
        app_link_section = f"""
      <div class="meta-item full-width">
        <span class="meta-label">Gemini Enterprise App</span>
        <div>
          <a href="{ge_url}" target="_blank" rel="noopener noreferrer" class="app-link-btn">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
            Open in Gemini Enterprise
          </a>
        </div>
      </div>
        """

    p1 = html.escape(prompts[0]) if len(prompts) > 0 else "Run operational diagnostics."
    p2 = html.escape(prompts[1]) if len(prompts) > 1 else "Analyze active anomalies and root causes."
    p3 = html.escape(prompts[2]) if len(prompts) > 2 else "Provide recommended actions and mitigation plan."
    p4 = html.escape(prompts[3]) if len(prompts) > 3 else "Stage authorized operational workflow and action plan."
    content = HTML_TEMPLATE.format(
        page_title=f"{clean_name} — Gemini Enterprise Demo Walkthrough",
        domain_icon=domain_icon,
        domain=domain,
        agent_icon=agent_icon,
        display_name=display_name,
        clean_name=clean_name,
        description=html.escape(description),
        model=model,
        agent_name=agent_name,
        persona=html.escape(persona),
        problem=html.escape(problem),
        solution=html.escape(solution),
        kpis=html.escape(kpis),
        tables=html.escape(tables),
        app_link_section=app_link_section,
        prompt_1=p1,
        prompt_2=p2,
        prompt_3=p3,
        prompt_4=p4,
    )
    domain_out = output_dir / domain
    domain_out.mkdir(parents=True, exist_ok=True)
    html_file = domain_out / f"{agent_name}.html"
    html_file.write_text(content, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Generate HTML showcase player for agent demo videos.")
    parser.add_argument("--name", type=str, help="Agent name")
    parser.add_argument("--domain", type=str, help="Domain name")
    parser.add_argument("--all", action="store_true", help="Generate for all agents")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "demos", help="Output directory")
    args = parser.parse_args()

    if args.name:
        domain = args.domain or resolve_agent_domain(args.name)
        out = generate_html_showcase(args.name, domain, args.output_dir)
        print(f"✅ Generated showcase: {out}")
    elif args.all:
        cat_file = REPO_ROOT / "web" / "catalog.json"
        if not cat_file.exists():
            print("❌ web/catalog.json not found.")
            return
        with open(cat_file, "r") as f:
            agents = json.load(f)
        count = 0
        for a in agents:
            generate_html_showcase(a["id"], a["domain"], args.output_dir)
            count += 1
        print(f"🎉 Generated {count} HTML demo showcase players under {args.output_dir}")

if __name__ == "__main__":
    main()
