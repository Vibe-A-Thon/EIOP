"""HTTP SPARQL 1.1 Protocol endpoint: ``GET|POST /api/v1/sparql`` (CRA-024.7; decisions D-CRA-024-02/-04).

* Query operation only (read-only): ``GET ?query=``, ``POST application/x-www-form-urlencoded`` and
  ``POST application/sparql-query``; protocol dataset parameters ``default-graph-uri`` /
  ``named-graph-uri``; results negotiated as SPARQL JSON / XML / CSV / TSV (406 otherwise).
  Updates by GET or POST are a 400; other methods are a 405.
* Authentication: the platform middleware already refuses anonymous requests (401) - login session or
  API token. Authorization: read tier of ``apps.api.route_policy`` (viewer and above; deny by default,
  unknown roles get nothing), checked here for GET as well as POST.
* Tenancy: the RDF dataset is chosen from the verified principal's tenant, never from the request.
  ``EOIP_SPARQL_BACKEND`` (``fuseki`` | ``graphdb``) and ``EOIP_SPARQL_ENDPOINT`` - a URL template with
  ``{tenant}`` (``http://fuseki:3030/{tenant}``, ``http://graphdb:7200/repositories/{tenant}``) - select
  the engine; ``EOIP_SPARQL_USER`` / ``EOIP_SPARQL_PASSWORD`` authenticate to it. Not configured: 503.
"""

import os
import re
import urllib.parse
from collections.abc import Callable
from typing import Any

from eoip.query.sparql_protocol import SparqlProtocolHandler

PATH = "/api/v1/sparql"
_TENANT = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")


def backend_from_env(tenant: str, env: dict[str, str] | None = None):
    """The tenant's RDF backend from configuration, or ``None`` when no SPARQL engine is configured."""
    from eoip.query.sparql_backend import FusekiSparqlBackend, GraphDBSparqlBackend

    env = dict(os.environ if env is None else env)
    kind, template = env.get("EOIP_SPARQL_BACKEND", ""), env.get("EOIP_SPARQL_ENDPOINT", "")
    if not kind or not template:
        return None
    if "{tenant}" not in template:
        raise ValueError("EOIP_SPARQL_ENDPOINT must contain {tenant}: one dataset per tenant")
    cls = {"fuseki": FusekiSparqlBackend, "graphdb": GraphDBSparqlBackend}[kind]
    return cls(template.replace("{tenant}", tenant), username=env.get("EOIP_SPARQL_USER", ""),
               password=env.get("EOIP_SPARQL_PASSWORD", ""))


def _configured_backend(tenant: str):
    return backend_from_env(tenant)  # looked up at call time (tests substitute the module attribute)


def parse_query_string(raw: bytes | str) -> dict[str, list[str]]:
    """URL parameters with repeated keys kept and strict UTF-8 (a non-UTF-8 query is a 400)."""
    text = raw.decode("ascii") if isinstance(raw, bytes) else raw
    return urllib.parse.parse_qs(text, keep_blank_values=True, encoding="utf-8", errors="strict")


def build_sparql_router(authorize: Callable[[str, str, Any], bool],
                        backend_for_tenant: Callable[[str], Any] | None = None):
    """``authorize(method, path, roles)`` is the platform role policy (``route_policy.allowed``)."""
    from fastapi import APIRouter, Request
    from fastapi.responses import Response

    router = APIRouter(tags=["sparql"])
    results_schema = {"type": "object", "required": ["head"], "properties": {
        "head": {"type": "object", "properties": {"vars": {"type": "array", "items": {"type": "string"}}}},
        "results": {"type": "object", "properties": {"bindings": {"type": "array", "items": {"type": "object"}}}},
        "boolean": {"type": "boolean"}}}
    text = {"schema": {"type": "string"}}
    ok = {"description": "SPARQL results, negotiated by Accept",
          "content": {"application/sparql-results+json": {"schema": results_schema},
                      "application/sparql-results+xml": text, "text/csv": text, "text/tab-separated-values": text}}
    errors = {code: {"description": desc, "content": {"text/plain": text}} for code, desc in (
        (400, "Malformed request, update operation (read-only endpoint) or query syntax error"),
        (401, "No authenticated principal"), (403, "Role lacks read access"),
        (406, "No acceptable results format"), (503, "SPARQL engine unavailable or not configured"),
        (504, "Query cancelled at the deadline"))}
    errors[422] = {"description": "Query outside the supported subset", "content": {"application/json": {
        "schema": {"type": "object", "properties": {"code": {"type": "string"}, "message": {"type": "string"}}}}}}

    async def _handle(request: Request) -> Response:
        principal = getattr(request.state, "principal", None)
        if principal is None:  # the middleware already answers 401; never serve anonymously
            return Response("Authentication required", status_code=401, media_type="text/plain")
        # Query is a read for any method: evaluate the read tier (POST classification) for GET too.
        if not authorize("POST", PATH, getattr(principal, "roles", ())):
            return Response("Role not permitted: read access required", status_code=403, media_type="text/plain")
        tenant = getattr(principal, "tenant_id", None) or "default"
        if not _TENANT.match(tenant):
            return Response("Tenant identifier cannot name an RDF dataset", status_code=403, media_type="text/plain")
        try:
            params = parse_query_string(request.scope.get("query_string", b""))
        except (UnicodeDecodeError, UnicodeEncodeError):
            return Response("Query string is not UTF-8", status_code=400, media_type="text/plain")
        try:
            backend = (backend_for_tenant or _configured_backend)(tenant)
        except (KeyError, ValueError) as exc:
            return Response(f"SPARQL backend misconfigured: {exc}", status_code=503, media_type="text/plain")
        handler = SparqlProtocolHandler(rdf_backend=backend)
        body = await request.body() if request.method == "POST" else None
        status, headers, payload = handler.handle_protocol_request(request.method, PATH, dict(request.headers), params, body)
        media = headers.pop("Content-Type", "text/plain")
        return Response(payload, status_code=status, media_type=media, headers=headers)

    @router.get(PATH, summary="SPARQL 1.1 Protocol query (GET)", response_class=Response,
                responses={200: ok, **errors})
    async def sparql_get(request: Request) -> Response:
        return await _handle(request)

    @router.post(PATH, summary="SPARQL 1.1 Protocol query (POST form or application/sparql-query)",
                 response_class=Response,
                 responses={200: ok, **errors, 415: {"description": "Unsupported request media type",
                                                     "content": {"text/plain": text}}})
    async def sparql_post(request: Request) -> Response:
        return await _handle(request)

    @router.api_route(PATH, methods=["PUT", "PATCH", "DELETE"], include_in_schema=False)
    async def sparql_other(request: Request) -> Response:
        return Response("Method Not Allowed", status_code=405, media_type="text/plain",
                        headers={"Allow": "GET, POST"})

    return router
