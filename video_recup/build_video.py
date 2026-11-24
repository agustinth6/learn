#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build: video_recup/build_video.py
Ensambla video explicativo con etapas, narracion (audio/etapaN.mp3) y
subtitulos quemados a partir de narracion.json.

Uso:  python build_video.py            # render completo
      python build_video.py --frames   # solo frames (debug sin audio)
Salida: video_recup/PRIMER_PARCIAL_modelos.mp4 + .srt
"""
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
W, H = 1280, 720
SLIDE_H = 556  # zona de slide; abajo va la banda de subtitulo

FONT_BOLD = ROOT / "fonts/DejaVuSans-Bold.ttf"
FONT_REG = ROOT / "fonts/DejaVuSans.ttf"
FONT_MONO = ROOT / "fonts/DejaVuSansMono.ttf"

COLORS = {
    "bg": "#0e1626",
    "header": "#16233c",
    "title": "#8ec7ff",
    "white": "#e8eef7",
    "green": "#9ece6a",
    "green_bg": "#17251a",
    "sub_bg": "#000000",
    "sub": "#ffffff",
    "kw": "#61afef",
    "fn": "#c678dd",
    "str": "#e5c07b",
    "num": "#d19a66",
    "com": "#6b7280",
}

TOKEN_RE = re.compile(
    r"(?P<com>#.*$)"
    r"|(?P<str>\"[^\"]*\"|'[^']*')"
    r"|(?P<kw>\b(?:def|return|if|elif|else|for|while|in|not|and|or|True|False|None|import)\b)"
    r"|(?P<fn>\b(?:print|input|range|int|float|str|len|list)\b)"
    r"|(?P<num>\b\d+(?:\.\d+)?\b)",
    re.M,
)


def font(path, size):
    return ImageFont.truetype(str(path), size)


def text_width(draw, s, f):
    return draw.textlength(s, font=f)


def wrap_text(draw, s, f, max_w):
    words = s.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_width(draw, t, f) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def split_cues(text, max_len=95):
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    cues = []
    for p in parts:
        p = p.strip()
        if not p:
            continue
        if len(p) <= max_len:
            cues.append(p)
            continue
        sub = re.split(r"(?<=[;,])\s+", p)
        buf = ""
        for s in sub:
            if not buf:
                buf = s
            elif len(buf) + 1 + len(s) <= max_len:
                buf += " " + s
            else:
                cues.append(buf.strip())
                buf = s
        if buf:
            cues.append(buf.strip())
    merged = []
    for c in cues:
        if merged and (
            (len(merged[-1]) < 30 or len(c) < 20)
            and len(merged[-1]) + 1 + len(c) <= max_len
        ):
            merged[-1] = merged[-1] + " " + c
        else:
            merged.append(c)
    return merged or [text]


def draw_code_line(draw, x, y, line, f):
    """Linea de codigo con colores basicos de tokens."""
    pos = 0
    for m in TOKEN_RE.finditer(line):
        if m.start() > pos:
            draw.text((x + text_width(draw, line[:pos], f), y),
                      line[pos:m.start()], font=f, fill=COLORS["white"])
        color = COLORS["com"] if m.lastgroup == "com" else (
            COLORS["str"] if m.lastgroup == "str" else (
                COLORS["kw"] if m.lastgroup == "kw" else (
                    COLORS["fn"] if m.lastgroup == "fn" else COLORS["num"])))
        draw.text((x + text_width(draw, line[:m.start()], f), y),
                  m.group(), font=f, fill=color)
        pos = m.end()
    if pos < len(line):
        draw.text((x + text_width(draw, line[:pos], f), y),
                  line[pos:], font=f, fill=COLORS["white"])


def render_frame(slide, subtitle, out_path):
    img = Image.new("RGB", (W, H), COLORS["bg"])
    d = ImageDraw.Draw(img)

    f_title = font(FONT_BOLD, 34)
    f_big = font(FONT_BOLD, 52)
    f_body = font(FONT_REG, 26)
    f_code = font(FONT_MONO, 22)
    f_res = font(FONT_BOLD, 24)
    f_sub = font(FONT_REG, 30)

    tipo = slide.get("tipo", "lista")
    titulo = slide.get("titulo", "")
    cuerpo = slide.get("cuerpo", [])
    res = slide.get("res", "")

    if tipo == "titulo":
        # tarjeta de titulo centrada
        d.rectangle([0, 0, W, SLIDE_H], fill=COLORS["header"])
        y = 140
        for ln in wrap_text(d, titulo, f_big, W - 120):
            w = text_width(d, ln, f_big)
            d.text(((W - w) / 2, y), ln, font=f_big, fill=COLORS["title"])
            y += 70
        y += 30
        for ln in cuerpo:
            w = text_width(d, ln, f_body)
            d.text(((W - w) / 2, y), ln, font=f_body, fill=COLORS["white"])
            y += 44
    else:
        # barra de titulo
        d.rectangle([0, 0, W, 64], fill=COLORS["header"])
        d.text((28, 14), titulo, font=f_title, fill=COLORS["title"])
        y = 84
        if tipo == "codigo":
            for line in cuerpo:
                draw_code_line(d, 32, y, line, f_code)
                y += 30
        else:  # lista
            for line in cuerpo:
                if line:
                    d.text((32, y), ("• " if not line.startswith(" ") else "") + line.strip()
                           if not re.match(r"^\d\)", line) else line,
                           font=f_body, fill=COLORS["white"])
                y += 44
        if res:
            ry = SLIDE_H - 78
            d.rectangle([24, ry, W - 24, ry + 60], fill=COLORS["green_bg"],
                        outline=COLORS["green"], width=2)
            d.text((40, ry + 15), res, font=f_res, fill=COLORS["green"])

    # banda de subtitulo
    d.rectangle([0, SLIDE_H, W, H], fill=COLORS["sub_bg"])
    lines = wrap_text(d, subtitle, f_sub, W - 100)
    lines = lines[:2]
    total_h = len(lines) * 40
    sy = SLIDE_H + (H - SLIDE_H - total_h) / 2 + 2
    for ln in lines:
        w = text_width(d, ln, f_sub)
        d.text(((W - w) / 2, sy), ln, font=f_sub, fill=COLORS["sub"])
        sy += 40

    img.save(out_path)


def fmt_ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(r.stderr[-3000:])
        sys.exit(f"ffmpeg fallo: {' '.join(cmd[:6])}...")
    return r


def main():
    from imageio_ffmpeg import get_ffmpeg_exe
    ff = get_ffmpeg_exe()

    data = json.loads((ROOT / "narracion.json").read_text(encoding="utf-8"))
    etapas = data["etapas"]
    frames_dir = ROOT / "frames"
    frames_dir.mkdir(exist_ok=True)
    only_frames = "--frames" in sys.argv

    # limpiar frames viejos
    for old in frames_dir.glob("*.png"):
        old.unlink()

    global_offset = 0.0
    srt_entries = []
    etapa_videos = []
    resumen = []

    for et in etapas:
        eid = et["id"]
        audio = ROOT / "audio" / f"etapa{eid}.mp3"
        narration = et["narracion"]
        slides = et["slides"]
        cues = split_cues(narration)

        if only_frames:
            dur = max(8.0, sum(len(c) for c in cues) / 14.5)  # ~14.5 chars/seg
        else:
            if not audio.exists():
                sys.exit(f"FALTA audio: {audio}")
            from mutagen.mp3 import MP3
            dur = MP3(audio).info.length

        # duraciones proporcionales al largo de cada cue
        weights = [len(c) + 18 for c in cues]
        wsum = sum(weights)
        durs = [dur * w / wsum for w in weights]

        # asignar slides a cues por ANCLA de narracion (el visual espera al audio)
        S, C = len(slides), len(cues)

        def norm(s):
            return "".join(
                c for c in unicodedata.normalize("NFD", s.casefold())
                if unicodedata.category(c) != "Mn")

        bounds = [0] * S
        prev = 0
        for i, sl in enumerate(slides):
            if i == 0:
                continue
            a = sl.get("ancla")
            if a:
                na = norm(a)
                found = None
                for k in range(prev, C):
                    if na in norm(cues[k]):
                        found = k
                        break
                if found is None:  # fallback: reparto parejo
                    found = min(C - 1, prev + max(1, (C - prev) // max(1, S - i)))
                bounds[i] = max(found, prev)
                prev = bounds[i]
            else:
                bounds[i] = prev
        for i, b in enumerate(bounds):
            cue0 = cues[b] if b < C else ""
            print(f"    slide {i}: cue {b:>2} '{cue0[:46]}'")

        def slide_of(k):
            idx = 0
            for i in range(S):
                if bounds[i] <= k:
                    idx = i
                else:
                    break
            return idx

        frame_paths = []
        t = 0.0
        for k, cue in enumerate(cues):
            fp = frames_dir / f"e{eid}_{k:03d}.png"
            render_frame(slides[slide_of(k)], cue, fp)
            frame_paths.append((fp, durs[k]))
            srt_entries.append((global_offset + t, global_offset + t + durs[k], cue))
            t += durs[k]

        resumen.append((eid, et["nombre"], dur, len(cues), S))

        if only_frames:
            global_offset += dur
            continue

        # lista concat de frames
        lst = ROOT / f"frames_e{eid}.txt"
        with lst.open("w") as fh:
            for fp, dd in frame_paths:
                fh.write(f"file '{fp}'\nduration {dd:.3f}\n")
            fh.write(f"file '{frame_paths[-1][0]}'\n")  # repetir ultimo
        out_e = ROOT / f"etapa{eid}.mp4"
        run([ff, "-y", "-f", "concat", "-safe", "0", "-i", str(lst),
             "-i", str(audio),
             "-r", "25", "-c:v", "libx264", "-preset", "medium",
             "-tune", "stillimage", "-crf", "20", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "128k",
             "-movflags", "+faststart", "-shortest", str(out_e)])
        etapa_videos.append(out_e)
        global_offset += dur
        print(f"  etapa {eid} OK: {et['nombre']} ({dur:.1f}s, {len(cues)} cues)")

    # SRT
    srt = ROOT / "PRIMER_PARCIAL_modelos.srt"
    with srt.open("w", encoding="utf-8") as fh:
        for i, (a, b, txt) in enumerate(srt_entries, 1):
            fh.write(f"{i}\n{fmt_ts(a)} --> {fmt_ts(b)}\n{txt}\n\n")

    if only_frames:
        print(f"frames listos: {sum(1 for _ in frames_dir.glob('*.png'))} "
              f"(dur estimada total {global_offset:.1f}s)")
        return

    # concat final
    final_list = ROOT / "concat_final.txt"
    with final_list.open("w") as fh:
        for v in etapa_videos:
            fh.write(f"file '{v}'\n")
    final = ROOT / "PRIMER_PARCIAL_modelos.mp4"
    run([ff, "-y", "-f", "concat", "-safe", "0", "-i", str(final_list),
         "-c", "copy", str(final)])

    from mutagen.mp4 import MP4
    total = MP4(str(final)).info.length
    print("\n== RESUMEN ==")
    for eid, nom, dur, nc, ns in resumen:
        print(f"  etapa {eid}: {nom:38s} {dur:6.1f}s  cues={nc:2d} slides={ns}")
    print(f"  TOTAL: {total/60:.1f} min | {final.stat().st_size/1e6:.1f} MB")
    print(f"  video: {final}")
    print(f"  srt  : {srt}")


if __name__ == "__main__":
    main()
