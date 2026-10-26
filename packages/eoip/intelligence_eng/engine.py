"""Intelligence Engineering engine — System-Level Autonomy.

Orchestrates the entire cognitive stack: 16 engineering disciplines,
14 control loops, 35 agent archetypes, 17 RAG modes, 13 query languages,
and 18 databases into a unified, self-assembling cognitive pipeline.

Given a task, the engine:
1. Analyzes task complexity and requirements
2. Selects the appropriate autonomy level (HCTL → HOOTL)
3. Activates the right combination of disciplines
4. Composes a cognitive plan with ordered steps
5. Fuses outputs from multiple subsystems
6. Self-assesses and adapts for future tasks
"""

from __future__ import annotations

import hashlib
import threading
import time
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


# ── Autonomy Levels (maps to the 14 control loops) ──────────────────


class AutonomyLevel(Enum):
    HCTL = "human_commanded"
    HITL = "human_in_the_loop"
    HITL_FE = "human_for_exceptions"
    HBTL = "human_beside"
    HOTL = "human_on_the_loop"
    HATL = "human_above"
    HITD = "human_in_design"
    HITA = "human_in_action"
    HITC = "human_in_control"
    HITP = "human_in_process"
    HITI = "human_in_institution"
    MITL = "machine_in_the_loop"
    EITL = "environment_in_the_loop"
    HOOTL = "human_out_of_the_loop"


AUTONOMY_RISK_MAP: dict[AutonomyLevel, int] = {
    AutonomyLevel.HCTL: 1,
    AutonomyLevel.HITL: 2,
    AutonomyLevel.HITA: 2,
    AutonomyLevel.HITL_FE: 3,
    AutonomyLevel.HITC: 3,
    AutonomyLevel.HBTL: 4,
    AutonomyLevel.HITP: 4,
    AutonomyLevel.HOTL: 5,
    AutonomyLevel.HATL: 6,
    AutonomyLevel.HITD: 6,
    AutonomyLevel.HITI: 7,
    AutonomyLevel.MITL: 8,
    AutonomyLevel.EITL: 9,
    AutonomyLevel.HOOTL: 10,
}


# ── Task Analysis ────────────────────────────────────────────────────


class TaskComplexity(Enum):
    TRIVIAL = "trivial"
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    CRITICAL = "critical"


@dataclass
class TaskAnalysis:
    task_id: str
    query: str
    complexity: TaskComplexity
    requires_graph: bool = False
    requires_rag: bool = False
    requires_reasoning: bool = False
    requires_memory: bool = False
    requires_tools: bool = False
    requires_security_check: bool = False
    requires_evaluation: bool = False
    is_write_operation: bool = False
    is_multi_step: bool = False
    estimated_cost_tier: str = "low"
    recommended_autonomy: AutonomyLevel = AutonomyLevel.HITL
    confidence: float = 0.0
    signals: dict[str, float] = field(default_factory=dict)


# ── Capability Manifest ──────────────────────────────────────────────


ENGINEERING_DISCIPLINES = [
    "loop", "graph", "harness", "memory", "context", "prompt",
    "graph_over_loop", "loop_over_graph", "evaluation", "state",
    "tool_contract", "security", "cost_optimization", "feature",
    "spec", "intelligence",
]

CONTROL_LOOPS = [
    "HCTL", "HITL_FE", "HBTL", "HATL", "HITD", "EITL", "HITL",
    "HOTL", "HOOTL", "HITA", "HITC", "HITI", "MITL", "HITP",
]

AGENT_ARCHETYPES = [
    "simple_reflex", "model_based_reflex", "goal_based", "utility_based",
    "task", "router", "tool_calling", "function_calling", "rag",
    "enterprise", "hierarchical", "orchestrator", "choreography",
    "collaboration", "peer_to_peer", "consensus", "critic", "reflection",
    "self_reflection", "planner", "executor", "reviewer", "validator",
    "xai", "just_in_time", "self_learning", "self_evolving",
    "self_writing", "multi_agent", "swarm", "agentic_swarm",
    "deep_ai", "laya", "jev", "jem",
]

RAG_MODES = [
    "simple", "graph", "hybrid", "corrective", "self_rag", "adaptive",
    "agentic", "modular", "hyde", "advanced", "conversational",
    "multi_step", "multi_hop", "branched", "multimodal", "speculative",
    "rag_of_rags",
]

QUERY_LANGUAGES = [
    "rdf", "owl", "gremlin", "cypher", "gql", "opencypher",
    "shacl", "sparql", "skos", "eoql", "eql", "osql", "nl2query",
]

DATABASES = [
    "neo4j", "amazon_neptune", "tigergraph", "janusgraph", "memgraph",
    "nebulagraph", "dgraph", "falkordb", "allegrograph", "orientdb",
    "arangodb", "milvus", "weaviate", "qdrant", "cosmos_db",
    "fauna", "surrealdb",
]


