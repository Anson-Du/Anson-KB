# -*- coding: utf-8 -*-
"""Generate cleaned transcript Word document for 0818 BlueRun Capital & ROBOX meeting."""

from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

output_path = r"D:\RoboX\02_股权融资\0818 蓝驰资本&ROBOX（清理版）.docx"

SPEAKER_COLORS = {
    '徐老师': RGBColor(0xC0, 0x00, 0x00),
    '高豪': RGBColor(0xC0, 0x00, 0x00),
    '田明': RGBColor(0x70, 0x30, 0xA0),
    '明修': RGBColor(0x70, 0x30, 0xA0),
    '李欣': RGBColor(0x00, 0x80, 0x80),
    'Anson': RGBColor(0x00, 0x33, 0x99),
}

doc = Document()

# Page setup
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

# Default font
style = doc.styles['Normal']
style.font.name = 'Microsoft YaHei'
style.font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
style.paragraph_format.line_spacing = 1.5


def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_after = Pt(6)


def add_note(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.italic = True
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_after = Pt(4)


def add_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    # Bottom border
    pPr = p._element.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single',
        qn('w:sz'): '6',
        qn('w:space'): '4',
        qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)


def add_dialogue(speaker, text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    color = SPEAKER_COLORS.get(speaker, RGBColor(0x00, 0x00, 0x00))
    run_s = p.add_run(speaker + '：')
    run_s.font.bold = True
    run_s.font.color.rgb = color
    run_s.font.size = Pt(11)
    run_s.font.name = 'Microsoft YaHei'
    run_s._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run_t = p.add_run(text)
    run_t.font.size = Pt(11)
    run_t.font.name = 'Microsoft YaHei'
    run_t._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_after = Pt(4)


def add_summary_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(14)
    run.font.bold = True
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    pPr = p._element.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single',
        qn('w:sz'): '6',
        qn('w:space'): '4',
        qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)


def add_summary_item(text):
    p = doc.add_paragraph(style='List Number')
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Microsoft YaHei'
    run._element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_after = Pt(3)


# ==================== DOCUMENT CONTENT ====================

add_title('0818 蓝驰资本 & ROBOX 投资交流会议（清理版）')

add_note('时间：2026年8月18日 下午2:03 | 时长：1小时13分钟')
add_note('参会人：徐老师、高豪、陶博（线上）、明修、田明、李欣、Anson')

# ==================== KEY POINTS SUMMARY ====================

add_summary_heading('会议关键要点')

