#!/usr/bin/env python3
"""Tabla corpus pipeline.

Subcommands: init | seed | fetch | extract | score | stats
Keep it boring: stdlib + requests + trafilatura + langdetect.
"""
import argparse
import hashlib
import pathlib
import re
import sqlite3
import sys
import time
import urllib.parse
import urllib.robotparser
import zlib

HERE = pathlib.Path(__file__).parent
DB = HERE / "corpus.db"
UA = "tabla-bayan-research/0.1 (personal research crawler; contact: github.com/hjosugi)"

# Keyword groups from docs/01-anatomy.md. Score = part_hits * technique_hits.
PART_TERMS = [
    "बायाँ", "डग्गा", "डगगा", "स्याही", "मैदान", "किनार", "कलाई", "मणिबंध",
    "বাঁয়া", "গাব", "ময়দান", "কিনার",
    "bayan", "baya", "duggi", "syahi", "maidan", "kinar",
]
TECH_TERMS = [
    "घे", "गे", "घिस्सा", "बोल", "आघात", "अँगुल", "उंगली", "दबाव",
    "ঘে", "গে", "আঘাত", "আঙ্গুল",
    "ghe", "ge ", "ghissa", "wrist", "pressure", "stroke", "modulation",
]


def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    return con


def canon(url: str) -> str:
    """Normalize URL: drop fragment, tracking params, trailing slash."""
    p = urllib.parse.urlsplit(url.strip())
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query)
         if not k.startswith(("utm_", "fbclid", "gclid"))]
    path = p.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit((p.scheme, p.netloc.lower(), path,
                                    urllib.parse.urlencode(q), ""))


def simhash64(text: str) -> int:
    """64-bit simhash over word 3-grams."""
    v = [0] * 64
    words = re.findall(r"\w+", text.lower())
    for i in range(max(len(words) - 2, 1)):
        h = int.from_bytes(
            hashlib.blake2b(" ".join(words[i:i + 3]).encode(), digest_size=8).digest(),
            "big")
        for b in range(64):
            v[b] += 1 if (h >> b) & 1 else -1
    return sum(1 << b for b in range(64) if v[b] > 0)


def cmd_init(_args):
    con = db()
    con.executescript((HERE / "schema.sql").read_text())
    con.commit()
    print(f"initialized {DB}")


def cmd_seed(_args):
    con = db()
    n = 0
    for line in (HERE / "seeds.txt").read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        cur = con.execute(
            "INSERT OR IGNORE INTO frontier(url, source, priority) VALUES (?, 'seed', 1)",
            (canon(line),))
        n += cur.rowcount
    con.commit()
    print(f"queued {n} seed urls")
    print("NOTE: run search queries in queries.txt through a search API "
          "and insert hits with source='search:<id>'.")


_robots_cache: dict[str, urllib.robotparser.RobotFileParser] = {}


def allowed(url: str) -> bool:
    host = urllib.parse.urlsplit(url).netloc
    if host not in _robots_cache:
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(f"https://{host}/robots.txt")
        try:
            rp.read()
        except Exception:
            rp = None  # unreachable robots.txt -> allow, be gentle
        _robots_cache[host] = rp
    rp = _robots_cache[host]
    return True if rp is None else rp.can_fetch(UA, url)


def cmd_fetch(args):
    import requests
    con = db()
    rows = con.execute(
        "SELECT url FROM frontier WHERE status='queued' ORDER BY priority LIMIT ?",
        (args.n,)).fetchall()
    last_hit: dict[str, float] = {}
    for r in rows:
        url = r["url"]
        if not allowed(url):
            con.execute("UPDATE frontier SET status='skipped' WHERE url=?", (url,))
            continue
        host = urllib.parse.urlsplit(url).netloc
        wait = 1.0 - (time.time() - last_hit.get(host, 0))
        if wait > 0:
            time.sleep(wait)  # 1 req/s per domain
        try:
            resp = requests.get(url, headers={"User-Agent": UA}, timeout=20)
            con.execute(
                "INSERT OR REPLACE INTO pages(url, http_status, content_type, html_z) "
                "VALUES (?,?,?,?)",
                (url, resp.status_code,
                 resp.headers.get("content-type", ""),
                 zlib.compress(resp.content)))
            con.execute("UPDATE frontier SET status='fetched' WHERE url=?", (url,))
        except Exception as e:
            print(f"fail {url}: {e}", file=sys.stderr)
            con.execute("UPDATE frontier SET status='failed' WHERE url=?", (url,))
        last_hit[host] = time.time()
        con.commit()
    print("fetch done")


