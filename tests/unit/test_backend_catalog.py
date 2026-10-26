"""Backend catalog honesty + §6.5 correction tests (SR-GDB-002/003/004)."""

import pytest
from eoip.adapters.apache_age import ApacheAGEStore, CypherToAgeSqlBuilder
from eoip.adapters.catalog import BackendCatalog, CatalogError
from eoip.adapters.janusgraph import JanusGraphStore
from eoip.adapters.manifests import load_manifests


@pytest.fixture(scope="module")
def catalog() -> BackendCatalog:
    return BackendCatalog()


class TestManifestCoverage:
    def test_all_section6_backends_present(self, catalog):
        expected = {
            # native graph
            "neo4j", "neptune", "hugegraph", "janusgraph", "memgraph", "falkordb",
            "tigergraph", "nebulagraph", "dgraph", "allegrograph", "arangodb",
            "typedb", "arcadedb", "cayley", "cozodb", "kuzu", "terminusdb",
            # rdf
            "graphdb", "stardog", "rdfox", "virtuoso", "jena_tdb2", "oxigraph",
            # multimodel / relational-graph
            "apache_age", "orientdb", "oracle_pg", "spanner_graph",
            "sqlserver_graph", "mongodb_atlas", "neptune_analytics",
            # vector
            "pinecone", "chroma", "lancedb", "vespa", "pgvector", "opensearch",
            "elasticsearch", "redis_search", "clickhouse", "typesense",
            "milvus", "weaviate", "qdrant",
            # operational
            "postgresql", "sqlite", "redis", "foundationdb", "dynamodb",
            "cassandra", "duckdb", "pinot", "druid", "timescaledb",
        }
        present = {m.backend for m in catalog.list()}
        assert expected <= present, expected - present

    def test_manifests_have_required_fields(self, catalog):
        for manifest in catalog.list():
            assert manifest.native_surface, manifest.backend
            assert manifest.tier in {"A", "B", "C", "P2"}
            assert manifest.adapter_status in {"real", "manifest-only"}


class TestHonestyValidation:
    @pytest.mark.parametrize("backend", ["memgraph", "falkordb", "orientdb", "pinecone", "typedb"])
    def test_manifest_only_cannot_instantiate(self, catalog, backend):
        with pytest.raises(CatalogError) as excinfo:
            catalog.create_store(backend)
        assert "manifest-only" in str(excinfo.value)

    def test_external_gate_refusal_is_explicit(self, catalog):
        with pytest.raises(CatalogError) as excinfo:
            catalog.create_store("falkordb")
        assert "External gate" in str(excinfo.value)

    def test_real_backends_instantiate(self, catalog):
        store = catalog.create_store("memory")
        assert store.health()
        janus = catalog.create_store("janusgraph", {"url": "http://unused", "transport": None})
        assert isinstance(janus, JanusGraphStore)
        age = catalog.create_store("apache_age")
        assert isinstance(age, ApacheAGEStore)

    def test_vector_backends_are_not_graph_stores(self, catalog):
        for backend in ["pinecone", "chroma", "milvus", "qdrant", "pgvector"]:
            m = catalog.get(backend)
            assert m.category == "vector", backend
            assert m.role == "vector_index", backend


class TestCorrections65:
    def test_orientdb_dedup(self, catalog):
        orientdb = [m for m in catalog.list() if m.display_name == "OrientDB"]
        assert len(orientdb) == 1
        assert orientdb[0].category == "multimodel"

    def test_falkordb_note(self, catalog):
        m = catalog.get("falkordb")
        assert any("GraphBLAS" in note for note in m.notes)
        assert m.external_gate

    def test_kuzu_archived_warning(self, catalog):
        m = catalog.get("kuzu")
        assert any("archived" in note for note in m.notes)

    def test_no_duplicate_backends(self):
        manifests = load_manifests()
        keys = [m.backend for m in manifests.values()]
        assert len(keys) == len(set(keys))


class TestRealAdapters:
    def test_janusgraph_uses_injected_transport(self):
        calls = []

        def transport(script, bindings):
            calls.append(script)
            if "count" in script:
                return {"result": {"data": [3]}}
            return {"result": {"data": [{"id": 1, "label": "Entity", "properties": {"canonical_id": [{"value": "urn:x"}]}}]}}

        store = JanusGraphStore("http://unused", transport=transport)
        assert store.count_vertices() == 3
        vertex = store.get_vertex_by_canonical_id("urn:x")
        assert vertex is not None
        assert vertex["canonical_id"] == "urn:x"
        assert any("has('canonical_id'" in c for c in calls)

    def test_age_sql_builder_is_deterministic_and_guarded(self):
        builder = CypherToAgeSqlBuilder(graph="eoip")
        sql = builder.upsert_vertex("Entity", {"canonical_id": "urn:1", "name": 'a"; DROP TABLE x;--'})
        assert sql.count("$$") == 2  # dollar-quoted, single statement
        with pytest.raises(ValueError):
            builder.upsert_vertex("Entity", {"canonical_id": "urn:1", "name": "bad$$inject"})
        with pytest.raises(ValueError):
            builder.upsert_vertex("Bad;Label", {"canonical_id": "urn:1"})
        with pytest.raises(ValueError):
            CypherToAgeSqlBuilder(graph="bad;graph")

    def test_age_statements_preview(self):
        store = ApacheAGEStore(graph="eoip")
        statements = store.statements()
        assert {"upsert_vertex", "upsert_edge", "count_vertices"} <= set(statements)
        assert "cypher" in statements["upsert_vertex"]
        # No executor wired -> execution is an honest External-gate refusal.
        with pytest.raises(RuntimeError):
            store._run("SELECT 1;")
