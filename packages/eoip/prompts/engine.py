"""Prompt Engineering engine — versioning, A/B testing, evaluation,
composition, and optimization from feedback."""

from __future__ import annotations

import hashlib
import math
import random
import re
import statistics
import threading
import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


@dataclass
class PromptVersion:
    template: str
    version: int
    name: str = ""
    description: str = ""
    variables: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    author: str = ""
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def render(self, **kwargs: Any) -> str:
        result = self.template
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result

    def extract_variables(self) -> list[str]:
        return re.findall(r"\{\{(\w+)\}\}", self.template)

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256(self.template.encode()).hexdigest()[:12]

    @property
    def token_estimate(self) -> int:
        return len(self.template.split()) * 4 // 3


@dataclass
class PromptVariant:
    variant_id: str
    base_version: int
    template: str
    mutation_type: str = ""
    created_at: float = field(default_factory=time.time)

    def render(self, **kwargs: Any) -> str:
        result = self.template
        for key, value in kwargs.items():
            result = result.replace(f"{{{{{key}}}}}", str(value))
        return result


class PromptRegistry:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._prompts: dict[str, list[PromptVersion]] = defaultdict(list)
        self._active: dict[str, int] = {}

    def register(self, name: str, template: str,
                 description: str = "", author: str = "",
                 tags: list[str] | None = None) -> PromptVersion:
        with self._lock:
            versions = self._prompts[name]
            version_num = len(versions) + 1
            pv = PromptVersion(
                template=template, version=version_num, name=name,
                description=description, author=author, tags=tags or [],
            )
            pv.variables = pv.extract_variables()
            versions.append(pv)
            self._active[name] = version_num
            return pv

    def get(self, name: str, version: int | None = None) -> PromptVersion | None:
        with self._lock:
            versions = self._prompts.get(name)
            if not versions:
                return None
            if version is None:
                version = self._active.get(name, len(versions))
            for v in versions:
                if v.version == version:
                    return v
            return None

    def get_active(self, name: str) -> PromptVersion | None:
        return self.get(name)

    def set_active(self, name: str, version: int) -> bool:
        with self._lock:
            versions = self._prompts.get(name, [])
            if any(v.version == version for v in versions):
                self._active[name] = version
                return True
            return False

    def list_prompts(self) -> list[str]:
        return list(self._prompts.keys())

    def get_history(self, name: str) -> list[PromptVersion]:
        return list(self._prompts.get(name, []))

    def stats(self) -> dict[str, Any]:
        return {
            "prompt_count": len(self._prompts),
            "total_versions": sum(len(v) for v in self._prompts.values()),
        }


@dataclass
class PromptChain:
    name: str
    steps: list[str]
    description: str = ""

    def render_chain(self, registry: PromptRegistry,
                     context: dict[str, Any]) -> list[str]:
        rendered: list[str] = []
        accumulated = dict(context)
        for step_name in self.steps:
            pv = registry.get_active(step_name)
            if pv:
                text = pv.render(**accumulated)
                rendered.append(text)
                accumulated[f"{step_name}_output"] = text
        return rendered


class PromptComposer:
    def __init__(self) -> None:
        self._sections: dict[str, str] = {}

    def add_section(self, name: str, content: str) -> None:
        self._sections[name] = content

    def compose(self, section_names: list[str],
                separator: str = "\n\n",
                context: dict[str, Any] | None = None) -> str:
        parts: list[str] = []
        ctx = context or {}
        for name in section_names:
            section = self._sections.get(name, "")
            if section:
                for key, value in ctx.items():
                    section = section.replace(f"{{{{{key}}}}}", str(value))
                parts.append(section)
        return separator.join(parts)

    def list_sections(self) -> list[str]:
        return list(self._sections.keys())