def cmd_extract(_args):
    import trafilatura
    from langdetect import detect
    con = db()
    rows = con.execute(
        "SELECT p.url, p.html_z FROM pages p "
        "LEFT JOIN documents d ON d.url = p.url WHERE d.url IS NULL "
        "AND p.http_status = 200").fetchall()
    for r in rows:
        html = zlib.decompress(r["html_z"]).decode("utf-8", "replace")
        text = trafilatura.extract(html) or ""
        if len(text) < 200:  # boilerplate-only pages
            continue
        meta = trafilatura.extract_metadata(html)
        title = meta.title if meta else None
        try:
            lang = detect(text)
        except Exception:
            lang = None
        con.execute(
            "INSERT OR IGNORE INTO documents(url, title, lang, text, simhash) "
            "VALUES (?,?,?,?,?)",
            (r["url"], title, lang, text, simhash64(text) - (1 << 63)))
    con.commit()
    # near-dup marking: O(n^2) is fine below ~50k docs; switch to LSH buckets after
    docs = con.execute(
        "SELECT doc_id, simhash FROM documents WHERE dup_of IS NULL "
        "ORDER BY doc_id").fetchall()
    for i, a in enumerate(docs):
        for b in docs[i + 1:]:
            if bin((a["simhash"] ^ b["simhash"]) & ((1 << 64) - 1)).count("1") <= 3:
                con.execute("UPDATE documents SET dup_of=? WHERE doc_id=?",
                            (a["doc_id"], b["doc_id"]))
    con.commit()
    print("extract done")


def cmd_score(_args):
    con = db()
    for r in con.execute("SELECT doc_id, text FROM documents WHERE dup_of IS NULL"):
        t = r["text"].lower()
        parts = sum(t.count(w.lower()) for w in PART_TERMS)
        tech = sum(t.count(w.lower()) for w in TECH_TERMS)
        score = (min(parts, 20) * min(tech, 20)) / 400.0
        con.execute(
            "INSERT INTO scores(doc_id, kw_score) VALUES (?,?) "
            "ON CONFLICT(doc_id) DO UPDATE SET kw_score=excluded.kw_score",
            (r["doc_id"], score))
    con.commit()
    print("score done; top docs:")
    for r in con.execute(
            "SELECT s.kw_score, d.lang, d.url FROM scores s "
            "JOIN documents d USING(doc_id) ORDER BY s.kw_score DESC LIMIT 10"):
        print(f"  {r['kw_score']:.2f} [{r['lang']}] {r['url']}")


def cmd_stats(_args):
    con = db()
    for r in con.execute("SELECT status, COUNT(*) c FROM frontier GROUP BY status"):
        print(f"frontier {r['status']}: {r['c']}")
    for r in con.execute("SELECT lang, COUNT(*) c FROM documents GROUP BY lang "
                         "ORDER BY c DESC"):
        print(f"docs [{r['lang']}]: {r['c']}")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    sub.add_parser("seed")
    f = sub.add_parser("fetch")
    f.add_argument("-n", type=int, default=50)
    sub.add_parser("extract")
    sub.add_parser("score")
    sub.add_parser("stats")
    args = ap.parse_args()
    {"init": cmd_init, "seed": cmd_seed, "fetch": cmd_fetch,
     "extract": cmd_extract, "score": cmd_score, "stats": cmd_stats}[args.cmd](args)


if __name__ == "__main__":
    main()
