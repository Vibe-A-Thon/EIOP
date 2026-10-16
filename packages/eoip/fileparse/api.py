"""Raw-binary upload routes reuse the host application's authentication boundary."""

from __future__ import annotations

import logging
from pathlib import Path
from uuid import UUID, uuid4

from eoip.fileparse.contracts import ParseError, ParseOptions
from eoip.fileparse.engine import FileParser, format_catalog
from eoip.fileparse.export import export_bundle
from eoip.graph.store import GraphStore
from eoip.ingestion.files import FileIngestionService
from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import FileResponse
from starlette.concurrency import run_in_threadpool

logger = logging.getLogger(__name__)


def build_router(store: GraphStore, root: Path) -> APIRouter:
    router = APIRouter()

    @router.get("/api/v1/connectors/files/formats")
    def formats():
        return {"formats": format_catalog(), "limits": ParseOptions().model_dump(exclude={
            "tesseract_path", "libreoffice_path",
        })}

    async def read_upload(request: Request, limit: int) -> bytes:
        media = request.headers.get("content-type", "").split(";", 1)[0].lower()
        if media != "application/octet-stream":
            raise HTTPException(415, "Send actual file bytes as application/octet-stream, not JSON or multipart")
        content = bytearray()
        async for block in request.stream():
            if len(content) + len(block) > limit:
                raise HTTPException(413, "File exceeds max_file_bytes")
            content.extend(block)
        return bytes(content)

    async def process(request: Request, filename: str, source_id: str, ocr: bool, ingest: bool, dry_run: bool):
        parser = FileParser(ParseOptions(ocr=ocr))
        content = await read_upload(request, parser.options.max_file_bytes)
        try:
            if ingest:
                service = FileIngestionService(store, root, parser)
                return await run_in_threadpool(
                    service.ingest, content, filename, source_id=source_id, dry_run=dry_run,
                    correlation_id=getattr(request.state, "correlation_id", None),
                )
            result = await run_in_threadpool(parser.parse_bytes, content, filename, source_id=source_id)
            bundle_id = str(uuid4())
            manifest = await run_in_threadpool(export_bundle, result, root / "fileparse" / bundle_id, vectors=True)
            return {"bundle_id": bundle_id, "manifest": manifest, "result": result.model_dump(mode="json")}
        except ParseError as exc:
            logger.warning("File upload decoding failed", extra={"error_category": exc.code})
            status = 503 if exc.code in {"dependency_unavailable", "tool_unavailable"} else (
                413 if exc.code.endswith("_limit") else 422
            )
            raise HTTPException(status, {"code": exc.code, "message": str(exc)}) from exc

    @router.post("/api/v1/admin/ingestion/files/parse")
    async def parse_file(
        request: Request, filename: str = Query(min_length=1, max_length=512),
        source_id: str = Query(default="file_upload", min_length=1, max_length=128), ocr: bool = False,
    ):
        return await process(request, filename, source_id, ocr, False, False)

    @router.post("/api/v1/admin/ingestion/files")
    async def ingest_file(
        request: Request, filename: str = Query(min_length=1, max_length=512),
        source_id: str = Query(default="file_upload", min_length=1, max_length=128),
        ocr: bool = False, dry_run: bool = False,
    ):
        return await process(request, filename, source_id, ocr, True, dry_run)

    @router.get("/api/v1/admin/ingestion/files/bundles/{bundle_id}/{artifact}")
    def download(bundle_id: UUID, artifact: str):
        allowed = {"parsed.json", "graph.json", "manifest.json", "chunks.jsonl", "keyword.jsonl", "vectors.jsonl"}
        if artifact not in allowed:
            raise HTTPException(404, "Unknown artifact")
        directory = (root / "fileparse").resolve()
        path = directory / str(bundle_id) / artifact
        if not path.resolve().is_relative_to(directory) or not path.is_file():
            raise HTTPException(404, "Artifact not found")
        return FileResponse(path, filename=artifact, media_type="application/json" if artifact.endswith(".json")
                            else "application/x-ndjson")

    return router
