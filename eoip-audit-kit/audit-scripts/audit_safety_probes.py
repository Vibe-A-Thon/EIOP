"""Local-only probes. No external network, live credentials or customer data."""

import json
from pathlib import Path
from unittest.mock import patch


def main():
    observations = []
    source = Path("packages/eoip/ragx/architectures.py")
    try:
        compile(source.read_bytes(), str(source), "exec")
        observations.append({"probe": "ragx-import-syntax", "result": "valid"})
    except SyntaxError as exc:
        observations.append({"probe": "ragx-import-syntax", "result": "invalid", "error": str(exc)})
    from eoip.models.provider import LocalModelProvider
    captured = []

    class SyntheticClient:
        def __init__(self, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def post(self, url, json):
            captured.append({"host_is_external": url.startswith("https://external.invalid/"),
                             "synthetic_content_forwarded": json["messages"][1]["content"] == "SYNTHETIC_AUDIT_SENTINEL"})

            class Response:
                def raise_for_status(self):
                    pass

                def json(self):
                    return {"message": {"content": "synthetic"}}

            return Response()

    with patch("eoip.models.provider.httpx.Client", SyntheticClient):
        LocalModelProvider(model="synthetic-audit", url="https://external.invalid").generate("synthetic", "SYNTHETIC_AUDIT_SENTINEL")
    observations.append({"probe": "configured-model-host-boundary", "captured": captured,
                         "limitation": "Mock transport proves local provider does not reject remote configuration, not that any network egress occurred."})
    print(json.dumps({"observations": observations, "network_calls": 0}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
