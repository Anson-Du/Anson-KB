# -*- coding: utf-8 -*-
"""
08-17 与长虹沟通会准备讨论会 - 清理版Word文档生成脚本
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

output_path = r"D:\RoboX\06_产业生态\长虹\0817与长虹沟通会准备讨论会（清理版）.docx"

SPEAKER_COLORS = {
    '碧莹': RGBColor(0x00, 0x80, 0x80),    # 青色
    '山相': RGBColor(0x00, 0x33, 0x99),    # 深蓝
    '田明': RGBColor(0x70, 0x30, 0xA0),    # 紫色
    'Anson': RGBColor(0xC0, 0x00, 0x00),   # 深红
    '明修': RGBColor(0x70, 0x30, 0xA0),    # 紫色
}

COLOR_HEADING = RGBColor(0x1F, 0x4E, 0x79)
COLOR_NORMAL = RGBColor(0x00, 0x00, 0x00)
COLOR_NOTE = RGBColor(0x80, 0x80, 0x80)
COLOR_SUMMARY = RGBColor(0x2E, 0x5C, 0x8A)  # 总结用色

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
    """添加关键要点标题（特殊样式）"""
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
    """添加关键要点条目"""
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

add_title('0817与长虹沟通会准备讨论会')

add_note('参会人：碧莹、山相、田明、Anson、明修')
add_note('时间：2026年8月17日 22:18，时长约23分钟')
add_note('主题：明天（8/18）与长虹团队对接会的准备讨论')

# ========== 关键要点总结 ==========

add_summary_heading('会议关键要点总结')

add_summary_item(
    '1. 会议背景：明天（8/18）长虹团队8人来ROBOX对接，各方向人员现场对齐。本次讨论会为内部准备会，明确合作模式、时间节点、诉求清单和角色分工。'
)
add_summary_item(
    '2. 硬件合作模式：ROBOX卖基础款数采装置给长虹（含相机等核心部件），长虹在此基础上做腰部自由度等定制（7人硬件团队），定制方案完成后ROBOX可复刻（不交付实物）。基础款不需产品级ID设计，只要能动、能采数即可。'
)
add_summary_item(
    '3. 数据采集两条线并行：\n'
    '   - 素材厂场景：9月初开始，9月底完成1000小时数据采集\n'
    '   - 真实场景（酒店）：9月底-10月初开始，需长虹提供酒店房间改造，采集整理/叠衣服/擦桌子等任务\n'
    '   - 硬件ready周期：腰部自由度定制至少1个月，9月中下旬才能ready'
)
add_summary_item(
    '4. 10月开源计划：1000小时灵巧操作数据集（世界最大），同步发布基线模型。'
    '战略意义：有了基础数据，所有人训练后都会来ROBOX测试，形成生态引力。'
    '融资节奏驱动：11月投资人进入投资报告期，10月必须开放数据。'
)
add_summary_item(
    '5. 长虹两个投资诉求：①长虹集团名义战略投资ROBOX；②成立合资公司。'
    'ROBOX态度：open，战略投资可与Eric对接，合资公司暂不建议（人力有限）。'
)
add_summary_item(
    '6. ROBOX明天核心诉求（四点）：\n'
    '   - 硬件定制支持（腰部自由度+移动能力，长虹7人团队保障）\n'
    '   - 数据合作（长虹采购基础款+采数，联合开源）\n'
    '   - 意向采购订单/POC合同（不写入MOU，私下沟通）\n'
    '   - 战略投资（长虹投资部已给任务，需明确提出）'
)
add_summary_item(
    '7. MOU准备：田明已起草MOU，会上逐条与长虹现场对齐。MOU内容往宽泛写留解释空间，'
    '但实质合作要点必须讲清楚，让长虹带回去向董事长汇报。下次董事长来直接拍板。'
)
add_summary_item(
    '8. 角色分工：田明主说MOU逐条对齐；碧莹补充+记录todo；明修负责技术/模型部分；'
    'Anson负责战略投资追问（田明与长虹论交情，碧莹谈生意条款，形成互补）。'
)
add_summary_item(
    '9. 太空舱场景：长虹已向省领导汇报并获认可，长虹自己立军令状做demo。'
    '可牵引长虹硬件定制需求（太空舱需要腰部自由度定制）。'
)
add_summary_item(
    '10. 后续行程：后天（8/19）田明/明修/Anson去广州长虹，然后去北京。'
    'PPT讨论约下周二早上。'
)

# ========== 正文 ==========

# ============================
add_heading('一、硬件合作模式与定制分工')
# ============================

add_dialogue('山相', '这一整套解决方案是我们给他们，还是一起做？是我们做、我们卖，但全部软硬件都是我们去团好了给他们一起开发？')

add_dialogue('田明', '边界可以商定。他们专门有工程的人搞，还有专门硬件负责人，7人团队都能搞。你主要出方案、出标准，碰到硬件问题他再问你。无问题数采装置要搞，基模的后训练他们可以帮我们做，我们主要提供基模。应用场景落地、硬件合作、投融资合作都在上面。')

add_dialogue('碧莹', '硬件合作在定制之前，我们可以先让他给我们做一个带臂的轮式本体，或者加一个小型的。')

add_dialogue('山相', '我有个困惑：像本体定制这种，我们希望他帮我们做，结果又变成这套设备是我们卖给他们，他们会接受吗？')

add_dialogue('田明', '一码归一码，评测是评测，本体定制是本体定制。本体定制我们是甲方，我们出钱的，他用BOM成本给我交付。')

add_dialogue('碧莹', '我们希望这一套也加一点定制，他定制然后他给我们买。他买基础版，他自己开发就开发了，我们也不跟他要钱，他也不跟我们要钱，但硬件还是加点钱卖给他。')

add_dialogue('田明', '可以，就是说他只买我们的基础版，反正最后他改完的东西如果我们要买，就按增值价格买回来。')

add_dialogue('碧莹', '我们也不用买，他改完告诉我怎么设，复刻一下就行。不需要他来交付，交付的是那套定制的轮式双臂的，这套给我们就好。另一套很简陋的只是能动就行。')

add_dialogue('田明', '都可以，反正你要啥他给你搞啥。他这次来8个人，就是为把各方向的人直接现场给你对接。然后你要告诉他时间节点，他7个人能不能保障。')

add_dialogue('山相', '像我们现在这套，相机支架这些是没有的，需要他们帮我们画出来。')

add_dialogue('田明', '那你就给他一个清单，说这些东西你要自购，然后给他个推荐。他有设计师，顺便帮你画了算了。')

# ============================
add_heading('二、数据采集时间节点')
# ============================

add_dialogue('碧莹', '请问1000小时的数据什么时候开始采？硬件要running的时间是什么时候？')

add_dialogue('田明', '今天在现场画一下就OK了。他先9月初评估，如果不行他再报一个时间，我们看能不能接受。')

add_dialogue('山相', '9月初我们是要有硬件开始采，不是1000小时的交付。')

add_dialogue('碧莹', '然后结束就是9月底，一个月能不能采1000小时？而且我们这个要真实场景，就不是素材厂那种。')

add_dialogue('山相', '真实场景的话，推到家里边的肯定来不及。')

add_dialogue('田明', '不一定是放家里，是放素材厂里面的。长虹酒店里可以腾几个房间让你去采。')

add_dialogue('山相', '要到真实场景去采，必须把腰部、移动那些自由度定制好才能采。9月初ready不了，他们两个礼拜不可能。')

add_dialogue('碧莹', '那得什么时候？')

add_dialogue('山相', '至少一个月的时间。')

add_dialogue('碧莹', '那就是9月中旬。')

add_dialogue('山相', '9月中下旬。然后硬件ready后，进家庭采集总不可能所有东西都挂着网线。现场干不了活，得是一套完整的。')

add_dialogue('碧莹', '这个事情得重检，有点过于乐观了。')

add_dialogue('山相', '现场干不了活，重检没用。明天硬件来了现场对一下。')

add_dialogue('碧莹', '素材厂是什么时候？')

add_dialogue('山相', '素材厂9月初就可以开始采，9月底1000小时。这是两码事。')

add_dialogue('碧莹', '9月底可以是真实场景？')

add_dialogue('山相', '9月底100%不行。真实场景得重新评估，差不多得一个月多点，9月底比较难。新城他们那一整套搭了至少半年。')

add_dialogue('碧莹', '但我们不去加，也不是随便敲门进家采，肯定是固定酒店、固定房间，把这个房间改成素材厂那种感觉。')

add_dialogue('山相', '那这和素材工厂有什么区别？他可以把素材工厂也布置成那样。')

add_dialogue('碧莹', '其实很难，光照、空间感都不一样。素材工厂是1:1复刻的现成房间。')

# ============================
add_heading('三、酒店场景任务定义')
# ============================

add_dialogue('山相', '酒店真实场景要采什么任务？')

add_dialogue('碧莹', '整理垃圾、擦桌子、叠床上衣服之类的。')

add_dialogue('山相', '叠衣服，酒店应该没有这个需求。')

add_dialogue('田明', '把衣服塞到洗衣机里面是有的。住酒店也有叠好的。')

add_dialogue('碧莹', '你在酒店也有叠衣服的需求。')

add_dialogue('田明', '没关系，这个将来也是用的。')

add_dialogue('碧莹', '那九月底十月初吧，肯定不是一个场。')

# ============================
add_heading('四、融资节奏驱动')
# ============================

add_dialogue('碧莹', '10月份我们要开一批数据，这批数据最好有一部分是真实场景。11月份投资人都不投资了，都搁那写投资报告了，都放假了。')

add_dialogue('山相', '数据要分不同样式。素材厂采的可以很快发出来，但拉到酒店或家庭采的没那么快。')

add_dialogue('田明', '创业公司急，不是光急在办事上，是急在融资节奏上。钱推着你走，不是大家为了加班而加班。')

add_dialogue('碧莹', '酒店是比较好采的场景，相对来说比较封闭，有点素材。')

# ============================
add_heading('五、1000小时数据集开源计划')
# ============================

add_dialogue('碧莹', '我们希望10月份一起把1000小时的灵巧操作数据集开放出去，其中有一定比例是真实场景下的。')

add_dialogue('明修', '200人日，他有20人10天就给你采完了。为什么要做这件事？做了之后所有人有了一个基础数据，用这个数据训练了都会来你这测。我们还发模型，告诉你baseline在哪。')

add_dialogue('碧莹', '这个数据也非常有意义，是世界上最大的，也是目前非常稀缺的灵巧操作数据。')

add_dialogue('明修', '而且过时不候，因为很快。他人已经有了，现在核心是忽悠他买机器。')

# ============================
add_heading('六、长虹投资诉求与交叉持股')
# ============================

add_dialogue('Anson', '他之前提出要跟我们交叉持股，这方面我们的态度是什么？')

add_dialogue('田明', 'Open的。他不光交叉持股，两个诉求：一是长虹集团名义战略投资我们；二是跟我们成立合资公司。投资的事跟Eric商量。')

add_dialogue('碧莹', '我不建议合资公司，我知道人就少，又要分出去一部分。')

# ============================
add_heading('七、明天会议核心诉求')
# ============================

add_dialogue('明修', '你们聊好了吗？哪几个方向确定？')

add_dialogue('田明', '合作项目主要就是时间节点。')

add_dialogue('碧莹', '明天不跟他提多少数据，直接说我们希望10月份有1000小时灵巧操作数据开源出去，让他来评估要买多少套、怎么投入。')

add_dialogue('Anson', '我们最想要什么，自己清不清楚？')

add_dialogue('碧莹', '我想要POC合同。')

add_dialogue('明修', '意向订单合同。')

add_dialogue('田明', '比如他买你这套用来做素材采集的方案。但他要确定真正的买单方，比如事业单位或政府那边，这是他们要做的工作。最终是我们两个一起合作赚政府产业订单的钱。')

add_dialogue('碧莹', '他其实也不一定需要确认，因为他只是给我们一个意向采购订单。')

add_dialogue('Anson', '战略投资的事情明天也需要提出来？')

add_dialogue('田明', '要提，因为他是带着任务来的，投资部给他的任务。')

# ============================
add_heading('八、MOU准备与角色分工')
# ============================

add_dialogue('Anson', '明修咱们是不是得讨论一下分工？明天谁主说？')

add_dialogue('田明', '明天有个MOU，我会把它投出来，然后每一条单独跟他们现场对。')

add_dialogue('碧莹', '田老师主说，我们给他补充。')

add_dialogue('Anson', '战略合作这一块，我们目前的表述是比较抽象的。')

add_dialogue('田明', '聊完之后他们还要提意见，我现场把细节在上面完善，双方法务还要看。MOU都会往宽泛角度写，将来有解释空间。')

add_dialogue('Anson', 'POC合同和真机合同在MOU里吗？')

add_dialogue('田明', '那个不能写在MOU里面，是你们私下交易的东西。')

add_dialogue('Anson', '反正记着，别漏掉这些关键点。')

add_dialogue('明修', '我们所有要跟他谈的点，自己先有个简单文档，会上勾。漏了谁就艾特谁负责提一下。')

add_dialogue('Anson', '你主说，有一些我会弄，今晚发群里。有一些要追问的你要追问，因为明修不适合他上——他跟他们得论交情、谈感情，你得谈生意。你就当一个铁面的人。')

add_dialogue('明修', '明天问一下周宇来不来。')

add_dialogue('田明', '他在外地，要拼命赶才能回来，我跟他说别着急了。')

# ============================
add_heading('九、太空舱场景与Demo')
# ============================

add_dialogue('碧莹', '明天核心两点诉求：第一是产数据，对长虹的价值是做评测和影响力；第二是场景落地，太空舱，我们让他提供硬件各方面的人支援我们做demo。')

add_dialogue('田明', 'demo他们自己就想做，已经立了军令状。')

add_dialogue('碧莹', '他们那边做素材、demo、硬件。')

add_dialogue('山相', '他们的场景是太空舱？')

add_dialogue('田明', '好多场景，太空舱已经跟省领导汇报了，省领导完全OK，找一个地方想推他们做。')

add_dialogue('山相', '那定制就让他们说太空舱需要这样的定制。')

# ============================
add_heading('十、合作主线梳理')
# ============================

add_dialogue('山相', '主线其实是从硬件到数据到模型。硬件那边需要前期先做移动加腰部自由度的定制，需要他们大力支持，我们人力肯定比他们少很多。数据这块我们给他们提供方案，他们采了之后我们一起开源。最后模型那块我们主导。')

add_dialogue('碧莹', '数据开源我们会伴随发一个模型，这是System 2的模型。')

add_dialogue('明修', '你们弄好了之后，我们也有一个模型出来给你。')

add_dialogue('碧莹', '我们给你抬轿子，最大抬轿子。')

add_dialogue('山相', '他们有训模型的人吗？Post train？那问题不大。')

# ============================
add_heading('十一、后续行程安排')
# ============================

add_dialogue('Anson', '明天10点，是吧？')

add_dialogue('田明', '10点。')

add_dialogue('Anson', '我和明修我们仨明天去广州，后天去广州。你记得给我一个我们要把啥事要弄清楚的清单，因为我没那么专业。')

add_dialogue('田明', '怕我漏点。')

add_dialogue('Anson', '然后你把发票抬头发给我。')

add_dialogue('明修', '广州去北京几点出发？明天见吧。')

add_dialogue('Anson', '十二点的飞机应该来得及，一点的飞机。回头我们群里商量。')

add_dialogue('田明', 'PPT我们约下周二早上，early bird合适的时间。')

# 保存
doc.save(output_path)
print(f"已生成: {output_path}")
