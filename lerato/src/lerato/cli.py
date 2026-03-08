"""Command-line entry point for Lerato."""

from __future__ import annotations

from pathlib import Path
import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lerato",
        description="Run a Lerato source file.",
    )
    parser.add_argument("source", nargs="?", help="Path to a .ler source file")
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print the Lerato package version and exit",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        from lerato import __version__

        print(__version__)
        return 0

    if not args.source:
        parser.print_help()
        return 1

    source_path = Path(args.source)
    if source_path.suffix != ".ler":
        parser.error("source file must use the .ler extension")

    if not source_path.exists():
        parser.error(f"source file not found: {source_path}")

    print(f"Lerato CLI bootstrap: ready to run {source_path}")
    return 0
