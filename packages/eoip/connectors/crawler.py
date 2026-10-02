"""Controlled allowlist-only web crawler for the EKAF generic web source."""

from __future__ import annotations

import hashlib
import ipaddress
import socket
from collections import deque
from collections.abc import Callable
from html.parser import HTMLParser
from urllib.parse import urldefrag, urljoin, urlsplit, urlunsplit

import httpx
from eoip.contracts.source_event import SourceEventV2, utc_now_iso
from pydantic import BaseModel, ConfigDict, Field, field_validator


class CrawlScope(BaseModel):
    model_config = ConfigDict(extra="forbid")

    start_urls: list[str] = Field(min_length=1, max_length=100)
    allowed_hosts: list[str] = Field(min_length=1, max_length=100)
    include_paths: list[str] = Field(default_factory=lambda: ["/"], max_length=100)
    exclude_paths: list[str] = Field(default_factory=list, max_length=100)
    max_depth: int = Field(default=2, ge=0, le=10)
    page_limit: int = Field(default=100, ge=1, le=10_000)
    mime_types: list[str] = Field(default_factory=lambda: ["text/html"], max_length=50)
    max_page_bytes: int = Field(default=2_000_000, ge=1024, le=50_000_000)

    @field_validator("allowed_hosts")
    @classmethod
    def normalize_hosts(cls, value: list[str]) -> list[str]:
        normalized = []
        for host in value:
            clean = host.strip().lower().rstrip(".")
            if not clean or ":" in clean or "/" in clean or "@" in clean:
                raise ValueError("allowed_hosts entries must be hostnames without ports")
            normalized.append(clean)
        return sorted(set(normalized))


class _HtmlDocumentParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.title: list[str] = []
        self.headings: list[str] = []
        self.text: list[str] = []
        self.links: list[str] = []
        self._in_title = False
        self._in_heading = False
        self._ignored = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag in {"script", "style", "noscript"}:
            self._ignored += 1
        elif tag == "title":
            self._in_title = True
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._in_heading = True
        elif tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"script", "style", "noscript"} and self._ignored:
            self._ignored -= 1
        elif tag == "title":
            self._in_title = False
        elif tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            self._in_heading = False

    def handle_data(self, data: str) -> None:
        value = " ".join(data.split())
        if not value or self._ignored:
            return
        self.text.append(value)
        if self._in_title:
            self.title.append(value)
        if self._in_heading:
            self.headings.append(value)


class ControlledWebCrawler:
    def __init__(
        self,
        source_id: str,
        scope: CrawlScope,
        *,
        client: httpx.Client | None = None,
        resolver: Callable[[str], list[str]] | None = None,
    ) -> None:
        self.source_id = source_id
        self.scope = scope
        self._client = client or httpx.Client(timeout=20, follow_redirects=False, trust_env=False)
        self._owns_client = client is None
        self._resolver = resolver or self._resolve

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def crawl(self) -> list[SourceEventV2]:
        frontier = deque((self._canonical(url), 0) for url in self.scope.start_urls)
        visited: set[str] = set()
        events: list[SourceEventV2] = []
        while frontier and len(events) < self.scope.page_limit:
            url, depth = frontier.popleft()
            if url in visited:
                continue
            visited.add(url)
            self._validate_target(url)
            response, final_url = self._fetch(url)
            content_type = response.headers.get("content-type", "").split(";", 1)[0].lower()
            if content_type not in self.scope.mime_types:
                continue
            body = response.content
            if len(body) > self.scope.max_page_bytes:
                raise ValueError("crawler response exceeds max_page_bytes")
            content_hash = hashlib.sha256(body).hexdigest()
            captured_at = utc_now_iso()
            payload: dict = {
                "url": final_url,
                "content_type": content_type,
                "status_code": response.status_code,
            }
            links: list[str] = []
            if content_type == "text/html":
                parser = _HtmlDocumentParser()
                parser.feed(response.text)
                links = [self._canonical(urljoin(final_url, link)) for link in parser.links]
                payload.update(
                    title=" ".join(parser.title),
                    headings=parser.headings,
                    text=" ".join(parser.text),
                    links=links,
                )
            event_id = hashlib.sha256(
                f"web:{self.source_id}:{final_url}:{content_hash}".encode()
            ).hexdigest()
            events.append(
                SourceEventV2(
                    event_id=event_id,
                    source_system="web",
                    source_instance_id=self.source_id,
                    source_record_id=final_url,
                    operation="UPSERT",
                    source_version=content_hash,
                    event_time=captured_at,
                    captured_at=captured_at,
                    content_hash=content_hash,
                    payload=payload,
                    metadata={"crawler": "controlled-web/1.0", "depth": depth},
                )
            )
            if depth < self.scope.max_depth:
                for link in links:
                    if link not in visited and self._is_in_scope(link):
                        frontier.append((link, depth + 1))
        return events

    def _fetch(self, url: str) -> tuple[httpx.Response, str]:
        current = url
        for _ in range(6):
            self._validate_target(current)
            response = self._client.get(current, headers={"User-Agent": "EOIP-ControlledCrawler/1.0"})
            if response.status_code in {301, 302, 303, 307, 308}:
                location = response.headers.get("location")
                if not location:
                    raise ValueError("redirect response has no Location")
                current = self._canonical(urljoin(current, location))
                continue
            response.raise_for_status()
            return response, current
        raise ValueError("crawler redirect limit exceeded")

    def _validate_target(self, url: str) -> None:
        if not self._is_in_scope(url):
            raise ValueError("crawler target is outside the configured allowlist")
        host = urlsplit(url).hostname or ""
        addresses = self._resolver(host)
        if not addresses:
            raise ValueError("crawler target did not resolve")
        for address in addresses:
            ip = ipaddress.ip_address(address)
            if not ip.is_global:
                raise ValueError("crawler target resolves to a non-public address")

    def _is_in_scope(self, url: str) -> bool:
        parsed = urlsplit(url)
        host = (parsed.hostname or "").lower().rstrip(".")
        if parsed.scheme not in {"http", "https"} or parsed.username or parsed.password:
            return False
        if host not in self.scope.allowed_hosts:
            return False
        path = parsed.path or "/"
        included = any(path.startswith(prefix) for prefix in self.scope.include_paths)
        excluded = any(path.startswith(prefix) for prefix in self.scope.exclude_paths)
        return included and not excluded

    @staticmethod
    def _canonical(url: str) -> str:
        clean, _fragment = urldefrag(url.strip())
        parsed = urlsplit(clean)
        scheme = parsed.scheme.lower()
        host = (parsed.hostname or "").lower().rstrip(".")
        port = parsed.port
        netloc = host if port is None or (scheme, port) in {("http", 80), ("https", 443)} else f"{host}:{port}"
        return urlunsplit((scheme, netloc, parsed.path or "/", parsed.query, ""))

    @staticmethod
    def _resolve(host: str) -> list[str]:
        return sorted({item[4][0] for item in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM)})
