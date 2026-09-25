# -*- coding: utf-8 -*-
"""Generate cleaned transcript Word document for 08-17 ROBOX team prep meeting with Changhong."""

from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

output_path = r"D:\RoboX\06_产业生态\长虹\0817与长虹沟通会准备讨论会（清理版）.docx"

SPEAKER_COLORS = {
    '碧莹': RGBColor(0x00, 0x80, 0x80),
    '山相': RGBColor(0x00, 0x33, 0x99),
    '田明': RGBColor(0x70, 0x30, 0xA0),
    'Anson': RGBColor(0xC0, 0x00, 0x00),
    '明修': RGBColor(0x70, 0x30, 0xA0),
}

doc = Document()

# Page margins
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

# Default font
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
    p.paragraph_format.space_before = Pt(6)


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
    # Bottom border
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single',
        qn('w:sz'): '6',
        qn('w:space'): '4',
        qn('w:color'): '1F4E79'
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
        qn('w:val'): 'single',
        qn('w:sz'): '6',
        qn('w:space'): '4',
        qn('w:color'): '1F4E79'
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


# ======================== DOCUMENT CONTENT ========================

add_title("0817与长虹沟通会准备讨论会（清理版）")

add_meeting_info("时间：2026年8月17日 22:18 | 时长：22分47秒")
add_meeting_info("参会人：碧莹、山相、田明、Anson、明修")
add_meeting_info("主题：明天（8/18）与长虹团队8人对接会的内部准备会")

# ======================== KEY POINTS SUMMARY ========================

add_summary_heading("会议关键要点总结")

summaries = [
    "硬件合作模式确定：ROBOX卖基础款数采装置给长虹，长虹在基础款上做腰部自由度定制。ROBOX出方案和标准，长虹7人硬件团队负责执行。定制完成后方案告知ROBOX，可直接复刻，无需长虹交付。",
    "数据采集分两条线推进：素材厂数据采集9月初开始、9月底完成1000小时；真实场景（酒店）数据采集需硬件定制完成后启动，预计9月底至10月初。",
    "10月开源里程碑：10月开源1000小时灵巧操作数据集（世界最大）+ baseline模型。融资节奏驱动，11月投资人放假前必须完成开源。",
    "长虹两个核心诉求：①长虹集团名义战略投资ROBOX（交叉持股或单方面投资）；②成立合资公司。ROBOX态度open，合资公司暂不建议。",
    "ROBOX核心诉求三点：①意向采购订单（POC合同）用于内部推进；②硬件定制支持（腰部自由度+移动）；③太空舱场景demo支援。",
    "MOU策略：MOU内容往宽泛写，保留解释空间；实质性合作要点在会上对齐，让长虹团队带回去向董事长汇报，为董事长下次来访直接拍板铺路。",
    "角色分工明确：田明主说MOU每一条现场对；碧莹补充+记todo；Anson追问战略投资和协议要点；明修负责技术方向。Anson负责整理今晚讨论要点发群。",
    "太空舱场景：已获省领导认可，长虹自己立军令状做demo，ROBOX提供硬件定制支持。省领导已找地方推动长虹实施。",
    '开源生态策略：开源数据+baseline模型，吸引所有人来ROBOX测试，建立生态壁垒。明修强调"过时不候"，很快会被超越。',
    '融资紧迫性：田明指出"钱推着你走"，不是为加班而加班，10月数据开源是融资关键节点。拿不到钱大家就over了。',
    "硬件简化原则：数采装置不需要产品化，不需要ID设计，能控操作采数即可。但需保证基本稳定性，不能推到酒店就故障塌掉。",
    '主线梳理（山相总结）：硬件定制（长虹支持）→数据采集（联合开源）→模型主导（ROBOX），形成"硬件-数据-模型"合作主线。',
    "明天会议安排：8月18日10点与长虹8人团队对接，现场逐条对齐MOU。长虹带着投资部任务来，ROBOX需把所有诉求讲清楚。",
    "会议纪要机制：Anson整理今晚讨论要点发群，田明逐条@到人，谁负责提哪条明确分工。碧莹对应每条MOU内容记todo。",
    "后续行程：后天去广州长虹，然后去北京；PPT约下周二早上early bird时间。确认周宇是否参加明天会议。",
]

for i, s in enumerate(summaries, 1):
    add_summary_item(i, s)

