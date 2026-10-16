"""Tests for the collaboration system — annotations, workspaces, activity, shared queries."""

import time
import pytest

from eoip.collaboration.annotations import (
    AnnotationStore, AnnotationType, AnnotationSeverity, AnnotationState,
)
from eoip.collaboration.workspaces import WorkspaceStore, WorkspaceRole
from eoip.collaboration.activity import ActivityFeed, ActivityAction
from eoip.collaboration.shared_queries import SharedQueryStore


# ── Annotations ───────────────────────────────────────────────────────

class TestAnnotationStore:
    def setup_method(self):
        self.store = AnnotationStore()

    def test_create_and_get(self):
        ann = self.store.create("entity", "e1", "alice", "looks wrong")
        assert ann.annotation_id
        assert ann.body == "looks wrong"
        fetched = self.store.get(ann.annotation_id)
        assert fetched is ann

    def test_update_body_and_state(self):
        ann = self.store.create("entity", "e1", "alice", "draft")
        updated = self.store.update(ann.annotation_id, body="final", state=AnnotationState.RESOLVED)
        assert updated.body == "final"
        assert updated.state == AnnotationState.RESOLVED

    def test_delete(self):
        ann = self.store.create("entity", "e1", "alice", "temp")
        assert self.store.delete(ann.annotation_id)
        assert self.store.get(ann.annotation_id) is None

    def test_threading(self):
        parent = self.store.create("entity", "e1", "alice", "parent note")
        child = self.store.create("entity", "e1", "bob", "reply", parent_id=parent.annotation_id)
        thread = self.store.get_thread(parent.annotation_id)
        assert len(thread) == 2
        assert thread[0].annotation_id == parent.annotation_id
        assert thread[1].annotation_id == child.annotation_id

    def test_reaction(self):
        ann = self.store.create("entity", "e1", "alice", "nice")
        self.store.add_reaction(ann.annotation_id, "👍", "bob")
        self.store.add_reaction(ann.annotation_id, "👍", "bob")  # duplicate
        assert len(ann.reactions["👍"]) == 1

    def test_search_by_type_and_severity(self):
        self.store.create("entity", "e1", "alice", "finding",
                         annotation_type=AnnotationType.FINDING,
                         severity=AnnotationSeverity.HIGH)
        self.store.create("entity", "e2", "bob", "comment")
        results = self.store.search(annotation_type=AnnotationType.FINDING)
        assert len(results) == 1
        assert results[0].severity == AnnotationSeverity.HIGH

    def test_search_by_text_query(self):
        self.store.create("entity", "e1", "alice", "payment gateway issue")
        self.store.create("entity", "e2", "bob", "schema change")
        results = self.store.search(query="payment")
        assert len(results) == 1

    def test_for_target(self):
        self.store.create("entity", "e1", "alice", "first")
        self.store.create("entity", "e1", "bob", "second")
        self.store.create("edge", "r1", "carol", "edge note")
        target_anns = self.store.get_for_target("entity", "e1")
        assert len(target_anns) == 2

    def test_stats(self):
        self.store.create("entity", "e1", "alice", "a")
        self.store.create("entity", "e2", "bob", "b", annotation_type=AnnotationType.TAG)
        stats = self.store.stats()
        assert stats["total"] == 2
        assert stats["unique_authors"] == 2

    def test_to_dict(self):
        ann = self.store.create("entity", "e1", "alice", "body")
        d = ann.to_dict()
        assert d["target_type"] == "entity"
        assert d["annotation_type"] == "COMMENT"


# ── Workspaces ────────────────────────────────────────────────────────

