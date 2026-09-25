from PIL import Image, ImageFilter
import numpy as np

def remove_white_bg(img, threshold=245, blur=1.5, erode=0):
    """把接近白色的背景转为透明，保留主体；仅对外轮廓做羽化。"""
    arr = np.array(img)
    luminance = arr[:, :, :3].mean(axis=2)
    alpha = np.where(luminance > threshold, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha
    img_rgba = Image.fromarray(arr, 'RGBA')
    if blur > 0 or erode > 0:
        r, g, b, a = img_rgba.split()
        if blur > 0:
            a = a.filter(ImageFilter.GaussianBlur(radius=blur))
        # 腐蚀 alpha，去除 JPG 压缩产生的彩色毛边
        for _ in range(erode):
            a = a.filter(ImageFilter.MinFilter(size=3))
        return Image.merge('RGBA', (r, g, b, a))
    return img_rgba

# 加载
head_path = 'd:/RoboX/generated-images/68dc80056b076088e7848461b854424d.jpg'
body_path = 'd:/RoboX/generated-images/A_cute_anime_style_doll_body___2026-08-09T06-59-04.png'
out_path = 'd:/RoboX/generated-images/RoboX_sailor_composite.png'

head = Image.open(head_path).convert('RGBA')
body = Image.open(body_path).convert('RGBA')

# 去背景：头部羽化边缘但控制宽度，减少在身体彩色区域上的灰边
head = remove_white_bg(head, threshold=250, blur=0.6, erode=0)

# 头部保持原尺寸
hw, hh = head.size

# 身体比例参数：苗条长腿
body_width_ratio = 1.02        # 身体宽度相对头部宽度的比例
head_sink_ratio = 0.49         # 头部与身体重叠比例（头底部下沉覆盖身体的量）

# 缩放身体
bw, bh = body.size
body_width = int(hw * body_width_ratio)
body_height = int(bh * body_width / bw)
body = body.resize((body_width, body_height), Image.LANCZOS)

head_sink = int(hh * head_sink_ratio)

# 画布尺寸
pad_x = 60
pad_y = 60
canvas_w = max(hw, body_width) + pad_x * 2
canvas_h = pad_y * 2 + (hh - head_sink) + body_height

# 创建白色背景画布
canvas = Image.new('RGBA', (canvas_w, canvas_h), (255, 255, 255, 255))

# 放置身体（居中，底部对齐，留出下边距）
body_x = (canvas_w - body_width) // 2
body_y = canvas_h - body_height - pad_y
canvas.paste(body, (body_x, body_y), body)

# 放置头部（居中，头底部与身体颈部重叠）
head_x = (canvas_w - hw) // 2
head_y = body_y - hh + head_sink

# 创建仅包含头部区域的图层，使用 alpha_composite 合成
head_layer = Image.new('RGBA', (canvas_w, canvas_h), (255, 255, 255, 0))
head_layer.paste(head, (head_x, head_y), head)
canvas = Image.alpha_composite(canvas, head_layer)

# 不使用额外阴影，依靠头部 alpha 边缘自然过渡

# 转 RGB 保存
final = canvas.convert('RGB')
final.save(out_path)
print(f'Saved composite: {final.size}')
