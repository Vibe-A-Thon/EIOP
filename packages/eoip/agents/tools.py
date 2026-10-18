"""Versioned, capability-scoped tool registry for Deep Agents."""

from __future__ import annotations

from collections.abc import Callable
from hashlib import sha256
from time import monotonic
from typing import Any

from eoip.contracts.tool import ToolContract, ToolRequest, ToolResult
from eoip.graph.store import GraphStore
from eoip.graph.traversal import GraphTraversal

ToolHandler = Callable[[dict[str, Any]], tuple[object, list[str]]]


class ToolRegistry:
    def __init__(self) -> None:
        self._contracts: dict[str, ToolContract] = {}
        self._handlers: dict[str, ToolHandler] = {}

    def register(self, contract: ToolContract, handler: ToolHandler) -> None:
        if contract.name in self._contracts:
            raise ValueError(f"Duplicate tool registration: {contract.name}")
        self._contracts[contract.name] = contract
        self._handlers[contract.name] = handler

    def get(self, name: str) -> ToolContract | None:
        return self._contracts.get(name)

    def list(self) -> list[ToolContract]:
        return [self._contracts[name] for name in sorted(self._contracts)]

    def invoke(
        self,
        request: ToolRequest,
        *,
        allowed_tools: set[str] | frozenset[str],
        remaining_seconds: float,
    ) -> ToolResult:
        started = monotonic()
        contract = self._contracts.get(request.tool_name)
        if contract is None or request.tool_name not in allowed_tools:
            return self._denied(request, started, "TOOL_NOT_ALLOWED")
        if contract.approval_required:
            code = "APPROVAL_REQUIRED" if not request.approval_id else "APPROVAL_NOT_VERIFIED"
            return self._denied(request, started, code)
        if remaining_seconds <= 0:
            return ToolResult(
                tool_call_id=request.tool_call_id,
                status="TIMEOUT",
                error={"code": "RUN_DEADLINE_EXCEEDED"},
            )
        try:
            result, evidence = self._handlers[request.tool_name](request.arguments)
            return ToolResult(
                tool_call_id=request.tool_call_id,
                status="SUCCEEDED",
                result=result,
                evidence_refs=sorted(set(evidence)),
                duration_ms=int((monotonic() - started) * 1000),
            )
        except (KeyError, TypeError, ValueError, RuntimeError) as exc:
            return ToolResult(
                tool_call_id=request.tool_call_id,
                status="FAILED",
                error={"code": type(exc).__name__, "message": str(exc)},
                duration_ms=int((monotonic() - started) * 1000),
            )

    @staticmethod
    def arguments_digest(arguments: dict[str, Any]) -> str:
        canonical = repr(sorted(arguments.items())).encode("utf-8")
        return sha256(canonical).hexdigest()

    @staticmethod
    def _denied(request: ToolRequest, started: float, code: str) -> ToolResult:
        return ToolResult(
            tool_call_id=request.tool_call_id,
            status="DENIED",
            error={"code": code},
            duration_ms=int((monotonic() - started) * 1000),
        )


def build_graph_tool_registry(store: GraphStore) -> ToolRegistry:
    """Create the default versioned read-tool registry over the graph port."""
    registry = ToolRegistry()

    def register(name: str, description: str, handler: ToolHandler) -> None:
        registry.register(ToolContract(name=name, description=description), handler)

    def entity(arguments: dict) -> tuple[object, list[str]]:
        canonical_id = str(arguments["canonical_id"])
        vertex = store.get_vertex_by_canonical_id(canonical_id)
        return vertex, [canonical_id] if vertex else []

    def impact(arguments: dict) -> tuple[object, list[str]]:
        canonical_id = str(arguments["canonical_id"])
        max_depth = min(int(arguments.get("max_depth", 4)), 8)
        result = GraphTraversal(store, max_results=100).impact(canonical_id, max_depth=max_depth)
        evidence = {
            edge["properties"].get("source_ref")
            for item in result["impacted"]
            for edge in item["path"]["edges"]
            if edge["properties"].get("source_ref")
        }
        return result, sorted(evidence)

    def path(arguments: dict) -> tuple[object, list[str]]:
        result = GraphTraversal(store, max_results=100).find_path(
            str(arguments["source_id"]),
            str(arguments["target_id"]),
            max_depth=min(int(arguments.get("max_depth", 8)), 8),
        )
        evidence = [] if result is None else sorted({
            edge["properties"].get("source_ref")
            for edge in result["edges"]
            if edge["properties"].get("source_ref")
        })
        return result, evidence

    def search(arguments: dict) -> tuple[object, list[str]]:
        label = arguments.get("label")
        limit = min(int(arguments.get("limit", 100)), 500)
        vertices = store.find_vertices(label=label, limit=limit)
        refs = [item["properties"].get("canonical_id", item["vid"]) for item in vertices]
        return vertices, refs

    register("entity", "Read one canonical graph entity", entity)
    register("impact", "Run bounded impact traversal", impact)
    register("path", "Find a bounded graph path", path)
    register("search", "Read a bounded set of graph entities", search)
    register("lineage", "Trace bounded source lineage", impact)
    register("evidence", "Read evidence-bearing graph entities", search)
    register("quality", "Read bounded graph facts for quality review", search)
    register("ontology", "Read bounded graph facts for ontology review", search)
    register("connector_status", "Read ingestion status entities", search)
    register("similarity", "Read bounded facts for similarity analysis", search)
    register("community", "Read bounded facts for community analysis", search)
    register("anomaly", "Read bounded facts for anomaly analysis", search)
    register("test_coverage", "Read bounded facts for test coverage analysis", search)
    register("incident_correlation", "Read bounded facts for incident correlation", search)

    from eoip.agents.mcp_pr_tools import MCPPRToolHandler
    pr_handler = MCPPRToolHandler(store)
    register("list_prs", "List pull requests in repository", pr_handler.list_prs)
    register("get_pr_impact", "Calculate cross-repo graph impact of a pull request", pr_handler.get_pr_impact)
    register("triage_prs", "Triage and rank multiple pull requests by graph impact risk", pr_handler.triage_prs)

    return registry

