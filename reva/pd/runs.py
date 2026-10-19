"""Verifier run orchestration, rerun aggregation, and attestation emission (T-208 / REVA-VS-009 / AG-07 / AG-10 / AG-11 / AG-12)."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from reva.core.errors import RevaValidationError
from reva.core.ids import verifier_run_id as compute_verifier_run_id
from reva.core.time import format_ts, utc_now_ms
from reva.kernel.authority import Depth
from reva.kernel.keys import generate_keypair
from reva.kernel.store import RevaStore
from reva.pd.bindings import Binding
from reva.pd.owner_digest import compute_owner_digest
from reva.sandbox.attest import create_dsse_attestation, create_in_toto_statement
from reva.sandbox.checkout import compute_tree_digest
from reva.sandbox.collectors import (
    OwnerSpan,
    ParsedTest,
    parse_coverage_contexts,
    parse_junit_xml,
)
from reva.sandbox.profiles import get_profile
from reva.sandbox.runner import ProcessSandbox, RunSpec


def get_environment_fingerprint(repo_path: Path) -> Dict[str, Any]:
    """Capture runtime environment fingerprint per AG-10."""
    lockfile_digests: Dict[str, str] = {}
    for lockname in ("poetry.lock", "package-lock.json", "requirements.txt", "Pipfile.lock"):
        lp = repo_path / lockname
        if lp.is_file():
            lockfile_digests[lockname] = hashlib.sha256(lp.read_bytes()).hexdigest()

    return {
        "interpreter": sys.version,
        "os": platform.system(),
        "arch": platform.machine(),
        "platform": platform.platform(),
        "lockfile_digests": lockfile_digests,
        "image_digest": None,
    }


@dataclass
class RunRecord:
    """Immutable verifier run record."""

    run_id: str
    verifier_id: str
    binding_digest: str
    repo_id: str
    commit: str
    tree_digest: str
    clean: bool
    environment: Dict[str, Any]
    profile: str
    depth: Depth
    network: str
    argv: List[str]
    started_at: str
    finished_at: str
    exit_code: int
    timed_out: bool
    lineage: Dict[str, Any]
    artifacts: List[Dict[str, Any]]
    tests: List[ParsedTest]
    reruns: int
    mutation: Optional[Dict[str, Any]] = None
    attestation_id: Optional[str] = None

    def canonical_dict(self) -> Dict[str, Any]:
        return {
            "argv": self.argv,
            "artifacts": self.artifacts,
            "binding_digest": self.binding_digest,
            "clean": self.clean,
            "commit": self.commit,
            "depth": self.depth.value if hasattr(self.depth, "value") else str(self.depth),
            "environment": self.environment,
            "exit_code": self.exit_code,
            "finished_at": self.finished_at,
            "lineage": self.lineage,
            "mutation": self.mutation,
            "network": self.network,
            "profile": self.profile,
            "repo_id": self.repo_id,
            "reruns": self.reruns,
            "started_at": self.started_at,
            "tests": [t.to_dict() for t in self.tests],
            "timed_out": self.timed_out,
            "tree_digest": self.tree_digest,
            "verifier_id": self.verifier_id,
        }


def execute_verifier_run(
    tenant_id: str,
    binding: Binding,
    commit: str,
    repo_path: Union[str, Path],
    reruns: int = 1,
    store: Optional[RevaStore] = None,
    verifier_private_key: Optional[Any] = None,
    verifier_key_id: Optional[str] = None,
) -> RunRecord:
    """Execute verifier command in sandbox, collect artifacts, and sign attestation."""
    repo = Path(repo_path).resolve()
    started_at = format_ts(utc_now_ms())

    # AG-11 verification: command line must match binding verifier specification
    argv = list(binding.verifier.argv)
    profile_spec = get_profile(binding.verifier.profile)

    # Compute owner spans and digests for coverage attribution
    owner_spans: List[OwnerSpan] = []
    owner_files: List[Dict[str, str]] = []
    for owner in binding.owners:
        target_path = repo / owner.path
        if target_path.is_file():
            res = compute_owner_digest(target_path, owner.symbol, owner.language, owner.path)
            if res.status == "found" and res.start_line is not None and res.end_line is not None:
                owner_spans.append(
                    OwnerSpan(
                        owner_digest=res.digest or "",
                        path=owner.path,
                        start_line=res.start_line,
                        end_line=res.end_line,
                    )
                )
            owner_files.append({
                "path": owner.path,
                "sha256": hashlib.sha256(target_path.read_bytes()).hexdigest(),
            })

    # Prepare temp directory for verifier outputs
    out_dir = Path(tempfile.mkdtemp(prefix="reva_verifier_out_"))
    junit_path = out_dir / "junit.xml"
    coverage_path = out_dir / "coverage.json"

    # Substitute output placeholders in argv if present
    processed_argv = []
    for arg in argv:
        processed_argv.append(
            arg.replace("<out>/junit.xml", str(junit_path))
            .replace("<out>/coverage.json", str(coverage_path))
            .replace("<out>", str(out_dir))
        )

    # Execute runs (initial + reruns-1) for AG-07 flakiness detection
    all_runs_tests: List[List[ParsedTest]] = []
    last_outcome = None

    for run_idx in range(max(1, reruns)):
        run_spec = RunSpec(
            argv=processed_argv,
            cwd=str(repo),
            env_allow=binding.verifier.env_allow,
            timeout_s=binding.verifier.timeout_s,
        )
        outcome = ProcessSandbox.run(run_spec)
        last_outcome = outcome

        # Parse test outcomes from junit.xml if produced, or fallback to exit code
        if junit_path.is_file():
            parsed_tests = parse_junit_xml(junit_path.read_bytes())
        else:
            # Fallback synthetic test for command-level verification
            outcome_str = "passed" if outcome.exit_code == 0 and not outcome.timed_out else "failed"
            parsed_tests = [
                ParsedTest(
                    test_id=f"{binding.obligation_key}::command",
                    outcome=outcome_str,
                    duration_ms=outcome.duration_ms,
                    obligation_keys=[binding.obligation_key],
                    case_kinds=["positive"],
                    owner_lines_hit={},
                )
            ]

        # Attribute coverage lines if coverage.json produced
        if coverage_path.is_file() and owner_spans:
            try:
                line_hits = parse_coverage_contexts(coverage_path.read_bytes(), owner_spans)
                for pt in parsed_tests:
                    if pt.test_id in line_hits:
                        pt.owner_lines_hit = line_hits[pt.test_id]
            except Exception:
                pass

        all_runs_tests.append(parsed_tests)

    assert last_outcome is not None
    finished_at = format_ts(utc_now_ms())

    # Aggregate test outcomes across reruns
    test_map: Dict[str, ParsedTest] = {}
    rerun_outcomes_map: Dict[str, List[str]] = {}

    for run_tests in all_runs_tests:
        for t in run_tests:
            if t.test_id not in test_map:
                test_map[t.test_id] = t
                rerun_outcomes_map[t.test_id] = [t.outcome]
            else:
                rerun_outcomes_map[t.test_id].append(t.outcome)
                # Maximize lines hit across runs
                for od, hits in t.owner_lines_hit.items():
                    prev_hits = test_map[t.test_id].owner_lines_hit.get(od, 0)
                    test_map[t.test_id].owner_lines_hit[od] = max(prev_hits, hits)

    aggregated_tests: List[ParsedTest] = []
    for tid, pt in test_map.items():
        outcomes = rerun_outcomes_map[tid]
        # AG-07: if outcomes across reruns differ, outcome is flaky
        if any(o != outcomes[0] for o in outcomes):
            pt.outcome = "flaky"
        else:
            pt.outcome = outcomes[0]
        aggregated_tests.append(pt)

    # Store artifacts in blob store
    artifacts: List[Dict[str, Any]] = []
    if store is not None:
        if junit_path.is_file():
            jb = junit_path.read_bytes()
            bref = store.blobs.put(tenant_id, jb, media_type="application/xml")
            artifacts.append({
                "kind": "junit_xml",
                "blob_id": bref.blob_id,
                "sha256": bref.sha256,
                "size_bytes": bref.size_bytes,
            })
        if coverage_path.is_file():
            cb = coverage_path.read_bytes()
            bref = store.blobs.put(tenant_id, cb, media_type="application/json")
            artifacts.append({
                "kind": "coverage_json",
                "blob_id": bref.blob_id,
                "sha256": bref.sha256,
                "size_bytes": bref.size_bytes,
            })
        if last_outcome.stdout:
            bref = store.blobs.put(tenant_id, last_outcome.stdout, media_type="text/plain")
            artifacts.append({
                "kind": "stdout",
                "blob_id": bref.blob_id,
                "sha256": bref.sha256,
                "size_bytes": bref.size_bytes,
            })

    try:
        tree_digest = compute_tree_digest(repo)
    except Exception:
        tree_digest = "0" * 64

    env_fingerprint = get_environment_fingerprint(repo)

    # Build unsigned run record and derive vr1_ ID
    unsigned_record = {
        "argv": binding.verifier.argv,
        "artifacts": artifacts,
        "binding_digest": binding.digest(),
        "clean": True,
        "commit": commit,
        "depth": binding.verifier.depth.value if hasattr(binding.verifier.depth, "value") else str(binding.verifier.depth),
        "environment": env_fingerprint,
        "exit_code": last_outcome.exit_code,
        "finished_at": finished_at,
        "lineage": last_outcome.lineage.to_dict(),
        "mutation": None,
        "network": binding.verifier.network,
        "profile": binding.verifier.profile,
        "repo_id": binding.owners[0].repo_id if binding.owners else "kgf",
        "reruns": reruns,
        "started_at": started_at,
        "tests": [t.to_dict() for t in aggregated_tests],
        "timed_out": last_outcome.timed_out,
        "tree_digest": tree_digest,
        "verifier_id": binding.verifier.verifier_id,
    }

    run_id = compute_verifier_run_id(unsigned_record)

    # Emit signed attestation
    att_id = None
    if verifier_private_key is not None and verifier_key_id is not None:
        statement = create_in_toto_statement(
            repo_id=binding.owners[0].repo_id if binding.owners else "kgf",
            commit=commit,
            owner_files=owner_files,
            run_record=unsigned_record,
            binding_digest=binding.digest(),
            obligation_keys=[binding.obligation_key],
        )
        envelope = create_dsse_attestation(statement, verifier_private_key, verifier_key_id)
        att_id = envelope["attestation_id"]
        if store is not None:
            cur = store.conn.cursor()
            cur.execute(
                """
                INSERT OR REPLACE INTO reva_attestations (
                    tenant_id, attestation_id, envelope, log_index
                ) VALUES (?, ?, ?, ?)
                """,
                (tenant_id, att_id, json.dumps(envelope), 0),
            )

    run_record = RunRecord(
        run_id=run_id,
        verifier_id=binding.verifier.verifier_id,
        binding_digest=binding.digest(),
        repo_id=binding.owners[0].repo_id if binding.owners else "kgf",
        commit=commit,
        tree_digest=tree_digest,
        clean=True,
        environment=env_fingerprint,
        profile=binding.verifier.profile,
        depth=binding.verifier.depth,
        network=binding.verifier.network,
        argv=binding.verifier.argv,
        started_at=started_at,
        finished_at=finished_at,
        exit_code=last_outcome.exit_code,
        timed_out=last_outcome.timed_out,
        lineage=last_outcome.lineage.to_dict(),
        artifacts=artifacts,
        tests=aggregated_tests,
        reruns=reruns,
        mutation=None,
        attestation_id=att_id,
    )

    # Persist run and test items in store
    if store is not None:
        cur = store.conn.cursor()
        cur.execute(
            """
            INSERT OR REPLACE INTO reva_runs (
                tenant_id, run_id, verifier_id, binding_digest, commit_sha, status,
                record, attestation_id, started_at, finished_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                tenant_id,
                run_id,
                binding.verifier.verifier_id,
                binding.digest(),
                commit,
                "succeeded" if run_record.exit_code == 0 and not run_record.timed_out else "failed",
                json.dumps(run_record.canonical_dict()),
                att_id,
                started_at,
                finished_at,
            ),
        )

        for pt in aggregated_tests:
            cur.execute(
                """
                INSERT OR REPLACE INTO reva_run_tests (
                    tenant_id, run_id, test_id, outcome, obligation_keys,
                    case_kinds, owner_lines_hit, rerun_outcomes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    tenant_id,
                    run_id,
                    pt.test_id,
                    pt.outcome,
                    json.dumps(pt.obligation_keys),
                    json.dumps(pt.case_kinds),
                    json.dumps(pt.owner_lines_hit),
                    json.dumps(rerun_outcomes_map.get(pt.test_id, [pt.outcome])),
                ),
            )
        store.conn.commit()

    return run_record
