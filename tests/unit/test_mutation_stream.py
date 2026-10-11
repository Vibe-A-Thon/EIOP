import pytest
import time
from eoip.streaming.mutation_stream import (
    MutationEvent,
    MutationType,
    SubscriptionFilter,
    MutationEventBus,
    WebhookConfig,
)


@pytest.mark.req("KGR-G-020")
def test_mutation_event_sse_and_serialization():
    event = MutationEvent(
        event_id="evt-1",
        mutation_type=MutationType.VERTEX_CREATED,
        entity_type="Service",
        entity_id="svc:payment",
        tenant_id="tenant-alpha",
        after={"name": "Payment Service", "tier": 1},
    )

    sse_data = event.to_sse()
    assert "event: VERTEX_CREATED" in sse_data
    assert "tenant-alpha" in sse_data
    assert "svc:payment" in sse_data

    d = event.to_dict()
    assert d["event_id"] == "evt-1"
    assert d["mutation_type"] == "VERTEX_CREATED"
    assert d["entity_type"] == "Service"
    assert d["tenant_id"] == "tenant-alpha"


@pytest.mark.req("KGR-G-020")
def test_subscription_filter():
    f = SubscriptionFilter(
        tenant_ids={"tenant-1"},
        mutation_types={MutationType.VERTEX_UPDATED},
        entity_types={"Service"},
        entity_id_prefix="svc:",
    )

    evt_match = MutationEvent(
        event_id="e1",
        mutation_type=MutationType.VERTEX_UPDATED,
        entity_type="Service",
        entity_id="svc:auth",
        tenant_id="tenant-1",
    )
    assert f.matches(evt_match)

    evt_mismatch_tenant = MutationEvent(
        event_id="e2",
        mutation_type=MutationType.VERTEX_UPDATED,
        entity_type="Service",
        entity_id="svc:auth",
        tenant_id="tenant-2",
    )
    assert not f.matches(evt_mismatch_tenant)

    evt_mismatch_type = MutationEvent(
        event_id="e3",
        mutation_type=MutationType.EDGE_CREATED,
        entity_type="Service",
        entity_id="svc:auth",
        tenant_id="tenant-1",
    )
    assert not f.matches(evt_mismatch_type)


@pytest.mark.req("KGR-G-020")
def test_mutation_event_bus_sse_delivery_and_replay():
    bus = MutationEventBus()
    sub_filter = SubscriptionFilter(entity_types={"Service"})
    sub = bus.subscribe_sse("sub-1", sub_filter)

    received_listener = []
    bus.add_listener(lambda e: received_listener.append(e.event_id))

    evt = MutationEvent(
        event_id="evt-live-1",
        mutation_type=MutationType.VERTEX_CREATED,
        entity_type="Service",
        entity_id="svc:inventory",
    )
    bus.publish(evt)

    # Verify listener received event
    assert len(received_listener) == 1
    assert received_listener[0] == "evt-live-1"

    # Verify queue received event
    queued_event = sub.queue.get(timeout=2.0)
    assert queued_event is not None
    assert queued_event.event_id == "evt-live-1"

    # Verify replay
    replayed = bus.replay(sub_filter)
    assert len(replayed) == 1
    assert replayed[0].event_id == "evt-live-1"

    assert bus.stats["total_events"] == 1
    assert bus.stats["active_sse_subscriptions"] == 1

    bus.unsubscribe_sse("sub-1")
    assert bus.stats["active_sse_subscriptions"] == 0


@pytest.mark.req("KGR-G-020")
def test_webhook_registration():
    bus = MutationEventBus()
    cfg = WebhookConfig(
        webhook_id="wh-test",
        url="http://localhost:9999/hook",
        filter=SubscriptionFilter(),
        secret="test-secret",
    )
    bus.register_webhook(cfg)
    assert bus.stats["active_webhooks"] == 1

    assert bus.unregister_webhook("wh-test")
    assert bus.stats["active_webhooks"] == 0
