import requests
import hashlib
import os
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
HTML_PATH = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan\index.html"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Read HTML
with open(HTML_PATH, "rb") as f:
    html_bytes = f.read()

# Create a new deploy for the second site with forced upload
site_id = "1520da0e-7bba-4c12-ac76-4a5fe7344986"

# Modify content slightly to force new hash
html_modified = html_bytes + b"\n<!-- redeploy -->"
file_hash = hashlib.sha1(html_modified).hexdigest()

print(f"Creating new deploy with hash: {file_hash}")

# Create deploy
deploy_body = {
    "files": {
        "/index.html": file_hash
    },
    "draft": False
}
resp = requests.post(f"{API}/sites/{site_id}/deploys", headers=HEADERS, json=deploy_body)
print(f"Create deploy: {resp.status_code}")
deploy = resp.json()
deploy_id = deploy["id"]
required = deploy.get("required", [])
print(f"Deploy ID: {deploy_id}")
print(f"Required: {required}")

# Upload file
if file_hash in required:
    print("Uploading file...")
    upload_url = f"{API}/deploys/{deploy_id}/files/index.html"
    resp = requests.put(
        upload_url,
        headers={**HEADERS, "Content-Type": "application/octet-stream"},
        data=html_modified
    )
    print(f"Upload status: {resp.status_code}")
    if resp.status_code in (200, 201):
        print("Upload successful!")
    else:
        print(f"Upload failed: {resp.text}")
else:
    print("File not in required list, trying direct upload anyway...")
    upload_url = f"{API}/deploys/{deploy_id}/files/index.html"
    resp = requests.put(
        upload_url,
        headers={**HEADERS, "Content-Type": "application/octet-stream"},
        data=html_modified
    )
    print(f"Direct upload status: {resp.status_code}")

# Check deploy state
resp = requests.get(f"{API}/deploys/{deploy_id}", headers=HEADERS)
if resp.status_code == 200:
    d = resp.json()
    print(f"\nDeploy state: {d.get('state')}")
    print(f"Deploy URL: {d.get('deploy_url')}")
    print(f"SSL URL: {d.get('ssl_url')}")
    print(f"Error: {d.get('error_message')}")
