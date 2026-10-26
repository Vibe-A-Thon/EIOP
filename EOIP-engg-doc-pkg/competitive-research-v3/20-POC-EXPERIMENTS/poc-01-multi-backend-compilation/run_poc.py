"""POC-01: Multi-Backend QueryPlan Compilation — SPECIFICATION STUB, NOT EXECUTED.

This file deliberately does not compile anything or claim a result. A 2026-10-19
version of this script hardcoded three fixed output strings that ignored the
`plan` argument entirely, then printed a fabricated "POC-01 PASS" regardless of
input. That version is removed; see README.md in this folder for why, and for
what a real version of this POC needs before any PASS/FAIL claim is meaningful.

Traces to: GAP-04, GAP-05, GAP-12, ADR-KG3-08, ADR-KG3-12.
"""

from __future__ import annotations

NOT_IMPLEMENTED = (
    "This POC is a specification, not an implementation. No compiler is wired "
    "up here, no backend is contacted, and nothing below is a result."
)

MISSING_PREREQUISITES = [
    "A QueryPlan fixture set covering every supported intent, including an adversarial "
    "fixture with an attacker-controlled property key/label (GAP-05).",
    "Live HugeGraph, Neo4j and (optionally) Fuseki/GraphDB containers pre-loaded with "
    "the same fixture graph.",
    "The actual compiler under test (packages/eoip/query/ast_compiler.py or its "
    "successor), not a mock — the current module is not on the production path "
    "(01a-BASELINE-DELTA-HEAD.md BL-09).",
    "A result-equivalence check per fixture across backends, with documented tolerances.",
    "An injection check: the adversarial fixture must not alter compiled-query structure.",
]


def main() -> None:
    print(NOT_IMPLEMENTED)
    print()
    print("Missing before this POC can be run for real:")
    for i, item in enumerate(MISSING_PREREQUISITES, 1):
        print(f"  {i}. {item}")
    print()
    print("No TODOs below were executed. No PASS/FAIL verdict is reported.")


if __name__ == "__main__":
    main()
