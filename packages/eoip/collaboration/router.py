"""REST API router for collaboration features.

Endpoints for annotations, workspaces, activity feeds, and shared queries.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field


# ── Request models ────────────────────────────────────────────────────

class AnnotationCreateRequest(BaseModel):
    target_type: str = Field(min_length=1, max_length=64)
    target_id: str = Field(min_length=1, max_length=256)
    author: str = Field(min_length=1, max_length=128)
    body: str = Field(min_length=1, max_length=10000)
    annotation_type: str = Field(default="COMMENT")
    severity: str = Field(default="INFO")
    tags: list[str] = Field(default_factory=list)
    parent_id: str | None = None
    workspace_id: str | None = None


class AnnotationUpdateRequest(BaseModel):
    body: str | None = None
    state: str | None = None
    severity: str | None = None
    tags: list[str] | None = None


class ReactionRequest(BaseModel):
    emoji: str = Field(min_length=1, max_length=16)
    user: str = Field(min_length=1, max_length=128)


class WorkspaceCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    description: str = Field(default="", max_length=2000)
    owner: str = Field(min_length=1, max_length=128)
    tenant_id: str | None = None
    tags: list[str] = Field(default_factory=list)


class MemberRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    role: str = Field(default="VIEWER")
    invited_by: str | None = None


class RoleUpdateRequest(BaseModel):
    user_id: str = Field(min_length=1, max_length=128)
    role: str = Field(min_length=1)


class PinRequest(BaseModel):
    resource_id: str = Field(min_length=1, max_length=256)


class SavedQueryCreateRequest(BaseModel):
    name: str = Field(min_length=1, max_length=256)
    query_text: str = Field(min_length=1, max_length=50000)
    query_language: str = Field(min_length=1, max_length=32)
    author: str = Field(min_length=1, max_length=128)
    description: str = Field(default="", max_length=2000)
    parameters: dict[str, Any] = Field(default_factory=dict)
    workspace_id: str | None = None
    tags: list[str] = Field(default_factory=list)
    is_public: bool = False


class SavedQueryUpdateRequest(BaseModel):
    query_text: str = Field(min_length=1, max_length=50000)
    author: str = Field(min_length=1, max_length=128)
    change_note: str = Field(default="", max_length=500)


class QueryExecutionRequest(BaseModel):
    executed_by: str = Field(min_length=1, max_length=128)


class QueryForkRequest(BaseModel):
    new_author: str = Field(min_length=1, max_length=128)
    workspace_id: str | None = None


def build_collaboration_router() -> APIRouter:
    """Build the collaboration features router."""
    router = APIRouter(prefix="/api/v1/collaboration", tags=["Collaboration"])

    # ── Annotations ───────────────────────────────────────────────────

    @router.post("/annotations", summary="Create annotation")
    def create_annotation(req: AnnotationCreateRequest) -> dict[str, Any]:
        from eoip.collaboration.annotations import (
            AnnotationType, AnnotationSeverity, get_annotation_store,
        )
        try:
            ann_type = AnnotationType(req.annotation_type)
        except ValueError:
            raise HTTPException(400, f"Invalid annotation type: {req.annotation_type}")
        try:
            severity = AnnotationSeverity(req.severity)
        except ValueError:
            raise HTTPException(400, f"Invalid severity: {req.severity}")
        ann = get_annotation_store().create(
            target_type=req.target_type,
            target_id=req.target_id,
            author=req.author,
            body=req.body,
            annotation_type=ann_type,
            severity=severity,
            tags=req.tags,
            parent_id=req.parent_id,
            workspace_id=req.workspace_id,
        )
        return ann.to_dict()

    @router.get("/annotations/{annotation_id}", summary="Get annotation")
    def get_annotation(annotation_id: str) -> dict[str, Any]:
        from eoip.collaboration.annotations import get_annotation_store
        ann = get_annotation_store().get(annotation_id)
        if ann is None:
            raise HTTPException(404, "Annotation not found")
        return ann.to_dict()

    @router.patch("/annotations/{annotation_id}", summary="Update annotation")
    def update_annotation(annotation_id: str, req: AnnotationUpdateRequest) -> dict[str, Any]:
        from eoip.collaboration.annotations import (
            AnnotationState, AnnotationSeverity, get_annotation_store,
        )
        state = None
        if req.state:
            try:
                state = AnnotationState(req.state)
            except ValueError:
                raise HTTPException(400, f"Invalid state: {req.state}")
        severity = None
        if req.severity:
            try:
                severity = AnnotationSeverity(req.severity)
            except ValueError:
                raise HTTPException(400, f"Invalid severity: {req.severity}")
        ann = get_annotation_store().update(
            annotation_id, body=req.body, state=state,
            severity=severity, tags=req.tags,
        )
        if ann is None:
            raise HTTPException(404, "Annotation not found")
        return ann.to_dict()

    @router.delete("/annotations/{annotation_id}", summary="Delete annotation")
    def delete_annotation(annotation_id: str) -> dict[str, Any]:
        from eoip.collaboration.annotations import get_annotation_store
        if not get_annotation_store().delete(annotation_id):
            raise HTTPException(404, "Annotation not found")
        return {"deleted": True}

    @router.post("/annotations/{annotation_id}/reactions", summary="Add reaction")
    def add_reaction(annotation_id: str, req: ReactionRequest) -> dict[str, Any]:
        from eoip.collaboration.annotations import get_annotation_store
        if not get_annotation_store().add_reaction(annotation_id, req.emoji, req.user):
            raise HTTPException(404, "Annotation not found")
        return {"added": True}

    @router.get("/annotations/target/{target_type}/{target_id}", summary="Get annotations for target")
    def get_target_annotations(target_type: str, target_id: str) -> list[dict[str, Any]]:
        from eoip.collaboration.annotations import get_annotation_store
        return [a.to_dict() for a in get_annotation_store().get_for_target(target_type, target_id)]

    @router.get("/annotations/{annotation_id}/thread", summary="Get annotation thread")
    def get_thread(annotation_id: str) -> list[dict[str, Any]]:
        from eoip.collaboration.annotations import get_annotation_store
        return [a.to_dict() for a in get_annotation_store().get_thread(annotation_id)]

    @router.get("/annotations/search", summary="Search annotations")
    def search_annotations(
        query: str | None = Query(default=None),
        annotation_type: str | None = Query(default=None),
        severity: str | None = Query(default=None),
        state: str | None = Query(default=None),
        workspace_id: str | None = Query(default=None),
        limit: int = Query(default=100, ge=1, le=500),
    ) -> dict[str, Any]:
        from eoip.collaboration.annotations import (
            AnnotationType, AnnotationSeverity, AnnotationState, get_annotation_store,
        )
        at = AnnotationType(annotation_type) if annotation_type else None
        sev = AnnotationSeverity(severity) if severity else None
        st = AnnotationState(state) if state else None
        results = get_annotation_store().search(
            query=query, annotation_type=at, severity=sev,
            state=st, workspace_id=workspace_id, limit=limit,
        )
        return {"results": [a.to_dict() for a in results], "total": len(results)}

    @router.get("/annotations/stats", summary="Annotation statistics")
    def annotation_stats() -> dict[str, Any]:
        from eoip.collaboration.annotations import get_annotation_store
        return get_annotation_store().stats()

    # ── Workspaces ────────────────────────────────────────────────────

    @router.post("/workspaces", summary="Create workspace")
    def create_workspace(req: WorkspaceCreateRequest) -> dict[str, Any]:
        from eoip.collaboration.workspaces import get_workspace_store
        ws = get_workspace_store().create(
            name=req.name, description=req.description,
            owner=req.owner, tenant_id=req.tenant_id, tags=req.tags,
        )
        return ws.to_dict()

    @router.get("/workspaces/{workspace_id}", summary="Get workspace")
    def get_workspace(workspace_id: str) -> dict[str, Any]:
        from eoip.collaboration.workspaces import get_workspace_store
        ws = get_workspace_store().get(workspace_id)
        if ws is None:
            raise HTTPException(404, "Workspace not found")
        return ws.to_dict()

    @router.post("/workspaces/{workspace_id}/members", summary="Add member")
    def add_member(workspace_id: str, req: MemberRequest) -> dict[str, Any]:
        from eoip.collaboration.workspaces import WorkspaceRole, get_workspace_store
        try:
            role = WorkspaceRole(req.role)
        except ValueError:
            raise HTTPException(400, f"Invalid role: {req.role}")
        if not get_workspace_store().add_member(
            workspace_id, req.user_id, role=role, invited_by=req.invited_by,
        ):
            raise HTTPException(404, "Workspace not found")
        return {"added": True}

    @router.delete("/workspaces/{workspace_id}/members/{user_id}", summary="Remove member")
    def remove_member(workspace_id: str, user_id: str) -> dict[str, Any]:
        from eoip.collaboration.workspaces import get_workspace_store
        if not get_workspace_store().remove_member(workspace_id, user_id):
            raise HTTPException(400, "Cannot remove member (not found or is owner)")
        return {"removed": True}

    @router.patch("/workspaces/{workspace_id}/members/role", summary="Update member role")
    def update_member_role(workspace_id: str, req: RoleUpdateRequest) -> dict[str, Any]:
        from eoip.collaboration.workspaces import WorkspaceRole, get_workspace_store
        try:
            role = WorkspaceRole(req.role)
        except ValueError:
            raise HTTPException(400, f"Invalid role: {req.role}")
        if not get_workspace_store().update_role(workspace_id, req.user_id, role):
            raise HTTPException(404, "Workspace or member not found")
        return {"updated": True}

    @router.post("/workspaces/{workspace_id}/pin-query", summary="Pin query to workspace")
    def pin_query(workspace_id: str, req: PinRequest) -> dict[str, Any]:
        from eoip.collaboration.workspaces import get_workspace_store
        if not get_workspace_store().pin_query(workspace_id, req.resource_id):
            raise HTTPException(404, "Workspace not found")
        return {"pinned": True}

    @router.post("/workspaces/{workspace_id}/pin-entity", summary="Pin entity to workspace")
    def pin_entity(workspace_id: str, req: PinRequest) -> dict[str, Any]:
        from eoip.collaboration.workspaces import get_workspace_store
        if not get_workspace_store().pin_entity(workspace_id, req.resource_id):
            raise HTTPException(404, "Workspace not found")
        return {"pinned": True}

    @router.get("/workspaces/user/{user_id}", summary="List user workspaces")
    def list_user_workspaces(user_id: str) -> list[dict[str, Any]]:
        from eoip.collaboration.workspaces import get_workspace_store
        return [ws.to_dict() for ws in get_workspace_store().list_for_user(user_id)]

    @router.delete("/workspaces/{workspace_id}", summary="Delete workspace")
    def delete_workspace(workspace_id: str) -> dict[str, Any]:
        from eoip.collaboration.workspaces import get_workspace_store
        if not get_workspace_store().delete(workspace_id):
            raise HTTPException(404, "Workspace not found")
        return {"deleted": True}

    @router.get("/workspaces/stats", summary="Workspace statistics")
    def workspace_stats() -> dict[str, Any]:
        from eoip.collaboration.workspaces import get_workspace_store
        return get_workspace_store().stats()

    # ── Activity Feed ─────────────────────────────────────────────────

    @router.get("/activity", summary="Get activity feed")
    def get_activity(
        workspace_id: str | None = Query(default=None),
        actor: str | None = Query(default=None),
        action: str | None = Query(default=None),
        resource_type: str | None = Query(default=None),
        limit: int = Query(default=50, ge=1, le=500),
    ) -> dict[str, Any]:
        from eoip.collaboration.activity import ActivityAction, get_activity_feed
        act = None
        if action:
            try:
                act = ActivityAction(action)
            except ValueError:
                raise HTTPException(400, f"Invalid action: {action}")
        events = get_activity_feed().get_feed(
            workspace_id=workspace_id, actor=actor,
            action=act, resource_type=resource_type, limit=limit,
        )
        return {"events": [e.to_dict() for e in events], "total": len(events)}

    @router.get("/activity/user/{user_id}", summary="Get user activity")
    def get_user_activity(user_id: str, limit: int = Query(default=50, ge=1, le=500)) -> dict[str, Any]:
        from eoip.collaboration.activity import get_activity_feed
        events = get_activity_feed().get_user_activity(user_id, limit=limit)
        return {"events": [e.to_dict() for e in events], "total": len(events)}

    @router.get("/activity/stats", summary="Activity feed statistics")
    def activity_stats() -> dict[str, Any]:
        from eoip.collaboration.activity import get_activity_feed
        return get_activity_feed().stats()

    # ── Shared Queries ────────────────────────────────────────────────

    @router.post("/queries", summary="Save query")
    def save_query(req: SavedQueryCreateRequest) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        sq = get_shared_query_store().save(
            name=req.name, query_text=req.query_text,
            query_language=req.query_language, author=req.author,
            description=req.description, parameters=req.parameters,
            workspace_id=req.workspace_id, tags=req.tags,
            is_public=req.is_public,
        )
        return sq.to_dict()

    @router.get("/queries/{query_id}", summary="Get saved query")
    def get_query(query_id: str) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        sq = get_shared_query_store().get(query_id)
        if sq is None:
            raise HTTPException(404, "Query not found")
        return sq.to_dict()

    @router.patch("/queries/{query_id}", summary="Update saved query")
    def update_query(query_id: str, req: SavedQueryUpdateRequest) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        sq = get_shared_query_store().update(
            query_id, query_text=req.query_text,
            author=req.author, change_note=req.change_note,
        )
        if sq is None:
            raise HTTPException(404, "Query not found")
        return sq.to_dict()

    @router.get("/queries/{query_id}/versions/{version}", summary="Get query version")
    def get_query_version(query_id: str, version: int) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        qv = get_shared_query_store().get_version(query_id, version)
        if qv is None:
            raise HTTPException(404, "Version not found")
        return {
            "version": qv.version,
            "query_text": qv.query_text,
            "parameters": qv.parameters,
            "author": qv.author,
            "change_note": qv.change_note,
            "created_at": qv.created_at,
        }

    @router.post("/queries/{query_id}/execute", summary="Record query execution")
    def record_execution(query_id: str, req: QueryExecutionRequest) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        if not get_shared_query_store().record_execution(query_id, req.executed_by):
            raise HTTPException(404, "Query not found")
        return {"recorded": True}

    @router.post("/queries/{query_id}/fork", summary="Fork saved query")
    def fork_query(query_id: str, req: QueryForkRequest) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        forked = get_shared_query_store().fork(
            query_id, new_author=req.new_author, workspace_id=req.workspace_id,
        )
        if forked is None:
            raise HTTPException(404, "Query not found")
        return forked.to_dict()

    @router.get("/queries/search", summary="Search saved queries")
    def search_queries(
        query: str | None = Query(default=None),
        workspace_id: str | None = Query(default=None),
        author: str | None = Query(default=None),
        language: str | None = Query(default=None),
        limit: int = Query(default=50, ge=1, le=500),
    ) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        results = get_shared_query_store().search(
            query=query, workspace_id=workspace_id,
            author=author, language=language, limit=limit,
        )
        return {"results": [sq.to_dict() for sq in results], "total": len(results)}

    @router.delete("/queries/{query_id}", summary="Delete saved query")
    def delete_query(query_id: str) -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        if not get_shared_query_store().delete(query_id):
            raise HTTPException(404, "Query not found")
        return {"deleted": True}

    @router.get("/queries/stats", summary="Shared query statistics")
    def query_stats() -> dict[str, Any]:
        from eoip.collaboration.shared_queries import get_shared_query_store
        return get_shared_query_store().stats()

    return router
