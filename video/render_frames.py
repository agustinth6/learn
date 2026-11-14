#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Renderiza los frames (PNG 1920x1080) de cada segmento del video.
Uso:  python video/render_frames.py
"""
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from segmentos import SEGMENTOS

ROOT = pathlib.Path(__file__).resolve().parent.parent
FRAMES_DIR = pathlib.Path(__file__).resolve().parent / "frames"

W, H = 1920, 1080
BG = (18, 20, 28)
TITLE_BAR = (24, 27, 38)
PANEL = (27, 30, 42)
FG = (232, 234, 240)
DIM = (140, 146, 162)
ACCENT = (224, 175, 104)
HL_BG = (46, 58, 89)
HL_NUM = (255, 214, 120)
COMMENT = (112, 164, 112)
STRING = (224, 175, 104)
KEYWORD = (187, 170, 247)
NUMBER = (255, 158, 100)
FUNCNAME = (122, 162, 247)

FONTS = "/usr/share/fonts/truetype/dejavu/"
F_TITLE = FONTS + "DejaVuSans-Bold.ttf"
F_REG = FONTS + "DejaVuSans.ttf"
F_MONO = FONTS + "DejaVuSansMono.ttf"
F_MONO_B = FONTS + "DejaVuSansMono-Bold.ttf"

TOKEN_RE = re.compile(
    r"(#.*$)"
    r"|(\"(?:[^\"\\]|\\.)*\"|'(?:[^'\\]|\\.)*')"
    r"|\b(def|return|if|elif|else|while|for|in|not|and|or|try|except|break|continue|None|True|False|import|from|as|pass|print|input|len|sum|float|int|str)\b"
    r"|\b(\d+(?:\.\d+)?)\b"
)

KEYWORDS = set(
    "def return if elif else while for in not and or try except break continue None True False import from as pass print input len sum float int str".split()
)


def font(path, size):
    return ImageFont.truetype(path, size)


def draw_text(draw, xy, text, fnt, fill, anchor=None):
    draw.text(xy, text, font=fnt, fill=fill, anchor=anchor)


def draw_rich_line(draw, x, y, line, fnt):
    """Dibuja una linea de codigo con colores simples por token."""
    pos = 0
    for m in TOKEN_RE.finditer(line):
        if m.start() > pos:
            draw.text((x, y), line[pos : m.start()], font=fnt, fill=FG)
            x += draw.textlength(line[pos : m.start()], font=fnt)
        tok = m.group(0)
        if m.group(1):          # comentario
            color = COMMENT
        elif m.group(2):        # string
            color = STRING
        elif m.group(3):        # palabra clave / funcion
            color = KEYWORD if tok in KEYWORDS else FUNCNAME
        else:                   # numero
            color = NUMBER
        draw.text((x, y), tok, font=fnt, fill=color)
        x += draw.textlength(tok, font=fnt)
        pos = m.end()
    if pos < len(line):
        draw.text((x, y), line[pos:], font=fnt, fill=FG)


def chrome(draw, seg, fnt_tag, fnt_head, fnt_foot):
    """Barra superior con tag + titulo, y pie de pagina."""
    draw.rectangle([0, 0, W, 96], fill=TITLE_BAR)
    tag = seg.get("tag", "")
    tw = draw.textlength(tag, font=fnt_tag)
    draw.rounded_rectangle([28, 24, 28 + tw + 36, 72], radius=10, fill=ACCENT)
    draw.text((46, 34), tag, font=fnt_tag, fill=(30, 26, 16))
    draw.text((28 + tw + 60, 30), seg.get("titulo", ""), font=fnt_head, fill=FG)
    draw.text((30, H - 52), "Técnicas de Programación · Python — Repaso del Parcial 2",
              font=fnt_foot, fill=(90, 96, 112))


def render_titulo(seg, path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_big = font(F_TITLE, 84)
    f_sub = font(F_REG, 42)
    f_tag = font(F_TITLE, 30)
    # franja decorativa
    d.rectangle([0, H // 2 - 190, W, H // 2 - 176], fill=ACCENT)
    d.text((W // 2, H // 2 - 90), seg["titulo"], font=f_big, fill=FG, anchor="mm")
    d.text((W // 2, H // 2 + 30), seg.get("subtitulo", ""), font=f_sub, fill=DIM, anchor="mm")
    d.text((W // 2, H // 2 + 150), seg.get("tag", ""), font=f_tag, fill=ACCENT, anchor="mm")
    img.save(path)


def render_concepto(seg, path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_tag = font(F_TITLE, 28)
    f_head = font(F_TITLE, 46)
    f_bul = font(F_REG, 40)
    f_foot = font(F_REG, 26)
    chrome(d, seg, f_tag, f_head, f_foot)
    y = 170
    for b in seg.get("bullets", []):
        # wrap manual ~100 chars
        words, lines, cur = b.split(), [], ""
        for w in words:
            trial = (cur + " " + w).strip()
            if d.textlength(trial, font=f_bul) > W - 260:
                lines.append(cur)
                cur = w
            else:
                cur = trial
        lines.append(cur)
        d.ellipse([70, y + 16, 92, y + 38], fill=ACCENT)
        for i, ln in enumerate(lines):
            d.text((130, y), ln, font=f_bul, fill=FG if i == 0 else DIM)
            y += 56
        y += 34
    img.save(path)


def load_block(archivo, funcion=None, marker=None):
    """Devuelve (lineas, inicio_abs) del bloque a mostrar (0-based abs)."""
    lines = (ROOT / archivo).read_text(encoding="utf-8").splitlines()
    if funcion:
        start = next(i for i, l in enumerate(lines) if l.startswith(f"def {funcion}("))
        end = start + 1
        while end < len(lines):
            l = lines[end]
            if l.startswith("def ") or l.startswith("# ---") or l.startswith("if __name__"):
                break
            end += 1
        while end > start and lines[end - 1].strip() == "":
            end -= 1
        return lines[start:end], start
    # marker
    desde, hasta = marker["desde"], marker["hasta"]
    start = next(i for i, l in enumerate(lines) if desde in l)
    end = start + 1
    while end < len(lines):
        if lines[end].strip() == hasta:
            break
        end += 1
    return lines[start : end + 1], start


def render_codigo(seg, path):
    archivo = seg["archivo"]
    block, abs_start = load_block(archivo, seg.get("funcion"), seg.get("marker"))
    n = len(block)

    # lineas a resaltar (indices relativos 0-based)
    hl = set()
    patrones = seg.get("patrones")
    if patrones:
        for i, l in enumerate(block):
            if any(p in l for p in patrones):
                hl.add(i)
        if not hl:
            print(f"  [AVISO] seg {seg['id']}: ningun patron coincide en {archivo}")

    # ventana alrededor de las resaltadas
    if hl:
        lo = max(0, min(hl) - 4)
        hi = min(n, max(hl) + 8)
    else:
        lo, hi = 0, min(n, 40)
    win = list(range(lo, hi))
    wn = len(win)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    f_tag = font(F_TITLE, 28)
    f_head = font(F_TITLE, 44)
    f_foot = font(F_REG, 26)
    chrome(d, seg, f_tag, f_head, f_foot)

    # panel de codigo
    top, bot = 126, H - 78
    d.rounded_rectangle([24, top, W - 24, bot], radius=14, fill=PANEL)

    avail = bot - top - 36
    lh = max(22, min(52, avail // max(wn, 1)))
    fnt_size = max(17, int(lh / 1.42))
    f_code = font(F_MONO, fnt_size)
    f_num = font(F_MONO, max(15, fnt_size - 3))

    y = top + 18
    for idx in win:
        abs_line = abs_start + idx + 1  # 1-based en el archivo
        code = block[idx]
        if idx in hl:
            d.rectangle([36, y - 2, W - 36, y + lh - 6], fill=HL_BG)
            d.rectangle([36, y - 2, 44, y + lh - 6], fill=ACCENT)
        num = str(abs_line)
        nw = d.textlength(num, font=f_num)
        d.text((110 - nw, y), num, font=f_num,
               fill=HL_NUM if idx in hl else (110, 116, 132))
        # recorta si es muy larga
        max_w = W - 170
        code_draw = code
        while d.textlength(code_draw, font=f_code) > max_w and len(code_draw) > 4:
            code_draw = code_draw[:-4] + "..."
        draw_rich_line(d, 130, y, code_draw, f_code)
        y += lh
    img.save(path)


def main():
    FRAMES_DIR.mkdir(parents=True, exist_ok=True)
    for seg in SEGMENTOS:
        path = FRAMES_DIR / f"{seg['id']:02d}.png"
        if seg["tipo"] == "titulo":
            render_titulo(seg, path)
        elif seg["tipo"] == "concepto":
            render_concepto(seg, path)
        else:
            render_codigo(seg, path)
        print(f"  frame {path.name}  <- seg {seg['id']} ({seg['tipo']})")
    print(f"OK: {len(SEGMENTOS)} frames en {FRAMES_DIR}")


if __name__ == "__main__":
    main()
