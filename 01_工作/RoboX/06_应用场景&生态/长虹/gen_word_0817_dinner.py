# -*- coding: utf-8 -*-
"""
08-17 双方团队晚餐 - 清理版Word文档生成脚本
删除所有与业务无关的闲聊，保留实质性业务讨论
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

output_path = r"D:\RoboX\06_产业生态\长虹\08-17 双方团队晚餐（清理版）.docx"

SPEAKER_COLORS = {
    'Anson': RGBColor(0xC0, 0x00, 0x00),    # 深红
    '田明': RGBColor(0x70, 0x30, 0xA0),     # 紫色
    '明修': RGBColor(0x70, 0x30, 0xA0),     # 紫色
    '碧莹': RGBColor(0x00, 0x80, 0x80),     # 青色
    '山相': RGBColor(0x00, 0x33, 0x99),     # 深蓝
    '长虹方': RGBColor(0x80, 0x80, 0x80),   # 灰色（长虹团队发言人）
    '静婷': RGBColor(0x00, 0x80, 0x80),     # 青色
    '团队成员': RGBColor(0x40, 0x40, 0x40),  # 深灰
}

COLOR_HEADING = RGBColor(0x1F, 0x4E, 0x79)
COLOR_NORMAL = RGBColor(0x00, 0x00, 0x00)
COLOR_NOTE = RGBColor(0x80, 0x80, 0x80)
COLOR_SUMMARY = RGBColor(0x2E, 0x5C, 0x8A)

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

style = doc.styles['Normal']
font = style.font
font.name = '微软雅黑'
font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
pf = style.paragraph_format
pf.space_after = Pt(6)
pf.line_spacing = 1.5


def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = COLOR_HEADING
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(12)
    p.paragraph_format.space_before = Pt(6)


def add_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = COLOR_HEADING
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '1F4E79')
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_dialogue(speaker, text):
    p = doc.add_paragraph()
    run_s = p.add_run(f'【{speaker}】')
    run_s.font.bold = True
    run_s.font.size = Pt(11)
    run_s.font.color.rgb = SPEAKER_COLORS.get(speaker, COLOR_NORMAL)
    run_s.font.name = '微软雅黑'
    run_s.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run_t = p.add_run(text)
    run_t.font.size = Pt(11)
    run_t.font.color.rgb = COLOR_NORMAL
    run_t.font.name = '微软雅黑'
    run_t.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.5


def add_note(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = COLOR_NOTE
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(1)


def add_summary_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = COLOR_SUMMARY
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'double')
    bottom.set(qn('w:sz'), '8')
    bottom.set(qn('w:space'), '2')
    bottom.set(qn('w:color'), '2E5C8A')
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_summary_item(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.color.rgb = COLOR_NORMAL
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Cm(0.5)


# ========== 文档内容 ==========

add_title('08-17 双方团队晚餐')

add_note('参会人：Anson、田明、明修、碧莹、山相、长虹方团队')
add_note('时间：2026年8月17日晚，时长约2小时53分钟')
add_note('说明：已删除所有与业务无关的闲聊（菜品/喝酒/家乡/个人经历等），仅保留实质性业务讨论')
add_note('会议分两部分：前半部分为双方团队晚餐交流，后半部分为ROBOX内部战略讨论')

# ========== 关键要点总结 ==========

add_summary_heading('会议关键要点总结')

add_summary_item(
    '1. 长虹机器人公司将于9月15日独立为独立法人实体（长虹机器人），目前挂在集团下模拟核算。长虹7人硬件团队可全力保障ROBOX合作。'
)
add_summary_item(
    '2. 长虹场景布局：太空舱已向省领导汇报并获认可，找场地推进；机器人商业化训练场已在杭州/成都布局；机器人产品大赛4月已举办第一届。'
)
add_summary_item(
    '3. 数据采集合作模式：长虹可做甲方提供商业化场景+数据回流，ROBOX提供大脑服务+标注处理。双方一起合作赚第三方（政府/品牌方）的钱。'
)
add_summary_item(
    '4. 生物制药实验室场景：长虹方有客户需求（检验师人工贵），ROBOX本周将跟生物制药集团董事长谈合作。核机器人（人造太阳/强磁环境）也有应用前景。'
)
add_summary_item(
    '5. 阿里退出具身智能方向：因千问在办公agent上与字节腾讯竞争激烈，且不具备硬件基因，决定不做。但前期投入巨大（算力不计成本投入），ROBOX团队受益于这些积累。'
)
add_summary_item(
    '6. 融资进展：第一轮20亿估值确认，蚂蚁战投感兴趣（可能加开一轮22-23亿），阿里战投在与Wuma沟通中。目标本轮拿到8-10亿，支撑24个月。宇树上市后市场情绪可能回调，需在此之前close。'
)
add_summary_item(
    '7. 下一轮融资规划：可能同时开三轮（40/50/60亿），中金已在接洽。每周聊5-8家投资人，20亿窗口1-2周内关闭。跟投方2000万规模，主投5000-8000万。'
)
add_summary_item(
    '8. 商业化四阶段路线图：①短程操作（高德四足狗）→ ②长程任务（太空舱限制餐饮）→ ③灵巧操作（科学实验场景）→ ④移动交互+操作融合（远期家庭）。'
)
add_summary_item(
    '9. AI for Science是远期蓝海：国家六大未来产业中具身智能、AI for Science、商业航天三个相关。生物制药实验室是中间路径——不承重、无节拍要求、人机分离。'
)
add_summary_item(
    '10. FA三个关键问题需回答：①技术差异化（自进化闭环如何实现）②竞争对标（长期对标特斯拉，中短期参考华为智驾）③商业化模式（卖什么、国内vs海外）。'
)
add_summary_item(
    '11. 开源策略（新提出）：封闭System 2（核心壁垒）+ 完全开放System 1（横扫所有人），System 1开箱即用可接System 2，也可自行post training。类比DeepSeek/千问的开源策略。'
)
add_summary_item(
    '12. 商业模式三种路径讨论：①卖手眼脑增量套件给本体厂商（客户=本体厂商）②直接面向场景方（本体=供应商/合作伙伴）③联合本体厂商面向客户。团队倾向不锁死单一模式，但投资人会质疑创业公司能否同时支持多种模式。'
)
add_summary_item(
    '13. 商业壁垒三个方向：客户锁定（差异化体验）、极致成本优势、利基市场市占率。核心定价权锚定在模型智能领先性和稀缺性上。'
)
add_summary_item(
    '14. 竞争对手分析任务分配：需深入研究元策未来、逆矩阵、微播AI等几家技术策略差异。可通过公开信息整合+专家访谈获取。Figure是否在做模型需确认（顶辉投了Figure）。'
)
add_summary_item(
    '15. 后续安排：周三去广州长虹→周四飞北京；明天（8/18）长虹8人来对接；FA（心流/波普）周三来谈方案；PPT讨论约下周二早上。'
)

# ========== 正文 ==========

# ============================
add_heading('一、长虹机器人独立化与团队情况')
# ============================

add_dialogue('长虹方', '新公司应该9月份到位，9月15号准备独立法人，变成长虹机器人。名字具体还没取好，单独独立处理，现在相当于挂在集团下面的一个模拟核算的公司。')

add_dialogue('田明', '他们这次来8个人，就是为了把各方向的人直接现场对接。硬件那边大概有7个人的团队，还是挺专业的。你主要出方案、出标准，碰到硬件问题他再问你。')

add_dialogue('长虹方', '张磊那边最近把市面上该测的都测了一遍，各种型号、各种品牌、各种路线都测了。但他们可是要真真实实的、不赚钱的，就是为了知道当前到底是什么态势，采集出来是什么样的东西。')

# ============================
add_heading('二、长虹场景布局与太空舱')
# ============================

add_dialogue('长虹方', '今年4月份我们搞了一个全国地区的机器人大赛产品大赛，大家感觉比较初级。你得把商业和灵动的体验一起追求。虽然机器人没有真正进入场景，但总得让大家看看以后机器人进入场景之后是什么样子。')

add_dialogue('长虹方', '我们从四五月份开始在杭州的机器人中心基地上面的厂房，成都的萝卜家、萝卜城市，做一些机器人的商业化布局。训练场的成果外放，让大家感受机器人服务，比如买咖啡、零售。')

add_dialogue('长虹方', '太空舱已经跟省领导汇报了，省领导完全OK，找一个地方想推我们做。好多场景都可以放。')

add_dialogue('田明', '太空舱他们自己就想做，已经立了军令状。他们那边做素材、demo、硬件。')

add_dialogue('碧莹', '所以就牵引吧，让他们说太空舱需要这样的定制。')

# ============================
add_heading('三、数据采集与商业合作模式')
# ============================

add_dialogue('长虹方', '我们其实可以作为甲方，直接提供商业化场景。你们采集的数据、评测结果可以回流给我们领导。你们是做大脑的，有核心服务，只需要标注怎么处理。场景方面，我们要一起合作去赚第三方的钱。')

add_dialogue('田明', '比如说机器人要做奶茶，我们都不做奶茶，别人怕出事。但他改造供应链，根据现在搞的产业分工。真正做产业分工的，可以找新宝等厂商一起。')

add_dialogue('长虹方', '我们希望精准对接，量身定制，包括中期评测。数据很大，我们专门有素材基地，配合做数据采集和长期训练。')

# ============================
add_heading('四、生物制药实验室场景')
# ============================

add_dialogue('长虹方', '训练场里面有个零下86度的生物冰箱，放卷帘的。现在领导有新的诉求。')

add_dialogue('田明', '绵阳的市委书记说来找我们。')

add_dialogue('Anson', '生物医药这个方向也可以放到我们合作里面。')

add_dialogue('长虹方', '我们初步接触了一下，发现他们有需求。他们之前苦恼的是模型能力不行，看过好多手了，但没有一个拿出解决方案。他们的试剂并不贵，贵的是人工——这些操作都得有检验师。')

add_dialogue('田明', '这种实验室多机系统，将来是一个核心需求。强磁环境、辐射环境的废渣处理，比普通环境稍微好一点。')

add_dialogue('山相', '我最早就做核机器人，人造太阳的那个轴。轴瓦如果掉了，谁也不敢去，必须造一个蛇一样的大机械臂开进去，末端装双臂遥操作。哈工大就做那个蛇臂。当时是国际伊特尔项目，中国在合肥等离子所1:1复刻了小型人造太阳，拉动各个环节。')

# ============================
add_heading('五、阿里退出具身智能方向')
# ============================

add_dialogue('Anson', '上个月阿里宣布不做具身智能方向了。因为千问在办公agent上跟字节腾讯竞争太激烈，所有资源都往那里投。而且阿里没有做硬件的基因，软硬结合不是强项，所以决定不做。')

add_dialogue('Anson', '好处是过去两年投入很大，该踩的坑也踩了很多。阿里云的算力不计成本地往里扔，把整个技术链路整出来了。现在核心算法都有了，机械臂、灵巧手两周前已到货开始训练。')

add_dialogue('Anson', '字节、阿里、腾讯这三家每年都是上千亿往里投。腾讯起步比较晚但速度极快，字节更猛。钉钉总部斜对面就是字节总部，两栋楼针锋相对。')

# ============================
add_heading('六、园区AI生态与产业资源')
# ============================

add_dialogue('Anson', '这个园区已经有将近8000平米都填满了，全是AI native企业和FDE企业。我们在杭州、武汉也做了，但发现效果没有杭州好。杭州确实是AI创业氛围目前在国内最好的，深圳我们也有，但杭州最好。')

add_dialogue('Anson', '本来我们在成都也想做，但成都高新区那边的楼基本上阿里云就用完了，没有空间。')

add_dialogue('Anson', '绵阳的市委书记说来找我们，我们可以多聊一聊。')

# ============================
add_heading('七、后续行程安排')
# ============================

add_dialogue('田明', '周三去广州长虹，周四飞北京。南航2点半的飞机，4点到。')

add_dialogue('Anson', '我和明修我们仨明天去广州，后天去广州。你给我一个我们要弄清楚什么事情的清单。')

add_dialogue('田明', 'PPT我们约下周二早上，early bird合适的时间。')

# ============================
add_heading('八、融资进展与规划（内部会议）')
# ============================

add_dialogue('田明', '上周我们也跟蚂蚁战投聊了，蚂蚁对我们非常感兴趣。第一轮按20亿估值没有问题，所有资方都在这个基础上往后看后续轮次。蚂蚁内部走完流程至少一个月，他们提出第一轮20亿可以先close掉，中间加开一轮22-23亿，他们可以team进来。')

add_dialogue('田明', '阿里战投这边在跟Wuma的核心团队沟通，已经做了一轮沟通，接下来要线下详细对一下。阿里战投会全力配合。')

add_dialogue('田明', '远景资本觉得项目没问题，但觉得贵。种子轮20亿在国内几乎绝无仅有，银通通用最早从5亿开始，智谱也是。但整体投资人都认可我们这个初创团队从20亿起步没有问题。')

add_dialogue('田明', '鼎辉这样的大PE也准备了8000万进来。主投5000-8000万，跟投一般2000万规模。第一个2个亿是非常确定的。接下来6个月最核心的事就是围绕融资展开。')

add_dialogue('田明', '宇树上周准备上市认购了，冲一波高以后会回调，市场情绪传导到一级市场后大家会进入谨慎状态。在这个之前我们希望拿到8-10亿资金，足够支撑未来24个月。')

add_dialogue('田明', '下一轮从20亿变成40亿，投资人会问跟20亿有什么区别。我们可能同时开三轮——40亿、50亿、60亿同时准备。中金已经在接洽，后续会进来。我们现在每周聊5-8家投资人。')

add_dialogue('田明', '融资有两个约束条件：第一是大家出来的时间，如果没完全出来投资人会有顾虑；第二是能不能拿到阿里的投资，有了阿里投资就不是20亿了，直接30亿起步。其他资方也在看阿里的态度来降低风险。')

# ============================
add_heading('九、长虹战略合作定位')
# ============================

add_dialogue('田明', '长虹集团见过董事长，省领导也很重视。他们有政府政策支持、大产业场景、硬件量产一致性能力、系统工程能力，全方位跟我们合作，是最合适的第一个战略合作伙伴。')

add_dialogue('田明', '核心场景是围绕进家庭服务的第一条线，倒推商业服务——太空舱里做限制餐饮、分配食品。他们已经明确准备好场地了，比如熊猫基地、四川文旅景区都可以放。')

add_dialogue('田明', '他们做系统集成、交付、维护，我们主要提供标准化能力——智能大脑服务。更进一步，硬件协同可以搞一个标品。后训练平台仍然是需要的，他们的算法可以在上面做场景微调。')

add_dialogue('明修', '在我长期的故事里，我是手眼脑协同的增量部件，加上一个后训练平台，这是基础产品。')

add_dialogue('碧莹', '这个后训练东西前期一直没有提到。')

add_dialogue('田明', '之前对外也有提过，可能没有真正同步。不过不着急，至少几个月时间都有。投资人也不会因为这个平台有无而决定很大估值影响。')

# ============================
add_heading('十、商业化四阶段路线图')
# ============================

add_dialogue('田明', '商业链路分四个阶段：第一阶段做相对短程的具体操作类动作，比如在高德四足狗上做一些任务。第二阶段把长程任务能力发展起来，在太空舱里连续完成限制参与的任务。第三阶段加入灵巧性的部分，在科学实验场景里做。第四阶段把更好的移动交互跟操作能力融合起来，做远期场景。')

add_dialogue('田明', '这是围绕技术成熟度和需求容错性在四大阶段里拉通的。')

# ============================
add_heading('十一、AI for Science与远期市场')
# ============================

add_dialogue('田明', '第二条链路：我们跟很多投资人聊，觉得很大的增量市场或蓝海机会，会发生在AI for Science和商业航天联动的市场。国家六大未来产业中，具身智能、AI for Science、商业航天三个相关。')

add_dialogue('田明', '大的未来趋势是AI驱动的research，物理世界的实验由机器人7×24规模化执行，空间想象力巨大。对应到中间路径，是生物制药公司的实验室——能很好把灵巧复杂操作用上，不承重、对节拍没有高要求、人机分离安全性可考虑。')

add_dialogue('田明', '这周我和Anson、明修会去跟大的生物制药集团董事长谈合作，他们很想做机器人的自动化智能化。包括高德这边，明修跟高德CEO已经形成沟通合作，后续高德相关的操作能力都可以用我们的部分。')

# ============================
add_heading('十二、FA关键问题：技术差异化')
# ============================

add_dialogue('田明', '我们找了FA——心流和波普，明天会带着方案来聊。FA有几个关键问题希望我们回答。')

add_dialogue('田明', '第一个是差异化。投资人现在听起来就是"基于手眼脑协同的自进化闭环"。技术上究竟怎么实现？自进化怎么做？为什么手眼脑协同对将来做具身智能效率最高、效果最好？故事怎么圆回来能够自洽？')

add_dialogue('田明', '头部投资人会看非常细。昨天跟一家资深投资人聊，他第一个要求就是把所有paper发给他研读。他们会下沉到paper具体环节，看我们跟元策未来、智航等团队的区别。')

add_dialogue('田明', '数据闭环很重要——在哪些feature上能做出差异化，比行业平均水平高？怎么证明模型服务、算力能力、inference部分能提供保障？手眼脑协同里，眼睛跟手怎么定义？怎么配合大脑服务？')

add_dialogue('田明', '两个关键feature：第一是System 2里打long horizon的长上下文，因为将来机器人要长持续在线，长上下文和in-context learning越来越靠谱；第二是灵巧操作加入触觉，技能比别人最丰富。把这两个feature占住，类似在数字AI里定义coding这种关键feature。')

add_dialogue('明修', '我感觉还不够，因为有其他公司也在做类似的事，没有明显差异。你很难保证没有直接竞争对手。')

add_dialogue('田明', '你要证明在同样的细分市场或技术路线的竞争对手里，你是number one。不光是研发insight，还包括执行效率和实现优化，要正面竞争。')

# ============================
add_heading('十三、FA关键问题：竞争对标')
# ============================

add_dialogue('田明', '第二个问题是对标。早期技术有不确定性，要找长期参考对象让投资人知道上限在哪。是不是对标特斯拉？还是对标华为智驾？还是对标π这样的公司？这直接倒推出公司未来上限。')

add_dialogue('田明', '长期对标特斯拉，中短期落地形式参考华为智驾。我本来很多人会觉得我们在对标Figure，但Figure是不是没有在做模型？')

add_dialogue('明修', '静婷你有没有准确反馈？Figure是不是没在做模型？')

add_dialogue('静婷', '顶辉投了Figure，但不代表我们知道他内部是否在做模型。可以问一下。')

add_dialogue('田明', '现在看到很多密矩阵、Libra AI等世界模型公司，我们重点又不讲这个。投资人会问你们是不是觉得世界模型公司都有问题，问题在哪？')

add_dialogue('田明', '竞争对手技术策略分析任务：元策未来、逆矩阵、微播AI等几家需要深入研究。可以先做公开信息整合，也可以通过专家访谈获取。先把能公开获取的信息源做一次整合。')

# ============================
add_heading('十四、FA关键问题：商业化模式')
# ============================

add_dialogue('田明', '第三个问题是商业化。我们不再是研究院，不是大厂里的成本中心，要考虑技术如何转化成商业价值。核心是：第一卖什么？卖不卖硬件？还是主要卖智能？第二国内和国外市场怎么区分？')

add_dialogue('田明', '国内主要做最佳实践案例的试验场。海外要有渠道，能触及哪些市场，用什么商业模式符合当地人需求。')

add_dialogue('田明', '海外肯定要OEM整机，因为海外没有很强的系统工程和硬件优势。国内做试验场，退一步做标准化的智能增量套件，结合合作方做系统集成和硬件，打最佳实践案例，然后向海外复制。')

add_dialogue('田明', '中东很多是大客户，做项目定制交付，不喜欢买断。泰国那些地方可以找泰国电信等代理商规模化触达，可以承诺销售额。')

add_dialogue('Anson', '为什么现阶段要讨论海外？')

add_dialogue('田明', '投资人已经开始提，出海怎么做。从大叙事上讲，将来商业化规模更多在海外出现。比如维达动力跟日本已经在确定订单了。投资人要的就是先想清楚海外是什么样，有没有策略和讲法。')

add_dialogue('Anson', '核心是先回答清楚国内怎么把商业化路径跑通，再去做海外。本质是国内的试验场做好后再复制。')

add_dialogue('田明', '对，国内是试验场，先写国内部分。但投资人day one就开始考虑海内外差异。最快能落地的肯定是海外，同样能力下海外比国内快。')

# ============================
add_heading('十五、商业模式选择讨论')
# ============================

add_dialogue('Anson', '当我们决定国内卖手眼脑增量套件时，客户就变成本体厂商了。除了这种选择，我们还可以作为总包方把硬件作为合作方，一起给场景方提供服务（项目制）；也可以跟硬件合作研发，一起面对客户。这是很慎重的决定。')

add_dialogue('田明', '如果聚焦项目定制总包，人力投入、工程化能力和交付能力要求更高，包括售后成本会长期拖住你，可能18个月才能交付。后期追求智能上线时会被拖住。')

add_dialogue('Anson', '可以不当总包，但一般总包的都是优质客户。如果是10亿订单的优质客户，我肯定自己做不会找你买。所以可以拉着庞总做。'

)

add_dialogue('田明', '我们不一定马上只选一种，可以说两到三种盈利模式。不同情况下我去跟本体厂商合作——他可以是客户；在什么情况下场景方是客户，我们拉着本体甚至本体变成供应商。像跟长虹、云康就是这种模式。别锁死客户就是本体厂商。')

add_dialogue('田明', '创业公司不做什么很重要。投资人会问你们不做什么。参考海康研究院AI摄像机的发展：凡是有规模、能标准化的，一定垂直做，整机规模成本更低；中长尾部分能力开放出来，拉合作伙伴做。两种模式。')

add_dialogue('田明', '现阶段不存在这么多种合作形式，太多了，人少，瞬间没有勇气自己垂直做交付。')

add_dialogue('Anson', '大客户是大的节点，需要大的产品生命周期甚至定制。但小的细的节点，每个路径中间都有很多不同客户需要接触。用户教育需要提前做，小场景需要让人感知。开发到交付中间每个节点的训练目标都可以找到对应的客户。这些细碎客户也是需要考虑的。')

# ============================
add_heading('十六、商业壁垒构建')
# ============================

add_dialogue('Anson', '形成商业产品时，壁垒在什么地方？不光是产品优秀不优秀的问题。')

add_dialogue('田明', '我们压住几点：第一，模型和服务的领先性和稀缺性；第二，手眼脑协同的硬件是围绕模型大脑所需结构反向由智能驱动定义的，本身就是在卖一种事实标准——脑生态，将来大家都用你的标准，定义权在你手上。')

add_dialogue('Anson', '这可能是技术壁垒，不是商业壁垒。技术壁垒没有完全的壁垒，第二家可能做得没那么好但价格便宜就能抢市场。成熟市场之前肯定要有商业规范和商业壁垒。可以通过平台化方式让更多商家厂家一起玩，制定市场规则。')

add_dialogue('田明', '商业壁垒一般三个方向：第一是客户锁定——差异化feature让客户觉得体验最好；第二是极致成本优势——规模+系统性优化，能不能卖得更便宜；第三是利基市场市占率——吃住某一个市场成为绝对领先者。我们要选择一个到两个方向集中资源。')

add_dialogue('田明', '参考大模型发展：只有DeepSeek在走极致性价比，是后来者。所有人都在卷智能上线，每个人轮流半个月。要么在coding场景是number one，要么在agent场景是number one，通过相对差异化形成客户锁定。')

add_dialogue('Anson', '比如只用灵巧手操作冰箱这个场景，所有冰箱厂商推出产品时都要适配我们这个标准，类似苹果App Store的概念。要成为规则制定者，手上要有定价权。有定价权一定有全产业链最稀缺的东西——我们认为是模型智能。')

add_dialogue('田明', '更好的智能决定了稀缺性，决定了定价权，决定了别人按我们方向形成标准，过程中有更多利益相关者构建起来。')

# ============================
add_heading('十七、开源策略：封闭System 2 + 开放System 1')
# ============================

add_dialogue('田明', '心流那边认为开源故事可以继续讲。现在整个具身智能开源里面没有讲得特别好的，达摩院一直在讲开源。他认为应该是封闭的System 2加上完全开放的System 1。')

add_dialogue('田明', '封闭的System 2是我们的核心壁垒。你必须要接我们开源的System 1，拿开放的System 1去横扫别人——用我这个东西，简单微调就能完成各种任务。System 1接System 2开箱即用，也可以拿去post training做成你自己要的。但我不会把System 2给你开出来。')

add_dialogue('明修', '为什么所有人都在用π？我们可能也要对标有这么一个基模出来。用这个VLA去把那些不如开源的模型全部干掉，集中度上升，把下限拉上来。')

add_dialogue('田明', 'π为什么大家会用？一是性能好，二是它一开始的主张就是"我就是要做开源"。时间窗口期6-12个月，能不能通过这样的模型快速吸收一批开发者。')

# ============================
add_heading('十八、竞争对手分析任务分配')
# ============================

add_dialogue('田明', '竞争对手技术策略分析需要深入研究几家：元策未来、逆矩阵、微播AI等。蚂蚁灵波算研究清了就不用写了。先把能公开获取的信息源做一次整合，看一下有什么问题。也可以通过专家访谈获取，匿名的就行。')

add_dialogue('田明', '技术同学在不同公司里的一些人脉也可以用上，比如在GitHub等技术框架图里可以找到线索。')

add_dialogue('田明', '明天跟长虹开会的时候也可以提一下，我们想知道他们那边了解的竞争对手情况。')

# 保存
doc.save(output_path)
print(f"已生成: {output_path}")
