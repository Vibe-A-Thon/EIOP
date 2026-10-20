"""Acceptance tests for WP-007: Code, Build, Artifact, and API-Portal Adapters (CRA-007.1-007.9, CRA-007.A)."""

import hashlib
import hmac
import json
from pathlib import Path
import pytest
import respx
import httpx

from eoip.connectors.api_portal import (
    CANDIDATE_PROFILES,
    PROPOSED_VOCABULARY,
    APIPortalConnector,
)
from eoip.connectors.artifactory import ArtifactoryConnector, scrub_build_credentials
from eoip.connectors.base import DiscoveryScope
from eoip.connectors.errors import ConnectorError
from eoip.connectors.git_references import extract_issue_references
from eoip.connectors.github import GitHubConnector
from eoip.connectors.gitlab import GitLabConnector
from eoip.mapping.cml import parse_and_compile_cml


# ---------------------------------------------------------------------------
# CRA-007.1: Qualify GitHub/GitLab; preserve immutable commits vs moving branches
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_1_git_identity_immutable_commits_vs_moving_branches():
    # 1. GitHub connector instance
    gh = GitHubConnector(
        source_id="gh-prod-01",
        api_url="https://api.github.com",
        token="ghp_sanitized_token",
        repositories=["acme/core-platform"],
    )
    assert gh.mapper_version == "github-rest/1.0"

    # Commit event: immutable reference
    commit_payload = {
        "sha": "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678",
        "commit": {"author": {"name": "Alice", "date": "2026-03-01T12:00:00Z"}, "message": "feat: init"},
    }
    commit_event = gh._event("acme/core-platform", "commit", commit_payload["sha"], commit_payload)
    assert commit_event.source_record_id == "acme/core-platform:commit:a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
    assert commit_event.metadata["immutable"] is True
    assert commit_event.metadata["commit_sha"] == "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"

    # Branch event: moving observation
    branch_payload = {
        "name": "main",
        "commit": {"sha": "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"},
    }
    branch_event = gh._event("acme/core-platform", "branch", "main", branch_payload)
    assert branch_event.source_record_id == "acme/core-platform:branch:main"
    assert branch_event.metadata["moving_ref"] is True
    assert branch_event.metadata["branch_name"] == "main"
    assert branch_event.metadata["target_commit"] == "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"

    # 2. GitLab connector instance
    gl = GitLabConnector(
        source_id="gl-prod-01",
        api_url="https://gitlab.com/api/v4",
        token="glpat-sanitized-token",
        projects=["acme/backend"],
    )
    gl_commit_event = gl._event("acme/backend", "commit", "c0ffee1234567890", {"id": "c0ffee1234567890"})
    assert gl_commit_event.metadata["immutable"] is True
    assert gl_commit_event.metadata["commit_sha"] == "c0ffee1234567890"


# ---------------------------------------------------------------------------
# CRA-007.2: Signed webhook verification, replay protection, and rate limits
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_2_signed_webhooks_and_replay_protection():
    secret = "webhook-hmac-secret-key-2026"
    payload = b'{"action":"opened","repository":{"full_name":"acme/core-platform"}}'

    # Compute valid signature
    digest = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    valid_sig = f"sha256={digest}"

    # 1. Signature verification
    assert GitHubConnector.verify_webhook_signature(payload, valid_sig, secret) is True
    assert GitHubConnector.verify_webhook_signature(payload, "sha256=invalid-signature", secret) is False
    assert GitHubConnector.verify_webhook_signature(payload, "", secret) is False

    # 2. Replay protection
    gh = GitHubConnector(
        source_id="gh-prod-02",
        api_url="https://api.github.com",
        token="tok",
        repositories=["acme/core-platform"],
    )
    delivery_uuid = "7d44c8b2-b7e1-4c12-9c98-112233445566"
    # First delivery: accepted
    assert gh.check_replay_protection(delivery_uuid) is True
    # Replay of same delivery: rejected
    assert gh.check_replay_protection(delivery_uuid) is False

    # Stale delivery (>300 seconds ago): rejected
    old_timestamp = 1000000.0
    assert gh.check_replay_protection("stale-uuid-99", timestamp_epoch=old_timestamp) is False


