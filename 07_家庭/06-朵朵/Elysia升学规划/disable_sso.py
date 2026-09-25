import requests
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

account_id = "6a77e7b8dad05aca2cc58cd1"
site_id = "1520da0e-7bba-4c12-ac76-4a5fe7344986"

# Try to disable SSO login at account level
print("Disabling SSO login at account level...")
resp = requests.patch(
    f"{API}/accounts/{account_id}",
    headers=HEADERS,
    json={
        "site_sso_login": False,
        "site_sso_login_context": "none"
    }
)
print(f"Account update status: {resp.status_code}")
if resp.status_code == 200:
    print("  Success!")
else:
    print(f"  Error: {resp.text[:300]}")

# Try to disable SSO login at site level
print("\nDisabling SSO login at site level...")
resp = requests.patch(
    f"{API}/sites/{site_id}",
    headers=HEADERS,
    json={
        "sso_login": False,
        "site_sso_login": False
    }
)
print(f"Site update status: {resp.status_code}")
if resp.status_code == 200:
    print("  Success!")
else:
    print(f"  Error: {resp.text[:300]}")

# Verify the changes
print("\nVerifying account settings...")
resp = requests.get(f"{API}/accounts/{account_id}", headers=HEADERS)
if resp.status_code == 200:
    account = resp.json()
    print(f"  site_sso_login: {account.get('site_sso_login')}")
    print(f"  site_sso_login_context: {account.get('site_sso_login_context')}")
