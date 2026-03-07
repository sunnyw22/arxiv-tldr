# Research Radar

Personalized paper discovery and screening for researchers. Monitors arXiv and INSPIRE-HEP, ranks papers against your research profile using LLM-powered relevance scoring, and delivers evidence-backed summaries.

## Quick Start

```bash
# 1. Clone and set up Python environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2. Set up your API key (see "API Key Setup" below)
cp .env.example .env
# Edit .env and add your key

# 3. Create your config
cp config/config.example.yaml config/config.yaml
# Edit config/config.yaml with your research interests

# 4. Run your first digest
python -m src.cli digest
```

## What It Does

Research Radar runs an automated pipeline that turns your research profile into a personalized paper digest:

```
┌─────────────┐     ┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│  Your Config │────▶│ Fetch Papers │────▶│  Deduplicate  │────▶│  Expand     │
│  (profile +  │     │ (arXiv +     │     │ (cross-source │     │  Keywords   │
│   sources)   │     │  INSPIRE)    │     │   + vs DB)    │     │  (LLM call) │
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

**Step by step:**

1. **Configure** — You define your research interests, expertise level, and project context in a YAML file. You also specify which arXiv categories and INSPIRE keywords to search.
2. **Fetch** — Papers are pulled from arXiv API and INSPIRE-HEP based on your source settings.
3. **Deduplicate** — Papers are deduplicated across sources (arXiv ID matching, cross-references) and against previously seen papers in the local database.
4. **Expand keywords** — An LLM call expands your topic interests into ~40 related terms (synonyms, abbreviations, adjacent concepts like "GNN" → "graph neural network", "message passing").
5. **Pre-sort** — Expanded keywords are matched against paper titles and abstracts to select the top ~50 candidates. This keeps LLM costs low by filtering before the expensive step.
6. **LLM rank + summarize** — Candidates are sent to the LLM in batches. Each paper receives a relevance score (1-10) with a concrete rubric, a "why this matters" explanation, and a concise summary.
7. **Generate reports** — Timestamped Markdown and HTML reports are generated with search metadata, scoring rubric, and ranked papers with links.
8. **Cache** — All papers and scores are saved to a local SQLite database. Subsequent runs with the same profile reuse previous scores, saving LLM costs. If you change your profile, everything is re-ranked from scratch.

## Output

Reports are saved to `output/` with timestamped filenames that include the model used:

```
output/digest_claude-sonnet-4_2026-03-07_1517.md
output/digest_claude-sonnet-4_2026-03-07_1517.html
output/digest_gpt-4o-mini_2026-03-07_1520.md
```

Each report includes:
- **Search summary** — date range, sources searched, categories, total papers fetched
- **Your profile** — topic interests, research context, expertise level
- **Scoring rubric** — what each score range means
- **Ranked papers** — title, score, authors, publication date, "why this matters", summary, and links
- **Cost report** — LLM token usage and estimated cost
See `output_sample` for example.

## Usage

```bash
# Run a digest with default config
python -m src.cli digest

# Use a custom config file
python -m src.cli digest --config path/to/config.yaml

# Use a custom database path
python -m src.cli digest --db path/to/database.db
```

## Configuration

Copy `config/config.example.yaml` to `config/config.yaml` and customize:

```yaml
profile:
  topic_interests:        # What you care about
    - "machine learning"
    - "particle physics"
  project_context: >      # Your current research focus (helps LLM rank better)
    Implementing ML to reconstruct particles from detector signals.
  expertise_level: "advanced"   # beginner, intermediate, advanced, expert

sources:
  arxiv:
    categories: ["hep-ex", "cs.LG"]    # arXiv categories to monitor
  inspire:
    keywords: ["tracking", "machine learning"]  # INSPIRE keyword search
    subject_codes: ["Experiment-HEP"]           # INSPIRE subject filter

summary:
  max_papers: 10          # Max papers in digest (ties at cutoff are included)

output:
  formats: ["markdown", "html"]
  output_dir: "output/"

llm:
  model: "anthropic/claude-sonnet-4-20250514"  # Any litellm-supported model
  temperature: 0.3
  max_tokens: 4096
```

## API Key Setup

Research Radar uses an LLM for ranking and summarization. Set your key in `.env`:

### Option 1: Anthropic (default)

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Add credits under Plans & Billing
3. Create an API key
4. Set `ANTHROPIC_API_KEY` in `.env`

### Option 2: OpenAI

1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Set `OPENAI_API_KEY` in `.env`
3. Update `llm.model` in config (e.g., `openai/gpt-4o-mini`)

### Option 3: Google Gemini (free tier)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) (Google account, no billing required)
2. Create an API key
3. Set `GEMINI_API_KEY` in `.env`
4. Update `llm.model` in config to `gemini/gemini-2.0-flash`

### Other providers

Research Radar uses [litellm](https://docs.litellm.ai/) for LLM abstraction. Any litellm-supported provider works — update `llm.model` in config and set the corresponding API key in `.env`.

## Cost

Typical costs per digest run (50 papers fetched, 10 shown):

| Model | Cost/run | Notes |
|-------|----------|-------|
| Claude Sonnet | ~$0.15–0.20 | Default. Best reasoning quality. |
| GPT-4o-mini | ~$0.001 | 100x cheaper, slightly less nuanced. |
| Gemini Flash | Free | Free tier available via Google AI Studio. |

## Project Structure

```
paper_radar/
  config/
    config.example.yaml   # Template — copy to config.yaml
  src/
    cli/                  # Command-line interface
    core/                 # Config, models, shared types
    sources/              # arXiv RSS/API, INSPIRE-HEP
    profiles/             # User profile schema
    ranking/              # Keyword pre-sort, LLM reranking
    summarization/        # LLM client, prompt templates
    reports/              # Markdown and HTML report generation
    storage/              # SQLite persistence and caching
    workflows/            # End-to-end pipeline orchestration
  output/                 # Generated reports (gitignored)
  data/                   # SQLite database (gitignored)
```
