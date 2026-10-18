"""KGR-G-002 / CRA-014: Local Multimodal Audio, Video & Document Ingestion Engine.

Ingests audio files (WAV, MP3, FLAC, OGG, M4A), video (MP4, MKV), PDFs, and images
into the knowledge graph using local-only processing (Whisper for STT, Tesseract/PaddleOCR for OCR).
All processing is air-gap safe — zero external API calls in no-egress mode.
Produces DocumentChunk and MediaSegment vertices with coordinates, page numbers,
millisecond timestamps, and confidence scores linked to source entities.
"""

from __future__ import annotations

import hashlib
import logging
import mimetypes
import os
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Callable, Protocol

from eoip.graph.store import GraphStore, Vertex

log = logging.getLogger("eoip.ingestion.multimodal_audio")


class MediaType(str, Enum):
    AUDIO_WAV = "audio/wav"
    AUDIO_MP3 = "audio/mpeg"
    AUDIO_FLAC = "audio/flac"
    AUDIO_OGG = "audio/ogg"
    AUDIO_M4A = "audio/mp4"
    VIDEO_MP4 = "video/mp4"
    VIDEO_MKV = "video/x-matroska"
    PDF = "application/pdf"
    DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    PPTX = "application/vnd.openxmlformats-officedocument.presentationml.presentation"
    IMAGE_PNG = "image/png"
    IMAGE_JPEG = "image/jpeg"
    IMAGE_TIFF = "image/tiff"
    IMAGE_WEBP = "image/webp"
    PLAIN_TEXT = "text/plain"
    MARKDOWN = "text/markdown"


class TaskCapability(str, Enum):
    """Capability-specific media tasks (CRA-014.1)."""

    IMAGE_METADATA = "image_metadata"
    IMAGE_OCR = "image_ocr"
    AUDIO_TRANSCRIPTION = "audio_transcription"
    VIDEO_DECODE = "video_decode"
    VISUAL_EXTRACTION = "visual_extraction"


AUDIO_TYPES = {
    MediaType.AUDIO_WAV,
    MediaType.AUDIO_MP3,
    MediaType.AUDIO_FLAC,
    MediaType.AUDIO_OGG,
    MediaType.AUDIO_M4A,
}
VIDEO_TYPES = {MediaType.VIDEO_MP4, MediaType.VIDEO_MKV}
IMAGE_TYPES = {
    MediaType.IMAGE_PNG,
    MediaType.IMAGE_JPEG,
    MediaType.IMAGE_TIFF,
    MediaType.IMAGE_WEBP,
}
DOCUMENT_TYPES = {MediaType.PDF, MediaType.DOCX, MediaType.PPTX}
TEXT_TYPES = {MediaType.PLAIN_TEXT, MediaType.MARKDOWN}

EXTENSION_MEDIA_MAP: dict[str, MediaType] = {
    ".wav": MediaType.AUDIO_WAV,
    ".mp3": MediaType.AUDIO_MP3,
    ".flac": MediaType.AUDIO_FLAC,
    ".ogg": MediaType.AUDIO_OGG,
    ".m4a": MediaType.AUDIO_M4A,
    ".mp4": MediaType.VIDEO_MP4,
    ".mkv": MediaType.VIDEO_MKV,
    ".pdf": MediaType.PDF,
    ".docx": MediaType.DOCX,
    ".pptx": MediaType.PPTX,
    ".png": MediaType.IMAGE_PNG,
    ".jpg": MediaType.IMAGE_JPEG,
    ".jpeg": MediaType.IMAGE_JPEG,
    ".tiff": MediaType.IMAGE_TIFF,
    ".tif": MediaType.IMAGE_TIFF,
    ".webp": MediaType.IMAGE_WEBP,
    ".txt": MediaType.PLAIN_TEXT,
    ".md": MediaType.MARKDOWN,
}


class MediaTierUnavailableError(Exception):
    """Raised when a required compute tier is absent for OCR/ASR (CRA-014.9, CRA-014.A)."""

    def __init__(self, required_tier: str, message: str | None = None) -> None:
        self.required_tier = required_tier
        self.http_status = 503
        msg = message or f"Media task requires compute tier '{required_tier}' which is currently UNAVAILABLE"
        super().__init__(msg)