# ======================== CHAPTERS ========================

# Chapter 1
add_heading("一、硬件定制合作模式")

add_dialogue("碧莹", "那个硬件的合作，在定制之前，我们可以先让他给我们做一个带臂的本体，或者加一个小的。")

add_dialogue("田明", "就是腰部自由度嘛，你把那方案给他。本体定制我们是甲方，我们出钱的，他用BOM成本给我交付。")

add_dialogue("碧莹", "我们让他买这一套，我们希望这一套也加一点点定制，就是他定制，然后他给我们买。他买基础版，他自己开发就开发了，硬件还是加点钱卖给他。")

add_dialogue("田明", "可以，就是说他只买我们的基础版，反正最后他改完的东西，如果我们要买，我们就按照增值的那个价格买回来就好。")

add_dialogue("碧莹", "我们也不用买，他改完那个东西告诉我怎么设，复刻一下就行了。不需要他来交付，交付的是那个定制的，这是两套——这套是个很简陋的，只是能动就行；另一套是真正的轮式双臂的，那一套给我们就好。")

add_dialogue("田明", "这样简单一点。你反正要啥，他给你搞啥嘛。他这次来8个人，就是为了把各个方向的人直接现场给你对了。然后你要告诉他的时间节点，他能不能有他的这7个人给你保障。他所有硬件人就围着你一个事干。")

add_dialogue("山相", "像我们现在这一套不是说所有都有，我们其实还缺里边一些东西，比如说相机支架我们是没有的。这个不是自购，是他们找个人画个图就能出来的，只是我们现在这边没有这种能力，需要他们帮我们画出来。")

add_dialogue("田明", "那就聊聊，别收钱了，顺便帮我画了算了。他有设计师。")

# Chapter 2
add_heading("二、数据采集时间节点")

add_dialogue("碧莹", "请问1000小时的数据什么时候开始采？开始采的时候是硬件要running的时间。9月初行不行？")

add_dialogue("田明", "可以，他先9月初评估，如果不行他再报一个时间，我们看能不能接受。他们回去就加班开始搞。")

add_dialogue("碧莹", "结束就是9月底，一个月能不能采1000小时的数据？做到10月。而且我们这个要的是真实场景，就不是素材厂那种。")

add_dialogue("山相", "真实场景的话，你必须得把那个腰部、移动那些自由度定制好才能采。9月初ready不了，他们硬件也ready不了，两个礼拜不可能。至少至少一个月的时间。")

add_dialogue("碧莹", "那就是9月中旬呗。")

add_dialogue("山相", "9月中旬，下旬。只是他们硬件ready的周期。然后硬件ready，你那些要进家庭采集，总不可能所有东西都挂着网线吧？")

add_dialogue("碧莹", "我觉得这个事情真的得重检，你这个有点过于那个啥了。")

add_dialogue("田明", "明天硬件来了，你现场简单对一下。")

add_dialogue("碧莹", "他定的时间，我不乐意怎么办？现场我们俩吵起来了，不太好。")

# Chapter 3
add_heading("三、真实场景采集讨论")

add_dialogue("山相", "你数据得分不同样式。如果是素材厂里边去采的，那可以很快发出来。但你要是拉到酒店或家庭里边去采，就没那么快。")

add_dialogue("碧莹", "那素材厂是什么时候？")

add_dialogue("山相", "素材厂就是9月初就可以开始采了。9月底完成1000小时。这是两码事。")

add_dialogue("碧莹", "9月底可以到真实场景吗？")

add_dialogue("山相", "9月底是100%不行。真实场景得重新评估。感觉差不多得一个月多点，就是9月底。新城他们那一套至少搭了有半年了。")

add_dialogue("碧莹", "但我们不要新城那样的。也不是说随便敲你家门就进你家采，肯定是一个固定酒店、固定的房间，只是把这个房间改成素材厂那种感觉。")

add_dialogue("山相", "那这和素材工厂有什么区别吗？他可以把素材工厂也布置成那样。")

add_dialogue("碧莹", "其实是很难的，你的光照啊、空间感啊，但是素材工厂都是现成的这种房间，1:1复刻的。")

add_dialogue("山相", "酒店真实场景要采什么任务？")

add_dialogue("碧莹", "就可能是整理一下垃圾呀，擦一下桌子呀，叠一下床上的一些衣服啊。")

