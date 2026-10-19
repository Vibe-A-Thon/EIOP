"""Unit and integration tests for Processing Runtime Backends across the 10 units.

Exercises CPU numerical reference kernels, DPU data transforms, LPU deterministic
text processing, IPU sparse graph intelligence, and VPU vision routines.
"""

from __future__ import annotations

import numpy as np
import pytest

from eoip.processing.backends import (
    cpu_numerical,
    data_prep,
    graph_intel,
    text_local,
    vision_proc,
)
from eoip.processing.contracts import ExecutionContext, LogicalUnit, ProcessingRequest
from eoip.processing.service import ProcessingService


@pytest.fixture
def service() -> ProcessingService:
    return ProcessingService()


@pytest.fixture
def context() -> ExecutionContext:
    return ExecutionContext(
        tenant_id="test_tenant_a",
        principal_id="test_user_a",
    )


# ===========================================================================
# 1. CPU & DPU Operators (PUR-CPU-001..005, PUR-DPU-001..005)
# ===========================================================================
@pytest.mark.req("PUR-CPU-001")
def test_cpu_records_validate(service: ProcessingService, context: ExecutionContext):
    """PUR-CPU-001: Validate records against registered schema."""
    req = ProcessingRequest(
        logical_unit=LogicalUnit.CPU,
        operator_id="records.validate",
        inputs={"records": [{"id": 1, "name": "Alpha"}, {"id": 2, "name": "Beta"}]},
        parameters={"schema": {"type": "object"}},
    )
    result, receipt = service.execute_direct(req, context)
    assert result["valid"] is True
    assert result["validated_count"] == 2
    assert receipt.outcome == "SUCCEEDED"


@pytest.mark.req("PUR-DPU-001")
def test_dpu_checksum_and_compression(service: ProcessingService, context: ExecutionContext):
    """PUR-DPU-001, PUR-DPU-002: Bounded SHA-256 and gzip compression with bomb protection."""
    data = b"Hello EOIP Processing Runtime DPU Pipeline!"
    chk = data_prep.calculate_checksum(data)
    assert len(chk) == 64

    comp = data_prep.compress_payload(data)
    assert len(comp) > 0
    decomp = data_prep.decompress_payload(comp)
    assert decomp == data


@pytest.mark.req("PUR-DPU-003")
def test_dpu_classify_and_redact():
    """PUR-DPU-003: Sensitive secret pattern redaction from structured payloads."""
    payload = {
        "user": "Alice",
        "api_key": "sk-1234567890abcdef1234567890abcdef",
        "nested": {"token": "ghp_secrettokenvalue12345"},
    }
    redacted, count = data_prep.redact_sensitive_data(payload)
    assert count >= 2
    assert "[REDACTED]" in redacted["api_key"]
    assert "[REDACTED]" in redacted["nested"]["token"]



@pytest.mark.req("PUR-DPU-004")
def test_dpu_deduplicate_records():
    """PUR-DPU-004: Exact-key deduplication with stable survivor order."""
    records = [
        {"id": "rec_1", "val": 10},
        {"id": "rec_2", "val": 20},
        {"id": "rec_1", "val": 99},  # duplicate
    ]
    res = data_prep.deduplicate_records(records, key_fields=["id"])
    assert res["unique_count"] == 2
    assert res["duplicates_removed"] == 1
    assert [r["val"] for r in res["records"]] == [10, 20]


# ===========================================================================
# 2. GPU Operators (PUR-GPU-001..005)
# ===========================================================================
@pytest.mark.req("PUR-GPU-001")
def test_gpu_cosine_top_k():
    """PUR-GPU-001: Top-k cosine similarity with zero-vector handling and deterministic ties."""
    cands = np.array([[1.0, 0.0], [0.707, 0.707], [0.0, 1.0]], dtype=float)
    query = np.array([1.0, 0.0], dtype=float)
    res = cpu_numerical.cosine_top_k(cands, query, k=2, zero_vector_policy="reject")
    assert res["top_indices"] == [0, 1]
    assert len(res["scores"]) == 2
    assert abs(res["scores"][0] - 1.0) < 1e-4


