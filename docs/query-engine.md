# EOIP Query Engine

EOIP supports 6 query languages, a structured QueryPlan executor, and a safety policy layer.

---

## Query Languages

| Language | Type | Parser | Description |
|----------|------|--------|-------------|
| EQL | Query | `query/eql.py` | EOIP Query Language — graph-native |
| NLQ | Query | `query/nlq.py` + `nl.py` | Natural language → QueryPlan |
| EOQL | Query | `query/languages.py` | Enterprise Object Query Language |
| OSQL | Query | `query/languages.py` | Ontology SQL |
| Semantic QL | Query | `query/languages.py` | Semantic Query Language |
| Gremlin (admin) | Admin | `graph/hugegraph.py` | Raw Gremlin — disabled by default |

---

## EQL — EOIP Query Language

`packages/eoip/query/eql.py`

Grammar supports:

```
FIND <label> WHERE <condition>
PATH FROM <id> TO <id> [MAX DEPTH <n>]
NEIGHBORS OF <id> [DEPTH <n>]
IMPACT OF <id> [DIRECTION DOWNSTREAM|UPSTREAM]
WHY <canonical_id>
WHY NOT <canonical_id>
WHAT CHANGED IN <domain> [SINCE <date>]
CONTEXT OF <id>
EDGES BETWEEN <id1> AND <id2>
COUNT <label> [WHERE <condition>]
DOMAINS
```

Example:
```eql
FIND WorkItem WHERE status = 'Open' AND domain = 'PAY'
PATH FROM urn:jira:PAY-123 TO urn:service:payment-gateway MAX DEPTH 5
IMPACT OF urn:service:auth DIRECTION DOWNSTREAM
```

---

## NLQ — Natural Language Query

`packages/eoip/query/nlq.py` + `packages/eoip/query/nl.py`

**Two-tier processing**:

1. **Rule-based fast path** (`nl.py:85-113`): Pattern matching for common intents (impact, path, search, what changed). Instant, no model call.

2. **Local model fallback** (`nlq.py:183-249`): When rule-based fails, calls Ollama to parse intent → produces structured QueryPlan.

**NLQ never produces raw Gremlin queries.** All natural language queries resolve to `QueryPlan` objects.

Example:
```
"What would break if auth-service is removed?"
→ {intent: IMPACT, anchors: [{canonical_id: "urn:service:auth"}], direction: DOWNSTREAM, depth: 4}
```

---

## EOQL — Enterprise Object Query Language

`packages/eoip/query/languages.py` — `parse_eoql()`

SQL-like syntax for graph entities:

```sql
SELECT WorkItem, CodeSymbol
WHERE WorkItem.status = 'Open'
JOIN WorkItem IMPLEMENTS CodeSymbol
LIMIT 50

TRAVERSE FROM urn:service:payment-gateway
WITH DEPTH 3
AGGREGATE COUNT BY domain

SELECT * WHERE domain IN ('CODE', 'WORK')
JOIN Commit REFERENCES WorkItem
```

Keywords: `SELECT`, `TRAVERSE`, `AGGREGATE`, `WHERE`, `JOIN`, `LIMIT`, `ORDER BY`

---

## OSQL — Ontology SQL

`packages/eoip/query/languages.py` — `parse_osql()`

Ontology-introspection language:

```sql
DESCRIBE WorkItem
LIST TYPES
LIST DOMAINS
LIST RELATIONSHIPS FROM WorkItem
INSTANCES OF CodeSymbol WHERE path LIKE '%payment%'
```

Keywords: `DESCRIBE`, `LIST TYPES`, `LIST DOMAINS`, `LIST RELATIONSHIPS`, `INSTANCES OF`

---

## Semantic Query Language

`packages/eoip/query/languages.py` — `parse_semantic_query()`

Conceptual / semantic queries:

