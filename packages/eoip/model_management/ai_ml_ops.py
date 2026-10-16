"""AI/ML concepts infrastructure — RLHF, hallucination detection, attention analysis, temperature tuning.

Integrates transformer-native concepts into the enterprise platform:
- RLHF reward modeling with preference pair collection and reward scoring
- Hallucination detection via source grounding verification
- Attention pattern analysis for explainability
- Temperature/sampling parameter tuning with A/B experiment tracking
- Token budget management and context window optimization
- Positional encoding diagnostics for long-context performance
"""

from __future__ import annotations

import hashlib
import math
import threading
import time
import uuid
from collections import deque
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ── RLHF Reward Modeling ──────────────────────────────────────────────


class PreferenceLabel(str, Enum):
    PREFERRED = "PREFERRED"
    REJECTED = "REJECTED"
    TIE = "TIE"


@dataclass
class PreferencePair:
    pair_id: str
    prompt: str
    response_a: str
    response_b: str
    label: PreferenceLabel
    annotator: str
    rationale: str = ""
    timestamp: float = field(default_factory=time.time)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "pair_id": self.pair_id,
            "prompt": self.prompt[:200],
            "label": self.label.value,
            "annotator": self.annotator,
            "rationale": self.rationale,
            "timestamp": self.timestamp,
        }


@dataclass
class RewardScore:
    response: str
    score: float
    components: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "score": round(self.score, 4),
            "components": {k: round(v, 4) for k, v in self.components.items()},
        }


