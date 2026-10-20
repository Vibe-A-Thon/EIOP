"""Runtime per-layer tenant isolation (SR-TEN-003).

``isolation.py`` records *where* each tenant lives on every layer; this module enforces it at
runtime for the platform's embedded backends. ``TenantLayers.for_tenant(tenant_id)`` returns a
handle whose every layer resolves resources only from that tenant's ``IsolationPlacement``:

==================  ==========================================================================
graph               canonical URNs / tenant graph IRI via ``TenantNamespace`` (cross-tenant ids raise)
vector              collection = placement ``vector_collection``; search sees only that collection
search              one ``InMemorySearchIndex`` per placement ``search_index``
relational          SQLite: a dedicated schema (connection) per placement value; an engine-level
                    authorizer refuses ATTACH/DETACH so a statement cannot reach another schema.
                    for a shared (POOL) schema the tenant gets its own logical schema inside it
object              filesystem bucket/prefix; path traversal outside the prefix is refused
event topics        publish/subscribe only on the tenant's topic
secrets             path-scoped secret store
KMS keys            per-tenant AES-256-GCM data key (HKDF from the master key and ``kms_key``);
                    ciphertext is bound to the tenant (AAD) and cannot be opened by another tenant
caches              key-prefixed views over a shared cache mapping
logs                records are routed to the tenant's ``log_stream``; reads are per stream
backups             encrypted with the tenant key into its ``backup_bucket``; restore refuses a
                    backup made for another tenant
exports             written under ``export_prefix``; another tenant cannot list or read them
==================  ==========================================================================

Managed external backends (Neo4j/Qdrant/Postgres/S3/KMS) remain an external gate: they must apply
the same placement values; these embedded implementations are the reference behaviour and what the
single-node / air-gapped profile runs.
"""

from __future__ import annotations

import json
import logging
import os
import sqlite3
from collections import defaultdict
from collections.abc import Callable, MutableMapping
from pathlib import Path
from typing import Any

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

from eoip.tenancy.isolation import IsolationRegistry


class IsolationViolation(PermissionError):
    """A tenant handle tried to reach another tenant's resource (SR-TEN-003)."""


class TenantLayers:
    def __init__(self, registry: IsolationRegistry, *, root: Path, master_key: bytes) -> None:
        if len(master_key) < 32:
            raise ValueError("master key must be at least 32 bytes")
        self.registry = registry
        self.root = Path(root)
        self._master = master_key
        self.vectors: dict[str, dict[str, tuple[list[float], dict]]] = defaultdict(dict)
        self.search_indexes: dict[str, Any] = {}
        self.search_docs: dict[str, dict[str, tuple[str, dict]]] = {}
        self.topics: dict[str, list[dict]] = defaultdict(list)
        self.subscribers: dict[str, list[Callable[[dict], None]]] = defaultdict(list)
        self.secrets: dict[str, str] = {}
        self.cache: MutableMapping[str, Any] = {}
        self.log_streams: dict[str, list[dict]] = defaultdict(list)
        self.schemas: dict[str, sqlite3.Connection] = {}

    def for_tenant(self, tenant_id: str) -> TenantHandle:
        return TenantHandle(self, tenant_id, self.registry.get(tenant_id))

    def log_handler(self) -> logging.Handler:
        layers = self

        class _Router(logging.Handler):
            def emit(self, record: logging.LogRecord) -> None:
                tenant = getattr(record, "tenant_id", None)
                try:
                    stream = layers.for_tenant(tenant)._p("log_stream") if tenant else "_platform"
                except Exception:  # noqa: BLE001 - unknown tenant -> platform stream, never another tenant's
                    stream = "_platform"
                layers.log_streams[stream].append({"tenant_id": tenant, "message": record.getMessage()})

        return _Router()


