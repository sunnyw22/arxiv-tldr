# Research Radar

Personalized paper discovery and screening for researchers. Monitors arXiv (API + RSS) and INSPIRE-HEP, ranks papers against your research profile using LLM-powered relevance scoring, and delivers evidence-backed daily digests — locally or via GitHub Actions with optional Mattermost notifications.

## Quick Start

```bash
# 1. Clone and install
git clone https://github.com/sunnyw22/paper_radar.git
cd paper_radar
python -m venv .venv
source .venv/bin/activate
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

## How It Works

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

1. **Fetch** — Papers are pulled from arXiv (RSS for CI/today-only, API for local with date filtering) and optionally INSPIRE-HEP. `max_results` auto-scales by category count (categories × 50).
2. **Deduplicate** — 4-tier dedup: arXiv ID → DOI → source ID → normalized title+first author+year. Also deduplicates against previously seen papers in the local SQLite database.
3. **Expand keywords** — An LLM call expands your topic interests into related terms (synonyms, abbreviations, adjacent concepts).
4. **Pre-sort** — Expanded keywords are matched against titles and abstracts to select the top candidates. This keeps LLM costs low by filtering before the expensive ranking step.
5. **LLM rank + summarize** — Candidates are sent to the LLM in batches. Each paper receives a relevance score (1-10), an evidence-grounded summary ("From the paper"), and a personalized assessment ("Model Name - Assessment").
6. **Generate reports** — Timestamped Markdown and HTML reports include your profile, pipeline stats, keyword expansion details, scoring rubric, and ranked papers with links.
7. **Cache** — All papers and scores are saved to SQLite. Subsequent runs reuse previous scores, saving LLM costs. Changing your profile triggers re-ranking.

## Output

Reports are saved to `output/` with timestamped filenames including the model used:

```
output/digest_gpt-4o-mini_2026-03-08_1019.md
output/digest_gpt-4o-mini_2026-03-08_1019.html
```

Each report includes:
- **Digest window** — how many papers were fetched and from which date range
- **User profile** — your topic interests, negative filters, project context, expertise level
- **Keyword expansion** — original interests → expanded search terms
- **Pipeline stats** — per-source fetch counts, dedup results, keyword filter pass/reject, LLM scored count
- **Scoring rubric** — what each score range (1-10) means
- **Ranked papers** — each with:
  - Title, relevance score, source tag (arXiv/INSPIRE), authors, date, categories
  - Collapsible abstract
  - "From the paper" — factual summary grounded in the abstract (problem, technique, results)
  - "Model Name - Assessment" — why this paper matters to your specific research
  - Links to paper and PDF
- **All fetched papers** — collapsible list of every paper retrieved, with links (zero LLM cost). Ranked papers are tagged.

See `output_sample/` for example reports.

## CLI Usage

### `digest` — Run a daily digest

```bash
# Run a digest (daily radar mode — uses checkpoint, defaults to last 7 days)
python -m src.cli digest

# Active search mode — fetch a specific date range (ignores checkpoint)
python -m src.cli digest --since 2026-03-01 --until 2026-03-07

# Custom config and database paths
python -m src.cli digest --config path/to/config.yaml --db path/to/database.db

# Skip LLM-based config validation (faster startup)
python -m src.cli digest --skip-validation

# Non-interactive mode (skip keyword review — use for CI/headless runs)
python -m src.cli digest --no-interactive

# Use arXiv RSS feed (today's announcements only — ideal for CI)
python -m src.cli digest --use-rss --no-interactive
```

**Fetch modes:**
- **Daily radar** (default): First run fetches the last 7 days. Subsequent runs pick up from the last checkpoint automatically.
- **Active search** (`--since`/`--until`): Fetches the specified window, ignores checkpoints, and does not update them.
- **RSS mode** (`--use-rss`): Fetches only today's arXiv announcements via RSS. No date filtering or checkpoints needed. Used in the GitHub Actions workflow.

### `setup` — Interactive config wizard

```bash
# Generate a config via LLM-assisted interview
python -m src.cli setup

# Custom output path and model
python -m src.cli setup --config config/my_config.yaml --model openai/gpt-4o-mini
```

### `purge` — Clean old data from the database

```bash
# Preview what would be deleted
python -m src.cli purge --older-than 90d --dry-run

# Delete old runs and orphaned papers
python -m src.cli purge --older-than 90d

# Supports days (d), months (m), years (y)
python -m src.cli purge --older-than 6m --db path/to/database.db
```

## Configuration

Copy `config/config.example.yaml` to `config/config.yaml` and customize:

```yaml
# Your research profile (what you care about)
profile:
  topic_interests:
    - "machine learning"
    - "particle tracking"
    - "graph neural networks"
  required_signals:            # Must-have keywords — boost relevance
    - "ATLAS"
    - "GNN"
  negative_filters:            # Papers matching these are deprioritized
    - "survey only"
    - "review article"
  project_context: >           # Your current research focus (helps LLM rank better)
    Applying machine learning methods, especially graph neural networks,
    to charged particle tracking and detector reconstruction in ATLAS.
  expertise_level: "advanced"  # beginner | intermediate | advanced | expert

# Where to look for papers
sources:
  arxiv:
    enabled: true
    categories: ["hep-ex", "hep-ph", "cs.LG", "cs.AI", "physics.data-an"]
    max_results: 50            # Auto-scales: categories × 50 when default
  inspire:
    enabled: false             # Most papers already on arXiv
    keywords: ["tracking", "machine learning"]
    subject_codes: ["Experiment-HEP"]
    max_results: 50

