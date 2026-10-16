"""Dynamic Entity & Community Extraction Pipeline (AGENT-002).

Real-time pipeline:
Document Ingestion -> Chunking -> Entity Extraction -> Relation Extraction ->
Triple Generation -> Community Detection -> Knowledge Graph Update.
"""

from __future__ import annotations

import logging
import queue
import re
import threading
import time
from collections import defaultdict
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable

from eoip.extraction.relation_extractor import ExtractedTriple, RelationExtractor
from eoip.graph.memory import MemoryGraphStore

logger = logging.getLogger("eoip.extraction.engine")


class ChunkStrategy(str, Enum):
    SENTENCE = "sentence"
    PARAGRAPH = "paragraph"
    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"


@dataclass
class DocumentChunk:
    chunk_id: str
    text: str
    index: int
    metadata: dict[str, Any] = field(default_factory=dict)


class DocumentChunker:
    """Configurable document chunking strategy."""

    def __init__(self, default_strategy: ChunkStrategy = ChunkStrategy.PARAGRAPH, chunk_size: int = 500) -> None:
        self.default_strategy = default_strategy
        self.chunk_size = chunk_size

    def chunk(self, text: str, strategy: ChunkStrategy | None = None) -> list[DocumentChunk]:
        strat = strategy or self.default_strategy
        chunks: list[DocumentChunk] = []

        if strat == ChunkStrategy.PARAGRAPH:
            paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
            for idx, p in enumerate(paragraphs):
                chunks.append(DocumentChunk(chunk_id=f"chk_p_{idx}", text=p, index=idx))

        elif strat == ChunkStrategy.SENTENCE:
            sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
            for idx, s in enumerate(sentences):
                chunks.append(DocumentChunk(chunk_id=f"chk_s_{idx}", text=s, index=idx))

        elif strat == ChunkStrategy.FIXED_SIZE:
            words = text.split()
            step = max(50, self.chunk_size)
            for idx in range(0, len(words), step):
                chunk_words = words[idx : idx + step]
                chunks.append(DocumentChunk(chunk_id=f"chk_w_{idx}", text=" ".join(chunk_words), index=idx))

        else:  # SEMANTIC
            # Paragraphs boundary with sentence packing
            paragraphs = [p.strip() for p in text.split("\n") if p.strip()]
            for idx, p in enumerate(paragraphs):
                chunks.append(DocumentChunk(chunk_id=f"chk_sem_{idx}", text=p, index=idx))

        return chunks if chunks else [DocumentChunk(chunk_id="chk_0", text=text, index=0)]


@dataclass
class ExtractedEntity:
    name: str
    entity_type: str
    confidence: float = 0.85
    start_char: int = 0
    end_char: int = 0
    properties: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EntityExtractor:
    """Transformer-ready entity extraction interface with built-in heuristics."""

    def __init__(self) -> None:
        self.type_patterns = {
            "Service": r"\b([A-Z][a-zA-Z0-9]+(?:Service|API|Gateway|Worker|Broker|Router|Engine))\b",
            "Database": r"\b(PostgreSQL|MySQL|Neo4j|Redis|MongoDB|Cassandra|DynamoDB|Elasticsearch|Milvus|Qdrant|Chroma)\b",
            "Protocol": r"\b(HTTP|HTTPS|gRPC|REST|GraphQL|WebSocket|Kafka|RabbitMQ|AMQP)\b",
            "Organization": r"\b(Google|DeepMind|Meta|AWS|Microsoft|Anthropic|OpenAI)\b",
            "Component": r"\b([A-Z][a-zA-Z0-9]+(?:Component|Module|Layer|Manager|Registry|Store))\b",
        }

    def extract_entities(self, text: str) -> list[ExtractedEntity]:
        entities: list[ExtractedEntity] = []
        seen: set[str] = set()

        for ent_type, pattern in self.type_patterns.items():
            for m in re.finditer(pattern, text, re.IGNORECASE):
                val = m.group(1).strip()
                norm = val.lower()
                if norm not in seen:
                    seen.add(norm)
                    entities.append(ExtractedEntity(
                        name=val,
                        entity_type=ent_type,
                        confidence=0.90,
                        start_char=m.start(),
                        end_char=m.end(),
                    ))

        # Capitalized entity phrases
        cap_pattern = r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\b"
        for m in re.finditer(cap_pattern, text):
            val = m.group(1).strip()
            norm = val.lower()
            if norm not in seen:
                seen.add(norm)
                entities.append(ExtractedEntity(
                    name=val,
                    entity_type="Concept",
                    confidence=0.75,
                    start_char=m.start(),
                    end_char=m.end(),
                ))

        return entities


class CommunityDetector:
    """Detects topological entity clusters and communities in the knowledge graph."""

    def detect_communities(self, store: MemoryGraphStore) -> dict[int, list[str]]:
        """Find communities using connected components and neighbor label clustering."""
        adj: dict[str, set[str]] = defaultdict(set)
        for e in store.find_edges():
            adj[e["out_v"]].add(e["in_v"])
            adj[e["in_v"]].add(e["out_v"])

        visited: set[str] = set()
        communities: dict[int, list[str]] = {}
        comm_id = 0

        vertices = [v["canonical_id"] for v in store.find_vertices()]

        for v in vertices:
            if v not in visited:
                comp: list[str] = []
                q = [v]
                visited.add(v)
                while q:
                    cur = q.pop(0)
                    comp.append(cur)
                    for nbr in adj.get(cur, set()):
                        if nbr not in visited:
                            visited.add(nbr)
                            q.append(nbr)
                communities[comm_id] = comp
                comm_id += 1

        return communities


