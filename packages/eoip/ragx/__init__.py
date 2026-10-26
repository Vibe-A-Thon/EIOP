"""RAG extensions (gap analysis §4): architectures, techniques, metrics, router.

- ``architectures`` — 22 §4 RAG architectures (Hierarchical, RAPTOR, LightRAG,
  HippoRAG, PathRAG, KGRAG, LazyGraphRAG, DRIFT, Global/LocalSearch, Temporal,
  Federated, Streaming, Incremental, StructuredData, Code, Multilingual,
  MultiAgent, PrivacyAware, ProvenanceAware, VersionAware, EventAware).
- ``techniques`` — 27 §4 retrieval/generation techniques (RAG-Fusion, RRF,
  chunking, reranking, verification, etc.).
- ``metrics`` — Recall@K, Precision@K, MRR, nDCG, citation accuracy,
  access-control correctness.
- ``router`` — lazy ``build_router(store)`` exposing ``/api/v1/ragx/*``.

Everything is deterministic-first; LLM narration is an optional hook with
graceful fallback. Remote federated sources are an External gate consumed via
``eoip.federation.planner.DataSourceAdapter``.
"""

from eoip.ragx.architectures import ARCHITECTURES, build_architecture
from eoip.ragx.core import Candidate, RagxArchitecture
from eoip.ragx.metrics import (
    access_control_correctness,
    citation_accuracy,
    mean_reciprocal_rank,
    ndcg_at_k,
    precision_at_k,
    recall_at_k,
)
from eoip.ragx.router import build_router
from eoip.ragx.techniques import TECHNIQUES

__all__ = [
    "ARCHITECTURES",
    "Candidate",
    "RagxArchitecture",
    "TECHNIQUES",
    "access_control_correctness",
    "build_architecture",
    "build_router",
    "citation_accuracy",
    "mean_reciprocal_rank",
    "ndcg_at_k",
    "precision_at_k",
    "recall_at_k",
]
