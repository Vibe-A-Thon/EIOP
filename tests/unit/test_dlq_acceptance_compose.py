"""FT-X11 / FT-X12: DLQ acceptance stack wiring (static checks).

FT-X11: the acceptance container runs as uid 10001 and used to write its report to a
host bind mount (../test-results), which fails on Linux unless the host directory is
world-writable. Reports now go to a named volume and are copied out with `<runtime> cp`.

FT-X12: the dlq-graph healthcheck probed /versions, which answers before the graph
backend can serve schema requests, so schema-init raced the graph. It now probes the
graph schema endpoint.
"""

from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
COMPOSE = ROOT / "deploy" / "docker-compose.dlq-acceptance.yml"


def _compose() -> dict:
    return yaml.safe_load(COMPOSE.read_text(encoding="utf-8"))


def test_acceptance_results_use_named_volume_not_host_bind_mount() -> None:
    doc = _compose()
    volumes = doc["services"]["acceptance"]["volumes"]
    results = [v for v in volumes if str(v).endswith(":/results")]
    assert results == ["dlq-results:/results"], volumes
    assert "dlq-results" in doc["volumes"]


def test_test_images_create_results_dir_owned_by_runtime_user() -> None:
    for name in ("Dockerfile", "Containerfile"):
        text = (ROOT / "deploy" / name).read_text(encoding="utf-8")
        test_stage = text.split("AS test", 1)[1]
        assert "mkdir -p /results && chown eoip:eoip /results" in test_stage, name


def test_container_scripts_copy_reports_out_of_the_volume() -> None:
    sh = (ROOT / "scripts" / "container.sh").read_text(encoding="utf-8")
    ps1 = (ROOT / "scripts" / "container.ps1").read_text(encoding="utf-8")
    sh_block = sh.split("dlq-acceptance)", 1)[1].split(";;", 1)[0]
    ps1_block = ps1.split("'dlq-acceptance' {", 1)[1].split("'recovery-acceptance'", 1)[0]
    assert '$CLI_CMD cp "$RUN_ID-acceptance:/results/."' in sh_block
    assert "--rm" not in sh_block.split("run_compose run", 1)[1].split("\n", 1)[0]
    assert "'cp', \"$runId-acceptance:/results/.\"" in ps1_block
    assert "'rm', '-f', \"$runId-acceptance\"" in ps1_block


def test_graph_healthcheck_probes_schema_endpoint_not_versions() -> None:
    health = _compose()["services"]["dlq-graph"]["healthcheck"]["test"]
    probe = " ".join(health)
    assert "/versions" not in probe
    assert "/graphs/hugegraph/schema" in probe
    # $$ escapes compose interpolation, so the container shell expands PASSWORD.
    assert "-u admin:$${PASSWORD}" in probe
