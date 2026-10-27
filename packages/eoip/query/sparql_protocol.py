"""SPARQL 1.1 Protocol Endpoint GET/POST /sparql (CRA-024.7).

Follows W3C SPARQL 1.1 Protocol specification.
Supports application/sparql-results+json, XML, CSV, and TSV format outputs.
Translates supported SPARQL algebra to LPG plan or dispatches to qualified RDF backend.
Unbounded property paths are strictly rejected with UNBOUNDED_PROPERTY_PATH error, never hanging.
"""
from __future__ import annotations

import csv
import io
import json
import re
import urllib.parse
from typing import Any, Optional
import xml.etree.ElementTree as ET

from eoip.capabilities.model import UnsupportedCapabilityError
from eoip.graph.rdf_backend import FusekiGraphStore, GraphDBGraphStore
from eoip.qlang.manifest_registry import ManifestRegistry


class _NoBackend(RuntimeError):
    pass


_TSV_BARE = {"http://www.w3.org/2001/XMLSchema#integer", "http://www.w3.org/2001/XMLSchema#decimal",
             "http://www.w3.org/2001/XMLSchema#double", "http://www.w3.org/2001/XMLSchema#boolean"}


def _csv_value(val: Optional[dict[str, Any]]) -> str:
    if not val:
        return ""
    return f"_:{val['value']}" if val.get("type") == "bnode" else val.get("value", "")


def _tsv_term(val: Optional[dict[str, Any]]) -> str:
    if not val:
        return ""
    kind, value = val.get("type"), val.get("value", "")
    if kind == "uri":
        return f"<{value}>"
    if kind == "bnode":
        return f"_:{value}"
    dt = val.get("datatype")
    if dt in _TSV_BARE and re.fullmatch(r"[+-]?[0-9.eE+-]+|true|false", value):
        return value
    esc = (value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r")
           .replace("\t", "\\t"))
    if val.get("xml:lang"):
        return f'"{esc}"@{val["xml:lang"]}'
    if dt and dt != "http://www.w3.org/2001/XMLSchema#string":
        return f'"{esc}"^^<{dt}>'
    return f'"{esc}"'