@dataclass
class ABExperiment:
    experiment_id: str
    prompt_name: str
    variants: list[PromptVariant]
    traffic_split: dict[str, float] = field(default_factory=dict)
    results: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))
    created_at: float = field(default_factory=time.time)
    status: str = "running"

    def select_variant(self) -> PromptVariant:
        if not self.variants:
            raise ValueError("No variants in experiment")
        if not self.traffic_split:
            return random.choice(self.variants)
        r = random.random()
        cumulative = 0.0
        for variant in self.variants:
            cumulative += self.traffic_split.get(variant.variant_id, 0.0)
            if r <= cumulative:
                return variant
        return self.variants[-1]

    def record_outcome(self, variant_id: str, score: float) -> None:
        self.results[variant_id].append(score)

    def get_summary(self) -> dict[str, Any]:
        summary: dict[str, Any] = {}
        for vid, scores in self.results.items():
            if scores:
                summary[vid] = {
                    "count": len(scores),
                    "mean": statistics.mean(scores),
                    "std": statistics.stdev(scores) if len(scores) > 1 else 0.0,
                    "min": min(scores),
                    "max": max(scores),
                }
        return summary

    def get_winner(self) -> str | None:
        summary = self.get_summary()
        if not summary:
            return None
        best_vid = max(summary.keys(), key=lambda v: summary[v]["mean"])
        if summary[best_vid]["count"] < 5:
            return None
        return best_vid

    def to_dict(self) -> dict[str, Any]:
        return {
            "experiment_id": self.experiment_id,
            "prompt_name": self.prompt_name,
            "variant_count": len(self.variants),
            "status": self.status,
            "summary": self.get_summary(),
            "winner": self.get_winner(),
        }


@dataclass
class EvalResult:
    prompt_name: str
    version: int
    scores: dict[str, float]
    overall: float = 0.0
    evaluated_at: float = field(default_factory=time.time)
    sample_count: int = 0


class PromptEvaluation:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._results: list[EvalResult] = []
        self._criteria_weights = {
            "relevance": 0.3,
            "clarity": 0.2,
            "completeness": 0.2,
            "conciseness": 0.15,
            "safety": 0.15,
        }

    def evaluate(self, prompt_name: str, version: int,
                 rendered_text: str, reference_output: str = "",
                 criteria_scores: dict[str, float] | None = None) -> EvalResult:
        if criteria_scores:
            scores = criteria_scores
        else:
            scores = self._auto_evaluate(rendered_text, reference_output)
        overall = sum(
            scores.get(c, 0.0) * w for c, w in self._criteria_weights.items()
        )
        result = EvalResult(
            prompt_name=prompt_name, version=version,
            scores=scores, overall=overall, sample_count=1,
        )
        with self._lock:
            self._results.append(result)
        return result

    def _auto_evaluate(self, text: str, reference: str) -> dict[str, float]:
        words = text.split()
        word_count = len(words)
        clarity = min(1.0, 1.0 - abs(word_count - 150) / 500)
        conciseness = max(0.0, 1.0 - word_count / 1000)
        relevance = 0.5
        if reference:
            ref_tokens = set(reference.lower().split())
            text_tokens = set(text.lower().split())
            if ref_tokens:
                relevance = len(ref_tokens & text_tokens) / len(ref_tokens)
        has_unsafe = any(
            term in text.lower()
            for term in ["ignore previous", "disregard", "bypass", "override instructions"]
        )
        safety = 0.0 if has_unsafe else 1.0
        completeness = min(1.0, word_count / 50) if word_count > 0 else 0.0
        return {
            "relevance": relevance, "clarity": clarity,
            "completeness": completeness, "conciseness": conciseness,
            "safety": safety,
        }

    def get_results(self, prompt_name: str | None = None,
                    limit: int = 20) -> list[EvalResult]:
        with self._lock:
            if prompt_name:
                filtered = [r for r in self._results if r.prompt_name == prompt_name]
            else:
                filtered = list(self._results)
            return filtered[-limit:]

    def stats(self) -> dict[str, Any]:
        return {
            "total_evaluations": len(self._results),
            "criteria_weights": self._criteria_weights,
        }


