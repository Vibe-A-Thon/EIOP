"""Normative Operator Catalog for the 10 Processing Units (PUR-FND-001, Section 9).

Registers all ten logical profiles (CPU, GPU, TPU, NPU, DPU, QPU, APU, LPU, IPU, VPU)
with their stable operator definitions, parameter bounds, accepted profiles,
and validation schemas.
"""

from __future__ import annotations

from typing import Dict, List, Optional

from eoip.processing.contracts import LogicalUnit, OperatorBudget, OperatorSpec


_OPERATOR_CATALOG: Dict[str, OperatorSpec] = {}
OPERATOR_CATALOG = _OPERATOR_CATALOG


def register_operator(spec: OperatorSpec) -> None:
    """Register an operator specification in the global catalog."""
    _OPERATOR_CATALOG[spec.operator_id] = spec


def get_operator_spec(operator_id: str) -> Optional[OperatorSpec]:
    """Retrieve an operator spec by ID."""
    return _OPERATOR_CATALOG.get(operator_id)


def list_operators(logical_unit: Optional[LogicalUnit] = None) -> List[OperatorSpec]:
    """List operators, optionally filtered by logical unit."""
    if logical_unit:
        return [op for op in _OPERATOR_CATALOG.values() if op.logical_unit == logical_unit]
    return list(_OPERATOR_CATALOG.values())


list_operator_specs = list_operators


def get_unit_capabilities() -> Dict[str, Any]:
    """Return catalog capabilities grouped by logical unit with physical/simulated metadata."""
    result: Dict[str, Any] = {}
    unit_meta = {
        LogicalUnit.CPU: {"name": "General Processing", "physical": True, "simulated": False},
        LogicalUnit.GPU: {"name": "Vector & Parallel Analytics", "physical": False, "simulated": False, "cpu_fallback": True},
        LogicalUnit.TPU: {"name": "Tensor Processing", "physical": False, "simulated": False, "portable_onnx": True},
        LogicalUnit.NPU: {"name": "Neural Inference", "physical": False, "simulated": False, "cpu_fallback": True},
        LogicalUnit.DPU: {"name": "Data Preparation", "physical": True, "simulated": False},
        LogicalUnit.QPU: {"name": "Quantum Simulation", "physical": False, "simulated": True, "strict_simulation_label": True},
        LogicalUnit.APU: {"name": "Heterogeneous Scheduling", "physical": True, "simulated": False},
        LogicalUnit.LPU: {"name": "Local Language Processing", "physical": True, "simulated": False, "air_gapped": True},
        LogicalUnit.IPU: {"name": "Graph Intelligence", "physical": True, "simulated": False},
        LogicalUnit.VPU: {"name": "Vision & Document Processing", "physical": True, "simulated": False},
    }
    for unit, meta in unit_meta.items():
        ops = list_operators(unit)
        result[unit.value] = {
            "unit": unit.value,
            "display_name": meta["name"],
            "physical": meta.get("physical", False),
            "simulated": meta.get("simulated", False),
            "operator_count": len(ops),
            "operators": [op.operator_id for op in ops],
            "metadata": meta,
        }
    return result