summary_points = [
    '蓝驰资本背景：前身硅谷战投，05年回国成立蓝驰，08年成立蓝驰中国，22年因贸易战完全切割。累计管20+期基金合计200+亿规模，最新一期40亿（人民币美元各半）。出资方含中关村、国家中小、上海国投、香港高校、新加坡/欧洲/中东高净值个人。23年起重点布局AI。',
    '蓝驰AI布局：模型层投了Moonshot/Kimi（四五轮）、Star；具身投了智云、踏实速度、逐迹动力、莫奇等；世界模型投了两家。投资逻辑两大方向：ASI（更高智能）+ 物理世界发展（具身智能布局原因）。只要有足够技术或产品差异化，愿意布局新团队。',
    'ROBOX团队：阿里达摩院核心具身智能团队，24年3月成建制成立，首批10位核心骨干覆盖预训练→后训练→数据管线→系统工程→解决方案全链路。报录比1000:1，核心算法负责人港中文背景。汇报对象为Xdian和集团总裁吴永明。',
    '出来原因：自身决定（需软硬结合做技术闭环，互联网偏软）+ 集团战略聚焦三大战役（通义大模型/AI应用/大消费闪购），具身智能改用市场化方式推进。已与Xdian、Wuma打招呼，集团表态支持。竞业6月底解除。',
    'RainBrain 1.1：122B参数千亿模型，7月16日发布。国内唯一被NVIDIA Cosmos 3 benchmark对比，多任务效果优于Cosmos 3。配套全无人机器人餐厅demo（煎牛排/拉椅子/工具使用等，一倍速真实展示，多本体同模型驱动）。',
    '大脑公司三标准：有技术报告敢于接受行业讨论 + 跨本体真机实验完整案例展示 + 被美国前沿团队benchmark引用——三个同时满足国内极难做到。',
    '模型演进：RainBrain 001（25年8月，首次证明ego-centric三视角数据+人类轨迹将下游任务成功率从50%提升至84.4%→90.6%，纯AR架构优于diffusion）→ RainBrain 1.0（增强物理空间理解）→ RainBrain 1.1（122B，千卡规模训练）。',
    'System 2/1/0分层架构：System 2（大脑，数据中心部署，122B，持续scaling，长上下文任务分解+工具调用+持续学习）→ System 1（小脑，同源蒸馏，纯AR非diffusion，享受大脑scaling红利，灵巧操作+触觉融入）→ System 0（端侧），三者通过latent space非语言交互，co-training时可等同同一模型。',
    'VLA架构瓶颈判断：action expert（diffusion）消耗算力约等于VLM同等规模，且VLM泛化参数不直接有助于action能力提升；高度耦合架构无法随数据规模增长持续scaling。纯AR + latent space交互才是最终范式。',
    '触觉数据策略：全行业触觉数据占比不到1%。ROBOX通过三层管线解决：仿真（原子技能恢复+触觉信号与视觉/语义对齐）→ 真机（真实触觉模态采集）→ ego-centric（触觉手套+RGB同构采集）。已实现小规模触觉未来预测模型。',
    '数据管线"一拖三"：全身动捕+手部触觉+ego-centric摄像头，由设备厂商量产，下游素材厂/场景方采集，ROBOX买数据。已有合作伙伴在产。目标12个月内推至100万小时。',
    '商业化两阶段：第一阶段TPF——"智能增量套件"（大脑模型+灵巧手+视觉传感器+后训练平台）服务中长尾本体厂商（已签四川机器人/长虹机器人）；第二阶段PMF——商业服务场景起步，杀手级应用方向：生物制药实验室→AI for Science→商业航天；最终走向家庭服务。',
    '与蚂蚁灵波对比：ROBOX比蚂蚁早半年成立，更早bet高自由度灵巧操作和System 2 scaling；蚂蚁灵波主要做夹爪，仍在做分拆（蚂蚁持大股）。团队吸引力大，通义/万象/灵波的人持续来找。',
    '对霍壳评价：夹爪定制末端+卡槽，单方向切豆腐，固定循环搅拌非真正搅拌——非通用操作。ROBOX用灵巧手操作工具完成通用任务，多个本体同一模型驱动。',
    '算力规划：当前192卡→年底512卡，历史峰值2000+卡。团队有千卡到万卡集群经验（通义万相背景）。已规划12个月算力预算，上游资源已联系完毕。',
    '融资进展：投前20亿估值，融2亿，领投7000-8000万（PE），多家在谈，已进入投资协议第一轮讨论。Eric Wang（CFO）已全职加入：阿里财务BP→金山CFO（与张宏江搭档）→Rokid CFO（正在上市），已全职加入ROBOX。',
]

for point in summary_points:
    add_summary_item(point)

# ==================== CHAPTERS ====================

# ===== Chapter 1 =====
add_heading('一、蓝驰资本介绍')
add_dialogue('徐老师', '蓝驰是国内成立比较久的机构，前身是硅谷的战投。老板是新加坡华人，05年从硅谷回来成立蓝驰，08年开始在国内做投资。22年后因贸易战完全切割。目前累计管了20多期基金，合计200多亿规模。最新一期是人民币加美元共40亿，人民币和美元大概一半一半，人民币稍微多些。人民币出资方主要是中关村、国家中小、上海国投等；美元那边更多元，包括香港高校、新加坡、欧洲、中东的高净值个人，基本是华人。从23年开始重点布局AI机会，投得比较激进。')
add_dialogue('徐老师', '模型层面投了Moonshot（Kimi），从第二轮开始一共投了四五轮。Star，跟Manus差不多但只在硅谷做了。具身这块投了很多，从最早的智云（通用），到后面的踏实速度、逐迹动力、莫奇等。新的一波做世界模型的投了两个。整体思路分两块：一是ASI，往更高智能走，可能通过self-evolving或新模型架构实现；二是往物理世界发展，这就是我们在具身上布局这么多的原因。新的团队只要有足够的技术或产品差异化，我们都愿意布局。')

