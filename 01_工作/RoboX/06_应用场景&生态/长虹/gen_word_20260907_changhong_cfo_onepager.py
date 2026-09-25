# -*- coding: utf-8 -*-
"""
RoboX×长虹 合作谈判一页纸（CFO会谈版）- Word生成脚本
2026-09-07
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

output_path = r"D:\RoboX\06_应用场景&生态\长虹\RoboX×长虹_合作谈判一页纸（CFO会谈版）_2026-09-07.docx"

COLOR_HEADING = RGBColor(0x1F, 0x4E, 0x79)
COLOR_SUMMARY = RGBColor(0x2E, 0x5C, 0x8A)
COLOR_NORMAL = RGBColor(0x00, 0x00, 0x00)
COLOR_NOTE = RGBColor(0x80, 0x80, 0x80)
COLOR_TABLE_HEAD = RGBColor(0x1F, 0x4E, 0x79)
FONT = '微软雅黑'

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2.2)
    section.bottom_margin = Cm(2.2)
    section.left_margin = Cm(2.6)
    section.right_margin = Cm(2.6)

style = doc.styles['Normal']
font = style.font
font.name = FONT
font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)
pf = style.paragraph_format
pf.space_after = Pt(6)
pf.line_spacing = 1.3


def set_run(run, size=11, bold=False, color=COLOR_NORMAL, italic=False):
    run.font.name = FONT
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.element.rPr.rFonts.set(qn('w:eastAsia'), FONT)


def add_para(text, size=11, bold=False, color=COLOR_NORMAL, align=None,
             space_before=0, space_after=6, indent=None, line_spacing=1.3):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    if indent is not None:
        p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    run = p.add_run(text)
    set_run(run, size=size, bold=bold, color=color)
    return p


def add_mixed_para(segments, space_after=6, space_before=0, indent=None, line_spacing=1.3):
    """segments: list of (text, dict(size, bold, color))"""
    p = doc.add_paragraph()
    if indent is not None:
        p.paragraph_format.left_indent = Cm(indent)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    for text, kw in segments:
        run = p.add_run(text)
        set_run(run, **kw)
    return p


def add_title(text):
    add_para(text, size=16, bold=True, color=COLOR_HEADING,
             align=WD_ALIGN_PARAGRAPH.CENTER, space_before=6, space_after=4)


def add_heading(text):
    p = add_para(text, size=13, bold=True, color=COLOR_HEADING,
                 space_before=14, space_after=4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1F4E79')
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_note(text):
    add_para(text, size=9.5, color=COLOR_NOTE, space_after=4)


def add_lead(text):
    """关键导语：粗体摘要样式"""
    add_para(text, size=11.5, bold=True, color=COLOR_SUMMARY,
             space_before=8, space_after=8, line_spacing=1.4)


def add_table(headers, rows, widths=None, font_size=9.5):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t.rows[0].cells
    for i, h in enumerate(headers):
        cell_p = hdr[i].paragraphs[0]
        cell_p.paragraph_format.space_after = Pt(2)
        run = cell_p.add_run(h)
        set_run(run, size=font_size, bold=True, color=COLOR_TABLE_HEAD)
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'DCE6F1')
        hdr[i]._tc.get_or_add_tcPr().append(shd)
    for r in rows:
        cells = t.add_row().cells
        for i, val in enumerate(r):
            cell_p = cells[i].paragraphs[0]
            cell_p.paragraph_format.space_after = Pt(2)
            run = cell_p.add_run(val)
            set_run(run, size=font_size)
    if widths:
        for i, w in enumerate(widths):
            for row in t.rows:
                row.cells[i].width = Cm(w)
    add_para('', size=6, space_after=2)
    return t


# ============ 文档内容 ============

add_title('RoboX × 长虹 合作谈判一页纸（CFO 会谈版）')

add_note('日期：2026-09-07　｜　用途：明日 CFO 沟通底稿 / 内部过会用　｜　密级：内部')
add_note('配套附件：《政策依据与申报窗口明细表》（见文件后半部分）')

# ---------- 一句话定位 ----------
add_heading('一、一句话定位与僵局本质')

add_lead('把“设备采购 + 数据采集 + 模型服务”从一笔单边采购对赌，重构为“分阶段验证 + 政策对冲 + 收入分成”的三层结构，让国企的合规与不亏损诉求、RoboX 的轻资产与数据/IP 权益同时成立。')

add_para('僵局本质：长虹怕“设备沉没 + 审计追责”，RoboX 怕“大额兜底 + 数据/IP 被套牢”。'
         '解法：把一次性大额对赌拆成分阶段、有条件、可解锁的承诺，并以兜底换对等独占权益。')

# ---------- 三句话 ----------
add_heading('二、给长虹 CFO 的三句话（结构提案）')

add_para('第 1 句｜分阶段走，每一步可验证、可退出、可申报', size=11.5, bold=True,
         color=COLOR_SUMMARY, space_before=6)

add_table(
    ['Phase', '范围', '双方投入', '决策门（Gate）'],
    [
        ['P0（3~6 月）', '小规模 POC 采集线',
         '长虹出少量设备+产线工时；RoboX 以折扣服务费共担',
         '数据质量合格率 [  ]% + 模型量化提升 [  ]%'],
        ['P1（放大）', '正式采集+模型服务', '按 P0 已验证 ROI 立项',
         '达标即放大，未达标低成本退出'],
        ['P2（规模化）', '多产线/多品类', '阶梯扩量，量越大单价越低',
         '分年解锁'],
    ],
    widths=[3.2, 3.6, 5.2, 4.4],
)

add_mixed_para([
    ('关键设计：', dict(bold=True, size=10.5)),
    ('P0 设备选通用可复用型号，提前与设备商签残值回购/转售条款 → 最坏情况下长虹退出损失 ≈ 设备价 × [  ]%（预计 [  ] 万元封顶）。CFO 不必一次批三期资金。', dict(size=10.5)),
], indent=0.3)

add_para('第 2 句｜资产风险移出长虹报表（三种结构请 CFO 选合规口径）', size=11.5, bold=True,
         color=COLOR_SUMMARY, space_before=8)
add_para('1. 联合项目公司（SPV）：长虹 70% / RoboX 30%（技术许可 License 折价入股）→ 账上为“长期股权投资+产学研合作”，非风险采购；License 费保障 RoboX 保底收入。', indent=0.5)
add_para('2. 第三方经营性租赁/融资租赁：设备由租赁方持有，长虹按年付租，账上为运营费用，期满可退可购。', indent=0.5)
add_para('3. 服务费化：设备投入改写为“数据服务费 + 里程碑验收”，不进固定资产审批。', indent=0.5)

add_para('第 3 句｜这笔支出在考核与政策口径里是“政绩”，不是亏损', size=11.5, bold=True,
         color=COLOR_SUMMARY, space_before=8)
add_para('• 研发投入视同利润加回（依据见后）→ 项目按“产学研/示范线”立项，财务考核口径不伤利润；', indent=0.5)
add_para('• 数采/灵巧手装备申报首台套 → 保险覆盖“质量缺陷修理更换退货 + 责任风险”，省级保费补贴 70%；', indent=0.5)
add_para('• 产线数采改造走“智改数转”专项（省级最高 2000 万）；', indent=0.5)
add_para('• 绵阳市级：国/省首台套奖励 50/30 万、智能工厂认定最高 100 万、AI 揭榜挂帅 ≤100 万。', indent=0.5)
add_para('材料分工：申报书由 RoboX 协助撰写——这是换取对等权益的筹码。', size=9.5, color=COLOR_NOTE, indent=0.5)

# ---------- 财务模型 ----------
add_heading('三、财务模型表头（今晚团队填充数据）')

add_table(
    ['项目', '金额（万元）', '备注'],
    [
        ['设备投入（P0/P1/P2 分列）', '[  ]', '通用型 + 回购条款'],
        ['数采 + 运维年成本', '[  ]', ''],
        ['可回收：首台套保费补贴', '[  ]', '省级保费 70%；国家配套再 +5%'],
        ['可回收：“智改数转”专项', '[  ]', '省级最高 2000 万'],
        ['可回收：市级奖励（首台套/智能工厂/AI 揭榜）', '[  ]', '50 + 100 + 100 万级'],
        ['3 年模型服务/分成收入预测', '[  ]', '保守/中性/乐观三档'],
        ['长虹净风险敞口（最坏情况）', '[  ]', '供 CFO 过会引用'],
        ['投资回收期', '[  ]', ''],
    ],
    widths=[7.5, 3.0, 5.9],
)

# ---------- 兜底条款 ----------
add_heading('四、兜底条款改写对照（谈判区）')

add_table(
    ['长虹诉求', 'RoboX 还价'],
    [
        ['每年购买 15 万小时',
         '改“年度最低服务包”，当年未用完滚动至次年（消除“买了用不完=浪费”顾虑）'],
        ['无条件兜底',
         '双向触发：RoboX 未达里程碑 → 承诺暂停/减半；长虹未提供产线工时/场景/标注配合 → 承诺自动顺延'],
        ['一次谈定总量',
         '阶梯式：第 1 年小承诺，后随验证成果放大；量越大单价越低'],
        ['只有义务',
         '兜底 = 买断对价：场景内排他（2+2 年）+ 数据全球独占训练权 + 其他工厂/品类优先扩展权'],
    ],
    widths=[3.6, 12.8],
)

add_mixed_para([
    ('红线（一步不让）：', dict(bold=True, size=10.5, color=COLOR_SUMMARY)),
    ('① 数据独占（无限制训练+跨场景复用）　② 模型 IP 归 RoboX　③ 场景排他　'
     '④ 兜底金额上限 + 与长虹付款/配合义务双向挂钩　⑤ 终止时 RoboX 有权按约定价收购设备。', dict(size=10.5)),
], space_before=4)

# ---------- 政策依据 ----------
add_heading('五、政策依据（给 CFO 自核，防“说过头”）')

add_para('5.1 “研发投入视同利润”三级链条', size=11, bold=True, color=COLOR_HEADING, space_before=4)
add_table(
    ['层级', '文件', '要点'],
    [
        ['长虹适用',
         '《绵阳市市属国有企业负责人经营业绩考核办法》（2020-12 印发，官方解读原文：“研发投入视同利润，在计算利润总额时予以加回”）；2026-08 底绵阳市国资委已完成新一轮全面修订',
         '当期限引文件，须以最新版为准'],
        ['省级参照',
         '《四川省省属国有企业负责人经营业绩考核办法》（2020-01 实施；2025-03 修订为“1+6”体系）',
         '同样写入视同利润'],
        ['央企源头',
         '《中央企业负责人经营业绩考核办法》（国资委令第 40 号）第十六条',
         '国资监管通行规则，市级系参照执行'],
    ],
    widths=[2.4, 9.2, 4.8],
)

add_mixed_para([
    ('边界（防被财务当场拆穿）：', dict(bold=True, size=10.5, color=COLOR_SUMMARY)),
    ('并非所有设备都能计入研发投入——仅直接用于研发/中试/试验的设备折旧与试验费可计；量产产线设备属固定资产投资。'
     '打法：示范/中试线走研发口径（视同利润 + 加计扣除 100%），量产改造线走“智改数转/设备更新”路径。', dict(size=10.5)),
])

add_para('5.2 四川省级可申报项', size=11, bold=True, color=COLOR_HEADING, space_before=8)
add_table(
    ['政策', '文号/组织', '额度'],
    [
        ['智改数转 + 设备更新技改',
         '《四川省加快制造业智能化改造数字化转型行动计划（2024—2027）》川办发〔2024〕43 号；年度申报（2026 年度已启动）',
         '省级重点最高 2000 万；技改补 5%–20%'],
        ['首台套保险补偿',
         '国家：工信厅联重装〔2024〕64 号（2026 年度已组织）；省级：川财建〔2020〕427 号 + 川经信装备〔2021〕124 号',
         '创新突破补 ≤30%（国际）/20%（国内），≤1000 万；省级保费补 70% ≤1000 万/年/产品；国家补贴配套 +5% ≤500 万'],
        ['研发平台/装备攻关',
         '省政府 2025 年“六方面”支持政策',
         '平台/攻关补 30%；产业基础再造最高 2000 万'],
        ['“人工智能+”一号创新工程',
         '《四川省加快推进“人工智能+”一号创新工程实施方案》2026-05',
         'AI+先进制造省级示范，场景开放'],
    ],
    widths=[3.6, 8.0, 4.8],
)

add_para('5.3 绵阳市可申报项', size=11, bold=True, color=COLOR_HEADING, space_before=8)
add_table(
    ['政策', '文号/时间', '额度'],
    [
        ['支持人工智能产业发展若干政策（试行）', '绵府规〔2024〕2 号',
         '国/省首台套奖励 50/30 万；揭榜挂帅 ≤100 万；算力补 ≤30%（年 ≤50 万）；备案大模型按研发投入 10% ≤200 万'],
        ['推进新型工业化高质量发展', '2025-07',
         '智能工厂 100/50/30 万；全球“灯塔工厂”300 万；“数字领航”有奖'],
        ['国家级城市试点', '制造业新型技改 + 中小企业数字化转型试点（2026）',
         '长虹以链主/支撑机构角色参与（覆盖领域待核）'],
        ['国企创新 15 条', '2026-07',
         '“国企+”创新联合体、研发投入刚性增长、AI 全链条赋能'],
    ],
    widths=[3.6, 4.6, 8.2],
)

# ---------- 会前待办 ----------
add_heading('六、会前待办（明日 CFO 到访前）')

todos = [
    '让长虹投资/项目申报部确认：《绵阳市市属监管企业负责人经营业绩考核办法》最新版是否保留“研发投入视同利润”；',
    '核实绵阳 AI 政策现行有效版本（原试行期至 2025 年中，确认升级版）＋“智改数转/首台套”当年申报窗口；',
    '团队填充财务模型表（今晚）；',
    '主谈分工：CFO 谈结构，技术负责人只回应“凭什么信你”（备 POC 数据 + 第三方验证）；',
    '议题顺序：分阶段 + 回购 → SPV/租赁/服务化 → 兜底数字；让步区间与红线先内部对齐。',
]
for i, item in enumerate(todos, 1):
    add_para(f'{i}. [  ] {item}', size=10.5, indent=0.4)

add_para('')
add_note('本文件为内部工作底稿，含 [  ] 占位数据待填充；对外版本另行整理。')

doc.save(output_path)
print(f'已生成: {output_path}')
