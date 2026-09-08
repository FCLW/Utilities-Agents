#!/usr/bin/env python3
"""
record_agent_demo.py — Playwright + FFmpeg Multi-Turn Agent Demo Video Recorder

Automates end-to-end recording of Gemini Enterprise Agent demo walkthroughs:
1. Browser Automation: Playwright driving Chromium at 1920x1080 (1080p).
2. Authentic Prompts: Extracts all 4 business prompts from sample_prompts.yaml.
3. Multi-Turn Execution:
   - Turn 1: Quantitative Data Insight with BigQuery queries, table breakdown, metrics table, anomaly detection.
   - Turn 2: Risk analysis & Root cause diagnostics with status badges and failure curves.
   - Turn 3: Strategic recommendations with visual KPI metrics and CapEx deferral plans.
   - Turn 4: Authentic Operational Directive & Human-in-the-Loop (HITL) Execution.
4. Readable Smooth Scrolling:
   - Positions user prompt and response header in view with pause for reading.
   - Smoothly scrolls down through tables, metrics, and recommendations at a readable pace (~150-180 px/s).
   - Generous pause at response bottom, followed by an overarching review scroll at the end.
5. Strict 1080p Geometry:
   - Zero horizontal overflow. All elements, tables, and bubbles stay within 1920x1080 bounds.
6. FFmpeg Transcoding:
   - Transcodes to 1080p MP4 via libx264, CRF 22, faststart.
7. Automated HTML Showcase Player:
   - Invokes generate_demo_html.py to produce the standalone dark-mode HTML player alongside the MP4 video.
"""

import argparse
import asyncio
from concurrent.futures import ProcessPoolExecutor
import html
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import time

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from scripts.prompt_parser import get_catalog_entry, parse_agent_prompts, resolve_agent_domain
from scripts.generate_demo_html import DOMAIN_ICONS, DOMAIN_TITLES, generate_html_showcase

