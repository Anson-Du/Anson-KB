# -*- coding: utf-8 -*-
"""生成0824 Anson与天溯检测两段交流合并清理版Word文档"""
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

OUT = r'D:\RoboX\04_听记纪要\转写与纪要\0824 Anson与天溯检测行业自动化合作探讨（清理版）.docx'

doc = Document()

# ---- Page setup ----
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

# ---- Default font ----
style = doc.styles['Normal']
font = style.font
font.name = '微软雅黑'
font.size = Pt(11)
font.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
pf = style.paragraph_format
pf.space_after = Pt(4)
pf.line_spacing = 1.5

SPEAKER_COLORS = {
    'Anson': RGBColor(0x00, 0x66, 0xB0),
    '李德健': RGBColor(0xC0, 0x00, 0x00),
}

def _set_font(run, name='微软雅黑', size=11, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.element.rPr.rFonts.set(qn('w:eastAsia'), name)
    if color:
        run.font.color.rgb = color

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pf = p.paragraph_format
    pf.space_before = Pt(20)
    pf.space_after = Pt(10)
    r = p.add_run(text)
    _set_font(r, size=16, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))

def add_meta(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text)
    _set_font(r, size=10, color=RGBColor(0x80, 0x80, 0x80))
    r.italic = True

def add_part_heading(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    _set_font(r, size=14, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))
    # bottom border
    pPr = p._element.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '6',
        qn('w:space'): '4', qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_chapter(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run(title)
    _set_font(r, size=13, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))
    pPr = p._element.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '4',
        qn('w:space'): '3', qn('w:color'): 'B0B0B0'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_speaker_line(speaker, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.5)
    color = SPEAKER_COLORS.get(speaker, RGBColor(0x00, 0x00, 0x00))
    r1 = p.add_run(speaker + '：')
    _set_font(r1, size=11, bold=True, color=color)
    r2 = p.add_run(text)
    _set_font(r2, size=11, color=RGBColor(0x33, 0x33, 0x33))

