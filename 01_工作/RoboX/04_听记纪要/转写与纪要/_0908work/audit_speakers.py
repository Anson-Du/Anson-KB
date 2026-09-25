# -*- coding: utf-8 -*-
"""审计：源 txt 中 7 个发言人编号的称谓分布 + 语料抽样，用于裁决 speaker 归因。"""
import re, collections, io, sys

SRC = r"D:/RoboX/04_听记纪要/转写与纪要/09-08 RoboX与长虹机器人业务财务团队战略合作洽谈.txt"

with io.open(SRC, encoding="utf-8") as f:
    raw = f.read()

# 分块：形如 "发言人 1（周总）  HH:MM:SS\n文本..."
block_re = re.compile(r"发言人\s+(\d+)\s*(?:（([^）]*)）)?\s*(\d{2}:\d{2}:\d{2})\s*\n(.*?)(?=\n发言人\s+\d|$)", re.S)
blocks = []
for m in block_re.finditer(raw):
    n = int(m.group(1)); tag = m.group(2) or ""; ts = m.group(3); text = m.group(4).strip()
    text = re.sub(r"\s+", "", text)  # 去空白便于计数
    blocks.append((n, tag, ts, text))

print("== 块统计 ==", collections.Counter(b[0] for b in blocks))

# 称谓词表（含常见转写误字）
terms = ["田总","田明","安森","岩松","杜总","Anson","饺子","邹总","邹","黄老师","明修","Eric","王舜德","王总",
         "周总","怡成","贾总","贾","澜鹏","张总","张维","张伟","张艺","张梅","张老师","童哥","万涛","涛哥","万总",
         "浩山","昊山","曾总","公务员","波委","委员","波纹","碧莹","刘恒","林燕","蓝红","木林","长风","长虹",
         "沙帕","锐帕","Sharpa","穆林","睦灵","要命"]

# 每个编号统计称谓
speaker_texts = collections.defaultdict(list)
for n, tag, ts, text in blocks:
    speaker_texts[n].append((ts, text))

for n in sorted(speaker_texts):
    alltext = "".join(t for _, t in speaker_texts[n])
    print("\n========== 发言人", n, "总字数", len(alltext), "==========")
    cnt = {}
    for t in terms:
        c = alltext.count(t)
        if c:
            cnt[t] = c
    for t, c in sorted(cnt.items(), key=lambda x: -x[1]):
        print("  ", t, c)

# 含"贾/童哥/涛/张总/张维/王总/黄老师/公务员"等关键称呼的句子上下文（带编号）
print("\n\n===== 关键称谓上下文（谁在称呼谁）=====")
pat = re.compile(r"(贾总|贾|童哥|涛哥|万总|万涛|张总|张维|张伟|王总|黄老师|饺子|公务员|波委|委员|浩山|昊山|曾总)")
for n, tag, ts, text in blocks:
    for kw in set(pat.findall(text)):
        # 找到 kw 在 text 中的位置，截取附近 40 字
        idx = 0
        while True:
            i = text.find(kw, idx)
            if i < 0: break
            seg = text[max(0, i-35): i+35]
            print(f"[发{n}|{ts}] …{seg}…")
            idx = i + len(kw)
            break  # 每个块每个词只打一次
