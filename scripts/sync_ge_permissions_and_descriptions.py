#!/usr/bin/env python3
"""
sync_ge_permissions_and_descriptions.py

Synchronizes all 113 agents in Gemini Enterprise Discovery Engine:
1. Sets default permission to "Agent User" for "All Users" (sharingConfig: {"scope": "ALL_USERS"}),
   matching the Utilities Master Orchestrator.
2. Updates each agent's description to its tailored business-purpose description.
"""

import json
import time
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests
import google.auth
import google.auth.transport.requests
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from config.settings import settings
from config.agent_descriptions import AGENT_DESCRIPTIONS

PROJECT_ID = settings.gcp_project_id
PROJECT_NUMBER = "1032317060288"
GE_APP_ID = f"projects/{PROJECT_NUMBER}/locations/global/collections/default_collection/engines/gemini-enterprise-utilitie_1787647502756"

def get_auth_token():
    try:
        token = subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()
        if token:
            return token
    except Exception:
        pass
    creds, _ = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return creds.token

def list_registered_ge_agents(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'x-goog-user-project': PROJECT_ID
    }
    url = f"https://discoveryengine.googleapis.com/v1alpha/{GE_APP_ID}/assistants/default_assistant/agents"
    registered = []
    page_token = ''
    while True:
        params = {'pageSize': 100}
        if page_token:
            params['pageToken'] = page_token
        r = requests.get(url, headers=headers, params=params)
        r.raise_for_status()
        data = r.json()
        agents = data.get('agents', [])
        registered.extend(agents)
        page_token = data.get('nextPageToken', '')
        if not page_token:
            break
    return registered

def update_agent_permission_and_desc(token, agent, catalog_map):
    resource_name = agent['name']
    agent_id_num = resource_name.split('/')[-1]
    display_name = agent.get('displayName', '')
    
    # Identify matching catalog item
    norm_key = display_name.lower().replace(" ", "_").replace("-", "_")
    cat_item = catalog_map.get(norm_key, {})
    canonical_id = cat_item.get('id', norm_key)
    
    desc = AGENT_DESCRIPTIONS.get(canonical_id, agent.get('description', ''))
    if not desc:
        desc = f"Autonomous Utilities Agent: {display_name} for Energy & Utilities operations."

    payload = {
        "description": desc,
        "sharingConfig": {
            "scope": "ALL_USERS"
        }
    }
    
    headers = {
        'Authorization': f'Bearer {token}',
        'x-goog-user-project': PROJECT_ID,
        'Content-Type': 'application/json'
    }
    url = f"https://discoveryengine.googleapis.com/v1alpha/{resource_name}?updateMask=description,sharingConfig"
    
    retries = 3
    for attempt in range(retries):
        try:
            r = requests.patch(url, headers=headers, json=payload, timeout=30)
            if r.status_code == 200:
                res = r.json()
                scope = res.get('sharingConfig', {}).get('scope', 'NONE')
                return {
                    "id": canonical_id,
                    "num_id": agent_id_num,
                    "name": display_name,
                    "status": "SUCCESS",
                    "scope": scope,
                    "desc_len": len(res.get('description', ''))
                }
            elif r.status_code == 429:
                time.sleep(2 * (attempt + 1))
            else:
                return {
                    "id": canonical_id,
                    "num_id": agent_id_num,
                    "name": display_name,
                    "status": f"ERROR_{r.status_code}",
                    "error": r.text[:120]
                }
        except Exception as e:
            if attempt == retries - 1:
                return {
                    "id": canonical_id,
                    "num_id": agent_id_num,
                    "name": display_name,
                    "status": "EXCEPTION",
                    "error": str(e)
                }
            time.sleep(2)

def main():
    print("🔑 Authenticating with Google Cloud...")
    token = get_auth_token()
    
    print("📖 Loading catalog...")
    catalog_path = REPO_ROOT / "web" / "catalog.json"
    with open(catalog_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)
        
    catalog_map = {}
    for item in catalog:
        k1 = item['id'].lower().replace(" ", "_").replace("-", "_")
        k2 = item['display_name'].lower().replace(" ", "_").replace("-", "_")
        catalog_map[k1] = item
        catalog_map[k2] = item

    print("🔎 Fetching registered agents in Discovery Engine (Gemini Enterprise)...")
    agents = list_registered_ge_agents(token)
    print(f"Found {len(agents)} registered agents in Gemini Enterprise.")

    print(f"🚀 Updating descriptions and setting default permissions (sharingConfig.scope='ALL_USERS') across all {len(agents)} agents...")
    start_time = time.time()
    
    results = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(update_agent_permission_and_desc, token, a, catalog_map): a for a in agents}
        for future in as_completed(futures):
            res = future.result()
            results.append(res)
            if res["status"] == "SUCCESS":
                print(f"  ✅ [{len(results)}/{len(agents)}] {res['name']} -> scope={res['scope']}, desc_len={res['desc_len']}")
            else:
                print(f"  ❌ [{len(results)}/{len(agents)}] {res['name']} -> {res['status']}: {res.get('error', '')}")

    elapsed = time.time() - start_time
    success_count = sum(1 for r in results if r["status"] == "SUCCESS")
    all_users_count = sum(1 for r in results if r.get("scope") == "ALL_USERS")
    
    print("\n" + "=" * 60)
    print("📊 GEMINI ENTERPRISE SYNCHRONIZATION SUMMARY")
    print(f"  • Total agents in Gemini Enterprise: {len(agents)}")
    print(f"  • Successfully updated:              {success_count}/{len(agents)}")
    print(f"  • Scope 'ALL_USERS' verified:        {all_users_count}/{len(agents)}")
    print(f"  • Execution time:                    {elapsed:.1f}s")
    print("=" * 60)

if __name__ == "__main__":
    main()
