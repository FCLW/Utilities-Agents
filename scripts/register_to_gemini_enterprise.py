import json
import time
import subprocess
import requests
import google.auth
import google.auth.transport.requests
from pathlib import Path

def get_auth():
    try:
        token = subprocess.check_output(['gcloud', 'auth', 'print-access-token'], text=True).strip()
        if token:
            return token
    except Exception:
        pass
    creds, project = google.auth.default()
    auth_req = google.auth.transport.requests.Request()
    creds.refresh(auth_req)
    return creds.token

def list_reasoning_engines(token, project_id, locations):
    headers = {
        'Authorization': f'Bearer {token}',
        'x-goog-user-project': project_id
    }
    all_engines = []
    for loc in locations:
        url = f'https://{loc}-aiplatform.googleapis.com/v1/projects/{project_id}/locations/{loc}/reasoningEngines'
        page_token = ''
        while True:
            params = {'pageSize': 100}
            if page_token:
                params['pageToken'] = page_token
            try:
                r = requests.get(url, headers=headers, params=params)
                if r.status_code != 200:
                    break
                data = r.json()
                engines = data.get('reasoningEngines', [])
                all_engines.extend(engines)
                page_token = data.get('nextPageToken', '')
                if not page_token:
                    break
            except Exception as e:
                print(f"Error listing engines in {loc}: {e}")
                break
    return all_engines

def get_registered_ge_agents(token, ge_app_id):
    headers = {
        'Authorization': f'Bearer {token}',
        'x-goog-user-project': 'utilities-agents'
    }
    url = f"https://discoveryengine.googleapis.com/v1alpha/{ge_app_id}/assistants/default_assistant/agents"
    registered = []
    page_token = ''
    while True:
        params = {'pageSize': 100}
        if page_token:
            params['pageToken'] = page_token
        try:
            r = requests.get(url, headers=headers, params=params)
            r.raise_for_status()
            data = r.json()
            agents = data.get('agents', [])
            registered.extend(agents)
            page_token = data.get('nextPageToken', '')
            if not page_token:
                break
        except Exception as e:
            print(f"Error listing GE agents: {e}")
            break
    return registered

def main():
    project_id = "utilities-agents"
    project_number = "1032317060288"
    ge_app_id = f"projects/{project_number}/locations/global/collections/default_collection/engines/gemini-enterprise-utilitie_1787647502756"
    locations = ["us-central1", "us-east4", "us-east1", "us-west1"]

    print("Authenticating...")
    token = get_auth()

    print("Loading catalog...")
    catalog_path = Path("web/catalog.json")
    catalog = []
    if catalog_path.exists():
        with open(catalog_path) as f:
            catalog = json.load(f)

    catalog_by_normalized = {}
    for item in catalog:
        key = item['display_name'].lower().replace(" ", "_").replace("-", "_")
        catalog_by_normalized[key] = item
        key_id = item['id'].lower().replace(" ", "_").replace("-", "_")
        catalog_by_normalized[key_id] = item

    print(f"Listing Reasoning Engines across {locations}...")
    engines = list_reasoning_engines(token, project_id, locations)
    print(f"Found {len(engines)} Reasoning Engines.")

    print(f"Listing existing Gemini Enterprise registrations...")
    existing_ge_agents = get_registered_ge_agents(token, ge_app_id)
    print(f"Found {len(existing_ge_agents)} existing Gemini Enterprise registered agents.")

    # Map existing registrations by reasoning_engine resource name
    existing_by_re = {}
    for agent in existing_ge_agents:
        adk_def = agent.get('adkAgentDefinition') or agent.get('adk_agent_definition') or {}
        prov = adk_def.get('provisionedReasoningEngine') or adk_def.get('provisioned_reasoning_engine') or {}
        re_name = prov.get('reasoningEngine') or prov.get('reasoning_engine')
        if re_name:
            existing_by_re[re_name] = agent

    headers = {
        'Authorization': f'Bearer {token}',
        'x-goog-user-project': project_id,
        'Content-Type': 'application/json'
    }
    list_url = f"https://discoveryengine.googleapis.com/v1alpha/{ge_app_id}/assistants/default_assistant/agents"

    registered_count = 0
    updated_count = 0
    skipped_count = 0

    for idx, engine in enumerate(engines, 1):
        d_name = engine.get('displayName')
        re_id = engine.get('name')
        if not d_name:
            continue
        
        norm_key = d_name.lower().replace(" ", "_").replace("-", "_")
        catalog_item = catalog_by_normalized.get(norm_key)

        description = f"Autonomous Utilities Agent: {d_name} for Energy & Utilities workflows."
        tool_description = f"Assists with {d_name} analysis, calculations, diagnostics, and domain operations."
        
        if catalog_item:
            if catalog_item.get('description'):
                description = catalog_item['description']
            elif catalog_item.get('readme'):
                # Extract first paragraph of readme or business problem
                readme = catalog_item['readme']
                if "## 🏢 Business Problem" in readme:
                    part = readme.split("## 🏢 Business Problem")[1].split("##")[0].strip()
                    if part:
                        description = part[:500]

        payload = {
            "displayName": d_name,
            "description": description,
            "icon": {
                "uri": "https://fonts.gstatic.com/s/i/short-term/release/googlesymbols/smart_toy/default/24px.svg"
            },
            "adk_agent_definition": {
                "tool_settings": {"tool_description": tool_description},
                "provisioned_reasoning_engine": {"reasoning_engine": re_id}
            }
        }

        try:
            if re_id in existing_by_re:
                existing_agent_name = existing_by_re[re_id]['name']
                update_url = f"https://discoveryengine.googleapis.com/v1alpha/{existing_agent_name}"
                resp = requests.patch(update_url, headers=headers, json=payload, timeout=30)
                if resp.status_code == 200:
                    updated_count += 1
                    print(f"[{idx}/{len(engines)}] 🔄 Updated: {d_name}")
                else:
                    print(f"[{idx}/{len(engines)}] ⚠️ Update failed ({resp.status_code}) for {d_name}: {resp.text[:100]}")
            else:
                resp = requests.post(list_url, headers=headers, json=payload, timeout=30)
                if resp.status_code in (200, 201):
                    registered_count += 1
                    print(f"[{idx}/{len(engines)}] ✅ Registered: {d_name}")
                else:
                    print(f"[{idx}/{len(engines)}] ⚠️ Registration failed ({resp.status_code}) for {d_name}: {resp.text[:100]}")
            
            # Small throttle to respect rate limits
            time.sleep(0.5)

        except Exception as e:
            print(f"[{idx}/{len(engines)}] ❌ Exception for {d_name}: {e}")

    print("\n--- Registration Summary ---")
    print(f"Total processed: {len(engines)}")
    print(f"Newly registered: {registered_count}")
    print(f"Updated in-place: {updated_count}")

if __name__ == "__main__":
    main()
