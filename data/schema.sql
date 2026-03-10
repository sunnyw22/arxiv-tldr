-- Research Radar — SQLite Schema
-- The database (research_radar.db) is auto-created on first run.
-- This file is for reference only.

CREATE TABLE papers (
    source_id       TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    authors         TEXT NOT NULL,       -- JSON list
    abstract        TEXT NOT NULL,
    categories      TEXT NOT NULL,       -- JSON list
    primary_category TEXT NOT NULL,
    submitted_date  TEXT NOT NULL,       -- ISO 8601
    updated_date    TEXT,                -- ISO 8601 or NULL
    source_url      TEXT NOT NULL,
    pdf_url         TEXT NOT NULL,
    source_type     TEXT NOT NULL,
    raw_metadata    TEXT NOT NULL,       -- JSON blob
    first_seen      TEXT NOT NULL        -- when we first fetched this paper
);

CREATE TABLE runs (
    run_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    run_timestamp   TEXT NOT NULL,       -- ISO 8601
    total_fetched   INTEGER NOT NULL DEFAULT 0,
    total_ranked    INTEGER NOT NULL DEFAULT 0,
    config_snapshot TEXT NOT NULL        -- JSON blob of config used
);

CREATE TABLE run_papers (
    run_id            INTEGER NOT NULL,
    source_id         TEXT NOT NULL,
    relevance_score   INTEGER NOT NULL,
    reasoning         TEXT NOT NULL,
    summary           TEXT NOT NULL,
    abstract_takeaway TEXT NOT NULL DEFAULT '',
    why_relevant      TEXT NOT NULL DEFAULT '',
    PRIMARY KEY (run_id, source_id),
    FOREIGN KEY (run_id) REFERENCES runs(run_id),
    FOREIGN KEY (source_id) REFERENCES papers(source_id)
);

CREATE TABLE source_checkpoints (
    source_name     TEXT PRIMARY KEY,
    last_fetched    TEXT NOT NULL,       -- ISO 8601 timestamp
    papers_fetched  INTEGER NOT NULL DEFAULT 0
);