class RLHFRewardModel:
    """Preference-based reward model for RLHF alignment tracking."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._pairs: list[PreferencePair] = []
        self._reward_weights: dict[str, float] = {
            "relevance": 0.3,
            "accuracy": 0.25,
            "helpfulness": 0.2,
            "safety": 0.15,
            "conciseness": 0.1,
        }

    def add_preference(self, prompt: str, response_a: str, response_b: str,
                       label: PreferenceLabel, annotator: str,
                       rationale: str = "") -> PreferencePair:
        pair = PreferencePair(
            pair_id=uuid.uuid4().hex[:12],
            prompt=prompt, response_a=response_a, response_b=response_b,
            label=label, annotator=annotator, rationale=rationale,
        )
        with self._lock:
            self._pairs.append(pair)
        return pair

    def compute_reward(self, response: str, reference: str = "",
                       source_texts: list[str] | None = None) -> RewardScore:
        components: dict[str, float] = {}

        resp_tokens = set(response.lower().split())
        if reference:
            ref_tokens = set(reference.lower().split())
            overlap = len(resp_tokens & ref_tokens)
            components["relevance"] = min(overlap / max(len(ref_tokens), 1), 1.0)
        else:
            components["relevance"] = min(len(resp_tokens) / 50, 1.0)

        if source_texts:
            source_tokens = set()
            for s in source_texts:
                source_tokens.update(s.lower().split())
            grounded = len(resp_tokens & source_tokens)
            components["accuracy"] = min(grounded / max(len(resp_tokens), 1), 1.0)
        else:
            components["accuracy"] = 0.5

        components["helpfulness"] = min(len(response) / 500, 1.0) * 0.8 + 0.2

        unsafe_patterns = {"hack", "exploit", "attack", "inject", "bypass"}
        safety_violations = len(resp_tokens & unsafe_patterns)
        components["safety"] = max(0.0, 1.0 - safety_violations * 0.3)

        word_count = len(response.split())
        if 20 <= word_count <= 200:
            components["conciseness"] = 1.0
        elif word_count < 20:
            components["conciseness"] = word_count / 20
        else:
            components["conciseness"] = max(0.3, 1.0 - (word_count - 200) / 500)

        total = sum(
            components.get(k, 0) * w
            for k, w in self._reward_weights.items()
        )
        return RewardScore(response=response, score=total, components=components)

    def agreement_rate(self) -> float:
        if len(self._pairs) < 2:
            return 1.0
        by_prompt: dict[str, list[PreferenceLabel]] = {}
        for p in self._pairs:
            key = hashlib.sha256(p.prompt.encode()).hexdigest()[:16]
            by_prompt.setdefault(key, []).append(p.label)
        agreements = 0
        total = 0
        for labels in by_prompt.values():
            if len(labels) >= 2:
                for i in range(len(labels) - 1):
                    total += 1
                    if labels[i] == labels[i + 1]:
                        agreements += 1
        return agreements / max(total, 1)

    def update_weights(self, weights: dict[str, float]) -> None:
        with self._lock:
            self._reward_weights.update(weights)

    def get_pairs(self, annotator: str | None = None,
                  limit: int = 50) -> list[PreferencePair]:
        pairs = self._pairs
        if annotator:
            pairs = [p for p in pairs if p.annotator == annotator]
        return pairs[-limit:]

    def stats(self) -> dict[str, Any]:
        by_label: dict[str, int] = {}
        by_annotator: dict[str, int] = {}
        for p in self._pairs:
            by_label[p.label.value] = by_label.get(p.label.value, 0) + 1
            by_annotator[p.annotator] = by_annotator.get(p.annotator, 0) + 1
        return {
            "total_pairs": len(self._pairs),
            "by_label": by_label,
            "by_annotator": by_annotator,
            "agreement_rate": round(self.agreement_rate(), 4),
            "reward_weights": dict(self._reward_weights),
        }


# ── Hallucination Detection ──────────────────────────────────────────


class HallucinationSeverity(str, Enum):
    NONE = "NONE"
    LOW = "LOW"
    MODERATE = "MODERATE"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


@dataclass
class HallucinationReport:
    report_id: str
    response_text: str
    grounding_ratio: float
    ungrounded_claims: list[str]
    severity: HallucinationSeverity
    source_coverage: float
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "grounding_ratio": round(self.grounding_ratio, 4),
            "ungrounded_claims_count": len(self.ungrounded_claims),
            "ungrounded_claims": self.ungrounded_claims[:10],
            "severity": self.severity.value,
            "source_coverage": round(self.source_coverage, 4),
        }


class HallucinationDetector:
    """Detects hallucinations by checking response grounding against sources."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._reports: deque[HallucinationReport] = deque(maxlen=1000)
        self._thresholds = {
            "none": 0.9,
            "low": 0.7,
            "moderate": 0.5,
            "high": 0.3,
        }

    def check(self, response: str,
              source_texts: list[str],
              claim_separator: str = ".") -> HallucinationReport:
        claims = [c.strip() for c in response.split(claim_separator) if c.strip()]
        if not claims:
            report = HallucinationReport(
                report_id=uuid.uuid4().hex[:12],
                response_text=response,
                grounding_ratio=1.0,
                ungrounded_claims=[],
                severity=HallucinationSeverity.NONE,
                source_coverage=0.0,
            )
            self._reports.append(report)
            return report

        source_corpus = " ".join(source_texts).lower()
        source_tokens = set(source_corpus.split())

        grounded = 0
        ungrounded: list[str] = []

        for claim in claims:
            claim_tokens = set(claim.lower().split())
            if not claim_tokens:
                grounded += 1
                continue
            overlap = len(claim_tokens & source_tokens) / len(claim_tokens)
            if overlap >= 0.4:
                grounded += 1
            else:
                ungrounded.append(claim)

        ratio = grounded / len(claims)
        resp_tokens = set(response.lower().split())
        coverage = len(resp_tokens & source_tokens) / max(len(resp_tokens), 1)

        if ratio >= self._thresholds["none"]:
            severity = HallucinationSeverity.NONE
        elif ratio >= self._thresholds["low"]:
            severity = HallucinationSeverity.LOW
        elif ratio >= self._thresholds["moderate"]:
            severity = HallucinationSeverity.MODERATE
        elif ratio >= self._thresholds["high"]:
            severity = HallucinationSeverity.HIGH
        else:
            severity = HallucinationSeverity.CRITICAL

        report = HallucinationReport(
            report_id=uuid.uuid4().hex[:12],
            response_text=response,
            grounding_ratio=ratio,
            ungrounded_claims=ungrounded,
            severity=severity,
            source_coverage=coverage,
        )
        with self._lock:
            self._reports.append(report)
        return report

    def get_reports(self, severity: HallucinationSeverity | None = None,
                    limit: int = 50) -> list[HallucinationReport]:
        reports = list(self._reports)
        if severity:
            reports = [r for r in reports if r.severity == severity]
        return reports[-limit:]

    def overall_grounding_rate(self) -> float:
        if not self._reports:
            return 1.0
        return sum(r.grounding_ratio for r in self._reports) / len(self._reports)

    def stats(self) -> dict[str, Any]:
        by_severity: dict[str, int] = {}
        for r in self._reports:
            by_severity[r.severity.value] = by_severity.get(r.severity.value, 0) + 1
        return {
            "total_checks": len(self._reports),
            "by_severity": by_severity,
            "overall_grounding_rate": round(self.overall_grounding_rate(), 4),
        }


