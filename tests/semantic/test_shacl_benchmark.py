"""SHACL throughput microbenchmark test (CRA-020.11).

Throughput qualification target: >= 20,000 nodes/s on node batches.
"""

from __future__ import annotations
import time
from types import SimpleNamespace
import pytest

from eoip.ontology.shacl_validator import SHACLValidator, SHACLShape, SHACLSeverity


def test_shacl_throughput_qualification():
    """CRA-020.11: SHACL throughput qualification target >= 20,000 nodes/s."""
    validator = SHACLValidator()
    validator.shapes = {}
    validator.register_shape(SHACLShape(
        shape_id="BenchmarkShape",
        target_class="Service",
        required_properties=["canonical_id", "name"],
        property_types={"name": "string"},
        min_counts={"name": 1},
        max_counts={"name": 1},
    ))

    # Generate 10,000 valid vertices
    batch_size = 10_000
    vertices = [
        {
            "label": "Service",
            "canonical_id": f"srv-{i}",
            "properties": {"name": f"Service-{i}", "canonical_id": f"srv-{i}"},
        }
        for i in range(batch_size)
    ]
    store = SimpleNamespace(find_vertices=lambda: vertices, find_edges=lambda: [])

    start = time.perf_counter()
    report = validator.validate(store, timeout_seconds=10.0)
    elapsed = time.perf_counter() - start

    assert report.conforms is True
    assert report.nodes_checked == batch_size

    nodes_per_second = batch_size / elapsed
    print(f"\nThroughput: {nodes_per_second:,.1f} nodes/sec (Elapsed: {elapsed*1000:.1f}ms for {batch_size} nodes)")
    # Target is >= 20,000 nodes/s
    assert nodes_per_second >= 20_000, f"Throughput {nodes_per_second} below target 20,000 nodes/s"
