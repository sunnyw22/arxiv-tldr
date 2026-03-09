"""LLM-assisted config wizard — interactive setup for Research Radar."""

import json
import sys
from pathlib import Path

import yaml

from src.core.config import LLMConfig
from src.summarization.llm_client import call_llm

# Common arXiv categories for validation
VALID_ARXIV_CATEGORIES = {
    # Physics
    "astro-ph", "astro-ph.CO", "astro-ph.EP", "astro-ph.GA", "astro-ph.HE",
    "astro-ph.IM", "astro-ph.SR",
    "cond-mat", "cond-mat.dis-nn", "cond-mat.mes-hall", "cond-mat.mtrl-sci",
    "cond-mat.other", "cond-mat.quant-gas", "cond-mat.soft",
    "cond-mat.stat-mech", "cond-mat.str-el", "cond-mat.supr-con",
    "gr-qc", "hep-ex", "hep-lat", "hep-ph", "hep-th",
    "math-ph", "nlin", "nucl-ex", "nucl-th",
    "physics.acc-ph", "physics.ao-ph", "physics.app-ph", "physics.atm-clus",
    "physics.atom-ph", "physics.bio-ph", "physics.chem-ph",
    "physics.class-ph", "physics.comp-ph", "physics.data-an",
    "physics.flu-dyn", "physics.gen-ph", "physics.geo-ph", "physics.hist-ph",
    "physics.ins-det", "physics.med-ph", "physics.optics",
    "physics.plasm-ph", "physics.pop-ph", "physics.soc-ph",
    "physics.space-ph",
    "quant-ph",
    # CS
    "cs.AI", "cs.AR", "cs.CC", "cs.CE", "cs.CG", "cs.CL", "cs.CR",
    "cs.CV", "cs.CY", "cs.DB", "cs.DC", "cs.DL", "cs.DM", "cs.DS",
    "cs.ET", "cs.FL", "cs.GL", "cs.GR", "cs.GT", "cs.HC", "cs.IR",
    "cs.IT", "cs.LG", "cs.LO", "cs.MA", "cs.MM", "cs.MS", "cs.NA",
    "cs.NE", "cs.NI", "cs.OH", "cs.OS", "cs.PF", "cs.PL", "cs.RO",
    "cs.SC", "cs.SD", "cs.SE", "cs.SI", "cs.SY",
    # Math
    "math.AC", "math.AG", "math.AP", "math.AT", "math.CA", "math.CO",
    "math.CT", "math.CV", "math.DG", "math.DS", "math.FA", "math.GM",
    "math.GN", "math.GR", "math.GT", "math.HO", "math.IT", "math.KT",
    "math.LO", "math.MG", "math.MP", "math.NA", "math.NT", "math.OA",
    "math.OC", "math.PR", "math.QA", "math.RA", "math.RT", "math.SG",
    "math.SP", "math.ST",
    # Stats
    "stat.AP", "stat.CO", "stat.ME", "stat.ML", "stat.OT", "stat.TH",
    # Q-Bio, Q-Fin, EESS
    "q-bio.BM", "q-bio.CB", "q-bio.GN", "q-bio.MN", "q-bio.NC",
    "q-bio.OT", "q-bio.PE", "q-bio.QM", "q-bio.SC", "q-bio.TO",
    "q-fin.CP", "q-fin.EC", "q-fin.GN", "q-fin.MF", "q-fin.PM",
    "q-fin.PR", "q-fin.RM", "q-fin.ST", "q-fin.TR",
    "eess.AS", "eess.IV", "eess.SP", "eess.SY",
}

VALID_INSPIRE_SUBJECTS = {
    "Accelerators", "Astrophysics", "Computing", "Data Analysis and Statistics",
    "Experiment-HEP", "Experiment-Nucl", "General Physics",
    "Gravitation and Cosmology", "Instrumentation", "Lattice",
    "Math and Math Physics", "Other", "Phenomenology-HEP",
    "Theory-HEP", "Theory-Nucl",
}

WIZARD_SYSTEM_PROMPT = """\
You are a setup assistant for Research Radar, a personalized paper discovery tool \
that monitors arXiv and INSPIRE-HEP.

Your job is to take a researcher's description of their interests and produce a \
structured JSON config. You must map their natural language description to:
1. Specific topic interests (short phrases for keyword matching)
2. Required signals (terms that boost relevance)
3. Negative filters (terms that reduce relevance)
4. A concise project context sentence
5. Appropriate arXiv categories
6. Appropriate INSPIRE keywords and subject codes (if relevant to physics)
7. Expertise level

Be precise with arXiv categories — only use real category codes."""