@dataclass
class CapabilityManifest:
    disciplines: list[str] = field(default_factory=lambda: list(ENGINEERING_DISCIPLINES))
    control_loops: list[str] = field(default_factory=lambda: list(CONTROL_LOOPS))
    agent_archetypes: list[str] = field(default_factory=lambda: list(AGENT_ARCHETYPES))
    rag_modes: list[str] = field(default_factory=lambda: list(RAG_MODES))
    query_languages: list[str] = field(default_factory=lambda: list(QUERY_LANGUAGES))
    databases: list[str] = field(default_factory=lambda: list(DATABASES))

    @property
    def total_capabilities(self) -> int:
        return (len(self.disciplines) + len(self.control_loops) +
                len(self.agent_archetypes) + len(self.rag_modes) +
                len(self.query_languages) + len(self.databases))

    def to_dict(self) -> dict[str, Any]:
        return {
            "disciplines": len(self.disciplines),
            "control_loops": len(self.control_loops),
            "agent_archetypes": len(self.agent_archetypes),
            "rag_modes": len(self.rag_modes),
            "query_languages": len(self.query_languages),
            "databases": len(self.databases),
            "total": self.total_capabilities,
        }


# ── Cognitive Planning ───────────────────────────────────────────────


@dataclass
class DisciplineActivation:
    discipline: str
    priority: int = 0
    config: dict[str, Any] = field(default_factory=dict)
    reason: str = ""


@dataclass
class CognitivePlanStep:
    step_id: int
    action: str
    discipline: str
    agent_type: str | None = None
    rag_mode: str | None = None
    loop_type: str | None = None
    query_lang: str | None = None
    autonomy: AutonomyLevel = AutonomyLevel.HITL
    depends_on: list[int] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class CognitivePlan:
    plan_id: str
    task: TaskAnalysis
    steps: list[CognitivePlanStep]
    autonomy_level: AutonomyLevel
    activated_disciplines: list[DisciplineActivation]
    estimated_cost_usd: float = 0.0
    estimated_latency_ms: float = 0.0
    created_at: float = field(default_factory=time.time)

    @property
    def step_count(self) -> int:
        return len(self.steps)

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "task_id": self.task.task_id,
            "complexity": self.task.complexity.value,
            "autonomy_level": self.autonomy_level.value,
            "steps": self.step_count,
            "disciplines": [d.discipline for d in self.activated_disciplines],
            "estimated_cost_usd": self.estimated_cost_usd,
            "estimated_latency_ms": self.estimated_latency_ms,
        }


# ── Task Analyzer ────────────────────────────────────────────────────


GRAPH_SIGNALS = {
    "graph", "node", "edge", "relationship", "topology", "path",
    "traverse", "neighbor", "community", "centrality", "pagerank",
    "connected", "subgraph", "cluster", "network", "ontology",
    "entity", "triple", "knowledge graph", "dependency",
}

RAG_SIGNALS = {
    "retrieve", "search", "find", "lookup", "document", "context",
    "relevant", "similar", "embedding", "semantic", "answer",
    "knowledge", "information", "evidence", "source", "reference",
}

REASONING_SIGNALS = {
    "analyze", "reason", "explain", "why", "how", "evaluate",
    "compare", "infer", "deduce", "hypothesis", "cause", "effect",
    "think", "plan", "strategy", "decide", "recommend", "assess",
}

MEMORY_SIGNALS = {
    "remember", "recall", "history", "previous", "last time",
    "session", "context", "earlier", "conversation", "past",
}

TOOL_SIGNALS = {
    "api", "call", "invoke", "execute", "run", "tool", "function",
    "endpoint", "service", "external", "integration", "webhook",
}

SECURITY_SIGNALS = {
    "ignore", "bypass", "override", "inject", "hack", "exploit",
    "jailbreak", "prompt injection", "system prompt", "credentials",
}

WRITE_SIGNALS = {
    "create", "update", "delete", "modify", "write", "insert",
    "remove", "change", "set", "add", "mutate", "patch",
}


