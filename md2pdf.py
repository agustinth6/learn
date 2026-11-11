#!/usr/bin/env python3
"""Convertidor Markdown -> PDF (estilo apunte/ficha de estudio) usando ReportLab.

Uso:  python3 md2pdf.py archivo.md salida.pdf

Soporta el subconjunto de Markdown usado en los resumenes:
titulos (#..####), parrafos, listas (-, 1.), anidados, tablas |..|,
bloques de codigo (```), citas (>), **negrita**, *italia*, `codigo`.
"""
import re
import sys
import unicodedata

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
    XPreformatted,
)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"
SANS = "DejaVu"
MONO = "DejaVuMono"

ACCENT = colors.HexColor("#1F5FA8")
ACCENT_SOFT = colors.HexColor("#EDF3FA")
CODE_BG = colors.HexColor("#F4F5F7")
CODE_BORDER = colors.HexColor("#D7DBE0")
QUOTE_BG = colors.HexColor("#FBF6E9")
QUOTE_BORDER = colors.HexColor("#E0C97F")
TEXT = colors.HexColor("#1A1A1A")
MUTED = colors.HexColor("#5A6472")
TABLE_HEAD = colors.HexColor("#1F5FA8")
TABLE_ALT = colors.HexColor("#F6F8FB")
GRID = colors.HexColor("#C9D2DC")

EMOJI_RE = re.compile(
    "["
    "\U0001F000-\U0001FAFF"
    "\u2600-\u27BF"
    "\u2B00-\u2BFF"
    "\uFE0F"
    "\u200d"
    "]",
    flags=re.UNICODE,
)


def register_fonts():
    pdfmetrics.registerFont(TTFont(SANS, FONT_DIR + "DejaVuSans.ttf"))
    pdfmetrics.registerFont(TTFont(SANS + "-Bold", FONT_DIR + "DejaVuSans-Bold.ttf"))
    pdfmetrics.registerFont(TTFont(MONO, FONT_DIR + "DejaVuSansMono.ttf"))
    pdfmetrics.registerFont(TTFont(MONO + "-Bold", FONT_DIR + "DejaVuSansMono-Bold.ttf"))
    registerFontFamily(
        SANS, normal=SANS, bold=SANS + "-Bold", italic=SANS, boldItalic=SANS + "-Bold"
    )
    registerFontFamily(
        MONO,
        normal=MONO,
        bold=MONO + "-Bold",
        italic=MONO,
        boldItalic=MONO + "-Bold",
    )


def styles():
    def st(name, **kw):
        base = dict(
            fontName=SANS,
            fontSize=9.6,
            leading=14.2,
            textColor=TEXT,
            alignment=TA_LEFT,
            spaceBefore=0,
            spaceAfter=4,
        )
        base.update(kw)
        return ParagraphStyle(name, **base)

    return {
        "title": st("title", fontSize=21, leading=27, textColor=ACCENT, spaceAfter=7),
        "subtitle": st("subtitle", fontSize=10.5, leading=14, textColor=MUTED, spaceAfter=10),
        "h2": st(
            "h2",
            fontSize=14.5,
            leading=18,
            textColor=colors.white,
            backColor=ACCENT,
            borderPadding=(5, 6, 5, 6),
            spaceBefore=14,
            spaceAfter=8,
            keepWithNext=1,
        ),
        "h3": st("h3", fontSize=11.6, leading=15, textColor=ACCENT, spaceBefore=10, spaceAfter=4, keepWithNext=1),
        "h4": st("h4", fontSize=10.4, leading=14, textColor=colors.HexColor("#2E5F8F"), spaceBefore=8, spaceAfter=3, keepWithNext=1),
        "body": st("body", spaceAfter=5),
        "bullet": st("bullet", leftIndent=13, bulletIndent=3, spaceAfter=2.5),
        "bullet2": st("bullet2", leftIndent=27, bulletIndent=17, spaceAfter=2, fontSize=9.3, leading=13.4),
        "num": st("num", leftIndent=16, bulletIndent=2, spaceAfter=2.5),
        "quote": st("quote", fontSize=9.3, leading=13.4, textColor=colors.HexColor("#6B5A28"), leftIndent=4, rightIndent=4, spaceAfter=0),
        "code": st("code", fontName=MONO, fontSize=8.3, leading=11.4, spaceAfter=0),
        "cell": st("cell", fontSize=8.6, leading=11.6, spaceAfter=0),
        "cellhead": st("cellhead", fontSize=8.6, leading=11.6, textColor=colors.white, spaceAfter=0),
        "note": st("note", fontSize=8.8, leading=12.4, textColor=MUTED),
    }


