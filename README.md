# 📡 arXiv TL;DR

### 🤖 *We read all the papers so you don't have to.*

**Your personalized daily arXiv digest — filtered, ranked, and summarized by AI.**

Stop drowning in preprints. arXiv TL;DR monitors arXiv (and optionally INSPIRE-HEP), scores every paper against your research profile, and delivers a concise daily digest of what actually matters to you. Run it locally, automate it with GitHub Actions, or get notifications in Mattermost.

> 🔬 **Customizable** — define your interests, expertise, and project context in a simple YAML config.
> 🤖 **LLM-powered** — keyword expansion, relevance scoring (1–10), evidence-grounded summaries.
> 📰 **Daily or on-demand** — RSS mode for today's announcements, API mode for date-range searches.
> 💰 **Cost-efficient** — keyword pre-filtering keeps LLM usage low (~30k tokens/run).

---

## 🚀 Quick Start

```bash
# 1. Clone and install
git clone https://github.com/sunnyw22/arxiv-tldr.git
cd arxiv-tldr
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Set up your API key
cp .env.example .env
# Edit .env and add your key (see "API Keys" below)

# 3. Create your config
cp config/config.example.yaml config/config.yaml
# Edit config/config.yaml with your research interests

# 4. Run your first digest
python -m src.cli digest
```

Reports are saved to `output/` as both Markdown and HTML.

---

## ⚙️ How It Works

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Your Config │────▶│ Fetch Papers │────▶│  Deduplicate  │────▶│  Expand     │
│  (profile +  │     │ (arXiv RSS/  │     │ (4-tier cross │     │  Keywords   │
│   sources)   │     │  API+INSPIRE)│     │  source+DB)   │     │  (LLM call) │
└─────────────┘     └─────────────┘     └──────────────┘     └──────┬──────┘
                                                                     │
                    ┌─────────────┐     ┌──────────────┐     ┌──────▼──────┐
                    │  Generate    │◀────│  LLM Rank +   │◀────│  Pre-sort   │
                    │  Reports     │     │  Summarize    │     │  (keyword   │
                    │  (MD + HTML) │     │  (score 1-10) │     │   matching) │
                    └──────┬──────┘     └──────────────┘     └─────────────┘
                           │
                    ┌──────▼──────┐
                    │  Save to DB  │
                    │  (cache for  │
                    │  next run)   │
                    └─────────────┘
```

1. **Fetch** — Pull papers from arXiv (RSS for today's announcements, API for date-range searches) and optionally INSPIRE-HEP. `max_results` auto-scales by category count.
2. **Deduplicate** — 4-tier dedup: arXiv ID → DOI → source ID → normalized title+author+year. Also deduplicates against the local SQLite cache.
3. **Expand keywords** — LLM expands your topic interests into related terms (synonyms, abbreviations, adjacent concepts).
4. **Pre-sort** — Expanded keywords are matched against titles and abstracts to select the top candidates, keeping LLM costs low.
5. **LLM rank + summarize** — Candidates are scored 1–10 with evidence-grounded summaries ("From the paper") and personalized assessments ("Model Name - Assessment").
6. **Generate reports** — Timestamped Markdown and HTML reports with your profile, pipeline stats, scoring rubric, and ranked papers with links.
7. **Cache** — All papers and scores are saved to SQLite. Subsequent runs reuse scores for unchanged profiles.

---

## 📄 Output

Reports are saved to `output/` with timestamped filenames:

```
output/digest_gpt-5.4_2026-03-12_0830.md
output/digest_gpt-5.4_2026-03-12_0830.html
```

Each report includes:
- **Digest window** — date range or "today's arXiv announcements"
- **User profile** — your interests, filters, project context, expertise level
- **Keyword expansion** — original interests → expanded search terms
- **Pipeline stats** — per-source fetch counts, dedup, keyword filter, LLM scored
- **Scoring rubric** — what each score range means
- **Ranked papers** — title, score, authors, abstract, evidence-grounded summary, assessment, links
- **All fetched papers** — collapsible list of every paper retrieved (zero LLM cost)

See `output_sample/` for example reports.

---

## 🖥️ CLI Usage

### `digest` — Run a daily digest

```bash
# Daily radar (default — uses checkpoint, first run fetches last 7 days)
python -m src.cli digest

# RSS mode — today's arXiv announcements only (ideal for CI)
python -m src.cli digest --use-rss --no-interactive

# Active search — specific date range (ignores checkpoint)
python -m src.cli digest --since 2026-03-01 --until 2026-03-07

# Custom config and database paths
python -m src.cli digest --config path/to/config.yaml --db path/to/database.db

