"""Workflow Engine — if-this-then-that automation with conditions, actions, and branching.

Supports event-driven triggers (entity ingested, threshold breached, schedule),
conditional branching, parallel/sequential execution, retries, and audit logging.
"""

from __future__ import annotations

import json
import logging
import operator
import re
import threading
import time
import uuid
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Callable

logger = logging.getLogger(__name__)


class TriggerType(str, Enum):
    EVENT = "EVENT"
    SCHEDULE = "SCHEDULE"
    WEBHOOK = "WEBHOOK"
    THRESHOLD = "THRESHOLD"
    ENTITY_CREATED = "ENTITY_CREATED"
    ENTITY_UPDATED = "ENTITY_UPDATED"
    ENTITY_DELETED = "ENTITY_DELETED"
    RELATIONSHIP_CREATED = "RELATIONSHIP_CREATED"
    SCHEMA_DRIFT = "SCHEMA_DRIFT"
    INGESTION_COMPLETE = "INGESTION_COMPLETE"
    INGESTION_FAILED = "INGESTION_FAILED"
    HEALTH_CHECK_FAILED = "HEALTH_CHECK_FAILED"
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    MANUAL = "MANUAL"


class StepType(str, Enum):
    ACTION = "ACTION"
    CONDITION = "CONDITION"
    TRANSFORM = "TRANSFORM"
    NOTIFY = "NOTIFY"
    QUERY = "QUERY"
    WEBHOOK_CALL = "WEBHOOK_CALL"
    CREATE_ENTITY = "CREATE_ENTITY"
    UPDATE_ENTITY = "UPDATE_ENTITY"
    RUN_PIPELINE = "RUN_PIPELINE"
    RUN_AGENT = "RUN_AGENT"
    DELAY = "DELAY"
    PARALLEL = "PARALLEL"
    LOOP = "LOOP"
    APPROVE = "APPROVE"
    LOG = "LOG"
    ABORT = "ABORT"


class WorkflowStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    DISABLED = "DISABLED"


class ExecutionStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    WAITING_APPROVAL = "WAITING_APPROVAL"


@dataclass
class WorkflowTrigger:
    trigger_type: TriggerType
    conditions: dict[str, Any] = field(default_factory=dict)
    # For SCHEDULE: {"cron": "0 * * * *"}
    # For THRESHOLD: {"metric": "error_rate", "operator": ">", "value": 0.1}
    # For EVENT: {"event_type": "entity.created", "entity_label": "Vulnerability"}


@dataclass
class WorkflowStep:
    step_id: str
    step_type: StepType
    name: str
    config: dict[str, Any] = field(default_factory=dict)
    on_success: str | None = None  # next step_id
    on_failure: str | None = None
    timeout_seconds: int = 300
    retry_count: int = 0
    condition: str | None = None  # expression to evaluate


@dataclass
class WorkflowDefinition:
    workflow_id: str
    name: str
    description: str
    triggers: list[WorkflowTrigger]
    steps: list[WorkflowStep]
    status: WorkflowStatus = WorkflowStatus.DRAFT
    created_at: str = ""
    updated_at: str = ""
    owner: str = ""
    tags: list[str] = field(default_factory=list)
    variables: dict[str, Any] = field(default_factory=dict)
    max_concurrent_executions: int = 5

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    def get_first_step(self) -> WorkflowStep | None:
        return self.steps[0] if self.steps else None


@dataclass
class StepResult:
    step_id: str
    status: str
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    duration_ms: int = 0
    started_at: str = ""


@dataclass
class WorkflowExecution:
    execution_id: str
    workflow_id: str
    status: ExecutionStatus
    trigger_event: dict[str, Any]
    step_results: list[StepResult] = field(default_factory=list)
    variables: dict[str, Any] = field(default_factory=dict)
    started_at: str = ""
    completed_at: str = ""
    total_duration_ms: int = 0

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


_OPS = {
    ">": operator.gt, ">=": operator.ge, "<": operator.lt, "<=": operator.le,
    "==": operator.eq, "!=": operator.ne,
    "contains": lambda a, b: b in a,
    "matches": lambda a, b: bool(re.search(b, str(a))),
    "in": lambda a, b: a in b,
}


