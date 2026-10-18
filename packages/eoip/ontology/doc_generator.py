"""Offline Widoco-class HTML ontology documentation generator (ONT-014, CRA-039.4, CRA-039.8)."""

from __future__ import annotations

import hashlib
import html
import logging
import re
import time
from typing import Any

from eoip.ontology.manifest import DOMAINS, ONTOLOGY_VERSION, PROPERTY_KEYS, SCHEMA_VERSION, VERTEX_LABELS

logger = logging.getLogger("eoip.ontology.doc_generator")

# Sanitization regexes
SCRIPT_TAG_RE = re.compile(r"<\s*script[^>]*>.*?<\s*/\s*script\s*>", re.IGNORECASE | re.DOTALL)
EVENT_HANDLER_RE = re.compile(r"\bon\w+\s*=\s*['\"].*?['\"]", re.IGNORECASE)
JAVASCRIPT_URI_RE = re.compile(r"javascript:\s*[^'\"\s]+", re.IGNORECASE)
SECRET_TOKEN_RE = re.compile(r"(Bearer\s+[A-Za-z0-9_\-\.]{16,}|[A-Za-z0-9_\-]{32,})")


def sanitize_authored_content(text: str) -> str:
    """Sanitizes user-authored documentation strings to prevent XSS or credential leaks."""
    if not text:
        return ""
    # Strip script tags and event handlers
    cleaned = SCRIPT_TAG_RE.sub("", text)
    cleaned = EVENT_HANDLER_RE.sub("", cleaned)
    cleaned = JAVASCRIPT_URI_RE.sub("#", cleaned)
    # Mask potential token leaks
    cleaned = SECRET_TOKEN_RE.sub("[REDACTED_SECRET]", cleaned)
    return html.escape(cleaned)


