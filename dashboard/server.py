#!/usr/bin/env python3
"""Dashboard locale delle offerte. Solo libreria standard.

Uso:
    python3 dashboard/server.py                 # usa data/jobs.sqlite, http://127.0.0.1:8765
    python3 dashboard/server.py --db data/demo.sqlite --port 8765
    python3 dashboard/server.py --avvia-pipeline  # il bottone "Prepara ora" lancia claude -p

Ascolta solo su 127.0.0.1: i dati sono personali.
"""
import argparse
import json
import mimetypes
import sqlite3
import subprocess
import sys
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse

ROOT = Path(__file__).resolve().parent.parent
HTML = Path(__file__).resolve().parent / "index.html"
SCHEMA = ROOT / "db" / "schema.sql"
APPS_DIR = ROOT / "data" / "applications"

JSON_FIELDS = ("benefit", "punti_forza", "gap")
# Transizioni che l'utente può fare dalla dashboard.
STATI_UTENTE = {"selezionata", "approvata", "valutata", "scartata", "archiviata", "inviata", "colloquio", "rifiutata"}


def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.executescript(SCHEMA.read_text(encoding="utf-8"))
    return conn


def documenti(job_id):
    d = APPS_DIR / job_id
    if not d.is_dir():
        return []
    return sorted(p.name for p in d.iterdir()
                  if p.is_file() and p.suffix.lower() in (".pdf", ".txt", ".md", ".png", ".docx"))


def row_to_dict(row):
    out = dict(row)
    for f in JSON_FIELDS:
        try:
            out[f] = json.loads(out.get(f) or "[]")
        except json.JSONDecodeError:
            out[f] = []
    out.pop("testo", None)  # testo completo non serve alla lista
    out["documenti"] = documenti(out["id"])
    return out


class Handler(BaseHTTPRequestHandler):
    db_path = None
    avvia_pipeline = False

    def log_message(self, fmt, *args):
        sys.stderr.write("[dashboard] " + fmt % args + "\n")

    def _send(self, code, body, ctype="application/json; charset=utf-8"):
        data = body if isinstance(body, bytes) else body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def _json(self, code, obj):
        self._send(code, json.dumps(obj, ensure_ascii=False))

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            return self._send(200, HTML.read_bytes(), "text/html; charset=utf-8")
        if path == "/api/jobs":
            with connect(self.db_path) as conn:
                rows = conn.execute("SELECT * FROM jobs ORDER BY match DESC NULLS LAST, data_trovata DESC").fetchall()
            return self._json(200, {"jobs": [row_to_dict(r) for r in rows],
                                    "avvia_pipeline": self.avvia_pipeline})
        if path.startswith("/files/"):
            parts = [unquote(p) for p in path.split("/")[2:]]
            if len(parts) != 2 or any(p in ("", ".", "..") or "/" in p or "\\" in p for p in parts):
                return self._json(400, {"errore": "percorso non valido"})
            f = (APPS_DIR / parts[0] / parts[1]).resolve()
            if APPS_DIR.resolve() not in f.parents or not f.is_file():
                return self._json(404, {"errore": "file non trovato"})
            ctype = mimetypes.guess_type(f.name)[0] or "application/octet-stream"
            return self._send(200, f.read_bytes(), ctype)
        return self._json(404, {"errore": "non trovato"})

    def do_POST(self):
        # Richiedere JSON impedisce a pagine di altri siti di inviare richieste "semplici" (CSRF).
        if not (self.headers.get("Content-Type") or "").startswith("application/json"):
            return self._json(415, {"errore": "serve application/json"})
        try:
            body = json.loads(self.rfile.read(int(self.headers.get("Content-Length") or 0)) or b"{}")
        except json.JSONDecodeError:
            return self._json(400, {"errore": "JSON non valido"})
        path = urlparse(self.path).path

        if path == "/api/stato":
            ids, stato = body.get("ids") or [], body.get("stato")
            if stato not in STATI_UTENTE or not isinstance(ids, list) or not ids:
                return self._json(400, {"errore": "stato o ids non validi"})
            ora = datetime.now().isoformat(timespec="seconds")
            with connect(self.db_path) as conn:
                q = ",".join("?" * len(ids))
                n = conn.execute(f"UPDATE jobs SET stato=?, nota_stato=?, aggiornato=? WHERE id IN ({q})",
                                 [stato, body.get("nota"), ora, *ids]).rowcount
            return self._json(200, {"aggiornate": n})

        if path == "/api/avvia-pipeline":
            if not self.avvia_pipeline:
                return self._json(403, {"errore": "avvio disattivato: riavvia il server con --avvia-pipeline"})
            log = (ROOT / "data" / "pipeline.log").open("a")
            subprocess.Popen(["claude", "-p", "/prepara-candidature", "--permission-mode", "acceptEdits"],
                             cwd=ROOT, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
            return self._json(202, {"avviata": True})

        return self._json(404, {"errore": "non trovato"})


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", default=str(ROOT / "data" / "jobs.sqlite"))
    ap.add_argument("--port", type=int, default=8765)
    ap.add_argument("--avvia-pipeline", action="store_true",
                    help="permette al bottone 'Prepara ora' di lanciare claude -p /prepara-candidature")
    a = ap.parse_args()
    Handler.db_path, Handler.avvia_pipeline = a.db, a.avvia_pipeline
    connect(a.db).close()
    srv = ThreadingHTTPServer(("127.0.0.1", a.port), Handler)
    print(f"Dashboard su http://127.0.0.1:{a.port}  (db: {a.db})")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
