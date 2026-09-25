import requests
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

site_id = "1520da0e-7bba-4c12-ac76-4a5fe7344986"
deploy_id = "6a77eaf68c59294786bea0c7"

# Check deploy files with metadata
print("Checking deploy files...")
resp = requests.get(f"{API}/deploys/{deploy_id}/files", headers=HEADERS)
print(f"Status: {resp.status_code}")
if resp.status_code == 200:
    files = resp.json()
    for f in files:
        print(f"  File: {json.dumps(f, indent=4)}")

# Check deploy details for content type
print("\nChecking deploy details...")
resp = requests.get(f"{API}/deploys/{deploy_id}", headers=HEADERS)
if resp.status_code == 200:
    deploy = resp.json()
    # Look for any content type or mime settings
    for key in deploy.keys():
        if 'content' in key.lower() or 'mime' in key.lower() or 'type' in key.lower():
            print(f"  {key}: {deploy[key]}")

    # Check the full deploy object for any relevant fields
    print("\n  All deploy keys:")
    for key in sorted(deploy.keys()):
        val = deploy[key]
        if not isinstance(val, (dict, list)) or not val:
            print(f"    {key}: {val}")

# Try to get the file content directly
print("\nTrying to get file content...")
resp = requests.get(f"{API}/deploys/{deploy_id}/files/index.html", headers=HEADERS)
print(f"Status: {resp.status_code}")
print(f"Content-Type: {resp.headers.get('content-type')}")
if resp.status_code == 200:
    print(f"Content length: {len(resp.text)}")
    print(f"First 200 chars: {resp.text[:200]}")
