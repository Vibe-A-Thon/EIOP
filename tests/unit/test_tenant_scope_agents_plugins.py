"""SR-TEN-001: tenant context is carried by agent tool calls and plugin invocations."""

from __future__ import annotations

import time

import pytest
from pydantic import ValidationError

from eoip.agents.runtime import AgentExecutionContext
from eoip.agents.tools import ToolRegistry
from eoip.contracts.agent import AgentBudgets, AgentContract, AgentRequest
from eoip.contracts.tenant_scope import current_tenant, tenant_scope
from eoip.contracts.tool import ToolContract, ToolRequest


def _registry(seen: list[str]) -> ToolRegistry:
    registry = ToolRegistry()

    def handler(args):
        seen.append(current_tenant())
        return {"ok": True}, []

    registry.register(ToolContract(name="probe", description="records the ambient tenant"), handler)
    return registry


@pytest.mark.req("SR-TEN-001")
def test_agent_tool_calls_run_and_are_recorded_under_the_request_tenant():
    seen: list[str] = []
    request = AgentRequest(request_id="r1", agent_id="a1", goal="g", actor_id="u1", tenant_id="acme")
    ctx = AgentExecutionContext(
        run_id="run-1", request=request,
        contract=AgentContract(agent_id="a1", purpose="p", allowed_tools=["probe"]),
        budgets=AgentBudgets(), tools=_registry(seen), deadline=time.monotonic() + 10,
        emit=lambda *a, **k: None,
    )
    result = ctx.use_tool("probe", {})
    assert result.status == "SUCCEEDED"
    assert seen == ["acme"]
    assert ctx.tool_calls[-1]["tenant_id"] == "acme"
    assert current_tenant() == "_platform"  # scope does not leak after the call


@pytest.mark.req("SR-TEN-001")
def test_tenant_context_is_never_blank():
    assert AgentRequest(request_id="r", agent_id="a", goal="g").tenant_id == "_platform"
    with pytest.raises(ValidationError):
        AgentRequest(request_id="r", agent_id="a", goal="g", tenant_id="")
    with pytest.raises(ValidationError):
        ToolRequest(tool_call_id="c", tool_name="t", arguments={}, tenant_id="")
    with pytest.raises(ValueError):
        with tenant_scope("  "):
            pass


@pytest.mark.req("SR-TEN-001")
def test_plugin_invocations_carry_the_tenant_into_the_sandbox_thread():
    from eoip.plugins.runtime import PluginRuntime

    class _Instance:
        status = None

        def _record_invocation(self):
            pass

        def _record_error(self, msg):
            pass

        def whoami(self):
            return current_tenant()

    from eoip.plugins.sdk import PluginStatus

    runtime = PluginRuntime()
    inst = _Instance()
    inst.status = PluginStatus.ACTIVE

    class _Loaded:
        instance = inst

    runtime._plugins["p1"] = _Loaded()
    assert runtime.execute_plugin("p1", "whoami", invocation_tenant="globex") == "globex"
    with tenant_scope("acme"):
        assert runtime.execute_plugin("p1", "whoami") == "acme"  # inherits the caller's scope
    assert [i["tenant_id"] for i in runtime.invocations] == ["globex", "acme"]
