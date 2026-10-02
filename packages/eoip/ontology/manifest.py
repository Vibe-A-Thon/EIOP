"""Ontology vocabulary and HugeGraph schema manifest (FR-ONTO-001, FR-ONTO-002).

The ontology is a controlled vocabulary: every entity type and relationship
declares domain/range, required properties and lifecycle/version. MVP terms
are enumerated here; namespaces for Organization, Work, Code, CI/CD,
Operations, Knowledge and AI/Agent concepts are preserved.
"""

ONTOLOGY_VERSION = "0.2.0"
SCHEMA_VERSION = "1.0"

# Graph domains (one physical graph, multiple logical domains — ADR-1)
DOMAINS = ["META", "WORK", "CODE", "CICD", "KNOWLEDGE", "IDENTITY", "AGENT"]

# Shared property keys (11-graph-schema.md) with HugeGraph data types.
# TEXT | INT | LONG | DOUBLE | BOOLEAN | DATE (ISO-8601 strings in MVP)
PROPERTY_KEYS: dict[str, str] = {
    "edge_key": "TEXT",
    "captured_at": "DATE",
    "canonical_id": "TEXT",
    "source_system": "TEXT",
    "source_id": "TEXT",
    "registry_source_id": "TEXT",
    "source_uri": "TEXT",
    "graph_domain": "TEXT",
    "entity_type": "TEXT",
    "name": "TEXT",
    "display_name": "TEXT",
    "content_hash": "TEXT",
    "creation_status": "TEXT",
    "confidence": "DOUBLE",
    "first_seen": "DATE",
    "last_seen": "DATE",
    "created_at": "DATE",
    "modified_at": "DATE",
    "deleted_at": "DATE",
    "valid_from": "DATE",
    "valid_to": "DATE",
    "source_version": "TEXT",
    "ingestion_run_id": "TEXT",
    "ontology_version": "TEXT",
    "schema_version": "TEXT",
    "repo_id": "TEXT",
    "path": "TEXT",
    "qualified_name": "TEXT",
    "symbol_kind": "TEXT",
    "start_line": "INT",
    "end_line": "INT",
    "start_column": "INT",
    "end_column": "INT",
    "issue_key": "TEXT",
    "commit_sha": "TEXT",
    "evidence_key": "TEXT",
    # domain-specific additive properties
    "email": "TEXT",
    "issue_type": "TEXT",
    "summary": "TEXT",
    "status": "TEXT",
    "description": "TEXT",
    "language": "TEXT",
    "parser_version": "TEXT",
    "mapper_version": "TEXT",
    "branch_name": "TEXT",
    "message": "TEXT",
    "author_email": "TEXT",
    "author_name": "TEXT",
    "parent_shas": "TEXT",
    "mr_iid": "INT",
    "mr_title": "TEXT",
    "source_branch": "TEXT",
    "target_branch": "TEXT",
    "pipeline_status": "TEXT",
    "ref": "TEXT",
    "resolved": "BOOLEAN",
    "fact_key": "TEXT",
    "severity": "TEXT",
    "rule_id": "TEXT",
    "remediation": "TEXT",
    "run_status": "TEXT",
    "run_kind": "TEXT",
    "counts": "TEXT",
    "started_at": "DATE",
    "finished_at": "DATE",
    "method": "TEXT",
    "source_ref": "TEXT",
    "doc_format": "TEXT",
    "content": "TEXT",
    "section_index": "INT",
    "agent_id": "TEXT",
    "goal": "TEXT",
    "budgets": "TEXT",
    "space_key": "TEXT",
    "media_type": "TEXT",
    "file_size": "LONG",
    "revision_id": "TEXT",
    "subject_id": "TEXT",
    "relationship_id": "TEXT",
    "relationship_type": "TEXT",
    "from_id": "TEXT",
    "to_id": "TEXT",
    "observed_at": "DATE",
    "is_current": "BOOLEAN",
    "previous_revision": "TEXT",
    "graph_version": "TEXT",
    "source_event_id": "TEXT",
    "change_kind": "TEXT",
    "payload_json": "TEXT",
    "external_id": "TEXT",
    "url": "TEXT",
    "visibility": "TEXT",
    "default_branch": "TEXT",
    "tag_name": "TEXT",
    "published_at": "DATE",
    "conclusion": "TEXT",
    "job_id": "TEXT",
    "stage": "TEXT",
    "duration_seconds": "DOUBLE",
    "artifact_type": "TEXT",
    "artifact_format": "TEXT",
    "environment": "TEXT",
    "deployable_id": "TEXT",
    "verified": "BOOLEAN",
    "project_key": "TEXT",
    "issue_type_id": "TEXT",
    "status_id": "TEXT",
    "version_id": "TEXT",
    "sprint_id": "TEXT",
    "comment_id": "TEXT",
    "change_id": "TEXT",
    "field_name": "TEXT",
    "from_value": "TEXT",
    "to_value": "TEXT",
    "released": "BOOLEAN",
    "release_date": "DATE",
    "start_date": "DATE",
    "end_date": "DATE",
    "link_type": "TEXT",
    "link_direction": "TEXT",
}

