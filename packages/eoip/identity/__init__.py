"""Identity resolution, alignment, and reversible merging (WP-023, CRA-023)."""

from eoip.identity.alignment import (
    AlignmentCandidate,
    AlignmentCandidateGenerator,
    AntiStubVerificationError,
    DeepOntoAlignmentWorker,
    TenantScopedEntityLinker,
)
from eoip.identity.candidates import IdentityCandidate, IdentityCandidateStore
from eoip.identity.evaluation import LinkingGateReport, evaluate_identity_linking_gate
from eoip.identity.merger import (
    HighImpactMergeApprovalRequiredError,
    IdentityMergeLedger,
    MergeLedgerOperationNotFoundError,
    ReversibleIdentityManager,
)
from eoip.identity.resolver import IdentityResolver, person_identity
from eoip.identity.scoped_table import ScopedSourceIdentityTable, SourceIdentityRecord

__all__ = [
    "AlignmentCandidate",
    "AlignmentCandidateGenerator",
    "AntiStubVerificationError",
    "DeepOntoAlignmentWorker",
    "HighImpactMergeApprovalRequiredError",
    "IdentityCandidate",
    "IdentityCandidateStore",
    "IdentityMergeLedger",
    "IdentityResolver",
    "LinkingGateReport",
    "MergeLedgerOperationNotFoundError",
    "ReversibleIdentityManager",
    "ScopedSourceIdentityTable",
    "SourceIdentityRecord",
    "TenantScopedEntityLinker",
    "evaluate_identity_linking_gate",
    "person_identity",
]