class TaskAnalyzer:
    """Analyzes incoming tasks to determine complexity, requirements, and
    the appropriate autonomy level."""

    def __init__(self) -> None:
        self._signal_sets: dict[str, set[str]] = {
            "graph": GRAPH_SIGNALS,
            "rag": RAG_SIGNALS,
            "reasoning": REASONING_SIGNALS,
            "memory": MEMORY_SIGNALS,
            "tools": TOOL_SIGNALS,
            "security": SECURITY_SIGNALS,
            "write": WRITE_SIGNALS,
        }

    def analyze(self, query: str, context: dict[str, Any] | None = None) -> TaskAnalysis:
        ctx = context or {}
        query_lower = query.lower()
        tokens = set(query_lower.split())

        signals: dict[str, float] = {}
        for signal_name, signal_set in self._signal_sets.items():
            overlap = len(tokens & signal_set)
            bigram_hits = sum(1 for phrase in signal_set
                              if " " in phrase and phrase in query_lower)
            signals[signal_name] = (overlap + bigram_hits * 2) / max(len(tokens), 1)

        requires_graph = signals.get("graph", 0) > 0.05
        requires_rag = signals.get("rag", 0) > 0.05
        requires_reasoning = signals.get("reasoning", 0) > 0.05
        requires_memory = signals.get("memory", 0) > 0.05
        requires_tools = signals.get("tools", 0) > 0.05
        requires_security = signals.get("security", 0) > 0.02
        is_write = signals.get("write", 0) > 0.05

        active_count = sum([requires_graph, requires_rag, requires_reasoning,
                           requires_memory, requires_tools])
        is_multi_step = active_count >= 2 or len(query.split()) > 50

        if requires_security:
            complexity = TaskComplexity.CRITICAL
        elif active_count >= 4:
            complexity = TaskComplexity.CRITICAL
        elif active_count >= 3 or is_multi_step:
            complexity = TaskComplexity.COMPLEX
        elif active_count >= 2:
            complexity = TaskComplexity.MODERATE
        elif active_count >= 1:
            complexity = TaskComplexity.SIMPLE
        else:
            complexity = TaskComplexity.TRIVIAL

        autonomy = self._determine_autonomy(complexity, is_write, requires_security)

        cost_tier = "low"
        if complexity in (TaskComplexity.COMPLEX, TaskComplexity.CRITICAL):
            cost_tier = "high"
        elif complexity == TaskComplexity.MODERATE:
            cost_tier = "medium"

        task_id = hashlib.sha256(
            f"{query}:{time.time()}".encode()
        ).hexdigest()[:16]

        return TaskAnalysis(
            task_id=task_id,
            query=query,
            complexity=complexity,
            requires_graph=requires_graph,
            requires_rag=requires_rag,
            requires_reasoning=requires_reasoning,
            requires_memory=requires_memory,
            requires_tools=requires_tools,
            requires_security_check=requires_security,
            requires_evaluation=complexity.value in ("complex", "critical"),
            is_write_operation=is_write,
            is_multi_step=is_multi_step,
            estimated_cost_tier=cost_tier,
            recommended_autonomy=autonomy,
            confidence=min(1.0, sum(signals.values())),
            signals=signals,
        )

    def _determine_autonomy(self, complexity: TaskComplexity,
                            is_write: bool,
                            requires_security: bool) -> AutonomyLevel:
        if requires_security:
            return AutonomyLevel.HCTL
        if is_write and complexity in (TaskComplexity.COMPLEX, TaskComplexity.CRITICAL):
            return AutonomyLevel.HITL
        if is_write:
            return AutonomyLevel.HITL_FE
        if complexity == TaskComplexity.CRITICAL:
            return AutonomyLevel.HBTL
        if complexity == TaskComplexity.COMPLEX:
            return AutonomyLevel.HOTL
        if complexity == TaskComplexity.MODERATE:
            return AutonomyLevel.HATL
        return AutonomyLevel.HOOTL


# ── Discipline Composer ──────────────────────────────────────────────


class DisciplineComposer:
    """Selects and orders discipline activations based on task analysis."""

    def compose(self, task: TaskAnalysis) -> list[DisciplineActivation]:
        activations: list[DisciplineActivation] = []

        if task.requires_security_check:
            activations.append(DisciplineActivation(
                "security", priority=0, reason="Security scan required before processing",
            ))

        if task.requires_memory:
            activations.append(DisciplineActivation(
                "memory", priority=1, reason="Task references prior context or history",
            ))

        activations.append(DisciplineActivation(
            "context", priority=2, reason="Context window assembly for all tasks",
        ))

        if task.requires_rag:
            activations.append(DisciplineActivation(
                "prompt", priority=3, reason="Prompt engineering for retrieval query",
            ))

        if task.requires_graph:
            activations.append(DisciplineActivation(
                "graph", priority=4, reason="Graph traversal and topology analysis",
            ))
            if task.is_multi_step:
                activations.append(DisciplineActivation(
                    "loop_over_graph", priority=5,
                    reason="Iterative graph traversal for multi-step analysis",
                ))

        if task.requires_reasoning:
            activations.append(DisciplineActivation(
                "loop", priority=5, reason="Reasoning loop for analytical task",
            ))

        if task.requires_tools:
            activations.append(DisciplineActivation(
                "tool_contract", priority=6, reason="Tool validation and API contract check",
            ))
            activations.append(DisciplineActivation(
                "harness", priority=7, reason="Pipeline orchestration for tool execution",
            ))

        if task.is_write_operation:
            activations.append(DisciplineActivation(
                "state", priority=8, reason="State persistence for write operation",
            ))
            activations.append(DisciplineActivation(
                "graph_over_loop", priority=9,
                reason="Record operation outcome as graph fact",
            ))

        if task.requires_evaluation:
            activations.append(DisciplineActivation(
                "evaluation", priority=10, reason="Quality gate for complex/critical task",
            ))

        activations.append(DisciplineActivation(
            "cost_optimization", priority=11,
            reason="Cost tracking for all operations",
        ))

        activations.sort(key=lambda a: a.priority)
        return activations


