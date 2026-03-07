"""Research Radar CLI — entry point for running digests."""

import argparse
import sys

from src.core.config import load_config
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

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "digest":
        _run_digest(args)


def _run_digest(args):
    try:
        config = load_config(args.config)
    except FileNotFoundError:
        print(f"Config file not found: {args.config}")
        print(f"Copy config/config.example.yaml to {args.config} and customize it.")
        sys.exit(1)

    result = run_daily_digest(config, db_path=args.db)

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
