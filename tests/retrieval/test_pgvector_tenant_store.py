"""CRA-025.6 / X-41: tenant-partitioned durable vector store on PostgreSQL + pgvector.

Runs against a real pgvector server (``EOIP_LIVE_PGVECTOR_DSN``, an owner/superuser DSN; CI starts
``pgvector/pgvector`` in Docker with a per-run password). The application role used for every
read/write is created here without ownership or BYPASSRLS, so the row-level-security assertions
are meaningful. Skipped when no server is configured.
"""
from __future__ import annotations

import math
import os
import random
import secrets
import uuid

import pytest

psycopg = pytest.importorskip("psycopg")
from eoip.retrieval.hybrid_vector_service import (
    DimensionMismatchError,
    IncompatibleEmbeddingFamilyError,
    IndexFamily,
    IndexMetadata,
    TenantVectorIndex,
    TestHashingEmbedder,
    VectorDocument,
)
from eoip.retrieval.pgvector_store import PgVectorAdmin, PgVectorIndex, TenantNotProvisioned
from psycopg import sql
from psycopg.conninfo import make_conninfo

DSN = os.environ.get("EOIP_LIVE_PGVECTOR_DSN")
pytestmark = [pytest.mark.req("CRA-025"),
              pytest.mark.skipif(not DSN, reason="EOIP_LIVE_PGVECTOR_DSN not set (no pgvector server)")]

APP_ROLE = "eoip_vec_app"
DIM = 32
VOCAB = ["payment", "ledger", "invoice", "gateway", "refund", "settlement", "checkout", "fraud", "risk", "score", "latency", "cache", "queue", "kafka", "broker", "topic", "consumer", "schema", "registry", "deploy", "rollback", "canary", "cluster", "node", "pod", "tenant", "graph", "lineage", "ontology", "policy", "audit", "token", "secret", "vault", "rotate", "certificate"]


@pytest.fixture(scope="module")
def app_dsn():
    pw = secrets.token_urlsafe(24)
    with psycopg.connect(DSN, autocommit=True) as con:
        exists = con.execute("SELECT 1 FROM pg_roles WHERE rolname = %s", (APP_ROLE,)).fetchone()
        verb = "ALTER" if exists else "CREATE"
        con.execute(sql.SQL(verb + " ROLE {} LOGIN NOSUPERUSER NOBYPASSRLS PASSWORD {}").format(
            sql.Identifier(APP_ROLE), sql.Literal(pw)))
    PgVectorAdmin(DSN).install(APP_ROLE)
    return make_conninfo(DSN, user=APP_ROLE, password=pw)


def _meta(tenant: str, index_id: str = "idx", dim: int = DIM, family: IndexFamily = IndexFamily.TEXT) -> IndexMetadata:
    return IndexMetadata(index_id=index_id, scope=tenant, family=family, source_revision="s1",
                         ontology_revision="o1", policy_revision="p1", provider="test-hashing",
                         model="sha256", tokenizer="regex-w", dimension=dim)


@pytest.fixture()
def tenants():
    a, b = f"acme-{uuid.uuid4().hex[:8]}", f"bolt-{uuid.uuid4().hex[:8]}"
    admin = PgVectorAdmin(DSN)
    for t in (a, b):
        admin.provision_tenant(t)
        admin.provision_index(_meta(t))
    return a, b


def _corpus(n: int, seed: int, prefix: str = "d") -> list[tuple[str, str]]:
    rnd = random.Random(seed)
    return [(f"{prefix}{i:04d}", " ".join(rnd.choice(VOCAB) for _ in range(rnd.randint(4, 14)))) for i in range(n)]


def _docs(corpus, emb, acl=None, cent=None):
    return [VectorDocument(d, t, emb.embed(t), IndexFamily.TEXT, list((acl or {}).get(d, [])), {"n": i},
                           (cent or {}).get(d, 0.0)) for i, (d, t) in enumerate(corpus)]


