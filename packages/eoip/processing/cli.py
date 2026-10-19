"""CLI commands for EOIP Processing Runtime (PU-W15).

Provides command-line subcommands for discovering capabilities, enumerating devices,
probing profiles, and executing processing operators locally.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import List, Optional

from eoip.processing.catalog import get_operator_spec, get_unit_capabilities, list_operator_specs
from eoip.processing.contracts import ExecutionContext, LogicalUnit, ProcessingRequest
from eoip.processing.devices import enumerate_devices
from eoip.processing.service import get_processing_service


def processing_cli_main(args: List[str]) -> int:
    parser = argparse.ArgumentParser(prog="eoip processing", description="EOIP Processing Runtime CLI")
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # capabilities
    cap_parser = subparsers.add_parser("capabilities", help="List processing units and operators")
    cap_parser.add_argument("--unit", choices=[u.value for u in LogicalUnit], help="Filter by logical unit")
    cap_parser.add_argument("--json", action="store_true", help="Output as raw JSON")

    # devices
    dev_parser = subparsers.add_parser("devices", help="List computing devices and acceleration hardware")
    dev_parser.add_argument("--json", action="store_true", help="Output as raw JSON")

    # probe
    probe_parser = subparsers.add_parser("probe", help="Probe an execution profile")
    probe_parser.add_argument("profile_id", help="Profile ID to probe (e.g. cpu, directml, openvino, qiskit_aer)")

    # run
    run_parser = subparsers.add_parser("run", help="Execute an operator directly")
    run_parser.add_argument("operator_id", help="ID of operator to execute (e.g. records.validate, vector.cosine_top_k)")
    run_parser.add_argument("--params", default="{}", help="JSON string of operator parameters")
    run_parser.add_argument("--inputs", default="{}", help="JSON string of operator inputs")
    run_parser.add_argument("--tenant", default="cli_tenant", help="Tenant ID")

    parsed = parser.parse_args(args)
    service = get_processing_service()

    if parsed.subcommand == "capabilities":
        caps = get_unit_capabilities()
        if parsed.unit:
            filtered = {k: v for k, v in caps.items() if k == parsed.unit}
            if parsed.json:
                print(json.dumps(filtered, indent=2))
            else:
                for unit_name, data in filtered.items():
                    print(f"[{unit_name}] {data['display_name']} ({data['operator_count']} operators)")
                    for op in data["operators"]:
                        print(f"  - {op}")
        else:
            if parsed.json:
                print(json.dumps(caps, indent=2))
            else:
                print("EOIP Processing Runtime Units & Capabilities:")
                for unit_name, data in caps.items():
                    sim_tag = " (Simulated)" if data.get("simulated") else ""
                    print(f"  • {unit_name}: {data['display_name']} - {data['operator_count']} operators{sim_tag}")
        return 0

    elif parsed.subcommand == "devices":
        devices = enumerate_devices()
        dev_dicts = [d.model_dump() for d in devices]
        if parsed.json:
            print(json.dumps(dev_dicts, indent=2))
        else:
            print(f"Discovered Computing Devices ({len(devices)}):")
            for d in devices:
                print(f"  - [{d.device_id}] {d.vendor} {d.model} ({d.device_type.upper()}) | Cores: {d.usable_cores} | RAM: {d.usable_memory_mib} MiB")
        return 0

    elif parsed.subcommand == "probe":
        probe_res = service.probe_profile(parsed.profile_id)
        print(json.dumps(probe_res, indent=2))
        return 0

    elif parsed.subcommand == "run":
        spec = get_operator_spec(parsed.operator_id)
        if not spec:
            print(f"Error: Unknown operator '{parsed.operator_id}'", file=sys.stderr)
            return 1
        try:
            params = json.loads(parsed.params)
            inputs = json.loads(parsed.inputs)
        except json.JSONDecodeError as exc:
            print(f"Error: Invalid JSON input: {exc}", file=sys.stderr)
            return 1

        req = ProcessingRequest(
            logical_unit=spec.logical_unit,
            operator_id=spec.operator_id,
            parameters=params,
            inputs=inputs,
        )
        ctx = ExecutionContext(
            tenant_id=parsed.tenant,
            principal_id="cli_user",
        )
        try:
            result, receipt = service.execute_direct(req, ctx)
            output = {
                "result": result,
                "receipt": receipt.model_dump(),
            }
            print(json.dumps(output, indent=2))
            return 0
        except Exception as exc:
            print(f"Execution failed: {exc}", file=sys.stderr)
            return 2

    return 0
