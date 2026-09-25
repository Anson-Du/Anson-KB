# -*- coding: utf-8 -*-
"""
生成 08-12 团队算力、数采工作任务讨论 清理版 Word 文档
发言人：明修(CTO)、碧莹(团队协调)、Anson(CSO)
"""

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

output_path = r"D:\RoboX\04_听记纪要\转写与纪要\2026-08-12 18.56 团队算力、数采工作任务讨论（清理版）.docx"

SPEAKER_COLORS = {
    '明修': RGBColor(0x70, 0x30, 0xA0),   # 紫色 - CTO
    '碧莹': RGBColor(0x00, 0x80, 0x80),   # 青色 - 团队协调
    'Anson': RGBColor(0xC0, 0x00, 0x00),  # 深红 - CSO/外部视角
}

COLOR_HEADING = RGBColor(0x1F, 0x4E, 0x79)
COLOR_NORMAL = RGBColor(0x00, 0x00, 0x00)
COLOR_NOTE = RGBColor(0x80, 0x80, 0x80)

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


# ========== 文档内容 ==========

add_title('08-12 团队算力、数采工作任务讨论')

add_note('参会人：明修（CTO）、碧莹（团队协调）、Anson（CSO）')
add_note('时间：2026年8月12日')

# ============================
add_heading('一、模型训练与算力规划')
# ============================

add_dialogue('明修', '先训一把，这把不带数据，数据还没那么多。9月底能到128张H100，之前给道处报的需求是9月底104张，先按108算。8月底前至少32张H100。')

add_dialogue('明修', 'System 2第一版需要27-30B参数量。推理和任务规划、简单agent优化要加强。之前推理和规划各算0.5，现在要把推理和任务规划强化。训练System 2时需要常驻256张卡，System 1也可能同时训练。')

add_dialogue('碧莹', '算力爬坡时间线确认：8月底32张 → 9月128张 → 10月128+256张 → 12月512张。10月128张这个数可以先定，后面可能还能调。')

add_dialogue('明修', '对，10月128可以。存储用OSS或NAS，存储和卡需要在同一个区域。卡都需要提前一个月规划，9月初128张常驻。')

add_dialogue('碧莹', '统一9月初。H100按2500块一天算，利用率要提高。')

add_dialogue('明修', '512张到12月底。System 2训练时System 1也可能同时训，所以算力要叠加上去。')

# ============================
add_heading('二、数据采集策略')
# ============================

add_dialogue('Anson', '自采的数据和跟外面买是两码事。未来很快就可以自采，是吧？')

add_dialogue('明修', '对，这个就是自采。我们前期设备、应用和采的数据的模态、数据结构都由我们来定。可以找人给我们做。')

add_dialogue('Anson', '采集的具体手部操作内容本身不重要，越离散越好，是吗？每个任务大概20小时左右就够了？')

add_dialogue('明修', '越多越好。第一阶段面向我们定的场景做验证，在有限场景下先开始。')

add_dialogue('Anson', '采和买之间的关系是什么？比例怎么定？')

add_dialogue('明修', '前期需要自采，不倾向买现成数据，质量估计不行。需要根据要演示的任务反推采哪些任务，在自己场地先采，确保质量后才能把需求派出去给别人。可以委托别人采（定制数据），但不是买训练场现成的数据。')

add_dialogue('碧莹', '可以做一个外包团队，搭一个采集站。')

add_dialogue('明修', '至少前期这份钱应该自己花。负责数据这块前期需要自己先做，坑还很多。装置没有就没法采，所以装置这块也得尽快推进。')

# ============================
add_heading('三、Ego数据政府合作')
# ============================

add_dialogue('Anson', 'Ego数据在跟几个政府谈，目前不适合跟杭州谈，在谈深圳和成都。需要政府提供场景，铺实门店、医院、大学、科研机构。AI for Science也是跟政府提的主要方向，希望政府能调动资源，让实验室、大学跟我们打招呼。')

add_dialogue('Anson', '真机素材需要场地，明修说500平米差不多，需要十几二十台本体（灵巧手、机械臂），打算跟政府提，看政府能不能投资。但杭州要等第一轮融资和IP隔离这些事收敛后才能谈。在跟政府没谈拢之前，合作方能不能先提供场景？')

