#!/usr/bin/env python3
"""Mini consola SQL para practicar con la base clinica_medica.

Lece practica/clinica_medica.sql, la carga en SQLite (sin necesidad de tener
MySQL instalado) y te deja ejecutar consultas.

Uso:
    python3 practica/run.py                      -> modo interactivo
    python3 practica/run.py "SELECT ..."         -> corre una consulta y sale
    python3 practica/run.py -f consultas.sql     -> corre un archivo
    python3 practica/run.py --tablas             -> resume las tablas

Trucos utiles en el modo interactivo:
    .tablas      mostrar filas y columnas de cada tabla
    .schema      DDL adaptado
    .load        recargar clinica_medica.sql (por si metiste un UPDATE/DELETE)
    .help        ayuda corta
"""
import os
import re
import sqlite3
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SQL_FILE = os.path.join(HERE, "clinica_medica.sql")
DB_FILE = os.path.join(HERE, ".clinica.sqlite")


def to_sqlite(text):
    """Adapta el script de MySQL para que lo acepte SQLite."""
    text = re.sub(r"^\s*--.*$", "", text, flags=re.M)
    keep = []
    for stmt in split_statements(text):
        if not stmt.strip():
            continue
        head = stmt.strip().upper().split(None, 1)[0]
        if head in ("USE", "SET"):
            continue
        if head == "DROP" and "TABLE" not in stmt.upper():
            continue
        if head == "CREATE" and re.match(r"(?i)^\s*CREATE\s+DATABASE", stmt):
            continue
        s = re.sub(
            r"(?i)\b(INT|INTEGER)\s+AUTO_INCREMENT\s+PRIMARY KEY\b",
            "INTEGER PRIMARY KEY AUTOINCREMENT",
            stmt.strip(),
        )
        s = re.sub(r"(?i)\s+AUTO_INCREMENT", "", s)
        keep.append(s + ";")
    return "\n".join(keep)


def split_statements(text):
    """Corta por ';' respetando comillas simples."""
    out, cur, quote = [], "", False
    for ch in text:
        if ch == "'":
            quote = not quote
        if ch == ";" and not quote:
            if cur.strip():
                out.append(cur.strip())
            cur = ""
            continue
        cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def build(force=False):
    if os.path.exists(DB_FILE) and not force:
        return sqlite3.connect(DB_FILE)
    raw = open(SQL_FILE, encoding="utf-8").read()
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    con = sqlite3.connect(DB_FILE)
    con.executescript("PRAGMA foreign_keys=ON;\n" + to_sqlite(raw))
    con.commit()
    return con


TABLES = ["especialidades", "pacientes", "medicos", "turnos"]


def info(con):
    print("filas por tabla:")
    for t in TABLES:
        n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
        cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
        print(f"  {t:<15} {n:>3} filas · columnas: {', '.join(cols)}")


