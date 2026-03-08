import json

from src.core.config import LLMConfig
from src.profiles.schema import UserProfile
from src.summarization.llm_client import call_llm
from src.summarization.prompts import build_synonym_prompt

MAX_REGENERATE = 3


def expand_keywords(profile: UserProfile, llm_config: LLMConfig) -> list[str]:
    """Use LLM to expand topic interests into a broader set of related terms.

    Makes one cheap LLM call to generate synonyms, abbreviations, and
    related concepts from the user's profile. Returns expanded term list
    for use in keyword pre-sorting.
    """
    if not profile.topic_interests and not profile.project_context:
        return []

    return _call_expansion(profile, llm_config)


def expand_keywords_interactive(
    profile: UserProfile, llm_config: LLMConfig
) -> list[str]:
    """Expand keywords with interactive user review.

    Shows expanded terms and lets the user accept, edit, regenerate,
    or skip expansion before proceeding.
    """
    if not profile.topic_interests and not profile.project_context:
        return []

    expanded = _call_expansion(profile, llm_config)
    regenerate_count = 0

    while True:
        original = set(t.lower() for t in profile.topic_interests)
        added = [t for t in expanded if t.lower() not in original]

        print(f"\nExpanded keywords ({len(expanded)} terms):")
        print(f"  Original:  {', '.join(profile.topic_interests)}")
        print(f"  Added:     {', '.join(added)}")
        print()
        print("  [a]ccept all")
        print("  [e]dit — remove specific terms (comma-separated)")
        print("  [r]egenerate — ask LLM for fresh expansion")
        print("  [s]kip — use only original interests")

        try:
            choice = input("\nChoice [a/e/r/s]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nUsing current expansion.")
            break

        if choice == "a" or choice == "":
            break
        elif choice == "s":
            expanded = list(profile.topic_interests)
            break
        elif choice == "r":
            regenerate_count += 1
            if regenerate_count >= MAX_REGENERATE:
                print(f"  Max regenerations ({MAX_REGENERATE}) reached, using current expansion.")
                break
            print("  Regenerating...")
            expanded = _call_expansion(profile, llm_config)
        elif choice == "e":
            to_remove = input("  Terms to remove (comma-separated): ").strip()
            if to_remove:
                remove_set = {t.strip().lower() for t in to_remove.split(",")}
                # Never remove original interests
                protected = original
                actually_removed = remove_set - protected
                if remove_set & protected:
                    kept = remove_set & protected
                    print(f"  Keeping original interests: {', '.join(kept)}")
                expanded = [
                    t for t in expanded if t.lower() not in actually_removed
                ]
                print(f"  Removed {len(actually_removed)} terms, {len(expanded)} remaining.")
        else:
            print("  Invalid choice, try again.")

    return expanded


def _call_expansion(profile: UserProfile, llm_config: LLMConfig) -> list[str]:
    """Make one LLM call for keyword expansion and return deduplicated terms."""
    prompt = build_synonym_prompt(profile)
    response = call_llm(prompt, llm_config, json_mode=True)

    try:
        data = json.loads(response)
        terms = data.get("expanded_terms", [])
        # Always include original interests first (LLM may rephrase or drop them)
        seen: set[str] = set()
        unique: list[str] = []
        for t in list(profile.topic_interests) + terms:
            lower = t.lower()
            if lower not in seen:
                seen.add(lower)
                unique.append(t)
        return unique
    except (json.JSONDecodeError, KeyError):
        # Fallback: return original interests if LLM response is unparseable
        return list(profile.topic_interests)