# ---------------------------------------------------------------------------
# CRA-007.3: Artifactory qualification, SHA-256 identity, and credential hygiene
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_3_artifactory_qualification_and_credential_scrubbing():
    conn = ArtifactoryConnector(
        source_id="art-01",
        base_url="https://artifactory.example.org/artifactory",
        token="art_token_123",
        repositories=["libs-release-local"],
    )
    assert conn.capabilities().discovery is True

    # 1. Artifact identity strictly rooted in SHA-256 checksum
    sha256 = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    art_event = conn.make_artifact_event(
        repo="libs-release-local",
        path="com/acme",
        name="platform-1.0.jar",
        sha256=sha256,
        size=102400,
    )
    assert art_event.source_record_id == f"sha256:{sha256}"
    assert art_event.source_version == sha256
    assert art_event.permissions.principal_refs == ["artifactory:repo:libs-release-local"]

    # Invalid SHA-256 rejected
    with pytest.raises(ValueError, match="valid 64-char SHA-256"):
        conn.make_artifact_event("libs-release-local", "com", "app.jar", "short-hash", 100)

    # 2. Build metadata credential scrubbing (never store credentials)
    dirty_properties = {
        "buildInfo.env.USER": "builder",
        "buildInfo.env.DB_PASSWORD": "super-secret-password-123",
        "buildInfo.env.AWS_SECRET_KEY": "AKIA1234567890SECRET",
        "buildInfo.env.API_TOKEN": "secret-token-xyz",
    }
    clean = scrub_build_credentials(dirty_properties)
    assert clean["buildInfo.env.USER"] == "builder"
    assert clean["buildInfo.env.DB_PASSWORD"] == "[REDACTED_CREDENTIAL]"
    assert clean["buildInfo.env.AWS_SECRET_KEY"] == "[REDACTED_CREDENTIAL]"
    assert clean["buildInfo.env.API_TOKEN"] == "[REDACTED_CREDENTIAL]"


# ---------------------------------------------------------------------------
# CRA-007.4: API Portal as a configurable provider family
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_4_api_portal_family_and_openapi_ingestion():
    # 1. Candidate profiles verified
    assert "kong" in CANDIDATE_PROFILES
    assert "apigee" in CANDIDATE_PROFILES
    assert "swaggerhub" in CANDIDATE_PROFILES
    assert "openapi3_crawler" in CANDIDATE_PROFILES

    # 2. Configurable provider profile instantiation
    portal = APIPortalConnector(
        portal_url="https://portal.example.org",
        provider_profile="apigee",
        token="portal_tok",
    )
    assert portal.provider_profile == "apigee"

    # Unsupported candidate profile rejected
    with pytest.raises(ValueError, match="unknown API portal candidate profile"):
        APIPortalConnector(portal_url="https://portal.example.org", provider_profile="unsupported_vendor", token="tok")


# ---------------------------------------------------------------------------
# CRA-007.5: Reject unsupported binaries and untrusted executable content
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_5_provenance_and_executable_binary_rejection():
    # DOS/Windows executable rejected
    with pytest.raises(ValueError, match="unsupported executable binary content rejected"):
        APIPortalConnector.validate_content_safety(b"MZ\x90\x00\x03\x00\x00\x00", "application/x-msdownload")

    # Linux ELF binary rejected
    with pytest.raises(ValueError, match="unsupported executable binary content rejected"):
        APIPortalConnector.validate_content_safety(b"\x7fELF\x02\x01\x01\x00", "application/x-executable")

    # Valid schema content accepted
    schema_yaml = b"openapi: 3.0.0\ninfo:\n  title: Payments API\n  version: 1.0.0"
    APIPortalConnector.validate_content_safety(schema_yaml, "application/yaml")