S = styles()


def clean(text):
    text = EMOJI_RE.sub("", text)
    text = (
        text.replace("\u2705", "")
        .replace("\u274c", "")
        .replace("\u2b50", "")
        .replace("\u21b9", "")
        .replace("\u21aa", "")
    )
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text


def inline(text, code_size=8.6):
    """Markdown en linea -> markup de Paragraph."""
    text = text.replace("\\", "\\\\")
    text = (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    # vinculos: [texto](url) -> texto (url)  |  anclas internas -> solo texto
    def link(m):
        label, url = m.group(1), m.group(2)
        if url.startswith("#"):
            return label
        return f"{label} ({url})"

    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    # citas `codigo` -> fuente mono (protegido del resto del markup)
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    text = re.sub(r"`([^`]+)`", stash, text)
    text = text.replace("&lt;br&gt;", "<br/>").replace("&lt;br/&gt;", "<br/>")
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?!\*)", r"<i>\1</i>", text)
    for i, code in enumerate(spans):
        code = code.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
        code = code.replace("\\", "\\\\")
        code = (
            code.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace(" ", "&nbsp;")
        )
        text = text.replace(
            f"\x00{i}\x00",
            f'<font face="{MONO}" size="{code_size}" color="#8A3324">{code}</font>',
        )
    return text


def boxed(flow, bg, border, pad=6):
    t = Table([[flow]], colWidths=[None], hAlign="LEFT")
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), bg),
                ("BOX", (0, 0), (-1, -1), 0.7, border),
                ("LEFTPADDING", (0, 0), (-1, -1), pad),
                ("RIGHTPADDING", (0, 0), (-1, -1), pad),
                ("TOPPADDING", (0, 0), (-1, -1), pad - 1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), pad - 1),
                ("LINEBEFORE", (0, 0), (0, -1), 2.2, border),
            ]
        )
    )
    return t


def _plain(cell):
    return re.sub(r"<br\s*/?>", " ", re.sub(r"[`*_]", "", cell))


_plain = lambda c: re.sub(r'<br\s*/?>', ' ', re.sub(r'[`*_]', '', c))


def make_table(rows, avail):
    avail = avail - 2.5  # pequeno respiro para no tocar el margen
    header, body = rows[0], rows[1:]
    ncols = max(len(r) for r in rows)
    header = (header + [""] * ncols)[:ncols]
    body = [(r + [""] * ncols)[:ncols] for r in body]
    all_rows = [header] + body

    CHAR_W = 6.0  # ancho aprox. por caracter a 8.6 pt (DejaVu / mono, con margen)
    PAD = 10

    def stats(i):
        lens = [len(_plain(r[i])) for r in all_rows]
        words = [
            max((len(w) for w in _plain(r[i]).split()), default=3) for r in all_rows
        ]
        return sum(lens) / len(lens), max(lens), max(words)

    info = [stats(i) for i in range(ncols)]
    # 1) minimo garantizado: la palabra mas larga entra sin cortarse
    min_w = [min(info[i][2] * CHAR_W + PAD, avail * 0.55) for i in range(ncols)]
    if sum(min_w) > avail:
        k = avail / sum(min_w)
        widths = [w * k for w in min_w]
    else:
        # 2) el resto del ancho se reparte segun el contenido de cada columna
        units = [max(min(avg * 1.6, longest) - words, 4) for avg, longest, words in info]
        free = avail - sum(min_w)
        widths = [min_w[i] + free * units[i] / sum(units) for i in range(ncols)]

    # en el encabezado de la tabla el `codigo` se deja como texto (fondo azul)
    data = [[Paragraph(inline(c.replace("`", ""), 7.9), S["cellhead"]) for c in header]]
    for r in body:
        data.append([Paragraph(inline(c, 7.9), S["cell"]) for c in r])

    t = Table(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEAD),
        ("GRID", (0, 0), (-1, -1), 0.5, GRID),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for i in range(1, len(data)):
        if i % 2 == 0:
            style.append(("BACKGROUND", (0, i), (-1, i), TABLE_ALT))
    t.setStyle(TableStyle(style))
    return t