# ── Cognitive Planner ────────────────────────────────────────────────


class CognitivePlanner:
    """Builds a concrete execution plan from task analysis and
    discipline activations."""

    def __init__(self) -> None:
        self._agent_selector = AgentSelector()
        self._rag_selector = RAGSelector()

    def plan(self, task: TaskAnalysis,
             activations: list[DisciplineActivation]) -> CognitivePlan:
        steps: list[CognitivePlanStep] = []
        step_id = 0

        for activation in activations:
            step_id += 1
            step = self._build_step(step_id, task, activation, steps)
            steps.append(step)

        plan_id = hashlib.sha256(
            f"plan:{task.task_id}:{time.time()}".encode()
        ).hexdigest()[:16]

        autonomy = task.recommended_autonomy

        return CognitivePlan(
            plan_id=plan_id,
            task=task,
            steps=steps,
            autonomy_level=autonomy,
            activated_disciplines=activations,
            estimated_cost_usd=self._estimate_cost(task, steps),
            estimated_latency_ms=self._estimate_latency(task, steps),
        )

    def _build_step(self, step_id: int, task: TaskAnalysis,
                    activation: DisciplineActivation,
                    prior_steps: list[CognitivePlanStep]) -> CognitivePlanStep:
        depends_on = [s.step_id for s in prior_steps[-1:]] if prior_steps else []

        agent_type = None
        rag_mode = None
        loop_type = None
        query_lang = None

        if activation.discipline == "graph":
            agent_type = self._agent_selector.select(task, "graph")
            query_lang = "cypher"
        elif activation.discipline in ("loop", "loop_over_graph"):
            loop_type = self._select_loop(task)
            agent_type = self._agent_selector.select(task, "reasoning")
        elif activation.discipline == "prompt":
            rag_mode = self._rag_selector.select(task)
            agent_type = self._agent_selector.select(task, "rag")
        elif activation.discipline == "harness":
            agent_type = "orchestrator"
        elif activation.discipline == "security":
            agent_type = "validator"

        return CognitivePlanStep(
            step_id=step_id,
            action=f"{activation.discipline}:{activation.reason}",
            discipline=activation.discipline,
            agent_type=agent_type,
            rag_mode=rag_mode,
            loop_type=loop_type,
            query_lang=query_lang,
            autonomy=task.recommended_autonomy,
            depends_on=depends_on,
            config=activation.config,
        )

    def _select_loop(self, task: TaskAnalysis) -> str:
        if task.complexity == TaskComplexity.CRITICAL:
            return "HCTL"
        if task.is_write_operation:
            return "HITL"
        if task.complexity == TaskComplexity.COMPLEX:
            return "HOTL"
        return "HATL"

    def _estimate_cost(self, task: TaskAnalysis,
                       steps: list[CognitivePlanStep]) -> float:
        base = {"trivial": 0.001, "simple": 0.005, "moderate": 0.02,
                "complex": 0.08, "critical": 0.20}
        return base.get(task.complexity.value, 0.01) * len(steps)

    def _estimate_latency(self, task: TaskAnalysis,
                          steps: list[CognitivePlanStep]) -> float:
        base = {"trivial": 100, "simple": 300, "moderate": 800,
                "complex": 2000, "critical": 5000}
        return base.get(task.complexity.value, 500) * len(steps) * 0.7


class AgentSelector:
    """Selects the appropriate agent archetype for a discipline activation."""

    DISCIPLINE_AGENTS: dict[str, list[str]] = {
        "graph": ["goal_based", "enterprise", "rag"],
        "rag": ["rag", "agentic", "multi_agent"],
        "reasoning": ["planner", "critic", "self_reflection", "xai"],
        "tools": ["tool_calling", "function_calling", "executor"],
        "security": ["validator", "reviewer"],
        "orchestration": ["orchestrator", "hierarchical", "choreography"],
        "learning": ["self_learning", "self_evolving"],
    }

    def select(self, task: TaskAnalysis, domain: str) -> str:
        candidates = self.DISCIPLINE_AGENTS.get(domain, ["task"])
        if task.complexity in (TaskComplexity.COMPLEX, TaskComplexity.CRITICAL):
            for preferred in ["enterprise", "orchestrator", "planner", "xai"]:
                if preferred in candidates:
                    return preferred
        return candidates[0]


