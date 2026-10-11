import pytest
from eoip.connectors.cicd import CICDConnector


@pytest.mark.req("G2-SRC-CICD-002")
def test_cicd_pipeline_discovery_and_extraction():
    connector = CICDConnector(source_id="cicd-jenkins", provider="jenkins")
    discovery = connector.discover()
    assert discovery.source_id == "cicd-jenkins"
    resource_ids = [r.resource_id for r in discovery.resources]
    assert "pipelines" in resource_ids
    assert "jobs" in resource_ids
    assert "deployments" in resource_ids

    pipelines = [
        {
            "pipeline_id": "pipe-100",
            "name": "build-and-test",
            "status": "SUCCESS",
            "ref": "refs/heads/main",
            "commit_sha": "abc12345",
            "created_at": "2026-10-01T12:00:00Z",
            "duration_seconds": 120,
        }
    ]
    events = connector.extract_pipelines(pipelines)
    assert len(events) == 1
    pipe_event = events[0]
    assert pipe_event.metadata["record_kind"] == "pipeline"
    assert pipe_event.payload["pipeline_id"] == "pipe-100"
    assert pipe_event.payload["status"] == "SUCCESS"
    assert pipe_event.payload["provider"] == "jenkins"


@pytest.mark.req("G2-SRC-CICD-003")
def test_cicd_job_and_deployment_run_extraction():
    connector = CICDConnector(source_id="cicd-gitlab", provider="gitlab")
    pipelines = [
        {
            "pipeline_id": "pipe-200",
            "name": "release-pipeline",
            "status": "SUCCESS",
            "jobs": [
                {
                    "job_id": "job-unit",
                    "name": "unit-tests",
                    "status": "PASSED",
                    "stage": "test",
                    "duration_seconds": 45,
                },
                {
                    "job_id": "job-build",
                    "name": "container-build",
                    "status": "PASSED",
                    "stage": "build",
                    "duration_seconds": 60,
                },
            ],
        }
    ]
    pipe_and_job_events = connector.extract_pipelines(pipelines)
    assert len(pipe_and_job_events) == 3  # 1 pipeline + 2 jobs
    job_events = [e for e in pipe_and_job_events if e.metadata["record_kind"] == "job"]
    assert len(job_events) == 2
    assert job_events[0].payload["job_id"] == "job-unit"
    assert job_events[0].payload["stage"] == "test"
    assert job_events[1].payload["job_id"] == "job-build"

    deployments = [
        {
            "deployment_id": "dep-300",
            "name": "production-rollout",
            "environment": "production",
            "status": "SUCCESS",
            "pipeline_id": "pipe-200",
            "commit_sha": "def67890",
            "url": "https://prod.internal",
        }
    ]
    deploy_events = connector.extract_deployments(deployments)
    assert len(deploy_events) == 1
    dep_event = deploy_events[0]
    assert dep_event.metadata["record_kind"] == "deployment"
    assert dep_event.payload["environment"] == "production"
    assert dep_event.payload["deployment_id"] == "dep-300"


@pytest.mark.req("G2-SRC-CICD-004")
def test_cicd_checkpoint_health_and_envelope_validation():
    connector = CICDConnector(source_id="cicd-actions", provider="github-actions")
    assert connector.checkpoint() is None

    health = connector.health()
    assert health.status == "HEALTHY"
    assert "github-actions" in health.detail

    events = connector.extract_pipelines([
        {"pipeline_id": "p-1", "name": "lint", "status": "SUCCESS"}
    ])
    assert len(events) == 1
    event = events[0]
    assert event.source_system == "cicd"
    assert event.source_instance_id == "cicd-actions"
    assert event.operation == "UPSERT"
    assert event.content_hash is not None
    assert event.schema_version == "2.0"
