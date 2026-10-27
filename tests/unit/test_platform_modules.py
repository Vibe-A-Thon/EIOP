"""Tests for all new platform modules — notifications, scheduling, incidents,
imports, model management, reasoning, maintenance, streaming, compliance, integrations.
"""

import time
import pytest

from eoip.notifications.hub import (
    NotificationHub, NotificationChannel, NotificationPriority, NotificationCategory,
)
from eoip.scheduling.executor import TaskExecutor, TaskStatus
from eoip.incidents.manager import (
    IncidentManager, IncidentSeverity, IncidentState,
)
from eoip.imports.engine import ImportEngine, ColumnMapping, ImportStatus
from eoip.model_management.registry import (
    ModelRegistry, ModelStatus, GuardrailAction,
)
from eoip.reasoning.knowledge_reasoning import (
    KnowledgeReasoningEngine, RuleType,
)
from eoip.maintenance.autonomous import MaintenanceEngine
from eoip.streaming.event_stream import EventStream, StreamChannel
from eoip.compliance.extended_packs import extended_packs, extended_pack_by_framework
from eoip.integrations.bus import (
    IntegrationBus, ConnectorConfig, ConnectorStatus, SyncDirection,
)


# ── Notification Hub ──────────────────────────────────────────────────

class TestNotificationHub:
    def setup_method(self):
        self.hub = NotificationHub()

    def test_send_and_inbox(self):
        n = self.hub.send("alice", "Test Subject", "Body text")
        assert n is not None
        inbox = self.hub.get_inbox("alice")
        assert len(inbox) == 1
        assert inbox[0].subject == "Test Subject"

    def test_mark_read(self):
        n = self.hub.send("alice", "S", "B")
        assert self.hub.get_unread_count("alice") == 1
        self.hub.mark_read(n.notification_id)
        assert self.hub.get_unread_count("alice") == 0

    def test_mark_all_read(self):
        self.hub.send("alice", "S1", "B1")
        self.hub.send("alice", "S2", "B2")
        count = self.hub.mark_all_read("alice")
        assert count == 2
        assert self.hub.get_unread_count("alice") == 0

    def test_channel_preference_filtering(self):
        self.hub.set_preferences("bob", enabled_channels={NotificationChannel.EMAIL})
        n = self.hub.send("bob", "S", "B", channel=NotificationChannel.IN_APP)
        assert n is None

    def test_urgent_bypasses_preferences(self):
        self.hub.set_preferences("bob", enabled_channels={NotificationChannel.EMAIL})
        n = self.hub.send("bob", "Urgent", "B",
                         channel=NotificationChannel.IN_APP,
                         priority=NotificationPriority.URGENT)
        assert n is not None

    def test_muted_category(self):
        self.hub.set_preferences("carol",
                                muted_categories={NotificationCategory.SYSTEM})
        n = self.hub.send("carol", "S", "B", category=NotificationCategory.SYSTEM)
        assert n is None

    def test_template_rendering(self):
        tmpl = self.hub.register_template(
            "welcome", "Welcome $name", "Hello $name, your account $action",
        )
        n = self.hub.send_from_template(tmpl.template_id, "alice",
                                        {"name": "Alice", "action": "is ready"})
        assert n is not None
        assert n.subject == "Welcome Alice"
        assert "is ready" in n.body

    def test_broadcast(self):
        results = self.hub.broadcast(["alice", "bob", "carol"], "Alert", "System down")
        assert len(results) == 3

    def test_digest_mode(self):
        self.hub.set_preferences("dave", digest_enabled=True)
        n = self.hub.send("dave", "S", "B")
        assert n is not None
        assert not n.delivered
        delivered = self.hub.flush_digest("dave")
        assert len(delivered) == 1
        assert delivered[0].delivered

    def test_delete(self):
        n = self.hub.send("alice", "S", "B")
        assert self.hub.delete(n.notification_id)
        assert len(self.hub.get_inbox("alice")) == 0

    def test_stats(self):
        self.hub.send("alice", "S", "B")
        stats = self.hub.stats()
        assert stats["total_sent"] == 1


# ── Scheduled Task Executor ──────────────────────────────────────────