class SparqlProtocolHandler:
    """SPARQL 1.1 Protocol handler for GET and POST /sparql endpoints."""

    def __init__(
        self,
        graph_store: Optional[Any] = None,
        rdf_backend: Optional[FusekiGraphStore | GraphDBGraphStore] = None,
        manifest_registry: Optional[ManifestRegistry] = None,
        enable_updates: bool = False,
    ) -> None:
        self.graph_store = graph_store
        self.rdf_backend = rdf_backend
        self.manifest_registry = manifest_registry or ManifestRegistry.get_instance()
        self.enable_updates = enable_updates

    def check_unbounded_paths(self, query: str) -> None:
        """Reject unbounded property paths like + or * without explicit bounds."""
        # Decided on the parsed algebra (CRA-024.7): ``SELECT *``, ``COUNT(*)`` and arithmetic such as
        # ``(?a) + ?b`` are not paths. Text that does not parse is refused later as PARSE_ERROR (400).
        from eoip.query.sparql_backend import has_unbounded_path

        if has_unbounded_path(query):
            raise UnsupportedCapabilityError(
                capability_id="SPARQL",
                construct="UNBOUNDED_PROPERTY_PATH"
            )

    def handle_request(
        self,
        method: str,
        path: str = "/sparql",
        headers: Optional[dict[str, str]] = None,
        query_params: Optional[dict[str, str]] = None,
        body: Optional[str | bytes] = None,
    ) -> tuple[int, dict[str, str], str]:
        """Processes GET or POST /sparql request and returns (status_code, headers, body)."""
        headers = {k.lower(): v for k, v in (headers or {}).items()}
        query_params = query_params or {}

        # 1. Extract query string
        query_str = ""
        is_update = False

        if method.upper() == "GET":
            query_str = query_params.get("query", "")
            if not query_str and "update" in query_params:
                return 400, {"Content-Type": "text/plain"}, "SPARQL UPDATE is not permitted via HTTP GET"
        elif method.upper() == "POST":
            content_type = headers.get("content-type", "").split(";")[0].strip().lower()
            if content_type == "application/sparql-query":
                query_str = body.decode("utf-8") if isinstance(body, bytes) else (body or "")
            elif content_type == "application/sparql-update":
                query_str = body.decode("utf-8") if isinstance(body, bytes) else (body or "")
                is_update = True
            elif content_type == "application/x-www-form-urlencoded":
                decoded_body = body.decode("utf-8") if isinstance(body, bytes) else (body or "")
                parsed = urllib.parse.parse_qs(decoded_body)
                if "query" in parsed:
                    query_str = parsed["query"][0]
                elif "update" in parsed:
                    query_str = parsed["update"][0]
                    is_update = True
            else:
                return 415, {"Content-Type": "text/plain"}, f"Unsupported Media Type: {content_type}"
        else:
            return 405, {"Content-Type": "text/plain"}, "Method Not Allowed"

        if not query_str.strip():
            return 400, {"Content-Type": "text/plain"}, "Missing SPARQL query parameter"

        # 2. Check update governance
        if is_update and not self.enable_updates:
            return 403, {"Content-Type": "text/plain"}, "SPARQL Update is disabled or ungoverned (CRA-024.7)"

        # 3. Validate query against manifest and unbounded property path check
        try:
            self.manifest_registry.check_query_constructs("SPARQL", query_str)
            self.check_unbounded_paths(query_str)
        except UnsupportedCapabilityError as exc:
            return 422, {"Content-Type": "application/json"}, json.dumps(exc.to_dict())

        # 4. Determine response format
        accept = headers.get("accept", "application/sparql-results+json")

        # 5. Execute query on a real engine
        from eoip.query.sparql_backend import SparqlBackendError, SparqlCancelled, SparqlRejected

        try:
            bindings, vars_list, is_ask, ask_result = self._execute_sparql(query_str)
        except SparqlRejected as exc:
            # Malformed queries are a 400 per the SPARQL 1.1 Protocol; supported-subset refusals are 422.
            status = 400 if exc.code in ("PARSE_ERROR", "BACKEND_REJECTED_QUERY") else 422
            return status, {"Content-Type": "application/json"}, json.dumps(exc.to_dict())
        except SparqlCancelled as exc:
            return 504, {"Content-Type": "text/plain"}, f"Query cancelled: {exc}"
        except (_NoBackend, SparqlBackendError) as exc:
            return 503, {"Content-Type": "text/plain"}, f"RDF backend unavailable: {exc}"
        except Exception as exc:  # noqa: BLE001
            return 400, {"Content-Type": "text/plain"}, f"SPARQL Execution Error: {exc}"

        # 6. Format response
        if is_ask:
            resp_body, ct = self._format_ask(ask_result, accept)
        else:
            resp_body, ct = self._format_results(vars_list, bindings, accept)

        return 200, {"Content-Type": ct}, resp_body

    def _backend(self):
        from eoip.query.sparql_backend import FusekiSparqlBackend

        b = self.rdf_backend
        if b is None:
            return None
        if hasattr(b, "query"):
            return b
        # legacy FusekiGraphStore / GraphDBGraphStore descriptors: dispatch over the SPARQL protocol
        return FusekiSparqlBackend(b.endpoint_url, username=getattr(b, "username", ""),
                                   password=getattr(b, "password", ""))

    def _execute_sparql(self, query: str) -> tuple[list[dict[str, Any]], list[str], bool, bool]:
        """Execute on the configured RDF backend (Fuseki/GraphDB over the protocol, or rdflib). There is
        no fabricated fallback: without a backend the endpoint answers 503."""
        backend = self._backend()
        if backend is None:
            raise _NoBackend("no RDF backend is configured for /sparql")
        res = backend.query(query)
        if res.kind == "ASK":
            return [], [], True, bool(res.boolean)
        return res.bindings, res.vars, False, False

    def _format_results(self, vars_list: list[str], bindings: list[dict[str, Any]], accept: str) -> tuple[str, str]:
        if "json" in accept or "*/*" in accept:
            payload = {
                "head": {"vars": vars_list},
                "results": {"bindings": bindings},
            }
            return json.dumps(payload, indent=2), "application/sparql-results+json"

        if "xml" in accept:  # SPARQL 1.1 Query Results XML Format
            root = ET.Element("sparql", xmlns="http://www.w3.org/2005/sparql-results#")
            head = ET.SubElement(root, "head")
            for v in vars_list:
                ET.SubElement(head, "variable", name=v)
            res = ET.SubElement(root, "results")
            for b in bindings:
                result = ET.SubElement(res, "result")
                for var, val in b.items():
                    binding = ET.SubElement(result, "binding", name=var)
                    kind = val.get("type", "uri")
                    if kind == "uri":
                        el = ET.SubElement(binding, "uri")
                    elif kind == "bnode":
                        el = ET.SubElement(binding, "bnode")
                    else:
                        el = ET.SubElement(binding, "literal")
                        if val.get("xml:lang"):
                            el.set("{http://www.w3.org/XML/1998/namespace}lang", val["xml:lang"])
                        elif val.get("datatype"):
                            el.set("datatype", val["datatype"])
                    el.text = val.get("value", "")
            return ET.tostring(root, encoding="unicode"), "application/sparql-results+xml"

        if "csv" in accept:  # SPARQL 1.1 Query Results CSV: plain values, RFC 4180 quoting, _: bnodes
            buf = io.StringIO()
            w = csv.writer(buf, lineterminator="\r\n")
            w.writerow(vars_list)
            for b in bindings:
                w.writerow([_csv_value(b.get(v)) for v in vars_list])
            return buf.getvalue(), "text/csv"

        if "tab-separated-values" in accept or "tsv" in accept:  # TSV: terms in SPARQL/Turtle syntax
            header = "\t".join(f"?{v}" for v in vars_list)
            rows = ["\t".join(_tsv_term(b.get(v)) for v in vars_list) for b in bindings]
            return "\n".join([header] + rows) + "\n", "text/tab-separated-values"

        # Default fallback JSON
        payload = {
            "head": {"vars": vars_list},
            "results": {"bindings": bindings},
        }
        return json.dumps(payload, indent=2), "application/sparql-results+json"

    def _format_ask(self, result: bool, accept: str) -> tuple[str, str]:
        if "xml" in accept:
            root = ET.Element("sparql", xmlns="http://www.w3.org/2005/sparql-results#")
            b = ET.SubElement(root, "boolean")
            b.text = "true" if result else "false"
            return ET.tostring(root, encoding="utf-8").decode("utf-8"), "application/sparql-results+xml"

        payload = {"head": {}, "boolean": result}
        return json.dumps(payload, indent=2), "application/sparql-results+json"
