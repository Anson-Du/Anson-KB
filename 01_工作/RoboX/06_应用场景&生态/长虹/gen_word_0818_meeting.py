# -*- coding: utf-8 -*-
"""Generate cleaned transcript Word document for 08-18 Changhong-ROBOX meeting."""

from docx import Document
from docx.shared import Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

output_path = r"D:\RoboX\06_产业生态\长虹\08-18 长虹CTO与ROBOX双方团队会晤（清理版）.docx"

SPEAKER_COLORS = {
    '田明': RGBColor(0x70, 0x30, 0xA0),
    '明修': RGBColor(0x70, 0x30, 0xA0),
    'Anson': RGBColor(0xC0, 0x00, 0x00),
    '山相': RGBColor(0x00, 0x33, 0x99),
    '碧莹': RGBColor(0x00, 0x80, 0x80),
    '贾文鹏': RGBColor(0x40, 0x40, 0x40),
    '张维': RGBColor(0x40, 0x40, 0x40),
    '万涛': RGBColor(0x40, 0x40, 0x40),
    '孟军': RGBColor(0x40, 0x40, 0x40),
    '长虹方': RGBColor(0x40, 0x40, 0x40),
}

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

style = doc.styles['Normal']
style.font.name = '微软雅黑'
style.font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(4)


def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(6)


