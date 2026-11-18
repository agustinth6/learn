"""Construye el video explicativo a partir de contenido.py + los audios.

Salida por capítulo:
  video/out/capXX.mp4   (con subtítulos incrustados)
  video/out/capXX.srt   (subtítulos como pista aparte)
"""
import os
import re
import subprocess
import sys

import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from contenido import CHAPTERS, NARRACION  # noqa: E402

W, H = 1280, 720
FPS = 25
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"

BG_TOP = (13, 20, 33)
BG_BOT = (24, 38, 60)
ACCENT = (126, 209, 255)
ACCENT2 = (110, 231, 183)
WHITE = (240, 246, 252)
GREY = (150, 170, 194)
CODE_BG = (10, 16, 26)
CODE_FG = (176, 240, 208)
NOTE_BG = (22, 44, 70)

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

F_TITLE = ImageFont.truetype(FONT_B, 46)
F_CHAP = ImageFont.truetype(FONT_B, 22)
F_BUL = ImageFont.truetype(FONT, 30)
F_CODE = ImageFont.truetype(MONO, 26)
F_NOTE = ImageFont.truetype(FONT, 27)
F_SUB = ImageFont.truetype(FONT_B, 26)
F_SUB2 = ImageFont.truetype(FONT, 24)


# ---------------------------------------------------------------- utilidades
def audio_duration(path):
    err = subprocess.run([FFMPEG, "-i", path], capture_output=True, text=True).stderr
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", err)
    if not m:
        raise RuntimeError(f"sin duración: {path}")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def gradient(w, h):
    img = Image.new("RGB", (1, h))
    d = ImageDraw.Draw(img)
    for y in range(h):
        t = y / (h - 1)
        d.point((0, y), tuple(int(BG_TOP[i] + (BG_BOT[i] - BG_TOP[i]) * t) for i in range(3)))
    return img.resize((w, h))


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        probe = (cur + " " + w_).strip()
        if draw.textlength(probe, font=font) <= maxw:
            cur = probe
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def split_captions(text, max_chars=84):
    """Divide la narración en bloques de subtítulo (2 líneas como máximo)."""
    parts = re.split(r"(?<=[.!?;:])\s+", text)
    chunks = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if len(p) <= max_chars:
            chunks.append(p)
            continue
        # demasiado largo: partir en comas y, si no alcanza, por palabras
        trozos, cur = [], ""
        for piece in re.split(r"(?<=,)\s+", p):
            cand = (cur + " " + piece).strip()
            if len(cand) <= max_chars:
                cur = cand
                continue
            if cur:
                trozos.append(cur)
            if len(piece) <= max_chars:
                cur = piece
            else:
                c2 = ""
                for w_ in piece.split():
                    if len((c2 + " " + w_).strip()) <= max_chars:
                        c2 = (c2 + " " + w_).strip()
                    else:
                        if c2:
                            trozos.append(c2)
                        c2 = w_
                cur = c2
        if cur:
            trozos.append(cur)
        # evita bloques finales de una sola palabra
        if len(trozos) > 1 and len(trozos[-1].split()) < 3:
            trozos[-2] = trozos[-2] + " " + trozos[-1]
            trozos.pop()
        chunks.extend(trozos)
    # une bloques muy cortos con el siguiente (evita subtítulos de 1 segundo)
    out, i = [], 0
    while i < len(chunks):
        c = chunks[i]
        if len(c) < 34 and i + 1 < len(chunks) and len(c) + len(chunks[i + 1]) <= 92:
            out.append(c + " " + chunks[i + 1])
            i += 2
        else:
            out.append(c)
            i += 1
    return [c for c in out if c]


