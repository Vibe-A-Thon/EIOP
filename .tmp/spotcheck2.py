refs = [
 ("packages/eoip/contracts/query_plan.py", 17, 25, "QueryPlan"),
 ("packages/eoip/query/executor.py", 29, 43, "structured query"),
 ("packages/eoip/query/executor.py", 165, 189, "bounded path"),
 ("packages/eoip/query/executor.py", 192, 200, "impact analysis"),
 ("packages/eoip/query/executor.py", 58, 70, "entity search"),
 ("packages/eoip/query/nl.py", 85, 113, "NL interpretation"),
 ("packages/eoip/query/nlq.py", 183, 200, "NLQ"),
 ("packages/eoip/query/policy.py", 1, 20, "safety policy"),
 ("packages/eoip/retrieval/service.py", 23, 40, "retrieval router"),
 ("packages/eoip/retrieval/service.py", 364, 380, "EvidenceManifest"),
 ("packages/eoip/models/provider.py", 1, 30, "LocalModelProvider"),
 ("packages/eoip/retrieval/vectors.py", 1, 9, "InMemorySearchIndex"),
 ("packages/eoip/retrieval/eval.py", 1, 20, "RAG eval"),
 ("packages/eoip/contracts/agent.py", 39, 59, "agent contract 22 types"),
 ("packages/eoip/contracts/agent.py", 82, 90, "dry-run"),
 ("packages/eoip/agents/runtime.py", 264, 280, "budget clamping"),
 ("packages/eoip/agents/runtime.py", 42, 67, "write approval boundary"),
 ("packages/eoip/contracts/tool.py", 14, 20, "READ_TOOLS"),
 ("packages/eoip/agents/trace_impact.py", 1, 20, "TraceImpact agent"),
 ("packages/eoip/contracts/memory.py", 4, 12, "scoped memory"),
 ("packages/eoip/audit/redaction.py", 1, 10, "redaction"),
 ("packages/eoip/authn/__init__.py", 18, 26, "secret isolation"),
 ("apps/api/extended.py", 1251, 1260, "metrics endpoint"),
 ("apps/api/main.py", 479, 483, "prometheus metrics"),
 ("packages/eoip/ontology/manifest.py", 386, 391, "cross-graph linking"),
 ("packages/eoip/graph/bitemporal.py", 1, 15, "bitemporal"),
 ("packages/eoip/graph/metrics.py", 147, 160, "blast radius"),
 ("packages/eoip/graph/metrics.py", 323, 349, "pagerank"),
 ("packages/eoip/graph/community.py", 122, 130, "label propagation"),
 ("packages/eoip/graph/community.py", 247, 255, "louvain"),
 ("packages/eoip/graph/paths.py", 44, 52, "BFS shortest paths"),
 ("packages/eoip/graph/paths.py", 112, 120, "Yens k-shortest"),
 ("packages/eoip/graph/similarity.py", 76, 84, "jaccard"),
 ("packages/eoip/graph/similarity.py", 169, 177, "link prediction"),
 ("packages/eoip/ontology/rdf.py", 27, 40, "JSON-LD"),
]
for path, a, b, note in refs:
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except FileNotFoundError:
        print(f"### MISSING FILE: {path} ({note})"); continue
    n = len(lines)
    snippet = " | ".join(s.strip()[:75] for s in lines[a-1:min(b, a+3)])
    flag = "OK" if b <= n else f"RANGE-OVERFLOW({n} lines)"
    print(f"{path}:{a}-{b} [{flag}] ({note})\n    {snippet}")
