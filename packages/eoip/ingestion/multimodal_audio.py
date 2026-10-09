"""KGR-G-002: Local Multimodal Audio & Document Ingestion.

Ingests audio files (WAV, MP3, FLAC, OGG), PDFs, DOCX, PPTX, and images
into the knowledge graph using local-only processing (Whisper for STT,
Tesseract/PaddleOCR for OCR).  All processing is air-gap safe — no
external API calls.  Produces DocumentChunk vertices linked to their
source entities.
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

from eoip.graph.store import GraphStore, Vertex

log = logging.getLogger("eoip.ingestion.multimodal_audio")


class MediaType(str, Enum):
    AUDIO_WAV = "audio/wav"
    AUDIO_MP3 = "audio/mpeg"
    AUDIO_FLAC = "audio/flac"
    AUDIO_OGG = "audio/ogg"
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_TIFF = "image/tiff"
    PLAIN_TEXT = "text/plain"
    MARKDOWN = "text/markdown"


AUDIO_TYPES = {MediaType.AUDIO_WAV, MediaType.AUDIO_MP3, MediaType.AUDIO_FLAC, MediaType.AUDIO_OGG}
IMAGE_TYPES = {MediaType.IMAGE_PNG, MediaType.IMAGE_JPEG, MediaType.IMAGE_TIFF}
DOCUMENT_TYPES = {MediaType.PDF, MediaType.DOCX, MediaType.PPTX}
TEXT_TYPES = {MediaType.PLAIN_TEXT, MediaType.MARKDOWN}

EXTENSION_MEDIA_MAP: dict[str, MediaType] = {
    ".wav": MediaType.AUDIO_WAV,
    ".mp3": MediaType.AUDIO_MP3,
    ".flac": MediaType.AUDIO_FLAC,
    ".ogg": MediaType.AUDIO_OGG,
    ".pdf": MediaType.PDF,
    ".docx": MediaType.DOCX,
    ".pptx": MediaType.PPTX,
    ".png": MediaType.IMAGE_PNG,
    ".jpg": MediaType.IMAGE_JPEG,
    ".jpeg": MediaType.IMAGE_JPEG,
    ".tiff": MediaType.IMAGE_TIFF,
    ".tif": MediaType.IMAGE_TIFF,
    ".txt": MediaType.PLAIN_TEXT,
    ".md": MediaType.MARKDOWN,
}


@dataclass(frozen=True)
class DocumentChunk:
    chunk_id: str
    source_path: str
    media_type: MediaType
    content: str
    chunk_index: int
    total_chunks: int
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def canonical_id(self) -> str:
        return f"docchunk:{self.chunk_id}"


@dataclass
class IngestionResult:
    source_path: str
    media_type: MediaType
    chunks: list[DocumentChunk]
    content_hash: str
    duration_seconds: float | None = None
    page_count: int | None = None
    word_count: int = 0
    errors: list[str] = field(default_factory=list)


class TranscriptionEngine(Protocol):
    """Local STT engine (Whisper-compatible interface)."""
    def transcribe(self, audio_path: str, *, language: str | None = None) -> dict[str, Any]: ...


class OCREngine(Protocol):
    """Local OCR engine (Tesseract/PaddleOCR-compatible interface)."""
    def extract_text(self, image_path: str, *, language: str | None = None) -> str: ...


class DocumentExtractor(Protocol):
    """Extracts text from structured documents (PDF, DOCX, PPTX)."""
    def extract(self, file_path: str) -> list[dict[str, Any]]: ...


class WhisperLocalEngine:
    """Whisper-based local STT with configurable model size."""

    def __init__(self, model_name: str = "base", device: str = "cpu") -> None:
        self.model_name = model_name
        self.device = device
        self._model: Any = None

    def _ensure_model(self) -> Any:
        if self._model is None:
            try:
                import whisper
                self._model = whisper.load_model(self.model_name, device=self.device)
            except ImportError:
                raise RuntimeError("whisper is not installed. Install with: pip install openai-whisper")
        return self._model

    def transcribe(self, audio_path: str, *, language: str | None = None) -> dict[str, Any]:
        model = self._ensure_model()
        options: dict[str, Any] = {}
        if language:
            options["language"] = language
        result = model.transcribe(audio_path, **options)
        return {
            "text": result.get("text", ""),
            "segments": result.get("segments", []),
            "language": result.get("language", language or "unknown"),
            "duration": result.get("duration"),
        }


class TesseractLocalEngine:
    """Tesseract-based local OCR."""

    def __init__(self, lang: str = "eng") -> None:
        self.lang = lang

    def extract_text(self, image_path: str, *, language: str | None = None) -> str:
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            raise RuntimeError("pytesseract or Pillow not installed")
        img = Image.open(image_path)
        return pytesseract.image_to_string(img, lang=language or self.lang)


class BasicDocumentExtractor:
    """Extracts text pages from PDF, DOCX, and PPTX using pure-Python libraries."""

    def extract(self, file_path: str) -> list[dict[str, Any]]:
        ext = Path(file_path).suffix.lower()
        if ext == ".pdf":
            return self._extract_pdf(file_path)
        if ext == ".docx":
            return self._extract_docx(file_path)
        if ext == ".pptx":
            return self._extract_pptx(file_path)
        return [{"page": 1, "text": Path(file_path).read_text(encoding="utf-8", errors="replace")}]

    def _extract_pdf(self, path: str) -> list[dict[str, Any]]:
        try:
            import fitz  # PyMuPDF
        except ImportError:
            raise RuntimeError("PyMuPDF (fitz) not installed. Install with: pip install pymupdf")
        doc = fitz.open(path)
        pages: list[dict[str, Any]] = []
        for i, page in enumerate(doc):
            pages.append({"page": i + 1, "text": page.get_text()})
        doc.close()
        return pages

    def _extract_docx(self, path: str) -> list[dict[str, Any]]:
        try:
            import docx
        except ImportError:
            raise RuntimeError("python-docx not installed")
        doc = docx.Document(path)
        text = "\n".join(p.text for p in doc.paragraphs)
        return [{"page": 1, "text": text}]

    def _extract_pptx(self, path: str) -> list[dict[str, Any]]:
        try:
            from pptx import Presentation
        except ImportError:
            raise RuntimeError("python-pptx not installed")
        prs = Presentation(path)
        slides: list[dict[str, Any]] = []
        for i, slide in enumerate(prs.slides):
            parts: list[str] = []
            for shape in slide.shapes:
                if shape.has_text_frame:
                    parts.append(shape.text_frame.text)
            slides.append({"page": i + 1, "text": "\n".join(parts)})
        return slides


def _content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _chunk_text(text: str, max_chunk_chars: int = 2000, overlap: int = 200) -> list[str]:
    if len(text) <= max_chunk_chars:
        return [text] if text.strip() else []
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = start + max_chunk_chars
        if end < len(text):
            break_at = text.rfind("\n", start, end)
            if break_at > start + max_chunk_chars // 2:
                end = break_at + 1
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


class MultimodalIngestionService:
    """Orchestrates local multimodal ingestion of audio, documents, and images."""

    def __init__(
        self,
        store: GraphStore,
        *,
        stt_engine: TranscriptionEngine | None = None,
        ocr_engine: OCREngine | None = None,
        doc_extractor: DocumentExtractor | None = None,
        chunk_size: int = 2000,
        chunk_overlap: int = 200,
    ) -> None:
        self.store = store
        self.stt = stt_engine or WhisperLocalEngine()
        self.ocr = ocr_engine or TesseractLocalEngine()
        self.doc_extractor = doc_extractor or BasicDocumentExtractor()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def detect_media_type(self, file_path: str | Path) -> MediaType:
        ext = Path(file_path).suffix.lower()
        mt = EXTENSION_MEDIA_MAP.get(ext)
        if mt is not None:
            return mt
        guessed, _ = mimetypes.guess_type(str(file_path))
        if guessed:
            try:
                return MediaType(guessed)
            except ValueError:
                pass
        raise ValueError(f"Unsupported file type: {ext}")

    def ingest_file(self, file_path: str | Path, *, source_id: str | None = None) -> IngestionResult:
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        media_type = self.detect_media_type(path)
        content_hash = _content_hash(path.read_bytes())
        source_id = source_id or path.stem

        if media_type in AUDIO_TYPES:
            return self._ingest_audio(path, media_type, content_hash, source_id)
        if media_type in IMAGE_TYPES:
            return self._ingest_image(path, media_type, content_hash, source_id)
        if media_type in DOCUMENT_TYPES:
            return self._ingest_document(path, media_type, content_hash, source_id)
        if media_type in TEXT_TYPES:
            return self._ingest_text(path, media_type, content_hash, source_id)
        raise ValueError(f"No handler for media type: {media_type}")

    def ingest_directory(self, dir_path: str | Path, *, recursive: bool = True) -> list[IngestionResult]:
        root = Path(dir_path)
        if not root.is_dir():
            raise NotADirectoryError(f"Not a directory: {root}")
        results: list[IngestionResult] = []
        pattern = "**/*" if recursive else "*"
        for p in sorted(root.glob(pattern)):
            if not p.is_file():
                continue
            try:
                self.detect_media_type(p)
            except ValueError:
                continue
            try:
                results.append(self.ingest_file(p))
            except Exception as exc:
                log.warning("Failed to ingest %s: %s", p, exc)
        return results

    def _ingest_audio(self, path: Path, media_type: MediaType, content_hash: str, source_id: str) -> IngestionResult:
        result = self.stt.transcribe(str(path))
        text = result.get("text", "")
        duration = result.get("duration")
        chunks = self._make_chunks(text, str(path), media_type, source_id)
        self._persist(chunks, source_id, media_type, content_hash)
        return IngestionResult(
            source_path=str(path),
            media_type=media_type,
            chunks=chunks,
            content_hash=content_hash,
            duration_seconds=duration,
            word_count=len(text.split()),
        )

    def _ingest_image(self, path: Path, media_type: MediaType, content_hash: str, source_id: str) -> IngestionResult:
        text = self.ocr.extract_text(str(path))
        chunks = self._make_chunks(text, str(path), media_type, source_id)
        self._persist(chunks, source_id, media_type, content_hash)
        return IngestionResult(
            source_path=str(path),
            media_type=media_type,
            chunks=chunks,
            content_hash=content_hash,
            word_count=len(text.split()),
        )

    def _ingest_document(self, path: Path, media_type: MediaType, content_hash: str, source_id: str) -> IngestionResult:
        pages = self.doc_extractor.extract(str(path))
        full_text = "\n\n".join(p["text"] for p in pages if p.get("text"))
        chunks = self._make_chunks(full_text, str(path), media_type, source_id)
        self._persist(chunks, source_id, media_type, content_hash)
        return IngestionResult(
            source_path=str(path),
            media_type=media_type,
            chunks=chunks,
            content_hash=content_hash,
            page_count=len(pages),
            word_count=len(full_text.split()),
        )

    def _ingest_text(self, path: Path, media_type: MediaType, content_hash: str, source_id: str) -> IngestionResult:
        text = path.read_text(encoding="utf-8", errors="replace")
        chunks = self._make_chunks(text, str(path), media_type, source_id)
        self._persist(chunks, source_id, media_type, content_hash)
        return IngestionResult(
            source_path=str(path),
            media_type=media_type,
            chunks=chunks,
            content_hash=content_hash,
            word_count=len(text.split()),
        )

    def _make_chunks(self, text: str, source_path: str, media_type: MediaType, source_id: str) -> list[DocumentChunk]:
        raw_chunks = _chunk_text(text, self.chunk_size, self.chunk_overlap)
        total = len(raw_chunks) or 1
        result: list[DocumentChunk] = []
        for i, content in enumerate(raw_chunks):
            chunk_id = hashlib.sha256(f"{source_id}:{i}:{content[:100]}".encode()).hexdigest()[:16]
            result.append(DocumentChunk(
                chunk_id=chunk_id,
                source_path=source_path,
                media_type=media_type,
                content=content,
                chunk_index=i,
                total_chunks=total,
                metadata={"source_id": source_id},
            ))
        return result

    def _persist(self, chunks: list[DocumentChunk], source_id: str, media_type: MediaType, content_hash: str) -> None:
        source_vid = f"multimodal_source:{source_id}"
        self.store.upsert_vertex("MultimodalSource", {
            "canonical_id": source_vid,
            "source_id": source_id,
            "media_type": media_type.value,
            "content_hash": content_hash,
        })
        for chunk in chunks:
            self.store.upsert_vertex("DocumentChunk", {
                "canonical_id": chunk.canonical_id,
                "chunk_id": chunk.chunk_id,
                "content": chunk.content,
                "chunk_index": chunk.chunk_index,
                "total_chunks": chunk.total_chunks,
                "media_type": media_type.value,
            })
            self.store.upsert_edge(
                "HAS_CHUNK",
                source_vid,
                chunk.canonical_id,
                {"chunk_index": chunk.chunk_index},
            )