class TestWorkspaceStore:
    def setup_method(self):
        self.store = WorkspaceStore()

    def test_create_workspace(self):
        ws = self.store.create("Team Alpha", "Alpha team workspace", "alice")
        assert ws.workspace_id
        assert ws.owner == "alice"
        assert "alice" in ws.members
        assert ws.members["alice"].role == WorkspaceRole.OWNER

    def test_add_and_remove_member(self):
        ws = self.store.create("Team", "desc", "alice")
        self.store.add_member(ws.workspace_id, "bob", role=WorkspaceRole.EDITOR, invited_by="alice")
        assert "bob" in ws.members
        assert ws.members["bob"].role == WorkspaceRole.EDITOR
        self.store.remove_member(ws.workspace_id, "bob")
        assert "bob" not in ws.members

    def test_cannot_remove_owner(self):
        ws = self.store.create("Team", "desc", "alice")
        assert not self.store.remove_member(ws.workspace_id, "alice")

    def test_update_role(self):
        ws = self.store.create("Team", "desc", "alice")
        self.store.add_member(ws.workspace_id, "bob", role=WorkspaceRole.VIEWER)
        self.store.update_role(ws.workspace_id, "bob", WorkspaceRole.EDITOR)
        assert ws.members["bob"].role == WorkspaceRole.EDITOR

    def test_permission_hierarchy(self):
        ws = self.store.create("Team", "desc", "alice")
        self.store.add_member(ws.workspace_id, "bob", role=WorkspaceRole.VIEWER)
        self.store.add_member(ws.workspace_id, "carol", role=WorkspaceRole.EDITOR)
        assert self.store.check_permission(ws.workspace_id, "alice", WorkspaceRole.OWNER)
        assert self.store.check_permission(ws.workspace_id, "carol", WorkspaceRole.EDITOR)
        assert self.store.check_permission(ws.workspace_id, "carol", WorkspaceRole.VIEWER)
        assert not self.store.check_permission(ws.workspace_id, "bob", WorkspaceRole.EDITOR)

    def test_pin_query_and_entity(self):
        ws = self.store.create("Team", "desc", "alice")
        self.store.pin_query(ws.workspace_id, "q1")
        self.store.pin_entity(ws.workspace_id, "ent1")
        assert "q1" in ws.pinned_queries
        assert "ent1" in ws.pinned_entities

    def test_list_for_user(self):
        self.store.create("WS1", "a", "alice")
        self.store.create("WS2", "b", "bob")
        ws3 = self.store.create("WS3", "c", "carol")
        self.store.add_member(ws3.workspace_id, "alice")
        assert len(self.store.list_for_user("alice")) == 2

    def test_delete_workspace(self):
        ws = self.store.create("Team", "desc", "alice")
        self.store.add_member(ws.workspace_id, "bob")
        assert self.store.delete(ws.workspace_id)
        assert self.store.get(ws.workspace_id) is None

    def test_stats(self):
        self.store.create("A", "a", "alice")
        self.store.create("B", "b", "bob")
        stats = self.store.stats()
        assert stats["total_workspaces"] == 2
        assert stats["unique_users"] == 2

    def test_to_dict(self):
        ws = self.store.create("Team", "desc", "alice")
        d = ws.to_dict()
        assert d["name"] == "Team"
        assert d["member_count"] == 1


# ── Activity Feed ─────────────────────────────────────────────────────

class TestActivityFeed:
    def setup_method(self):
        self.feed = ActivityFeed(max_events=100)

    def test_record_and_retrieve(self):
        ev = self.feed.record(
            ActivityAction.ENTITY_CREATED, "alice", "entity", "e1", "Created entity e1",
        )
        assert ev.event_id
        events = self.feed.get_feed()
        assert len(events) == 1
        assert events[0].action == ActivityAction.ENTITY_CREATED

    def test_filter_by_actor(self):
        self.feed.record(ActivityAction.ENTITY_CREATED, "alice", "entity", "e1", "alice creates")
        self.feed.record(ActivityAction.QUERY_EXECUTED, "bob", "query", "q1", "bob queries")
        assert len(self.feed.get_feed(actor="alice")) == 1

    def test_filter_by_workspace(self):
        self.feed.record(ActivityAction.ENTITY_CREATED, "alice", "entity", "e1", "a",
                        workspace_id="ws1")
        self.feed.record(ActivityAction.ENTITY_CREATED, "bob", "entity", "e2", "b",
                        workspace_id="ws2")
        assert len(self.feed.get_workspace_feed("ws1")) == 1

    def test_ring_buffer_truncation(self):
        small_feed = ActivityFeed(max_events=5)
        for i in range(10):
            small_feed.record(ActivityAction.ENTITY_CREATED, "alice", "entity", f"e{i}", f"item {i}")
        assert len(small_feed.get_feed(limit=100)) == 5

    def test_filter_by_action(self):
        self.feed.record(ActivityAction.ENTITY_CREATED, "alice", "entity", "e1", "c")
        self.feed.record(ActivityAction.QUERY_EXECUTED, "alice", "query", "q1", "q")
        results = self.feed.get_feed(action=ActivityAction.QUERY_EXECUTED)
        assert len(results) == 1

    def test_user_activity(self):
        self.feed.record(ActivityAction.ENTITY_CREATED, "alice", "entity", "e1", "a")
        self.feed.record(ActivityAction.QUERY_EXECUTED, "alice", "query", "q1", "b")
        self.feed.record(ActivityAction.ENTITY_CREATED, "bob", "entity", "e2", "c")
        assert len(self.feed.get_user_activity("alice")) == 2

    def test_stats(self):
        self.feed.record(ActivityAction.ENTITY_CREATED, "alice", "entity", "e1", "a")
        self.feed.record(ActivityAction.QUERY_EXECUTED, "bob", "query", "q1", "b")
        stats = self.feed.stats()
        assert stats["total_events"] == 2
        assert stats["unique_actors"] == 2

    def test_to_dict(self):
        ev = self.feed.record(ActivityAction.ENTITY_CREATED, "alice", "entity", "e1", "summary")
        d = ev.to_dict()
        assert d["action"] == "entity.created"
        assert d["actor"] == "alice"