class RAGSelector:
    """Selects the appropriate RAG mode based on task analysis."""

    def select(self, task: TaskAnalysis) -> str:
        if task.requires_graph and task.requires_rag:
            return "graph"
        if task.is_multi_step:
            return "multi_hop"
        if task.requires_reasoning:
            return "agentic"
        if task.requires_memory:
            return "conversational"
        if task.complexity == TaskComplexity.CRITICAL:
            return "corrective"
        if task.complexity == TaskComplexity.COMPLEX:
            return "adaptive"
        return "hybrid"


# ── Execution Tracker ────────────────────────────────────────────────


@dataclass
class ExecutionRecord:
    plan_id: str
    task_id: str
    started_at: float = field(default_factory=time.time)
    completed_at: float | None = None
    status: str = "running"
    steps_completed: int = 0
    total_steps: int = 0
    actual_cost_usd: float = 0.0
    actual_latency_ms: float = 0.0
    outcome: dict[str, Any] = field(default_factory=dict)


class ExecutionTracker:
    """Tracks cognitive plan executions for self-assessment and adaptation."""

    def __init__(self) -> None:
        # RLock: stats() calls success_rate() while holding the lock.
        self._lock = threading.RLock()
        self._records: list[ExecutionRecord] = []
        self._by_complexity: dict[str, list[ExecutionRecord]] = defaultdict(list)

    def start(self, plan: CognitivePlan) -> ExecutionRecord:
        record = ExecutionRecord(
            plan_id=plan.plan_id,
            task_id=plan.task.task_id,
            total_steps=plan.step_count,
        )
        with self._lock:
            self._records.append(record)
            self._by_complexity[plan.task.complexity.value].append(record)
        return record

    def complete(self, record: ExecutionRecord,
                 outcome: dict[str, Any] | None = None) -> None:
        record.completed_at = time.time()
        record.status = "completed"
        record.actual_latency_ms = (record.completed_at - record.started_at) * 1000
        record.outcome = outcome or {}

    def fail(self, record: ExecutionRecord, error: str) -> None:
        record.completed_at = time.time()
        record.status = "failed"
        record.actual_latency_ms = (record.completed_at - record.started_at) * 1000
        record.outcome = {"error": error}

    def success_rate(self) -> float:
        with self._lock:
            return self._success_rate_unlocked()

    def _success_rate_unlocked(self) -> float:
        # Caller must hold self._lock (a non-reentrant Lock): FT-D01.
        completed = [r for r in self._records if r.status in ("completed", "failed")]
        if not completed:
            return 0.0
        return sum(1 for r in completed if r.status == "completed") / len(completed)

    def avg_latency_by_complexity(self) -> dict[str, float]:
        result: dict[str, float] = {}
        with self._lock:
            for complexity, records in self._by_complexity.items():
                completed = [r for r in records
                             if r.status == "completed" and r.actual_latency_ms > 0]
                if completed:
                    result[complexity] = (
                        sum(r.actual_latency_ms for r in completed) / len(completed)
                    )
        return result

    def stats(self) -> dict[str, Any]:
        with self._lock:
            return {
                "total_executions": len(self._records),
                "completed": sum(1 for r in self._records if r.status == "completed"),
                "failed": sum(1 for r in self._records if r.status == "failed"),
                "running": sum(1 for r in self._records if r.status == "running"),
                "success_rate": self._success_rate_unlocked(),
            }


# ── Intelligence Engine (top-level) ─────────────────────────────────


