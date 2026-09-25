import requests
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

site_id = "1520da0e-7bba-4c12-ac76-4a5fe7344986"

# Check site for identity/access settings
resp = requests.get(f"{API}/sites/{site_id}", headers=HEADERS)
site = resp.json()

print("Checking for access control settings...")
print(f"  has_identity: {site.get('has_identity')}")
print(f"  identity: {site.get('identity')}")
print(f"  access_control: {site.get('access_control')}")

# Try to disable identity
if site.get('has_identity'):
    print("\nDisabling identity...")
    resp = requests.patch(
        f"{API}/sites/{site_id}",
        headers=HEADERS,
        json={"has_identity": False}
    )
    print(f"  Status: {resp.status_code}")

# Try to set public access
print("\nSetting public access...")
resp = requests.patch(
    f"{API}/sites/{site_id}",
    headers=HEADERS,
    json={
        "public_access": True,
        "auth_lifetime": 0,
        "role": "public"
    }
)
print(f"  Status: {resp.status_code}")
if resp.status_code != 200:
    print(f"  Error: {resp.text[:300]}")

# Check identity endpoints
print("\nChecking identity endpoints...")
resp = requests.get(f"{API}/sites/{site_id}/identity", headers=HEADERS)
print(f"  Identity status: {resp.status_code}")
if resp.status_code == 200:
    print(f"  Identity: {resp.json()}")

# Try to delete/disable identity
resp = requests.delete(f"{API}/sites/{site_id}/identity", headers=HEADERS)
print(f"  Delete identity: {resp.status_code}")

# Check for snippet injections or access rules
print("\nChecking for access rules...")
resp = requests.get(f"{API}/sites/{site_id}/access_rules", headers=HEADERS)
print(f"  Access rules: {resp.status_code}")
if resp.status_code == 200:
    print(f"  Rules: {resp.json()}")
