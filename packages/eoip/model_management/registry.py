"""AI Model Management — registry, prompt versioning, guardrails, performance tracking.

Centralized management of AI/ML model deployments with prompt version control,
input/output guardrails, and latency/accuracy tracking.
"""

from __future__ import annotations

import enum
import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any


class ModelStatus(str, enum.Enum):
    REGISTERED = "REGISTERED"
    ACTIVE = "ACTIVE"
    DEPRECATED = "DEPRECATED"
    DISABLED = "DISABLED"


class GuardrailAction(str, enum.Enum):
    BLOCK = "BLOCK"
    WARN = "WARN"
    LOG = "LOG"
    REDACT = "REDACT"


@dataclass
class PromptVersion:
    version_id: str
    version: int
    template: str
    variables: list[str]
    author: str
    change_note: str = ""
    is_active: bool = False
    total_invocations: int = 0
    avg_latency_ms: float = 0.0
    avg_quality_score: float = 0.0
    created_at: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "version_id": self.version_id,
            "version": self.version,
            "template": self.template,
            "variables": self.variables,
            "author": self.author,
            "change_note": self.change_note,
            "is_active": self.is_active,
            "total_invocations": self.total_invocations,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "avg_quality_score": round(self.avg_quality_score, 3),
            "created_at": self.created_at,
        }


@dataclass
class Guardrail:
    guardrail_id: str
    name: str
    description: str
    check_type: str
    action: GuardrailAction
    parameters: dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    triggered_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "guardrail_id": self.guardrail_id,
            "name": self.name,
            "description": self.description,
            "check_type": self.check_type,
            "action": self.action.value,
            "enabled": self.enabled,
            "triggered_count": self.triggered_count,
        }


@dataclass
class GuardrailResult:
    guardrail_id: str
    passed: bool
    action: GuardrailAction
    message: str = ""


@dataclass
class ModelEntry:
    model_id: str
    name: str
    model_type: str
    provider: str
    description: str = ""
    status: ModelStatus = ModelStatus.REGISTERED
    config: dict[str, Any] = field(default_factory=dict)
    prompt_versions: list[PromptVersion] = field(default_factory=list)
    guardrails: list[Guardrail] = field(default_factory=list)
    total_invocations: int = 0
    total_errors: int = 0
    total_latency_ms: float = 0.0
    total_tokens: int = 0
    tags: list[str] = field(default_factory=list)
    created_at: float = field(default_factory=time.time)
    updated_at: float = field(default_factory=time.time)

    @property
    def avg_latency_ms(self) -> float:
        if self.total_invocations == 0:
            return 0.0
        return self.total_latency_ms / self.total_invocations

    @property
    def error_rate(self) -> float:
        if self.total_invocations == 0:
            return 0.0
        return self.total_errors / self.total_invocations

    @property
    def active_prompt(self) -> PromptVersion | None:
        for pv in self.prompt_versions:
            if pv.is_active:
                return pv
        return None

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_id": self.model_id,
            "name": self.name,
            "model_type": self.model_type,
            "provider": self.provider,
            "description": self.description,
            "status": self.status.value,
            "total_invocations": self.total_invocations,
            "total_errors": self.total_errors,
            "avg_latency_ms": round(self.avg_latency_ms, 2),
            "error_rate": round(self.error_rate, 4),
            "total_tokens": self.total_tokens,
            "prompt_versions_count": len(self.prompt_versions),
            "active_prompt_version": self.active_prompt.version if self.active_prompt else None,
            "guardrails_count": len(self.guardrails),
            "tags": self.tags,
            "created_at": self.created_at,
        }


