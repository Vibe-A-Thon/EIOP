import sys
refs = [
 ("packages/eoip/connectors/base.py", 49, 68, "connector SDK discover/extract/checkpoint/health/replay"),
 ("packages/eoip/connectors/rest.py", 25, 32, "resiliency"),
 ("packages/eoip/connectors/acquisition.py", 66, 88, "resiliency/dry-run"),
 ("packages/eoip/connectors/confluence.py", 33, 98, "confluence connector"),
 ("packages/eoip/contracts/source_event.py", 1, 20, "immutable SourceEvent"),
 ("packages/eoip/contracts/normalized.py", 14, 38, "canonicalization"),
 ("packages/eoip/ingestion/pipeline.py", 30, 40, "canonicalization pipeline"),
 ("packages/eoip/graph/hugegraph.py", 95, 96, "canonical IDs"),
 ("packages/eoip/graph/hugegraph.py", 331, 361, "idempotent mutation"),
 ("packages/eoip/jobs.py", 22, 30, "job lifecycle"),
 ("packages/eoip/ingestion/dlq.py", 1, 20, "DLQ"),
 ("packages/eoip/ingestion/replay.py", 41, 60, "replay"),
 ("packages/eoip/graph/meta.py", 17, 30, "14 domains meta"),
 ("packages/eoip/graph/meta.py", 102, 120, "meta graph"),
 ("packages/eoip/graph/hugegraph.py", 208, 220, "schema bootstrap"),
 ("packages/eoip/identity/resolver.py", 12, 29, "identity resolution"),
 ("packages/eoip/ontology/manifest.py", 406, 420, "bridge edges"),
 ("packages/eoip/query/intelligence.py", 381, 400, "gremlin templates"),
 ("packages/eoip/ontology/manifest.py", 449, 471, "index strategy"),
 ("packages/eoip/graph/evolution.py", 20, 40, "version journal"),
]
for path, a, b, note in refs:
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        print(f"### MISSING FILE: {path} ({note})")
        continue
    n = len(lines)
    snippet = lines[a-1:min(b, a+3)]
    snippet = " | ".join(s.strip()[:80] for s in snippet)
    flag = "OK" if b <= n else f"RANGE-OVERFLOW(file has {n} lines)"
    print(f"{path}:{a}-{b} [{flag}] ({note})\n    {snippet}")
