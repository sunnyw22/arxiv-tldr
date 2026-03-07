import re
from dataclasses import dataclass, field

from dotenv import load_dotenv
import litellm

from src.core.config import LLMConfig

# Load .env file for API keys
load_dotenv()


def strip_markdown_fences(text: str) -> str:
    """Strip markdown code fences from LLM responses."""
    return re.sub(r"^```(?:json)?\s*\n?|\n?```\s*$", "", text.strip())


@dataclass
class TokenUsage:
    """Tracks cumulative token usage across LLM calls."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    call_count: int = 0

    def add(self, usage):
        """Add usage from a single LLM response."""
        if usage:
            self.prompt_tokens += getattr(usage, "prompt_tokens", 0) or 0
            self.completion_tokens += getattr(usage, "completion_tokens", 0) or 0
            self.total_tokens += getattr(usage, "total_tokens", 0) or 0
            self.call_count += 1

    def report(self) -> str:
        """Return a human-readable usage report."""
        return (
            f"LLM Usage: {self.call_count} calls, "
            f"{self.prompt_tokens:,} prompt tokens, "
            f"{self.completion_tokens:,} completion tokens, "
            f"{self.total_tokens:,} total tokens"
        )


# Global token tracker — reset per pipeline run
token_usage = TokenUsage()


def reset_token_usage():
    """Reset the global token usage tracker."""
    token_usage.prompt_tokens = 0
    token_usage.completion_tokens = 0
    token_usage.total_tokens = 0
    token_usage.call_count = 0


def call_llm(
    prompt: str,
    config: LLMConfig,
    system_prompt: str | None = None,
    json_mode: bool = False,
) -> str:
    """Make a single LLM call via litellm.

    Args:
        prompt: The user prompt.
        config: LLM configuration (model, temperature, max_tokens).
        system_prompt: Optional system prompt.
        json_mode: If True, request JSON output format.

    Returns:
        The LLM response text.

    Raises:
        RuntimeError: If the API call fails (auth, rate limit, network, etc.)
    """
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    kwargs = {
        "model": config.model,
        "messages": messages,
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
    }

    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}

    try:
        response = litellm.completion(**kwargs)
    except litellm.exceptions.AuthenticationError:
        raise RuntimeError(
            f"API authentication failed for model '{config.model}'. "
            "Check that your API key is correct and has sufficient credits. "
            "Keys should be set in the .env file."
        )
    except litellm.exceptions.RateLimitError:
        raise RuntimeError(
            f"Rate limit exceeded for model '{config.model}'. "
            "Wait a moment and try again, or switch to a different model in config."
        )
    except Exception as e:
        raise RuntimeError(
            f"LLM API call failed for model '{config.model}': {e}"
        )

    token_usage.add(response.usage)

    content = response.choices[0].message.content
    if json_mode:
        content = strip_markdown_fences(content)
    return content
