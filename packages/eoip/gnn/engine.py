"""Graph Neural Network Integration Engine (GRAPH-004).

GNN-powered and representation learning graph intelligence:
- GraphEmbedder: node2vec random-walk embeddings and TransE knowledge graph embeddings
- LinkPredictor: missing link prediction with calibrated confidence scores
- NodeClassifier: entity type/role inference via neighborhood message passing
- CommunityPredictor: graph-level pattern prediction and community clustering
"""

from __future__ import annotations

import logging
import threading
from dataclasses import asdict, dataclass
from enum import Enum
from typing import Any, NoReturn

from eoip.capabilities.model import CapabilityUnavailableError
from eoip.graph.memory import MemoryGraphStore
from eoip.neural.runtime import NeuralTier, require_tier

logger = logging.getLogger("eoip.gnn.engine")


class EmbeddingModelType(str, Enum):
    NODE2VEC = "NODE2VEC"
    TRANSE = "TRANSE"
    SAGE = "SAGE"


from eoip.retrieval.hybrid_vector_service import ProductionConfigurationError


class GraphEmbedder:
    """Compatibility boundary for qualified graph encoders; never fabricates embeddings."""

    def __init__(self, default_dimensions: int = 32, profile: str = "development") -> None:
        if profile.lower() == "production":
            raise ProductionConfigurationError(
                "Hash-based graph vectors are refused in production profile (CRA-025.7, CRA-025.9)"
            )
        self.default_dimensions = default_dimensions
        self.profile = profile

    @staticmethod
    def require_qualified_model(capability: str) -> NoReturn:
        require_tier(NeuralTier.NEURAL)
        raise CapabilityUnavailableError(
            capability_id=capability,
            reason="No trained model has passed the required evaluation and registry promotion gates.",
        )


@dataclass
class LinkPrediction:
    source_id: str
    target_id: str
    predicted_label: str
    confidence: float
    score: float

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class LinkPredictor:
    """Predicts missing graph connections using representation similarity."""

    def __init__(self, embedder: GraphEmbedder | None = None) -> None:
        self.embedder = embedder or GraphEmbedder()

    def predict_links(
        self,
        store: MemoryGraphStore,
        source_id: str,
        candidate_ids: list[str] | None = None,
        top_k: int = 5,
        default_label: str = "ASSOCIATED_WITH",
    ) -> list[LinkPrediction]:
        self.embedder.require_qualified_model("gnn.link-prediction")


@dataclass
class NodeClassification:
    vertex_id: str
    predicted_class: str
    confidence: float
    neighbor_evidence_count: int

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class NodeClassifier:
    """Compatibility boundary for a trained, promoted node classifier."""

    def classify_node(self, store: MemoryGraphStore, vertex_id: str) -> NodeClassification:
        GraphEmbedder.require_qualified_model("gnn.node-classification")


class GNNEngine:
    """Centralized Graph Neural Network and Graph Representation Engine."""

    _instance: GNNEngine | None = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        self.embedder = GraphEmbedder()
        self.link_predictor = LinkPredictor(self.embedder)
        self.node_classifier = NodeClassifier()

    @classmethod
    def get_instance(cls) -> GNNEngine:
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    def compute_embeddings(
        self,
        store: MemoryGraphStore,
        model_type: EmbeddingModelType = EmbeddingModelType.NODE2VEC,
        dimensions: int = 32,
    ) -> dict[str, list[float]]:
        self.embedder.require_qualified_model(f"gnn.embedding.{model_type.value.lower()}")

    def predict_links(
        self,
        store: MemoryGraphStore,
        source_id: str,
        top_k: int = 5,
    ) -> list[dict[str, Any]]:
        preds = self.link_predictor.predict_links(store, source_id, top_k=top_k)
        return [p.to_dict() for p in preds]

    def classify_node(self, store: MemoryGraphStore, vertex_id: str) -> dict[str, Any]:
        return self.node_classifier.classify_node(store, vertex_id).to_dict()


def get_gnn_engine() -> GNNEngine:
    return GNNEngine.get_instance()
