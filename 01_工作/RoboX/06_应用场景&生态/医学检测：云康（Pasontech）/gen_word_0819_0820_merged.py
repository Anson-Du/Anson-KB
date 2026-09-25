# -*- coding: utf-8 -*-
"""Generate merged cleaned transcript Word document for Aug 19-20 discussions."""

from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

output_path = r"D:\RoboX\06_产业生态\ICL（独立医学实验室）\0819-0820 医疗出海与云康合作讨论（清理版）.docx"

SPEAKER_COLORS = {
    'Anson': RGBColor(0xC0, 0x00, 0x00),
    '田明': RGBColor(0x70, 0x30, 0xA0),
    '明修': RGBColor(0x70, 0x30, 0xA0),
    '碧莹': RGBColor(0x00, 0x80, 0x80),
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
font = style.font
font.name = '微软雅黑'
font.size = Pt(11)
font.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
pf = style.paragraph_format
pf.line_spacing = 1.5
pf.space_after = Pt(4)

def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_after = Pt(6)

def add_meta(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1)
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    run.italic = True
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

def add_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(2)
    # Bottom border
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single',
        qn('w:sz'): '6',
        qn('w:space'): '1',
        qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_summary_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)

def add_summary_item(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.5)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(2)

def add_dialogue(speaker, text):
    p = doc.add_paragraph()
    color = SPEAKER_COLORS.get(speaker, RGBColor(0x00, 0x00, 0x00))
    run_s = p.add_run(speaker + ': ')
    run_s.bold = True
    run_s.font.color.rgb = color
    run_s.font.size = Pt(11)
    run_s.font.name = '微软雅黑'
    run_s.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    run_t = p.add_run(text)
    run_t.font.size = Pt(11)
    run_t.font.name = '微软雅黑'
    run_t.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(4)

