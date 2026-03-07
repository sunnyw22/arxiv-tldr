import os
import re

from dotenv import load_dotenv
import litellm

from src.core.config import LLMConfig

# Load .env file for API keys
load_dotenv()


def strip_markdown_fences(text: str) -> str:
    """Strip markdown code fences from LLM responses."""
    return re.sub(r"^```(?:json)?\s*\n?|\n?```\s*$", "", text.strip())


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

    response = litellm.completion(**kwargs)
    content = response.choices[0].message.content
    if json_mode:
        content = strip_markdown_fences(content)
    return content
