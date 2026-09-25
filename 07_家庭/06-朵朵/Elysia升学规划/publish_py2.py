import subprocess, os

shim = r"C:\Users\Lenovo\.qoderworkcn\bin\ext\cli-common-shim-windows-amd64.exe"
work_dir = r"C:\Users\Lenovo\.qoderworkcn\workspace\msg3usob6k94fhku\outputs\elysia-plan"

env = os.environ.copy()
env['QWORK_SHIM_ROUTE'] = 'lark-cli'

# Try with CREATE_NEW_CONSOLE to force new process with correct cwd
result = subprocess.run(
    [shim, 'apps', '+html-publish', '--app-id', 'app_17bjymg1qe6', '--path', 'index.html', '--as', 'user'],
    cwd=work_dir,
    env=env,
    capture_output=True,
    text=True,
    timeout=60,
    creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.CREATE_NEW_PROCESS_GROUP
)

print(f"Return code: {result.returncode}")
print(f"Stdout: {result.stdout}")
print(f"Stderr: {result.stderr}")
