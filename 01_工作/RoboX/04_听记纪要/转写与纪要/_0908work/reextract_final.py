# -*- coding: utf-8 -*-
"""从上一版 docx 逆向重建 chapters 数据，并按 2026-09-09 确认的人物事实正确归因 speaker。
输出单一数据文件 data_final_chapters.py（含 CHAPTERS 全量列表）。
"""
import re
from docx import Document

DOCX = 'D:/RoboX/04_听记纪要/转写与纪要/09-08 RoboX与长虹机器人业务财务团队战略合作洽谈（清理版）.docx'
OUT = 'D:/RoboX/04_听记纪要/转写与纪要/_0908work/data_final_chapters.py'

doc = Document(DOCX)

# 遍历收集章节结构
chapters = []           # 每个: {"title":.., "qa_pairs":[(spk,text)]}
cur = None
in_body = False
for p in doc.paragraphs:
    t = p.text.strip()
    if not t:
        continue
    runs = p.runs
    # 标题检测：下划线 run
    is_title = bool(runs) and bool(runs[0].font.underline) and t[0] in '一二三四五六七八九十'
    # 正文开始标记
    if t.startswith('一、开场与双方介绍'):
        in_body = True
    if t == '—— 会议转写清理结束 ——':
        break
    if in_body and is_title:
        cur = {'title': t, 'qa_pairs': []}
        chapters.append(cur)
        continue
    if in_body and cur is not None and runs and len(runs) >= 2:
        speaker = runs[0].text
        # 显示名还原为原始 speaker 键
        if speaker.startswith('发言人'):
            speaker = speaker.split('（')[0].strip()
        # 提取正文：去掉 speaker 与 "：" 前缀
        body = t
        # 前缀 = speaker + 冒号
        if body.startswith(speaker):
            body = body[len(speaker):]
        if body.startswith('：'):
            body = body[1:]
        body = body.strip()
        if body:
            cur['qa_pairs'].append((speaker, body))

# ---- speaker 归因映射（2026-09-09 确认口径）----
def map_speaker(spk, text):
    if spk == '明修':
        if '田明，你来同步' in text:
            return 'Anson'
        if ('框架+子合同的标准架构' in text) or ('合同细节' in text and '张维' in text):
            return '邹宇（Tony）'
        return '田明'
    if spk == '黄老师':
        return '邹宇（Tony）'
    if spk == '张伟':
        return '张维'
    if spk == '发言人1':
        return '曾昊山（总助）'
    if spk == '周总':
        return '周总（周怡成）'
    return spk

# 文本称谓修正
def fix_text(text):
    text = text.replace('这跟黄老师一起做了规划', '这跟邹宇（Tony）一起做了规划')
    text = text.replace('再跟张伟再对一下', '再跟张维再对一下')
    text = text.replace('张伟老师', '张维老师')
    text = text.replace('首笔 5000 万今天到账', '首笔 5000 万正在打款流程中、预计本周到账')
    text = text.replace('首笔 5000 万已到账、第一轮', '首笔 5000 万预计本周到账、第一轮')
    return text

final_chapters = []
for ch in chapters:
    qa = []
    for spk, body in ch['qa_pairs']:
        new_spk = map_speaker(spk, body)
        qa.append((new_spk, fix_text(body)))
    final_chapters.append({'title': ch['title'], 'qa_pairs': qa})

# 输出 python 文件
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('# -*- coding: utf-8 -*-\n')
    f.write('# 0908 长虹洽谈 - 章节正文（2026-09-09 由 docx 逆向重建 + 人物归因修正）\n')
    f.write('CHAPTERS = [\n')
    for ch in final_chapters:
        f.write('    {\n')
        f.write(f'        "title": {ch["title"]!r},\n')
        f.write('        "qa_pairs": [\n')
        for spk, body in ch['qa_pairs']:
            f.write(f'            ({spk!r}, {body!r}),\n')
        f.write('        ]\n')
        f.write('    },\n')
    f.write(']\n')

# 校验输出
from collections import Counter
total_qa = sum(len(c['qa_pairs']) for c in final_chapters)
all_spk = [s for c in final_chapters for s, _ in c['qa_pairs']]
cnt = Counter(all_spk)
print(f'✅ 逆向重建完成: {len(final_chapters)} 个章节, {total_qa} 条对话')
for s, c in cnt.most_common():
    print(f'  {s}: {c}')
# 残留检查
for bad in ['明修', '黄老师', '张伟', '发言人1']:
    if bad in all_spk:
        print(f'  ⚠️ speaker 残留: {bad}')
# 展示每个章节首尾
for i, ch in enumerate(final_chapters):
    first = ch['qa_pairs'][0] if ch['qa_pairs'] else ('', '')
    print(f'  [{i+1}] {ch["title"]} ({len(ch["qa_pairs"])}条) 首条: {first[0]}')
