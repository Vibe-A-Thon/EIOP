"""Comprehensive Unit Tests for EOIP Phase 4 — Phase 4 Infrastructure & DevOps.

Validates:
- INFRA-001: Multi-Level Caching (L1/L2 hierarchy, write policies, invalidation, warming)
- INFRA-002: OAuth2 / OIDC / SAML SSO Integration (PKCE, token exchange, discovery, assertion processing)
- INFRA-004: Log Aggregation (Structured JSON formatting, correlation IDs, sampling)
- INFRA-005: Distributed Scheduling (Leader election, distributed lock, TaskDAG topological order)
- INFRA-006: API Versioning & SDK Generation (Version routing, deprecation headers, SDK generators)
- INFRA-007: Automated Backup & Restore (Encrypted backup, SHA-256 integrity, restore test drill)
"""

import time
import pytest

from eoip.enterprise.cache import (
    CacheCoordinator,
    IntelligentCache,
    L2Cache,
    WritePolicy,
    get_cache_coordinator,
)
from eoip.authn.oauth_sso import (
    IdPFederation,
    OIDCDiscovery,
    OAuthProvider,
    SAMLAdapter,
    TokenValidator,
)
from eoip.observability.logging import (
    LogFormat,
    SamplingFilter,
    StructuredLogFormatter,
    StructuredLogger,
    get_trace_context,
    set_trace_context,
)
from eoip.scheduling.executor import (
    DistributedLock,
    LeaderElection,
    TaskDAG,
)
from eoip.sdk.versioning import (
    APIVersionManager,
    ClientSDKGenerator,
    VersionStatus,
)
from eoip.recovery.backup_scheduler import (
    BackupArchive,
    BackupScheduler,
    BackupVerifier,
    RestoreTestRunner,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.mark.req("INFRA-001")
class TestInfra001MultiLevelCache:
    """INFRA-001: Multi-Level Caching."""

    def test_l1_l2_hierarchy_and_promotion(self):
        l1 = IntelligentCache(max_size=10, default_ttl=60.0)
        l2 = L2Cache(default_ttl=300.0)
        coord = CacheCoordinator(l1_cache=l1, l2_cache=l2, policy=WritePolicy.WRITE_THROUGH)

        # Write to coordinator -> writes to both L1 and L2
        coord.put("user_101", {"name": "Alice"})
        assert l1.get("user_101") == {"name": "Alice"}
        assert l2.get("user_101") == {"name": "Alice"}

        # Evict from L1 only
        l1.invalidate("user_101")
        assert l1.get("user_101") is None

        # Fetch through coordinator: misses L1, hits L2, promotes back to L1
        promoted = coord.get("user_101")
        assert promoted == {"name": "Alice"}
        assert l1.get("user_101") == {"name": "Alice"}

    def test_invalidation_broadcast_and_warming(self):
        coord = CacheCoordinator()
        invalidated_keys = []
        coord.subscribe_invalidation(lambda k: invalidated_keys.append(k))

        coord.put("item_alpha", 42)
        coord.invalidate("item_alpha")

        assert "item_alpha" in invalidated_keys
        assert coord.get("item_alpha") is None

        # Cache warming
        warmed_count = coord.warm_cache({"hot_1": 100, "hot_2": 200})
        assert warmed_count == 2
        assert coord.get("hot_1") == 100
        assert coord.get("hot_2") == 200


@pytest.mark.req("INFRA-002")
class TestInfra002OAuthAndSSO:
    """INFRA-002: OAuth2 / OIDC / SAML SSO Integration."""

    def test_oauth_pkce_flow(self):
        provider = OAuthProvider("test_client", "test_secret", "https://app.io/callback")
        verifier, challenge = provider.generate_pkce_pair()

        # Authorization URL
        auth_url = provider.create_authorization_url("https://idp.io/auth", "state_123", challenge)
        assert "code_challenge=" in auth_url
        assert "code_challenge_method=S256" in auth_url

        # Issue code and exchange
        code = provider.issue_authorization_code("user_bob", challenge)
        tokens = provider.exchange_code_for_token(code, verifier)

        assert len(tokens.access_token) >= 20
        assert tokens.expires_in == 3600

        # Invalid verifier should raise
        code_fail = provider.issue_authorization_code("user_fail", challenge)
        with pytest.raises(ValueError, match="PKCE verification failed"):
            provider.exchange_code_for_token(code_fail, "wrong_verifier")

    def test_oidc_discovery_and_saml_adapter(self):
        # 1. OIDC Discovery
        disc = OIDCDiscovery()
        cfg = disc.register_configuration("https://auth.enterprise.com", {
            "issuer": "https://auth.enterprise.com",
            "authorization_endpoint": "https://auth.enterprise.com/oauth2/v1/authorize",
            "token_endpoint": "https://auth.enterprise.com/oauth2/v1/token",
        })
        assert cfg.issuer == "https://auth.enterprise.com"

        # 2. SAML Adapter
        saml = SAMLAdapter(expected_audience="eoip-platform", idp_entity_id="okta-saml")
        principal = saml.process_assertion('{"sub": "charlie@enterprise.com", "roles": ["admin"]}')
        assert principal.username == "charlie@enterprise.com"
        assert "admin" in principal.roles

    def test_token_validator(self):
        validator = TokenValidator(secret_key="my-secret-key")
        with pytest.raises(ValueError, match="Invalid token"):
            validator.validate_token("token_string_with_sufficient_length")


@pytest.mark.req("INFRA-004")
class TestInfra004LogAggregation:
    """INFRA-004: Log Aggregation."""

    def test_structured_json_logging_with_correlation(self):
        set_trace_context(correlation_id="corr-999", request_id="req-777", trace_id="trace-111")
        ctx = get_trace_context()
        assert ctx["correlation_id"] == "corr-999"

        logger = StructuredLogger()
        json_log = logger.format_log("INFO", "Agent task initiated", logger_name="eoip.agent")

        import json
        data = json.loads(json_log)
        assert data["level"] == "INFO"
        assert data["message"] == "Agent task initiated"
        assert data["correlation_id"] == "corr-999"
        assert data["request_id"] == "req-777"

    def test_sampling_filter(self):
        filt = SamplingFilter(sample_rate=0.0)  # Drop debug/info
        import logging
        rec_info = logging.LogRecord("test", logging.INFO, "", 0, "msg", (), None)
        rec_warn = logging.LogRecord("test", logging.WARNING, "", 0, "msg", (), None)

        assert filt.filter(rec_info) is False
        assert filt.filter(rec_warn) is True  # Warnings always pass


@pytest.mark.req("INFRA-005")
class TestInfra005DistributedScheduling:
    """INFRA-005: Distributed Scheduling."""

    def test_leader_election(self):
        node_a = LeaderElection(node_id="node_a", lease_duration=2.0)
        node_b = LeaderElection(node_id="node_b", lease_duration=2.0)

        assert node_a.try_acquire() is True
        assert node_a.is_leader is True

        # Node B cannot acquire while Node A holds lease
        assert node_b.try_acquire() is False
        assert node_b.is_leader is False

        # Node A steps down
        node_a.step_down()
        assert node_a.is_leader is False

        # Node B acquires
        assert node_b.try_acquire() is True
        assert node_b.is_leader is True

    def test_distributed_lock_and_task_dag(self):
        # 1. Distributed Lock
        lock_1 = DistributedLock("task_nightly_reindex", "worker_1", ttl_seconds=10.0)
        lock_2 = DistributedLock("task_nightly_reindex", "worker_2", ttl_seconds=10.0)

        assert lock_1.acquire() is True
        assert lock_2.acquire() is False
        assert lock_1.release() is True
        assert lock_2.acquire() is True

        # 2. TaskDAG Topological Sort
        dag = TaskDAG()
        dag.add_dependency("task_train_model", "task_prepare_data")
        dag.add_dependency("task_evaluate_model", "task_train_model")
        dag.add_dependency("task_deploy_model", "task_evaluate_model")

        order = dag.execution_order()
        assert order == ["task_prepare_data", "task_train_model", "task_evaluate_model", "task_deploy_model"]

        # Cycle detection
        dag_cycle = TaskDAG()
        dag_cycle.add_dependency("task_a", "task_b")
        dag_cycle.add_dependency("task_b", "task_a")
        with pytest.raises(ValueError, match="Cycle detected"):
            dag_cycle.execution_order()


@pytest.mark.req("INFRA-006")
class TestInfra006APIVersioning:
    """INFRA-006: API Versioning & Client SDK Generation."""

    def test_api_versioning_and_headers(self):
        mgr = APIVersionManager()
        ver, sub = mgr.route_version("/api/v1/graph/query")
        assert ver == "v1"
        assert sub == "/graph/query"

        meta_v1 = mgr.get_version("v1")
        assert meta_v1.status == VersionStatus.DEPRECATED
        headers = meta_v1.get_response_headers()
        assert headers["Deprecation"] == "true"
        assert "Sunset" in headers

    def test_sdk_generation(self):
        gen = ClientSDKGenerator()
        spec = {
            "info": {"title": "KnowGridFlow"},
            "paths": {
                "/api/v1/platform/xai/explain": {},
                "/api/v1/platform/graph/query": {},
            },
        }

        py_sdk = gen.generate_python_sdk(spec)
        assert "class KnowGridFlowClient:" in py_sdk
        assert "def api_v1_platform_xai_explain" in py_sdk

        ts_sdk = gen.generate_typescript_sdk(spec)
        assert "export class KnowGridFlowClient" in ts_sdk

        go_sdk = gen.generate_go_sdk(spec)
        assert "package knowgridflow" in go_sdk


@pytest.mark.req("INFRA-007")
class TestInfra007BackupAndRestore:
    """INFRA-007: Automated Backup & Restore Testing."""

    def test_backup_encryption_and_integrity(self):
        store = MemoryGraphStore()
        store.upsert_vertex("Service", {"name": "AuthService", "service_id": "srv_auth", "canonical_id": "srv_auth"})
        store.upsert_vertex("Service", {"name": "PaymentService", "service_id": "srv_pay", "canonical_id": "srv_pay"})
        store.upsert_edge("CALLS", "srv_auth", "srv_pay", {})

        scheduler = BackupScheduler(encryption_key="secret-key-123")
        archive = scheduler.create_backup(store, encrypt=True, retention_days=14)

        assert archive.encrypted is True
        assert archive.vertex_count == 2
        assert archive.edge_count == 1
        assert len(archive.checksum) == 64

        # Verify integrity
        ver = BackupVerifier.verify(archive, encryption_key="secret-key-123")
        assert ver["conforms"] is True
        assert ver["checksum_valid"] is True
        assert ver["data_valid"] is True

        # Tampered payload fails verification
        tampered_archive = BackupArchive(
            backup_id="tampered",
            created_at=archive.created_at,
            vertex_count=archive.vertex_count,
            edge_count=archive.edge_count,
            checksum=archive.checksum,
            encrypted=True,
            payload_bytes=b"corrupted_bytes",
        )
        ver_tampered = BackupVerifier.verify(tampered_archive, encryption_key="secret-key-123")
        assert ver_tampered["conforms"] is False

    def test_automated_restore_drill(self):
        store = MemoryGraphStore()
        store.upsert_vertex("Service", {"name": "SearchService", "service_id": "srv_search", "canonical_id": "srv_search"})
        store.upsert_vertex("Service", {"name": "IndexService", "service_id": "srv_index", "canonical_id": "srv_index"})
        store.upsert_edge("CALLS", "srv_search", "srv_index", {})

        scheduler = BackupScheduler()
        archive = scheduler.create_backup(store, encrypt=True)

        drill = scheduler.run_automated_restore_drill(archive.backup_id)
        assert drill["success"] is True
        assert drill["restored_vertices"] == 2
        assert drill["restored_edges"] == 1
        assert drill["isolated_store_healthy"] is True
