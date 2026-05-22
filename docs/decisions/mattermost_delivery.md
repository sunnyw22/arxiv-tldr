# Mattermost Digest Delivery

How the daily digest is rendered and posted to Mattermost via incoming webhook
(`src/reports/mattermost.py`, orchestrated by `daily_digest._maybe_send_mattermost`).

## Message structure

The digest is posted as **multiple messages**, in order:

1. **Overview** (`format_intro_message`) — header + flavour quote + processed
   count + (optional) target profile + scoring rubric + pipeline breakdown +
   a compact `Score | Field | Paper` table. A `♻️` marker flags re-published
   rows so the overview mirrors the split below.
2. **Newly published** (`:page_facing_up:`) — detailed per-paper summaries for
   papers arXiv announced as `new` or `cross`.
3. **Re-published / v2+ updates** (`:recycle:`) — summaries for papers arXiv
   announced as `replace` / `replace-cross`.

Empty buckets produce no message (e.g. a day with no v2 updates posts only 1–2
messages).

## New vs. v2 classification

`_is_replacement(paper)`:
- **Primary signal:** arXiv RSS `arxiv_announce_type` in `raw_metadata`.
  `replace` / `replace-cross` → re-published; `new` / `cross` → newly published.
  (Cross-listings are treated as new — they are newly appearing in the feed,
  not version updates.)
- **Fallback (API mode, no announce_type):** a version suffix `> v1` in the
  `source_id`.

`announce_type` is captured by the RSS source and round-trips through SQLite
(`raw_metadata` is JSON-persisted), so reused/cached papers classify correctly.

## Field tag

`_field_tag(paper)` renders the arXiv primary category (e.g. `cs.LG`). Non-arXiv
papers (INSPIRE) fall back to the source label. Shown in both the overview table
and each summary block header.

## Truncation handling (length-safety split)

Mattermost servers enforce a server-side max post size (commonly 16383, sometimes
4000) and **silently truncate** anything over it. Previously each message was
hard-sliced at a fixed limit, which silently dropped the tail papers.

Now `format_summary_messages` measures each bucket and packs per-paper blocks
into as many messages as needed via `_pack_messages`, splitting **only at paper
boundaries** so no paper is cut mid-block. Continuation messages are marked
`(cont.)`. A single paper larger than the budget is hard-truncated as a last
resort (rare).

- Default per-message budget: `MAX_MESSAGE_LEN = 14000`.
- Override with env var **`MATTERMOST_MAX_POST_CHARS`** to match your server.

## Pipeline breakdown label

The overview shows the real ranking funnel:
`Keyword filter: N passed, M rejected · K sent to LLM · R reused from cache · F made the cut`.

`K` (`pipeline_stats["llm_candidates"]`) is the count actually sent to the LLM —
after the keyword filter **and** the top-50 candidate cap in
`daily_digest._rank_papers`. This replaced the old "LLM scored: X" figure, which
confusingly reported post-cutoff survivors rather than papers sent.