# ── Shared Queries ────────────────────────────────────────────────────

class TestSharedQueryStore:
    def setup_method(self):
        self.store = SharedQueryStore()

    def test_save_and_get(self):
        sq = self.store.save("Top entities", "MATCH (n) RETURN n", "gremlin", "alice")
        assert sq.query_id
        assert sq.current_version == 1
        fetched = self.store.get(sq.query_id)
        assert fetched.name == "Top entities"

    def test_update_creates_version(self):
        sq = self.store.save("Q1", "SELECT 1", "sql", "alice")
        self.store.update(sq.query_id, "SELECT 2", "bob", change_note="fix query")
        assert sq.current_version == 2
        assert sq.query_text == "SELECT 2"

    def test_get_version(self):
        sq = self.store.save("Q1", "v1 text", "cypher", "alice")
        self.store.update(sq.query_id, "v2 text", "alice")
        v1 = self.store.get_version(sq.query_id, 1)
        v2 = self.store.get_version(sq.query_id, 2)
        assert v1.query_text == "v1 text"
        assert v2.query_text == "v2 text"

    def test_record_execution(self):
        sq = self.store.save("Q1", "MATCH (n) RETURN n", "cypher", "alice")
        self.store.record_execution(sq.query_id, "bob")
        self.store.record_execution(sq.query_id, "carol")
        assert sq.execution_count == 2
        assert sq.last_executed_by == "carol"

    def test_fork(self):
        original = self.store.save("Q1", "MATCH (n)", "cypher", "alice",
                                   tags=["graph"], description="original")
        forked = self.store.fork(original.query_id, "bob")
        assert forked.name == "Q1 (fork)"
        assert forked.forked_from == original.query_id
        assert forked.author == "bob"
        assert forked.query_text == original.query_text

    def test_search_by_name(self):
        self.store.save("Payment entities", "MATCH (p:Payment)", "cypher", "alice")
        self.store.save("User nodes", "MATCH (u:User)", "cypher", "bob")
        results = self.store.search(query="payment")
        assert len(results) == 1

    def test_search_by_language(self):
        self.store.save("SQL Q", "SELECT 1", "sql", "alice")
        self.store.save("Cypher Q", "MATCH (n)", "cypher", "bob")
        results = self.store.search(language="sql")
        assert len(results) == 1

    def test_search_by_tags(self):
        self.store.save("Q1", "q", "sql", "alice", tags=["production", "finance"])
        self.store.save("Q2", "q", "sql", "bob", tags=["staging"])
        results = self.store.search(tags=["production"])
        assert len(results) == 1

    def test_search_by_workspace(self):
        self.store.save("Q1", "q", "sql", "alice", workspace_id="ws1")
        self.store.save("Q2", "q", "sql", "bob", workspace_id="ws2")
        results = self.store.search(workspace_id="ws1", include_public=False)
        assert len(results) == 1

    def test_public_queries_included(self):
        self.store.save("Q1", "q", "sql", "alice", workspace_id="ws1")
        self.store.save("Public Q", "q", "sql", "bob", workspace_id="ws2", is_public=True)
        results = self.store.search(workspace_id="ws1", include_public=True)
        assert len(results) == 2

    def test_delete(self):
        sq = self.store.save("Q1", "q", "sql", "alice")
        assert self.store.delete(sq.query_id)
        assert self.store.get(sq.query_id) is None

    def test_stats(self):
        self.store.save("Q1", "q", "sql", "alice")
        self.store.save("Q2", "q", "cypher", "bob")
        self.store.save("Q3", "q", "sql", "alice")
        stats = self.store.stats()
        assert stats["total_queries"] == 3
        assert stats["by_language"]["sql"] == 2
        assert stats["unique_authors"] == 2

    def test_to_dict(self):
        sq = self.store.save("Q1", "MATCH (n)", "cypher", "alice", description="test")
        d = sq.to_dict()
        assert d["name"] == "Q1"
        assert d["query_language"] == "cypher"
        assert d["current_version"] == 1

    def test_search_sorted_by_execution_count(self):
        sq1 = self.store.save("Q1", "q", "sql", "alice")
        sq2 = self.store.save("Q2", "q", "sql", "bob")
        for _ in range(5):
            self.store.record_execution(sq2.query_id, "carol")
        self.store.record_execution(sq1.query_id, "carol")
        results = self.store.search()
        assert results[0].query_id == sq2.query_id
