"""Builds F1_PowerBI_walkthrough.mp4 from Power BI screenshots captured in Chrome.

Each scene = one screenshot, cropped to the report page, with a gentle zoom
into the part being discussed, a red focus box, a plain-English caption and
the animated race strip re-composited into the header.  Title / explainer /
verdict cards are drawn with PIL.  Frames are piped to ffmpeg (H.264, 30 fps).
"""
import math, subprocess, sys, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SS = "/tmp/claude-chrome-screenshots-0k1jfr/"
ASSETS = "/home/claude/proj/powerbi/assets/"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/home/claude/proj/video/F1_PowerBI_walkthrough.mp4"
W, H, FPS = 1920, 1080, 30
XF = 0.5                      # crossfade seconds
TOP, VP_H, CAP_Y = 64, 836, 900

BG = (7, 9, 14); RED = (225, 6, 0); BLUE = (56, 163, 255); ORANGE = (255, 122, 47)
WHITE = (240, 243, 248); GREY = (160, 170, 185)
F = "/usr/share/fonts/opentype/inter/"
def font(w, s): return ImageFont.truetype(F + {"b": "Inter-Bold.otf", "x": "Inter-ExtraBold.otf",
                                                  "s": "Inter-SemiBold.otf", "m": "Inter-Medium.otf",
                                                  "r": "Inter-Regular.otf"}[w], s)

# ---------- race strip GIF frames ----------
gif = Image.open(ASSETS + "race_strip.gif")
STRIP = []
for i in range(gif.n_frames):
    gif.seek(i); STRIP.append(gif.convert("RGB"))
def strip_at(t): return STRIP[int(t * 1000 / 45) % len(STRIP)]

CROP = (212, 103, 1272, 760)          # report page inside a 1513x784 screenshot
STRIP_BOX = (433, 4, 848, 55)         # strip position inside the crop

def wrap(draw, text, fnt, width):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        test = (cur + " " + w_).strip()
        if draw.textlength(test, font=fnt) <= width: cur = test
        else: lines.append(cur); cur = w_
    if cur: lines.append(cur)
    return lines

# ---------- overlays ----------
def top_bar(progress, label):
    im = Image.new("RGBA", (W, TOP), BG + (255,))
    d = ImageDraw.Draw(im)
    # chequered flag
    for r in range(4):
        for c in range(4):
            if (r + c) % 2 == 0: d.rectangle([24 + c * 9, 14 + r * 9, 32 + c * 9, 22 + r * 9], fill=WHITE)
    d.text((72, 16), "F1 LAP-TIME LAB", font=font("x", 26), fill=WHITE)
    d.text((72 + d.textlength("F1 LAP-TIME LAB", font=font("x", 26)) + 18, 22),
           "Linear Regression vs Random Forest  ·  2023 Italian GP (Monza)", font=font("m", 18), fill=GREY)
    tw = d.textlength(label, font=font("s", 18))
    d.rounded_rectangle([W - tw - 56, 15, W - 24, 49], radius=17, fill=(30, 36, 48))
    d.text((W - tw - 40, 21), label, font=font("s", 18), fill=WHITE)
    d.rectangle([0, TOP - 4, W, TOP], fill=(40, 44, 55))
    d.rectangle([0, TOP - 4, int(W * progress), TOP], fill=RED)
    return im

def caption(chip, head, body):
    im = Image.new("RGBA", (W, H - CAP_Y), BG + (255,))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 2], fill=(40, 44, 55))
    d.rectangle([60, 26, 66, 150], fill=RED)
    x = 92
    if chip:
        cw = d.textlength(chip, font=font("b", 16))
        d.rounded_rectangle([x, 24, x + cw + 24, 50], radius=6, fill=RED)
        d.text((x + 12, 28), chip, font=font("b", 16), fill=WHITE)
        x2 = x + cw + 40
    else:
        x2 = x
    hf = font("b", 34)
    d.text((x2, 20), head, font=hf, fill=WHITE)
    bf = font("r", 27)
    for i, ln in enumerate(wrap(d, body, bf, W - 92 - 60)[:3]):
        d.text((92, 70 + i * 36), ln, font=bf, fill=GREY)
    return im