class TestTaskExecutor:
    def setup_method(self):
        self.executor = TaskExecutor()

    def test_register_and_execute(self):
        task = self.executor.register("cleanup", lambda: "done", description="test")
        result = self.executor.execute(task.task_id)
        assert result.status == TaskStatus.COMPLETED
        assert result.output == "done"

    def test_failure_tracking(self):
        task = self.executor.register("fail", lambda: 1/0, max_retries=0)
        result = self.executor.execute(task.task_id)
        assert result.status == TaskStatus.FAILED
        assert task.total_failures == 1

    def test_retry_on_failure(self):
        counter = {"n": 0}
        def flaky():
            counter["n"] += 1
            if counter["n"] < 3:
                raise RuntimeError("not yet")
            return "ok"
        task = self.executor.register("flaky", flaky, max_retries=3,
                                      retry_delay_seconds=0.01)
        result = self.executor.execute(task.task_id)
        assert result.status == TaskStatus.COMPLETED
        assert result.attempt == 3

    def test_history(self):
        task = self.executor.register("hist", lambda: 42)
        self.executor.execute(task.task_id)
        self.executor.execute(task.task_id)
        history = self.executor.get_history(task.task_id)
        assert len(history) == 2

    def test_enable_disable(self):
        task = self.executor.register("toggle", lambda: 1, interval_seconds=60)
        assert task.enabled
        self.executor.disable(task.task_id)
        assert not task.enabled
        self.executor.enable(task.task_id)
        assert task.enabled

    def test_list_tasks(self):
        self.executor.register("a", lambda: 1, tags=["cleanup"])
        self.executor.register("b", lambda: 2, tags=["sync"])
        assert len(self.executor.list_tasks()) == 2
        assert len(self.executor.list_tasks(tag="cleanup")) == 1

    def test_remove(self):
        task = self.executor.register("temp", lambda: 1)
        assert self.executor.remove(task.task_id)
        assert self.executor.get(task.task_id) is None

    def test_stats(self):
        task = self.executor.register("s", lambda: 1)
        self.executor.execute(task.task_id)
        stats = self.executor.stats()
        assert stats["total_runs"] == 1
        assert stats["total_successes"] == 1


# ── Incident Management ──────────────────────────────────────────────

class TestIncidentManager:
    def setup_method(self):
        self.mgr = IncidentManager()

    def test_create_incident(self):
        inc = self.mgr.create("API down", "500 errors", IncidentSeverity.SEV1, "alice")
        assert inc.state == IncidentState.OPEN
        assert len(inc.timeline) == 1

    def test_state_transitions(self):
        inc = self.mgr.create("Outage", "desc", IncidentSeverity.SEV2, "alice")
        self.mgr.transition(inc.incident_id, IncidentState.ACKNOWLEDGED, "bob")
        assert inc.state == IncidentState.ACKNOWLEDGED
        self.mgr.transition(inc.incident_id, IncidentState.INVESTIGATING, "bob")
        assert inc.state == IncidentState.INVESTIGATING
        self.mgr.transition(inc.incident_id, IncidentState.RESOLVED, "bob")
        assert inc.state == IncidentState.RESOLVED
        assert inc.resolved_at is not None

    def test_invalid_transition(self):
        inc = self.mgr.create("Test", "desc", IncidentSeverity.SEV3, "alice")
        result = self.mgr.transition(inc.incident_id, IncidentState.RESOLVED, "bob")
        assert result is None

    def test_escalation(self):
        inc = self.mgr.create("Slow", "desc", IncidentSeverity.SEV3, "alice")
        self.mgr.escalate(inc.incident_id, IncidentSeverity.SEV1, "mgr", "getting worse")
        assert inc.severity == IncidentSeverity.SEV1
        assert inc.escalation_count == 1

    def test_assignment(self):
        inc = self.mgr.create("Bug", "desc", IncidentSeverity.SEV4, "alice")
        self.mgr.assign(inc.incident_id, "bob", "alice")
        assert inc.assignee == "bob"

    def test_post_mortem(self):
        inc = self.mgr.create("Outage", "desc", IncidentSeverity.SEV1, "alice")
        self.mgr.transition(inc.incident_id, IncidentState.INVESTIGATING, "alice")
        self.mgr.transition(inc.incident_id, IncidentState.RESOLVED, "alice")
        self.mgr.attach_post_mortem(
            inc.incident_id, "API timeout cascade", "connection pool exhaustion",
            "30min downtime", "DB connections pooled to API",
            ["Add connection pool monitoring"],
            [{"action": "Add pool size alert", "owner": "bob"}],
            "alice",
        )
        assert inc.post_mortem is not None
        assert inc.post_mortem.root_cause == "connection pool exhaustion"

    def test_timeline(self):
        inc = self.mgr.create("Bug", "desc", IncidentSeverity.SEV3, "alice")
        self.mgr.add_update(inc.incident_id, "bob", "investigating logs")
        self.mgr.transition(inc.incident_id, IncidentState.INVESTIGATING, "bob")
        assert len(inc.timeline) >= 3

    def test_list_by_state(self):
        self.mgr.create("A", "a", IncidentSeverity.SEV1, "alice")
        inc2 = self.mgr.create("B", "b", IncidentSeverity.SEV2, "bob")
        self.mgr.transition(inc2.incident_id, IncidentState.ACKNOWLEDGED, "bob")
        open_incs = self.mgr.list_incidents(state=IncidentState.OPEN)
        assert len(open_incs) == 1

    def test_stats(self):
        self.mgr.create("A", "a", IncidentSeverity.SEV1, "alice")
        stats = self.mgr.stats()
        assert stats["total_incidents"] == 1