# ===== Chapter 2 =====
add_heading('二、ROBOX团队背景')
add_dialogue('田明', '我们团队有几个大标签。第一，我们是阿里集团核心做具身智能的团队，之前主要汇报对象是达摩院总裁Xdian和集团总裁吴永明。核心骨干来自阿里达摩院具身智能实验室，24年3月成立，成建制做具身的团队，愿景是以最快速度触达物理AI的智能上限。')
add_dialogue('田明', '第一批10位核心leader覆盖了从预训练到后训练、数据管线、模型系统工程到解决方案架构和产品的全链路。第二个特点是有很核心的工作产出和积累，处于全球第一梯队。')
add_dialogue('田明', '主要工作是做具身智能的大脑系统。上个月发布了RainBrain 1.1，122B参数的千亿模型。做了很多真机展示案例，是全球首个类似Genesis的多机展示灵巧复杂操作。在美国Cosmos 3论文中作为国内唯一大脑模型做benchmark对比，很多任务上效果比Cosmos 3还要好。')
add_dialogue('田明', '如何判断大脑公司是否靠谱？三个观察视角：第一，有技术报告，敢于接受全行业讨论；第二，有跨本体真机实验完整案例展示；第三，被美国前沿团队作为benchmark对比引用。三个同时满足，国内绝大多数企业很难做到。')

# ===== Chapter 3 =====
add_heading('三、出来创业的原因')
add_dialogue('明修', '今天用人类知识教会机器人感知世界是共识，最终目标是让机器人走进家庭。但路径比较遥远，今天具身智能机器人在家里三小时叠几件衣服就会被人骂出来。如何找到合适路径让机器人具备灵巧操作能力和泛化智能，极其关键。短期要锚定一些高价值场景结合。')
add_dialogue('明修', '手眼脑协同是智能提升的最小闭环。手部是模型输出action的关键硬件载体，尤其是灵巧手；眼部是视觉传感器，是模型输入感知最关键的部分。同构的眼睛和手能最大减少不同构型之间的gap，跟大脑服务形成更好的技术闭环。')
add_dialogue('明修', '但在阿里集团这样的互联网公司里，更希望不碰硬件，模型最好都偏软。真正要做好这件事，一定是软硬结合。另外，团队是经验丰富的穿越周期的团队，达摩院报录比1000:1，核心算法负责人是港中文的，下面带清华、北大、浙大到南洋理工的小天才团队。')
add_dialogue('田明', '第二个原因是集团战略调整。阿里聚焦三大战役：通义千问大模型（大量烧资源保持第一梯队）、AI应用（豆包vs千问APP）、大消费（淘宝闪购）。具身智能改用市场化方式推进。两方面共同因素促成了出来创业。')
add_dialogue('徐老师', '所以出来是自己的决定，还是跟集团协商的决定？')
add_dialogue('明修', '本身是我们自己的决定，出来之前跟Xdian、Wuma都打了招呼。')
add_dialogue('田明', '集团层面也有表态。')
add_dialogue('Anson', '之前也出不来，都背着竞业。到6月底、7月份集团决定战略聚焦，这时就具备出来的条件了。')
add_dialogue('田明', '一方面是把事做好的因素，另一方面正好集团有调整，不会为难我们，还会给支持。')

# ===== Chapter 4 =====
add_heading('四、技术路线与行业走访')
add_dialogue('明修', '今天单纯的VLA或world action model是不是最终走向智能上限的范式，需要打个问号。现有VLA把苹果从桌上拿到盘子里作为一个技能单元，这种方式不可能真正产生最终智能。对智能的定义：泛化只是很小一个维度，如何让模型持续提升对物理世界感知的baseline才是关键。')
add_dialogue('明修', '灵巧操作在今年初之前几乎没有人提。我们走访了全行业50+企业，发现要解决具体灵巧操作任务时，全行业都做不到。接触是至关重要的，手部灵活度也是。没有触觉时能做什么、不能做什么，很少人能讲清楚。')
add_dialogue('明修', '2月份走访了50+企业，包括自变量、星图赋能、星海图、千寻、星动纪元等。当时给他们一个无人机器人餐厅的任务，让各厂商做demo。结论是：本体灵巧度决定智能下限——如果连遥操都做不到，就别谈智能了。大部分企业当时要么是低自由度灵巧手，要么是夹爪，基本无法完成任务。')
add_dialogue('明修', '从模型角度，即使允许定制末端，在煎牛排过程中对不同牛排、不同黄油形态的操作，模型厂商也很难做到。不论简单还是复杂任务，模型本身都处在极早期阶段。所以最终只能自己做。Day one就开始做高自由度灵巧手的灵巧操作模型。')
add_dialogue('明修', '7月16日发布了新模型和全无人机器人餐厅所有角色的任务demo。一倍速，统一大脑驱动，架构型机器人本体完成灵巧复杂操作。这是第一款双足人形机器人（宇树本体），包括拉椅子推椅子的全身运动控制，天机5G灵巧手双臂协同使用工具，从开火到把牛排从生做到熟的完整智能驱动实现。')
add_dialogue('田明', '视频风格跟Genesis的H26.5非常像。轮式底盘双臂是星辰智能机器人，同一模型也做了适配。同一个模型兼容了夹爪、自由度手、三自由度低自由度手，多种本体混合在一个模型里。')
add_dialogue('明修', '模型相比GR00T 0.7和0.5、OpenVLA，效果都好很多。项目主页有一镜到底的代码和开源模型。')

