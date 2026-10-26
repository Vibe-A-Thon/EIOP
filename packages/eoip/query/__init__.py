"""Query engine: QueryPlan compilation, policy enforcement, bounded templates, and typed federation."""

from eoip.query.executor import QueryExecutor
from eoip.query.nl import NLInterpretation, interpret
from eoip.query.nlq import NLQProcessor, NLQResponse, process
from eoip.query.policy import QueryPolicy
from eoip.query.service import QueryBudget, QueryService, ValidationResult, CostEstimate, ExplainResult, ExecutionProfile
from eoip.query.plan_engine import TypedPlanEngine, TrustedScope, ScopeViolationError
from eoip.query.sparql_protocol import SparqlProtocolHandler
from eoip.query.bi_connectivity import BISessionDriver, BISessionEmulator

__all__ = [
    "NLInterpretation",
    "NLQProcessor",
    "NLQResponse",
    "QueryExecutor",
    "QueryPolicy",
    "QueryService",
    "QueryBudget",
    "ValidationResult",
    "CostEstimate",
    "ExplainResult",
    "ExecutionProfile",
    "TypedPlanEngine",
    "TrustedScope",
    "ScopeViolationError",
    "SparqlProtocolHandler",
    "BISessionDriver",
    "BISessionEmulator",
    "interpret",
    "process",
]

