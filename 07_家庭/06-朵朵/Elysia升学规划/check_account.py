import requests
import json

TOKEN = "nfp_8BPNhfW6hayu59G2W5KoZgpEyzqENz7r5457"
API = "https://api.netlify.com/api/v1"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Check account/user settings
print("Checking user/account settings...")
resp = requests.get(f"{API}/user", headers=HEADERS)
if resp.status_code == 200:
    user = resp.json()
    print(f"User ID: {user.get('id')}")
    print(f"Email: {user.get('email')}")
    print(f"Slug: {user.get('slug')}")
    # Check for any account-level settings
    for key in user.keys():
        if 'verify' in key.lower() or 'access' in key.lower() or 'strict' in key.lower():
            print(f"  {key}: {user[key]}")

# Check account
account_id = "6a77e7b8dad05aca2cc58cd1"
print(f"\nChecking account {account_id}...")
resp = requests.get(f"{API}/accounts/{account_id}", headers=HEADERS)
if resp.status_code == 200:
    account = resp.json()
    print(f"Account details:")
    for key in sorted(account.keys()):
        val = account[key]
        if not isinstance(val, (dict, list)) or not val:
            print(f"  {key}: {val}")

# Try to update site to disable strict verification
site_id = "1520da0e-7bba-4c12-ac76-4a5fe7344986"
print(f"\nTrying to disable strict contributor verification...")
resp = requests.patch(
    f"{API}/sites/{site_id}",
    headers=HEADERS,
    json={
        "strict_contributor_verification": False,
        "public_access": True
    }
)
print(f"Status: {resp.status_code}")
if resp.status_code != 200:
    print(f"Error: {resp.text[:300]}")
