# -*- coding: utf-8 -*-
"""
生成 0818 FA波谱资本沟通BP 录音转写清理版 Word 文档
"""
import sys
import os
sys.path.insert(0, r'C:\Users\Lenovo\.workbuddy\skills\transcript-cleaner\scripts')

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

# 全局样式
style = doc.styles['Normal']
style.font.name = 'Microsoft YaHei'
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
style.font.size = Pt(11)

# 页面设置
section = doc.sections[0]
section.top_margin = Cm(2.54)
section.bottom_margin = Cm(2.54)
section.left_margin = Cm(3.18)
section.right_margin = Cm(3.18)

# 颜色定义
COLOR_TITLE = RGBColor(0x1F, 0x4E, 0x79)
COLOR_HEADING = RGBColor(0x1F, 0x4E, 0x79)
COLOR_FA = RGBColor(0xC0, 0x00, 0x00)         # Summer - 深红色（外部嘉宾/FA）
COLOR_CTO = RGBColor(0x70, 0x30, 0xA0)        # 明修 - 紫色
COLOR_COF = RGBColor(0x00, 0x80, 0x80)        # 田明 - 青色
COLOR_CSO = RGBColor(0x80, 0x60, 0x40)        # Anson - 棕色
COLOR_TEAM = RGBColor(0x40, 0x40, 0x40)
COLOR_GRAY = RGBColor(0x80, 0x80, 0x80)
COLOR_RED_HIGHLIGHT = RGBColor(0xC0, 0x00, 0x00)

SPEAKER_COLORS = {
    '明修': COLOR_CTO,
    '田明': COLOR_COF,
    'Summer': COLOR_FA,
    'Anson': COLOR_CSO,
    '团队成员': COLOR_TEAM,
}

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_TITLE

