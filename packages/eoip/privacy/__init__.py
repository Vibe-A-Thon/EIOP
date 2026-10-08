"""EOIP privacy controls (SR-PRV-001..004, SR-PRV-006, partial).

Ingest classification engine (patterns/dictionaries/entropy, customer
extensible; labels propagate to derived records), DSAR locate across
graph/raw-captures/derived surfaces, erasure propagation with proof,
retention policies with expiry evaluation, purpose/consent tracking, and
residency pinning validation.

ADR-gated / External gate: NER-ML detectors (ADR), legal-hold workflows
(ADR), DPIA generation (ADR), DP aggregates (ADR), crypto-shred of
backups (External gate), cross-border transfer legal review (External
gate), runtime residency enforcement routing (ADR).
"""

from eoip.privacy.classification import (
    ClassificationEngine,
    ClassificationResult,
    ClassifiedField,
    DetectorKind,
    DetectorRule,
    SensitivityLabel,
    propagate_labels,
    shannon_entropy,
)
from eoip.privacy.consent import ConsentRecord, ConsentRegistry, Purpose
from eoip.privacy.dsar import (
    ErasureProof,
    ErasurePropagator,
    SubjectAccessReport,
    SubjectHit,
    locate_subject,
    proof_digest,
)
from eoip.privacy.residency import (
    RegionSet,
    ResidencyAspect,
    ResidencyPolicy,
    ResidencyValidation,
    ResidencyValidator,
    ResidencyViolation,
)
from eoip.privacy.retention import (
    DataClass,
    ExpiryAction,
    ExpiryDecision,
    RetainableRecord,
    RetentionEngine,
    RetentionPolicy,
)

__all__ = [
    "ClassificationEngine",
    "ClassificationResult",
    "ClassifiedField",
    "ConsentRecord",
    "ConsentRegistry",
    "DataClass",
    "DetectorKind",
    "DetectorRule",
    "ErasureProof",
    "ErasurePropagator",
    "ExpiryAction",
    "ExpiryDecision",
    "Purpose",
    "RegionSet",
    "ResidencyAspect",
    "ResidencyPolicy",
    "ResidencyValidation",
    "ResidencyValidator",
    "ResidencyViolation",
    "RetainableRecord",
    "RetentionEngine",
    "RetentionPolicy",
    "SensitivityLabel",
    "SubjectAccessReport",
    "SubjectHit",
    "locate_subject",
    "proof_digest",
    "propagate_labels",
    "shannon_entropy",
]
