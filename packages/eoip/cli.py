"""EOIP command-line entry point."""

from __future__ import annotations

import argparse
from pathlib import Path

from eoip.ingestion.incremental_indexer import GitHookInstaller
from eoip.ingestion.incremental_indexer import main as incremental_index_main


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="eoip", description="EOIP developer utilities")
    subcommands = parser.add_subparsers(dest="command", required=True)

    hooks = subcommands.add_parser("install-hooks", help="Install EOIP git hooks")
    hooks.add_argument("--repo-root", type=Path, default=Path.cwd())
    hooks.add_argument("--hook-type", default="post-commit")
    hooks.add_argument("--uninstall", action="store_true")

    incremental = subcommands.add_parser("incremental-index", help="Run KGR-G-012 diff-only AST indexing")
    incremental.add_argument("args", nargs=argparse.REMAINDER)

    args = parser.parse_args(argv)
    if args.command == "install-hooks":
        if args.uninstall:
            removed = GitHookInstaller.uninstall(str(args.repo_root), args.hook_type)
            print(f"Removed {args.hook_type}: {removed}")
        else:
            hook_path = GitHookInstaller.install(str(args.repo_root), args.hook_type)
            print(f"Installed {args.hook_type}: {hook_path}")
        return 0
    if args.command == "incremental-index":
        return incremental_index_main(args.args)
    parser.error("unknown command")
    return 2
