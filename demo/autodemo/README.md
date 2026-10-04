# EOIP Automated Demo

Runs the full EOIP demo walkthrough non-interactively against an in-memory graph store.
Loads demo data, executes queries, validates the graph, and reports results.

## Usage

```powershell
# From repository root
.\.venv\Scripts\python.exe -m demo.autodemo.runner --verbose

# Save results to JSON
.\.venv\Scripts\python.exe -m demo.autodemo.runner --output demo/autodemo/results.json
```

## What it tests

1. Graph store initialization
2. Demo data loading (Jira, Git, enterprise scenario pack)
3. Vertex and edge count verification (>= 50 vertices, >= 40 edges)
4. Search for EOIP-1 work item
5. Golden path query: EOIP-1 to compute_impact symbol
6. Impact analysis from EOIP-1
7. Graph validation (zero errors)
8. Quality metrics computation
9. Required vertex label presence

## Exit codes

- `0` — all steps passed
- `1` — one or more steps failed