# ===== Chapter 5 =====
add_heading('五、模型演进：RainBrain 001到1.1')
add_dialogue('明修', '最早25年6月发布World VLA，全行业首个将world model和action model相结合的范式，两者抽离力帮助安全模型做得更好。迭代正式版本RainBrain 1.1，行业里很早在做人物模型验证的团队。')
add_dialogue('明修', '25年8月发布RainBrain 001。实际探索追溯到24年底，最早做具身智能时就在想如何scaling。专门做了APP让玩家协同玩游戏采真机数据，但发现速度和成本过大。于是思考能否用人类数据。第一视角更符合机器人看到的视角，也更容易让模型理解，因为人手操作跟机器人末端轨迹是匹配的。')
add_dialogue('明修', 'RainBrain 001是全行业最早用ego-centric三视角数据以及人类轨迹数据帮助模型效果提升的工作。在通用VLM backbone基础上，发现下游任务成功率只有50%左右。加入ego-centric数据做feature prediction后提升至84.4%，进一步引入人类轨迹（FVAE形式，加入3D信息），成功率提升至90.6%。纯AR架构优于OpenVLA离散预测或接MLP做回归。')
add_dialogue('明修', '生成action相比生成复杂画面和video应该更简单。全身关节31个自由度，加上高自由度灵巧手22个，不到80个自由度，在物理约束下的action space完全不需要用diffusion这样更复杂的结构。Action VAE是System 2和System 1最终同源的最佳选择。')
add_dialogue('明修', '26年2月发现所有模型都用了VLM backbone，思考是否有瓶颈。做消融实验后发现：提升基模能力后对下游任务有下限提升。于是在通用VLM基础上增强物理空间理解（replay工作），对操作和导航相关下游任务都有很好的效果提升。同期英伟达Cosmos 3把我们工作引用进去并做了benchmark对标。7月发布的模型又在Cosmos 3基础上做了很大提升。')
add_dialogue('明修', '从本质上提升world model层面的物理空间理解能力，才是将具身智能下限提到新台阶的根本思路。具身智能不只是VLA，还包括未来有工具调用的人机交互，这些都应该发生在System 2（大脑模型）层面。所以更聚焦以大脑模型为切入口提升全栈模型能力。')

