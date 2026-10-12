"""GAP-NLP: Local NLP pipeline (entity extraction, tagging, classification,
concept recommendation).  Pure Python, deterministic, no cloud or model
downloads; every component can be trained/seeded from the local graph.
"""

from __future__ import annotations

import math
import re
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from typing import Any, Iterable

from eoip.graph.store import GraphStore

_TOKEN = re.compile(r"[A-Za-z][A-Za-z0-9_\-]*|\d+(?:\.\d+)*")
_CAMEL = re.compile(r"[a-z0-9]+|[A-Z][a-z0-9]*|[A-Z]+(?![a-z])")

STOPWORDS = frozenset(
    "a an and are as at be but by for from has have he her his i if in into is it its "
    "of on or our she that the their them then there these they this to was we were "
    "will with you your not no can could should would do does did been being than so "
    "also via per about after before over under".split()
)


def tokenize(text: str, *, keep_stopwords: bool = False) -> list[str]:
    toks = [t.lower() for t in _TOKEN.findall(text or "")]
    return toks if keep_stopwords else [t for t in toks if t not in STOPWORDS and len(t) > 1]


def split_identifier(name: str) -> list[str]:
    """`PaymentGateway_v2` -> ['payment', 'gateway', 'v2']."""
    parts: list[str] = []
    for chunk in re.split(r"[_\-\s:./]+", name):
        parts.extend(m.lower() for m in _CAMEL.findall(chunk))
    return [p for p in parts if p]


# ---------------------------------------------------------------- entities
@dataclass(frozen=True)
class Entity:
    text: str
    kind: str
    start: int
    end: int
    canonical_id: str | None = None
    confidence: float = 1.0


_PATTERNS: list[tuple[str, re.Pattern[str], float]] = [
    ("ISSUE_KEY", re.compile(r"\b[A-Z][A-Z0-9]{1,9}-\d+\b"), 0.95),
    ("EMAIL", re.compile(r"\b[\w.+-]+@[\w-]+(?:\.[\w-]+)+\b"), 0.99),
    ("URL", re.compile(r"https?://[^\s)>\]\"']+"), 0.99),
    ("COMMIT_SHA", re.compile(r"\b[0-9a-f]{7,40}\b"), 0.6),
    ("VERSION", re.compile(r"\bv?\d+\.\d+(?:\.\d+)?(?:-[A-Za-z0-9.]+)?\b"), 0.7),
    ("FILE_PATH", re.compile(r"(?<![\w/])(?:[\w.-]+/)+[\w.-]+\.\w{1,6}\b"), 0.8),
    ("CODE_IDENTIFIER", re.compile(r"\b[a-z]+(?:[A-Z][a-z0-9]+)+\b|\b[A-Z][a-z0-9]+(?:[A-Z][a-z0-9]+)+\b"), 0.65),
]


class Gazetteer:
    """Longest-match phrase dictionary built from graph vertices / ontology labels."""

    def __init__(self) -> None:
        self._phrases: dict[tuple[str, ...], tuple[str, str]] = {}
        self._max_len = 1

    def add(self, surface: str, *, kind: str, canonical_id: str) -> None:
        toks = tuple(tokenize(surface, keep_stopwords=True))
        if not toks:
            return
        self._phrases[toks] = (kind, canonical_id)
        self._max_len = max(self._max_len, len(toks))

    def __len__(self) -> int:
        return len(self._phrases)

    @classmethod
    def from_store(cls, store: GraphStore, *, limit: int = 50_000) -> "Gazetteer":
        gz = cls()
        for v in store.find_vertices(limit=limit):
            props = v.get("properties", {})
            cid = props.get("canonical_id") or v.get("canonical_id")
            for key in ("name", "display_name", "summary", "api_name", "issue_key"):
                val = props.get(key)
                if isinstance(val, str) and 2 < len(val) <= 80:
                    gz.add(val, kind=v["label"], canonical_id=str(cid))
        return gz

    def find(self, text: str) -> list[Entity]:
        spans = [(m.group(), m.start(), m.end()) for m in _TOKEN.finditer(text)]
        low = [s[0].lower() for s in spans]
        out: list[Entity] = []
        i = 0
        while i < len(low):
            for n in range(min(self._max_len, len(low) - i), 0, -1):
                hit = self._phrases.get(tuple(low[i:i + n]))
                if hit:
                    start, end = spans[i][1], spans[i + n - 1][2]
                    out.append(Entity(text[start:end], hit[0], start, end, hit[1], 0.9))
                    i += n
                    break
            else:
                i += 1
        return out


