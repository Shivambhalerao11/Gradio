import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets", exist_ok=True)
os.makedirs("icons", exist_ok=True)

# 1. Create a cute sample cat image (400x300)
cat_img = Image.new("RGB", (500, 380), color="#1E293B")
draw = ImageDraw.Draw(cat_img)

# Soft gradient background simulation
for i in range(380):
    r = int(30 + (i / 380) * 20)
    g = int(41 + (i / 380) * 30)
    b = int(59 + (i / 380) * 40)
    draw.line([(0, i), (500, i)], fill=(r, g, b))

# Draw cute stylized cat silhouette / illustration
# Ears
draw.polygon([(170, 140), (210, 70), (240, 150)], fill="#E2E8F0")
draw.polygon([(185, 135), (210, 85), (230, 145)], fill="#F472B6")

draw.polygon([(330, 140), (290, 70), (260, 150)], fill="#E2E8F0")
draw.polygon([(315, 135), (290, 85), (270, 145)], fill="#F472B6")

# Head
draw.ellipse([(170, 110), (330, 270)], fill="#F8FAFC")

# Eyes
draw.ellipse([(205, 160), (235, 195)], fill="#0EA5E9")
draw.ellipse([(265, 160), (295, 195)], fill="#0EA5E9")
draw.ellipse([(220, 165), (232, 185)], fill="#0F172A")
draw.ellipse([(280, 165), (292, 185)], fill="#0F172A")
draw.ellipse([(227, 168), (232, 175)], fill="#FFFFFF")
draw.ellipse([(287, 168), (292, 175)], fill="#FFFFFF")

# Nose & Mouth
draw.polygon([(243, 205), (257, 205), (250, 215)], fill="#F472B6")
draw.arc([(230, 212), (250, 226)], start=0, end=180, fill="#475569", width=3)
draw.arc([(250, 212), (270, 226)], start=0, end=180, fill="#475569", width=3)

# Whiskers
draw.line([(150, 195), (200, 200)], fill="#CBD5E1", width=2)
draw.line([(140, 215), (195, 210)], fill="#CBD5E1", width=2)
draw.line([(300, 200), (350, 195)], fill="#CBD5E1", width=2)
draw.line([(305, 210), (360, 215)], fill="#CBD5E1", width=2)

# Collar & Bell
draw.rectangle([(210, 255), (290, 270)], fill="#6366F1")
draw.ellipse([(240, 265), (260, 285)], fill="#F59E0B")

# Label text
try:
    draw.text((20, 20), "cat_image.jpg", fill="#94A3B8")
except Exception:
    pass

cat_img.save("assets/cat_image.jpg")
print("Saved assets/cat_image.jpg")

# 2. Create Bot Avatar (128x128)
bot_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
b_draw = ImageDraw.Draw(bot_img)
b_draw.ellipse([(4, 4), (124, 124)], fill="#4F8BFF")
b_draw.rectangle([(34, 44), (94, 84)], fill="#FFFFFF")
b_draw.ellipse([(44, 54), (58, 68)], fill="#1E293B")
b_draw.ellipse([(70, 54), (84, 68)], fill="#1E293B")
b_draw.rectangle([(54, 74), (74, 78)], fill="#64748B")
bot_img.save("icons/bot_avatar.png")
print("Saved icons/bot_avatar.png")

# 3. Create User Avatar (128x128)
user_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
u_draw = ImageDraw.Draw(user_img)
u_draw.ellipse([(4, 4), (124, 124)], fill="#6C5CE7")
u_draw.ellipse([(44, 28), (84, 68)], fill="#FFFFFF")
u_draw.ellipse([(24, 74), (104, 124)], fill="#FFFFFF")
user_img.save("icons/user_avatar.png")
print("Saved icons/user_avatar.png")

# 4. Create Slack logo SVG
slack_svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 127.14 127.14" width="64" height="64">
  <path fill="#E01E5A" d="M27.35,79.51a13.68,13.68,0,1,1-13.68-13.68H27.35ZM34.18,79.51a13.68,13.68,0,1,1,27.35,0V106.86a13.68,13.68,0,1,1-27.35,0Z"/>
  <path fill="#36C5F0" d="M47.63,27.35a13.68,13.68,0,1,1,13.68-13.68V27.35ZM47.63,34.18a13.68,13.68,0,1,1,0,27.35H20.28a13.68,13.68,0,1,1,0-27.35Z"/>
  <path fill="#2EB67D" d="M99.79,47.63a13.68,13.68,0,1,1,13.68,13.68H99.79ZM92.96,47.63a13.68,13.68,0,1,1-27.35,0V20.28a13.68,13.68,0,1,1,27.35,0Z"/>
  <path fill="#ECB22E" d="M79.51,99.79a13.68,13.68,0,1,1-13.68,13.68V99.79ZM79.51,92.96a13.68,13.68,0,1,1,0-27.35H106.86a13.68,13.68,0,1,1,0,27.35Z"/>
</svg>"""
with open("icons/slack.svg", "w", encoding="utf-8") as f:
    f.write(slack_svg)
print("Saved icons/slack.svg")