def add_note(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    run.italic = True
    run.font.name = '微软雅黑'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_after = Pt(4)

def add_divider():
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('--- ' * 15)
    run.font.color.rgb = RGBColor(0xBF, 0xBF, 0xBF)
    run.font.size = Pt(10)

# ========== DOCUMENT CONTENT ==========

add_title('0819-0820 医疗出海与云康合作讨论（清理版）')

add_meta('时间：2026年8月19日晚（酒店路上） + 8月20日晚（团队讨论）')
add_meta('参会人：明修、田明、Anson、碧莹')

doc.add_paragraph()

# ========== SUMMARY SECTION ==========
add_summary_heading('会议关键要点总结')

add_summary_item('1. 医疗出海是漫长过程，不应期待今年就能在海外赚钱，国内医疗器械申请认证意义不大。')
add_summary_item('2. 实验验证路径：可与张总在浙江的实验室合作，张总有全国检测网点，浙江应该有据点。')
add_summary_item('3. 投资人日程协调：绿洲资本（上海）有意与合伙人沟通，拟安排周五或周二中午见面；敦煌/东方嘉富机会有限，取决于杭州银行人的实力，如无实质意义则取消。')
add_summary_item('4. 海外农业场景机会：澳洲苹果采摘日薪1000澳元，未来可输出产品和方案，对方有澳洲农场资源。')
add_summary_item('5. 云康集团股权结构问题：政府拖欠大量资金导致持续减值处理，大股东与二股东（广州国资）股权比例已接近，控制权存在风险。')
add_summary_item('6. 云康出海策略：拟在香港设立新主体，持有云康股份，规避上市公司体系中二股东的制约，以更大比例控制新公司。')
add_summary_item('7. 合作模式建议（田明）：可与云康（上市公司）单独签MOU，也可与新公司签合同。MOU无法律约束，二股东不会有意见，实质合作在新公司落地。')
add_summary_item('8. 合作核心目的：利用云康数百家实验室支撑生命科学实验叙事——当投资人问"机器人为何能完成实验"时，有合作伙伴提供场景和资源。')
add_summary_item('9. MOU与商业合同区别：MOU是合作意向，不受法律约束；商业合同有法律约束力。MOU的作用是向投资人展示有合作伙伴一起做事。')
add_summary_item('10. 投资人DD考虑（明修）：签署MOU可在投资人尽调时提供合作佐证，但MOU本身不放入data pack，仅作为补充材料。')
add_summary_item('11. PR策略（田明）：短期内不公开PR与云康的合作关系。云康在检测领域排第四或第五，需评估竞争对手（如元路）是否与行业老大合作。')
add_summary_item('12. 风险判断：田明认为不需过度关注云康当前财务状况——"我只会表示我有一个合作伙伴，他们有几百家实验室支撑我们今天要讨论生命科学的故事"。')
add_summary_item('13. Anson角色：梳理合作方式，明天输出合作框架建议；已将参会董总用模型做的公司分析发送给明修。')
add_summary_item('14. 类比分析：碧莹指出云康模式类似马老师开蚂蚁——在大型体系外设立创新业务主体自己控股；田明补充云康比蚂蚁更彻底，已剥离拿出资金在香港重新设公司。')

doc.add_paragraph()

# ========== PART 1: AUG 19 ==========
add_divider()
add_meta('以下为8月19日晚（酒店路上）讨论内容')
add_divider()
doc.add_paragraph()

add_heading('一、医疗出海与实验验证')

add_dialogue('明修', '泛化究竟在哪个程度上是物体放置还是动作方法？')

add_dialogue('田明', '我认为在国内确实很难，无论是医疗器械还是人类，我们肯定不用关心。')

add_dialogue('Anson', '在国内基本上申请了医疗认证，证明的意义不大。出海是一个漫长的过程，从事医疗领域的人不应该期待今年就可以出国赚钱，这是过于天真的想法。')

add_dialogue('明修', '你的叙事能力很强，实际上就是这个层面。你只需要做一个TOC，这件事情就需要等待整个行业和样本达到极限。你仅仅是进行一个实验。')

add_dialogue('Anson', '实际上，做这件事情和做实验本质上是同一件事情。另外是否为开放实验？实际上进行实验都是如此。')

add_dialogue('碧莹', '我们可以购买一些这个产品。')

add_dialogue('明修', '我建议在公司内部建立展厅。')

add_dialogue('Anson', '我认为你们不必纠结这个问题，可以与张总好好谈论，看他是否有一个实验室，比如在杭州的实验室。肯定有浙江的点，他有全国的点，所以浙江应该有点。没关系，请将验证派发给我们。')

add_heading('二、投资人日程协调')

add_dialogue('Anson', '我再讲述一件事情。早上我和田明——文超，上海有一家名为绿洲资本的公司，你是否听到今天在FA上谈论的内容？')

add_dialogue('田明', '我听到了。')

add_dialogue('Anson', '绿洲资本今天想与我们合伙人沟通，并且询问我们是否可以去上海。周五和周二他们有足够的时间吗？中午与文超交谈完毕。我的意思是能否将敦煌的时间提前到9:30或者10点，中午可以空出两个小时与绿洲沟通，之后你才有机会去。我先询问他有没有时间，如果绿洲确定了再说。')

add_dialogue('明修', '将敦煌向前推进，敦煌是早期投资运输的兄弟。')

add_dialogue('Anson', '敦煌的机会并不大，除非杭州银行的人非常有实力。东方嘉富虽然没有与杭州银行同样的饭局，但是我认为他们没有实力。如果没有实力，那不要去，没有意义。特别是这些人只是让我们过去听一听。我会在周五中午、明天和后天中午询问敦煌是否有机会，如果没有，我们就取消。我们去上海的目的是为了完成下午最后一场活动。')

add_dialogue('明修', '其他理由需要说明，因为不是陈波，而是另外一个人推荐的。行长当时表示这是关系非常好的兄弟。')

add_dialogue('Anson', '我询问陈波是否愿意推荐。')

add_heading('三、海外农业场景机会')

add_dialogue('明修', '昨天有个兄弟来了之后讲在澳洲从事苹果采摘的人就是你们的成本。')

add_dialogue('Anson', '昨天晚上他回去之后，我告诉他他给我发了一堆令人头疼的概念，我说未来我们就是输出。')

add_dialogue('碧莹', '澳洲采摘一天可以赚取1000澳元。')

add_dialogue('Anson', '他告诉我他有澳洲的农场。我表示以后我们需要输出产品和方案。')

add_dialogue('明修', '他并未理解你的意图，今天你带领他一起将其售卖。')

doc.add_paragraph()

# ========== PART 2: AUG 20 ==========
add_divider()
add_meta('以下为8月20日晚（团队讨论云康合作）内容')
add_divider()
doc.add_paragraph()

add_heading('四、云康集团背景分析')

add_note('（碧莹开场同步云康合作背景）')

add_dialogue('碧莹', '关于云康，我有一个事情想与大家同步。当时在会议上，张总和庄总提到要在香港寻找一个主体与我们合作或者签订MOU。我了解了这件事情的背景并且想与大家同步。我将昨晚参会的董总使用他的模型进行的公司分析发送给明修，稍后我将其发送给大家。')

add_dialogue('碧莹', '这家公司过去几年由于政府拖欠很多资金，导致他们赖账，因此他们不断进行减值处理，包括处理各大股东的股权质押。目前他们的股权已经稀释到接近二股东，与二股东相差无几。虽然二股东是广州国资，但是他们对公司的控制权仍然存在。他们需要与二股东商议做哪些事情。他们现在做创新事情希望不受制于二股东，并且提出很多国资质疑。')

add_dialogue('碧莹', '他既然要做出海业务，就想在香港设立一个主体，这个主体也有云康的股份。他能够以更大比例控制公司的控制权，以免在现有的上市公司体系里受到二股东的制约太多。这是它的背景，其中信息非常重要。虽然公司目前在经营上有序，但是大股东与二股东的股权比例相近，因此判断不会丧失控制权的风险。然而在现有体系中推动业务会受到一些影响。')

add_heading('五、香港主体与合作模式')

add_dialogue('田明', '他已经清楚了自己的诉求。')

add_dialogue('碧莹', '我没有诉求，只是了解到这个信息。')

add_dialogue('田明', '他希望使用一个主体可以帮助我们合作。')

add_dialogue('碧莹', '他想以香港为主体与我们合作。')

add_dialogue('田明', '问题不大，这对我们有劣势吗？')

add_dialogue('碧莹', '我没有劣势，只需关注合作主体中银行的比重。否则我们与一个没有来路的公司合作，为什么要与他合作？我必须了解他们与云康的关系，他们能够支配并充分调动云康的资源。')

add_dialogue('碧莹', '这跟我们原先的模式类似，在大型国企中，实际上赚不到太多钱，需要形成创新业务，自己控股。')

add_dialogue('碧莹', '我认为与马老师开蚂蚁相似。')

add_dialogue('田明', '他比马老师开设蚂蚁公司更加彻底，相当于他已经剥离并且拿出资金。他在香港重新开设一家公司，仅持有云康的股份。')

add_heading('六、MOU策略与法律边界')

add_dialogue('碧莹', '明修、田明，我明天会梳理我们的合作方式。如果各位现在有自己的判断和想法，那么也可以分享。')

add_dialogue('田明', '我认为与云康可以单独签订MOU协议，也可以与他的新公司签订合同。云康是上市公司，新公司并非如此，这取决于他是否愿意。MOU没有任何约束，我相信二股东不会有意见。我们只是在新公司内真正落地合作。')

add_dialogue('碧莹', '目前你对MOU框架有一些比较坚定的想法。')

add_dialogue('田明', 'MOU没有特别过分的限制，也没有法律协议，不要有法律约束。合作诉求是我们共同合作完成某些事情，我们有自己的解释权，他们也有解释权。合作MOU与商业合同是两回事，商业合同有法律约束，MOU不受法律约束。我们是朋友，我可以告诉投资人，我有个朋友希望与我一起完成这件事情，这是MOU的目的。')

add_dialogue('明修', '虽然可以不放在data pack里面，但是后续可能会有投资人在进行公司尽职调查时要求我们提供这个软件——不是软件，而是签署MOU协议。')

add_dialogue('田明', '这个没有问题。我认为与上市公司签订协议是一个原因，否则你所说的都是虚假的。')

add_dialogue('碧莹', '他只是合作诉求，还是双方共同投资的诉求？')

add_dialogue('田明', '我们不仅需要签订协议，我们还有合作意向。MOU是合作意向。')

add_heading('七、合作目的与PR策略')

add_dialogue('碧莹', '我们需要确认未来对外PR时能否提及云康集团。')

add_dialogue('田明', '我并不想PR，他在检测领域是老四还是老五。你知道元路与谁合作吗？如果元路与老大合作，我们就与老四合作。')

add_dialogue('碧莹', '我不确定元路是否与老大合作。')

add_dialogue('碧莹', '我们签MOU的主要目的是什么？')

add_dialogue('田明', '我们讨论生命科学，因此机器人需要进行实验。当别人询问你为何能够完成实验？我们只有这个目的——他真的愿意将这个场景提供给我们，一起做实验。这是我们经过12小时的努力达成的共识，否则我们也不知道机器人需要做这些实验和动作，这对双方都有收获。')

add_dialogue('田明', '我们并非凭空要求签MOU，而是真的希望朝着这个方向发展。短期内我们与他合作时不会发表意见，这种形式大家都没有问题。')

add_dialogue('碧莹', '关于这个话题，我没有需要补充的内容。')

add_dialogue('碧莹', '碧莹，还有其他问题吗？没有，我们先到这里。')

add_dialogue('明修', '我没有其他问题。')

add_dialogue('碧莹', '辛苦各位。')

add_dialogue('田明', '辛苦大家。')

# Save
doc.save(output_path)
print(f'Document saved: {output_path}')
print(f'File size: {os.path.getsize(output_path)} bytes')
