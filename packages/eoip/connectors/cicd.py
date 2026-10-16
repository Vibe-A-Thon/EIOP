"""Generic CI/CD pipeline and deployment connector (G2-SRC-CICD-001..004).

Ingests pipeline, job and deployment metadata from generic CI/CD systems
as SourceEventV2 envelopes. Designed to be subclassed for specific CI/CD
providers or used directly with pre-formatted pipeline/deployment dicts.
"""

from __future__ import annotations

import hashlib
import json
import logging
from typing import Any

from eoip.connectors.base import ConnectorHealth, DiscoveredResource, DiscoveryResult, DiscoveryScope
from eoip.contracts.source_event import SourceEventV2, utc_now_iso

logger = logging.getLogger(__name__)


class CICDConnector:
    """Generic CI/CD pipeline and deployment connector (G2-SRC-CICD-001..004).

    Provides ``discover``, ``extract_pipelines``, ``extract_deployments``,
    ``checkpoint`` and ``health`` methods following the common connector
    pattern.
    """

    source_system = "cicd"
    mapper_version = "cicd-generic/1.0"

    def __init__(
        self,
        *,
        source_id: str = "cicd-default",
        provider: str = "generic",
    ) -> None:
        self.source_id = source_id
        self.provider = provider
        self._checkpoint: str | None = None

    def _make_event(
        self,
        record_kind: str,
        record_id: str,
        payload: dict[str, Any],
        version: str | None = None,
    ) -> SourceEventV2:
        captured_at = utc_now_iso()
        payload_json = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
        content_hash = hashlib.sha256(payload_json.encode("utf-8")).hexdigest()
        event_id = hashlib.sha256(
            f"{self.source_system}:{record_kind}:{record_id}:{content_hash}".encode()
        ).hexdigest()
        return SourceEventV2(
            event_id=event_id,
            source_system=self.source_system,
            source_instance_id=self.source_id,
            source_record_id=record_id,
            operation="UPSERT",
            source_version=version or content_hash[:16],
            event_time=payload.get("created_at") or captured_at,
            captured_at=captured_at,
            content_hash=content_hash,
            payload=payload,
            metadata={
                "mapper_version": self.mapper_version,
                "record_kind": record_kind,
                "provider": self.provider,
            },
        )

    def discover(self, scope: DiscoveryScope | None = None) -> DiscoveryResult:
        """Discover available CI/CD resource types."""
        resources = [
            DiscoveredResource(
                resource_id="pipelines",
                resource_type="pipeline",
                name="CI/CD Pipelines",
                metadata={"provider": self.provider},
            ),
            DiscoveredResource(
                resource_id="jobs",
                resource_type="job",
                name="CI/CD Jobs",
                metadata={"provider": self.provider},
            ),
            DiscoveredResource(
                resource_id="deployments",
                resource_type="deployment",
                name="CI/CD Deployments",
                metadata={"provider": self.provider},
            ),
        ]
        return DiscoveryResult(source_id=self.source_id, resources=resources)

    def extract_pipelines(
        self,
        pipelines: list[dict[str, Any]] | None = None,
    ) -> list[SourceEventV2]:
        """Extract pipeline and job metadata into SourceEventV2 envelopes.

        Parameters
        ----------
        pipelines:
            List of pipeline dicts with ``pipeline_id``, ``name``,
            ``status``, ``ref``, ``commit_sha``, ``jobs`` (optional list
            of job dicts) and timing metadata.

        Returns
        -------
        list[SourceEventV2]
            Extracted source events for pipelines and their jobs.
        """
        events: list[SourceEventV2] = []
        for pipeline in pipelines or []:
            pipeline_id = pipeline.get("pipeline_id", "")
            name = pipeline.get("name", f"pipeline-{pipeline_id}")
            record_id = f"{self.source_id}:pipeline:{pipeline_id}"
            version = pipeline.get("updated_at") or pipeline.get("created_at")
            payload = {
                "pipeline_id": pipeline_id,
                "name": name,
                "status": pipeline.get("status"),
                "ref": pipeline.get("ref"),
                "commit_sha": pipeline.get("commit_sha"),
                "source_branch": pipeline.get("source_branch"),
                "target_branch": pipeline.get("target_branch"),
                "created_at": pipeline.get("created_at"),
                "started_at": pipeline.get("started_at"),
                "finished_at": pipeline.get("finished_at"),
                "duration_seconds": pipeline.get("duration_seconds"),
                "provider": self.provider,
            }
            events.append(self._make_event("pipeline", record_id, payload, version))

            # Extract jobs nested within the pipeline
            for job in pipeline.get("jobs", []):
                if not isinstance(job, dict):
                    continue
                job_id = job.get("job_id", "")
                job_name = job.get("name", f"job-{job_id}")
                job_record_id = f"{self.source_id}:job:{pipeline_id}:{job_id}"
                job_version = job.get("finished_at") or job.get("created_at")
                job_payload = {
                    "job_id": job_id,
                    "pipeline_id": pipeline_id,
                    "name": job_name,
                    "status": job.get("status"),
                    "stage": job.get("stage"),
                    "ref": job.get("ref") or pipeline.get("ref"),
                    "commit_sha": job.get("commit_sha") or pipeline.get("commit_sha"),
                    "created_at": job.get("created_at"),
                    "started_at": job.get("started_at"),
                    "finished_at": job.get("finished_at"),
                    "duration_seconds": job.get("duration_seconds"),
                    "provider": self.provider,
                }
                events.append(self._make_event("job", job_record_id, job_payload, job_version))

        return events

    def extract_deployments(
        self,
        deployments: list[dict[str, Any]] | None = None,
    ) -> list[SourceEventV2]:
        """Extract deployment metadata into SourceEventV2 envelopes.

        Parameters
        ----------
        deployments:
            List of deployment dicts with ``deployment_id``, ``name``,
            ``environment``, ``status``, ``ref``, ``commit_sha`` and
            timing metadata.

        Returns
        -------
        list[SourceEventV2]
            Extracted source events for deployments.
        """
        events: list[SourceEventV2] = []
        for deploy in deployments or []:
            deploy_id = deploy.get("deployment_id", "")
            name = deploy.get("name", f"deploy-{deploy_id}")
            record_id = f"{self.source_id}:deployment:{deploy_id}"
            version = deploy.get("updated_at") or deploy.get("created_at")
            payload = {
                "deployment_id": deploy_id,
                "name": name,
                "environment": deploy.get("environment"),
                "status": deploy.get("status"),
                "ref": deploy.get("ref"),
                "commit_sha": deploy.get("commit_sha"),
                "pipeline_id": deploy.get("pipeline_id"),
                "created_at": deploy.get("created_at"),
                "finished_at": deploy.get("finished_at"),
                "url": deploy.get("url"),
                "provider": self.provider,
            }
            events.append(self._make_event("deployment", record_id, payload, version))

        return events

    def checkpoint(self) -> str | None:
        """Return the current extraction checkpoint."""
        return self._checkpoint

    def health(self) -> ConnectorHealth:
        """Check connector health. Always HEALTHY as a generic connector."""
        return ConnectorHealth(
            status="HEALTHY",
            checked_at=utc_now_iso(),
            detail=f"CI/CD connector ready (provider: {self.provider})",
        )
