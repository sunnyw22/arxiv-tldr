"""LLM-based config validation — pre-flight check for config issues."""

import json

from src.core.config import LLMConfig
from src.summarization.llm_client import call_llm

CONFIG_SCHEMA = """\
profile:
  topic_interests: list[str]
  required_signals: list[str]
  negative_filters: list[str]
  project_context: str
  expertise_level: str  # one of: beginner, intermediate, advanced, expert
sources:
  arxiv:
    enabled: bool
    categories: list[str]  # arXiv category codes like hep-ex, cs.LG
    max_results: int  # positive integer, default 50
  inspire:
    enabled: bool
    keywords: list[str]
    subject_codes: list[str]
    max_results: int  # positive integer, default 50
summary:
  style: str  # one of: concise, detailed, technical
  max_papers: int  # positive integer
output:
  formats: list[str]  # subset of: markdown, html
  output_dir: str
llm:
  model: str  # litellm format: provider/model-name
  temperature: float  # 0.0-2.0
  max_tokens: int  # positive integer
schedule:
  cron: str  # cron expression
  timezone: str
"""

VALIDATION_SYSTEM_PROMPT = """\
You are a configuration validator for a research paper discovery tool called Research Radar.
Your job is to analyze a user's YAML config and return a JSON array of warning strings.
Each warning should be a short, actionable sentence describing the issue.

Rules:
- Do NOT silently correct anything. Only report issues.
- Compare keys against the expected schema and flag misspelled or unknown keys.
- Flag wrong value types (e.g., a string where a list is expected).
- Flag nonsensical values (e.g., temperature > 2.0, max_papers <= 0, empty topic_interests).
- Flag missing commonly-needed fields (e.g., no profile.topic_interests means the system has nothing to search for).
- If the config looks valid, return an empty JSON array: []

Return ONLY a JSON array of strings. No other text."""

VALIDATION_USER_PROMPT_TEMPLATE = """\
Here is the expected config schema:

```
{schema}
```

Here is the user's config YAML to validate:

```yaml
{config_yaml}
```

Return a JSON array of warning strings. Return [] if no issues found."""


def validate_config(raw_yaml: str, llm_config: LLMConfig) -> list[str]:
    """Validate raw YAML config using an LLM call.

    Sends the raw YAML to the LLM along with the expected schema,
    and returns a list of warning/suggestion strings. An empty list
    means no issues were found.

    Args:
        raw_yaml: The raw YAML config text.
        llm_config: LLM configuration to use for the validation call.

    Returns:
        A list of warning strings (empty if config looks valid).
    """
    prompt = VALIDATION_USER_PROMPT_TEMPLATE.format(
        schema=CONFIG_SCHEMA,
        config_yaml=raw_yaml,
    )

    # Use a low max_tokens since we expect a short response
    validation_llm_config = LLMConfig(
        model=llm_config.model,
        temperature=0.0,
        max_tokens=512,
    )

    try:
        response = call_llm(
            prompt=prompt,
            config=validation_llm_config,
            system_prompt=VALIDATION_SYSTEM_PROMPT,
            json_mode=True,
        )
        warnings = json.loads(response)
    except (json.JSONDecodeError, RuntimeError):
        # If LLM call or parsing fails, don't block the pipeline
        return []

    if not isinstance(warnings, list):
        return []

    return [str(w) for w in warnings if isinstance(w, str)]
