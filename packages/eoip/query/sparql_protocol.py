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


_FORMATS = {
    "application/sparql-results+json": "json", "application/json": "json",
    "application/sparql-results+xml": "xml", "application/xml": "xml", "text/xml": "xml",
    "text/csv": "csv", "text/tab-separated-values": "tsv",
}


def negotiate(accept: str, *, ask: bool = False) -> Optional[str]:
    """HTTP content negotiation over the SPARQL results formats (q-values honoured; ties keep the
    client's order). No Accept header, or ``*/*``, gives JSON. ``None`` means 406. CSV/TSV are not
    defined for ASK results."""
    if not accept.strip():
        return "json"
    offered = [f for f in ("json", "xml", "csv", "tsv") if not (ask and f in ("csv", "tsv"))]
    best: tuple[float, int, str] | None = None
    for i, part in enumerate(accept.split(",")):
        bits = [b.strip() for b in part.split(";")]
        mime, q = bits[0].lower(), 1.0
        for b in bits[1:]:
            if b.startswith("q="):
                try:
                    q = float(b[2:])
                except ValueError:
                    q = 0.0
        if q <= 0:
            continue
        if mime in ("*/*", "application/*"):
            cands = ["json"]
        elif mime == "text/*":
            cands = [f for f in ("csv", "tsv", "xml") if f in offered][:1]
        else:
            cands = [_FORMATS[mime]] if _FORMATS.get(mime) in offered else []
        for c in cands:
            if best is None or q > best[0]:
                best = (q, i, c)
    return best[2] if best else None


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
        query_params: Optional[dict[str, Any]] = None,
        body: Optional[str | bytes] = None,
    ) -> tuple[int, dict[str, str], str]:
        """One SPARQL 1.1 Protocol query operation; returns (status_code, headers, body).

        ``query_params`` maps a URL parameter to a value or a list of values (repeated parameters matter:
        two ``query`` values are a 400). The endpoint is read-only: an update by GET or POST is a 400.
        """
        headers = {k.lower(): v for k, v in (headers or {}).items()}
        params = {k: (list(v) if isinstance(v, (list, tuple)) else [v]) for k, v in (query_params or {}).items()}
        text = {"Content-Type": "text/plain; charset=utf-8"}
        verb = method.upper()
        if verb not in ("GET", "POST"):
            return 405, {**text, "Allow": "GET, POST"}, "Method Not Allowed: the SPARQL query operation is GET or POST"

        if verb == "GET":
            fields = params
        else:
            content_type = headers.get("content-type", "").split(";")[0].strip().lower()
            try:
                raw = body.decode("utf-8") if isinstance(body, bytes) else (body or "")
            except UnicodeDecodeError:
                return 400, text, "Request body is not UTF-8"
            if content_type == "application/x-www-form-urlencoded":
                try:
                    fields = urllib.parse.parse_qs(raw, keep_blank_values=True, strict_parsing=False,
                                                   encoding="utf-8", errors="strict")
                except UnicodeDecodeError:
                    return 400, text, "Form fields are not UTF-8"
            elif content_type == "application/sparql-query":
                fields = {**params, "query": [raw]}
            elif content_type == "application/sparql-update":
                fields = {**params, "update": [raw]}
            else:
                return 415, text, (f"Unsupported Media Type: {content_type or '(none)'}; use "
                                   "application/x-www-form-urlencoded or application/sparql-query")
        if fields.get("update") or fields.get("using-graph-uri") or fields.get("using-named-graph-uri"):
            return 400, text, "This SPARQL endpoint is read-only: update operations are not accepted (CRA-024.7)"
        queries = fields.get("query") or []
        if len(queries) > 1:
            return 400, text, "Exactly one 'query' parameter is allowed"
        query_str = queries[0] if queries else ""
        if not query_str.strip():
            return 400, text, "Missing SPARQL query parameter"
        dataset = {k: fields[k] for k in ("default-graph-uri", "named-graph-uri") if fields.get(k)}

        # Validate query against manifest and unbounded property path check
        try:
            self.manifest_registry.check_query_constructs("SPARQL", query_str)
            self.check_unbounded_paths(query_str)
        except UnsupportedCapabilityError as exc:
            return 422, {"Content-Type": "application/json"}, json.dumps(exc.to_dict())

        from eoip.query.sparql_backend import SparqlBackendError, SparqlCancelled, SparqlRejected, validate_query

        try:
            kind = validate_query(query_str)
        except SparqlRejected as exc:
            status = 400 if exc.code in ("PARSE_ERROR", "BACKEND_REJECTED_QUERY") else 422
            if exc.code == "UPDATE_NOT_PERMITTED":
                status = 400
            return status, {"Content-Type": "application/json"}, json.dumps(exc.to_dict())
        fmt = negotiate(headers.get("accept", ""), ask=kind == "ASK")
        if fmt is None:
            return 406, text, ("Not Acceptable: results are available as application/sparql-results+json, "
                               "application/sparql-results+xml" + ("" if kind == "ASK" else
                                                                   ", text/csv, text/tab-separated-values"))

        try:
            bindings, vars_list, is_ask, ask_result = self._execute_sparql(query_str, dataset)
        except SparqlRejected as exc:
            # Malformed queries are a 400 per the SPARQL 1.1 Protocol; supported-subset refusals are 422.
            status = 400 if exc.code in ("PARSE_ERROR", "BACKEND_REJECTED_QUERY", "DATASET_NOT_SUPPORTED") else 422
            return status, {"Content-Type": "application/json"}, json.dumps(exc.to_dict())
        except SparqlCancelled as exc:
            return 504, text, f"Query cancelled: {exc}"
        except (_NoBackend, SparqlBackendError) as exc:
            return 503, text, f"RDF backend unavailable: {exc}"
        except Exception as exc:  # noqa: BLE001
            return 400, text, f"SPARQL Execution Error: {exc}"

        if is_ask:
            resp_body, ct = self._format_ask(ask_result, fmt)
        else:
            resp_body, ct = self._format_results(vars_list, bindings, fmt)
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

    def _execute_sparql(self, query: str, dataset: Optional[dict[str, list[str]]] = None
                        ) -> tuple[list[dict[str, Any]], list[str], bool, bool]:
        """Execute on the configured RDF backend (Fuseki/GraphDB over the protocol, or rdflib). There is
        no fabricated fallback: without a backend the endpoint answers 503."""
        backend = self._backend()
        if backend is None:
            raise _NoBackend("no RDF backend is configured for /sparql")
        res = backend.query(query, dataset=dataset) if dataset else backend.query(query)
        if res.kind == "ASK":
            return [], [], True, bool(res.boolean)
        return res.bindings, res.vars, False, False

    def _format_results(self, vars_list: list[str], bindings: list[dict[str, Any]], accept: str) -> tuple[str, str]:
        if accept == "json":
            payload = {
                "head": {"vars": vars_list},
                "results": {"bindings": bindings},
            }
            return json.dumps(payload, indent=2), "application/sparql-results+json"

        if accept == "xml":  # SPARQL 1.1 Query Results XML Format
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

        if accept == "csv":  # SPARQL 1.1 Query Results CSV: plain values, RFC 4180 quoting, _: bnodes
            buf = io.StringIO()
            w = csv.writer(buf, lineterminator="\r\n")
            w.writerow(vars_list)
            for b in bindings:
                w.writerow([_csv_value(b.get(v)) for v in vars_list])
            return buf.getvalue(), "text/csv"

        if accept == "tsv":  # TSV: terms in SPARQL/Turtle syntax
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
        if accept == "xml":
            root = ET.Element("sparql", xmlns="http://www.w3.org/2005/sparql-results#")
            b = ET.SubElement(root, "boolean")
            b.text = "true" if result else "false"
            return ET.tostring(root, encoding="utf-8").decode("utf-8"), "application/sparql-results+xml"

        payload = {"head": {}, "boolean": result}
        return json.dumps(payload, indent=2), "application/sparql-results+json"
