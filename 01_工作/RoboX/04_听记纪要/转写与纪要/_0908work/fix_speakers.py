# -*- coding: utf-8 -*-
"""0908 speaker 归因修正脚本：明修→田明/Anson/邹宇(Tony)，黄老师→邹宇(Tony)，张伟→张维"""
import re

BASE = 'D:/RoboX/04_听记纪要/转写与纪要/_0908work/'

def fix_file(fn, special_rule):
    path = BASE + fn
    with open(path, encoding='utf-8') as f:
        text = f.read()
    # 逐行处理：定位 speaker 元组 ("NAME", "...")
    lines = text.split('\n')
    out = []
    for line in lines:
        m = re.match(r'^(\s*\()"([^"]+)"(,\s*")(.*)("\),?)$', line)
        if m:
            indent, speaker, mid, content, tail = m.groups()
            # 用 content 匹配特殊规则（先于通用规则）
            new_speaker = None
            if speaker == '明修':
                if '田明，你来同步' in content:
                    new_speaker = 'Anson'
                elif ('供应采购单' in content) or ('再跟张' in content and '合同细节' in content) or ('框架+子合同' in content):
                    new_speaker = '邹宇（Tony）'
                elif ('统一牵头人' in content) or ('项目经理' in content):
                    new_speaker = '田明'
                else:
                    new_speaker = '田明'
            elif speaker == '黄老师':
                new_speaker = '邹宇（Tony）'
            elif speaker == '张伟':
                new_speaker = '张维'
            elif speaker == '发言人1':
                new_speaker = '曾昊山（总助）'
            elif speaker == '周总':
                new_speaker = '周总（周怡成）'
            # 特殊行整体替换（content 改写）
            if speaker in special_rule:
                new_speaker, new_content = special_rule[speaker]
                content = new_content
            if new_speaker:
                line = f'{indent}"{new_speaker}"{mid}{content}{tail}'
        out.append(line)
    # 正文内的称谓替换（保留主语/讲述语境）
    text2 = '\n'.join(out)
    # 仅在正文文本(非speaker字段)替换会引起误伤的，仅处理明确称谓提及
    text2 = text2.replace('这跟黄老师一起做了规划', '这跟邹宇（Tony）一起做了规划')
    text2 = text2.replace('张艺/张伟等', '张维等')
    text2 = text2.replace('再跟张伟再对一下', '再跟张维再对一下')
    text2 = text2.replace('张伟老师', '张维老师')
    text2 = text2.replace('张梅压力大的话', '张梅压力大的话')
    # 融资到账表述修正（如仍残留"已到账/今日到账"在回答语境中）
    text2 = text2.replace('首笔 5000 万今天到账', '首笔 5000 万正在打款流程中、预计本周到账')
    text2 = text2.replace('首笔 5000 万已到账、第一轮', '首笔 5000 万预计本周到账、第一轮')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text2)
    print(f'✅ {fn} 修正完成')

# data2 特殊行（key = 原speaker）
special2 = {
    '发言人1': ('曾昊山（总助）',
                '今天是 9 月 8 号，欢迎大家来做这场交流。先介绍一下我们长虹这边的情况：运营整体由贾澜鹏（贾总）统筹推进——合同签署、公司成立这些事都是他在整体跟进；周总（周怡成）是财务负责人；童哥负责合规法务；张维负责数采厂；万涛负责硬件对接。今天我们也从集团合规和财务层面跟大家多交流。'),
    'Anson': ('田明',
              '我代表睦灵科技先做一个开场介绍。今天创始人明修也到了，主要想当面听听大家的意见；我（田明）负责产品；Anson 负责产业生态和政府关系（GA）；邹宇（Tony）负责业务方案和合同对接。今天主要是想跟长虹团队深度交流，把我们的公司背景、合作模式和接下来的推进节奏都完整过一遍。'),
    '明修': ('田明',
            '没问题，先回答融资节奏。首笔 5000 万正在打款流程中、预计本周到账；第一轮计划 2 亿，现在已经超募了，投后 20 亿。6-9 个月内我们要发布全新 RynnBrain 系列模型，再加上至少一个场景落地 demo，那一轮的估值能到 50 亿。第二轮就是 25-30 亿的估值。每轮稀释 10%，给团队期权池预留。创始人保持绝对控股，65%。'),
}
fix_file('data2_chapters.py', special2)

special3 = {}
fix_file('data3_chapters.py', special3)
print('全部完成')
