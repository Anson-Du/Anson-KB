import os, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOTS = [r"C:\Users\Lenovo"]
ZIP_EXTS = {'.zip', '.rar', '.7z', '.tar', '.gz', '.tgz', '.bz2', '.xz', '.cab'}
SKIP = ('\\AppData\\', '\\.git\\', '\\node_modules\\',
        '\\WindowsApps\\', '\\OneDrive\\')
MIN_ZIP_SIZE = 1 * 1024 * 1024

pairs = []
scanned_files = 0
scanned_dirs = 0

for root in ROOTS:
    for dirpath, dirnames, filenames in os.walk(root, onerror=lambda e: None):
        scanned_dirs += 1
        if any(s in dirpath for s in SKIP):
            continue
        scanned_files += len(filenames)
        zips = []
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in ZIP_EXTS:
                full = os.path.join(dirpath, fn)
                try:
                    sz = os.path.getsize(full)
                except OSError:
                    continue
                if sz >= MIN_ZIP_SIZE:
                    zips.append((fn, ext, full, sz))
        if not zips:
            continue
        for fn, ext, full, sz in zips:
            stem = fn[:-(len(ext))]
            folder = os.path.join(dirpath, stem)
            sibling_candidates = []
            has_dir = os.path.isdir(folder)
            if has_dir:
                sibling_candidates.append(stem + os.sep)
            for sib in filenames:
                if sib == fn:
                    continue
                if sib.startswith(stem + '.') or sib == stem:
                    sib_ext = os.path.splitext(sib)[1].lower()
                    if sib_ext in {'', '.iso', '.img', '.exe', '.msi', '.dmg',
                                   '.wim', '.bin', '.tar', '.zip'}:
                        sibling_candidates.append(sib)
            if has_dir or sibling_candidates:
                pairs.append({
                    'dir': dirpath,
                    'zip': fn,
                    'ext': ext,
                    'size_mb': round(sz / 1024 / 1024, 2),
                    'sibling_dir': has_dir,
                    'siblings': sibling_candidates[:5],
                })

report = {
    'roots': ROOTS,
    'scanned_dirs': scanned_dirs,
    'scanned_files': scanned_files,
    'min_zip_size_mb': MIN_ZIP_SIZE / 1024 / 1024,
    'pair_count': len(pairs),
    'total_mb': round(sum(p['size_mb'] for p in pairs), 2),
    'pairs': pairs,
}
with open(r"e:\11-其他\codebuddy\dupes_report.json", "w", encoding="utf-8") as f:
    json.dump(report, f, ensure_ascii=False, indent=2)

print("扫描根目录:", ROOTS)
print("扫描目录数:", scanned_dirs, "扫描文件数:", scanned_files)
print("压缩包阈值: ≥ 1 MB")
print("命中可清理对:", len(pairs))
total_mb = sum(p['size_mb'] for p in pairs)
if total_mb >= 1024:
    print(f"预计可释放: {round(total_mb/1024, 2)} GB")
else:
    print(f"预计可释放: {round(total_mb, 2)} MB")
print("--- 前 30 条样例 ---")
for p in pairs[:30]:
    sib = ','.join(p['siblings']) if p['siblings'] else '(同名目录)'
    print(f"  [{p['size_mb']}MB] {p['dir']}\\{p['zip']}  <->  {sib}")
print("完整报告: e:\\11-其他\\codebuddy\\dupes_report.json")