def test_partitions_and_row_level_security_isolate_tenants(app_dsn, tenants):
    a, b = tenants
    emb = TestHashingEmbedder(DIM)
    with PgVectorIndex(app_dsn, _meta(a)) as ia, PgVectorIndex(app_dsn, _meta(b)) as ib:
        ia.add_documents(_docs([("a1", "payment ledger refund"), ("a2", "kafka broker topic")], emb))
        ib.add_documents(_docs([("b1", "payment ledger refund"), ("b2", "vault rotate secret")], emb))
        q = emb.embed("payment ledger refund")
        assert [r["doc_id"] for r in ia.hybrid_search("payment ledger", q, IndexFamily.TEXT, [], top_k=5)] == ["a1", "a2"]
        assert [r["doc_id"] for r in ib.hybrid_search("payment ledger", q, IndexFamily.TEXT, [], top_k=5)] == ["b1", "b2"]
        assert ia.count() == 2 and ib.count() == 2

    with psycopg.connect(app_dsn) as con:
        # Bound to tenant a, an explicit predicate on tenant b still sees nothing (RLS, not app filtering).
        con.execute("SELECT set_config('eoip.tenant_id', %s, false)", (a,))
        assert con.execute("SELECT count(*) FROM eoip_vec.docs WHERE tenant_id = %s", (b,)).fetchone()[0] == 0
        assert con.execute("SELECT count(*) FROM eoip_vec.docs").fetchone()[0] == 2
        # Writing a row for tenant b while bound to tenant a violates the policy's WITH CHECK.
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            con.execute("INSERT INTO eoip_vec.docs (tenant_id, index_id, doc_id, body, embedding, doc_len) "
                        "VALUES (%s, 'idx', 'x', 'x', %s::vector, 1)", (b, "[" + ",".join(["0.1"] * DIM) + "]"))
        con.rollback()
        # Unbound session: nothing visible at all.
        con.execute("SELECT set_config('eoip.tenant_id', '', false)")
        assert con.execute("SELECT count(*) FROM eoip_vec.docs").fetchone()[0] == 0
        # The app role has no privileges on the partitions themselves: only the RLS-guarded parent is reachable.
        part = con.execute("SELECT c.relname FROM pg_inherits i JOIN pg_class c ON c.oid = i.inhrelid "
                           "WHERE i.inhparent = 'eoip_vec.docs'::regclass AND pg_get_expr(c.relpartbound, c.oid) "
                           "LIKE %s", (f"%'{b}'%",)).fetchone()[0]
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            con.execute(sql.SQL("SELECT count(*) FROM {}").format(sql.Identifier("eoip_vec", part)))

    with psycopg.connect(DSN) as con:  # owner view: one physical partition per tenant, rows only for that tenant
        role = con.execute("SELECT rolsuper, rolbypassrls FROM pg_roles WHERE rolname = %s", (APP_ROLE,)).fetchone()
        assert role == (False, False)
        rows = con.execute(
            "SELECT c.relname, pg_get_expr(c.relpartbound, c.oid), c.relrowsecurity, c.relforcerowsecurity "
            "FROM pg_inherits i JOIN pg_class c ON c.oid = i.inhrelid "
            "WHERE i.inhparent = 'eoip_vec.docs'::regclass").fetchall()
        mine = {bound: (name, rls, force) for name, bound, rls, force in rows if a in bound or b in bound}
        assert len(mine) == 2 and all(v[1] and v[2] for v in mine.values())
        for t in (a, b):
            name = next(v[0] for k, v in mine.items() if t in k)
            got = con.execute(sql.SQL("SELECT DISTINCT tenant_id FROM {}").format(sql.Identifier("eoip_vec", name))).fetchall()
            assert got == [(t,)]


def test_unprovisioned_tenant_is_refused(app_dsn):
    with pytest.raises(TenantNotProvisioned):
        PgVectorIndex(app_dsn, _meta(f"ghost-{uuid.uuid4().hex[:8]}"))


def test_bm25_and_hybrid_rankings_match_the_in_process_index(app_dsn, tenants):
    a, _ = tenants
    emb = TestHashingEmbedder(DIM)
    corpus = _corpus(120, seed=7)
    cent = {d: (i % 5) / 10 for i, (d, _) in enumerate(corpus)}
    mem = TenantVectorIndex(_meta(a))
    for d in _docs(corpus, emb, cent=cent):
        mem.add_document(d)
    with PgVectorIndex(app_dsn, _meta(a)) as pg:
        pg.add_documents(_docs(corpus, emb, cent=cent))
        exact_dense = 0
        for query in ("payment refund latency", "kafka topic consumer schema", "vault token rotate rotate", "zzz"):
            m, p = mem.bm25_search(query, top_k=15), pg.bm25_search(query, top_k=15)
            assert [d for d, _ in p] == [d for d, _ in m], query
            assert all(math.isclose(x, y, rel_tol=1e-9) for (_, x), (_, y) in zip(p, m))
            qv = emb.embed(query)
            # Exact cosine ordering (float64) vs pgvector's HNSW (float4): same top candidates.
            exact = sorted(mem.documents, key=lambda d: -sum(x * y for x, y in zip(qv, mem.documents[d].vector)))[:20]
            dense = [d for d, _ in pg.dense_search(qv, 20, [])]
            assert len(set(dense) & set(exact)) >= 18, query
            hm = mem.hybrid_search(query, qv, IndexFamily.TEXT, [], top_k=5)
            hp = pg.hybrid_search(query, qv, IndexFamily.TEXT, [], top_k=5)
            if dense == exact:
                exact_dense += 1
                assert [r["doc_id"] for r in hp] == [r["doc_id"] for r in hm], query
            assert all(r["index_family"] == "TEXT" for r in hp)
        assert exact_dense >= 3  # HNSW returned the exact top-20 for most queries, so fusion was compared
        # Removing a document updates document frequencies (in both implementations).
        victim = pg.bm25_search("payment", top_k=1)[0][0]
        assert pg.remove_document(victim) and mem.remove_document(victim)
        assert [d for d, _ in pg.bm25_search("payment", 10)] == [d for d, _ in mem.bm25_search("payment", 10)]
        assert all(math.isclose(x, y, rel_tol=1e-9)
                   for (_, x), (_, y) in zip(pg.bm25_search("payment", 10), mem.bm25_search("payment", 10)))


