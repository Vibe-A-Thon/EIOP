# POC-01: Multi-Backend QueryPlan Compilation

## Objective
Demonstrate that a single structured `QueryPlan` compiles deterministically into:
1. Apache HugeGraph Gremlin REST payload.
2. Neo4j Cypher 25 query string with parameters.
3. W3C SPARQL 1.1 query text.

## How to Run
```bash
python run_poc.py
```
