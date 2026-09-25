# -*- coding: utf-8 -*-
"""抽样 dump 发言人 1/4/7 的全部块前 60 字 + 时间戳，人工判断主题与身份。"""
import re, io, sys

SRC = r"D:/RoboX/04_听记纪要/转写与纪要/09-08 RoboX与长虹机器人业务财务团队战略合作洽谈.txt"
with io.open(SRC, encoding="utf-8") as f:
    raw = f.read()

block_re = re.compile(r"发言人\s+(\d+)\s*(?:（([^）]*)）)?\s*(\d{2}:\d{2}:\d{2})\s*\n(.*?)(?=\n发言人\s+\d|$)", re.S)
blocks = []
for m in block_re.finditer(raw):
    n = int(m.group(1)); tag = m.group(2) or ""; ts = m.group(3); text = re.sub(r"\s+", "", m.group(4).strip())
    blocks.append((n, tag, ts, text))

targets = sys.argv[1:] or ["4", "7", "1"]
for t in targets:
    print(f"\n################ 发言人 {t} 全量抽样 ################")
    for n, tag, ts, text in blocks:
        if str(n) == t:
            print(f"[{ts}] {text[:80]}")
