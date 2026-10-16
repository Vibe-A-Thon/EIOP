"""Phase 7 tests: event emitter — subscribe, emit, poll, filter."""


import asyncio

import pytest
from eoip.events.emitter import EventType, GraphEvent, GraphEventEmitter

# --- Event emitter subscribe/unsubscribe ---

@pytest.mark.asyncio
async def test_emitter_subscribe_receives_events():
    emitter = GraphEventEmitter()
    q = emitter.subscribe()
    event = GraphEvent(type=EventType.VERTEX_UPSERTED, data={"canonical_id": "urn:a", "label": "File"})
    await emitter.emit(event)
    received = q.get_nowait()
    assert received.type == EventType.VERTEX_UPSERTED
    assert received.data["canonical_id"] == "urn:a"


@pytest.mark.asyncio
async def test_emitter_unsubscribe_stops_delivery():
    emitter = GraphEventEmitter()
    q = emitter.subscribe()
    assert emitter.subscriber_count == 1
    emitter.unsubscribe(q)
    assert emitter.subscriber_count == 0
    event = GraphEvent(type=EventType.EDGE_UPSERTED, data={})
    await emitter.emit(event)
    assert q.empty()


# --- Event serialization ---

def test_event_to_dict():
    event = GraphEvent(type="vertex_upserted", data={"canonical_id": "urn:test"}, timestamp="2026-10-03T10:00:00Z")
    d = event.to_dict()
    assert d["type"] == "vertex_upserted"
    assert d["data"]["canonical_id"] == "urn:test"
    assert d["timestamp"] == "2026-10-03T10:00:00Z"
    assert "event_id" in d


def test_event_auto_timestamp():
    event = GraphEvent(type="edge_upserted", data={})
    assert event.timestamp is not None
    assert len(event.timestamp) > 10


# --- Polling fallback ---

@pytest.mark.asyncio
async def test_poll_events_since_timestamp():
    emitter = GraphEventEmitter()
    e1 = GraphEvent(type="vertex_upserted", data={"id": "1"}, timestamp="2026-10-03T09:00:00Z")
    e2 = GraphEvent(type="edge_upserted", data={"id": "2"}, timestamp="2026-10-03T10:00:00Z")
    e3 = GraphEvent(type="vertex_deleted", data={"id": "3"}, timestamp="2026-10-03T11:00:00Z")
    await emitter.emit(e1)
    await emitter.emit(e2)
    await emitter.emit(e3)
    results = emitter.events_since("2026-10-03T09:30:00Z")
    assert len(results) == 2
    assert results[0]["data"]["id"] == "2"


@pytest.mark.asyncio
async def test_poll_events_since_id():
    emitter = GraphEventEmitter()
    e1 = GraphEvent(type="vertex_upserted", data={"a": 1})
    e2 = GraphEvent(type="edge_upserted", data={"b": 2})
    await emitter.emit(e1)
    await emitter.emit(e2)
    results = emitter.events_since_id(e1.event_id)
    assert len(results) == 1
    assert results[0]["data"]["b"] == 2


# --- Event type filtering ---

@pytest.mark.asyncio
async def test_recent_events_returns_latest():
    emitter = GraphEventEmitter(buffer_size=5)
    for i in range(10):
        await emitter.emit(GraphEvent(type="vertex_upserted", data={"i": i}))
    recent = emitter.recent_events(limit=3)
    assert len(recent) == 3
    assert recent[0]["data"]["i"] == 7


@pytest.mark.asyncio
async def test_ring_buffer_overflow():
    emitter = GraphEventEmitter(buffer_size=3)
    for i in range(5):
        await emitter.emit(GraphEvent(type="vertex_upserted", data={"i": i}))
    all_events = emitter.recent_events(limit=10)
    assert len(all_events) == 3
    assert all_events[0]["data"]["i"] == 2


@pytest.mark.asyncio
async def test_sync_emit_from_worker_thread_before_first_queue_read():
    emitter = GraphEventEmitter()
    queue = emitter.subscribe()
    event = GraphEvent("vertex_upserted", {"tenant_id": "alpha"})
    await asyncio.to_thread(emitter.emit_sync, event)
    assert await asyncio.wait_for(queue.get(), timeout=2) is event


@pytest.mark.asyncio
async def test_full_subscriber_queue_does_not_raise_in_event_loop():
    emitter = GraphEventEmitter()
    queue = emitter.subscribe()
    event = GraphEvent("vertex_upserted", {})
    for _ in range(queue.maxsize):
        queue.put_nowait(event)
    loop = asyncio.get_running_loop()
    previous = loop.get_exception_handler()
    errors = []
    loop.set_exception_handler(lambda _, context: errors.append(context))
    try:
        await asyncio.to_thread(emitter.emit_sync, event)
        await asyncio.sleep(0)
        assert not errors
        assert queue.qsize() == queue.maxsize
    finally:
        loop.set_exception_handler(previous)


@pytest.mark.parametrize("tenant", ["alpha", "default"])
def test_polling_filters_before_limit_and_rejects_ambiguous_events(tenant):
    emitter = GraphEventEmitter()
    first = GraphEvent("vertex_upserted", {"tenant_id": tenant})
    emitter.emit_sync(first)
    for data in ({}, {"tenant_id": "beta"}, {"tenant_id": tenant, "canonical_id": "g:beta:node:1"}):
        emitter.emit_sync(GraphEvent("vertex_upserted", data))
    assert emitter.recent_events(limit=1, tenant_id=tenant) == [first.to_dict()]
    assert emitter.events_since("", limit=1, tenant_id=tenant) == [first.to_dict()]
    assert emitter.events_since_id(0, limit=1, tenant_id=tenant) == [first.to_dict()]


def test_emitter_durable_journal_and_restart_recovery(tmp_path):
    journal_path = tmp_path / "events.jsonl"
    emitter1 = GraphEventEmitter(buffer_size=10, journal_path=journal_path)

    # Emit 5 events
    for i in range(5):
        emitter1.emit_sync(GraphEvent("vertex_upserted", {"val": i, "tenant_id": "alpha"}))

    assert journal_path.exists()
    lines = journal_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 5

    # Simulate restart with fresh emitter pointing at same journal
    emitter2 = GraphEventEmitter(buffer_size=10, journal_path=journal_path)
    # Verify next emitted event has strictly higher event_id
    next_event = GraphEvent("vertex_upserted", {"val": "next", "tenant_id": "alpha"})
    emitter2.emit_sync(next_event)
    assert next_event.event_id > 5

    # Verify journal has 6 lines now
    lines2 = journal_path.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines2) == 6


def test_emitter_replay_across_buffer_overflow(tmp_path):
    journal_path = tmp_path / "events.jsonl"
    # Small buffer size of 3
    emitter = GraphEventEmitter(buffer_size=3, journal_path=journal_path)

    event_ids = []
    for i in range(10):
        ev = GraphEvent("vertex_upserted", {"val": i, "tenant_id": "alpha"})
        emitter.emit_sync(ev)
        event_ids.append(ev.event_id)

    # Buffer only keeps last 3
    assert len(emitter.recent_events(limit=10, tenant_id="alpha")) == 3

    # But events_since_id from beginning can replay all 10 from journal!
    replayed = emitter.events_since_id(event_ids[0] - 1, limit=20, tenant_id="alpha")
    assert len(replayed) == 10
    assert [e["data"]["val"] for e in replayed] == list(range(10))

