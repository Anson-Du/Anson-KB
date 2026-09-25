# -*- coding: utf-8 -*-
"""
为 RoboX BP PDF 添加水印
水印字样: To 成都高新区数字经济局

思路：
1. 用 reportlab 按原页尺寸生成 overlay（对角水印）
2. 用 pypdf 把 overlay 合并到原 PDF 每一页
"""

import io
import os
import warnings

warnings.filterwarnings("ignore")

from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader, PdfWriter

# ========== 配置 ==========
SRC = r"D:\RoboX\02_股权融资\BP\RoboX Robotics - 1.0.4.pdf"
DST = r"D:\RoboX\02_股权融资\BP\RoboX Robotics - 1.0.4 (To 成都高新区数字经济局).pdf"
WATERMARK = "To 成都高新区数字经济局"

# ========== 字体注册 ==========
FONT_NAME = "MSYH"
FONT_PATH = r"C:\Windows\Fonts\msyh.ttc"
if os.path.exists(FONT_PATH):
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_PATH, subfontIndex=0))
    print(f"[字体] 已注册微软雅黑: {FONT_PATH}")
else:
    from reportlab.pdfbase.cidfonts import UnicodeCIDFont
    pdfmetrics.registerFont(UnicodeCIDFont("STSong-Light"))
    FONT_NAME = "STSong-Light"
    print("[字体] 回退到 STSong-Light")

# ========== 水印样式 ==========
# 注意：本 BP 全部为深色版面（黑/深蓝底），水印必须用浅色才够清晰
WM_COLOR = Color(0.72, 0.76, 0.85)   # 亮银蓝（深底上呈清晰浅灰蓝）
WM_ALPHA = 0.45                       # 单层透明度（v1=0.17 太浅，v3=0.45+浅色）
FONT_SIZE = 50
ROTATION = 30                         # 旋转角度（度）


def make_overlay(width, height):
    """生成单页 overlay PDF（bytes）"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(width, height))

    c.saveState()
    c.setFillColor(WM_COLOR)
    c.setFillAlpha(WM_ALPHA)

    # 沿对角方向铺 3 层，形成密度适中的覆盖，不易被裁切规避
    # 布局：以页面中心为基准，沿垂直方向上下偏移
    offsets = [0]
    if height > 400:
        offsets = [height * 0.30, 0, -height * 0.30]

    for dy in offsets:
        c.saveState()
        c.translate(width / 2.0, height / 2.0 + dy)
        c.rotate(ROTATION)
        c.setFont(FONT_NAME, FONT_SIZE)
        tw = c.stringWidth(WATERMARK, FONT_NAME, FONT_SIZE)
        c.drawString(-tw / 2.0, 0, WATERMARK)
        c.restoreState()

    c.restoreState()
    c.save()
    buf.seek(0)
    return buf


def main():
    reader = PdfReader(SRC)
    writer = PdfWriter()

    total = len(reader.pages)
    for i, page in enumerate(reader.pages):
        box = page.mediabox
        w = float(box.width)
        h = float(box.height)

        overlay = PdfReader(make_overlay(w, h)).pages[0]

        # 兼容不同 pypdf 版本的合并 API
        try:
            page.merge_page(overlay)
        except AttributeError:
            from pypdf import Transformation
            page.merge_transformed_page(overlay, Transformation())

        writer.add_page(page)

        if (i + 1) % 5 == 0 or (i + 1) == total:
            print(f"  已处理 {i+1}/{total} 页")

    writer.add_metadata({
        "/Title": "RoboX Robotics BP 1.0.4 (To 成都高新区数字经济局)",
        "/Subject": WATERMARK,
        "/Keywords": "Confidential; 成都高新区数字经济局",
        "/Creator": "RoboX",
    })

    os.makedirs(os.path.dirname(DST), exist_ok=True)
    with open(DST, "wb") as f:
        writer.write(f)

    size_kb = os.path.getsize(DST) / 1024
    print(f"\n[完成] {DST}")
    print(f"[大小] {size_kb:.1f} KB  共 {total} 页")


if __name__ == "__main__":
    main()
