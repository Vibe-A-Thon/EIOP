"""Command line interface for REVA (T-216 / REVA-MC-007 / §9.3)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Optional
import click

from reva.core.time import format_ts, utc_now_ms
from reva.kernel.kernel import WarrantKernel
from reva.kernel.store import RevaStore
from reva.kernel.translog import MerkleLog
from reva.pd.closure import ClosureContext, evaluate_closure
from reva.pd.export_html import render_ledger_html
from reva.pd.gates import evaluate_gate, load_gate_definition
from reva.pd.ledger import LedgerRecord, build_ledger
from reva.pd.obligations import Obligation, load_obligations, sync_obligations
from reva.sandbox.attest import verify_dsse_attestation
from reva.workflows.doctor import run_doctor


def get_default_store(tenant_id: str = "default") -> RevaStore:
    db_path = Path.home() / ".reva" / f"{tenant_id}.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return RevaStore(str(db_path))


@click.group()
@click.option("--tenant", default="default", help="REVA tenant identifier")
@click.option("--json", "json_mode", is_flag=True, help="Emit JSON output")
@click.pass_context
def cli(ctx: click.Context, tenant: str, json_mode: bool):
    """REVA — Verification, Evidence, and Assurance CLI."""
    ctx.ensure_object(dict)
    ctx.obj["tenant"] = tenant
    ctx.obj["json_mode"] = json_mode


@cli.command()
@click.pass_context
def doctor(ctx: click.Context):
    """Diagnose installation and runtime readiness."""
    tenant = ctx.obj["tenant"]
    json_mode = ctx.obj["json_mode"]
    store = get_default_store(tenant)
    translog = MerkleLog(store)

    report = run_doctor(store, translog, tenant_id=tenant)
    if json_mode:
        click.echo(
            json.dumps({
                "healthy": report.healthy,
                "status": report.status,
                "checks": [
                    {"name": c.name, "status": c.status, "message": c.message, "details": c.details}
                    for c in report.checks
                ],
            }, indent=2)
        )
    else:
        click.echo(f"REVA Doctor Status: {report.status.upper()}")
        for c in report.checks:
            symbol = "✓" if c.status == "ok" else ("!" if c.status == "warning" else "✗")
            click.echo(f"  [{symbol}] {c.name}: {c.message}")

    if not report.healthy:
        sys.exit(1)


@cli.group()
def obligation():
    """Manage normative Proof-of-Done obligations."""
    return None


@obligation.command(name="sync")
@click.argument("yaml_file", type=click.Path(exists=True))
@click.pass_context
def obligation_sync(ctx: click.Context, yaml_file: str):
    """Load and synchronize obligations from YAML file."""
    tenant = ctx.obj["tenant"]
    json_mode = ctx.obj["json_mode"]
    store = get_default_store(tenant)

    obs = load_obligations(Path(yaml_file))
    count = sync_obligations(store, tenant, obs)

    if json_mode:
        click.echo(json.dumps({"synced_count": count}))
    else:
        click.echo(f"Successfully synced {count} obligations for tenant '{tenant}'")


@cli.group()
def closure():
    """Evaluate Proof-of-Done closure status."""
    return None


@closure.command(name="evaluate")
@click.option("--scope", default="all", help="Evaluation scope")
@click.option("--commit", default="HEAD", help="Target commit SHA")
@click.pass_context
def closure_evaluate(ctx: click.Context, scope: str, commit: str):
    """Run pure closure evaluation and generate ledger."""
    tenant = ctx.obj["tenant"]
    json_mode = ctx.obj["json_mode"]
    store = get_default_store(tenant)

    cur = store.conn.cursor()
    ob_rows = cur.execute("SELECT definition FROM reva_obligations WHERE tenant_id = ?", (tenant,)).fetchall()
    obligations = [Obligation.model_validate(json.loads(r["definition"])) for r in ob_rows]

    decisions = []
    for ob in obligations:
        ctx_eval = ClosureContext(obligation=ob, commit=commit)
        dec = evaluate_closure(ctx_eval)
        decisions.append(dec)

    ledger = build_ledger(tenant, scope, commit, decisions, store=store)

    if json_mode:
        click.echo(json.dumps(ledger.canonical_dict(), indent=2))
    else:
        click.echo(f"Ledger ID: {ledger.ledger_id}")
        click.echo(f"Complete: {ledger.complete}")
        click.echo(f"Summary: {ledger.summary}")


@cli.group()
def ledger():
    """Export and verify Proof-of-Done ledgers."""
    return None


@ledger.command(name="export")
@click.option("--scope", default="all", help="Ledger scope")
@click.option("--format", "fmt", type=click.Choice(["json", "md", "html"]), default="json")
@click.option("--out", type=click.Path(), default=None, help="Output file path")
@click.pass_context
def ledger_export(ctx: click.Context, scope: str, fmt: str, out: Optional[str]):
    """Export latest canonical ledger."""
    tenant = ctx.obj["tenant"]
    store = get_default_store(tenant)

    cur = store.conn.cursor()
    row = cur.execute(
        "SELECT record FROM reva_ledgers WHERE tenant_id = ? AND scope = ? ORDER BY created_at DESC LIMIT 1",
        (tenant, scope),
    ).fetchone()
    if not row:
        click.echo(f"No ledger found for scope '{scope}'", err=True)
        sys.exit(1)

    raw_data = json.loads(row["record"])
    closures_data = raw_data.get("closures", [])
    from reva.pd.closure import ClosureDecision
    decisions = [
        ClosureDecision(
            closure_id=c.get("closure_id", ""),
            obligation_key=c.get("obligation_key", ""),
            obligation_version=c.get("obligation_version", 1),
            commit=c.get("commit", ""),
            outcome=c.get("outcome", "open"),
            reasons=c.get("reasons", []),
            checks=[],
            inputs={},
        )
        for c in closures_data
    ]
    led = LedgerRecord(
        ledger_id=raw_data.get("ledger_id", ""),
        tenant_id=tenant,
        scope=scope,
        commit=raw_data.get("commit", ""),
        complete=raw_data.get("complete", False),
        summary=raw_data.get("summary", {}),
        closures=decisions,
        created_at=raw_data.get("created_at", ""),
    )

    if fmt == "json":
        output = json.dumps(raw_data, indent=2)
    elif fmt == "md":
        output = led.to_markdown()
    elif fmt == "html":
        output = render_ledger_html(led)

    if out:
        Path(out).write_text(output, encoding="utf-8")
        click.echo(f"Exported {fmt.upper()} to {out}")
    else:
        click.echo(output)


if __name__ == "__main__":
    cli()
