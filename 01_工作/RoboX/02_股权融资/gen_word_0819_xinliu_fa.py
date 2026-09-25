# -*- coding: utf-8 -*-
"""Generate cleaned transcript Word document for 0819 FA Xinliu Capital 2nd round strategy meeting."""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

output_path = r"D:\RoboX\02_股权融资\0819 FA心流资本第二轮融资策略沟通（清理版）.docx"

SPEAKER_COLORS = {
    'FA心流': RGBColor(0xC0, 0x00, 0x00),
    '田明': RGBColor(0x00, 0x80, 0x80),
    '明修': RGBColor(0x70, 0x30, 0xA0),
    '碧莹': RGBColor(0x00, 0x80, 0x80),
    'Anson': RGBColor(0x00, 0x33, 0x99),
}

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

style = doc.styles['Normal']
style.font.name = 'Microsoft YaHei'
style.font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
style.paragraph_format.line_spacing = 1.5


def add_title(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run.font.size = Pt(16)
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.bold = True
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_after = Pt(6)


def add_subtitle(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    run.italic = True
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')


def add_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run.font.size = Pt(13)
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.bold = True
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '6',
        qn('w:space'): '1', qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_note(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run.font.size = Pt(10)
    run.font.color.rgb = RGBColor(0x80, 0x80, 0x80)
    run.italic = True
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.left_indent = Cm(1)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(3)


def add_dialogue(speaker, text):
    p = doc.add_paragraph()
    run_s = p.add_run(speaker + '\u3000')
    run_s.font.name = 'Microsoft YaHei'
    run_s.font.size = Pt(11)
    run_s.bold = True
    color = SPEAKER_COLORS.get(speaker, RGBColor(0, 0, 0))
    run_s.font.color.rgb = color
    run_s.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    run_t = p.add_run(text)
    run_t.font.name = 'Microsoft YaHei'
    run_t.font.size = Pt(11)
    run_t.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)


def add_summary_heading(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run.font.size = Pt(14)
    run.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    run.bold = True
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '6',
        qn('w:space'): '1', qn('w:color'): '1F4E79'
    })
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_summary_item(text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Microsoft YaHei'
    run.font.size = Pt(11)
    run.element.rPr.rFonts.set(qn('w:eastAsia'), 'Microsoft YaHei')
    p.paragraph_format.left_indent = Cm(0.5)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)


# ========================
# DOCUMENT CONTENT
# ========================

add_title('FA心流资本第二轮融资策略沟通')
add_subtitle('2026年8月19日 | 约1小时5分钟')
add_note('参会人：明修、田明、碧莹、FA心流资本代表')

# ---- Key Points Summary ----
add_summary_heading('会议关键要点')

summary_items = [
    '1. 本轮进展：5-6家已基本完成沟通，总额超目标；大额7-8千万/中等3-5千万，9月中旬close本轮。重要业务方如窗口期允许也可挤入第一轮。',
    '2. 领投方未定：最大领投方上周五刚完成尽调，本周约谈；另一家5千万以上已发协议；第三家科技属性更强的约下周一见面。FA对各方信息做隔离处理。',
    '3. 融资节奏规划：第1周BP故事优化（已启动）\u2192第2-3周密集路演（最高优先级机构先跑）\u2192第4-6周锁定交易框架+条款谈判+法律文件\u2192第9周推进下一轮。',
    '4. 投资人优先级：最高优先级（美元基金为主）1-2周跑完；高优先级（人民币基金）第2-3周跟进。部分最高优先级机构已聊过3家，3家在约，1家已在谈。',
    '5. 估值阶梯策略：本轮20亿\u2192下一轮30-35亿\u2192再下一轮50亿左右。每轮涨一些，50亿前累计融资10-15亿。具身智能烧钱，估值涨幅不要太大。',
    '6. 时间窗口：年底前close到50亿估值，11-12月完成尽调交割。9月中旬close本轮后即可推进下一轮。',
    '7. BP优化方向：基于上次讨论的三个核心问题优化叙事，统一投资人口径，控制信息披露分寸——给多了容易被竞争对手抄袭，给少了投资人做不了决策。',
    '8. 模型公司估值逻辑（FA核心观点）：靠刷榜（benchmark排名）而非订单。持续保持第一名=应得对应估值。如模型能力\u2265自变量，应得200亿+估值（自变量也无订单但200亿+）。',
    '9. 对标案例：某团队2-3个月融三轮（1亿\u21922.5亿\u21924亿美金），通过分轮估值阶梯+领投方跟投配额凑盘子。6月底从华为离职，至今完成。',
    '10. 右派投资人应对：约2/3投资人认同技术优先路线（先提升智能上限再打场景），1/3强调订单收入的不适合投模型公司——他们适合看灵巧手/本体公司。',
    '11. 机构分析：美元基金节奏快（见投资负责人\u2192大老板两周点头\u2192IC过），适合第一轮；人民币基金流程长（浙商/光源/复星等），适合第二轮。',
    '12. 已分析机构：财通证券偏慢、光源资本央企背景慢、复星战投最慢（复星创富稍快）、招商局创投较快适合早期、策源资本母基金交易需求大、TCL创投市场化但流程长。',
    '13. 团队补强叙事：下一轮重点一是团队增强（引入教授/顾问签咨询协议），二是技术刷榜。算法负责人蔡老师背景强（华为天才少年offer、大厂算法负责人），需提升其知名度。',
    '14. 退出路径：10亿美金前不讲退出，10亿美金后面向不同投资人群体可讲退出路径（上市地点、标准、预期倍数）。',
    '15. 合作确认：FA协议已发出，确认合作后输出BP更新版本。后续每周提前对齐管理时间表+复盘。',
]

for item in summary_items:
    add_summary_item(item)

# ========================
# CHAPTER 1
# ========================
add_heading('一、本轮进展与时间节点')

add_dialogue('田明', '5-6家已经完成了沟通，如果都谈完的话基本上就够了。还有一些一两千万的配置，如果都放进来肯定要超额。有一些重要的业务方也在推进流程中，如果窗口期允许，也会让他们挤到第一轮里来。额度每家不一样，大的7-8千万，中等3-5千万。')

add_dialogue('田明', '时间节点卡在9月中旬，先把这一轮close掉。打款可能会延迟一点，中途这段时间可以先用预付款。不管交割多少，我们都会直接把资金扣死掉用于公司运营。')

# ========================
# CHAPTER 2
# ========================
add_heading('二、领投方沟通与额度分配')

add_dialogue('田明', '领投方还没确认给到最大的那家。上周五刚完成最后一轮尽调，这两天会约他再聊。另外一家5千万以上的，协议已经发过去了。还有一家科技属性更强的，约了下周一跟资金负责人见面。我们想看看这个盘子怎么组织——不希望直接把额度给掉了。')

add_dialogue('FA心流', '我们对各方信息做了隔离处理。项目安全起见，不同机构之间不互通信息。')

add_dialogue('田明', '领投方虽然很大，但还在观望第二轮的玩家。我们在帮忙推进，非常支持，希望有人接盘。愿意领投这个问题一般不需要有什么顾虑。')

add_dialogue('FA心流', '可以适当压一压额度，均衡一点。比如压到5千万以下，让更多机构参与，平衡盘子。')

# ========================
# CHAPTER 3
# ========================
add_heading('三、融资节奏与BP优化计划')

add_dialogue('FA心流', '很多机构比较关注下一轮是否有机构持续跟投。基于上次深入交流的三个问题，公司也发回来了反馈，轻微修改一下就可以。花一周半时间把故事做完善，BP定稿。然后花2-3周时间去核心机构密集路演，对本轮起到定心丸确定性的作用。')

add_dialogue('FA心流', '第4-6周确认整体交易架构，争取6周左右锁定交易框架，进行条款谈判和法律文件起草同步推进。大约第9周可以推进下一步。')

add_dialogue('田明', '第一周故事优化我们上周已经开始做了。')

add_dialogue('FA心流', '基于之前讨论的三个问题，我们再跟公司碰一下，大方向不变，稍微改动一些。面对不同投资人传递的价值主张需要一致，我们帮管理层统一口径。这一轮融资结构要严格把控——估值和第一轮有较大跨度，维持稳定的市场情绪信号，提高转化率同时降低交割风险。')

add_dialogue('FA心流', '后续每周提前对齐管理时间表并进行复盘。针对不同投资人在不同阶段，信息披露程度不一样——给多了容易被竞争对手抄袭，给少了投资人做不了决策，我们帮团队拿捏分寸。')

# ========================
# CHAPTER 4
# ========================
add_heading('四、投资人清单与优先级分级')

add_dialogue('FA心流', '材料准备约1-2周：先优化BP，完成数据包，输出BP文本和融资投资人清单。第3-5周进行具体路演，以说明会（NDR）为主。第3周做路演，后续以尽调和管理层访谈为主，交易条款签署我们全程陪同谈判，帮各家机构之间推进。')

add_dialogue('FA心流', '本轮策略以美元基金定价为主——他们的灵活度比较大，而且有知名机构撑估值。后续轮次以杭州本土投资人为主，产业资本多种维持。产业方跟进速度慢的可以放到这一部分作为小的份额，也能起到推进作用。')

add_dialogue('FA心流', '投资策略分三类：最高优先级、高优先级、观察级。最高优先级1-2周跑一遍路演，第2周开始跑高优先级。')

add_dialogue('田明', '最高优先级里有一半我们应该接触过了。但没有聊到最高决策人的，是否可以换线？需要看看推荐的机构有没有在内部讨论过，给了什么反馈——是说等一等，还是内部考虑了但看阶段。')

add_dialogue('FA心流', '最高优先级聊过3家，3家在约时间，1家已在谈。这些大机构组很多，比如高瓴有三个组，每个组都有自己的NGO可以推。每轮估值不同，推的角度也不一样——第一轮觉得偏早期，第二轮觉得戴帽子惊艳，以demo状态推。只要对团队评价positive就可以推。')

add_dialogue('FA心流', '有两类机构节奏快——见投资负责人，下一步大老板过来聊，两周大老板点头基本IC能过。人民币机构后台复杂，可能赶不上节奏。')

# ========================
# CHAPTER 5
# ========================
add_heading('五、机构分析：人民币基金特点')

add_dialogue('FA心流', '几个机构分析一下。财通证券偏人民币，流程比较长，得看是否见到董事长CEO层级，到了这个层级节奏会快一些。光源资本是光大那边的，央企基金，也比较慢。复星战投最慢——复星有很多条线，复星创富稍快，复星集团战略投资是最慢的。复星创富今年还是比较认同的，可能投第二轮概率大一些，第二轮是他们比较舒服的阶段。')

add_dialogue('FA心流', '招商局资本有几条线，招商局创投比较快，投早期。总部在香港，大部分分支在深圳。策源资本是四川的母基金，交易需求会大一些。银河创新资本是银河证券下面的，券商系很难做早期，大部分来聊聊认识一下，到中后期再找他们，还希望把券商业务带进来。')

add_dialogue('FA心流', '保险类资本（人保资本等）不太会投早期。险资券商都是这样。中金资本有几十条线，得看具体对的是哪个基金、哪个团队，本身流程也比较长。远洋投资自己钱不多。TCL创投可以聊，融的是外面的钱比较市场化，但流程长，整体TCL体系比较保守。中新融创跟TCL有相关性，看跟中信文化那边有什么结合。')

# ========================
# CHAPTER 6
# ========================
add_heading('六、估值策略：阶梯式增长')

add_dialogue('FA心流', '某团队2-3个月融了三轮：第一轮1亿美金拿了一些产业的钱估值低一些，第二轮2.5亿，第三轮4亿。2.5亿跟投方配4亿美金额度，相当于优惠。4亿之后开始做6-8亿美金。6月底从华为离职到现在，三轮做完。')

add_dialogue('田明', '三轮之间估值上升的逻辑是什么？')

add_dialogue('FA心流', '第一轮有产业方进来，会给一些场景结合，所以上来估值有变化。2.5亿和4亿区别不大——2.5亿时让更好的机构同时配4亿美金额度，相当于持续陆陆续续投入。核心两三个人先出来，然后团队编制完成，产业方给了一些合作。')

add_dialogue('FA心流', '跟投策略：领投方在下一轮需配跟投份额作为优惠条件。确定交易结构和份额时会跟领投方聊。')

add_dialogue('FA心流', '估值阶梯建议：本轮20亿，下一轮大概30-35亿，再下一轮50亿左右。每轮涨一些，50亿前能拿10-15亿左右。具身智能比较烧钱，每轮估值涨幅不要太大，对项目安全性高。具身智能数据周期和商业周期长，希望多拿钱而不是做收入。')

add_dialogue('FA心流', '时间节点：到50亿估值，从现在算年底11-12月完成尽调交割。')

# ========================
# CHAPTER 7
# ========================
add_heading('七、叙事策略：刷榜vs订单')

add_dialogue('田明', '下一轮叙事层面，是建议团队补强，还是交付demo或订单？哪种牵引整个团队在下一阶段快速准备？')

add_dialogue('FA心流', '持续优化——让投资人觉得团队更牛逼，这是最核心的考量因素。会不断有项目说"谁又签了""某教授加入了"。全职加入肯定加分，非全职但咖位高也OK，现在希望老师在学校里，这样可以白嫖博士生。只要签个咨询协议和领域经验性协议就行。')

add_dialogue('田明', '下一步要尝试交付场景demo还是系统应用？一种是远期但想象力大的demo，另一种是务实的能讲订单的。你倾向哪种？')

add_dialogue('FA心流', '对投资人讲订单的逻辑很难——订单里面水分多。核心是你有一个NDR跟他讲"我这一轮是模型能力"，比如公司会喊ranking看排名。模型公司本质是讲智力上限，怎么量化？就是榜单上的排名。')

add_dialogue('田明', '今年10月份尽快融下一轮钱，每一轮估值怎么加上去？只靠刷榜支撑力够吗？')

add_dialogue('FA心流', '刷榜就够了。持续保持第一名，理论上其他200亿的公司就是垃圾——动态比较过程。比如你现在模型能力超过自变量，就应该有自变量的估值。自变量也没有订单，但200多亿了。')

# ========================
# CHAPTER 8
# ========================
add_heading('八、模型公司估值逻辑与右派投资人应对')

add_dialogue('FA心流', '做模型公司只要做得好，没有靠订单活下去的。投资人很难认订单。现在不是做收入的阶段——模式都没搞清楚，做收入没有意义。做模型还没到做收入的阶段，你跟本体公司要外提的话才需要收入。')

add_dialogue('田明', 'AI范式变化是先达到通用的80分可用，再逐渐在具体场景专用。现在聊的投资人大概2/3认同这种看法。偏左派。偏右派有1/3强调产业资源、进工业要有订单。')

add_dialogue('FA心流', '问这种问题的人在这个领域出过钱的很少，他们不太了解行业现在什么情况。如果你们定位是做商业化、做数据担保公司，他们确实需要看商业订单——数据行业已经有大量收入了。但如果定位是快速提升智能上限的模型公司，拉收入没有意义。百川就是做金融做法律做错了，MiniMax发现不对掉头回来做模型就走出来了。Kimi和智谱完全不会去搞收入。')

add_dialogue('FA心流', '跟投模型公司的人关注的是技术烧、当前阶段是哪里。强调订单收入的投资人适合看灵巧手、本体公司，不是投模型方向的。1/3的投资人本身就不是投这个方向，不用管。')

add_dialogue('田明', '具身智能跟数字AI不一样——没有很好的公开应用场景做通用对标，榜单参与率没那么高、共识没那么强。')

add_dialogue('FA心流', '榜单是一块，但大家更测真机——现场随便问几个问题让机器人做动作，看失败率成功率，对比很明显。失败率高的别看了。朱浩他们也是坚定做模型，200多亿人民币也不会说要去搞收入。')

# ========================
# CHAPTER 9
# ========================
add_heading('九、退出路径与下一轮准备')

add_dialogue('田明', '有投资人专门提醒退出路径怎么跟投资人讲清楚。')

add_dialogue('FA心流', '问退出路径的是投中后期的，他们关注产品费——周期就是两年，要上市就退了。早期投资人看的是公司能力够大、速度够快，能对标就行。10亿美金以后可以讲怎么退——那时候面向的投资人群体不一样。10亿美金之前讲太早。')

add_dialogue('田明', '下一轮面向什么估值、需要做哪些准备，可以拉动起来了。')

add_dialogue('FA心流', '首先是估值——具身智能烧钱，每轮估值涨幅不要太大。其次看同行：智元每一轮涨一些估值，尽量把钱都圈进来。第三是10亿美金后的过渡——面向中后期投资人讲上市地点、标准、预期倍数。')

add_dialogue('田明', '蔡老师（算法负责人）背景很强——之前做ViLa引用量很高，年纪轻轻大厂算法负责人，当年拿到华为天才少年offer没去选了当阿里星。只是有点低调。')

add_dialogue('FA心流', '算法团队和刷榜是主打。同步讲算法模型架构的创新。10亿美金之前靠刷榜，10亿美金后有落地合作项目进一步证明。大部分机器人订单都是意向订单，没法交付——几十个亿的订单根本交付不了。')

# ========================
# CHAPTER 10
# ========================
add_heading('十、合作确认与后续推进')

add_dialogue('碧莹', 'PPT会有更新版本吗？如果合作的话，我们可以改一下。合作是什么形式？有前置条件吗？')

add_dialogue('FA心流', '协议已经发过了。协议没问题就可以推进。协议发到微信群里，应该是发给你。后续合作也是好的。')

add_dialogue('田明', '感谢大家的时间，后面看怎么合作。')

add_dialogue('FA心流', '感谢大家辛苦。')

# Save
doc.save(output_path)
print(f'Document saved: {output_path}')