class TenantHandle:
    def __init__(self, layers: TenantLayers, tenant_id: str, placement: Any) -> None:
        self.layers, self.tenant_id, self.placement = layers, tenant_id, placement

    def _p(self, layer: str) -> str:
        """Resolved resource for a layer. Layers the isolation model dedicates use the placement
        value as is; shared (logically isolated) layers are namespaced by tenant inside it, so two
        POOL/BRIDGE tenants sharing a cache prefix or topic still never see each other's entries."""
        value = self.placement.layer(layer)
        if layer in self.placement.model.dedicated_layers:
            return value
        return f"{value}#{self.tenant_id}"

    # -- graph ---------------------------------------------------------------
    def graph_id(self, raw_id: str) -> str:
        from eoip.tenancy.isolation_hardened import TenantNamespace

        return TenantNamespace.format_canonical_id(self.tenant_id, raw_id)

    # -- vector --------------------------------------------------------------
    def vector_upsert(self, doc_id: str, vector: list[float], payload: dict | None = None) -> None:
        self.layers.vectors[self._p("vector_collection")][doc_id] = (list(vector), dict(payload or {}))

    def vector_items(self) -> dict[str, tuple[list[float], dict]]:
        return dict(self.layers.vectors.get(self._p("vector_collection"), {}))

    def vector_delete(self, doc_id: str) -> bool:
        return self.layers.vectors.get(self._p("vector_collection"), {}).pop(doc_id, None) is not None

    def vector_search(self, vector: list[float], k: int = 5, *, collection: str | None = None) -> list[str]:
        own = self._p("vector_collection")
        if collection is not None and collection != own:
            raise IsolationViolation(f"collection {collection} does not belong to tenant {self.tenant_id}")
        docs = self.layers.vectors.get(own, {})

        def score(v: list[float]) -> float:
            return sum(a * b for a, b in zip(vector, v, strict=False))
        return [d for d, _ in sorted(docs.items(), key=lambda kv: -score(kv[1][0]))[:k]]

    # -- search --------------------------------------------------------------
    def search_index(self) -> Any:
        from eoip.retrieval.vectors import InMemorySearchIndex

        name = self._p("search_index")
        return self.layers.search_indexes.setdefault(name, InMemorySearchIndex())

    def search_add(self, doc_id: str, text: str, meta: dict | None = None) -> None:
        self.search_index().add(doc_id, text)
        self.layers.search_docs.setdefault(self._p("search_index"), {})[doc_id] = (text, dict(meta or {}))

    def search_remove(self, doc_id: str) -> None:
        self.search_index().remove(doc_id)
        self.layers.search_docs.get(self._p("search_index"), {}).pop(doc_id, None)

    def search_docs(self) -> dict[str, tuple[str, dict]]:
        return dict(self.layers.search_docs.get(self._p("search_index"), {}))

    # -- relational (dedicated schema + engine-level authorizer) ---------------
    def sql(self, statement: str, params: tuple = ()) -> list[tuple]:
        """Run SQL in the tenant's own schema. The connection only ever opens that schema, and an
        engine-level authorizer refuses ATTACH/DETACH so no statement can reach another schema."""
        schema = self._p("relational_schema")
        db = self.layers.schemas.get(schema)
        if db is None:
            db = sqlite3.connect(":memory:", check_same_thread=False)

            def authorizer(action, *_):
                if action in (sqlite3.SQLITE_ATTACH, sqlite3.SQLITE_DETACH):
                    return sqlite3.SQLITE_DENY
                return sqlite3.SQLITE_OK
            db.set_authorizer(authorizer)
            self.layers.schemas[schema] = db
        try:
            rows = db.execute(statement, params).fetchall()
            db.commit()
            return rows
        except sqlite3.DatabaseError as exc:
            if "not authorized" in str(exc):
                raise IsolationViolation(f"relational access outside schema {schema}") from exc
            raise

    # -- object storage ------------------------------------------------------
    def _object_path(self, key: str) -> Path:
        base = (self.layers.root / "objects" / self._p("object_prefix")).resolve()
        target = (base / key).resolve()
        if base != target and base not in target.parents:
            raise IsolationViolation(f"object key {key!r} escapes the tenant prefix")
        return target

    def put_object(self, key: str, data: bytes) -> None:
        path = self._object_path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)

    def get_object(self, key: str) -> bytes:
        return self._object_path(key).read_bytes()

    def list_objects(self, prefix: str = "") -> list[str]:
        base = (self.layers.root / "objects" / self._p("object_prefix")).resolve()
        if not base.exists():
            return []
        return sorted(str(p.relative_to(base)) for p in base.rglob("*") if p.is_file()
                      and str(p.relative_to(base)).startswith(prefix))

    def delete_object(self, key: str) -> bool:
        path = self._object_path(key)
        if path.exists():
            path.unlink()
            return True
        return False

    # -- events --------------------------------------------------------------
    def publish(self, event: dict, *, topic: str | None = None) -> None:
        own = self._p("event_topic")
        if topic is not None and topic != own:
            raise IsolationViolation(f"topic {topic} does not belong to tenant {self.tenant_id}")
        msg = {**event, "tenant_id": self.tenant_id}
        self.layers.topics[own].append(msg)
        for fn in self.layers.subscribers[own]:
            fn(msg)

    def subscribe(self, fn: Callable[[dict], None], *, topic: str | None = None) -> None:
        own = self._p("event_topic")
        if topic is not None and topic != own:
            raise IsolationViolation(f"topic {topic} does not belong to tenant {self.tenant_id}")
        self.layers.subscribers[own].append(fn)

    # -- secrets -------------------------------------------------------------
    def _secret_key(self, name: str) -> str:
        if "/" in name or ".." in name:
            raise IsolationViolation("secret names are relative to the tenant path")
        return f"{self._p('secrets_path')}/{name}"

    def put_secret(self, name: str, value: str) -> None:
        self.layers.secrets[self._secret_key(name)] = value

    def get_secret(self, name: str) -> str:
        return self.layers.secrets[self._secret_key(name)]

    # -- KMS -----------------------------------------------------------------
    def _data_key(self) -> bytes:
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=None,
                    info=f"eoip-kms:{self._p('kms_key')}".encode()).derive(self.layers._master)

    def encrypt(self, plaintext: bytes) -> bytes:
        nonce = os.urandom(12)
        return nonce + AESGCM(self._data_key()).encrypt(nonce, plaintext, self.tenant_id.encode())

    def decrypt(self, blob: bytes) -> bytes:
        try:
            return AESGCM(self._data_key()).decrypt(blob[:12], blob[12:], self.tenant_id.encode())
        except InvalidTag as exc:
            raise IsolationViolation("ciphertext was not produced for this tenant's key") from exc

    # -- caches --------------------------------------------------------------
    def _ck(self, key: str) -> str:
        return f"{self._p('cache_key_prefix')}:{key}"

    def cache_set(self, key: str, value: Any) -> None:
        self.layers.cache[self._ck(key)] = value

    def cache_get(self, key: str, default: Any = None) -> Any:
        return self.layers.cache.get(self._ck(key), default)

    def cache_items(self) -> dict[str, Any]:
        prefix = self._ck("")
        return {k[len(prefix):]: v for k, v in self.layers.cache.items() if k.startswith(prefix)}

    def cache_delete(self, key: str) -> bool:
        return self.layers.cache.pop(self._ck(key), None) is not None

    def cache_clear(self) -> int:
        prefix = self._ck("")
        mine = [k for k in self.layers.cache if k.startswith(prefix)]
        for k in mine:
            del self.layers.cache[k]
        return len(mine)

    # -- logs ----------------------------------------------------------------
    def read_logs(self, *, stream: str | None = None) -> list[dict]:
        own = self._p("log_stream")
        if stream is not None and stream != own:
            raise IsolationViolation(f"log stream {stream} does not belong to tenant {self.tenant_id}")
        return list(self.layers.log_streams.get(own, []))

    # -- backups -------------------------------------------------------------
    def backup(self, name: str, state: dict) -> Path:
        path = self.layers.root / "backups" / self._p("backup_bucket") / f"{name}.bak"
        path.parent.mkdir(parents=True, exist_ok=True)
        header = json.dumps({"tenant_id": self.tenant_id}).encode()
        path.write_bytes(header + b"\n" + self.encrypt(json.dumps(state, sort_keys=True).encode()))
        return path

    def list_backups(self) -> list[Path]:
        bucket = self.layers.root / "backups" / self._p("backup_bucket")
        return sorted(bucket.glob("*.bak")) if bucket.exists() else []

    def restore(self, path: Path) -> dict:
        path = Path(path).resolve()
        bucket = (self.layers.root / "backups" / self._p("backup_bucket")).resolve()
        if bucket not in path.parents:
            raise IsolationViolation("backup is not in this tenant's backup bucket")
        header, blob = path.read_bytes().split(b"\n", 1)
        if json.loads(header).get("tenant_id") != self.tenant_id:
            raise IsolationViolation("backup was made for another tenant")
        return json.loads(self.decrypt(blob))

    # -- exports -------------------------------------------------------------
    def _export_dir(self) -> Path:
        return self.layers.root / "exports" / self._p("export_prefix")

    def write_export(self, name: str, data: bytes) -> Path:
        if "/" in name or ".." in name:
            raise IsolationViolation("export names are relative to the tenant prefix")
        d = self._export_dir()
        d.mkdir(parents=True, exist_ok=True)
        (d / name).write_bytes(data)
        return d / name

    def list_exports(self) -> list[str]:
        d = self._export_dir()
        return sorted(p.name for p in d.iterdir()) if d.exists() else []

    def delete_export(self, name: str) -> bool:
        if "/" in name or ".." in name:
            raise IsolationViolation("export names are relative to the tenant prefix")
        path = self._export_dir() / name
        if path.exists():
            path.unlink()
            return True
        return False

    def read_export(self, name: str) -> bytes:
        if "/" in name or ".." in name:
            raise IsolationViolation("export names are relative to the tenant prefix")
        return (self._export_dir() / name).read_bytes()