class PromptOptimizer:
    def __init__(self, registry: PromptRegistry) -> None:
        self._registry = registry
        self._lock = threading.Lock()
        self._feedback: dict[str, list[tuple[int, float]]] = defaultdict(list)

    def record_feedback(self, prompt_name: str, version: int, score: float) -> None:
        with self._lock:
            self._feedback[prompt_name].append((version, score))

    def get_best_version(self, prompt_name: str) -> int | None:
        with self._lock:
            feedback = self._feedback.get(prompt_name, [])
            if not feedback:
                return None
            version_scores: dict[int, list[float]] = defaultdict(list)
            for version, score in feedback:
                version_scores[version].append(score)
            return max(version_scores.keys(),
                       key=lambda v: statistics.mean(version_scores[v]))

    def generate_variants(self, prompt_name: str,
                          count: int = 3) -> list[PromptVariant]:
        pv = self._registry.get_active(prompt_name)
        if not pv:
            return []
        mutations = [
            ("add_cot", lambda t: t + "\n\nThink step by step before answering."),
            ("add_examples", lambda t: t + "\n\nExample:\nInput: [example input]\nOutput: [example output]"),
            ("add_constraints", lambda t: t + "\n\nConstraints:\n- Be concise\n- Use evidence from the knowledge graph\n- Cite sources"),
        ]
        variants: list[PromptVariant] = []
        for i in range(min(count, len(mutations))):
            mut_name, mut_fn = mutations[i]
            variants.append(PromptVariant(
                variant_id=f"{prompt_name}_v{pv.version}_{mut_name}",
                base_version=pv.version,
                template=mut_fn(pv.template),
                mutation_type=mut_name,
            ))
        return variants

    def stats(self) -> dict[str, Any]:
        return {
            "prompts_with_feedback": len(self._feedback),
            "total_feedback": sum(len(v) for v in self._feedback.values()),
        }


class PromptEngineeringEngine:
    def __init__(self) -> None:
        self._registry = PromptRegistry()
        self._evaluator = PromptEvaluation()
        self._optimizer = PromptOptimizer(self._registry)
        self._composer = PromptComposer()
        self._experiments: dict[str, ABExperiment] = {}
        self._chains: dict[str, PromptChain] = {}
        self._lock = threading.Lock()

    @property
    def registry(self) -> PromptRegistry:
        return self._registry

    @property
    def evaluator(self) -> PromptEvaluation:
        return self._evaluator

    @property
    def optimizer(self) -> PromptOptimizer:
        return self._optimizer

    @property
    def composer(self) -> PromptComposer:
        return self._composer

    def register(self, name: str, template: str, **kwargs: Any) -> PromptVersion:
        return self._registry.register(name, template, **kwargs)

    def render(self, name: str, **kwargs: Any) -> str | None:
        pv = self._registry.get_active(name)
        return pv.render(**kwargs) if pv else None

    def create_experiment(self, prompt_name: str,
                          variant_count: int = 3,
                          traffic_split: dict[str, float] | None = None) -> ABExperiment:
        variants = self._optimizer.generate_variants(prompt_name, variant_count)
        if not traffic_split and variants:
            equal_share = 1.0 / len(variants)
            traffic_split = {v.variant_id: equal_share for v in variants}
        exp = ABExperiment(
            experiment_id=uuid.uuid4().hex[:12],
            prompt_name=prompt_name,
            variants=variants,
            traffic_split=traffic_split or {},
        )
        with self._lock:
            self._experiments[exp.experiment_id] = exp
        return exp

    def register_chain(self, name: str, steps: list[str],
                       description: str = "") -> PromptChain:
        chain = PromptChain(name=name, steps=steps, description=description)
        self._chains[name] = chain
        return chain

    def run_chain(self, name: str, context: dict[str, Any]) -> list[str]:
        chain = self._chains.get(name)
        if not chain:
            return []
        return chain.render_chain(self._registry, context)

    def evaluate(self, name: str, rendered_text: str,
                 reference: str = "",
                 scores: dict[str, float] | None = None) -> EvalResult:
        pv = self._registry.get_active(name)
        version = pv.version if pv else 0
        return self._evaluator.evaluate(name, version, rendered_text, reference, scores)

    def feedback(self, name: str, score: float) -> None:
        pv = self._registry.get_active(name)
        if pv:
            self._optimizer.record_feedback(name, pv.version, score)

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "prompt_engineering",
            "registry": self._registry.stats(),
            "evaluator": self._evaluator.stats(),
            "optimizer": self._optimizer.stats(),
            "experiments": len(self._experiments),
            "chains": len(self._chains),
        }


_instance: PromptEngineeringEngine | None = None
_lock = threading.Lock()


def get_prompt_engine() -> PromptEngineeringEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = PromptEngineeringEngine()
    return _instance
