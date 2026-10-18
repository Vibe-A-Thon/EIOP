"""Text, structured data, HTML, XML and RTF parsers (no external requests)."""

from __future__ import annotations

import csv
import io
import json
import math
from html.parser import HTMLParser

from eoip.fileparse.common import Extraction, decode_text, dependency
from eoip.fileparse.contracts import ParseError


class VisibleHTML(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts: list[str] = []
        self.links: list[dict[str, str]] = []
        self.in_title = False
        self.title: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in {"script", "style", "template"}:
            self.hidden += 1
        if tag == "title":
            self.in_title = True
        if not self.hidden:
            if tag in {"p", "div", "br", "li", "tr", "h1", "h2", "h3"}:
                self.parts.append("\n")
            if tag == "a":
                href = dict(attrs).get("href")
                if href:
                    self.links.append({"href": href})

    def handle_endtag(self, tag):
        if tag in {"script", "style", "template"} and self.hidden:
            self.hidden -= 1
        if tag == "title":
            self.in_title = False
        if not self.hidden and tag in {"p", "div", "li", "tr", "h1", "h2", "h3"}:
            self.parts.append("\n")

    def handle_data(self, data):
        if not self.hidden:
            self.parts.append(data)
            if self.in_title:
                self.title.append(data)


def parse_text(content: bytes, suffix: str, out: Extraction) -> None:
    text = decode_text(content, out.options.encoding)
    if len(text) > out.options.max_text_chars:
        raise ParseError("text_limit", "Input text exceeds max_text_chars")
    if suffix == ".json":
        def reject_constant(value):
            raise ValueError(f"Non-JSON constant: {value}")

        def finite_float(value):
            number = float(value)
            if not math.isfinite(number):
                raise ValueError("JSON number exceeds finite floating-point range")
            return number

        out.document.data = json.loads(text, parse_constant=reject_constant, parse_float=finite_float)
        out.section("json", json.dumps(out.document.data, ensure_ascii=False, indent=2))
    elif suffix == ".csv":
        try:
            reader = csv.reader(io.StringIO(text, newline=""), strict=True)
            columns = next(reader, [])
            rows = []
            for row in reader:
                if len(rows) >= out.options.max_rows:
                    raise ParseError("row_limit", "CSV exceeds max_rows")
                if len(row) != len(columns):
                    raise ParseError("invalid_csv", "CSV row width differs from the header")
                rows.append(row)
        except csv.Error as exc:
            raise ParseError("invalid_csv", "CSV is malformed or exceeds the local CSV field-size limit") from exc
        out.table("csv", columns, rows)
    elif suffix in {".html", ".htm", ".xhtml"}:
        parser = VisibleHTML()
        parser.feed(text)
        parser.close()
        out.document.title = "".join(parser.title).strip() or out.document.title
        out.document.metadata["links"] = parser.links
        out.section("html", "".join(parser.parts).strip())
    elif suffix == ".xml":
        etree = dependency("defusedxml.ElementTree")
        errors = dependency("defusedxml.common")
        try:
            root = etree.fromstring(text)
        except (etree.ParseError, errors.DefusedXmlException) as exc:
            raise ParseError("invalid_xml", "XML is malformed or contains prohibited entities") from exc
        out.document.metadata["root_tag"] = root.tag
        for index, element in enumerate(root.iter()):
            if element.text and element.text.strip():
                out.section("xml", element.text.strip(), element=element.tag, element_index=index)
            if element.tail and element.tail.strip():
                out.section("xml", element.tail.strip(), element=element.tag, element_index=index, tail=True)
    elif suffix == ".tsv":
        try:
            reader = csv.reader(io.StringIO(text, newline=""), delimiter="\t", strict=True)
            columns = next(reader, [])
            rows = []
            for row in reader:
                if len(rows) >= out.options.max_rows:
                    raise ParseError("row_limit", "TSV exceeds max_rows")
                if len(row) != len(columns):
                    raise ParseError("invalid_csv", "TSV row width differs from the header")
                rows.append(row)
        except csv.Error as exc:
            raise ParseError("invalid_csv", "TSV is malformed or exceeds the local CSV field-size limit") from exc
        out.table("tsv", columns, rows)
    elif suffix in {".yaml", ".yml"}:
        yaml = dependency("yaml")
        try:
            data = yaml.safe_load(text)
        except Exception as exc:
            raise ParseError("invalid_format", f"YAML is malformed: {exc}") from exc
        out.document.data = data
        out.section("yaml", json.dumps(data, default=str, ensure_ascii=False, indent=2))
    elif suffix == ".jsonld":
        try:
            data = json.loads(text)
        except Exception as exc:
            raise ParseError("invalid_format", f"JSON-LD is malformed: {exc}") from exc
        out.document.data = data
        out.document.metadata["jsonld_context"] = data.get("@context") if isinstance(data, dict) else None
        out.section("jsonld", json.dumps(data, default=str, ensure_ascii=False, indent=2))
    elif suffix in {".md", ".markdown"}:
        lines = text.splitlines()
        out.section("markdown", text, line_start=1, line_end=len(lines))
    elif suffix in {".adoc", ".asciidoc"}:
        lines = text.splitlines()
        out.section("asciidoc", text, line_start=1, line_end=len(lines))
    elif suffix == ".rtf":
        if not text.lstrip().startswith("{\\rtf"):
            raise ParseError("invalid_format", "RTF header is missing")
        striprtf = dependency("striprtf.striprtf")
        out.section("rtf", striprtf.rtf_to_text(text, errors="strict"))
    else:
        out.section("text", text, line_start=1, line_end=len(text.splitlines()))