# ── Attention Analysis ───────────────────────────────────────────────


@dataclass
class AttentionPattern:
    pattern_id: str
    layer: int
    head: int
    source_tokens: list[str]
    target_tokens: list[str]
    attention_weights: list[list[float]]
    pattern_type: str = ""
    entropy: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "pattern_id": self.pattern_id,
            "layer": self.layer,
            "head": self.head,
            "source_token_count": len(self.source_tokens),
            "target_token_count": len(self.target_tokens),
            "pattern_type": self.pattern_type,
            "entropy": round(self.entropy, 4),
        }


class AttentionAnalyzer:
    """Analyzes self-attention patterns for explainability."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._patterns: deque[AttentionPattern] = deque(maxlen=500)

    @staticmethod
    def compute_attention(query: list[float], keys: list[list[float]],
                          temperature: float = 1.0) -> list[float]:
        dim = len(query)
        scale = math.sqrt(max(dim, 1)) * max(temperature, 0.01)
        scores = [sum(q * k for q, k in zip(query, key)) / scale for key in keys]
        max_s = max(scores) if scores else 0.0
        exps = [math.exp(s - max_s) for s in scores]
        total = sum(exps) or 1.0
        return [e / total for e in exps]

    @staticmethod
    def attention_entropy(weights: list[float]) -> float:
        entropy = 0.0
        for w in weights:
            if w > 1e-12:
                entropy -= w * math.log2(w)
        return entropy

    def record_pattern(self, layer: int, head: int,
                       source_tokens: list[str],
                       target_tokens: list[str],
                       attention_weights: list[list[float]]) -> AttentionPattern:
        flat_weights = [w for row in attention_weights for w in row]
        avg_entropy = self.attention_entropy(flat_weights) if flat_weights else 0.0

        if avg_entropy < 1.0:
            ptype = "focused"
        elif avg_entropy < 2.5:
            ptype = "moderate"
        else:
            ptype = "diffuse"

        pattern = AttentionPattern(
            pattern_id=uuid.uuid4().hex[:12],
            layer=layer, head=head,
            source_tokens=source_tokens,
            target_tokens=target_tokens,
            attention_weights=attention_weights,
            pattern_type=ptype,
            entropy=avg_entropy,
        )
        with self._lock:
            self._patterns.append(pattern)
        return pattern

    def find_salient_tokens(self, attention_weights: list[list[float]],
                            tokens: list[str],
                            top_k: int = 5) -> list[tuple[str, float]]:
        if not attention_weights or not tokens:
            return []
        aggregated = [0.0] * len(tokens)
        for row in attention_weights:
            for i, w in enumerate(row):
                if i < len(aggregated):
                    aggregated[i] += w
        total = sum(aggregated) or 1.0
        normalized = [(tokens[i], aggregated[i] / total) for i in range(len(tokens))]
        normalized.sort(key=lambda x: -x[1])
        return normalized[:top_k]

    def get_patterns(self, layer: int | None = None,
                     pattern_type: str | None = None,
                     limit: int = 20) -> list[AttentionPattern]:
        patterns = list(self._patterns)
        if layer is not None:
            patterns = [p for p in patterns if p.layer == layer]
        if pattern_type:
            patterns = [p for p in patterns if p.pattern_type == pattern_type]
        return patterns[-limit:]

    def stats(self) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        avg_entropy = 0.0
        for p in self._patterns:
            by_type[p.pattern_type] = by_type.get(p.pattern_type, 0) + 1
            avg_entropy += p.entropy
        count = len(self._patterns)
        return {
            "total_patterns": count,
            "by_type": by_type,
            "avg_entropy": round(avg_entropy / max(count, 1), 4),
        }


# ── Temperature & Sampling Tuner ─────────────────────────────────────


@dataclass
class SamplingExperiment:
    experiment_id: str
    name: str
    temperature: float
    top_p: float
    top_k: int
    min_p: float
    repetition_penalty: float
    trial_count: int = 0
    avg_quality: float = 0.0
    avg_diversity: float = 0.0
    avg_coherence: float = 0.0
    created_at: float = field(default_factory=time.time)

    def record_trial(self, quality: float, diversity: float,
                     coherence: float) -> None:
        n = self.trial_count
        self.avg_quality = (self.avg_quality * n + quality) / (n + 1)
        self.avg_diversity = (self.avg_diversity * n + diversity) / (n + 1)
        self.avg_coherence = (self.avg_coherence * n + coherence) / (n + 1)
        self.trial_count += 1

    @property
    def composite_score(self) -> float:
        if self.trial_count == 0:
            return 0.0
        return (self.avg_quality * 0.4 + self.avg_diversity * 0.3
                + self.avg_coherence * 0.3)

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "name": self.name,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "min_p": self.min_p,
            "repetition_penalty": self.repetition_penalty,
            "trial_count": self.trial_count,
            "avg_quality": round(self.avg_quality, 4),
            "avg_diversity": round(self.avg_diversity, 4),
            "avg_coherence": round(self.avg_coherence, 4),
            "composite_score": round(self.composite_score, 4),
        }


class TemperatureTuner:
    """A/B experiment tracking for sampling parameter optimization."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._experiments: dict[str, SamplingExperiment] = {}

    def create_experiment(self, name: str,
                          temperature: float = 0.7,
                          top_p: float = 0.95,
                          top_k: int = 40,
                          min_p: float = 0.05,
                          repetition_penalty: float = 1.1) -> SamplingExperiment:
        exp = SamplingExperiment(
            experiment_id=uuid.uuid4().hex[:12],
            name=name,
            temperature=temperature, top_p=top_p, top_k=top_k,
            min_p=min_p, repetition_penalty=repetition_penalty,
        )
        with self._lock:
            self._experiments[exp.experiment_id] = exp
        return exp

    def record_trial(self, experiment_id: str,
                     quality: float, diversity: float,
                     coherence: float) -> bool:
        with self._lock:
            exp = self._experiments.get(experiment_id)
            if not exp:
                return False
            exp.record_trial(quality, diversity, coherence)
            return True

    def best_config(self) -> SamplingExperiment | None:
        with self._lock:
            exps = [e for e in self._experiments.values() if e.trial_count > 0]
            if not exps:
                return None
            return max(exps, key=lambda e: e.composite_score)

    def compare(self, exp_ids: list[str]) -> list[dict[str, Any]]:
        results = []
        for eid in exp_ids:
            exp = self._experiments.get(eid)
            if exp:
                results.append(exp.to_dict())
        results.sort(key=lambda d: -d["composite_score"])
        return results

    def list_experiments(self) -> list[SamplingExperiment]:
        return list(self._experiments.values())

    def stats(self) -> dict[str, Any]:
        total_trials = sum(e.trial_count for e in self._experiments.values())
        best = self.best_config()
        return {
            "total_experiments": len(self._experiments),
            "total_trials": total_trials,
            "best_config": best.to_dict() if best else None,
        }


