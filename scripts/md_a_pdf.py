#!/usr/bin/env python3
"""
Convierte el resumen de estudio (Markdown) en un PDF con formato de apunte.

Uso:  python3 scripts/md_a_pdf.py resumen.md salida.pdf "Título del documento"
"""
import re
import sys
import html

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer,
    Table, TableStyle, KeepTogether, PageBreak, CondPageBreak,
)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DejaVu", f"{FONT_DIR}/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", f"{FONT_DIR}/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("Mono", f"{FONT_DIR}/DejaVuSansMono.ttf"))
pdfmetrics.registerFont(TTFont("Mono-Bold", f"{FONT_DIR}/DejaVuSansMono-Bold.ttf"))
pdfmetrics.registerFontFamily("DejaVu", normal="DejaVu", bold="DejaVu-Bold",
                              italic="DejaVu", boldItalic="DejaVu-Bold")

INK = colors.HexColor("#1a1a1a")
ACCENT = colors.HexColor("#1f4e79")      # azul títulos
ACCENT2 = colors.HexColor("#2e7d5b")     # verde subtítulos
CODE_BG = colors.HexColor("#f4f5f7")
CODE_BORDER = colors.HexColor("#d7dbe0")
RULE = colors.HexColor("#c9ced6")
ZEBRA = colors.HexColor("#f7f9fb")


def styles():
    ss = getSampleStyleSheet()
    s = {}
    s["body"] = ParagraphStyle(
        "body", parent=ss["BodyText"], fontName="DejaVu", fontSize=8.9,
        leading=12.6, textColor=INK, spaceAfter=4, alignment=TA_LEFT,
    )
    s["h1"] = ParagraphStyle(
        "h1", fontName="DejaVu-Bold", fontSize=18, leading=22, textColor=ACCENT,
        spaceBefore=0, spaceAfter=10,
    )
    s["h2"] = ParagraphStyle(
        "h2", fontName="DejaVu-Bold", fontSize=13, leading=16, textColor=ACCENT,
        spaceBefore=16, spaceAfter=7,
    )
    s["h3"] = ParagraphStyle(
        "h3", fontName="DejaVu-Bold", fontSize=10.4, leading=13, textColor=ACCENT2,
        spaceBefore=11, spaceAfter=5,
    )
    s["bullet"] = ParagraphStyle(
        "bullet", parent=s["body"], leftIndent=11, bulletIndent=2,
        spaceAfter=2.2,
    )
    s["code"] = ParagraphStyle(
        "code", fontName="Mono", fontSize=7.5, leading=9.9, textColor=INK,
        leftIndent=6, rightIndent=2, spaceBefore=1, spaceAfter=1,
    )
    s["cell"] = ParagraphStyle(
        "cell", fontName="DejaVu", fontSize=7.9, leading=10.4, textColor=INK,
    )
    s["cellh"] = ParagraphStyle(
        "cellh", fontName="DejaVu-Bold", fontSize=7.9, leading=10.4,
        textColor=colors.white,
    )
    s["toc"] = ParagraphStyle(
        "toc", fontName="DejaVu", fontSize=9, leading=14.5, textColor=INK,
    )
    return s


def inline(text):
    """Markdown inline -> etiquetas soportadas por ReportLab."""
    text = html.escape(text, quote=False)
    # código inline primero (protegido con marcadores)
    held = []

    def hold(m):
        held.append(f'<font name="Mono" size="8">{m.group(1)}</font>')
        return f"\x00{len(held)-1}\x00"

    text = re.sub(r"`([^`]+)`", hold, text)
    # enlaces markdown [texto](#ancla) -> solo el texto
    text = re.sub(r"\[([^\]]+)\]\(#[^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", text)
    for i, frag in enumerate(held):
        text = text.replace(f"\x00{i}\x00", frag)
    return text