# ===========================================================================
# 1. CPU: General Processing (PUR-CPU-001..005)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="records.validate",
    logical_unit=LogicalUnit.CPU,
    description="Validate JSON records against a registered JSON Schema without echoing secret values.",
    parameter_schema={"schema_id": {"type": "string"}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="records.transform",
    logical_unit=LogicalUnit.CPU,
    description="Declarative select/rename/filter/cast with an allowlisted expression AST; no eval.",
    parameter_schema={"projections": {"type": "object"}, "filter": {"type": "object"}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="records.aggregate",
    logical_unit=LogicalUnit.CPU,
    description="Count/sum/min/max/mean grouped by declared fields with stable ordering.",
    parameter_schema={"group_by": {"type": "array"}, "aggregations": {"type": "object"}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="records.sort_deduplicate",
    logical_unit=LogicalUnit.CPU,
    description="Stable key sort and exact-key deduplication with first/last/error policy.",
    parameter_schema={"keys": {"type": "array"}, "policy": {"type": "string", "enum": ["first", "last", "error"]}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="graph.bounded_traverse",
    logical_unit=LogicalUnit.CPU,
    description="Traverse authorized graph snapshot with depth/result bounds and cycle rejection.",
    parameter_schema={"root_id": {"type": "string"}, "max_depth": {"type": "integer", "maximum": 8}},
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))


# ===========================================================================
# 2. GPU: Vector and Parallel Analytics (PUR-GPU-001..005)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="vector.cosine_top_k",
    logical_unit=LogicalUnit.GPU,
    description="Vector cosine similarity top-k ranking over numeric candidate matrix with zero-vector policy.",
    accepted_profiles=["cpu", "gpu_directml"],
    parameter_schema={"k": {"type": "integer", "minimum": 1, "maximum": 1000}, "zero_vector_policy": {"type": "string"}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="tensor.matmul",
    logical_unit=LogicalUnit.GPU,
    description="2D and batched matrix multiplication with broadcast checks and precision preservation.",
    accepted_profiles=["cpu", "gpu_directml"],
    parameter_schema={"transpose_b": {"type": "boolean"}},
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="vector.reduce",
    logical_unit=LogicalUnit.GPU,
    description="Axis-wise reduction (sum, mean, min, max, L2 norm) over numeric arrays.",
    accepted_profiles=["cpu", "gpu_directml"],
    parameter_schema={"axis": {"type": "integer"}, "op": {"type": "string", "enum": ["sum", "mean", "min", "max", "l2_norm"]}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="sparse.matmul",
    logical_unit=LogicalUnit.GPU,
    description="Compressed Sparse Row (CSR) by dense matrix multiplication with zero unexpected densification.",
    accepted_profiles=["cpu", "gpu_directml"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))


# ===========================================================================
# 3. TPU: Tensor Processing (PUR-TPU-001..005)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="tensor.elementwise",
    logical_unit=LogicalUnit.TPU,
    description="Elementwise tensor operations (add, multiply, relu, sigmoid).",
    accepted_profiles=["cpu", "onnx_cpu"],
    parameter_schema={"op": {"type": "string", "enum": ["add", "multiply", "relu", "sigmoid"]}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="tensor.softmax",
    logical_unit=LogicalUnit.TPU,
    description="Numerically stable softmax along declared tensor axis.",
    accepted_profiles=["cpu", "onnx_cpu"],
    parameter_schema={"axis": {"type": "integer"}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="tensor.conv2d",
    logical_unit=LogicalUnit.TPU,
    description="2D Convolution over NCHW tensor with explicit pads/stride/dilation.",
    accepted_profiles=["cpu", "onnx_cpu"],
    parameter_schema={"stride": {"type": "integer"}, "padding": {"type": "integer"}},
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="tensor.pool2d",
    logical_unit=LogicalUnit.TPU,
    description="2D Pooling (max/average) over NCHW tensor.",
    accepted_profiles=["cpu", "onnx_cpu"],
    parameter_schema={"mode": {"type": "string", "enum": ["max", "avg"]}, "kernel_size": {"type": "integer"}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="tensor.normalize",
    logical_unit=LogicalUnit.TPU,
    description="Tensor normalization (L2 or LayerNorm) with explicit epsilon.",
    accepted_profiles=["cpu", "onnx_cpu"],
    parameter_schema={"epsilon": {"type": "number", "default": 1e-5}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="tensor.reshape",
    logical_unit=LogicalUnit.TPU,
    description="Validated element count and dimension layout reshape.",
    accepted_profiles=["cpu", "onnx_cpu"],
    parameter_schema={"target_shape": {"type": "array"}},
    default_budgets=OperatorBudget(deadline_seconds=10.0, memory_mib=128),
))

register_operator(OperatorSpec(
    operator_id="tensor.graph_infer",
    logical_unit=LogicalUnit.TPU,
    description="Execute approved ONNX computational graph with fixed allowed opsets and shapes.",
    accepted_profiles=["cpu", "onnx_cpu"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="model.quantization_evaluate",
    logical_unit=LogicalUnit.TPU,
    description="Evaluate quantized model against reference with metrics and resource delta.",
    accepted_profiles=["cpu"],
    default_budgets=OperatorBudget(deadline_seconds=120.0, memory_mib=1024),
))


# ===========================================================================
# 4. NPU: Neural Inference (PUR-NPU-001..005)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="model.infer",
    logical_unit=LogicalUnit.NPU,
    description="Execute approved neural model artifact with bounded inputs.",
    accepted_profiles=["cpu", "onnx_cpu", "npu_openvino"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="text.embed",
    logical_unit=LogicalUnit.NPU,
    description="Generate dense text embeddings using approved local model and tokenizer.",
    accepted_profiles=["cpu", "onnx_cpu", "npu_openvino"],
    parameter_schema={"normalize": {"type": "boolean", "default": True}},
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="model.classify",
    logical_unit=LogicalUnit.NPU,
    description="Neural classification with label mapping and explicit abstention threshold.",
    accepted_profiles=["cpu", "onnx_cpu", "npu_openvino"],
    parameter_schema={"abstention_threshold": {"type": "number", "default": 0.5}},
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="model.batch_infer",
    logical_unit=LogicalUnit.NPU,
    description="Bounded microbatching preserving per-input IDs without cross-tenant mixing.",
    accepted_profiles=["cpu", "onnx_cpu", "npu_openvino"],
    parameter_schema={"batch_size": {"type": "integer", "maximum": 32}},
    default_budgets=OperatorBudget(deadline_seconds=90.0, memory_mib=1024),
))


# ===========================================================================
# 5. DPU: Data Preparation (PUR-DPU-001..005)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="data.prepare_batches",
    logical_unit=LogicalUnit.DPU,
    description="Stream bounded records from acquired artifact, validate schema, and batch by bytes/rows.",
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="data.checksum",
    logical_unit=LogicalUnit.DPU,
    description="Calculate verified SHA-256 digest of artifact payload.",
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=128),
))

register_operator(OperatorSpec(
    operator_id="data.compress",
    logical_unit=LogicalUnit.DPU,
    description="Compress payload using standard gzip with size checks.",
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="data.decompress",
    logical_unit=LogicalUnit.DPU,
    description="Decompress gzip stream with decompressed-byte ratio and bomb protection.",
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="data.classify_redact",
    logical_unit=LogicalUnit.DPU,
    description="Recursive classification and PII/secret redaction before model delivery.",
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="data.deduplicate",
    logical_unit=LogicalUnit.DPU,
    description="Content/key-based duplicate detection with collision-safe digest verification.",
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="data.ingestion_envelope",
    logical_unit=LogicalUnit.DPU,
    description="Produce typed SourceEvent v2 envelopes with provenance handoff and quality counts.",
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))


# ===========================================================================
# 6. QPU: Quantum Simulation (PUR-QPU-001..006)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="quantum.simulate",
    logical_unit=LogicalUnit.QPU,
    description="Simulate bounded quantum circuit (statevector/density matrix); always flagged simulation=true.",
    accepted_profiles=["cpu_qiskit_aer"],
    parameter_schema={"method": {"type": "string", "enum": ["statevector", "density_matrix"]}},
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="quantum.sample",
    logical_unit=LogicalUnit.QPU,
    description="Sample bitstrings from simulated quantum circuit with declared endianness and seed.",
    accepted_profiles=["cpu_qiskit_aer"],
    parameter_schema={"shots": {"type": "integer", "maximum": 4096}, "seed": {"type": "integer"}},
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="quantum.expectation",
    logical_unit=LogicalUnit.QPU,
    description="Calculate expectation value of Pauli observable sums over simulated state.",
    accepted_profiles=["cpu_qiskit_aer"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="quantum.maxcut_experiment",
    logical_unit=LogicalUnit.QPU,
    description="Bounded QAOA-style MaxCut experiment (<=12 vertices, p<=2) compared with classical solver.",
    accepted_profiles=["cpu_qiskit_aer"],
    default_budgets=OperatorBudget(deadline_seconds=90.0, memory_mib=512),
))


# ===========================================================================
# 7. APU: Heterogeneous Workflow Scheduling (PUR-APU-001..005)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="workflow.plan",
    logical_unit=LogicalUnit.APU,
    description="Validate and compile heterogeneous operator DAG with aggregate budgets and cycle checks.",
    default_budgets=OperatorBudget(deadline_seconds=15.0, memory_mib=128),
))