# ── Data Import Engine ────────────────────────────────────────────────

class TestImportEngine:
    def setup_method(self):
        self.engine = ImportEngine()

    def test_csv_import(self):
        csv_data = "name,email\nAlice,alice@test.com\nBob,bob@test.com"
        mappings = [
            ColumnMapping("name", "display_name"),
            ColumnMapping("email", "email_address"),
        ]
        result = self.engine.import_csv(csv_data, "user", mappings)
        assert result.status == ImportStatus.COMPLETED
        assert result.imported_rows == 2

    def test_json_import(self):
        json_data = '[{"id": 1, "value": "x"}, {"id": 2, "value": "y"}]'
        mappings = [
            ColumnMapping("id", "entity_id", transform="to_int"),
            ColumnMapping("value", "data"),
        ]
        result = self.engine.import_json(json_data, "record", mappings)
        assert result.imported_rows == 2

    def test_dry_run(self):
        csv_data = "name\nAlice"
        result = self.engine.import_csv(csv_data, "user", [], dry_run=True)
        assert result.status == ImportStatus.DRY_RUN
        assert result.imported_rows == 0
        assert result.valid_rows == 1

    def test_validation_required_field(self):
        validator = self.engine.register_validator("user")
        validator.add_field_rule("name", "string", required=True)
        csv_data = "name,email\n,alice@test.com\nBob,bob@test.com"
        result = self.engine.import_csv(csv_data, "user",
                                        [ColumnMapping("name", "name"),
                                         ColumnMapping("email", "email")])
        assert result.invalid_rows == 1
        assert result.imported_rows == 1
        assert result.status == ImportStatus.PARTIAL

    def test_validation_range(self):
        validator = self.engine.register_validator("metric")
        validator.add_field_rule("score", "float", min_val=0, max_val=100)
        json_data = '[{"score": "50"}, {"score": "150"}]'
        result = self.engine.import_json(json_data, "metric",
                                         [ColumnMapping("score", "score")])
        assert len(result.validation_issues) == 1

    def test_transform_lowercase(self):
        csv_data = "name\nALICE"
        mappings = [ColumnMapping("name", "name", transform="lowercase")]
        self.engine.import_csv(csv_data, "entity", mappings)
        records = self.engine.get_imported_records("entity")
        assert records[0]["name"] == "alice"

    def test_list_jobs(self):
        self.engine.import_csv("a\n1", "t", [])
        assert len(self.engine.list_jobs()) == 1

    def test_stats(self):
        self.engine.import_csv("a\n1", "t", [])
        stats = self.engine.stats()
        assert stats["total_jobs"] == 1


# ── AI Model Registry ────────────────────────────────────────────────

