#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera GUIA_ESTUDIO_parcial.pdf a partir de GUIA_ESTUDIO_parcial.md,
agregando como ANEXO el codigo fuente de las soluciones.

Uso:  python generar_pdf.py
Requiere: markdown, xhtml2pdf, pypdf  (instalados en /home/user/.venv)
"""
import html
import io
import pathlib
import re
import sys

import markdown
from xhtml2pdf import pisa

ROOT = pathlib.Path(__file__).resolve().parent
MD_PATH = ROOT / "GUIA_ESTUDIO_parcial.md"
PDF_PATH = ROOT / "GUIA_ESTUDIO_parcial.pdf"
ANEXOS = [
    ("Anexo A &mdash; ejercicio1_estudiantes.py", ROOT / "ejercicio1_estudiantes.py"),
    ("Anexo B &mdash; ejercicio2_stock.py", ROOT / "ejercicio2_stock.py"),
    ("Anexo C &mdash; ejercicio3_inventario.py", ROOT / "ejercicio3_inventario.py"),
]

# ---------------------------------------------------------------
# Sanitizado: la tipografia del PDF (Helvetica/DejaVu) no cubre
# emojis ni flechas/cuadros Unicode. Los convertimos a texto.
# ---------------------------------------------------------------
REEMPLAZOS = {
    "\u2192": "->",   "\u2190": "<-",   "\u2191": "^",    "\u2193": "v",
    "\u2265": ">=",   "\u2264": "<=",
    "\u2500": "-",    "\u2502": "|",    "\u251c": "+-",   "\u2514": "+-",
    "\u25b6": ">",    "\u25c0": "<",    "\u25b2": "^",    "\u25bc": "v",
    "\u2713": "[OK]", "\u2717": "[X]",  "\u26a0": "[!]",
    "\u2705": "[OK]", "\u274c": "[X]",
    "\u2260": "!=",
}
DESCONOCIDOS = set()


def sanitize(text: str) -> str:
    for old, new in REEMPLAZOS.items():
        text = text.replace(old, new)
    # emojis y variantes visuales (U+1F000.., VS16, ZWJ, misc symbols)
    text = re.sub(r"[\U0001F000-\U0001FAFF\uFE0F\u200D\u2600-\u26FF]", "", text)
    out = []
    for ch in text:
        try:
            ch.encode("cp1252")   # todo lo que Helvetica soporta
            out.append(ch)
        except UnicodeEncodeError:
            DESCONOCIDOS.add(ch)
            out.append("?")
    return "".join(out)


CSS = """
@page { size: A4; margin: 1.5cm 1.4cm; }
@font-face { font-family: 'DejaVu'; src: url(file:///usr/share/fonts/truetype/dejavu/DejaVuSans.ttf); }
@font-face { font-family: 'DejaVu'; src: url(file:///usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf); font-weight: bold; }
@font-face { font-family: 'DejaVuMono'; src: url(file:///usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf); }
body { font-family: DejaVu, Helvetica, sans-serif; font-size: 9.3pt; line-height: 1.35; color: #111; }
h1 { font-size: 16pt; color: #0f3460; margin-bottom: 3pt; }
h2 { font-size: 12.5pt; color: #0f3460; margin-top: 13pt; padding-bottom: 2pt;
     border-bottom: 1px solid #bbb; page-break-after: avoid; }
h3 { font-size: 10.5pt; color: #16213e; margin-top: 9pt; page-break-after: avoid; }
h2.anexo { page-break-before: always; }
pre { font-family: DejaVuMono, monospace; font-size: 7.4pt; line-height: 1.25;
      background-color: #f6f6f6; border: 1px solid #dddddd;
      padding: 5pt; margin: 4pt 0 7pt 0; }
code { font-family: DejaVuMono, monospace; font-size: 8pt; background-color: #f0f0f0; }
pre code { font-size: 7.4pt; background-color: transparent; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 8.3pt; }
th, td { border: 1px solid #888888; padding: 3pt 4pt; vertical-align: top; }
th { background-color: #e8eef7; }
blockquote { border-left: 3px solid #999999; margin: 5pt 0; padding: 2pt 8pt; color: #333333; }
ul, ol { margin-top: 2pt; margin-bottom: 4pt; }
li { margin-bottom: 1.5pt; }
hr { color: #cccccc; }
strong { color: #000000; }
"""


def build_html() -> str:
    md_text = sanitize(MD_PATH.read_text(encoding="utf-8"))
    body = markdown.markdown(md_text, extensions=["tables", "fenced_code", "sane_lists"])

    anexos = []
    for titulo, path in ANEXOS:
        if not path.exists():
            continue
        code = sanitize(path.read_text(encoding="utf-8"))
        anexos.append(f"<h2>{titulo}</h2>\n<pre>{html.escape(code)}</pre>")

    return (
        "<html><head><meta charset='utf-8'><style>"
        + CSS
        + "</style></head><body>"
        + body
        + "\n".join(anexos)
        + "</body></html>"
    )


def main() -> None:
    if not MD_PATH.exists():
        sys.exit(f"No existe {MD_PATH}")

    full_html = build_html()
    buffer = io.BytesIO()
    status = pisa.CreatePDF(
        io.BytesIO(full_html.encode("utf-8")), dest=buffer, encoding="utf-8"
    )
    if status.err:
        sys.exit("xhtml2pdf reporto errores al generar el PDF")

    PDF_PATH.write_bytes(buffer.getvalue())

    # ---- verificacion ----
    from pypdf import PdfReader
    reader = PdfReader(str(PDF_PATH))
    text = "\n".join((page.extract_text() or "") for page in reader.pages)
    plano = re.sub(r"\s+", "", text)   # sin espacios/saltos: tolera cortes de linea

    chequeos = [
        ("guia completa (final)", "Datos de prueba oficiales"),
        ("checklist", "CHECKLIST"),
        ("anexo A (inicio)", "AnexoA"),
        ("anexo A (final - no cortado)", "5)Listadeaprobados"),
        ("anexo B (final - no cortado)", "4)Productosconstockpromediomenor"),
        ("anexo C (final - no cortado)", "5)Productossinstock"),
        ("valor total Ej3", "815000"),
        ("errata Ej1", "Reprobado"),
    ]
    for nombre, token in chequeos:
        ok = re.sub(r"\s+", "", token) in plano
        print(f"  [{'OK' if ok else 'FALTA'}] {nombre}")

    if DESCONOCIDOS:
        print("  caracteres sin soporte (reemplazados por '?'): ", sorted(DESCONOCIDOS))

    print(f"  paginas: {len(reader.pages)}")
    print(f"  tamano : {PDF_PATH.stat().st_size / 1024:.0f} KB")
    print(f"  salida : {PDF_PATH}")


if __name__ == "__main__":
    main()
