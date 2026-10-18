"""Deterministic, non-fetching extraction of Confluence storage XHTML fragments."""

from __future__ import annotations

import re
from html.entities import name2codepoint
from typing import Any
from urllib.parse import urljoin, urlsplit
from xml.etree import ElementTree as ET

PARSER_VERSION = "confluence-storage/1.1"
_AC = "{http://atlassian.com/content}"
_RI = "{http://atlassian.com/resource/identifier}"
_HEADINGS = {f"h{level}": level for level in range(1, 7)}
_MAX_BODY_CHARS = 2_000_000
_MAX_ELEMENTS = 50_000


def _text(element: ET.Element) -> str:
    return " ".join("".join(element.itertext()).split())


def _entities(fragment: str) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match[1]
        point = name2codepoint.get(name)
        return f"&#{point};" if point is not None else match[0]

    # Code macro CDATA is literal source, not XHTML entity text.
    pieces = re.split(r"(<!\[CDATA\[.*?\]\]>)", fragment, flags=re.DOTALL)
    return "".join(
        piece if piece.startswith("<![CDATA[") else re.sub(r"&([A-Za-z][\w]*);", replace, piece)
        for piece in pieces
    )


def _url_link(href: str, text: str, page_url: str) -> dict[str, str] | None:
    href = href.strip()
    if href.startswith("urn:eoip:") and not any(character.isspace() for character in href):
        return {"kind": "entity", "target": href, "text": text}
    target = urljoin(page_url, href)
    parsed = urlsplit(target)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return None
    kind = "anchor" if href.startswith("#") else (
        "internal" if parsed.netloc == urlsplit(page_url).netloc else "external"
    )
    return {"kind": kind, "target": target, "text": text}


def _table_rows(table: ET.Element) -> list[list[dict[str, Any]]]:
    rows = []
    for child in table:
        if child.tag in {"thead", "tbody", "tfoot"}:
            rows.extend(_table_rows(child))
        elif child.tag == "tr":
            cells = []
            for cell in child:
                if cell.tag not in {"th", "td"}:
                    continue
                try:
                    rowspan = int(cell.get("rowspan", "1"))
                    colspan = int(cell.get("colspan", "1"))
                except ValueError as exc:
                    raise ValueError("invalid Confluence table span") from exc
                if not 1 <= rowspan <= 1000 or not 1 <= colspan <= 1000:
                    raise ValueError("Confluence table span must be between 1 and 1000")
                cells.append({
                    "text": _text(cell), "header": cell.tag == "th",
                    "rowspan": rowspan, "colspan": colspan,
                })
            rows.append(cells)
    return rows


def extract_storage_body(body: str, page_url: str) -> dict[str, Any]:
    if len(body) > _MAX_BODY_CHARS:
        raise ValueError("Confluence storage body exceeds 2000000 characters")
    markup = re.sub(r"<!\[CDATA\[.*?\]\]>", "", body, flags=re.DOTALL)
    if re.search(r"<!\s*(DOCTYPE|ENTITY)\b", markup, flags=re.IGNORECASE):
        raise ValueError("Confluence storage declarations are not supported")
    try:
        root = ET.fromstring(
            '<body xmlns:ac="http://atlassian.com/content" '
            'xmlns:ri="http://atlassian.com/resource/identifier">'
            + _entities(body) + "</body>"
        )
    except ET.ParseError as exc:
        raise ValueError("invalid Confluence storage XHTML") from exc
    if sum(1 for _ in root.iter()) > _MAX_ELEMENTS:
        raise ValueError("Confluence storage body exceeds 50000 elements")
    pending = [(root, 0)]
    while pending:
        element, depth = pending.pop()
        if depth > 128:
            raise ValueError("Confluence storage body exceeds 128 nesting levels")
        if element.tag.startswith("{http://www.w3.org/1999/xhtml}"):
            element.tag = element.tag.split("}", 1)[1]
        pending.extend((child, depth + 1) for child in element)
    for parent in root.iter():
        for child in list(parent):
            if child.tag in {"script", "style", "noscript"}:
                parent.remove(child)

    result: dict[str, Any] = {
        "schema_version": "1.0", "parser_version": PARSER_VERSION,
        "headings": [], "anchors": [], "links": [], "code_snippets": [], "tables": [],
        "diagnostics": {"unsupported_macros": []},
    }
    pre_children = {id(child) for pre in root.iter("pre") for child in pre.iter() if child is not pre}
    for element in root.iter():
        tag = element.tag
        anchor = element.get("id") or (element.get("name") if tag == "a" else None)
        if anchor and anchor not in result["anchors"]:
            result["anchors"].append(anchor)
        if tag in _HEADINGS:
            result["headings"].append({
                "level": _HEADINGS[tag], "text": _text(element), "anchor": anchor or "",
            })
        if tag == "a" and element.get("href"):
            link = _url_link(element.attrib["href"], _text(element), page_url)
            if link:
                result["links"].append(link)
        elif tag == _AC + "link":
            page = element.find(_RI + "page")
            attachment = element.find(_RI + "attachment")
            url = element.find(_RI + "url")
            if page is not None:
                result["links"].append({
                    "kind": "page", "title": page.get(_RI + "content-title", ""),
                    "space_key": page.get(_RI + "space-key", ""),
                    "anchor": element.get(_AC + "anchor", ""), "text": _text(element),
                })
            elif attachment is not None:
                result["links"].append({
                    "kind": "attachment", "filename": attachment.get(_RI + "filename", ""),
                    "text": _text(element),
                })
            elif url is not None:
                link = _url_link(url.get(_RI + "value", ""), _text(element), page_url)
                if link:
                    result["links"].append(link)
            elif element.get(_AC + "anchor"):
                result["links"].append({
                    "kind": "anchor", "target": urljoin(page_url, "#" + element.attrib[_AC + "anchor"]),
                    "text": _text(element),
                })
        elif tag == _AC + "structured-macro":
            parameters = {
                item.get(_AC + "name", ""): _text(item)
                for item in element.findall(_AC + "parameter")
            }
            name = element.get(_AC + "name")
            if name == "anchor" and parameters.get(""):
                if parameters[""] not in result["anchors"]:
                    result["anchors"].append(parameters[""])
            elif name == "code":
                content = element.find(_AC + "plain-text-body")
                if content is not None:
                    result["code_snippets"].append({
                        "language": parameters.get("language", ""),
                        "text": "".join(content.itertext()),
                    })
            else:
                if name:
                    result["diagnostics"]["unsupported_macros"].append(name)
        elif tag in {"pre", "code"} and id(element) not in pre_children:
            result["code_snippets"].append({
                "language": element.get("data-language", ""), "text": "".join(element.itertext()),
            })
        elif tag == "table":
            result["tables"].append({"rows": _table_rows(element)})
    return result
