"""Natural-language query processor for graph, EQL, and query operators.

The processor is the public NLQ layer. It routes plain-language questions to
the safest existing engine that can answer them:

1. deterministic graph-fact/operator routes for counts, labels, domains, WHY,
   WHY NOT, WHAT CHANGED, and contextual questions;
2. NL -> QueryPlan interpretation plus policy-checked QueryExecutor execution;
3. graph-domain search fallback for unresolved but obviously graph-related
   questions.

It never accepts executable query language from natural language input.
"""

from __future__ import annotations

import re
from typing import Any, Literal

from eoip.contracts.graph_result import GraphNode, GraphResult
from eoip.contracts.query_plan import QueryPlan
from eoip.graph.store import GraphStore
from eoip.ontology.manifest import EDGE_LABELS, VERTEX_LABELS
from eoip.query.eql import parse_and_execute
from eoip.query.executor import PolicyViolation, QueryExecutor
from eoip.query.nl import CLARIFICATION_PROMPT, NLInterpretation, interpret
from pydantic import BaseModel, Field


EngineName = Literal["query_plan", "eql", "operator", "search_fallback", "clarification"]


class NLQResponse(BaseModel):
    question: str
    engine: EngineName
    interpretation: NLInterpretation
    result: Any = None
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    highlights: list[str] = Field(default_factory=list)
    followups: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)


_WHY_NOT = re.compile(r"\bwhy\s+(?:is|are|does|do)?\s*(?:not|n't)\b", re.IGNORECASE)
_WHY = re.compile(r"\bwhy\b", re.IGNORECASE)
_WHAT_CHANGED = re.compile(r"\b(what\s+changed|changes?|history|recent\s+change)\b", re.IGNORECASE)
_CONTEXT = re.compile(r"\b(who|when|where|how|context|metadata|owner|author)\b", re.IGNORECASE)
_COUNT = re.compile(r"\b(how\s+many|count|number\s+of|total)\b", re.IGNORECASE)
_LIST_SCHEMA = re.compile(r"\b(list|show|what|which)\b", re.IGNORECASE)
_WORD = re.compile(r"\b[a-z][a-z0-9_-]{2,}\b", re.IGNORECASE)
_CID = re.compile(r"\burn:eoip:[A-Za-z0-9:._/-]+", re.IGNORECASE)
_ISSUE_KEY = re.compile(r"\b([A-Z][A-Z0-9]+-\d+)\b")
_SHA = re.compile(r"\b([0-9a-f]{40})\b")
_GRAPH_HINTS = {
    "api",
    "author",
    "branch",
    "build",
    "capability",
    "change",
    "class",
    "code",
    "commit",
    "component",
    "dependency",
    "document",
    "edge",
    "entity",
    "file",
    "function",
    "graph",
    "impact",
    "incident",
    "issue",
    "jira",
    "lineage",
    "method",
    "module",
    "node",
    "owner",
    "path",
    "pipeline",
    "query",
    "relationship",
    "repo",
    "requirement",
    "requirements",
    "service",
    "services",
    "symbol",
    "symbols",
    "test",
    "tests",
    "trace",
    "work",
}
_STOPWORDS = {
    "about",
    "after",
    "all",
    "also",
    "and",
    "any",
    "are",
    "between",
    "can",
    "connected",
    "count",
    "does",
    "find",
    "for",
    "from",
    "give",
    "has",
    "have",
    "how",
    "impact",
    "into",
    "list",
    "many",
    "number",
    "of",
    "show",
    "the",
    "this",
    "to",
    "total",
    "touch",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}


_LABEL_ALIASES = {
    "apis": "API",
    "api": "API",
    "branches": "Branch",
    "branch": "Branch",
    "builds": "Build",
    "build": "Build",
    "commits": "Commit",
    "commit": "Commit",
    "dependencies": "Dependency",
    "dependency": "Dependency",
    "documents": "Document",
    "document": "Document",
    "files": "File",
    "file": "File",
    "incidents": "Incident",
    "incident": "Incident",
    "merge requests": "MergeRequest",
    "merge request": "MergeRequest",
    "mrs": "MergeRequest",
    "mr": "MergeRequest",
    "people": "Person",
    "person": "Person",
    "pipelines": "PipelineRun",
    "pipeline": "PipelineRun",
    "repositories": "Repository",
    "repository": "Repository",
    "repos": "Repository",
    "repo": "Repository",
    "requirements": "WorkItem",
    "requirement": "WorkItem",
    "services": "Service",
    "service": "Service",
    "symbols": "CodeSymbol",
    "symbol": "CodeSymbol",
    "tests": "TestCase",
    "test": "TestCase",
    "work items": "WorkItem",
    "work item": "WorkItem",
    "issues": "WorkItem",
    "issue": "WorkItem",
}