def add_note(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(0.5)
    r = p.add_run(text)
    _set_font(r, size=10, color=RGBColor(0x80, 0x80, 0x80))
    r.italic = True

def add_summary_group(title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(title)
    _set_font(r, size=11, bold=True, color=RGBColor(0x1F, 0x4E, 0x79))

def add_summary_point(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.left_indent = Cm(0.8)
    r = p.add_run('• ' + text)
    _set_font(r, size=11, color=RGBColor(0x33, 0x33, 0x33))

# =====================================================================
# DOCUMENT CONTENT
# =====================================================================

add_title('Anson与天溯检测行业自动化合作探讨')
add_meta('时间：2026年8月24日')
add_meta('地点：天溯检测实验室（广州）')
add_meta('参会人：Anson、李德健')

add_note('说明：本文档合并两段交流转写（上午约1小时8分钟 + 下午约20分钟），原始转写质量较差，已进行重度清理与语义重构。发言人"李德健"为天溯检测团队成员。')

# ---- Summary ----
add_part_heading('沟通总结')

add_summary_group('一、天溯检测背景与能力')
add_summary_point('天溯检测为上市公司，主营新能源电池/储能检测，近期拓展车联网、机器人、物联网安全检测，与政府合资成立子公司运营安全实验室。')
add_summary_point('李德健此前主导开发无纸化测试软件平台，实现检测设备远程监控与无人值守，95%以上工作线上完成，已具备数字化基础。')
add_summary_point('天溯与哈工大联合提交具身智能安全课题（三部分：大脑安全研究、运行延迟监控、固件安全），承接其中两部分。')
add_summary_point('天溯发现了运输机器人的高危漏洞，正在研究机器人防火墙概念——对机器人运行进行安全监控、异常流量预警与上报。')

add_summary_group('二、检测行业自动化需求')
add_summary_point('检测行业三大自动化环节：①样品接收/仓储搬运（夹爪即可，不需灵巧操作）②样品拆包/贴标/功能调试/拆解（需灵巧操作）③检测执行与过程审查（可AI自动化合规审查）。')
add_summary_point('场景选择共识：实验室环境固定、结构化程度高、场地价值高（大场地2000元/小时 vs 小场地300元/小时），优于非结构化场景，是早期落地的最佳选择。')
add_summary_point('高价值机器人应用场景：接线/插拔测试、温度传感器粘贴（502胶）、充电测试操作（插电/开机/设参/APP操控）、样品拆解——固定场景+重复操作+人工效率低。')
add_summary_point('第三方检测市场规模：全国5700亿/年（电子电器类约800亿），12000+家有资质实验室，20+上市公司，民营企业仅3-4家。')

add_summary_group('三、ROBOX（睦灵科技）技术底座')
add_summary_point('System 2/1/0三层同源架构：System 0解决闭环物理稳定（小脑功能），System 1实现灵巧操作（端侧），System 2负责自主推理与长程任务进化。三层同源是核心难点，目前全球仅少数团队实现。')
add_summary_point('122B千亿参数，国内唯一达到千亿参数的具身智能公司；在英伟达官方报告中全球排名前三，领先约3-5个月。')
add_summary_point('跨本体操作能力：模型可驱动不同本体和末端执行器；异构数据训练（不同手+躯干+臂分别训练）反而提升模型泛化速度。')
add_summary_point('触觉世界模型（TacWM）：可实现无视觉条件下基于触觉旋转苹果、煎牛排（视觉+触觉+时间三因子判断熟度）等灵巧操作。')
add_summary_point('融资情况：第一轮投后估值约20亿元（即将关闭），第二轮目标估值约40亿元。')

add_summary_group('四、合作意向与后续行动')
add_summary_point('李德健本周拍摄测试场景视频（含EMC暗室、接线、温度粘贴等），供睦灵科技算法团队评估场景适配性与研发周期。')
add_summary_point('双方讨论MOU意向（无法律约束力的合作意向），李德健愿意推动公司层面建立持续交流关系。')
add_summary_point('李德健引荐集成方案公司"东昇射频"（星汇智云集团旗下，曾为天溯开发测试软件平台），作为实验室自动化集成方面的潜在合作方。')
add_summary_point('黑灯实验室概念：数字化→智能化→机器人应用三步走，工业自动化+灵巧智能结合可实现端到端无人实验室运营。')

# =====================================================================
# PART 1 - First session (~1hr 8min)
# =====================================================================
add_part_heading('第一部分：具身智能技术与检测行业自动化合作探讨')
add_meta('时长：约1小时8分钟')

# --- Chapter 1 ---
add_chapter('一、开场与双方背景介绍')
add_speaker_line('李德健', '我加入天溯只有几个月，之前在另一家检测机构工作了十年，后来在别的单位，现在又回来了。')
add_speaker_line('Anson', '您之前在哪家检测公司？')
add_speaker_line('李德健', '我已经在这个行业待了十年，这是第二次来这里。')
add_speaker_line('Anson', '这家公司去年年底刚上市。我上个月刚从阿里离职，团队成立了一个新公司——睦灵科技，目前正处于融资阶段。')
add_speaker_line('李德健', '我似乎听说过。')
add_speaker_line('Anson', '你们肯定没听说过，因为上周才对外公开。6月份成立后一直没有启用这个名称。主要是因为阿里决定不再做具身智能，因此整个团队大约二三十人，核心团队都做模型和算法，成建制地出来了。')
add_speaker_line('Anson', '阿里没有具身智能的基因有两个原因。第一，阿里是淘宝起家，硬件不是我们的长项，我们与华为、海康不是同一个领域。第二，具身智能对模型和算法的要求比大语言模型高出几个数量级。目前阿里面临的竞争非常激烈，在千问的基础模型和通义等AI产品上，已经和腾讯、字节进入白热化竞争，每年至少2000亿元的投入，没有资金再做具身智能。')
add_speaker_line('Anson', '所谓"有钱"不能只看账面现金，还要看接下来要做什么。每年为了芯片、千问的基础模型和AI产品的投入都是千亿级别，加上淘宝补贴也要大几百亿。')
add_speaker_line('李德健', '放弃这条路线也会有很大损失。')
add_speaker_line('Anson', '我们投资过一些机器人本体公司，发现它们仍处于玩具阶段。首先没有大脑，其次没有手，这条路需要很长时间。宇树上市之后近两天跌了2000多亿，起点太高。为什么？因为大家都知道这是一家玩具公司，只会翻跟头和跳舞，实际上大脑是零。')

# --- Chapter 2 ---
add_chapter('二、天溯的实验室自动化平台经验')
add_speaker_line('李德健', '例如企业管理系统、ERP、实验室LIMS系统，这些我之前都做过。我们基于这个方向进行所有数据管理，一旦所有内容都能线上化，就可以将线下硬件人员的操作都放到线上，然后再引入机器人进行控制。')
add_speaker_line('Anson', '这是两件事——一件是信息化/数字化问题，另一件是灵巧智能问题。')
add_speaker_line('李德健', '当时操作这部分基本已做得比较成熟。我把所有软件、测试软件和设备全部关联起来，实现远程监控。底层是一个大数据池，上面是AI驱动系统。我们之前做的工作相当于将国内外采购的仪器都配备测试软件——寻找实验室将测试软件直接对接，开发测试软件平替原有系统。每个设备绑定测试软件并集成到平台中。')
add_speaker_line('李德健', '平台生成检测计划后推送到每个测试软件，实现无纸化。你只需识别测试计划并执行即可。任务从平台下发到每个软件，每个项目的运行情况都在平台里汇总。95%以上的工作都在线上完成，还有无人值守功能。')
add_speaker_line('Anson', '这是你几年前做的？')
add_speaker_line('李德健', '是的。但他们的想法可能不够超前，所以一直停留在基础层面。')
add_speaker_line('Anson', '这是天溯做的吗？')
add_speaker_line('李德健', '不是，我之前的想法是寻找老板投资。后来我们已经完成了这些工作，就直接跳转到机器人领域。')

# --- Chapter 3 ---
add_chapter('三、检测行业三大自动化环节')
add_speaker_line('李德健', '实验室分为各个环节：样品的接收、验收、登记、入库、搬运，从A点到B点，甚至包括文件管理、样品调试等。')
add_speaker_line('Anson', '这个文件是指纸质文件还是电子化文件？')
add_speaker_line('李德健', '电子化文件不需要，但实际场景中仍然需要一些纸质文件。检测机构每年会有很多评审老师来检查，他们只看纸质报告和文件，检查时需要准备大量评审材料。')
add_speaker_line('Anson', '大家会习惯这种方式吗？这部分后期会逐渐减少。')
add_speaker_line('李德健', '仓储机器人和样品调试机器人——我接收到一个样品后，需要验证它是否能正常充电、功能是否正常，之后才进入测试阶段。如果功能不正常就无法测试。接收样品后会进行入库登记或搬运。')
add_speaker_line('Anson', '我理解为这一环节不需要灵巧操作，只需要搬运。例如末端执行器可能不是手，而是夹爪。')
add_speaker_line('李德健', '如果要求较高，还会有样品的包装拆解。需要对样品拍照，了解接收状态和配件。配件需要贴标签，连接打印机。虽然搬运不需要灵巧手，但样品识别和标签粘贴是必要的。')
add_speaker_line('李德健', '样品接收、识别、调试和拆解都有实验室需求。无论是化学食品还是药品，最终都需要将样品分解。例如做完测试后需要拆开产品，拍摄内部照片确认测试的产品是否正确。')
add_speaker_line('Anson', '这非常有趣——无论是拆解包装还是拆解电子产品，都需要灵巧操作。')
add_speaker_line('李德健', '从实验室角度来看，如果要建立完全无人的实验站，大脑部分仍需有人监督，其他部分基本不需要人。其他方面还包括供电网络、设备监控、仪器状态监控、机器人测试监督、项目审查、仓储样品检测执行等。')
add_speaker_line('Anson', '因为它可以提供所有视觉监控，所以不需要人监督。')
add_speaker_line('李德健', '一个依靠视觉，另一个依靠仪器。端口接到平台后随时可以抓取运行状态、温度、运行时长等数据。')
add_speaker_line('Anson', '你刚才提到了三个方面：仓储机器人、样品调试机器人、检测执行机器人——这三个环节最需要灵巧手。')
add_speaker_line('李德健', '样品功能调试完成后反馈给我们，我们再进行样品拆解和管理。')
add_speaker_line('Anson', '检测项目审查和过程优化呢？')
add_speaker_line('李德健', '优化基本不需要了，现在平台都用AI。申请表和检测信息已经录入，对应的检测标准也已录入，基本上一键审查合规。')

# --- Chapter 4 ---
add_chapter('四、实验室场景的结构化优势')
add_speaker_line('Anson', '李总提到这三个环节后有一个重要观点：你认为实验室大场地比非结构化场景更合适。有几个原因——第一，实验室场地相对固定，不需要太多移动；第二，价值更高。')
add_speaker_line('李德健', '可以作为第一个典型场景进行实验，场地和尺寸位置基本固定。')
add_speaker_line('Anson', '环境更加结构化，不像非结构化场景那样不可控。')
add_speaker_line('李德健', '目前非结构化场景的价值相对较低。例如楼下小场地客户测试每小时收费300元，而大场地是2000元一小时。')
add_speaker_line('Anson', '固定场景、重复且价值高的场景最合适。早期需要半结构化环境，非结构化场景并不友好。')

# --- Chapter 5 ---
add_chapter('五、ROBOX（睦灵科技）技术体系介绍')
add_speaker_line('李德健', '你们灵巧手使用的是通讯协议吗？我想了解灵巧手从硬件端口上的情况。')
add_speaker_line('Anson', '我稍后向你介绍。我们目前并不自己生产手，而是大脑与小脑协同——你可以理解为一个模型与另一个模型的结合来操作手。我们现在可以实现跨本体操作，无论是谁的手，使用我的模型都可以操作。五指灵巧手在机器人没有视觉的情况下，根据触觉旋转一个苹果——目前全球还没有人能实现这个功能。')
add_speaker_line('Anson', '首先它需要触觉预判断，通过后还需要触觉反馈。五指之间需要协同，才能完成旋转苹果这样的动作。')
add_speaker_line('李德健', '现在机器人灵巧手的多数动作是什么水平？')
add_speaker_line('Anson', '无人能实现。')
add_speaker_line('李德健', '现在机器人的大脑去感知，而手无论是动作还是其他方面，可能只是机械性的，没有另外的控制——没有灵魂。')
add_speaker_line('Anson', '模型分为几层。动作执行和触觉模型位于端侧，安装在手部或大脑上。最智能的大脑模型保证触觉不仅在末端手部感知，同时大脑也逐步形成对物理世界的预判断和触觉反馈，形成完整闭环。这就是物理世界的难点——不能产生任何幻觉。例如想拿对面箱子里的水，如果没有对物理世界的理解，机器人就会直接穿过障碍物去拿。如果有理解，就知道要绕过去，这就是差别。')
add_speaker_line('Anson', '现有的机器人也能做一些动作，但那是遥控手柄或编程——基于结构化环境通过预设程序实现操作，这不意味着智能。它不能自主决策和进化，这才是真正的智能。宇树的机器人只能卖给两种客户：赚钱的和表演的。')
add_speaker_line('Anson', '我们设计了三层模型架构。最底层是System 0，解决闭环物理稳定，类似小脑功能。System 1主要解决端侧灵巧操作，一方面依靠视觉，另一方面采用无本体数据学习方式。目前我们仍在持续采集大量第一视角手部操作数据。System 0和System 1通过挑战智能上限，蒸馏数据用于System 2。')
add_speaker_line('Anson', '这三层模型都是同源的，这非常困难。两三年前我们做这件事时，三层架构同源解决两个问题：一是智能上限，在长程任务中自主学习进化；二是灵巧操作。除了旋转苹果，我们还可以让机器人全程煎好一份牛排——自己翻面、拿铲子。目前市面上其他方案都是用夹爪和卡槽夹住牛排，而我们直接伸手拿铲子。')
add_speaker_line('Anson', '煎牛排依靠三个因子判断熟度：第一是视觉观察颜色，第二是触觉力反馈，第三是时间。时间因素只占15%左右，主要是触觉和视觉。')
add_speaker_line('Anson', '我们目前参数已达到千亿，是国内唯一能达到千亿参数的具身智能公司。核心是自主推理加长程进化，以及System 1实现灵巧操作。现在很多人提到VLA，实际上VLA只能解决整个全栈问题的一部分，架构无法覆盖全栈。我们具备全栈能力。')

# --- Chapter 6 ---
add_chapter('六、三拨人做大脑与行业竞争格局')
add_speaker_line('Anson', '目前有三拨人在做这件事。第一拨是本体厂商，例如宇树等本体公司，融资拿到钱后才考虑如何做大脑。但王兴兴也提到这件事难度极高，对模型和参数的要求是大语言模型的几何倍数。人的感知分为触觉、味觉、嗅觉、视觉以及各种力反馈，非常复杂，需要对物理世界有非常强的交互和理解。')
add_speaker_line('Anson', '第二拨是我们本身从事模型工作的团队，通过兼容控制来接管末端或本体。')
add_speaker_line('Anson', '第三拨是以前从事车联网和自动驾驶的人。现在这个行业已经饱和，这些人转来做机器人。但自动驾驶只需要三个维度的环境感知，而机器人需要全维度环境感知，难度系数完全不同。')
add_speaker_line('李德健', '我们目前也在做车联网，但只做细分领域，例如自动驾驶的视觉对抗测试。视觉对抗样本会存在对应的bug。')
add_speaker_line('Anson', '自动驾驶只需三个轴线对空间理解即可，机器人不同——需要全维度。')

# --- Chapter 7 ---
add_chapter('七、天溯的安全检测能力')
add_speaker_line('李德健', '我们属于检测实验室，自己开发平台，例如智能体安全测评、部件漏扫、协议分析、信息安全和流量分析等。目前还在研究机器人和机械安全方面的漏洞挖掘。运输机器人也存在漏洞，我们发现了一个高危漏洞。')
add_speaker_line('李德健', '我们在物联网领域的网络安全、机器人和人工智能方面已经与政府成立子公司，由政府挂牌运营。公司有两个实验室专门负责机器人安全等工作。开发资源平台主要围绕机械安全、物联网安全和人工智能安全。')
add_speaker_line('李德健', '如果你们需要安全检测，我们也可以帮助完成。前期我们这边的资源比较多，不需要谈费用。')
add_speaker_line('Anson', '你们可以把具身智能机器人当作检测对象来理解。')

# --- Chapter 8 ---
add_chapter('八、哈工大联合课题与机器人安全')
add_speaker_line('李德健', '我们已经与哈工大联合提交了一个课题，共分三部分。第一部分是具身智能大脑的研究，第二部分和第三点我们需要进一步确定。第三部分是固件方面，这是我们的工作，因此我们承接了两个部分，他们负责一个。')
add_speaker_line('Anson', '第二部分主要解决机器人运行过程中的延迟——即实时性、可解释、可审计的手段。')
add_speaker_line('李德健', '围绕机器人运作原理：假设政府要求自动清扫机器人即街道扫地机器人在每个地方运作时，是否偏离轨道、是否遭受异常流量攻击、固件更新时是否出现恶意后门注入等情况。需要监控机器人是否被异常流量攻击。')
add_speaker_line('李德健', '我们还有一个想法是机器人防火墙。类似于无人机管控——飞到一定高度信号就没有了，直接掉下来。机器人在后期发展时也面临这个问题。如果可以实现远程操控，那么机器狗也可以被控制。例如控制机器人完成某个动作后自行短路。')
add_speaker_line('Anson', '这需要在未来有监控手段预警——该平台在不同社区需要管控、及时预警和上报。')
add_speaker_line('李德健', '机器人与智能汽车相同，一旦车辆被控制就可以自动驾驶，非常恐怖。')
add_speaker_line('Anson', '核心是安全——如何让机器接下来的操作和行动更加安全。')
add_speaker_line('李德健', '如果灵巧手的操作达到一定可用水平，我们检测行业可以找到方法进行安全评测。')
add_speaker_line('Anson', '我们属于两个角色，思考角度不同。对于我们团队而言，核心是让灵巧手具备智能化和灵巧操作能力。至于如何收敛到安全边界，虽然不是我们主要考虑的问题，但你们考虑的肯定正确——否则太灵巧了，它可以像小偷一样随便拿东西。这是有必要的，上面有人关注这一块，我们也可以进行交流。我们的核心任务是让手眼协同能力指数级提升。')

# --- Chapter 9 ---
add_chapter('九、融资情况与灵巧手生态评价')
add_speaker_line('Anson', '我们8月份第一轮融资即将关闭，投资估值大约20亿元。目前正在启动第二轮，估值大约40亿元。我们只做大脑，可以使用本体进行跨本体合作。过去两三年里，市面上的本体都与我们合作过，但真正能合作的并不多。')
add_speaker_line('李德健', '例如因诺特的灵巧手？')
add_speaker_line('Anson', '舞肌和Sharpa的使用效果较好。Sharpa是新加坡华人创办的，舞肌是深圳公司。天机的臂与它们不同，我们认为这两个产品可行。他们会根据我们的意见进行调整，因为他们只做手，模型不行，意味着对需求理解不够透彻。')
add_speaker_line('李德健', '他们的量产能力如何？')
add_speaker_line('Anson', '量产能力一般。我们长期跟踪灵巧手厂商，不能说他们以后不行，但至少目前产品还不够成熟。我们作为大甲方做模型，与所有做手和做机械臂的厂商沟通，他们在自己场景里搭建各种demo，按我们的要求实现，会立刻看出大家的差异。')
add_speaker_line('Anson', '阿里云并非用于算力，但我们了解厂商在运行什么模型、参数量和消耗量。我们清楚他们是否真正在采集数据。建模型的核心在于高质量数据。在处理数据时，通过数据跑训练一定会充分消耗算力——如果有些公司拿了钱但算力没有消耗，我们是知道的。')
add_speaker_line('Anson', '如果进行无本体数据采集，至少需要百万级小时才可以，否则数据不能仅依赖真机数据，还需要机器学习人类的数据。就像小孩刚出生时需要观看仿真数据，然后观察真实世界在做什么——尝试制作时是真机数据，看到的数据是无本体数据。')
add_speaker_line('Anson', '我们从上周开始启用睦灵科技这个名称，主要利用人类数据训练手部和上半身的手、眼、脑协同。核心能力是智能上限，需要大量数据。融资两个亿最多覆盖到这里。')

# --- Chapter 10 ---
add_chapter('十、数据采集与异构训练方法')
add_speaker_line('Anson', '目前国内和全球号称可以达到百万小时数据的公司有好几个，他们都是目标，实际实现的数量很少。我们会真正将数据做出来。')
add_speaker_line('Anson', '我们用不同的手给模型进行训练，模型的泛化速度比用同一只手训练更快。我们之前没有预料到——甚至将手臂的整体躯干和手三个部分采用不同的异构架构，这种方式对机器和模型来说更好，它们喜欢不同的东西。')
add_speaker_line('Anson', '数据采集时每个场景只采集20小时，需要更换场景。模型需要完全不同且离散的场景，它不喜欢在同一场景反复完成——这些场景已经学完，没有必要继续。')

# --- Chapter 11 ---
add_chapter('十一、EMC电磁兼容测试现场参观')
add_speaker_line('Anson', '10米法半电波暗室，大概什么时候可以有实际场景？')
add_speaker_line('李德健', '我们应该即刻有。这是半电波暗室——你可以看到金属地面，全吸波材料覆盖地面上也是无反射的。6面都无反射，都有吸波材料。可以直接将电磁波发射转化为热能或电流引出，没有反射，这样可以非常直观地测量产品在运行时发射的电磁波。')
add_speaker_line('Anson', '全电波和半电波的区别是什么？')
add_speaker_line('李德健', '全电波暗室6面都有吸波材料，半电波暗室地面是金属反射面。')
add_speaker_line('Anson', '它可以接收电磁波。这边是一个转台，会旋转360度采集每个角度发射的电磁波。这种样品在哪里？')
add_speaker_line('李德健', '这是样品。这是一个家用的小型充电桩。')
add_speaker_line('Anson', '充电桩的检测流程是什么？')
add_speaker_line('李德健', '这种方式相对简单，直接通电然后开机设定参数。有些情况可能比较复杂，例如通过APP发送任务。消费类产品如平板电脑需要开机充电、运行指定软件、满足CPU要求等。')
add_speaker_line('Anson', '需要直接操作电脑和一些软件？')
add_speaker_line('李德健', '是的。')
add_speaker_line('Anson', '你们的样品大概有多少种类型？')
add_speaker_line('李德健', '百级、千级或万级。基本上所有电子电器产品都需要进行检测——家电、灯具、玩具、工业用、消费用、打印机、入耳式耳机、AI眼镜都需要。核心在于测试样品信号对环境的影响，这个测试叫辐射骚扰测试，即产品工作时发射的非蓄意电磁波是否在法规限值以内。')
add_speaker_line('Anson', '每个国家都有强制法规，发射量必须低于一定限值。你们的工作时间是从早上8点到晚上10点？')
add_speaker_line('李德健', '前两天我在广州有一个专门做医学检测的机构，他们晚上10点才开始工作，因为所有样本都是白天汇集到检测中心，晚上运载完成后才开始检测，一直工作到凌晨2点。')
add_speaker_line('Anson', '检测行业实验都是通宵进行？')
add_speaker_line('李德健', '实际上通宵进行的工作。')
add_speaker_line('Anson', '后夜班如果有机器人替代，就可以解放人力。')

# --- Chapter 12 ---
add_chapter('十二、合作意向与后续安排')
add_speaker_line('李德健', '如果后期有必要，我可以制作一些产品架设的视频供你观看。')
add_speaker_line('Anson', '非常需要。如果您能给我一个就很好——我需要根据架设情况让算法和产品同事进行判断。如果最初快速做概念验证(POC)，需要搭建怎样的模拟场景？因为我们平时不在广州，最早期demo阶段倾向于放在杭州，人员效率更高。')
add_speaker_line('李德健', '我们对可靠性和可行性有一些判断。可以在这里建立一个项目。')
add_speaker_line('Anson', '我们可以合作。')
add_speaker_line('李德健', '我之前认识一家专注于集成方案的公司叫东昇射频（星汇智云）。他们也有这个平台，我会先给你们老板打电话让他们联系好。他们大概十五六年前从华为离职创业。')
add_speaker_line('Anson', '华为的硬件能力和工程能力很强，我们的模型能力很强。')
add_speaker_line('李德健', '他们的服务有上千家甲方和乙方实验室。他们一直在开发平台，我之前也问过他们下一步的应用。如果想要发展就需要有噱头，比如机器人运行的产品训练，这是非常有必要的。')
add_speaker_line('李德健', '关于双方的合作，如果您认为将来可以更多地密集交流和沟通，我们也愿意与你们建立类似的关系。')
add_speaker_line('Anson', 'MOU——没有任何法律约束的意向合作。')
add_speaker_line('李德健', '我认为这种事情应该想办法推动。如果你感兴趣，我们愿意。你有时间可以去杭州参观，我们在余杭阿里的总部非常好，顺便去杭州可以吗？')
add_speaker_line('Anson', '我先离开，等您准备好之后我们再联系。')
add_speaker_line('李德健', '李总您把刚才介绍的PPT发送给我。')
add_speaker_line('Anson', '我只能截取一些可以发送的内容发给您。')
add_speaker_line('李德健', '我可能会联系他们，询问你们是哪家公司在做什么。我可能会告诉他们我的集成方向。')

# =====================================================================
# PART 2 - Second session (~20min)
# =====================================================================
add_part_heading('第二部分：第三方检测行业自动化与机器人应用合作探讨')
add_meta('时长：约20分钟')

# --- Chapter 13 ---
add_chapter('十三、新能源产品测试与数字化路径')
add_speaker_line('李德健', '新能源领域的产品不同，你们负责测试，我们对项目也是如此，都是大型企业提供的服务。新能源增长比较迅速，AI算力方面现在为了有用，可以在晚上用电集中时将电存储。虽然它可以移动，但基本属于商用和户外使用。车辆5分钟充满之后会导致电网问题，因此通常在晚上使用低价电。')
add_speaker_line('李德健', '从数字化方面来看，首先要打通检测设备和检测流程，包括SOP (Standard Operating Procedure，标准操作流程)。确保所有流程都有标准，并且有一条可以体现在线化的流程。接下来是是否可以实现无人监管。')
add_speaker_line('Anson', '10米法半电波暗室——无反射的暗室。目的是测量机器人在工作过程中向外辐射的电磁波强度，需要控制在一定限值以内，否则会对其他产品造成干扰。')
add_speaker_line('Anson', '无论是机器人还是车，都在测试产品对外界电磁波的干扰。请问是否有具体的测试场景或视频供我观看？我想了解灵巧手的能力与大脑协同。')
add_speaker_line('李德健', '我之前设计了一个方案，由一个专门负责视频监督的机器人操作，虽然可以采用轮式设计，但必须有手。实际场景对机器人非常复杂——测试样品是不同类型的，可以是机器人、音箱或其他类型。')
add_speaker_line('Anson', '只要它可以枚举即可。')
add_speaker_line('李德健', '例如机器人需要准备对应的配件，测试人员会准备好。机器人一开始有配件，之后会有一份测试计划，计划按AI能理解的方式写出测试模式。例如机器人需要测试充电模式，我们已经将法规灌输了进去，拥有自己的知识库和严格SOP。这时需要测试机器人的充电模式并接上机器人。')
add_speaker_line('Anson', '你是将机器人接上，还是测试机器人？')
add_speaker_line('李德健', '我需要它满足某个测试模式，它需要实现这个模式。包括插电和充电后的摆放以及线路安排，我们都有非常清晰的要求。')

# --- Chapter 14 ---
add_chapter('十四、第三方检测行业市场概况')
add_speaker_line('李德健', '从中国国内来看，第三方检测行业每年的市场检测业绩金额大约为5700多亿元。')
add_speaker_line('Anson', '已经达到5000亿，您所指的检测是工业检测还是包含医疗检测？')
add_speaker_line('李德健', '医疗领域都包含在内，但医疗体量并不高。纯电子电器类产品的检测大约800多亿元。国内有资质的检测实验室大约12000多家。')
add_speaker_line('Anson', '上市公司有多少家？')
add_speaker_line('李德健', '上市公司有20多家，包括外资合资的，民营企业较少——只有三四家。这20多家企业也有分工，不聚焦的方向。例如华测和毕维涉及食品、药品检测、化学、矿产石油勘探等多个领域。')
add_speaker_line('Anson', '这一大盘一共是5000多亿。')
add_speaker_line('李德健', '国内市场很大，国外市场并不大。我曾经为东昇射频制作过平台，他们现在已经实现了将所有软件放入操作平台，并且可以与所有测试设备连接。')
add_speaker_line('Anson', '它能实现灵巧操作吗？')
add_speaker_line('李德健', '他们下一步需要进入实际物理应用部分。目前可以在软件层面自动运作，但下一步必须进行机器人操作。我之前为他制定商业计划书时已经提到：先实现数字化，再到智能化，最后到机器人应用场景。')
add_speaker_line('Anson', '最难的是最后一步，它的参数要求和模型要求比大语言模型高。他对触觉和视觉都有要求。')
add_speaker_line('李德健', '难度较大的事情才有趣，可以长期讲这个故事。')

# --- Chapter 15 ---
add_chapter('十五、机器人作为检测对象')
add_speaker_line('Anson', '目前很多人已经知道这个东西在使用，你们平时会使用吗？')
add_speaker_line('李德健', '虽然每天排班安排很满，但基本都在下午。')
add_speaker_line('Anson', '我们稍后再过来是否会有问题？')
add_speaker_line('李德健', '早上正好在评审，所有人都上去了。')
add_speaker_line('Anson', '我可以拍张照片吗？')
add_speaker_line('李德健', '之前有一个设想——如果我建立一个实验室测试平台，可以实现黑灯实验室。')
add_speaker_line('Anson', '工业自动化和灵巧智能结合可以实现端到端的输出。')
add_speaker_line('李德健', '三年前人工智能基建发展不佳，那时模型各方面都无法实现。')
add_speaker_line('Anson', '你们从事安全工作？')
add_speaker_line('李德健', '我们在网络安全方面，灵巧手暂时无法用于网络安全领域。网络安全主要涉及数据和软件，虽然也涉及接线，但独立接线会有一定麻烦。结构化到现场工业自动化就可以，但无法解决复杂且非标准化的问题。')
add_speaker_line('李德健', '例如我们需要使用机器人接线——现在由谁负责？12月份应该给他一个新任务。我们会有很多接线产品，使用灵巧手就是要看它能否实现替代人的程度。')
add_speaker_line('Anson', '他希望灵巧手能够实现找到合适的端口并插入线路。')
add_speaker_line('李德健', '目前这种情况应该还是如此。我最想实现类似的产品。')
add_speaker_line('Anson', '你之所以认为想在大房间里实现这个目标，是因为人工做这件事没有效率，还是其他原因？')
add_speaker_line('李德健', '一方面是效率问题，另一方面是场地较为固定，场地价值更高。')
add_speaker_line('Anson', '固定价值很重要，如果价值低就没有必要。')
add_speaker_line('李德健', '首先场景固定，例如我们这边的场景会随时移动或搬动，这就需要灵巧手去适应。')

# --- Chapter 16 ---
add_chapter('十六、温度粘贴等高价值场景与合作共识')
add_speaker_line('Anson', '固定场景、重复且价值高的场景最合适。')
add_speaker_line('李德健', '产品复杂性确实比较多。例如华测那边的产品可能受到限制，需要对应的粘贴或焊接——在指定的点上量测温度。')
add_speaker_line('Anson', '你是拿着焊枪进行操作吗？')
add_speaker_line('李德健', '并非焊枪，而是使用502胶水粘贴温度传感器。产品外观基本不同，但许多实验室的产品类型相差无几——电视机或大显示屏也是如此制作。')
add_speaker_line('Anson', '有一只手拿着胶水，把一条线粘上去？你认为这也是一个高价值环节。')
add_speaker_line('李德健', '温度传感器粘贴需要消耗一定时间。假设产品已有明确电路，每个点已明确粘贴位置。如果它能通过识别并执行，就会省掉很多人力。现在刚刚起步，很多人看不到明显的意义。这些起步到后面对实验室而言，用机器人替代人工是一个趋势。')
add_speaker_line('Anson', '没关系，不用着急。')

# ---- Save ----
doc.save(OUT)
print('saved:', OUT)