# Vertex labels -> (graph_domain, required properties, optional properties)
VERTEX_LABELS: dict[str, tuple[str, list[str], list[str]]] = {
    "DataSource": ("META", ["canonical_id", "name", "source_system"], ["source_uri", "description"]),
    "IngestionRun": ("META", ["canonical_id", "run_status", "run_kind"], ["counts", "started_at", "finished_at", "source_system", "ingestion_run_id"]),
    "GraphDomain": ("META", ["canonical_id", "name"], ["description"]),
    "OntologyVersion": ("META", ["canonical_id", "ontology_version"], ["schema_version"]),
    "Evidence": ("META", ["canonical_id", "source_system", "source_ref", "method"], ["captured_at", "parser_version", "mapper_version", "confidence", "evidence_key"]),
    "ValidationRun": ("META", ["canonical_id", "run_status"], ["started_at", "finished_at", "counts"]),
    "ValidationFinding": ("META", ["canonical_id", "severity", "rule_id"], ["remediation", "description"]),
    "Project": ("WORK", ["canonical_id", "name"], ["display_name", "issue_key"]),
    "WorkItem": ("WORK", ["canonical_id", "issue_key", "summary"], ["issue_type", "status", "description", "created_at", "modified_at", "deleted_at"]),
    "Person": ("IDENTITY", ["canonical_id", "display_name"], ["email"]),
    "Repository": ("CODE", ["canonical_id", "repo_id", "name"], ["source_uri"]),
    "Branch": ("CODE", ["canonical_id", "branch_name"], ["repo_id"]),
    "Commit": ("CODE", ["canonical_id", "commit_sha"], ["message", "author_email", "author_name", "created_at", "parent_shas"]),
    "MergeRequest": ("CICD", ["canonical_id", "mr_iid", "mr_title"], ["source_branch", "target_branch", "status"]),
    "PipelineRun": ("CICD", ["canonical_id", "name"], ["pipeline_status", "ref", "commit_sha", "created_at"]),
    "File": ("CODE", ["canonical_id", "repo_id", "path"], ["language", "content_hash"]),
    "CodeSymbol": ("CODE", ["canonical_id", "qualified_name", "symbol_kind"], ["name", "repo_id", "path", "start_line", "end_line", "start_column", "end_column", "language", "parser_version"]),
    "Dependency": ("CODE", ["canonical_id", "name"], ["resolved", "language"]),
    "Document": ("KNOWLEDGE", ["canonical_id", "name", "path"], ["doc_format", "content_hash", "description", "repo_id"]),
    "KnowledgeSpace": ("KNOWLEDGE", ["canonical_id", "name", "space_key"], ["description"]),
    "DocumentSection": ("KNOWLEDGE", ["canonical_id", "name"], ["path", "section_index", "content_hash", "start_line", "end_line"]),
    "AgentRun": ("AGENT", ["canonical_id", "agent_id", "goal"], ["run_status", "budgets", "started_at", "finished_at"]),
    "EntityRevision": ("META", ["canonical_id", "revision_id", "subject_id", "observed_at", "is_current", "payload_json", "source_event_id"], ["valid_from", "valid_to", "previous_revision", "source_version", "graph_version", "entity_type"]),
    "RelationshipRevision": ("META", ["canonical_id", "revision_id", "relationship_id", "relationship_type", "from_id", "to_id", "observed_at", "is_current", "payload_json", "source_event_id"], ["valid_from", "valid_to", "previous_revision", "source_version", "graph_version"]),
    "GraphVersion": ("META", ["canonical_id", "graph_version", "created_at"], ["source_event_id", "change_kind", "counts"]),
    "SemanticChange": ("META", ["canonical_id", "graph_version", "change_kind", "observed_at", "payload_json"], ["source_event_id", "subject_id", "relationship_id"]),
    "Organization": ("IDENTITY", ["canonical_id", "name"], ["external_id", "url", "source_system"]),
    "Tag": ("CODE", ["canonical_id", "repo_id", "tag_name"], ["commit_sha", "source_system"]),
    "Release": ("CICD", ["canonical_id", "name", "tag_name"], ["external_id", "published_at", "url", "status", "description", "repo_id"]),
    "Job": ("CICD", ["canonical_id", "job_id", "name"], ["status", "stage", "ref", "commit_sha", "created_at", "duration_seconds", "url", "repo_id"]),
    "Artifact": ("CICD", ["canonical_id", "name"], ["artifact_type", "artifact_format", "file_size", "url", "repo_id"]),
    "Deployment": ("CICD", ["canonical_id", "name"], ["status", "environment", "ref", "commit_sha", "created_at", "deployable_id", "url", "repo_id"]),
    "IssueType": ("WORK", ["canonical_id", "issue_type_id", "name"], ["description", "project_key"]),
    "Status": ("WORK", ["canonical_id", "status_id", "name"], ["description", "project_key"]),
    "Version": ("WORK", ["canonical_id", "version_id", "name"], ["description", "project_key", "released", "release_date", "status"]),
    "Sprint": ("WORK", ["canonical_id", "sprint_id", "name"], ["description", "project_key", "status", "start_date", "end_date"]),
    "Comment": ("WORK", ["canonical_id", "comment_id", "content"], ["created_at", "modified_at", "source_system", "source_id"]),
    "WorkItemChange": ("WORK", ["canonical_id", "change_id", "field_name"], ["from_value", "to_value", "created_at", "source_system", "source_id"]),
}

