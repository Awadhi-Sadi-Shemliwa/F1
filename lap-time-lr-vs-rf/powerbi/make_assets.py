"""Builds the Power BI styling assets: theme JSON, page backgrounds, animated race strip GIF."""
import json, math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = Path(__file__).parent / "assets"; OUT.mkdir(exist_ok=True)
LR, RF, RED = "#38A3FF", "#FF7A2F", "#E10600"
BG, PANEL, BORDER, TEXT, MUTED = "#0A0D13", "#121824", "#27324A", "#F3F5F9", "#9AA3B5"

def font(size, bold=False):
    names = ["DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"]
    for n in names:
        for d in ["/usr/share/fonts/truetype/dejavu/", ""]:
            try: return ImageFont.truetype(d + n, size)
            except OSError: pass
    return ImageFont.load_default()

def hexrgb(h, a=255): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (a,)

# ---------------------------------------------------------------- theme
theme = {
  "name": "F1 Night Race",
  "dataColors": [LR, RF, "#FF9A57", "#B07CFF", "#FF4F9A", "#7C8CFF", "#FFD23F", RED],
  "background": BG, "foreground": TEXT, "tableAccent": RED,
  "good": "#2BD67B", "neutral": "#FFD23F", "bad": RED,
  "textClasses": {
    "callout": {"fontSize": 28, "fontFace": "Segoe UI Bold", "color": TEXT},
    "title":   {"fontSize": 13, "fontFace": "Segoe UI Semibold", "color": TEXT},
    "header":  {"fontSize": 12, "fontFace": "Segoe UI Semibold", "color": TEXT},
    "label":   {"fontSize": 10, "fontFace": "Segoe UI", "color": "#C9D0DE"}
  },
  "visualStyles": {
    "*": {"*": {
      "background": [{"show": True, "color": {"solid": {"color": PANEL}}, "transparency": 12}],
      "border": [{"show": True, "color": {"solid": {"color": BORDER}}, "radius": 12}],
      "dropShadow": [{"show": True, "color": {"solid": {"color": "#000000"}}, "position": "Outer", "preset": "BottomRight"}],
      "title": [{"show": True, "fontColor": {"solid": {"color": TEXT}}, "fontSize": 13}],
      "subTitle": [{"fontColor": {"solid": {"color": MUTED}}}],
      "visualHeader": [{"foreground": {"solid": {"color": MUTED}}, "background": {"solid": {"color": PANEL}}, "border": {"solid": {"color": BORDER}}}],
      "categoryAxis": [{"labelColor": {"solid": {"color": "#C9D0DE"}}, "titleColor": {"solid": {"color": MUTED}}, "gridlineColor": {"solid": {"color": "#222B3D"}}}],
      "valueAxis": [{"labelColor": {"solid": {"color": "#C9D0DE"}}, "titleColor": {"solid": {"color": MUTED}}, "gridlineColor": {"solid": {"color": "#222B3D"}}}],
      "legend": [{"labelColor": {"solid": {"color": "#DDE2EC"}}}],
      "labels": [{"color": {"solid": {"color": TEXT}}}],
      "smallMultiplesLayout": [{"gridLineColor": {"solid": {"color": BORDER}}}],
      "subheader": [{"fontColor": {"solid": {"color": "#DDE2EC"}}}]
    }},
    "slicer": {"*": {
      "items": [{"fontColor": {"solid": {"color": TEXT}}, "background": {"solid": {"color": "#18202F"}}, "outlineColor": {"solid": {"color": BORDER}}}],
      "header": [{"fontColor": {"solid": {"color": MUTED}}, "show": True}],
      "selection": [{"selectAllCheckboxEnabled": False}]
    }},
    "tableEx": {"*": {
      "columnHeaders": [{"fontColor": {"solid": {"color": "#FFFFFF"}}, "backColor": {"solid": {"color": "#1E2737"}}}],
      "values": [{"fontColorPrimary": {"solid": {"color": TEXT}}, "backColorPrimary": {"solid": {"color": PANEL}},
                  "fontColorSecondary": {"solid": {"color": TEXT}}, "backColorSecondary": {"solid": {"color": "#161D2B"}}}],
      "grid": [{"gridHorizontalColor": {"solid": {"color": BORDER}}, "gridVerticalColor": {"solid": {"color": BORDER}}, "outlineColor": {"solid": {"color": BORDER}}}]
    }},
    "page": {"*": {
      "background": [{"color": {"solid": {"color": BG}}, "transparency": 0}],
      "outspace": [{"color": {"solid": {"color": "#05070B"}}, "transparency": 0}]
    }}
  }
}
(OUT / "F1_Night_Race_theme.json").write_text(json.dumps(theme, indent=2))

# ---------------------------------------------------------------- page backgrounds (1920 x 1200)
W, H, HEADER = 1920, 1200, 112

