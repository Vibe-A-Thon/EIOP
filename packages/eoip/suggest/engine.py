"""Suggestion engine: ranked candidate interpretations for NL questions.

Deterministic core (SR-NLQ-001/002): parse -> resolve entities against the
graph store (name / canonical_id / alias crosswalk, SR-NLQ-003) -> emit one
candidate per plausible intent-entity combination, ranked by a deterministic
confidence score. An optional LLM-assist hook (External gate) may append
candidates for open-ended phrasing; results sourced from it are labeled
``llm_assist``. No model is required or invoked by default.
"""

from __future__ import annotations

import itertools
from typing import Any, Callable, Protocol

from eoip.contracts.query_plan import QueryPlan
from eoip.suggest import parser
from eoip.suggest.models import (
    COST_TIERS,
    INTENT_PLAN_PERMISSIONS,
    CandidateInterpretation,
    EntityAlternative,
    EntityBinding,
    PermissionNote,
    SuggestionRequest,
    SuggestionResponse,
    choose_answer_mode,
)

_ID_COUNTER = itertools.count(1)

# Entity properties consulted, in order, for mention resolution.
_NAME_KEYS = ("name", "display_name", "canonical_id", "source_aliases", "id", "key")


class LLMAssistHook(Protocol):
    """External gate: optional LLM assist for open-ended phrasing (SR-NLQ-001).

    Implementations call an external model; the engine treats them as an
    untrusted suggestion source and labels their output accordingly.
    """

    def __call__(self, question: str, *, limit: int = 3) -> list[CandidateInterpretation]: ...


