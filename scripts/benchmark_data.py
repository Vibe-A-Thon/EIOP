"""Deterministic benchmark dataset generator (NFR-PERF-001).

Produces the engineering-doc dataset profile scaled down for CI and local
runs, built directly into a MemoryGraphStore via the standard upsert APIs.

Profiles:
    s: 200 work items, 2 repos, 30 commits, 500 files/symbols, ~2.3k edges
    m: 2000 work items, 10 repos, 150 commits, 2500 files/symbols, ~19k edges

Generation is fully deterministic for a given (scale, seed).

TODO(NFR-PERF-001): full-scale benchmarking against HugeGraph under the
Docker Compose profile; this script only reproduces the shape at CI scale.
"""

from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path

from eoip.graph.memory import MemoryGraphStore
from eoip.jobs import write_json
from eoip.ontology.manifest import SCHEMA_VERSION
from eoip.snapshot import digest

SCALES = {
    "s": {"work_items": 200, "repos": 2, "commits": 30, "files_symbols": 500, "extra_refs": 500},
    "m": {"work_items": 2000, "repos": 10, "commits": 150, "files_symbols": 2500, "extra_refs": 8000},
}


def build_store(scale: str = "s", seed: int = 42) -> MemoryGraphStore:
    if scale not in SCALES:
        raise ValueError(f"unknown scale: {scale}")
    profile = SCALES[scale]
    rng = random.Random(seed)
    store = MemoryGraphStore()

    n_projects = max(2, profile["work_items"] // 50)
    projects = [
        store.upsert_vertex(
            "Project",
            {"canonical_id": f"urn:bench:project:{p}", "name": f"Bench Project {p}", "issue_key": f"BENCHP-{p}"},
        )
        for p in range(n_projects)
    ]

    items = []
    for i in range(profile["work_items"]):
        item = store.upsert_vertex(
            "WorkItem",
            {
                "canonical_id": f"urn:bench:item:{i}",
                "issue_key": f"BENCH-{i}",
                "summary": f"Benchmark item {i}: tune throughput of component {i % 17}",
                "issue_type": "Task",
                "status": "Open",
            },
        )
        items.append(item)
        store.upsert_edge(
            "CONTAINS", projects[i % n_projects]["vid"], item["vid"], {"fact_key": f"contains-{i}"}
        )

    # Chain of REFERENCES guarantees short, deterministic paths between items.
    for i in range(len(items) - 1):
        store.upsert_edge(
            "REFERENCES",
            items[i]["vid"],
            items[i + 1]["vid"],
            {"fact_key": f"chain-{i}", "source_ref": f"bench://ref/{i}"},
        )
    for k in range(profile["extra_refs"]):
        a, b = rng.randrange(len(items)), rng.randrange(len(items))
        if a != b:
            store.upsert_edge(
                "REFERENCES",
                items[a]["vid"],
                items[b]["vid"],
                {"fact_key": f"ref-{k}", "source_ref": f"bench://ref/x{k}"},
            )

    n_repos = profile["repos"]
    commits_per_repo = profile["commits"] // n_repos
    commits = []
    for r in range(n_repos):
        repo = store.upsert_vertex(
            "Repository",
            {"canonical_id": f"urn:bench:repo:{r}", "repo_id": f"bench-repo-{r}", "name": f"bench-repo-{r}"},
        )
        branch = store.upsert_vertex(
            "Branch",
            {"canonical_id": f"urn:bench:branch:{r}", "branch_name": "main", "repo_id": f"bench-repo-{r}"},
        )
        store.upsert_edge("HAS_BRANCH", repo["vid"], branch["vid"], {"fact_key": f"branch-{r}"})
        for c in range(commits_per_repo):
            commit = store.upsert_vertex(
                "Commit",
                {
                    "canonical_id": f"urn:bench:commit:{r}:{c}",
                    "commit_sha": f"{r:02x}{c:038x}",
                    "message": f"commit {r}:{c} implements benchmark work",
                    "author_email": f"dev{c % 7}@bench.invalid",
                },
            )
            commits.append((commit, r))
            store.upsert_edge(
                "HAS_COMMIT",
                branch["vid"],
                commit["vid"],
                {"fact_key": f"commit-{r}-{c}", "source_ref": f"bench://commit/{r}/{c}"},
            )
            for _ in range(2):
                store.upsert_edge(
                    "IMPLEMENTS",
                    commit["vid"],
                    items[rng.randrange(len(items))]["vid"],
                    {"fact_key": f"impl-{r}-{c}", "source_ref": f"bench://commit/{r}/{c}"},
                )

    n_files = profile["files_symbols"] // 2
    files = []
    for f in range(n_files):
        r = f % n_repos
        file_v = store.upsert_vertex(
            "File",
            {
                "canonical_id": f"urn:bench:file:{f}",
                "repo_id": f"bench-repo-{r}",
                "path": f"src/mod{f % 97}/file_{f}.py",
                "language": "python",
            },
        )
        files.append(file_v)
        commit = commits[r * commits_per_repo + f % commits_per_repo][0]
        store.upsert_edge(
            "MODIFIES",
            commit["vid"],
            file_v["vid"],
            {"fact_key": f"mod-{f}", "source_ref": f"bench://commit/{r}/{f % commits_per_repo}"},
        )

    dependencies = [
        store.upsert_vertex(
            "Dependency",
            {"canonical_id": f"urn:bench:dependency:{d}", "name": f"bench-lib-{d}", "language": "python"},
        )
        for d in range(8 * n_repos)
    ]

    symbols = []
    for s in range(profile["files_symbols"] - n_files):
        file_v = files[s % n_files]
        symbol = store.upsert_vertex(
            "CodeSymbol",
            {
                "canonical_id": f"urn:bench:symbol:{s}",
                "qualified_name": f"bench.mod{s % 97}.symbol_{s}",
                "symbol_kind": "function",
                "name": f"symbol_{s}",
                "repo_id": file_v["properties"]["repo_id"],
                "path": file_v["properties"]["path"],
            },
        )
        symbols.append(symbol)
        store.upsert_edge(
            "DECLARES", file_v["vid"], symbol["vid"], {"fact_key": f"decl-{s}", "source_ref": f"bench://file/{s}"}
        )
        if s > 0 and symbols[s - 1]["properties"]["path"] == symbol["properties"]["path"]:
            store.upsert_edge(
                "CALLS",
                symbol["vid"],
                symbols[s - 1]["vid"],
                {"fact_key": f"call-{s}", "source_ref": f"bench://file/{s}"},
            )
        store.upsert_edge(
            "IMPORTS",
            symbol["vid"],
            dependencies[rng.randrange(len(dependencies))]["vid"],
            {"fact_key": f"import-{s}", "source_ref": f"bench://file/{s}"},
        )
    return store


def store_stats(store: MemoryGraphStore, scale: str, seed: int) -> dict:
    return {
        "scale": scale,
        "seed": seed,
        "vertices": store.count_vertices(),
        "edges": store.count_edges(),
        "work_items": SCALES[scale]["work_items"],
        "repos": SCALES[scale]["repos"],
        "commits": SCALES[scale]["commits"],
        "files_symbols": SCALES[scale]["files_symbols"],
    }


def dump_store(store: MemoryGraphStore, destination: str | Path) -> dict:
    payload = {
        "schema_version": SCHEMA_VERSION,
        "vertices": store.find_vertices(limit=1_000_000),
        "edges": store.find_edges(limit=1_000_000),
        "raw_files": {},
    }
    write_json(Path(destination), {"sha256": digest(payload), "payload": payload})
    return {"file": str(destination), "sha256": digest(payload)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scale", choices=sorted(SCALES), default="s")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--dump", metavar="PATH", help="Optional JSON snapshot output (restorable via eoip.snapshot.restore).")
    args = parser.parse_args(argv)

    store = build_store(args.scale, args.seed)
    stats = store_stats(store, args.scale, args.seed)
    if args.dump:
        stats["dump"] = dump_store(store, args.dump)
    print(json.dumps(stats, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