add_dialogue('Anson', '长虹。田明说长虹在四川有素材基地。长虹CTO下周二过来，届时碧莹可以把需求提给他。')

add_dialogue('碧莹', '真机短期内可能耽误验证，可以先关注APP装置和可穿戴设备。')

# ============================
add_heading('四、采集装置开发')
# ============================

add_dialogue('明修', '三类装置需要处理：APP可穿戴设备、真机装置、带深度的头部摄像头。萌萌那套带不出来，需要自己搭或买现成。如果装置能ready，尽量一起采，第一版模型用不用再说。')

add_dialogue('明修', '可以同步做：自建验证+外购调研。bring up（硬件点亮）一周，但采集的整套逻辑、各模态数据整合、pipeline上传链路还需要开发。参考现有方案，硬件方案不用再花时间，软件看能不能复刻，买板子加接口估计两周能运行起来，再加上采集链路一周能看到效果。')

add_dialogue('碧莹', '之前听你们说一周，以为很快。')

add_dialogue('明修', 'bring up是东西都在了，能跑起来。但采集软件、数据模态整合、pipeline上传链路还需要开发。自建一个月都不一定能把硬件打好，不如找专业做嵌入式的公司。奥比（Orbbe）只是双目鱼眼摄像头，什么都没有。现在相当于把萌萌那套双目摄像头换成头环，但主控板、主系统、程序都得有，需要找专业做嵌入式的人来开发。')

add_dialogue('碧莹', '能直接买现成的吗？2万到10万一套的那种。')

add_dialogue('明修', '可以同步做，不是二选一。外购也可以，或者找数据解决方案公司定制。比如奥比有头环，可以让他们定制带深度或整套方案。光剑科技也可以聊，他们有数据手套。还可以跟UMI合作。现在还没开始寻源，给不了结论，但要尽快去找。嵌入式这块我可以先做。')

add_dialogue('碧莹', '9月底之前能不能ready？')

add_dialogue('明修', '9月底之前应该有机会。APP写起来比较快，采集流程已经做完了，但依赖后面平台的存储部分。8月底能把APP数据链路串起来。')

# ============================
add_heading('五、触觉手套与设备适配')
# ============================

add_dialogue('碧莹', '手套已经到了，带触觉接触反馈（震感），不是力反馈。买了两套，9月到货，先借一套用。')

add_dialogue('明修', '手套偏小，装不到天机5G上面去。天机5G跟二代手要适配，得看转接件。举桥支持定制5G，可以去寻源。达摩院还要继续做数据，可以问萌萌举桥新一代手套到了没有。')

add_dialogue('碧莹', '已经跟供应商坦白了（即将离职的事），可以直接问。')

add_dialogue('明修', '天机5G如果有现成转接件，不要让别人白做。相机支架可以用长虹的。GMSL的相机线细、头蓝，找一下看是不是。')

add_dialogue('碧莹', '确认一下，首个项目不带声音？')

add_dialogue('明修', '对，现在真机用的都没带声音。')

# ============================
add_heading('六、数据规模与节奏')
# ============================

add_dialogue('明修', '按PPT计划6个月5-10万小时，一年10万小时。第一版模型1.5万小时。触觉占比1%-10%。真机demo可能20-30小时。9月中数据到位开始采。')

add_dialogue('Anson', '明修之前说年底或半年内希望逼近10万小时。')

add_dialogue('明修', '半年10万小时，一个月4000多小时，所有项目化运作。一个动作可能5秒，所有产业操作任务的数据都可以运行。100人一天400小时，一个月1.2万小时。')

add_dialogue('Anson', '前期需要大量去买，同时也要采。采和买的比例怎么定？')

add_dialogue('明修', '前期需要采。需要知道要什么数据，根据要演示的任务反推采哪些任务，在自己场地先采，差一点也没关系，才放心把需求派出去给别人。不倾向买现成数据，可以委托别人采。')

add_dialogue('碧莹', 'M4之前1-2万小时。')

