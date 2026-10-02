"""RetrievalResult v1 — GraphRAG context package.

Normative: EOIP-engg-doc-pkg/schemas/retrieval_result.schema.json
"""

from pydantic import BaseModel


class RetrievalContext(BaseModel):
    kind: str  # e.g. entity, relationship, path, document_section, summary
    ref: str
    text: str
    citations: list[str] = []


class RetrievalResult(BaseModel):
    retrieval_id: str
    strategy: str
    contexts: list[RetrievalContext] = []
    evidence_refs: list[str]
    metrics: dict | None = None
    answer: str | None = None
    warnings: list[str] | None = None
    generation: str | None = None
    partial: bool | None = None
    facts: list[dict] | None = None
    graph: dict | None = None
