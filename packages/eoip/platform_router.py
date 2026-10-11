"""Unified platform router — aggregates all feature routers.

Wires collaboration, notifications, scheduling, incidents, imports,
model management, maintenance, streaming, compliance, integrations,
edge deployment, API gateway, semantic search, disaster recovery,
cognitive copilot, and AI/ML ops into a single FastAPI router.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field


# ── Pydantic request models (module-level for OpenAPI schema resolution) ──


class NotifSendRequest(BaseModel):
    recipient: str = Field(min_length=1)
    subject: str = Field(min_length=1, max_length=500)
    body: str = Field(min_length=1, max_length=10000)
    channel: str = Field(default="IN_APP")
    priority: str = Field(default="NORMAL")
    category: str = Field(default="SYSTEM")


class IncidentCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    description: str = Field(min_length=1, max_length=5000)
    severity: str = Field(default="SEV3")
    reporter: str = Field(min_length=1)
    assignee: str | None = None
    affected_services: list[str] = Field(default_factory=list)


class IncidentTransitionRequest(BaseModel):
    new_state: str = Field(min_length=1)
    actor: str = Field(min_length=1)
    details: str = Field(default="")


class ImportCSVRequest(BaseModel):
    csv_data: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    author: str = Field(default="")
    dry_run: bool = Field(default=False)


class EdgeNodeRequest(BaseModel):
    node_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    region: str = Field(min_length=1)
    sync_direction: str = Field(default="BIDIRECTIONAL")
    sync_interval: int = Field(default=300, ge=10)
    tags: list[str] = Field(default_factory=list)


class EdgeSyncRequest(BaseModel):
    node_id: str = Field(min_length=1)
    deltas: list[dict[str, Any]] = Field(default_factory=list)


class EdgePromoteRequest(BaseModel):
    node_id: str = Field(min_length=1)
    entity_ids: list[str] = Field(min_length=1)


class GatewayTypeRequest(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(default="")
    fields: list[dict[str, Any]] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list)


class GatewayQueryRequest(BaseModel):
    query: str = Field(min_length=1)
    client_id: str = Field(default="__anonymous__")


class SemanticIndexRequest(BaseModel):
    entity_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    entity_type: str = Field(default="")
    language: str = Field(default="en")


class SemanticSearchRequest(BaseModel):
    query_text: str = Field(min_length=1)
    top_k: int = Field(default=10, ge=1, le=100)
    entity_type: str | None = None
    min_score: float = Field(default=0.0, ge=0.0, le=1.0)


class PlatformHybridSearchRequest(BaseModel):
    query_text: str = Field(min_length=1)
    top_k: int = Field(default=10, ge=1, le=100)
    keyword_weight: float = Field(default=0.3, ge=0.0, le=1.0)
    vector_weight: float = Field(default=0.7, ge=0.0, le=1.0)


class WALAppendRequest(BaseModel):
    operation: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    entity_id: str = Field(min_length=1)
    payload: dict[str, Any] = Field(default_factory=dict)
    tenant_id: str = Field(default="default")


class WALPeerRequest(BaseModel):
    peer_id: str = Field(min_length=1)
    role: str = Field(min_length=1)
    endpoint: str = Field(min_length=1)


class CopilotMessageRequest(BaseModel):
    session_id: str = Field(min_length=1)
    role: str = Field(default="user")
    content: str = Field(min_length=1, max_length=10000)


class CopilotRuleRequest(BaseModel):
    name: str = Field(min_length=1)
    trigger_pattern: str = Field(min_length=1)
    action_template: str = Field(min_length=1)
    cooldown_seconds: float = Field(default=60.0, ge=1.0)


class CopilotInsightRequest(BaseModel):
    entity_stats: dict[str, Any] = Field(default_factory=dict)
    graph_stats: dict[str, Any] = Field(default_factory=dict)


class RLHFPreferenceRequest(BaseModel):
    prompt: str = Field(min_length=1)
    response_a: str = Field(min_length=1)
    response_b: str = Field(min_length=1)
    label: str = Field(min_length=1)
    annotator: str = Field(min_length=1)
    rationale: str = Field(default="")


class RewardScoreRequest(BaseModel):
    response: str = Field(min_length=1)
    reference: str = Field(default="")
    source_texts: list[str] = Field(default_factory=list)


class HallucinationCheckRequest(BaseModel):
    response: str = Field(min_length=1)
    source_texts: list[str] = Field(min_length=1)


class SamplingExperimentRequest(BaseModel):
    name: str = Field(min_length=1)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    top_p: float = Field(default=0.95, ge=0.0, le=1.0)
    top_k: int = Field(default=40, ge=0)
    min_p: float = Field(default=0.05, ge=0.0, le=1.0)
    repetition_penalty: float = Field(default=1.1, ge=1.0, le=3.0)


class TrialRecordRequest(BaseModel):
    experiment_id: str = Field(min_length=1)
    quality: float = Field(ge=0.0, le=1.0)
    diversity: float = Field(ge=0.0, le=1.0)
    coherence: float = Field(ge=0.0, le=1.0)


class TokenBudgetRequest(BaseModel):
    name: str = Field(min_length=1)
    max_prompt: int = Field(default=100000, ge=1)
    max_completion: int = Field(default=50000, ge=1)
    max_total: int = Field(default=150000, ge=1)


class TokenConsumeRequest(BaseModel):
    budget_id: str = Field(min_length=1)
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)


class HybridSearchIndexRequest(BaseModel):
    entity_id: str = Field(min_length=1)
    text: str = Field(min_length=1)
    entity_type: str = Field(default="")
    fields: dict[str, Any] = Field(default_factory=dict)

class HybridSearchEdgeRequest(BaseModel):
    source: str = Field(min_length=1)
    target: str = Field(min_length=1)
    label: str = Field(default="RELATED")
    weight: float = Field(default=1.0, ge=0.0)

class HybridSearchQueryRequest(BaseModel):
    query: str = Field(min_length=1)
    top_k: int = Field(default=20, ge=1, le=200)
    modalities: list[str] | None = None
    structured_filters: dict[str, Any] | None = None
    graph_seeds: list[str] | None = None
    graph_hops: int = Field(default=2, ge=1, le=5)
    user_id: str | None = None

class HybridSearchUserContextRequest(BaseModel):
    user_id: str = Field(min_length=1)
    role: str = Field(default="")
    team: str = Field(default="")
    recent_entities: list[str] = Field(default_factory=list)
    preferred_types: list[str] = Field(default_factory=list)
    search_history: list[str] = Field(default_factory=list)
    expertise_domains: list[str] = Field(default_factory=list)


class PromptRegisterRequest(BaseModel):
    name: str = Field(min_length=1)
    template: str = Field(min_length=1)
    description: str = Field(default="")
    author: str = Field(default="")
    tags: list[str] = Field(default_factory=list)


class PromptRenderRequest(BaseModel):
    name: str = Field(min_length=1)
    variables: dict[str, str] = Field(default_factory=dict)


class SecurityScanRequest(BaseModel):
    text: str = Field(min_length=1)


class CostRecordRequest(BaseModel):
    operation: str = Field(min_length=1)
    model: str = Field(min_length=1)
    tokens_in: int = Field(ge=0)
    tokens_out: int = Field(ge=0)
    cost_usd: float = Field(ge=0)
    latency_ms: float = Field(ge=0)


class ContextItemRequest(BaseModel):
    item_id: str = Field(min_length=1)
    content: str = Field(min_length=1)
    priority: str = Field(default="MEDIUM")
    source: str = Field(default="")


class MemoryStoreRequest(BaseModel):
    content: str = Field(min_length=1)
    tier: str = Field(default="working")
    tags: list[str] = Field(default_factory=list)
    ttl_seconds: float | None = None


class MemoryRecallRequest(BaseModel):
    query: str = Field(min_length=1)
    tier: str | None = None
    limit: int = Field(default=10, ge=1, le=100)


class FeatureExtractRequest(BaseModel):
    entity_id: str = Field(min_length=1)
    properties: dict[str, Any] = Field(default_factory=dict)
    neighbors: list[str] = Field(default_factory=list)


class SpecDefineRequest(BaseModel):
    name: str = Field(min_length=1)
    fields: dict[str, dict[str, Any]] = Field(default_factory=dict)
    description: str = Field(default="")


class EvalRunRequest(BaseModel):
    prompt_name: str = Field(min_length=1)
    rendered_text: str = Field(min_length=1)
    reference: str = Field(default="")


class ToolRegisterRequest(BaseModel):
    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    schema: dict[str, Any] = Field(default_factory=dict)
    version: str = Field(default="1.0.0")
    category: str = Field(default="")
    tags: list[str] = Field(default_factory=list)


def build_platform_router() -> APIRouter:
    """Build the unified platform features router."""
    router = APIRouter(prefix="/api/v1/platform", tags=["Platform"])

    # ── Notifications ─────────────────────────────────────────────────

    @router.post("/notifications/send", summary="Send notification",
                 tags=["Notifications"])
    def send_notification(req: NotifSendRequest) -> dict[str, Any]:
        from eoip.notifications.hub import (
            NotificationChannel, NotificationPriority, NotificationCategory,
            get_notification_hub,
        )
        n = get_notification_hub().send(
            recipient=req.recipient, subject=req.subject, body=req.body,
            channel=NotificationChannel(req.channel),
            priority=NotificationPriority(req.priority),
            category=NotificationCategory(req.category),
        )
        if n is None:
            return {"delivered": False, "reason": "filtered by preferences"}
        return n.to_dict()

    @router.get("/notifications/inbox/{recipient}", summary="Get inbox",
                tags=["Notifications"])
    def get_inbox(recipient: str, unread_only: bool = Query(False),
                  limit: int = Query(50, ge=1, le=500)) -> dict[str, Any]:
        from eoip.notifications.hub import get_notification_hub
        inbox = get_notification_hub().get_inbox(recipient, unread_only=unread_only, limit=limit)
        return {"notifications": [n.to_dict() for n in inbox], "total": len(inbox)}

    @router.post("/notifications/{notification_id}/read", summary="Mark as read",
                 tags=["Notifications"])
    def mark_read(notification_id: str) -> dict[str, Any]:
        from eoip.notifications.hub import get_notification_hub
        if not get_notification_hub().mark_read(notification_id):
            raise HTTPException(404, "Notification not found")
        return {"read": True}

    @router.get("/notifications/stats", summary="Notification statistics",
                tags=["Notifications"])
    def notification_stats() -> dict[str, Any]:
        from eoip.notifications.hub import get_notification_hub
        return get_notification_hub().stats()

    # ── Scheduling ────────────────────────────────────────────────────

    @router.get("/tasks", summary="List scheduled tasks",
                tags=["Scheduling"])
    def list_tasks(tag: str | None = Query(None),
                   enabled_only: bool = Query(False)) -> dict[str, Any]:
        from eoip.scheduling.executor import get_task_executor
        tasks = get_task_executor().list_tasks(tag=tag, enabled_only=enabled_only)
        return {"tasks": tasks, "total": len(tasks)}

    @router.post("/tasks/{task_id}/execute", summary="Execute task now",
                 tags=["Scheduling"])
    def execute_task(task_id: str) -> dict[str, Any]:
        from eoip.scheduling.executor import get_task_executor
        try:
            result = get_task_executor().execute(task_id)
        except ValueError:
            raise HTTPException(404, "Task not found")
        return result.to_dict()

    @router.get("/tasks/{task_id}/history", summary="Task execution history",
                tags=["Scheduling"])
    def task_history(task_id: str, limit: int = Query(20, ge=1, le=200)) -> dict[str, Any]:
        from eoip.scheduling.executor import get_task_executor
        history = get_task_executor().get_history(task_id, limit=limit)
        return {"history": [r.to_dict() for r in history], "total": len(history)}

    @router.get("/tasks/stats", summary="Scheduler statistics",
                tags=["Scheduling"])
    def task_stats() -> dict[str, Any]:
        from eoip.scheduling.executor import get_task_executor
        return get_task_executor().stats()

    # ── Incidents ─────────────────────────────────────────────────────

    @router.post("/incidents", summary="Create incident",
                 tags=["Incidents"])
    def create_incident(req: IncidentCreateRequest) -> dict[str, Any]:
        from eoip.incidents.manager import IncidentSeverity, get_incident_manager
        inc = get_incident_manager().create(
            title=req.title, description=req.description,
            severity=IncidentSeverity(req.severity),
            reporter=req.reporter, assignee=req.assignee,
            affected_services=req.affected_services,
        )
        return inc.to_dict()

    @router.get("/incidents", summary="List incidents",
                tags=["Incidents"])
    def list_incidents(state: str | None = Query(None),
                       severity: str | None = Query(None),
                       limit: int = Query(100, ge=1, le=500)) -> dict[str, Any]:
        from eoip.incidents.manager import IncidentState, IncidentSeverity, get_incident_manager
        st = IncidentState(state) if state else None
        sev = IncidentSeverity(severity) if severity else None
        incs = get_incident_manager().list_incidents(state=st, severity=sev, limit=limit)
        return {"incidents": [i.to_dict() for i in incs], "total": len(incs)}

    @router.get("/incidents/{incident_id}", summary="Get incident",
                tags=["Incidents"])
    def get_incident(incident_id: str) -> dict[str, Any]:
        from eoip.incidents.manager import get_incident_manager
        inc = get_incident_manager().get(incident_id)
        if inc is None:
            raise HTTPException(404, "Incident not found")
        return inc.to_dict()

    @router.post("/incidents/{incident_id}/transition", summary="Transition incident state",
                 tags=["Incidents"])
    def transition_incident(incident_id: str, req: IncidentTransitionRequest) -> dict[str, Any]:
        from eoip.incidents.manager import IncidentState, get_incident_manager
        inc = get_incident_manager().transition(
            incident_id, IncidentState(req.new_state), req.actor, req.details,
        )
        if inc is None:
            raise HTTPException(400, "Invalid transition or incident not found")
        return inc.to_dict()

    @router.get("/incidents/stats", summary="Incident statistics",
                tags=["Incidents"])
    def incident_stats() -> dict[str, Any]:
        from eoip.incidents.manager import get_incident_manager
        return get_incident_manager().stats()

    # ── Data Import ───────────────────────────────────────────────────

    @router.post("/imports/csv", summary="Import CSV data",
                 tags=["Data Import"])
    def import_csv(req: ImportCSVRequest) -> dict[str, Any]:
        from eoip.imports.engine import get_import_engine
        result = get_import_engine().import_csv(
            req.csv_data, req.entity_type, [],
            author=req.author, dry_run=req.dry_run,
        )
        return result.to_dict()

    @router.get("/imports/jobs", summary="List import jobs",
                tags=["Data Import"])
    def list_import_jobs(limit: int = Query(50, ge=1, le=200)) -> dict[str, Any]:
        from eoip.imports.engine import get_import_engine
        jobs = get_import_engine().list_jobs(limit=limit)
        return {"jobs": jobs, "total": len(jobs)}

    @router.get("/imports/stats", summary="Import statistics",
                tags=["Data Import"])
    def import_stats() -> dict[str, Any]:
        from eoip.imports.engine import get_import_engine
        return get_import_engine().stats()

    # ── Model Management ──────────────────────────────────────────────

    @router.get("/models", summary="List AI models",
                tags=["Model Management"])
    def list_models(status: str | None = Query(None),
                    model_type: str | None = Query(None)) -> dict[str, Any]:
        from eoip.model_management.registry import ModelStatus, get_model_registry
        st = ModelStatus(status) if status else None
        models = get_model_registry().list_models(status=st, model_type=model_type)
        return {"models": models, "total": len(models)}

    @router.get("/models/stats", summary="Model registry statistics",
                tags=["Model Management"])
    def model_stats() -> dict[str, Any]:
        from eoip.model_management.registry import get_model_registry
        return get_model_registry().stats()

    # ── Knowledge Maintenance ─────────────────────────────────────────

    @router.post("/maintenance/scan", summary="Run staleness scan",
                 tags=["Knowledge Maintenance"])
    def run_staleness_scan(threshold_days: float = Query(30.0, ge=1)) -> dict[str, Any]:
        from eoip.maintenance.autonomous import get_maintenance_engine
        report = get_maintenance_engine().scan_staleness(
            stale_threshold_days=threshold_days,
        )
        return report.to_dict()

    @router.get("/maintenance/entity/{entity_id}", summary="Get entity health",
                tags=["Knowledge Maintenance"])
    def get_entity_health(entity_id: str) -> dict[str, Any]:
        from eoip.maintenance.autonomous import get_maintenance_engine
        health = get_maintenance_engine().get_entity_health(entity_id)
        if health is None:
            raise HTTPException(404, "Entity not found")
        return health.to_dict()

    @router.get("/maintenance/enrichments", summary="Get enrichment queue",
                tags=["Knowledge Maintenance"])
    def get_enrichment_queue(status: str | None = Query(None),
                             limit: int = Query(50, ge=1, le=500)) -> dict[str, Any]:
        from eoip.maintenance.autonomous import get_maintenance_engine
        queue = get_maintenance_engine().get_enrichment_queue(status=status, limit=limit)
        return {"queue": queue, "total": len(queue)}

    @router.get("/maintenance/stats", summary="Maintenance statistics",
                tags=["Knowledge Maintenance"])
    def maintenance_stats() -> dict[str, Any]:
        from eoip.maintenance.autonomous import get_maintenance_engine
        return get_maintenance_engine().stats()

    # ── Event Streaming ───────────────────────────────────────────────

    @router.get("/streaming/channels/{channel}/latest", summary="Get latest events",
                tags=["Streaming"])
    def stream_latest(channel: str, limit: int = Query(20, ge=1, le=100)) -> dict[str, Any]:
        from eoip.streaming.event_stream import StreamChannel, get_event_stream
        try:
            ch = StreamChannel(channel)
        except ValueError:
            raise HTTPException(400, f"Invalid channel: {channel}")
        events = get_event_stream().get_latest(ch, limit=limit)
        return {"events": [e.to_dict() for e in events], "total": len(events)}

    @router.get("/streaming/subscriptions", summary="List stream subscriptions",
                tags=["Streaming"])
    def list_subscriptions() -> dict[str, Any]:
        from eoip.streaming.event_stream import get_event_stream
        subs = get_event_stream().list_subscriptions()
        return {"subscriptions": subs, "total": len(subs)}

    @router.get("/streaming/stats", summary="Streaming statistics",
                tags=["Streaming"])
    def streaming_stats() -> dict[str, Any]:
        from eoip.streaming.event_stream import get_event_stream
        return get_event_stream().stats()

    # ── Compliance ────────────────────────────────────────────────────

    @router.get("/compliance/frameworks", summary="List compliance frameworks",
                tags=["Compliance"])
    def list_frameworks() -> dict[str, Any]:
        from eoip.compliance.extended_packs import extended_packs
        from eoip.compliance.packs import builtin_packs
        all_packs = builtin_packs() + extended_packs()
        return {
            "frameworks": [
                {"framework": p.framework, "controls": len(p.controls),
                 "description": p.description}
                for p in all_packs
            ],
            "total": len(all_packs),
        }

    # ── Integrations ──────────────────────────────────────────────────

    @router.get("/integrations", summary="List integration connectors",
                tags=["Integrations"])
    def list_connectors(connector_type: str | None = Query(None)) -> dict[str, Any]:
        from eoip.integrations.bus import get_integration_bus
        connectors = get_integration_bus().list_connectors(connector_type=connector_type)
        return {"connectors": connectors, "total": len(connectors)}

    @router.post("/integrations/{connector_id}/health", summary="Check connector health",
                 tags=["Integrations"])
    def check_health(connector_id: str) -> dict[str, Any]:
        from eoip.integrations.bus import get_integration_bus
        status = get_integration_bus().check_health(connector_id)
        return {"connector_id": connector_id, "status": status.value}

    @router.post("/integrations/{connector_id}/sync", summary="Trigger sync",
                 tags=["Integrations"])
    def trigger_sync(connector_id: str) -> dict[str, Any]:
        from eoip.integrations.bus import get_integration_bus
        record = get_integration_bus().sync(connector_id)
        if record is None:
            raise HTTPException(404, "Connector not found")
        return record.to_dict()

    @router.get("/integrations/{connector_id}/history", summary="Sync history",
                tags=["Integrations"])
    def sync_history(connector_id: str,
                     limit: int = Query(20, ge=1, le=200)) -> dict[str, Any]:
        from eoip.integrations.bus import get_integration_bus
        history = get_integration_bus().get_sync_history(connector_id, limit=limit)
        return {"history": history, "total": len(history)}

    @router.get("/integrations/stats", summary="Integration statistics",
                tags=["Integrations"])
    def integration_stats() -> dict[str, Any]:
        from eoip.integrations.bus import get_integration_bus
        return get_integration_bus().stats()

    # ── Knowledge Reasoning ───────────────────────────────────────────

    @router.get("/reasoning/rules", summary="List inference rules",
                tags=["Knowledge Reasoning"])
    def list_rules() -> dict[str, Any]:
        from eoip.reasoning.knowledge_reasoning import get_knowledge_reasoning_engine
        rules = get_knowledge_reasoning_engine().get_rules()
        return {"rules": rules, "total": len(rules)}

    @router.get("/reasoning/inferences", summary="Recent inferences",
                tags=["Knowledge Reasoning"])
    def recent_inferences(limit: int = Query(50, ge=1, le=500)) -> dict[str, Any]:
        from eoip.reasoning.knowledge_reasoning import get_knowledge_reasoning_engine
        infs = get_knowledge_reasoning_engine().get_recent_inferences(limit=limit)
        return {"inferences": infs, "total": len(infs)}

    @router.get("/reasoning/stats", summary="Reasoning statistics",
                tags=["Knowledge Reasoning"])
    def reasoning_stats() -> dict[str, Any]:
        from eoip.reasoning.knowledge_reasoning import get_knowledge_reasoning_engine
        return get_knowledge_reasoning_engine().stats()

    # ── Edge Deployment ───────────────────────────────────────────────

    @router.post("/edge/nodes", summary="Register edge node",
                 tags=["Edge Deployment"])
    def register_edge_node(req: EdgeNodeRequest) -> dict[str, Any]:
        from eoip.edge.runtime import get_edge_runtime, SyncDirection
        node = get_edge_runtime().register_node(
            node_id=req.node_id, name=req.name, region=req.region,
            sync_direction=SyncDirection(req.sync_direction),
            sync_interval=req.sync_interval, tags=req.tags,
        )
        return node.to_dict()

    @router.get("/edge/nodes", summary="List edge nodes",
                tags=["Edge Deployment"])
    def list_edge_nodes(region: str | None = Query(None),
                        status: str | None = Query(None)) -> dict[str, Any]:
        from eoip.edge.runtime import get_edge_runtime, EdgeNodeStatus
        st = EdgeNodeStatus(status) if status else None
        nodes = get_edge_runtime().list_nodes(region=region, status=st)
        return {"nodes": [n.to_dict() for n in nodes], "total": len(nodes)}

    @router.post("/edge/sync", summary="Sync edge node",
                 tags=["Edge Deployment"])
    def sync_edge_node(req: EdgeSyncRequest) -> dict[str, Any]:
        from eoip.edge.runtime import get_edge_runtime, SyncDelta
        deltas = [SyncDelta(**d) for d in req.deltas] if req.deltas else None
        result = get_edge_runtime().sync_node(req.node_id, incoming_deltas=deltas)
        return result.to_dict()

    @router.post("/edge/promote", summary="Promote edge entities to cloud",
                 tags=["Edge Deployment"])
    def promote_edge_entities(req: EdgePromoteRequest) -> dict[str, Any]:
        from eoip.edge.runtime import get_edge_runtime
        return get_edge_runtime().promote_to_cloud(req.node_id, req.entity_ids)

    @router.get("/edge/nodes/{node_id}/query", summary="Offline query",
                tags=["Edge Deployment"])
    def edge_offline_query(node_id: str,
                           entity_type: str | None = Query(None),
                           limit: int = Query(100, ge=1, le=1000)) -> dict[str, Any]:
        from eoip.edge.runtime import get_edge_runtime
        results = get_edge_runtime().offline_query(
            node_id, entity_type=entity_type, limit=limit,
        )
        return {"results": results, "total": len(results)}

    @router.get("/edge/stats", summary="Edge runtime statistics",
                tags=["Edge Deployment"])
    def edge_stats() -> dict[str, Any]:
        from eoip.edge.runtime import get_edge_runtime
        return get_edge_runtime().stats()

    # ── API Gateway / SDK ─────────────────────────────────────────────

    @router.post("/gateway/types", summary="Register schema type",
                 tags=["API Gateway"])
    def register_gateway_type(req: GatewayTypeRequest) -> dict[str, Any]:
        from eoip.sdk.gateway import get_api_gateway, SchemaType, SchemaField
        fields = [SchemaField(**f) for f in req.fields]
        st = SchemaType(name=req.name, description=req.description,
                        fields=fields, relationships=req.relationships)
        get_api_gateway().register_type(st)
        return st.to_dict()

    @router.post("/gateway/query", summary="Execute gateway query",
                 tags=["API Gateway"])
    def execute_gateway_query(req: GatewayQueryRequest) -> dict[str, Any]:
        from eoip.sdk.gateway import get_api_gateway
        result = get_api_gateway().execute(req.query, client_id=req.client_id)
        return result.to_dict()

    @router.get("/gateway/introspect", summary="Schema introspection",
                tags=["API Gateway"])
    def gateway_introspect() -> dict[str, Any]:
        from eoip.sdk.gateway import get_api_gateway
        return get_api_gateway().introspect()

    @router.get("/gateway/openapi", summary="Export OpenAPI spec",
                tags=["API Gateway"])
    def gateway_openapi() -> dict[str, Any]:
        from eoip.sdk.gateway import get_api_gateway
        return get_api_gateway().export_openapi_spec()

    @router.get("/gateway/playground", summary="API playground metadata",
                tags=["API Gateway"])
    def gateway_playground() -> dict[str, Any]:
        from eoip.sdk.gateway import get_api_gateway
        return get_api_gateway().playground_metadata()

    @router.get("/gateway/stats", summary="Gateway statistics",
                tags=["API Gateway"])
    def gateway_stats() -> dict[str, Any]:
        from eoip.sdk.gateway import get_api_gateway
        return get_api_gateway().stats()

    # ── Semantic Vector Search ────────────────────────────────────────

    @router.post("/semantic/index", summary="Index entity for semantic search",
                 tags=["Semantic Search"])
    def semantic_index_entity(req: SemanticIndexRequest) -> dict[str, Any]:
        from eoip.search.semantic import get_semantic_index
        get_semantic_index().index_entity(
            entity_id=req.entity_id, text=req.text,
            entity_type=req.entity_type, language=req.language,
        )
        return {"indexed": True, "entity_id": req.entity_id}

    @router.post("/semantic/search", summary="Semantic similarity search",
                 tags=["Semantic Search"])
    def semantic_search(req: SemanticSearchRequest) -> dict[str, Any]:
        from eoip.search.semantic import get_semantic_index
        results = get_semantic_index().search_by_text(
            query_text=req.query_text, top_k=req.top_k,
            entity_type=req.entity_type, min_score=req.min_score,
        )
        return {"results": [r.to_dict() for r in results], "total": len(results)}

    @router.post("/semantic/hybrid", summary="Hybrid keyword + vector search",
                 tags=["Semantic Search"])
    def hybrid_search(req: PlatformHybridSearchRequest) -> dict[str, Any]:
        from eoip.search.semantic import get_semantic_index
        results = get_semantic_index().hybrid_search(
            query_text=req.query_text, top_k=req.top_k,
            keyword_weight=req.keyword_weight,
            vector_weight=req.vector_weight,
        )
        return {"results": [r.to_dict() for r in results], "total": len(results)}

    @router.get("/semantic/similar/{entity_id}", summary="Find similar entities",
                tags=["Semantic Search"])
    def find_similar(entity_id: str,
                     top_k: int = Query(10, ge=1, le=100)) -> dict[str, Any]:
        from eoip.search.semantic import get_semantic_index
        results = get_semantic_index().find_similar(entity_id, top_k=top_k)
        return {"results": [r.to_dict() for r in results], "total": len(results)}

    @router.post("/semantic/snapshot/{snapshot_id}", summary="Save vector snapshot",
                 tags=["Semantic Search"])
    def save_snapshot(snapshot_id: str) -> dict[str, Any]:
        from eoip.search.semantic import get_semantic_index
        count = get_semantic_index().save_snapshot(snapshot_id)
        return {"snapshot_id": snapshot_id, "entities_captured": count}

    @router.get("/semantic/drift", summary="Detect concept drift",
                tags=["Semantic Search"])
    def detect_drift(old_snapshot: str = Query(...),
                     new_snapshot: str = Query(...),
                     threshold: float = Query(0.15)) -> dict[str, Any]:
        from eoip.search.semantic import get_semantic_index
        reports = get_semantic_index().detect_drift(
            old_snapshot, new_snapshot, threshold=threshold,
        )
        return {"drifts": [r.to_dict() for r in reports], "total": len(reports)}

    @router.get("/semantic/stats", summary="Semantic search statistics",
                tags=["Semantic Search"])
    def semantic_stats() -> dict[str, Any]:
        from eoip.search.semantic import get_semantic_index
        return get_semantic_index().stats()

    # ── WAL & Disaster Recovery ───────────────────────────────────────

    @router.post("/recovery/wal/append", summary="Append WAL entry",
                 tags=["Disaster Recovery"])
    def wal_append(req: WALAppendRequest) -> dict[str, Any]:
        from eoip.recovery.wal import get_wal, WALOperationType
        entry = get_wal().append(
            operation=WALOperationType(req.operation),
            entity_type=req.entity_type,
            entity_id=req.entity_id,
            payload=req.payload,
            tenant_id=req.tenant_id,
        )
        return entry.to_dict()

    @router.get("/recovery/wal/read", summary="Read WAL from LSN",
                tags=["Disaster Recovery"])
    def wal_read(start_lsn: int = Query(1, ge=1),
                 limit: int = Query(100, ge=1, le=1000)) -> dict[str, Any]:
        from eoip.recovery.wal import get_wal
        entries = get_wal().read_from(start_lsn, limit=limit)
        return {"entries": [e.to_dict() for e in entries], "total": len(entries)}

    @router.post("/recovery/checkpoint", summary="Create checkpoint",
                 tags=["Disaster Recovery"])
    def create_checkpoint(label: str = Query("")) -> dict[str, Any]:
        from eoip.recovery.wal import get_wal
        cp = get_wal().checkpoint(label=label)
        return cp.to_dict()

    @router.get("/recovery/checkpoints", summary="List checkpoints",
                tags=["Disaster Recovery"])
    def list_checkpoints(limit: int = Query(20, ge=1, le=100)) -> dict[str, Any]:
        from eoip.recovery.wal import get_wal
        cps = get_wal().list_checkpoints(limit=limit)
        return {"checkpoints": [c.to_dict() for c in cps], "total": len(cps)}

    @router.post("/recovery/restore/{point_id}", summary="Restore to checkpoint",
                 tags=["Disaster Recovery"])
    def restore_checkpoint(point_id: str) -> dict[str, Any]:
        from eoip.recovery.wal import get_wal
        return get_wal().recover_to_point(point_id)

    @router.post("/recovery/peers", summary="Add replication peer",
                 tags=["Disaster Recovery"])
    def add_peer(req: WALPeerRequest) -> dict[str, Any]:
        from eoip.recovery.wal import get_wal, ReplicationRole
        peer = get_wal().add_peer(
            peer_id=req.peer_id, role=ReplicationRole(req.role),
            endpoint=req.endpoint,
        )
        return peer.to_dict()

    @router.get("/recovery/peers", summary="List replication peers",
                tags=["Disaster Recovery"])
    def list_peers() -> dict[str, Any]:
        from eoip.recovery.wal import get_wal
        peers = get_wal().list_peers()
        return {"peers": [p.to_dict() for p in peers], "total": len(peers)}

    @router.get("/recovery/rpo", summary="RPO/RTO status",
                tags=["Disaster Recovery"])
    def rpo_status() -> dict[str, Any]:
        from eoip.recovery.wal import get_wal
        return get_wal().rpo_status()

    @router.get("/recovery/stats", summary="Recovery statistics",
                tags=["Disaster Recovery"])
    def recovery_stats() -> dict[str, Any]:
        from eoip.recovery.wal import get_wal
        return get_wal().stats()

    # ── Cognitive Copilot ─────────────────────────────────────────────

    @router.post("/copilot/message", summary="Process copilot message",
                 tags=["Cognitive Copilot"])
    def copilot_message(req: CopilotMessageRequest) -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        return get_copilot_engine().process_message(
            session_id=req.session_id, role=req.role, content=req.content,
        )

    @router.get("/copilot/suggest/{session_id}",
                summary="Get suggested questions",
                tags=["Cognitive Copilot"])
    def copilot_suggestions(session_id: str,
                            limit: int = Query(5, ge=1, le=20)) -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        suggestions = get_copilot_engine().suggest_questions(session_id, limit=limit)
        return {"suggestions": [s.to_dict() for s in suggestions],
                "total": len(suggestions)}

    @router.post("/copilot/insights", summary="Generate proactive insights",
                 tags=["Cognitive Copilot"])
    def generate_insights(req: CopilotInsightRequest) -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        insights = get_copilot_engine().generate_insights(
            entity_stats=req.entity_stats, graph_stats=req.graph_stats,
        )
        return {"insights": [i.to_dict() for i in insights], "total": len(insights)}

    @router.get("/copilot/insights", summary="List active insights",
                tags=["Cognitive Copilot"])
    def list_insights(limit: int = Query(20, ge=1, le=100)) -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        insights = get_copilot_engine().get_insights(limit=limit)
        return {"insights": [i.to_dict() for i in insights], "total": len(insights)}

    @router.post("/copilot/rules", summary="Add automation rule",
                 tags=["Cognitive Copilot"])
    def add_automation_rule(req: CopilotRuleRequest) -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        rule = get_copilot_engine().add_rule(
            name=req.name, trigger_pattern=req.trigger_pattern,
            action_template=req.action_template,
            cooldown_seconds=req.cooldown_seconds,
        )
        return rule.to_dict()

    @router.get("/copilot/rules", summary="List automation rules",
                tags=["Cognitive Copilot"])
    def list_copilot_rules() -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        rules = get_copilot_engine().list_rules()
        return {"rules": [r.to_dict() for r in rules], "total": len(rules)}

    @router.get("/copilot/sessions", summary="List copilot sessions",
                tags=["Cognitive Copilot"])
    def list_copilot_sessions() -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        sessions = get_copilot_engine().list_sessions()
        return {"sessions": sessions, "total": len(sessions)}

    @router.get("/copilot/stats", summary="Copilot statistics",
                tags=["Cognitive Copilot"])
    def copilot_stats() -> dict[str, Any]:
        from eoip.copilot.engine import get_copilot_engine
        return get_copilot_engine().stats()

    # ── AI/ML Ops ─────────────────────────────────────────────────────

    @router.post("/aiml/rlhf/preference", summary="Add RLHF preference pair",
                 tags=["AI/ML Ops"])
    def add_preference(req: RLHFPreferenceRequest) -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops, PreferenceLabel
        pair = get_aiml_ops().rlhf.add_preference(
            prompt=req.prompt, response_a=req.response_a,
            response_b=req.response_b,
            label=PreferenceLabel(req.label),
            annotator=req.annotator, rationale=req.rationale,
        )
        return pair.to_dict()

    @router.post("/aiml/rlhf/reward", summary="Compute reward score",
                 tags=["AI/ML Ops"])
    def compute_reward(req: RewardScoreRequest) -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        score = get_aiml_ops().rlhf.compute_reward(
            response=req.response, reference=req.reference,
            source_texts=req.source_texts or None,
        )
        return score.to_dict()

    @router.get("/aiml/rlhf/stats", summary="RLHF statistics",
                tags=["AI/ML Ops"])
    def rlhf_stats() -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        return get_aiml_ops().rlhf.stats()

    @router.post("/aiml/hallucination/check", summary="Check for hallucinations",
                 tags=["AI/ML Ops"])
    def check_hallucination(req: HallucinationCheckRequest) -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        report = get_aiml_ops().hallucination.check(
            response=req.response, source_texts=req.source_texts,
        )
        return report.to_dict()

    @router.get("/aiml/hallucination/stats", summary="Hallucination detection stats",
                tags=["AI/ML Ops"])
    def hallucination_stats() -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        return get_aiml_ops().hallucination.stats()

    @router.post("/aiml/temperature/experiment",
                 summary="Create sampling experiment",
                 tags=["AI/ML Ops"])
    def create_experiment(req: SamplingExperimentRequest) -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        exp = get_aiml_ops().temperature.create_experiment(
            name=req.name, temperature=req.temperature,
            top_p=req.top_p, top_k=req.top_k,
            min_p=req.min_p, repetition_penalty=req.repetition_penalty,
        )
        return exp.to_dict()

    @router.post("/aiml/temperature/trial", summary="Record experiment trial",
                 tags=["AI/ML Ops"])
    def record_trial(req: TrialRecordRequest) -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        ok = get_aiml_ops().temperature.record_trial(
            req.experiment_id, req.quality, req.diversity, req.coherence,
        )
        if not ok:
            raise HTTPException(404, "Experiment not found")
        return {"recorded": True}

    @router.get("/aiml/temperature/best", summary="Best sampling config",
                tags=["AI/ML Ops"])
    def best_sampling_config() -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        best = get_aiml_ops().temperature.best_config()
        if not best:
            return {"best": None}
        return {"best": best.to_dict()}

    @router.post("/aiml/tokens/budget", summary="Create token budget",
                 tags=["AI/ML Ops"])
    def create_token_budget(req: TokenBudgetRequest) -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        budget = get_aiml_ops().token_budgets.create_budget(
            name=req.name, max_prompt=req.max_prompt,
            max_completion=req.max_completion, max_total=req.max_total,
        )
        return budget.to_dict()

    @router.post("/aiml/tokens/consume", summary="Consume token budget",
                 tags=["AI/ML Ops"])
    def consume_tokens(req: TokenConsumeRequest) -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        ok = get_aiml_ops().token_budgets.consume(
            req.budget_id, req.prompt_tokens, req.completion_tokens,
        )
        return {"allowed": ok}

    @router.get("/aiml/stats", summary="AI/ML Ops unified statistics",
                tags=["AI/ML Ops"])
    def aiml_stats() -> dict[str, Any]:
        from eoip.model_management.ai_ml_ops import get_aiml_ops
        return get_aiml_ops().stats()

    # ── Unified Hybrid Search Engine ──────────────────────────────────

    @router.post("/search/index", summary="Index entity for hybrid search",
                 tags=["Hybrid Search"])
    def hybrid_search_index(req: HybridSearchIndexRequest) -> dict[str, Any]:
        from eoip.search.hybrid_engine import get_hybrid_search_engine
        get_hybrid_search_engine().index_entity(
            entity_id=req.entity_id, text=req.text,
            entity_type=req.entity_type, fields=req.fields,
        )
        return {"indexed": True, "entity_id": req.entity_id}

    @router.post("/search/edge", summary="Add graph edge for search",
                 tags=["Hybrid Search"])
    def hybrid_search_edge(req: HybridSearchEdgeRequest) -> dict[str, Any]:
        from eoip.search.hybrid_engine import get_hybrid_search_engine
        get_hybrid_search_engine().add_edge(
            source=req.source, target=req.target,
            label=req.label, weight=req.weight,
        )
        return {"added": True}

    @router.post("/search/user-context",
                 summary="Register user context for contextual search",
                 tags=["Hybrid Search"])
    def register_search_user(req: HybridSearchUserContextRequest) -> dict[str, Any]:
        from eoip.search.hybrid_engine import get_hybrid_search_engine, UserContext
        ctx = UserContext(
            user_id=req.user_id, role=req.role, team=req.team,
            recent_entities=req.recent_entities,
            preferred_types=req.preferred_types,
            search_history=req.search_history,
            expertise_domains=req.expertise_domains,
        )
        get_hybrid_search_engine().contextual.register_user(ctx)
        return {"registered": True, "user_id": req.user_id}

    @router.post("/search/query", summary="Execute unified hybrid search",
                 tags=["Hybrid Search"])
    def unified_hybrid_search(req: HybridSearchQueryRequest) -> dict[str, Any]:
        from eoip.search.hybrid_engine import get_hybrid_search_engine, SearchModality
        modalities = None
        if req.modalities:
            modalities = [SearchModality(m) for m in req.modalities]

        user_ctx = None
        if req.user_id:
            user_ctx = get_hybrid_search_engine().contextual.get_user(req.user_id)

        results = get_hybrid_search_engine().search(
            query=req.query, top_k=req.top_k,
            modalities=modalities,
            user_context=user_ctx,
            structured_filters=req.structured_filters,
            graph_seeds=req.graph_seeds,
            graph_hops=req.graph_hops,
        )
        return {"results": [r.to_dict() for r in results], "total": len(results)}

    @router.get("/search/plan", summary="Get search execution plan",
                tags=["Hybrid Search"])
    def search_plan(query: str = Query(..., min_length=1)) -> dict[str, Any]:
        from eoip.search.hybrid_engine import get_hybrid_search_engine
        plan = get_hybrid_search_engine().plan_search(query)
        return plan.to_dict()

    @router.get("/search/metrics", summary="Search performance metrics",
                tags=["Hybrid Search"])
    def search_metrics(limit: int = Query(20, ge=1, le=100)) -> dict[str, Any]:
        from eoip.search.hybrid_engine import get_hybrid_search_engine
        metrics = get_hybrid_search_engine().get_metrics(limit=limit)
        return {"metrics": metrics, "total": len(metrics)}

    @router.get("/search/stats", summary="Hybrid search engine statistics",
                tags=["Hybrid Search"])
    def hybrid_search_stats() -> dict[str, Any]:
        from eoip.search.hybrid_engine import get_hybrid_search_engine
        return get_hybrid_search_engine().stats()

    # ── Prompt Engineering ───────────────────────────────────────────

    @router.post("/prompts/register", summary="Register prompt template",
                 tags=["Prompt Engineering"])
    def register_prompt(req: PromptRegisterRequest) -> dict[str, Any]:
        from eoip.prompts.engine import get_prompt_engine
        pv = get_prompt_engine().register(
            req.name, req.template, description=req.description,
            author=req.author, tags=req.tags,
        )
        return {"name": pv.name, "version": pv.version, "fingerprint": pv.fingerprint}

    @router.post("/prompts/render", summary="Render prompt with variables",
                 tags=["Prompt Engineering"])
    def render_prompt(req: PromptRenderRequest) -> dict[str, Any]:
        from eoip.prompts.engine import get_prompt_engine
        result = get_prompt_engine().render(req.name, **req.variables)
        if result is None:
            raise HTTPException(404, f"Prompt '{req.name}' not found")
        return {"rendered": result}

    @router.get("/prompts/list", summary="List registered prompts",
                tags=["Prompt Engineering"])
    def list_prompts() -> dict[str, Any]:
        from eoip.prompts.engine import get_prompt_engine
        return {"prompts": get_prompt_engine().registry.list_prompts()}

    @router.get("/prompts/stats", summary="Prompt engineering stats",
                tags=["Prompt Engineering"])
    def prompt_stats() -> dict[str, Any]:
        from eoip.prompts.engine import get_prompt_engine
        return get_prompt_engine().stats()

    # ── Feature Engineering ──────────────────────────────────────────

    @router.post("/features/extract", summary="Extract features for entity",
                 tags=["Feature Engineering"])
    def extract_features(req: FeatureExtractRequest) -> dict[str, Any]:
        from eoip.features.engine import get_feature_engine
        result = get_feature_engine().extract(
            req.entity_id, req.properties, req.neighbors,
        )
        return {"entity_id": req.entity_id, "features": result}

    @router.get("/features/stats", summary="Feature engineering stats",
                tags=["Feature Engineering"])
    def feature_stats() -> dict[str, Any]:
        from eoip.features.engine import get_feature_engine
        return get_feature_engine().stats()

    # ── Spec Engineering ─────────────────────────────────────────────

    @router.post("/specs/define", summary="Define entity specification",
                 tags=["Spec Engineering"])
    def define_spec(req: SpecDefineRequest) -> dict[str, Any]:
        from eoip.specs.engine import get_spec_engine
        spec = get_spec_engine().define_entity(req.name, req.fields,
                                                description=req.description)
        return {"name": spec.name, "fields": len(spec.fields),
                "fingerprint": spec.fingerprint()}

    @router.get("/specs/stats", summary="Spec engineering stats",
                tags=["Spec Engineering"])
    def spec_stats() -> dict[str, Any]:
        from eoip.specs.engine import get_spec_engine
        return get_spec_engine().stats()

    # ── Security & Red-Teaming ───────────────────────────────────────

    @router.post("/security/scan", summary="Scan input for threats",
                 tags=["Security"])
    def security_scan(req: SecurityScanRequest) -> dict[str, Any]:
        from eoip.security.engine import get_security_engine
        report = get_security_engine().scan(req.text)
        return {
            "threat_level": report.threat_level.value,
            "detections": report.detections,
            "sanitized": report.sanitized_text,
        }

    @router.post("/security/red-team", summary="Run red-team probe suite",
                 tags=["Security"])
    def run_red_team() -> dict[str, Any]:
        from eoip.security.engine import get_security_engine
        results = get_security_engine().run_red_team()
        return {
            "results": [{"probe_id": r.probe_id, "passed": r.passed,
                          "blocked": r.blocked} for r in results],
            "pass_rate": sum(1 for r in results if r.passed) / max(len(results), 1),
        }

    @router.get("/security/stats", summary="Security engine stats",
                tags=["Security"])
    def security_stats() -> dict[str, Any]:
        from eoip.security.engine import get_security_engine
        return get_security_engine().stats()

    # ── Cost & Latency Optimization ──────────────────────────────────

    @router.post("/cost/record", summary="Record cost event",
                 tags=["Cost Optimization"])
    def record_cost(req: CostRecordRequest) -> dict[str, Any]:
        from eoip.cost_optimization.engine import get_cost_engine
        alerts = get_cost_engine().record_operation(
            req.operation, req.model, req.tokens_in, req.tokens_out,
            req.cost_usd, req.latency_ms,
        )
        return {"recorded": True, "alerts": [a.message for a in alerts]}

    @router.get("/cost/recommendations", summary="Get optimization recommendations",
                tags=["Cost Optimization"])
    def cost_recommendations() -> dict[str, Any]:
        from eoip.cost_optimization.engine import get_cost_engine
        recs = get_cost_engine().get_recommendations()
        return {"recommendations": [
            {"category": r.category, "description": r.description,
             "savings_pct": r.estimated_savings_pct} for r in recs
        ]}

    @router.get("/cost/stats", summary="Cost optimization stats",
                tags=["Cost Optimization"])
    def cost_stats() -> dict[str, Any]:
        from eoip.cost_optimization.engine import get_cost_engine
        return get_cost_engine().stats()

    # ── Context Engineering ──────────────────────────────────────────

    @router.get("/context/stats", summary="Context engineering stats",
                tags=["Context Engineering"])
    def context_stats() -> dict[str, Any]:
        from eoip.context.engine import get_context_engine
        return get_context_engine().stats()

    # ── State & Persistence ──────────────────────────────────────────

    @router.get("/state/stats", summary="State & persistence stats",
                tags=["State & Persistence"])
    def state_stats() -> dict[str, Any]:
        from eoip.state.engine import get_state_engine
        return get_state_engine().stats()

    # ── Harness Engineering ──────────────────────────────────────────

    @router.get("/harness/stats", summary="Harness engineering stats",
                tags=["Harness Engineering"])
    def harness_stats() -> dict[str, Any]:
        from eoip.harness.engine import get_harness_engine
        return get_harness_engine().stats()

    # ── Tool & API Contract / MCP ────────────────────────────────────

    @router.post("/tools/register", summary="Register tool with schema",
                 tags=["Tool Contract"])
    def register_tool(req: ToolRegisterRequest) -> dict[str, Any]:
        from eoip.tools_contract.engine import get_tool_contract_engine
        get_tool_contract_engine().register_tool(
            req.name, req.description, req.schema,
            version=req.version, category=req.category, tags=req.tags,
        )
        return {"registered": True, "name": req.name}

    @router.get("/tools/stats", summary="Tool contract stats",
                tags=["Tool Contract"])
    def tool_contract_stats() -> dict[str, Any]:
        from eoip.tools_contract.engine import get_tool_contract_engine
        return get_tool_contract_engine().stats()

    # ── Graph-over-Loop & Loop-over-Graph ────────────────────────────

    @router.get("/graph-loop/stats", summary="Graph-loop engineering stats",
                tags=["Graph Loop"])
    def graph_loop_stats() -> dict[str, Any]:
        from eoip.graph_loop.engine import get_graph_loop_engine
        return get_graph_loop_engine().stats()

    # ── Evaluation & Benchmarking ────────────────────────────────────

    @router.post("/eval/run", summary="Evaluate prompt quality",
                 tags=["Evaluation"])
    def run_eval(req: EvalRunRequest) -> dict[str, Any]:
        from eoip.prompts.engine import get_prompt_engine
        result = get_prompt_engine().evaluate(
            req.prompt_name, req.rendered_text, req.reference,
        )
        return {"scores": result.scores, "overall": result.overall}

    @router.get("/eval/stats", summary="Evaluation & benchmarking stats",
                tags=["Evaluation"])
    def eval_stats() -> dict[str, Any]:
        from eoip.evaluation.engine import get_evaluation_engine
        return get_evaluation_engine().stats()

    # ── Memory Engineering ───────────────────────────────────────────

    @router.post("/memory/store", summary="Store a memory entry",
                 tags=["Memory Engineering"])
    def store_memory(req: MemoryStoreRequest) -> dict[str, Any]:
        from eoip.memory_eng.engine import get_memory_engine, MemoryTier
        tier = MemoryTier(req.tier) if req.tier else MemoryTier.WORKING
        entry = get_memory_engine().remember(
            req.content, tier=tier, tags=req.tags, ttl=req.ttl_seconds,
        )
        return {"entry_id": entry.entry_id, "tier": entry.tier.value}

    @router.post("/memory/recall", summary="Recall memories by query",
                 tags=["Memory Engineering"])
    def recall_memory(req: MemoryRecallRequest) -> dict[str, Any]:
        from eoip.memory_eng.engine import get_memory_engine, MemoryTier
        tier = MemoryTier(req.tier) if req.tier else None
        entries = get_memory_engine().recall(req.query, tier=tier, limit=req.limit)
        return {"entries": [
            {"entry_id": e.entry_id, "content": e.content,
             "tier": e.tier.value, "relevance": e.relevance}
            for e in entries
        ]}

    @router.get("/memory/stats", summary="Memory engineering stats",
                tags=["Memory Engineering"])
    def memory_stats() -> dict[str, Any]:
        from eoip.memory_eng.engine import get_memory_engine
        return get_memory_engine().stats()

    return router
