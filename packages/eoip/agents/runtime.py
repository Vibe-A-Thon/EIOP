"""Governed Deep Agent runtime with bounded execution and replayable XAI traces."""

from __future__ import annotations

import concurrent.futures
import logging
from collections import defaultdict
from time import monotonic
from typing import Protocol
from uuid import uuid4

import httpx
from eoip.agents.firewall import KnowledgeFirewall
from eoip.agents.memory import (
    AgentResultCache,
    FileMemoryStore,
    MemoryPolicyError,
    MemoryStorageError,
    MemoryStore,
)
from eoip.agents.proposals import ProposalStore
from eoip.agents.tools import ToolRegistry, build_graph_tool_registry
from eoip.agents.trace import AgentTraceStore
from eoip.contracts.agent import (
    AgentBudgets,
    AgentContract,
    AgentExecutionTrace,
    AgentPhase,
    AgentRequest,
    AgentResult,
    AgentTraceEvent,
    ExplanationEnvelope,
    RuleDecision,
)
from eoip.contracts.memory import MemoryRecord
from eoip.contracts.source_event import utc_now_iso
from eoip.contracts.tool import ToolRequest, ToolResult
from eoip.graph.store import GraphStore

log = logging.getLogger("eoip.agents")

READ_TOOLS = frozenset({
    "search", "entity", "path", "impact", "lineage", "quality",
    "ontology", "connector_status", "evidence", "similarity", "community",
    "anomaly", "test_coverage", "incident_correlation",
})


class Agent(Protocol):
    agent_id: str
    allowed_tools: frozenset[str]
    max_steps: int
    max_seconds: float

    def execute(self, request: AgentRequest, store: GraphStore) -> AgentResult: ...


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, Agent] = {}
        self._contracts: dict[str, AgentContract] = {}

    def register(self, agent: Agent, contract: AgentContract | None = None) -> None:
        allowed = frozenset(agent.allowed_tools)
        if not allowed.issubset(READ_TOOLS):
            forbidden = allowed - READ_TOOLS
            raise ValueError(f"Agent registers non-read tools: {sorted(forbidden)}")
        contract = contract or AgentContract(
            agent_id=agent.agent_id,
            purpose=(agent.__class__.__doc__ or f"Execute {agent.agent_id}").strip(),
            capabilities=[agent.agent_id],
            allowed_tools=sorted(allowed),
            budgets=AgentBudgets(max_steps=agent.max_steps, max_seconds=agent.max_seconds),
        )
        if contract.agent_id != agent.agent_id:
            raise ValueError("Agent id must match its contract")
        if set(contract.allowed_tools) != set(allowed):
            raise ValueError("Agent tools must match its contract")
        self._agents[agent.agent_id] = agent
        self._contracts[agent.agent_id] = contract

    def get(self, agent_id: str) -> Agent | None:
        return self._agents.get(agent_id)

    def get_contract(self, agent_id: str) -> AgentContract | None:
        return self._contracts.get(agent_id)

    def list_agents(self) -> list[str]:
        return sorted(self._agents)

    def list_contracts(self) -> list[AgentContract]:
        return [self._contracts[key] for key in sorted(self._contracts)]


