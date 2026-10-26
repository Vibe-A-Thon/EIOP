"""Durable tenant-partitioned vector store on PostgreSQL + pgvector (CRA-025.6, X-41).

Isolation is layered so that a bug in one layer does not leak another tenant's vectors:

1. **Physical partitioning** - every table is ``PARTITION BY LIST (tenant_id)``; a tenant's rows live
   in its own partitions, created only by :meth:`PgVectorAdmin.provision_tenant`. Writes for an
   unprovisioned tenant fail (``TenantNotProvisioned``) instead of landing in a shared table.
2. **Row-level security** - ``ENABLE`` + ``FORCE ROW LEVEL SECURITY`` with a policy
   ``tenant_id = current_setting('eoip.tenant_id')`` for reads *and* writes (``WITH CHECK``). The
   application role is not the table owner and has no ``BYPASSRLS``.
3. **Transaction-scoped tenant binding** - :class:`PgVectorIndex` sets ``eoip.tenant_id`` with
   ``set_config(..., is_local => true)`` inside every transaction, from the index metadata's scope.

Retrieval mirrors :class:`~eoip.retrieval.hybrid_vector_service.TenantVectorIndex`: dense cosine
kNN (HNSW partial index per tenant/index, ``vector_cosine_ops``, iterative scan so ACL filtering
does not starve results), BM25 computed in SQL over a per-tenant postings table with the same
tokeniser and constants (k1 = 1.2, b = 0.75), ACL pre-filtering in both candidate queries, and the
shared :func:`~eoip.retrieval.hybrid_vector_service.rrf_fuse` (k = 60) with the graph-centrality
signal and delivery post-filter. The policy epoch is stored in the database, so a revocation in
one process invalidates cached results in every process.
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from typing import Any, Self

from eoip.retrieval.hybrid_vector_service import (
    DimensionMismatchError,
    IncompatibleEmbeddingFamilyError,
    IndexFamily,
    IndexMetadata,
    VectorDocument,
    rrf_fuse,
)

SCHEMA = "eoip_vec"
_TOKEN = re.compile(r"\w+")
_ROLE_RE = re.compile(r"^[a-z_][a-z0-9_]{0,62}$")


class TenantNotProvisioned(LookupError):
    """The tenant has no partitions (or the index is not registered) in the vector store."""


def _psycopg():
    try:
        import psycopg
        from psycopg import sql
    except ImportError as exc:  # pragma: no cover - exercised when the extra is absent
        raise RuntimeError("pgvector store needs psycopg: pip install 'eoip[pgvector]'") from exc
    return psycopg, sql


def _suffix(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:16]


def _vec(v: list[float]) -> str:
    return "[" + ",".join(repr(float(x)) for x in v) + "]"


def tokenize(text: str) -> list[str]:
    """Same tokeniser as the in-process BM25 index."""
    return _TOKEN.findall(text.lower())


class PgVectorAdmin:
    """DDL side: schema install, tenant partitions, per-index HNSW indexes. Run with an owner role."""

    def __init__(self, conninfo: str) -> None:
        self.conninfo = conninfo

    def _run(self, *statements: Any) -> None:
        psycopg, _ = _psycopg()
        with psycopg.connect(self.conninfo, autocommit=True) as con:
            for st in statements:
                con.execute(st)

    def install(self, app_role: str) -> None:
        if not _ROLE_RE.match(app_role):
            raise ValueError("app_role must be a plain lower-case identifier")
        _, sql = _psycopg()
        s, r = sql.Identifier(SCHEMA), sql.Identifier(app_role)
        stmts = [
            sql.SQL("CREATE EXTENSION IF NOT EXISTS vector"),
            sql.SQL("CREATE SCHEMA IF NOT EXISTS {}").format(s),
            sql.SQL("""CREATE TABLE IF NOT EXISTS {}.indexes (
                tenant_id text NOT NULL, index_id text NOT NULL, family text NOT NULL, dimension int NOT NULL,
                metadata jsonb NOT NULL, policy_epoch bigint NOT NULL DEFAULT 1,
                PRIMARY KEY (tenant_id, index_id)) PARTITION BY LIST (tenant_id)""").format(s),
            sql.SQL("""CREATE TABLE IF NOT EXISTS {}.docs (
                tenant_id text NOT NULL, index_id text NOT NULL, doc_id text NOT NULL, body text NOT NULL,
                embedding vector NOT NULL, acl_roles text[] NOT NULL DEFAULT '{{}}', metadata jsonb NOT NULL DEFAULT '{{}}',
                centrality double precision NOT NULL DEFAULT 0, doc_len int NOT NULL,
                PRIMARY KEY (tenant_id, index_id, doc_id)) PARTITION BY LIST (tenant_id)""").format(s),
            sql.SQL("""CREATE TABLE IF NOT EXISTS {}.postings (
                tenant_id text NOT NULL, index_id text NOT NULL, term text NOT NULL, doc_id text NOT NULL,
                tf int NOT NULL, PRIMARY KEY (tenant_id, index_id, term, doc_id)) PARTITION BY LIST (tenant_id)""").format(s),
            sql.SQL("GRANT USAGE ON SCHEMA {} TO {}").format(s, r),
        ]
        for t in ("indexes", "docs", "postings"):
            tbl = sql.Identifier(SCHEMA, t)
            pol = sql.Identifier(f"{t}_tenant_isolation")
            stmts += [
                sql.SQL("ALTER TABLE {} ENABLE ROW LEVEL SECURITY").format(tbl),
                sql.SQL("ALTER TABLE {} FORCE ROW LEVEL SECURITY").format(tbl),
                sql.SQL("DROP POLICY IF EXISTS {} ON {}").format(pol, tbl),
                sql.SQL("CREATE POLICY {} ON {} USING (tenant_id = current_setting('eoip.tenant_id', true)) "
                        "WITH CHECK (tenant_id = current_setting('eoip.tenant_id', true))").format(pol, tbl),
                sql.SQL("GRANT SELECT, INSERT, UPDATE, DELETE ON {} TO {}").format(tbl, r),
            ]
        self._run(*stmts)

    def provision_tenant(self, tenant_id: str) -> None:
        _, sql = _psycopg()
        sfx = _suffix(tenant_id)
        stmts = []
        for t in ("indexes", "docs", "postings"):
            part = sql.Identifier(SCHEMA, f"{t}_t_{sfx}")
            stmts += [
                sql.SQL("CREATE TABLE IF NOT EXISTS {} PARTITION OF {} FOR VALUES IN ({})").format(
                    part, sql.Identifier(SCHEMA, t), sql.Literal(tenant_id)),
                sql.SQL("ALTER TABLE {} ENABLE ROW LEVEL SECURITY").format(part),
                sql.SQL("ALTER TABLE {} FORCE ROW LEVEL SECURITY").format(part),
            ]
        self._run(*stmts)

    def provision_index(self, meta: IndexMetadata, m: int = 16, ef_construction: int = 64) -> None:
        """Register the index and build its HNSW partial index inside the tenant's partition."""
        _, sql = _psycopg()
        sfx = _suffix(meta.scope)
        part = sql.Identifier(SCHEMA, f"docs_t_{sfx}")
        name = sql.Identifier(f"hnsw_{_suffix(meta.scope, meta.index_id)}")
        ops = {"COSINE": "vector_cosine_ops", "L2": "vector_l2_ops", "IP": "vector_ip_ops"}[meta.metric.upper()]
        self._run(
            sql.SQL("CREATE INDEX IF NOT EXISTS {} ON {} USING hnsw ((embedding::vector({})) {}) "
                    "WITH (m = {}, ef_construction = {}) WHERE index_id = {}").format(
                name, part, sql.Literal(int(meta.dimension)), sql.SQL(ops), sql.Literal(int(m)),
                sql.Literal(int(ef_construction)), sql.Literal(meta.index_id)),
        )