class TestModelRegistry:
    def setup_method(self):
        self.reg = ModelRegistry()

    def test_register_and_get(self):
        m = self.reg.register("gpt-4", "LLM", "openai", description="main model")
        assert m.model_id
        assert self.reg.get(m.model_id) is not None

    def test_activate_and_deprecate(self):
        m = self.reg.register("model-a", "LLM", "anthropic")
        self.reg.activate(m.model_id)
        assert m.status == ModelStatus.ACTIVE
        self.reg.deprecate(m.model_id)
        assert m.status == ModelStatus.DEPRECATED

    def test_prompt_versioning(self):
        m = self.reg.register("model-a", "LLM", "anthropic")
        pv1 = self.reg.add_prompt_version(m.model_id,
            "Answer: $question", ["question"], "alice", set_active=True)
        pv2 = self.reg.add_prompt_version(m.model_id,
            "You are helpful. Answer: $question", ["question"],
            "bob", change_note="improved prompt")
        assert pv1.is_active
        assert pv2.version == 2
        self.reg.set_active_prompt(m.model_id, 2)
        assert not pv1.is_active
        assert pv2.is_active

    def test_guardrails(self):
        m = self.reg.register("model-a", "LLM", "anthropic")
        self.reg.add_guardrail(m.model_id, "Max Length", "limit input",
                              "max_length", parameters={"max_length": 10})
        results = self.reg.check_guardrails(m.model_id, "short")
        assert all(r.passed for r in results)
        results = self.reg.check_guardrails(m.model_id, "x" * 100)
        assert not results[0].passed

    def test_blocked_words_guardrail(self):
        m = self.reg.register("model-b", "LLM", "anthropic")
        self.reg.add_guardrail(m.model_id, "No PII", "block PII",
                              "blocked_words",
                              parameters={"words": ["password", "ssn"]})
        results = self.reg.check_guardrails(m.model_id, "my password is 123")
        assert not results[0].passed

    def test_invocation_tracking(self):
        m = self.reg.register("model-a", "LLM", "anthropic")
        self.reg.add_prompt_version(m.model_id, "t", [], "alice", set_active=True)
        self.reg.record_invocation(m.model_id, 150.0, tokens=100)
        self.reg.record_invocation(m.model_id, 250.0, tokens=200, error=True)
        assert m.total_invocations == 2
        assert m.total_errors == 1
        assert m.avg_latency_ms == 200.0

    def test_list_models(self):
        self.reg.register("a", "LLM", "openai")
        self.reg.register("b", "embedding", "anthropic")
        assert len(self.reg.list_models()) == 2
        assert len(self.reg.list_models(model_type="LLM")) == 1

    def test_stats(self):
        self.reg.register("a", "LLM", "openai")
        stats = self.reg.stats()
        assert stats["total_models"] == 1


# ── Knowledge Reasoning ──────────────────────────────────────────────

class TestKnowledgeReasoning:
    def setup_method(self):
        self.engine = KnowledgeReasoningEngine()

    def test_add_rule_and_inference(self):
        self.engine.add_rule("transitive_manages", RuleType.TRANSITIVE,
            {"relation": "manages"},
            {"relation": "manages", "inferred": True})
        facts = [
            {"entity_id": "a", "relation": "manages", "target": "b"},
            {"entity_id": "b", "relation": "manages", "target": "c"},
        ]
        results = self.engine.run_inference(facts)
        assert len(results) >= 1

    def test_temporal_facts(self):
        now = time.time()
        self.engine.add_temporal_fact("e1", "status", "active",
                                     valid_from=now - 100)
        self.engine.add_temporal_fact("e1", "status", "inactive",
                                     valid_from=now + 100)
        current = self.engine.get_temporal_state("e1")
        assert len(current) == 1
        assert current[0].value == "active"

    def test_temporal_history(self):
        self.engine.add_temporal_fact("e1", "role", "engineer",
                                     valid_from=1000, valid_to=2000)
        self.engine.add_temporal_fact("e1", "role", "manager",
                                     valid_from=2000)
        history = self.engine.get_temporal_history("e1", "role")
        assert len(history) == 2
        assert history[0].value == "engineer"

    def test_temporal_conflicts(self):
        now = time.time()
        self.engine.add_temporal_fact("e1", "status", "active",
                                     valid_from=now - 100)
        self.engine.add_temporal_fact("e1", "status", "inactive",
                                     valid_from=now - 50)
        conflicts = self.engine.detect_temporal_conflicts("e1")
        assert len(conflicts) == 1

    def test_counterfactual(self):
        facts = [
            {"entity_id": "srv1", "type": "service", "status": "running"},
            {"entity_id": "srv2", "type": "service", "status": "running"},
        ]
        scenario = self.engine.counterfactual(
            "What if srv1 goes down?",
            [{"action": "modify", "entity_id": "srv1",
              "changes": {"status": "down"}}],
            facts,
        )
        assert scenario.scenario_id
        assert "srv1" in scenario.affected_entities

    def test_stats(self):
        self.engine.add_rule("r1", RuleType.TRANSITIVE, {}, {})
        stats = self.engine.stats()
        assert stats["total_rules"] == 1


