"""CLI for ontology semantic diff / CI publish gate (GAP-GITOPS).

Usage:
    python -m scripts.ontology_diff old.json new.json
    python -m scripts.ontology_diff - new.json        # current manifest as old
Exit 0 when publishable (no breaking changes), 1 otherwise.
"""

from __future__ import annotations

import sys

from eoip.ontology.gitops import main as gitops_main


def main(argv: list[str] | None = None) -> int:
    return gitops_main(argv)


if __name__ == "__main__":
    sys.exit(main())