CODE_MAXCH = 86  # caracteres por linea en fuente mono a 8.3 pt


def wrap_code(lines):
    """Respeta la sangria y parte las lineas que no entren en la caja."""
    out = []
    for line in lines:
        if len(line) <= CODE_MAXCH:
            out.append(line)
            continue
        indent = line[: len(line) - len(line.lstrip())]
        body = line.strip()
        cur = indent
        for word in body.split(" "):
            if cur.strip() and len(cur) + len(word) + 1 > CODE_MAXCH:
                out.append(cur.rstrip())
                cur = indent + "    "
            cur += word + " "
        out.append(cur.rstrip())
    return out


def code_block(lines, avail):
    txt = "\n".join(wrap_code(lines))
    txt = (
        txt.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    pre = XPreformatted(txt, S["code"])
    inner = Table([[pre]], colWidths=[avail - 14])
    inner.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return boxed(inner, CODE_BG, CODE_BORDER, pad=7)


def parse(md, avail):
    flow = []
    lines = md.split("\n")
    i = 0
    para = []
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            i += 1
            continue

        if stripped.startswith("```"):
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            i += 1
            buf = []
            while i < len(lines) and not lines[i].strip().startswith("```"):
                buf.append(lines[i].rstrip())
                i += 1
            nonblank = [b for b in buf if b.strip()]
            if nonblank:
                cut = min(len(b) - len(b.lstrip()) for b in nonblank)
                buf = [b[cut:] if b.strip() else "" for b in buf]
            i += 1
            flow.append(Spacer(1, 2))
            flow.append(code_block(buf, avail))
            flow.append(Spacer(1, 5))
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                r = lines[i].strip().strip("|")
                cells = [c.strip() for c in r.split("|")]
                rows.append(cells)
                i += 1
            rows = [r for r in rows if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in r)]
            if rows:
                flow.append(Spacer(1, 2))
                flow.append(make_table(rows, avail))
                flow.append(Spacer(1, 7))
            continue

        if re.fullmatch(r"-{3,}", stripped):
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            flow.append(Spacer(1, 3))
            flow.append(HRFlowable(width="100%", thickness=0.6, color=GRID))
            flow.append(Spacer(1, 5))
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            level, text = len(m.group(1)), m.group(2)
            if level <= 4:  # en los titulos el codigo se deja como texto
                text = text.replace("`", "")
            if level == 1:
                flow.append(Paragraph(inline(text), S["title"]))
            elif level == 2:
                flow.append(Paragraph(inline(text), S["h2"]))
            elif level == 3:
                flow.append(Paragraph(inline(text), S["h3"]))
            else:
                flow.append(Paragraph(inline(text), S["h4"]))
            i += 1
            continue

        if stripped.startswith(">"):
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                t = lines[i].strip()[1:].strip()
                if t:
                    buf.append(t)
                i += 1
            blocks = []
            for t in buf:
                blocks.append(Paragraph(inline(t), S["quote"]))
            q = Table([[b] for b in blocks], colWidths=[avail - 12])
            q.setStyle(
                TableStyle(
                    [
                        ("BACKGROUND", (0, 0), (-1, -1), QUOTE_BG),
                        ("LINEBEFORE", (0, 0), (0, -1), 2.6, QUOTE_BORDER),
                        ("LEFTPADDING", (0, 0), (-1, -1), 8),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                        ("TOPPADDING", (0, 0), (-1, -1), 2.5),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
                        ("VALIGN", (0, 0), (-1, -1), "TOP"),
                    ]
                )
            )
            flow.append(Spacer(1, 2))
            flow.append(q)
            flow.append(Spacer(1, 6))
            continue

        mb = re.match(r"^(\s*)([-*+])\s+(.*)$", raw)
        if mb:
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            depth = 1 if len(mb.group(1)) >= 2 else 0
            text = mb.group(3)
            # sub-listas o codigo dentro de la lista
            j = i + 1
            while j < len(lines) and re.match(r"^\s{2,}(\S|$)", lines[j]) and not re.match(
                r"^\s{0,1}[-*+]\s", lines[j]
            ):
                sub = lines[j].strip()
                if sub.startswith("- "):
                    flow.append(
                        Paragraph(
                            inline(sub[2:]),
                            S["bullet2"],
                            bulletText="–",
                        )
                    )
                elif sub.startswith("```"):
                    k = j + 1
                    buf = []
                    while k < len(lines) and not lines[k].strip().startswith("```"):
                        buf.append(lines[k].rstrip())
                        k += 1
                    nb = [b for b in buf if b.strip()]
                    if nb:
                        cut = min(len(b) - len(b.lstrip()) for b in nb)
                        buf = [b[cut:] if b.strip() else "" for b in buf]
                    flow.append(Spacer(1, 2))
                    flow.append(
                        boxed(
                            Paragraph(
                                "<br/>".join(
                                    b.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                                    for b in buf
                                ),
                                S["code"],
                            ),
                            CODE_BG,
                            CODE_BORDER,
                            pad=5,
                        )
                    )
                    flow.append(Spacer(1, 3))
                    j = k
                j += 1
            flow.append(
                Paragraph(
                    inline(text),
                    S["bullet2"] if depth else S["bullet"],
                    bulletText="•",
                )
            )
            i = j
            continue

        mn = re.match(r"^(\d+)[.)]\s+(.*)$", stripped)
        if mn:
            if para:
                flow.append(Paragraph(inline(" ".join(para)), S["body"]))
                para = []
            flow.append(
                Paragraph(inline(mn.group(2)), S["num"], bulletText=f"{mn.group(1)}.")
            )
            i += 1
            continue

        para.append(stripped)
        i += 1

    if para:
        flow.append(Paragraph(inline(" ".join(para)), S["body"]))
    return flow