def add_note(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = COLOR_GRAY

def add_summary_heading(text):
    """关键要点标题（深红色突出）"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_RED_HIGHLIGHT
    # 加底部边框
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), 'C00000')
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_summary_item(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run('• ' + text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(11)

def add_heading(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_HEADING
    # 底部边框
    pPr = p._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1F4E79')
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_dialogue(speaker, text, indent=True):
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(0.75)
    p.paragraph_format.line_spacing = 1.5
    # 发言人
    run = p.add_run(f'{speaker}：')
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.bold = True
    run.font.size = Pt(11)
    run.font.color.rgb = SPEAKER_COLORS.get(speaker, COLOR_TEAM)
    # 内容
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(11)

def add_paragraph(text, indent=False):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    if indent:
        p.paragraph_format.left_indent = Cm(0.75)
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run.font.size = Pt(11)

# === 文档标题 ===
add_title('0818 FA波谱资本沟通BP 录音转写清理版')

# === 会议信息 ===
add_note('会议时间：2026年8月18日 16:50｜时长：37分钟52秒')
add_note('参会人：明修、田明、Summer、Anson、团队成员')

# === 关键要点总结 ===
add_summary_heading('一、会议关键要点（综合转写与三张图片）')

summary_items = [
    'BP 核心诊断：Summer 判断当前 BP 信息过载，每一页都好但"什么都想"，投资人记不住。需要从信息过载收敛到记忆点——一页一个核心差异点。',
    '唯一记忆点重构：第8页要突出"同源 AR 架构 + 触觉闭环"，这是 ROBOX 的核心差异化标签，必须让人一眼记住。',
    '七大差异化标签：成果图谱 + 全 AR 架构 + 构成在 System Two + 主脑图路/触觉 + 触发数据始标 + 自我本心引训练 + 模型营部卡性——形成完整差异化叙事链。',
    '页面重构建议（Echo AI 整理）：第2、3页合并为架构与触觉；第4、6页业务规划合并；第5页中试地兴触；第9页触觉集成；第10页训练短姿脑铁；第11~13页触觉图集；第13页36个月路经。',
    '叙事原则：抓重点（每页一个核心记忆点）、只讲自己（差异化口径完全认到）、以人的视角叙事（从第三视角+代际认知+拼延能力）、硬件美术交付化（不拿paper做信任凭据）。',
    '商业化口径：不要设延——初期通过软件思维+合规路地 tschedule；中期通过产品发布+跟随生态天规——明确日期口径，不模糊。',
    '估值策略：当前轮 20亿人民币投后，下一轮 40亿，提议分 20亿×38亿（保留最后一轮 20亿）三段策略，避免估值倒挂。',
    '时间窗口：目标是年底 close 第一轮，最稳节点 9月20号（团队预算到位），本轮无法 close 就多轮并行推进，不被动等待。',
    '机构推进现状：红杉（已约三次，本周二/周三/下周）｜高瓴/集核（周已了解，下轮沟通推荐人）｜IDG（五源/已约）｜五源（已了解/AI投后主投）｜深势期院（多轮/优质组合）｜阿斯亚亚创始曹泰睿有鹰｜其他大美元基金。',
    '资金结构与派活：美元 vs 人民币（风投节奏差异）｜超级转债（向下轮权力过渡工具）｜JV 主体架构（新加坡，便于美元基金进入）｜并行推进多轮不被动。',
    '场景叙事三层：近期（合作方提供场景+ROBOX出基模/lessons）｜中期（AI for Science/生物制药等高价值密度场景）｜远期（特种场景/太空/星辰大海——画面感太强可省略）。',
    '商业化问题应答：内部要准备答案（商业化三种讲法：卖数据/卖本体/模型嵌本体），对外不主动讲，关键还是追求模型智能上限。',
    '首席科学家/顾问问题：明修已经不讲首席，顾问看参与深度。中国顾问团在 BP 里是减分项，容易漏气。',
    '后续投资行动：高瓴周五见面（思涵陪同）｜北京/上海/杭州集中约见｜国庆节冲刺 close 第一轮｜新加坡 JV 主体准备就绪。',
    '基金生态观察：丁丁基金（10亿美金许华哲/80亿估值）、量子计算/太空算力（半年160亿中科天算）——情绪到位就有可能性，但不要跟随报。',
]
for item in summary_items:
    add_summary_item(item)

# === 二、图片核心结论（融资策略与机构推进地图）===
add_summary_heading('二、融资策略与机构推进地图（图片1核心结论）')

img1_items = [
    '【估值策略】第一轮 20亿人民币投后，第二轮 40亿，建议分 20亿×38亿（保留最后一轮 20亿），三段分轮避免估值倒挂。',
    '【时间窗口】年底 close 第一轮为目标；9月20号左右是协议谈判物理极限；本轮无法 close 就并行推进多轮不被动。',
    '【机构现状】红杉已约三次（Weiming责任）｜高瓴集核已有了解｜IDG同体销｜五源 AI 投后主投｜深势期院优质组合｜阿斯亚亚创始曹泰睿有鹰。',
    '【资金结构】美元 vs 人民币双线｜超级转债作为下轮权力过渡工具｜JV 主体（新加坡）便于美元基金进入｜并行推进多轮不被动。',
    '【估值参照】朋本尔 2.5亿美元最新轮｜大朋分研源逻辑 5500万~1.5亿美元｜TT 2.5~3.5亿美元｜Brisup 生产估值参照。',
    '【关键结论】对方团队当前最关切是 summer 机构要量产落浪，要把多数机听后期 summer —— 啥子是急心的推动最激动，下周后定线下秋季交提。',
]
for item in img1_items:
    add_summary_item(item)

# === 三、BP重构指南（图片2核心结论）===
add_summary_heading('三、BP 重构指南：从信息过载到记忆点（图片2核心结论）')

img2_items = [
    '【核心诊断】当前 BP 内容太多，每一页都很好但"什么都想"，投资人不可能把每页都记住——需要精品放到记忆位。',
    '【7大差异化标签】①成就图谱（全量和别人不一样）②深度 AR 架构（co-design+co-training，去 diffusion）③构成在 System Two（ego-centric 3D+Shadow layers）④主脑图路/触觉 Model System Two ⑤触发数据始标（ego-centric 3D+视觉/触觉/光感视觉触觉）⑥自我本心引训练（长程/同成中点）⑦模型营部卡性。',
    '【页面重构】第1页标题放松｜第2、3页合并为架构与触觉｜第4、6页业务规划合并｜第5页中试地兴触｜第9页触觉集成｜第10页训练短姿脑铁｜第11~13页触觉图集｜36 个月路经（家庭造应）。',
    '【叙事原则】抓重点（每页一个核心记忆点）｜只讲自己（差异化口径完全认到）｜以人的视角叙事（从第三视角+代际认知+拼延能力路径）｜硬件美术交付化（不拿 paper 做信任凭据）。',
    '【商业化口径】不要设延——初期通过软件思维+合规路地 tschedule，中期通过产品发布+跟随生态天规，明确日期不模糊。',
]
for item in img2_items:
    add_summary_item(item)

# === 四、本周行动清单（图片3核心结论）===
add_summary_heading('四、本周行动清单（图片3核心结论）')

img3_items = [
    '【今天立即】①重写 BP 第8页突出"同源 AR 架构 + 触觉闭环"唯一记忆点｜②团队页提到第3页（投资人听到核心团队再来）｜③删除/合并第3、6页重复的行业铺垫｜④准备商业化问题应答口径（不主动讲，被问到能答）。',
    '【本周】①安排 2~3 场 summer 跟进（边听边调）｜②周五高瓴见面，summer 安排思涵陪同｜③制作夏都接洽面图，summer 安排合伙人｜④确定北京/上海/杭州机构拜访计划，集中约见。',
    '【下周】正式冲刺，目标国庆节 close 第一轮｜九月二十号资金瓶颈完机构｜同步推进多轮/加轮沟通（多线并行，不需 close）。',
    '【持续】①推进与高瓴、长虹与合作伙伴的战略协议/MOU（作为场景验证证据）｜②准备新加坡 JV 主体架构（便于美元基金进入）。',
]
for item in img3_items:
    add_summary_item(item)


# === 五、录音转写正文 ===
add_heading('五、录音转写正文')

# --- 第一章：BP核心诊断 ---
add_heading('一、BP核心诊断：信息过载，没有记忆点')

add_dialogue('明修', '架构这个现在其实基本没有人提。这里面又涉及到比如是不是自然语言不重要，而是前空间的传递才重要——这是我们提到的同源架构。')
add_dialogue('田明', '前空间这个都太细了，比如同架构。')
add_dialogue('明修', '对，同架构，全 AR 的同架构。然后提两个 feature：大脑的 scaling 要通过长程任务来做，在灵巧操作层面把触觉融入进去。主要讲的就是这几件事。')
add_dialogue('Summer', '都会讲，都会讲一下，就最后讲。')
add_dialogue('明修', '因为现在看盘就是我们其实所有的 scanner 是在模型架构上会做 scanner，就是在架构上会有些创新，因为现在架构都 scaling 不了，我们会在这里面去改一些很底层的东西。')
add_dialogue('Summer', '我觉得可能先讲，或者说这里面有太总结，跟其他的那个对比过。')
add_dialogue('明修', '基本串起来。')
add_dialogue('Anson', '对。')
add_dialogue('明修', '刚才就是"我要成为啥"然后"别人啥问题"，你看我们这做的很好——在整个模型架构上我们要做啥嘛？这就是我们想要做的。核心几个 feature：同源的 AR 架构、做长程任务、做触觉，进入模型结构里，模型能力持续是领先的。这里面就会去拆这几个关键工作——大脑要验证啥？这个要验证啥？模型要验证完的点，就是那我缺数据，数据我要怎么去做？')
add_dialogue('Summer', '别人菜是菜在没有定义出关键的。')
add_dialogue('Anson', '四和五是告诉你你能看懂的东西对吧？其实不一定你看懂了的——你看到很多这些第四页就是 50 亿以上、100 亿的公司，对吧？做成怎么样？我告诉你我做成怎么样。')
add_dialogue('Summer', '哎这里面有一个比较有意思的点：你说大家是怎么一个模型的智能？我们设计一下怎么让它变得更智能？还有一个就是 scaling 对吧？就这两个我们有点揉在一起了。')
add_dialogue('Anson', '智能和 scaling 不是一回事吗？')
add_dialogue('Summer', '不，我觉得大家还是有一点区别的——scaling 这件事情的话，因为大家现在普遍讲的就是说你怎么在某一个场景里面去建立起一个很强的智能，模型怎么去设计的，然后再讲怎么去 scanning、怎么去泛化。目前都是这么讲。')
add_dialogue('Anson', '听到了吗？')
add_dialogue('Summer', '对啊，都这么讲。所以就会觉得有点这个揉在一起——对应到我们就是灵巧智能跟 scanning，我们可能这么讲，其实分开讲。')
add_dialogue('Anson', '灵巧智能和 scanning 分开。')
add_dialogue('Summer', '现在他们讲 scanning，他们数据 scanning。')
add_dialogue('Anson', '数据 scanning 和模型 scanning 应该是关键啊——数据 scanning 上去了 100 万小时、1000 万小时，模型吃不下。我现在就是告诉你三条路线里面，这两条根本就吃不下 1000 万小时。')
add_dialogue('明修', '那你上来就讲。')
add_dialogue('Anson', '我是上来就讲这个，就直接把 VLA 和……除了第七页之外，第七页非常重要——就是第七页是我们的整个思路，然后马上告诉你现在的自建模型和 VLA 都是错的。')
add_dialogue('田明', '对对对。')
add_dialogue('Anson', '对，就你投了那么多，我告诉你他们都错了。')
add_dialogue('田明', '我觉得可以把第七页就放在第二页后面，整个三四五六可以多讲后续或者干。')
add_dialogue('Anson', '第七页放在第二页。')
add_dialogue('Summer', '我刚才聊就是把第七页放到第二页——这两页其实有点……')
add_dialogue('Anson', '其实对，删是可以删的。这页的确是可以删了。')
add_dialogue('Summer', '对，这两页可以删了。然后对，这对应到这一页也可以删了——这两页其实就是在讲问题。那其实这两页问题，这两页怎么去放？')
add_dialogue('明修', '这个就是讲系统性的严格的，就是我们要做啥。')
add_dialogue('Summer', '没有领先性。')
add_dialogue('明修', '对，先把。然后并且是验证过的。')
add_dialogue('Summer', '这个也引掉，这个也引掉。')
add_dialogue('Anson', '把引掉的都往后。这两页讲问题的是不是放一起？这两页你要么放这里，然后讲别人的状态、我们的状态，这两个视频是——做对比效果的，有连贯的冲击的。讲完这段放完视频之后，就出我们模型介绍。')
add_dialogue('明修', '我感觉这一页应该在这个后。我们可能说这说我们很有前瞻性，那跟别人对比我们确实很厉害就开始讲——为什么他们不厉害？他们有什么问题？其实就是这个嘛，讲他们有什么问题，就应该抛你的那个。')
add_dialogue('Summer', '抛的是这个，对吧？')
add_dialogue('明修', '抛你的三层架构，这个三层架构是要连在他后边。')
add_dialogue('Anson', '三层架构连他后面。')
add_dialogue('明修', '对呀，你看因为你这就是三层架构嘛，所以你这样就是你三层架构的展开嘛——我三层架构就是这样的，然后你就去介绍你这核心的。')
add_dialogue('Summer', '这个我觉得是的，这是的。')
add_dialogue('明修', '对吧——你说这俩架构不行，我要做这种架构，这种架构是啥？你就把这玩意打开了呀，然后你再往下，不就讲你这第一第二层的做了啥？这个系统一又做了啥？就总分结构嘛。')
add_dialogue('田明', '其实我觉得 4 和 5 号不是矛盾一，6 面临的问题——6 面临的问题是因为你刚说的那一句，大家现在都要往里面水再加足，加特别会议、各种乱七八糟的会议，但其实这个它支撑不了。这应该是四五那个要送的问题。')
add_dialogue('Summer', '四五六这个顺序我感觉不是特别的。')
add_dialogue('明修', '四五六是把问题讲完，然后引出我们这个——四五应该。')
add_dialogue('田明', '这应该有一个新的用户，其实讲的是这个。')
add_dialogue('Summer', '我为什么想把这俩放一起写？这都是在展示行业问题。')
add_dialogue('田明', '对，但是他又不是讲他的。')
add_dialogue('Summer', '对，这个讲明巧，对，这个讲的是 stand node。')
add_dialogue('田明', '对，然后这一页完了之后，其实应该有一页就讲那几个关键词，就是我们不要讲一样一样的。')
add_dialogue('Summer', '这一页要调，只是放这，这一页内容都得调。')
add_dialogue('明修', '其实这一页核心讲的内容是什么？全 AR 的一个……是是是，模型，对，就是这样的一个。')
add_dialogue('Summer', '就是你的你这个模型的核心的亮点。')
add_dialogue('Anson', '那我这是不是要讲完这两个模型铺垫呢？这个是 brain，这是 vri。')
add_dialogue('Summer', '没有没有，我觉得就先讲这一页，然后再。')
add_dialogue('明修', '它是总分结构，总分结构。')
add_dialogue('Anson', '这两页是我们过去的工作。但过去工作引入了，就是告诉我为什么，就是告诉大家为什么我要选这个路线？')
add_dialogue('明修', '你是先讲的因，然后他很多人讲的就是你要干啥？讲果。你要你要干啥？对，他想先听到你要干啥，然后他再去倒推你为什么要这么干。')
add_dialogue('Summer', '是。先说你干啥，然后你为什么。')
add_dialogue('田明', '然后这两个月的核心问题是他没有表达出你刚才说的那部分。')
add_dialogue('Anson', '或者说这样，就是到这里讲，就是说现在现状的没有影响操作，对他们这事做——好，加了引角操作你看我们就能做好了。这个引角操作如何有一个更泛化的效果呢？我就要在模型架构这。')
add_dialogue('田明', '我觉得太绕了，我们就要很，这样你就没有很冲击力了，你看上来就是就把这个药。')
add_dialogue('明修', '那那那那那那就是说吧，那就是把药接到这个 3 后面——对对对，上来就是说我们一直是技术领先的，这就是我们的一个主张，你看别人没那么干、干那么菜，我们干干那么好。我接下来要做什么？就从这开始讲——也就是说其实我觉得这几页解释，解释更多的应该是讲我们后续要做什么，而不是之前我们做了什么。')
add_dialogue('Anson', '这几页解释的目的是为了证明，其实它是证明我们团队能力，我们烧了很多的钱，然后有了这样子的一个。')
add_dialogue('明修', '不不不冲突——你这一页里面，其实就是我基于我原来做的这个东西，我接下来的一个验证点是什么？我基于原来做的东西，我接下来这块要验证的点是什么？你要持续给大家传达我下一阶段要验证什么，所以我才需要钱去验证。')
add_dialogue('田明', '我之前做过这个，接下来我要我组的话，我现在的创新点是这个。')
add_dialogue('明修', '那你还要以怎么样自洽的形式？')
add_dialogue('Anson', '那你还不如把 8 和 9 提到 3 后面。')
add_dialogue('Summer', '不，还有一个——你怎么讲述？你怎么讲述？')
add_dialogue('明修', '他喜欢从分到总讲，我喜欢从总到分讲。')
add_dialogue('Summer', '对，所以就是最终来讲还是你讲的舒服了。他喜欢铺垫先。')
add_dialogue('明修', '我喜欢上来先抛东西，抛完了以后我再去展开。')
add_dialogue('Anson', '对，我有时候讲现在是跳的，就看你对投资人哪个页感兴趣，我就会跳到那页。')
add_dialogue('Summer', '对，看你的风格。')
add_dialogue('Anson', '我觉得听得懂的人这一页会感兴趣——这一页基本上就是听我讲不会提问，但是他能理解这中间的价值，这三页是最感兴趣的。这一页更多的是解释，我一直在解释。')
add_dialogue('Summer', '这一页其实我觉得就是信息太多了——这一页非常关键为什么要完成签？因为这一页是最大差异化，表达也很好——这个 demo 就是炫富嘛，这一页也在表达某种意义上在表达我们的一些差异化，那这两页的话，那这两页的话就是还是能。')
add_dialogue('Anson', '所以最早是要放一起的——最早就是先放视频，然后。')
add_dialogue('Summer', '我觉得倒也没有——这个其实是一个行业铺垫啊，这个是展现我们行业认知的，其实它也不涉及到我们差异化什么东西。')
add_dialogue('Anson', '这两页都是行业。')
add_dialogue('Summer', '证书一个，效果。')
add_dialogue('田明', '第五页是不是做个自我介绍？')
add_dialogue('Anson', '第五页是啊——说实话是提神，讲到这的时候其实已经困了，有可能就要开始看视频了。')
add_dialogue('田明', '怎么讲到第四页就困了呢？原来这在后面。')
add_dialogue('明修', '你至少要在第五页你就要去讲你的核心差异了，你要干啥——很多人上来他是先关心你要干啥，因为他们他们之前是有 context 的。')
add_dialogue('Anson', '那是不是我们第一页就应该讲清楚我们，我们要干啥？')
add_dialogue('明修', '第一页先建立一个信任——第一页就是我得很，你就得先相信我，然后我讲我要干啥。')
add_dialogue('Anson', '有道理——第一页是我是谁嘛？第二个我要干啥是吧？')
add_dialogue('Summer', '对对对。我觉得这样先这样讲，讲了你是不是——我觉得这，但是这一页都有，这页内容。')
add_dialogue('Anson', '这页是，我就感觉这页很重要，但是每天都在解释，解释完也懵了。')
add_dialogue('明修', '我要我要干啥？我要怎么干了？从企业，下面那几个，我要验证哪里？')
add_dialogue('Summer', '其实这几页也都是我们怎么干的——这几页是拆开讲。')
add_dialogue('明修', '但他现在讲的这几个页是过去怎么干的——实际上我想说的是，基于过去怎么干的，我下一阶段我要做哪几个关键点？')
add_dialogue('Anson', '感受到了，我要给大家解释解释我的差异。')
add_dialogue('明修', '他是从这个里面展开的，只不过原来是先铺垫完再放的这种嘛——对，当你一铺垫完的时候，别人就会陷进去，然后问十一页嘛，那个很多。')
add_dialogue('Anson', '11 页是有很多人就根本不知道初选数据哪里来——第 10 页我现在基本不讲，因为我觉得模型架构已经不重要了。其实第 10 页是可以隐掉的，就直接从。')
add_dialogue('明修', '在这就讲了，在这就讲。第 10 页在这就讲。')
add_dialogue('Anson', '或者明修，我们能不能在就是主报告后边附一个——如果你关心这个问题，在附件几，在附件几，就是有一个附件，把一些你认为有可能他会关心的。')
add_dialogue('Summer', '这些都可以放附录。')
add_dialogue('Anson', '第十三页。')
add_dialogue('明修', '就转苹果那个。')
add_dialogue('Anson', '转苹，不是转苹果，那个是数据管线。')
add_dialogue('明修', '啊，数据管线就是采集那——这种创新点太多了，也不好。')
add_dialogue('Summer', '我觉得，创新点太多了之后一直到第十四页——没有没有，我觉得也没有你们那个啥，我我觉得现在这个也不用太太，我觉得关键把这一页再改改，然后这两页的话就是因为这一页的重点不够突出，所以导致你讲到这一页的时候，大家有点懵逼——为什么突然讲到数据了？而且数据会那啥，因为你这一页不够关键、不够 highlight 的触觉吧，所以你这两页讲，其实这个很顺的，我觉得这个讲的挺顺的——从大脑到操作再到触觉，触觉也是一个有亮点特色的地方，但是你这一页不强调，你突然跳到触觉，就有点懵。')
add_dialogue('明修', '我觉得这个就是要做啥，就这一页他们是要你历史的东西，那么你要下一阶段，你无论你要做啥，那个你要做啥。')
add_dialogue('Summer', '核心就是把这一页改改——其他的我觉得就先讲，我觉得还好。然后这个月我觉得要再加速一下，时间点上，36 个月是不是太长了？')
add_dialogue('明修', '我们已经很左倾了，再加速点就是极左主义。')
add_dialogue('田明', '我们已经很努力了。')
add_dialogue('Summer', '我可以激进一点，把它改 25。')
add_dialogue('明修', '哈哈哈，24 个人。')
add_dialogue('Summer', '没事，其实我是这么一说啊。')
add_dialogue('Anson', '我感觉如果稍微懂一点的投资人，他就觉得你这个在乱吹。')
add_dialogue('Summer', '因为就是说，你就是说我复刻一个原来这个时间更短，毕竟有些还是复刻的工作，你不是从零开始。')
add_dialogue('明修', '不，我们现在都不敢，我们都不提复刻，就直接就是我们就会造一个新的东西，会在下一阶段就有。')
add_dialogue('Anson', '这也可以。好久没讲，好久没讲——对，这也删了。')
add_dialogue('Summer', '因为你真的——你讲自己盘的嘛。你讲那一页，人家有问题，你这个确实有很多卡的问题，自己不好解决。')
add_dialogue('明修', '但卡我们准备好了。')
add_dialogue('Summer', '所以现在这个逻辑试一试。')
add_dialogue('明修', '我还有个问题，就是团队是放在最后讲还是放前面讲？')
add_dialogue('Summer', '按照现在这个逻辑放最后。但是。')
add_dialogue('Anson', '你刚才不说上来讲我是谁？')
add_dialogue('Summer', '对呀——是这样的，对，但是他这个逻辑下面的话，就是最后为什么我们能把上面盖好？就是我们是完整的交付的。')
add_dialogue('明修', '对，现在这个逻辑先讲事后讲人——对，实际上当我真正面对一个投资人的时候，我首先还要介绍自己。我就首先就要先去介绍人，然后才会去介绍事。')
add_dialogue('Anson', '你介绍人不会介绍特别久——就一上来你把第一那页团队其实很多内容，这页内容很多。')
add_dialogue('Summer', '其实先介绍自己是对的，就先讲。')
add_dialogue('明修', '把这个移到第三页。')
add_dialogue('Anson', '这移到第三页，一上来就介绍团队了。')
add_dialogue('明修', '啊对——因为大家被吸引过来是因为你是阿里的核心团队，对，不是因为你是做抽烟岛的。')
add_dialogue('Summer', '嗯，对。你像吗？大概是定位是我。')
add_dialogue('Anson', '有道理——对，是的。')
add_dialogue('明修', '你你跟路人做抽烟岛也没人进。')
add_dialogue('Summer', '对，我们肯定介绍的时候都已经铺垫过了，这是一个什么产品。')
add_dialogue('明修', '我看他们其他的那个团队——我爸是院士的那种，就直接就上来就对——你们最大的差异化是什么？我爸是院士——哈哈哈，你们应该知道是某家公司。我觉得那个图，你跟 VLA 重点要讲，你基于过去的基础上，我们要做什么？')
add_dialogue('Anson', '16 也在这页讲，在这页讲——就这页你要讲差异化，就要把未来要做什么。')
add_dialogue('明修', '你的核心 feature 要讲。然后那你过去的里面，这个是不是也要包含？')
add_dialogue('田明', '为什么这一页效果这么好？是因为这一页的信息很直观，理解。')
add_dialogue('Anson', '是是——太多内容了。我知道，所以这一页我讲，我做的很开心啊——哈哈哈，但是后面还没有认真开始去重构。')
add_dialogue('Summer', '我觉得把第八页重构掉了就差不多了——第第九页也也也挺 highlight，虽然东西看的多但是也挺 highlight。第十页的话就就确实不重要，带过一下，但也不能说删掉——十一十二是闭环的，十三、十四，就十三页我就新建一个。')
add_dialogue('明修', '十一那讲我意思是想从 2 位转化数据。')
add_dialogue('Anson', '没有，就是你现在是没有数据的，所以你在这里要体现传播上的能力——然后说这里是没有数据的，所以后面数据该怎么办？那数据最大问题是没有数据，而不是别的模型架构。')
add_dialogue('Summer', '我们把这版再发一下，这个规划这个——这个规划我觉得我们可以试。')

# --- 第二章：估值与时间窗口 ---
add_heading('二、估值策略与时间窗口')

add_dialogue('明修', '就是我们本来称的 WR。')
add_dialogue('Summer', '明天在广州，周四周五在北京。')
add_dialogue('明修', '周六应该可以。就你这样，先推一推。')
add_dialogue('Summer', '对，北京的——把蓝旗要推一下，什么？')
add_dialogue('明修', '蓝旗还是见面聊。')
add_dialogue('Summer', '哦，不是蓝旗，是高瓴——高瓴，周五是高瓴，蓝旗是刚才徐。')
add_dialogue('明修', '高瓴可以聊聊，无所谓——高瓴可以聊，到时候我让思涵去陪一下，正好也听一听——那就周五——对，周五。对——因为刘冲那个也不浪费，我还是那句话，就是纯粹就面熟。把它列出来，你们他那条线反正不投，到时候换一条就行。那，说实话，万一呢？对吧？万一呢？对，还是那句话，就万一呢？')
add_dialogue('Summer', '蓝驰是下午刚聊完。对，还是他。')
add_dialogue('明修', '线上。')
add_dialogue('Summer', '线，这里。他不来这里，我不跟他聊——可以。')
add_dialogue('明修', '现在不来这里，我基本上不聊，线上太累。')
add_dialogue('Summer', '线上感觉也不用，因为因为说实话价格这么贵，线下也不动——我觉得后面就是一个来杭州，第二个是我们可能集中的上海建一个，北京建一个——对吧？效率。')
add_dialogue('明修', '可以，就这么搞。其他的看你还有，看你们还有啥问题？')

# --- 第三章：场景叙事与商业化口径 ---
add_heading('三、场景叙事与商业化口径')

add_dialogue('Anson', '就是我有几个问题——我们说我们是干什么的时候，你觉得我们这种叙事现在，你们有什么意见？')
add_dialogue('田明', '你们能第一时间听懂沟通。')
add_dialogue('Anson', '就是我们是干什么的，意思就是说我们的产品是什么？我们的客户是谁？我们这个趋势，你觉得清不清晰？')
add_dialogue('Summer', '因为我们是干什么？我们客户是谁？当然现在我们这里面都还就没有讲我们到底的落地场景——就刚才我们又聊。')
add_dialogue('Anson', '就场景是场景嘛——关键就是我们是干什么的？我们的定位，我对我们卖什么、我卖给谁——这件事情说，你觉得说的够不够清晰？')
add_dialogue('Summer', '现在实话实说啊，做 world model 这帮做模型的公司，这件事情不太重要。')
add_dialogue('田明', '哦，不，不重要。')
add_dialogue('Summer', '太重要——你说模型公司卖给谁？模型公司的商业模式是什么？')
add_dialogue('Anson', '但是是这样啊，这个问题如果讲不清楚的话，所有的后边的跟商业有关的，比如说营收的节奏、对。甚至我们的客户是谁？我们的商业模式——这些叙事就都更离散了。')
add_dialogue('Summer', '我知道我知道——因为为什么这么说这件事情呢？因为今天大家都模型，也是知道模型的智能的价值是最高的。上来你去讲你的应用的话，你就是，要不就是你是跟本地厂的合作，你给本地厂卖大佬吗？还是说你是怎么个模式？我觉得就是我们去回答这个问题很简单——我们第一个阶段还是追求的模型的智能上限。')
add_dialogue('Anson', '他是做右派，坚定的右派。')
add_dialogue('Summer', '就是我们要坚定，对吧？')
add_dialogue('Anson', '那那我不懂。')
add_dialogue('Summer', '因为你说实话，如果你坚定地去走，就右派的话，那就变成了比如说……')
add_dialogue('Anson', '那我理解是这样——我的理解明修就是说，其实我们自己内部要非常的战略性的重视这个话题，但是对外的话呢，我们不一定非得要主动的去。')
add_dialogue('Summer', '因为你现在去补齐去讲商业，就是讲不。')
add_dialogue('Anson', '啊啊，我明白。')
add_dialogue('Summer', '就是就是在具身，就是就 word model 的商业模式就是不清晰的。')
add_dialogue('田明', '那面临投资人这方面的问题，我们怎么回答？')
add_dialogue('Summer', '这这里面我觉得有很多啊——比如说很多讲一概子讲卖数据，对吧？有很多去讲，有不同的讲法卖数据，有的也得干本体，对吧？有的也要干本体去卖本体，对吧？因为你的模型嵌在本体里。')
add_dialogue('Anson', '那就是说。')
add_dialogue('Summer', '对吧？都有各种各样的讲法。')
add_dialogue('Anson', '那要不要回答？就如果问我，就是说肯定不可能不回答嘛。')
add_dialogue('Summer', '我觉得这件事情——就是内部再商量一下，我没有办法给一个，因为这个跟你们的基因有关系。')
add_dialogue('Anson', '你的建议就是我们肯定是要准备一个。')
add_dialogue('Summer', '对，但是你要很坚定。')
add_dialogue('Anson', '但不一定主动放，是这意思吗？')
add_dialogue('Summer', '对对对，在这个阶段的话，我们最关键还是要追求模型的智能上线。')
add_dialogue('Anson', '是每一个。对对对。')
add_dialogue('明修', '讲完，嗯——他问的商业化部分之后，比如说田明会主动讲这个，然后我一般会补话，我们现在更多的还在聚焦。')
add_dialogue('Summer', '对对，这个角度，对吧？')
add_dialogue('Anson', '那你听懂了——就是您的意思就是，要准备怎么回答？而且要认真准备——但是呢，不一定一定要主动的说——那好，那第二个问题，我的第二个问题就是说，关于刚才您说的场景——就场景这件事情，我们是要主动说吗？还是说，因为商业模式是商业模式嘛。')
add_dialogue('Summer', '我觉得我觉得我觉得场景这一页的话，还是要带一下，因为我们不也提到——我们在那 36 个月。')
add_dialogue('Anson', '要主动讲，是吧？')
add_dialogue('Summer', '还都要讲，这个场景还是挺关键。')
add_dialogue('Anson', '就今天上午，我们跟我们的合作方开会的时候，我有一个感觉就是说其实我们可以讲一个场景矩阵——什么意思呢？就是近期可能我们为了快速的铺开市场，包括甚至就是为了收集数据以及影响力，我可能会再切入某一些场景，但这个场景可能不是那么高价值的场景，但是我们的同时也在推高价值的场景。我想讲一个，我的什么意思呢？我当我说场景这件事情的时候，我尽可能，')
add_dialogue('明修', '我觉得把场景刚才说的能力的路径——我们可能从短期能做的，中期要探索的，远期畅想的，画在一张图上搞出来。到时候我讲这一页的时候跳出来的——就他肯定是一个能力矩阵。')
add_dialogue('Anson', '就你你你你，明修，我刚才没听懂，你再你再说一遍。')
add_dialogue('明修', '就是说现在短期啊，其实比如说像长虹、高德跟我们合作，比如说高德会聚焦做导航，然后把操作能力交给我们——那这些呢就是现有的能力直接可以覆盖掉的，而且不用我们自己主动去做，我们更多的是提供一个基模。然后第二层的话就是做一些生物实验，那我们可能要去探索灵巧操作的上限的——因为他会操作透明物体、柔性物体、液体，会涉及到复杂的流程组合，极考验我们的大脑和操作的灵巧性，这是我们亲自会想去做的。那未来的话会探索人不能及的一些任务，比如说在太空上做一些他的科学实验，有些是要太空环境的——那现在基本上没法做，必须要有这个能力在地球上已经做好了，你进入到太空，同步的，那进入到太空之后他面临的是另外一个重力场，他是失重场。')
add_dialogue('Summer', '这个这个有点太……')
add_dialogue('明修', '太大了。')
add_dialogue('Summer', '太大了，我觉得这有点远，我觉得没必要。')
add_dialogue('明修', '就是短、中、长，就三个不同的阶段。')
add_dialogue('Summer', '对对对，你说的长那个，反正特种场景——太空也是特种场景，对。')
add_dialogue('明修', '就做这些场景的目的都是说探索我们的灵巧和智能的上限，最终快速进入到家庭。')
add_dialogue('Anson', '原来呢——我就是我刚才陈明就讲的是什么呢？就是近期我们呢，有我们已经有了一些生合作伙伴了，包括像高德呀、长虹啊这样的，那我们实际上是呢——我说用的跟随这个词总不太好，所以我们换一个。什么意思？他已经有他的场景了，但是我们也一起讨论出一些场景了。那我们就根据这场景铺，我们更多的是基模或者 lessons。然后呢，在现在我们也主动在做的什么呢？就是比如像 AI for sense，我觉得这个场景挺好，它高价值，我们其实也也在铺这个东西。但这个东西呢，可能得需要跟这个场景方一起配合，要做一段时间，有个周期的，我才能让它真正的能够商业化落地和规模化。对。然后当然他讲的那个是叫，他说第三个呢，一二三——第三个他说的是星辰大海，就是说有特别有画面感的，比如说我们将来发射的那些火箭，上面这些东西其实都不用人上去了，对，我们也可以修的——这个呢，你说现在不讲也行，但因为现在毕竟我们在初期嘛哈，但是这个东西是是讲我们愿景，这这也可以。')
add_dialogue('Summer', '明白——其实我觉得一二两部其实挺挺够了。里面合作好。')
add_dialogue('Anson', '2 呢，其实我们很快会有别的，就 AI 复赛的话，除了就是现在比如说我们的有一些这种策——要检测和实验的话，还有一些特种的，特种行业它实际上也是高价值。是是。然后呢，但是呢，以前我们说检修检修，但是实际上检和修两码事——修必须用零销售，检是不用的。就这些东西我们也在探索，但是我现在可以讲的是这个，比如说一些测试这样的话可能会大家觉得我们是有考虑的，就是我们有考虑到到到什么了？第一，近期我们怎么做？我们是是跟生态伙伴一起做，然后呢，同时我们在铺的呢，我们我们非常重视它的价值密度，高价值密度。')
add_dialogue('Summer', '可以——喂，一二，不，星辰大海反而觉得有点远。一二这两个挺务实的讲讲——一更务实，二也是需要去做实验、做 POC 的嘛。')
add_dialogue('明修', '对，这个是直接会有战略协议。')
add_dialogue('Summer', '就会签。')
add_dialogue('明修', '是是是——然后二的话应该在谈。对。对。如果有机会也会拿。')
add_dialogue('Summer', '然后未来可能家庭场景之类都去试。')
add_dialogue('Anson', '我也想问，就是在这种商业化的政策方面，你们对这个部分会有一个什么样的态度？订单。')
add_dialogue('Summer', '我们现在没有啊，都没有——正在等。')
add_dialogue('Anson', '你你你很快就会有了。')
add_dialogue('Summer', '那是我们马上就有了吧？这不是加分吗？')
add_dialogue('田明', '但是要什么类型呢？要多颗粒度，战略协议也 OK。')
add_dialogue('Summer', '就是说实话，你战略协议肯定是订单更有说服力嘛——OK。对啊，但是本身我们是个初创公司。')
add_dialogue('Anson', '它这里边的逻辑是啥呢——我理解一下，第一呢就是说场景需求，我们以说这个我们的伙伴他有这个场景需求，这是第一步。第二步呢，他呢就合作锁定——各种方式的锁定，不管是说他给我们股权上加持、做我们投资人也好，还是我们成一个合合资公司好，还是 MOU 好也好，还是签订一个协议也好——当然这里边的级别不一样，但他他肯定是都是有效的，哪怕是 MOU 也是也是一个，实际上是就是已经锁定、愿意跟我们合作了，再给我们加持了。不认可。啊，认可了。然后那再往下的话，那就是量，有规模化——就是他他的量有多，到底有多大？就是那天你跟我说的，我觉得特别好。比如说我做一个，我我跟他合作，我到底有多大的量？那意味着这个大的到底市场规模是多少？')
add_dialogue('田明', '但这个其实放到第一个。')
add_dialogue('Anson', '哦，对，差不多吧，就是可能是投资人会比较关心的问题——就是到底哪些场景对你有，对你这种有需求，他是想看到需求方的反馈的，是吧？然后而且他还跟你锁定了合作的。不是，我的都不一定对的，他是问你呢，我是只是只讲一下我的理解——我没有资格回答他的问题。')
add_dialogue('Summer', '没有——我我是觉得就刚才那个问题还好，不太关键、不太重要，就是你就在这个屋——你不能跟他陷入到一个就是订单的细节的纠结里面去，你要是陷到这个里面去，我觉得就是没必要——大家，我相信你应该今天没有遇到过跟订单有关的细节问题。')
add_dialogue('田明', '对，不需要的话，接下来比如说 40 亿，是不是就得拿这个东西？')
add_dialogue('Summer', '你先把前面让别人认可，我们才去才有到这个层面。')
add_dialogue('Anson', '对对——你的意思就是说早期的时候，这这讲完了。')
add_dialogue('Summer', '就是在这三轮里面——他业务都没有质的变化。哦哦，对吧？就刚才念的那部分业务都没有质的变化。那那那那——你说的 40 亿的话，如果是真的说要 40 亿，那就是明年。')
add_dialogue('Anson', '那比如说。')
add_dialogue('Summer', '过了半年你得有订单变化。')
add_dialogue('Anson', '比如说到了第三轮的时候，我如果我们发布了一个我们的产品，和我们的拿到了订单，哪个你觉得会更有价值？发布产品。发布产品，是吧？')
add_dialogue('Summer', '对啊，因为订单这玩意就是搞的有的没的的。对吧？讲白了就是大家都能搞。')
add_dialogue('田明', '没有订单也可以融到 40 亿、80 亿。')
add_dialogue('Summer', '有公司能融到——我们领，我们就是当然就奔着这个目标去的嘛，对吧？哈哈哈，对不对？你看那些公司谁发布了产品，谁有订单？')

# --- 第四章：基金生态观察 ---
add_heading('四、基金生态观察与估值参照')

add_dialogue('明修', '许华哲现在站在哪个位置上？')
add_dialogue('Summer', '许华哲现在还偏具成本。')
add_dialogue('明修', '我是说站在多少钱的？')
add_dialogue('Summer', '我这个我还真没、真记不得了，我得问问。')
add_dialogue('明修', '他那 10 亿美金能实现吗？')
add_dialogue('Summer', '10 亿美金——')
add_dialogue('田明', '安宁是拿了什么东西，他能融 100 亿？')
add_dialogue('Summer', 'formal——情绪啊，对吧？你只要情绪到位的话，怎么都有可能性啊。那你看这个量子计算啊，什么太空算力啊，你刚才说太空，对吧？那比这个更宽，对吧？量子算力，那个什么中科天算，对吧？半年时间的话，160 亿了。')
add_dialogue('Anson', '这个不用跟跟随报，应该叫别——嗯，换一个别的词。')
add_dialogue('Summer', '你跟丁丁很熟吗？所以就比较宽。')
add_dialogue('明修', '他很难受，看到他们——哈哈哈，为啥为啥？对呀，就是太熟悉了吧，可能对，看到太熟悉的人过得这么好。')
add_dialogue('Anson', '有一点吧。')

# --- 第五章：技术差异化与首席科学家 ---
add_heading('五、技术差异化与首席科学家/顾问')

add_dialogue('Anson', '当我们讲我们的技术和我技术的范式跟别人的差异性的时候，现在你们觉得还有什么地方讲的不够——有锐度，我指的有锐度就是说让我们差异化会更鲜明。')
add_dialogue('Summer', '其实我们刚刚聊的就是这个。')
add_dialogue('Anson', '啊，对——已经讲了，已经讲了，好 OK，OK，好。')
add_dialogue('Summer', '怎么改这个 BP？OK——对，因为信息太多了。')
add_dialogue('Anson', '还有，然后还有一个是之前我们比较关心的——就是说一个首席科学家对我们来讲是一个特别重要的事情嘛，对我们这个 team。')
add_dialogue('明修', '都还好了——现在还好。我已经从来不讲首席。')
add_dialogue('Anson', '啊，OK。')
add_dialogue('Summer', '有肯定更好，对吧？有肯定。')
add_dialogue('Anson', '那东西我我们感觉，就是梅修好像感。')
add_dialogue('Summer', '顾问怎么样？看什么样类型的顾问——首先看这个顾问参与深度，如果纯挂个名，那我觉得可挂可不挂。如果是参与还可以的。')
add_dialogue('明修', '那我觉得可以放——但是因为我怕的是 BP 漏出去，因为那些顾问需要不能够，那可以讲。')
add_dialogue('Anson', '写明的，是吧？')
add_dialogue('Summer', '到时候讲就行，不放就行——BP 这样就。')
add_dialogue('Anson', '其实明修从过往的咱们最近这段时间的沟通记录来看，没有人问——我们反倒就是一种，就这样。')
add_dialogue('Summer', '因为中国顾问团的顾问很多很少。')
add_dialogue('Anson', '容易漏漏气——就是，明修，我过去这几年我就是评，我不也天天评审这些项目到底能不能进来咱们园区嘛。哎，你越是把自己顾顾问团这写了半天的，中国的。我们又又觉得就不是加分项。')
add_dialogue('Summer', '就这样——不是加分项。')
add_dialogue('Anson', '都有这个问题——所以我觉得还要慎重，甚至没准不是加分项。')

# --- 第六章：收尾与后续行程 ---
add_heading('六、收尾与后续行程')

add_dialogue('明修', '我好像 5、5 点半的时候还有。')
add_dialogue('Anson', '差不多。')
add_dialogue('明修', '苏杭他们现在多少个组？')
add_dialogue('Anson', 'Serena。')

# === 保存 ===
output_path = r'D:\RoboX\02_股权融资\0818 FA波谱资本沟通BP（清理版）.docx'
doc.save(output_path)
print(f'文档已保存：{output_path}')