# ===== Chapter 6 =====
add_heading('六、System 2/1/0分层架构')
add_dialogue('明修', '行业大部分厂家更多面向操作层面（VLA或action model）。VLA本质是VLM加action expert，得部署在机器人本体上才能完成连续操作，否则action chunk之间抖动或网络推理延迟会导致连续型任务失败。模型锁定在有限算力下，规模受限。')
add_dialogue('明修', '受限有两个点：一是很大的VLM要理解语言能力，二是diffusion不论是1000 step优化到flow matching 10步或4步，400M左右的action expert乘4就接近2B推理算力，占到了VLM同等大小。英伟达的Posem 13中间事件模型也是类似思路，直接将reasoning power的参数copy过来。两者遇到同样问题：要提升模型尺寸就会受限。')
add_dialogue('明修', 'VLA里VLM学到的泛化参数并不直接有助于action model提升能力下限。英伟达Cosmos 3用reasoning tool的基模能力（语言和图像多模态理解）作为初始化提升生成塔下限，思路是对的，但高度耦合架构不会是最终范式。假设数据规模从几万小时到百万小时到千万小时，模型尺寸一定会上去，天然受限。')
add_dialogue('明修', '我们提出新的模型架构设想：蓝色部分跑在数据中心，RainBrain 1.1最大122B，持续提高尺寸吃下更多数据。Action model必须能享受这个上限提升带来的好处，所以必须跟数据中心的brain同源。不是diffusion架构，而是纯AR架构加action生成能力，在RainBrain 001里已验证效果不错。')
add_dialogue('明修', '大尺寸、规模持续提升、吃下更多模态数据、具有上限智能的大脑，结合同源小脑，中间通过非语言方式交互（latent space变量）。大脑的高层意图信息隐含在latent space里带出来，作为condition让action model生成对应action。这是分层解耦的思路。')
add_dialogue('明修', '我们在实践过程中得出这个结论，可能架构思想跟元测未来等类似，但走得更扎实更远，已经迈出这一步了。RainBrain核心是通过语言caption引导，让模型在多模态通用基础上学习对物理空间的感知、推理和定位能力。')
add_dialogue('明修', '思路简单粗暴：在caption层面增加对物理画面或video里空间信息的描述——有多少物体、相对位置关系、完整trajectory。通过next token prediction天然让模型加强物理空间理解。相比GPT-4o等通用多模态模型有很好的效果提升，比英伟达Cosmos 3最大规模模型效果也更好。用掉的卡片规模接近千卡。')
add_dialogue('明修', 'RainBrain 001三个最大贡献：一，首次证明通用模型下游50%成功率基础上，加入ego-centric数据做feature prediction能提升至84.4%；二，引入轨迹抽象（FVAE形式）将人手轨迹加入预训练，成功率提升至90.6%；三，纯AR架构优于OpenVLA离散预测或接MLP回归。')
add_dialogue('明修', 'World VLA和VLA 002验证了未来画面预测对训练的重要性：没有未来画面预测会有30%效果损失。相比全行业现在讲的世界模型，我们要早6到12个月。从System 2入手做同源System 1 action model能吃到泛化红利，纯AR结构才能兼容。System 1和System 0已天然实现latent space交互，未来System 1和System 2通过latent space交互更符合第一性原理。Co-training时三者可等同同一模型，只是推理阶段拆到不同部分。')
add_dialogue('徐老师', '这个system升级的定义是行业标准定义，还是我们自己提的？')
add_dialogue('明修', '我们很早就提了，从自己的业务和模型研发角度出发做的思考和总结。')
add_dialogue('Anson', '明修现在这种三层架构是不是也不能说行业已经有共识？')
add_dialogue('明修', '行业还没有完全有共识。')

# ===== Chapter 7 =====
add_heading('七、触觉数据策略')
add_dialogue('明修', 'Action模型还有一个重要模块缺失——触觉模态，System 2和System 1都需要。想象一下，如果我拿一根针捏两头，大脑能想象出针头刺到肉的感觉和疼痛感，这都是在大脑里想象发生的。但全行业触觉数据在具身智能数据里占比不到1%。相比模型架构，更要解决触觉数据从哪来的问题。')
add_dialogue('明修', '现在让机器人拿铲子旋转换个姿态，基本没有公司能做到。这是遥操从手套或手映射到灵巧手上的对齐问题。我们的思路：人类从小孩开始从基本原子能力学起——捏、五指捏、两手捏、揉搓等，慢慢学会跟多种物体交互。在ego-centric路线里，我们已有渠道获取大规模人类手部精细操作的各种类型和场景数据。')
add_dialogue('明修', '从1~3D数据中可以恢复人类操作的原子技能（捏放、推拉拽、揉等），在仿真里可以将原子技能变成模型可驱动的能力，同步采集触觉信号。仿真里绿色点是触觉信号，白色点是RGB恢复的3D信息，本质上把触觉模态跟视觉和语言模态做了一次对齐。')
add_dialogue('明修', '推、拉、拽、捏、揉是几十上百种技能，日常摸到的物品种类悟性是有限的（雪碧、可乐、芬达手感类似）。进一步在真机上部署，采集最真实的真机触觉模态数据，强化原子技能。再加上ego-centric操作，在纯RGB基础上增加触觉手套采集同构人手操作的触觉模态。但人手和灵巧手姿态有gap，真机是最终对齐的最高质量数据。')
add_dialogue('明修', '已做了简单尝试：用有限数据规模做模型对触觉模态做未来预测。绿色点是模型预测与真实触觉信号一致的部分，红色是不一致的部分。随着数据规模扩增效果持续提升。关键是继续完善数据管线实现大规模采集。')

