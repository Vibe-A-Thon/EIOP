"""EOIP neural and numerical stack with lazy optional-tier imports."""

from __future__ import annotations

from importlib import import_module
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from eoip.neural.antistub import AntiStubHarness, AntiStubReport, SimpleLearnedGNN
    from eoip.neural.datasets import (
        ContentAddressedSnapshot,
        EdgeEvent,
        TemporalLeakageError,
        TemporalSplit,
        create_event_time_split,
        sample_type_constrained_negatives,
        validate_batch_leakage,
    )
    from eoip.neural.discriminator import (
        AdversarialPlausibilityDiscriminator,
        ResearchSandboxTenant,
        TripletEvaluationResult,
    )
    from eoip.neural.encoders import (
        ChebNetFilter,
        GraphGPSModel,
        GraphSAGELayer,
        GraphSAGEModel,
        HGTModel,
        RGATModel,
        RGCNBasisLayer,
        RGCNModel,
    )
    from eoip.neural.evaluation import (
        AUROCOnlyReportRefusedError,
        BaselineComparisonReport,
        ModelEvaluationHarness,
        compute_auprc,
        compute_auroc,
        compute_ece,
        compute_macro_f1,
        compute_time_filtered_mrr,
    )
    from eoip.neural.explain import NeuralExplainer, SubgraphExplanation
    from eoip.neural.lifecycle import (
        FailureModeGuards,
        ModelNotQualifiedError,
        NeuralModelLifecycleManager,
        RegisteredModelRecord,
        create_model_prediction_assertion,
    )
    from eoip.neural.numerics import (
        MemoryGuard,
        assert_finite,
        capture_environment,
        cosine_matrix,
        cosine_similarity,
        ensure_float32,
        l2_normalize,
        seed_everything,
        stable_log,
        stable_softmax,
        to_array,
        to_list,
    )
    from eoip.neural.planes import (
        EpochBoundSnapshot,
        GraphLevel,
        GraphPlane,
        GraphPlaneCoordinator,
        ParallelTemporalStoreProhibitedError,
    )
    from eoip.neural.runtime import NeuralRuntime, NeuralTier, get_runtime, require_tier

