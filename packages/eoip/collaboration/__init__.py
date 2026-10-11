"""Collaboration — multi-user annotations, workspaces, activity feeds, shared queries.

Provides the social layer for enterprise knowledge graph teams:
- Annotations on any graph entity/edge with structured metadata
- Workspaces for logical grouping of graphs, queries, reports
- Activity feeds tracking who did what across the platform
- Shared saved queries with version history
"""

from eoip.collaboration.annotations import (
    Annotation,
    AnnotationStore,
    AnnotationType,
    get_annotation_store,
)
from eoip.collaboration.workspaces import (
    Workspace,
    WorkspaceMember,
    WorkspaceRole,
    WorkspaceStore,
    get_workspace_store,
)
from eoip.collaboration.activity import (
    ActivityEvent,
    ActivityFeed,
    get_activity_feed,
)
from eoip.collaboration.shared_queries import (
    SavedQuery,
    SharedQueryStore,
    get_shared_query_store,
)

__all__ = [
    "Annotation",
    "AnnotationStore",
    "AnnotationType",
    "ActivityEvent",
    "ActivityFeed",
    "SavedQuery",
    "SharedQueryStore",
    "Workspace",
    "WorkspaceMember",
    "WorkspaceRole",
    "WorkspaceStore",
    "get_activity_feed",
    "get_annotation_store",
    "get_shared_query_store",
    "get_workspace_store",
]