# ===== Chapter 8 =====
add_heading('八、数据管线与采集方案')
add_dialogue('明修', '数据规模是另一道坎。英伟达最近发100万小时数据，国内卢策吾发布50万小时（真正用到模型里的只有7万小时），千寻说有20万小时。真实超过10万小时规模数据送进模型训练的极少。')
add_dialogue('明修', '达摩院内部有完整数据管线，核心为内部模型训练服务，采集更多规模化数据。但不全自己采集，更多是做好参考设计，让合作伙伴做量产。数据厂商都希望有模型厂商驱动，告诉数据应该怎么采。')
add_dialogue('明修', '正在跟摄像头厂商、设备眼镜厂商合作，由他们量产带全身动捕+手部触觉+ego-centric的摄像头的全模态数据采集设备。也有简单手机方案做大规模数据采集，或手机外接双目加深度摄像头做更深度模态采集。三者组成完整数据装置解决方案。')
add_dialogue('明修', '下游场景方（素材厂）在自己真实场景里采集。素材厂也不知道买谁家设备好、数据采集出来能不能用，所以很愿意跟我们合作。我们告诉他们要什么设备、什么场景，帮我们采集，我们买数据。已有一批合作伙伴在做这件事。RainBrain模型就是以合作形式找他们买数据训练出来的。')

# ===== Chapter 9 =====
add_heading('九、商业化路径与产品形态')
add_dialogue('明修', '36个月规划：第一年将System 2/1/0全栈模型管线跑通，随数据规模提升实现正向闭环。结合上下游伙伴快速将数据规模推到100万小时。')
add_dialogue('明修', '第二年结合高价值落地场景做模型上线提升，包括精巧灵巧操作（机器人带触觉后才能做好、人类做得不太好的场景）。跟下游本体厂商一起打磨手眼脑协同系统。模型成熟度相比本体成熟度会更好。')
add_dialogue('明修', '第三年尝试在商业场景里提升模型智能，积攒进入家庭的技能。快速进入家庭实现模型智能提升和数据闭环，让机器人在家庭生存8小时，才有机会进一步提升智能上限。')
add_dialogue('田明', '团队介绍：我是项目创始人陈明修，田明是产品负责人，李欣是算法负责人（港中文博士，Google Scholar引用上万，主导过东南亚小语种LM+CL及VideoLlama 1/2/3三代负责人，做过大规模预训练）。')
add_dialogue('田明', 'CFO Eric Wang：曾阿里集团财务BP，后跟张宏江搭档在金山做CFO，现在Rokid的CFO（Rokid正在上市），已全职加入我们，帮Rokid做完上市工作。')
add_dialogue('明修', '具身智能赛道充斥大量非共识判断，过去两年真金白银将判断转换成工作，领先行业6到12个月。现阶段共识大概是我们6到12个月前做的工作。未来从System 2入手继续提升模型上线将是重要突破口。')

# ===== Chapter 10 =====
add_heading('十、问答：三层架构训练特点')
add_dialogue('徐老师', '这个三层计算架构，从模型训练上有什么特殊的地方？')
add_dialogue('明修', '相比VLA，我们坚信同源的大脑蒸馏出小脑，远比从通用VLM提升上限要好。Action expert不可用，Action VAE是我们的重要发现。生成action的复杂度远不如生成图像，action VAE足够。通用模型没有很强物理空间理解——Qwen VL在感知、推理和定位方面远不如RainBrain。这是具身原生foundation model的重要能力体现。')
add_dialogue('徐老师', '意思是从大模型生出一个小的？')
add_dialogue('明修', '对。大脑会持续提升整体能力，包括工具调用、长期记忆、持续学习，最终实现以第三视角人类示范的技能学习新范式。')
add_dialogue('田明', '技术差异化总结：第一，分层架构里做了重大改进——已通过实验证明从System 2蒸馏出System 1对快慢脑协同效果很好。System 2的长上下文能做长程任务分解，对智能提升很有帮助。第二，System 1核心是把触觉规模化融入，涉及触觉世界模型和触觉与VLA协同，主打灵巧操作能力。把长上下文规划跟灵巧操作两个核心feature打出来。')
add_dialogue('田明', '手眼脑协同方面：数据管线上对数据素材做重构，将来视觉传感器装在机器人本体眼睛上gap最小，触觉手套跟灵巧手同理。')

# ===== Chapter 11 =====
add_heading('十一、问答：基础模型物理理解')
add_dialogue('徐老师', '李欣提到基础模型的物理理解会更强，这个是怎么实现的？')
add_dialogue('李欣', '我们的模型更关注物理空间。不仅理解语言和整张图片，更理解图片的某一区域以及时间维度上的变化趋势。加了很多这样的数据做预训练，所以在物理空间理解上会有提升。')
add_dialogue('明修', '通过语言的caption范式去引导模型，比纯world action model或纯语言场景预测未来画面，学习到的更加本质和直接。')
add_dialogue('李欣', '模型可以理解任意粒度的视觉信息——给一张图片，可以给任意指代：一个bounding box、一个mask、一个坐标或坐标组合，只要是一个区域都支持理解。我们自己构建了很多第一视角数据，通过数据管线构造了物理空间理解和推理。')

