import subprocess, os, shutil

# Try to find if there's a token/config we can use directly
config_dirs = [
    os.path.expanduser("~/.lark-cli"),
    os.path.expanduser("~/.config/lark-cli"),
    os.path.join(os.environ.get('APPDATA', ''), 'lark-cli'),
    os.path.join(os.environ.get('LOCALAPPDATA', ''), 'lark-cli'),
]

for d in config_dirs:
    if os.path.exists(d):
        print(f"Found config dir: {d}")
        for f in os.listdir(d):
            fp = os.path.join(d, f)
            if os.path.isfile(fp):
                print(f"  File: {f} ({os.path.getsize(fp)} bytes)")
            elif os.path.isdir(fp):
                print(f"  Dir: {f}/")
                for ff in os.listdir(fp)[:5]:
                    print(f"    {ff}")

# Also check qoderworkcn dir for lark config
qw_dir = os.path.expanduser("~/.qoderworkcn")
if os.path.exists(qw_dir):
    print(f"\nQoderWork dir: {qw_dir}")
    for item in os.listdir(qw_dir):
        if 'lark' in item.lower():
            print(f"  Lark-related: {item}")