_EXPORTS = {
    "NeuralTier": ("runtime", "NeuralTier"),
    "NeuralRuntime": ("runtime", "NeuralRuntime"),
    "get_runtime": ("runtime", "get_runtime"),
    "require_tier": ("runtime", "require_tier"),
    "seed_everything": ("numerics", "seed_everything"),
    "assert_finite": ("numerics", "assert_finite"),
    "ensure_float32": ("numerics", "ensure_float32"),
    "to_array": ("numerics", "to_array"),
    "to_list": ("numerics", "to_list"),
    "cosine_similarity": ("numerics", "cosine_similarity"),
    "cosine_matrix": ("numerics", "cosine_matrix"),
    "l2_normalize": ("numerics", "l2_normalize"),
    "stable_softmax": ("numerics", "stable_softmax"),
    "stable_log": ("numerics", "stable_log"),
    "MemoryGuard": ("numerics", "MemoryGuard"),
    "capture_environment": ("numerics", "capture_environment"),
    "AntiStubHarness": ("antistub", "AntiStubHarness"),
    "AntiStubReport": ("antistub", "AntiStubReport"),
    "SimpleLearnedGNN": ("antistub", "SimpleLearnedGNN"),
    "GraphPlane": ("planes", "GraphPlane"),
    "GraphLevel": ("planes", "GraphLevel"),
    "EpochBoundSnapshot": ("planes", "EpochBoundSnapshot"),
    "GraphPlaneCoordinator": ("planes", "GraphPlaneCoordinator"),
    "ParallelTemporalStoreProhibitedError": ("planes", "ParallelTemporalStoreProhibitedError"),
    "ContentAddressedSnapshot": ("datasets", "ContentAddressedSnapshot"),
    "EdgeEvent": ("datasets", "EdgeEvent"),
    "TemporalSplit": ("datasets", "TemporalSplit"),
    "TemporalLeakageError": ("datasets", "TemporalLeakageError"),
    "create_event_time_split": ("datasets", "create_event_time_split"),
    "validate_batch_leakage": ("datasets", "validate_batch_leakage"),
    "sample_type_constrained_negatives": ("datasets", "sample_type_constrained_negatives"),
    "compute_auprc": ("evaluation", "compute_auprc"),
    "compute_auroc": ("evaluation", "compute_auroc"),
    "compute_macro_f1": ("evaluation", "compute_macro_f1"),
    "compute_time_filtered_mrr": ("evaluation", "compute_time_filtered_mrr"),
    "compute_ece": ("evaluation", "compute_ece"),
    "BaselineComparisonReport": ("evaluation", "BaselineComparisonReport"),
    "ModelEvaluationHarness": ("evaluation", "ModelEvaluationHarness"),
    "AUROCOnlyReportRefusedError": ("evaluation", "AUROCOnlyReportRefusedError"),
    "RGCNBasisLayer": ("encoders", "RGCNBasisLayer"),
    "RGCNModel": ("encoders", "RGCNModel"),
    "GraphSAGELayer": ("encoders", "GraphSAGELayer"),
    "GraphSAGEModel": ("encoders", "GraphSAGEModel"),
    "RGATModel": ("encoders", "RGATModel"),
    "HGTModel": ("encoders", "HGTModel"),
    "GraphGPSModel": ("encoders", "GraphGPSModel"),
    "ChebNetFilter": ("encoders", "ChebNetFilter"),
    "AdversarialPlausibilityDiscriminator": ("discriminator", "AdversarialPlausibilityDiscriminator"),
    "ResearchSandboxTenant": ("discriminator", "ResearchSandboxTenant"),
    "TripletEvaluationResult": ("discriminator", "TripletEvaluationResult"),
    "NeuralExplainer": ("explain", "NeuralExplainer"),
    "SubgraphExplanation": ("explain", "SubgraphExplanation"),
    "NeuralModelLifecycleManager": ("lifecycle", "NeuralModelLifecycleManager"),
    "RegisteredModelRecord": ("lifecycle", "RegisteredModelRecord"),
    "ModelNotQualifiedError": ("lifecycle", "ModelNotQualifiedError"),
    "FailureModeGuards": ("lifecycle", "FailureModeGuards"),
    "create_model_prediction_assertion": ("lifecycle", "create_model_prediction_assertion"),
}

__all__ = [
    "NeuralTier", "NeuralRuntime", "get_runtime", "require_tier",
    "seed_everything", "assert_finite", "ensure_float32", "to_array", "to_list",
    "cosine_similarity", "cosine_matrix", "l2_normalize", "stable_softmax", "stable_log",
    "MemoryGuard", "capture_environment", "AntiStubHarness", "AntiStubReport",
    "SimpleLearnedGNN", "GraphPlane", "GraphLevel", "EpochBoundSnapshot",
    "GraphPlaneCoordinator", "ParallelTemporalStoreProhibitedError", "ContentAddressedSnapshot",
    "EdgeEvent", "TemporalSplit", "TemporalLeakageError", "create_event_time_split",
    "validate_batch_leakage", "sample_type_constrained_negatives", "compute_auprc", "compute_auroc",
    "compute_macro_f1", "compute_time_filtered_mrr", "compute_ece", "BaselineComparisonReport",
    "ModelEvaluationHarness", "AUROCOnlyReportRefusedError", "RGCNBasisLayer", "RGCNModel",
    "GraphSAGELayer", "GraphSAGEModel", "RGATModel", "HGTModel", "GraphGPSModel",
    "ChebNetFilter", "AdversarialPlausibilityDiscriminator", "ResearchSandboxTenant",
    "TripletEvaluationResult", "NeuralExplainer", "SubgraphExplanation", "NeuralModelLifecycleManager",
    "RegisteredModelRecord", "ModelNotQualifiedError", "FailureModeGuards",
    "create_model_prediction_assertion",
]


def __getattr__(name: str) -> Any:
    export = _EXPORTS.get(name)
    if export is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module_name, attribute_name = export
    value = getattr(import_module(f"{__name__}.{module_name}"), attribute_name)
    globals()[name] = value
    return value