def render(cols, rows):
    cells = []
    for r in rows:
        cells.append(
            [
                "NULL"
                if v is None
                else (f"{v:.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v))
                for v in r
            ]
        )
    head = [c if c else "?" for c in cols]
    if not cells:
        print("(0 filas)")
        return
    w = [len(h) for h in head]
    for r in cells:
        for i, v in enumerate(r):
            w[i] = max(w[i], len(v))
    line = "  ".join("-" * x for x in w)
    print("  ".join(h.ljust(w[i]) for i, h in enumerate(head)))
    print(line)
    for r in cells:
        print("  ".join(v.ljust(w[i]) for i, v in enumerate(r)))
    print(f"({len(cells)} fila{'s' if len(cells) != 1 else ''})")


AGGS = ("COUNT(", "SUM(", "AVG(", "MAX(", "MIN(", "GROUP_CONCAT(")


def _split_top(text, sep=","):
    """Parte por `sep` sin romper parentesis (para listas de columnas)."""
    out, cur, depth = [], "", 0
    for ch in text:
        if ch == "(":
            depth += 1
        elif ch == ")":
            depth -= 1
        if ch == sep and depth == 0:
            out.append(cur)
            cur = ""
            continue
        cur += ch
    out.append(cur)
    return [x.strip() for x in out if x.strip()]


def _depth0(text):
    """Devuelve la lista de profundidades de parentesis por caracter."""
    d, out = 0, []
    for ch in text:
        if ch == "(":
            out.append(d)
            d += 1
        elif ch == ")":
            d -= 1
            out.append(d)
        else:
            out.append(d)
    return out


def _at_top_level(text, pat):
    """Primera coincidencia de `pat` que este con parentesis balanceados (nivel 0)."""
    depths = _depth0(text)
    for m in re.finditer(pat, text, flags=re.I | re.S):
        if depths[m.start()] == 0:
            return m
    return None


def lint_group_by(stmt):
    """Aviso si la consulta reventaria en MySQL con ONLY_FULL_GROUP_BY."""
    g = _at_top_level(stmt, r"\bGROUP\s+BY\b")
    s = _at_top_level(stmt, r"\bSELECT\b")
    if not g or not s:
        return []
    frm = _at_top_level(stmt[s.end():], r"\bFROM\b")
    if not frm or s.end() + frm.start() > g.start():
        return []
    select_list = stmt[s.end() : s.end() + frm.start()]
    gb = re.split(r"(?is)\bHAVING\b|\bORDER\b|\bLIMIT\b", stmt[g.end() :])[0]
    grouped = [c.strip().rstrip(",;").lower() for c in _split_top(gb)]
    grouped_names = {c.split(".")[-1].strip("`") for c in grouped}
    # MySQL deja seleccionar columnas "dependientes" de la clave que esta agrupada
    keys = {c.split(".")[0] for c in grouped if c.split(".")[-1].startswith("id_")}
    bare_key = any(c.startswith("id_") and "." not in c for c in grouped)
    warns = []
    for col in _split_top(select_list):
        if "*" in col or any(a in col.upper() for a in AGGS):
            continue
        parts = re.split(r"(?i)\s+AS\s+", col, maxsplit=1)
        expr, alias = (parts[0], parts[-1]) if len(parts) == 2 else (col, col)
        cand = {x.split(".")[-1].strip("`").strip().rstrip(",;").lower() for x in (alias, expr)}
        cand.discard("")
        if cand & grouped_names:
            continue
        name = sorted(cand)[0] if cand else ""
        if not name:
            continue
        prefix = col.split(".")[0].strip("`").lower() if "." in col else ""
        if (prefix and prefix in keys) or bare_key:
            continue
        warns.append(
            f"`{name}` está en el SELECT sin estar en el GROUP BY ni dentro de una "
            "función de agregación → en MySQL con ONLY_FULL_GROUP_BY da error 1055."
        )
    return warns


def run(con, sql, label=""):
    rows = None
    for stmt in split_statements(sql):
        if not stmt.strip():
            continue
        try:
            cur = con.execute(stmt)
        except sqlite3.Error as e:
            print(f"❌ ERROR: {e}")
            print(f"   consulta: {' '.join(stmt.split())[:150]}")
            return
        for w in lint_group_by(stmt):
            print(f"⚠️  {w}")
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        con.commit()
        if label:
            print(f"-- {label}")
        title = " ".join(stmt.split())
        print(f"» {title[:100]}{'…' if len(title) > 100 else ''}")
        if cols:
            render(cols, rows)
        else:
            print("   (sentencia ejecutada, sin filas de resultado)")


def main():
    con = build(force="--reload" in sys.argv)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]

    if "--tablas" in sys.argv or args == ["--tablas"]:
        info(con)
        return

    if args and args[0] == "-f":
        run(con, open(args[1], encoding="utf-8").read())
        return

    if args:
        run(con, " ".join(args))
        return

    print("clinica_medica · modo interactivo (.help para ver los comandos)")
    buf = ""
    while True:
        try:
            line = input("sql> " if not buf else "  -> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        s = line.strip()
        if not buf and s.startswith("."):
            if s in (".quit", ".exit"):
                break
            if s == ".tablas":
                info(con)
            elif s == ".schema":
                print(to_sqlite(open(SQL_FILE, encoding="utf-8").read())[:1500])
            elif s == ".load":
                con.close()
                con = build(force=True)
                print("base recargada desde clinica_medica.sql")
            elif s == ".help":
                print(__doc__)
            else:
                print("comandos: .tablas .schema .load .help .quit")
            continue
        buf += " " + line
        if buf.count(";") and buf.rstrip().endswith(";"):
            run(con, buf)
            buf = ""


if __name__ == "__main__":
    main()
