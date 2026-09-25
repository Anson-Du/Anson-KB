import urllib.request
import sys

url = "https://vcg-prod-1258344699.cos.ap-guangzhou.tencentcos.cn/text_to_video/results/1379431822/0943e55d-0a6d-4fa7-a0a0-f5a0af4fd25a_1786247967.mp4?q-sign-algorithm=sha1&q-ak=AKID8PcPB70x2Ibr49A1vnkdSBcTJ6lMrLgp&q-sign-time=1786248039%3B1786334439&q-key-time=1786248039%3B1786334439&q-header-list=host&q-url-param-list=&q-signature=1ada1e958979dc81cc63806bbcccf000904d7620"

output_path = r"d:\RoboX\04_听记纪要\Elysia_心_读书感受视频.mp4"

print(f"Downloading video from {url[:80]}...")
urllib.request.urlretrieve(url, output_path)
print(f"Video saved to: {output_path}")
