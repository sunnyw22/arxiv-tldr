"""Research Radar CLI — entry point for running digests."""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.cli.wizard import run_wizard
from src.core.config import load_config
from src.core.config_validator import validate_config
from src.workflows.daily_digest import run_daily_digest

DEFAULT_CONFIG = "config/config.yaml"
DEFAULT_DB = "data/research_radar.db"


def main():
    parser = argparse.ArgumentParser(
        prog="research-radar",
        description="Personalized paper discovery and screening for researchers.",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- digest command ---
    digest_parser = subparsers.add_parser(
        "digest", help="Run a daily digest — fetch, rank, and summarize papers"
    )
    digest_parser.add_argument(
        "--config", "-c",
        default=DEFAULT_CONFIG,
        help=f"Path to config YAML (default: {DEFAULT_CONFIG})",
    )
    digest_parser.add_argument(
        "--db",
        default=DEFAULT_DB,
        help=f"Path to SQLite database (default: {DEFAULT_DB})",
    )
    digest_parser.add_argument(
        "--skip-validation",
        action="store_true",
        default=False,
        help="Skip LLM-based config validation pre-flight check",
    )
    digest_parser.add_argument(
        "--since",
        default=None,
        help="Only include papers submitted on or after this date (YYYY-MM-DD)",
    )
    digest_parser.add_argument(
        "--until",
        default=None,
        help="Only include papers submitted on or before this date (YYYY-MM-DD)",
    )
    digest_parser.add_argument(
        "--no-interactive",
        action="store_true",
        default=False,
        help="Skip interactive prompts (keyword review, etc). Use for CI/headless runs.",
    )

    # --- setup command ---
    setup_parser = subparsers.add_parser(
        "setup", help="Interactive wizard to generate a config file"
    )
    setup_parser.add_argument(
        "--config", "-c",
        default=DEFAULT_CONFIG,
        help=f"Output path for generated config (default: {DEFAULT_CONFIG})",
    )
    setup_parser.add_argument(
        "--model",
        default="openai/gpt-4o-mini",
        help="LLM model to use for config generation (default: openai/gpt-4o-mini)",
    )

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "digest":
        _run_digest(args)
    elif args.command == "setup":
        run_wizard(output_path=args.config, model=args.model)


def _parse_date(date_str: str, label: str) -> datetime:
    """Parse a YYYY-MM-DD date string into a timezone-aware datetime."""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        print(f"Invalid date format for --{label}: '{date_str}'. Expected YYYY-MM-DD.")
        sys.exit(1)


def _run_digest(args):
    config_path = Path(args.config)

    try:
        config = load_config(config_path)
    except FileNotFoundError:
        print(f"Config file not found: {args.config}")
        print(f"Copy config/config.example.yaml to {args.config} and customize it.")
        sys.exit(1)

    if not args.skip_validation:
        raw_yaml = config_path.read_text()
        warnings = validate_config(raw_yaml, config.llm)

        if warnings:
            print("\n--- Config Validation Warnings ---")
            for i, warning in enumerate(warnings, 1):
                print(f"  {i}. {warning}")
            print("----------------------------------\n")

            answer = input("Proceed anyway? [y/N] ").strip().lower()
            if answer != "y":
                print("Aborted. Please fix your config and try again.")
                sys.exit(1)

    # Parse date window flags
    since_date = _parse_date(args.since, "since") if args.since else None
    until_date = _parse_date(args.until, "until") if args.until else None

    interactive = not args.no_interactive
    result = run_daily_digest(
        config,
        db_path=args.db,
        since_date=since_date,
        until_date=until_date,
        interactive=interactive,
    )

    if not result["ranked_papers"]:
        print("\nNo relevant papers found for your profile.")
        return

    print(f"\nDigest complete: {result['stats']['final_count']} papers")
    if result.get("md_path"):
        print(f"  Markdown: {result['md_path']}")
    if result.get("html_path"):
        print(f"  HTML:     {result['html_path']}")


if __name__ == "__main__":
    main()
