#!/usr/bin/env python3
"""Tabla corpus search engine.

  python search/app.py --port 8765
  open http://localhost:8765/

Serves full-text search over crawler/corpus.db (FTS5 trigram) with
cross-lingual query expansion via synonyms.tsv: a query for "wrist"
also matches कलाई / কব্জি / 手首 and vice versa. No dependencies.
"""
import argparse
import html
import json
import pathlib
import re
import sqlite3
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler

HERE = pathlib.Path(__file__).resolve().parent
DB = HERE.parent / "crawler" / "corpus.db"
SYN = HERE / "synonyms.tsv"

PAGE = """<!doctype html><meta charset="utf-8">
<title>tabla corpus search</title>
<style>
 body{font-family:sans-serif;max-width:760px;margin:2rem auto;padding:0 1rem}
 input{width:70%;font-size:1.1rem;padding:.4rem}
 button{font-size:1.1rem;padding:.4rem .8rem}
 .hit{margin:1.2rem 0}.u{color:#666;font-size:.85rem;word-break:break-all}
 .lang{background:#eee;border-radius:4px;padding:0 .4rem;font-size:.8rem;margin-right:.4rem}
 mark{background:#ffe08a}
 .exp{color:#888;font-size:.85rem;margin-top:.5rem}
</style>
<h2>tabla corpus search</h2>
<form onsubmit="go();return false">
 <input id="q" placeholder="wrist / कलाई / 手首 / ঘে ..." autofocus>
 <button>search</button>
</form>
<div id="exp" class="exp"></div><div id="r"></div>
<script>
async function go(){
 const q=document.getElementById('q').value;
 const res=await fetch('/api/search?q='+encodeURIComponent(q));
 const d=await res.json();
 document.getElementById('exp').textContent=
   d.expanded.length>1?'expanded: '+d.expanded.join(', '):'';
 document.getElementById('r').innerHTML=d.hits.map(h=>
  `<div class="hit"><span class="lang">${h.lang||'?'}</span>`+
  `<a href="${h.url}">${h.title||h.url}</a>`+
  `<div>${h.snip}</div><div class="u">${h.url}</div></div>`).join('')||'no hits';
}
</script>"""


def load_synonyms():
    concept_terms: dict[str, list[str]] = {}
    term_concept: dict[str, str] = {}
    for line in SYN.read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        concept, term = line.split("\t")
        concept_terms.setdefault(concept, []).append(term)
        term_concept[term.lower()] = concept
    return concept_terms, term_concept


CONCEPT_TERMS, TERM_CONCEPT = load_synonyms()


def expand(token: str) -> list[str]:
    c = TERM_CONCEPT.get(token.lower())
    return CONCEPT_TERMS[c] if c else [token]


def run_query(q: str):
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    tokens = q.split()
    groups = [expand(t) for t in tokens]
    flat = sorted({t for g in groups for t in g})
    long_ok = all(len(t) >= 3 for g in groups for t in g)
    if long_ok:
        # (a OR b) AND (c OR d) ...; trigram needs quoted terms of >= 3 chars
        match = " AND ".join(
            "(" + " OR ".join(f'"{t}"' for t in g) + ")" for g in groups)
        sql = ("SELECT d.url, d.title, d.lang, "
               "snippet(doc_fts, 0, '<mark>', '</mark>', ' ... ', 16) AS snip, "
               "rank + (1.0 - COALESCE(s.kw_score, 0)) AS r "
               "FROM doc_fts JOIN documents d ON d.doc_id = doc_fts.rowid "
               "LEFT JOIN scores s ON s.doc_id = d.doc_id "
               "WHERE doc_fts MATCH ? AND d.dup_of IS NULL "
               "ORDER BY r LIMIT 20")
        rows = con.execute(sql, (match,)).fetchall()
    else:
        # short CJK tokens: LIKE scan per group
        cond = " AND ".join(
            "(" + " OR ".join("d.text LIKE ?" for _ in g) + ")" for g in groups)
        params = [f"%{t}%" for g in groups for t in g]
        rows = con.execute(
            f"SELECT d.url, d.title, d.lang, substr(d.text, 1, 200) AS snip, 0 AS r "
            f"FROM documents d WHERE {cond} AND d.dup_of IS NULL LIMIT 20",
            params).fetchall()
        rows = [dict(r) | {"snip": html.escape(r["snip"])} for r in rows]
    hits = [{"url": r["url"], "title": r["title"], "lang": r["lang"],
             "snip": r["snip"] if isinstance(r, dict) else r["snip"]}
            for r in rows]
    return {"expanded": flat, "hits": hits}


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        u = urllib.parse.urlsplit(self.path)
        if u.path == "/":
            body, ctype = PAGE.encode(), "text/html; charset=utf-8"
        elif u.path == "/api/search":
            q = urllib.parse.parse_qs(u.query).get("q", [""])[0]
            body = json.dumps(run_query(q), ensure_ascii=False).encode()
            ctype = "application/json; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", type=int, default=8765)
    args = ap.parse_args()
    print(f"serving http://localhost:{args.port}/ (db: {DB})")
    HTTPServer(("127.0.0.1", args.port), H).serve_forever()


if __name__ == "__main__":
    main()