register_operator(OperatorSpec(
    operator_id="workflow.run",
    logical_unit=LogicalUnit.APU,
    description="Execute approved DAG workflow with checkpointing and atomic stage publication.",
    default_budgets=OperatorBudget(deadline_seconds=300.0, memory_mib=1024),
))


# ===========================================================================
# 8. LPU: Local Language Processing (PUR-LPU-001..006)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="text.chunk",
    logical_unit=LogicalUnit.LPU,
    description="Deterministic Unicode-safe text chunking with byte offsets and overlap tracking.",
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="text.tokenize",
    logical_unit=LogicalUnit.LPU,
    description="Exact token counting and offset mapping using pinned tokenizer.",
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="text.retrieve",
    logical_unit=LogicalUnit.LPU,
    description="Authorized hybrid retrieval returning exact source spans and citations.",
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="text.extract",
    logical_unit=LogicalUnit.LPU,
    description="Local model extraction constrained to registered schema with evidence spans and abstention.",
    accepted_profiles=["cpu_llm_local"],
    default_budgets=OperatorBudget(deadline_seconds=90.0, memory_mib=1024),
))

register_operator(OperatorSpec(
    operator_id="text.summarize_grounded",
    logical_unit=LogicalUnit.LPU,
    description="Citation-bearing summarization strictly grounded in authorized retrieved passages.",
    accepted_profiles=["cpu_llm_local"],
    default_budgets=OperatorBudget(deadline_seconds=90.0, memory_mib=1024),
))

