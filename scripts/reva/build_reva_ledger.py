#!/usr/bin/env python3
"""RETIRED (FT-F04): this script used to self-certify the REVA ledger.

It synthesized passing pytest run records (exit_code=0) without executing any test,
fabricated "lead_architect" review warrants and marked every obligation closed. That is not
evidence, so it now refuses to run. Use the real runner instead:

    python scripts/reva/run_reva_ledger.py [--write-docs]

which runs ``pytest tests/reva`` and records only what that run proves.
"""

import sys

MESSAGE = (
    "build_reva_ledger.py is retired: it synthesized passing runs and closed every obligation "
    "without executing tests. Use scripts/reva/run_reva_ledger.py, which records a real test run."
)


def main() -> int:
    print(MESSAGE, file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