class NLQProcessor:
    def __init__(self, store: GraphStore, executor: QueryExecutor | None = None) -> None:
        self._store = store
        self._executor = executor or QueryExecutor(store)

    def process(self, question: str) -> NLQResponse:
        text = question.strip()
        if not text:
            return _clarification(text, "The question was empty")

        routed = self._route_operator_or_eql(text)
        if routed is not None:
            return routed

        interpretation = interpret(text, store=self._store)
        if interpretation.plan is not None:
            result = self._executor.execute(interpretation.plan)
            return NLQResponse(
                question=text,
                engine="query_plan",
                interpretation=interpretation,
                result=result,
                answer=_answer_graph_result(interpretation.plan, result),
                confidence=_confidence_for(interpretation),
                highlights=_node_ids(result.nodes),
                followups=_followups_for(interpretation.plan),
                warnings=list(result.warnings),
            )

        fallback_plan = _fallback_search_plan(text)
        if fallback_plan is not None:
            try:
                result = self._executor.execute(fallback_plan)
            except PolicyViolation:
                result = None
            if result is not None and result.nodes:
                fallback_interpretation = NLInterpretation(
                    plan=fallback_plan,
                    explanation=(
                        "No exact entity anchor resolved, so NLQ searched graph text "
                        "for the strongest domain phrase."
                    ),
                    interpreted_via="fallback",
                )
                return NLQResponse(
                    question=text,
                    engine="search_fallback",
                    interpretation=fallback_interpretation,
                    result=result,
                    answer=_answer_graph_result(fallback_plan, result),
                    confidence=0.55,
                    highlights=_node_ids(result.nodes),
                    followups=["Ask for impact, traceability, lineage, or a path from one result."],
                    warnings=["Search fallback was used because no canonical anchor was resolved."],
                )

        return NLQResponse(
            question=text,
            engine="clarification",
            interpretation=interpretation,
            result=None,
            answer=interpretation.clarification or CLARIFICATION_PROMPT,
            confidence=0.0,
            followups=[
                "Try an issue key, commit SHA, file path, symbol, canonical ID, or an exact entity name."
            ],
        )

    def _route_operator_or_eql(self, text: str) -> NLQResponse | None:
        lower = text.casefold()
        eql = _eql_for(text)
        if eql is not None:
            result = parse_and_execute(self._store, eql)
            return NLQResponse(
                question=text,
                engine="eql",
                interpretation=NLInterpretation(
                    plan=_search_plan(eql),
                    explanation=f"Routed schema/fact question to EQL: {eql}",
                    interpreted_via="rules",
                ),
                result=result,
                answer=_answer_eql(result),
                confidence=0.92,
                followups=["Ask for impact, path, lineage, or traceability on a specific entity."],
            )

        anchors = _ordered_anchors(text, self._store)
        if _WHY_NOT.search(text) and len(anchors) >= 2:
            from eoip.graph.query_operators import query_why_not

            result = query_why_not(self._store, anchors[0], anchors[1])
            return _operator_response(text, "WHY_NOT", result, anchors, _answer_operator("WHY_NOT", result))
        if _WHAT_CHANGED.search(text) and anchors:
            from eoip.graph.query_operators import query_what_changed

            result = query_what_changed(self._store, anchors[0])
            return _operator_response(text, "WHAT_CHANGED", result, anchors, _answer_operator("WHAT_CHANGED", result))
        if _WHY.search(text) and anchors:
            from eoip.graph.query_operators import query_why

            result = query_why(self._store, anchors[0])
            return _operator_response(text, "WHY", result, anchors, _answer_operator("WHY", result))
        if _CONTEXT.search(text) and anchors and not {"path", "impact"} & set(lower.split()):
            from eoip.graph.query_operators import query_context

            result = query_context(self._store, anchors[0])
            return _operator_response(text, "CONTEXT", result, anchors, _answer_operator("CONTEXT", result))
        return None