# ------------------------------------------------------------------ láminas
def slide(ch, scene, ch_title, total_scenes, idx, limite=None):
    """Dibuja una lámina. `limite` = Y máximo disponible (por la banda de subtítulos)."""
    img = gradient(W, H).copy()
    d = ImageDraw.Draw(img, "RGBA")
    limite = limite or (H - 30)

    # barra superior
    d.rectangle([0, 0, W, 6], fill=ACCENT)
    d.text((70, 52), f"CAPÍTULO {ch['n']} DE {len(CHAPTERS)}", font=F_CHAP, fill=ACCENT)
    d.text((70, 82), ch_title, font=ImageFont.truetype(FONT, 22), fill=GREY)
    d.line([70, 120, W - 70, 120], fill=(60, 80, 105), width=1)

    # ---- ajuste automático: busca la escala más grande que entre completa ----
    def total_height(scale):
        h = 0.0
        for kind, txt in scene["lines"]:
            if kind == "b":
                f = ImageFont.truetype(FONT, int(30 * scale))
                n = len(wrap(d, txt, f, W - 230))
                h += n * (40 * scale) + 14 * scale
            elif kind == "code":
                h += 54 * scale
            else:
                f = ImageFont.truetype(FONT, int(27 * scale))
                n = len(wrap(d, txt, f, W - 260))
                h += (24 + 36 * n) * scale + 16 * scale
        return h

    titulo_alto = 152 + (52 if d.textlength(scene["title"], font=F_TITLE) > W - 140 else 0) + 62
    disp = limite - 24 - titulo_alto
    scale = 1.0
    while scale > 0.62 and total_height(scale) > disp:
        scale -= 0.04

    # título de la lámina (2 líneas si hace falta)
    ty = 152
    tf = F_TITLE
    if d.textlength(scene["title"], font=tf) > W - 140:
        tf = ImageFont.truetype(FONT_B, 38)
    for ln in wrap(d, scene["title"], tf, W - 140):
        d.text((70, ty), ln, font=tf, fill=WHITE)
        ty += tf.size + 10
    y = ty + 26

    f_bul = ImageFont.truetype(FONT, int(30 * scale))
    f_code = ImageFont.truetype(MONO, int(26 * scale))
    f_note = ImageFont.truetype(FONT, int(27 * scale))

    for kind, txt in scene["lines"]:
        if kind == "b":
            d.ellipse([72, y + 13 * scale, 80, y + 21 * scale], fill=ACCENT2)
            for ln in wrap(d, txt, f_bul, W - 230):
                d.text((100, y), ln, font=f_bul, fill=WHITE)
                y += 40 * scale
            y += 14 * scale

        elif kind == "code":
            tw = d.textlength(txt, font=f_code)
            d.rounded_rectangle([70, y - 4, min(70 + tw + 34, W - 70), y + 40 * scale],
                                radius=6, fill=CODE_BG)
            d.text((88, y + 4), txt, font=f_code, fill=CODE_FG)
            y += 54 * scale

        elif kind == "note":
            lines = wrap(d, txt, f_note, W - 260)
            hgt = (24 + 36 * len(lines)) * scale
            d.rounded_rectangle([70, y, W - 70, y + hgt], radius=8, fill=NOTE_BG)
            d.rectangle([70, y, 76, y + hgt], fill=ACCENT2)
            yy = y + 12 * scale
            for ln in lines:
                d.text((96, yy), ln, font=f_note, fill=(214, 236, 255))
                yy += 36 * scale
            y += hgt + 16 * scale

    # pie
    d.text((W - 70, 56), f"lámina {idx}/{total_scenes}",
           font=ImageFont.truetype(FONT, 18), fill=(110, 130, 155), anchor="ra")
    return img


