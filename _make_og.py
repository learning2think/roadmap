"""Generate og.png — 1200x630 share-preview card, on-brand with the dashboard."""
from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630
BG       = (11, 11, 11)      # --bg
CARD     = (19, 19, 19)      # --bg-card
BORDER   = (42, 42, 42)      # --border-l
TEXT     = (236, 236, 236)
DIM      = (138, 138, 138)
SCIENCE  = (61, 158, 87)     # --science
SKILLS   = (26, 144, 120)    # --skills
VIS      = (70, 130, 180)    # --vis
STUDY    = (184, 146, 30)

def font(paths, size):
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default()

WF = os.environ.get("WINDIR", r"C:\Windows") + r"\Fonts"
def jb(name_variants, size):
    cands = []
    for n in name_variants:
        cands += [os.path.join(WF, n)]
    # JetBrains Mono if installed, else Consolas
    return font(cands, size)

f_brand = jb(["JetBrainsMono-Bold.ttf", "consolab.ttf"], 72)
f_role  = jb(["JetBrainsMono-Regular.ttf", "consola.ttf"], 30)
f_goal  = jb(["JetBrainsMono-Regular.ttf", "consola.ttf"], 24)
f_chip  = jb(["JetBrainsMono-Medium.ttf", "JetBrainsMono-Regular.ttf", "consola.ttf"], 23)
f_chipb = jb(["JetBrainsMono-Bold.ttf", "consolab.ttf"], 23)
f_foot  = jb(["JetBrainsMono-Regular.ttf", "consola.ttf"], 22)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# subtle border frame
d.rectangle([0, 0, W - 1, H - 1], outline=(24, 24, 24), width=1)
# left accent bar (like a card's border-left)
d.rectangle([0, 0, 6, H], fill=SCIENCE)

PAD = 84
y = 120

# prompt mark + handle
d.text((PAD, y), "// learning2think", font=f_brand, fill=TEXT)
y += 104

d.text((PAD, y), "computational neuroscience  ·  cheminformatics  ·  ML",
       font=f_role, fill=DIM)
y += 50

# thin accent rule
d.rectangle([PAD, y + 14, PAD + 360, y + 16], fill=SCIENCE)
y += 64

d.text((PAD, y), "med student  →  funded PhD  ·  In Silico BBB (open-source)",
       font=f_goal, fill=(170, 170, 170))

# metric chips row near the bottom
chips = [
    ("0.92", " AUC · BBB", SCIENCE),
    ("0.44", " R² · logBB", VIS),
    ("~1,500", " tests · CI", SKILLS),
    ("12", " REST endpoints", STUDY),
]
cx = PAD
cy = H - 150
ch = 56
for big, rest, accent in chips:
    tb = d.textbbox((0, 0), big, font=f_chipb)
    tr = d.textbbox((0, 0), rest, font=f_chip)
    wbig = tb[2] - tb[0]
    wrest = tr[2] - tr[0]
    cw = wbig + wrest + 44
    d.rectangle([cx, cy, cx + cw, cy + ch], fill=CARD, outline=BORDER, width=1)
    # top accent line
    d.rectangle([cx, cy, cx + cw, cy + 2], fill=accent)
    ty = cy + (ch - (tb[3] - tb[1])) / 2 - 4
    d.text((cx + 22, ty), big, font=f_chipb, fill=TEXT)
    d.text((cx + 22 + wbig, ty + 1), rest, font=f_chip, fill=DIM)
    cx += cw + 18

# footer right
foot = "learning2think.github.io/roadmap"
fb = d.textbbox((0, 0), foot, font=f_foot)
d.text((W - PAD - (fb[2] - fb[0]), H - 70), foot, font=f_foot, fill=(90, 90, 90))

img.save("og.png", "PNG")
print("wrote og.png", os.path.getsize("og.png"), "bytes")
