# CLAUDE.md — Research Radar

## Project overview

Research Radar is a personalized paper discovery and screening system for researchers. It monitors arXiv, filters and ranks papers based on a user profile, and produces evidence-backed summaries to help researchers decide what to read. The system runs locally via CLI, uses YAML config for personalization, and stores data in SQLite.

## Key directories

- `vault/` — project memory and design docs (product vision, architecture, MVP scope, roadmap, workflows, collaboration model)
- `src/` — source code (all implementation lives here)
- `config/` — user configuration files (YAML)
- `output/` — generated reports and digests (gitignored)

## Development rules

1. **Read context first** — before non-trivial work, read relevant `vault/` docs and source modules. Prefer targeted context over broad exploration.
2. **Plan before implementing** — for any task beyond a tiny fix, produce a short plan identifying affected modules, risks, validation approach, and whether scope/architecture is changing.
3. **Stay inside agreed scope** — do not silently introduce features, dependencies, or architectural changes not already agreed or documented. Surface scope changes explicitly before coding.
4. **Validate before declaring done** — code compiling is not completion. Run relevant validation checks. If validation cannot be completed, say so clearly.
5. **Update vault docs** — when a task changes architecture, workflow, schema, scope, or key behavior, update the relevant file(s) in `vault/`.
6. **Ask before unagreed work** — discuss with the user before changing product scope, architecture boundaries, dependencies, data model, output formats, or deployment decisions.

## Architecture boundaries

These modules are separate and must not mix concerns:

- **Sources** — retrieval and raw parsing only; no summarization logic
- **Ranking** — candidate generation and relevance scoring; no report formatting
- **Summarization** — LLM prompts, provider interaction, structured outputs; no direct source fetching
- **Reports** — rendering from normalized data and summaries; no ranking decisions
- **Workflows** — orchestration of end-to-end jobs; calls lower-level modules, does not duplicate their logic
- **Storage** — persistence layer; accessed through defined interfaces
- **Profiles** — user profile schema and loading
- **Core** — shared config, models, logging

## Tech stack

- **Language**: Python
- **Config**: YAML files for user settings and profiles
- **Persistence**: SQLite (local)
- **LLM abstraction**: litellm for provider-agnostic LLM calls
- **CLI**: Python CLI for execution
- **Outputs**: Markdown (default), HTML/email

## Validation contract

Every non-trivial change should be validated on applicable dimensions:

- **Functional** — does it work correctly? (ingestion, CLI, reports, config)
- **Design alignment** — are architecture boundaries respected? Are schema contracts intact?
- **Trustworthiness** — do summaries preserve source links? Are claims grounded?
- **Regression** — do previous commands/configs/workflows still work?
- **Documentation** — are vault docs updated when behavior or design changed?

## Task completion reporting

At the end of a task, report:

- What changed
- What was validated
- What remains unverified
- Any risks or assumptions

## Security

- NEVER commit API keys, secrets, or credentials into the repo. All secrets must go in `.env` (which is gitignored). Use environment variables or config references to access them at runtime.

## Block workflow

After each implementation block:
1. **Review risks** — discuss what could trick us in the future before moving on
2. **Document discussions** — capture design decisions, deferred ideas, and discussion outcomes into vault md files as we build
3. **Commit** — commit all changes after discussion and before starting a new block

## Coding principles

- **Avoid hardcoding paths and values** — make things configurable (e.g., accept `--config` flag with a sensible default fallback)
- **Keep things flexible** — prefer parameters over constants where the value might reasonably vary

## What to avoid

- Skipping context gathering before implementation
- Coding before planning on non-trivial tasks
- Silent architecture drift (changing boundaries without discussion)
- Unvalidated completion claims
- Undocumented design changes
- Introducing unagreed complexity into the MVP
- Hardcoding provider-specific behavior into shared modules
- Bypassing normalized schema contracts
- Hardcoding file paths — always allow configuration with sensible defaults