add_dialogue("山相", "叠衣服，酒店应该没有叠衣服的需求。")

add_dialogue("碧莹", "有啊，你住酒店不给你叠衣服吗？都是叠好的。")

add_dialogue("田明", "反正把衣服塞到洗衣机里面是有的。没关系，反正这个玩意将来也是用的嘛。")

add_dialogue("碧莹", "那九月底十月初吧，肯定不是一个场。")

# Chapter 4
add_heading("四、融资节奏驱动")

add_dialogue("碧莹", "你肯定10月就得开放这批数据了呀。11月份不行，11月份投资人都不投资了，都搁那写投资报告了，投资人都放假了。")

add_dialogue("田明", "他采的人可以无限扩，但是你硬件反正就有限嘛。")

add_dialogue("碧莹", "真的10月份我们要开一批数据的时候，这批数据最好有一部分是真实场景。我是觉得酒店是一个比较好采的场景，相对来说比较封闭，有点素材。")

add_dialogue("田明", "所以创业公司急，他不是光急在办事上，他是急在融资节奏上。钱推着你走。不是大家为了加班而加班，赶节点。")

add_dialogue("碧莹", "如果拿不到钱，那大家就over了。")

add_dialogue("田明", "肯定是拿钱，钱推着你走。")

# Chapter 5
add_heading("五、长虹战略合作诉求")

add_dialogue("Anson", "他不是之前要提出跟我们交叉持股，这方面我们的态度是什么？")

add_dialogue("田明", "open的。他两个诉求：一，长虹集团名义可以单投我们，就是战略投资我们；第二个是跟我们成立一个合资公司。到时候可以跟Eric商量。")

add_dialogue("碧莹", "我不建议合资公司，我知道人就少，又要分出去一部分。")

add_dialogue("Anson", "战略投资的事情是我们明天也需要提出来的，是吧？")

add_dialogue("田明", "要提，因为他是带着任务来的，他这个任务就是投资部给他的任务。")

# Chapter 6
add_heading("六、10月开源数据与模型策略")

add_dialogue("碧莹", "我们希望10月份一起把这个1000小时的世界上最大的灵巧操作的数据集开放出去，其中有一定比例是真实场景下的。")

add_dialogue("明修", "然后为什么要做这件事？因为做了这件事之后，所有人有了一个基础数据，用这个数据训练了之后都会来你这测。然后我们还发模型，告诉你baseline在哪。而且过时不候，因为很快。")

add_dialogue("碧莹", "这个模型也是，而且这个数据也非常有意义，是世界上最大的，也是目前非常稀缺的灵巧操作数据。")

add_dialogue("明修", "他人已经有了，现在核心是忽悠他买机器。")

add_dialogue("田明", "然后他那边能给你们扩人嘛。")

# Chapter 7
add_heading("七、ROBOX核心诉求：意向订单与场景支援")

add_dialogue("Anson", "我们最想要什么，我们自己清不清楚？")

add_dialogue("碧莹", "我想要的是POC合同。")

add_dialogue("明修", "意向订单合同。")

add_dialogue("碧莹", "对，还想要的是带场景。")

add_dialogue("田明", "但他肯定要确定真正的买单方，比如说是事业单位或者政府那边，这个是他们要做的工。因为最终就是我们两个是一起合作赚政府产业订单的钱。")

add_dialogue("碧莹", "但他其实也不一定需要确认，因为他只是给我们一个意向采购订单。")

add_dialogue("明修", "就是你的意思，我有个意向订单，我们内部好推进，对吧？上面都聊完了，这些合作我们要有个意向订单去推进嘛。")

add_dialogue("山相", "主线其实是从硬件到数据到模型。硬件那边需要前期，先是我们刚才提的移动加腰部自由度的定制，这一块需要他们大力支持。我们人力肯定比他们少很多。数据这一块就是我们给他们提供方案，他们那边采了之后，我们一起开源。最后模型那块我们主导。")

add_dialogue("碧莹", "数据开源是我们会伴随那个数据开源，发一个模型，这是baseline的模型。")

add_dialogue("明修", "对，你们弄好了之后，我们也有一个模型出来给你。")

add_dialogue("碧莹", "我们给你抬轿子。我们最大抬轿子。")

add_dialogue("山相", "他们有训模型的人吗？Post train？那问题不大。")

# Chapter 8
add_heading("八、MOU策略与角色分工")

