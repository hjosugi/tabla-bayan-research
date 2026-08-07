#!/usr/bin/env python3
"""Full-text search over this repo's markdown notes.

Usage:
  python tools/notes_search.py <query>          # search (auto-reindex if stale)
  python tools/notes_search.py --rebuild        # force reindex

Uses SQLite FTS5 with the trigram tokenizer so Japanese, Hindi (Devanagari),
and Bengali queries work without word segmentation. Index lives in
tools/notes.db and is derived data (gitignored).
"""
import pathlib
import signal
import re
import sqlite3
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DB = pathlib.Path(__file__).resolve().parent / "notes.db"
GLOBS = ["README.md", "FINDINGS.md", "INDEX.md", "docs/*.md", "crawler/README.md"]


def md_files():
    for g in GLOBS:
        yield from sorted(ROOT.glob(g))


def sections(path: pathlib.Path):
    """Split a markdown file into (heading, body) chunks."""
    heading = "(top)"
    buf: list[str] = []
    for line in path.read_text().splitlines():
        m = re.match(r"^#{1,4}\s+(.*)", line)
        if m:
            if buf:
                yield heading, "\n".join(buf)
            heading, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    if buf:
        yield heading, "\n".join(buf)


def mtime_sum() -> int:
    return sum(int(p.stat().st_mtime) for p in md_files())


def build(con: sqlite3.Connection):
    con.executescript(
        "DROP TABLE IF EXISTS notes;"
        "CREATE VIRTUAL TABLE notes USING fts5(file, heading, body, tokenize='trigram');"
        "CREATE TABLE IF NOT EXISTS meta(k TEXT PRIMARY KEY, v INTEGER);"
    )
    for p in md_files():
        rel = str(p.relative_to(ROOT))
        for heading, body in sections(p):
            con.execute("INSERT INTO notes(file, heading, body) VALUES (?,?,?)",
                        (rel, heading, body))
    con.execute("INSERT OR REPLACE INTO meta VALUES ('mtime_sum', ?)", (mtime_sum(),))
    con.commit()


def ensure_index(con: sqlite3.Connection, force: bool):
    try:
        row = con.execute("SELECT v FROM meta WHERE k='mtime_sum'").fetchone()
        stale = row is None or row[0] != mtime_sum()
    except sqlite3.OperationalError:
        stale = True
    if force or stale:
        build(con)


def search(con: sqlite3.Connection, query: str):
    tokens = query.split()
    if all(len(t) >= 3 for t in tokens):
        # trigram tokenizer: quote each token; needs >= 3 chars
        q = " ".join(f'"{t}"' for t in tokens)
        rows = con.execute(
            "SELECT file, heading, snippet(notes, 2, '>>', '<<', ' ... ', 12) AS snip "
            "FROM notes WHERE notes MATCH ? ORDER BY rank LIMIT 15", (q,)).fetchall()
    else:
        # short CJK tokens (手首, 打点...) fall below trigram minimum -> LIKE scan
        cond = " AND ".join("(body LIKE ? OR heading LIKE ?)" for _ in tokens)
        params = [x for t in tokens for x in (f"%{t}%", f"%{t}%")]
        rows = [(f, h, b[max(b.find(tokens[0]) - 30, 0):b.find(tokens[0]) + 50])
                for f, h, b in con.execute(
                    f"SELECT file, heading, body FROM notes WHERE {cond} LIMIT 15",
                    params)]
    if not rows:
        print("no hits")
        return
    for f, h, s in rows:
        s = re.sub(r"\s+", " ", s).strip()
        print(f"{f} :: {h}\n    {s}\n")


def main():
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    args = sys.argv[1:]
    con = sqlite3.connect(DB)
    if args == ["--rebuild"]:
        build(con)
        n = con.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        print(f"indexed {n} sections")
        return
    if not args:
        print(__doc__)
        sys.exit(1)
    ensure_index(con, force=False)
    search(con, " ".join(args))


if __name__ == "__main__":
    main()