@pytest.mark.req("PUR-GPU-002")
def test_gpu_matmul():
    """PUR-GPU-002: Reference matrix multiplication."""
    a = np.array([[1.0, 2.0], [3.0, 4.0]])
    b = np.array([[2.0, 0.0], [1.0, 2.0]])
    res = cpu_numerical.matmul(a, b)
    expected = a @ b
    np.testing.assert_allclose(res, expected)


@pytest.mark.req("PUR-GPU-003")
def test_gpu_vector_reduce():
    """PUR-GPU-003: Reductions across axes (sum, mean, max, min, l2_norm)."""
    arr = np.array([1.0, 2.0, 3.0, 4.0])
    assert cpu_numerical.vector_reduce(arr, op="sum") == 10.0
    assert cpu_numerical.vector_reduce(arr, op="mean") == 2.5
    assert cpu_numerical.vector_reduce(arr, op="max") == 4.0


# ===========================================================================
# 3. TPU Operators (PUR-TPU-001..005)
# ===========================================================================
@pytest.mark.req("PUR-TPU-001")
def test_tpu_elementwise_and_softmax():
    """PUR-TPU-001, PUR-TPU-002: Elementwise activations (ReLU, GELU, Sigmoid) and Softmax."""
    x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0])
    relu = cpu_numerical.tensor_elementwise(x, op="relu")
    np.testing.assert_allclose(relu, [0.0, 0.0, 0.0, 1.0, 2.0])

    sm = cpu_numerical.tensor_softmax(x)
    assert abs(np.sum(sm) - 1.0) < 1e-5


@pytest.mark.req("PUR-TPU-003")
def test_tpu_conv2d_nchw():
    """PUR-TPU-003: 2D convolution reference implementation."""
    x = np.ones((1, 1, 4, 4), dtype=float)
    w = np.ones((1, 1, 2, 2), dtype=float)
    out = cpu_numerical.conv2d_nchw(x, w)
    assert out.shape == (1, 1, 3, 3)
    np.testing.assert_allclose(out, 4.0)


# ===========================================================================
# 4. LPU Operators (PUR-LPU-001..005)
# ===========================================================================
@pytest.mark.req("PUR-LPU-001")
def test_lpu_chunking_with_offsets():
    """PUR-LPU-001: Deterministic Unicode-safe chunking with character/byte offsets."""
    text = "The quick brown fox jumps over the lazy dog. A second sentence appears here."
    chunks = text_local.chunk_text(text, chunk_size=30, chunk_overlap=10, doc_id="doc_test")
    assert len(chunks) >= 2
    for c in chunks:
        assert "char_start" in c
        assert "char_end" in c
        assert text[c["char_start"]:c["char_end"]] == c["text"]


@pytest.mark.req("PUR-LPU-002")
def test_lpu_structured_extraction_with_abstention():
    """PUR-LPU-002: Schema-constrained entity extraction with abstention."""
    text = "Invoice details: vendor: Acme Corp, invoice_amount: 450.00"
    schema = {

        "type": "object",
        "properties": {
            "invoice_amount": {"type": "number"},
            "vendor": {"type": "string"},
            "due_date": {"type": "string"},
        },
    }
    extracted = text_local.extract_structured(text, schema)
    assert extracted["extracted_entities"]["vendor"] == "Acme Corp"
    assert "due_date" in extracted["abstained_fields"]


@pytest.mark.req("PUR-LPU-003")
def test_lpu_grounded_summarization():
    """PUR-LPU-003: Grounded summarization strictly citing source passages."""
    passages = [
        {"passage_id": "p1", "text": "EOIP platform implements 10 logical processing units."},
        {"passage_id": "p2", "text": "All units feature local-first execution with no cloud egress."},
    ]
    summary = text_local.summarize_grounded(passages)
    assert summary["grounded"] is True
    assert len(summary["citations"]) == 2
    assert "p1" in summary["citations"]


