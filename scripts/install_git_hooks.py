"""Install EOIP developer git hooks.

KGR-G-012: installs the incremental AST re-index post-commit hook without
embedding demo data or environment-specific graph credentials.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from eoip.ingestion.incremental_indexer import GitHookInstaller


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path.cwd())
    parser.add_argument("--hook-type", default="post-commit")
    parser.add_argument("--uninstall", action="store_true")
    args = parser.parse_args(argv)
    if args.uninstall:
        removed = GitHookInstaller.uninstall(str(args.repo_root), args.hook_type)
        print(f"Removed {args.hook_type}: {removed}")
        return 0
    hook_path = GitHookInstaller.install(str(args.repo_root), args.hook_type)
    print(f"Installed {args.hook_type}: {hook_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