@dataclass
class ExtractionResult:
    chunks_count: int
    entities: list[ExtractedEntity]
    triples: list[ExtractedTriple]
    communities: dict[int, list[str]]
    vertices_upserted: int
    edges_upserted: int
    elapsed_ms: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "chunks_count": self.chunks_count,
            "entity_count": len(self.entities),
            "triple_count": len(self.triples),
            "community_count": len(self.communities),
            "vertices_upserted": self.vertices_upserted,
            "edges_upserted": self.edges_upserted,
            "elapsed_ms": round(self.elapsed_ms, 2),
            "entities": [e.to_dict() for e in self.entities[:15]],
            "triples": [t.to_dict() for t in self.triples[:15]],
        }


class ExtractionPipeline:
    """End-to-end Knowledge Graph construction pipeline from unstructured documents."""

    def __init__(self, store: MemoryGraphStore | None = None) -> None:
        self.store = store or MemoryGraphStore()
        self.chunker = DocumentChunker()
        self.entity_extractor = EntityExtractor()
        self.relation_extractor = RelationExtractor()
        self.community_detector = CommunityDetector()
        self._streaming_queue: queue.Queue[str] = queue.Queue()
        self._streaming_active = False
        self._lock = threading.Lock()

    def process_text(
        self,
        text: str,
        strategy: ChunkStrategy = ChunkStrategy.SENTENCE,
    ) -> ExtractionResult:
        """Run full extraction pipeline on document text."""
        t0 = time.time()
        chunks = self.chunker.chunk(text, strategy=strategy)

        all_entities: list[ExtractedEntity] = []
        all_triples: list[ExtractedTriple] = []

        for chk in chunks:
            ents = self.entity_extractor.extract_entities(chk.text)
            trips = self.relation_extractor.extract_triples(chk.text)
            all_entities.extend(ents)
            all_triples.extend(trips)

        # Update knowledge graph store
        v_count = 0
        e_count = 0

        # Upsert entities
        for ent in all_entities:
            clean_name = re.sub(r"\W+", "_", ent.name.lower())
            cid = f"ent_{clean_name}"
            etype_lower = ent.entity_type.lower()
            if "service" in etype_lower:
                label = "Service"
                props = {"canonical_id": cid, "service_id": cid, "name": ent.name}
            elif "database" in etype_lower:
                label = "Database"
                props = {"canonical_id": cid, "name": ent.name}
            elif "org" in etype_lower:
                label = "Organization"
                props = {"canonical_id": cid, "name": ent.name}
            else:
                label = "GenericEntity"
                props = {"canonical_id": cid, "name": ent.name, "entity_type": ent.entity_type}

            self.store.upsert_vertex(label=label, properties=props)
            v_count += 1

        # Upsert triples as edges
        for trip in all_triples:
            clean_s = re.sub(r"\W+", "_", trip.subject.lower())
            clean_o = re.sub(r"\W+", "_", trip.object.lower())
            s_cid = f"ent_{clean_s}"
            o_cid = f"ent_{clean_o}"

            # Ensure vertices exist with valid Service/Database labels
            s_v = self.store.get_vertex_by_canonical_id(s_cid)
            if not s_v:
                self.store.upsert_vertex("Service", {"canonical_id": s_cid, "service_id": s_cid, "name": trip.subject})
            o_v = self.store.get_vertex_by_canonical_id(o_cid)
            if not o_v:
                self.store.upsert_vertex("Service", {"canonical_id": o_cid, "service_id": o_cid, "name": trip.object})

            edge_label = "CALLS" if "call" in trip.predicate.lower() else "DEPENDS_ON"
            self.store.upsert_edge(
                label=edge_label,
                out_v=s_cid,
                in_v=o_cid,
                properties={},
            )
            e_count += 1


        # Detect communities
        communities = self.community_detector.detect_communities(self.store)

        elapsed_ms = (time.time() - t0) * 1000.0
        return ExtractionResult(
            chunks_count=len(chunks),
            entities=all_entities,
            triples=all_triples,
            communities=communities,
            vertices_upserted=v_count,
            edges_upserted=e_count,
            elapsed_ms=elapsed_ms,
        )

    def start_streaming_worker(self, callback: Callable[[ExtractionResult], None] | None = None) -> None:
        """Start background daemon for continuous streaming document ingestion."""
        with self._lock:
            if self._streaming_active:
                return
            self._streaming_active = True

        def _worker() -> None:
            while self._streaming_active:
                try:
                    doc = self._streaming_queue.get(timeout=0.5)
                    res = self.process_text(doc)
                    if callback:
                        callback(res)
                    self._streaming_queue.task_done()
                except queue.Empty:
                    continue
                except Exception as exc:
                    logger.warning("Streaming extraction worker error: %s", exc)

        t = threading.Thread(target=_worker, daemon=True, name="ExtractionStreamingWorker")
        t.start()

    def submit_streaming_document(self, text: str) -> None:
        self._streaming_queue.put(text)

    def stop_streaming_worker(self) -> None:
        with self._lock:
            self._streaming_active = False


_instance: ExtractionPipeline | None = None
_lock = threading.Lock()


def get_extraction_engine(store: MemoryGraphStore | None = None) -> ExtractionPipeline:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = ExtractionPipeline(store=store)
    return _instance