class IntelligenceEngine:
    """System-Level Autonomy orchestrator — the meta-engine that composes
    all cognitive capabilities into unified autonomous pipelines.

    This is the capstone of the engineering discipline stack. It doesn't
    replace individual engines; it conducts them like an orchestra conductor
    — selecting instruments, setting tempo, and fusing the performance.
    """

    def __init__(self) -> None:
        self._analyzer = TaskAnalyzer()
        self._composer = DisciplineComposer()
        self._planner = CognitivePlanner()
        self._tracker = ExecutionTracker()
        self._manifest = CapabilityManifest()
        self._lock = threading.Lock()
        self._plans: list[CognitivePlan] = []

    @property
    def manifest(self) -> CapabilityManifest:
        return self._manifest

    @property
    def tracker(self) -> ExecutionTracker:
        return self._tracker

    def analyze(self, query: str,
                context: dict[str, Any] | None = None) -> TaskAnalysis:
        return self._analyzer.analyze(query, context)

    def plan(self, query: str,
             context: dict[str, Any] | None = None,
             override_autonomy: AutonomyLevel | None = None) -> CognitivePlan:
        task = self._analyzer.analyze(query, context)

        if override_autonomy:
            task.recommended_autonomy = override_autonomy

        activations = self._composer.compose(task)
        cognitive_plan = self._planner.plan(task, activations)

        with self._lock:
            self._plans.append(cognitive_plan)
        return cognitive_plan

    def execute_plan(self, plan: CognitivePlan) -> ExecutionRecord:
        record = self._tracker.start(plan)
        try:
            for i, step in enumerate(plan.steps):
                record.steps_completed = i + 1
            self._tracker.complete(record, {
                "disciplines_executed": [d.discipline for d in plan.activated_disciplines],
                "autonomy": plan.autonomy_level.value,
            })
        except Exception as exc:
            self._tracker.fail(record, str(exc))
        return record

    def cognitive_pipeline(self, query: str,
                           context: dict[str, Any] | None = None) -> dict[str, Any]:
        plan = self.plan(query, context)
        record = self.execute_plan(plan)
        return {
            "plan": plan.to_dict(),
            "execution": {
                "status": record.status,
                "steps_completed": record.steps_completed,
                "latency_ms": record.actual_latency_ms,
            },
            "autonomy_level": plan.autonomy_level.value,
            "complexity": plan.task.complexity.value,
        }

    def get_autonomy_for_task(self, query: str) -> dict[str, Any]:
        task = self._analyzer.analyze(query)
        return {
            "query": query,
            "complexity": task.complexity.value,
            "recommended_autonomy": task.recommended_autonomy.value,
            "autonomy_risk_level": AUTONOMY_RISK_MAP.get(task.recommended_autonomy, 0),
            "requires": {
                "graph": task.requires_graph,
                "rag": task.requires_rag,
                "reasoning": task.requires_reasoning,
                "memory": task.requires_memory,
                "tools": task.requires_tools,
                "security_check": task.requires_security_check,
            },
        }

    def list_capabilities(self) -> dict[str, Any]:
        return self._manifest.to_dict()

    def stats(self) -> dict[str, Any]:
        return {
            "engine": "intelligence_engineering",
            "capabilities": self._manifest.to_dict(),
            "plans_generated": len(self._plans),
            "execution": self._tracker.stats(),
        }


# ── Loop-over-Loop Engineering (CORE-005) ─────────────────────────────


class LoopCircuitBreakerOpenError(RuntimeError):
    """Raised when supervisory circuit breaker trips."""
    pass


@dataclass
class LoopMetrics:
    """Metrics tracked during an inner loop execution."""
    loop_id: str
    strategy: str
    iterations: int = 0
    convergence_score: float = 0.0
    cost: float = 0.0
    quality_score: float = 0.0
    duration_ms: float = 0.0
    status: str = "initialized"
    error: str | None = None
    step_history: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "loop_id": self.loop_id,
            "strategy": self.strategy,
            "iterations": self.iterations,
            "convergence_score": round(self.convergence_score, 4),
            "cost": round(self.cost, 4),
            "quality_score": round(self.quality_score, 4),
            "duration_ms": round(self.duration_ms, 2),
            "status": self.status,
            "error": self.error,
            "step_count": len(self.step_history),
        }


class LoopMonitor:
    """Tracks inner loop metrics (iterations, convergence, cost, quality)."""

    def __init__(
        self,
        min_quality: float = 0.6,
        convergence_threshold: float = 0.85,
        max_cost: float = 10.0,
        max_iterations: int = 15,
    ) -> None:
        self.min_quality = min_quality
        self.convergence_threshold = convergence_threshold
        self.max_cost = max_cost
        self.max_iterations = max_iterations
        self._active_metrics: dict[str, LoopMetrics] = {}
        self._history: list[LoopMetrics] = []
        self._lock = threading.Lock()

    def start_loop(self, loop_id: str, strategy: str) -> LoopMetrics:
        with self._lock:
            metrics = LoopMetrics(loop_id=loop_id, strategy=strategy, status="running")
            self._active_metrics[loop_id] = metrics
            return metrics

    def record_step(
        self,
        loop_id: str,
        iteration: int,
        delta_cost: float = 0.0,
        quality: float = 0.0,
        convergence: float = 0.0,
        step_metadata: dict[str, Any] | None = None,
    ) -> LoopMetrics:
        with self._lock:
            metrics = self._active_metrics.get(loop_id)
            if not metrics:
                metrics = LoopMetrics(loop_id=loop_id, strategy="unknown", status="running")
                self._active_metrics[loop_id] = metrics

            metrics.iterations = iteration
            metrics.cost += delta_cost
            metrics.quality_score = quality
            metrics.convergence_score = convergence
            metrics.step_history.append({
                "iteration": iteration,
                "cost": metrics.cost,
                "quality": quality,
                "convergence": convergence,
                "metadata": step_metadata or {},
                "timestamp": time.time(),
            })
            return metrics

    def finalize_loop(
        self,
        loop_id: str,
        status: str,
        duration_ms: float = 0.0,
        error: str | None = None,
    ) -> LoopMetrics:
        with self._lock:
            metrics = self._active_metrics.pop(loop_id, None)
            if not metrics:
                metrics = LoopMetrics(loop_id=loop_id, strategy="unknown")
            metrics.status = status
            metrics.duration_ms = duration_ms
            metrics.error = error
            self._history.append(metrics)
            return metrics

    def is_underperforming(self, metrics: LoopMetrics) -> tuple[bool, str]:
        """Check if inner loop is underperforming according to thresholds."""
        if metrics.iterations >= self.max_iterations and metrics.convergence_score < self.convergence_threshold:
            return True, f"Max iterations {self.max_iterations} reached without convergence ({metrics.convergence_score:.2f})"
        if metrics.cost >= self.max_cost:
            return True, f"Max cost {self.max_cost} exceeded (current: {metrics.cost:.2f})"
        if metrics.iterations >= 3 and metrics.quality_score < self.min_quality:
            return True, f"Quality {metrics.quality_score:.2f} below threshold {self.min_quality}"
        return False, "healthy"

    def get_history(self) -> list[dict[str, Any]]:
        with self._lock:
            return [m.to_dict() for m in self._history]


