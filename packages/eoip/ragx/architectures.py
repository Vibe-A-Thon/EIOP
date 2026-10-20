"""RAG extension architectures (gap analysis §4, table "RAG architectures").

Every architecture is deterministic-first: retrieval and answer scaffolding run
without any LLM; optional narration plugs in via ``RagxArchitecture``'s
``narrator`` hook. External integrations (remote federated sources) are
marked **External gate** and accept adapter protocols instead of faking
connectivity.
"""

from __future__ import annotations

import hashlib
import math
import re
from collections import defaultdict
from typing import Any

from eoip.graph.store import GraphStore
from eoip.ragx.core import Candidate, RagxArchitecture, all_vertices, overlap_score, vertex_text

_SENTENCE_RE = re.compile(r"(?<=[.!?])\s+|\n+")
_STOPWORDS = frozenset(
    "the a an and or of to in on for with is are was were be been by at as it its this that".split()
)


def _keywords(query: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9_]+", query.lower()) if t not in _STOPWORDS and len(t) > 2}


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in _SENTENCE_RE.split(text) if s.strip()]


def _summary(text: str, max_sentences: int = 2) -> str:
    """Deterministic extractive summary: highest token-coverage sentences."""
    sents = _sentences(text)
    if len(sents) <= max_sentences:
        return " ".join(sents)
    tokens = set(_keywords(text))
    scored = sorted(
        sents,
        key=lambda s: (-len(_keywords(s) & tokens), s),
    )
    ordered = sorted(scored[:max_sentences], key=sents.index)
    return " ".join(ordered)


# ---------------------------------------------------------------------------
# A1. Hierarchical RAG
# ---------------------------------------------------------------------------


class HierarchicalRAG(RagxArchitecture):
    """§4 Hierarchical RAG: coarse label/community level first, then members."""

    name = "hierarchical"
    description = "Hierarchical RAG: top-level grouping selection, then member drill-down"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for v in all_vertices(self._store):
            groups[v["label"]].append(v)
        scored = []
        for label, members in groups.items():
            text = " ".join(vertex_text(m["label"], m["properties"]) for m in members)
            scored.append((overlap_score(query, text), label, members))
        scored.sort(key=lambda item: (-item[0], item[1]))
        out: list[Candidate] = []
        for group_score, label, members in scored[:2]:
            out.append(Candidate(
                source_id=f"urn:eoip:ragx:group:{label}",
                text=f"[{label}] group summary: {_summary(' '.join(vertex_text(m['label'], m['properties']) for m in members))}",
                score=group_score,
                kind="community",
                label=label,
            ))
            for m in members[: int(context.get("members_per_group", 5))]:
                text = vertex_text(m["label"], m["properties"])
                out.append(Candidate(
                    source_id=m["canonical_id"],
                    text=text,
                    score=group_score * (0.5 + 0.5 * overlap_score(query, text)),
                    label=m["label"],
                    properties=dict(m["properties"]),
                    citations=[r for r in (m["properties"].get("source_ref"),) if r],
                ))
        return out


# ---------------------------------------------------------------------------
# A2. RAPTOR-style recursive clustering summary tree
# ---------------------------------------------------------------------------