WIZARD_PROMPT_TEMPLATE = """\
A researcher described their interests as follows:

Research field: {field}
Specific topics: {topics}
What they want to stay current on: {current}
Must-have keywords: {signals}
Expertise level: {level}
Topics to avoid: {avoid}

Based on this, generate a Research Radar config as a JSON object with this exact structure:

{{
  "profile": {{
    "topic_interests": ["list of 3-6 specific topic phrases"],
    "required_signals": ["1-3 terms from the researcher's must-have keywords"],
    "negative_filters": ["1-3 terms from the researcher's avoidance topics"],
    "project_context": "one sentence describing their research focus",
    "expertise_level": "beginner|intermediate|advanced|expert"
  }},
  "sources": {{
    "arxiv": {{
      "enabled": true,
      "categories": ["list of 2-5 arXiv category codes like cs.LG, hep-ex"],
      "max_results": 50
    }},
    "inspire": {{
      "enabled": true or false (true only if physics-related),
      "keywords": ["list of INSPIRE keywords if physics-related, else empty"],
      "subject_codes": ["list of INSPIRE subject codes if physics-related, else empty"]
    }}
  }},
  "search_days_back": integer number of days to search back (e.g., 7, 30, 365, 1825)
}}

The researcher specified a search window of: {days_back}

Rules:
- topic_interests should be short (1-4 words each), specific to their research
- required_signals: use the researcher's must-have keywords directly. \
Only infer if they left it blank. Never fabricate signals.
- negative_filters: use the researcher's avoidance topics directly. Should be empty [] if they didn't mention any.
- arXiv categories must be real codes (e.g., cs.LG not "machine learning")
- Only enable INSPIRE if the research is physics-related
- project_context should be a single concise sentence
- search_days_back must be an integer: convert natural language like \
"1 year" to 365, "5 years" to 1825, "2 weeks" to 14, "3 months" to 90, etc.

Return ONLY the JSON object, no other text."""


def run_wizard(output_path: str = "config/config.yaml", model: str = "openai/gpt-4o-mini"):
    """Run the interactive config wizard."""
    print("=" * 60)
    print("  Research Radar — Config Setup Wizard")
    print("=" * 60)
    print()
    print("I'll ask a few questions about your research interests,")
    print("then generate a config file for you.\n")

    # --- Step 1: Gather user input ---
    answers = _ask_questions()

    # --- Step 2: Generate config via LLM ---
    llm_config = LLMConfig(model=model, temperature=0.2, max_tokens=1024)
    config_data = _build_config(answers, llm_config, model)

    # --- Step 3: Review loop ---
    config_data = _review_loop(config_data, answers, llm_config, model)
    if config_data is None:
        return None

    # --- Step 4: Save ---
    output = _save_config(config_data, output_path)
    if output is None:
        return None

    # --- Step 5: Offer to run digest ---
    _offer_digest(output, config_data)

    return str(output)


def _build_config(
    answers: dict, llm_config: LLMConfig, model: str
) -> dict:
    """Generate and finalize config from answers."""
    print("\nGenerating config...")
    config_data = _generate_config(answers, llm_config)

    if config_data is None:
        print("  LLM generation failed. Creating from template instead.")
        config_data = _fallback_config(answers)

    # Validate arXiv categories
    config_data = _validate_categories(config_data)

    # Override arXiv categories if user specified them
    user_cats = answers.get("arxiv_categories", "").strip()
    if user_cats:
        parsed_cats = [c.strip() for c in user_cats.split(",") if c.strip()]
        if parsed_cats:
            config_data.setdefault("sources", {})
            config_data["sources"].setdefault("arxiv", {})
            config_data["sources"]["arxiv"]["categories"] = parsed_cats
            config_data = _validate_categories(config_data)

    # Ensure search_days_back is a valid integer
    raw_days = config_data.get("search_days_back")
    if not isinstance(raw_days, int) or raw_days <= 0:
        config_data["search_days_back"] = _parse_days_back(
            answers.get("days_back", "7")
        )

    # Add default sections
    config_data.setdefault(
        "summary", {"style": "concise", "max_papers": 15, "min_score": 4}
    )
    config_data.setdefault(
        "output", {"formats": ["markdown", "html"], "output_dir": "output/"}
    )
    config_data.setdefault(
        "llm", {"model": model, "temperature": 0.3, "max_tokens": 4096}
    )
    config_data.setdefault(
        "schedule", {"cron": "0 8 * * *", "timezone": "UTC"}
    )

    return config_data


def _display_config(config_data: dict):
    """Print the config in a readable format."""
    yaml_str = yaml.dump(config_data, default_flow_style=False, sort_keys=False)
    print("\n" + "=" * 60)
    print("  Generated Config")
    print("=" * 60)
    print()
    print(yaml_str)