def add_meeting_info(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')


def add_summary_heading(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '6',
        qn('w:space'): '4', qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_summary_item(num, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_after = Pt(4)
    run_num = p.add_run(f"{num}. ")
    run_num.font.name = '微软雅黑'
    run_num.font.size = Pt(11)
    run_num.font.bold = True
    run_num.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run_num.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(11)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')


def add_heading(text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '6',
        qn('w:space'): '4', qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_dialogue(speaker, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.left_indent = Cm(0.5)
    color = SPEAKER_COLORS.get(speaker, RGBColor(0x00, 0x00, 0x00))
    run_s = p.add_run(f"{speaker}：")
    run_s.font.name = '微软雅黑'
    run_s.font.size = Pt(11)
    run_s.font.bold = True
    run_s.font.color.rgb = color
    run_s.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run = p.add_run(text)
    run.font.name = '微软雅黑'
    run.font.size = Pt(11)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')


# ======================== DOCUMENT ========================

add_title("长虹CTO与ROBOX双方团队会晤（清理版）")

add_meeting_info("时间：2026年8月18日 10:13 | 时长：2小时6分钟")
add_meeting_info("参会人：田明、明修、Anson、山相、碧莹、贾文鹏、万涛、张维、孟军、何军")
add_meeting_info("主题：ROBOX与长虹团队战略合作MOU逐条讨论，明确落地todo与商业模式")

# ======================== KEY POINTS ========================

add_summary_heading("会议关键要点总结")

summaries = [
    '会议框架：三大议题——①战略合作事项逐条讨论MOU ②梳理快速落地的todo（具体到人）③商业订单与业务模式初步沟通。',
    '训练场合作模式：ROBOX作为甲方出钱采购评测和数据采集服务，长虹训练场作为乙方提供场地和执行。同时长虹通过ROBOX渠道采购天机臂等硬件，双方形成双向甲乙方关系，满足政府审计要求。',
    '硬件选型三阶段：第一阶段天机臂+5G灵巧手（现成采购，无需定制）；第二阶段加腰部自由度（pitch+yaw）+升降；第三阶段加移动底盘。长虹训练场现有宇树G1/G1D可先用起来。',
    '开源数据里程碑：1000小时灵巧操作数据集，约330人天（5台机器x2个月）。数据发布同时开源baseline模型action部分。目标10月开源，赶在投资人年终总结前。明修强调"过时不候"。',
    '商业模式设计：ROBOX压价后长虹从ROBOX采购天机硬件，ROBOX从长虹采购数据和评测服务。"大家各取所需"，长虹有收入流水满足政府审计，ROBOX获得数据。',
    '数采装置路线：第一阶段手机APP+外接摄像头（快速铺开）；第二阶段触觉手套装置（需搭建时间，后续推进）。ROBOX持续输出方案定义，长虹做产品化工作。',
    '家庭数据采集宏目标：6个月10万小时，一年100万小时。两阶段：先用50元/户采集空镜数据筛选用户，留存用户持续按小时付费采集操作数据。学生联合培养基地+自有资源池双轨并行。',
    '长虹训练场设施：三层建筑——一楼全身控制/展厅，二楼家庭场景样板间（厨房/卧室/客厅，L型布局便于机器人运动），三楼灵活空间（天轨/地插/网口，可大规模采集）。',
    '基模后训练合作：ROBOX提供模型服务化能力，支持长虹二次开发。合作模式待探索（License/买断/云服务），ROBOX部分基模不开源走商业化路线。长虹需要带空间感知能力的基模。',
    '太空舱餐饮场景：50万成本（机器人+双臂+仓体），两年回本。现制果汁/烘焙加热等高价值餐饮，政府渠道拉动+品牌联名（茶百道/霸王茶姬）。与田螺云厨2万元自动化方案形成成本差异，需政策补贴弥补。',
    '太空舱落地路径：先在训练场做一套demo（省级展厅窗口效应），领导参观后帮助推渠道和餐饮资源。长虹负责仓体集成+软件应用开发，ROBOX提供模型大脑+灵巧手选型。',
    '康复场景讨论：ROBOX定位长周期赛道（康复≠养老），港大合作背景。长虹建议先内部研判再推政府。当前康复科在医院不受重视、预算低，但长期看好4亿老人市场。ROBOX有康复治疗经验团队成员。',
    '硬件降本方案：长虹规划5万元双臂方案（年底出样），基于OpenArm改进，行星关节、额定4kg负载、毫米级精度。配套主从臂VR遥操+力反馈已打通。明修认为廉价方案也能做能力验证。',
    '投融资合作：长虹+申万宏源基金有意战略投资ROBOX。明修已与长虹沟通，对方"要抓紧投"。ROBOX第一轮基本close，希望产业方做战略投资者。曾投星动纪元等项目。',
    '数据比例与场景优先级：无本体数据:真机数据 > 10:1。场景优先级：家庭（最多样）> 酒店（餐饮+洗衣）> 实验室/检测 > 工厂产线（节拍太快不适合）> 康复（长周期单独推进）。',
    '模型评测部署：需在西部部署机房解决网络延迟（当前2分钟动作测试要15-20分钟且频繁掉线）。ROBOX提供本地化SDK+端云交互方案，阿里云可配合。碧莹为对接入口，分发各专项负责人。',
]

for i, s in enumerate(summaries, 1):
    add_summary_item(i, s)

# ======================== CHAPTERS ========================

add_heading("一、开场介绍与议程说明")

add_dialogue("田明", "我理解今天大家的议程可能有三个方面：第一，围绕具体战略合作事项，逐条讨论框架协议MOU；第二，根据讨论内容梳理快速落地的todo，具体到每个同学；第三，围绕合作项初步沟通业务模式和商业订单需求。今天双方都来了很多同学，我们希望快速形成具体合作。")

add_dialogue("田明", "先介绍一下我们这边同学：Anson老师，主要负责战略和政府关系；碧莹，负责商务和项目方案；山相（曾明华），运动控制负责人，硬件方面有很深了解；丹泽（赵亚西），原华为车BU算法骨干，现在做触觉泛化和VLA；陆洲，清华算法核心骨干。")

add_dialogue("明修", "我介绍一下长虹这边：贾文鹏，技术负责人；万涛，硬件；周梦军；张维，训练场负责人；何军，算法，正在做系统整体架构；还有几位负责生态和软件项目的同学。")

add_heading("二、训练场合作：评测与数据采集")

add_dialogue("田明", "第一个议题围绕训练场合作推进。长虹有省级训练场，我们在素材装置上先行做了一些工作。两个部分：第一，评测业务的细化，ROBOX作为甲方，围绕模型大脑需要评测的能力配置设备，形成商业化订单；第二，数据采集和处理服务，模型本身可以做action标注。另外补充一点——开源数据。当前灵巧操作数据开源存在整体缺位，如果我们快速形成1000小时数据开源，可以打全球首个灵巧操作数据开源。")

add_dialogue("明修", "对于一个开发者做具身智能模型，有几个卡点：第一在哪里训练？第二在哪里测试？第三数据哪里来？开源数据第一个解决数据问题，第二个引导开发者来训练场测试，第三个探索基建和商业模式。如果开发者没有很强的处理能力，我们有开箱即用的能力包，引导出二次开发需求。")

add_dialogue("明修", "本体方面，聚焦灵巧操作一定是灵巧手，可以多方面考虑，比如高中低三种不同自由度的灵巧手。高的话可能到22个自由度，低的话可能到11个自由度。最重要的还是有真实的环境、真实的机器人被允许用户来测试。")

add_heading("三、硬件选型：天机臂+5G灵巧手")

add_dialogue("山相", "我们现在暂时用的方案是双臂加一个七自由度双臂加20自由度灵巧手。七自由度主要是实际交叉的内容，并集更符合我们需求，工作空间更接近。但现在没有腰部自由度、头部自由度和移动能力，只能局限做桌面灵巧操作。")

add_dialogue("明修", "天机5G这套是现在所有做操作模型的标配。天机这款机械臂比宇树那款的稳定性、对模型的友好程度高好多个数量级。5G的灵巧手说实话做得也一般般，但今天如果你决定做灵巧操作模型，市面上只有它这一款能买来用。40万一个，其他的连遥操作都还没有打通。所以训练场肯定是持续迭代的，我们可以知道模型侧现在最主流用的是什么本体。")

add_dialogue("明修", "我建议第一阶段用天机5G，第二阶段可以基于宇树的生态去拓展手部的自由度。宇树G1和G1D可以先用起来，虽然少了腰部自由度但可以升降。然后中间补一档，用G1D先继续走一部分，可以动起来了。")

add_dialogue("田明", "我们展示一下最新工作的视频。这是基于122B千亿参数具身大脑实现的跨本体灵巧操作最佳实践。三种本体范式：天机5G的范式能完成使用工具的连续长程灵巧操作；第二类本体范式，我们有完整的煎牛排15分钟一镜到底视频；第三类是移动底盘加上半身双臂。我们在国内能完整完成跨真机的大脑适配和智能运行，处于头部梯队。")

add_heading("四、开源数据策略与时间节点")

add_dialogue("明修", "1000小时如果按一天3小时，就是330人天。看机器数量和预期发布时间点。你们数据只要到位了就开始训模型，数据发布出去的一瞬间对应的baseline就出来了。最好基建也到位，有限开放几个名额给别人测试。")

add_dialogue("田明", "从融资节奏角度，过了10月之后投资人逐渐进入年终总结阶段，很多东西赶不上融资节奏。我们建议一个半月到两个月完成。")

add_dialogue("明修", "一个月的话33天就得10个人10台。两个月算的话5台就好。模型在action部分我们会开源，基于这1000小时的checkpoint会开出来。")

add_dialogue("贾文鹏", "模型全开源吗？")

add_dialogue("明修", "第一阶段action部分会开源，商业化基模不开源。")

add_heading("五、商业模式：甲乙方关系与设备采购")

add_dialogue("明修", "帮张伟问一个问题：关于设备采购和商业化订单，现在是怎么定的？张伟那边有一些到期预算和政府审批的要求。")

add_dialogue("张维", "政府审计会一笔一笔审计我们的投资和人力支出，每笔要求有一定的产出或价值。")

add_dialogue("田明", "我抛砖引玉：有了数据，我们作为数据方出钱，你们采。评测也是我们出钱，你们做——我们做甲方，你们做乙方。评测需要本体，本体是训练场的资产，理论上训练场来购买。我们可能也有渠道，你们购买时我们作为渠道，跟天机压价，你们从我们这边过一道手。大家各取所需。")

add_dialogue("张维", "一定要有甲方跟乙方的关系，要有兑换才行。至少要有收入。")

add_dialogue("贾文鹏", "张维现在手里砸了几十台机器人没有产生价值，他需要去讲这个价值。")

add_dialogue("明修", "模型需要的本体其实很有限。我们知道哪些能用，比如测过宇树，为什么还选5G？因为做操作的时候5G做得好，宇树做不好。")

add_heading("六、数采装置产品化")

add_dialogue("田明", "第二个议题是无本体数采装置。长虹希望未来做成独立业务、产品化和规模量产。ROBOX持续输出方案定义，长虹做产品化工作。未来如果需要用这套装置，直接分润。")

add_dialogue("明修", "原来那套在内部做的，外部从0到1重新规划。做几个样板出来，大家看是否要量产。目前有几个方案：第一，基于纯手机摄像头；第二，手机APP基础上去外接摄像头支持更多模态采集；第三，原来的装置方案，但需要重新搭建。分镜和异构数据采集可以基于手机加摄像头实现。")

add_dialogue("田明", "手套那套还做吗？")

add_dialogue("明修", "手套是装置，需要时间，但会持续推进。当前手机加摄像头就可以。")

add_heading("七、家庭数据采集计划")

add_dialogue("明修", "第一个目标是进入足够多的家庭，而且是真实家庭，不是样板间或空着的租房，希望里面有个人用品。")

add_dialogue("碧莹", "我们希望家庭是真实家庭，不是样板间，里面是空着的。希望是摆着个人用品、正儿八经住的。")

add_dialogue("田明", "一般是50块钱一户，我们去年做过空镜数据采集。先带摄像头采集空镜，圈起来后继续做操作，按小时收费。")

add_dialogue("明修", "两阶段：第一阶段Ego带摄像头，50块一户，把用户圈起来；第二阶段设备继续留着，开始做操作——叠衣服、打扫卫生等，按小时收费，持续要。")

add_dialogue("碧莹", "目标6个月采10万小时。APP和装置加起来。")

add_dialogue("明修", "6个月10万小时只是初步练兵，一年100万小时。")

add_dialogue("Anson", "青岛和无锡的主要做法是跟学校签联合培养基地，发实习证书，学校算学分。学生本身也需要实习证明，各自有利益。学校也需要，因为学生不好就业。这样能动员出学生及其背后的家庭来做数据，甚至不需要钱。")

add_dialogue("贾文鹏", "我们有联合培养基地，但学生不可控性太强。还有自有的资源池，签了合作的甚至员工类的。")

add_dialogue("Anson", "多种手段并行，核心是满足大规模数据且节奏要求很快。签成的家庭保有，持续扩展。")

add_heading("八、长虹训练场场景介绍")

add_dialogue("张维", "我们训练场整体是一个三层的建筑。一楼是有曲折廊道的空间，做全身控制展厅；二楼是长虹家电和家居产品的体验区，配置了比较完备的厨房、卧室、客厅，家居生活系统；三楼是灵活空间，有天轨、很多地插和网口，以后主要用三楼做大规模采集。现在能利用的场景是家庭和桌面级工业。")

add_dialogue("明修", "二楼偏家庭场景，厨房和卧室数量怎样？")

add_dialogue("张维", "现在只有一套，可以理解成样板间。如果想要不同的卧室，可以在酒店找不同房型。我们售楼部的样板间也可以用，周边还有楼盘。")

add_dialogue("山相", "二楼家庭场景是按样板间设计的，还是根据机器人特性改造的？")

add_dialogue("张维", "设计时根据机器人特性改造了。整体样板间是很开放的环境，L型布局，便于参观和机器人运动。设备比较多：烤箱、微波炉、茶吧机、洗碗槽、烟机灶具等都可以做。")

add_heading("九、基模后训练合作")

add_dialogue("田明", "第三个议题是基模后训练合作。ROBOX主要做大脑，foundation model持续研发。长虹有算法团队，可能考虑后训练工作。模型如何做二次开发是需要准备的链路。模型服务化形式被人二次开发，这个合作模式需要思考。")

add_dialogue("明修", "这部分基模不开源，走商业化路线。以服务化的形式被使用，具体什么模式我们还得想一下，但未来肯定值得推进。")

add_dialogue("贾文鹏", "我们跟阿里买过端侧模型，一次性买断或几百万费用。也有License加ERE的模式。基模不会拿去往外传，直接加密、服务化。")

add_dialogue("贾文鹏", "我们后续应该会把整个基模完全切出来，全部采用合作伙伴的。你们的基模后续带空间感知能力吗？我们现在强行把OCC信息加到模型里，如果你们模型比较好可以直接上。")

add_dialogue("明修", "可以，一起探索。后训练平台你们会对外开放吗？")

add_dialogue("贾文鹏", "自己用，自己账号。")

add_heading("十、太空舱餐饮场景")

add_dialogue("田明", "第四个议题是应用场景合作。核心场景包括太空舱现制餐饮、生物医药、康养等。先选太空舱做第一个demo。ROBOX提供基础产品（模型大脑服务+灵巧手选型），长虹已有基础设施，纳入整个系统做定制开发和交付。买单方应该是政府事业单位，做分润。")

add_dialogue("孟军", "现制餐饮场景需求我们认可，但想了解回本周期、成本测算、渠道费用等详细信息。另外田螺云厨的机械臂加自动化设备方案成本只有2万多，我们拿50万的东西去推会面临同样的问题。")

add_dialogue("田明", "太空舱加机器人双臂大概50万，两年回本。一天现榨果汁收入2000多，一个月5万，一年60万。杭州田螺云厨做了15年餐饮自动化，CEO跑了一年半市场调研后决定核心干太空舱产品，6个月回本。我们联系了茶百道、霸王茶姬等品牌方做三方联名，他们提供原料和品牌。")

add_dialogue("碧莹", "我们做高价值餐饮，餐饮价值成倍上升，回本周期也会成倍下降。")

add_dialogue("Anson", "理解你的意思——消费降级。能不能跟人工智能场景应用示范结合，让地方政府给补贴？现在落场景政府有政策给补贴，不涉及一事一议，是普适政策。用政策让地方政府跟营收捆绑给补贴。")

add_dialogue("孟军", "如果核心目的是融资和发出声量，我们就把需求带回去找渠道铺进去。我们需要了解做这个事情最核心的目的，回去好有一套叙事逻辑。")

add_dialogue("Anson", "有一点一定要讲清楚：我们绝对不是说只干这个事情，一定奔着高价值密度去。太空舱承担阶段性任务——宣传、快速积累数据、给资本市场和政府形成认知。中长期一定尽快铺高价值密度的赛道。")

add_heading("十一、太空舱落地路径与demo计划")

add_dialogue("孟军", "建议先投资源做一套出来摆在训练场，因为政府现在都要看实物。训练场也是省级展厅，很多人来看。做什么可以根据渠道方的要求来定。")

add_dialogue("明修", "每天都有不同领导来看，领导带着任务来，可能负责某些景区或地域，看到后自己会代入，帮我们拉餐饮资源。")

add_dialogue("贾文鹏", "比如最近我们搞了一套变脸的，领导帮我们推到各个集团去采购。可以走这个模式。")

add_dialogue("碧莹", "太空舱里面做灵巧操作，对自动化设备要求没那么高，可以用现成的不带智能化的设备。你们选定做什么之后我们一起对。")

add_dialogue("孟军", "可以分两步走：先投资源做一套摆在训练场，看完后根据真正买单方和渠道方的要求来定做什么。旅游景点很多，哪些适合卖烤肠、哪些卖奶茶，同时拿着去跟茶百道、霸王茶姬同步推。")

add_heading("十二、康复场景讨论")

add_dialogue("贾文鹏", "康养这块大家感不感兴趣？")

add_dialogue("明修", "其实不是养老，是康复。养老跟康复是两回事。养老做的是端茶送水很杂的活，康复是一个很长周期的事。首先要有很好的护工康复员，用素材设备把手法治下来，然后才开始做技能。康复有很多动作，不是所有现阶段都可以做到。它是一个长周期赛道，没这么快落地。")

add_dialogue("Anson", "康复对我们是长周期态度。几个问题：第一，接触人风险很大，出一个问题整个事就崩了；第二，康复科在中国医疗体系里最不受待见，医院有费用也不会拨给康复科，没有预算。但我们看好它，因为中国将来有4亿65岁以上老人。")

add_dialogue("孟军", "如果是要单独推康复，这是单独议题，我们可以拿共同认知和渠道资源去跟政府推。他们肯定会感兴趣，预期会被我们影响和降低。")

add_dialogue("明修", "可以先拉起来，我们有一个做过康复医疗治疗的同学，可以跟你们一起聊一下。")

add_dialogue("Anson", "内部先研判，然后再去找政府。在此之前先别去推。")

add_heading("十三、硬件合作：降本方案与灵巧手")

add_dialogue("田明", "硬件合作方面，轮式双臂灵巧操作机器人整机定制需求，ROBOX作为甲方以订单形式。另外我们对灵巧手很感兴趣，了解到华丰可能在做类似的事情。")

add_dialogue("贾文鹏", "需求我们在华丰那边让他们看一下，搞不了就先用5G的。")

add_dialogue("明修", "可以跟华丰直接聊一下，进展同步给我们。华丰做高速连接器，航天方面也有供货。商业航天和具身智能结合是未来方向，如果机器人在做实验的地方能用到，这个三方向结合很好。")

add_dialogue("万涛", "我们现在想的方案是搭一套成本5万以内的，每个臂七自由度。基于OpenArm改进，电机和结构都换了，行星关节，额定4kg负载，毫米级精度。希望在年底拿出样机。现在廉价方案频繁发出来，2万块的时装臂只是引流价，实际七八万。半年后如果还是30万成本就不有竞争力了。")

add_dialogue("明修", "天机5G这套是阶段性选择。降本是另一条线，今天用很烂的机械臂也可以做能力验证。OpenArm我们很早之前就研究过，你们是基于OpenArm改的？")

add_dialogue("万涛", "对，整个电机和结构都换了。主从臂VR遥操和非复式遥操都打通了，加了力反馈但还比较原始。")

add_dialogue("明修", "腰部自由度是哪两个？")

add_dialogue("万涛", "pitch和yaw，不是roll。需要升降加腰部两个自由度。")

add_dialogue("明修", "这些是短期方案，长期我们自己要单独拉会讨论。前面定了很多现成的要赶紧推。")

add_heading("十四、投融资合作")

add_dialogue("田明", "投融资这块，浩山老师提到申万宏源对我们很感兴趣，可以先对接起来。")

add_dialogue("Anson", "关于股权投资，我们第一轮基本close了，希望有产业方来做战略投资者。")

add_dialogue("明修", "我跟长虹这边聊了，从机器人公司角度希望他们能投一些做绑定。他们很感兴趣，对合作关系想要投的话从领导层面更好推动。长虹和申万宏源一支基金。")

add_dialogue("贾文鹏", "他们之前看了很多机器人项目但没投进去，星动纪元等。领导层面对咱们有限制，挺希望和我们合作。")

add_heading("十五、数据比例与场景优先级")

add_dialogue("张维", "想了解一下后续对数据要求的具体结构——真机素材和无本体素材的比例？我们尽量用资源去匹配。")

add_dialogue("明修", "成本限制下，无本体素材比真机比例应该大于10:1。如果无限加大真机数据，我们就不做。")

add_dialogue("张维", "后续会不会出现设备放到我们这托管，我们出人力和管理？")

add_dialogue("明修", "硬件托管，我们不是本体公司，不会买很多本体。现阶段买太多不合适。")

add_dialogue("贾文鹏", "无本体场景希望能尽快有一个家庭的，我们已经收到了。还有没有其他的？")

add_dialogue("明修", "其他场景在商业服务里看哪个最可靠、最有可能去做的。家庭装需要一段时间，酒店也值得探索——酒店比工厂更多样。实验室、检测室、维修都可以。核心是足够的多样性，家庭天然多样，酒店次之，工厂适当配一部分。")

add_heading("十六、模型评测部署与网络优化")

add_dialogue("贾文鹏", "上次测达摩那个模型，两分钟的动作张伟那边要测到15-20分钟，中间会掉线重连。现场感官效果不太好，很多家希望把测试过程录下来做宣传，但现场达不到水平，主要是网络波动。")

add_dialogue("明修", "两个点：第一，部署机房在哪？我们没有西部机房，合作的话可以在西部专门部署一个机房，把延迟打下来。第二，专门的本地化SDK，双方协作。端云交互实时更新，测完就走。机房迁到西部是最快的。")

add_dialogue("贾文鹏", "现在评测平台还能用吗？还是重新开发？")

add_dialogue("明修", "新公司肯定得重新开发，内部那套也还可以用。线上搭服务很快，线下部署离线协同节点是最优方案。")

add_dialogue("贾文鹏", "真机评测的人张维那边出，后续系统这块想做成商业化的，你那边出一个人对接。")

add_dialogue("明修", "山向这边对接系统部署。碧莹是统一入口，会分发各专项负责人。")

add_dialogue("田明", "好，那我们边吃边聊。收获颇丰，这次合作。")

# ======================== SAVE ========================
doc.save(output_path)
print(f"Document saved to: {output_path}")
