# Research Radar

Personalized paper discovery and screening for researchers. Monitors arXiv and INSPIRE-HEP, ranks papers against your research profile using LLM-powered relevance scoring, and delivers evidence-backed summaries.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## API Key Setup

Research Radar uses an LLM for paper ranking and summarization. The default (and free) option is Google Gemini.

### Google Gemini (free tier)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account (no billing required)
3. Click **Create API Key**
4. Copy `.env.example` to `.env` and paste your key:

```bash
cp .env.example .env
# Edit .env and replace your_gemini_api_key_here with your actual key
```

Free tier limits: 15 requests/min, 1M tokens/day — more than enough for daily digests.

### Other providers

Research Radar uses [litellm](https://docs.litellm.ai/) for LLM abstraction. Any litellm-supported provider works — just update the `llm.model` field in your config and set the corresponding API key in `.env`. See `.env.example` for supported keys.

## Configuration

Copy `config/config.example.yaml` to `config/config.yaml` and edit to match your research interests.

## Usage

Coming soon — MVP in development.

## Project docs

Design documentation lives in `vault/`. See `RESEARCH_RADAR_PLAN.md` for the development roadmap.
