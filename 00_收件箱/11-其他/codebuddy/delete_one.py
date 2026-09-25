import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

target = r"C:\Users\Lenovo\RoboX\04_听记纪要\转写与纪要\0819FA心流资本第二轮融资策略沟通.zip"
folder = target[:-4]   # 去掉 .zip
allowed_ext = {'.zip', '.rar', '.7z', '.tar', '.gz', '.tgz', '.bz2', '.xz', '.cab'}

ext = os.path.splitext(target)[1].lower()
assert ext in allowed_ext, f"拒绝: 扩展名 {ext} 不在白名单"
assert os.path.isfile(target), f"拒绝: 文件不存在 {target}"
assert os.path.isdir(folder), f"拒绝: 同名解压目录不存在 {folder}"

size_before = os.path.getsize(target)
print(f"目标: {target}")
print(f"扩展名: {ext} (白名单内)")
print(f"同名目录存在: {folder} (✓ 解压产物)")
print(f"删除前大小: {size_before/1024/1024:.2f} MB")

try:
    os.remove(target)
    assert not os.path.exists(target), "删除后文件仍存在"
    print(f"[已删除] {target}")
    print(f"[释放空间] {size_before/1024/1024:.2f} MB")
except Exception as e:
    print(f"[失败] {e!r}")
    sys.exit(1)

# 验证同名目录仍存在
print(f"[保留] 同名解压目录: {folder} (共 {len(os.listdir(folder))} 个条目)")