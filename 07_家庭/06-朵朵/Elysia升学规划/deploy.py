import zipfile, io, requests, sys, json, uuid, os

html_path = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan\index.html"

# Generate random subdomain
random_id = uuid.uuid4().hex[:12]
site_name = f"elysia-plan-{random_id}"
print(f"Target site name: {site_name}")

# Create zip in memory
buf = io.BytesIO()
with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.write(html_path, 'index.html')
buf.seek(0)

# Try Netlify anonymous deploy
print("Uploading to Netlify...")
try:
    r = requests.post(
        'https://api.netlify.com/api/v1/sites',
        files={'zip': ('site.zip', buf, 'application/zip')},
        timeout=60
    )
    print(f"Status: {r.status_code}")
    if r.status_code in (200, 201):
        data = r.json()
        url = data.get('ssl_url') or data.get('url', '')
        site_id = data.get('id', '')
        admin_url = data.get('admin_url', '')
        print(f"SUCCESS")
        print(f"URL: {url}")
        print(f"Site ID: {site_id}")
        print(f"Admin URL: {admin_url}")
        
        # Now try to update the site subdomain
        if site_id:
            print(f"\nUpdating subdomain to: {site_name}")
            r2 = requests.patch(
                f'https://api.netlify.com/api/v1/sites/{site_id}',
                json={'name': site_name},
                timeout=30
            )
            if r2.status_code == 200:
                d2 = r2.json()
                new_url = d2.get('ssl_url') or d2.get('url', '')
                print(f"Updated URL: {new_url}")
                # Save the final URL
                with open(r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\deploy_result.txt", 'w') as f:
                    f.write(new_url)
            else:
                print(f"Subdomain update failed: {r2.status_code}")
                with open(r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\deploy_result.txt", 'w') as f:
                    f.write(url)
        else:
            with open(r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\deploy_result.txt", 'w') as f:
                f.write(url)
        sys.exit(0)
    else:
        print(f"Response: {r.text[:500]}")
        print("Netlify anonymous deploy not available.")
        sys.exit(1)
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