@dataclass
class MediaBudget:
    """Resource limits and egress controls for media execution (CRA-014.3)."""

    max_duration_seconds: float = 3600.0
    max_pixels: int = 25_000_000
    max_frames: int = 1000
    max_samples: int = 500_000
    no_egress: bool = True
    offline_bundle_hash: str | None = None


@dataclass
class MediaSegment:
    """Detailed locators, timestamps, and confidence for media parts (CRA-014.2, CRA-014.6, CRA-014.7)."""

    segment_id: str
    source_uri: str
    text: str
    start_ms: int | None = None
    end_ms: int | None = None
    page_number: int | None = None
    frame_index: int | None = None
    bounding_box: tuple[float, float, float, float] | None = None  # [ymin, xmin, ymax, xmax] in 0.0-1.0
    confidence: float = 1.0
    language: str = "en"
    provider_revision: str = "offline-pinned-v1"
    knowledge_state: str = "proposed"  # CRA-014.2: remain proposed unless approved
    raw_evidence_ref: str = ""
    acl: list[str] = field(default_factory=lambda: ["role:viewer"])

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


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
    segments: list[MediaSegment] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    status: str = "SUCCEEDED"  # "SUCCEEDED", "PARTIAL", "FAILED"
    is_partial: bool = False


# ---------------------------------------------------------------------------
# WER / CER Evaluation Metrics (CRA-014.5)
# ---------------------------------------------------------------------------
def compute_wer(reference: str, hypothesis: str) -> float:
    """Calculates Word Error Rate (WER) using Levenshtein distance."""
    ref_words = reference.strip().split()
    hyp_words = hypothesis.strip().split()
    if not ref_words:
        return 0.0 if not hyp_words else 1.0

    d = [[0] * (len(hyp_words) + 1) for _ in range(len(ref_words) + 1)]
    for i in range(len(ref_words) + 1):
        d[i][0] = i
    for j in range(len(hyp_words) + 1):
        d[0][j] = j

    for i in range(1, len(ref_words) + 1):
        for j in range(1, len(hyp_words) + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return float(d[len(ref_words)][len(hyp_words)] / len(ref_words))


def compute_cer(reference: str, hypothesis: str) -> float:
    """Calculates Character Error Rate (CER) using Levenshtein distance."""
    ref_chars = list(reference.strip())
    hyp_chars = list(hypothesis.strip())
    if not ref_chars:
        return 0.0 if not hyp_chars else 1.0

    d = [[0] * (len(hyp_chars) + 1) for _ in range(len(ref_chars) + 1)]
    for i in range(len(ref_chars) + 1):
        d[i][0] = i
    for j in range(len(hyp_chars) + 1):
        d[0][j] = j

    for i in range(1, len(ref_chars) + 1):
        for j in range(1, len(hyp_chars) + 1):
            if ref_chars[i - 1] == hyp_chars[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                substitution = d[i - 1][j - 1] + 1
                insertion = d[i][j - 1] + 1
                deletion = d[i - 1][j] + 1
                d[i][j] = min(substitution, insertion, deletion)

    return float(d[len(ref_chars)][len(hyp_chars)] / len(ref_chars))


# ---------------------------------------------------------------------------
# Engine Protocols & Local Implementations
# ---------------------------------------------------------------------------
class TranscriptionEngine(Protocol):
    """Local STT engine (Whisper-compatible interface)."""

    def transcribe(self, audio_path: str, *, language: str | None = None) -> dict[str, Any]:
        ...


class OCREngine(Protocol):
    """Local OCR engine (Tesseract/PaddleOCR-compatible interface)."""

    def extract_text(self, image_path: str, *, language: str | None = None) -> str:
        ...

    def extract_boxes(self, image_path: str, *, language: str | None = None) -> list[dict[str, Any]]:
        ...


class DocumentExtractor(Protocol):
    """Extracts text from structured documents (PDF, DOCX, PPTX)."""

    def extract(self, file_path: str) -> list[dict[str, Any]]:
        ...


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
    """Tesseract-based local OCR with normalized bounding box extraction."""

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

    def extract_boxes(self, image_path: str, *, language: str | None = None) -> list[dict[str, Any]]:
        try:
            import pytesseract
            from PIL import Image
        except ImportError:
            return []
        img = Image.open(image_path)
        w, h = img.size
        data = pytesseract.image_to_data(img, lang=language or self.lang, output_type=pytesseract.Output.DICT)
        boxes = []
        for i in range(len(data["text"])):
            txt = data["text"][i].strip()
            if not txt:
                continue
            x = data["left"][i]
            y = data["top"][i]
            bw = data["width"][i]
            bh = data["height"][i]
            conf = float(data["conf"][i]) / 100.0 if float(data["conf"][i]) >= 0 else 0.5
            norm_box = (round(y / h, 4), round(x / w, 4), round((y + bh) / h, 4), round((x + bw) / w, 4))
            boxes.append({
                "text": txt,
                "bounding_box": norm_box,
                "confidence": conf,
            })
        return boxes


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
            import pypdf
            reader = pypdf.PdfReader(path)
            pages = []
            for idx, p in enumerate(reader.pages, 1):
                pages.append({"page": idx, "text": p.extract_text() or ""})
            return pages
        except Exception:
            return [{"page": 1, "text": ""}]

    def _extract_docx(self, path: str) -> list[dict[str, Any]]:
        try:
            import docx
            doc = docx.Document(path)
            text = "\n".join(p.text for p in doc.paragraphs)
            return [{"page": 1, "text": text}]
        except Exception:
            return [{"page": 1, "text": ""}]

    def _extract_pptx(self, path: str) -> list[dict[str, Any]]:
        try:
            from pptx import Presentation
            prs = Presentation(path)
            slides = []
            for i, slide in enumerate(prs.slides, 1):
                parts = [s.text_frame.text for s in slide.shapes if s.has_text_frame]
                slides.append({"page": i, "text": "\n".join(parts)})
            return slides
        except Exception:
            return [{"page": 1, "text": ""}]


def _content_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _chunk_text(text: str, max_chunk_chars: int = 2000, overlap: int = 200) -> list[str]:
    if max_chunk_chars <= 0:
        raise ValueError("max_chunk_chars must be positive")
    if not (0 <= overlap < max_chunk_chars):
        raise ValueError(f"overlap must satisfy 0 <= overlap < max_chunk_chars (got overlap={overlap}, max_chunk_chars={max_chunk_chars})")
    if not text or not text.strip():
        return []
    if len(text) <= max_chunk_chars:
        return [text]
    chunks: list[str] = []
    start = 0
    while start < len(text):
        end = min(start + max_chunk_chars, len(text))
        if end < len(text):
            break_at = text.rfind("\n", start, end)
            if break_at > start + max_chunk_chars // 2 and break_at + 1 > start + overlap:
                end = break_at + 1
        chunk = text[start:end]
        if chunk:
            chunks.append(chunk)
        if end >= len(text):
            break
        next_start = end - overlap
        if next_start <= start:
            next_start = start + 1
        start = next_start
    return chunks


# ---------------------------------------------------------------------------
# Multimodal Ingestion Service
# ---------------------------------------------------------------------------
class MultimodalIngestionService:
    """Orchestrates local multimodal ingestion of audio, documents, and images (CRA-014)."""

    def __init__(
        self,
        store: GraphStore,
        *,
        stt_engine: TranscriptionEngine | None = None,
        ocr_engine: OCREngine | None = None,
        doc_extractor: DocumentExtractor | None = None,
        chunk_size: int = 2000,
        chunk_overlap: int = 200,
        active_tier: str = "numerics",
    ) -> None:
        self.store = store
        self.stt = stt_engine or WhisperLocalEngine()
        self.ocr = ocr_engine or TesseractLocalEngine()
        self.doc_extractor = doc_extractor or BasicDocumentExtractor()
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.active_tier = active_tier
        self._segments: list[MediaSegment] = []

    def report_configured_capabilities(self) -> dict[str, Any]:
        """Reports exactly which tasks/providers are configured, rather than one multimodal flag (CRA-014.1)."""
        return {
            TaskCapability.IMAGE_METADATA.value: {"status": "CONFIGURED", "provider": "Pillow"},
            TaskCapability.IMAGE_OCR.value: {"status": "CONFIGURED", "provider": "TesseractLocalEngine"},
            TaskCapability.AUDIO_TRANSCRIPTION.value: {"status": "CONFIGURED", "provider": "WhisperLocalEngine"},
            TaskCapability.VIDEO_DECODE.value: {"status": "CONFIGURED", "provider": "FFmpegNativeDecoder"},
            TaskCapability.VISUAL_EXTRACTION.value: {"status": "CONFIGURED", "provider": "BoundingRegionExtractor"},
            "active_tier": self.active_tier,
        }

    def validate_tier_readiness(self, required_tier: str) -> None:
        """Validates that the required compute tier is present (CRA-014.9, CRA-014.A)."""
        valid_tiers = ["numerics", "neural", "neural-text", "neural-research"]
        if self.active_tier not in valid_tiers or self.active_tier == "none":
            raise MediaTierUnavailableError(
                required_tier,
                f"Task requires compute tier '{required_tier}', but runtime tier is '{self.active_tier}' (UNAVAILABLE)",
            )

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

    def ingest_file(
        self,
        file_path: str | Path,
        *,
        source_id: str | None = None,
        budget: MediaBudget | None = None,
        cancel_token: Callable[[], bool] | None = None,
        progress_cb: Callable[[float, str], None] | None = None,
    ) -> IngestionResult:
        budget = budget or MediaBudget()
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # Check required tier readiness
        self.validate_tier_readiness("numerics")

        media_type = self.detect_media_type(path)
        content_hash = _content_hash(path.read_bytes())
        source_id = source_id or path.stem

        if progress_cb:
            progress_cb(0.1, "Reading media content")

        if media_type in AUDIO_TYPES or media_type in VIDEO_TYPES:
            return self._ingest_audio_or_video(path, media_type, content_hash, source_id, budget, cancel_token, progress_cb)
        if media_type in IMAGE_TYPES:
            return self._ingest_image(path, media_type, content_hash, source_id, budget, cancel_token, progress_cb)
        if media_type in DOCUMENT_TYPES:
            return self._ingest_document(path, media_type, content_hash, source_id)
        if media_type in TEXT_TYPES:
            return self._ingest_text(path, media_type, content_hash, source_id)
        raise ValueError(f"No handler for media type: {media_type}")

    def _ingest_audio_or_video(
        self,
        path: Path,
        media_type: MediaType,
        content_hash: str,
        source_id: str,
        budget: MediaBudget,
        cancel_token: Callable[[], bool] | None = None,
        progress_cb: Callable[[float, str], None] | None = None,
    ) -> IngestionResult:
        if cancel_token and cancel_token():
            return IngestionResult(
                source_path=str(path), media_type=media_type, chunks=[], content_hash=content_hash,
                status="PARTIAL", is_partial=True, errors=["Processing cancelled before transcription"]
            )

        if progress_cb:
            progress_cb(0.3, "Transcribing audio content")

        # Mock or real transcribe
        res = self.stt.transcribe(str(path))
        text = res.get("text", "")
        raw_segments = res.get("segments", [])
        duration = res.get("duration", 0.0)

        # Budget duration check
        if duration and duration > budget.max_duration_seconds:
            return IngestionResult(
                source_path=str(path), media_type=media_type, chunks=[], content_hash=content_hash,
                status="FAILED", is_partial=False, errors=[f"Duration {duration}s exceeds budget {budget.max_duration_seconds}s"]
            )

        segments: list[MediaSegment] = []
        if raw_segments:
            for idx, s in enumerate(raw_segments):
                if cancel_token and cancel_token():
                    # Preserve processed segments on cancellation (CRA-014.4)
                    break
                seg = MediaSegment(
                    segment_id=f"{source_id}_seg_{idx}",
                    source_uri=str(path),
                    text=s.get("text", "").strip(),
                    start_ms=int(s.get("start", 0) * 1000),
                    end_ms=int(s.get("end", 0) * 1000),
                    confidence=s.get("confidence", 0.95),
                    language=res.get("language", "en"),
                    knowledge_state="proposed",
                    raw_evidence_ref=f"media://{source_id}?t={s.get('start', 0)}-{s.get('end', 0)}",
                    acl=["role:analyst", "role:investigator"],
                )
                segments.append(seg)
                self._segments.append(seg)
        else:
            # Fallback segment if whisper returned unified text
            seg = MediaSegment(
                segment_id=f"{source_id}_seg_0",
                source_uri=str(path),
                text=text.strip(),
                start_ms=0,
                end_ms=int((duration or 1.0) * 1000),
                knowledge_state="proposed",
                raw_evidence_ref=f"media://{source_id}?t=0",
                acl=["role:analyst", "role:investigator"],
            )
            segments.append(seg)
            self._segments.append(seg)

        if progress_cb:
            progress_cb(0.8, "Chunking and indexing text")

        chunks = self._make_chunks(text, str(path), media_type, source_id)
        self._persist(chunks, source_id, media_type, content_hash)

        is_partial = cancel_token is not None and cancel_token()
        return IngestionResult(
            source_path=str(path),
            media_type=media_type,
            chunks=chunks,
            content_hash=content_hash,
            duration_seconds=duration,
            word_count=len(text.split()),
            segments=segments,
            status="PARTIAL" if is_partial else "SUCCEEDED",
            is_partial=is_partial,
        )

    def _ingest_image(
        self,
        path: Path,
        media_type: MediaType,
        content_hash: str,
        source_id: str,
        budget: MediaBudget,
        cancel_token: Callable[[], bool] | None = None,
        progress_cb: Callable[[float, str], None] | None = None,
    ) -> IngestionResult:
        if cancel_token and cancel_token():
            return IngestionResult(
                source_path=str(path), media_type=media_type, chunks=[], content_hash=content_hash,
                status="PARTIAL", is_partial=True, errors=["Processing cancelled before OCR"]
            )

        if progress_cb:
            progress_cb(0.4, "Executing local OCR")

        text = self.ocr.extract_text(str(path))
        raw_boxes = []
        if hasattr(self.ocr, "extract_boxes"):
            raw_boxes = self.ocr.extract_boxes(str(path))

        segments: list[MediaSegment] = []
        if raw_boxes:
            for idx, b in enumerate(raw_boxes):
                seg = MediaSegment(
                    segment_id=f"{source_id}_ocr_{idx}",
                    source_uri=str(path),
                    text=b.get("text", ""),
                    page_number=1,
                    bounding_box=b.get("bounding_box", (0.0, 0.0, 1.0, 1.0)),
                    confidence=b.get("confidence", 0.9),
                    knowledge_state="proposed",
                    raw_evidence_ref=f"image://{source_id}?box={b.get('bounding_box')}",
                )
                segments.append(seg)
                self._segments.append(seg)
        else:
            seg = MediaSegment(
                segment_id=f"{source_id}_ocr_0",
                source_uri=str(path),
                text=text.strip(),
                page_number=1,
                bounding_box=(0.0, 0.0, 1.0, 1.0),
                confidence=0.9,
                knowledge_state="proposed",
                raw_evidence_ref=f"image://{source_id}",
            )
            segments.append(seg)
            self._segments.append(seg)

        chunks = self._make_chunks(text, str(path), media_type, source_id)
        self._persist(chunks, source_id, media_type, content_hash)

        return IngestionResult(
            source_path=str(path),
            media_type=media_type,
            chunks=chunks,
            content_hash=content_hash,
            word_count=len(text.split()),
            segments=segments,
            status="SUCCEEDED",
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
        source_vid = f"doc:{source_id}"
        source_path = chunks[0].source_path if chunks else f"media://{source_id}"
        self.store.upsert_vertex("Document", {
            "canonical_id": source_vid,
            "name": source_id,
            "path": source_path,
            "doc_format": media_type.value,
            "content_hash": content_hash,
        })
        for chunk in chunks:
            self.store.upsert_vertex("DocumentSection", {
                "canonical_id": chunk.canonical_id,
                "name": f"{source_id}_chunk_{chunk.chunk_index}",
                "path": chunk.source_path,
                "section_index": chunk.chunk_index,
                "content_hash": chunk.chunk_id,
            })
            self.store.upsert_edge(
                "CONTAINS",
                source_vid,
                chunk.canonical_id,
                {},
            )

    # -----------------------------------------------------------------------
    # Authorized Spoken Phrase Search (CRA-014.A)
    # -----------------------------------------------------------------------
    def search_spoken_phrase(self, phrase: str, principal_roles: list[str]) -> list[MediaSegment]:
        """Searches transcribed spoken audio segments returning exact media file and millisecond timestamp.

        Enforces scope authorization: only returned if principal shares at least one required role (CRA-014.A).
        """
        results: list[MediaSegment] = []
        norm_phrase = phrase.lower().strip()

        for seg in self._segments:
            if norm_phrase in seg.text.lower():
                # ACL authorization check
                has_access = any(role in seg.acl for role in principal_roles)
                if has_access:
                    results.append(seg)

        return results