def split_row(line):
    """Divide una fila de tabla markdown respetando los | escapados y el inline."""
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells, buf, in_code = [], [], False
    for ch in line:
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def build(md_path, pdf_path, title):
    md = open(md_path, encoding="utf-8").read()
    st = styles()
    story = []

    lines = md.split("\n")
    i = 0
    first_h1 = True

    while i < len(lines):
        line = lines[i]

        # --- bloque de código ---
        if line.strip().startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            code = "\n".join(buf).rstrip("\n")
            if code:
                blk = code_block(code, st)
                if isinstance(blk, list):
                    story.extend(blk)
                else:
                    story.append(blk)
            continue

        # --- tabla ---
        if line.strip().startswith("|") and i + 1 < len(lines) and \
                re.match(r"^\s*\|[\s:|-]+\|\s*$", lines[i + 1]):
            header = split_row(line)
            i += 2
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i]))
                i += 1
            story.extend(table_block(header, rows, st))
            continue

        # --- separador ---
        if re.match(r"^\s*---+\s*$", line):
            story.append(Spacer(1, 3))
            story.append(hr())
            i += 1
            continue

        # --- títulos ---
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            if level == 1:
                if first_h1:
                    story.append(Paragraph(inline(text), st["h1"]))
                    first_h1 = False
                else:
                    story.append(Paragraph(inline(text), st["h1"]))
                story.append(hr(thick=True))
            elif level == 2:
                story.append(Spacer(1, 4))
                story.append(Paragraph(inline(text), st["h2"]))
                story.append(hr())
            else:
                story.append(Paragraph(inline(text), st["h3"]))
            i += 1
            continue

        # --- cita ---
        if line.strip().startswith(">"):
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip().lstrip(">").strip())
                i += 1
            story.extend(quote_block(" ".join(buf), st))
            continue

        # --- listas ---
        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\s*[-*]\s+", lines[i]):
                items.append(re.sub(r"^\s*[-*]\s+", "", lines[i]))
                i += 1
                # continuación indentada
                while i < len(lines) and lines[i].startswith("  ") and \
                        lines[i].strip() and not re.match(r"^\s*[-*]\s+", lines[i]):
                    items[-1] += " " + lines[i].strip()
                    i += 1
            for it in items:
                story.append(Paragraph(inline(it), st["bullet"], bulletText="•"))
            story.append(Spacer(1, 2))
            continue

        # --- listas numeradas ---
        if re.match(r"^\s*\d+\.\s+", line):
            while i < len(lines) and re.match(r"^\s*\d+\.\s+", lines[i]):
                num = re.match(r"^\s*(\d+)\.\s+(.*)$", lines[i])
                txt = num.group(2)
                i += 1
                while i < len(lines) and lines[i].startswith("   ") and \
                        lines[i].strip():
                    txt += " " + lines[i].strip()
                    i += 1
                story.append(Paragraph(inline(txt), st["bullet"],
                                       bulletText=f"{num.group(1)}."))
            story.append(Spacer(1, 2))
            continue

        # --- línea vacía ---
        if not line.strip():
            i += 1
            continue

        # --- párrafo ---
        buf = []
        while i < len(lines) and lines[i].strip() and \
                not lines[i].strip().startswith(("```", "|", ">", "#")) and \
                not re.match(r"^\s*[-*]\s+", lines[i]) and \
                not re.match(r"^\s*\d+\.\s+", lines[i]) and \
                not re.match(r"^\s*---+\s*$", lines[i]):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            story.append(Paragraph(inline(" ".join(buf)), st["body"]))

    # --- títulos: nunca dejarlos solos al pie de página ---
    frame_w = A4[0] - 3.7 * cm
    frame_h = A4[1] - 3.1 * cm
    import io as _io
    from reportlab.pdfgen.canvas import Canvas as _Canvas
    _c = _Canvas(_io.BytesIO(), pagesize=A4)

    def _h(f):
        try:
            return f.wrapOn(_c, frame_w, frame_h)[1]
        except Exception:
            return 0

    fixed = []
    k = 0
    while k < len(story):
        item = story[k]
        if isinstance(item, Paragraph) and item.style.name in ("h2", "h3"):
            j = k + 1
            while j < len(story) and isinstance(story[j], (Spacer, CondPageBreak)):
                j += 1
            group = [item] + story[k + 1:j]
            if j < len(story):
                hb = _h(story[j])
                # solo se arrastra el bloque si es corto (no parte tablas grandes)
                if 0 < hb < frame_h * 0.5:
                    group.append(story[j])
                    j += 1
            fixed.append(KeepTogether(group))
            k = j
            continue
        fixed.append(item)
        k += 1
    story = fixed

    doc = BaseDocTemplate(
        pdf_path, pagesize=A4,
        leftMargin=1.85 * cm, rightMargin=1.85 * cm,
        topMargin=1.6 * cm, bottomMargin=1.5 * cm,
        title=title, author="Resumen de estudio",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame],
                                       onPage=decorate(title))])
    doc.build(story)
    print(f"PDF generado: {pdf_path}")