class ModelRegistry:
    """Centralized AI model registry with prompt versioning and guardrails."""

    def __init__(self) -> None:
        self._models: dict[str, ModelEntry] = {}
        self._lock = threading.Lock()

    def register(self, name: str, model_type: str, provider: str,
                 description: str = "", config: dict[str, Any] | None = None,
                 tags: list[str] | None = None) -> ModelEntry:
        entry = ModelEntry(
            model_id=uuid.uuid4().hex[:12],
            name=name,
            model_type=model_type,
            provider=provider,
            description=description,
            config=config or {},
            tags=tags or [],
        )
        with self._lock:
            self._models[entry.model_id] = entry
        return entry

    def get(self, model_id: str) -> ModelEntry | None:
        with self._lock:
            return self._models.get(model_id)

    def activate(self, model_id: str) -> bool:
        with self._lock:
            m = self._models.get(model_id)
            if m is None:
                return False
            m.status = ModelStatus.ACTIVE
            m.updated_at = time.time()
            return True

    def deprecate(self, model_id: str) -> bool:
        with self._lock:
            m = self._models.get(model_id)
            if m is None:
                return False
            m.status = ModelStatus.DEPRECATED
            m.updated_at = time.time()
            return True

    def add_prompt_version(self, model_id: str, template: str,
                           variables: list[str], author: str,
                           change_note: str = "",
                           set_active: bool = False) -> PromptVersion | None:
        with self._lock:
            m = self._models.get(model_id)
            if m is None:
                return None
            version_num = len(m.prompt_versions) + 1
            pv = PromptVersion(
                version_id=uuid.uuid4().hex[:12],
                version=version_num,
                template=template,
                variables=variables,
                author=author,
                change_note=change_note,
            )
            if set_active:
                for existing in m.prompt_versions:
                    existing.is_active = False
                pv.is_active = True
            m.prompt_versions.append(pv)
            m.updated_at = time.time()
            return pv

    def set_active_prompt(self, model_id: str, version: int) -> bool:
        with self._lock:
            m = self._models.get(model_id)
            if m is None:
                return False
            found = False
            for pv in m.prompt_versions:
                if pv.version == version:
                    pv.is_active = True
                    found = True
                else:
                    pv.is_active = False
            return found

    def add_guardrail(self, model_id: str, name: str, description: str,
                      check_type: str,
                      action: GuardrailAction = GuardrailAction.BLOCK,
                      parameters: dict[str, Any] | None = None) -> Guardrail | None:
        with self._lock:
            m = self._models.get(model_id)
            if m is None:
                return None
            g = Guardrail(
                guardrail_id=uuid.uuid4().hex[:12],
                name=name,
                description=description,
                check_type=check_type,
                action=action,
                parameters=parameters or {},
            )
            m.guardrails.append(g)
            m.updated_at = time.time()
            return g

    def check_guardrails(self, model_id: str,
                         input_text: str) -> list[GuardrailResult]:
        with self._lock:
            m = self._models.get(model_id)
            if m is None:
                return []
            guardrails = [g for g in m.guardrails if g.enabled]

        results = []
        for g in guardrails:
            passed = True
            message = ""

            if g.check_type == "max_length":
                max_len = g.parameters.get("max_length", 10000)
                if len(input_text) > max_len:
                    passed = False
                    message = f"Input exceeds maximum length of {max_len}"
            elif g.check_type == "blocked_words":
                blocked = g.parameters.get("words", [])
                input_lower = input_text.lower()
                found = [w for w in blocked if w.lower() in input_lower]
                if found:
                    passed = False
                    message = f"Input contains blocked words: {found}"
            elif g.check_type == "min_length":
                min_len = g.parameters.get("min_length", 1)
                if len(input_text.strip()) < min_len:
                    passed = False
                    message = f"Input below minimum length of {min_len}"

            if not passed:
                with self._lock:
                    g.triggered_count += 1

            results.append(GuardrailResult(
                guardrail_id=g.guardrail_id,
                passed=passed,
                action=g.action,
                message=message,
            ))

        return results

    def record_invocation(self, model_id: str, latency_ms: float,
                          tokens: int = 0, error: bool = False,
                          quality_score: float | None = None) -> bool:
        with self._lock:
            m = self._models.get(model_id)
            if m is None:
                return False
            m.total_invocations += 1
            m.total_latency_ms += latency_ms
            m.total_tokens += tokens
            if error:
                m.total_errors += 1

            active = m.active_prompt
            if active:
                n = active.total_invocations
                active.avg_latency_ms = (active.avg_latency_ms * n + latency_ms) / (n + 1)
                if quality_score is not None:
                    active.avg_quality_score = (
                        (active.avg_quality_score * n + quality_score) / (n + 1)
                    )
                active.total_invocations += 1

            return True

    def list_models(self, status: ModelStatus | None = None,
                    model_type: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            models = list(self._models.values())
        results = []
        for m in models:
            if status and m.status != status:
                continue
            if model_type and m.model_type != model_type:
                continue
            results.append(m.to_dict())
        return results

    def stats(self) -> dict[str, Any]:
        with self._lock:
            total_invocations = sum(m.total_invocations for m in self._models.values())
            total_errors = sum(m.total_errors for m in self._models.values())
            by_status: dict[str, int] = {}
            by_type: dict[str, int] = {}
            for m in self._models.values():
                by_status[m.status.value] = by_status.get(m.status.value, 0) + 1
                by_type[m.model_type] = by_type.get(m.model_type, 0) + 1
            return {
                "total_models": len(self._models),
                "total_invocations": total_invocations,
                "total_errors": total_errors,
                "overall_error_rate": round(total_errors / max(total_invocations, 1), 4),
                "by_status": by_status,
                "by_type": by_type,
                "total_guardrails": sum(len(m.guardrails) for m in self._models.values()),
                "total_prompt_versions": sum(len(m.prompt_versions) for m in self._models.values()),
            }


_INSTANCE: ModelRegistry | None = None
_LOCK = threading.Lock()


def get_model_registry() -> ModelRegistry:
    global _INSTANCE
    if _INSTANCE is None:
        with _LOCK:
            if _INSTANCE is None:
                _INSTANCE = ModelRegistry()
    return _INSTANCE