def test_acl_prefilter_with_hnsw_does_not_starve_results(app_dsn, tenants):
    a, _ = tenants
    emb = TestHashingEmbedder(DIM)
    corpus = _corpus(400, seed=11)
    acl = {d: ["secops"] for i, (d, _) in enumerate(corpus) if i % 20}  # 95% restricted
    with PgVectorIndex(app_dsn, _meta(a)) as pg:
        pg.add_documents(_docs(corpus, emb, acl=acl))
        plan = pg.explain_dense(emb.embed("payment"), 10)
        assert "Index Scan using hnsw_" in plan and plan.count("docs_t_") == 1, plan  # one tenant partition only
        qv = emb.embed("payment ledger")
        dense = pg.dense_search(qv, 10, ["analyst"])
        assert len(dense) == 10 and all(d not in acl for d, _ in dense)
        res = pg.hybrid_search("payment ledger", qv, IndexFamily.TEXT, ["analyst"], top_k=10)
        assert res and all(r["doc_id"] not in acl for r in res)
        sec = pg.hybrid_search("payment ledger", qv, IndexFamily.TEXT, ["secops"], top_k=10)
        assert any(r["doc_id"] in acl for r in sec)


def test_policy_epoch_is_durable_across_processes(app_dsn, tenants):
    a, _ = tenants
    emb = TestHashingEmbedder(DIM)
    with PgVectorIndex(app_dsn, _meta(a)) as w, PgVectorIndex(app_dsn, _meta(a)) as r:
        w.add_documents(_docs([("p1", "payroll export"), ("p2", "payroll ledger")], emb))
        qv = emb.embed("payroll")
        before = [x["doc_id"] for x in r.hybrid_search("payroll", qv, IndexFamily.TEXT, ["analyst"])]
        assert sorted(before) == ["p1", "p2"]
        w.add_documents(_docs([("p1", "payroll export")], emb, acl={"p1": ["hr"]}))
        w.revoke_policy_epoch()  # another "process" revokes; r must not serve its cached result
        after = [x["doc_id"] for x in r.hybrid_search("payroll", qv, IndexFamily.TEXT, ["analyst"])]
        assert after == ["p2"] and r.metadata.policy_epoch == w.metadata.policy_epoch


def test_dimension_and_family_mismatches_are_hard_errors(app_dsn, tenants):
    a, _ = tenants
    emb = TestHashingEmbedder(DIM)
    with PgVectorIndex(app_dsn, _meta(a)) as pg:
        with pytest.raises(DimensionMismatchError):
            pg.add_document(VectorDocument("x", "x", [0.1] * (DIM + 1), IndexFamily.TEXT))
        with pytest.raises(IncompatibleEmbeddingFamilyError):
            pg.add_document(VectorDocument("x", "x", emb.embed("x"), IndexFamily.GRAPH_STRUCTURE))
        with pytest.raises(DimensionMismatchError):
            pg.hybrid_search("x", [0.1] * 3, IndexFamily.TEXT, [])
        with pytest.raises(IncompatibleEmbeddingFamilyError):
            pg.hybrid_search("x", emb.embed("x"), IndexFamily.GRAPH_STRUCTURE, [])
    with pytest.raises(DimensionMismatchError):  # the registry pins the dimension of an existing index
        PgVectorIndex(app_dsn, _meta(a, dim=DIM * 2))
