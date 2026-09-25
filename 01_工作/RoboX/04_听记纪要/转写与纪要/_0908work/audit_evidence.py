# -*- coding: utf-8 -*-
"""0908 发言人归属证据表（v3, 可裁决版）

方法：以 10-gram 倒排索引把清理版每条 QA 定位回源文发言人块。
指标：
  cover = 该 QA 的 10-gram 中被该源块命中的比例（0~1）
  lcs   = 该 QA 与该源块的最长公共子串长度（字符）
裁决规则：
  cover>=0.30 且 lcs>=12 → 高置信；0.15<=cover<0.30 → 中置信；否则低置信（不作数）
"""
import re, io, sys, importlib.util
from collections import defaultdict, Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = 'D:/RoboX/04_听记纪要/转写与纪要/'
SRC = BASE + '09-08 RoboX与长虹机器人业务财务团队战略合作洽谈.txt'

N2NAME = {1: '曾昊山（总助）', 2: '田明', 3: '邹宇（Tony）', 4: '贾澜鹏（运营总监）',
          5: '周总（周怡成）', 6: 'Anson', 7: '张总（财务合规）'}

# ---------- 解析源文块 ----------
blocks = []
cur = None
for ln in open(SRC, encoding='utf-8').read().split('\n'):
    m = re.match(r'^发言人 ?(\d+)(?:（([^）]+)）)?\s+([\d:]+)\s*$', ln.strip())
    if m:
        cur = {'n': int(m.group(1)), 'txt': []}
        blocks.append(cur)
    elif cur is not None and ln.strip():
        cur['txt'].append(ln.strip())
for b in blocks:
    b['text'] = re.sub(r'\s', '', ''.join(b['txt']))
blocks = [b for b in blocks if len(b['text']) >= 4]

# ---------- 10-gram 倒排索引 ----------
K = 10
idx = defaultdict(set)
for bi, b in enumerate(blocks):
    s = b['text']
    for i in range(len(s) - K + 1):
        idx[s[i:i + K]].add(bi)

def lcs_len(a, b):
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    best = 0
    for i in range(1, len(a) + 1):
        cur = [0] * (len(b) + 1)
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                cur[j] = prev[j - 1] + 1
                if cur[j] > best:
                    best = cur[j]
        prev = cur
    return best

def locate(qa):
    """返回排序后的 (cover, lcs, bi) 列表"""
    s = re.sub(r'\s', '', qa)
    grams = [s[i:i + K] for i in range(len(s) - K + 1)]
    if not grams:
        return []
    votes = Counter()
    for g in grams:
        for bi in idx.get(g, ()):
            votes[bi] += 1
    out = []
    for bi, v in votes.items():
        l = lcs_len(s, blocks[bi]['text'])
        out.append((v / len(grams), l, bi))
    out.sort(key=lambda x: (-x[0], -x[1]))
    return out[:3]

# ---------- 载入清理版章节 ----------
spec = importlib.util.spec_from_file_location('dfc', BASE + '_0908work/data_final_chapters.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
CHAPTERS = mod.CHAPTERS

# ---------- 逐条核对 ----------
conf = defaultdict(Counter)     # docx_speaker -> {(source_n, level): count}
low = []
total = 0
for ci, ch in enumerate(CHAPTERS):
    for si, (spk, qa) in enumerate(ch['qa_pairs']):
        total += 1
        r = locate(qa)
        if not r:
            low.append((ci + 1, si, spk, '-', 0, 0, qa))
            continue
        cover, l, bi = r[0]
        src_n = blocks[bi]['n']
        level = '高' if (cover >= 0.30 and l >= 12) else ('中' if cover >= 0.15 else '低')
        conf[spk][(src_n, level)] += 1
        if level == '低':
            low.append((ci + 1, si, spk, f'{src_n}:{N2NAME.get(src_n)}', cover, l, qa))

print('=' * 108)
print('0908 长虹洽谈 — 发言人归属证据矩阵（清理版 speaker × 源文发言人编号）')
print('=' * 108)
hdr = f"{'清理版 speaker':<16}" + ''.join(f'{n}:{N2NAME.get(n,"?"):<10}' for n in range(1, 8)) + ' 合计'
print(hdr)
print('-' * 108)
for spk in ['田明', 'Anson', '邹宇（Tony）', '曾昊山（总助）', '周总（周怡成）', '童哥', '张维', '万涛']:
    row = f'{spk:<16}'
    tot = 0
    for n in range(1, 8):
        c = sum(v for (sn, lv), v in conf[spk].items() if sn == n)
        hi = sum(v for (sn, lv), v in conf[spk].items() if sn == n and lv == '高')
        tot += c
        row += f'{c}{"(" + str(hi) + "高)" if hi else "":<10}'[:10].ljust(10) if c else '·'.ljust(10)
    print(row + f' {tot}')
print('-' * 108)
print('括号内为该格“高置信”条数；· 表示无匹配')

print()
print(f"QA 总数: {total}    低置信条目: {len(low)}")
if low:
    print()
    print('=== 低置信条目（需人工裁决，前 30 条）===')
    for ci, si, spk, src, cover, l, qa in low[:30]:
        print(f'  [章{ci}:{si}] 现标={spk:<14} 源={src:<20} cover={cover:.2f} lcs={l:<3} {qa[:40]}')