class PgVectorIndex:
    """A tenant's index in the pgvector store, with the ``TenantVectorIndex`` search API."""

    def __init__(self, conninfo: str, metadata: IndexMetadata) -> None:
        psycopg, _ = _psycopg()
        self.metadata = metadata
        self.tenant_id = metadata.scope
        self._con = psycopg.connect(conninfo)
        self._cache: dict[tuple[str, int], list[dict[str, Any]]] = {}
        with self._tx() as cur:
            try:
                cur.execute(
                    f"INSERT INTO {SCHEMA}.indexes (tenant_id, index_id, family, dimension, metadata) "
                    "VALUES (%s, %s, %s, %s, %s) ON CONFLICT (tenant_id, index_id) DO NOTHING",
                    (self.tenant_id, metadata.index_id, metadata.family.value, metadata.dimension,
                     json.dumps(metadata.to_dict())))
            except psycopg.errors.CheckViolation as exc:  # no partition holds this tenant
                raise TenantNotProvisioned(f"tenant {self.tenant_id!r} is not provisioned") from exc
            cur.execute(f"SELECT family, dimension FROM {SCHEMA}.indexes WHERE index_id = %s",
                        (metadata.index_id,))
            family, dim = cur.fetchone()
        if family != metadata.family.value or dim != metadata.dimension:
            raise DimensionMismatchError(
                f"index {metadata.index_id} is registered as {family}/{dim}, not "
                f"{metadata.family.value}/{metadata.dimension} (CRA-025.2)")

    # -- plumbing -------------------------------------------------------------------------------
    def _tx(self):
        index = self

        class _Tx:
            def __enter__(self_inner):
                self_inner.tx = index._con.transaction()
                self_inner.tx.__enter__()
                self_inner.cur = index._con.cursor()
                self_inner.cur.execute("SELECT set_config('eoip.tenant_id', %s, true)", (index.tenant_id,))
                return self_inner.cur

            def __exit__(self_inner, *exc):
                self_inner.cur.close()
                return self_inner.tx.__exit__(*exc)

        return _Tx()

    def close(self) -> None:
        self._con.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @staticmethod
    def _visible(acl: list[str], roles: list[str]) -> bool:
        return not acl or any(r in roles for r in acl)

    # -- writes ---------------------------------------------------------------------------------
    def add_document(self, doc: VectorDocument) -> None:
        self.add_documents([doc])

    def add_documents(self, docs: list[VectorDocument]) -> None:
        psycopg, _ = _psycopg()
        for doc in docs:
            if len(doc.vector) != self.metadata.dimension:
                raise DimensionMismatchError(
                    f"Vector dimension {len(doc.vector)} does not match index dimension "
                    f"{self.metadata.dimension} (CRA-025.2)")
            if doc.family != self.metadata.family:
                raise IncompatibleEmbeddingFamilyError(
                    f"Cannot add document family {doc.family} into {self.metadata.family} index (CRA-025.8)")
        iid = self.metadata.index_id
        try:
            with self._tx() as cur:
                for doc in docs:
                    tokens = tokenize(doc.text)
                    cur.execute(f"DELETE FROM {SCHEMA}.postings WHERE index_id = %s AND doc_id = %s", (iid, doc.doc_id))
                    cur.execute(
                        f"INSERT INTO {SCHEMA}.docs (tenant_id, index_id, doc_id, body, embedding, acl_roles, metadata,"
                        " centrality, doc_len) VALUES (%s, %s, %s, %s, %s::vector, %s, %s, %s, %s)"
                        " ON CONFLICT (tenant_id, index_id, doc_id) DO UPDATE SET body = EXCLUDED.body,"
                        " embedding = EXCLUDED.embedding, acl_roles = EXCLUDED.acl_roles, metadata = EXCLUDED.metadata,"
                        " centrality = EXCLUDED.centrality, doc_len = EXCLUDED.doc_len",
                        (self.tenant_id, iid, doc.doc_id, doc.text, _vec(doc.vector), list(doc.acl_allow_roles),
                         json.dumps(doc.metadata), float(doc.graph_centrality), len(tokens)))
                    cur.executemany(
                        f"INSERT INTO {SCHEMA}.postings (tenant_id, index_id, term, doc_id, tf) VALUES (%s, %s, %s, %s, %s)",
                        [(self.tenant_id, iid, t, doc.doc_id, n) for t, n in Counter(tokens).items()])
        except psycopg.errors.CheckViolation as exc:
            raise TenantNotProvisioned(f"tenant {self.tenant_id!r} is not provisioned") from exc
        self._cache.clear()

    def remove_document(self, doc_id: str) -> bool:
        iid = self.metadata.index_id
        with self._tx() as cur:
            cur.execute(f"DELETE FROM {SCHEMA}.postings WHERE index_id = %s AND doc_id = %s", (iid, doc_id))
            cur.execute(f"DELETE FROM {SCHEMA}.docs WHERE index_id = %s AND doc_id = %s", (iid, doc_id))
            removed = cur.rowcount > 0
        self._cache.clear()
        return removed

    def revoke_policy_epoch(self) -> None:
        """Bump the durable policy epoch; every process's cached results for this index become stale."""
        with self._tx() as cur:
            cur.execute(f"UPDATE {SCHEMA}.indexes SET policy_epoch = policy_epoch + 1 WHERE index_id = %s "
                        "RETURNING policy_epoch", (self.metadata.index_id,))
            self.metadata.policy_epoch = int(cur.fetchone()[0])
        self._cache.clear()

    def count(self) -> int:
        with self._tx() as cur:
            cur.execute(f"SELECT count(*) FROM {SCHEMA}.docs WHERE index_id = %s", (self.metadata.index_id,))
            return int(cur.fetchone()[0])

    # -- reads ----------------------------------------------------------------------------------
    def bm25_search(self, query: str, top_k: int = 20, caller_roles: list[str] | None = None) -> list[tuple[str, float]]:
        """BM25 (k1 = 1.2, b = 0.75, idf = ln((N - df + .5) / (df + .5) + 1)) computed in SQL.

        ``caller_roles=None`` ranks over every document (parity with the in-process index); a role list
        applies the ACL pre-filter inside the query.
        """
        terms = tokenize(query)
        if not terms:
            return []
        with self._tx() as cur:
            return self._bm25(cur, terms, top_k, caller_roles)

    def _bm25(self, cur: Any, terms: list[str], top_k: int, roles: list[str] | None) -> list[tuple[str, float]]:
        acl = "" if roles is None else " AND (cardinality(d.acl_roles) = 0 OR d.acl_roles && %(roles)s)"
        cur.execute(
            f"""WITH q AS (SELECT unnest(%(terms)s::text[]) AS term),
                    st AS (SELECT count(*)::float8 AS n, avg(doc_len)::float8 AS avgdl
                           FROM {SCHEMA}.docs WHERE index_id = %(iid)s),
                    df AS (SELECT term, count(*)::float8 AS df FROM {SCHEMA}.postings
                           WHERE index_id = %(iid)s AND term IN (SELECT term FROM q) GROUP BY term)
                SELECT p.doc_id,
                       sum(ln((st.n - df.df + 0.5) / (df.df + 0.5) + 1.0) * (p.tf * 2.2)
                           / (p.tf + 1.2 * (0.25 + 0.75 * d.doc_len / greatest(st.avgdl, 1e-9)))) AS score
                FROM q JOIN df USING (term)
                JOIN {SCHEMA}.postings p ON p.index_id = %(iid)s AND p.term = q.term
                JOIN {SCHEMA}.docs d ON d.index_id = p.index_id AND d.doc_id = p.doc_id
                CROSS JOIN st
                WHERE true{acl}
                GROUP BY p.doc_id ORDER BY score DESC, p.doc_id LIMIT %(k)s""",
            {"terms": terms, "iid": self.metadata.index_id, "k": int(top_k), "roles": list(roles or [])})
        return [(r[0], float(r[1])) for r in cur.fetchall()]

    def dense_search(self, query_vector: list[float], top_k: int, caller_roles: list[str], cur: Any = None,
                     ef_search: int | None = None) -> list[tuple[str, float]]:
        if cur is None:
            with self._tx() as c:
                return self.dense_search(query_vector, top_k, caller_roles, c, ef_search)
        dim = int(self.metadata.dimension)
        cur.execute("SELECT set_config('hnsw.ef_search', %s, true), set_config('hnsw.iterative_scan', 'relaxed_order', true)",
                    (str(max(40, ef_search or top_k * 4)),))
        cur.execute(
            f"""SELECT doc_id, 1 - (embedding::vector({dim}) <=> %(q)s::vector({dim})) AS sim
                FROM {SCHEMA}.docs
                WHERE tenant_id = %(tid)s AND index_id = %(iid)s
                  AND (cardinality(acl_roles) = 0 OR acl_roles && %(roles)s)
                ORDER BY embedding::vector({dim}) <=> %(q)s::vector({dim}) LIMIT %(k)s""",
            {"q": _vec(query_vector), "iid": self.metadata.index_id, "roles": list(caller_roles), "k": int(top_k),
             "tid": self.tenant_id})
        return sorted(((r[0], float(r[1])) for r in cur.fetchall()), key=lambda kv: -kv[1])

    def explain_dense(self, query_vector: list[float], top_k: int = 10, force_index: bool = True) -> str:
        """EXPLAIN of the dense query, showing the tenant partition's HNSW index can serve it.

        With ``force_index`` sequential scans, bitmap scans and explicit sorts are disabled for this transaction: on small test
        partitions the planner otherwise (correctly) prefers an exact sort, which proves nothing about the
        index. Partition pruning to the caller's tenant happens at plan time via the explicit predicate.
        """
        dim = int(self.metadata.dimension)
        with self._tx() as cur:
            if force_index:
                cur.execute("SET LOCAL enable_seqscan = off")
                cur.execute("SET LOCAL enable_bitmapscan = off")
                cur.execute("SET LOCAL enable_sort = off")
            cur.execute(
                f"EXPLAIN SELECT doc_id FROM {SCHEMA}.docs WHERE tenant_id = %(tid)s AND index_id = %(iid)s "
                f"ORDER BY embedding::vector({dim}) <=> %(q)s::vector({dim}) LIMIT %(k)s",
                {"q": _vec(query_vector), "iid": self.metadata.index_id, "k": int(top_k), "tid": self.tenant_id})
            return "\n".join(r[0] for r in cur.fetchall())

    def hybrid_search(
        self,
        query_text: str,
        query_vector: list[float],
        query_family: IndexFamily,
        caller_roles: list[str],
        top_k: int = 10,
        rrf_k: int = 60,
        use_graph_centrality: bool = True,
    ) -> list[dict[str, Any]]:
        if query_family != self.metadata.family:
            raise IncompatibleEmbeddingFamilyError(
                f"Query family {query_family} is incompatible with index family {self.metadata.family} (CRA-025.8)")
        if len(query_vector) != self.metadata.dimension:
            raise DimensionMismatchError(
                f"Query vector dimension {len(query_vector)} != index dimension {self.metadata.dimension}")
        with self._tx() as cur:
            cur.execute(f"SELECT policy_epoch FROM {SCHEMA}.indexes WHERE index_id = %s", (self.metadata.index_id,))
            row = cur.fetchone()
            if row is None:
                raise TenantNotProvisioned(f"index {self.metadata.index_id!r} is not registered for this tenant")
            epoch = int(row[0])
            key = (hashlib.sha256(json.dumps([query_text, sorted(caller_roles), list(query_vector), top_k, rrf_k,
                                              bool(use_graph_centrality)]).encode("utf-8")).hexdigest(), epoch)
            if key in self._cache:
                return self._cache[key]
            dense = self.dense_search(query_vector, top_k * 2, caller_roles, cur)
            terms = tokenize(query_text)
            sparse = self._bm25(cur, terms, top_k * 2, caller_roles) if terms else []
            ids = sorted({d for d, _ in dense} | {d for d, _ in sparse})
            docs: dict[str, VectorDocument] = {}
            if ids:
                cur.execute(f"SELECT doc_id, body, acl_roles, metadata, centrality FROM {SCHEMA}.docs "
                            "WHERE index_id = %s AND doc_id = ANY(%s)", (self.metadata.index_id, ids))
                for doc_id, body, acl, meta, cent in cur.fetchall():
                    docs[doc_id] = VectorDocument(doc_id, body, [], self.metadata.family, list(acl or []),
                                                  meta or {}, float(cent))
        self.metadata.policy_epoch = epoch
        results = rrf_fuse(dense, sparse, docs, caller_roles, self.metadata.family, top_k=top_k, rrf_k=rrf_k,
                           use_graph_centrality=use_graph_centrality)
        self._cache[key] = results
        return results
