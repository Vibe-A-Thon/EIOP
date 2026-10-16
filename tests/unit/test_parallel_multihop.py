import pytest
from eoip.analytics.parallel_multihop import (
    SparseGraphBuilder,
    SparseGraphMatrix,
    ParallelMultiHopEngine,
    SubgraphPartitioner,
    FraudRingDetector,
)
from eoip.graph.memory import MemoryGraphStore


@pytest.mark.req("KGR-G-018")
def test_sparse_graph_builder_and_csr():
    builder = SparseGraphBuilder()
    builder.add_edge("A", "B", 1.0)
    builder.add_edge("B", "C", 2.0)
    builder.add_edge("C", "D", 1.5)
    matrix = builder.build()

    assert matrix.num_nodes == 4
    assert matrix.num_edges == 3
    assert "A" in matrix.node_index
    assert "B" in matrix.node_index

    a_idx = matrix.node_index["A"]
    neighbors = matrix.neighbors(a_idx)
    assert len(neighbors) == 1
    target_idx, weight = neighbors[0]
    assert matrix.node_ids[target_idx] == "B"
    assert weight == 1.0


@pytest.mark.req("KGR-G-018")
def test_parallel_multihop_bfs_deep_traversal():
    builder = SparseGraphBuilder()
    # Create chain A -> B -> C -> D -> E -> F -> G (6 hops)
    nodes = ["N0", "N1", "N2", "N3", "N4", "N5", "N6"]
    for i in range(len(nodes) - 1):
        builder.add_edge(nodes[i], nodes[i + 1])
    # Add a branch at N3 -> X -> Y
    builder.add_edge("N3", "X")
    builder.add_edge("X", "Y")

    matrix = builder.build()
    engine = ParallelMultiHopEngine(matrix, max_hops=10, max_workers=2)

    res = engine.multi_hop_bfs("N0", hops=6)
    assert res.root_node == "N0"
    assert res.total_hops == 6
    assert res.total_nodes_reached == 8  # N1..N6, X, Y
    assert len(res.per_hop) == 6
    assert res.per_hop[0].nodes == ["N1"]
    assert "N6" in res.per_hop[5].nodes or "Y" in res.per_hop[4].nodes


@pytest.mark.req("KGR-G-018")
def test_influence_propagation():
    builder = SparseGraphBuilder()
    builder.add_edge("source", "A", 1.0)
    builder.add_edge("A", "B", 0.8)
    builder.add_edge("B", "C", 0.5)

    matrix = builder.build()
    engine = ParallelMultiHopEngine(matrix)

    scores = engine.influence_propagation(["source"], hops=4, decay_factor=0.5)
    assert scores["source"] == 1.0
    assert scores["A"] == 0.5
    assert scores["B"] == 0.5 * 0.5 * 0.8  # 0.2
    assert "C" in scores
    assert scores["C"] < scores["B"]


@pytest.mark.req("KGR-G-018")
def test_subgraph_partitioning_and_fraud_ring_detector():
    builder = SparseGraphBuilder()
    # Create cycle: R1 -> R2 -> R3 -> R1
    builder.add_edge("R1", "R2")
    builder.add_edge("R2", "R3")
    builder.add_edge("R3", "R1")

    # Create isolated edge: I1 -> I2
    builder.add_edge("I1", "I2")

    matrix = builder.build()
    partitioner = SubgraphPartitioner()
    components = partitioner.partition_by_component(matrix)
    assert len(components) == 2

    degree_partitions = partitioner.partition_by_degree(matrix, num_partitions=2)
    assert len(degree_partitions) == 2

    engine = ParallelMultiHopEngine(matrix)
    detector = FraudRingDetector(engine)
    rings = detector.detect_rings(min_ring_size=3, max_ring_size=5)
    assert len(rings) >= 1
    ring_nodes = set(rings[0].nodes)
    assert {"R1", "R2", "R3"}.issubset(ring_nodes)
    assert rings[0].risk_score > 0.0


@pytest.mark.req("KGR-G-018")
def test_from_graph_store():
    store = MemoryGraphStore()
    v1 = store.upsert_vertex("Service", {"canonical_id": "svc:v1", "name": "V1"})
    v2 = store.upsert_vertex("Service", {"canonical_id": "svc:v2", "name": "V2"})
    store.upsert_edge("CALLS", v1["vid"], v2["vid"], {})

    builder = SparseGraphBuilder()
    matrix = builder.from_graph_store(store)
    assert matrix.num_nodes == 2
    assert matrix.num_edges == 1
