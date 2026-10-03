"""Source-provided page metadata, without cross-source identity inference."""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from eoip.connectors.rest import parse_utc

MAX_PAGE_VERSIONS = 1000


def _object(value: Any, field: str) -> dict:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise TypeError(f"Confluence {field} must be an object")
    return value


def _actor(value: Any, field: str) -> dict[str, str] | None:
    actor = _object(value, field)
    result = {}
    for source, target in (
        ("type", "type"), ("userKey", "user_key"),
        ("username", "username"), ("displayName", "display_name"),
    ):
        text = actor.get(source)
        if text is not None:
            if not isinstance(text, str):
                raise ValueError(f"Confluence {field}.{source} must be text")
            result[target] = text
    return result or None


def _timestamp(value: Any, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Confluence {field} must be a timestamp")
    try:
        parsed = parse_utc(value)
    except ValueError as exc:
        raise ValueError(f"Confluence {field} must be a timestamp") from exc
    if parsed is None:
        raise ValueError(f"Confluence {field} must be a timestamp")
    return parsed.isoformat().replace("+00:00", "Z")


def extract_page_metadata(record: dict) -> dict[str, Any]:
    metadata = _object(record.get("metadata"), "metadata")
    labels = []
    if metadata.get("labels") is not None:
        collection = _object(metadata["labels"], "metadata.labels")
        links = _object(collection.get("_links"), "metadata.labels._links")
        next_link = links.get("next")
        if next_link is not None and not isinstance(next_link, str):
            raise ValueError("Confluence label continuation must be text")
        if next_link:
            raise ValueError("incomplete Confluence label collection")
        rows = collection.get("results")
        if not isinstance(rows, list):
            raise ValueError("Confluence label results must be a list")
        unique = set()
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get("name"), str) or not row["name"].strip():
                raise ValueError("Confluence label name must be nonempty text")
            prefix = row.get("prefix", "")
            if not isinstance(prefix, str):
                raise TypeError("Confluence label prefix must be text")
            unique.add((prefix, row["name"]))
        labels = [{"name": name, "prefix": prefix} for prefix, name in sorted(unique)]
    history = _object(record.get("history"), "history")
    version = _object(record.get("version"), "version")
    return {
        "schema_version": "1.0", "labels": labels,
        "author": _actor(history.get("createdBy"), "history.createdBy"),
        "editor": _actor(version.get("by"), "version.by"),
        "created_at": _timestamp(history.get("createdDate"), "history.createdDate"),
        "modified_at": _timestamp(version.get("when"), "version.when"),
    }


def extract_page_history(record: dict, base_url: str) -> dict[str, Any]:
    collection = record.get("version_history")
    complete = False
    if collection is not None:
        collection = _object(collection, "version_history")
        complete = collection.get("complete")
        if not isinstance(complete, bool):
            raise TypeError("Confluence history completeness must be boolean")
        versions = collection.get("results")
        if not isinstance(versions, list):
            raise TypeError("Confluence history results must be a list")
    else:
        history = _object(record.get("history"), "history")
        versions = [record.get("version"), *(
            history.get(key) for key in ("previousVersion", "nextVersion", "lastUpdated")
        )]
        versions = [item for item in versions if item is not None]
    if len(versions) > MAX_PAGE_VERSIONS:
        raise ValueError("Confluence page history exceeds 1000 versions")
    revisions = {}
    for item in versions:
        item = _object(item, "history version")
        number = item.get("number")
        if not item and not complete:
            continue
        if isinstance(number, bool) or not isinstance(number, int) or number < 1:
            raise ValueError("Confluence history version number must be a positive integer")
        message = item.get("message", "")
        minor_edit = item.get("minorEdit", False)
        if not isinstance(message, str) or not isinstance(minor_edit, bool):
            raise TypeError("Confluence history message/minorEdit have invalid types")
        revision = {
            "number": number, "modified_at": _timestamp(item.get("when"), "history version.when"),
            "editor": _actor(item.get("by"), "history version.by"),
            "message": message, "minor_edit": minor_edit,
            "source_ref": (
                f"{base_url.rstrip('/')}/rest/api/content/{quote(str(record['id']), safe='')}"
                f"?status=historical&version={number}"
            ),
        }
        if number in revisions and (complete or revisions[number] != revision):
            raise ValueError("Confluence history contains duplicate/conflicting versions")
        revisions[number] = revision
    if complete:
        page_version = _object(record.get("version"), "version")
        current = page_version.get("number")
        if (
            isinstance(current, bool) or not isinstance(current, int)
            or not 1 <= current <= MAX_PAGE_VERSIONS
            or sorted(revisions) != list(range(1, current + 1))
        ):
            raise ValueError("incomplete Confluence page history")
        if next(item for item in versions if item["number"] == current) != page_version:
            raise ValueError("Confluence history current version disagrees with page metadata")
    return {
        "schema_version": "1.0", "complete": complete,
        "revisions": [revisions[number] for number in sorted(revisions, reverse=True)],
    }
