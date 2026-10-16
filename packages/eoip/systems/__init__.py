"""EOIP Systems Registry — unified system connection, onboarding, and pipeline management."""

from eoip.systems.registry import SystemsRegistry, SystemEntry, SystemStatus
from eoip.systems.auto_onboard import AutoOnboardOrchestrator, OnboardingResult
from eoip.systems.schema_generator import AutoSchemaGenerator, GeneratedSchema
from eoip.systems.pipeline_factory import PipelineFactory, PipelineSpec

__all__ = [
    "SystemsRegistry",
    "SystemEntry",
    "SystemStatus",
    "AutoOnboardOrchestrator",
    "OnboardingResult",
    "AutoSchemaGenerator",
    "GeneratedSchema",
    "PipelineFactory",
    "PipelineSpec",
]