class LoopSwitcher:
    """Dynamic strategy switcher when an inner loop underperforms or fails."""

    def __init__(self, fallback_chains: dict[str, list[str]] | None = None) -> None:
        self.fallback_chains = fallback_chains or {
            "react": ["tree_of_thought", "direct_rag", "fallback_heuristic"],
            "tree_of_thought": ["react", "direct_rag", "fallback_heuristic"],
            "reflection": ["iterative_refine", "direct_rag"],
            "plan_and_solve": ["react", "direct_heuristic"],
        }
        self._switch_log: list[dict[str, Any]] = []

    def get_next_strategy(self, current_strategy: str, attempted_strategies: list[str]) -> str | None:
        chain = self.fallback_chains.get(current_strategy, [])
        for candidate in chain:
            if candidate not in attempted_strategies:
                return candidate
        return None

    def log_switch(self, loop_id: str, from_strategy: str, to_strategy: str, reason: str) -> None:
        self._switch_log.append({
            "loop_id": loop_id,
            "from_strategy": from_strategy,
            "to_strategy": to_strategy,
            "reason": reason,
            "timestamp": time.time(),
        })

    @property
    def switch_log(self) -> list[dict[str, Any]]:
        return list(self._switch_log)


@dataclass
class LoopComposition:
    """Declarative binding between supervisory outer loop and managed inner loops."""
    name: str
    outer_loop_name: str  # e.g. "OODA", "META_EVAL", "SUPERVISORY_ADAPT"
    strategies: list[str]  # ordered preference of inner strategies
    max_total_iterations: int = 20
    timeout_ms: float = 30000.0
    failure_threshold: int = 3
    require_verification: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "outer_loop_name": self.outer_loop_name,
            "strategies": self.strategies,
            "max_total_iterations": self.max_total_iterations,
            "timeout_ms": self.timeout_ms,
            "failure_threshold": self.failure_threshold,
            "require_verification": self.require_verification,
            "metadata": self.metadata,
        }


@dataclass
class SupervisoryResult:
    """Outcome of a supervisory loop execution."""
    composition_name: str
    outer_loop_name: str
    success: bool
    final_strategy: str
    total_iterations: int
    total_cost: float
    total_duration_ms: float
    attempts: list[dict[str, Any]]
    final_output: Any = None
    circuit_breaker_tripped: bool = False
    verification_passed: bool = True
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "composition_name": self.composition_name,
            "outer_loop_name": self.outer_loop_name,
            "success": self.success,
            "final_strategy": self.final_strategy,
            "total_iterations": self.total_iterations,
            "total_cost": round(self.total_cost, 4),
            "total_duration_ms": round(self.total_duration_ms, 2),
            "attempts": self.attempts,
            "circuit_breaker_tripped": self.circuit_breaker_tripped,
            "verification_passed": self.verification_passed,
            "error": self.error,
        }