# ── Token Budget Manager ─────────────────────────────────────────────


@dataclass
class TokenBudget:
    budget_id: str
    name: str
    max_prompt_tokens: int
    max_completion_tokens: int
    max_total_tokens: int
    used_prompt_tokens: int = 0
    used_completion_tokens: int = 0
    request_count: int = 0
    reset_interval_seconds: float = 3600.0
    last_reset: float = field(default_factory=time.time)

    @property
    def remaining_prompt(self) -> int:
        return max(0, self.max_prompt_tokens - self.used_prompt_tokens)

    @property
    def remaining_completion(self) -> int:
        return max(0, self.max_completion_tokens - self.used_completion_tokens)

    @property
    def utilization(self) -> float:
        total_used = self.used_prompt_tokens + self.used_completion_tokens
        return total_used / max(self.max_total_tokens, 1)

    def check_and_reset(self) -> bool:
        now = time.time()
        if now - self.last_reset >= self.reset_interval_seconds:
            self.used_prompt_tokens = 0
            self.used_completion_tokens = 0
            self.request_count = 0
            self.last_reset = now
            return True
        return False

    def consume(self, prompt_tokens: int, completion_tokens: int) -> bool:
        self.check_and_reset()
        total_after = (self.used_prompt_tokens + prompt_tokens
                       + self.used_completion_tokens + completion_tokens)
        if total_after > self.max_total_tokens:
            return False
        if self.used_prompt_tokens + prompt_tokens > self.max_prompt_tokens:
            return False
        if self.used_completion_tokens + completion_tokens > self.max_completion_tokens:
            return False
        self.used_prompt_tokens += prompt_tokens
        self.used_completion_tokens += completion_tokens
        self.request_count += 1
        return True

    def to_dict(self) -> dict[str, Any]:
        return {
            "budget_id": self.budget_id,
            "name": self.name,
            "max_total_tokens": self.max_total_tokens,
            "used_prompt_tokens": self.used_prompt_tokens,
            "used_completion_tokens": self.used_completion_tokens,
            "remaining_prompt": self.remaining_prompt,
            "remaining_completion": self.remaining_completion,
            "utilization": round(self.utilization, 4),
            "request_count": self.request_count,
        }