def build(md_path, pdf_path, doc_title):
    register_fonts()
    md = clean(open(md_path, encoding="utf-8").read())

    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=1.7 * cm,
        rightMargin=1.7 * cm,
        topMargin=1.5 * cm,
        bottomMargin=1.5 * cm,
        title=doc_title,
        author="Resumen de estudio",
    )
    avail = doc.width

    def footer(canvas, _doc):
        canvas.saveState()
        canvas.setFont(SANS, 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawString(doc.leftMargin, 0.85 * cm, doc_title)
        canvas.drawRightString(
            A4[0] - doc.rightMargin, 0.85 * cm, f"Página {canvas.getPageNumber()}"
        )
        canvas.setStrokeColor(GRID)
        canvas.setLineWidth(0.5)
        canvas.line(doc.leftMargin, 1.15 * cm, A4[0] - doc.rightMargin, 1.15 * cm)
        canvas.restoreState()

    story = [
        Spacer(1, 2),
        Paragraph(f"Resumen de estudio · SQL y MySQL · {doc_date()}", S["note"]),
        Spacer(1, 6),
    ] + parse(md, avail)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return pdf_path


def doc_date():
    import datetime

    return datetime.date.today().strftime("%d/%m/%Y")


if __name__ == "__main__":
    src = sys.argv[1] if len(sys.argv) > 1 else "resumen-estudio-sql-mysql.md"
    dst = sys.argv[2] if len(sys.argv) > 2 else src.rsplit(".", 1)[0] + ".pdf"
    build(src, dst, "SQL y MySQL — Resumen de estudio")
    print("OK ->", dst)