class AgentExecutionContext:
    """Cooperative budget/capability boundary for context-aware agents."""

    def __init__(
        self,
        *,
        run_id: str,
        request: AgentRequest,
        contract: AgentContract,
        budgets: AgentBudgets,
        tools: ToolRegistry,
        deadline: float,
        emit,
        memory_store: MemoryStore | None = None,
    ) -> None:
        self.run_id = run_id
        self.request = request
        self.contract = contract
        self.budgets = budgets
        self._tools = tools
        self._deadline = deadline
        self._emit = emit
        self._memory_store = memory_store
        self.tool_calls: list[dict] = []

    def recall_task(self, run_id: str) -> MemoryRecord | None:
        if self.contract.memory_policy != "APPROVED" or self._memory_store is None:
            raise PermissionError("Persistent task memory is not approved for this agent")
        if self.remaining_seconds <= 0:
            raise TimeoutError("Agent run deadline exceeded")
        if len(self.tool_calls) >= self.budgets.max_tool_calls:
            raise RuntimeError("Tool-call budget exhausted")
        call = {
            "tool_call_id": str(uuid4()), "tool_name": "task_memory",
            "status": "FAILED", "evidence_refs": [],
        }
        self.tool_calls.append(call)
        try:
            record = self._memory_store.get(
                run_id, scope=f"agent:{self.contract.agent_id}", owner=self.request.actor_id,
            )
        except (MemoryPolicyError, MemoryStorageError):
            self._emit("OBSERVE", "FAILED", "Scoped task memory lookup failed")
            raise
        call.update({
            "status": "SUCCEEDED" if record else "NOT_FOUND",
            "evidence_refs": record.provenance_refs if record else [],
        })
        self._emit("OBSERVE", "SUCCEEDED", "Scoped task memory lookup completed")
        return record

    @property
    def remaining_seconds(self) -> float:
        return max(0.0, self._deadline - monotonic())

    def use_tool(self, name: str, arguments: dict) -> ToolResult:
        if len(self.tool_calls) >= self.budgets.max_tool_calls:
            raise RuntimeError("Tool-call budget exhausted")
        if self.remaining_seconds <= 0:
            raise TimeoutError("Agent run deadline exceeded")
        call_id = str(uuid4())
        result = self._tools.invoke(
            ToolRequest(
                tool_call_id=call_id,
                tool_name=name,
                arguments=arguments,
                actor_id=self.request.actor_id,
                tenant_id=self.request.tenant_id,
                run_id=self.run_id,
                dry_run=self.request.dry_run,
            ),
            allowed_tools=set(self.contract.allowed_tools),
            remaining_seconds=self.remaining_seconds,
        )
        record = {
            "tool_call_id": call_id,
            "tool_name": name,
            "tenant_id": self.request.tenant_id,
            "status": result.status,
            "risk_level": (self._tools.get(name).risk_level if self._tools.get(name) else "R0"),
            "duration_ms": result.duration_ms,
            "evidence_refs": result.evidence_refs or [],
            "arguments_digest": self._tools.arguments_digest(arguments),
            "error_code": (result.error or {}).get("code"),
        }
        self.tool_calls.append(record)
        self._emit("OBSERVE", result.status, f"Tool {name} returned {result.status}", result.evidence_refs or [])
        return result


class ReadOnlyGraphStore:
    """Capability boundary for deterministic agents using the legacy store interface."""

    _READ_METHODS = frozenset({
        "health", "ping", "schema_status", "get_vertex", "get_vertex_by_canonical_id",
        "find_vertex_by_property", "find_vertices", "count_vertices", "get_edge",
        "find_edge_by_key", "find_edges", "edges_from", "edges_to", "count_edges",
    })

    def __init__(self, store: GraphStore, max_items: int) -> None:
        self._store = store
        self._max_items = max_items

    def __getattr__(self, name: str):
        if name not in self._READ_METHODS:
            raise PermissionError(f"Agent graph capability denied: {name}")
        method = getattr(self._store, name)

        def bounded(*args, **kwargs):
            if "limit" in kwargs:
                kwargs["limit"] = min(int(kwargs["limit"]), self._max_items)
            return method(*args, **kwargs)

        return bounded


