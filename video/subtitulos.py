#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera video/subtitulos.srt a partir de los textos de segmentos.py.
La duracion de cada segmento sale de su mp3; dentro del segmento,
cada cue recibe un tiempo proporcional a su longitud de caracteres.

Uso:  python video/subtitulos.py
"""
import pathlib
import re
import subprocess
import sys

import imageio_ffmpeg

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from segmentos import SEGMENTOS

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = pathlib.Path(__file__).resolve().parent
AUDIO = BASE / "audio"
SRT = BASE / "subtitulos.srt"

MAX_LEN = 92      # caracteres maximos por cue (≈ 2 renglones)
MIN_LEN = 16      # cues mas cortos que esto se fusionan con el vecino


def duracion(path):
    r = subprocess.run([FF, "-hide_banner", "-i", str(path)],
                       capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        raise RuntimeError(f"no pude leer duracion de {path}")
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def dividir_cues(texto):
    """Divide el texto en cues cortos (frases naturales)."""
    texto = texto.strip()
    partes = re.split(r"(?<=[.!?;:])\s+", texto)
    cues = []
    for p in partes:
        while len(p) > MAX_LEN:
            cut = p.rfind(", ", 0, MAX_LEN)
            if cut < MAX_LEN * 0.4:
                cut = p.rfind(" ", 0, MAX_LEN)
            if cut <= 0:
                cut = MAX_LEN
            cues.append(p[: cut + 1].strip())
            p = p[cut + 1 :].strip()
        if p:
            cues.append(p)
    # fusiona cues muy cortos con el anterior
    fusion = []
    for c in cues:
        if fusion and (len(c) < MIN_LEN or len(fusion[-1]) < MIN_LEN) \
                and len(fusion[-1]) + len(c) + 1 <= MAX_LEN:
            fusion[-1] = fusion[-1] + " " + c
        else:
            fusion.append(c)
    return fusion


def fmt(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int(round((t - int(t)) * 1000))
    if ms == 1000:
        s, ms = s + 1, 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main():
    bloques = []   # (t0, t1, texto)
    cursor = 0.0
    total_cues = 0
    for seg in SEGMENTOS:
        i = f"{seg['id']:02d}"
        mp3 = AUDIO / f"seg_{i}.mp3"
        clip = BASE / "segmentos_mp4" / f"{i}.mp4"
        if not mp3.exists():
            raise SystemExit(f"falta {mp3}")
        # la voz ocupa los primeros d_voz segundos; la frontera del segmento
        # en la linea de tiempo del video final es la duracion del CLIP
        d_voz = duracion(mp3)
        d_clip = duracion(clip) if clip.exists() else d_voz
        cues = dividir_cues(seg["texto"])
        pesos = [max(len(c), 1) for c in cues]
        total = sum(pesos)
        t = cursor
        for c, w in zip(cues, pesos):
            dur_cue = d_voz * w / total
            bloques.append((t, t + dur_cue, c))
            t += dur_cue
            total_cues += 1
        cursor += d_clip

    lineas = []
    for n, (t0, t1, txt) in enumerate(bloques, 1):
        lineas.append(str(n))
        lineas.append(f"{fmt(t0)} --> {fmt(t1)}")
        lineas.append(txt)
        lineas.append("")
    SRT.write_text("\n".join(lineas), encoding="utf-8")

    print(f"SRT: {SRT}")
    print(f"  cues: {total_cues}")
    print(f"  duracion total: {cursor/60:.1f} min")
    print("  primeras cues:")
    for n, (t0, t1, txt) in enumerate(bloques[:4], 1):
        print(f"    {fmt(t0)} -> {fmt(t1)}  | {txt}")


if __name__ == "__main__":
    main()