# Skip LLM-based config validation (faster startup)
python -m src.cli digest --skip-validation
```

**Fetch modes:**
| Mode | Description |
|------|-------------|
| **Daily radar** (default) | First run: last 7 days. Then picks up from checkpoint. |
| **RSS mode** (`--use-rss`) | Today's arXiv announcements only. No checkpoints. |
| **Active search** (`--since`/`--until`) | Specific window. No checkpoint update. |

### `setup` — Interactive config wizard

```bash
python -m src.cli setup
python -m src.cli setup --config config/my_config.yaml --model openai/gpt-4o-mini
```

### `purge` — Clean old data

```bash
python -m src.cli purge --older-than 90d --dry-run   # Preview
python -m src.cli purge --older-than 90d              # Delete
python -m src.cli purge --older-than 6m               # Supports d/m/y
```

---

## 🔧 Configuration

Copy `config/config.example.yaml` to `config/config.yaml` and customize:

```yaml
profile:
  topic_interests:
    - "machine learning"
    - "particle tracking"
    - "graph neural networks"
  required_signals: ["ATLAS", "GNN"]         # Boost relevance
  negative_filters: ["survey only"]          # Deprioritize
  project_context: >
    Applying GNNs to charged particle tracking in ATLAS.
  expertise_level: "advanced"                # beginner | intermediate | advanced | expert

sources:
  arxiv:
    enabled: true
    categories: ["hep-ex", "cs.LG", "cs.AI"]
    max_results: 50                          # Auto-scales: categories × 50
  inspire:
    enabled: false

summary:
  max_papers: 10                             # Max papers in digest
  min_score: 4                               # Minimum relevance score (1-10)

llm:
  model: "openai/gpt-5.4"                   # Any litellm-supported model
  temperature: 0.3
  max_tokens: 4096
```

---

## 🔑 API Keys

Set your API key in `.env`. Research Radar uses [litellm](https://docs.litellm.ai/) — any supported provider works.

| Provider | Env var | Example model | Setup |
|----------|---------|---------------|-------|
| **OpenAI** | `OPENAI_API_KEY` | `openai/gpt-5.4` | [platform.openai.com](https://platform.openai.com) |
| **Google Gemini** | `GEMINI_API_KEY` | `gemini/gemini-2.0-flash` | [aistudio.google.com](https://aistudio.google.com/apikey) (free tier) |
| **Anthropic** | `ANTHROPIC_API_KEY` | `anthropic/claude-sonnet-4-20250514` | [console.anthropic.com](https://console.anthropic.com) |

---

## 💰 Token Usage

A typical run (5 arXiv categories, ~250 papers fetched, ~10 shown) uses approximately:

| Metric | Typical value |
|--------|---------------|
| LLM calls | ~6 |
| Prompt tokens | ~20,000 |
| Completion tokens | ~13,000 |
| **Total tokens** | **~33,000** |

Actual cost depends on your LLM provider's pricing. The keyword pre-filter ensures only relevant candidates reach the LLM, keeping token usage low regardless of how many papers are fetched.

---

## 🤖 GitHub Actions (Automated Daily Digest)

The repo includes a workflow that runs the digest automatically on weekdays.

### Schedule

- **Runs Mon–Fri at 02:00 UTC** (~1–2 hours after arXiv announcements)
- Uses `--use-rss` to fetch only today's announcements
- Reports are uploaded as workflow artifacts

### Setup (for forks)

1. Fork the repository
2. Add repository secrets (Settings → Secrets → Actions):
   - `OPENAI_API_KEY` — required
   - `MATTERMOST_WEBHOOK_URL` — optional, for channel notifications
3. Edit `config/config.example.yaml` with your research interests (the workflow copies it to `config.yaml`)
4. The workflow runs automatically, or trigger manually via Actions → Daily Radar → "Run workflow"

The manual trigger supports optional `--since` / `--until` date filtering.

---

## 💬 Mattermost Integration

Post digest summaries to a Mattermost channel via incoming webhook.

### Setup

1. In Mattermost: **Product menu → Integrations → Incoming Webhooks → Add**
2. Set the webhook URL as an env var (never in config/logs):

```bash
# .env (local)
MATTERMOST_WEBHOOK_URL=https://mattermost.yourorg.com/hooks/xxxxxxxxxxxxx

# GitHub Actions: add as a repository secret
```

### What gets posted

Two messages per digest:
1. **Intro** — LLM-generated quote of the day, your profile summary, scoring rubric
2. **Report** — Pipeline stats, scored paper table with one-line takeaways and arXiv links

Bot name is derived from the LLM model (e.g., "T-Gpt-5.4"). If `MATTERMOST_WEBHOOK_URL` is not set, delivery is silently skipped.

---

## 📁 Project Structure

```
arxiv-tldr/
  config/
    config.example.yaml     # Template — copy to config.yaml
  src/
    cli/                    # CLI interface + setup wizard
    core/                   # Config, models, shared types
    sources/                # arXiv API, arXiv RSS, INSPIRE-HEP
    profiles/               # User profile schema
    ranking/                # Keyword pre-sort, LLM reranking
    summarization/          # LLM client, prompt templates
    reports/                # Markdown, HTML, Mattermost webhook
    storage/                # SQLite persistence and caching
    workflows/              # End-to-end pipeline orchestration
  output/                   # Generated reports (gitignored)
  output_sample/            # Example report outputs
  data/
    schema.sql              # SQLite schema reference
  .github/workflows/
    ci.yml                  # Tests + lint on push/PR
    daily_radar.yml         # Scheduled daily digest
```
