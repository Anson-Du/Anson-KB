import requests

url = "https://elysia-dashboard-2d47a24b2921.netlify.app"
resp = requests.get(url, timeout=10)
print(f"Status: {resp.status_code}")
print(f"Headers: {dict(resp.headers)}")
print(f"Content-Type: {resp.headers.get('content-type')}")
print(f"Content length: {len(resp.text)}")
print(f"First 500 chars:\n{resp.text[:500]}")