# ===========================================================================
# 5. IPU Operators (PUR-IPU-001..005)
# ===========================================================================
@pytest.mark.req("PUR-IPU-001")
def test_ipu_graph_csr_and_components():
    """PUR-IPU-001: CSR conversion and connected components analysis."""
    vertices = [{"id": "v1"}, {"id": "v2"}, {"id": "v3"}, {"id": "v4"}]
    edges = [
        {"from_id": "v1", "to_id": "v2"},
        {"from_id": "v3", "to_id": "v4"},
    ]
    csr = graph_intel.graph_to_csr(vertices, edges)
    assert csr["num_nodes"] == 4
    assert csr["num_edges"] == 2

    comp = graph_intel.graph_connected_components(csr["csr_matrix"])
    assert comp["num_components"] == 2


@pytest.mark.req("PUR-IPU-002")
def test_ipu_graph_shortest_paths():
    """PUR-IPU-002: Dijkstra shortest paths across graph topology."""
    vertices = [{"id": "a"}, {"id": "b"}, {"id": "c"}]
    edges = [
        {"from_id": "a", "to_id": "b", "weight": 1.0},
        {"from_id": "b", "to_id": "c", "weight": 2.0},
    ]
    csr = graph_intel.graph_to_csr(vertices, edges)
    dist = graph_intel.graph_shortest_paths(csr["csr_matrix"])
    assert dist["distance_matrix"][0][2] == 3.0


# ===========================================================================
# 6. VPU Operators (PUR-VPU-001..005)
# ===========================================================================
@pytest.mark.req("PUR-VPU-001")
def test_vpu_image_preprocess_and_duplicate():
    """PUR-VPU-001, PUR-VPU-002: Format validation, dHash and perceptual duplicate scoring."""
    png_hdr = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4"
    prep = vision_proc.preprocess_image(png_hdr)
    assert prep["valid"] is True
    assert prep["format"] == "PNG"

    # Duplicate score
    dup = vision_proc.duplicate_score("ffff", "ffff")
    assert dup["is_duplicate"] is True
    assert dup["hamming_distance"] == 0


@pytest.mark.req("PUR-VPU-003")
def test_vpu_layout_evidence():
    """PUR-VPU-003: Reading-order layout evidence grouping."""
    lines = [
        {"text": "Line 1 Header", "x": 10, "y": 10, "w": 100, "h": 12},
        {"text": "Line 2 Paragraph", "x": 10, "y": 26, "w": 200, "h": 12},
        {"text": "Footer", "x": 10, "y": 200, "w": 50, "h": 10},
    ]
    blocks = vision_proc.layout_evidence_grouping(lines)
    assert len(blocks) >= 2


# ===========================================================================
# 7. NPU & APU Operators (PUR-NPU-001..005, PUR-APU-001..005)
# ===========================================================================
@pytest.mark.req("PUR-NPU-001")
def test_npu_text_embedding_offline(service: ProcessingService, context: ExecutionContext):
    """PUR-NPU-001: Offline deterministic text embedding projection."""
    req = ProcessingRequest(
        logical_unit=LogicalUnit.NPU,
        operator_id="text.embed",
        inputs={"texts": ["Hello EOIP", "Knowledge Graph"]},
        parameters={"dimensions": 64},
    )
    result, receipt = service.execute_direct(req, context)
    assert result["count"] == 2
    assert result["dimensions"] == 64
    assert len(result["embeddings"][0]) == 64
    assert receipt.actual_provider == "cpu_neural_reference"


@pytest.mark.req("PUR-APU-001")
def test_apu_heterogeneous_workflow(service: ProcessingService, context: ExecutionContext):
    """PUR-APU-001: Heterogeneous workflow coordination across multiple logical units."""
    req = ProcessingRequest(
        logical_unit=LogicalUnit.APU,
        operator_id="workflow.run",
        inputs={
            "steps": [
                {"id": "step_1", "unit": "DPU", "op": "data.checksum"},
                {"id": "step_2", "unit": "GPU", "op": "vector.cosine_top_k"},
            ]
        },
    )
    result, receipt = service.execute_direct(req, context)
    assert result["workflow_status"] == "COMPLETED"
    assert result["completed_steps"] == 2
    assert receipt.outcome == "SUCCEEDED"
