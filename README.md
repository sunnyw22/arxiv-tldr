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

```bash
# Run a digest with default settings
python -m src.cli digest

# Custom config file
python -m src.cli digest --config path/to/config.yaml

# Custom database path
python -m src.cli digest --db path/to/database.db

# Filter by date range
python -m src.cli digest --since 2026-03-01 --until 2026-03-07

# Skip LLM-based config validation (faster startup)
python -m src.cli digest --skip-validation
```

## Configuration

Copy `config/config.example.yaml` to `config/config.yaml` and customize:

```yaml
# Your research profile (what you care about)
profile:
  topic_interests:
    - "large language models"
    - "retrieval-augmented generation"
  required_signals:          # Keywords that boost relevance
    - "benchmark"
    - "evaluation"
  negative_filters:          # Keywords that reject papers
    - "survey only"
    - "workshop abstract"
  project_context: >         # Your current research focus (helps LLM rank better)
    I am studying how retrieval-augmented generation can improve
    factual accuracy in domain-specific question answering.
  expertise_level: "advanced"  # beginner | intermediate | advanced | expert

# Where to look for papers
sources:
  arxiv:
    enabled: true
    categories: ["cs.LG", "cs.CL"]    # arXiv categories to monitor
    max_results: 50                     # Max papers to fetch per run
  inspire:
    enabled: true
    keywords: ["machine learning"]      # INSPIRE keyword search
    subject_codes: ["Experiment-HEP"]   # INSPIRE subject filter
    max_results: 50

# Output settings
summary:
  max_papers: 15             # Max papers in digest (ties at cutoff included)

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
- Monday also picks up weekend INSPIRE papers via the "most recent N" fetch

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
