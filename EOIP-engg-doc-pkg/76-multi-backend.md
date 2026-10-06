# EOIP Multi-Backend GraphStore

EOIP supports multiple graph storage backends, selected via configuration file or environment variable. The default backend is Apache HugeGraph; Amazon Neptune and an in-process Memory backend are also available.

---

## Backend Registry (`packages/eoip/graph/backends.py`)

`create_graph_store(path=None) -> GraphStore` is the single factory entry point used throughout the platform. It reads `config/graph-store.yaml` (or the path passed as argument), selects the configured backend, and returns a fully initialized `GraphStore` instance.

```python
from eoip.graph.backends import create_graph_store, backend_capabilities

store = create_graph_store()                    # uses config/graph-store.yaml
store = create_graph_store("custom-graph.yaml") # use a custom config

caps = backend_capabilities()                   # capabilities for primary backend
caps = backend_capabilities("neptune")          # capabilities for named backend
```

`packages/eoip/runtime.py` re-exports this as `create_store()` — the common entry point for Docker service containers.

---

## Supported Backends

| Backend | Module | Default | Transport | Use Case |
|---------|--------|---------|-----------|---------|
| `hugegraph` | `graph/hugegraph.py` | **Yes** | Gremlin REST API | All production deployments |
| `neptune` | `graph/neptune.py` | No | openCypher HTTPS | AWS-managed Neptune deployments |
| `memory` | `graph/memory.py` | No | In-process | Tests and local development harnesses |

---

## Configuration (`config/graph-store.yaml`)

```yaml
# Primary backend — which backend create_graph_store() returns
primary: hugegraph     # hugegraph | neptune | memory

connections:
  hugegraph:
    type: hugegraph
    url: http://hugegraph-server:8080
    graph: hugegraph
    username: admin
    password: ""

  neptune:
    type: neptune
    url: https://your-neptune-endpoint:8182
    database: neptune
    open_cypher_path: /openCypher
    sparql_path: /sparql
    gremlin_path: /gremlin
    verify_tls: true

  memory:
    type: memory
```

### Environment Variable Overrides

| Variable | Purpose |
|----------|---------|
| `EOIP_GRAPH_BACKEND` | Override backend by name (`hugegraph`, `neptune`, `memory`) |
| `EOIP_GRAPH_URL` / `EOIP_NEPTUNE_URL` | Connection URL |
| `EOIP_GRAPH_DATABASE` | Logical database / graph name |
| `EOIP_GRAPH_USER` | Username (HugeGraph) |
| `EOIP_GRAPH_PASSWORD` | Password (HugeGraph) |

Config selection order: `EOIP_GRAPH_BACKEND` env → `primary` in `graph-store.yaml` → legacy HugeGraph env vars (`EOIP_HUGEGRAPH_*`).

---

## Amazon Neptune Adapter (`packages/eoip/graph/neptune.py`)

`NeptuneGraphStore` implements the full `GraphStore` protocol using Amazon Neptune's openCypher HTTPS endpoint.

### Key design points

- **Vertices** are identified by `canonical_id` + `eoip_vid` property (deterministic, same as HugeGraph)
- **Edges** are upserted using EOIP's deterministic `edge_key` (no duplicate edges)
- **Identifier sanitization** — `_IDENTIFIER_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")` rejects unsafe label names
- All query operations use parameterized openCypher — no string interpolation
- TLS is enforced by default (`verify_tls: true`)

### Neptune Endpoint Requirements

Neptune is not included in the default Docker deployment. To use it:

1. Provision an Amazon Neptune cluster (engine version 1.3+ for full openCypher support)
2. Set `EOIP_GRAPH_BACKEND=neptune` and `EOIP_NEPTUNE_URL=https://<endpoint>:8182`
3. Ensure the EOIP runtime has network access and valid IAM credentials (for IAM auth) or VPC connectivity

---

## GraphBackendCapabilities

`backend_capabilities()` returns a dict describing what each backend supports:

```python
@dataclass(frozen=True)
class GraphBackendCapabilities:
    backend: str
    models: list[str]             # underlying data models: ["property_graph"], etc.
    query_languages: list[str]    # native query languages
    native_query_language: str    # primary native language (Gremlin, openCypher, etc.)
    exports: list[str]            # export formats supported
    architecture: list[str]       # deployment architecture notes
    application_query_languages: list[str]  # EOIP-level languages (EQL, NLQ, EOQL, etc.)
    notes: list[str]              # capability notes
```

EOIP application-level query languages (EQL, EOQL, OSQL, Semantic QL, NLQ, Gremlin admin) are available on all backends. The underlying native language differs:

| Backend | Native Language |
|---------|----------------|
| HugeGraph | Gremlin (REST) |
| Neptune | openCypher (HTTPS) |
| Memory | Internal Python dict traversal |

---

## Backend-Invariant Contract (`packages/eoip/graph/store.py`)

All backends implement the `GraphStore` protocol:

```python
class GraphStore(Protocol):
    def upsert_vertex(self, canonical_id: str, label: str, properties: dict) -> str: ...
    def upsert_edge(self, edge_key: str, label: str, from_id: str, to_id: str, properties: dict) -> str: ...
    def tombstone_vertex(self, canonical_id: str) -> None: ...
    def get_vertex(self, canonical_id: str) -> dict | None: ...
    def get_neighbors(self, canonical_id: str, direction: str, labels: list[str]) -> list[dict]: ...
    def execute_query(self, query: str, params: dict) -> list[dict]: ...
    def schema_bootstrap(self, manifest) -> None: ...
```

Ingestion services, agents, and query executor all type-check against `GraphStore` — swapping the backend requires only the config change.

---

## Supported Export Formats (All Backends)

The `format_converter.py` export layer is backend-agnostic:

`rdf`, `rdf_xml`, `rdfs`, `owl`, `gremlin`, `cypher`, `opencypher`, `gql`, `sparql`, `shacl`, `pgql`, `json_ld`

---

## Tests

`tests/unit/test_graph_backends.py` — covers backend registry, config loading, Neptune adapter contract, env var overrides, and memory backend correctness.