add_dialogue("Anson", "明天谁主说？")

add_dialogue("田明", "明天有个MOU，我会把它投出来，然后每一条单独跟他们现场对。")

add_dialogue("碧莹", "田老师主说，然后我们给他补充。")

add_dialogue("Anson", "战略合作这一块，我看咱们现目前表述是比较抽象的。")

add_dialogue("田明", "对，聊完之后他们还要提出意见，我现场会把这个细节在上面完善一下，然后双方法务还要看。MOU都会往宽泛的角度去写，因为将来会有解释空间。")

add_dialogue("Anson", "MOU肯定是往宽泛写，这我们没有分歧。但是毕竟董事长要来了，我们要在这之前把我们所有的诉求都讲得非常明白，那些东西未必会写在MOU里边，但他们得带回去跟董事长汇报。")

add_dialogue("田明", "对，会议纪要很重要，你把todo列下来。")

add_dialogue("碧莹", "就是田老师聊一点，我就说这一点对应的todo是啥。")

add_dialogue("Anson", "我们明天是要把MOU讨论出来然后签署的，这只是今天议题之一。明天双方的所有诉求都要讲出来而且要对焦，然后为了下次董事长来之后直接拍板。说白了他们回去商量完了，董事长来就是鼓掌拉倒了，董事长讨论不了。")

add_dialogue("田明", "董事长只是搞政治的。")

add_dialogue("Anson", "你主说，有一些我会弄，我今晚发群里面。有一些要追问的你要追问，因为明修不适合直接上，他跟他们得论交情、谈感情，你得谈生意。你就当一个铁板一样的人。")

add_dialogue("碧莹", "一个唱红脸一个唱白脸。")

add_dialogue("Anson", "你就得做这事。")

add_dialogue("明修", "我们所有要跟他谈的点，我们自己先有一个简单的文档，到时候会上勾。漏了我会再提出来，谁漏了就@你负责提一下。")

add_dialogue("Anson", "我待会会把今天这段录下来整理一下。")

add_dialogue("田明", "你也把你的投上，每一条我都要@到人，到时候谁负责什么明确。")

# Chapter 9
add_heading("九、明天会议核心诉求梳理")

add_dialogue("碧莹", "我觉得明天核心的我们有两点诉求：第一就是产数据，这个数据对他来说的价值是做评测和影响力。第二点就是他其实是想做场景落地——太空舱，我们可能就是让他提供硬件各方面的人支援我们做这个demo。")

add_dialogue("田明", "demo他们自己就想做，他们已经立了军令状。好多场景，太空舱已经跟省领导汇报了，省领导也完全OK了，找一个地方想推他们做。")

add_dialogue("碧莹", "所以就牵引吧，他们那边做素材、demo、硬件。")

add_dialogue("山相", "那定制就让他们说太空舱需要这样的定制。")

add_dialogue("Anson", "那你除了这两个之外，刚才说的那个协议的事情是不是我们也要说，只是不写在MOU里而已？另外还有战略投资的事情。")

add_dialogue("田明", "对，这两个。")

add_dialogue("碧莹", "还有一个就是想要跟他签一个意向订单。")

add_dialogue("明修", "就是上面都聊完了，这些合作我们要有个意向订单去推进嘛。")

# Chapter 10
add_heading("十、后续行程与安排")

add_dialogue("Anson", "明天10点，是吧？")

add_dialogue("田明", "10点。")

add_dialogue("Anson", "我这有俩事跟你说一下，一个就是深圳那边问，跟那个姓严的推荐了个公司的事情。")

add_dialogue("田明", "我还得给周宇打电话。")

add_dialogue("Anson", "另外一个，我和明修我们仨明天去广州，你记得给我一个我们要把啥事要弄清楚的清单，因为我没那么专业。")

add_dialogue("田明", "怕我漏点啊。没有，我定的。")

add_dialogue("Anson", "然后你把那个发票抬头也发给我。")

add_dialogue("明修", "广州去北京我们几点出发？明天见吧。")

add_dialogue("Anson", "广州去北京几点出发？十二点的飞机应该来得及。")

add_dialogue("田明", "不行，一点到两点的飞机吧，回头我们群里商量一下。然后那个PPT我们约下周二早上，early bird合适的时间。")

# ======================== SAVE ========================
doc.save(output_path)
print(f"Document saved to: {output_path}")