```
MEANING OF payment-processing
RELATED TO fraud-detection
EXPLAIN urn:jira:PAY-123
COMPARE urn:service:auth-v1 AND urn:service:auth-v2
CLASSIFY urn:commit:abc123
```

Keywords: `MEANING OF`, `RELATED TO`, `EXPLAIN`, `COMPARE`, `CLASSIFY`

API: `POST /api/v1/query/language`  
Tests: `tests/unit/test_query_languages.py` — 29 cases.

---

## QueryPlan Executor (`packages/eoip/query/executor.py`)

### QueryPlan (`packages/eoip/contracts/query_plan.py`)

```python
class QueryPlan(BaseModel):
    intent: QueryIntent        # SEARCH|PATH|IMPACT|NEIGHBORS|NLQ
    anchors: list[EntityRef]   # starting entities
    depth: int = 3             # max traversal depth
    timeout: int = 30          # seconds
    evidence_mode: str = "SUMMARY"  # FULL|SUMMARY|NONE
    direction: str = "BOTH"    # OUTGOING|INCOMING|BOTH
```

### Intent Dispatch

| Intent | Handler | Description |
|--------|---------|-------------|
| `SEARCH` | `executor.py:58-131` | Multi-field entity search |
| `PATH` | `executor.py:165-189` | BFS / k-shortest paths |
| `IMPACT` | `executor.py:192-200` | Blast-radius analysis |
| `NEIGHBORS` | `executor.py:133-163` | k-hop neighborhood |
| `NLQ` | `nl.py:85-113` | NL→QueryPlan conversion |

### GraphResult

```python
class GraphResult(BaseModel):
    nodes: list[GraphNode]
    edges: list[GraphEdge]
    paths: list[GraphPath]
    evidence: list[EvidenceCitation]
    partial: bool              # True if timeout or result limit hit
    query_time_ms: int
```

---

## Query Safety Policy (`packages/eoip/query/policy.py`)

Enforced on every QueryPlan before execution:

| Policy | Default | Override |
|--------|---------|---------|
| `max_depth` | 8 | Cannot exceed 8 |
| `max_results` | 500 | Cannot exceed 500 |
| `timeout` | 30s | Cannot exceed 30s |
| `allowed_intents` | All | Configurable deny-list |
| `blocked_edges` | None | List of forbidden edge labels |
| `read_only` | True | Always |

Policy violations raise `QueryPolicyViolation` before any graph access.

---

## Parameterized Gremlin Templates

`packages/eoip/query/intelligence.py:381-468`

Internal parameterized templates for graph traversal. Never exposed to user input.

Injection prevention: all parameters are validated — forbids `{}$\` characters. Retrieved content is treated as data, never as Gremlin code.

The admin Gremlin endpoint (`/api/v1/admin/gremlin`) bypasses templates but is **disabled by default** and requires `EOIP_ADMIN_GREMLIN_ENABLED=1`.

---

## Export Formats

`packages/eoip/graph/format_converter.py`

12 export formats for graph data:

| Format | Method | Spec |
|--------|--------|------|
| RDF (Turtle) | `to_rdf_turtle` | W3C RDF |
| RDF/XML | `to_rdf_xml` | W3C RDF/XML |
| RDFS | `to_rdfs` | W3C RDFS |
| OWL | `to_owl` | W3C OWL 2 |
| JSON-LD 1.1 | (via `rdf.py`) | W3C JSON-LD 1.1 |
| Gremlin | `to_gremlin` | Apache TinkerPop |
| Cypher | `to_cypher` | openCypher |
| GQL | `to_gql` | ISO 39075 |
| SPARQL INSERT | `to_sparql_insert` | W3C SPARQL |
| SHACL | `to_shacl` | W3C SHACL |
| PGQL | `to_pgql` | Oracle PGQL |
| OpenCypher | `to_opencypher` | ISO openCypher |

API: `GET /api/v1/export/formats`, `GET /api/v1/ontology/export`