def title_card(ch):
    img = gradient(W, H).copy()
    d = ImageDraw.Draw(img, "RGBA")
    d.rectangle([0, 0, W, 8], fill=ACCENT)
    d.text((W // 2, H // 2 - 130), f"CAPÍTULO {ch['n']}", font=ImageFont.truetype(FONT_B, 30),
           fill=ACCENT, anchor="mm")
    for i, ln in enumerate(wrap(d, ch["title"], ImageFont.truetype(FONT_B, 52), W - 260)):
        d.text((W // 2, H // 2 - 30 + i * 68), ln,
               font=ImageFont.truetype(FONT_B, 52), fill=WHITE, anchor="mm")
    d.line([W // 2 - 90, H // 2 + 70, W // 2 + 90, H // 2 + 70], fill=ACCENT2, width=3)
    d.text((W // 2, H // 2 + 120), "Repaso de la materia + parcial CinePlus",
           font=ImageFont.truetype(FONT, 24), fill=GREY, anchor="mm")
    return img


def with_subtitle(base, text):
    """Devuelve una copia de la lámina con la banda de subtítulos."""
    img = base.copy()
    d = ImageDraw.Draw(img, "RGBA")
    lines = wrap(d, text, F_SUB, W - 300)
    if len(lines) > 2:
        # reajusta en dos líneas más parejas
        half = len(lines) // 2 + len(lines) % 2
        lines = [" ".join(lines[:half]), " ".join(lines[half:])]
    band_h = 30 + 36 * len(lines)
    top = H - band_h - 16
    d.rectangle([0, top, W, H], fill=(0, 0, 0, 190))
    d.rectangle([0, top, W, top + 3], fill=(*ACCENT2, 200))
    y = top + 14
    for ln in lines:
        d.text((W // 2, y), ln, font=F_SUB, fill=(255, 255, 255), anchor="ma")
        y += 36
    return img


# ------------------------------------------------------------------- tiempos
def cronometrar(texto, dur):
    """Reparte `dur` segundos entre los bloques de subtítulo."""
    chunks = split_captions(texto)
    weights = [max(len(c), 12) for c in chunks]
    total = sum(weights)
    out, t = [], 0.0
    for c, w_ in zip(chunks, weights):
        d = dur * w_ / total
        out.append((t, t + d, c))
        t += d
    # corrige el redondeo en el último
    if out:
        s, _, c = out[-1]
        out[-1] = (s, dur, c)
    return out


def asignar_escenas(ch, dur):
    pesos = ch.get("weight_per_scene") or [1.0] * len(ch["scenes"])
    total = sum(pesos)
    bounds, t = [], 0.0
    for p in pesos:
        d = dur * p / total
        bounds.append((t, t + d))
        t += d
    bounds[-1] = (bounds[-1][0], dur)
    return bounds


def srt_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    ms = int(round((s - int(s)) * 1000))
    if ms == 1000:
        ms, sec = 0, sec + 1
    return f"{h:02d}:{m:02d}:{sec:02d},{ms:03d}"


# ----------------------------------------------------------------- ejecución
def build_chapter(ch):
    n = ch["n"]
    audio = f"audio/{ch['dir']}.mp3"
    if not os.path.exists(audio):
        print(f"  ⚠ capítulo {n}: falta {audio}, se omite")
        return None

    dur = audio_duration(audio)
    narr = NARRACION.get(n, "")
    if not narr:
        print(f"  ⚠ capítulo {n}: sin narración, se omite")
        return None

    bounds = asignar_escenas(ch, dur)
    subs = cronometrar(narr, dur)

    # láminas base por escena
    # reserva espacio para la banda de subtítulos (2 líneas = ~105 px)
    LIMITE = H - 105
    base_imgs = [slide(ch, sc, ch["title"], len(ch["scenes"]), i + 1, limite=LIMITE)
                 for i, sc in enumerate(ch["scenes"])]

    # tarjeta de título (2.4 s) + audio desplazado
    lead = 2.4
    segs = []          # (imagen, duración)
    segs.append((title_card(ch), lead))

    # para cada bloque de subtítulo: imagen de su escena + subtítulo
    for (s, e, txt) in subs:
        mid = (s + e) / 2
        idx = 0
        for i, (a, b) in enumerate(bounds):
            if a <= mid < b:
                idx = i
                break
            if mid >= b:
                idx = i
        segs.append((with_subtitle(base_imgs[idx], txt), e - s))

    # render de frames
    tmp = f"tmp/{ch['dir']}"
    os.makedirs(tmp, exist_ok=True)
    listfile = os.path.join(tmp, "lista.txt")
    with open(listfile, "w") as f:
        for i, (img, d) in enumerate(segs):
            p = os.path.abspath(os.path.join(tmp, f"f{i:04d}.png"))
            img.save(p)
            f.write(f"file '{p}'\nduration {d:.3f}\n")
        # repite la última para que el concat no la descarte
        f.write(f"file '{os.path.abspath(os.path.join(tmp, f'f{len(segs)-1:04d}.png'))}'\n")

    out = f"out/{ch['dir']}.mp4"
    cmd = [
        FFMPEG, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", listfile,
        "-i", audio,
        "-filter_complex", f"[1:a]adelay={int(lead*1000)}|{int(lead*1000)},apad[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
        "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", str(FPS * 2),
        "-c:a", "aac", "-b:a", "128k",
        "-shortest", "-movflags", "+faststart",
        out,
    ]
    subprocess.run(cmd, check=True)

    # .srt aparte
    srt = f"out/{ch['dir']}.srt"
    with open(srt, "w", encoding="utf-8") as f:
        for i, (s, e, txt) in enumerate(subs, 1):
            f.write(f"{i}\n{srt_time(s+lead)} --> {srt_time(e+lead)}\n{txt}\n\n")

    print(f"  ✓ cap {n}: {out}  ({dur+lead:.0f}s, {len(segs)} segmentos)")
    return out


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.makedirs("out", exist_ok=True)
    hechos = []
    for ch in CHAPTERS:
        r = build_chapter(ch)
        if r:
            hechos.append(r)
    if not hechos:
        print("nada para unir")
        return
    with open("out/lista_video.txt", "w") as f:
        for p in hechos:
            f.write(f"file '{os.path.abspath(p)}'\n")
    print("capítulos listos:", len(hechos))


if __name__ == "__main__":
    main()
