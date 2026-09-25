# -*- coding: utf-8 -*-
"""v2: 用 IDF 加权的稀有 bigram 把正文行定位回源发言人编号。"""
import re, io, sys, math
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from collections import Counter, defaultdict

SRC = 'D:/RoboX/04_听记纪要/转写与纪要/09-08 RoboX与长虹机器人业务财务团队战略合作洽谈.txt'
N2NAME = {1:'曾昊山（总助）',2:'田明',3:'邹宇（Tony）',4:'贾澜鹏（运营总监）',5:'周总（周怡成）',6:'Anson',7:'张总（财务合规）'}

lines = open(SRC, encoding='utf-8').read().split('\n')
blocks = []
cur = None
for ln in lines:
    m = re.match(r'^发言人 ?(\d+)(?:（([^）]+)）)?\s+([\d:]+)\s*$', ln.strip())
    if m:
        cur = {'n': int(m.group(1)), 'texts': []}; blocks.append(cur)
    else:
        if cur is not None and ln.strip():
            cur['texts'].append(ln.strip())

corpus = defaultdict(str)
for b in blocks:
    corpus[b['n']] += ''.join(b['texts'])

def norm(s):
    return re.sub(r'[\s，。、；：？！,.;:!?（）()""''「」\-—…·~0-9A-Za-z%元个小时天台人亿等最多可以我们你们他们咱们这个那个这些那些一下目前现在因为所以但是如果就是还是已经开始进行相关主要都是会把把]', '', s)

# 全局 bigram 频次（用于 IDF）
docfreq = Counter()
n_docs = len(corpus)
for n, t in corpus.items():
    s = norm(t)
    for i in range(len(s)-1):
        docfreq[s[i:i+2]] += 1
N_TOTAL = sum(docfreq.values())
def idf(b):
    # 稀有度：出现在越少发言人语料中越有区分度
    return 1.0 / (0.5 + docfreq[b])

# 每个发言人的 bigram 集合
corpus_bg = {}
for n, t in corpus.items():
    s = norm(t)
    corpus_bg[n] = Counter(s[i:i+2] for i in range(len(s)-1))

import importlib.util
spec = importlib.util.spec_from_file_location('dfc', 'D:/RoboX/04_听记纪要/转写与纪要/_0908work/data_final_chapters.py')
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
CHAPTERS = mod.CHAPTERS

def best_speaker(text):
    s = norm(text)
    if len(s) < 4:
        return None, 0.0, {}
    bgs = [s[i:i+2] for i in range(len(s)-1)]
    scores = {}
    for n in corpus_bg:
        sc = 0.0; hit = 0
        for b in bgs:
            if corpus_bg[n][b] > 0:
                sc += idf(b); hit += 1
        scores[n] = sc
    total = sum(scores.values()) or 1
    r = {n: sc/total for n, sc in scores.items()}
    top = sorted(r.items(), key=lambda x: -x[1])
    return top[0], top[0][1], dict(r)

print('='*100)
print(f"{'章:行':<8}{'当前speaker':<14}{'建议(源编号)':<18}{'置信':<7}正文前45字")
print('='*100)
total_change = 0
for ci, ch in enumerate(CHAPTERS):
    for si, (spk, text) in enumerate(ch['qa_pairs']):
        res = best_speaker(text)
        if res is None or res[0] is None:
            continue  # 过短无区分度，保持原 speaker
        (bn, bs), conf, r = res
        sug = N2NAME.get(bn, f'发言人{bn}')
        flag = '★' if (sug != spk and conf > 0.45) else ' '
        if sug != spk and conf > 0.45:
            total_change += 1
        print(f"[{ci+1}:{si:<2}] {flag}{spk:<13} {sug:<16} {conf:.2f}  {text[:45]}")
print()
print(f'高置信建议变更: {total_change}')