def carbon(w, h):
    img = Image.new("RGBA", (w, h), hexrgb(BG))
    d = ImageDraw.Draw(img)
    s = 8
    for y in range(0, h, s):
        for x in range(0, w, s):
            shade = 16 if ((x // s) + (y // s)) % 2 == 0 else 11
            d.rectangle([x, y, x + s - 1, y + s // 2 - 1], fill=(shade, shade + 2, shade + 6, 255))
            d.rectangle([x, y + s // 2, x + s - 1, y + s - 1], fill=(shade - 3, shade - 1, shade + 3, 255))
    return img

def background(title, subtitle, fname):
    img = carbon(W, H)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    # diagonal speed streaks
    rnd = random.Random(7)
    for _ in range(46):
        x = rnd.randint(-300, W); y = rnd.randint(HEADER + 20, H); L = rnd.randint(180, 520)
        col = hexrgb(rnd.choice([LR, RF, RED, "#FFFFFF"]), rnd.randint(28, 70))
        g.line([x, y, x + L, y - L * 0.18], fill=col, width=rnd.randint(1, 3))
    glow = glow.filter(ImageFilter.GaussianBlur(1.2)); img.alpha_composite(glow)
    halo = Image.new("RGBA", (W, H), (0, 0, 0, 0)); hd = ImageDraw.Draw(halo)
    hd.ellipse([-500, 500, 700, 1500], fill=hexrgb(LR, 38)); hd.ellipse([1300, -300, 2400, 700], fill=hexrgb(RF, 34))
    hd.ellipse([700, 900, 1500, 1500], fill=hexrgb(RED, 22))
    img.alpha_composite(halo.filter(ImageFilter.GaussianBlur(160)))
    d = ImageDraw.Draw(img)
    # header band
    for y in range(HEADER):
        t = y / HEADER
        d.line([0, y, W, y], fill=(int(8 + 10 * t), int(10 + 10 * t), int(16 + 14 * t), 255))
    # red accent + kerb under header
    d.rectangle([0, HEADER - 6, W, HEADER - 2], fill=hexrgb(RED))
    for i, x in enumerate(range(0, W, 40)):
        d.rectangle([x, HEADER - 2, x + 39, HEADER + 4], fill=hexrgb(RED) if i % 2 == 0 else (240, 240, 240, 255))
    # chequered flag block
    cs = 13
    for r in range(8):
        for c in range(3):
            if (r + c) % 2 == 0:
                d.rectangle([14 + c * cs, 4 + r * cs, 14 + c * cs + cs - 1, 4 + r * cs + cs - 1], fill=(238, 238, 238, 255))
    d.text((70, 14), title, font=font(44, True), fill=hexrgb(TEXT))
    d.text((72, 70), subtitle, font=font(19), fill=hexrgb(MUTED))
    # footer signature
    d.text((W - 520, H - 22), "Data: FastF1 · 2023 Italian GP race · INM431 mini-project", font=font(13), fill=(110, 120, 140, 255))
    img.convert("RGB").save(OUT / fname, optimize=True)

background("F1 LAP-TIME LAB", "Linear Regression vs Random Forest  ·  2023 Italian GP (Monza)  ·  862 laps",
           "bg_page1_model_comparison.png")
background("FORECAST & PREDICTION", "Trained on laps 2-38  ·  predicting laps 39-51",
           "bg_page2_forecast.png")

# ---------------------------------------------------------------- animated race strip GIF
GW, GH, SCALE = 760, 92, 2
FR = 40
def car(d, x, y, col, label, phase, s):
    """Original generic open-wheel race car, side view, facing right. (x, y) = rear-wheel ground contact."""
    c = hexrgb(col); dark = (20, 22, 28, 255); car_len = 150 * s
    # shadow
    d.ellipse([x - 12 * s, y - 3 * s, x + car_len, y + 4 * s], fill=(0, 0, 0, 110))
    # rear wing
    d.polygon([(x - 14 * s, y - 34 * s), (x + 6 * s, y - 34 * s), (x + 6 * s, y - 27 * s), (x - 14 * s, y - 27 * s)], fill=c)
    d.rectangle([x - 4 * s, y - 27 * s, x + 1 * s, y - 16 * s], fill=dark)
    # main body / sidepod / nose
    body = [(x - 6 * s, y - 20 * s), (x + 40 * s, y - 24 * s), (x + 62 * s, y - 30 * s), (x + 80 * s, y - 24 * s),
            (x + 140 * s, y - 13 * s), (x + 152 * s, y - 9 * s), (x + 150 * s, y - 6 * s), (x + 100 * s, y - 7 * s),
            (x + 20 * s, y - 8 * s), (x - 6 * s, y - 10 * s)]
    d.polygon(body, fill=c)
    d.polygon([(x + 30 * s, y - 13 * s), (x + 120 * s, y - 11 * s), (x + 150 * s, y - 7 * s), (x + 30 * s, y - 8 * s)], fill=(255, 255, 255, 60))
    # cockpit, halo, helmet
    d.ellipse([x + 56 * s, y - 37 * s, x + 70 * s, y - 25 * s], fill=(245, 245, 245, 255))
    d.rectangle([x + 58 * s, y - 33 * s, x + 69 * s, y - 30 * s], fill=dark)
    d.line([(x + 48 * s, y - 31 * s), (x + 64 * s, y - 39 * s), (x + 80 * s, y - 27 * s)], fill=dark, width=max(2, int(2 * s)))
    # front wing
    d.polygon([(x + 128 * s, y - 6 * s), (x + 158 * s, y - 6 * s), (x + 158 * s, y - 2 * s), (x + 128 * s, y - 2 * s)], fill=dark)
    # wheels with rotating spokes
    for wx in (x + 8 * s, x + 118 * s):
        r = 14 * s; cy = y - r
        d.ellipse([wx - r, cy - r, wx + r, cy + r], fill=(14, 14, 16, 255))
        d.ellipse([wx - r * 0.55, cy - r * 0.55, wx + r * 0.55, cy + r * 0.55], fill=(70, 74, 84, 255))
        for k in range(3):
            a = phase + k * 2 * math.pi / 3
            d.line([(wx, cy), (wx + r * 0.5 * math.cos(a), cy + r * 0.5 * math.sin(a))], fill=(170, 176, 188, 255), width=max(1, int(1.5 * s)))
    # number board on sidepod
    d.text((x + 86 * s, y - 24 * s), label, font=font(int(11 * s), True), fill=(255, 255, 255, 255))
    # rain light flashing
    if int(phase * 2) % 2 == 0:
        d.rectangle([x - 16 * s, y - 22 * s, x - 12 * s, y - 18 * s], fill=hexrgb(RED))

frames = []
for f in range(FR):
    t = f / FR
    W2, H2 = GW * SCALE, GH * SCALE
    im = Image.new("RGBA", (W2, H2), (16, 19, 26, 255)); d = ImageDraw.Draw(im)
    # asphalt texture lines
    off = int(t * 120 * SCALE)
    for k in range(-2, W2 // (120 * SCALE) + 3):
        x0 = k * 120 * SCALE - off
        d.rectangle([x0, H2 // 2 - 2 * SCALE, x0 + 60 * SCALE, H2 // 2 + 1 * SCALE], fill=(200, 205, 215, 120))
    # kerbs top & bottom
    koff = int(t * 40 * SCALE)
    for k in range(-2, W2 // (40 * SCALE) + 3):
        x0 = k * 40 * SCALE - koff
        colk = hexrgb(RED) if k % 2 == 0 else (235, 235, 235, 255)
        d.rectangle([x0, H2 - 6 * SCALE, x0 + 40 * SCALE, H2], fill=colk)
        d.rectangle([x0, 0, x0 + 40 * SCALE, 4 * SCALE], fill=colk)
    # speed streaks
    rnd = random.Random(3)
    for _ in range(14):
        sy = rnd.randint(8, GH - 10) * SCALE; L = rnd.randint(30, 90) * SCALE
        sx = (rnd.randint(0, W2) - int(t * W2 * 2)) % (W2 + L) - L
        d.line([sx, sy, sx + L, sy], fill=(255, 255, 255, 40), width=SCALE)
    # cars: RF leads, LR closes in and pulls level (forecast twist), seamless loop
    s = 0.62 * SCALE
    rf_x = (330 + 40 * math.sin(2 * math.pi * t)) * SCALE
    lr_x = (230 + 70 * math.sin(2 * math.pi * t + 1.3)) * SCALE
    car(d, lr_x, 50 * SCALE, LR, "LR", 2 * math.pi * t * 6, s)
    car(d, rf_x, 86 * SCALE, RF, "RF", 2 * math.pi * t * 6 + 1, s)
    # finish gantry text
    d.text((W2 - 210 * SCALE, 10 * SCALE), "LIGHTS OUT", font=font(12 * SCALE, True), fill=(255, 255, 255, 200))
    for i in range(5):
        on = i < int((t * 10) % 6)
        cx = W2 - 205 * SCALE + i * 24 * SCALE
        d.ellipse([cx, 30 * SCALE, cx + 14 * SCALE, 44 * SCALE], fill=hexrgb(RED) if on else (60, 20, 20, 255))
    frames.append(im.resize((GW, GH), Image.LANCZOS).convert("RGB").quantize(colors=96, method=Image.MEDIANCUT, dither=Image.NONE))

frames[0].save(OUT / "race_strip.gif", save_all=True, append_images=frames[1:], duration=45, loop=0, optimize=True, disposal=2)
frames[0].convert("RGB").save(OUT / "race_strip_preview.png")
print("done", [p.name for p in OUT.iterdir()])
