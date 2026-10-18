"""Worker protocol and resource class definitions (CRA-002.7, CRA-002.8, CRA-002.9).

JSON-RPC 2.0 over stdio/pipes carrying:
- request ID, deadline, resource class, engine name/version/profile, input artifact hashes.
- outcomes: COMPLETED, FAILED, TIMEOUT, OOM, LIMIT_EXCEEDED.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ResourceClass(str, Enum):
    STANDARD = "standard"
    HEAVY = "heavy"


class WorkerOutcome(str, Enum):
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMEOUT = "TIMEOUT"
    OOM = "OOM"
    LIMIT_EXCEEDED = "LIMIT_EXCEEDED"
    KILLED = "KILLED"


@dataclass(frozen=True)
class WorkerLimits:
    max_memory_mb: int
    max_cpu_cores: int
    max_wall_time_seconds: float

    @classmethod
    def standard_default(cls) -> WorkerLimits:
        """CRA-002.7: standard <= 2 GiB RSS, <= 2 CPU, 30 s wall clock."""
        return cls(max_memory_mb=2048, max_cpu_cores=2, max_wall_time_seconds=30.0)

    @classmethod
    def heavy_default(cls) -> WorkerLimits:
        """CRA-002.7: heavy <= 8 GiB RSS, <= 4 CPU, 600 s wall clock."""
        return cls(max_memory_mb=8192, max_cpu_cores=4, max_wall_time_seconds=600.0)

    @classmethod
    def resolve_effective(
        cls,
        resource_class: ResourceClass | str,
        tenant_limits: WorkerLimits | None = None,
    ) -> WorkerLimits:
        """CRA-002.7: Lower of tenant and class limit wins."""
        base = cls.heavy_default() if str(resource_class) == ResourceClass.HEAVY.value else cls.standard_default()
        if tenant_limits is None:
            return base

        return cls(
            max_memory_mb=min(base.max_memory_mb, tenant_limits.max_memory_mb),
            max_cpu_cores=min(base.max_cpu_cores, tenant_limits.max_cpu_cores),
            max_wall_time_seconds=min(base.max_wall_time_seconds, tenant_limits.max_wall_time_seconds),
        )


@dataclass
class WorkerInputArtifact:
    name: str
    sha256: str
    ref: str


@dataclass
class WorkerRequest:
    request_id: str
    deadline_ms: int
    resource_class: str
    engine: str
    engine_version: str
    profile: str
    inputs: list[WorkerInputArtifact] = field(default_factory=list)
    payload: dict[str, Any] = field(default_factory=dict)
    jsonrpc: str = "2.0"
    method: str = "execute"

    def to_json(self) -> str:
        d = {
            "jsonrpc": self.jsonrpc,
            "id": self.request_id,
            "method": self.method,
            "params": {
                "request_id": self.request_id,
                "deadline_ms": self.deadline_ms,
                "resource_class": self.resource_class,
                "engine": self.engine,
                "engine_version": self.engine_version,
                "profile": self.profile,
                "inputs": [asdict(inp) for inp in self.inputs],
                "payload": self.payload,
            },
        }
        return json.dumps(d)

    @classmethod
    def from_json(cls, raw: str) -> WorkerRequest:
        data = json.loads(raw)
        params = data.get("params", {})
        inputs = [
            WorkerInputArtifact(
                name=inp.get("name", ""),
                sha256=inp.get("sha256", ""),
                ref=inp.get("ref", ""),
            )
            for inp in params.get("inputs", [])
        ]
        return cls(
            request_id=params.get("request_id", data.get("id", "")),
            deadline_ms=int(params.get("deadline_ms", 30000)),
            resource_class=params.get("resource_class", "standard"),
            engine=params.get("engine", ""),
            engine_version=params.get("engine_version", ""),
            profile=params.get("profile", "P0"),
            inputs=inputs,
            payload=params.get("payload", {}),
            jsonrpc=data.get("jsonrpc", "2.0"),
            method=data.get("method", "execute"),
        )


@dataclass
class WorkerResult:
    status: WorkerOutcome
    outputs: dict[str, Any] = field(default_factory=dict)
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkerError:
    code: int
    message: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass
class WorkerResponse:
    request_id: str
    result: WorkerResult | None = None
    error: WorkerError | None = None
    jsonrpc: str = "2.0"

    def to_json(self) -> str:
        d: dict[str, Any] = {
            "jsonrpc": self.jsonrpc,
            "id": self.request_id,
        }
        if self.result is not None:
            d["result"] = {
                "status": self.result.status.value,
                "outputs": self.result.outputs,
                "metrics": self.result.metrics,
            }
        elif self.error is not None:
            d["error"] = asdict(self.error)
        return json.dumps(d)

    @classmethod
    def from_json(cls, raw: str) -> WorkerResponse:
        data = json.loads(raw)
        req_id = str(data.get("id", ""))
        res_dict = data.get("result")
        err_dict = data.get("error")

        result = None
        if res_dict:
            result = WorkerResult(
                status=WorkerOutcome(res_dict.get("status", WorkerOutcome.COMPLETED.value)),
                outputs=res_dict.get("outputs", {}),
                metrics=res_dict.get("metrics", {}),
            )

        error = None
        if err_dict:
            error = WorkerError(
                code=int(err_dict.get("code", -1)),
                message=str(err_dict.get("message", "")),
                data=err_dict.get("data", {}),
            )

        return cls(
            request_id=req_id,
            result=result,
            error=error,
            jsonrpc=data.get("jsonrpc", "2.0"),
        )
