"""Normalize declared code-export facts into the existing ontology."""

from __future__ import annotations

import json
from typing import Any


def normalize_code_export(data: dict[str, Any]) -> dict[str, Any]:
    repository = data["repository"]
    if isinstance(repository, str):
        repository = {
            "repo_id": repository, "name": repository,
            "source_uri": data.get("remote_url", ""),
        }
    if (
        not isinstance(repository, dict)
        or not isinstance(repository.get("repo_id"), str)
        or not repository["repo_id"].strip()
    ):
        raise ValueError("Code export repository requires repo_id")
    repo_id = str(repository["repo_id"])
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    aliases: dict[str, str] = {}
    labels: dict[str, str] = {}

    def declare(label: str, key: str, properties: dict[str, Any], *, alias: str = "") -> str:
        cid = f"{label}:{repo_id}:{key}" if key else f"{label}:{repo_id}"
        if alias:
            if alias in aliases:
                raise ValueError(f"Duplicate code export endpoint: {alias}")
            aliases[alias] = cid
            labels[alias] = label
        entities.append({**properties, "entity_type": label, "canonical_id": cid})
        return cid

    repository_cid = declare("Repository", "", {
        **repository, "name": repository.get("name") or repo_id,
    })
    declare("Service", "", {
        "service_id": repo_id, "name": repository.get("name") or repo_id,
        "description": data.get("description", ""),
    }, alias=repo_id)

    def records(section: str) -> list[dict[str, Any]]:
        items = data.get(section, [])
        if not isinstance(items, list) or any(not isinstance(item, dict) for item in items):
            raise ValueError(f"Code export {section} must be an array of objects")
        return items

    for file in records("files"):
        if not isinstance(file.get("path"), str) or not file["path"].strip():
            raise ValueError("Code export file requires path")
        cid = declare("File", file["path"], {**file, "repo_id": repo_id}, alias=file["path"])
        relationships.append({"from_id": repository_cid, "to_id": cid, "type": "CONTAINS"})

    for symbol in records("symbols"):
        name = symbol.get("qualified_name")
        kind = symbol.get("symbol_kind") or symbol.get("kind")
        path = symbol.get("path")
        if (
            not isinstance(name, str) or not name.strip()
            or not isinstance(kind, str) or not kind.strip()
            or not isinstance(path, str) or path not in aliases or labels[path] != "File"
        ):
            raise ValueError(f"Code export symbol requires qualified_name, kind and declared file: {name}")
        cid = declare("CodeSymbol", name, {
            **symbol, "symbol_kind": kind, "repo_id": repo_id,
        }, alias=name)
        relationships.append({"from_id": aliases[path], "to_id": cid, "type": "DECLARES"})

    for dependency in records("dependencies"):
        name = dependency.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Code export dependency requires name")
        declare("Dependency", name, {
            **dependency, "description": json.dumps(dependency, sort_keys=True),
        }, alias=name)

    for dependency in records("runtime_dependencies"):
        key = dependency.get("id")
        if (
            not isinstance(key, str) or not key.strip()
            or not isinstance(dependency.get("name"), str) or not dependency["name"].strip()
        ):
            raise ValueError("Code export runtime dependency requires id and name")
        declare("Dependency", f"runtime:{key}", dependency, alias=key)

    for edge in records("edges"):
        source = edge.get("source") or edge.get("from_symbol") or edge.get("from_node")
        target = edge.get("target") or edge.get("to_symbol") or edge.get("to_node")
        kind = edge.get("edge_type") or edge.get("kind")
        if (
            not isinstance(source, str) or not isinstance(target, str)
            or source not in aliases or target not in aliases
        ):
            raise ValueError(f"Code export edge endpoint not declared: {source} -> {target}")
        if kind == "calls":
            relation = "CALLS"
        elif kind == "imports" and labels[target] == "Dependency":
            relation = "IMPORTS"
        elif kind in ("uses", "imports", "CONNECTS_TO", "DEPLOYED_ON", "USES_SERVICE_ACCOUNT"):
            relation = "DEPENDS_ON"
        else:
            raise ValueError(f"Unsupported code export edge type: {kind}")
        relationships.append({
            "from_id": aliases[source], "to_id": aliases[target], "type": relation,
            "properties": {
                "description": f"{kind}: {edge.get('evidence') or edge.get('metadata', {})}",
                "payload_json": json.dumps(edge, sort_keys=True),
            },
        })
    return {"entities": entities, "relationships": relationships}
