# API Application

## Entry Points

- `main.py:create_app`: supported runtime factory. Constructs graph storage, queue, registry, validation, audit, agents, identity and HTTP boundary handling.
- `app.py:create_app(store, ...)`: lower-level injected-store query application. A caller must supply a store; it is useful for isolated tests but is not a substitute for the runtime security boundary.
- `extended.py`: additional domain route/state composition. Trace its initialization before assuming a domain is durable or tenant-isolated.
- `asg.py`: access/security registry composition used by the main factory.

## Local Run

Install `.[dev]` and use the complete environment/command in [Getting Started](../../docs/getting-started.md). The runtime entry is:

```powershell
python -m uvicorn apps.api.main:create_app --factory --host 127.0.0.1 --port 8000 --reload
```

`EOIP_API_TOKEN`, `EOIP_GRAPH_BACKEND` and `EOIP_DATA_DIR` must be selected deliberately. Run from repository root because several loaders use relative config paths. Memory graph mode is disposable; separate worker/API processes do not share a memory graph.

## HTTP and Security Contract

Inspect deployed `/openapi.json` for exact HTTP contracts. `/health/live`, `/health/ready`, `/metrics`, schema/docs paths and permitted preflight/webhook paths have special boundary handling in `main.py`; do not describe every route as requiring the same bearer flow. Restrict exposure of operational/schema endpoints at deployment level as needed.

Protected requests resolve identity from authenticated credentials. High-risk mutation families have administrative checks and audit preflight; route-specific domain policy still matters. The body boundary caps buffered requests at 4,000,000 bytes. Error bodies and audit/correlation headers are not uniform across every early return, so clients must tolerate missing optional headers.

Source webhook authentication is its own protocol boundary. Exemption from the generic bearer check is not permission to skip source signature/secret validation. MCP/client-supplied actor fields must not override trusted identity.

The new optional REVA mount is `/api/reva/v1`, controlled by `REVA_ENABLED` (default false). Its health path is also exempt from the generic bearer check and does not validate kernel readiness. The inspected mount suppresses import/initialization errors and does not initialize the warrant kernel. See [REVA integration limits](../../reva/README.md) before enabling or exposing these routes; tenant/principal binding needs separate verification.

## Changing the API

Trace route -> contract -> authorization -> domain -> storage/job -> response. Keep graph adapters and business logic out of new route-local shortcuts. Add positive and denied cases, malformed input checks, compatibility tests and restart/effect checks where relevant. Update [API reference](../../docs/api-reference.md), [schemas](../../schemas/README.md), clients and owning requirements. See [migration procedure](../../docs/migration-refactoring-guide.md).

Useful checks include `tests/security/test_token_validation_contract.py`, `tests/security/test_http_and_realtime_contract.py`, `tests/security/test_cors_contract.py` and the affected unit/integration tests. These are test starting points, not production qualification claims.
