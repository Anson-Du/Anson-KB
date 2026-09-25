import re
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

input_path = r"D:\RoboX\04_听记纪要\转写与纪要\08-10 RoboX团队讨论（清理版）.txt"
output_path = r"D:\RoboX\04_听记纪要\转写与纪要\08-10 RoboX团队讨论（清理版）.docx"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

doc = Document()

# Page margins
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.18)
    section.right_margin = Cm(3.18)

# Set default font
style = doc.styles['Normal']
font = style.font
font.name = '微软雅黑'
font.size = Pt(11)
style.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

# Paragraph spacing defaults
pf = style.paragraph_format
pf.space_after = Pt(6)
pf.space_before = Pt(0)
pf.line_spacing = 1.5

separator_pattern = re.compile(r'^[=]+')

for line in lines:
    line = line.rstrip('\n').rstrip('\r')
    stripped = line.strip()

    # Skip empty lines
    if not stripped:
        continue

    # Skip separator lines
    if separator_pattern.match(stripped):
        continue

    # Title (first non-empty line)
    if stripped == lines[0].strip():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(12)
        run = p.add_run(stripped)
        run.font.name = '微软雅黑'
        run.font.size = Pt(18)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x1a, 0x1a, 0x2e)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        continue

    # Meta info (参会人/时长)
    if stripped.startswith('参会人') or stripped.startswith('时长'):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(stripped)
        run.font.name = '微软雅黑'
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(0x66, 0x66, 0x66)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        continue

    # Chapter headers (一、二、三...)
    chapter_pattern = re.compile(r'^[一二三四五六七八九十]+、')
    if chapter_pattern.match(stripped):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(18)
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(stripped)
        run.font.name = '微软雅黑'
        run.font.size = Pt(14)
        run.font.bold = True
        run.font.color.rgb = RGBColor(0x18, 0x5F, 0xA5)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
        # Add bottom border
        pPr = p._p.get_or_add_pPr()
        pBdr = pPr.makeelement(qn('w:pBdr'), {})
        bottom = pBdr.makeelement(qn('w:bottom'), {
            qn('w:val'): 'single',
            qn('w:sz'): '6',
            qn('w:space'): '4',
            qn('w:color'): '185FA5'
        })
        pBdr.append(bottom)
        pPr.append(pBdr)
        continue

    # Content paragraphs with speaker names
    # Detect speaker: "姓名：" or "姓名:"
    speaker_pattern = re.compile(r'^(明修|Eric|Anson|田明|静婷|技术成员A|技术成员B|团队成员)([：:])(.*)')
    match = speaker_pattern.match(stripped)
    if match:
        speaker = match.group(1)
        rest = match.group(3)

        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(8)
        p.paragraph_format.first_line_indent = Cm(0)

        # Speaker name in bold
        run_speaker = p.add_run(speaker + '：')
        run_speaker.font.name = '微软雅黑'
        run_speaker.font.size = Pt(11)
        run_speaker.font.bold = True
        run_speaker.font.color.rgb = RGBColor(0x53, 0x4A, 0xB7)
        run_speaker.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

        # Content
        run_content = p.add_run(rest)
        run_content.font.name = '微软雅黑'
        run_content.font.size = Pt(11)
        run_content.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')
    else:
        # Regular content paragraph
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        run = p.add_run(stripped)
        run.font.name = '微软雅黑'
        run.font.size = Pt(11)
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '微软雅黑')

doc.save(output_path)
print(f"Word文档已生成: {output_path}")
print(f"段落数: {len(doc.paragraphs)}")
