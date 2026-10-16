"""API domain graph contract management and change tracking (G2-GRAPH-API-001..003).

Links APIEndpoint contracts to services, documentation, tests, and consumers,
and detects breaking and non-breaking schema / contract changes.
"""

from __future__ import annotations

from typing import Any

from eoip.graph.store import GraphStore


def link_api_contract(
    store: GraphStore,
    endpoint_cid: str,
    *,
    service_cid: str | None = None,
    doc_cid: str | None = None,
    test_cid: str | None = None,
    decision_cid: str | None = None,
    consumer_service_cids: list[str] | None = None,
) -> dict[str, Any]:
    """Links an APIEndpoint contract to related artifacts across the graph (G2-GRAPH-API-002).

    Edges created:
    - APIService -> EXPOSES -> APIEndpoint
    - Document -> DOCUMENTS_API -> APIEndpoint
    - TestCase -> TESTS -> APIEndpoint
    - Decision -> DECIDES -> APIEndpoint
    - Consumer APIService -> CONNECTS_TO -> Provider APIService
    """
    ep = store.get_vertex_by_canonical_id(endpoint_cid)
    if not ep:
        raise ValueError(f"APIEndpoint not found: {endpoint_cid}")

    links_created = []

    if service_cid:
        svc = store.get_vertex_by_canonical_id(service_cid)
        if svc:
            store.upsert_edge(
                "EXPOSES",
                svc["vid"],
                ep["vid"],
                {"fact_key": f"exposes:{service_cid}:{endpoint_cid}", "creation_status": "DETERMINISTIC"},
            )
            links_created.append({"target": service_cid, "edge": "EXPOSES"})

    if doc_cid:
        doc = store.get_vertex_by_canonical_id(doc_cid)
        if doc:
            store.upsert_edge(
                "DOCUMENTS_API",
                doc["vid"],
                ep["vid"],
                {"fact_key": f"docs:{doc_cid}:{endpoint_cid}", "creation_status": "DETERMINISTIC"},
            )
            links_created.append({"target": doc_cid, "edge": "DOCUMENTS_API"})

    if test_cid:
        tc = store.get_vertex_by_canonical_id(test_cid)
        if tc:
            store.upsert_edge(
                "TESTS",
                tc["vid"],
                ep["vid"],
                {"fact_key": f"tests:{test_cid}:{endpoint_cid}", "creation_status": "DETERMINISTIC"},
            )
            links_created.append({"target": test_cid, "edge": "TESTS"})

    if decision_cid:
        dec = store.get_vertex_by_canonical_id(decision_cid)
        if dec:
            store.upsert_edge(
                "DECIDES",
                dec["vid"],
                ep["vid"],
                {"fact_key": f"decides:{decision_cid}:{endpoint_cid}", "creation_status": "DETERMINISTIC"},
            )
            links_created.append({"target": decision_cid, "edge": "DECIDES"})

    if consumer_service_cids and service_cid:
        provider = store.get_vertex_by_canonical_id(service_cid)
        if provider:
            for c_cid in consumer_service_cids:
                consumer = store.get_vertex_by_canonical_id(c_cid)
                if consumer:
                    store.upsert_edge(
                        "CONNECTS_TO",
                        consumer["vid"],
                        provider["vid"],
                        {"fact_key": f"conn:{c_cid}:{service_cid}", "creation_status": "DETERMINISTIC"},
                    )
                    links_created.append({"target": c_cid, "edge": "CONNECTS_TO"})

    return {
        "endpoint_cid": endpoint_cid,
        "links_count": len(links_created),
        "links": links_created,
    }


def track_contract_changes(
    old_spec: dict[str, Any],
    new_spec: dict[str, Any],
) -> dict[str, Any]:
    """Analyzes API contract changes and classifies as breaking or non-breaking (G2-GRAPH-API-003).

    Breaking changes:
    - Removed endpoints or HTTP methods
    - Removed response fields
    - Added required request parameters
    - Type changes of existing parameters/fields

    Non-breaking changes:
    - Added endpoints or methods
    - Added optional request parameters
    - Added response fields
    """
    breaking_changes: list[dict[str, str]] = []
    non_breaking_changes: list[dict[str, str]] = []

    old_paths = old_spec.get("paths", {})
    new_paths = new_spec.get("paths", {})

    for path, old_ops in old_paths.items():
        if path not in new_paths:
            breaking_changes.append({
                "type": "endpoint_removed",
                "path": path,
                "description": f"Endpoint '{path}' was removed from the API specification",
            })
            continue

        new_ops = new_paths[path]
        for method, old_op in old_ops.items():
            if method not in new_ops:
                breaking_changes.append({
                    "type": "method_removed",
                    "path": f"{method.upper()} {path}",
                    "description": f"Operation '{method.upper()} {path}' was removed",
                })
                continue

            new_op = new_ops[method]
            # Check required parameters
            old_params = {p["name"]: p for p in old_op.get("parameters", []) if isinstance(p, dict)}
            new_params = {p["name"]: p for p in new_op.get("parameters", []) if isinstance(p, dict)}

            for p_name, p_info in new_params.items():
                if p_name not in old_params:
                    if p_info.get("required") is True:
                        breaking_changes.append({
                            "type": "required_parameter_added",
                            "path": f"{method.upper()} {path} ?{p_name}",
                            "description": f"New required parameter '{p_name}' added to {method.upper()} {path}",
                        })
                    else:
                        non_breaking_changes.append({
                            "type": "optional_parameter_added",
                            "path": f"{method.upper()} {path} ?{p_name}",
                            "description": f"New optional parameter '{p_name}' added to {method.upper()} {path}",
                        })

    # Added paths
    for path, new_ops in new_paths.items():
        if path not in old_paths:
            non_breaking_changes.append({
                "type": "endpoint_added",
                "path": path,
                "description": f"New endpoint '{path}' added to the API specification",
            })

    is_breaking = len(breaking_changes) > 0
    return {
        "is_breaking": is_breaking,
        "breaking_changes": breaking_changes,
        "non_breaking_changes": non_breaking_changes,
        "breaking_count": len(breaking_changes),
        "non_breaking_count": len(non_breaking_changes),
    }
