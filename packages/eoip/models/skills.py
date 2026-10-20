"""Prompt / skill registry (SR-LLM-006).

A skill version bundles a prompt template, an output JSON Schema and a few-shot set. Versions are
immutable; a version becomes active only after it passes its regression suite at least as well as
the active one. A/B splits route deterministically by request id. Tenants may override a skill with
their own version (same regression gate). Rendered prompts are DLP-scanned: raw sensitive values
are refused unless the tenant's policy allows them.
"""

from __future__ import annotations

import hashlib
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from eoip.egress.dlp import DlpScanner

_VAR = re.compile(r"\{\{(\w+)\}\}")


class SensitivePromptContent(PermissionError):
    pass


class RegressionFailed(ValueError):
    pass


@dataclass(frozen=True)
class SkillVersion:
    name: str
    version: int
    template: str
    output_schema: dict[str, Any]
    few_shot: tuple[tuple[str, str], ...] = ()
    tenant_id: str | None = None  # None = platform default

    @property
    def fingerprint(self) -> str:
        return hashlib.sha256(repr((self.template, sorted(self.output_schema.items()), self.few_shot)).encode()
                              ).hexdigest()[:16]


@dataclass
class RegressionCase:
    variables: dict[str, Any]
    check: Callable[[str], bool]  # check on the rendered prompt / model output


@dataclass
class SkillRegistry:
    scanner: DlpScanner = field(default_factory=DlpScanner)
    raw_sensitive_allowed: set[str] = field(default_factory=set)  # tenants whose policy allows it
    versions: dict[tuple[str, str | None], list[SkillVersion]] = field(default_factory=dict)
    active: dict[tuple[str, str | None], int] = field(default_factory=dict)
    scores: dict[tuple[str, str | None, int], float] = field(default_factory=dict)
    ab: dict[str, tuple[int, int, float]] = field(default_factory=dict)
    ab_outcomes: dict[tuple[str, int], list[float]] = field(default_factory=dict)

    def add(self, name: str, template: str, output_schema: dict[str, Any],
            few_shot: list[tuple[str, str]] | None = None, *, tenant_id: str | None = None) -> SkillVersion:
        key = (name, tenant_id)
        history = self.versions.setdefault(key, [])
        sv = SkillVersion(name, len(history) + 1, template, dict(output_schema), tuple(few_shot or ()), tenant_id)
        history.append(sv)
        return sv

    def evaluate(self, sv: SkillVersion, suite: list[RegressionCase],
                 run: Callable[[SkillVersion, str], str] | None = None) -> float:
        """Score = fraction of regression cases passing. ``run`` maps a rendered prompt to model output."""
        passed = 0
        for case in suite:
            rendered = self._render_raw(sv, case.variables)
            passed += bool(case.check(run(sv, rendered) if run else rendered))
        score = passed / len(suite) if suite else 0.0
        self.scores[(sv.name, sv.tenant_id, sv.version)] = score
        return score

    def promote(self, sv: SkillVersion, suite: list[RegressionCase],
                run: Callable[[SkillVersion, str], str] | None = None) -> float:
        """Activate ``sv`` only if it scores >= the currently active version (regression gate)."""
        if not suite:
            raise RegressionFailed("a regression suite is required to promote a skill")
        key = (sv.name, sv.tenant_id)
        score = self.evaluate(sv, suite, run)
        current = self.active.get(key)
        if current is not None:
            baseline = self.evaluate(self.versions[key][current - 1], suite, run)
            if score < baseline:
                raise RegressionFailed(f"{sv.name} v{sv.version} scored {score:.2f} < active v{current} {baseline:.2f}")
        self.active[key] = sv.version
        return score

    def start_ab(self, name: str, a: int, b: int, share_b: float) -> None:
        self.ab[name] = (a, b, share_b)

    def record_outcome(self, name: str, version: int, score: float) -> None:
        self.ab_outcomes.setdefault((name, version), []).append(score)

    def ab_result(self, name: str, *, min_samples: int = 20) -> dict[str, Any]:
        """Mean outcome per arm; a winner is named only with enough samples on both arms."""
        a, b, _ = self.ab[name]
        arms = {v: self.ab_outcomes.get((name, v), []) for v in (a, b)}
        means = {v: (sum(x) / len(x) if x else None) for v, x in arms.items()}
        enough = all(len(x) >= min_samples for x in arms.values())
        winner = max(means, key=lambda v: means[v]) if enough and means[a] != means[b] else None
        return {"means": means, "samples": {v: len(x) for v, x in arms.items()}, "winner": winner}

    def resolve(self, name: str, *, tenant_id: str, request_id: str = "") -> SkillVersion:
        """Tenant override first, then platform default (with any A/B split)."""
        if (name, tenant_id) in self.active:
            return self.versions[(name, tenant_id)][self.active[(name, tenant_id)] - 1]
        version = self.active[(name, None)]
        if name in self.ab:
            a, b, share_b = self.ab[name]
            bucket = int(hashlib.sha256(f"{name}:{request_id}".encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
            version = b if bucket < share_b else a
        return self.versions[(name, None)][version - 1]

    def _render_raw(self, sv: SkillVersion, variables: dict[str, Any]) -> str:
        missing = set(_VAR.findall(sv.template)) - set(variables)
        if missing:
            raise KeyError(f"missing prompt variables: {sorted(missing)}")
        shots = "".join(f"Input: {i}\nOutput: {o}\n\n" for i, o in sv.few_shot)
        return shots + _VAR.sub(lambda m: str(variables[m.group(1)]), sv.template)

    def render(self, name: str, variables: dict[str, Any], *, tenant_id: str, request_id: str = "") -> str:
        sv = self.resolve(name, tenant_id=tenant_id, request_id=request_id)
        text = self._render_raw(sv, variables)
        findings = self.scanner.scan_text(text)
        if findings and tenant_id not in self.raw_sensitive_allowed:
            raise SensitivePromptContent(
                "rendered prompt contains sensitive values: " + ",".join(sorted({f.detector for f in findings})))
        return text
