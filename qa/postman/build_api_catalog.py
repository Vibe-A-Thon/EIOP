"""Generate non-executable Postman request blueprints for every API operation."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "qa" / "postman" / "EOIP-API-operation-catalog.postman_collection.json"
METHODS = {"get", "post", "put", "patch", "delete", "options", "head", "trace"}


def collection(document: dict) -> dict:
    groups: dict[str, list[dict]] = {}
    for path, operations in sorted(document["paths"].items()):
        for method, operation in sorted(operations.items()):
            if method not in METHODS:
                continue
            tag = (operation.get("tags") or ["Untagged"])[0]
            variables = re.findall(r"\{([^{}]+)\}", path)
            url_path = re.sub(r"\{([^{}]+)\}", lambda match: "{{qa_" + match.group(1) + "}}", path)
            description = (
                "REQUEST BLUEPRINT ONLY. This collection unconditionally skips every request. "
                "Copy this item into a reviewed, fixture-backed collection and add response, "
                "authorization, side-effect and cleanup assertions before executing.\n\n"
                f"Operation ID: {operation.get('operationId', 'unspecified')}\n"
                f"Summary: {operation.get('summary', 'unspecified')}\n"
                f"Path variables: {', '.join(variables) or 'none'}\n"
                f"Request body declared: {'yes' if 'requestBody' in operation else 'no'}\n"
                f"Response statuses: {', '.join(sorted(operation.get('responses', {})))}"
            )
            groups.setdefault(tag, []).append({
                "name": f"{method.upper()} {path}",
                "request": {
                    "method": method.upper(),
                    "header": [{"key": "Accept", "value": "application/json"}],
                    "url": {"raw": "{{baseUrl}}" + url_path, "host": ["{{baseUrl}}"], "path": url_path.lstrip("/").split("/")},
                    "description": description,
                },
                "response": [],
            })
    return {
        "info": {
            "name": "EOIP complete API operation catalog - NON-EXECUTABLE",
            "description": "Design inventory only. Every request is skipped. This is not a functional test suite or proof of coverage.",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
        },
        "event": [{
            "listen": "prerequest",
            "script": {"type": "text/javascript", "exec": [
                "// Deliberate hard stop: operations may mutate data or require explicit fixtures.",
                "pm.execution.skipRequest();",
            ]},
        }],
        "variable": [{"key": "baseUrl", "value": "http://127.0.0.1:8000"}],
        "item": [{"name": tag, "item": items} for tag, items in sorted(groups.items())],
    }


def main(argv: list[str] | None = None) -> int:
    from qa.bench import offline_document

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if the reviewed catalog differs from the current API")
    args = parser.parse_args(argv)
    generated = collection(offline_document())
    if args.check:
        current = json.loads(OUTPUT.read_text(encoding="utf-8")) if OUTPUT.exists() else None
        if current != generated:
            print("API request catalog drift; regenerate and review the diff")
            return 1
        print("API request catalog matches current OpenAPI")
        return 0
    OUTPUT.write_text(json.dumps(generated, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUTPUT.relative_to(ROOT)} with {sum(len(group['item']) for group in generated['item'])} disabled request blueprints")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