register_operator(OperatorSpec(
    operator_id="query.propose",
    logical_unit=LogicalUnit.LPU,
    description="Generate structured read-query proposal without automatic execution.",
    accepted_profiles=["cpu_llm_local"],
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=512),
))


# ===========================================================================
# 9. IPU: Graph Intelligence (PUR-IPU-001..005)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="graph.to_csr",
    logical_unit=LogicalUnit.IPU,
    description="Export authorized graph snapshot into validated CSR sparse representation with stable IDs.",
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="graph.components",
    logical_unit=LogicalUnit.IPU,
    description="Compute connected components (weak/strong) over CSR matrix via SciPy.",
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="graph.shortest_paths",
    logical_unit=LogicalUnit.IPU,
    description="Compute bounded shortest paths over graph topology.",
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="graph.aggregate_features",
    logical_unit=LogicalUnit.IPU,
    description="Sparse neighbor feature aggregation (sum/mean) with normalization.",
    default_budgets=OperatorBudget(deadline_seconds=45.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="graph.cluster_features",
    logical_unit=LogicalUnit.IPU,
    description="K-means/spectral clustering diagnostics over graph feature matrix.",
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="graph.model_infer",
    logical_unit=LogicalUnit.IPU,
    description="Execute approved graph neural model artifact with provenance attribution.",
    accepted_profiles=["cpu", "onnx_cpu"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))


# ===========================================================================
# 10. VPU: Vision and Document Processing (PUR-VPU-001..006)
# ===========================================================================
register_operator(OperatorSpec(
    operator_id="vision.preprocess",
    logical_unit=LogicalUnit.VPU,
    description="Allowlisted image decode, resize, grayscale/threshold, and deskew via OpenCV.",
    accepted_profiles=["cpu_opencv"],
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="vision.ocr",
    logical_unit=LogicalUnit.VPU,
    description="Local OCR extraction returning structured boxes, text, and confidence scores.",
    accepted_profiles=["cpu_tesseract"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="vision.layout_evidence",
    logical_unit=LogicalUnit.VPU,
    description="Deterministic grouping of OCR text lines into reading-order layout blocks.",
    accepted_profiles=["cpu"],
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="vision.duplicate_score",
    logical_unit=LogicalUnit.VPU,
    description="Pixel hash and perceptual difference distance between two image artifacts.",
    accepted_profiles=["cpu"],
    default_budgets=OperatorBudget(deadline_seconds=30.0, memory_mib=256),
))

register_operator(OperatorSpec(
    operator_id="vision.keyframes",
    logical_unit=LogicalUnit.VPU,
    description="Extract keyframes from uploaded video with duration and pixel limits.",
    accepted_profiles=["cpu_opencv"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))

register_operator(OperatorSpec(
    operator_id="vision.model_infer",
    logical_unit=LogicalUnit.VPU,
    description="Execute approved ONNX vision model with preprocessed image tensors.",
    accepted_profiles=["cpu", "onnx_cpu"],
    default_budgets=OperatorBudget(deadline_seconds=60.0, memory_mib=512),
))
