import requests, sys, json, zipfile, io, os

html_path = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan\index.html"

# Method 1: Try uploading to catbox.moe (free file hosting, serves HTML)
print("=== Method 1: catbox.moe ===")
try:
    with open(html_path, 'rb') as f:
        r = requests.post(
            'https://catbox.moe/user/api.php',
            data={'reqtype': 'fileupload'},
            files={'fileToUpload': ('index.html', f, 'text/html')},
            timeout=30
        )
    if r.status_code == 200 and r.text.startswith('http'):
        print(f"SUCCESS: {r.text.strip()}")
        with open(r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\deploy_result.txt", 'w') as f:
            f.write(r.text.strip())
        sys.exit(0)
    else:
        print(f"Failed: {r.status_code} - {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Method 2: Try litterbox (temporary hosting on catbox)
print("\n=== Method 2: litterbox.catbox.moe ===")
try:
    with open(html_path, 'rb') as f:
        r = requests.post(
            'https://litterbox.catbox.moe/resources/internals/api.php',
            data={'reqtype': 'fileupload', 'time': '72h'},
            files={'fileToUpload': ('index.html', f, 'text/html')},
            timeout=30
        )
    if r.status_code == 200 and r.text.startswith('http'):
        print(f"SUCCESS (72h): {r.text.strip()}")
        with open(r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\deploy_result.txt", 'w') as f:
            f.write(r.text.strip())
        sys.exit(0)
    else:
        print(f"Failed: {r.status_code} - {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

# Method 3: Try 0x0.st
print("\n=== Method 3: 0x0.st ===")
try:
    with open(html_path, 'rb') as f:
        r = requests.post(
            'https://0x0.st',
            files={'file': ('index.html', f, 'text/html')},
            timeout=30
        )
    if r.status_code == 200 and r.text.startswith('http'):
        print(f"SUCCESS: {r.text.strip()}")
        with open(r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\deploy_result.txt", 'w') as f:
            f.write(r.text.strip())
        sys.exit(0)
    else:
        print(f"Failed: {r.status_code} - {r.text[:200]}")
except Exception as e:
    print(f"Error: {e}")

print("\nAll free hosting methods failed.")
sys.exit(1)