# ── Autonomous Maintenance ───────────────────────────────────────────

class TestMaintenanceEngine:
    def setup_method(self):
        self.engine = MaintenanceEngine()

    def test_register_and_get_health(self):
        health = self.engine.register_entity("e1", "Person", 0.9)
        assert health.current_confidence == 0.9

    def test_decay_policy(self):
        self.engine.add_decay_policy("person_decay", "Person", half_life_days=30)
        old_time = time.time() - (60 * 86400)
        self.engine.register_entity("e1", "Person", 0.9,
                                    last_verified_at=old_time)
        health = self.engine.apply_decay("e1")
        assert health.current_confidence < 0.9
        assert health.decay_applied

    def test_staleness_scan(self):
        old = time.time() - (45 * 86400)
        self.engine.register_entity("e1", "Person", 0.8, last_verified_at=old)
        self.engine.register_entity("e2", "Person", 0.9)
        report = self.engine.scan_staleness(stale_threshold_days=30)
        assert report.stale_entities == 1
        assert report.total_entities == 2

    def test_verify_entity_resets_decay(self):
        old = time.time() - (60 * 86400)
        self.engine.add_decay_policy("p", "Person", half_life_days=30)
        self.engine.register_entity("e1", "Person", 0.9, last_verified_at=old)
        self.engine.apply_decay("e1")
        health_before = self.engine.get_entity_health("e1")
        assert health_before.current_confidence < 0.9
        self.engine.verify_entity("e1")
        health_after = self.engine.get_entity_health("e1")
        assert health_after.current_confidence == 0.9

    def test_enrichment_queue(self):
        action = self.engine.queue_enrichment("e1", "re-verify", "Check source", priority=5)
        queue = self.engine.get_enrichment_queue(status="PENDING")
        assert len(queue) == 1
        self.engine.process_enrichment(action.action_id, "verified OK")
        queue = self.engine.get_enrichment_queue(status="PENDING")
        assert len(queue) == 0

    def test_stats(self):
        self.engine.register_entity("e1", "Person", 0.8)
        stats = self.engine.stats()
        assert stats["total_entities"] == 1


# ── Event Streaming ──────────────────────────────────────────────────

class TestEventStream:
    def setup_method(self):
        self.stream = EventStream(buffer_size=100)

    def test_publish_and_replay(self):
        ev = self.stream.publish(StreamChannel.GRAPH_CHANGES, "entity.created",
                                {"id": "e1"})
        assert ev.sequence == 1
        events = self.stream.replay(StreamChannel.GRAPH_CHANGES)
        assert len(events) == 1

    def test_subscribe_and_receive(self):
        received = []
        self.stream.subscribe(StreamChannel.ALERTS, "alice",
                             callback=lambda e: received.append(e))
        self.stream.publish(StreamChannel.ALERTS, "threshold.exceeded",
                           {"metric": "cpu", "value": 95})
        assert len(received) == 1
        assert received[0].payload["metric"] == "cpu"

    def test_event_type_filter(self):
        received = []
        self.stream.subscribe(StreamChannel.GRAPH_CHANGES, "alice",
                             callback=lambda e: received.append(e),
                             event_types={"entity.deleted"})
        self.stream.publish(StreamChannel.GRAPH_CHANGES, "entity.created", {})
        self.stream.publish(StreamChannel.GRAPH_CHANGES, "entity.deleted", {})
        assert len(received) == 1

    def test_pause_resume(self):
        received = []
        sub = self.stream.subscribe(StreamChannel.SYSTEM, "alice",
                                   callback=lambda e: received.append(e))
        self.stream.pause_subscription(sub.subscription_id)
        self.stream.publish(StreamChannel.SYSTEM, "heartbeat", {})
        assert len(received) == 0
        self.stream.resume_subscription(sub.subscription_id)
        self.stream.publish(StreamChannel.SYSTEM, "heartbeat", {})
        assert len(received) == 1

    def test_unsubscribe(self):
        received = []
        sub = self.stream.subscribe(StreamChannel.ALERTS, "alice",
                                   callback=lambda e: received.append(e))
        self.stream.unsubscribe(sub.subscription_id)
        self.stream.publish(StreamChannel.ALERTS, "test", {})
        assert len(received) == 0

    def test_get_latest(self):
        for i in range(10):
            self.stream.publish(StreamChannel.GRAPH_CHANGES, "ev", {"i": i})
        latest = self.stream.get_latest(StreamChannel.GRAPH_CHANGES, limit=5)
        assert len(latest) == 5

    def test_stats(self):
        self.stream.publish(StreamChannel.ALERTS, "test", {})
        stats = self.stream.stats()
        assert stats["total_published"] == 1


