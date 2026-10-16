"""Tests for the NL suggestion engine (SR-NLQ-001..005)."""

from __future__ import annotations

import pytest

from eoip.authz.core import PolicyEnforcer, PolicyStatement
from eoip.graph.memory import MemoryGraphStore
from eoip.suggest import SuggestionEngine, SuggestionRequest, choose_answer_mode
from eoip.suggest.models import COST_TIERS
from eoip.suggest.parser import parse_question
from eoip.suggest.router import build_router

pytestmark = pytest.mark.skipif(False, reason="SR-NLQ tests always run")


def _store_with_ambiguous_service() -> MemoryGraphStore:
    store = MemoryGraphStore()
    for cid, env in (("svc:payments:dev", "dev"), ("svc:payments:prod", "prod")):
        store.upsert_vertex("Service", {
            "canonical_id": f"urn:eoip:svc:{cid}",
            "service_id": cid,
            "name": "payments",
            "source_system": env,
            "environment": env,
            "source_aliases": f"{env}:payments",
        })
    return store


class TestParser:
    def test_impact_intent_scores_highest(self):
        parsed = parse_question("what is the blast radius if payments goes down?")
        assert parsed.intent == "impact"
        assert parsed.mentions

    def test_all_taxonomy_intents_recognized(self):
        cases = {
            "lookup": "what is the payments service?",
            "traversal": "what depends on payments?",
            "impact": "what is the blast radius of payments?",
            "ownership": "who owns the payments service?",
            "change-history": "who changed payments recently?",
            "coverage": "what coverage do we have for payments?",
            "temporal": "what did payments look like as of 2026-01-01?",
            "aggregation": "how many services are there per team?",
            "similarity": "what services are similar to payments?",
            "explain-why": "why is payments marked critical?",
        }
        for intent, question in cases.items():
            assert parse_question(question).intent == intent, question


class TestSuggestionEngine:
    def test_ambiguous_service_returns_candidates_with_alternatives(self):
        engine = SuggestionEngine(_store_with_ambiguous_service())
        resp = engine.suggest(SuggestionRequest(question='what is "payments"?'))
        assert resp.candidates
        top = resp.candidates[0]
        assert top.entity_bindings, "expected entity bindings for a resolvable mention"
        binding = top.entity_bindings[0]
        assert binding.ambiguous
        assert len(binding.alternatives) >= 2  # dev + prod duplicates (SR-NLQ-003)
        envs = {a.environment for a in binding.alternatives}
        assert envs == {"dev", "prod"}
        assert top.paraphrase
        assert top.result_shape["kind"]
        assert top.data_coverage_note

    def test_impact_question_produces_blast_radius_plan_with_cost_tier(self):
        engine = SuggestionEngine(_store_with_ambiguous_service())
        resp = engine.suggest(SuggestionRequest(question="what is the blast radius if payments fails?"))
        top = resp.candidates[0]
        assert top.intent == "impact"
        assert top.plan_preview.intent == "IMPACT"
        assert top.plan_preview.max_depth >= 3
        assert top.cost_tier in COST_TIERS
        assert top.estimated_latency_ms == COST_TIERS[top.cost_tier]["estimated_latency_ms"]
        assert "blast radius" in top.paraphrase

    def test_deterministic_no_model(self):
        engine = SuggestionEngine(_store_with_ambiguous_service())
        req = SuggestionRequest(question="who owns payments?")
        first = engine.suggest(req)
        second = engine.suggest(req)
        assert not first.llm_assist_used
        assert all(c.source == "template" for c in first.candidates)
        strip = lambda r: [[c.paraphrase, c.confidence, c.plan_preview.intent] for c in r.candidates]
        assert strip(first) == strip(second)

    def test_permission_note_present(self):
        engine = SuggestionEngine(_store_with_ambiguous_service())
        resp = engine.suggest(SuggestionRequest(question="what is payments?"))
        note = resp.candidates[0].permissions
        assert "graph:read" in note.permissions
        assert note.note

    def test_permission_precheck_with_enforcer(self):
        enforcer = PolicyEnforcer([PolicyStatement(
            policy_id="p1", role="analyst", permission="graph:read",
        )])
        engine = SuggestionEngine(_store_with_ambiguous_service(), enforcer=enforcer)
        resp = engine.suggest(SuggestionRequest(
            question="what is payments?", user_id="u1", roles=["analyst"],
        ))
        note = resp.candidates[0].permissions
        assert note.evaluated
        assert note.allowed is True
        denied = SuggestionEngine(_store_with_ambiguous_service(), enforcer=enforcer).suggest(
            SuggestionRequest(question="what is payments?", user_id="u2", roles=[])
        )
        assert denied.candidates[0].permissions.allowed is False

    def test_ranking_confidence_monotonic(self):
        engine = SuggestionEngine(_store_with_ambiguous_service())
        resp = engine.suggest(SuggestionRequest(question="what is the blast radius of payments?"))
        confidences = [c.confidence for c in resp.candidates]
        assert confidences == sorted(confidences, reverse=True)
        assert len(set(confidences)) > 1 or len(confidences) == 1

    def test_no_store_still_suggests(self):
        engine = SuggestionEngine()
        resp = engine.suggest(SuggestionRequest(question="who owns payments?"))
        assert resp.candidates
        assert resp.candidates[0].permissions.permissions == ["graph:read"]


class TestAnswerModes:
    def test_choose_answer_mode(self):
        assert choose_answer_mode("lookup") == "deterministic"
        assert choose_answer_mode("impact") == "deterministic"
        assert choose_answer_mode("explain-why") == "exploratory"
        assert choose_answer_mode("similarity") == "exploratory"
        assert choose_answer_mode("anything", long_form=True) == "report"

    def test_candidates_carry_answer_mode(self):
        engine = SuggestionEngine(_store_with_ambiguous_service())
        resp = engine.suggest(SuggestionRequest(question="why is payments critical?"))
        assert resp.candidates[0].answer_mode == "exploratory"


class TestRouter:
    def test_suggest_route(self):
        from fastapi.testclient import TestClient
        from fastapi import FastAPI

        app = FastAPI()
        app.include_router(build_router(_store_with_ambiguous_service()))
        client = TestClient(app)
        resp = client.post("/api/v1/suggest", json={"question": "what is payments?"})
        assert resp.status_code == 200
        body = resp.json()
        assert body["candidates"]
        assert body["parse"]["intent"] == "lookup"

    def test_intents_route(self):
        from fastapi.testclient import TestClient
        from fastapi import FastAPI

        app = FastAPI()
        app.include_router(build_router())
        client = TestClient(app)
        resp = client.get("/api/v1/suggest/intents")
        assert resp.status_code == 200
        assert "impact" in resp.json()["intents"]