# Output settings
summary:
  style: "concise"           # concise | detailed | technical
  max_papers: 15             # Max papers in digest (ties at cutoff included)
  min_score: 4               # Minimum relevance score to include (1-10)

output:
  formats: ["markdown", "html"]
  output_dir: "output/"

# LLM provider (any litellm-supported model)
llm:
  model: "openai/gpt-5.4"     # See "API Keys" and "Cost" sections
  temperature: 0.3
  max_tokens: 4096
```

## API Keys

Research Radar uses an LLM for keyword expansion, ranking, and summarization. Set your API key in `.env`:

### OpenAI (default)

1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Set `OPENAI_API_KEY` in `.env`
3. Config: `model: "openai/gpt-4o-mini"`

### Google Gemini (free tier)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) (no billing required)
2. Create an API key
3. Set `GEMINI_API_KEY` in `.env`
4. Config: `model: "gemini/gemini-2.0-flash"`

### Anthropic

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Add credits and create an API key
3. Set `ANTHROPIC_API_KEY` in `.env`
4. Config: `model: "anthropic/claude-sonnet-4-20250514"`

### Other providers

Research Radar uses [litellm](https://docs.litellm.ai/) for LLM abstraction. Any litellm-supported provider works — set the model name in config and the corresponding API key in `.env`.

## Cost

Typical costs per digest run (~250 papers fetched via 5 categories, ~15 shown):

| Model | Cost/run | Notes |
|-------|----------|-------|
| GPT-5.4 | ~$0.01–0.02 | Default. Best quality-to-cost ratio. |
| GPT-4o-mini | ~$0.001 | Budget option, good quality. |
| Gemini Flash | Free | Free tier via Google AI Studio. |
| Claude Sonnet | ~$0.15–0.20 | Strong reasoning quality. |

## GitHub Actions (Automated Daily Digest)

The repo includes a GitHub Actions workflow that runs the digest automatically on weekdays.

### Schedule

- **Runs Mon–Fri at 02:00 UTC** (~1–2 hours after arXiv announcements)
- arXiv announces new papers Sun–Thu evenings at 20:00 ET (00:00–01:00 UTC next day)
- Monday's run catches Sunday evening's announcement (Thu–Fri submissions + weekend backlog)
- Uses `--use-rss` to fetch only today's announcements (no checkpoints needed in CI)

### Setup (for forks)

1. Fork the repository
2. Add repository secrets (Settings → Secrets and variables → Actions):
   - `OPENAI_API_KEY` — required
   - `MATTERMOST_WEBHOOK_URL` — optional, for channel notifications
3. Edit `config/config.example.yaml` with your research interests (the workflow copies it to `config.yaml`)
4. The workflow runs automatically, or trigger manually via Actions → Daily Radar → "Run workflow"
5. Download digest reports from the workflow's Artifacts section (always uploaded, regardless of Mattermost)

### Manual trigger

The workflow supports optional date filtering via the manual trigger:
- **since** — only include papers from this date (YYYY-MM-DD)
- **until** — only include papers until this date (YYYY-MM-DD)

## Mattermost Integration

Research Radar can post digest summaries to a Mattermost channel via an incoming webhook.

### Webhook Setup

1. Go to **Product menu → Integrations → Incoming Webhooks → Add Incoming Webhook**
2. Pick the target channel and set a display name (e.g. `Research Radar`)
3. Click **Save** and **copy the webhook URL** — this is your only secret

### Configuration

Set the webhook URL as an environment variable (never in config files or logs):

```bash
# In .env (local)
MATTERMOST_WEBHOOK_URL=https://mattermost.yourorg.com/hooks/xxxxxxxxxxxxx

# In GitHub Actions (Settings → Secrets → Actions)
# Add MATTERMOST_WEBHOOK_URL as a repository secret
```

No config file changes needed — the webhook URL encodes the channel.

### What Gets Posted

Two messages are sent per digest:

1. **Intro message** — LLM-generated quote (Skynet/HAL-9000 personality), your profile summary, scoring rubric
2. **Report message** — Pipeline stats, scored paper table with one-line takeaways and arXiv links

The bot name is derived from the LLM model (e.g., "T-Gpt-5.4").

### Security

- The webhook URL is the only secret — it grants posting access to one channel
- Never commit it to config, logs, or code — use env vars only
- If `MATTERMOST_WEBHOOK_URL` is not set, Mattermost delivery is silently skipped

## Project Structure

```
paper_radar/
  config/
    config.example.yaml   # Template — copy to config.yaml
  src/
    cli/                  # Command-line interface
    core/                 # Config, models, shared types
    sources/              # arXiv API, arXiv RSS, INSPIRE-HEP
    profiles/             # User profile schema
    ranking/              # Keyword pre-sort, LLM reranking
    summarization/        # LLM client, prompt templates
    reports/              # Markdown, HTML, Mattermost webhook
    storage/              # SQLite persistence and caching
    workflows/            # End-to-end pipeline orchestration
  output/                 # Generated reports (gitignored)
  output_sample/          # Example report outputs
  data/
    schema.sql            # SQLite schema reference
  .github/workflows/
    ci.yml                # Tests + lint on push/PR
    daily_radar.yml       # Scheduled daily digest (Mon-Fri, RSS + Mattermost)
```
