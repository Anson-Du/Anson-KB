# -*- coding: utf-8 -*-
"""0908 长虹洽谈 - 转写清理版 Word 文档生成"""

import sys
import os
from datetime import datetime

# 引入数据
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data1_summary import SUMMARY_SECTIONS, ACTION_ITEMS, METADATA
from data_final_chapters import CHAPTERS

from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# 颜色定义（统一深蓝色）
COLOR_DARK_BLUE = RGBColor(0x1F, 0x4E, 0x79)
COLOR_GRAY = RGBColor(0x59, 0x59, 0x59)
COLOR_DARK = RGBColor(0x33, 0x33, 0x33)
COLOR_LIGHT_GRAY = RGBColor(0x99, 0x99, 0x99)
COLOR_BROWN = RGBColor(0x0B, 0x3C, 0x6B)  # 田明（主讲，深宝蓝）
COLOR_TEAL = RGBColor(0x00, 0x70, 0x80)  # 邹宇（Tony/饺子）
COLOR_OLIVE = RGBColor(0x55, 0x6B, 0x2F)  # 周总
COLOR_PURPLE = RGBColor(0x6A, 0x2C, 0x70)  # 童哥
COLOR_ORANGE = RGBColor(0xCC, 0x66, 0x00)  # 张维
COLOR_DEEP_GREEN = RGBColor(0x1E, 0x55, 0x2B)  # 万涛
COLOR_CRIMSON = RGBColor(0xB2, 0x22, 0x22)  # 备用（深红）
COLOR_NAVY = RGBColor(0x00, 0x2B, 0x5B)  # Anson
COLOR_GOLD = RGBColor(0xB8, 0x86, 0x0B)  # 曾昊山（总助/主持）
COLOR_BLACK = RGBColor(0x00, 0x00, 0x00)  # 正文默认色

# 发言人颜色映射（2026-09-20 人物归因修正定稿版）
# 睦灵方：田明（产品负责人/开场主讲，深宝蓝）、Anson（产业生态与GA，藏蓝）、邹宇（Tony/饺子，业务方案/合同，青）
# 长虹方：曾昊山（总助/主持，金褐）、周总（周怡成，CFO，橄榄）、童哥（合规法务，紫）、张维（数采厂，橙）、万涛（硬件，深绿）
# 说明：创始人明修到场仅短暂参会、未作正式发言，故不设发言人配色；贾澜鹏（运营总监）/张总仅被提及，预留配色以防后续补录
SPEAKER_COLORS = {
    "田明": COLOR_BROWN,
    "Anson": COLOR_NAVY,
    "安森": COLOR_NAVY,
    "邹宇（Tony）": COLOR_TEAL,
    "曾昊山（总助）": COLOR_GOLD,
    "周总（周怡成）": COLOR_OLIVE,
    "童哥": COLOR_PURPLE,
    "张维": COLOR_ORANGE,
    "万涛": COLOR_DEEP_GREEN,
    "贾澜鹏（运营总监）": COLOR_GOLD,
    "张总（财务合规）": COLOR_OLIVE,
}

# 发言人归一化（speaker 字段已为最终显示名，直接透传）
SPEAKER_NAME_MAP = {}


def set_chinese_font(run, font_name="微软雅黑", size=11, bold=False, italic=False, color=None):
    """设置中文字体（中文用微软雅黑）"""
    run.font.name = font_name
    run._element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color


