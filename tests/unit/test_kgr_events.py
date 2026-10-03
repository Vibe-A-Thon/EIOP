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