class EntityExtractor:
    def __init__(self, gazetteer: Gazetteer | None = None) -> None:
        self.gazetteer = gazetteer or Gazetteer()

    def extract(self, text: str) -> list[Entity]:
        found = list(self.gazetteer.find(text))
        taken = [(e.start, e.end) for e in found]
        for kind, pattern, conf in _PATTERNS:
            for m in pattern.finditer(text):
                if kind == "COMMIT_SHA" and not any(c.isdigit() for c in m.group()):
                    continue
                if any(m.start() < b and m.end() > a for a, b in taken):
                    continue
                taken.append((m.start(), m.end()))
                found.append(Entity(m.group(), kind, m.start(), m.end(), None, conf))
        return sorted(found, key=lambda e: (e.start, -(e.end - e.start)))


# ------------------------------------------------------- tagging (TF-IDF)
class TfidfModel:
    def __init__(self) -> None:
        self.df: Counter[str] = Counter()
        self.n_docs = 0

    def fit(self, docs: Iterable[str]) -> "TfidfModel":
        for d in docs:
            self.n_docs += 1
            self.df.update(set(tokenize(d)))
        return self

    def idf(self, term: str) -> float:
        return math.log((1 + self.n_docs) / (1 + self.df.get(term, 0))) + 1.0

    def vector(self, text: str) -> dict[str, float]:
        tf = Counter(tokenize(text))
        vec = {t: (1 + math.log(c)) * self.idf(t) for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in vec.values())) or 1.0
        return {t: x / norm for t, x in vec.items()}


def cosine(a: dict[str, float], b: dict[str, float]) -> float:
    if len(a) > len(b):
        a, b = b, a
    return sum(x * b.get(t, 0.0) for t, x in a.items())


class KeyphraseTagger:
    """Ranks unigrams + bigrams by TF-IDF to produce tags."""

    def __init__(self, model: TfidfModel | None = None) -> None:
        self.model = model or TfidfModel()

    def tag(self, text: str, *, top_k: int = 8) -> list[tuple[str, float]]:
        toks = tokenize(text)
        grams = Counter(toks)
        grams.update(f"{a} {b}" for a, b in zip(toks, toks[1:]))
        scores = {}
        for g, c in grams.items():
            parts = g.split()
            idf = sum(self.model.idf(p) for p in parts) / len(parts)
            scores[g] = (1 + math.log(c)) * idf * (1.15 if len(parts) == 2 and c > 1 else 1.0)
        ranked = sorted(scores.items(), key=lambda kv: (-kv[1], kv[0]))
        # drop unigrams subsumed by a selected bigram
        chosen: list[tuple[str, float]] = []
        for g, s in ranked:
            if any(" " in c and g in c.split() for c, _ in chosen):
                continue
            chosen.append((g, round(s, 6)))
            if len(chosen) >= top_k:
                break
        return chosen


# ---------------------------------------------------------- classification
class NaiveBayesClassifier:
    """Multinomial Naive Bayes with Laplace smoothing, trained locally."""

    def __init__(self, alpha: float = 1.0) -> None:
        self.alpha = alpha
        self.class_docs: Counter[str] = Counter()
        self.term_counts: dict[str, Counter[str]] = defaultdict(Counter)
        self.vocab: set[str] = set()

    @property
    def labels(self) -> list[str]:
        return sorted(self.class_docs)

    def fit(self, samples: Iterable[tuple[str, str]]) -> "NaiveBayesClassifier":
        for text, label in samples:
            self.class_docs[label] += 1
            toks = tokenize(text)
            self.term_counts[label].update(toks)
            self.vocab.update(toks)
        return self

    def predict_proba(self, text: str) -> dict[str, float]:
        if not self.class_docs:
            raise ValueError("classifier has not been trained")
        total = sum(self.class_docs.values())
        v = len(self.vocab)
        toks = [t for t in tokenize(text) if t in self.vocab]
        logp = {}
        for label, nd in self.class_docs.items():
            denom = sum(self.term_counts[label].values()) + self.alpha * v
            lp = math.log(nd / total)
            for t in toks:
                lp += math.log((self.term_counts[label][t] + self.alpha) / denom)
            logp[label] = lp
        m = max(logp.values())
        exp = {k: math.exp(x - m) for k, x in logp.items()}
        z = sum(exp.values())
        return {k: x / z for k, x in exp.items()}

    def predict(self, text: str, *, min_confidence: float = 0.0) -> tuple[str | None, float]:
        probs = self.predict_proba(text)
        label, p = max(probs.items(), key=lambda kv: (kv[1], kv[0]))
        return (label, p) if p >= min_confidence else (None, p)


