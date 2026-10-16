"""Workspace management for team collaboration.

Workspaces are logical groupings of graphs, queries, reports and
annotations that teams share. Each workspace has role-based membership
(OWNER, EDITOR, VIEWER) and tracks its own activity.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class WorkspaceRole(str, enum.Enum):
    OWNER = "OWNER"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"
    COMMENTER = "COMMENTER"


@dataclass
class WorkspaceMember:
    user_id: str
    role: WorkspaceRole
    joined_at: float = field(default_factory=time.time)
    invited_by: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_id": self.user_id,
            "role": self.role.value,
            "joined_at": self.joined_at,
            "invited_by": self.invited_by,
        }


@dataclass
class Workspace:
    workspace_id: str
    name: str
    description: str
    owner: str
    tenant_id: str | None = None
    members: dict[str, WorkspaceMember] = field(default_factory=dict)
    pinned_queries: list[str] = field(default_factory=list)
    pinned_entities: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace_id": self.workspace_id,
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "tenant_id": self.tenant_id,
            "members": {uid: m.to_dict() for uid, m in self.members.items()},
            "member_count": len(self.members),
            "pinned_queries": self.pinned_queries,
            "pinned_entities": self.pinned_entities,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


class WorkspaceStore:
    """Thread-safe workspace management."""

    def __init__(self) -> None:
        self._workspaces: dict[str, Workspace] = {}
        self._by_user: dict[str, list[str]] = {}
        self._lock = threading.Lock()

    def create(self, name: str, description: str, owner: str,
               tenant_id: str | None = None, tags: list[str] | None = None) -> Workspace:
        ws = Workspace(
            workspace_id=uuid.uuid4().hex[:12],
            name=name,
            description=description,
            owner=owner,
            tenant_id=tenant_id,
            tags=tags or [],
        )
        owner_member = WorkspaceMember(user_id=owner, role=WorkspaceRole.OWNER)
        ws.members[owner] = owner_member
        with self._lock:
            self._workspaces[ws.workspace_id] = ws
            self._by_user.setdefault(owner, []).append(ws.workspace_id)
        return ws

    def get(self, workspace_id: str) -> Workspace | None:
        with self._lock:
            return self._workspaces.get(workspace_id)

    def add_member(self, workspace_id: str, user_id: str,
                   role: WorkspaceRole = WorkspaceRole.VIEWER,
                   invited_by: str | None = None) -> bool:
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            ws.members[user_id] = WorkspaceMember(
                user_id=user_id, role=role, invited_by=invited_by,
            )
            ws.updated_at = time.time()
            self._by_user.setdefault(user_id, []).append(workspace_id)
            return True

    def remove_member(self, workspace_id: str, user_id: str) -> bool:
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or user_id not in ws.members:
                return False
            if ws.members[user_id].role == WorkspaceRole.OWNER:
                return False
            del ws.members[user_id]
            ws.updated_at = time.time()
            if user_id in self._by_user:
                self._by_user[user_id] = [w for w in self._by_user[user_id] if w != workspace_id]
            return True

    def update_role(self, workspace_id: str, user_id: str, role: WorkspaceRole) -> bool:
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None or user_id not in ws.members:
                return False
            ws.members[user_id].role = role
            ws.updated_at = time.time()
            return True

    def check_permission(self, workspace_id: str, user_id: str,
                         required: WorkspaceRole) -> bool:
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            member = ws.members.get(user_id)
            if member is None:
                return False
            hierarchy = {
                WorkspaceRole.VIEWER: 0,
                WorkspaceRole.COMMENTER: 1,
                WorkspaceRole.EDITOR: 2,
                WorkspaceRole.OWNER: 3,
            }
            return hierarchy.get(member.role, 0) >= hierarchy.get(required, 0)

    def pin_query(self, workspace_id: str, query_id: str) -> bool:
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            if query_id not in ws.pinned_queries:
                ws.pinned_queries.append(query_id)
                ws.updated_at = time.time()
            return True

    def pin_entity(self, workspace_id: str, canonical_id: str) -> bool:
        with self._lock:
            ws = self._workspaces.get(workspace_id)
            if ws is None:
                return False
            if canonical_id not in ws.pinned_entities:
                ws.pinned_entities.append(canonical_id)
                ws.updated_at = time.time()
            return True

    def list_for_user(self, user_id: str) -> list[Workspace]:
        with self._lock:
            ws_ids = self._by_user.get(user_id, [])
            return [self._workspaces[wid] for wid in ws_ids if wid in self._workspaces]

    def delete(self, workspace_id: str) -> bool:
        with self._lock:
            ws = self._workspaces.pop(workspace_id, None)
            if ws is None:
                return False
            for uid in ws.members:
                if uid in self._by_user:
                    self._by_user[uid] = [w for w in self._by_user[uid] if w != workspace_id]
            return True

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total_members = sum(len(ws.members) for ws in self._workspaces.values())
            return {
                "total_workspaces": len(self._workspaces),
                "total_memberships": total_members,
                "unique_users": len(self._by_user),
            }


_INSTANCE: WorkspaceStore | None = None
_LOCK = threading.Lock()


def get_workspace_store() -> WorkspaceStore:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = WorkspaceStore()
    return _INSTANCE
