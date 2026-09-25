import qrcode
from PIL import Image, ImageDraw, ImageFont

url = "https://ai-native-d8gox2tz63118e2f3-1334209523.tcloudbaseapp.com/"

# 1) 二维码 PNG
qr = qrcode.QRCode(box_size=12, border=4)
qr.add_data(url)
qr.make(fit=True)
qr_img = qr.make_image(fill_color="#1f3d5e", back_color="white")
qr_img.save(r"e:\11-其他\ray-plan-qr.png")
print("qr saved")

# 2) 分享卡片 800x1000
W, H = 800, 1000
card = Image.new("RGB", (W, H), "#f5f6f8")
d = ImageDraw.Draw(card)
d.rectangle([0, 0, W, 300], fill="#1f3d5e")

font_title = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 38)
font_sub = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)
font_note = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 22)
font_url = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 24)

d.text((40, 60), "Ray 升学规划 · 专业选择篇", font=font_title, fill="#ffd98a")
d.text((40, 140), "墨尔本大学 · 双目标兼顾", font=font_sub, fill="#ffffff")
d.text((40, 190), "美国 MFE 硕士 + 澳洲移民", font=font_sub, fill="#d9e8e5")

qr_big = qr.make_image(fill_color="#1f3d5e", back_color="white").convert("RGB")
qr_big = qr_big.resize((520, 520), Image.LANCZOS)
card.paste(qr_big, ((W - 520) // 2, 320))

d.text((40, 872), "扫一扫，查看完整规划", font=font_note, fill="#5b6b7b")
d.text((40, 920), url, font=font_url, fill="#1f3d5e")

card.save(r"e:\11-其他\ray-plan-share.png")
print("share card saved")
