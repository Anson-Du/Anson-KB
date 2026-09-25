import requests
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

site_id = "1520da0e-7bba-4c12-ac76-4a5fe7344986"
deploy_id = "6a77eaf68c59294786bea0c7"

# Check deploy details
resp = requests.get(f"{API}/deploys/{deploy_id}", headers=HEADERS)
if resp.status_code == 200:
    deploy = resp.json()
    print("Deploy details:")
    for key in ['id', 'state', 'name', 'url', 'ssl_url', 'deploy_url',
                'draft', 'locked', 'published', 'title', 'context',
                'commit_ref', 'error_message']:
        if key in deploy:
            print(f"  {key}: {deploy[key]}")

    # Check if draft
    if deploy.get('draft'):
        print("\n  Deploy is DRAFT - publishing...")
        resp2 = requests.post(
            f"{API}/sites/{site_id}/deploys/{deploy_id}/publish",
            headers=HEADERS
        )
        print(f"  Publish status: {resp2.status_code}")
        if resp2.status_code == 200:
            print("  Published!")
        else:
            print(f"  Publish failed: {resp2.text[:200]}")

    # Check files in deploy
    print("\n  Files in deploy:")
    resp3 = requests.get(f"{API}/deploys/{deploy_id}/files", headers=HEADERS)
    if resp3.status_code == 200:
        files = resp3.json()
        for f in files[:10]:
            print(f"    {f.get('path')} - {f.get('sha1')}")
    else:
        print(f"  Could not list files: {resp3.status_code}")
