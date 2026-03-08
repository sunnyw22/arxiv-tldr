import json

from src.core.config import LLMConfig
from src.profiles.schema import UserProfile
from src.summarization.llm_client import call_llm
from src.summarization.prompts import build_synonym_prompt


def expand_keywords(profile: UserProfile, llm_config: LLMConfig) -> list[str]:
    """Use LLM to expand topic interests into a broader set of related terms.

    Makes one cheap LLM call to generate synonyms, abbreviations, and
    related concepts from the user's profile. Returns expanded term list
    for use in keyword pre-sorting.
    """
    if not profile.topic_interests and not profile.project_context:
        return []

    prompt = build_synonym_prompt(profile)
    response = call_llm(prompt, llm_config, json_mode=True)

    try:
        data = json.loads(response)
        terms = data.get("expanded_terms", [])
        # Always include original interests first (LLM may rephrase or drop them)
        seen = set()
        unique = []
        for t in list(profile.topic_interests) + terms:
            lower = t.lower()
            if lower not in seen:
                seen.add(lower)
                unique.append(t)
        return unique
    except (json.JSONDecodeError, KeyError):
        # Fallback: return original interests if LLM response is unparseable
        return list(profile.topic_interests)