# Edge labels -> (out vertex labels, in vertex labels, properties)
# Endpoint/domain-range validation uses these constraints (FR-ONTO-002,
# FR-VALID-002). RELATED_TO is deliberately absent (forbidden).
EDGE_LABELS: dict[str, tuple[list[str], list[str], list[str]]] = {
    "CONTAINS": (
        ["Project", "Repository", "Document", "DataSource", "KnowledgeSpace", "Organization"],
        ["WorkItem", "File", "DocumentSection", "Project", "Document", "Repository"],
        [],
    ),
    "PARENT_OF": (["WorkItem"], ["WorkItem"], []),
    "ASSIGNED_TO": (["WorkItem"], ["Person"], []),
    "AUTHORED_BY": (["Commit", "MergeRequest", "Comment", "WorkItemChange"], ["Person"], []),
    "HAS_BRANCH": (["Repository"], ["Branch"], []),
    "HAS_COMMIT": (["Repository", "Branch"], ["Commit"], []),
    "HAS_MERGE_REQUEST": (["Repository"], ["MergeRequest"], []),
    "HAS_TAG": (["Repository"], ["Tag"], []),
    "HAS_RELEASE": (["Repository"], ["Release"], []),
    "HAS_ISSUE_TYPE": (["Project"], ["IssueType"], []),
    "HAS_STATUS": (["Project", "WorkItem"], ["Status"], []),
    "HAS_VERSION": (["Project"], ["Version"], []),
    "HAS_SPRINT": (["Project"], ["Sprint"], []),
    "IN_SPRINT": (["WorkItem"], ["Sprint"], []),
    "FIXED_IN": (["WorkItem"], ["Version"], []),
    "HAS_COMMENT": (["WorkItem"], ["Comment"], []),
    "HAS_CHANGE": (["WorkItem"], ["WorkItemChange"], []),
    "OF_TYPE": (["WorkItem"], ["IssueType"], []),
    "REPORTED_BY": (["WorkItem"], ["Person"], []),
    "BLOCKS": (["WorkItem"], ["WorkItem"], []),
    "DUPLICATES": (["WorkItem"], ["WorkItem"], []),
    "CLONES": (["WorkItem"], ["WorkItem"], []),
    "HAS_JOB": (["PipelineRun"], ["Job"], []),
    "PRODUCES": (["Job"], ["Artifact"], []),
    "DEPLOYS": (["PipelineRun", "Job"], ["Deployment"], []),
    "MODIFIES": (["Commit", "MergeRequest"], ["File"], []),
    "DECLARES": (["File"], ["CodeSymbol"], []),
    "CALLS": (["CodeSymbol"], ["CodeSymbol"], []),
    "IMPORTS": (["File", "CodeSymbol"], ["Dependency"], []),
    "DEPENDS_ON": (["CodeSymbol", "File"], ["Dependency", "CodeSymbol", "File"], []),
    "IMPLEMENTS": (["MergeRequest", "Commit"], ["WorkItem"], []),
    "REFERENCES": (["MergeRequest", "Commit", "Document", "DocumentSection", "WorkItem", "PipelineRun"], ["WorkItem", "Commit", "CodeSymbol", "Dependency", "File"], []),
    "DOCUMENTS": (["Document", "DocumentSection"], ["CodeSymbol", "WorkItem", "File"], []),
    "EVIDENCED_BY": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Dependency", "Document", "DocumentSection", "Person", "Project", "Repository", "Branch", "KnowledgeSpace", "Organization", "Tag", "Release", "Job", "Artifact", "Deployment", "IssueType", "Status", "Version", "Sprint", "Comment", "WorkItemChange"], ["Evidence"], []),
    "INGESTED_IN": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Document", "DocumentSection", "Person", "Project", "Repository", "Branch", "Dependency", "KnowledgeSpace", "Organization", "Tag", "Release", "Job", "Artifact", "Deployment", "IssueType", "Status", "Version", "Sprint", "Comment", "WorkItemChange"], ["IngestionRun"], []),
    "BELONGS_TO_DOMAIN": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Document", "DocumentSection", "Person", "Project", "Repository", "Branch", "Dependency", "Evidence", "KnowledgeSpace", "Organization", "Tag", "Release", "Job", "Artifact", "Deployment", "IssueType", "Status", "Version", "Sprint", "Comment", "WorkItemChange"], ["GraphDomain"], []),
    "VALIDATED_BY": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Document", "DocumentSection", "Repository", "Project", "Tag", "Release", "Job", "Artifact", "Deployment", "IssueType", "Status", "Version", "Sprint", "Comment", "WorkItemChange"], ["ValidationRun"], []),
    "PRODUCED_BY": (["PipelineRun", "Document", "DocumentSection", "Release", "Deployment"], ["Commit", "PipelineRun", "MergeRequest", "Job"], []),
}

