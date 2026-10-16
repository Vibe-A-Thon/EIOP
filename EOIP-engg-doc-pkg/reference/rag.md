# EOIP GraphRAG Retrieval System

EOIP implements a local-first, graph-grounded RAG system with 7 retrieval strategies, an adaptive strategy registry, stable evidence citations, and no mandatory vector database.

---

## Architecture Overview

```
Question
    ↓
RAGRouter.select_strategy() — 17 routing patterns
    ↓
RetrievalStrategy (GRAPH | KEYWORD | HYBRID | SEMANTIC | EVIDENCE | LINEAGE | AGENT)
    ↓
StrategyRegistry.execute_chain() — up to 4 chained built-in strategies
    ↓
LocalModelProvider.generate() (Ollama) OR structured fallback
    ↓
EvidenceManifest (stable URN citations)
```

---

## Retrieval Service (`packages/eoip/retrieval/service.py`)

### `retrieve(question, strategy, context)`
Main entry point. Routes to appropriate strategy, executes retrieval, calls local model, returns grounded answer.

### Model-Down Fallback
When Ollama is unavailable, `retrieve()` returns a structured `PartialResult` with:
- Top retrieved graph facts and document chunks
- Evidence URNs (no hallucinated answer)
- `partial: true` flag

**The fallback is always structured — never an empty response.**

---

## RAGRouter (`packages/eoip/graph/rag_router.py`)

17 routing patterns that map question context to retrieval strategy:

| Pattern | Strategy | Trigger |
|---------|----------|---------|
| Code question | GRAPH + KEYWORD | mentions symbol, file, function |
| Incident question | EVIDENCE + LINEAGE | mentions incident, error, failure |
| Architecture question | GRAPH + SEMANTIC | mentions service, dependency, design |
| Change question | LINEAGE | mentions "changed", "modified", last week |
| People question | GRAPH + KEYWORD | mentions person, team, assignment |
| Cross-domain | HYBRID | spans multiple domains |
| Documentation | KEYWORD + SEMANTIC | mentions doc, wiki, runbook |
| Impact question | AGENT | "what would break if..." |
| ...and 9 more | | |

---

## Retrieval Strategies

### GRAPH
Graph traversal-based retrieval. Expands from anchor entities via BFS, collects facts at each hop.

Best for: "What does service X depend on?", "Who worked on issue PAY-123?"

### KEYWORD
BM25-style keyword search across indexed graph entities and document chunks.

Best for: "Find all issues related to payment timeout", general search.

### HYBRID
Combines GRAPH traversal + keyword matching. Default strategy.

### SEMANTIC
Embedding-based similarity search using `HashingEmbedder`.

Best for: conceptually related facts not sharing exact keywords.

### EVIDENCE
Retrieves evidence trail for specific graph facts.

Best for: "Where does this claim come from?", "Show me the source."

### LINEAGE
Traces provenance chain: graph fact → source event → ingestion run.

Best for: "Why does the graph say X?", data quality investigations.

### AGENT
Delegates to TraceImpactAgent for multi-hop reasoning.

Best for: "What would break if...", complex impact questions.

---

## Strategy Registry (`packages/eoip/retrieval/strategy_registry.py`)

The adaptive strategy framework allows runtime plugin registration.

### RAGStrategyPlugin Protocol
```python
class RAGStrategyPlugin(Protocol):
    @property
    def name(self) -> str: ...
    @property
    def phase(self) -> StrategyPhase: ...
    def execute(self, context: StrategyContext) -> StrategyResult: ...
    def can_handle(self, context: StrategyContext) -> bool: ...
```

### StrategyPhase
`RETRIEVE → RERANK → SYNTHESIZE → VALIDATE`

### StrategyRegistry
```python
registry = StrategyRegistry()
registry.register(MyPlugin())           # add plugin
registry.select_strategies(context)    # select applicable plugins
registry.execute_chain(context)        # run full pipeline
```

### Built-in Strategies (4)

| Strategy | Phase | Behavior |
|----------|-------|----------|
| `GraphDepthStrategy` | RETRIEVE | Depth-first graph traversal from anchor |
| `EvidenceWeightStrategy` | RERANK | Reranks by evidence confidence and count |
| `DomainFocusStrategy` | RETRIEVE | Filters to relevant domain(s) |
| `FreshnessStrategy` | RERANK | Reranks by recency (updated_at) |

Tests: `tests/unit/test_strategy_registry.py` — 16 tests.

---

## Vector Search (No Vector DB Required)

`packages/eoip/retrieval/vectors.py` provides pure-Python in-memory search:

- `InMemorySearchIndex`: BM25-style keyword + semantic search
- `KeywordIndex`: TF-IDF term weighting
- `HashingEmbedder`: Locality-sensitive hashing for semantic similarity

No Qdrant, Pinecone, ChromaDB, or any vector database is required. The hash-based embedder provides approximate semantic similarity without external dependencies.

---

## Local Model Abstraction (`packages/eoip/models/provider.py`)

`LocalModelProvider` wraps Ollama:

```python
provider = LocalModelProvider(base_url="http://localhost:11434")
result = provider.generate(prompt, context_docs, max_tokens=2048)
```

- No external/cloud API calls
- Graceful model-down fallback always available
- Supports any Ollama-compatible model (default: llama3)

---

## Evidence Citations (`packages/eoip/contracts/retrieval.py`)

All RAG responses include an `EvidenceManifest` with stable URN citations:

```python
class EvidenceManifest:
    citations: list[EvidenceCitation]
    total_facts: int
    coverage_score: float

class EvidenceCitation:
    canonical_id: str      # "urn:jira:PAY-123"
    source_ref: str        # "jira://PAY/PAY-123"
    confidence: float
    fact_text: str
```

Citations use **canonical IDs** (not graph-internal vertex IDs) so they remain stable across graph rebuilds.

---

## RAG Evaluation (`packages/eoip/retrieval/eval.py`)

```python
harness = RAGEvaluationHarness(retrieval_service)
report = harness.evaluate(question_set)
```

Metrics:
- `precision`: fraction of retrieved facts that are relevant
- `recall`: fraction of relevant facts that were retrieved
- `evidence_coverage`: fraction of answer claims grounded in evidence
- `groundedness`: semantic alignment between answer and evidence
- `latency_p50_ms`, `latency_p95_ms`: retrieval + generation latency

Tests: `tests/unit/test_retrieval.py`
