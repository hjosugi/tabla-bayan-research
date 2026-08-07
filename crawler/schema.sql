-- Corpus DB schema. SQLite 3.35+ (FTS5 enabled).

PRAGMA journal_mode = WAL;

CREATE TABLE IF NOT EXISTS frontier (
  url          TEXT PRIMARY KEY,          -- canonicalized URL
  source       TEXT NOT NULL,             -- 'seed' | 'search:<query_id>' | 'link:<parent_url>'
  priority     INTEGER NOT NULL DEFAULT 5,-- 1 = highest
  status       TEXT NOT NULL DEFAULT 'queued', -- queued | fetched | failed | skipped
  discovered_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS pages (
  url          TEXT PRIMARY KEY,
  http_status  INTEGER,
  content_type TEXT,
  html_z       BLOB,                      -- zlib-compressed raw body; keep for re-extraction
  fetched_at   TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS documents (
  doc_id       INTEGER PRIMARY KEY,
  url          TEXT NOT NULL UNIQUE,
  title        TEXT,
  lang         TEXT,                      -- 'hi' | 'bn' | 'en' | ...
  text         TEXT NOT NULL,
  simhash      INTEGER,                   -- 64-bit; near-dup if hamming <= 3
  dup_of       INTEGER REFERENCES documents(doc_id),
  extracted_at TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS scores (
  doc_id        INTEGER PRIMARY KEY REFERENCES documents(doc_id),
  kw_score      REAL,                     -- co-occurrence keyword score
  llm_relevance REAL,                     -- 0..1, second-pass only
  llm_summary   TEXT
);

-- One row per extracted claim about playing technique.
-- topic: wrist_position | finger_angle | strike_point | pressure | finger_choice | damping | tuning | other
-- stance: free text normalized later, e.g. 'maidan', 'kinar', 'syahi-edge'
CREATE TABLE IF NOT EXISTS claims (
  claim_id   INTEGER PRIMARY KEY,
  doc_id     INTEGER NOT NULL REFERENCES documents(doc_id),
  topic      TEXT NOT NULL,
  stance     TEXT NOT NULL,
  quote      TEXT,                        -- short original-language snippet, <= 25 words
  confidence REAL
);

-- Full-text search. trigram handles unsegmented Devanagari/Bengali better than unicode61.
CREATE VIRTUAL TABLE IF NOT EXISTS doc_fts USING fts5(
  text, title,
  content='documents', content_rowid='doc_id',
  tokenize='trigram'
);

CREATE TRIGGER IF NOT EXISTS documents_ai AFTER INSERT ON documents BEGIN
  INSERT INTO doc_fts(rowid, text, title) VALUES (new.doc_id, new.text, new.title);
END;

CREATE INDEX IF NOT EXISTS idx_frontier_status ON frontier(status, priority);
CREATE INDEX IF NOT EXISTS idx_documents_lang ON documents(lang);
CREATE INDEX IF NOT EXISTS idx_claims_topic ON claims(topic, stance);