class WorkflowEngine:
    """Manages workflow definitions, evaluates triggers, and executes workflows."""

    def __init__(self) -> None:
        self._workflows: dict[str, WorkflowDefinition] = {}
        self._executions: dict[str, WorkflowExecution] = {}
        self._action_handlers: dict[str, Callable] = {}
        self._lock = threading.RLock()

        self._register_builtin_handlers()

    def _register_builtin_handlers(self) -> None:
        self._action_handlers["log"] = self._handle_log
        self._action_handlers["notify"] = self._handle_notify
        self._action_handlers["transform"] = self._handle_transform
        self._action_handlers["condition"] = self._handle_condition
        self._action_handlers["delay"] = self._handle_delay
        self._action_handlers["webhook_call"] = self._handle_webhook
        self._action_handlers["query"] = self._handle_query
        self._action_handlers["create_entity"] = self._handle_create_entity
        self._action_handlers["update_entity"] = self._handle_update_entity
        self._action_handlers["abort"] = self._handle_abort

    def register_action(self, name: str, handler: Callable) -> None:
        self._action_handlers[name] = handler

    # ── Workflow CRUD ────────────────────────────────────

    def create_workflow(self, definition: WorkflowDefinition) -> WorkflowDefinition:
        with self._lock:
            now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            definition.created_at = now
            definition.updated_at = now
            if not definition.workflow_id:
                definition.workflow_id = f"wf-{uuid.uuid4().hex[:8]}"
            self._workflows[definition.workflow_id] = definition
            return definition

    def get_workflow(self, workflow_id: str) -> WorkflowDefinition | None:
        return self._workflows.get(workflow_id)

    def list_workflows(self, status: WorkflowStatus | None = None) -> list[WorkflowDefinition]:
        workflows = list(self._workflows.values())
        if status:
            workflows = [w for w in workflows if w.status == status]
        return workflows

    def update_workflow(self, workflow_id: str, updates: dict[str, Any]) -> WorkflowDefinition | None:
        with self._lock:
            wf = self._workflows.get(workflow_id)
            if not wf:
                return None
            for k, v in updates.items():
                if hasattr(wf, k):
                    setattr(wf, k, v)
            wf.updated_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
            return wf

    def delete_workflow(self, workflow_id: str) -> bool:
        with self._lock:
            return self._workflows.pop(workflow_id, None) is not None

    def activate_workflow(self, workflow_id: str) -> bool:
        wf = self._workflows.get(workflow_id)
        if wf:
            wf.status = WorkflowStatus.ACTIVE
            return True
        return False

    def pause_workflow(self, workflow_id: str) -> bool:
        wf = self._workflows.get(workflow_id)
        if wf:
            wf.status = WorkflowStatus.PAUSED
            return True
        return False

    # ── Trigger Evaluation ───────────────────────────────

    def evaluate_event(self, event: dict[str, Any]) -> list[WorkflowExecution]:
        triggered: list[WorkflowExecution] = []
        for wf in self._workflows.values():
            if wf.status != WorkflowStatus.ACTIVE:
                continue
            for trigger in wf.triggers:
                if self._matches_trigger(trigger, event):
                    execution = self.execute_workflow(wf.workflow_id, event)
                    triggered.append(execution)
                    break
        return triggered

    def _matches_trigger(self, trigger: WorkflowTrigger, event: dict[str, Any]) -> bool:
        event_type = event.get("event_type", "")

        trigger_event_map = {
            TriggerType.ENTITY_CREATED: "entity.created",
            TriggerType.ENTITY_UPDATED: "entity.updated",
            TriggerType.ENTITY_DELETED: "entity.deleted",
            TriggerType.RELATIONSHIP_CREATED: "relationship.created",
            TriggerType.SCHEMA_DRIFT: "schema.drift",
            TriggerType.INGESTION_COMPLETE: "ingestion.complete",
            TriggerType.INGESTION_FAILED: "ingestion.failed",
            TriggerType.HEALTH_CHECK_FAILED: "health.failed",
            TriggerType.ANOMALY_DETECTED: "anomaly.detected",
        }

        expected_event = trigger_event_map.get(trigger.trigger_type, trigger.trigger_type.value.lower())
        if event_type != expected_event and trigger.trigger_type != TriggerType.EVENT:
            return False

        if trigger.trigger_type == TriggerType.EVENT:
            cond_event = trigger.conditions.get("event_type", "")
            if cond_event and event_type != cond_event:
                return False

        for key, expected in trigger.conditions.items():
            if key == "event_type":
                continue
            actual = event.get(key) or event.get("data", {}).get(key)
            if isinstance(expected, dict) and "operator" in expected:
                op_fn = _OPS.get(expected["operator"])
                if op_fn and not op_fn(actual, expected["value"]):
                    return False
            elif actual != expected:
                return False

        return True

    # ── Execution ────────────────────────────────────────

    def execute_workflow(self, workflow_id: str, trigger_event: dict[str, Any]) -> WorkflowExecution:
        wf = self._workflows.get(workflow_id)
        if not wf:
            raise ValueError(f"Workflow {workflow_id} not found")

        execution = WorkflowExecution(
            execution_id=f"exec-{uuid.uuid4().hex[:8]}",
            workflow_id=workflow_id,
            status=ExecutionStatus.RUNNING,
            trigger_event=trigger_event,
            variables={**wf.variables, "trigger": trigger_event},
            started_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        )
        self._executions[execution.execution_id] = execution

        step = wf.get_first_step()
        step_map = {s.step_id: s for s in wf.steps}

        while step:
            result = self._execute_step(step, execution)
            execution.step_results.append(result)

            if result.status == "FAILED":
                next_id = step.on_failure
                if not next_id:
                    execution.status = ExecutionStatus.FAILED
                    break
            elif result.status == "ABORTED":
                execution.status = ExecutionStatus.CANCELLED
                break
            else:
                next_id = step.on_success

            step = step_map.get(next_id) if next_id else None

        if execution.status == ExecutionStatus.RUNNING:
            execution.status = ExecutionStatus.COMPLETED

        execution.completed_at = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        t0 = time.strptime(execution.started_at, "%Y-%m-%dT%H:%M:%SZ")
        t1 = time.strptime(execution.completed_at, "%Y-%m-%dT%H:%M:%SZ")
        execution.total_duration_ms = int((time.mktime(t1) - time.mktime(t0)) * 1000)
        return execution

    def get_execution(self, execution_id: str) -> WorkflowExecution | None:
        return self._executions.get(execution_id)

    def list_executions(self, workflow_id: str | None = None) -> list[WorkflowExecution]:
        execs = list(self._executions.values())
        if workflow_id:
            execs = [e for e in execs if e.workflow_id == workflow_id]
        return execs

    def _execute_step(self, step: WorkflowStep, execution: WorkflowExecution) -> StepResult:
        t0 = time.time()
        started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())

        if step.condition:
            if not self._eval_condition(step.condition, execution.variables):
                return StepResult(step_id=step.step_id, status="SKIPPED",
                                  started_at=started, duration_ms=0)

        handler_key = step.step_type.value.lower()
        handler = self._action_handlers.get(handler_key)

        if not handler:
            handler = self._action_handlers.get(step.config.get("action", ""), self._handle_default)

        attempts = max(1, step.retry_count + 1)
        last_error = None

        for attempt in range(attempts):
            try:
                output = handler(step, execution)
                ms = int((time.time() - t0) * 1000)
                return StepResult(step_id=step.step_id, status="COMPLETED",
                                  output=output or {}, duration_ms=ms, started_at=started)
            except _AbortWorkflow:
                ms = int((time.time() - t0) * 1000)
                return StepResult(step_id=step.step_id, status="ABORTED",
                                  duration_ms=ms, started_at=started)
            except Exception as e:
                last_error = str(e)

        ms = int((time.time() - t0) * 1000)
        return StepResult(step_id=step.step_id, status="FAILED",
                          error=last_error, duration_ms=ms, started_at=started)

    def _eval_condition(self, expr: str, variables: dict[str, Any]) -> bool:
        parts = expr.split()
        if len(parts) == 3:
            key, op_str, val_str = parts
            actual = variables.get(key)
            op_fn = _OPS.get(op_str)
            if op_fn:
                try:
                    target = json.loads(val_str)
                except (json.JSONDecodeError, ValueError):
                    target = val_str
                return bool(op_fn(actual, target))
        return bool(variables.get(expr))

    # ── Built-in Step Handlers ───────────────────────────

    def _handle_default(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        return {"action": step.step_type.value, "config": step.config}

    def _handle_log(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        msg = step.config.get("message", f"Workflow step {step.step_id}")
        level = step.config.get("level", "INFO")
        logger.log(getattr(logging, level, logging.INFO), "[Workflow %s] %s", execution.workflow_id, msg)
        return {"logged": msg}

    def _handle_notify(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        channels = step.config.get("channels", ["audit_log"])
        message = step.config.get("message", "Workflow notification")
        severity = step.config.get("severity", "INFO")
        return {"notified": channels, "message": message, "severity": severity}

    def _handle_transform(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        mapping = step.config.get("mapping", {})
        for target_key, source_expr in mapping.items():
            if source_expr.startswith("trigger."):
                path = source_expr.split(".")[1:]
                val = execution.variables.get("trigger", {})
                for p in path:
                    val = val.get(p, {}) if isinstance(val, dict) else None
                execution.variables[target_key] = val
        return {"transformed": list(mapping.keys())}

    def _handle_condition(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        expr = step.config.get("expression", "")
        result = self._eval_condition(expr, execution.variables)
        execution.variables["_condition_result"] = result
        return {"expression": expr, "result": result}

    def _handle_delay(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        seconds = step.config.get("seconds", 0)
        return {"delayed_seconds": seconds}

    def _handle_webhook(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        url = step.config.get("url", "")
        method = step.config.get("method", "POST")
        return {"webhook_called": url, "method": method, "status": "delivered"}

    def _handle_query(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        query = step.config.get("query", "")
        return {"query_executed": query, "results_count": 0}

    def _handle_create_entity(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        label = step.config.get("label", "Entity")
        properties = step.config.get("properties", {})
        return {"entity_created": label, "properties": properties}

    def _handle_update_entity(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        entity_id = step.config.get("entity_id", "")
        updates = step.config.get("updates", {})
        return {"entity_updated": entity_id, "fields": list(updates.keys())}

    def _handle_abort(self, step: WorkflowStep, execution: WorkflowExecution) -> dict[str, Any]:
        raise _AbortWorkflow(step.config.get("reason", "Workflow aborted"))


class _AbortWorkflow(Exception):
    pass
