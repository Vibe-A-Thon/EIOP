"""Workers package — isolated worker processes and supervisor for safe execution."""

from eoip.workers.protocol import (
    ResourceClass,
    WorkerLimits,
    WorkerOutcome,
    WorkerRequest,
    WorkerResponse,
    WorkerResult,
)
from eoip.workers.supervisor import (
    SupervisorStats,
    WorkerExecutionRequest,
    WorkerExecutionResponse,
    WorkerSupervisor,
    get_worker_supervisor,
)

__all__ = [
    "ResourceClass",
    "WorkerLimits",
    "WorkerOutcome",
    "WorkerRequest",
    "WorkerResponse",
    "WorkerResult",
    "SupervisorStats",
    "WorkerExecutionRequest",
    "WorkerExecutionResponse",
    "WorkerSupervisor",
    "get_worker_supervisor",
]
