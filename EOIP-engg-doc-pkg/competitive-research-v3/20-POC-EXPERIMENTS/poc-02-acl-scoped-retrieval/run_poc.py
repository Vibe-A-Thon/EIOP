"""POC-02: ACL-scoped retrieval — zero cross-user / cross-tenant leakage.

STATUS: SPECIFICATION STUB. NOT EXECUTED.

Per KNOWLEDGE_GRAPH_COMPETITIVE_RESEARCH_MASTER_PROMPT_v3.md Section 16 item 21,
POC experiments "run only if authorized and possible" -- none is authorized in
this research run. This file defines argument parsing and the intended shape
of the experiment (see 20-POC-EXPERIMENTS/poc-02-acl-scoped-retrieval/README.md
for the full design) so that whoever is authorized to run it does not have to
re-derive the fixture or the pass/fail logic from prose. Every action below is
a TODO. Nothing here calls a network, a database, or an EOIP module, and no
line of this script fabricates a PASS/FAIL outcome -- it only ever reports
NOT EXECUTED.

Validates (once implemented and run): BM-04 and BM-05 in
15-VALIDATION-BENCHMARK-PLAN.md. Targets the gaps named GAP-02, GAP-03, and
(for the memory-read extension) GAP-34 in 07-GAP-REGISTER.md, and the
self-inversion cards INV-SELF-01 / INV-SELF-02 in
09-CON-TO-PRO-INVERSION-REGISTER.md Section 3.
"""

import argparse
import sys

NOT_EXECUTED = "NOT EXECUTED (specification stub -- see README.md)"


# ---------------------------------------------------------------------------
# Fixture definition (data shape only -- no fixture is actually generated or
# written by this stub; see README.md Section 2.1 for the full design).
# ---------------------------------------------------------------------------

FIXTURE_SPEC = {
    "tenants": ["tenant_a", "tenant_b"],
    "users": {
        # user_id: (tenant, [source_acl_clearances])
        "user_a1": ("tenant_a", ["source:jira", "source:confluence"]),
        "user_a2": ("tenant_a", ["source:confluence"]),  # deliberately narrower
        "user_b1": ("tenant_b", ["source:jira", "source:confluence"]),  # same
        # clearance labels as user_a1, different tenant -- isolates the
        # tenant-leakage probe from the source-ACL-leakage probe.
    },
    "retrieval_modes": ["keyword", "vector", "hybrid", "graph_scoped", "graph_unscoped"],
    # TODO: define the actual fact set (10-20 facts, half tagged source:jira /
    # Tenant A, half source:confluence / Tenant A, a disjoint structurally
    # similar set owned by Tenant B, at least one fact reachable only via a
    # derived/inferred edge). See README.md Section 2.1.
}


def seed_fixture(args):
    """TODO: ingest FIXTURE_SPEC's facts into the target store (MemoryGraphStore
    first, per INV-SELF-01's own sequencing) via SourceEvent v2 with
    PermissionMetadata/acl_hash (contracts/source_event.py:42,50,74).

    Not implemented. This function performs no ingestion.
    """
    print(f"[seed-fixture] {NOT_EXECUTED}")
    print("  TODO: construct SourceEvent v2 records for FIXTURE_SPEC's fact set")
    print("  TODO: ingest via the validation gate (validation/gate.py) into the")
    print("        chosen GraphStore (MemoryGraphStore for the first pass)")
    print("  TODO: record the independently-computed expected-visible set per")
    print("        user (see README.md Section 2.3 step 3) for later diffing")
    return 0


def run_retrieval_probe(args):
    """TODO: for each (user, retrieval_mode) pair, issue the identical question
    and collect every fact/citation/cache-entry/memory-record surfaced.

    retrieval modes to probe (per README.md Section 2.2):
      - keyword   -> retrieval/service.py search_keyword
      - vector    -> retrieval/service.py search_vector (hashing embedder)
      - hybrid    -> search/hybrid_engine.py RRF fusion
      - graph_scoped   -> retrieve() called WITH scope passed (manual, bypassing
                           the production call sites that omit it per GAP-02)
      - graph_unscoped -> retrieve() called as every deployed route calls it
                           today (no scope) -- this is the as-deployed leakage
                           surface

    Not implemented. This function performs no retrieval call.
    """
    print(f"[run-retrieval-probe] {NOT_EXECUTED}")
    for mode in FIXTURE_SPEC["retrieval_modes"]:
        print(f"  TODO: probe mode={mode!r} for users {list(FIXTURE_SPEC['users'])}")
    print("  TODO: diff each response's surfaced-fact set against the")
    print("        independently-computed expected-visible set")
    print("  TODO: tag every surfaced item not in the expected-visible set as a")
    print("        LEAK, recording (user, mode, fact_id)")
    return 0


def report(args):
    """TODO: print a per-mode leak-count table and exit non-zero if any leak
    was recorded by run_retrieval_probe().

    Not implemented. This function performs no scoring and asserts nothing.
    A real implementation must never print PASS/FAIL without having actually
    executed seed_fixture() and run_retrieval_probe() in the same invocation.
    """
    print(f"[report] {NOT_EXECUTED}")
    print("  TODO: emit a (user x mode) leak-count table")
    print("  TODO: exit 0 only if every cell is exactly zero; exit 1 otherwise")
    return 0


def main(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "POC-02 ACL-scoped retrieval experiment -- SPECIFICATION STUB, "
            "NOT EXECUTED. See README.md for the full design."
        )
    )
    parser.add_argument(
        "--seed-fixture",
        action="store_true",
        help="TODO: seed the two-tenant / three-user fixture described in README.md 2.1.",
    )
    parser.add_argument(
        "--run",
        action="store_true",
        help="TODO: run the retrieval probe across all modes in FIXTURE_SPEC.",
    )
    parser.add_argument(
        "--mode",
        choices=["all", *FIXTURE_SPEC["retrieval_modes"]],
        default="all",
        help="TODO: restrict the probe to one retrieval mode (default: all).",
    )
    parser.add_argument(
        "--report",
        choices=["text", "json"],
        default="text",
        help="TODO: report format for the leak-count table (not implemented).",
    )
    args = parser.parse_args(argv)

    print("POC-02: ACL-scoped retrieval -- specification stub, NOT EXECUTED.")
    print("No network call, database call, or EOIP module import happens in this script.")
    print("See 20-POC-EXPERIMENTS/poc-02-acl-scoped-retrieval/README.md for the full design.")
    print()

    if not (args.seed_fixture or args.run):
        print("Nothing to do: pass --seed-fixture and/or --run (both are TODO stubs).")
        return 0

    rc = 0
    if args.seed_fixture:
        rc = seed_fixture(args) or rc
    if args.run:
        rc = run_retrieval_probe(args) or rc
        rc = report(args) or rc
    return rc


if __name__ == "__main__":
    sys.exit(main())