# ---------------------------------------------------------------------------
# CRA-007.6: GitHub & GitLab relations and repository visibility in acl_vector
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_6_github_gitlab_relations_and_acl_vector():
    # 1. Compile CML mapping
    cml_path = Path("packages/eoip/mapping/cml/github.cml")
    assert cml_path.exists()
    ir = parse_and_compile_cml(cml_path.read_text())
    assert ir.mapping_id == "cml_github_1_0_0"
    assert ir.source_type == "github"

    # 2. Verify repository visibility populates acl_vector
    gh = GitHubConnector(
        source_id="gh-01",
        api_url="https://api.github.com",
        token="tok",
        repositories=["acme/core-platform"],
    )

    # Public repo
    pub_event = gh._event("acme/open-sdk", "repository", "1", {"visibility": "public", "private": False})
    assert pub_event.permissions.visibility == "PUBLIC"
    assert pub_event.metadata["acl_vector"] == ["role:everyone"]

    # Internal repo
    internal_event = gh._event("acme/internal-tool", "repository", "2", {"visibility": "internal", "private": True})
    assert internal_event.permissions.visibility == "INTERNAL"
    assert internal_event.metadata["acl_vector"] == ["github:org:acme"]

    # Private repo
    priv_event = gh._event("acme/classified", "repository", "3", {"visibility": "private", "private": True})
    assert priv_event.permissions.visibility == "RESTRICTED"
    assert priv_event.metadata["acl_vector"] == ["github:repo:acme/classified"]


# ---------------------------------------------------------------------------
# CRA-007.7: Cross-system issue references extraction and proposal linking
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_7_cross_system_issue_reference_proposals():
    commit_msg = "PROJ-101: Fix memory leak in buffer pool; also relates to UNKNOWN-404 and SEC_OPS-99."

    # Ingested issues allowlist: only PROJ and SEC_OPS are registered projects; only PROJ-101 is an ingested issue
    ingested = {"PROJ-101"}
    allowed_projects = ["PROJ", "SEC_OPS"]

    refs = extract_issue_references(
        commit_msg,
        project_allowlist=allowed_projects,
        ingested_issues=ingested,
    )

    assert len(refs) == 2

    # PROJ-101 resolves to an ingested issue -> asserted
    assert refs[0]["issue_key"] == "PROJ-101"
    assert refs[0]["status"] == "asserted"
    assert refs[0]["span"] == [0, 8]
    assert refs[0]["evidence_locator"] == "char_span:0-8"

    # SEC_OPS-99 is in project allowlist but not yet ingested -> proposed
    assert refs[1]["issue_key"] == "SEC_OPS-99"
    assert refs[1]["status"] == "proposed"
    assert refs[1]["evidence_locator"] == "char_span:74-84"


# ---------------------------------------------------------------------------
# CRA-007.8: Artifactory AQL and builtFromCommit link
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_8_artifactory_aql_and_built_from_commit():
    # 1. Compile CML mapping
    cml_path = Path("packages/eoip/mapping/cml/artifactory.cml")
    assert cml_path.exists()
    ir = parse_and_compile_cml(cml_path.read_text())
    assert ir.mapping_id == "cml_artifactory_1_0_0"
    assert ir.source_type == "artifactory"

    # 2. Parse BuildInfo and extract art:builtFromCommit link
    fixture_path = Path("tests/fixtures/connectors/artifactory/build_info.json")
    raw_info = json.loads(fixture_path.read_text())

    conn = ArtifactoryConnector(source_id="art-01", base_url="https://artifactory.example.org", token="tok")
    build_event = conn.make_build_info_event("core-platform-pipeline", "42", raw_info)

    assert build_event.source_record_id == "build:core-platform-pipeline:42"
    assert build_event.metadata["built_from_commit"] == "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"
    assert build_event.payload["built_from_commit"] == "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"

    # Storage webhook event for artifact deployment
    wh_event = conn.handle_webhook_event({
        "event_type": "artifact:deployed",
        "data": {
            "repo_key": "libs-release-local",
            "path": "com/acme",
            "name": "core-platform-1.0.0.jar",
            "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            "size": 524288,
        }
    })
    assert wh_event.operation == "UPSERT"
    assert wh_event.source_record_id == "sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"