def process(question: str, *, store: GraphStore, executor: QueryExecutor | None = None) -> NLQResponse:
    return NLQProcessor(store, executor).process(question)


def _operator_response(
    question: str,
    operator: str,
    result: dict,
    anchors: list[str],
    answer: str,
) -> NLQResponse:
    plan = QueryPlan(
        intent="SEARCH",
        anchors=anchors,
        max_depth=1,
        result_limit=25,
        evidence_mode="NONE",
        filters={"operator": operator},
    )
    return NLQResponse(
        question=question,
        engine="operator",
        interpretation=NLInterpretation(
            plan=plan,
            explanation=f"Routed natural language to the structured {operator} query operator.",
            interpreted_via="rules",
        ),
        result=result,
        answer=answer,
        confidence=0.9,
        highlights=anchors,
        followups=["Ask for impact, path, traceability, or source context for the same entity."],
    )


def _eql_for(text: str) -> str | None:
    lower = text.casefold()
    if not (_COUNT.search(text) or _LIST_SCHEMA.search(text)):
        return None
    if "edge label" in lower or "relationship type" in lower or "edge type" in lower:
        return "EDGE LABELS"
    if "vertex label" in lower or "entity type" in lower or "node type" in lower or "labels" in lower:
        return "LABELS"
    if "domain" in lower:
        return "DOMAINS"
    if _COUNT.search(text):
        if any(word in lower for word in ("edge", "edges", "relationship", "relationships")):
            return "COUNT EDGES"
        if any(word in lower for word in ("vertex", "vertices", "node", "nodes", "entity", "entities")):
            return "COUNT VERTICES"
        label = _label_from_text(lower)
        if label:
            return f"COUNT {label}"
    return None


