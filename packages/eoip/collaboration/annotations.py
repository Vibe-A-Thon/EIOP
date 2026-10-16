"""Annotation system for graph entities and edges.

Allows users to attach structured comments, tags, severity labels,
and review states to any graph entity or relationship. Annotations
are stored independently from graph data and support threading.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class AnnotationType(str, enum.Enum):
    COMMENT = "COMMENT"
    TAG = "TAG"
    REVIEW = "REVIEW"
    QUESTION = "QUESTION"
    FINDING = "FINDING"
    DECISION = "DECISION"
    ACTION_ITEM = "ACTION_ITEM"
    BOOKMARK = "BOOKMARK"


class AnnotationSeverity(str, enum.Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class AnnotationState(str, enum.Enum):
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    ACKNOWLEDGED = "ACKNOWLEDGED"
    WONT_FIX = "WONT_FIX"


@dataclass
class Annotation:
    annotation_id: str
    target_type: str
    target_id: str
    author: str
    annotation_type: AnnotationType
    body: str
    severity: AnnotationSeverity = AnnotationSeverity.INFO
    state: AnnotationState = AnnotationState.OPEN
    tags: list[str] = field(default_factory=list)
    parent_id: str | None = None
    workspace_id: str | None = None
    reactions: dict[str, list[str]] = field(default_factory=dict)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "annotation_id": self.annotation_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "author": self.author,
            "annotation_type": self.annotation_type.value,
            "body": self.body,
            "severity": self.severity.value,
            "state": self.state.value,
            "tags": self.tags,
            "parent_id": self.parent_id,
            "workspace_id": self.workspace_id,
            "reactions": self.reactions,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": self.metadata,
        }


class AnnotationStore:
    """Thread-safe annotation storage with querying capabilities."""

    def __init__(self) -> None:
        self._annotations: dict[str, Annotation] = {}
        self._by_target: dict[str, list[str]] = {}
        self._by_author: dict[str, list[str]] = {}
        self._by_workspace: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    def create(
        self,
        target_type: str,
        target_id: str,
        author: str,
        body: str,
        annotation_type: AnnotationType = AnnotationType.COMMENT,
        severity: AnnotationSeverity = AnnotationSeverity.INFO,
        tags: list[str] | None = None,
        parent_id: str | None = None,
        workspace_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> Annotation:
        ann = Annotation(
            annotation_id=uuid.uuid4().hex[:12],
            target_type=target_type,
            target_id=target_id,
            author=author,
            annotation_type=annotation_type,
            body=body,
            severity=severity,
            tags=tags or [],
            parent_id=parent_id,
            workspace_id=workspace_id,
            metadata=metadata or {},
        )
        with self._lock:
            self._annotations[ann.annotation_id] = ann
            self._by_target.setdefault(f"{target_type}:{target_id}", []).append(ann.annotation_id)
            self._by_author.setdefault(author, []).append(ann.annotation_id)
            if workspace_id:
                self._by_workspace.setdefault(workspace_id, []).append(ann.annotation_id)
        return ann

    def get(self, annotation_id: str) -> Annotation | None:
        with self._lock:
            return self._annotations.get(annotation_id)

    def update(self, annotation_id: str, body: str | None = None,
               state: AnnotationState | None = None,
               severity: AnnotationSeverity | None = None,
               tags: list[str] | None = None) -> Annotation | None:
        with self._lock:
            ann = self._annotations.get(annotation_id)
            if ann is None:
                return None
            if body is not None:
                ann.body = body
            if state is not None:
                ann.state = state
            if severity is not None:
                ann.severity = severity
            if tags is not None:
                ann.tags = tags
            ann.updated_at = time.time()
            return ann

    def delete(self, annotation_id: str) -> bool:
        with self._lock:
            ann = self._annotations.pop(annotation_id, None)
            if ann is None:
                return False
            key = f"{ann.target_type}:{ann.target_id}"
            if key in self._by_target:
                self._by_target[key] = [a for a in self._by_target[key] if a != annotation_id]
            if ann.author in self._by_author:
                self._by_author[ann.author] = [a for a in self._by_author[ann.author] if a != annotation_id]
            return True

    def add_reaction(self, annotation_id: str, emoji: str, user: str) -> bool:
        with self._lock:
            ann = self._annotations.get(annotation_id)
            if ann is None:
                return False
            ann.reactions.setdefault(emoji, [])
            if user not in ann.reactions[emoji]:
                ann.reactions[emoji].append(user)
            return True

    def get_for_target(self, target_type: str, target_id: str,
                       include_threads: bool = True) -> list[Annotation]:
        with self._lock:
            key = f"{target_type}:{target_id}"
            ids = self._by_target.get(key, [])
            annotations = [self._annotations[aid] for aid in ids if aid in self._annotations]
            if not include_threads:
                annotations = [a for a in annotations if a.parent_id is None]
            return sorted(annotations, key=lambda a: a.created_at)

    def get_thread(self, parent_id: str) -> list[Annotation]:
        with self._lock:
            parent = self._annotations.get(parent_id)
            if parent is None:
                return []
            replies = [a for a in self._annotations.values() if a.parent_id == parent_id]
            return [parent] + sorted(replies, key=lambda a: a.created_at)

    def get_by_author(self, author: str, limit: int = 50) -> list[Annotation]:
        with self._lock:
            ids = self._by_author.get(author, [])
            annotations = [self._annotations[aid] for aid in ids if aid in self._annotations]
            return sorted(annotations, key=lambda a: a.created_at, reverse=True)[:limit]

    def search(self, query: str | None = None,
               annotation_type: AnnotationType | None = None,
               severity: AnnotationSeverity | None = None,
               state: AnnotationState | None = None,
               tags: list[str] | None = None,
               workspace_id: str | None = None,
               limit: int = 100) -> list[Annotation]:
        with self._lock:
            if workspace_id:
                ids = self._by_workspace.get(workspace_id, [])
                candidates = [self._annotations[aid] for aid in ids if aid in self._annotations]
            else:
                candidates = list(self._annotations.values())

        results = []
        query_lower = query.lower() if query else None
        required_tags = set(tags) if tags else None

        for ann in candidates:
            if annotation_type and ann.annotation_type != annotation_type:
                continue
            if severity and ann.severity != severity:
                continue
            if state and ann.state != state:
                continue
            if query_lower and query_lower not in ann.body.lower():
                continue
            if required_tags and not required_tags.issubset(set(ann.tags)):
                continue
            results.append(ann)

        return sorted(results, key=lambda a: a.created_at, reverse=True)[:limit]

    def stats(self) -> dict[str, Any]:
        with self._lock:
            by_type: dict[str, int] = {}
            by_state: dict[str, int] = {}
            for ann in self._annotations.values():
                by_type[ann.annotation_type.value] = by_type.get(ann.annotation_type.value, 0) + 1
                by_state[ann.state.value] = by_state.get(ann.state.value, 0) + 1
            return {
                "total": len(self._annotations),
                "by_type": by_type,
                "by_state": by_state,
                "unique_authors": len(self._by_author),
                "unique_targets": len(self._by_target),
            }


_INSTANCE: AnnotationStore | None = None
_LOCK = threading.Lock()


def get_annotation_store() -> AnnotationStore:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = AnnotationStore()
    return _INSTANCE
