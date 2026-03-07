# Research Radar

Personalized paper discovery and screening for researchers. Monitors arXiv and INSPIRE-HEP, ranks papers against your research profile using LLM-powered relevance scoring, and delivers evidence-backed summaries.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## API Key Setup

Research Radar uses an LLM for paper ranking and summarization. The default model is Anthropic Claude Sonnet.

### Option 1: Anthropic (default)

1. Sign up at [console.anthropic.com](https://console.anthropic.com)
2. Add credits under Plans & Billing
3. Create an API key
4. Copy `.env.example` to `.env` and set your key:

```bash
cp .env.example .env
# Edit .env and set ANTHROPIC_API_KEY=your_key_here
```

### Option 2: OpenAI

1. Get an API key from [platform.openai.com](https://platform.openai.com)
2. Set `OPENAI_API_KEY` in `.env`
3. Update `llm.model` in your config to `openai/gpt-4o-mini` (or any OpenAI model)

### Option 3: Google Gemini (free tier)

1. Go to [Google AI Studio](https://aistudio.google.com/apikey) (Google account, no billing required)
2. Create an API key
3. Set `GEMINI_API_KEY` in `.env`
4. Update `llm.model` in your config to `gemini/gemini-2.0-flash`

### Other providers

Research Radar uses [litellm](https://docs.litellm.ai/) for LLM abstraction. Any litellm-supported provider works — update `llm.model` in config and set the corresponding API key in `.env`.

## Configuration

Copy `config/config.example.yaml` to `config/config.yaml` and edit to match your research interests.

## Usage

Coming soon — MVP in development.

## Project docs

Design documentation lives in `vault/`. See `RESEARCH_RADAR_PLAN.md` for the development roadmap.
