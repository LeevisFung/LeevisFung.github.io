# -*- coding: utf-8 -*-
"""Generate simple Flick demo GIFs for the landing page."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 640, 400
BG = (23, 22, 20)
PANEL = (40, 38, 34)
INK = (236, 232, 225)
MUTED = (155, 149, 139)
ACCENT = (240, 120, 79)
BORDER = (60, 57, 52)

FONT_PATH = "C:/Windows/Fonts/msyh.ttc"
FONT_BOLD = "C:/Windows/Fonts/msyhbd.ttc"

def font(size, bold=False):
    path = FONT_BOLD if bold else FONT_PATH
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

def new_frame():
    return Image.new("RGB", (W, H), BG)

def draw_canvas(draw):
    for x in range(20, W, 32):
        for y in range(44, H, 32):
            draw.ellipse([x - 1, y - 1, x + 1, y + 1], fill=(45, 43, 40))

def draw_topbar(draw):
    draw.rectangle([0, 0, W, 40], fill=(26, 25, 23))
    draw.line([0, 40, W, 40], fill=(40, 38, 34))
    draw.ellipse([16, 14, 28, 26], fill=ACCENT)
    draw.text((36, 10), "Flick 灵感画布", font=font(16, True), fill=INK)

def draw_note(draw, x, y, lines, w=190, h=86, accent=False, selected=False):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=PANEL,
                           outline=ACCENT if accent or selected else BORDER,
                           width=2 if selected else 1)
    draw.text((x + 14, y + 12), lines, font=font(15), fill=INK, spacing=6)

def draw_hint(draw, text):
    draw.text((W // 2 - 90, H - 40), text, font=font(14), fill=MUTED)

def draw_shortcut(draw, text):
    draw.rounded_rectangle([W // 2 - 130, H - 52, W // 2 + 130, H - 16],
                           radius=18, fill=(26, 25, 23), outline=ACCENT, width=1)
    draw.text((W // 2 - 110, H - 46), text, font=font(15, True), fill=ACCENT)

def save_gif(frames, name, durations):
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), name)
    frames[0].save(out, save_all=True, append_images=frames[1:],
                   duration=durations, loop=0, disposal=2)
    print("saved", out, "frames", len(frames))


def gif_1_canvas():
    frames = []

    # 1: empty canvas
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    draw_hint(d, "双击画布，随手记录灵感")
    frames.append(img)

    # 2: first note
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    draw_note(d, 210, 140, "双击画布\n随手记下灵感", accent=True)
    draw_hint(d, "无限画布 · 不设边界")
    frames.append(img)

    # 3: second note
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    draw_note(d, 210, 140, "双击画布\n随手记下灵感", accent=True)
    draw_note(d, 380, 230, "截图也能\n直接贴进来")
    draw_hint(d, "文字 / 图片 / 截图，都在同一块画布")
    frames.append(img)

    # 4: third note + shortcut
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    draw_note(d, 210, 140, "双击画布\n随手记下灵感", accent=True)
    draw_note(d, 380, 230, "截图也能\n直接贴进来")
    draw_note(d, 100, 260, "无限画布\n随便放")
    draw_shortcut(d, "Ctrl+Space 呼出 / 隐藏")
    frames.append(img)

    save_gif(frames, "demo-1.gif", [500, 700, 700, 900])


def gif_2_capture():
    frames = []

    # 1: canvas with notes
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    draw_note(d, 160, 140, "需求记录\n会前随手记")
    draw_note(d, 360, 220, "流程图\n待补充")
    draw_hint(d, "按 Ctrl+Shift+A 截图速记")
    frames.append(img)

    # 2: crosshair overlay
    img = new_frame().convert("RGBA"); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    draw_note(d, 160, 140, "需求记录\n会前随手记")
    draw_note(d, 360, 220, "流程图\n待补充")
    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 110))
    img = Image.alpha_composite(img, overlay)
    d = ImageDraw.Draw(img)
    cx, cy = 300, 190
    d.line([cx - 24, cy, cx + 24, cy], fill=ACCENT, width=2)
    d.line([cx, cy - 24, cx, cy + 24], fill=ACCENT, width=2)
    d.rounded_rectangle([cx - 90, cy - 60, cx + 90, cy + 60], outline=ACCENT, width=2, radius=6)
    frames.append(img.convert("RGB"))

    # 3: capture flash
    img = Image.new("RGB", (W, H), (245, 235, 225)); d = ImageDraw.Draw(img)
    d.text((W // 2 - 50, H // 2 - 12), "已截图", font=font(20, True), fill=ACCENT)
    frames.append(img)

    # 4: pasted image card
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    draw_note(d, 160, 140, "需求记录\n会前随手记")
    draw_note(d, 360, 220, "流程图\n待补充")
    x, y = 220, 130
    d.rounded_rectangle([x, y, x + 200, y + 130], radius=8, fill=(58, 55, 51), outline=ACCENT, width=2)
    d.text((x + 18, y + 20), "截图内容", font=font(16, True), fill=INK)
    d.text((x + 18, y + 48), "自动贴到画布", font=font(13), fill=MUTED)
    d.rounded_rectangle([x + 18, y + 78, x + 182, y + 108], radius=4, fill=(240, 120, 79))
    d.text((x + 56, y + 84), "Flick", font=font(13, True), fill=(26, 25, 23))
    draw_shortcut(d, "Ctrl+Shift+A 截图速记")
    frames.append(img)

    save_gif(frames, "demo-2.gif", [500, 800, 250, 1000])


def gif_3_align():
    starts = [(100, 80), (330, 210), (220, 310)]
    ends = [(130, 150), (300, 150), (470, 150)]
    labels = ["想法 A", "想法 B", "想法 C"]
    frames = []
    durations = []

    # 1: scattered
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    for (x, y), label in zip(starts, labels):
        draw_note(d, x, y, label)
    draw_hint(d, "拖得有点乱？一键对齐")
    frames.append(img); durations.append(500)

    # 2: selected
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    for (x, y), label in zip(starts, labels):
        draw_note(d, x, y, label, selected=True)
    draw_hint(d, "选中多个节点")
    frames.append(img); durations.append(600)

    # 3-4: moving to aligned
    steps = 2
    for step in range(steps):
        img = new_frame(); d = ImageDraw.Draw(img)
        draw_canvas(d); draw_topbar(d)
        t = (step + 1) / steps
        for (sx, sy), (ex, ey), label in zip(starts, ends, labels):
            x = int(sx + (ex - sx) * t)
            y = int(sy + (ey - sy) * t)
            draw_note(d, x, y, label, selected=True)
        if step == steps - 1:
            draw_shortcut(d, "Shift+O / Shift+P 一键对齐")
        else:
            draw_hint(d, "正在对齐…")
        frames.append(img)
        durations.append(350 if step == 0 else 400)

    # 5: aligned final
    img = new_frame(); d = ImageDraw.Draw(img)
    draw_canvas(d); draw_topbar(d)
    for (x, y), label in zip(ends, labels):
        draw_note(d, x, y, label, selected=True)
    draw_shortcut(d, "Shift+O / Shift+P 一键对齐")
    frames.append(img); durations.append(1000)

    save_gif(frames, "demo-3.gif", durations)


if __name__ == "__main__":
    gif_1_canvas()
    gif_2_capture()
    gif_3_align()
