#!/usr/bin/env python3
"""Servidor estático mínimo con soporte de Range (206) para poder seekear video/audio.

Uso: python3 scripts/serve.py [puerto]
"""
import os
import posixpath
import re
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

TYPES = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "application/javascript; charset=utf-8",
    ".json": "application/json; charset=utf-8",
    ".md": "text/plain; charset=utf-8",
    ".srt": "text/plain; charset=utf-8",
    ".sql": "text/plain; charset=utf-8",
    ".txt": "text/plain; charset=utf-8",
    ".pdf": "application/pdf",
    ".mp4": "video/mp4",
    ".webm": "video/webm",
    ".mp3": "audio/mpeg",
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".svg": "image/svg+xml",
}

RANGE_RE = re.compile(r"bytes=(\d*)-(\d*)")


class Handler(BaseHTTPRequestHandler):
    server_version = "StudyServer/1.0"

    def _resolve(self):
        path = unquote(urlparse(self.path).path)
        path = posixpath.normpath(path)
        if path in ("/", ""):
            path = "/index.html"
        if path.startswith("/..") or "/../" in path:
            return None
        full = os.path.join(ROOT, path.lstrip("/"))
        if os.path.isdir(full):
            full = os.path.join(full, "index.html")
        return full if os.path.isfile(full) else None

    def _common_headers(self):
        self.send_header("Accept-Ranges", "bytes")
        self.send_header("Cache-Control", "no-cache")
        # permite embeber en el iframe del preview
        self.send_header("X-Frame-Options", "ALLOWALL")
        self.send_header("Access-Control-Allow-Origin", "*")

    def do_HEAD(self):
        self._serve(head_only=True)

    def do_GET(self):
        self._serve(head_only=False)

    def _serve(self, head_only=False):
        full = self._resolve()
        if not full:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            if not head_only:
                self.wfile.write(b"404 - no encontrado")
            return

        size = os.path.getsize(full)
        ctype = TYPES.get(os.path.splitext(full)[1].lower(), "application/octet-stream")
        start, end = 0, size - 1
        status = 200

        rng = self.headers.get("Range")
        if rng:
            m = RANGE_RE.match(rng.strip())
            if m:
                a, b = m.group(1), m.group(2)
                if a:
                    start = int(a)
                    end = int(b) if b else size - 1
                elif b:  # sufijo: últimos N bytes
                    start = max(size - int(b), 0)
                if start > end or start >= size:
                    self.send_response(416)
                    self.send_header("Content-Range", f"bytes */{size}")
                    self.end_headers()
                    return
                end = min(end, size - 1)
                status = 206

        length = end - start + 1
        self.send_response(status)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(length))
        if status == 206:
            self.send_header("Content-Range", f"bytes {start}-{end}/{size}")
        self._common_headers()
        self.end_headers()

        if head_only:
            return

        chunk = 64 * 1024
        with open(full, "rb") as f:
            f.seek(start)
            remaining = length
            while remaining > 0:
                data = f.read(min(chunk, remaining))
                if not data:
                    break
                try:
                    self.wfile.write(data)
                except (BrokenPipeError, ConnectionResetError):
                    return
                remaining -= len(data)

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    os.chdir(ROOT)
    srv = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"sirviendo {ROOT} en http://0.0.0.0:{PORT}", flush=True)
    srv.serve_forever()