# ── Extended Compliance Packs ─────────────────────────────────────────

class TestExtendedCompliancePacks:
    def test_four_packs_available(self):
        packs = extended_packs()
        assert len(packs) == 4
        frameworks = {p.framework for p in packs}
        assert "CCPA" in frameworks
        assert "PCI-DSS" in frameworks
        assert "NIST-CSF" in frameworks
        assert "ISO42001" in frameworks

    def test_each_pack_has_10_controls(self):
        for pack in extended_packs():
            assert len(pack.controls) >= 10, f"{pack.framework} has {len(pack.controls)} controls"

    def test_pack_by_framework(self):
        ccpa = extended_pack_by_framework("ccpa")
        assert ccpa is not None
        assert ccpa.framework == "CCPA"

    def test_controls_have_evidence(self):
        for pack in extended_packs():
            for ctrl in pack.controls:
                assert len(ctrl.evidence) > 0, f"{ctrl.control_id} has no evidence"

    def test_nonexistent_framework(self):
        assert extended_pack_by_framework("FAKE") is None


# ── Integration Bus ──────────────────────────────────────────────────

class TestIntegrationBus:
    def setup_method(self):
        self.bus = IntegrationBus()

    def test_register_connector(self):
        config = ConnectorConfig("postgresql", "Main DB", endpoint="localhost:5432")
        conn = self.bus.register(config)
        assert conn.connector_id
        assert conn.status == ConnectorStatus.REGISTERED

    def test_health_check_with_fn(self):
        config = ConnectorConfig("api", "External API")
        conn = self.bus.register(config, health_fn=lambda: True)
        status = self.bus.check_health(conn.connector_id)
        assert status == ConnectorStatus.HEALTHY

    def test_health_check_failure(self):
        config = ConnectorConfig("api", "Bad API")
        conn = self.bus.register(config, health_fn=lambda: False)
        self.bus.check_health(conn.connector_id)
        self.bus.check_health(conn.connector_id)
        self.bus.check_health(conn.connector_id)
        assert conn.status == ConnectorStatus.ERROR

    def test_sync(self):
        config = ConnectorConfig("db", "Test DB")
        conn = self.bus.register(config, sync_fn=lambda batch: (batch, 0))
        record = self.bus.sync(conn.connector_id)
        assert record.status == "COMPLETED"
        assert record.records_processed == 100

    def test_sync_failure(self):
        config = ConnectorConfig("db", "Bad DB")
        conn = self.bus.register(config, sync_fn=lambda b: (_ for _ in ()).throw(RuntimeError("fail")))
        record = self.bus.sync(conn.connector_id)
        assert record.status == "FAILED"
        assert conn.total_errors == 1

    def test_disconnect(self):
        config = ConnectorConfig("api", "API")
        conn = self.bus.register(config)
        self.bus.disconnect(conn.connector_id)
        assert conn.status == ConnectorStatus.DISCONNECTED

    def test_list_connectors(self):
        self.bus.register(ConnectorConfig("api", "A"))
        self.bus.register(ConnectorConfig("db", "B"))
        assert len(self.bus.list_connectors()) == 2
        assert len(self.bus.list_connectors(connector_type="api")) == 1

    def test_sync_history(self):
        config = ConnectorConfig("db", "DB")
        conn = self.bus.register(config, sync_fn=lambda b: (b, 0))
        self.bus.sync(conn.connector_id)
        self.bus.sync(conn.connector_id)
        history = self.bus.get_sync_history(conn.connector_id)
        assert len(history) == 2

    def test_stats(self):
        self.bus.register(ConnectorConfig("api", "A"))
        stats = self.bus.stats()
        assert stats["total_connectors"] == 1