class AgentRuntime:
    def __init__(
        self,
        store: GraphStore,
        registry: AgentRegistry,
        *,
        tools: ToolRegistry | None = None,
        trace_store: AgentTraceStore | None = None,
        firewall: KnowledgeFirewall | None = None,
        proposal_store: ProposalStore | None = None,
        failure_threshold: int = 3,
        memory_store: MemoryStore | None = None,
        result_cache: AgentResultCache | None = None,
    ) -> None:
        self._store = store
        self._registry = registry
        self._tools = tools or build_graph_tool_registry(store)
        self._trace_store = trace_store or AgentTraceStore()
        self._firewall = firewall or KnowledgeFirewall()
        self._proposal_store = proposal_store or ProposalStore()
        self._failures: defaultdict[str, int] = defaultdict(int)
        self._failure_threshold = failure_threshold
        self._memory_store = memory_store or FileMemoryStore()
        self._results = result_cache or AgentResultCache(policy=self._memory_store.policy)

    @property
    def registry(self) -> AgentRegistry:
        return self._registry

    @property
    def trace_store(self) -> AgentTraceStore:
        return self._trace_store

    @property
    def proposal_store(self) -> ProposalStore:
        return self._proposal_store

    @property
    def memory_store(self) -> MemoryStore:
        return self._memory_store

    def get_memory(self, run_id: str) -> MemoryRecord | None:
        trace = self._trace_store.get(run_id)
        if trace is None:
            return None
        contract = self._registry.get_contract(trace.agent_id)
        if contract is None or not contract.enabled or contract.memory_policy != "APPROVED":
            return None
        return self._memory_store.get(
            run_id, scope=f"agent:{trace.agent_id}", owner=trace.actor_id,
        )

    def get_result(self, run_id: str) -> AgentResult | None:
        return self._results.get(run_id)

    def run(self, request: AgentRequest) -> AgentResult:
        agent = self._registry.get(request.agent_id)
        contract = self._registry.get_contract(request.agent_id)
        if agent is None or contract is None:
            return self._denied(request, f"Unknown agent: {request.agent_id}")
        if not contract.enabled:
            return self._denied(request, f"Agent is disabled: {request.agent_id}")
        if self._failures[request.agent_id] >= self._failure_threshold:
            return self._denied(request, f"Circuit breaker is open for {request.agent_id}")

        run_id = request.request_id
        correlation_id = request.correlation_id or request.request_id
        events: list[AgentTraceEvent] = []

        def emit(
            phase: AgentPhase,
            status: str,
            summary: str,
            evidence_refs: list[str] | None = None,
            metadata: dict | None = None,
        ) -> None:
            events.append(AgentTraceEvent(
                sequence=len(events),
                phase=phase,
                occurred_at=utc_now_iso(),
                status=status,
                summary=summary,
                evidence_refs=evidence_refs or [],
                metadata=metadata or {},
            ))

        emit("RECEIVE", "SUCCEEDED", "Request accepted by governed runtime")
        try:
            budgets = self._clamped_budgets(request, contract)
        except (TypeError, ValueError):
            emit("VALIDATE", "DENIED", "Invalid execution budget")
            result = self._denied(request, "Invalid execution budget", run_id=run_id)
            return self._finish(request, contract, result, events, 0.0)
        if request.recursion_depth > budgets.max_recursion:
            emit("VALIDATE", "DENIED", "Recursion budget exceeded")
            result = self._denied(request, "Recursion budget exceeded", run_id=run_id)
            return self._finish(request, contract, result, events, 0.0)

        request = request.model_copy(update={
            "correlation_id": correlation_id,
            "budgets": {**(request.budgets or {}), **budgets.model_dump()},
        })
        firewall = self._firewall.inspect(request.goal)
        request = request.model_copy(update={"goal": firewall.content})
        emit("CONTEXT", "SUCCEEDED", "Context passed through knowledge firewall", metadata={
            "rule_decisions": [item.model_dump() for item in firewall.decisions],
        })
        emit("PLAN", "SUCCEEDED", "Bounded execution plan selected", metadata={
            "max_steps": budgets.max_steps,
            "max_tool_calls": budgets.max_tool_calls,
            "max_seconds": budgets.max_seconds,
        })
        emit("VALIDATE", "SUCCEEDED", "Contract, capabilities, and budgets validated")

        start = monotonic()
        context = AgentExecutionContext(
            run_id=run_id,
            request=request,
            contract=contract,
            budgets=budgets,
            tools=self._tools,
            deadline=start + budgets.max_seconds,
            emit=emit,
            memory_store=self._memory_store,
        )
        emit("EXECUTE", "STARTED", f"Executing {request.agent_id}")
        result = self._execute_bounded(agent, request, context, budgets.max_seconds)
        elapsed = monotonic() - start

        if context.tool_calls:
            result = result.model_copy(update={"tool_calls": context.tool_calls})
        elif result.tool_calls:
            result = result.model_copy(update={
                "tool_calls": [self._sanitize_legacy_tool_call(item) for item in result.tool_calls]
            })
        warnings = list(result.warnings or [])
        if result.tool_calls and len(result.tool_calls) > budgets.max_steps:
            warnings.append(f"Execution exceeded step budget ({len(result.tool_calls)} > {budgets.max_steps})")
            result = result.model_copy(update={"status": "PARTIAL", "warnings": warnings})

        if result.status in {"FAILED", "CANCELLED"}:
            self._failures[request.agent_id] += 1
        else:
            self._failures[request.agent_id] = 0
        emit("EVALUATE", result.status, "Execution outcome evaluated", result.evidence_refs)
        explanation = result.explanation or self._explain(result, firewall.decisions)
        emit(
            "EXPLAIN",
            "SUCCEEDED",
            "Evidence-linked explanation produced",
            result.evidence_refs,
            {"explanation": explanation.model_dump()},
        )
        result = result.model_copy(update={
            "run_id": run_id,
            "explanation": explanation,
        })
        for proposal in result.proposals:
            self._proposal_store.create(proposal)
        return self._finish(request, contract, result, events, elapsed)

    def _execute_bounded(
        self,
        agent: Agent,
        request: AgentRequest,
        context: AgentExecutionContext,
        max_seconds: float,
    ) -> AgentResult:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        execute_context = getattr(agent, "execute_context", None)
        future = executor.submit(
            execute_context if execute_context is not None else agent.execute,
            request,
            context if execute_context is not None else ReadOnlyGraphStore(
                self._store, context.budgets.max_context_items
            ),
        )
        try:
            return future.result(timeout=max_seconds)
        except concurrent.futures.TimeoutError:
            future.cancel()
            return AgentResult(
                request_id=request.request_id,
                status="CANCELLED",
                summary="Agent execution stopped at its time budget.",
                evidence_refs=[],
                warnings=["Execution time budget exceeded"],
            )
        except (
            httpx.HTTPError,
            OSError,
            PermissionError,
            RuntimeError,
            TimeoutError,
            TypeError,
            ValueError,
        ) as exc:
            log.error("agent.failed", extra={
                "event": "agent.failed",
                "agent_id": request.agent_id,
                "request_id": request.request_id,
                "error_type": type(exc).__name__,
            })
            return AgentResult(
                request_id=request.request_id,
                status="FAILED",
                summary=f"Agent execution failed: {type(exc).__name__}",
                evidence_refs=[],
                warnings=[str(exc)],
            )
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def _finish(
        self,
        request: AgentRequest,
        contract: AgentContract,
        result: AgentResult,
        events: list[AgentTraceEvent],
        elapsed: float,
    ) -> AgentResult:
        initial_result = result
        events.append(AgentTraceEvent(
            sequence=len(events), phase="AUDIT", occurred_at=utc_now_iso(),
            status="SUCCEEDED", summary="Run prepared for durable audit",
        ))
        events.append(AgentTraceEvent(
            sequence=len(events), phase="FINISH", occurred_at=utc_now_iso(),
            status=result.status, summary=result.summary, evidence_refs=result.evidence_refs,
        ))
        trace = AgentExecutionTrace(
            run_id=result.run_id or request.request_id,
            request_id=request.request_id,
            agent_id=request.agent_id,
            actor_id=request.actor_id,
            correlation_id=request.correlation_id or request.request_id,
            contract_version=contract.version,
            events=events,
            final_status=result.status,
        )
        persisted = self._persist_run(request, result, elapsed)
        try:
            self._trace_store.save(trace)
        except OSError as exc:
            log.error("agent.trace.persist_failed", extra={
                "event": "agent.trace.persist_failed", "error_type": type(exc).__name__,
                "correlation_id": trace.correlation_id,
            })
            persisted = False
        if not persisted:
            result = self._with_persistence_warning(result, "Agent run could not be persisted")
        if contract.memory_policy == "APPROVED" and result.status != "DENIED" and persisted:
            try:
                self._memory_store.put(MemoryRecord(
                    memory_id=result.run_id or request.request_id,
                    kind="TASK",
                    scope=f"agent:{contract.agent_id}",
                    owner=request.actor_id,
                    source=contract.agent_id,
                    ttl_seconds=request.metadata.get(
                        "memory_ttl_seconds", self._memory_store.policy.ttl_seconds,
                    ),
                    provenance_refs=[f"urn:eoip:agent:run:{result.run_id or request.request_id}"],
                    confidence=result.explanation.confidence if result.explanation else None,
                    classification="INTERNAL",
                    deletion_policy="DELETE_AT_EXPIRY",
                    content={"status": result.status, "evidence_count": len(result.evidence_refs)},
                ), correlation_id=request.correlation_id or request.request_id)
            except (MemoryPolicyError, MemoryStorageError, ValueError) as exc:
                log.error("agent.memory.persist_failed", extra={
                    "event": "agent.memory.persist_failed",
                    "correlation_id": request.correlation_id or request.request_id,
                    "error_type": type(exc).__name__,
                })
                result = self._with_persistence_warning(
                    result, f"Task memory could not be persisted ({type(exc).__name__})",
                )
        if result != initial_result:
            for index, event in enumerate(events):
                if event.phase == "EXPLAIN" and result.explanation is not None:
                    events[index] = event.model_copy(update={
                        "status": result.status,
                        "metadata": {**event.metadata, "explanation": result.explanation.model_dump()},
                    })
                elif event.phase == "FINISH":
                    events[index] = event.model_copy(update={"status": result.status})
            trace = trace.model_copy(update={"events": events, "final_status": result.status})
            refreshed = self._persist_run(request, result, elapsed) if persisted else False
            try:
                self._trace_store.save(trace)
            except OSError as exc:
                log.error("agent.trace.persist_failed", extra={
                    "event": "agent.trace.persist_failed", "error_type": type(exc).__name__,
                    "correlation_id": trace.correlation_id,
                })
                refreshed = False
            if persisted and not refreshed:
                result = self._with_persistence_warning(result, "Agent run could not be persisted")
        self._results.put(trace.run_id, result)
        return result

    def _with_persistence_warning(self, result: AgentResult, warning: str) -> AgentResult:
        updated = result.model_copy(update={
            "status": "PARTIAL" if result.status == "SUCCEEDED" else result.status,
            "warnings": [*(result.warnings or []), warning],
        })
        return updated.model_copy(update={
            "explanation": self._explain(
                updated, result.explanation.rule_decisions if result.explanation else [],
            ),
        })

    @staticmethod
    def _clamped_budgets(request: AgentRequest, contract: AgentContract) -> AgentBudgets:
        requested = request.budgets or {}
        configured = contract.budgets
        values = configured.model_dump()
        for key in values:
            if key in requested:
                values[key] = min(requested[key], values[key])
        return AgentBudgets.model_validate(values)

    @staticmethod
    def _explain(result: AgentResult, decisions: list[RuleDecision]) -> ExplanationEnvelope:
        confidence = None
        uncertainty = list(result.warnings or [])
        if result.status == "SUCCEEDED":
            confidence = 0.9 if result.evidence_refs else 0.6
        elif result.status == "PARTIAL":
            confidence = 0.5
        return ExplanationEnvelope(
            decision_summary=result.summary,
            evidence_refs=result.evidence_refs,
            rule_decisions=decisions,
            confidence=confidence,
            uncertainty=uncertainty,
        )

    def _sanitize_legacy_tool_call(self, item: dict) -> dict:
        name = str(item.get("tool_name") or item.get("tool") or "unknown")
        arguments = item.get("arguments") or item.get("input") or {}
        contract = self._tools.get(name)
        return {
            "tool_call_id": str(uuid4()),
            "tool_name": name,
            "status": "SUCCEEDED",
            "risk_level": contract.risk_level if contract else "R0",
            "duration_ms": 0,
            "evidence_refs": [],
            "arguments_digest": self._tools.arguments_digest(arguments),
            "error_code": None,
        }

    @staticmethod
    def _denied(request: AgentRequest, summary: str, *, run_id: str | None = None) -> AgentResult:
        return AgentResult(
            request_id=request.request_id,
            run_id=run_id,
            status="DENIED",
            summary=summary,
            evidence_refs=[],
            warnings=[summary],
            explanation=ExplanationEnvelope(
                decision_summary=summary,
                rule_decisions=[RuleDecision(
                    rule_id="AGENT-RUNTIME-DENY", outcome="DENY", summary=summary,
                )],
                uncertainty=["No agent action was executed."],
            ),
        )

    def _persist_run(self, request: AgentRequest, result: AgentResult, elapsed: float) -> bool:
        try:
            self._store.upsert_vertex("AgentRun", {
                "canonical_id": f"urn:eoip:agent:run:{result.run_id or request.request_id}",
                "agent_id": request.agent_id,
                "request_id": request.request_id,
                "actor_id": request.actor_id,
                "correlation_id": request.correlation_id or request.request_id,
                "goal": request.goal,
                "run_status": result.status,
                "started_at": utc_now_iso(),
                "finished_at": utc_now_iso(),
                "budgets": str({**(request.budgets or {}), "elapsed": round(elapsed, 3)}),
            })
        except (httpx.HTTPError, OSError, ValueError) as exc:
            log.error("agent.run.persist_failed", extra={
                "event": "agent.run.persist_failed",
                "agent_id": request.agent_id,
                "request_id": request.request_id,
                "error_type": type(exc).__name__,
            })
            return False
        return True