# ===== Chapter 12 =====
add_heading('十二、问答：Agentic能力与分层交互')
add_dialogue('徐老师', 'System 2很重要的一点是agentic能力，去执行长程任务。具体技术点是什么？')
add_dialogue('李欣', 'agentic最重要的是在长程任务中在合适时间点决定调用或不调用工具。涉及调用工具就会涉及跟System 1的交互。现在训练VLA基模的数据都是非常简单清晰的短程任务指令（如把杯子从A点拿到B点），而且都是positive example，没有否定表述，语言歧义性理解是不够的。')
add_dialogue('李欣', '大脑模型调用工具时是不是只能通过语言？语言天然有歧义性。我们希望可以直接给视觉坐标、box或mask等任意模态输入，System 1都能理解并完成操作。所以要做co-training——让它更有办法理解语言，给更多条件，可以是结构化输入（坐标框、截图分割的mask等）。理论上给更多条件不会比只给语言差。')
add_dialogue('田明', '语言是人类沟通方式，描述物理世界本身就很抽象。')
add_dialogue('李欣', '语言其实是一个不完全观测。有很多种方式可以把物理世界信息给到操作模型。')
add_dialogue('田明', '分层架构核心要解决的问题是分层之间信息传递如何高效而准确。一定在特征空间里做，同源架构可以很好把System 2 scaling学到的东西继承到System 1。已做了对应路线的实证结果。System 2看到action expert有明显约束，把结构做优化后可以更快把scaling堆上去。')

# ===== Chapter 13 =====
add_heading('十三、问答：数据采集与场景规划')
add_dialogue('徐老师', '数据层面我们现在主要就是自己做那个一拖三的数据管线？')
add_dialogue('明修', '对，一拖三数据管线。')
add_dialogue('徐老师', '从场景上想先切偏商业服务，后续再到家庭。需要专门搜集这类场景的数据吗？')
add_dialogue('明修', '数据分两块：第一，采集足够diverse的家庭场景数据。做RainBrain时进入过上干个家庭，面向的不是最终选的那个家庭，而是每1000个不同房子里足够diverse的场景，对空间理解是通用的。第二，通用数据基础上针对专用场景采集——比如生物实验的透明器具、橡胶、滴管操作，以及做咖啡、酒店等商业场景。目标是更diversity加专用场景。')
add_dialogue('田明', '预训练主要把数据多样性规模做出来，后训练聚焦到场景里沉淀数据。')
add_dialogue('明修', '核心做短线——快速完成数据质检恢复和效果验证，下游伙伴帮我们采集。')

# ===== Chapter 14 =====
add_heading('十四、商业化路径与产品定义')
add_dialogue('田明', '整体路径分两个大阶段。现在具身智能还在第一阶段——技术与产品契合（TPF）。重要事情是把技术scaling水位快速抬上去，定义出智能的最小闭环，需要基础产品形态：具身智能大脑（模型分层服务）+灵巧手硬件+视觉sensor=智能增量套件组合，再加后训练平台。第一阶段就可以服务于中长尾机器人本体供应商，已有定的合作，如四川机器人、长虹机器人。')
add_dialogue('田明', '第二阶段PMF要打几个关键领域case。站在未来看具身智能通用技术的杀手级应用：AI革命本质是人机共生关系分工再调整，机器人挑战创造力和生产力上限。很看好从生物制药公司实验室的灵巧复杂操作，逐步走向AI for Science，再到具身智能与商业航天结合的蓝海市场。另外人逐渐拓大成消费者，家庭服务是机器人造福每个人的愿景。')
add_dialogue('田明', '倒推回来更倾向商业服务，半开放环境可以打磨任务成功率、稳定性、效率和安全，最终才能去全开放的家庭。')
add_dialogue('明修', '现在还比较早，更多还是提升模型。有很多线下伙伴需要模型，我们基模可以私有化或license，他们做后续链路交互。')

