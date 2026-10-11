"""Shared Saved Queries with version history.

Named queries that teams share, with full version tracking,
fork/clone support, and usage analytics.
"""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


@dataclass
class QueryVersion:
    version: int
    query_text: str
    parameters: dict[str, Any]
    author: str
    change_note: str = ""
    created_at: float = field(default_factory=time.time)


@dataclass
class SavedQuery:
    query_id: str
    name: str
    description: str
    query_text: str
    query_language: str
    parameters: dict[str, Any]
    author: str
    workspace_id: str | None = None
    tags: list[str] = field(default_factory=list)
    is_public: bool = False
    versions: list[QueryVersion] = field(default_factory=list)
    execution_count: int = 0
    last_executed_at: float | None = None
    last_executed_by: str | None = None
    forked_from: str | None = None
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    @property
    def current_version(self) -> int:
        return len(self.versions)

    def to_dict(self) -> dict[str, Any]:
        return {
            "query_id": self.query_id,
            "name": self.name,
            "description": self.description,
            "query_text": self.query_text,
            "query_language": self.query_language,
            "parameters": self.parameters,
            "author": self.author,
            "workspace_id": self.workspace_id,
            "tags": self.tags,
            "is_public": self.is_public,
            "current_version": self.current_version,
            "execution_count": self.execution_count,
            "last_executed_at": self.last_executed_at,
            "last_executed_by": self.last_executed_by,
            "forked_from": self.forked_from,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class SharedQueryStore:
    """Thread-safe shared query storage with versioning."""

    def __init__(self) -> None:
        self._queries: dict[str, SavedQuery] = {}
        self._by_workspace: dict[str, list[str]] = {}
        self._by_author: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    def save(self, name: str, query_text: str, query_language: str,
             author: str, description: str = "",
             parameters: dict[str, Any] | None = None,
             workspace_id: str | None = None,
             tags: list[str] | None = None,
             is_public: bool = False) -> SavedQuery:
        sq = SavedQuery(
            query_id=uuid.uuid4().hex[:12],
            name=name,
            description=description,
            query_text=query_text,
            query_language=query_language,
            parameters=parameters or {},
            author=author,
            workspace_id=workspace_id,
            tags=tags or [],
            is_public=is_public,
        )
        sq.versions.append(QueryVersion(
            version=1,
            query_text=query_text,
            parameters=sq.parameters,
            author=author,
            change_note="Initial version",
        ))
        with self._lock:
            self._queries[sq.query_id] = sq
            self._by_author.setdefault(author, []).append(sq.query_id)
            if workspace_id:
                self._by_workspace.setdefault(workspace_id, []).append(sq.query_id)
        return sq

    def update(self, query_id: str, query_text: str, author: str,
               change_note: str = "") -> SavedQuery | None:
        with self._lock:
            sq = self._queries.get(query_id)
            if sq is None:
                return None
            sq.query_text = query_text
            sq.updated_at = time.time()
            sq.versions.append(QueryVersion(
                version=len(sq.versions) + 1,
                query_text=query_text,
                parameters=sq.parameters,
                author=author,
                change_note=change_note,
            ))
            return sq

    def get(self, query_id: str) -> SavedQuery | None:
        with self._lock:
            return self._queries.get(query_id)

    def get_version(self, query_id: str, version: int) -> QueryVersion | None:
        with self._lock:
            sq = self._queries.get(query_id)
            if sq is None or version < 1 or version > len(sq.versions):
                return None
            return sq.versions[version - 1]

    def record_execution(self, query_id: str, executed_by: str) -> bool:
        with self._lock:
            sq = self._queries.get(query_id)
            if sq is None:
                return False
            sq.execution_count += 1
            sq.last_executed_at = time.time()
            sq.last_executed_by = executed_by
            return True

    def fork(self, query_id: str, new_author: str,
             workspace_id: str | None = None) -> SavedQuery | None:
        with self._lock:
            original = self._queries.get(query_id)
            if original is None:
                return None

        forked = self.save(
            name=f"{original.name} (fork)",
            query_text=original.query_text,
            query_language=original.query_language,
            author=new_author,
            description=original.description,
            parameters=dict(original.parameters),
            workspace_id=workspace_id,
            tags=list(original.tags),
        )
        forked.forked_from = query_id
        return forked

    def search(self, query: str | None = None,
               workspace_id: str | None = None,
               author: str | None = None,
               language: str | None = None,
               tags: list[str] | None = None,
               include_public: bool = True,
               limit: int = 50) -> list[SavedQuery]:
        with self._lock:
            if workspace_id:
                ids = self._by_workspace.get(workspace_id, [])
                candidates = [self._queries[qid] for qid in ids if qid in self._queries]
                if include_public:
                    candidates += [sq for sq in self._queries.values()
                                   if sq.is_public and sq.workspace_id != workspace_id]
            elif author:
                ids = self._by_author.get(author, [])
                candidates = [self._queries[qid] for qid in ids if qid in self._queries]
            else:
                candidates = list(self._queries.values())

        results = []
        query_lower = query.lower() if query else None
        required_tags = set(tags) if tags else None

        for sq in candidates:
            if language and sq.query_language != language:
                continue
            if query_lower and query_lower not in sq.name.lower() and query_lower not in sq.description.lower():
                continue
            if required_tags and not required_tags.issubset(set(sq.tags)):
                continue
            results.append(sq)

        results.sort(key=lambda s: s.execution_count, reverse=True)
        return results[:limit]

    def delete(self, query_id: str) -> bool:
        with self._lock:
            sq = self._queries.pop(query_id, None)
            return sq is not None

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total_executions = sum(sq.execution_count for sq in self._queries.values())
            languages: dict[str, int] = {}
            for sq in self._queries.values():
                languages[sq.query_language] = languages.get(sq.query_language, 0) + 1
            return {
                "total_queries": len(self._queries),
                "total_executions": total_executions,
                "by_language": languages,
                "unique_authors": len(self._by_author),
            }


_INSTANCE: SharedQueryStore | None = None
_LOCK = threading.Lock()


def get_shared_query_store() -> SharedQueryStore:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = SharedQueryStore()
    return _INSTANCE
