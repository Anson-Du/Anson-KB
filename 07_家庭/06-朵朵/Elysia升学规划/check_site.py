import requests
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Check site by ID
site_id = "1520da0e-7bba-4c12-ac76-4a5fe7344986"
resp = requests.get(f"{API}/sites/{site_id}", headers=HEADERS)
print(f"Site details (status {resp.status_code}):")
if resp.status_code == 200:
    site = resp.json()
    for key in ['id', 'name', 'url', 'ssl_url', 'admin_url', 'password_protected',
                'state', 'deploy_url', 'published_deploy', 'account_id',
                'managed_dns', 'domain_aliases', 'prime']:
        if key in site:
            val = site[key]
            if isinstance(val, dict):
                print(f"  {key}: {json.dumps(val, indent=4)[:200]}")
            else:
                print(f"  {key}: {val}")

    # Check if there's a password or auth setting
    print("\n  Checking for auth/password settings...")
    if 'password' in site:
        print(f"  Password: {site['password']}")
    if 'auth' in site:
        print(f"  Auth: {site['auth']}")

    # Try to update site to remove any password protection
    print("\n  Attempting to disable password protection...")
    resp2 = requests.patch(
        f"{API}/sites/{site_id}",
        headers=HEADERS,
        json={"password_protected": False}
    )
    print(f"  Update status: {resp2.status_code}")
    if resp2.status_code == 200:
        print("  Updated successfully")
    else:
        print(f"  Update failed: {resp2.text[:200]}")
else:
    print(f"Error: {resp.text}")
