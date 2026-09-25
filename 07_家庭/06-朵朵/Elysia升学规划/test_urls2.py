import requests

# Try different URLs
urls = [
    "https://elysia-dashboard-2d47a24b2921.netlify.app",
    "http://elysia-dashboard-2d47a24b2921.netlify.app",
    "http://6a77eaf68c59294786bea0c7--elysia-dashboard-2d47a24b2921.netlify.app",
    "https://6a77eaf68c59294786bea0c7--elysia-dashboard-2d47a24b2921.netlify.app",
]

for url in urls:
    try:
        resp = requests.get(url, timeout=10, allow_redirects=False)
        print(f"\n{url}")
        print(f"  Status: {resp.status_code}")
        print(f"  Location: {resp.headers.get('location', 'N/A')}")
        if resp.status_code == 200:
            print(f"  Content-Type: {resp.headers.get('content-type')}")
            print(f"  First 200 chars: {resp.text[:200]}")
    except Exception as e:
        print(f"\n{url}")
        print(f"  Error: {e}")