add_dialogue('明修', '触觉数据第一版占不了多少，150小时还是1500小时，希望是上千的。1%-10%来评估。带触觉的Ego装置9月底前ready，10月可以开始采数据。看投入——100人的话100套设备，触觉占比1%就1套，10%就10套。10套长虹出钱还是我们出钱，需要倒推。')

# ============================
add_heading('七、长虹合作')
# ============================

add_dialogue('Anson', '长虹CTO下周二来，碧莹可以把数据采集需求提给他。长虹有酒店、餐馆、工厂、展厅门店等场景，但没有家庭场景。碧莹需要把具体需求提给长虹。')

add_dialogue('明修', 'APP采集可以让长虹配合，100人一天400小时，一个月1.2万小时。但APP的Ego采集直接给长虹在工厂里采3万小时，真的有意义吗？需要找真实场景，要告诉长虹需要什么场景——酒店、餐馆、工厂。需要diversity的场景，提细的需求给长虹沟通。')

add_dialogue('碧莹', '长虹没有家庭场景。')

add_dialogue('明修', '对，所以一定要提细的需求。长虹常务部门马上会签战略合作协议，只要APP能出去，就能带着去采。')

# ============================
add_heading('八、Demo场景')
# ============================

add_dialogue('明修', 'Demo场景至关重要，需要尽快确定。科学实验、养老、服务、家庭场景方向不同，搭建完全不同。难度高的任务确实要提前定。如果做科学实验，就要实验室；做家庭的话14楼已经有家具了（冰箱、床、洗衣机，有人送的），搭起来就能用。')

add_dialogue('碧莹', '需要实验室？')

add_dialogue('明修', '如果做科学实验就要实验室。做养老还是服务还是家庭，需要你们下结论。大方向要确定。真机调好后一周内确定场景。在场就你一个产品经理，所以这个得你们接走。')

add_dialogue('碧莹', '搭完真机之后就开始试了。')

add_dialogue('明修', '对。14楼已经准备好了家居场景，八月底真机调好后开始试。室内拍摄要求：用头环戴摄像头，实时建图，能看到扫描进度。光剑大概率有深度摄像头方案，或者内部先用RealSense试一下。')

# ============================
add_heading('九、真机系统优化')
# ============================

add_dialogue('明修', '真机数据采集系统需要优化重构。在沙发上做了一些改进，有些任务之前根本采不下来，改进完之后就可以了。比如单手重新握住物体，之前必须用另一只手协同，现在有办法做到单手直接重新握住。这些优化对选择经济case比较关键。')

add_dialogue('碧莹', '你们俩一起协同来做。')

add_dialogue('明修', '是协同起来，但需要有人来帮忙做技术运行。跟叶老师聊过，需要有同学支持。算力没问题，需要一台就够了。真机基于天机5G 2.0来做，上面做原子计算。改造还需要时间，但可以先按原有链路把常规任务采起来，有相关同学后再优化提升。')

# ============================
add_heading('十、团队招聘与行政')
# ============================

add_dialogue('明修', '嵌入式/Linux开发人员需要招。不是开发嵌入式系统，是做Linux开发，类似赵峰、萌萌的角色。可以找推荐的人。长虹那边也有人可以用，黄一的师兄做硬件。')

add_dialogue('碧莹', '需要等到下周二还是现在就可以提需求？')

add_dialogue('明修', '提给长虹。但你们最好对齐——天机5G如果有现成的转接件，不要让别人白做。相机支架肯定没有现成的，可以找中介。')

add_dialogue('碧莹', '钉钉企业版需要购买和实名认证。需要创建组织，用营业执照认证，先买10-20个席位。语雀文档迁移到钉钉文档。')

add_dialogue('明修', '碧莹记得把语雀文档里算力爬坡计划改一下。确定用钉钉了，不要再用语雀了。买席位的事可以找花姐（法人）来认证购买。')

add_dialogue('碧莹', '电脑已经买好了，明天可以领，Mac电脑。中午开会，然后领电脑。')

add_dialogue('明修', '把关键设备信息发群里给大家看看。H100利用率要提高，2500块一天。碧莹你到时候把算力爬坡计划改一下，转到钉钉文档里去。')

# 保存
doc.save(output_path)
print(f"已生成: {output_path}")