def add_title(doc, text, size=22, color=COLOR_DARK_BLUE, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    p.alignment = align
    run = p.add_run(text)
    set_chinese_font(run, size=size, bold=bold, color=color)
    return p


def add_subtitle(doc, text, size=14, color=COLOR_GRAY, align=WD_ALIGN_PARAGRAPH.CENTER):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(18)
    p.alignment = align
    run = p.add_run(text)
    set_chinese_font(run, size=size, color=color)
    return p


def add_para(doc, text, size=11, color=COLOR_DARK, bold=False, indent=True, line_spacing=1.5, alignment=WD_ALIGN_PARAGRAPH.LEFT):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = line_spacing
    p.paragraph_format.space_after = Pt(3)
    if indent:
        p.paragraph_format.first_line_indent = Cm(0.74)
    p.alignment = alignment
    run = p.add_run(text)
    set_chinese_font(run, size=size, bold=bold, color=color)
    return p


def add_h1(doc, text, size=16, color=COLOR_DARK_BLUE):
    """一级标题（深蓝带下划线分隔）"""
    p = add_title(doc, text, size=size, color=color, bold=True, align=WD_ALIGN_PARAGRAPH.LEFT)
    # 添加下划线装饰（在标题下方）
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(2)
    run = p.runs[0]
    run.font.underline = True
    return p


def add_h2(doc, text, size=13, color=COLOR_DARK_BLUE):
    """二级标题"""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = p.add_run(text)
    set_chinese_font(run, size=size, bold=True, color=color)
    return p


def add_qa_pair(doc, speaker, text):
    """添加问答对（发言人加粗着色，内容紧随其后）"""
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.space_after = Pt(5)
    p.paragraph_format.first_line_indent = Cm(0.74)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT

    # 发言人姓名
    speaker_display = SPEAKER_NAME_MAP.get(speaker, speaker)
    speaker_color = SPEAKER_COLORS.get(speaker, COLOR_DARK)
    if speaker_display not in SPEAKER_COLORS:
        # 复合名映射（如"发言人1（长虹运营总监）"），按原 speaker 颜色
        pass

    run_speaker = p.add_run(speaker_display)
    set_chinese_font(run_speaker, size=11, bold=True, color=speaker_color)

    run_colon = p.add_run("：")
    set_chinese_font(run_colon, size=11, color=COLOR_DARK)

    # 正文
    run_text = p.add_run(text)
    set_chinese_font(run_text, size=11, color=COLOR_DARK)


def add_bullet(doc, text, indent_level=0, size=11):
    p = doc.add_paragraph()
    p.paragraph_format.line_spacing = 1.5
    p.paragraph_format.left_indent = Cm(0.74 + 0.6 * indent_level)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.first_line_indent = Cm(-0.6)  # 悬挂缩进
    run_b = p.add_run("• ")
    set_chinese_font(run_b, size=size, bold=True, color=COLOR_DARK_BLUE)
    run_t = p.add_run(text)
    set_chinese_font(run_t, size=size, color=COLOR_DARK)
    return p


def add_info_table(doc, headers, rows, col_widths=None):
    """添加信息表"""
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.allow_autofit = True

    # 设置列宽
    if col_widths:
        for i, w in enumerate(col_widths):
            for r in table.rows:
                r.cells[i].width = w

    # 表头
    hdr_cells = table.rows[0].cells
    for i, h in enumerate(headers):
        cell = hdr_cells[i]
        cell.paragraphs[0].paragraph_format.line_spacing = 1.2
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = cell.paragraphs[0].add_run(h)
        set_chinese_font(run, size=11, bold=True, color=RGBColor(0xFF, 0xFF, 0xFF))
        # 单元格背景色
        shading = OxmlElement('w:shd')
        shading.set(qn('w:fill'), '1F4E79')
        cell._tc.get_or_add_tcPr().append(shading)

    # 数据行
    for r_idx, row_data in enumerate(rows):
        row_cells = table.rows[r_idx + 1].cells
        for c_idx, val in enumerate(row_data):
            cell = row_cells[c_idx]
            cell.paragraphs[0].paragraph_format.line_spacing = 1.2
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT
            run = cell.paragraphs[0].add_run(str(val))
            set_chinese_font(run, size=10.5, color=COLOR_DARK)

    # 表格边框
    for row in table.rows:
        for cell in row.cells:
            tc = cell._tc
            tcPr = tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for border_name in ['top', 'left', 'bottom', 'right']:
                border = OxmlElement(f'w:{border_name}')
                border.set(qn('w:val'), 'single')
                border.set(qn('w:sz'), '4')
                border.set(qn('w:color'), 'BFBFBF')
                tcBorders.append(border)
            tcPr.append(tcBorders)

    return table


def add_doc_meta(doc, meta):
    """添加文档元信息表"""
    add_h2(doc, "会议基本信息", size=13)
    rows = [
        ["会议日期", meta["date"]],
        ["会议时长", meta["duration"]],
        ["会议地点", meta["venue"]],
        ["睦灵方参会", "；".join(meta["participants_mulin"])],
        ["长虹方参会", "；".join(meta["participants_changhong"])],
    ]
    add_info_table(doc, ["项目", "内容"], rows, col_widths=[Cm(3.2), Cm(13.0)])

    # 特别说明
    add_para(doc, meta["memo_note"], size=10, color=COLOR_LIGHT_GRAY)


def add_summary_sections(doc, sections):
    """添加沟通总结分区"""
    for sec in sections:
        add_h1(doc, sec["title"], size=15)
        for item in sec["items"]:
            add_bullet(doc, item)


def add_action_items(doc, items):
    """添加 Action Items 表"""
    add_h1(doc, "Action Items（行动项与责任人）", size=15)
    rows = []
    for i, item in enumerate(items, 1):
        rows.append([str(i), item["owner"], item["action"]])

    table = add_info_table(
        doc,
        headers=["序号", "责任人", "行动项"],
        rows=rows,
        col_widths=[Cm(1.4), Cm(3.0), Cm(11.8)]
    )


def add_chapters(doc, all_chapters):
    """添加所有章节"""
    for ch in all_chapters:
        add_h1(doc, ch["title"], size=15)
        for speaker, text in ch["qa_pairs"]:
            add_qa_pair(doc, speaker, text)


def main():
    doc = Document()

    # 全局样式
    style = doc.styles['Normal']
    style.font.name = '微软雅黑'
    style._element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    style.font.size = Pt(11)

    # 页面设置
    section = doc.sections[0]
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)

    # === 标题 ===
    add_title(doc, METADATA["title"], size=22, color=COLOR_DARK_BLUE, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_subtitle(doc, METADATA["subtitle"], size=13, color=COLOR_GRAY, align=WD_ALIGN_PARAGRAPH.CENTER)

    # === 会议基本信息 ===
    add_doc_meta(doc, METADATA)

    # === 沟通总结 ===
    add_h1(doc, "沟通总结（结论与共识）", size=18)
    add_summary_sections(doc, SUMMARY_SECTIONS)

    # === Action Items ===
    add_action_items(doc, ACTION_ITEMS)

    # === 章节正文 ===
    add_chapters(doc, CHAPTERS)

    # === 文档结尾 ===
    add_para(doc, "", size=10)
    add_h2(doc, "—— 会议转写清理结束 ——", size=12, color=COLOR_LIGHT_GRAY)

    # === 保存 ===
    output_path = "D:/RoboX/04_听记纪要/转写与纪要/09-08 RoboX与长虹机器人业务财务团队战略合作洽谈（清理版）.docx"
    doc.save(output_path)
    print(f"✅ Word 文档已生成: {output_path}")

    # 文件信息
    file_size = os.path.getsize(output_path) / 1024
    print(f"📦 文件大小: {file_size:.1f} KB")
    print(f"📅 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # 段落数统计
    para_count = len(doc.paragraphs)
    print(f"📝 段落数: {para_count}")


if __name__ == "__main__":
    main()
