#!/usr/bin/env python3
"""Convierte un resumen en Markdown a PDF (A4), sin partir tablas ni bloques de código.

Uso:  python md2pdf.py entrada.md salida.pdf
Requiere:  pip install markdown pymupdf   y las fuentes DejaVu instaladas.
"""
import os, re, shutil, sys, tempfile
import markdown
import pymupdf

FONTS = '/usr/share/fonts/truetype/dejavu'
CSS = """
@font-face { font-family: DV; src: url(DejaVuSans.ttf); }
@font-face { font-family: DV; src: url(DejaVuSans-Bold.ttf); font-weight: bold; }
@font-face { font-family: DVM; src: url(DejaVuSansMono.ttf); }
@font-face { font-family: DVM; src: url(DejaVuSansMono-Bold.ttf); font-weight: bold; }
body { font-family: DV; font-size: 9.5pt; line-height: 1.35; color: #1a1a1a; }
h1 { font-size: 19pt; color: #12355b; margin: 0 0 6pt 0; line-height: 1.2; }
h2 { font-size: 14pt; color: #12355b; border-bottom: 1.2pt solid #12355b; padding-bottom: 2pt; margin: 16pt 0 6pt 0; page-break-after: avoid; }
h3 { font-size: 11pt; color: #1f5a8a; margin: 10pt 0 4pt 0; page-break-after: avoid; }
p { margin: 0 0 5pt 0; }
p.mark { margin: 0; font-size: 1pt; line-height: 1; }
ul, ol { margin: 0 0 5pt 0; padding-left: 16pt; }
li { margin-bottom: 1.5pt; }
em { font-family: DV; font-style: normal; }
code { font-family: DVM; font-size: 8.8pt; background-color: #eef1f4; }
pre { font-family: DVM; font-size: 8pt; line-height: 1.15; border: 0.5pt solid #c9d1d9; padding: 6pt; margin: 4pt 0 8pt 0; white-space: pre; }
pre code { font-size: 8pt; background-color: #ffffff; }
table { border-collapse: collapse; margin: 4pt 0 8pt 0; width: 100%; }
th { color: #12355b; font-weight: bold; padding: 3pt 4pt; text-align: left; font-size: 9pt; border: 0.5pt solid #b5bfc9; border-bottom: 1.5pt solid #12355b; }
td { padding: 3pt 4pt; border: 0.5pt solid #b5bfc9; font-size: 9pt; vertical-align: top; }
hr { display: none; }
"""
BRK = ' style="page-break-before: always"'


def to_html(src):
    src = src.replace('\ufe0f', '')
    out, incode = [], False
    for line in src.split('\n'):          # python-markdown pide 4 espacios para listas anidadas
        if line.startswith('```'):
            incode = not incode
        if not incode:
            m = re.match(r'^( +)(- |\d+\. |\S)', line)
            if m:
                line = m.group(1) + line
        out.append(line)
    html = markdown.markdown('\n'.join(out), extensions=['tables', 'fenced_code', 'sane_lists'])
    n = [0]

    def tag_table(m):
        n[0] += 1
        t = m.group(0).replace('<table>', f'<table id="s{n[0]}">', 1)
        k = t.rindex('<tr>')
        return t[:k] + f'<tr id="e{n[0]}">' + t[k + 4:]

    def tag_pre(m):
        n[0] += 1
        return f'<pre id="s{n[0]}">' + m.group(1) + f'</pre>\n<p class="mark" id="e{n[0]}"></p>'

    html = re.sub(r'<table>.*?</table>', tag_table, html, flags=re.S)
    html = re.sub(r'<pre>(.*?)</pre>', tag_pre, html, flags=re.S)

    def tag_h(m):
        n[0] += 1
        return f'<{m.group(1)} id="h{n[0]}">'

    html = re.sub(r'<(h[23])>', tag_h, html)
    return html


def render(html, workdir, raw):
    page = pymupdf.paper_rect('a4')
    where = page + (48, 50, -48, -56)
    story = pymupdf.Story(html=f'<html><body>{html}</body></html>', user_css=CSS, archive=pymupdf.Archive(workdir))
    w = pymupdf.DocumentWriter(raw)
    pages, low, more, pno = {}, set(), 1, 0
    while more:
        pno += 1
        dev = w.begin_page(page)
        more, _ = story.place(where)

        def cb(pos):
            if pos.id and pos.id[0] in 'se':
                pages.setdefault(pos.id[1:], set()).add(pos.page)
            elif pos.id and pos.id[0] == 'h' and pos.rect[3] > where.y1 - 60:
                low.add(pos.id[1:])           # título suelto al pie de la página
        story.element_positions(cb, {'page': pno})
        story.draw(dev)
        w.end_page()
    w.close()
    return pages, low


def main(src_path, out_path):
    src = open(src_path, encoding='utf-8').read()
    title = re.search(r'^# (.+)$', src, flags=re.M).group(1)
    html = to_html(src)
    workdir = tempfile.mkdtemp()
    for f in os.listdir(FONTS):
        if f.startswith('DejaVuSans'):
            shutil.copy(os.path.join(FONTS, f), workdir)
    raw = os.path.join(workdir, 'raw.pdf')
    done = set()
    for _ in range(80):                   # agrega saltos hasta que ningún bloque quede partido
        pages, low = render(html, workdir, raw)
        split = sorted([(int(k), 's') for k, ps in pages.items() if len(ps) > 1 and k not in done]
                       + [(int(k), 'h') for k in low if k not in done])
        if not split:
            break
        k, kind = str(split[0][0]), split[0][1]
        done.add(k)
        idx = html.index(f' id="{kind}{k}"')
        idx = html.rindex('<', 0, idx)
        if kind == 'h':
            m = re.search(r'(<h2 id="h\d+">[^\n]*</h2>\n)$', html[:idx])
        else:
            m = re.search(r'(<h2 id="h\d+">[^\n]*</h2>\n)?(<h3 id="h\d+">[^\n]*</h3>\n)?((?:<p>[^\n]{0,220}</p>\n){0,2})$', html[:idx])
        if m and m.group(0):
            end = html.index('>', m.start())
            html = html[:end] + BRK + html[end:]
        elif kind == 'h':
            end = html.index('>', idx)
            html = html[:end] + BRK + html[end:]
        else:
            html = html[:idx] + f'<p class="mark"{BRK}></p>\n' + html[idx:]
    left = [k for k, ps in render(html, workdir, raw)[0].items() if len(ps) > 1]
    doc = pymupdf.open(raw)
    font = pymupdf.Font(fontfile=os.path.join(workdir, 'DejaVuSans.ttf'))
    for i, p in enumerate(doc):
        p.wrap_contents()
        tw = pymupdf.TextWriter(p.rect, color=(0.45, 0.45, 0.45))
        t = f'{title} — página {i + 1} de {len(doc)}'
        tw.append(((p.rect.width - font.text_length(t, 7.5)) / 2, p.rect.height - 28), t, font=font, fontsize=7.5)
        tw.write_text(p)
    doc.set_metadata({'title': title})
    doc.subset_fonts()
    doc.save(out_path, garbage=4, deflate=True)
    print(f'{out_path}: {len(doc)} páginas, saltos agregados: {len(done)}, bloques aún partidos: {len(left)}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