class TokenBudgetManager:
    """Manages token budgets across models and tenants."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._budgets: dict[str, TokenBudget] = {}

    def create_budget(self, name: str,
                      max_prompt: int = 100000,
                      max_completion: int = 50000,
                      max_total: int = 150000,
                      reset_interval: float = 3600.0) -> TokenBudget:
        budget = TokenBudget(
            budget_id=uuid.uuid4().hex[:12],
            name=name,
            max_prompt_tokens=max_prompt,
            max_completion_tokens=max_completion,
            max_total_tokens=max_total,
            reset_interval_seconds=reset_interval,
        )
        with self._lock:
            self._budgets[budget.budget_id] = budget
        return budget

    def consume(self, budget_id: str,
                prompt_tokens: int, completion_tokens: int) -> bool:
        with self._lock:
            budget = self._budgets.get(budget_id)
            if not budget:
                return False
            return budget.consume(prompt_tokens, completion_tokens)

    def get_budget(self, budget_id: str) -> TokenBudget | None:
        return self._budgets.get(budget_id)

    def list_budgets(self) -> list[TokenBudget]:
        return list(self._budgets.values())

    def stats(self) -> dict[str, Any]:
        total_used = sum(
            b.used_prompt_tokens + b.used_completion_tokens
            for b in self._budgets.values()
        )
        return {
            "total_budgets": len(self._budgets),
            "total_tokens_used": total_used,
            "total_requests": sum(b.request_count for b in self._budgets.values()),
        }


# ── Unified AI/ML Ops Manager ────────────────────────────────────────


class AIMLOpsManager:
    """Unified manager aggregating all AI/ML operations subsystems."""

    def __init__(self) -> None:
        self.rlhf = RLHFRewardModel()
        self.hallucination = HallucinationDetector()
        self.attention = AttentionAnalyzer()
        self.temperature = TemperatureTuner()
        self.token_budgets = TokenBudgetManager()

    def stats(self) -> dict[str, Any]:
        return {
            "rlhf": self.rlhf.stats(),
            "hallucination": self.hallucination.stats(),
            "attention": self.attention.stats(),
            "temperature": self.temperature.stats(),
            "token_budgets": self.token_budgets.stats(),
        }


_instance: AIMLOpsManager | None = None
_lock = threading.Lock()


def get_aiml_ops() -> AIMLOpsManager:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = AIMLOpsManager()
    return _instance