def _token_jaccard(a: str, b: str) -> float:
    ta, tb = _keywords(a), _keywords(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


class RaptorTree:
    """Deterministic RAPTOR tree: agglomerative clustering by token Jaccard."""

    def __init__(self, documents: dict[str, str], threshold: float = 0.25) -> None:
        self.leaf_ids = sorted(documents)
        self.nodes: dict[str, dict[str, Any]] = {}
        clusters = [[cid] for cid in self.leaf_ids]
        level = 0
        while True:
            merged = self._merge_pass(clusters, documents, threshold)
            if len(merged) == len(clusters):
                break
            clusters = merged
            level += 1
            if level > 10:
                break
        for idx, cluster in enumerate(clusters):
            text = " ".join(documents[cid] for cid in cluster)
            node_id = f"urn:eoip:ragx:raptor:root:{idx}"
            self.nodes[node_id] = {
                "members": cluster,
                "summary": _summary(text, 3),
                "text": text,
            }
        self.roots = [f"urn:eoip:ragx:raptor:root:{i}" for i in range(len(clusters))]

    def _merge_pass(self, clusters, documents, threshold):
        used = [False] * len(clusters)
        merged = []
        texts = [" ".join(documents[cid] for cid in c) for c in clusters]
        for i in range(len(clusters)):
            if used[i]:
                continue
            group = list(clusters[i])
            used[i] = True
            for j in range(i + 1, len(clusters)):
                if used[j]:
                    continue
                if _token_jaccard(texts[i], texts[j]) >= threshold:
                    group.extend(clusters[j])
                    used[j] = True
            merged.append(group)
        return merged


class RaptorRAG(RagxArchitecture):
    """§4 RAPTOR: recursive clustering + summary tree, top-down retrieval."""

    name = "raptor"
    description = "RAPTOR-style recursive clustering summary tree retrieval"

    def __init__(self, store: GraphStore, *args: Any, **kwargs: Any) -> None:
        super().__init__(store, *args, **kwargs)
        self._tree: RaptorTree | None = None

    @property
    def tree(self) -> RaptorTree:
        if self._tree is None:
            docs = {
                v["canonical_id"]: vertex_text(v["label"], v["properties"])
                for v in all_vertices(self._store)
            }
            self._tree = RaptorTree(docs)
        return self._tree

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        tree = self.tree
        scored = sorted(
            ((overlap_score(query, tree.nodes[r]["summary"] + " " + tree.nodes[r]["text"]), r) for r in tree.roots),
            key=lambda item: (-item[0], item[1]),
        )
        out: list[Candidate] = []
        for score, root_id in scored[:2]:
            node = tree.nodes[root_id]
            out.append(Candidate(
                source_id=root_id, text=node["summary"], score=score, kind="community",
            ))
            members = sorted(node["members"], key=lambda cid: (-overlap_score(query, cid), cid))
            for cid in members[: int(context.get("leaf_count", 5))]:
                if cid in tree.leaf_ids:
                    vertex = self._store.get_vertex_by_canonical_id(cid)
                    if vertex:
                        text = vertex_text(vertex["label"], vertex["properties"])
                        out.append(Candidate(
                            source_id=cid, text=text,
                            score=score * (0.4 + 0.6 * overlap_score(query, text)),
                            label=vertex["label"], properties=dict(vertex["properties"]),
                        ))
        return out


# ---------------------------------------------------------------------------
# A3. LightRAG-style dual local/global over a lightweight KG
# ---------------------------------------------------------------------------


def _extract_mentions(text: str) -> list[str]:
    """Lightweight entity extraction: capitalized spans (deterministic)."""
    return sorted(set(re.findall(r"\b[A-Z][A-Za-z0-9_]+(?:\s+[A-Z][A-Za-z0-9_]+)*\b", text)))


class LightKG:
    """Lightweight knowledge graph: entity mentions + co-mention relations."""

    def __init__(self, documents: dict[str, str]) -> None:
        self.entity_docs: dict[str, set[str]] = defaultdict(set)
        self.doc_entities: dict[str, set[str]] = {}
        for cid, text in documents.items():
            ents = set(_extract_mentions(text)) | {cid}
            self.doc_entities[cid] = ents
            for e in ents:
                self.entity_docs[e].add(cid)
        self.edges: dict[tuple[str, str], set[str]] = defaultdict(set)
        for cid, ents in self.doc_entities.items():
            ordered = sorted(ents)
            for i in range(len(ordered)):
                for j in range(i + 1, len(ordered)):
                    self.edges[(ordered[i], ordered[j])].add(cid)

    def related_entities(self, entity: str, limit: int = 20) -> list[str]:
        out: set[str] = set()
        for (a, b), _docs in self.edges.items():
            if a == entity:
                out.add(b)
            elif b == entity:
                out.add(a)
        return sorted(out)[:limit]

    def top_relations(self, query: str, limit: int = 20) -> list[tuple[str, str, float]]:
        q = _keywords(query)
        scored = []
        for (a, b), docs in self.edges.items():
            score = len(_keywords(a + " " + b) & q) + 0.01 * len(docs)
            if score > 0:
                scored.append((a, b, score))
        scored.sort(key=lambda item: (-item[2], item[0], item[1]))
        return scored[:limit]


class LightRAG(RagxArchitecture):
    """§4 LightRAG: dual LOW-level (entity-centric) / HIGH-level (relation-centric) retrieval."""

    name = "lightrag"
    description = "LightRAG-style dual local/global retrieval over a lightweight KG"

    def __init__(self, store: GraphStore, *args: Any, **kwargs: Any) -> None:
        super().__init__(store, *args, **kwargs)
        self._kg: LightKG | None = None

    @property
    def kg(self) -> LightKG:
        if self._kg is None:
            docs = {
                v["canonical_id"]: vertex_text(v["label"], v["properties"])
                for v in all_vertices(self._store)
            }
            self._kg = LightKG(docs)
        return self._kg

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        mode = str(context.get("mode", "hybrid")).lower()
        kg = self.kg
        out: list[Candidate] = []
        if mode in ("low", "local", "hybrid"):
            seeds = [e for e in kg.entity_docs if _keywords(e) & _keywords(query)]
            for seed in sorted(seeds)[:5]:
                for cid in sorted(kg.entity_docs[seed])[:3]:
                    vertex = self._store.get_vertex_by_canonical_id(cid)
                    if vertex:
                        out.append(Candidate(
                            source_id=cid,
                            text=vertex_text(vertex["label"], vertex["properties"]),
                            score=1.0,
                            label=vertex["label"],
                            properties=dict(vertex["properties"]),
                        ))
        if mode in ("high", "global", "hybrid"):
            for a, b, score in kg.top_relations(query, limit=int(context.get("top_k", 10))):
                out.append(Candidate(
                    source_id=f"urn:eoip:ragx:rel:{hashlib.sha1(f'{a}|{b}'.encode()).hexdigest()[:12]}",
                    text=f"{a} -[related]-> {b}",
                    score=score,
                    kind="relation",
                ))
        seen: set[str] = set()
        unique: list[Candidate] = []
        for c in out:
            if c.source_id in seen:
                continue
            seen.add(c.source_id)
            unique.append(c)
        return unique[: int(context.get("top_k", 10)) * 2]


# ---------------------------------------------------------------------------
# A4. HippoRAG-style associative memory (PPR over mention graph)
# ---------------------------------------------------------------------------


class HippoRAG(RagxArchitecture):
    """§4 HippoRAG: Personalized-PageRank spreading activation over a mention graph."""

    name = "hipporag"
    description = "HippoRAG-style associative memory via PPR over the mention graph"

    def __init__(self, store: GraphStore, *args: Any, alpha: float = 0.35, **kwargs: Any) -> None:
        super().__init__(store, *args, **kwargs)
        self.alpha = alpha
        self._kg: LightKG | None = None

    @property
    def kg(self) -> LightKG:
        if self._kg is None:
            docs = {
                v["canonical_id"]: vertex_text(v["label"], v["properties"])
                for v in all_vertices(self._store)
            }
            self._kg = LightKG(docs)
        return self._kg

    def _ppr(self, seeds: dict[str, float], iterations: int = 20) -> dict[str, float]:
        kg = self.kg
        nodes = sorted(kg.entity_docs)
        rank = {n: 0.0 for n in nodes}
        for n, s in seeds.items():
            if n in rank:
                rank[n] = s
        adj: dict[str, set[str]] = defaultdict(set)
        for (a, b) in kg.edges:
            adj[a].add(b)
            adj[b].add(a)
        for _ in range(iterations):
            nxt = {n: (1.0 - self.alpha) * seeds.get(n, 0.0) for n in nodes}
            for n in nodes:
                r = rank[n]
                if r == 0.0:
                    continue
                nbrs = adj.get(n)
                if not nbrs:
                    continue
                share = self.alpha * r / len(nbrs)
                for m in nbrs:
                    nxt[m] += share
            if max(abs(nxt[n] - rank[n]) for n in nodes) < 1e-9:
                rank = nxt
                break
            rank = nxt
        return rank

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        kg = self.kg
        q = _keywords(query)
        seeds = {
            e: 1.0 / max(1, len([e]))
            for e in kg.entity_docs
            if _keywords(e) & q
        }
        if not seeds:
            return self.search(query, top_k=int(context.get("top_k", 10)))
        total = sum(seeds.values())
        seeds = {k: v / total for k, v in seeds.items()}
        rank = self._ppr(seeds)
        scored = sorted(rank.items(), key=lambda kv: (-kv[1], kv[0]))
        out: list[Candidate] = []
        for entity, r in scored[: int(context.get("top_k", 10)) * 3]:
            for cid in sorted(kg.entity_docs[entity])[:2]:
                vertex = self._store.get_vertex_by_canonical_id(cid)
                if vertex:
                    out.append(Candidate(
                        source_id=cid,
                        text=vertex_text(vertex["label"], vertex["properties"]),
                        score=r,
                        label=vertex["label"],
                        properties=dict(vertex["properties"]),
                    ))
        seen: set[str] = set()
        unique = []
        for c in out:
            if c.source_id not in seen:
                seen.add(c.source_id)
                unique.append(c)
        return unique[: int(context.get("top_k", 10))]


# ---------------------------------------------------------------------------
# A5. PathRAG — path-pruned context
# ---------------------------------------------------------------------------


class PathRAG(RagxArchitecture):
    """§4 PathRAG: keep only entities lying on relevant inter-seed paths."""

    name = "pathrag"
    description = "PathRAG: prune context to entities on paths between query-relevant seeds"

    def _bfs_path(self, src_vid: str, dst_vid: str, max_depth: int = 4) -> list[str] | None:
        from collections import deque

        queue: deque[tuple[str, list[str]]] = deque([(src_vid, [src_vid])])
        seen = {src_vid}
        while queue:
            vid, path = queue.popleft()
            if vid == dst_vid:
                return path
            if len(path) > max_depth:
                continue
            for edge in self._store.edges_from(vid, limit=100) + self._store.edges_to(vid, limit=100):
                nxt = edge["in_v"] if edge["out_v"] == vid else edge["out_v"]
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append((nxt, path + [nxt]))
        return None

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        seeds = self.search(query, top_k=int(context.get("seed_count", 4)))
        seed_vids = []
        for c in seeds:
            v = self._store.get_vertex_by_canonical_id(c.source_id)
            if v:
                seed_vids.append(v["vid"])
        max_paths = int(context.get("max_paths", 3))
        out: list[Candidate] = []
        seen_paths: set[tuple[str, ...]] = set()
        for i in range(len(seed_vids)):
            for j in range(i + 1, len(seed_vids)):
                if len(out) >= max_paths:
                    break
                path = self._bfs_path(seed_vids[i], seed_vids[j], int(context.get("max_depth", 4)))
                if not path:
                    continue
                key = tuple(path)
                if key in seen_paths:
                    continue
                seen_paths.add(key)
                cids = []
                for vid in path:
                    vertex = self._store.get_vertex(vid)
                    if vertex:
                        cids.append(vertex["canonical_id"])
                score = sum(c.score for c in seeds if c.source_id in cids) / max(1, len(cids))
                out.append(Candidate(
                    source_id=f"urn:eoip:ragx:path:{len(out) + 1}",
                    text=" -> ".join(cids),
                    score=score * len(cids),
                    kind="path",
                    properties={"path": cids},
                ))
        if not out:  # fall back to plain search when graph has no inter-seed paths
            return seeds
        return out


# ---------------------------------------------------------------------------
# A6. KGRAG — entity-relation grounded
# ---------------------------------------------------------------------------


class KGRAG(RagxArchitecture):
    """§4 KGRAG: answers grounded in (entity, relation, entity) triples."""

    name = "kgrag"
    description = "KGRAG: entity-relation grounded retrieval with explicit triples"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        base = self.search(query, top_k=int(context.get("seed_count", 5)))
        out: list[Candidate] = []
        for c in base:
            out.append(c)
            for rel in self.relations_of(c.source_id, limit=int(context.get("relations_per_entity", 5))):
                if rel["from"] == c.source_id or rel["to"] == c.source_id:
                    out.append(Candidate(
                        source_id=rel["eid"] or f"urn:eoip:ragx:rel:{len(out)}",
                        text=f"{rel['from']} -[{rel['label']}]-> {rel['to']}",
                        score=c.score * 0.8,
                        kind="relation",
                        citations=rel["citations"],
                    ))
        return out[: int(context.get("top_k", 15))]

    def generate(self, query: str, candidates: list[Candidate], context: dict[str, Any]) -> Any:
        triples = [c for c in candidates if c.kind == "relation"]
        if not triples:
            return super().generate(query, candidates, context)
        lines = [f"  - {t.text}" for t in triples[:10]]
        from eoip.graph.rag_router import RAGResult

        return RAGResult(
            answer=f"Grounded triples for '{query}':\n" + "\n".join(lines),
            pattern=self.name,
            confidence=min(0.9, 0.4 + 0.05 * len(triples)),
            sources=[c.source_id for c in candidates if c.source_id],
            highlight_ids=[c.source_id for c in candidates[:10]],
            metadata={"generation": "deterministic", "triple_count": len(triples)},
        )


# ---------------------------------------------------------------------------
# A7. LazyGraphRAG — token-budget graph retrieval
# ---------------------------------------------------------------------------


class LazyGraphRAG(RagxArchitecture):
    """§4 LazyGraphRAG: defer deep graph work; fill a token budget greedily."""

    name = "lazygraphrag"
    description = "LazyGraphRAG: token-budgeted greedy evidence packing"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        budget = int(context.get("token_budget", 200))
        pool = self.search(query, top_k=int(context.get("pool_size", 30)))
        pool.sort(key=lambda c: (-c.score, c.source_id))
        out: list[Candidate] = []
        used = 0
        for c in pool:
            cost = max(1, len(c.text.split()))
            if used + cost > budget:
                continue
            used += cost
            out.append(c)
        return out


# ---------------------------------------------------------------------------
# A8. DRIFT-style: community -> local drill
# ---------------------------------------------------------------------------


class DRIFTRAG(RagxArchitecture):
    """§4 DRIFT search: community-level summary first, then local drill-down."""

    name = "drift"
    description = "DRIFT-style: community answer followed by entity-level drill-down"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        from eoip.graph.community import CommunityDetectionEngine

        engine = CommunityDetectionEngine(self._store)
        out: list[Candidate] = []
        try:
            result = engine.detect(algorithm="louvain", resolution=1.0)
            communities = result.get("communities", [])
        except Exception:  # noqa: BLE001 - fall back to label grouping
            communities = []
        if not communities:
            hierarchical = HierarchicalRAG(self._store, self._index, self._policy, self._narrator)
            return hierarchical.retrieve(query, context)
        scored = sorted(
            communities,
            key=lambda comm: (-overlap_score(query, " ".join(map(str, comm.get("members", [])))), str(comm.get("id"))),
        )
        best = scored[0]
        members = list(best.get("members", []))[: int(context.get("drill_count", 6))]
        out.append(Candidate(
            source_id=f"urn:eoip:ragx:community:{best.get('id')}",
            text=f"Community {best.get('id')} ({best.get('size', len(members))} members): "
                 + ", ".join(map(str, members)),
            score=1.0,
            kind="community",
        ))
        for cid in members:
            vertex = self._store.get_vertex_by_canonical_id(str(cid))
            if vertex:
                text = vertex_text(vertex["label"], vertex["properties"])
                out.append(Candidate(
                    source_id=vertex["canonical_id"], text=text,
                    score=0.5 + 0.5 * overlap_score(query, text),
                    label=vertex["label"], properties=dict(vertex["properties"]),
                ))
        return out


# ---------------------------------------------------------------------------
# A9/A10. GlobalSearch / LocalSearch (Microsoft GraphRAG split)
# ---------------------------------------------------------------------------


class GlobalSearch(RagxArchitecture):
    """§4 GlobalSearch: map-reduce over all communities for graph-wide questions."""

    name = "global_search"
    description = "GlobalSearch: community summaries ranked and merged graph-wide"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        from eoip.graph.community import CommunityDetectionEngine

        try:
            result = CommunityDetectionEngine(self._store).detect(algorithm="louvain", resolution=1.0)
            communities = result.get("communities", [])
        except Exception:  # noqa: BLE001
            communities = []
        if not communities:
            groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
            for v in all_vertices(self._store):
                groups[v["label"]].append(v)
            communities = [
                {"id": label, "members": [m["canonical_id"] for m in members], "size": len(members)}
                for label, members in groups.items()
            ]
        scored = []
        for comm in communities:
            member_text = " ".join(
                vertex_text(v["label"], v["properties"])
                for m in comm.get("members", [])
                if (v := self._store.get_vertex_by_canonical_id(str(m))) is not None
            )
            scored.append((overlap_score(query, member_text), comm))
        scored.sort(key=lambda item: (-item[0], str(item[1].get("id"))))
        out = []
        for score, comm in scored[: int(context.get("top_k", 5))]:
            members = [str(m) for m in comm.get("members", [])]
            out.append(Candidate(
                source_id=f"urn:eoip:ragx:community:{comm.get('id')}",
                text=f"Community {comm.get('id')}: {_summary(' '.join(members), 2)}",
                score=score,
                kind="community",
                properties={"members": members},
            ))
        return out


class LocalSearch(RagxArchitecture):
    """§4 LocalSearch: seed-centric multi-hop expansion with keyword filtering."""

    name = "local_search"
    description = "LocalSearch: entity-centric neighborhood expansion"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        seeds = self.search(query, top_k=int(context.get("seed_count", 3)))
        hops = int(context.get("hops", 2))
        out: list[Candidate] = []
        for c in seeds:
            for vertex in self.neighborhood(c.source_id, max_hops=hops, limit=int(context.get("limit", 30))):
                text = vertex_text(vertex["label"], vertex["properties"])
                out.append(Candidate(
                    source_id=vertex["canonical_id"],
                    text=text,
                    score=c.score * (0.4 + 0.6 * overlap_score(query, text)),
                    label=vertex["label"],
                    properties=dict(vertex["properties"]),
                ))
        seen: set[str] = set()
        unique = []
        for cand in sorted(out, key=lambda x: (-x.score, x.source_id)):
            if cand.source_id not in seen:
                seen.add(cand.source_id)
                unique.append(cand)
        return unique[: int(context.get("top_k", 10))]


# ---------------------------------------------------------------------------
# A11. TemporalRAG — bitemporal filtering
# ---------------------------------------------------------------------------


class TemporalRAG(RagxArchitecture):
    """§4 TemporalRAG: evidence filtered to a bitemporal coordinate.

    Uses ``eoip.graph.bitemporal.BitemporalQueryEngine`` when the store keeps
    an ``EntityRevision`` journal; otherwise filters vertex properties
    (``valid_from`` / ``valid_to`` / ``observed_at``) directly.
    """

    name = "temporal"
    description = "TemporalRAG: bitemporally-filtered retrieval (valid/known time)"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        valid_at = context.get("valid_at")
        known_at = context.get("known_at")
        base = self.search(query, top_k=int(context.get("pool_size", 25)))
        from eoip.graph.bitemporal import ENTITY_REVISION_LABEL, BitemporalQueryEngine

        has_journal = bool(self._store.find_vertices(label=ENTITY_REVISION_LABEL, limit=1))
        if has_journal and (valid_at or known_at):
            engine = BitemporalQueryEngine(self._store)
            if valid_at and known_at:
                state = engine.slice(valid_at, known_at)
            elif known_at:
                state = engine.known_at(known_at)
            else:
                state = engine.valid_at(valid_at)
            live = {r.subject_id for r in state.entities if not r.is_delete}
            base = [c for c in base if c.source_id in live]
        else:
            base = [c for c in base if self._prop_valid(c.properties, valid_at, known_at)]
        return base[: int(context.get("top_k", 10))]

    @staticmethod
    def _prop_valid(props: dict[str, Any], valid_at: str | None, known_at: str | None) -> bool:
        if known_at is not None and props.get("observed_at", "\x00") > known_at:
            return False
        if valid_at is not None:
            vf = props.get("valid_from")
            vt = props.get("valid_to")
            if vf is not None and valid_at < str(vf):
                return False
            if vt is not None and valid_at >= str(vt):
                return False
        return True


# ---------------------------------------------------------------------------
# A12. FederatedRAG — across registered sources
# ---------------------------------------------------------------------------


class FederatedRAG(RagxArchitecture):
    """§4 FederatedRAG: retrieval merged across registered federation sources.

    Remote sources are an **External gate**: this architecture only talks to
    ``eoip.federation.planner.DataSourceAdapter`` implementations. The local
    graph participates via ``LocalGraphStoreAdapter``; remote adapters must be
    registered by the wiring layer with real connectivity.
    """

    name = "federated"
    description = "FederatedRAG: merged retrieval across registered federation sources"

    def __init__(self, store: GraphStore, planner: Any | None = None, *args: Any, **kwargs: Any) -> None:
        super().__init__(store, *args, **kwargs)
        if planner is None:
            from eoip.federation.planner import FederatedQueryPlanner, LocalGraphStoreAdapter, SourceCapability

            planner = FederatedQueryPlanner()
            planner.register(LocalGraphStoreAdapter(
                SourceCapability(source_id="local", entity_types=[], locality=1.0), store))
        self._planner = planner

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        entity_types = list(context.get("entity_types", []))
        filters = dict(context.get("filters", {}))
        result = self._planner.execute(entity_types, filters or None)
        rows = result.get("rows", result) if isinstance(result, dict) else result
        out = []
        for row in rows[: int(context.get("top_k", 10))]:
            cid = str(row.get("canonical_id") or row.get("id") or f"urn:eoip:ragx:fed:{len(out)}")
            text = " ".join(str(v) for v in row.values() if isinstance(v, (str, int, float)))
            prov = row.get("_provenance", {})
            out.append(Candidate(
                source_id=cid,
                text=text,
                score=1.0,
                label=str(row.get("entity_type", "record")),
                properties=dict(row),
                citations=list(prov.get("source_urns", [])) if isinstance(prov, dict) else [],
            ))
        return out


# ---------------------------------------------------------------------------
# A13. StreamingRAG — append-only delta incorporation
# ---------------------------------------------------------------------------


class StreamingRAG(RagxArchitecture):
    """§4 StreamingRAG: append-only deltas incorporated between queries."""

    name = "streaming"
    description = "StreamingRAG: append-only evidence deltas, always queryable"

    def __init__(self, store: GraphStore, *args: Any, **kwargs: Any) -> None:
        super().__init__(store, *args, **kwargs)
        self.deltas: list[dict[str, Any]] = []

    def append_delta(self, delta: dict[str, Any]) -> None:
        """Ingest an append-only delta: {canonical_id, text, op: ADD|UPDATE}."""
        cid = str(delta.get("canonical_id", ""))
        if not cid:
            raise ValueError("delta requires canonical_id")
        self.deltas.append(dict(delta))
        self.index.add(cid, str(delta.get("text", cid)))

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        out = self.search(query, top_k=int(context.get("top_k", 10)))
        # Newest deltas get a freshness boost (append-only: never removed).
        recent = {str(d.get("canonical_id")) for d in self.deltas[-5:]}
        for c in out:
            if c.source_id in recent:
                c.score *= 1.25
        out.sort(key=lambda c: (-c.score, c.source_id))
        return out


# ---------------------------------------------------------------------------
# A14. IncrementalRAG — index updates on CDC events
# ---------------------------------------------------------------------------


class IncrementalRAG(RagxArchitecture):
    """§4 IncrementalRAG: maintain the index from change-data-capture events."""

    name = "incremental"
    description = "IncrementalRAG: CDC-driven index maintenance (upsert/delete)"

    def on_cdc(self, event: dict[str, Any]) -> None:
        """Apply a CDC event: {operation: UPSERT|DELETE, canonical_id, text?}."""
        op = str(event.get("operation", "UPSERT")).upper()
        cid = str(event.get("canonical_id", ""))
        if not cid:
            raise ValueError("cdc event requires canonical_id")
        if op == "DELETE":
            self.index.remove(cid)
        else:
            self.index.add(cid, str(event.get("text", cid)))

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        return self.search(query, top_k=int(context.get("top_k", 10)))


# ---------------------------------------------------------------------------
# A15. StructuredDataRAG — tables/records as evidence
# ---------------------------------------------------------------------------


class StructuredDataRAG(RagxArchitecture):
    """§4 StructuredDataRAG: structured records rendered as evidence rows."""

    name = "structured"
    description = "StructuredDataRAG: table/record evidence with row rendering"

    RECORD_LABELS = frozenset({"Record", "Table", "Document", "WorkItem", "Metric"})

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        labels = set(context.get("record_labels", [])) or self.RECORD_LABELS
        base = [c for c in self.search(query, top_k=50) if c.label in labels]
        if not base:
            base = self.search(query, top_k=int(context.get("top_k", 10)))
        return base[: int(context.get("top_k", 10))]

    def generate(self, query: str, candidates: list[Candidate], context: dict[str, Any]) -> Any:
        from eoip.graph.rag_router import RAGResult

        if not candidates:
            return super().generate(query, candidates, context)
        header_keys: list[str] = []
        for c in candidates:
            for k in c.properties:
                if k not in header_keys and not k.startswith("_"):
                    header_keys.append(k)
            if len(header_keys) >= 6:
                break
        header_keys = header_keys[:6]
        lines = [" | ".join(header_keys)]
        for c in candidates[:10]:
            lines.append(" | ".join(str(c.properties.get(k, ""))[:30] for k in header_keys))
        return RAGResult(
            answer=f"Records for '{query}':\n" + "\n".join(lines),
            pattern=self.name,
            confidence=min(0.9, 0.4 + 0.05 * len(candidates)),
            sources=[c.source_id for c in candidates],
            highlight_ids=[c.source_id for c in candidates[:10]],
            metadata={"generation": "deterministic", "columns": header_keys},
        )


# ---------------------------------------------------------------------------
# A16. CodeRAG — symbol-level retrieval
# ---------------------------------------------------------------------------


class CodeRAG(RagxArchitecture):
    """§4 CodeRAG: symbol-level retrieval over codegraph-labeled vertices."""

    name = "coderag"
    description = "CodeRAG: symbol-level retrieval (CodeSymbol/File/Repository)"

    CODE_LABELS = frozenset({"CodeSymbol", "File", "Repository", "Commit", "Dependency", "MergeRequest", "PipelineRun"})

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        pool = self.search(query, top_k=50)
        code = [c for c in pool if c.label in self.CODE_LABELS]
        if not code:  # fall back so the architecture still answers non-code graphs
            return pool[: int(context.get("top_k", 10))]
        code.sort(key=lambda c: (-c.score, c.source_id))
        return code[: int(context.get("top_k", 10))]

    def generate(self, query: str, candidates: list[Candidate], context: dict[str, Any]) -> Any:
        from eoip.graph.rag_router import RAGResult

        symbols = [
            f"  - [{c.label}] {c.properties.get('qualified_name') or c.properties.get('path') or c.source_id}"
            for c in candidates
        ]
        return RAGResult(
            answer=f"Code symbols for '{query}':\n" + "\n".join(symbols),
            pattern=self.name,
            confidence=0.6 if candidates else 0.1,
            sources=[c.source_id for c in candidates],
            highlight_ids=[c.source_id for c in candidates[:10]],
            metadata={"generation": "deterministic", "symbol_count": len(candidates)},
        )


# ---------------------------------------------------------------------------
# A17. MultilingualRAG — language-tagged retrieval
# ---------------------------------------------------------------------------

_LANG_HINTS = {
    "en": frozenset("the and of to in is are for with on as at by an be this that".split()),
    "de": frozenset("der die und das ist den dem mit für auf ein eine nicht".split()),
    "fr": frozenset("le la les des une un est dans pour avec pas plus".split()),
    "es": frozenset("el la los las una un es en por para con del".split()),
}


def detect_language(text: str) -> str:
    """Deterministic language guess by stopword overlap (§4 MultilingualRAG)."""
    tokens = set(re.findall(r"[a-zàâäéèêëîïôöùûüçñ]+", text.lower()))
    best, best_score = "en", -1.0
    for lang, hints in _LANG_HINTS.items():
        score = len(tokens & hints)
        if score > best_score:
            best, best_score = lang, score
    return best


class MultilingualRAG(RagxArchitecture):
    """§4 MultilingualRAG: language-tagged retrieval with cross-language fallback."""

    name = "multilingual"
    description = "MultilingualRAG: language-tagged retrieval and fallback"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        q_lang = str(context.get("language") or detect_language(query))
        pool = self.search(query, top_k=int(context.get("pool_size", 20)))
        tagged = []
        for c in pool:
            lang = str(c.properties.get("language") or detect_language(c.text))
            c.properties["detected_language"] = lang
            if lang == q_lang:
                c.score *= 1.5
            tagged.append(c)
        tagged.sort(key=lambda c: (-c.score, c.source_id))
        same_lang = [c for c in tagged if c.properties.get("detected_language") == q_lang]
        if same_lang or not context.get("strict_language"):
            return tagged[: int(context.get("top_k", 10))]
        return same_lang[: int(context.get("top_k", 10))]


# ---------------------------------------------------------------------------
# A18. MultiAgentRAG — retriever / critic / synthesizer
# ---------------------------------------------------------------------------


class MultiAgentRAG(RagxArchitecture):
    """§4 MultiAgentRAG: retriever, critic and synthesizer agents (deterministic)."""

    name = "multiagent"
    description = "MultiAgentRAG: retriever -> critic -> synthesizer agent loop"

    def execute(self, query: str, context: dict[str, Any] | None = None) -> Any:
        from eoip.graph.rag_router import RAGResult

        ctx = context or {}
        # Agent 1: retriever
        candidates = self.retrieve(query, ctx)
        # Agent 2: critic — scores evidence coverage, may trigger one re-retrieval
        coverage = len({c.source_id for c in candidates if c.source_id})
        critique = {"coverage": coverage, "verdict": "sufficient" if coverage >= 2 else "expand"}
        if critique["verdict"] == "expand":
            expanded = f"{query} " + " ".join(sorted({t for c in candidates[:3] for t in list(_keywords(c.text))[:3]}))
            more = self.retrieve(expanded, {**ctx, "top_k": int(ctx.get("top_k", 10)) * 2})
            seen = {c.source_id for c in candidates}
            candidates.extend([c for c in more if c.source_id not in seen])
        # Agent 3: synthesizer
        if not candidates:
            result = RAGResult(answer="No relevant evidence found.", pattern=self.name, confidence=0.1)
        else:
            summary = "; ".join(c.source_id for c in candidates[:5])
            result = RAGResult(
                answer=f"Synthesized from {len(candidates)} evidence item(s): {summary}",
                pattern=self.name,
                confidence=min(0.9, 0.3 + 0.1 * len(candidates)),
                sources=[c.source_id for c in candidates if c.source_id],
                highlight_ids=[c.source_id for c in candidates[:10]],
                metadata={"generation": "deterministic", "critique": critique, "agents": ["retriever", "critic", "synthesizer"]},
            )
        result.metadata["evidence_count"] = len(candidates)
        return self._apply_policy(result)


# ---------------------------------------------------------------------------
# A19. PrivacyAwareRAG — authz filtering before ranking
# ---------------------------------------------------------------------------


class PrivacyAwareRAG(RagxArchitecture):
    """§4 PrivacyAwareRAG: enforce eoip.authz policies before ranking."""

    name = "privacy_aware"
    description = "PrivacyAwareRAG: authorization-filtered retrieval (pre-ranking)"

    def __init__(self, store: GraphStore, enforcer: Any | None, *args: Any, **kwargs: Any) -> None:
        super().__init__(store, *args, **kwargs)
        self._enforcer = enforcer

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        user = context.get("user")
        action = str(context.get("action", "rag:read"))
        pool = self.search(query, top_k=int(context.get("pool_size", 30)))
        if user is None or self._enforcer is None:
            return pool[: int(context.get("top_k", 10))]
        allowed = []
        for c in pool:
            decision = self._enforcer.enforce(user, action, dict(c.properties))
            if decision.allow:
                allowed.append(c)
            else:
                self._denied = getattr(self, "_denied", 0) + 1
        return allowed[: int(context.get("top_k", 10))]

    @property
    def denied_count(self) -> int:
        return getattr(self, "_denied", 0)


# ---------------------------------------------------------------------------
# A20. ProvenanceAwareRAG — evidence-locked citations
# ---------------------------------------------------------------------------


class ProvenanceAwareRAG(RagxArchitecture):
    """§4 ProvenanceAwareRAG: every claim locked to a provenance citation."""

    name = "provenance_aware"
    description = "ProvenanceAwareRAG: evidence-locked citations (source_ref required)"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        pool = self.search(query, top_k=int(context.get("pool_size", 30)))
        locked = []
        for c in pool:
            if not c.citations:
                vertex = self._store.get_vertex_by_canonical_id(c.source_id)
                props = dict((vertex or {}).get("properties") or {})
                c.citations = [r for r in (props.get("source_ref"), props.get("evidence_key")) if r]
            if c.citations:
                locked.append(c)
        if not locked and not context.get("strict", True):
            return pool[: int(context.get("top_k", 10))]
        return locked[: int(context.get("top_k", 10))]

    def generate(self, query: str, candidates: list[Candidate], context: dict[str, Any]) -> Any:
        from eoip.graph.rag_router import RAGResult

        if not candidates:
            return RAGResult(answer="Abstained: no provenance-locked evidence.", pattern=self.name,
                             confidence=0.0, abstained=True, abstention_reasons=["NO_PROVENANCE_LOCKED_EVIDENCE"])
        lines = [f"  - {c.text[:80]} [{', '.join(c.citations)}]" for c in candidates[:10]]
        return RAGResult(
            answer=f"Provenance-locked evidence for '{query}':\n" + "\n".join(lines),
            pattern=self.name,
            confidence=min(0.95, 0.5 + 0.05 * len(candidates)),
            sources=[c.source_id for c in candidates],
            highlight_ids=[c.source_id for c in candidates[:10]],
            metadata={"generation": "deterministic", "citations_locked": True},
        )


# ---------------------------------------------------------------------------
# A21. VersionAwareRAG — document-version pinning
# ---------------------------------------------------------------------------


class VersionAwareRAG(RagxArchitecture):
    """§4 VersionAwareRAG: pin retrieval to a specific document version."""

    name = "version_aware"
    description = "VersionAwareRAG: document-version pinned retrieval"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        pool = self.search(query, top_k=int(context.get("pool_size", 30)))
        pinned = context.get("version") or context.get("doc_version")
        if pinned is None:
            return pool[: int(context.get("top_k", 10))]
        out = [
            c for c in pool
            if str(c.properties.get("doc_version") or c.properties.get("version")) == str(pinned)
        ]
        return out[: int(context.get("top_k", 10))]


# ---------------------------------------------------------------------------
# A22. EventAwareRAG — event-centric retrieval
# ---------------------------------------------------------------------------


class EventAwareRAG(RagxArchitecture):
    """§4 EventAwareRAG: retrieve entities participating in a given event."""

    name = "event_aware"
    description = "EventAwareRAG: event-centric participant/evidence retrieval"

    def retrieve(self, query: str, context: dict[str, Any]) -> list[Candidate]:
        event_id = context.get("event_id")
        event_types = list(context.get("event_types", ["CAUSES", "TRIGGERS", "PARTICIPATES_IN", "RELATES_TO"]))
        base = self.search(query, top_k=int(context.get("top_k", 10)))
        if not event_id:
            return base
        seed = self._store.get_vertex_by_canonical_id(str(event_id))
        if seed is None:
            return base
        out: list[Candidate] = []
        for edge in self._store.edges_from(seed["vid"], limit=200) + self._store.edges_to(seed["vid"], limit=200):
            if event_types and edge["label"] not in event_types:
                continue
            other_cid = edge["in_cid"] if edge["out_v"] == seed["vid"] else edge["out_cid"]
            vertex = self._store.get_vertex_by_canonical_id(other_cid)
            if vertex:
                text = vertex_text(vertex["label"], vertex["properties"])
                props = edge.get("properties") or {}
                out.append(Candidate(
                    source_id=other_cid,
                    text=text,
                    score=1.0 + overlap_score(query, text),
                    label=vertex["label"],
                    properties=dict(vertex["properties"]),
                    citations=[r for r in (props.get("source_ref"), props.get("evidence_key")) if r],
                ))
        out.sort(key=lambda c: (-c.score, c.source_id))
        return out[: int(context.get("top_k", 10))] or base


ARCHITECTURES: dict[str, type[RagxArchitecture]] = {
    cls.name: cls
    for cls in (
        HierarchicalRAG, RaptorRAG, LightRAG, HippoRAG, PathRAG, KGRAG,
        LazyGraphRAG, DRIFTRAG, GlobalSearch, LocalSearch, TemporalRAG,
        FederatedRAG, StreamingRAG, IncrementalRAG, StructuredDataRAG,
        CodeRAG, MultilingualRAG, MultiAgentRAG, PrivacyAwareRAG,
        ProvenanceAwareRAG, VersionAwareRAG, EventAwareRAG,
    )
}


def build_architecture(name: str, store: GraphStore, **kwargs: Any) -> RagxArchitecture:
    cls = ARCHITECTURES[name]
    if cls is PrivacyAwareRAG:
        return cls(store, kwargs.pop("enforcer", None), **kwargs)
    if cls is FederatedRAG:
        return cls(store, kwargs.pop("planner", None), **kwargs)
    return cls(store, **kwargs)