class SuggestionEngine:
    """Deterministic suggestion engine over a GraphStore (SR-NLQ-002)."""

    def __init__(
        self,
        store: Any = None,
        *,
        enforcer: Any = None,
        llm_hook: LLMAssistHook | None = None,
        domains: list[str] | None = None,
    ) -> None:
        self._store = store
        self._enforcer = enforcer
        self._llm_hook = llm_hook
        self._domains = list(domains or [])

    # -- entity resolution (SR-NLQ-003) ------------------------------------

    def resolve_mention(self, mention: str, *, role: str = "subject") -> EntityBinding:
        alternatives: list[EntityAlternative] = []
        if self._store is not None:
            for key in _NAME_KEYS:
                hits = self._lookup(key, mention)
                if not hits:
                    hits = self._lookup(key, mention.casefold())
                for vertex in hits:
                    alternatives.append(self._to_alternative(vertex, mention, key))
                if alternatives:
                    break
            if not alternatives:
                alternatives = self._fuzzy_scan(mention)
        alternatives = _dedupe_alternatives(alternatives)[:5]
        resolved = alternatives[0] if alternatives else None
        return EntityBinding(
            mention=mention,
            role=role,
            resolved=resolved,
            alternatives=alternatives,
            ambiguous=len(alternatives) > 1,
        )

    def _lookup(self, key: str, value: str) -> list:
        """find_vertex_by_property across all vertex labels (stores require an
        exact label match; try the known ontology labels plus a wildcard)."""
        labels: list[str | None] = [None]
        try:
            from eoip.ontology.manifest import VERTEX_LABELS

            labels = list(VERTEX_LABELS)
        except Exception:
            pass
        for label in labels:
            try:
                hits = self._store.find_vertex_by_property(label or "", key, value, limit=10)
            except Exception:
                hits = []
            if hits:
                return list(hits)
        return []

    @staticmethod
    def _props(vertex: Any) -> dict:
        if isinstance(vertex, dict):
            return dict(vertex.get("properties") or {})
        return dict(getattr(vertex, "properties", None) or {})

    @staticmethod
    def _vid(vertex: Any, props: dict) -> str:
        if isinstance(vertex, dict):
            return str(vertex.get("vid") or vertex.get("canonical_id") or props.get("canonical_id") or "")
        return str(getattr(vertex, "id", "") or props.get("canonical_id") or "")

    def _to_alternative(self, vertex: Any, mention: str, key: str) -> EntityAlternative:
        props = self._props(vertex)
        name = str(props.get("name") or props.get("display_name") or props.get("canonical_id") or "")
        score = 1.0 if key in ("name", "display_name") else 0.9
        if mention.casefold() == name.casefold():
            score = 1.0
        basis = "alias" if key == "source_aliases" else ("canonical_id" if key == "canonical_id" else "name")
        return EntityAlternative(
            entity_id=self._vid(vertex, props),
            display_name=name,
            entity_type=props.get("entity_type") or props.get("type"),
            source_system=props.get("source_system"),
            environment=props.get("environment"),
            match_basis=basis,
            match_score=round(score, 3),
        )

    def _fuzzy_scan(self, mention: str) -> list[EntityAlternative]:
        needle = mention.casefold()
        out: list[EntityAlternative] = []
        try:
            vertices = self._store.find_vertices(limit=500)
        except Exception:
            return out
        for vertex in vertices:
            props = self._props(vertex)
            haystacks = [props.get(k) for k in ("name", "display_name", "source_aliases")]
            if any(needle and needle in str(h).casefold() for h in haystacks if h):
                name = str(props.get("name") or props.get("display_name") or "")
                out.append(EntityAlternative(
                    entity_id=self._vid(vertex, props),
                    display_name=name,
                    entity_type=props.get("entity_type") or props.get("type"),
                    source_system=props.get("source_system"),
                    environment=props.get("environment"),
                    match_basis="fuzzy",
                    match_score=0.6,
                ))
        return out

    # -- permission pre-check (SR-NLQ-002) ----------------------------------

    def _permission_note(self, intent: str, request: SuggestionRequest) -> PermissionNote:
        permissions = list(INTENT_PLAN_PERMISSIONS.get(intent, ["graph:read"]))
        if self._enforcer is None or not request.user_id:
            return PermissionNote(
                permissions=permissions,
                evaluated=False,
                note="Not evaluated: no PolicyEnforcer or user supplied; plan requires "
                + ", ".join(permissions),
            )
        from eoip.authz.core import User

        user = User(user_id=request.user_id, roles=list(request.roles))
        allowed = True
        for permission in permissions:
            decision = self._enforcer.enforce(user, permission, {})
            if not decision.allow:
                allowed = False
        note = (
            f"User '{request.user_id}' is pre-authorized for: {', '.join(permissions)}"
            if allowed
            else f"User '{request.user_id}' lacks one or more required permissions: {', '.join(permissions)}"
        )
        return PermissionNote(permissions=permissions, evaluated=True, allowed=allowed, note=note)

    # -- candidate generation & ranking --------------------------------------

    def suggest(self, request: SuggestionRequest) -> SuggestionResponse:
        parsed = parser.parse_question(request.question)
        bindings = [self.resolve_mention(m) for m in parsed.mentions]

        candidates: list[CandidateInterpretation] = []
        intents = sorted(parsed.intent_scores, key=parsed.intent_scores.get, reverse=True) or [None]
        for intent in intents[:3]:
            if intent is None:
                continue
            candidates.append(self._candidate(intent, parsed, bindings, request))

        llm_used = False
        if self._llm_hook is not None and (parsed.intent is None or len(candidates) < 2):
            try:
                assisted = self._llm_hook(request.question, limit=3)
            except Exception:
                assisted = []
            for cand in assisted:
                cand.source = "llm_assist"
            candidates.extend(assisted)
            llm_used = bool(assisted)

        candidates.sort(key=lambda c: c.confidence, reverse=True)
        candidates = candidates[: request.limit]
        return SuggestionResponse(
            question=request.question,
            candidates=candidates,
            llm_assist_used=llm_used,
            parse={
                "intent": parsed.intent,
                "intent_scores": parsed.intent_scores,
                "mentions": list(parsed.mentions),
            },
        )

    def _candidate(
        self,
        intent: str,
        parsed: parser.ParsedQuestion,
        bindings: list[EntityBinding],
        request: SuggestionRequest,
    ) -> CandidateInterpretation:
        anchors = [b.resolved.entity_id for b in bindings if b.resolved]
        mention = parsed.mentions[0] if parsed.mentions else None
        plan = parser.plan_for_intent(intent, anchors)
        tier = parser.cost_tier_for_intent(intent)
        confidence = self._confidence(intent, parsed, bindings)
        return CandidateInterpretation(
            candidate_id=f"cand-{next(_ID_COUNTER)}",
            intent=intent,
            paraphrase=parser.paraphrase(intent, mention, parsed.question),
            plan_preview=plan,
            result_shape=parser.result_shape_for_intent(intent),
            entity_bindings=bindings,
            cost_tier=tier,  # type: ignore[arg-type]
            estimated_latency_ms=COST_TIERS[tier]["estimated_latency_ms"],
            confidence=confidence,
            data_coverage_note=parser.coverage_note(intent, mention, self._domains),
            permissions=self._permission_note(intent, request),
            answer_mode=choose_answer_mode(intent),
        )

    def _confidence(
        self,
        intent: str,
        parsed: parser.ParsedQuestion,
        bindings: list[EntityBinding],
    ) -> float:
        scores = parsed.intent_scores
        top = scores.get(intent, 0.0)
        total = sum(scores.values()) or 1.0
        confidence = 0.35 + 0.45 * (top / total)
        if bindings:
            best = max((b.resolved.match_score for b in bindings if b.resolved), default=0.0)
            confidence += 0.15 * best
            if any(b.ambiguous for b in bindings):
                confidence -= 0.15  # ambiguity penalty, spread across candidates
        else:
            confidence -= 0.1  # no entity anchors resolved
        return round(max(0.05, min(0.99, confidence)), 3)


def _dedupe_alternatives(items: list[EntityAlternative]) -> list[EntityAlternative]:
    seen: dict[str, EntityAlternative] = {}
    for item in items:
        current = seen.get(item.entity_id)
        if current is None or item.match_score > current.match_score:
            seen[item.entity_id] = item
    return sorted(seen.values(), key=lambda a: a.match_score, reverse=True)
