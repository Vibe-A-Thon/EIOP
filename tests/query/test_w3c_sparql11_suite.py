"""W3C SPARQL 1.1 query test suite through the EOIP /sparql pipeline on live engines (CRA-024.7).

Needs the pinned suite (``scripts/fetch_w3c_sparql_tests.sh``; ``EOIP_W3C_SUITE`` points at its
``sparql/sparql11`` directory) and a live engine (``EOIP_LIVE_FUSEKI_URL`` / ``EOIP_LIVE_GRAPHDB_URL``).
CI runs this in the ``sparql-fuseki`` job and fails when it is skipped.

Honest reporting: a test passes, is refused by design (verified independently here), or is a recorded
known gap in ``w3c_sparql11_known_gaps.json`` that must also fail when sent straight to the engine.
Nothing that fails is reported as passing; a gap that starts passing must be removed from the file.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import pytest
from rdflib.plugins.sparql import prepareQuery

from eoip.query.sparql_backend import has_unbounded_path
from eoip.query.w3c_conformance import _Store, load_tests, run, summarize

SUITE = Path(os.environ.get("EOIP_W3C_SUITE", ".cache/rdf-tests/sparql/sparql11"))
GAPS = json.loads((Path(__file__).with_name("w3c_sparql11_known_gaps.json")).read_text(encoding="utf-8"))
OUT = Path(os.environ.get("EOIP_W3C_REPORT_DIR", "test-results"))


def _backends() -> list[tuple[str, str, tuple[str, str] | None]]:
    out = []
    if os.environ.get("EOIP_LIVE_FUSEKI_URL"):
        server = os.environ["EOIP_LIVE_FUSEKI_URL"].rstrip("/").rsplit("/", 1)[0]
        user = os.environ.get("EOIP_LIVE_FUSEKI_USER", "admin")
        out.append(("fuseki", server, (user, os.environ.get("EOIP_LIVE_FUSEKI_PASSWORD", ""))))
    if os.environ.get("EOIP_LIVE_GRAPHDB_URL"):
        out.append(("graphdb", os.environ["EOIP_LIVE_GRAPHDB_URL"].rstrip("/"), None))
    return out


pytestmark = [
    pytest.mark.skipif(not (SUITE / "manifest-sparql11-query.ttl").exists(),
                       reason="W3C suite not fetched (scripts/fetch_w3c_sparql_tests.sh)"),
]


def _design_refusal_is_real(query_path: Path, code: str) -> bool:
    text = query_path.read_text(encoding="utf-8")
    if code == "UNBOUNDED_PROPERTY_PATH":
        return has_unbounded_path(text)
    if code == "UNSUPPORTED_QUERY_FORM":
        try:
            return prepareQuery(text, base="http://example.org/").algebra.name not in ("SelectQuery", "AskQuery")
        except Exception:  # noqa: BLE001
            return False
    return code in ("SERVICE_NOT_APPROVED", "UPDATE_NOT_PERMITTED")


@pytest.mark.parametrize("backend", [b[0] for b in _backends()] or ["none"])
def test_w3c_sparql11_query_suite(backend: str) -> None:
    configured = {b[0]: b for b in _backends()}
    if backend not in configured:
        pytest.skip("no live Fuseki/GraphDB configured")
    _, server, auth = configured[backend]
    store = _Store(backend, server, "w3c", auth)
    store.create()
    tests = load_tests(SUITE)
    outcomes = run(tests, store, SUITE)
    by_id = {o.id: o for o in outcomes}
    OUT.mkdir(parents=True, exist_ok=True)
    report = {"backend": backend, "rdf_tests_commit": GAPS["rdf_tests_commit"], "summary": summarize(outcomes),
              "outcomes": [o.__dict__ for o in outcomes]}
    (OUT / f"w3c-sparql11-{backend}.json").write_text(json.dumps(report, indent=2), encoding="utf-8")

    assert len(outcomes) == len(tests) > 300, "every approved test gets an outcome"
    known = GAPS["known_gaps"].get(backend, {})
    unexpected = [f"{o.id}: {o.outcome} {o.detail}" for o in outcomes
                  if o.outcome in ("fail", "error") and o.id not in known]
    assert not unexpected, "new W3C failures (fix them, or record a known gap with a decision):\n" + "\n".join(unexpected)
    stale = [t for t, g in known.items() if t not in by_id or by_id[t].outcome != g["outcome"]]
    assert not stale, f"known gaps that no longer fail as recorded (update the file): {stale}"
    not_engine = [t for t in known if by_id[t].engine_direct != by_id[t].outcome]
    assert not not_engine, f"failures that do not reproduce on the bare engine are EOIP defects: {not_engine}"
    tc_by_id = {t.id: t for t in tests}
    bogus = [o.id for o in outcomes if o.outcome == "rejected_by_design"
             and not _design_refusal_is_real(tc_by_id[o.id].query, o.detail)]
    assert not bogus, f"queries refused as out of scope that do not use the refused construct: {bogus}"
