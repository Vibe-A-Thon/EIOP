import time
import pytest
from eoip.agents.memory import StreamingAgentMemory
from eoip.moonshot.streaming_agent_memory import (
    ConflictResolver,
    DualTimelineIndex,
    MemoryEventType,
    SalienceDecayFunction,
    StreamingMemoryIngester,
    TemporalMemoryEvent,
)


@pytest.mark.req("KGR-G-014")
def test_streaming_agent_memory_dual_timeline_indexing():
    index = DualTimelineIndex()
    # Event 1: event_time 100, ingestion_time 200
    e1 = TemporalMemoryEvent(
        event_id="e1",
        agent_id="agent-alpha",
        event_type=MemoryEventType.OBSERVATION,
        content={"fact": "Service X deployed"},
        event_time=100.0,
        ingestion_time=200.0,
    )
    # Event 2: event_time 150, ingestion_time 250
    e2 = TemporalMemoryEvent(
        event_id="e2",
        agent_id="agent-alpha",
        event_type=MemoryEventType.INFERENCE,
        content={"fact": "Service X unhealthy"},
        event_time=150.0,
        ingestion_time=250.0,
    )
    index.insert(e1)
    index.insert(e2)

    # Query event_time axis
    events_by_event_time = index.query_event_time_range(90.0, 120.0)
    assert len(events_by_event_time) == 1
    assert events_by_event_time[0].event_id == "e1"

    # Query ingestion_time axis
    events_by_ingestion_time = index.query_ingestion_time_range(240.0, 260.0)
    assert len(events_by_ingestion_time) == 1
    assert events_by_ingestion_time[0].event_id == "e2"


@pytest.mark.req("KGR-G-014")
def test_streaming_agent_memory_conflict_resolution():
    resolver = ConflictResolver()
    old_event = TemporalMemoryEvent(
        event_id="fact-1",
        agent_id="agent-alpha",
        event_type=MemoryEventType.OBSERVATION,
        content={"version": "1.0"},
        event_time=100.0,
        salience=0.5,
    )
    # Correction event overrides observation
    correction = TemporalMemoryEvent(
        event_id="fact-1",
        agent_id="agent-alpha",
        event_type=MemoryEventType.CORRECTION,
        content={"version": "2.0"},
        event_time=105.0,
        salience=0.5,
    )
    winner = resolver.resolve(old_event, correction)
    assert winner is correction

    # Higher salience overrides lower
    newer_salient = TemporalMemoryEvent(
        event_id="fact-2",
        agent_id="agent-alpha",
        event_type=MemoryEventType.OBSERVATION,
        content={"status": "critical"},
        event_time=110.0,
        salience=0.9,
    )
    old_salient = TemporalMemoryEvent(
        event_id="fact-2",
        agent_id="agent-alpha",
        event_type=MemoryEventType.OBSERVATION,
        content={"status": "normal"},
        event_time=100.0,
        salience=0.4,
    )
    assert resolver.resolve(old_salient, newer_salient) is newer_salient


@pytest.mark.req("KGR-G-014")
def test_streaming_agent_memory_decay_and_pruning():
    decay = SalienceDecayFunction(half_life_seconds=10.0, min_salience=0.05)
    # After 1 half-life (10s), salience is halved
    salience_10s = decay.compute(1.0, 10.0)
    assert pytest.approx(salience_10s, 0.05) == 0.5

    # After 5 half-lives (50s), salience reaches minimum threshold
    salience_50s = decay.compute(1.0, 50.0)
    assert salience_50s <= 0.05
    assert decay.should_evict(salience_50s)


@pytest.mark.req("KGR-G-014")
def test_streaming_agent_memory_integration():
    memory = StreamingAgentMemory()
    t0 = time.time()

    # Record observations
    memory.record_memory(
        "agent-1",
        {"target": "db-primary", "metric": "cpu", "value": 85},
        event_time=t0,
        salience=0.8,
    )
    memory.record_memory(
        "agent-1",
        {"target": "db-primary", "metric": "memory", "value": 70},
        event_time=t0 + 10,
        salience=0.6,
    )

    # Query dual-timeline
    results = memory.query_dual_timeline(
        event_time_range=(t0 - 5, t0 + 15),
    )
    assert len(results) == 2

    # Query agent context sorted by salience
    context = memory.get_agent_context("agent-1", max_events=10, min_salience=0.1)
    assert len(context) == 2
    assert context[0].content["metric"] == "cpu"  # Higher salience first