# ---------- scenes ----------
def S(f): return SS + f
P1, P2 = "PAGE 1 · MODEL COMPARISON", "PAGE 2 · FORECAST & PREDICTION"
SCENES = [
    ("card", "intro", 6.5),
    ("card", "explain", 12.0),
    ("shot", S("screenshot-1794746609949-1.jpg"), None, 6.5, P1, "Page 1: how close did each model get?",
     "Each model predicted all 862 laps, and every lap was predicted by a model that had never seen it. Blue = Linear Regression, orange = Random Forest, white = the real lap time."),
    ("shot", S("screenshot-1794746625612-4.jpg"), (220, 175, 475, 420), 6.0, P1, "Tick Random Forest: average miss 0.22 s",
     "On a typical lap the forest's guess is off by about two tenths of a second, quicker than a blink."),
    ("shot", S("screenshot-1794746625612-5.jpg"), (220, 175, 475, 420), 6.0, P1, "Switch to Linear Regression: 0.29 s",
     "The straight-line model misses by more. On normal laps the Random Forest is about 25 % more accurate."),
    ("shot", S("screenshot-1794746636630-6.jpg"), (220, 175, 1000, 420), 6.0, P1, "Only laps on Hard tyres",
     "Click the Hard tile and every chart updates. Hard-tyre laps: Linear Regression 0.28 s, Random Forest 0.22 s."),
    ("shot", S("screenshot-1794746651080-8.jpg"), (485, 175, 1000, 420), 5.5, P1, "Pick a driver: Lewis Hamilton",
     "The driver dropdown narrows the whole page to one car. Here we choose HAM."),
    ("shot", S("screenshot-1794746651081-9.jpg"), (220, 175, 1265, 420), 6.0, P1, "Hamilton on Hard tyres",
     "He used the Hard tyre from lap 2 to lap 26. Linear Regression 0.28 s, Random Forest 0.23 s off."),
    ("shot", S("screenshot-1794746674935-10.jpg"), (220, 175, 1265, 420), 6.0, P1, "Carlos Sainz on Hard tyres",
     "For the Ferrari of Sainz the forest is off by only 0.17 s per lap, against 0.25 s for the straight line."),
    ("shot", S("screenshot-1794746684177-11.jpg"), (220, 430, 870, 760), 7.0, P1, "Sainz's last 13 laps, fighting for the podium",
     "The white line is what really happened. The blue straight line stays flat; the orange forest follows the ups and downs. Error: 0.34 s vs 0.20 s."),
    ("shot", S("screenshot-1794746692512-12.jpg"), (875, 410, 1265, 760), 6.5, P1, "Hover any dot to see the lap",
     "Sainz, lap 48: really 86.80 s, the forest predicted 86.93 s. A perfect model would put every dot on the diagonal."),
    ("shot", S("screenshot-1794746782802-13.jpg"), (875, 430, 1265, 760), 6.0, P1, "Reset: all 862 laps",
     "The orange cloud hugs the diagonal more tightly than the blue one. On laps like the ones it learned from, Random Forest wins."),
    ("shot", S("screenshot-1794746782803-14.jpg"), None, 7.0, P2, "Page 2: the harder test, predicting the future",
     "Both models learn only from laps 2-38, then must predict laps 39-51, which they have never seen. That is like forecasting the end of the race from its first part."),
    ("shot", S("screenshot-1794746797218-15.jpg"), (220, 465, 870, 760), 7.0, P2, "The forest gets stuck on the future",
     "A Random Forest can only repeat answers it has already seen, so on older tyres it drifts. Lap 43: real 86.38 s, forecast 86.64 s."),
    ("shot", S("screenshot-1794746811427-18.jpg"), (220, 175, 870, 465), 7.0, P2, "The straight line keeps the trend going",
     "Linear Regression carries its rule forward (more fuel burnt = faster, older tyres = slower). On these future laps its error is 15 % smaller: 0.45 s vs 0.53 s."),
    ("shot", S("screenshot-1794746797219-16.jpg"), (875, 175, 1265, 455), 6.5, P2, "Which clues matter most?",
     "Longer bar = more important. For Linear Regression, lap number (fuel burning off) and tyre age matter most: tyre age alone is worth 0.46 s of accuracy."),
    ("shot", S("screenshot-1794746811427-19.jpg"), (875, 175, 1265, 455), 6.0, P2, "Click the legend to highlight Random Forest",
     "The forest spreads its attention: it also uses starting position, team and tyre type, which helps on normal laps."),
    ("shot", S("screenshot-1794746797220-17.jpg"), (875, 465, 1265, 760), 7.0, P2, "What-if prediction: a Ferrari on lap 30",
     "Each extra lap on the same tyres adds time. Hard (white) stays quicker than Medium (yellow): 26-lap-old tyres give 87.11 s on Hard vs 87.31 s on Medium."),
    ("card", "verdict", 10.0),
    ("card", "outro", 6.0),
]