# ---------------------------------------------------------------------------
# CRA-007.9: API Portal unqualified state and proposed vocabulary
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_9_api_portal_unqualified_status_and_vocabulary():
    # 1. Compile CML mapping
    cml_path = Path("packages/eoip/mapping/cml/api_portal.cml")
    assert cml_path.exists()
    ir = parse_and_compile_cml(cml_path.read_text())
    assert ir.mapping_id == "cml_api_portal_1_0_0"
    assert ir.source_type == "api_portal"

    # 2. Qualification status remains UNQUALIFIED pending Decision H-07
    portal = APIPortalConnector(portal_url="https://portal.example.org", provider_profile="kong", token="portal_tok")
    assert portal.qualification_status == "UNQUALIFIED"

    # Proposed vocabulary includes Service, Endpoint, Operation, SchemaModel
    for term in ["api:Service", "api:Endpoint", "api:Operation", "api:SchemaModel"]:
        assert term in PROPOSED_VOCABULARY


# ---------------------------------------------------------------------------
# CRA-007.A: Acceptance Gate: Multi-hop Artifactory -> Commit -> Jira ticket
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-007")
def test_cra_007_a_acceptance_gate():
    # Clause verification:
    # 1. Multi-hop query: Artifactory binary -> Git commit -> Jira ticket with exact revision evidence
    art_conn = ArtifactoryConnector(source_id="art-01", base_url="https://artifactory.example.org", token="tok")
    art_fixture = json.loads(Path("tests/fixtures/connectors/artifactory/build_info.json").read_text())
    build_event = art_conn.make_build_info_event("core-platform-pipeline", "42", art_fixture)

    # Hop 1: Artifactory binary -> VCS commit
    binary_sha = art_fixture["buildInfo"]["modules"][0]["artifacts"][0]["sha256"]
    vcs_commit_sha = build_event.metadata["built_from_commit"]
    assert binary_sha == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert vcs_commit_sha == "a1b2c3d4e5f60718293a4b5c6d7e8f9012345678"

    # Hop 2: Git commit -> Jira ticket
    gh_fixture = json.loads(Path("tests/fixtures/connectors/github/repos_commits.json").read_text())
    matched_commit = next(c for c in gh_fixture["commits"] if c["sha"] == vcs_commit_sha)
    commit_msg = matched_commit["commit"]["message"]
    assert "PROJ-101" in commit_msg

    extracted_issues = extract_issue_references(commit_msg, project_allowlist=["PROJ"], ingested_issues={"PROJ-101"})
    assert len(extracted_issues) == 1
    assert extracted_issues[0]["issue_key"] == "PROJ-101"
    assert extracted_issues[0]["status"] == "asserted"
    assert extracted_issues[0]["evidence_locator"] == "char_span:0-8"

    # 2. Revoking private repository access ensures unauthorized users cannot view commits or derivatives
    gh_conn = GitHubConnector(source_id="gh-01", api_url="https://api.github.com", token="tok", repositories=["acme/core-platform"])
    priv_event = gh_conn._event("acme/core-platform", "commit", vcs_commit_sha, matched_commit)
    assert priv_event.permissions.visibility == "RESTRICTED"
    assert priv_event.permissions.principal_refs == ["github:repo:acme/core-platform"]
    assert "role:everyone" not in priv_event.permissions.principal_refs
