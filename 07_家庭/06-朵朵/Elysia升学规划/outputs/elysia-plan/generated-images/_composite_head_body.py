from PIL import Image, ImageFilter
import numpy as np

def remove_white_bg(img, threshold=245):
    """把接近白色的背景转为透明，保留主体；仅对外轮廓做羽化。"""
    arr = np.array(img)
    luminance = arr[:, :, :3].mean(axis=2)
    # 硬 mask：白色背景透明，主体不透明
    alpha = np.where(luminance > threshold, 0, 255).astype(np.uint8)
    arr[:, :, 3] = alpha
    img_rgba = Image.fromarray(arr, 'RGBA')
    # 对 alpha 通道做轻微高斯模糊，仅柔化边缘锯齿，不改变主体透明度
    r, g, b, a = img_rgba.split()
    a = a.filter(ImageFilter.GaussianBlur(radius=1.5))
    return Image.merge('RGBA', (r, g, b, a))

# 加载
head = Image.open('d:/RoboX/generated-images/68dc80056b076088e7848461b854424d.jpg').convert('RGBA')
body = Image.open('d:/RoboX/generated-images/A_3D_render_of_a_cute_chibi_pl_2026-08-09T06-49-30.png').convert('RGBA')

# 去背景
head = remove_white_bg(head, threshold=245)

# 裁掉身体顶部 28%（去掉颈部开口硬边），保留更多躯干
bw, bh = body.size
crop_top = int(bh * 0.28)
body = body.crop((0, crop_top, bw, bh))
bw, bh = body.size

# 头部保持原尺寸
hw, hh = head.size

# 缩放身体：宽度接近头部，让头身更协调
body_width = int(hw * 0.82)
body_height = int(bh * body_width / bw)
body = body.resize((body_width, body_height), Image.LANCZOS)

# 画布尺寸
canvas_w = max(hw, body_width) + 80
canvas_h = hh + body_height - int(hh * 0.38)  # 头部大幅下沉，覆盖身体裁剪区

# 创建白色背景画布
canvas = Image.new('RGBA', (canvas_w, canvas_h), (255, 255, 255, 255))

# 先放身体（居中，底部对齐）
body_x = (canvas_w - body_width) // 2
body_y = canvas_h - body_height
canvas.paste(body, (body_x, body_y), body)

# 放头部（居中，稍微下沉覆盖身体）
head_x = (canvas_w - hw) // 2
head_y = 0
canvas.paste(head, (head_x, head_y), head)

# 在头部与身体交界处做轻微羽化阴影，掩盖硬边
# 创建一个小阴影条放在头部下方、身体上方
shadow_h = 40
shadow = Image.new('RGBA', (canvas_w, shadow_h), (200, 200, 200, 0))
for y in range(shadow_h):
    alpha = int(25 * (1 - y / shadow_h))
    for x in range(canvas_w):
        shadow.putpixel((x, y), (160, 160, 160, alpha))

shadow_y = head_y + hh - int(hh * 0.10)
canvas.paste(shadow, (0, shadow_y), shadow)

# 转 RGB 保存
final = canvas.convert('RGB')
final.save('d:/RoboX/generated-images/RoboX_composite_final.png')
print(f'Saved composite: {final.size}')
