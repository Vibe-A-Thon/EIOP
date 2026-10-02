"""Ontology vocabulary and HugeGraph schema manifest (FR-ONTO-001, FR-ONTO-002).

The ontology is a controlled vocabulary: every entity type and relationship
declares domain/range, required properties and lifecycle/version. MVP terms
are enumerated here; namespaces for Organization, Work, Code, CI/CD,
Operations, Knowledge and AI/Agent concepts are preserved.
"""

ONTOLOGY_VERSION = "0.1.1"
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
    "section_index": "INT",
    "agent_id": "TEXT",
    "goal": "TEXT",
    "budgets": "TEXT",
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
    "Document": ("KNOWLEDGE", ["canonical_id", "name", "path"], ["doc_format", "content_hash", "repo_id"]),
    "DocumentSection": ("KNOWLEDGE", ["canonical_id", "name"], ["path", "section_index", "content_hash", "start_line", "end_line"]),
    "AgentRun": ("AGENT", ["canonical_id", "agent_id", "goal"], ["run_status", "budgets", "started_at", "finished_at"]),
}

# Edge labels -> (out vertex labels, in vertex labels, properties)
# Endpoint/domain-range validation uses these constraints (FR-ONTO-002,
# FR-VALID-002). RELATED_TO is deliberately absent (forbidden).
EDGE_LABELS: dict[str, tuple[list[str], list[str], list[str]]] = {
    "CONTAINS": (["Project", "Repository", "Document", "DataSource"], ["WorkItem", "File", "DocumentSection", "Project"], []),
    "PARENT_OF": (["WorkItem"], ["WorkItem"], []),
    "ASSIGNED_TO": (["WorkItem"], ["Person"], []),
    "AUTHORED_BY": (["Commit", "MergeRequest"], ["Person"], []),
    "HAS_BRANCH": (["Repository"], ["Branch"], []),
    "HAS_COMMIT": (["Repository", "Branch"], ["Commit"], []),
    "HAS_MERGE_REQUEST": (["Repository"], ["MergeRequest"], []),
    "MODIFIES": (["Commit"], ["File"], []),
    "DECLARES": (["File"], ["CodeSymbol"], []),
    "CALLS": (["CodeSymbol"], ["CodeSymbol"], []),
    "IMPORTS": (["File", "CodeSymbol"], ["Dependency"], []),
    "DEPENDS_ON": (["CodeSymbol", "File"], ["Dependency", "CodeSymbol"], []),
    "IMPLEMENTS": (["MergeRequest", "Commit"], ["WorkItem"], []),
    "REFERENCES": (["MergeRequest", "Commit", "Document", "DocumentSection", "WorkItem", "PipelineRun"], ["WorkItem", "Commit", "CodeSymbol", "Dependency", "File"], []),
    "DOCUMENTS": (["Document", "DocumentSection"], ["CodeSymbol", "WorkItem", "File"], []),
    "EVIDENCED_BY": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Dependency", "Document", "DocumentSection", "Person", "Project", "Repository", "Branch"], ["Evidence"], []),
    "INGESTED_IN": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Document", "DocumentSection", "Person", "Project", "Repository", "Branch", "Dependency"], ["IngestionRun"], []),
    "BELONGS_TO_DOMAIN": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Document", "DocumentSection", "Person", "Project", "Repository", "Branch", "Dependency", "Evidence"], ["GraphDomain"], []),
    "VALIDATED_BY": (["WorkItem", "Commit", "File", "CodeSymbol", "MergeRequest", "PipelineRun", "Document", "DocumentSection", "Repository", "Project"], ["ValidationRun"], []),
    "PRODUCED_BY": (["PipelineRun", "Document", "DocumentSection"], ["Commit", "PipelineRun", "MergeRequest"], []),
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
