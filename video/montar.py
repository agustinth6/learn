#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Une frames + audios en el MP4 final.
Uso:  python video/montar.py
Construye un clip por segmento (imagen loop + audio) y luego los concatena.
"""
import pathlib
import re
import subprocess
import sys

import imageio_ffmpeg

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from segmentos import SEGMENTOS

FF = imageio_ffmpeg.get_ffmpeg_exe()
BASE = pathlib.Path(__file__).resolve().parent          # video/
FRAMES = BASE / "frames"
AUDIO = BASE / "audio"
SEGS = BASE / "segmentos_mp4"
OUT = BASE.parent / "video_explicativo_parcial.mp4"


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def duracion(path):
    r = run([FF, "-hide_banner", "-i", str(path)])
    m = re.search(r"Duration: (\d+):(\d+):(\d+\.\d+)", r.stderr)
    if not m:
        return None
    return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))


def main():
    SEGS.mkdir(parents=True, exist_ok=True)
    hechos = []
    for seg in SEGMENTOS:
        i = f"{seg['id']:02d}"
        frame = FRAMES / f"{i}.png"
        audio = AUDIO / f"seg_{i}.mp3"
        out = SEGS / f"{i}.mp4"
        if not frame.exists():
            print(f"  salto {i}: falta frame")
            continue
        if not audio.exists():
            print(f"  salto {i}: falta audio")
            continue
        cmd = [
            FF, "-y", "-hide_banner", "-loglevel", "error",
            "-loop", "1", "-framerate", "25", "-i", str(frame),
            "-i", str(audio),
            "-c:v", "libx264", "-tune", "stillimage", "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "128k", "-shortest",
            str(out),
        ]
        r = run(cmd)
        if r.returncode != 0:
            print(f"  ERROR seg {i}: {r.stderr[:400]}")
            continue
        d = duracion(out) or 0
        print(f"  seg {i}: {d:6.1f}s")
        hechos.append(out)

    if not hechos:
        print("No hay nada para unir (faltan audios).")
        return

    lst = BASE / "concat.txt"
    lst.write_text(
        "".join(f"file '{p.resolve()}'\n" for p in hechos), encoding="utf-8"
    )
    r = run([
        FF, "-y", "-hide_banner", "-loglevel", "error",
        "-f", "concat", "-safe", "0", "-i", str(lst),
        "-c", "copy", str(OUT),
    ])
    if r.returncode != 0:
        print("  concat con copy fallo; re-codifico...")
        r = run([
            FF, "-y", "-hide_banner", "-loglevel", "error",
            "-f", "concat", "-safe", "0", "-i", str(lst),
            "-c:v", "libx264", "-tune", "stillimage", "-crf", "20",
            "-c:a", "aac", str(OUT),
        ])
        if r.returncode != 0:
            print(r.stderr[:600])
            sys.exit(1)

    total = duracion(OUT) or 0
    print(
        f"OK: {OUT.name}  —  {total/60:.1f} min, "
        f"{OUT.stat().st_size // 1024} KB, {len(hechos)} segmentos"
    )


if __name__ == "__main__":
    main()
