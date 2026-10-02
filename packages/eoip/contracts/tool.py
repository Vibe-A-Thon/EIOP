"""ToolRequest v1 / ToolResult v1.

Normative: EOIP-engg-doc-pkg/schemas/tool_request.schema.json,
EOIP-engg-doc-pkg/schemas/tool_result.schema.json
MVP registers read-only tools only (FR-AGENT-004, FR-MCP-002).
"""

from typing import Literal

from pydantic import BaseModel

ToolStatus = Literal["SUCCEEDED", "FAILED", "DENIED", "TIMEOUT"]


class ToolRequest(BaseModel):
    tool_call_id: str
    tool_name: str
    arguments: dict
    risk_level: str | None = None


class ToolResult(BaseModel):
    tool_call_id: str
    status: ToolStatus
    result: object | None = None
    evidence_refs: list[str] | None = None
    error: dict | None = None
