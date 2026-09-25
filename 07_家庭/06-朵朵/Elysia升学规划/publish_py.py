import subprocess, os, sys, shutil

# Create a temp dir at root level
temp_dir = "C:\\lark_publish_temp"
os.makedirs(temp_dir, exist_ok=True)

# Copy the HTML file
src = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan\index.html"
dst = os.path.join(temp_dir, "index.html")
shutil.copy2(src, dst)

print(f"Copied to: {dst}")
print(f"Temp dir: {temp_dir}")
print(f"File exists: {os.path.exists(dst)}")

# Run lark-cli from temp dir
shim = r"C:\Users\Lenovo\.qoderworkcn\bin\ext\cli-common-shim-windows-amd64.exe"
env = os.environ.copy()
env['QWORK_SHIM_ROUTE'] = 'lark-cli'

result = subprocess.run(
    [shim, 'apps', '+html-publish', '--app-id', 'app_17bjymg1qe6', '--path', 'index.html', '--as', 'user'],
    cwd=temp_dir,
    env=env,
    capture_output=True,
    text=True,
    timeout=60
)

print(f"\nReturn code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")

# Cleanup
try:
    shutil.rmtree(temp_dir)
except:
    pass
