# -*- coding: utf-8 -*-
"""把 data_final_chapters.py 中每一行对回源 txt 发言人编号（字符bigram模糊匹配），
并按 2026-09-09 权威映射输出建议 speaker，供人工核对。"""
import re, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SRC = 'D:/RoboX/04_听记纪要/转写与纪要/09-08 RoboX与长虹机器人业务财务团队战略合作洽谈.txt'

# 权威映射
N2NAME = {
    1: '曾昊山（总助）',
    2: '田明',
    3: '邹宇（Tony）',
    4: '贾澜鹏（运营总监）',
    5: '周总（周怡成）',
    6: 'Anson',
    7: '张总（财务合规）',
}

# ---- 解析源文件 ----
lines = open(SRC, encoding='utf-8').read().split('\n')
blocks = []  # (n, text)
cur = None
for ln in lines:
    m = re.match(r'^发言人 ?(\d+)(?:（([^）]+)）)?\s+([\d:]+)\s*$', ln.strip())
    if m:
        cur = {'n': int(m.group(1)), 'texts': []}
        blocks.append(cur)
    else:
        if cur is not None and ln.strip():
            cur['texts'].append(ln.strip())
raw = [(b['n'], ''.join(b['texts'])) for b in blocks]


def norm(s):
    return re.sub(r'[\s，。、；：？！,.;:!?（）()""''「」\-—…·~A-Za-z0-9]', '', s)


def bigram_overlap(a, b):
    a = norm(a); b = norm(b)
    if not a or not b:
        return 0
    ba = set(a[i:i+2] for i in range(len(a)-1))
    bb = set(b[i:i+2] for i in range(len(b)-1))
    if not bb:
        return 0
    return len(ba & bb) / max(1, len(bb))


# ---- 载入数据 ----
import importlib.util
spec = importlib.util.spec_from_file_location('dfc', 'D:/RoboX/04_听记纪要/转写与纪要/_0908work/data_final_chapters.py')
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
CHAPTERS = mod.CHAPTERS

# 把整段raw拼成每发言人全文（用于低置信度回退）
per_speaker = {}
for n, t in raw:
    per_speaker.setdefault(n, []).append(t)

changed = []      # 建议变更行
keep = []         # 保持行（仍打印供抽查）
for ci, ch in enumerate(CHAPTERS):
    for si, (spk, text) in enumerate(ch['qa_pairs']):
        best = None; best_score = 0
        for n, t in raw:
            sc = bigram_overlap(text, t)
            if sc > best_score:
                best_score = sc; best = n
        suggest = N2NAME.get(best, f'发言人{best}')
        flag = '★CHANGE' if suggest != spk else '  ok    '
        line_info = f'[{ci+1}:{si}] {flag} cur={spk}  <->  源#{best}({suggest}) score={best_score:.2f}'
        # 取源句样例
        for n, t in raw:
            if n == best:
                snippet = norm(t)[:30]
                break
        if suggest != spk:
            changed.append((line_info, snippet, text[:60]))
        else:
            keep.append((line_info, snippet, text[:60]))

print('='*80)
print(f'建议变更 {len(changed)} 条 vs 保持 {len(keep)} 条 (共{len(changed)+len(keep)}条)')
print('='*80)
for info, snip, txt in changed:
    print(info)
    print(f'   源样例…{snip}')
    print(f'   正文…{txt}')
print()
print('----- 抽查 keep 中 score<0.25 的低置信行 -----')
for info, snip, txt in keep:
    sc = float(info.split('score=')[1])
    if sc < 0.25:
        print(info)
        print(f'   源样例…{snip}')
        print(f'   正文…{txt}')
