# Research Radar

Personalized paper discovery and screening for researchers. Monitors arXiv and INSPIRE-HEP, ranks papers against your research profile using LLM-powered relevance scoring, and delivers evidence-backed daily digests.

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
│  (profile +  │     │ (arXiv +     │     │ (4-tier cross │     │  Keywords   │
│   sources)   │     │  INSPIRE)    │     │  source+DB)   │     │  (LLM call) │
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

1. **Fetch** — Papers are pulled from arXiv API and INSPIRE-HEP based on your configured categories and keywords.
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
```

**Fetch modes:**
- **Daily radar** (default): First run fetches the last 7 days. Subsequent runs pick up from the last checkpoint automatically.
- **Active search** (`--since`/`--until`): Fetches the specified window, ignores checkpoints, and does not update them.

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
    categories: ["hep-ex", "cs.LG"]   # arXiv categories to monitor
    max_results: 50                     # Safety cap for API fetch
  inspire:
    enabled: true
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
  model: "openai/gpt-4o-mini"   # See "API Keys" and "Cost" sections
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

Typical costs per digest run (50 papers fetched, ~15 shown):

| Model | Cost/run | Notes |
|-------|----------|-------|
| GPT-4o-mini | ~$0.001 | Default. Good quality, very cheap. |
| Gemini Flash | Free | Free tier via Google AI Studio. |
| Claude Sonnet | ~$0.15–0.20 | Best reasoning quality. |

## GitHub Actions (Automated Daily Digest)

The repo includes a GitHub Actions workflow that runs the digest automatically on weekdays.

### Schedule

- **Runs Mon–Fri at 02:00 UTC** (~1–2 hours after arXiv announcements)
- arXiv announces new papers Sun–Thu evenings at 20:00 ET (00:00–01:00 UTC next day)
- Monday's run catches Sunday evening's announcement (Thu–Fri submissions + weekend backlog)
- Each scheduled run picks up from the last checkpoint automatically (no gaps, no duplicates)

### Setup (for forks)

1. Fork the repository
2. Add `OPENAI_API_KEY` as a repository secret (Settings → Secrets and variables → Actions)
3. Edit `config/config.example.yaml` with your research interests (the workflow copies it to `config.yaml`)
4. The workflow runs automatically, or trigger manually via Actions → Daily Radar → "Run workflow"
5. Download digest reports from the workflow's Artifacts section

### Manual trigger

The workflow supports optional date filtering via the manual trigger:
- **since** — only include papers from this date (YYYY-MM-DD)
- **until** — only include papers until this date (YYYY-MM-DD)

## Mattermost Bot Integration

Research Radar can post digest summaries and attach report files to a Mattermost channel via a bot account.

### Bot Setup (Mattermost Admin)

1. **Create a bot account**: Go to **Product menu → Integrations → Bot Accounts → Add Bot Account**
2. Set username (e.g. `research-radar`), optionally add an icon
3. Select **"Post to all Mattermost channels"** permission
4. Click **Create Bot Account** and **copy the token immediately** (it's shown once and can't be retrieved later)
5. **Add the bot to your target channel**: Open the channel → channel dropdown → **Invite People → Invite Member** → search for the bot username
6. **Get the channel ID**: Open the channel → click the channel name → **View Info** → copy the ID shown at the bottom

### Research Radar Config

Add to your `config/config.yaml`:

```yaml
output:
  mattermost_url: "https://mattermost.yourorg.com"
  mattermost_channel_id: "your-channel-id-here"
```

Set the bot token as an environment variable (never in config files):

```bash
# In .env (local)
MATTERMOST_TOKEN=your-bot-token-here

# In GitHub Actions (Settings → Secrets)
# Add MATTERMOST_TOKEN as a repository secret
```

### What Gets Posted

- A compact **scored table** in the channel (title + score + one-liner per paper)
- The full **report file** (HTML or Markdown) attached to the message
- If file upload fails, the summary is posted without attachment

### Requirements

- Bot must be a **channel member** (required for file uploads)
- Bot needs `post:all` permission (no system admin required)
- `MATTERMOST_TOKEN` env var must be set — if missing, Mattermost delivery is silently skipped

## Project Structure

```
paper_radar/
  config/
    config.example.yaml   # Template — copy to config.yaml
  src/
    cli/                  # Command-line interface
    core/                 # Config, models, shared types
    sources/              # arXiv API, INSPIRE-HEP
    profiles/             # User profile schema
    ranking/              # Keyword pre-sort, LLM reranking
    summarization/        # LLM client, prompt templates
    reports/              # Markdown and HTML report generation
    storage/              # SQLite persistence and caching
    workflows/            # End-to-end pipeline orchestration
  output/                 # Generated reports (gitignored)
  output_sample/          # Example report outputs
  data/                   # SQLite database (gitignored)
  .github/workflows/
    ci.yml                # Tests + lint on push/PR
    daily_radar.yml       # Scheduled daily digest (Mon-Fri)
```
