import requests
import hashlib
import os
import json
import uuid

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
HTML_PATH = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan\index.html"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Read HTML and compute SHA1 hash
with open(HTML_PATH, "rb") as f:
    html_bytes = f.read()

file_hash = hashlib.sha1(html_bytes).hexdigest()
print(f"File size: {len(html_bytes)} bytes")
print(f"File SHA1: {file_hash}")

# Step 1: Create site with random name
random_id = uuid.uuid4().hex[:12]
site_name = f"elysia-dashboard-{random_id}"
print(f"Creating site: {site_name}")

resp = requests.post(f"{API}/sites", headers=HEADERS, json={"name": site_name})
print(f"Create site status: {resp.status_code}")
if resp.status_code not in (200, 201):
    print(f"Error: {resp.text}")
    exit(1)

site = resp.json()
site_id = site["id"]
site_url = site.get("ssl_url") or site.get("url")
print(f"Site ID: {site_id}")
print(f"Site URL: {site_url}")

# Step 2: Create deploy with file digests
deploy_body = {
    "files": {
        "/index.html": file_hash
    }
}
resp = requests.post(f"{API}/sites/{site_id}/deploys", headers=HEADERS, json=deploy_body)
print(f"Create deploy status: {resp.status_code}")
if resp.status_code not in (200, 201):
    print(f"Error: {resp.text}")
    exit(1)

deploy = resp.json()
deploy_id = deploy["id"]
required = deploy.get("required", [])
print(f"Deploy ID: {deploy_id}")
print(f"Required files: {required}")

# Step 3: Upload the file if required
if file_hash in required:
    upload_url = f"{API}/deploys/{deploy_id}/files/index.html"
    resp = requests.put(
        upload_url,
        headers={**HEADERS, "Content-Type": "application/octet-stream"},
        data=html_bytes
    )
    print(f"Upload file status: {resp.status_code}")
    if resp.status_code not in (200, 201):
        print(f"Upload error: {resp.text}")
        exit(1)
else:
    print("File already cached, no upload needed")

# Final URL
final_url = f"https://{site_name}.netlify.app"
print(f"\n=== DEPLOYMENT SUCCESSFUL ===")
print(f"URL: {final_url}")

# Save URL
with open(r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\deploy_url.txt", "w") as f:
    f.write(final_url)