def _label_from_text(lower: str) -> str | None:
    for phrase, label in sorted(_LABEL_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        if phrase in lower and label in VERTEX_LABELS:
            return label
    for label in VERTEX_LABELS:
        if label.casefold() in lower:
            return label
    return None


def _ordered_anchors(text: str, store: GraphStore) -> list[str]:
    anchors: list[str] = []
    seen: set[str] = set()
    tokens = [match.group(0) for match in _CID.finditer(text)]
    tokens.extend(match.group(1) for match in _ISSUE_KEY.finditer(text))
    tokens.extend(match.group(1) for match in _SHA.finditer(text))
    tokens.extend(_quoted_phrases(text))
    for token in tokens:
        cid = _resolve_anchor(token, store)
        if cid and cid not in seen:
            seen.add(cid)
            anchors.append(cid)
    return anchors


def _resolve_anchor(token: str, store: GraphStore) -> str | None:
    if token.startswith("urn:eoip:"):
        return token if store.get_vertex_by_canonical_id(token) else token
    lookups = (
        ("WorkItem", "issue_key"),
        ("Commit", "commit_sha"),
        ("CodeSymbol", "qualified_name"),
        ("File", "path"),
        ("Document", "name"),
        ("Service", "name"),
        ("Repository", "name"),
    )
    for label, prop in lookups:
        if label not in VERTEX_LABELS:
            continue
        matches = store.find_vertices(label=label, filters={prop: token}, limit=2)
        if matches:
            return matches[0]["canonical_id"]
    return None


def _quoted_phrases(text: str) -> list[str]:
    phrases = re.findall(r'"([^"]{2,120})"|\'([^\']{2,120})\'', text)
    return [a or b for a, b in phrases]


def _fallback_search_plan(text: str) -> QueryPlan | None:
    words = [word.casefold() for word in _WORD.findall(text)]
    if not (set(words) & _GRAPH_HINTS):
        return None
    terms = [word for word in words if word not in _STOPWORDS and word not in _GRAPH_HINTS]
    if not terms:
        return None
    return QueryPlan(
        intent="SEARCH",
        anchors=[" ".join(terms[:4])],
        max_depth=1,
        result_limit=25,
        evidence_mode="NONE",
    )


def _search_plan(anchor: str) -> QueryPlan:
    return QueryPlan(
        intent="SEARCH",
        anchors=[anchor],
        max_depth=1,
        result_limit=25,
        evidence_mode="NONE",
    )


def _confidence_for(interpretation: NLInterpretation) -> float:
    if interpretation.interpreted_via == "rules":
        return 0.88
    if interpretation.interpreted_via == "model":
        return 0.72
    return 0.45


def _node_ids(nodes: list[GraphNode]) -> list[str]:
    return [node.id for node in nodes[:25]]


def _node_name(node: GraphNode) -> str:
    props = node.properties
    return str(
        props.get("issue_key")
        or props.get("name")
        or props.get("display_name")
        or props.get("qualified_name")
        or props.get("path")
        or props.get("commit_sha")
        or node.id
    )


def _answer_graph_result(plan: QueryPlan, result: GraphResult) -> str:
    node_count = len(result.nodes)
    edge_count = len(result.edges)
    if node_count == 0:
        return "I could not find matching graph facts within the current query bounds."
    if plan.intent == "SEARCH":
        preview = ", ".join(f"{_node_name(node)} ({node.label})" for node in result.nodes[:5])
        more = "" if node_count <= 5 else f", plus {node_count - 5} more"
        return f"Found {node_count} matching graph entit{'y' if node_count == 1 else 'ies'}: {preview}{more}."
    if plan.intent == "PATH":
        if not result.paths:
            return "No path was found between the requested anchors within the configured depth."
        names = {node.id: _node_name(node) for node in result.nodes}
        first = result.paths[0]
        route = " -> ".join(names.get(node_id, node_id) for node_id in first.node_ids)
        return f"Found a path with {len(first.node_ids)} entities: {route}."
    if plan.intent == "IMPACT":
        return f"Impact analysis returned {node_count} entities and {edge_count} relationships within {plan.max_depth} hops."
    if plan.intent == "NEIGHBORHOOD":
        return f"The neighborhood contains {node_count} entities and {edge_count} relationships."
    if plan.intent == "LINEAGE":
        return f"Lineage returned {node_count} entities and {edge_count} evidence/provenance relationships."
    if plan.intent == "TRACEABILITY":
        return f"Traceability returned {node_count} entities, {edge_count} relationships, and {len(result.evidence)} evidence references."
    return f"Returned {node_count} entities and {edge_count} relationships."


def _answer_eql(result: dict) -> str:
    if "error" in result:
        return str(result["error"])
    if result.get("query") == "COUNT":
        return f"{result['target']} count: {result['count']}."
    if "domains" in result:
        return f"Available graph domains: {', '.join(result['domains'])}."
    if "labels" in result:
        labels = result.get("labels", [])
        return f"Available labels ({len(labels)}): {', '.join(labels[:20])}."
    return "The graph fact query completed."


def _answer_operator(operator: str, result: dict) -> str:
    if result.get("error"):
        return str(result["error"])
    if operator == "WHY":
        total = result.get("total_reasons", len(result.get("reasons", [])))
        return f"Found {total} reason{'s' if total != 1 else ''} for {result.get('entity')}."
    if operator == "WHY_NOT":
        if result.get("connected"):
            return "Those entities are already directly connected."
        reasons = result.get("reasons", [])
        if not reasons:
            return "No direct connection was found, and no additional diagnostic reason was available."
        return "; ".join(str(reason.get("description") or reason.get("type")) for reason in reasons)
    if operator == "WHAT_CHANGED":
        total = result.get("total_changes", len(result.get("changes", [])))
        return f"Found {total} recorded change{'s' if total != 1 else ''} for {result.get('entity')}."
    if operator == "CONTEXT":
        parts = [name for name in ("when", "who", "where", "how") if result.get(name)]
        return f"Context for {result.get('entity')} includes: {', '.join(parts) if parts else 'no populated context fields'}."
    return "The structured query operator completed."


def _followups_for(plan: QueryPlan) -> list[str]:
    anchor = plan.anchors[0] if plan.anchors else "that entity"
    if plan.intent == "SEARCH":
        return ["Ask for impact, traceability, lineage, or a path using one of the returned IDs."]
    if plan.intent == "PATH":
        return ["Ask why either endpoint exists, or request impact from an endpoint."]
    return [
        f"Ask why {anchor} exists.",
        f"Ask what changed for {anchor}.",
    ]


def _clarification(question: str, reason: str) -> NLQResponse:
    return NLQResponse(
        question=question,
        engine="clarification",
        interpretation=NLInterpretation(
            clarification=CLARIFICATION_PROMPT,
            explanation=reason,
            interpreted_via="fallback",
        ),
        answer=CLARIFICATION_PROMPT,
        confidence=0.0,
    )
