"""
utils/image_utils.py
--------------------
Image generation utilities used by the asset creation script.
Isolated here so create_assets.py stays clean and these helpers
can be tested independently.
"""

from __future__ import annotations

from PIL import Image, ImageDraw


def create_cat_image(width: int = 500, height: int = 380) -> Image.Image:
    """Generate the stylised cat illustration used as the demo sample image."""
    img  = Image.new("RGB", (width, height), color="#1E293B")
    draw = ImageDraw.Draw(img)

    # Gradient background
    for i in range(height):
        r = int(30 + (i / height) * 20)
        g = int(41 + (i / height) * 30)
        b = int(59 + (i / height) * 40)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

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

    # Nose & mouth
    draw.polygon([(243, 205), (257, 205), (250, 215)], fill="#F472B6")
    draw.arc([(230, 212), (250, 226)], start=0, end=180, fill="#475569", width=3)
    draw.arc([(250, 212), (270, 226)], start=0, end=180, fill="#475569", width=3)

    # Whiskers
    draw.line([(150, 195), (200, 200)], fill="#CBD5E1", width=2)
    draw.line([(140, 215), (195, 210)], fill="#CBD5E1", width=2)
    draw.line([(300, 200), (350, 195)], fill="#CBD5E1", width=2)
    draw.line([(305, 210), (360, 215)], fill="#CBD5E1", width=2)

    # Collar & bell
    draw.rectangle([(210, 255), (290, 270)], fill="#6366F1")
    draw.ellipse([(240, 265), (260, 285)],   fill="#F59E0B")

    return img


def create_bot_avatar(size: int = 128) -> Image.Image:
    """Generate the circular bot avatar icon."""
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    p    = 4  # padding

    draw.ellipse([(p, p), (size - p, size - p)], fill="#4F8BFF")
    draw.rectangle([(34, 44), (94, 84)],         fill="#FFFFFF")
    draw.ellipse([(44, 54), (58, 68)],           fill="#1E293B")
    draw.ellipse([(70, 54), (84, 68)],           fill="#1E293B")
    draw.rectangle([(54, 74), (74, 78)],         fill="#64748B")
    return img


def create_user_avatar(size: int = 128) -> Image.Image:
    """Generate the circular user avatar icon."""
    img  = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    p    = 4

    draw.ellipse([(p, p), (size - p, size - p)], fill="#6C5CE7")
    draw.ellipse([(44, 28), (84, 68)],            fill="#FFFFFF")
    draw.ellipse([(24, 74), (104, 124)],          fill="#FFFFFF")
    return img


SLACK_SVG: str = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 127.14 127.14" width="64" height="64">
  <path fill="#E01E5A" d="M27.35,79.51a13.68,13.68,0,1,1-13.68-13.68H27.35ZM34.18,79.51a13.68,13.68,0,1,1,27.35,0V106.86a13.68,13.68,0,1,1-27.35,0Z"/>
  <path fill="#36C5F0" d="M47.63,27.35a13.68,13.68,0,1,1,13.68-13.68V27.35ZM47.63,34.18a13.68,13.68,0,1,1,0,27.35H20.28a13.68,13.68,0,1,1,0-27.35Z"/>
  <path fill="#2EB67D" d="M99.79,47.63a13.68,13.68,0,1,1,13.68,13.68H99.79ZM92.96,47.63a13.68,13.68,0,1,1-27.35,0V20.28a13.68,13.68,0,1,1,27.35,0Z"/>
  <path fill="#ECB22E" d="M79.51,99.79a13.68,13.68,0,1,1-13.68,13.68V99.79ZM79.51,92.96a13.68,13.68,0,1,1,0-27.35H106.86a13.68,13.68,0,1,1,0,27.35Z"/>
</svg>"""