def load_agent_golden_dataset(agent_name: str, domain: str) -> list[tuple[str, str]]:
    """Loads input-output pairs from tests/eval/datasets/golden-dataset.json."""
    gd_path = REPO_ROOT / "agents" / domain / agent_name / "tests" / "eval" / "datasets" / "golden-dataset.json"
    if gd_path.exists():
        try:
            with open(gd_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [(item.get("input", "").strip(), item.get("expected_output", "").strip()) for item in data]
        except Exception:
            pass
    return []

def md_to_html(md: str) -> str:
    """Converts markdown output from golden dataset into clean, styled HTML."""
    lines = md.strip().split("\n")
    out = []
    in_code = False
    code_block = []
    in_table = False
    table_rows = []

    def format_inline(text: str) -> str:
        text = html.escape(text)
        text = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", text)
        text = re.sub(r"`(.*?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[TIER 2 ACTION REQUIRED\]", r"<span class=\"action-pill\">⚡ TIER 2 ACTION REQUIRED</span>", text)
        text = re.sub(r"\[TIER 1 NOTIFICATION\]", r"<span class=\"action-pill\">ℹ️ TIER 1 NOTIFICATION</span>", text)
        text = re.sub(r"🚨\s*Critical", r"<span class=\"badge-crit\">🚨 Critical</span>", text)
        text = re.sub(r"⚠️\s*Warning", r"<span class=\"badge-warn\">⚠️ Warning</span>", text)
        text = re.sub(r"✅\s*Normal", r"<span class=\"badge-ok\">✅ Normal</span>", text)
        text = re.sub(r"✅\s*Compliant", r"<span class=\"badge-ok\">✅ Compliant</span>", text)
        return text

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                in_code = False
                out.append(f"<pre class=\"code-box\"><code>{html.escape(chr(10).join(code_block))}</code></pre>")
                code_block = []
            else:
                in_code = True
                code_block = []
            continue
        if in_code:
            code_block.append(line)
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            if not in_table:
                in_table = True
                table_rows = []
            table_rows.append(stripped)
            continue
        else:
            if in_table:
                in_table = False
                if len(table_rows) >= 2:
                    out.append("<div class=\"table-wrap\"><table class=\"data-table\">")
                    header_cols = [c.strip() for c in table_rows[0].strip("|").split("|")]
                    out.append("<thead><tr>" + "".join(f"<th>{format_inline(c)}</th>" for c in header_cols) + "</tr></thead>")
                    out.append("<tbody>")
                    for row in table_rows[2:]:
                        cols = [c.strip() for c in row.strip("|").split("|")]
                        out.append("<tr>" + "".join(f"<td>{format_inline(c)}</td>" for c in cols) + "</tr>")
                    out.append("</tbody></table></div>")
                table_rows = []

        if not stripped:
            continue

        if stripped.startswith("#### "):
            out.append(f"<h4>{format_inline(stripped[5:])}</h4>")
        elif stripped.startswith("### "):
            out.append(f"<h3>{format_inline(stripped[4:])}</h3>")
        elif stripped.startswith("## "):
            out.append(f"<h2>{format_inline(stripped[3:])}</h2>")
        elif stripped.startswith("# "):
            out.append(f"<h1>{format_inline(stripped[2:])}</h1>")
        elif stripped.startswith("- ") or stripped.startswith("* "):
            out.append(f"<li class=\"agent-bullet\">{format_inline(stripped[2:])}</li>")
        elif re.match(r"^\d+\.\s+", stripped):
            content = re.sub(r"^\d+\.\s+", "", stripped)
            out.append(f"<li class=\"agent-bullet-num\">{format_inline(content)}</li>")
        else:
            out.append(f"<p>{format_inline(stripped)}</p>")

    if in_table and len(table_rows) >= 2:
        out.append("<div class=\"table-wrap\"><table class=\"data-table\">")
        header_cols = [c.strip() for c in table_rows[0].strip("|").split("|")]
        out.append("<thead><tr>" + "".join(f"<th>{format_inline(c)}</th>" for c in header_cols) + "</tr></thead>")
        out.append("<tbody>")
        for row in table_rows[2:]:
            cols = [c.strip() for c in row.strip("|").split("|")]
            out.append("<tr>" + "".join(f"<td>{format_inline(c)}</td>" for c in cols) + "</tr>")
        out.append("</tbody></table></div>")

    return "\n".join(out)

def generate_interactive_demo_page(agent_name: str, domain: str, prompts: list[str], speed: str = "fast") -> str:
    cat_entry = get_catalog_entry(agent_name)
    display_name = cat_entry.get("name", agent_name.replace("_", " ").title())
    clean_name = display_name.split(":")[-1].strip() if ":" in display_name else display_name
    agent_icon = cat_entry.get("icon", "🤖")
    domain_icon = DOMAIN_ICONS.get(domain, "⚡")
    domain_title = DOMAIN_TITLES.get(domain, domain.replace("_", " ").title())
    model = cat_entry.get("model", "gemini-3.7-flash")
    persona = cat_entry.get("persona", "Utility Operations Analyst")
    problem = cat_entry.get("problem", "Manual tracking is slow and error-prone.")
    solution = cat_entry.get("solution", "Autonomous AI monitoring and workflows.")
    kpis = cat_entry.get("kpis", ["Process Efficiency", "Reliability Index"])
    tables = cat_entry.get("tables", [f"utilities_{domain}.{agent_name}_logs"])
    primary_table = tables[0] if tables else f"utilities_{domain}.logs"

    qa_pairs = load_agent_golden_dataset(agent_name, domain)
    if not qa_pairs:
        qa_pairs = [(p, f"Analysis and operational findings for {clean_name} based on telemetry and domain rules.") for p in prompts]

    p1 = prompts[0] if len(prompts) > 0 else (qa_pairs[0][0] if len(qa_pairs) > 0 else f"Analyze recent telemetry and operational performance metrics for {clean_name}.")
    p2 = prompts[1] if len(prompts) > 1 else (qa_pairs[1][0] if len(qa_pairs) > 1 else f"Identify active anomalies, degradation signatures, and root-cause indicators.")
    p3 = prompts[2] if len(prompts) > 2 else (qa_pairs[2][0] if len(qa_pairs) > 2 else f"Generate prioritized operational recommendations and preventive maintenance schedule.")
    p4 = prompts[3] if len(prompts) > 3 else (qa_pairs[3][0] if len(qa_pairs) > 3 else f"Stage an authorized operational workflow and action plan for {clean_name}.")

    a1_html = md_to_html(qa_pairs[0][1]) if len(qa_pairs) > 0 else f"<p>Operational performance analyzed for {clean_name}.</p>"
    a2_html = md_to_html(qa_pairs[1][1]) if len(qa_pairs) > 1 else f"<p>Root cause diagnostics completed for {clean_name}.</p>"
    a3_html = md_to_html(qa_pairs[2][1]) if len(qa_pairs) > 2 else f"<p>Remediation actions generated for {clean_name}.</p>"
    a4_html = md_to_html(qa_pairs[3][1]) if len(qa_pairs) > 3 else f"<p>Authorized operational plan staged for {clean_name}.</p>"

    # Animation timing multipliers
    delay_mult = 0.65 if speed == "fast" else 1.0

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{html.escape(clean_name)} — Gemini Enterprise Demo</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;600;700&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    * {{
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }}
    body {{
      font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #131314;
      color: #e3e3e3;
      overflow: hidden;
      width: 1920px;
      max-width: 1920px;
      height: 1080px;
      max-height: 1080px;
      display: flex;
    }}

    /* Left App Sidebar (270px) */
    .app-sidebar {{
      width: 270px;
      max-width: 270px;
      min-width: 270px;
      height: 1080px;
      background-color: #1e1f20;
      border-right: 1px solid #2e2f31;
      display: flex;
      flex-direction: column;
      padding: 18px 16px;
      flex-shrink: 0;
      user-select: none;
    }}
    .sidebar-brand {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 6px 10px;
      margin-bottom: 20px;
    }}
    .gemini-sparkle {{
      width: 32px;
      height: 32px;
      background: linear-gradient(135deg, #4285f4, #9b72cb, #d96570);
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: 700;
      font-size: 18px;
      box-shadow: 0 2px 8px rgba(66, 133, 244, 0.4);
    }}
    .brand-title {{
      font-family: 'Google Sans', sans-serif;
      font-size: 1.18rem;
      font-weight: 600;
      color: #f1f3f4;
      letter-spacing: -0.01em;
    }}
    .new-chat-btn {{
      display: flex;
      align-items: center;
      gap: 12px;
      background: #282a2c;
      border: 1px solid #3c4043;
      border-radius: 24px;
      padding: 12px 18px;
      color: #e8eaed;
      font-size: 0.9rem;
      font-weight: 500;
      cursor: pointer;
      margin-bottom: 24px;
      transition: background 0.2s;
    }}
    .new-chat-btn:hover {{
      background: #333538;
    }}
    .sidebar-nav-title {{
      font-size: 0.74rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: #9aa0a6;
      padding: 6px 12px;
      margin-bottom: 6px;
      font-weight: 600;
    }}
    .nav-item {{
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 10px 14px;
      border-radius: 12px;
      color: #c4c7c5;
      font-size: 0.88rem;
      cursor: pointer;
      margin-bottom: 4px;
    }}
    .nav-item.active {{
      background: #333538;
      color: #ffffff;
      font-weight: 600;
    }}
    .agent-pill-pinned {{
      background: rgba(66, 133, 244, 0.12);
      border: 1px solid rgba(66, 133, 244, 0.35);
      color: #8ab4f8;
      margin-top: auto;
      padding: 14px;
      border-radius: 14px;
      display: flex;
      flex-direction: column;
      gap: 6px;
    }}
    .agent-pill-pinned .pill-name {{
      font-weight: 600;
      font-size: 0.88rem;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #e8eaed;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }}
    .agent-pill-pinned .pill-domain {{
      font-size: 0.76rem;
      color: #9aa0a6;
      display: flex;
      align-items: center;
      gap: 6px;
    }}

    /* Main Workspace Container (Strictly 1650px) */
    .main-workspace {{
      width: 1650px;
      max-width: 1650px;
      min-width: 1650px;
      height: 1080px;
      display: flex;
      flex-direction: column;
      position: relative;
      background-color: #131314;
      overflow: hidden;
    }}

    /* Top Agent Header Bar */
    .agent-topbar {{
      height: 64px;
      width: 1650px;
      max-width: 1650px;
      border-bottom: 1px solid #2e2f31;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 32px;
      background: #18191a;
      flex-shrink: 0;
      z-index: 10;
    }}
    .topbar-left {{
      display: flex;
      align-items: center;
      gap: 14px;
    }}
    .topbar-icon {{
      font-size: 24px;
    }}
    .topbar-agent-title {{
      font-family: 'Google Sans', sans-serif;
      font-size: 1.12rem;
      font-weight: 600;
      color: #f1f3f4;
    }}
    .topbar-tags {{
      display: flex;
      align-items: center;
      gap: 10px;
    }}
    .tag-badge {{
      font-size: 0.78rem;
      padding: 5px 12px;
      border-radius: 12px;
      font-weight: 500;
      background: #282a2c;
      color: #bdc1c6;
      border: 1px solid #3c4043;
      display: flex;
      align-items: center;
      gap: 6px;
    }}
    .tag-model {{
      background: rgba(30, 142, 62, 0.2);
      color: #81c995;
      border-color: rgba(30, 142, 62, 0.4);
      font-weight: 600;
    }}
    .tag-bq {{
      background: rgba(66, 133, 244, 0.15);
      color: #8ab4f8;
      border-color: rgba(66, 133, 244, 0.3);
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.74rem;
    }}
    .status-dot {{
      width: 8px;
      height: 8px;
      background: #34a853;
      border-radius: 50%;
      box-shadow: 0 0 8px #34a853;
    }}

    /* Scrollable Conversation Stream */
    .chat-history {{
      width: 1650px;
      max-width: 1650px;
      flex: 1;
      overflow-y: scroll;
      overflow-x: hidden;
      padding: 32px 80px 140px;
      display: flex;
      flex-direction: column;
      gap: 32px;
      scroll-behavior: auto;
    }}
    .chat-history::-webkit-scrollbar {{
      width: 8px;
    }}
    .chat-history::-webkit-scrollbar-thumb {{
      background: #3c4043;
      border-radius: 4px;
    }}

    /* Message Bubbles */
    .msg-user {{
      align-self: flex-end;
      max-width: 75%;
      background: #2b2c2f;
      border: 1px solid #3c4043;
      color: #f1f3f4;
      padding: 14px 22px;
      border-radius: 20px 20px 4px 20px;
      font-size: 1rem;
      line-height: 1.5;
      box-shadow: 0 3px 10px rgba(0,0,0,0.3);
      word-break: break-word;
    }}
    .msg-agent {{
      align-self: flex-start;
      width: 100%;
      max-width: 100%;
      display: flex;
      gap: 16px;
      font-size: 0.96rem;
      line-height: 1.65;
      color: #e3e3e3;
    }}
    .agent-avatar {{
      width: 36px;
      height: 36px;
      background: linear-gradient(135deg, #1a73e8, #8ab4f8);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      flex-shrink: 0;
      margin-top: 4px;
      box-shadow: 0 2px 8px rgba(26, 115, 232, 0.4);
    }}
    .msg-body {{
      flex: 1;
      min-width: 0;
      max-width: calc(100% - 52px);
      display: flex;
      flex-direction: column;
      gap: 10px;
      overflow-wrap: break-word;
      word-break: break-word;
    }}
    .msg-body h1, .msg-body h2, .msg-body h3, .msg-body h4 {{
      font-family: 'Google Sans', sans-serif;
      color: #f1f3f4;
      margin-top: 10px;
      margin-bottom: 4px;
      font-weight: 600;
    }}
    .msg-body h1 {{ font-size: 1.25rem; }}
    .msg-body h2 {{ font-size: 1.15rem; }}
    .msg-body h3 {{ font-size: 1.05rem; color: #8ab4f8; }}
    .msg-body h4 {{ font-size: 0.98rem; color: #bdc1c6; }}
    .msg-body p {{
      margin: 4px 0;
      color: #e3e3e3;
    }}
    .msg-body strong {{
      color: #ffffff;
      font-weight: 600;
    }}
    .agent-bullet, .agent-bullet-num {{
      margin-left: 20px;
      color: #d1d5db;
      line-height: 1.55;
      margin-top: 2px;
      margin-bottom: 2px;
    }}

    /* Thinking Step Box */
    .thinking-box {{
      display: flex;
      align-items: center;
      gap: 12px;
      color: #9aa0a6;
      font-size: 0.88rem;
      padding: 12px 18px;
      background: #1e1f20;
      border-radius: 12px;
      border-left: 4px solid #8ab4f8;
      margin-bottom: 8px;
      width: fit-content;
      box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }}
    .spinner {{
      width: 16px;
      height: 16px;
      border: 2px solid #8ab4f8;
      border-top-color: transparent;
      border-radius: 50%;
      animation: spin 0.8s linear infinite;
    }}
    @keyframes spin {{
      to {{ transform: rotate(360deg); }}
    }}

    /* Data Tables */
    .table-wrap {{
      width: 100%;
      max-width: 100%;
      margin: 14px 0;
      border-radius: 10px;
      border: 1px solid #3c4043;
      overflow-x: auto;
      background: #18191a;
      box-shadow: 0 2px 8px rgba(0,0,0,0.3);
    }}
    .data-table {{
      width: 100%;
      min-width: 650px;
      border-collapse: collapse;
      font-size: 0.88rem;
    }}
    .data-table th, .data-table td {{
      padding: 10px 14px;
      border-bottom: 1px solid #2e2f31;
      text-align: left;
    }}
    .data-table th {{
      background: #242628;
      color: #f1f3f4;
      font-weight: 600;
      font-family: 'Google Sans', sans-serif;
      font-size: 0.86rem;
      border-bottom: 2px solid #3c4043;
    }}
    .data-table tr:nth-child(even) {{
      background: #1b1c1d;
    }}
    .data-table tr:hover {{
      background: #232527;
    }}

    /* Badges & Pills */
    .badge-warn {{
      background: rgba(249, 171, 0, 0.2);
      color: #fdd663;
      padding: 3px 9px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.78rem;
      border: 1px solid rgba(249, 171, 0, 0.35);
      display: inline-block;
    }}
    .badge-crit {{
      background: rgba(234, 67, 53, 0.2);
      color: #f28b82;
      padding: 3px 9px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.78rem;
      border: 1px solid rgba(234, 67, 53, 0.35);
      display: inline-block;
    }}
    .badge-ok {{
      background: rgba(52, 168, 83, 0.2);
      color: #81c995;
      padding: 3px 9px;
      border-radius: 6px;
      font-weight: 600;
      font-size: 0.78rem;
      border: 1px solid rgba(52, 168, 83, 0.35);
      display: inline-block;
    }}
    .action-pill {{
      background: rgba(66, 133, 244, 0.2);
      color: #8ab4f8;
      padding: 4px 10px;
      border-radius: 6px;
      font-weight: 700;
      font-size: 0.82rem;
      border: 1px solid rgba(66, 133, 244, 0.4);
      display: inline-block;
      letter-spacing: 0.02em;
    }}

    /* Code & JSON Boxes */
    .code-box {{
      width: 100%;
      max-width: 100%;
      background: #0d1117;
      border: 1px solid #30363d;
      border-radius: 8px;
      padding: 14px 16px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 0.82rem;
      color: #79c0ff;
      margin: 12px 0;
      overflow-x: auto;
      line-height: 1.5;
      white-space: pre-wrap;
      word-break: break-all;
    }}

    /* Bottom Fixed Input Box */
    .input-container {{
      position: absolute;
      bottom: 24px;
      left: 80px;
      right: 80px;
      width: calc(100% - 160px);
      max-width: calc(100% - 160px);
      background: #1e1f20;
      border: 1px solid #3c4043;
      border-radius: 30px;
      display: flex;
      align-items: center;
      padding: 10px 20px;
      box-shadow: 0 6px 24px rgba(0,0,0,0.5);
      z-index: 10;
    }}
    .input-field {{
      flex: 1;
      background: transparent;
      border: none;
      outline: none;
      color: #f1f3f4;
      font-size: 1rem;
      padding: 6px 10px;
      font-family: inherit;
    }}
    .input-field::placeholder {{
      color: #80868b;
    }}
    .input-actions {{
      display: flex;
      align-items: center;
      gap: 12px;
    }}
    .action-btn {{
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: #8ab4f8;
      color: #131314;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      font-weight: bold;
      transition: all 0.2s;
    }}
    .action-btn.stop {{
      background: #e37400;
      color: white;
    }}

    /* Virtual Smooth Cursor */
    #virtual-cursor {{
      position: fixed;
      top: 0;
      left: 0;
      width: 24px;
      height: 24px;
      z-index: 9999;
      pointer-events: none;
      transition: transform 0.35s cubic-bezier(0.2, 0.8, 0.2, 1);
      filter: drop-shadow(0 2px 5px rgba(0,0,0,0.6));
    }}
  </style>
</head>
<body>

  <!-- Left Sidebar -->
  <aside class="app-sidebar">
    <div class="sidebar-brand">
      <div class="gemini-sparkle">✦</div>
      <div class="brand-title">Gemini Enterprise</div>
    </div>

    <button class="new-chat-btn">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
      <span>New Consultation</span>
    </button>

    <div class="sidebar-nav-title">Active AI Fleet</div>
    <div class="nav-item active">
      <span>{agent_icon}</span>
      <span>{html.escape(clean_name)}</span>
    </div>
    <div class="nav-item">
      <span>🌐</span>
      <span>Utilities Master Orchestrator</span>
    </div>
    <div class="nav-item">
      <span>⚡</span>
      <span>Smart Grid Control Room</span>
    </div>

    <div class="agent-pill-pinned">
      <div class="pill-name">{agent_icon} {html.escape(clean_name)}</div>
      <div class="pill-domain">{domain_icon} {html.escape(domain_title)}</div>
    </div>
  </aside>

  <!-- Main Workspace -->
  <main class="main-workspace">
    <header class="agent-topbar">
      <div class="topbar-left">
        <span class="topbar-icon">{agent_icon}</span>
        <span class="topbar-agent-title">{html.escape(clean_name)}</span>
        <div class="status-dot" title="Agent Online & Reasoning Ready"></div>
      </div>
      <div class="topbar-tags">
        <div class="tag-badge tag-model">✦ {model}</div>
        <div class="tag-badge tag-bq">📊 {primary_table}</div>
        <div class="tag-badge">{domain_icon} {html.escape(domain_title)}</div>
      </div>
    </header>

    <section class="chat-history" id="chatHistory">
      <!-- Conversation turns injected here -->
    </section>

    <!-- Bottom Fixed Input -->
    <div class="input-container">
      <input type="text" class="input-field" id="userInput" placeholder="Ask {html.escape(clean_name)} about telemetry, anomalies, optimization, or actions..." readonly />
      <div class="input-actions">
        <button class="action-btn" id="actionBtn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg>
        </button>
      </div>
    </div>
  </main>

  <!-- Virtual Smooth Cursor -->
  <svg id="virtual-cursor" viewBox="0 0 24 24" fill="none">
    <path d="M3 3l7 18 3-7 7-3L3 3z" fill="#ffffff" stroke="#000000" stroke-width="1.5" stroke-linejoin="round"/>
  </svg>

  <script>
    const P1 = {json.dumps(p1)};
    const A1_HTML = {json.dumps(a1_html)};

    const P2 = {json.dumps(p2)};
    const A2_HTML = {json.dumps(a2_html)};

    const P3 = {json.dumps(p3)};
    const A3_HTML = {json.dumps(a3_html)};

    const P4 = {json.dumps(p4)};
    const A4_HTML = {json.dumps(a4_html)};

    const SPEED_MULT = {delay_mult};
    const chatHistory = document.getElementById('chatHistory');
    const userInput = document.getElementById('userInput');
    const actionBtn = document.getElementById('actionBtn');
    const cursor = document.getElementById('virtual-cursor');

    function sleep(ms) {{
      return new Promise(resolve => setTimeout(resolve, ms * SPEED_MULT));
    }}

    function moveCursor(x, y) {{
      cursor.style.transform = `translate(${{x}}px, ${{y}}px)`;
    }}

    async function typePrompt(text) {{
      userInput.value = "";
      for (let i = 0; i <= text.length; i++) {{
        userInput.value = text.substring(0, i);
        await sleep(14);
      }}
      actionBtn.classList.add('stop');
      await sleep(220);
      userInput.value = "";
      actionBtn.classList.remove('stop');
    }}

    function appendUserMessage(text) {{
      const msg = document.createElement('div');
      msg.className = 'msg-user';
      msg.innerText = text;
      chatHistory.appendChild(msg);
      return msg;
    }}

    async function appendAgentThinking(stepText) {{
      const box = document.createElement('div');
      box.className = 'thinking-box';
      box.innerHTML = `<div class="spinner"></div><span>${{stepText}}</span>`;
      chatHistory.appendChild(box);
      return box;
    }}

    function appendAgentMessage(contentHtml) {{
      const msg = document.createElement('div');
      msg.className = 'msg-agent';
      msg.innerHTML = `
        <div class="agent-avatar">{agent_icon}</div>
        <div class="msg-body">${{contentHtml}}</div>
      `;
      chatHistory.appendChild(msg);
      return msg;
    }}

    /*
     * Smoothly scrolls the chat container to a specific target scroll position.
     * speedPx: pixels scrolled per frame (16ms).
     * 2.5px per 16ms = ~156 px/sec, perfectly readable for human viewers!
     */
    async function smoothScrollChat(targetScrollTop, speedPx = 2.5) {{
      const start = chatHistory.scrollTop;
      const dist = targetScrollTop - start;
      if (Math.abs(dist) < 2) {{
        chatHistory.scrollTop = targetScrollTop;
        return;
      }}
      const step = dist > 0 ? speedPx : -speedPx;
      let current = start;
      while ((dist > 0 && current < targetScrollTop) || (dist < 0 && current > targetScrollTop)) {{
        current += step;
        if ((dist > 0 && current > targetScrollTop) || (dist < 0 && current < targetScrollTop)) {{
          current = targetScrollTop;
        }}
        chatHistory.scrollTop = current;
        await sleep(16);
      }}
      chatHistory.scrollTop = targetScrollTop;
    }}

    /*
     * Displays an agent response with slow, comfortable, readable pacing:
     * 1. Scrolls to place user prompt + response summary in clear view.
     * 2. Pauses 1800ms so the viewer reads the prompt and summary.
     * 3. Smoothly scrolls down through the response body (tables, metrics, root causes) at ~150px/sec.
     * 4. Pauses 1800ms at the bottom so recommendations and action items are digested.
     */
    async function presentAgentResponse(userMsgEl, agentMsgEl) {{
      // 1. Position user prompt at top of visible chat viewport
      const userTop = userMsgEl.offsetTop - chatHistory.offsetTop - 16;
      chatHistory.scrollTop = Math.max(0, userTop);
      await sleep(1800);

      // 2. Smoothly scroll down to bottom of agent response
      const targetBottom = chatHistory.scrollHeight - chatHistory.clientHeight;
      if (targetBottom > chatHistory.scrollTop + 20) {{
        await smoothScrollChat(targetBottom, 2.5);
        await sleep(1800);
      }} else {{
        await sleep(1600);
      }}
    }}

    async function runDemoSequence() {{
      moveCursor(960, 540);
      await sleep(600);

      // ==========================================
      // TURN 1: Quantitative Data Insight
      // ==========================================
      moveCursor(600, 1030);
      await typePrompt(P1);
      const u1 = appendUserMessage(P1);
      const think1 = await appendAgentThinking("Querying BigQuery table {primary_table} & analyzing telemetry streams...");
      await sleep(700);
      think1.remove();
      const a1 = appendAgentMessage(A1_HTML);
      await presentAgentResponse(u1, a1);

      // ==========================================
      // TURN 2: Root Cause & Diagnostics
      // ==========================================
      moveCursor(600, 1030);
      await typePrompt(P2);
      const u2 = appendUserMessage(P2);
      const think2 = await appendAgentThinking("Cross-referencing IEEE / FERC operational failure curves and degradation baselines...");
      await sleep(700);
      think2.remove();
      const a2 = appendAgentMessage(A2_HTML);
      await presentAgentResponse(u2, a2);

      // ==========================================
      // TURN 3: Recommendations & Optimization
      // ==========================================
      moveCursor(600, 1030);
      await typePrompt(P3);
      const u3 = appendUserMessage(P3);
      const think3 = await appendAgentThinking("Synthesizing multi-agent optimization plan and CapEx deferral scenarios...");
      await sleep(700);
      think3.remove();
      const a3 = appendAgentMessage(A3_HTML);
      await presentAgentResponse(u3, a3);

      // ==========================================
      // TURN 4: Authentic Operational Directive & HITL Execution
      // ==========================================
      moveCursor(600, 1030);
      await typePrompt(P4);
      const u4 = appendUserMessage(P4);
      const think4 = await appendAgentThinking("Processing operational directive & staging authorization...");
      await sleep(800);
      think4.remove();
      const a4 = appendAgentMessage(A4_HTML);
      await presentAgentResponse(u4, a4);

      // ==========================================
      // End Review: Smooth Walkthrough to Top
      // ==========================================
      moveCursor(960, 500);
      await sleep(500);
      // Smoothly scroll back to top of conversation
      await smoothScrollChat(0, 8);
      await sleep(2200);

      // Signal completion to Playwright
      window.demoFinished = true;
    }}

    window.runDemoSequence = runDemoSequence;
  </script>
</body>
</html>
"""

async def record_single_agent_demo(
    agent_name: str,
    domain: str,
    prompts: list[str],
    output_dir: Path,
    speed: str = "fast",
    video_format: str = "mp4",
    resolution: str = "1080p",
    dry_run: bool = False,
    skip_existing: bool = False
) -> Path:
    domain_output_dir = output_dir / domain
    domain_output_dir.mkdir(parents=True, exist_ok=True)
    target_video_file = domain_output_dir / f"{agent_name}.{video_format}"

    if dry_run:
        print(f"🔍 [Dry Run] Agent: {agent_name} | Domain: {domain} | Prompts: {len(prompts)}", flush=True)
        return target_video_file

    if skip_existing and target_video_file.exists() and target_video_file.stat().st_size > 50000:
        print(f"⏩ [Skip] {agent_name} demo video already exists ({target_video_file.stat().st_size / (1024*1024):.2f} MB)", flush=True)
        try:
            generate_html_showcase(agent_name=agent_name, domain=domain, output_dir=output_dir)
        except Exception:
            pass
        return target_video_file

    # 1. Create temporary HTML file for Playwright
    html_content = generate_interactive_demo_page(agent_name, domain, prompts, speed=speed)
    temp_dir = Path(tempfile.mkdtemp(prefix=f"ge_demo_{agent_name}_"))
    html_path = temp_dir / "index.html"
    html_path.write_text(html_content, encoding="utf-8")

    # 2. Setup video recording dir
    video_capture_dir = temp_dir / "video"
    video_capture_dir.mkdir(parents=True, exist_ok=True)

    from playwright.async_api import async_playwright

    w, h = (1920, 1080) if resolution == "1080p" else (1280, 720)

    print(f"🎬 Recording {agent_name} ({domain}) at {w}x{h}...", flush=True)
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                f"--window-size={w},{h}"
            ]
        )
        context = await browser.new_context(
            viewport={"width": w, "height": h},
            record_video_dir=str(video_capture_dir),
            record_video_size={"width": w, "height": h}
        )
        page = await context.new_page()
        page.on("console", lambda msg: print(f"  [{agent_name}] {msg.text}", flush=True))
        page.on("pageerror", lambda err: print(f"  [{agent_name} ERROR] {err}", flush=True))

        # Navigate to the generated mock Gemini Enterprise page
        await page.goto(f"file://{html_path}", wait_until="domcontentloaded")
        await asyncio.sleep(0.3)
        await page.evaluate("window.runDemoSequence()")

        # Wait until window.demoFinished is true (timeout 60s)
        try:
            await page.wait_for_function("() => window.demoFinished === true", timeout=60000)
            await asyncio.sleep(1.0)
        except Exception as e:
            print(f"⚠️ Warning during playback for {agent_name}: {e}", flush=True)

        await page.close()
        await context.close()
        await browser.close()

    # 3. Locate raw recorded video
    recorded_files = list(video_capture_dir.glob("*.webm"))
    if not recorded_files:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise RuntimeError(f"No video file recorded for {agent_name}")

    raw_video = recorded_files[0]

    # 4. Transcode to MP4 with FFmpeg (or keep WebM)
    if video_format == "mp4":
        ffmpeg_cmd = [
            "ffmpeg", "-y",
            "-i", str(raw_video),
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "22",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            str(target_video_file)
        ]
        proc = subprocess.run(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if proc.returncode != 0:
            print(f"⚠️ FFmpeg error, copying raw webm: {proc.stderr.decode()[:200]}", flush=True)
            shutil.copy2(str(raw_video), str(target_video_file.with_suffix(".webm")))
    else:
        shutil.copy2(str(raw_video), str(target_video_file))

    # Clean up temp files
    shutil.rmtree(temp_dir, ignore_errors=True)

    size_mb = target_video_file.stat().st_size / (1024 * 1024) if target_video_file.exists() else 0
    print(f"✅ Saved video: {target_video_file} ({size_mb:.2f} MB)", flush=True)

    # 5. Generate matching HTML showcase player
    try:
        generate_html_showcase(agent_name=agent_name, domain=domain, output_dir=output_dir)
    except Exception as e:
        print(f"⚠️ Error generating HTML showcase: {e}", flush=True)

    return target_video_file

def _worker_record(agent_tuple):
    agent_name, domain, prompts, output_dir_str, speed, video_format, resolution, skip_existing = agent_tuple
    output_dir = Path(output_dir_str)
    try:
        vid_path = asyncio.run(
            record_single_agent_demo(
                agent_name=agent_name,
                domain=domain,
                prompts=prompts,
                output_dir=output_dir,
                speed=speed,
                video_format=video_format,
                resolution=resolution,
                skip_existing=skip_existing
            )
        )
        return (agent_name, domain, True, str(vid_path))
    except Exception as e:
        print(f"❌ Error recording {agent_name}: {e}", flush=True)
        return (agent_name, domain, False, str(e))

def main():
    parser = argparse.ArgumentParser(description="Utilities Enterprise Agents Demo Video Recorder")
    parser.add_argument("--name", type=str, help="Target agent name (e.g. capital_replacement_simulator)")
    parser.add_argument("--domain", type=str, help="Target sub-domain name (e.g. asset_management)")
    parser.add_argument("--all", action="store_true", help="Record all agents")
    parser.add_argument("--workers", type=int, default=4, help="Number of concurrent worker processes (default: 4)")
    parser.add_argument("--speed", choices=["normal", "fast"], default="fast", help="Pacing speed (default: fast)")
    parser.add_argument("--format", choices=["mp4", "webm"], default="mp4", help="Video output format (default: mp4)")
    parser.add_argument("--resolution", choices=["1080p", "720p"], default="1080p", help="Resolution (default: 1080p)")
    parser.add_argument("--output-dir", type=Path, default=REPO_ROOT / "demos", help="Output directory")
    parser.add_argument("--dry-run", action="store_true", help="Validate prompts without recording")
    parser.add_argument("--skip-existing", action="store_true", help="Skip agents whose video already exists")

    args = parser.parse_args()

    if not args.name and not args.all and not args.domain:
        parser.error("Must provide --name, --domain, or --all")

    agents_to_record = []

    cat_file = REPO_ROOT / "web" / "catalog.json"
    catalog_agents = []
    if cat_file.exists():
        with open(cat_file, "r") as f:
            catalog_agents = json.load(f)

    if args.name:
        domain = args.domain or resolve_agent_domain(args.name)
        readme = REPO_ROOT / "agents" / domain / args.name / "README.md"
        prompts = parse_agent_prompts(readme, args.name)
        agents_to_record.append((args.name, domain, prompts))
    elif args.domain and not args.all:
        for a in catalog_agents:
            if a.get("domain") == args.domain:
                readme = REPO_ROOT / "agents" / a["domain"] / a["id"] / "README.md"
                prompts = parse_agent_prompts(readme, a["id"])
                agents_to_record.append((a["id"], a["domain"], prompts))
    elif args.all:
        for a in catalog_agents:
            readme = REPO_ROOT / "agents" / a["domain"] / a["id"] / "README.md"
            prompts = parse_agent_prompts(readme, a["id"])
            agents_to_record.append((a["id"], a["domain"], prompts))

    print(f"📋 Found {len(agents_to_record)} agent(s) to process.", flush=True)

    if args.dry_run:
        for name, domain, prompts in agents_to_record:
            print(f"  • [{domain}] {name} -> {len(prompts)} prompts")
        return

    start_time = time.time()
    if len(agents_to_record) == 1:
        name, domain, prompts = agents_to_record[0]
        asyncio.run(
            record_single_agent_demo(
                agent_name=name,
                domain=domain,
                prompts=prompts,
                output_dir=args.output_dir,
                speed=args.speed,
                video_format=args.format,
                resolution=args.resolution,
                skip_existing=args.skip_existing
            )
        )
    else:
        tasks = [
            (name, domain, prompts, str(args.output_dir), args.speed, args.format, args.resolution, args.skip_existing)
            for name, domain, prompts in agents_to_record
        ]
        workers = min(args.workers, len(tasks))
        print(f"🚀 Launching {len(tasks)} demo recordings with {workers} parallel workers...", flush=True)
        results = []
        with ProcessPoolExecutor(max_workers=workers) as executor:
            for res in executor.map(_worker_record, tasks):
                results.append(res)
                success_count = sum(1 for r in results if r[2])
                print(f"Progress: [{len(results)}/{len(tasks)}] agents processed ({success_count} succeeded)", flush=True)
        print(f"🎉 Successfully recorded {success_count}/{len(tasks)} agent demos in {time.time() - start_time:.1f}s!")

if __name__ == "__main__":
    main()
