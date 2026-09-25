from PIL import Image

img = Image.open('d:/RoboX/generated-images/68dc80056b076088e7848461b854424d.jpg')
iw, ih = img.size
print(f'Original size: {iw}x{ih}')

# 下方预留 0.7 倍高度给身体
body_height = int(ih * 0.7)
new_h = ih + body_height
canvas = Image.new('RGB', (iw, new_h), (255, 255, 255))
canvas.paste(img, (0, 0))

canvas.save('d:/RoboX/generated-images/_ref_head_with_space.png')
print(f'Saved reference: {iw}x{new_h}')
