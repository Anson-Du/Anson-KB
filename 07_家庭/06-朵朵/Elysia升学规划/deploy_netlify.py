import requests
import zipfile
import os
import uuid
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
HTML_PATH = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan\index.html"
WORK_DIR = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku"

# Create zip file
zip_path = os.path.join(WORK_DIR, "deploy.zip")
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(HTML_PATH, "index.html")

# Generate random subdomain
random_id = uuid.uuid4().hex[:12]
site_name = f"elysia-plan-{random_id}"

print(f"Deploying as site: {site_name}")
print(f"Zip size: {os.path.getsize(zip_path)} bytes")

# Deploy to Netlify
url = f"https://api.netlify.com/api/v1/sites?name={site_name}"
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/zip"
}

with open(zip_path, 'rb') as f:
    resp = requests.post(url, headers=headers, data=f, timeout=60)

print(f"Status: {resp.status_code}")
result = resp.json()

if resp.status_code == 200 or resp.status_code == 201:
    site_url = result.get("ssl_url") or result.get("url") or f"https://{site_name}.netlify.app"
    print(f"SUCCESS! URL: {site_url}")
    # Save URL for QR generation
    with open(os.path.join(WORK_DIR, "deploy_url.txt"), "w") as f:
        f.write(site_url)
else:
    print(f"FAILED: {json.dumps(result, indent=2)}")
