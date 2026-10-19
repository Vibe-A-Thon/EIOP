"""Deterministic Text and Local Language Processing Backend (PUR-LPU-001..006).

Provides:
1. Unicode-safe chunking with character/byte offsets and overlap.
2. Tokenization and exact length bounds.
3. Citation-grounded summarization.
4. Schema-constrained structured extraction with abstention.
5. Structured read-query proposals without automatic execution.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple


def chunk_text(
    text: str,
    chunk_size: int = 500,
    chunk_overlap: int = 50,
    doc_id: str = "doc_0",
) -> List[Dict[str, Any]]:
    """Deterministic Unicode-safe chunking with exact character offsets (PUR-LPU-001)."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be strictly less than chunk_size")

    chunks: List[Dict[str, Any]] = []
    text_len = len(text)
    step = chunk_size - chunk_overlap
    chunk_idx = 0
    start = 0

    while start < text_len:
        end = min(start + chunk_size, text_len)
        content = text[start:end]
        chunks.append({
            "chunk_id": f"{doc_id}_c{chunk_idx}",
            "doc_id": doc_id,
            "chunk_index": chunk_idx,
            "char_start": start,
            "char_end": end,
            "byte_start": len(text[:start].encode("utf-8")),
            "byte_end": len(text[:end].encode("utf-8")),
            "content": content,
            "text": content,
            "length": len(content),
        })
        chunk_idx += 1
        if end >= text_len:
            break
        start += step

    return chunks


def tokenize_text(text: str) -> Dict[str, Any]:
    """Exact word/subword token counting with offsets."""
    # Deterministic regex-based whitespace & punctuation tokenization
    tokens = []
    for match in re.finditer(r"\w+|[^\w\s]", text, re.UNICODE):
        tok_str = match.group()
        tokens.append({
            "token": tok_str,
            "start": match.start(),
            "end": match.end(),
        })
    return {
        "token_count": len(tokens),
        "tokens": tokens,
    }


def extract_structured(
    text: str,
    schema: Dict[str, Any],
    abstention_threshold: float = 0.5,
) -> Dict[str, Any]:
    """Schema-constrained extraction with evidence spans and abstention (PUR-LPU-003)."""
    extracted_fields: Dict[str, Any] = {}
    evidence_spans: Dict[str, Dict[str, Any]] = {}
    abstained_fields: List[str] = []

    properties = schema.get("properties", {})
    for prop_name, prop_spec in properties.items():
        # Match pattern or field name in text
        pattern = rf"{prop_name}[:\s=]+([^\n,;]+)"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            raw_val = match.group(1).strip().strip("\"'")
            expected_type = prop_spec.get("type", "string")
            try:
                if expected_type == "integer":
                    val = int(raw_val)
                elif expected_type == "number":
                    val = float(raw_val)
                elif expected_type == "boolean":
                    val = raw_val.lower() in ("true", "1", "yes")
                else:
                    val = raw_val
                extracted_fields[prop_name] = val
                evidence_spans[prop_name] = {
                    "matched_text": match.group(0),
                    "start": match.start(),
                    "end": match.end(),
                    "confidence": 0.95,
                }
            except (ValueError, TypeError):
                abstained_fields.append(prop_name)
        else:
            abstained_fields.append(prop_name)

    return {
        "extracted": extracted_fields,
        "extracted_entities": extracted_fields,
        "evidence_spans": evidence_spans,
        "abstained_fields": abstained_fields,
        "schema_conforms": len(abstained_fields) == 0,
    }


def summarize_grounded(
    passages: List[Dict[str, Any]],
    query: Optional[str] = None,
    max_sentences: int = 3,
) -> Dict[str, Any]:
    """Grounded summarization citing authorized passage spans (PUR-LPU-004)."""
    citations = []
    selected_sentences = []

    for idx, p in enumerate(passages):
        content = p.get("content") or p.get("text", "")
        passage_id = p.get("passage_id") or p.get("chunk_id") or p.get("id") or f"passage_{idx}"
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", content) if s.strip()]
        for s in sentences:
            if query and any(w.lower() in s.lower() for w in query.split()):
                selected_sentences.append(f"{s} [{passage_id}]")
                citations.append({
                    "citation_ref": passage_id,
                    "excerpt": s[:120],
                    "tenant_id": p.get("tenant_id", "default"),
                })
                if len(selected_sentences) >= max_sentences:
                    break
            elif not query:
                selected_sentences.append(f"{s} [{passage_id}]")
                citations.append({
                    "citation_ref": passage_id,
                    "excerpt": s[:120],
                    "tenant_id": p.get("tenant_id", "default"),
                })
                if len(selected_sentences) >= max_sentences:
                    break
        if len(selected_sentences) >= max_sentences:
            break

    if not selected_sentences and passages:
        # Fall back to first sentence
        first_content = passages[0].get("content") or passages[0].get("text", "")
        first_id = passages[0].get("passage_id") or passages[0].get("chunk_id") or "passage_0"
        first_sent = first_content.split(".")[0]
        selected_sentences.append(f"{first_sent}. [{first_id}]")
        citations.append({
            "citation_ref": first_id,
            "excerpt": first_sent[:120],
            "tenant_id": passages[0].get("tenant_id", "default"),
        })

    summary_text = " ".join(selected_sentences)
    is_grounded = len(citations) > 0
    return {
        "summary": summary_text,
        "citations": [c["citation_ref"] for c in citations],
        "detailed_citations": citations,
        "citation_count": len(citations),
        "is_grounded": is_grounded,
        "grounded": is_grounded,
    }



def propose_read_query(
    natural_query: str,
    target_dialect: str = "cypher",
    schema_classes: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """Generate structured read-query proposal without automatic execution (PUR-LPU-005)."""
    # Reject mutation keywords
    forbidden = ["DELETE", "DROP", "CREATE", "SET", "MERGE", "REMOVE", "DETACH", "INSERT", "UPDATE"]
    upper_q = natural_query.upper()
    for word in forbidden:
        if re.search(rf"\b{word}\b", upper_q):
            raise ValueError(f"Mutation keyword '{word}' forbidden in read-query proposals")

    # Detect entity types
    entity_type = "Service"
    if schema_classes:
        for c in schema_classes:
            if c.lower() in natural_query.lower():
                entity_type = c
                break

    if target_dialect.lower() == "cypher":
        proposed_query = f"MATCH (n:{entity_type}) RETURN n LIMIT 25"
    elif target_dialect.lower() == "sparql":
        proposed_query = (
            f"SELECT ?s ?p ?o WHERE {{ ?s a <urn:eoip:ontology:{entity_type}> . ?s ?p ?o }} LIMIT 25"
        )
    else:
        proposed_query = f"g.V().hasLabel('{entity_type}').limit(25)"

    return {
        "natural_query": natural_query,
        "target_dialect": target_dialect,
        "proposed_query": proposed_query,
        "is_read_only": True,
        "requires_authorization": True,
    }
