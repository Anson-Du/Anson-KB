import requests
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Check both sites
sites = [
    ("elysia-plan-1f2ffd0a93a1", "6a77e8a58c59293fafbea0cf"),
    ("elysia-dashboard-2d47a24b2921", "6a77e9ee6a27af059fa22944")
]

for name, deploy_id in sites:
    print(f"\n=== Site: {name} ===")
    resp = requests.get(f"{API}/sites/{name}", headers=HEADERS)
    if resp.status_code == 200:
        site = resp.json()
        print(f"  ID: {site.get('id')}")
        print(f"  URL: {site.get('url')}")
        print(f"  SSL URL: {site.get('ssl_url')}")
        print(f"  Admin URL: {site.get('admin_url')}")
        print(f"  Password protected: {site.get('password_protected')}")
        print(f"  State: {site.get('state')}")
        print(f"  Deploy URL: {site.get('deploy_url')}")
    else:
        print(f"  Error: {resp.status_code} - {resp.text[:200]}")

    # Check deploy status
    print(f"\n  Deploy {deploy_id}:")
    resp = requests.get(f"{API}/deploys/{deploy_id}", headers=HEADERS)
    if resp.status_code == 200:
        deploy = resp.json()
        print(f"    State: {deploy.get('state')}")
        print(f"    SSL URL: {deploy.get('ssl_url')}")
        print(f"    Deploy URL: {deploy.get('deploy_url')}")
        print(f"    Required: {deploy.get('required', [])[:3]}...")
        print(f"    Error: {deploy.get('error_message')}")
    else:
        print(f"    Error: {resp.status_code}")