def load_shot(path):
    im = Image.open(path).convert("RGB")
    if im.size != (1513, 784): im = im.resize((1513, 784), Image.LANCZOS)
    return im.crop(CROP)

def ease(x): x = max(0.0, min(1.0, x)); return x * x * (3 - 2 * x)

FIT = min(W / 1060, VP_H / 657)

def render_shot(src, focus, t, dur, cap, bar):
    base = src.copy()
    base.paste(strip_at(t).resize((STRIP_BOX[2] - STRIP_BOX[0], STRIP_BOX[3] - STRIP_BOX[1])), STRIP_BOX[:2])
    cx0, cy0, z0 = 530, 328.5, FIT
    if focus:
        fx0, fy0, fx1, fy1 = [focus[0] - CROP[0], focus[1] - CROP[1], focus[2] - CROP[0], focus[3] - CROP[1]]
        z1 = min(W * 0.9 / (fx1 - fx0), VP_H * 0.86 / (fy1 - fy0), FIT * 2.1)
        z1 = max(z1, FIT * 1.05)
        cx1, cy1 = (fx0 + fx1) / 2, (fy0 + fy1) / 2
        k = ease((t - 0.9) / 1.6)
    else:
        z1, cx1, cy1 = FIT * 1.06, cx0, cy0
        k = ease(t / dur)
    z = z0 + (z1 - z0) * k; cx = cx0 + (cx1 - cx0) * k; cy = cy0 + (cy1 - cy0) * k
    # keep the view inside the page where possible
    hw, hh = W / 2 / z, VP_H / 2 / z
    if hw < 530: cx = min(max(cx, hw), 1060 - hw)
    if hh < 328.5: cy = min(max(cy, hh), 657 - hh)
    box = (cx - hw, cy - hh, cx + hw, cy + hh)
    view = base.transform((W, VP_H), Image.EXTENT, box, Image.BICUBIC, fillcolor=BG)
    if focus:
        a = ease((t - 0.4) / 0.6)
        if a > 0:
            ov = Image.new("RGBA", (W, VP_H), (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
            X = lambda x: (x - box[0]) * z; Y = lambda y: (y - box[1]) * z
            pulse = 0.75 + 0.25 * math.sin(t * 4)
            d.rounded_rectangle([X(fx0) - 6, Y(fy0) - 6, X(fx1) + 6, Y(fy1) + 6], radius=14,
                                outline=RED + (int(255 * a * pulse),), width=5)
            view = view.convert("RGBA"); view.alpha_composite(ov); view = view.convert("RGB")
    fr = Image.new("RGB", (W, H), BG)
    fr.paste(view, (0, TOP))
    fr.paste(bar, (0, 0), bar)
    ca = ease(t / 0.5)
    if ca < 1:
        tmp = Image.new("RGBA", cap.size, BG + (255,)); fr.paste(Image.blend(tmp, cap, ca), (0, CAP_Y))
    else:
        fr.paste(cap, (0, CAP_Y))
    return fr

# ---------- cards ----------
BGIMG = Image.open(ASSETS + "bg_generic.png").convert("RGB").resize((W, H), Image.LANCZOS)
BGIMG = Image.blend(BGIMG, Image.new("RGB", (W, H), BG), 0.55)

def card_base(t):
    fr = BGIMG.copy()
    s = strip_at(t).resize((965, 117))
    fr.paste(s, (-5, H - 117)); fr.paste(s, (960, H - 117))
    return fr

def txt_center(d, y, s, f, fill):
    d.text(((W - d.textlength(s, font=f)) / 2, y), s, font=f, fill=fill)

def panel(d, box, col):
    d.rounded_rectangle(box, radius=18, fill=(18, 24, 36), outline=col, width=3)

def render_card(kind, t):
    fr = card_base(t); d = ImageDraw.Draw(fr)
    a = ease(t / 0.6)
    if kind == "intro":
        txt_center(d, 250, "F1 LAP-TIME LAB", font("x", 120), WHITE)
        d.rectangle([W / 2 - 160, 395, W / 2 + 160, 401], fill=RED)
        txt_center(d, 430, "Can a computer predict how fast an F1 car will lap?", font("s", 46), WHITE)
        txt_center(d, 505, "Linear Regression  vs  Random Forest", font("b", 40), GREY)
        txt_center(d, 565, "862 real laps · 2023 Italian Grand Prix (Monza) · interactive Power BI dashboard", font("r", 30), GREY)
    elif kind == "explain":
        txt_center(d, 130, "How do you predict a lap time?", font("x", 64), WHITE)
        lines = wrap(d, "A lap time depends on a few clues: how much fuel is left (a lighter car is faster), how old the tyres are (worn tyres are slower), which tyre type, the car, and the traffic around it.", font("r", 32), 1500)
        for i, ln in enumerate(lines): txt_center(d, 235 + i * 44, ln, font("r", 32), GREY)
        y0 = 235 + len(lines) * 44 + 40
        for j, (col, name, body) in enumerate([
            (BLUE, "Linear Regression", "Draws one straight-line rule, like \"every extra lap on the same tyres costs about 0.07 s\". Simple, and easy to explain."),
            (ORANGE, "Random Forest", "Asks hundreds of yes/no questions (\"tyres older than 15 laps? Ferrari?\") and averages the answers. Flexible, but it can only repeat what it has seen.")]):
            x0 = 160 + j * 830
            panel(d, [x0, y0, x0 + 770, y0 + 300], col)
            d.ellipse([x0 + 36, y0 + 42, x0 + 64, y0 + 70], fill=col)
            d.text((x0 + 82, y0 + 32), name, font=font("b", 42), fill=WHITE)
            for i, ln in enumerate(wrap(d, body, font("r", 30), 690)):
                d.text((x0 + 40, y0 + 110 + i * 42), ln, font=font("r", 30), fill=GREY)
        txt_center(d, y0 + 340, "Fair test: every lap is predicted by a model that never saw that lap.", font("s", 32), WHITE)
    elif kind == "verdict":
        txt_center(d, 130, "The verdict", font("x", 72), WHITE)
        tiles = [
            (ORANGE, "Normal laps", "Random Forest wins", "Typical error 0.30 s vs 0.38 s, about 20 % better. Best at filling in gaps it has seen before."),
            (BLUE, "Future laps (39-51)", "Linear Regression wins", "Typical error 0.45 s vs 0.53 s, about 15 % better. A simple rule carries on where patterns run out."),
            (RED, "Best of both", "Combine them", "Let the straight line set the trend and the forest fix what it misses: the most accurate on both tests."),
        ]
        for j, (col, k1, k2, body) in enumerate(tiles):
            x0 = 110 + j * 580
            panel(d, [x0, 260, x0 + 540, 640], col)
            d.text((x0 + 36, 292), k1.upper(), font=font("b", 24), fill=col)
            d.text((x0 + 36, 332), k2, font=font("x", 40), fill=WHITE)
            for i, ln in enumerate(wrap(d, body, font("r", 30), 470)):
                d.text((x0 + 36, 410 + i * 44), ln, font=font("r", 30), fill=GREY)
        txt_center(d, 700, "Lesson: the \"smartest\" model depends on the question you ask it.", font("s", 38), WHITE)
    elif kind == "outro":
        txt_center(d, 260, "F1 LAP-TIME LAB", font("x", 96), WHITE)
        d.rectangle([W / 2 - 140, 385, W / 2 + 140, 391], fill=RED)
        txt_center(d, 425, "Python (FastF1, scikit-learn) for the models  ·  Power BI for the dashboard", font("m", 34), GREY)
        txt_center(d, 485, "Full notebook, poster, data and dashboard guide: GitHub repo F1", font("s", 34), WHITE)
        txt_center(d, 560, "Thanks for watching", font("b", 44), WHITE)
    if a < 1:
        fr = Image.blend(Image.new("RGB", (W, H), BG), fr, a) if kind == "intro" else fr
    return fr

# ---------- timeline ----------
def main():
    total = sum(s[2] if s[0] == "card" else s[3] for s in SCENES) - XF * (len(SCENES) - 1)
    prepared, t0 = [], 0.0
    shot_idx = 0; n_shots = sum(1 for s in SCENES if s[0] == "shot")
    for s in SCENES:
        if s[0] == "card":
            prepared.append(dict(kind="card", card=s[1], dur=s[2], start=t0))
        else:
            shot_idx += 1
            prepared.append(dict(kind="shot", src=load_shot(s[1]), focus=s[2], dur=s[3], start=t0,
                                 cap=caption(s[4], s[5], s[6]), label=f"{shot_idx:02d} / {n_shots:02d}"))
        t0 += prepared[-1]["dur"] - XF
    def frame_of(p, lt, gt):
        if p["kind"] == "card": return render_card(p["card"], lt)
        return render_shot(p["src"], p["focus"], lt, p["dur"], p["cap"], top_bar(gt / total, p["label"]))
    nframes = int(total * FPS)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
           "-movflags", "+faststart", OUT]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for n in range(nframes):
        gt = n / FPS
        act = [p for p in prepared if p["start"] <= gt < p["start"] + p["dur"]]
        if len(act) == 1:
            img = frame_of(act[0], gt - act[0]["start"], gt)
        else:
            a, b = act[0], act[1]
            k = ease((gt - b["start"]) / XF)
            img = Image.blend(frame_of(a, gt - a["start"], gt), frame_of(b, gt - b["start"], gt), k)
        if n == nframes - 1 or (n > nframes - FPS):   # fade out last second
            img = Image.blend(img, Image.new("RGB", (W, H), BG), (n - (nframes - FPS)) / FPS)
        pr.stdin.write(img.tobytes())
        if n % 300 == 0: print(f"{n}/{nframes}", flush=True)
    pr.stdin.close(); pr.wait()
    print("done", OUT, f"{total:.1f}s")

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[2] == "preview":
        # write a few stills for checking
        os.makedirs("/home/claude/proj/video/preview", exist_ok=True)
        for kind in ["intro", "explain", "verdict", "outro"]:
            render_card(kind, 1.0).save(f"/home/claude/proj/video/preview/card_{kind}.jpg", quality=85)
        for i in [2, 9, 10, 13, 17]:
            s = SCENES[i]
            img = render_shot(load_shot(s[1]), s[2], s[3] - 0.5, s[3], caption(s[4], s[5], s[6]), top_bar(0.4, "07 / 16"))
            img.save(f"/home/claude/proj/video/preview/shot_{i}.jpg", quality=85)
    else:
        main()