def hr(thick=False):
    from reportlab.platypus import Flowable

    class Rule(Flowable):
        def __init__(self, thick):
            super().__init__()
            self.thick = thick
            self.width = 0
            self.height = 4

        def wrap(self, aw, ah):
            self.width = aw
            return aw, 4

        def draw(self):
            self.canv.setStrokeColor(ACCENT if self.thick else RULE)
            self.canv.setLineWidth(1.1 if self.thick else 0.5)
            self.canv.line(0, 2, self.width, 2)

    return Rule(thick)


CHUNK = 30  # líneas por tramo: permite cortar de página en bloques largos


def _code_table(lines, st):
    inner = []
    for ln in lines:
        safe = html.escape(ln, quote=False).replace(" ", "&nbsp;")
        inner.append(Paragraph(safe if safe else "&nbsp;", st["code"]))
    t = Table([[inner]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), CODE_BG),
        ("BOX", (0, 0), (-1, -1), 0.5, CODE_BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def code_block(code, st):
    """Devuelve una lista de flowables; los bloques largos se parten en tramos."""
    lines = code.split("\n")
    if len(lines) <= CHUNK:
        t = _code_table(lines, st)
        h = 8 * len(lines) + 14
        head = [CondPageBreak(min(h + 10, 20 * cm))] if h else []
        return head + [Spacer(1, 3), t, Spacer(1, 7)]

    out = []
    for start in range(0, len(lines), CHUNK):
        part = lines[start:start + CHUNK]
        out.append(_code_table(part, st))
        out.append(Spacer(1, 1.5))
    out.append(Spacer(1, 5.5))
    return out


def table_block(header, rows, st):
    ncols = len(header)
    data = [[Paragraph(inline(c), st["cellh"]) for c in header]]
    for r in rows:
        r = (r + [""] * ncols)[:ncols]
        data.append([Paragraph(inline(c), st["cell"]) for c in r])

    # ancho: la primera columna un poco más angosta si hay muchas columnas
    avail = A4[0] - 3.7 * cm
    if ncols <= 2:
        widths = [avail * 0.34, avail * 0.66]
    elif ncols == 3:
        widths = [avail * 0.24, avail * 0.42, avail * 0.34]
    else:
        widths = [avail / ncols] * ncols

    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), ACCENT),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, CODE_BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3.6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3.6),
    ]
    for r in range(1, len(data)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), ZEBRA))
    t.setStyle(TableStyle(style))
    return [Spacer(1, 3), t, Spacer(1, 8)]


def quote_block(text, st):
    p = Paragraph(inline(text), st["body"])
    t = Table([[p]], colWidths=["100%"])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#eef4fa")),
        ("LINEBEFORE", (0, 0), (0, -1), 2.5, ACCENT),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    return [Spacer(1, 3), t, Spacer(1, 7)]


def decorate(title):
    def draw(canvas, doc):
        canvas.saveState()
        canvas.setFont("DejaVu", 7)
        canvas.setFillColor(colors.HexColor("#8a9199"))
        canvas.drawString(doc.leftMargin, A4[1] - 1.05 * cm, title)
        canvas.drawRightString(A4[0] - doc.rightMargin, A4[1] - 1.05 * cm,
                               "Administración y Gestión de Bases de Datos")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, A4[1] - 1.22 * cm,
                    A4[0] - doc.rightMargin, A4[1] - 1.22 * cm)
        canvas.line(doc.leftMargin, 1.15 * cm,
                    A4[0] - doc.rightMargin, 1.15 * cm)
        canvas.setFont("DejaVu", 7.5)
        canvas.drawCentredString(A4[0] / 2, 0.82 * cm, f"{doc.page}")
        canvas.restoreState()
    return draw


if __name__ == "__main__":
    build(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "Resumen")
