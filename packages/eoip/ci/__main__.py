"""CLI entry: ``python -m packages.eoip.ci``.

Runs the KG CI/CD pipeline and exits 0/1 per the report verdict.
"""

from __future__ import annotations

import sys

from eoip.ci.pipeline import main

if __name__ == "__main__":
    sys.exit(main())
