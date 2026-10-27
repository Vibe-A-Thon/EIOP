"""Model Provider Port (SR-LLM-001, SR-LLM-002, SR-LLM-004, SR-LLM-008).

One port in core for every model capability (decision D-SR-LLM-001-01):

* ``ModelPort`` - adapters declare capabilities; requests are negotiated against them (context
  length, modalities, tools, determinism) before any call (SR-LLM-001). Structured output is
  validated against the request's JSON Schema.
* Local by default (SR-LLM-002): adapters for local runtime classes register active; an external
  adapter stays inactive until an authorized tenant administrator enables it AND its egress
  gateway endpoint is enabled, and every external call goes through the egress gateway.
* ``TaskRouter`` (SR-LLM-004): small models for classification/extraction/routing, large models
  for synthesis, ordered fallbacks, per-tenant circuit breakers (reusing SR-TEN-006) and per-tenant
  model allowlists.
* ``LLMTelemetry`` (SR-LLM-008): latency, tokens, cost, cache hits, refusals, guardrail triggers and
  quality per call, kept locally; export only for tenants that opted in.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from eoip.tenancy.quotas import CircuitOpen, TenantCircuitBreaker


class Capability(str, Enum):
    CHAT = "chat"
    STRUCTURED_OUTPUT = "structured_output"
    TOOL_CALLING = "tool_calling"
    EMBEDDINGS = "embeddings"
    RERANK = "rerank"
    VISION_OCR = "vision_ocr"
    SPEECH = "speech"


#: Local/self-hosted runtime classes (SR-LLM-002).
LOCAL_RUNTIMES = frozenset({"vllm", "sglang", "llama_cpp", "ollama", "tgi", "onnxruntime", "openvino",
                            "tensorrt_llm"})
SMALL_TASKS = frozenset({"classification", "extraction", "routing"})
LARGE_TASKS = frozenset({"synthesis", "summarization", "answer"})


class CapabilityMismatch(ValueError):
    """The request needs something the adapter did not declare (SR-LLM-001)."""


class AdapterInactive(PermissionError):
    pass


class StructuredOutputInvalid(ValueError):
    pass


class NoModelAvailable(RuntimeError):
    pass


@dataclass(frozen=True)
class ModelCapabilities:
    capabilities: frozenset[Capability]
    context_length: int
    modalities: frozenset[str] = frozenset({"text"})
    supports_tools: bool = False
    deterministic: bool = False  # temperature-0 / seeded decoding is reproducible
    size_class: str = "small"  # small | large


@dataclass
class ModelRequest:
    task: str
    capability: Capability
    input: Any
    tenant_id: str = "_platform"
    input_tokens: int = 0
    modalities: frozenset[str] = frozenset({"text"})
    tools: tuple[str, ...] = ()
    json_schema: dict[str, Any] | None = None
    require_determinism: bool = False
    max_tokens: int = 512


@dataclass
class ModelResult:
    output: Any
    adapter: str
    tokens_in: int = 0
    tokens_out: int = 0
    cost: float = 0.0
    refused: bool = False
    cache_hit: bool = False
    quality_score: float | None = None
    guardrail_triggers: list[str] = field(default_factory=list)
    notice: str | None = None  # visible to the user, e.g. local fallback after an egress outage (SR-LLM-019)


@dataclass
class ModelAdapter:
    """A model runtime behind the port. ``invoke(request) -> ModelResult``."""

    name: str
    runtime: str
    caps: ModelCapabilities
    invoke: Callable[[ModelRequest], ModelResult]
    egress_endpoint_id: str | None = None  # required for external adapters

    @property
    def local(self) -> bool:
        return self.runtime in LOCAL_RUNTIMES


def negotiate(request: ModelRequest, caps: ModelCapabilities) -> None:
    """Raise ``CapabilityMismatch`` naming every unmet need (SR-LLM-001)."""
    problems = []
    if request.capability not in caps.capabilities:
        problems.append(f"capability {request.capability.value}")
    if request.json_schema is not None and Capability.STRUCTURED_OUTPUT not in caps.capabilities:
        problems.append("structured output")
    if request.input_tokens + request.max_tokens > caps.context_length:
        problems.append(f"context length {request.input_tokens + request.max_tokens} > {caps.context_length}")
    missing_modalities = set(request.modalities) - set(caps.modalities)
    if missing_modalities:
        problems.append("modalities " + ",".join(sorted(missing_modalities)))
    if request.tools and not caps.supports_tools:
        problems.append("tools")
    if request.require_determinism and not caps.deterministic:
        problems.append("determinism")
    if problems:
        raise CapabilityMismatch("; ".join(problems))


class LLMTelemetry:
    """Per-call LLM telemetry kept locally (SR-LLM-008)."""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self._export_enabled: dict[str, str] = {}  # tenant -> admin who enabled

    def record(self, *, tenant_id: str, adapter: str, task: str, latency_ms: float, result: ModelResult) -> dict:
        rec = {"tenant_id": tenant_id, "adapter": adapter, "task": task, "latency_ms": round(latency_ms, 3),
               "tokens_in": result.tokens_in, "tokens_out": result.tokens_out, "cost": result.cost,
               "cache_hit": result.cache_hit, "refused": result.refused,
               "guardrail_triggers": list(result.guardrail_triggers), "quality_score": result.quality_score,
               "at": time.time()}
        self.calls.append(rec)
        return rec

    def summary(self, tenant_id: str) -> dict[str, Any]:
        calls = [c for c in self.calls if c["tenant_id"] == tenant_id]
        n = len(calls) or 1
        return {"calls": len(calls), "avg_latency_ms": sum(c["latency_ms"] for c in calls) / n,
                "tokens_in": sum(c["tokens_in"] for c in calls), "tokens_out": sum(c["tokens_out"] for c in calls),
                "cost": round(sum(c["cost"] for c in calls), 6), "cache_hits": sum(c["cache_hit"] for c in calls),
                "refusals": sum(c["refused"] for c in calls),
                "guardrail_triggers": sum(len(c["guardrail_triggers"]) for c in calls)}

    def enable_export(self, tenant_id: str, *, admin: str) -> None:
        if not admin:
            raise PermissionError("an administrator must enable telemetry export")
        self._export_enabled[tenant_id] = admin

    def export(self, tenant_id: str) -> list[dict[str, Any]]:
        """Telemetry leaves the platform only for tenants that opted in (local-only default)."""
        if tenant_id not in self._export_enabled:
            raise PermissionError(f"telemetry export is not enabled for tenant {tenant_id}")
        return [dict(c) for c in self.calls if c["tenant_id"] == tenant_id]


class ModelPort:
    """Registry + invocation path for every model capability."""

    def __init__(self, *, egress_gateway: Any = None, telemetry: LLMTelemetry | None = None,
                 guardrails: Any = None, clock: Callable[[], float] = time.monotonic) -> None:
        self.adapters: dict[str, ModelAdapter] = {}
        self.active: set[str] = set()
        self.egress = egress_gateway
        self.telemetry = telemetry or LLMTelemetry()
        self.guardrails = guardrails
        self._clock = clock
        self._cache: dict[str, ModelResult] = {}
        self.audit: list[dict[str, Any]] = []

    def register(self, adapter: ModelAdapter) -> None:
        if adapter.name in self.adapters:
            raise ValueError(f"duplicate adapter {adapter.name}")
        if not adapter.local and not adapter.egress_endpoint_id:
            raise ValueError("an external adapter must name its egress gateway endpoint")
        self.adapters[adapter.name] = adapter
        if adapter.local:
            self.active.add(adapter.name)  # local/self-hosted by default

    def enable_external(self, name: str, *, admin: str, admin_roles: set[str]) -> None:
        """Only an authorized tenant administrator can activate an external adapter (SR-LLM-002)."""
        adapter = self.adapters[name]
        if adapter.local:
            return
        if not admin or "tenant_admin" not in admin_roles:
            raise PermissionError("only a tenant administrator can enable an external model provider")
        endpoint = (getattr(self.egress, "endpoints", {}) or {}).get(adapter.egress_endpoint_id)
        if endpoint is None or not getattr(endpoint, "enabled", False):
            raise PermissionError("the adapter's egress endpoint is not enabled in the egress gateway")
        self.active.add(name)
        self.audit.append({"event": "model.external_enabled", "adapter": name, "admin": admin})

    def invoke(self, adapter_name: str, request: ModelRequest) -> ModelResult:
        adapter = self.adapters[adapter_name]
        if adapter_name not in self.active:
            raise AdapterInactive(f"adapter {adapter_name} is not enabled")
        negotiate(request, adapter.caps)
        triggers: list[str] = []
        if self.guardrails is not None:
            triggers += self.guardrails.check_input(request)
        cache_key = None
        if request.require_determinism or adapter.caps.deterministic:
            cache_key = hashlib.sha256(json.dumps(
                [adapter_name, request.task, request.capability.value, request.input, request.json_schema],
                sort_keys=True, default=str).encode()).hexdigest()
        started = self._clock()
        if cache_key and cache_key in self._cache:
            cached = self._cache[cache_key]
            result = ModelResult(**{**cached.__dict__, "cache_hit": True, "guardrail_triggers": list(triggers)})
        else:
            if adapter.local:
                result = adapter.invoke(request)
            else:
                result = self._via_egress(adapter, request)
            if request.json_schema is not None and not result.refused:
                import jsonschema

                err = next(jsonschema.Draft202012Validator(request.json_schema).iter_errors(result.output), None)
                if err is not None:
                    raise StructuredOutputInvalid(f"output does not match the requested schema: {err.message}")
            if self.guardrails is not None:
                result.output, out_triggers = self.guardrails.check_output(result.output)
                triggers += out_triggers
            result.guardrail_triggers = list(triggers)
            if cache_key:
                self._cache[cache_key] = result
        self.telemetry.record(tenant_id=request.tenant_id, adapter=adapter_name, task=request.task,
                              latency_ms=(self._clock() - started) * 1000, result=result)
        return result

    def _via_egress(self, adapter: ModelAdapter, request: ModelRequest) -> ModelResult:
        if self.egress is None:
            raise AdapterInactive("external adapters require the egress gateway")
        sent = self.egress.call(endpoint_id=adapter.egress_endpoint_id, task=request.task,
                                payload={"input": request.input}, user_id=f"model-port:{request.tenant_id}",
                                role="service", data_classes=["D0"])
        response = sent.get("response")
        return ModelResult(output=response, adapter=adapter.name,
                           guardrail_triggers=[f"egress:{f}" for f in sent.get("response_findings", [])])


class TaskRouter:
    """Task-based routing with fallbacks, per-tenant breakers and allowlists (SR-LLM-004)."""

    def __init__(self, port: ModelPort, *, breaker: TenantCircuitBreaker | None = None) -> None:
        self.port = port
        self.breaker = breaker or TenantCircuitBreaker(failure_threshold=2, cooldown_s=30.0)
        self.allowlists: dict[str, set[str]] = {}
        self.decisions: list[dict[str, Any]] = []
        #: task -> deterministic fallback used when no model can answer (SR-LLM-019)
        self.deterministic: dict[str, Callable[[ModelRequest], Any]] = {}

    def set_allowlist(self, tenant_id: str, adapters: set[str]) -> None:
        self.allowlists[tenant_id] = set(adapters)

    def candidates(self, request: ModelRequest) -> list[str]:
        wanted = "small" if request.task in SMALL_TASKS else "large" if request.task in LARGE_TASKS else None
        allowed = self.allowlists.get(request.tenant_id)
        names = sorted(n for n in self.port.active if allowed is None or n in allowed)
        usable = []
        for name in names:
            try:
                negotiate(request, self.port.adapters[name].caps)
            except CapabilityMismatch:
                continue
            usable.append(name)
        # preferred size class first; within a class local models before external ones (local by
        # default, SR-LLM-002); the rest are fallbacks in that order (SR-LLM-019)
        return sorted(usable, key=lambda n: (self.port.adapters[n].caps.size_class != wanted,
                                             not self.port.adapters[n].local, n))

    def route(self, request: ModelRequest) -> ModelResult:
        from eoip.egress.gateway import EgressDenied, EgressOutage
        from eoip.models.guardrails import GuardrailBlocked

        tried: list[tuple[str, str]] = []
        egress_problem: str | None = None
        for name in self.candidates(request):
            try:
                self.breaker.before_call(request.tenant_id, name)
            except CircuitOpen:
                tried.append((name, "circuit_open"))
                continue
            try:
                result = self.port.invoke(name, request)
            except (CapabilityMismatch, StructuredOutputInvalid, AdapterInactive, GuardrailBlocked):
                raise  # request problems, not model faults: no fallback, no breaker penalty
            except EgressOutage as exc:
                self.breaker.record_failure(request.tenant_id, name)
                tried.append((name, "egress_outage"))
                egress_problem = egress_problem or exc.fallback_notice
                continue
            except EgressDenied as exc:  # policy denial is not a runtime fault: no breaker penalty
                tried.append((name, "egress_denied"))
                egress_problem = egress_problem or exc.fallback_notice
                continue
            except Exception as exc:  # noqa: BLE001 - adapter failure -> breaker + next fallback
                self.breaker.record_failure(request.tenant_id, name)
                tried.append((name, type(exc).__name__))
                continue
            self.breaker.record_success(request.tenant_id, name)
            if egress_problem:
                result.notice = f"{egress_problem}; answered by local model {name}"
            self.decisions.append({"tenant_id": request.tenant_id, "task": request.task, "adapter": name,
                                   "fallbacks": tried, "notice": result.notice})
            return result
        if request.task in self.deterministic:
            result = ModelResult(output=self.deterministic[request.task](request), adapter="deterministic",
                                 notice=f"{egress_problem or 'no model available'}; answered in deterministic mode")
            self.decisions.append({"tenant_id": request.tenant_id, "task": request.task, "adapter": "deterministic",
                                   "fallbacks": tried, "notice": result.notice})
            return result
        raise NoModelAvailable(f"no model available for task {request.task!r} (tried {tried})")


# ---------------------------------------------------------------------------
# Local runtime adapters (SR-LLM-002)
# ---------------------------------------------------------------------------

#: Chat endpoint per local runtime class. vLLM, SGLang, llama.cpp server, TGI and TensorRT-LLM
#: (trtllm-serve) expose the OpenAI-compatible route; OpenVINO Model Server uses /v3; Ollama its own.
RUNTIME_CHAT_PATHS = {
    "vllm": "/v1/chat/completions", "sglang": "/v1/chat/completions", "llama_cpp": "/v1/chat/completions",
    "tgi": "/v1/chat/completions", "tensorrt_llm": "/v1/chat/completions",
    "openvino": "/v3/chat/completions", "ollama": "/api/chat",
}


def http_chat_adapter(name: str, runtime: str, *, url: str, model: str, caps: ModelCapabilities,
                      client_factory: Callable[[], Any] | None = None, timeout: float = 60.0) -> ModelAdapter:
    """Adapter for an HTTP-served local runtime. ``client_factory`` lets tests inject a transport.

    The endpoint URL is validated against the same local egress policy as
    ``LocalModelProvider`` (CC3-001): http/https only, no redirects, allowlisted hosts only.
    """
    if runtime not in RUNTIME_CHAT_PATHS:
        raise ValueError(f"no HTTP chat route for runtime {runtime!r}")
    from eoip.models.provider import validate_model_endpoint_url

    validate_model_endpoint_url(url)
    import httpx

    path = RUNTIME_CHAT_PATHS[runtime]
    factory = client_factory or (lambda: httpx.Client(timeout=timeout, trust_env=False))

    def invoke(request: ModelRequest) -> ModelResult:
        messages = request.input if isinstance(request.input, list) else [{"role": "user", "content": str(request.input)}]
        body: dict[str, Any] = {"model": model, "messages": messages, "stream": False}
        if runtime == "ollama":
            body["options"] = {"temperature": 0, "num_predict": request.max_tokens}
        else:
            body.update(temperature=0, max_tokens=request.max_tokens)
            if request.json_schema is not None:
                body["response_format"] = {"type": "json_schema",
                                           "json_schema": {"name": "output", "schema": request.json_schema}}
        with factory() as client:
            resp = client.post(f"{url}{path}", json=body)
            resp.raise_for_status()
            data = resp.json()
        if runtime == "ollama":
            content, t_in, t_out = data["message"]["content"], data.get("prompt_eval_count", 0), data.get("eval_count", 0)
        else:
            content = data["choices"][0]["message"]["content"]
            usage = data.get("usage") or {}
            t_in, t_out = usage.get("prompt_tokens", 0), usage.get("completion_tokens", 0)
        output: Any = content
        if request.json_schema is not None:
            output = json.loads(content)
        return ModelResult(output=output, adapter=name, tokens_in=t_in or 0, tokens_out=t_out or 0)

    return ModelAdapter(name=name, runtime=runtime, caps=caps, invoke=invoke)


def in_process_adapter(name: str, runtime: str, fn: Callable[[ModelRequest], Any], *,
                       caps: ModelCapabilities) -> ModelAdapter:
    """Adapter for an in-process runtime (ONNX Runtime GenAI, OpenVINO GenAI, llama.cpp bindings)."""
    if runtime not in LOCAL_RUNTIMES:
        raise ValueError(f"{runtime!r} is not a local runtime class")

    def invoke(request: ModelRequest) -> ModelResult:
        out = fn(request)
        return out if isinstance(out, ModelResult) else ModelResult(output=out, adapter=name)

    return ModelAdapter(name=name, runtime=runtime, caps=caps, invoke=invoke)


# ---------------------------------------------------------------------------
# Existing callers (NLQ planning, GraphRAG synthesis) go through the port
# ---------------------------------------------------------------------------

#: Process-wide telemetry for every model call made through ``generate_via_port`` (SR-LLM-008).
DEFAULT_TELEMETRY = LLMTelemetry()


def _default_guardrails() -> Any:
    from eoip.models.guardrails import Guardrails

    # Default deployment is local-only: PII never leaves the tenant, so it is not redacted;
    # injection/jailbreak input and secrets are still blocked and active output neutralised.
    return Guardrails(redact_pii=False)


def provider_adapter(provider: Any, *, name: str = "local-model", context_length: int = 32768) -> ModelAdapter:
    """Wrap a ``LocalModelProvider``-style object (``generate(system, user, max_tokens=)``)."""

    def invoke(request: ModelRequest) -> ModelResult:
        resp = provider.generate(request.input["system"], request.input["user"], max_tokens=request.max_tokens)
        return ModelResult(output=resp.content, adapter=name, tokens_out=getattr(resp, "tokens_used", None) or 0)

    caps = ModelCapabilities(capabilities=frozenset({Capability.CHAT}), context_length=context_length,
                             deterministic=True, size_class="small")
    return ModelAdapter(name=name, runtime="ollama", caps=caps, invoke=invoke)


def generate_via_port(provider: Any, *, task: str, system_prompt: str, user_content: str,
                      max_tokens: int = 512, tenant_id: str = "_platform") -> ModelResult:
    """Run one generation through ModelPort + TaskRouter: guardrails, telemetry, fallback handling.

    Raises ``ModelUnavailable`` when the model is not configured, every route failed, or a guardrail
    blocked the input - callers keep their deterministic path in all three cases.
    """
    from eoip.models.guardrails import GuardrailBlocked
    from eoip.models.provider import ModelUnavailable

    if not getattr(provider, "available", False):
        raise ModelUnavailable("No local model is configured")
    port = ModelPort(telemetry=DEFAULT_TELEMETRY, guardrails=_default_guardrails())
    port.register(provider_adapter(provider))
    request = ModelRequest(task=task, capability=Capability.CHAT, tenant_id=tenant_id,
                           input={"system": system_prompt, "user": user_content},
                           input_tokens=(len(system_prompt) + len(user_content)) // 4, max_tokens=max_tokens)
    try:
        return TaskRouter(port).route(request)
    except GuardrailBlocked as exc:
        raise ModelUnavailable(f"guardrail blocked the model input: {exc}") from exc
    except NoModelAvailable as exc:
        raise ModelUnavailable(str(exc)) from exc
