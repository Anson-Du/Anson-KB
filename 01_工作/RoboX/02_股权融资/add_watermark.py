#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
为PDF添加多行斜向水印 "ROBOX FOR AEF"
"""

import io
import math
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.colors import Color
from pypdf import PdfReader, PdfWriter

INPUT_PDF = r"D:\RoboX\02_股权融资\RoboX Robotics - 0.9.9.pdf"
OUTPUT_PDF = r"D:\RoboX\02_股权融资\RoboX Robotics - 0.9.9 (watermarked).pdf"
WATERMARK_TEXT = "ROBOX FOR AEF"

def create_watermark_overlay(page_width, page_height):
    """创建一页水印PDF（透明背景 + 多行斜向重复文字）"""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=(page_width, page_height))

    # 水印颜色：浅灰色，透明度约25%
    watermark_color = Color(0.5, 0.5, 0.5, alpha=0.25)
    c.setFillColor(watermark_color)
    
    # 字体大小
    font_size = 28
    c.setFont("Helvetica-Bold", font_size)

    # 旋转45度
    angle = math.radians(45)
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    # 计算文字宽度（近似）
    text_width = c.stringWidth(WATERMARK_TEXT, "Helvetica-Bold", font_size)
    
    # 水印间距
    x_spacing = text_width + 120  # 水平间距
    y_spacing = 80                 # 垂直行间距

    # 计算覆盖整页所需的行列数（考虑旋转后对角线长度）
    diagonal = math.sqrt(page_width**2 + page_height**2)
    cols = int(diagonal / x_spacing) + 4
    rows = int(diagonal / y_spacing) + 4

    # 起始偏移，使水印均匀分布
    x_start = -diagonal / 2
    y_start = -diagonal / 2

    for row in range(rows):
        for col in range(cols):
            # 偶数行偏移半个间距，形成交错效果
            x_offset = (col * x_spacing) + (x_spacing / 2 if row % 2 == 1 else 0)
            x = x_start + x_offset
            y = y_start + row * y_spacing

            # 将旋转后的坐标映射到页面坐标系
            # 旋转45度: new_x = x*cos - y*sin, new_y = x*sin + y*cos
            rx = x * cos_a - y * sin_a + page_width / 2
            ry = x * sin_a + y * cos_a + page_height / 2

            # 只在页面范围内绘制（粗略裁剪）
            if -200 < rx < page_width + 200 and -200 < ry < page_height + 200:
                c.saveState()
                c.translate(rx, ry)
                c.rotate(45)
                c.drawCentredString(0, 0, WATERMARK_TEXT)
                c.restoreState()

    c.save()
    buf.seek(0)
    return buf


def add_watermark(input_path, output_path):
    """为PDF每一页添加水印"""
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for i, page in enumerate(reader.pages):
        # 获取页面尺寸
        page_width = float(page.mediabox.width)
        page_height = float(page.mediabox.height)

        # 创建该页尺寸对应的水印
        watermark_buf = create_watermark_overlay(page_width, page_height)
        watermark_reader = PdfReader(watermark_buf)
        watermark_page = watermark_reader.pages[0]

        # 将水印叠加到原页面上
        page.merge_page(watermark_page)
        writer.add_page(page)

        print(f"  第 {i+1}/{len(reader.pages)} 页水印添加完成")

    with open(output_path, "wb") as f:
        writer.write(f)
    print(f"\n输出文件: {output_path}")
    print(f"总页数: {len(reader.pages)}")


if __name__ == "__main__":
    print(f"输入文件: {INPUT_PDF}")
    print(f"水印文字: {WATERMARK_TEXT}")
    print(f"开始处理...\n")
    add_watermark(INPUT_PDF, OUTPUT_PDF)
    print("\n完成！")
