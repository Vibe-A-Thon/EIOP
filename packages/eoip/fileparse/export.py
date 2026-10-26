"""Atomic JSON/JSONL artifacts for graph, keyword, vector and RAG consumers."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory

from eoip.fileparse.contracts import ParseResult
from eoip.retrieval.vectors import tokenize


def graph_data(result: ParseResult) -> dict:
    entities = []
    relationships = []
    for document in result.documents:
        entities.append({
            "canonical_id": document.document_id, "entity_type": "Document",
            "name": document.title, "path": document.source_uri, "doc_format": document.format,
            "content_hash": document.content_hash, "parser_version": document.parser_version,
            "description": "\n".join(section.text for section in document.sections),
            "payload_json": json.dumps(document.model_dump(mode="json"), ensure_ascii=False, allow_nan=False),
        })
        if document.parent_id:
            relationships.append({
                "from_id": document.parent_id, "to_id": document.document_id, "type": "CONTAINS",
                "properties": {"source_ref": document.source_uri},
            })
    for chunk in result.chunks:
        entities.append({
            "canonical_id": chunk.chunk_id, "entity_type": "DocumentSection",
            "name": f"Section {chunk.section_index} ({chunk.start_char}:{chunk.end_char})",
            "path": chunk.citations[0], "content": chunk.text, "section_index": chunk.section_index,
            "content_hash": hashlib.sha256(chunk.text.encode()).hexdigest(),
            "payload_json": json.dumps(chunk.model_dump(mode="json"), ensure_ascii=False),
        })
        relationships.append({
            "from_id": chunk.document_id, "to_id": chunk.chunk_id, "type": "CONTAINS",
            "properties": {"source_ref": chunk.citations[0]},
        })
    return {"entities": entities, "relationships": relationships}


def export_bundle(result: ParseResult, destination: str | Path, *, vectors: bool = False) -> dict:
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists():
        raise FileExistsError("Export destination already exists; use a new bundle directory")
    with TemporaryDirectory(prefix=".eoip-export-", dir=destination.parent) as temporary:
        staging = Path(temporary) / "bundle"
        staging.mkdir()
        documents = staging / "documents"
        documents.mkdir()

        def write_json(path: Path, value) -> None:
            path.write_text(
                json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8",
            )

        def write_jsonl(path: Path, records) -> None:
            with path.open("w", encoding="utf-8") as stream:
                for record in records:
                    stream.write(json.dumps(record, ensure_ascii=False, allow_nan=False) + "\n")

        write_json(staging / "parsed.json", result.model_dump(mode="json"))
        for document in result.documents:
            write_json(documents / f"{document.document_id.rsplit(':', 1)[-1]}.json", document.model_dump(mode="json"))
        write_jsonl(staging / "chunks.jsonl", (chunk.model_dump(mode="json") for chunk in result.chunks))
        write_json(staging / "graph.json", graph_data(result))
        write_jsonl(staging / "keyword.jsonl", (
            {"id": chunk.chunk_id, "document_id": chunk.document_id, "tokens": tokenize(chunk.text),
             "citations": chunk.citations}
            for chunk in result.chunks
        ))
        model = family = None
        if vectors:
            from eoip.models.embeddings import embedder_family, semantic_embedder

            embedder = semantic_embedder()
            family = embedder_family(embedder)
            model = "test-hashing-256" if family == "test-hashing" else getattr(embedder, "model_name", "")
            embed = getattr(embedder, "embed_one", None) or embedder.embed
            write_jsonl(staging / "vectors.jsonl", (
                {"id": chunk.chunk_id, "document_id": chunk.document_id, "vector": embed(chunk.text),
                 "embedding_model": model, "embedding_family": family, "citations": chunk.citations}
                for chunk in result.chunks
            ))
        files = {
            path.relative_to(staging).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in sorted(staging.rglob("*")) if path.is_file()
        }
        manifest = {
            "schema_version": "1.0", "status": result.status, "parser_version": result.parser_version,
            "documents": len(result.documents), "chunks": len(result.chunks),
            "errors": [issue.model_dump() for issue in result.errors], "files": files,
            "embedding_model": model if vectors else None,
            "embedding_family": family if vectors else None,
            "embedding_note": ("Deterministic lexical hashing (test-hashing), not a trained semantic embedding model"
                               if vectors and family == "test-hashing" else None),
        }
        write_json(staging / "manifest.json", manifest)
        os.rename(staging, destination)
    return manifest
