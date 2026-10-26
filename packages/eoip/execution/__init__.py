"""§7 durable execution infrastructure.

Submodules:

* :mod:`eoip.execution.eventstore`  — append-only event store, snapshots, reconciliation.
* :mod:`eoip.execution.workflows`   — event-sourced durable workflow engine.
* :mod:`eoip.execution.scheduling`  — lease-based priority work claiming (reuses eoip.ha).
* :mod:`eoip.execution.router`      — ``build_router()`` HTTP surface.
"""

from eoip.execution.eventstore import Event, EventStore, ReconciliationReport, Snapshot
from eoip.execution.scheduling import PriorityWorkQueue, SchedulerElection, WorkItem
from eoip.execution.workflows import (
    ExecutionEngine,
    StepDefinition,
    WorkflowDefinition,
    WorkflowState,
    apply_event,
)

__all__ = [
    "Event",
    "EventStore",
    "ExecutionEngine",
    "PriorityWorkQueue",
    "ReconciliationReport",
    "SchedulerElection",
    "Snapshot",
    "StepDefinition",
    "WorkItem",
    "WorkflowDefinition",
    "WorkflowState",
    "apply_event",
]