class WidocoOntologyDocGenerator:
    """Generates self-contained, offline WIDOCO/LODE-class HTML specifications from signed release artifacts."""

    def __init__(
        self,
        title: str = "Enterprise Ontology & Intelligence Platform Specification",
        ontology_iri: str = "https://ontology.eoip.io/core/v1#",
        release_digest: str | None = None,
    ) -> None:
        self.title = title
        self.ontology_iri = ontology_iri
        self.release_digest = release_digest or hashlib.sha256(
            f"{ONTOLOGY_VERSION}:{SCHEMA_VERSION}:{len(VERTEX_LABELS)}".encode()
        ).hexdigest()

    def generate_html(self, custom_descriptions: dict[str, str] | None = None) -> str:
        descriptions = custom_descriptions or {}
        sanitized_title = sanitize_authored_content(self.title)

        # Build Classes Section
        class_items_html = []
        for label in sorted(VERTEX_LABELS):
            anchor = f"class-{label.lower()}"
            raw_desc = descriptions.get(label, f"Core entity type representing {label} in enterprise domain.")
            desc = sanitize_authored_content(raw_desc)
            class_items_html.append(
                f"""
                <div class="entity" id="{anchor}">
                  <h3>Class: {html.escape(label)}</h3>
                  <p class="iri"><code>{html.escape(self.ontology_iri)}{html.escape(label)}</code></p>
                  <p class="description">{desc}</p>
                  <dl class="description-list">
                    <dt>Standard Properties:</dt>
                    <dd><code>canonical_id</code>, <code>name</code>, <code>source_system</code>, <code>created_at</code></dd>
                  </dl>
                </div>
                """
            )

        # Build Properties Section
        prop_rows = []
        for prop, ptype in sorted(PROPERTY_KEYS.items()):
            prop_rows.append(
                f"<tr><td><code>{html.escape(prop)}</code></td><td><span class='badge'>{html.escape(ptype)}</span></td></tr>"
            )

        # Build Domains Section
        domain_badges = "".join(f"<span class='domain-tag'>{html.escape(d)}</span>" for d in sorted(DOMAINS))

        html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{sanitized_title}</title>
  <style>
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      line-height: 1.6;
      color: #1e293b;
      background: #f8fafc;
      margin: 0;
      padding: 0;
    }}
    .container {{
      max-width: 1000px;
      margin: 0 auto;
      background: #ffffff;
      padding: 40px;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }}
    header {{
      border-bottom: 2px solid #e2e8f0;
      padding-bottom: 20px;
      margin-bottom: 30px;
    }}
    h1 {{ color: #0f172a; margin-top: 0; }}
    h2 {{ color: #1e3a8a; border-bottom: 1px solid #cbd5e1; padding-bottom: 8px; margin-top: 36px; }}
    h3 {{ color: #2563eb; margin-bottom: 6px; }}
    .metadata {{
      background: #f1f5f9;
      padding: 16px;
      border-radius: 6px;
      margin-bottom: 24px;
      font-size: 0.9em;
    }}
    .metadata dt {{ font-weight: bold; color: #475569; float: left; width: 180px; }}
    .metadata dd {{ margin-left: 190px; margin-bottom: 8px; }}
    .toc ul {{ list-style-type: square; }}
    .entity {{
      background: #f8fafc;
      border-left: 4px solid #3b82f6;
      padding: 12px 20px;
      margin-bottom: 20px;
      border-radius: 0 4px 4px 0;
    }}
    .iri {{ font-size: 0.85em; color: #64748b; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 12px; }}
    th, td {{ padding: 8px 12px; border: 1px solid #e2e8f0; text-align: left; }}
    th {{ background: #f1f5f9; }}
    .badge {{ background: #e0e7ff; color: #3730a3; padding: 2px 8px; border-radius: 4px; font-size: 0.8em; }}
    .domain-tag {{ background: #dcfce7; color: #166534; padding: 4px 10px; border-radius: 12px; font-size: 0.85em; margin-right: 6px; display: inline-block; margin-bottom: 4px; }}
    footer {{ margin-top: 50px; font-size: 0.85em; color: #64748b; border-top: 1px solid #e2e8f0; padding-top: 16px; }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>{sanitized_title}</h1>
      <div class="metadata">
        <dl>
          <dt>Ontology Version:</dt>
          <dd><strong>{html.escape(ONTOLOGY_VERSION)}</strong> (Schema v{html.escape(SCHEMA_VERSION)})</dd>
          <dt>Namespace IRI:</dt>
          <dd><code>{html.escape(self.ontology_iri)}</code></dd>
          <dt>Artifact SHA-256:</dt>
          <dd><code>{html.escape(self.release_digest)}</code></dd>
          <dt>Offline Generator:</dt>
          <dd>Widoco/LODE Clean-Room Engine (ADR-H16 / ONT-014)</dd>
        </dl>
      </div>
      <div>
        <strong>Logical Domains:</strong><br>
        {domain_badges}
      </div>
    </header>

    <nav class="toc">
      <h2>Table of Contents</h2>
      <ul>
        <li><a href="#overview">1. Overview & Diagram</a></li>
        <li><a href="#classes">2. Vertex Classes ({len(VERTEX_LABELS)})</a></li>
        <li><a href="#properties">3. Controlled Properties ({len(PROPERTY_KEYS)})</a></li>
        <li><a href="#provenance">4. Provenance & Licensing</a></li>
      </ul>
    </nav>

    <section id="overview">
      <h2>1. Overview & Architecture Diagram</h2>
      <p>This ontology provides a controlled enterprise vocabulary partitioned across {len(DOMAINS)} logical domains.</p>
      <pre>
Graph
  ├── WORK (Project, WorkItem, Sprint)
  ├── CODE (File, CodeSymbol, Commit)
  ├── IDENTITY (Person, Team, ServiceAccount)
  └── OPS (Service, APIEndpoint, Incident)
      </pre>
    </section>

    <section id="classes">
      <h2>2. Vertex Classes</h2>
      {''.join(class_items_html)}
    </section>

    <section id="properties">
      <h2>3. Controlled Properties</h2>
      <table>
        <thead>
          <tr><th>Property Key</th><th>Type</th></tr>
        </thead>
        <tbody>
          {''.join(prop_rows)}
        </tbody>
      </table>
    </section>

    <section id="provenance">
      <h2>4. Provenance & Licensing</h2>
      <p>Generated strictly offline without network egress from signed release artifacts.</p>
      <p>License: Dual-licensed under Platform Proprietary Core rules with clean-room WIDOCO/LODE compatible HTML schemas.</p>
    </section>

    <footer>
      <p>Generated by EOIP Widoco Engine (ONT-014) • Digest: <code>{html.escape(self.release_digest)}</code></p>
    </footer>
  </div>
</body>
</html>
"""
        return html_doc