# ------------------------------------------------- concept recommendation
@dataclass
class ConceptRecommendation:
    concept_id: str
    label: str
    score: float
    matched_terms: list[str] = field(default_factory=list)


class ConceptRecommender:
    """Recommends known concepts (ontology/graph labels) for free text."""

    def __init__(self) -> None:
        self._concepts: dict[str, tuple[str, str]] = {}
        self.model = TfidfModel()
        self._vecs: dict[str, dict[str, float]] = {}

    def fit(self, concepts: Iterable[dict[str, Any]]) -> "ConceptRecommender":
        """concepts: {id, label, alt_labels?: [..], definition?: str}"""
        docs = {}
        for c in concepts:
            parts = [c["label"], *c.get("alt_labels", []), c.get("definition", "")]
            text = " ".join(parts) + " " + " ".join(split_identifier(c["label"]))
            docs[c["id"]] = text
            self._concepts[c["id"]] = (c["label"], text)
        self.model = TfidfModel().fit(docs.values())
        self._vecs = {cid: self.model.vector(t) for cid, t in docs.items()}
        return self

    @classmethod
    def from_store(cls, store: GraphStore, *, limit: int = 50_000) -> "ConceptRecommender":
        seen: dict[str, dict[str, Any]] = {}
        for v in store.find_vertices(limit=limit):
            p = v.get("properties", {})
            name = p.get("name") or p.get("display_name") or p.get("summary")
            cid = p.get("canonical_id")
            if cid and isinstance(name, str):
                seen[cid] = {"id": cid, "label": name, "definition": str(p.get("description", ""))}
        return cls().fit(seen.values())

    def recommend(self, text: str, *, top_k: int = 5, min_score: float = 0.05) -> list[ConceptRecommendation]:
        q = self.model.vector(text + " " + " ".join(split_identifier(text)))
        out = []
        for cid, vec in self._vecs.items():
            s = cosine(q, vec)
            if s >= min_score:
                matched = sorted(set(q) & set(vec))
                out.append(ConceptRecommendation(cid, self._concepts[cid][0], round(s, 6), matched))
        out.sort(key=lambda r: (-r.score, r.concept_id))
        return out[:top_k]


# ------------------------------------------------------------- pipeline
@dataclass
class NLPAnalysis:
    text: str
    tokens: list[str]
    entities: list[Entity]
    tags: list[tuple[str, float]]
    classification: tuple[str | None, float] | None
    concepts: list[ConceptRecommendation]

    def to_dict(self) -> dict[str, Any]:
        return {
            "tokens": self.tokens,
            "entities": [e.__dict__ for e in self.entities],
            "tags": [{"tag": t, "score": s} for t, s in self.tags],
            "classification": (
                {"label": self.classification[0], "confidence": round(self.classification[1], 6)}
                if self.classification else None
            ),
            "concepts": [r.__dict__ for r in self.concepts],
        }


class LocalNLPPipeline:
    def __init__(
        self,
        *,
        extractor: EntityExtractor | None = None,
        tagger: KeyphraseTagger | None = None,
        classifier: NaiveBayesClassifier | None = None,
        recommender: ConceptRecommender | None = None,
    ) -> None:
        self.extractor = extractor or EntityExtractor()
        self.tagger = tagger or KeyphraseTagger()
        self.classifier = classifier
        self.recommender = recommender

    @classmethod
    def from_store(cls, store: GraphStore, **kwargs: Any) -> "LocalNLPPipeline":
        docs = []
        for v in store.find_vertices(limit=50_000):
            p = v.get("properties", {})
            docs.append(" ".join(str(p.get(k, "")) for k in ("name", "summary", "description")))
        return cls(
            extractor=EntityExtractor(Gazetteer.from_store(store)),
            tagger=KeyphraseTagger(TfidfModel().fit(docs)),
            recommender=ConceptRecommender.from_store(store),
            **kwargs,
        )

    def analyze(self, text: str, *, top_tags: int = 8, top_concepts: int = 5) -> NLPAnalysis:
        cls = None
        if self.classifier is not None and self.classifier.class_docs:
            cls = self.classifier.predict(text)
        return NLPAnalysis(
            text=text,
            tokens=tokenize(text),
            entities=self.extractor.extract(text),
            tags=self.tagger.tag(text, top_k=top_tags),
            classification=cls,
            concepts=self.recommender.recommend(text, top_k=top_concepts) if self.recommender else [],
        )