# Index baseline (11-graph-schema.md §Index baseline; FR-GRAPH-008)
INDEXES: list[dict] = [
    {"name": "idx_canonical_id", "type": "UNIQUE", "label": None, "fields": ["canonical_id"]},
    {"name": "idx_source_identity", "type": "SECONDARY", "label": None, "fields": ["source_system", "source_id"]},
    {"name": "idx_issue_key", "type": "SECONDARY", "label": "WorkItem", "fields": ["issue_key"]},
    {"name": "idx_commit_sha", "type": "SECONDARY", "label": "Commit", "fields": ["commit_sha"]},
    {"name": "idx_repo_path", "type": "SECONDARY", "label": "File", "fields": ["repo_id", "path"]},
    {"name": "idx_qualified_name", "type": "SECONDARY", "label": "CodeSymbol", "fields": ["qualified_name"]},
    {"name": "idx_domain_type", "type": "SECONDARY", "label": None, "fields": ["graph_domain", "entity_type"]},
    {"name": "idx_name", "type": "SECONDARY", "label": None, "fields": ["name"]},
    {"name": "idx_entity_revision_current", "type": "SECONDARY", "label": "EntityRevision", "fields": ["subject_id", "is_current"]},
    {"name": "idx_relationship_revision_current", "type": "SECONDARY", "label": "RelationshipRevision", "fields": ["relationship_id", "is_current"]},
    {"name": "idx_graph_version", "type": "SECONDARY", "label": "GraphVersion", "fields": ["graph_version"]},
]

# Business vertex labels counted as "business" (non-meta) facts
BUSINESS_LABELS = [
    label for label, (domain, _req, _opt) in VERTEX_LABELS.items() if domain != "META"
]


def edge_endpoints_valid(edge_label: str, out_label: str, in_label: str) -> bool:
    spec = EDGE_LABELS.get(edge_label)
    if spec is None:
        return False
    outs, ins, _props = spec
    return out_label in outs and in_label in ins


def label_known(label: str) -> bool:
    return label in VERTEX_LABELS or label in EDGE_LABELS


def domain_of(label: str) -> str | None:
    if label in VERTEX_LABELS:
        return VERTEX_LABELS[label][0]
    return None