def _review_loop(
    config_data: dict,
    answers: dict,
    llm_config: LLMConfig,
    model: str,
) -> dict | None:
    """Show config and let user approve or request changes. Returns final config or None."""
    while True:
        _display_config(config_data)

        print("  [y] Looks good — save it")
        print("  [e] Edit — describe what to change")
        print("  [r] Regenerate from scratch")
        print("  [q] Quit without saving")

        try:
            choice = input("\nChoice [y/e/r/q]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            return None

        if choice == "y" or choice == "":
            return config_data
        elif choice == "q":
            print("Aborted.")
            return None
        elif choice == "r":
            print("\nRegenerating...")
            config_data = _build_config(answers, llm_config, model)
        elif choice == "e":
            feedback = _get_feedback()
            if feedback:
                config_data = _apply_feedback(
                    config_data, feedback, llm_config
                )
                config_data = _validate_categories(config_data)
        else:
            print("  Invalid choice, try again.")


def _get_feedback() -> str:
    """Get change request from user."""
    try:
        return input(
            "\nWhat would you like to change?\n"
            "  (e.g., 'add cs.CV to categories', "
            "'remove survey from negative filters')\n  > "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print()
        return ""


def _apply_feedback(
    config_data: dict, feedback: str, llm_config: LLMConfig
) -> dict:
    """Use LLM to apply user feedback to the existing config."""
    current_yaml = yaml.dump(
        config_data, default_flow_style=False, sort_keys=False
    )
    prompt = (
        "Here is the current Research Radar config:\n\n"
        f"```yaml\n{current_yaml}```\n\n"
        f"The user wants to make these changes: {feedback}\n\n"
        "Apply the requested changes and return the FULL updated config "
        "as a JSON object with the same structure. "
        "Only change what was requested — keep everything else the same.\n\n"
        "Return ONLY the JSON object, no other text."
    )

    try:
        response = call_llm(
            prompt=prompt,
            config=llm_config,
            system_prompt=WIZARD_SYSTEM_PROMPT,
            json_mode=True,
        )
        updated = json.loads(response)
        if "profile" in updated and "sources" in updated:
            # Preserve default sections the LLM might drop
            for key in ("summary", "output", "llm", "schedule",
                        "search_days_back"):
                if key in config_data and key not in updated:
                    updated[key] = config_data[key]
            print("  Changes applied.")
            return updated
    except (json.JSONDecodeError, RuntimeError) as e:
        print(f"  Failed to apply changes: {e}")

    print("  Keeping previous config.")
    return config_data


def _save_config(config_data: dict, output_path: str) -> Path | None:
    """Save config to file with overwrite protection. Returns path or None."""
    output = Path(output_path)

    if output.exists():
        print(f"WARNING: {output_path} already exists.")
        try:
            answer = input("Overwrite? [y/N] ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            return None
        if answer != "y":
            alt_path = output.parent / "config.generated.yaml"
            print(f"Saving to {alt_path} instead.")
            output = alt_path

    output.parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        f.write("# Research Radar — Generated Configuration\n")
        f.write(
            "# Edit this file to customize your paper discovery settings.\n\n"
        )
        yaml.dump(config_data, f, default_flow_style=False, sort_keys=False)

    print(f"\nConfig saved to {output}")
    return output


def _offer_digest(output: Path, config_data: dict):
    """Offer to run a digest with the newly created config."""
    days_back = config_data.get("search_days_back", 7)
    if not isinstance(days_back, int) or days_back <= 0:
        days_back = 7

    try:
        run_now = input("\nRun a digest now? [Y/n] ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        print("\nSkipping digest.")
        return

    if run_now == "n":
        print(
            "Run your first digest with: "
            "python -m src.cli.main digest"
        )
        return

    from datetime import datetime, timedelta, timezone

    from src.core.config import load_config
    from src.workflows.daily_digest import run_daily_digest

    config = load_config(str(output))
    since_date = datetime.now(timezone.utc) - timedelta(days=days_back)

    print(f"\nRunning digest (papers from last {days_back} days)...\n")
    result = run_daily_digest(
        config,
        since_date=since_date,
        interactive=True,
    )

    if not result["ranked_papers"]:
        print("\nNo relevant papers found for your profile.")
    else:
        print(f"\nDigest complete: {result['stats']['final_count']} papers")
        if result.get("md_path"):
            print(f"  Markdown: {result['md_path']}")
        if result.get("html_path"):
            print(f"  HTML:     {result['html_path']}")


def _ask_questions() -> dict:
    """Ask the user about their research interests."""
    questions = [
        ("field",
         "What is your research field?\n"
         "  (e.g., machine learning, particle physics, neuroscience)\n  > "),
        ("topics",
         "What specific topics are you working on?\n"
         "  (e.g., graph neural networks for tracking, LLM reasoning)\n  > "),
        ("current",
         "What do you want to stay current on?\n"
         "  (e.g., new architectures, benchmark results, specific methods)\n  > "),
        ("signals",
         "What keywords MUST appear for a paper to be highly relevant?\n"
         "  These are specific terms central to your work — names of methods,\n"
         "  experiments, datasets, or tools you actively use.\n"
         "  (e.g., ATLAS, transformer, benchmark, PyTorch — leave blank to skip)\n  > "),
        ("level",
         "What is your expertise level?"
         " [beginner/intermediate/advanced/expert]\n  > "),
        ("avoid",
         "Any topics you want to AVOID?\n"
         "  Papers matching these terms will be deprioritized.\n"
         "  (e.g., survey only, review article, Monte Carlo — leave blank to skip)\n  > "),
    ]

    answers = {}
    for key, prompt in questions:
        try:
            val = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAborted.")
            sys.exit(1)
        answers[key] = val or "not specified"

    # Optional: arXiv categories
    print()
    try:
        cats = input(
            "arXiv categories to monitor? (comma-separated, leave blank for auto)\n"
            "  (e.g., cs.LG, cs.CL, hep-ex, stat.ML)\n  > "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(1)
    answers["arxiv_categories"] = cats

    # Optional: search time window
    try:
        days = input(
            "\nHow far back to search? (e.g., 7, 30 days, 1 year — default: 7 days)\n  > "
        ).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nAborted.")
        sys.exit(1)
    answers["days_back"] = days

    return answers


def _generate_config(answers: dict, llm_config: LLMConfig) -> dict | None:
    """Generate config JSON from user answers via LLM."""
    prompt = WIZARD_PROMPT_TEMPLATE.format(**answers)

    try:
        response = call_llm(
            prompt=prompt,
            config=llm_config,
            system_prompt=WIZARD_SYSTEM_PROMPT,
            json_mode=True,
        )
        data = json.loads(response)
        # Basic structure validation
        if "profile" not in data or "sources" not in data:
            return None
        return data
    except (json.JSONDecodeError, RuntimeError) as e:
        print(f"  LLM error: {e}")
        return None


def _validate_categories(config_data: dict) -> dict:
    """Validate and filter arXiv categories against known list."""
    arxiv_config = config_data.get("sources", {}).get("arxiv", {})
    categories = arxiv_config.get("categories", [])
    valid = []
    invalid = []
    for cat in categories:
        if cat in VALID_ARXIV_CATEGORIES:
            valid.append(cat)
        else:
            invalid.append(cat)
    if invalid:
        print(f"  Removed invalid arXiv categories: {', '.join(invalid)}")
    if valid:
        config_data["sources"]["arxiv"]["categories"] = valid
    return config_data


def _parse_days_back(raw: str) -> int:
    """Parse a natural language duration into days.

    Handles: "7", "30 days", "1 year", "5 years", "2 weeks", "3 months", etc.
    Returns 7 as default if unparseable.
    """
    raw = raw.strip().lower()
    if not raw:
        return 7

    # Try plain integer first
    try:
        val = int(raw)
        return val if val > 0 else 7
    except ValueError:
        pass

    # Parse "N unit" patterns
    import re
    match = re.match(r"(\d+)\s*(day|week|month|year)s?", raw)
    if match:
        n = int(match.group(1))
        unit = match.group(2)
        multipliers = {"day": 1, "week": 7, "month": 30, "year": 365}
        return n * multipliers.get(unit, 1)

    return 7


def _fallback_config(answers: dict) -> dict:
    """Create a minimal config from user answers without LLM."""
    topics = [t.strip() for t in answers.get("topics", "").split(",") if t.strip()]
    if not topics:
        topics = [answers.get("field", "research")]

    level = answers.get("level", "intermediate").lower()
    if level not in ("beginner", "intermediate", "advanced", "expert"):
        level = "intermediate"

    return {
        "profile": {
            "topic_interests": topics,
            "required_signals": [],
            "negative_filters": [],
            "project_context": answers.get("current", ""),
            "expertise_level": level,
        },
        "sources": {
            "arxiv": {
                "enabled": True,
                "categories": ["cs.LG"],
                "max_results": 50,
            },
            "inspire": {
                "enabled": False,
                "keywords": [],
                "subject_codes": [],
            },
        },
        "search_days_back": _parse_days_back(answers.get("days_back", "7")),
    }
