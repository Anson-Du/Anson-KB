# -*- coding: utf-8 -*-
"""0908 发言人归属证据表（v4, 按发言人编号投票）

相对 v3 的改进：
  1) k-gram 从 10 降到 6，提高对"清理改写"文本的召回；
  2) 不再只取单个最佳块，而是把命中块按【源发言人编号】聚合投票，
     取得票最高者作为建议归属（更抗源文碎片化）。
指标：
  share = 该编号得票 / 全部命中票（0~1）
  lcs   = QA 与"该编号语料全文"的最长公共子串长度
裁决：share>=0.50 且 lcs>=12 → 高；share>=0.35 → 中；否则低
"""
import re, io, sys, importlib.util
from collections import defaultdict, Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
BASE = 'D:/RoboX/04_听记纪要/转写与纪要/'
SRC = BASE + '09-08 RoboX与长虹机器人业务财务团队战略合作洽谈.txt'
N2NAME = {1: '曾昊山', 2: '田明', 3: '邹宇Tony', 4: '贾澜鹏', 5: '周怡成', 6: 'Anson', 7: '张总财务'}

# ---- 源文块 & 编号语料 ----
blocks, cur = [], None
for ln in open(SRC, encoding='utf-8').read().split('\n'):
    m = re.match(r'^发言人 ?(\d+)(?:（([^）]+)）)?\s+([\d:]+)\s*$', ln.strip())
    if m:
        cur = {'n': int(m.group(1)), 'txt': []}; blocks.append(cur)
    elif cur is not None and ln.strip():
        cur['txt'].append(ln.strip())
for b in blocks:
    b['text'] = re.sub(r'\s', '', ''.join(b['txt']))
blocks = [b for b in blocks if len(b['text']) >= 4]
corpus = defaultdict(str)
for b in blocks:
    corpus[b['n']] += b['text']

K = 6
idx = defaultdict(set)
for bi, b in enumerate(blocks):
    s = b['text']
    for i in range(len(s) - K + 1):
        idx[s[i:i + K]].add(bi)

def lcs_len(a, b):
    if not a or not b: return 0
    prev = [0] * (len(b) + 1); best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        ai = a[i - 1]
        for j in range(1, len(b) + 1):
            if ai == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best: best = cur[j]
        prev = cur
    return best

def locate(qa):
    s = re.sub(r'\s', '', qa)
    grams = [s[i:i + K] for i in range(len(s) - K + 1)]
    if not grams: return None
    bvotes = Counter()
    for g in grams:
        for bi in idx.get(g, ()):
            bvotes[bi] += 1
    if not bvotes: return None
    nvotes = Counter()
    for bi, v in bvotes.items():
        nvotes[blocks[bi]['n']] += v
    tot = sum(nvotes.values())
    n, v = nvotes.most_common(1)[0]
    return n, v / tot, lcs_len(s, corpus[n]), tot, nvotes

spec = importlib.util.spec_from_file_location('dfc', BASE + '_0908work/data_final_chapters.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)

agg = defaultdict(Counter); nomatch = []; low = []
total = 0
for ci, ch in enumerate(mod.CHAPTERS):
    for si, (spk, qa) in enumerate(ch['qa_pairs']):
        total += 1
        r = locate(qa)
        if r is None:
            nomatch.append((ci + 1, si, spk, qa)); continue
        n, share, l, tot, nv = r
        level = '高' if (share >= 0.50 and l >= 12) else ('中' if share >= 0.35 else '低')
        agg[spk][(n, level)] += 1
        if level == '低':
            low.append((ci + 1, si, spk, f'{n}:{N2NAME.get(n)}', share, l, qa))

print('=' * 100)
print('0908 长虹洽谈 — 清理版 speaker × 源文发言人编号 证据矩阵（k=6 投票）')
print('=' * 100)
print(f"{'清理版 speaker':<16} " + ' '.join(f'{n}:{N2NAME.get(n):<9}' for n in range(1, 8)) + ' 合计')
print('-' * 100)
for spk in ['田明', 'Anson', '邹宇（Tony）', '曾昊山（总助）', '周总（周怡成）', '童哥', '张维', '万涛']:
    row, tot = f'{spk:<16} ', 0
    for n in range(1, 8):
        c = sum(v for (sn, lv), v in agg[spk].items() if sn == n)
        hi = sum(v for (sn, lv), v in agg[spk].items() if sn == n and lv == '高')
        tot += c
        row += (f'{c}({hi}高)' if hi else str(c) if c else '·').ljust(12)
    print(row + f'{tot}')
print('-' * 100)
print(f'QA 总数 {total}｜可定位 {total - len(nomatch)}｜完全无命中 {len(nomatch)}｜低置信 {len(low)}')
print()
print('=== 完全无命中（改写幅度过大，源文无对应 6-gram）===')
for ci, si, spk, qa in nomatch[:12]:
    print(f'  [章{ci}:{si}] {spk:<14} {qa[:52]}')
print()
print('=== 低置信（需人工裁决）===')
for ci, si, spk, src, share, l, qa in low[:25]:
    print(f'  [章{ci}:{si}] 现={spk:<14} 建议={src:<16} share={share:.2f} lcs={l:<3} {qa[:40]}')