# ===== Chapter 15 =====
add_heading('十五、线上问答：煎牛排demo与霍壳对比')
add_dialogue('高豪', '您最开始展示的煎牛排demo，前段时间霍壳也发了一个麻婆豆腐。您对霍壳的技术路线有什么了解？感觉像Cosmos那种。')
add_dialogue('明修', '霍壳大家可以关注细节动作：拿刀前用夹爪夹起来，刀柄是方形的；夹爪拿上刀后另一只手要推一下把刀推到卡槽里，夹爪上面还做了卡槽。切豆腐只有一个方向，豆腐稍微换个位置就不能工作了。最后煮豆腐搅拌过程是固定转圈圈，不是真正搅拌——人类搅拌是通过豆腐性状判断应该伸向哪。所以核心展示的是：我们通过人手/灵巧手操作工具完成通用任务，而不是为刀定制末端。多个机器人两台，每个末端有差异，为完成任务长出四只手。')
add_dialogue('高豪', '煎牛排用的是手，后面换成夹爪，那是？')
add_dialogue('明修', '所有机器人用的是同一个模型。而且所有机器人用同一个模型效果比每个机器人单独做post训练还更好。')

# ===== Chapter 16 =====
add_heading('十六、线上问答：触觉模型与数据精度')
add_dialogue('高豪', '触觉这块用的是自己做的模组还是TLC的？')
add_dialogue('明修', '第一阶段做原子技能恢复用的是CHARON（视触觉）。但规模化手套时可能不选视触觉，因为戴上后对真实采集操作手感影响很大。在跟伙伴做五感触觉手套，行业上现在能选的不多。')
add_dialogue('高豪', '如果做触觉视觉模型，仿真里可以拿到object pose和mesh，但如果用真人ego data或真机器人，没有Oracle的object pose，精度能保证吗？')
add_dialogue('明修', '在仿真里拿到真实object 6D pose只是做teacher模型学习，最后蒸馏出一个基于纯视觉的小模型做视觉约束，不会再用仿真里的帧值了。')
add_dialogue('高豪', '现在能判断比如抓苹果时食指或大拇指移动了距离，然后预测下一步位移吗？')
add_dialogue('明修', '现在已经在削梨子了，可以施加任何方向的力，目标是维持稳定。')
add_dialogue('高豪', '模型可以在action执行之前就draw出来很多受动动作了？')
add_dialogue('明修', '对，是的。')

# ===== Chapter 17 =====
add_heading('十七、算力与人才')
add_dialogue('徐老师', '之前在达摩院的时候有多少卡？')
add_dialogue('明修', '做了12个月规划，现阶段卡片在爬坡，下周到192卡，年底到512卡。6个月左右有一版模型要发，重新签卡。上游资源都联系完了。常驻约300多卡，弹性出去千卡级。最多时2000多卡。')
add_dialogue('田明', '团队核心很多人在几千卡到上万卡大规模集群里做过事（通义万相背景），对当前具身智能领域的模型scaling有降维打击的先机。')
add_dialogue('徐老师', '人才梯队方面？')
add_dialogue('明修', '人才反而没那么担心。现阶段已十多位了，持续有通义、万象、灵波的人来找我们。团队出来后吸引力很大，阿里内所有做操作的部分基本没地方去了。')
add_dialogue('徐老师', '灵波也做分拆？')
add_dialogue('明修', '蚂蚁灵波也做分拆，但蚂蚁持了很大股份。对我们团队来讲，真正创业机会更大。')
add_dialogue('田明', '我们比蚂蚁成立还早半年，而且更早bet灵巧操作——他们主要做夹爪，我们核心攻克高自由度灵巧手操作。第二我们相信System 2将来能快速scaling，这是显著差异。')

# ===== Chapter 18 =====
add_heading('十八、融资进展')
add_dialogue('明修', '融资方面，刚出来一个星期，已经进入到close，正在聊投资协议第一轮。第一轮估值20亿（投前），融2亿。')
add_dialogue('徐老师', '领投单笔金额是多少？')
add_dialogue('明修', '七八千万。')
add_dialogue('徐老师', '就大PE了。')
add_dialogue('明修', '对，领投。都是open的。')
add_dialogue('田明', '不止一家，几家有活动，还在确认。前两轮更多是长期合作伙伴。')
add_dialogue('徐老师', '好的，我们这边没什么问题，同事后面会讨论一下。')
add_dialogue('田明', '感谢感谢。')
add_dialogue('徐老师', '感谢感谢。')
add_dialogue('田明', '线上老师我们就先到这里了，拜拜。')

# ==================== SAVE ====================
doc.save(output_path)
print(f'文档已生成：{output_path}')