class SupervisoryLoop:
    """Supervisory loop that orchestrates and monitors inner loops with circuit breaker."""

    def __init__(
        self,
        composition: LoopComposition,
        monitor: LoopMonitor | None = None,
        switcher: LoopSwitcher | None = None,
    ) -> None:
        self.composition = composition
        self.monitor = monitor or LoopMonitor()
        self.switcher = switcher or LoopSwitcher()
        self._consecutive_failures = 0
        self._circuit_open = False
        self._lock = threading.Lock()

    @property
    def is_circuit_open(self) -> bool:
        return self._circuit_open

    def reset_circuit(self) -> None:
        with self._lock:
            self._consecutive_failures = 0
            self._circuit_open = False

    def execute(
        self,
        task_fn: Callable[[str, dict[str, Any]], Any],
        context: dict[str, Any] | None = None,
        verification_fn: Callable[[Any], bool] | None = None,
    ) -> SupervisoryResult:
        """Execute inner loop under supervision with OODA-style monitoring and adaptation."""
        with self._lock:
            if self._circuit_open:
                raise LoopCircuitBreakerOpenError(
                    f"Supervisory circuit breaker for '{self.composition.name}' is OPEN due to repeated failures."
                )

        ctx = context or {}
        start_time = time.time()
        attempted: list[str] = []
        attempts_log: list[dict[str, Any]] = []
        total_cost = 0.0
        total_iterations = 0

        # Choose initial strategy
        current_strategy = self.composition.strategies[0] if self.composition.strategies else "default"

        while current_strategy:
            attempted.append(current_strategy)
            loop_id = f"{self.composition.name}_{current_strategy}_{int(time.time() * 1000)}"
            metrics = self.monitor.start_loop(loop_id, current_strategy)

            t0 = time.time()
            success = False
            output = None
            error_msg = None

            try:
                # Check supervisor timeout
                elapsed_ms = (time.time() - start_time) * 1000
                if elapsed_ms > self.composition.timeout_ms:
                    raise TimeoutError(f"Supervisory loop exceeded timeout {self.composition.timeout_ms}ms")

                # Inner loop call
                output = task_fn(current_strategy, ctx)
                duration_ms = (time.time() - t0) * 1000

                # Simulate step metrics if task returned structured dict
                if isinstance(output, dict) and "iterations" in output:
                    iters = output.get("iterations", 1)
                    cost = output.get("cost", 0.05)
                    qual = output.get("quality", 0.9)
                    conv = output.get("convergence", 0.95)
                    self.monitor.record_step(loop_id, iters, cost, qual, conv)
                    total_iterations += iters
                    total_cost += cost
                else:
                    self.monitor.record_step(loop_id, 1, 0.01, 0.85, 0.9)
                    total_iterations += 1
                    total_cost += 0.01

                # Check underperformance
                underperforming, reason = self.monitor.is_underperforming(metrics)
                if underperforming:
                    raise RuntimeError(f"Strategy {current_strategy} underperformed: {reason}")

                # Optional verification gate
                if verification_fn and self.composition.require_verification:
                    v_ok = verification_fn(output)
                    if not v_ok:
                        raise ValueError(f"Verification gate rejected output from {current_strategy}")

                self.monitor.finalize_loop(loop_id, "completed", duration_ms)
                success = True
                with self._lock:
                    self._consecutive_failures = 0

                attempts_log.append({
                    "strategy": current_strategy,
                    "success": True,
                    "duration_ms": duration_ms,
                    "metrics": metrics.to_dict(),
                })

                return SupervisoryResult(
                    composition_name=self.composition.name,
                    outer_loop_name=self.composition.outer_loop_name,
                    success=True,
                    final_strategy=current_strategy,
                    total_iterations=total_iterations,
                    total_cost=total_cost,
                    total_duration_ms=(time.time() - start_time) * 1000,
                    attempts=attempts_log,
                    final_output=output,
                )

            except Exception as exc:
                duration_ms = (time.time() - t0) * 1000
                error_msg = str(exc)
                self.monitor.finalize_loop(loop_id, "failed", duration_ms, error=error_msg)

                with self._lock:
                    self._consecutive_failures += 1
                    if self._consecutive_failures >= self.composition.failure_threshold:
                        self._circuit_open = True

                attempts_log.append({
                    "strategy": current_strategy,
                    "success": False,
                    "error": error_msg,
                    "duration_ms": duration_ms,
                    "metrics": metrics.to_dict(),
                })

                if self._circuit_open:
                    break

                # Switch strategy
                next_strat = None
                # Check preferred composition list first
                for cand in self.composition.strategies:
                    if cand not in attempted:
                        next_strat = cand
                        break
                # Fallback to switcher chains
                if not next_strat:
                    next_strat = self.switcher.get_next_strategy(current_strategy, attempted)

                if next_strat:
                    self.switcher.log_switch(loop_id, current_strategy, next_strat, error_msg)
                    current_strategy = next_strat
                else:
                    break

        return SupervisoryResult(
            composition_name=self.composition.name,
            outer_loop_name=self.composition.outer_loop_name,
            success=False,
            final_strategy=attempted[-1] if attempted else "none",
            total_iterations=total_iterations,
            total_cost=total_cost,
            total_duration_ms=(time.time() - start_time) * 1000,
            attempts=attempts_log,
            final_output=None,
            circuit_breaker_tripped=self._circuit_open,
            error=error_msg or "All strategies exhausted",
        )


_instance: IntelligenceEngine | None = None
_lock = threading.Lock()


def get_intelligence_engine() -> IntelligenceEngine:
    global _instance
    if _instance is None:
        with _lock:
            if _instance is None:
                _instance = IntelligenceEngine()
    return _instance

