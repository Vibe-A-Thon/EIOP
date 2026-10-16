import json

import pytest
from eoip.graph.memory import MemoryGraphStore

from scripts import demo_reset


def test_reset_preserves_audit_history_and_closes_store(tmp_path, monkeypatch):
    audit = tmp_path / "audit"
    audit.mkdir()
    previous = {"event_type": "previous_operation"}
    (audit / "audit.jsonl").write_text(json.dumps(previous) + "\n", encoding="utf-8")
    store = MemoryGraphStore()
    closed = []
    monkeypatch.setattr(demo_reset, "create_store", lambda: store)
    monkeypatch.setattr(store, "close", lambda: closed.append(True), raising=False)
    monkeypatch.setattr(
        demo_reset, "load_demo",
        lambda *_: {"jira": {"records_accepted": 2}, "git": {"files": 1}},
    )

    demo_reset.main(["--data-dir", str(tmp_path), "--confirm"])

    events = [json.loads(line) for line in (audit / "audit.jsonl").read_text().splitlines()]
    assert events[0] == previous
    assert [event["event_type"] for event in events[1:]] == ["demo_reset_intent", "demo_reset"]
    assert events[-1]["outcome"] == "success"
    assert closed == [True]


def test_failed_graph_clear_keeps_raw_evidence_and_reports_failure(tmp_path, monkeypatch):
    raw = tmp_path / "raw" / "jira" / "event.json"
    raw.parent.mkdir(parents=True)
    raw.write_text('{"event_id":"previous"}', encoding="utf-8")
    store = MemoryGraphStore()
    closed = []
    loaded = []
    monkeypatch.setattr(demo_reset, "create_store", lambda: store)
    monkeypatch.setattr(store, "close", lambda: closed.append(True), raising=False)
    monkeypatch.setattr(demo_reset, "load_demo", lambda *_: loaded.append(True))

    def refuse_clear():
        raise RuntimeError("Runtime graph deletion is disabled")

    monkeypatch.setattr(store, "clear", refuse_clear)
    with pytest.raises(RuntimeError, match="deletion is disabled"):
        demo_reset.main(["--data-dir", str(tmp_path), "--confirm"])
    assert json.loads(raw.read_text()) == {"event_id": "previous"}
    assert loaded == []
    assert closed == [True]
    events = [json.loads(line) for line in (tmp_path / "audit" / "audit.jsonl").read_text().splitlines()]
    assert events[-1]["outcome"] == "failure"


def test_reset_requires_confirmation_before_opening_store(tmp_path, monkeypatch):
    opened = []
    monkeypatch.setattr(demo_reset, "create_store", lambda: opened.append(True))
    with pytest.raises(SystemExit) as exc:
        demo_reset.main(["--data-dir", str(tmp_path)])
    assert exc.value.code == 2
    assert opened == []
    assert not (tmp_path / "audit").exists()


def test_failed_audit_preflight_does_not_clear_store(tmp_path, monkeypatch):
    store = MemoryGraphStore()
    vertex = store.upsert_vertex("WorkItem", {"canonical_id": "issue:1"})
    closed = []
    monkeypatch.setattr(demo_reset, "create_store", lambda: store)
    monkeypatch.setattr(store, "close", lambda: closed.append(True), raising=False)

    def refuse_audit(*_args, **_kwargs):
        raise OSError("audit disk unavailable")

    monkeypatch.setattr(demo_reset.AuditSink, "emit", refuse_audit)
    with pytest.raises(OSError, match="audit disk unavailable"):
        demo_reset.main(["--data-dir", str(tmp_path), "--confirm"])
    assert store.get_vertex(vertex["vid"]) is not None
    assert closed == [True]
