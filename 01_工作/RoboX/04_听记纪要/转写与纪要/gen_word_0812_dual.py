# -*- coding: utf-8 -*-
"""生成08-12两份录音转写清理版Word文档"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ========== 格式引擎 ==========

COLOR_HEADING = RGBColor(0x1F, 0x4E, 0x79)
COLOR_NORMAL = RGBColor(0x00, 0x00, 0x00)
COLOR_NOTE = RGBColor(0x80, 0x80, 0x80)

def create_doc(speaker_colors):
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
    return doc

def add_title(doc, text):
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

def add_heading(doc, text):
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

def add_dialogue(doc, speaker_colors, speaker, text):
    p = doc.add_paragraph()
    run_s = p.add_run(f'\u3010{speaker}\u3011')
    run_s.font.bold = True
    run_s.font.size = Pt(11)
    run_s.font.color.rgb = speaker_colors.get(speaker, COLOR_NORMAL)
    run_s.font.name = '微软雅黑'
    run_s.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run_t = p.add_run(text)
    run_t.font.size = Pt(11)
    run_t.font.color.rgb = COLOR_NORMAL
    run_t.font.name = '微软雅黑'
    run_t.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.line_spacing = 1.5

def add_note(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = COLOR_NOTE
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.left_indent = Cm(1)

# ========== 文档1：成都高新区交流 ==========

SC1 = {
    '副总': RGBColor(0xC0, 0x00, 0x00),
    '管委会代表': RGBColor(0x00, 0x70, 0xC0),
    '田明': RGBColor(0x00, 0x80, 0x80),
    '明修': RGBColor(0x70, 0x30, 0xA0),
    'Anson': RGBColor(0x00, 0x60, 0x00),
}

doc1 = create_doc(SC1)
out1 = r"D:\RoboX\04_听记纪要\转写与纪要\2026-08-12 17.01 成都高新区财政国资局投资促进处和高新策源投资（清理版）.docx"

add_title(doc1, '08-12 成都高新区财政国资局投资促进处与高新策源投资交流')
add_note(doc1, '参会人：副总（高新策源投资）、管委会代表（财政国资局）、田明（ROBOX联合创始人/产品负责人）、明修（ROBOX创始人/CTO）、Anson（ROBOX CSO）')
add_note(doc1, '时间：2026年8月12日')

add_heading(doc1, '一、团队背景介绍')
add_dialogue(doc1, SC1, '副总', '请田总介绍一下公司情况——团队背景、出来做什么、为什么出来、团队大概怎么样。')
add_dialogue(doc1, SC1, '田明', '我从两个层面介绍：第一是团队背景和出来发展的动机，第二是项目核心方向及匹配资源。我们团队有几个关键标签：')
add_dialogue(doc1, SC1, '田明', '第一个标签，我们是阿里集团做具身智能的核心团队，骨干出自阿里达摩院具身智能实验室，2024年3月成立，愿景是以最快速度提升物理智能上限，向集团总裁吴泳铭定期汇报进展。')
add_dialogue(doc1, SC1, '田明', '第二个标签，我们是个系统化团队。本月关键方向的PL或负责人10人以上会参与进来，第二梯队也不少于10人，建制完整，具备核心能力且充分打磨过。从具身智能大脑的预训练、后训练，到数据管线、解决方案架构和产品，都有核心专家坐镇。')
add_dialogue(doc1, SC1, '田明', '第三个标签，年轻且专业化。校招简历报录比1000:1，核心算法负责人是阿里星出身（类似华为天才少年），也拿到了华为天才少年offer。核心研发人才主要来自港中文、清华、北大、浙大、南阳理工。')
add_dialogue(doc1, SC1, '田明', '第四个标签，有系统化积累。24年3月成立至今做了近三年的标志性探索，包括具身大脑模型Rainbow Brain，以及VLA层面的VLA 001。我们在大厂全球智能第一梯队的积累上持续创新，有系统化交付能力。')
add_dialogue(doc1, SC1, '田明', '团队完整度上，CFO是原阿里财务副总裁，后应雷军邀请去金山当CFO，有丰富的多家大型企业推进上市经验，会全职加入。政府关系和生态方面有阿里战略部门资深专家支撑。')

add_heading(doc1, '二、ROBOX技术定位')
add_dialogue(doc1, SC1, '田明', '我们新组织叫ROBOX，核心愿景是用人类知识教会机器人改变物理世界。定位是一家专注于做具身智能大脑及配套系统的公司，核心是智能技术驱动。')
add_dialogue(doc1, SC1, '田明', '核心技术主张是通过手眼脑协同的物理智能系统来提升物理智能上限。从第一性原理出发，具身智能最大特点是在物理世界中通过连续复杂的接触产生应用价值，需要软硬结合、密切协同来提升智能。')
add_dialogue(doc1, SC1, '田明', '从阿里出来的第一个动机：大厂更喜欢在数字世界闭环，比如在仿真里走标踩分去scaling，而软硬协同不是大厂擅长的。第二个动机：阿里战略调整，今年有几场必赢之战——数字AI foundation model（千问承压）、AI应用侧（通义APP对豆包）、大消费侧（淘宝闪购消耗现金流），所以具身智能方向更迎接市场化行动。')

add_heading(doc1, '三、煎牛排Demo与技术能力展示')
add_dialogue(doc1, SC1, '田明', '2026年开始业内共识全面转向"以人类为中心"的数据筛选，需要把对智能提升有关的数据——灵巧手相关的触觉、灵巧操作、眼部视觉感知——以人为本体来训练。我们认为具身智能最小组合是：灵巧手（硬件执行）+视觉传感器（感知）+大脑服务（智能迭代闭环）。')
add_dialogue(doc1, SC1, '田明', '今年上半年我们面向行业头部具身智能公司统一提出煎牛排任务，用统一的牛排和夹子作为物理世界测试集。自变量、星辰智能等都参与了。自变量因为没有灵巧手操作，用夹爪完成打开柔性保温袋取牛排的动作时，牛排会变形，缺乏力触反馈。这说明当前智能水位由于灵巧性不足，约束性很大。')
add_dialogue(doc1, SC1, '田明', '我们的最佳实践：大脑已做到千亿规模参数，可在不同构型机器人本体上自动化驱动。宇树双足机器人可以通过智能做微小拉凳子推凳子动作。与天机5G完成双臂协同煎牛排，全程一倍速，是全球首个跨本体真机协同demo，对标美国前沿智能公司。')
add_dialogue(doc1, SC1, '田明', '判断一家具身智能公司是否靠谱的三条标准：第一，有没有对外开放的完整技术报告；第二，有没有真机系统化实践案例；第三，有没有被美国最前沿研究团队纳入benchmark对比。我们的Rainbow Brain在英伟达Cosmos 3世界模型中作为国内唯一对比的大脑模型，同时满足三条标准的公司在国内非常屈指可数。')

add_heading(doc1, '四、System 2/1/0分层架构')
add_dialogue(doc1, SC1, '田明', '我们主张分层模型架构。System 2是超大规模大脑，学先验知识做任务拆解；System 1负责原子动作的高效准确执行；System 0下沉到关节电机层面做高频闭环反馈。三层对频率和资源需求不同。')
add_dialogue(doc1, SC1, '田明', 'System 2目前122B，国内最顶尖的千亿规模参数，在千卡集群上训练，对创业公司试错成本很高但我们有体系化经验。分层模型应联合优化——VLA操作模型从大脑模型用同源架构设计，保证信息在latent space（潜在空间）交互，而非自然语言串联，同源架构有系统性优势。')
add_dialogue(doc1, SC1, '田明', 'System 1的触觉分两阶段：接触前用WTM（世界触觉模型）融合触觉与VLA信息，知道用多大力抓；接触后做手掌内调整（in-hand manipulation），不需要视觉先验，根据触觉调整——这就是触觉世界模型。全球还没能处理好这个问题。')
add_dialogue(doc1, SC1, '田明', 'IP隔离方面：模型都对外开源，不会沿用原来的IP。现在模型迭代很快，我们会在新能力项上直接做新版本，不会带数据出来，快速根据需求收集数据。三个月内可完成新基础设施恢复，3到6个月发布新版本模型。')

add_heading(doc1, '五、数据采集方案')
add_dialogue(doc1, SC1, '田明', '数据门槛第一指标是50万小时。generous的正一今年上半年在美国发的第一个SOTA，BH0.8刚发也达到50万小时，百万小时数据也在出。我们希望3到6个月快速达到50万小时门槛。')
add_dialogue(doc1, SC1, '田明', '全模态采集方案：头戴式第一人称素材+手部手套+全身tracker，已在四川长虹训练场开始采集，获得四川省领导高度认可，原话是"最全面、最专业的方案"。业内数据厂商最大问题是不从智能提升角度驱动，不能说清数据为什么好、为什么可用。我们的数据在自己模型上已验证预训练和后训练效果提升曲线。')
add_dialogue(doc1, SC1, '田明', '低成本方案：裸手头戴摄像头采集，用高质量数据做标注模型，对低成本数据做伪标注提升质量。高精度到低成本扩量的完整方案体系。数据不作为商业化业务——高质量数据是模型提升的壁垒。')

add_heading(doc1, '六、发展路线图')
add_dialogue(doc1, SC1, '田明', '当前具身智能还没到达PMF（产品市场契合）爆发点，处于TPF（技术产品契合）验证期。核心任务是把技术可用性做到80分水位，定义出基础产品形态——手眼脑软硬协同组合+二次开发平台。前12个月主要做能力提升。')
add_dialogue(doc1, SC1, '田明', '然后做关键最佳实践：商业服务场景标杆打造，考虑康养和户外移动餐车鲜榨果汁等限制餐饮。已在谈落地合作，如熊猫基地、头部景区，长虹已汇报省领导获高度认可。第三是AI for Research方向——数字AI规划研究方向，机器人完成大规模生物理化实验，这是巨大蓝海市场。终局是进入家庭。')

add_heading(doc1, '七、融资情况')
add_dialogue(doc1, SC1, '副总', '这轮准备融多少？融资close预计什么节点？')
add_dialogue(doc1, SC1, '田明', '第一轮2个亿，基本已经超额认购，还在选择领投方，希望早期投资人能作为伙伴持续支持。种子轮20亿人民币估值，投资人已达成高度共识。下一轮40到50亿。')
add_dialogue(doc1, SC1, '明修', '种子轮已经在close中，两三周内。第一个协议已经谈完，后面几家看条款增减。')
add_dialogue(doc1, SC1, '副总', '如果成都要投，大比例投入可能安排在哪一轮？')
add_dialogue(doc1, SC1, '明修', '下一轮比例剩不多了，大比例可能得第三轮。下一轮融的也就几个亿，都被吃完了。第三轮可以考虑。')
add_dialogue(doc1, SC1, '田明', '我们对"西部第一大脑"的概念觉得蛮性感的。')

add_heading(doc1, '八、IP隔离与达摩院资产')
add_dialogue(doc1, SC1, '副总', '达摩院的专利和数据能不能拿出来？团队有竞业吗？')
add_dialogue(doc1, SC1, '田明', '公司的资产我们不会带出来，无论是模型还是数据。核心骨干人才会一起来做探索。我们会在下一代模型结构上，用经验积累快速做新版本，三个月内完成新基础设施。不会带数据出来，不会有产权纠纷，已与集团高层密切沟通。')
add_dialogue(doc1, SC1, '明修', '不是单纯恢复达摩院的工作——下一代模型有新的思考和架构设计，模型选型也有变化。数据配方、规模、架构设计都在新公司重新做。3到6个月争取发布新版本模型。')
add_dialogue(doc1, SC1, '副总', '目前公司是全建制团队但没有资产的状态？')
add_dialogue(doc1, SC1, '田明', '资产已有明确计划，第一批启动资金已开始恢复，时间大约三个月以内。')

add_heading(doc1, '九、商业化路径')
add_dialogue(doc1, SC1, '副总', '6到12个月有商业化的可能性吗？')
add_dialogue(doc1, SC1, '明修', '6到12个月产生正向商业回报对我们做模型来讲不现实。')
add_dialogue(doc1, SC1, '田明', '我们的思路是核心锚定提升技术上限，同时跟合作伙伴深入协同。比如数采装置可以跟长虹合作做量产和服务，产生数据订单和模型服务输出。移动餐车已获四川省领导确认可以快速推动，我们提供标准化大脑能力，结合四川系统集成优势做落地和分成。四川具身人形也表示希望采买我们的大脑服务。')
add_dialogue(doc1, SC1, '明修', '我们会分为"做智能上限"和"沿途下蛋"。大规模商业化是通过合作伙伴推动完成的，我们提供标准化能力分成。核心不在于盈亏平衡，而在于通过商业化场景牵引技术证明价值。')
add_dialogue(doc1, SC1, '田明', '我们核心偏左——追求技术上限快速提升。MiniMax和智谱的成功在于回归Foundation Model快速提升智能水位；反例是百川过早放弃训练去做医疗金融，零一万物也分散了。模型技术水位快速提升时一切系统场景都会被重构。')

add_heading(doc1, '十、成都算力与数据政策')
add_dialogue(doc1, SC1, 'Anson', '我们关心的几个点：第一，低成本算力方面，如果落地高新区有什么产业政策和优惠？第二，数据采集方面，区里有什么政策和基础设施可以给到帮助？')
add_dialogue(doc1, SC1, '管委会代表', '算力券方面，30券每年2个亿，模式券每年4个亿，这是高新区常规政策，范围内都可以申请。特别重要的项目会有额外支持。')
add_dialogue(doc1, SC1, '管委会代表', '算力中心方面，目前存量算力主要是华为系——910A，马上上910C，两三百P的算力储备。第二期在规划建设，投入几十亿量级。具体优惠政策今年下半年应该会出政策。训练数据方面，有在投相关公司都在成都，可以一起合作。')
add_dialogue(doc1, SC1, 'Anson', '我们算力消耗最大的是H卡（裸卡），这方面有相应算力吗？')
add_dialogue(doc1, SC1, '管委会代表', '英伟达目前成都没有规划，主要还是华为的。阿里云在高新区的ADC是传统云计算，不是模型训练用的智算。')

add_heading(doc1, '十一、场景公司经验分享')
add_dialogue(doc1, SC1, '管委会代表', '成都最近搞了创业公司统筹整个城市场景资源，国资优先采购、优先开放产品。从场景层面讲这是城市弯道超车的重要策略。')
add_dialogue(doc1, SC1, 'Anson', '场景公司这件事最早做的是杭州，坦率讲过去几年效果并不好。主要问题是场景需求方和供给方之间——需求质量不高，很多是任务工程，场景不真实、落不了地。需要属地政府强力帮助去和高校、实验室、科研机构、商业服务场景推进。不是让他们采购设备，而是在真实场景里做数据采集，需要场景提供方的人配合、甚至设施设备增加。这不是场景公司能搞定的，需要政府强力支持。')
add_dialogue(doc1, SC1, 'Anson', '数据采集方式需要在足够多的不同类型场景和岗位上采集上半身、尤其手部操作的第一视角数据，每个场景岗位可能10到20小时就结束再切换。涉及面比较大，不是一个企业能量能推动的。')
add_dialogue(doc1, SC1, '管委会代表', '成都2300万人口，场景是最大优势。成都高校50多所，医院和科研机构量也很大。现在领导已认识到这点，围绕AI for Science这块，也是高新区人工智能主要方向。')

add_heading(doc1, '十二、总部落地与合作意向')
add_dialogue(doc1, SC1, '管委会代表', '我们最主要的投资方式是产权化投资——产业转移过来、总部落地，这种基本可以非常大，10亿级的。高新区管委会层面可以做决策。另外有市场化投资，1亿以下份额。')
add_dialogue(doc1, SC1, '管委会代表', '成都如果再错过具身智能产业，就只能拖回服务业了。具身大脑是目前最欠缺的，如果说供应链是红海，那具身大脑能够把国内最领先的团队放到成都来，举全市之力支持，包括上游产业协同，这种是有可能性的。')
add_dialogue(doc1, SC1, 'Anson', '我们看重的点除了价格之外，算力（低成本高质量）、数据采集便利、应用场景、生态伙伴，这些是我们非常看重的。')
add_dialogue(doc1, SC1, '管委会代表', '融资额还是权重要大一块的对吧？')
add_dialogue(doc1, SC1, '明修', 'Anson说的点可能也是我们更看重的，大额投资方其实都挺多的。')
add_dialogue(doc1, SC1, '管委会代表', '你们大概什么规模、什么价码能谈总部落地？两种方式：直接谈总部，或者先买马（跟星动纪元一样先投一笔）。')
add_dialogue(doc1, SC1, '明修', '我们内部需要再沟通一下才能给答复。')
add_dialogue(doc1, SC1, 'Anson', '我们特别喜欢成都，各位领导也特别坦诚和认可，我们保持联系。')

doc1.save(out1)
print(f"文档1已生成: {out1}")

# ========== 文档2：团队算力、数采工作任务讨论 ==========

SC2 = {
    '明修': RGBColor(0x70, 0x30, 0xA0),
    '碧莹': RGBColor(0xC0, 0x00, 0x00),
    'Anson': RGBColor(0x00, 0x60, 0x00),
}

doc2 = create_doc(SC2)
out2 = r"D:\RoboX\04_听记纪要\转写与纪要\2026-08-12 18.56 团队算力、数采工作任务讨论（清理版）.docx"

add_title(doc2, '08-12 团队算力、数采工作任务讨论')
add_note(doc2, '参会人：明修（ROBOX CTO）、碧莹（团队运营）、Anson（ROBOX CSO）')
add_note(doc2, '时间：2026年8月12日')

add_heading(doc2, '一、模型训练规划')
add_dialogue(doc2, SC2, '明修', '先训一把，这把不带数据，用开源数据分开训练。System 2第一版大脑27到30B参数，要把推理、任务规划和简单agent能力优化一下。System 1打底256卡，按照非自回归架构，类似Pi 0和Pi 0.5。触觉这版单独训练。')
add_dialogue(doc2, SC2, '明修', 'System 2训练常驻，System 1也会同时训。System 2的scaling law上去后效果提升直接反哺操作模型。触觉大规模叠加在后面，第一版先不加触觉。')

add_heading(doc2, '二、算力卡需求与时间线')
add_dialogue(doc2, SC2, '明修', '算力爬坡计划：8月底至少32张H100；9月底128卡；10月底128加256卡；12月底512卡。统一按H100算。')
add_dialogue(doc2, SC2, '碧莹', '存储方面呢？')
add_dialogue(doc2, SC2, '明修', '存储用OSS，同一个区域的存储报社可以搞定。NAS正常配置。日本那批70台H卡，现在还不确定是H卡还是B卡，需要问清楚。')
add_dialogue(doc2, SC2, '碧莹', 'System 2训练是弹一下就好还是常驻？')
add_dialogue(doc2, SC2, '明修', '常驻。System 2训练时System 1也可能同时训，所以卡的需求要叠加。10月128+256，12月512卡左右。')

add_heading(doc2, '三、数据采集策略')
add_dialogue(doc2, SC2, '明修', '前期需要自采——我们需要知道要什么样的数据，根据最终要演示的任务或落地场景反推要采哪些任务。自采任务一定在自己场地先验证，才放心把需求派出去给别人。不太倾向于买现成数据，质量不可控。可以委托别人采（定制数据）。')
add_dialogue(doc2, SC2, 'Anson', '前期大量去买，同时也要采，采需要前置工作。采和买的关系和比例怎么安排？')
add_dialogue(doc2, SC2, '明修', '前期反而需要采。开源数据加仿真大概1万小时起步，真机demo 20到30小时。2.2版本开始翻倍。')
add_dialogue(doc2, SC2, 'Anson', '明修跟我说希望半年内逼近10万小时。')
add_dialogue(doc2, SC2, '明修', '对，6个月10万小时。之前按计划6个月5万小时，一年10万小时。现在提速到半年10万小时。10万小时一个月才4000多小时，需要项目化运作。')

add_heading(doc2, '四、Ego数据政府合作')
add_dialogue(doc2, SC2, 'Anson', 'Ego数据方面，现在在跟深圳和成都在谈，还没有到收敛阶段。杭州暂时不能谈——等第一轮融资和前期事情收敛一下才能跟杭州政府谈。需求已提给政府：需要他们提供场景，铺实相关门店、医院、大学、科研机构。AI for Science是跟政府提的主要方向。')
add_dialogue(doc2, SC2, 'Anson', '真机素材需要一个场地，明修说500平米差不多，需要十几二十台本体（灵巧手或机械臂），也希望政府能投资设备。在跟政府谈拢之前，合作方能不能先提供？')
add_dialogue(doc2, SC2, 'Anson', '长虹在四川有素材基地，他们CTO下周二过来，到时候可以把需求提给他。')

add_heading(doc2, '五、数据采集装置开发')
add_dialogue(doc2, SC2, '明修', '三种装置需要处理：APP（头戴采集）、异构装置（带触觉手套的全模态采集）、真机（可穿戴设备）。萌萌那套不能完全1:1搬出来——Pico太重，大概率得去掉。需要带深度的头部摄像头加带触觉的手套，还有全身定位方案。')
add_dialogue(doc2, SC2, '碧莹', '能做一个决策吗？直接买现成的，2万到10万一套的那种。')
add_dialogue(doc2, SC2, '明修', '可以同步做，不是二选一。自建一套用于验证（知道数据怎么用、怎么采、要哪些数据），同时调研外购方案。参考现有方案如果硬件不用再花时间，软件复刻（不带出资料），买板子加接口大概两周，整个采集链路一周看到效果。调试过程会持续。')
add_dialogue(doc2, SC2, '明修', '外购候选：奥比（有头戴设备，可谈定制带深度的整套方案，他们也做过假关节定位和外部摄像机）；光剑科技（有数据手套）。')
add_dialogue(doc2, SC2, '碧莹', '自建一个月都不一定把硬件打好。')
add_dialogue(doc2, SC2, '明修', 'bring up（点亮）一周，但整套采集链路开发加调试要两到一个月。DVT都不会做——更重要的是知道数据怎么用、怎么采、pipeline怎么样、模型怎么用。')

add_heading(doc2, '六、触觉手套与灵巧手设备')
add_dialogue(doc2, SC2, '碧莹', '触觉手套已到——带接触反馈/震感的手套，两套已买，9月到货，先借一套用。还有灵巧手也到了。')
add_dialogue(doc2, SC2, '明修', '这不是力反馈，是接触反馈、震感反馈。手套偏小，戴不到5G手上，但勉强可以用。举桥那边应该可以定制5G版本，可以寻源举桥。达摩院还要继续做数据，可以问萌萌举桥新一代手套到了没有。')
add_dialogue(doc2, SC2, '明修', '灵巧手转接件只剩一个了，原来配了三个。天机5G的接口跟一代手不一样，需要找天机先适配转接件。天机5G和5G不在一个群，需要拉群对接。相机支架可以找长虹那边黄一的师兄做。')

add_heading(doc2, '七、数据规模与节奏')
add_dialogue(doc2, SC2, '明修', '第一版模型需要1.5万小时。触觉占比1%到10%，需要评估。带触觉的Ego装置9月底前ready或者能开始采数据（10月开始采），然后看产能。100人一天400小时，一个月1.2万小时。触觉比例决定装置数量——1%就一套，10%就十套，十套是长虹出钱还是我们出钱需要倒推。')
add_dialogue(doc2, SC2, '碧莹', 'APP的Ego数据采集，给长虹在工厂采3万小时，真有意义吗？')
add_dialogue(doc2, SC2, '明修', '不在素材工厂，要去找真实场景——酒店、餐馆、工厂都有。需要提细的需求给长虹，看他们有多少场景。要diversity的场景才有用。')

add_heading(doc2, '八、Demo场景选择')
add_dialogue(doc2, SC2, '明修', 'Demo场景至关重要。如果做科学实验就要实验室场景，做养老就要康养场景，做服务就是商业场景——搭的场景完全不一样，难度高的任务需要提前准备。你们要尽快把demo场景定下来。')
add_dialogue(doc2, SC2, '明修', '真机搭完调好之后一周内确定demo场景。你们要确认好场景，找出能做的实验或功能有哪些，然后搭对应环境。14楼有家庭场景——冰箱、床、洗衣机等家具都送了，搭起来就能用。')
add_dialogue(doc2, SC2, '明修', '室内拍摄需要实时建图反馈。可以找光剑（有深度加双目摄像头），或者先用RealSense内部试一下。给出一段数据就能产生采集要求。')

add_heading(doc2, '九、团队招聘与行政')
add_dialogue(doc2, SC2, '明修', '需要嵌入式/Linux开发人员——类似赵峰、萌萌这样的角色，做软硬件结合。不是开发嵌入式系统，是做Linux开发。可以先招人挂在自己名下，需要资源再去推。')
add_dialogue(doc2, SC2, '碧莹', '钉钉企业版需要认证，要有营业执照。先创建组织、认证、然后买版本。5个人不够用，需要升级。')
add_dialogue(doc2, SC2, '明修', '碧莹，把语雀文档里算力爬坡计划改一下，文档迁移到钉钉。钉钉企业版我来处理认证。')
add_dialogue(doc2, SC2, '碧莹', '新电脑已买好，Mac可以来领了。明天就能领，后天也行。把想要的型号发给我。')
add_dialogue(doc2, SC2, '明修', 'H100利用率要提高，2500块钱一天。')

doc2.save(out2)
print(f"文档2已生成: {out2}")
