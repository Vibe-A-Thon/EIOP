"""Tests for the 5 previously-missing feature tiers.

Covers:
- Edge Deployment & Offline Mode (Tier 2)
- SDK & API Gateway (Tier 7)
- Semantic Vector Search (Tier 8)
- WAL & Disaster Recovery (Tier 9)
- Cognitive Copilot (Tier 11)
"""

from __future__ import annotations

import time
import unittest


# ═══════════════════════════════════════════════════════════════════════
# Tier 2: Edge Deployment & Offline Mode
# ═══════════════════════════════════════════════════════════════════════


class TestEdgeNodeRegistration(unittest.TestCase):
    def setUp(self):
        from eoip.edge.runtime import EdgeSyncProtocol
        self.runtime = EdgeSyncProtocol()

    def test_register_node(self):
        node = self.runtime.register_node("edge-1", "NYC Edge", "us-east")
        self.assertEqual(node.node_id, "edge-1")
        self.assertEqual(node.region, "us-east")
        self.assertEqual(node.status.value, "OFFLINE")

    def test_list_nodes_by_region(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        self.runtime.register_node("e2", "London", "eu-west")
        self.runtime.register_node("e3", "Virginia", "us-east")
        us = self.runtime.list_nodes(region="us-east")
        self.assertEqual(len(us), 2)

    def test_decommission_node(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        self.assertTrue(self.runtime.decommission_node("e1"))
        node = self.runtime.get_node("e1")
        self.assertEqual(node.status.value, "DECOMMISSIONED")

    def test_decommission_prevents_sync(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        self.runtime.decommission_node("e1")
        result = self.runtime.sync_node("e1")
        self.assertFalse(result.success)


class TestEdgeSyncProtocol(unittest.TestCase):
    def setUp(self):
        from eoip.edge.runtime import EdgeSyncProtocol, SyncDelta
        self.runtime = EdgeSyncProtocol()
        self.SyncDelta = SyncDelta

    def test_sync_with_incoming_deltas(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        deltas = [
            self.SyncDelta(entity_id="ent-1", operation="INSERT",
                           payload={"name": "Test", "type": "Service"}, version=1),
            self.SyncDelta(entity_id="ent-2", operation="INSERT",
                           payload={"name": "Test2", "type": "Service"}, version=1),
        ]
        result = self.runtime.sync_node("e1", incoming_deltas=deltas)
        self.assertTrue(result.success)
        self.assertEqual(result.deltas_received, 2)

    def test_offline_query_after_sync(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        deltas = [
            self.SyncDelta(entity_id="ent-1", operation="INSERT",
                           payload={"name": "Alpha", "type": "Service"}, version=1),
            self.SyncDelta(entity_id="ent-2", operation="INSERT",
                           payload={"name": "Beta", "type": "Person"}, version=1),
        ]
        self.runtime.sync_node("e1", incoming_deltas=deltas)
        results = self.runtime.offline_query("e1", entity_type="Service")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["name"], "Alpha")

    def test_enqueue_and_sync_outbound(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        self.runtime.enqueue_delta("e1", self.SyncDelta(
            entity_id="local-1", operation="INSERT",
            payload={"name": "EdgeDiscovery"}, version=1,
        ))
        result = self.runtime.sync_node("e1")
        self.assertEqual(result.deltas_sent, 1)

    def test_version_conflict_detection(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        self.runtime.sync_node("e1", incoming_deltas=[
            self.SyncDelta(entity_id="ent-1", operation="INSERT",
                           payload={"v": 1}, version=5),
        ])
        result = self.runtime.sync_node("e1", incoming_deltas=[
            self.SyncDelta(entity_id="ent-1", operation="UPDATE",
                           payload={"v": 2}, version=3),
        ])
        self.assertGreater(result.conflicts, 0)

    def test_promote_to_cloud(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        self.runtime.sync_node("e1", incoming_deltas=[
            self.SyncDelta(entity_id="ent-1", operation="INSERT",
                           payload={"name": "Discovered"}, version=1),
        ])
        promo = self.runtime.promote_to_cloud("e1", ["ent-1"])
        self.assertEqual(promo["promoted"], 1)

    def test_sync_history(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        self.runtime.sync_node("e1")
        self.runtime.sync_node("e1")
        history = self.runtime.get_sync_history("e1")
        self.assertEqual(len(history), 2)

    def test_nodes_needing_sync(self):
        self.runtime.register_node("e1", "NYC", "us-east",
                                          sync_interval=0)
        needing = self.runtime.nodes_needing_sync()
        self.assertIn("e1", needing)

    def test_stats(self):
        self.runtime.register_node("e1", "NYC", "us-east")
        stats = self.runtime.stats()
        self.assertEqual(stats["total_nodes"], 1)


# ═══════════════════════════════════════════════════════════════════════
# Tier 7: SDK & API Gateway
# ═══════════════════════════════════════════════════════════════════════


class TestAPIGateway(unittest.TestCase):
    def setUp(self):
        from eoip.sdk.gateway import (
            APIGateway, SchemaType, SchemaField, RateLimitPolicy,
        )
        self.gw = APIGateway()
        self.SchemaType = SchemaType
        self.SchemaField = SchemaField
        self.RateLimitPolicy = RateLimitPolicy
        self.gw.register_type(SchemaType(
            name="Service",
            description="A microservice",
            fields=[
                SchemaField("name", "String", False, "Service name"),
                SchemaField("status", "String", True, "Current status"),
                SchemaField("owner", "String", True, "Owner team"),
            ],
        ))
        self.gw.register_data_source("Service", [
            {"name": "auth-svc", "status": "healthy", "owner": "platform"},
            {"name": "billing-svc", "status": "degraded", "owner": "finance"},
            {"name": "search-svc", "status": "healthy", "owner": "platform"},
        ])

    def test_execute_simple_query(self):
        result = self.gw.execute("Service() { name, status }")
        self.assertEqual(len(result.data), 3)
        self.assertIn("name", result.data[0])

    def test_execute_filtered_query(self):
        result = self.gw.execute('Service(owner: platform) { name }')
        self.assertEqual(len(result.data), 2)

    def test_introspect(self):
        schema = self.gw.introspect()
        self.assertIn("Service", schema["types"])
        self.assertEqual(len(schema["types"]["Service"]["fields"]), 3)

    def test_introspect_single_type(self):
        t = self.gw.introspect_type("Service")
        self.assertIsNotNone(t)
        self.assertEqual(t["name"], "Service")

    def test_openapi_export(self):
        spec = self.gw.export_openapi_spec()
        self.assertEqual(spec["openapi"], "3.1.0")
        self.assertIn("Service", spec["components"]["schemas"])

    def test_playground_metadata(self):
        meta = self.gw.playground_metadata()
        self.assertIn("Service", meta["available_types"])
        self.assertTrue(len(meta["example_queries"]) > 0)

    def test_rate_limiting_allows(self):
        self.gw.set_rate_limit(self.RateLimitPolicy(
            name="test", requests_per_second=100, burst_size=50,
        ))
        result = self.gw.execute("Service() { name }")
        self.assertFalse(result.errors)

    def test_rate_limiting_blocks(self):
        self.gw.set_rate_limit(self.RateLimitPolicy(
            name="strict", requests_per_second=0.001, burst_size=1,
        ))
        self.gw.execute("Service() { name }", client_id="c1")
        result = self.gw.execute("Service() { name }", client_id="c1")
        self.assertTrue(any("Rate limited" in e for e in result.errors))

    def test_query_log(self):
        self.gw.execute("Service() { name }")
        log = self.gw.query_log()
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0]["root_type"], "Service")

    def test_stats(self):
        stats = self.gw.stats()
        self.assertEqual(stats["registered_types"], 1)
        self.assertEqual(stats["total_records"], 3)


# ═══════════════════════════════════════════════════════════════════════
# Tier 8: Semantic Vector Search
# ═══════════════════════════════════════════════════════════════════════


class TestSemanticVectorIndex(unittest.TestCase):
    def setUp(self):
        from eoip.search.semantic import SemanticVectorIndex
        self.idx = SemanticVectorIndex(dim=64)

    def test_index_and_search(self):
        self.idx.index_entity("e1", "machine learning algorithms")
        self.idx.index_entity("e2", "deep learning neural networks")
        self.idx.index_entity("e3", "database optimization queries")
        results = self.idx.search_by_text("neural network", top_k=2)
        self.assertGreater(len(results), 0)

    def test_find_similar(self):
        self.idx.index_entity("e1", "kubernetes container orchestration")
        self.idx.index_entity("e2", "docker container runtime")
        self.idx.index_entity("e3", "financial reporting system")
        similar = self.idx.find_similar("e1", top_k=2)
        self.assertGreater(len(similar), 0)
        self.assertNotEqual(similar[0].entity_id, "e1")

    def test_filter_by_type(self):
        self.idx.index_entity("e1", "auth service", entity_type="Service")
        self.idx.index_entity("e2", "auth person", entity_type="Person")
        results = self.idx.search_by_text("auth", entity_type="Service")
        self.assertTrue(all(r.entity_type == "Service" for r in results))

    def test_filter_by_language(self):
        self.idx.index_entity("e1", "service mesh", language="en")
        self.idx.index_entity("e2", "maillage de services", language="fr")
        results = self.idx.similarity_search(
            self.idx._entities["e1"].vector, language="fr",
        )
        self.assertTrue(all(r.language == "fr" for r in results))

    def test_hybrid_search(self):
        self.idx.index_entity("e1", "kubernetes pod scaling")
        self.idx.index_entity("e2", "database query optimization")
        results = self.idx.hybrid_search("kubernetes scaling")
        self.assertGreater(len(results), 0)
        self.assertGreater(results[0].combined_score, 0)

    def test_remove_entity(self):
        self.idx.index_entity("e1", "test entity")
        self.assertTrue(self.idx.remove_entity("e1"))
        results = self.idx.search_by_text("test entity")
        self.assertEqual(len(results), 0)

    def test_snapshot_and_drift(self):
        self.idx.index_entity("e1", "original concept")
        self.idx.save_snapshot("v1")
        self.idx.index_entity("e1", "completely different meaning")
        self.idx.save_snapshot("v2")
        drifts = self.idx.detect_drift("v1", "v2", threshold=0.01)
        self.assertGreater(len(drifts), 0)
        self.assertGreater(drifts[0].drift_distance, 0)

    def test_cross_lingual_search(self):
        self.idx.index_entity("e1", "authentication service", language="en")
        self.idx.index_entity("e2", "service authentification", language="fr")
        results = self.idx.cross_lingual_search("auth service", ["en", "fr"])
        self.assertIn("en", results)
        self.assertIn("fr", results)

    def test_dimension_mismatch_raises(self):
        with self.assertRaises(ValueError):
            self.idx.index_entity("e1", "test", vector=[0.1, 0.2])

    def test_stats(self):
        self.idx.index_entity("e1", "test", entity_type="Service")
        stats = self.idx.stats()
        self.assertEqual(stats["total_entities"], 1)
        self.assertEqual(stats["dimension"], 64)


# ═══════════════════════════════════════════════════════════════════════
# Tier 9: WAL & Disaster Recovery
# ═══════════════════════════════════════════════════════════════════════


class TestWriteAheadLog(unittest.TestCase):
    def setUp(self):
        from eoip.recovery.wal import WriteAheadLog, RecoveryConfig, WALOperationType
        self.wal = WriteAheadLog(RecoveryConfig(
            segment_size=5, max_wal_entries=100,
        ))
        self.WALOperationType = WALOperationType

    def test_append_increments_lsn(self):
        e1 = self.wal.append(self.WALOperationType.INSERT, "Service", "svc-1", {"name": "auth"})
        e2 = self.wal.append(self.WALOperationType.INSERT, "Service", "svc-2", {"name": "billing"})
        self.assertEqual(e1.lsn, 1)
        self.assertEqual(e2.lsn, 2)

    def test_read_from_lsn(self):
        for i in range(10):
            self.wal.append(self.WALOperationType.INSERT, "Service", f"svc-{i}", {})
        entries = self.wal.read_from(5)
        self.assertTrue(all(e.lsn >= 5 for e in entries))

    def test_segment_sealing(self):
        for i in range(12):
            self.wal.append(self.WALOperationType.INSERT, "Service", f"svc-{i}", {})
        segments = self.wal.list_segments()
        self.assertGreater(len(segments), 0)
        self.assertTrue(segments[0].sealed)

    def test_checkpoint_and_restore(self):
        for i in range(5):
            self.wal.append(self.WALOperationType.INSERT, "Service", f"svc-{i}", {})
        cp = self.wal.checkpoint("before-migration")
        for i in range(5):
            self.wal.append(self.WALOperationType.DELETE, "Service", f"svc-{i}", {})
        result = self.wal.recover_to_point(cp.point_id)
        self.assertTrue(result["success"])
        self.assertEqual(result["target_lsn"], 5)

    def test_restore_invalid_checkpoint(self):
        result = self.wal.recover_to_point("nonexistent")
        self.assertFalse(result["success"])

    def test_recover_to_timestamp(self):
        self.wal.append(self.WALOperationType.INSERT, "Service", "svc-1", {})
        result = self.wal.recover_to_timestamp(time.time() + 1)
        self.assertTrue(result["success"])

    def test_entry_checksum(self):
        e = self.wal.append(self.WALOperationType.INSERT, "Service", "svc-1", {})
        self.assertTrue(len(e.checksum) > 0)


class TestReplication(unittest.TestCase):
    def setUp(self):
        from eoip.recovery.wal import (
            WriteAheadLog, RecoveryConfig, WALOperationType, ReplicationRole,
        )
        self.wal = WriteAheadLog(RecoveryConfig(segment_size=100))
        self.WALOperationType = WALOperationType
        self.ReplicationRole = ReplicationRole

    def test_add_peer(self):
        peer = self.wal.add_peer("standby-1", self.ReplicationRole.STANDBY,
                                 "https://standby1:8443")
        self.assertEqual(peer.state.value, "HEALTHY")

    def test_ack_updates_lag(self):
        self.wal.add_peer("s1", self.ReplicationRole.STANDBY, "https://s1:8443")
        for i in range(10):
            self.wal.append(self.WALOperationType.INSERT, "Service", f"svc-{i}", {})
        self.wal.ack_peer("s1", 7)
        peer = self.wal._peers["s1"]
        self.assertEqual(peer.lag_entries, 3)

    def test_promote_standby(self):
        self.wal.add_peer("s1", self.ReplicationRole.STANDBY, "https://s1:8443")
        result = self.wal.promote_standby("s1")
        self.assertTrue(result["success"])
        self.assertEqual(result["new_primary"], "s1")

    def test_promote_non_standby_fails(self):
        self.wal.add_peer("w1", self.ReplicationRole.WITNESS, "https://w1:8443")
        result = self.wal.promote_standby("w1")
        self.assertFalse(result["success"])

    def test_remove_peer(self):
        self.wal.add_peer("s1", self.ReplicationRole.STANDBY, "https://s1:8443")
        self.assertTrue(self.wal.remove_peer("s1"))
        self.assertFalse(self.wal.remove_peer("s1"))

    def test_rpo_status(self):
        self.wal.append(self.WALOperationType.INSERT, "Service", "svc-1", {})
        self.wal.checkpoint()
        status = self.wal.rpo_status()
        self.assertIn("rpo_target_seconds", status)
        self.assertIn("within_rpo", status)

    def test_stats(self):
        self.wal.append(self.WALOperationType.INSERT, "Service", "svc-1", {})
        stats = self.wal.stats()
        self.assertEqual(stats["current_lsn"], 1)
        self.assertEqual(stats["role"], "PRIMARY")


# ═══════════════════════════════════════════════════════════════════════
# Tier 11: Cognitive Copilot
# ═══════════════════════════════════════════════════════════════════════


class TestConversationMemory(unittest.TestCase):
    def setUp(self):
        from eoip.copilot.engine import ConversationMemory
        self.mem = ConversationMemory(max_turns=50)

    def test_add_turn(self):
        turn = self.mem.add_turn("user", "What is ServiceA?", entities=["ServiceA"])
        self.assertEqual(turn.role, "user")
        self.assertIn("ServiceA", turn.entities_mentioned)

    def test_context_window(self):
        for i in range(20):
            self.mem.add_turn("user", f"Message {i}")
        window = self.mem.get_context_window(last_n=5)
        self.assertEqual(len(window), 5)

    def test_entity_frequency(self):
        self.mem.add_turn("user", "Check ServiceA", entities=["ServiceA"])
        self.mem.add_turn("user", "Check ServiceA again", entities=["ServiceA"])
        self.mem.add_turn("user", "Check ServiceB", entities=["ServiceB"])
        top = self.mem.top_entities(2)
        self.assertEqual(top[0][0], "ServiceA")
        self.assertEqual(top[0][1], 2)

    def test_topic_shift_detection(self):
        for i in range(6):
            ents = ["TopicA"] if i < 3 else ["TopicZ"]
            self.mem.add_turn("user", f"msg {i}", entities=ents)
        self.assertTrue(self.mem.detect_topic_shift(window=3))

    def test_summarize(self):
        self.mem.add_turn("user", "hello", entities=["Svc"])
        summary = self.mem.summarize()
        self.assertEqual(summary["total_turns"], 1)
        self.assertEqual(summary["unique_entities"], 1)


class TestCopilotEngine(unittest.TestCase):
    def setUp(self):
        from eoip.copilot.engine import CopilotEngine
        self.copilot = CopilotEngine()

    def test_process_message_detects_intent(self):
        result = self.copilot.process_message(
            "s1", "user", "What is the status of ServiceA?",
        )
        self.assertEqual(result["intent"], "question")
        self.assertGreater(result["confidence"], 0)

    def test_process_message_extracts_entities(self):
        result = self.copilot.process_message(
            "s1", "user", 'Show me details about "AuthService"',
        )
        self.assertIn("AuthService", result["detected_entities"])

    def test_suggest_questions(self):
        self.copilot.process_message("s1", "user", "Tell me about ServiceA",)
        self.copilot._sessions["s1"].add_turn(
            "user", "details", entities=["ServiceA"],
        )
        suggestions = self.copilot.suggest_questions("s1")
        self.assertGreater(len(suggestions), 0)
        self.assertTrue(any("ServiceA" in s.question for s in suggestions))

    def test_generate_staleness_insight(self):
        insights = self.copilot.generate_insights(
            entity_stats={"total_entities": 100, "stale_count": 40},
        )
        self.assertGreater(len(insights), 0)
        self.assertEqual(insights[0].insight_type.value, "WARNING")

    def test_generate_orphan_insight(self):
        insights = self.copilot.generate_insights(
            entity_stats={"total_entities": 50, "stale_count": 0,
                          "orphan_count": 5, "orphan_ids": ["a", "b"]},
        )
        anomalies = [i for i in insights if i.insight_type.value == "ANOMALY"]
        self.assertGreater(len(anomalies), 0)

    def test_generate_graph_density_insight(self):
        insights = self.copilot.generate_insights(
            graph_stats={"node_count": 100, "edge_count": 10},
        )
        opps = [i for i in insights if i.insight_type.value == "OPPORTUNITY"]
        self.assertGreater(len(opps), 0)

    def test_dismiss_insight(self):
        self.copilot.generate_insights(
            entity_stats={"total_entities": 100, "stale_count": 50},
        )
        insights = self.copilot.get_insights()
        self.assertTrue(self.copilot.dismiss_insight(insights[0].insight_id))
        active = self.copilot.get_insights(include_dismissed=False)
        dismissed_ids = {i.insight_id for i in insights[:1]}
        self.assertTrue(all(i.insight_id not in dismissed_ids for i in active))

    def test_automation_rule_trigger(self):
        self.copilot.add_rule(
            name="alert-on-incident",
            trigger_pattern=r"\bincident\b",
            action_template="Escalate to on-call",
        )
        result = self.copilot.process_message(
            "s1", "user", "We have an incident with the auth service",
        )
        self.assertGreater(len(result["triggered_rules"]), 0)

    def test_automation_rule_cooldown(self):
        self.copilot.add_rule(
            name="test", trigger_pattern=r"fire",
            action_template="action", cooldown_seconds=3600,
        )
        self.copilot.process_message("s1", "user", "fire alert")
        result2 = self.copilot.process_message("s1", "user", "fire again")
        self.assertEqual(len(result2["triggered_rules"]), 0)

    def test_disable_enable_rule(self):
        rule = self.copilot.add_rule("r1", r"test", "action")
        self.assertTrue(self.copilot.disable_rule(rule.rule_id))
        result = self.copilot.process_message("s1", "user", "test message")
        self.assertEqual(len(result["triggered_rules"]), 0)
        self.copilot.enable_rule(rule.rule_id)
        result2 = self.copilot.process_message("s2", "user", "test message")
        self.assertGreater(len(result2["triggered_rules"]), 0)

    def test_list_sessions(self):
        self.copilot.process_message("s1", "user", "hello")
        self.copilot.process_message("s2", "user", "world")
        sessions = self.copilot.list_sessions()
        self.assertEqual(len(sessions), 2)

    def test_end_session(self):
        self.copilot.process_message("s1", "user", "hello")
        self.assertTrue(self.copilot.end_session("s1"))
        self.assertFalse(self.copilot.end_session("s1"))

    def test_stats(self):
        self.copilot.process_message("s1", "user", "hello")
        self.copilot.add_rule("r1", r"x", "action")
        stats = self.copilot.stats()
        self.assertEqual(stats["active_sessions"], 1)
        self.assertEqual(stats["automation_rules"], 1)


if __name__ == "__main__":
    unittest.main()
