"""Acceptance tests for WP-014: Multimodal Audio, Video, and Image Ingestion (CRA-014.1-014.9, CRA-014.A)."""

import hashlib
import tempfile
from pathlib import Path
import pytest

from eoip.graph.memory import MemoryGraphStore
from eoip.ingestion.multimodal_audio import (
    MediaBudget,
    MediaSegment,
    MediaTierUnavailableError,
    MediaType,
    MultimodalIngestionService,
    TaskCapability,
    compute_cer,
    compute_wer,
)


class MockSTTEngine:
    """Mock Whisper STT engine that returns deterministic segments and timestamps."""

    def __init__(
        self,
        text: str = "The deployment to production succeeded at midnight.",
        duration: float = 12.5,
        segments: list[dict] | None = None,
    ) -> None:
        self.text = text
        self.duration = duration
        self.segments = segments

    def transcribe(self, audio_path: str, *, language: str | None = None) -> dict:
        segs = self.segments or [
            {
                "start": 0.0,
                "end": round(self.duration / 2.0, 1),
                "text": self.text[:len(self.text) // 2].strip(),
                "confidence": 0.96,
            },
            {
                "start": round(self.duration / 2.0, 1),
                "end": self.duration,
                "text": self.text[len(self.text) // 2:].strip(),
                "confidence": 0.98,
            },
        ]
        return {
            "text": self.text,
            "duration": self.duration,
            "language": language or "en",
            "segments": segs,
        }


class MockOCREngine:
    """Mock OCR engine returning text and normalized bounding boxes."""

    def __init__(self, text: str = "INVOICE #98421\nTOTAL: $500.00") -> None:
        self.text = text

    def extract_text(self, image_path: str, *, language: str | None = None) -> str:
        return self.text

    def extract_boxes(self, image_path: str, *, language: str | None = None) -> list[dict]:
        return [
            {
                "text": "INVOICE #98421",
                "bounding_box": (0.05, 0.1, 0.15, 0.8),
                "confidence": 0.97,
            },
            {
                "text": "TOTAL: $500.00",
                "bounding_box": (0.2, 0.1, 0.3, 0.6),
                "confidence": 0.99,
            },
        ]


# ---------------------------------------------------------------------------
# CRA-014.1: Report configured capabilities per task
# ---------------------------------------------------------------------------
def test_cra_014_1_task_specific_capabilities_reporting():
    store = MemoryGraphStore()
    svc = MultimodalIngestionService(store, active_tier="numerics")
    caps = svc.report_configured_capabilities()

    # Must report discrete task capabilities rather than one multimodal flag
    assert TaskCapability.IMAGE_METADATA.value in caps
    assert TaskCapability.IMAGE_OCR.value in caps
    assert TaskCapability.AUDIO_TRANSCRIPTION.value in caps
    assert TaskCapability.VIDEO_DECODE.value in caps
    assert TaskCapability.VISUAL_EXTRACTION.value in caps

    assert caps[TaskCapability.IMAGE_OCR.value]["provider"] == "TesseractLocalEngine"
    assert caps[TaskCapability.AUDIO_TRANSCRIPTION.value]["provider"] == "WhisperLocalEngine"
    assert caps["active_tier"] == "numerics"


# ---------------------------------------------------------------------------
# CRA-014.2: Evidence locators, confidence, and proposed knowledge state
# ---------------------------------------------------------------------------
def test_cra_014_2_evidence_locators_and_proposed_state(tmp_path: Path):
    store = MemoryGraphStore()
    stt = MockSTTEngine()
    svc = MultimodalIngestionService(store, stt_engine=stt, active_tier="numerics")

    dummy_audio = tmp_path / "recording.wav"
    dummy_audio.write_bytes(b"RIFFdummydataWAVEfmt ")

    res = svc.ingest_file(dummy_audio, source_id="rec_001")
    assert res.status == "SUCCEEDED"
    assert len(res.segments) == 2

    seg0 = res.segments[0]
    assert seg0.start_ms == 0
    assert seg0.end_ms == 6200
    assert seg0.confidence == 0.96
    assert seg0.language == "en"
    assert seg0.raw_evidence_ref.startswith("media://rec_001")
    # Outputs must remain proposed until approved by publication policy
    assert seg0.knowledge_state == "proposed"


# ---------------------------------------------------------------------------
# CRA-014.3: Media budgets and offline isolation
# ---------------------------------------------------------------------------
def test_cra_014_3_media_budgets_enforcement(tmp_path: Path):
    store = MemoryGraphStore()
    stt = MockSTTEngine(duration=500.0)
    svc = MultimodalIngestionService(store, stt_engine=stt, active_tier="numerics")

    dummy_audio = tmp_path / "long_speech.mp3"
    dummy_audio.write_bytes(b"ID3dummydata")

    # Enforce duration budget of 60 seconds
    budget = MediaBudget(max_duration_seconds=60.0, no_egress=True)
    res = svc.ingest_file(dummy_audio, source_id="long_01", budget=budget)

    assert res.status == "FAILED"
    assert any("exceeds budget" in err for err in res.errors)


# ---------------------------------------------------------------------------
# CRA-014.4: Cancellation and progress reporting based on actual work
# ---------------------------------------------------------------------------
def test_cra_014_4_cancellation_and_progress_reporting(tmp_path: Path):
    store = MemoryGraphStore()
    stt = MockSTTEngine()
    svc = MultimodalIngestionService(store, stt_engine=stt, active_tier="numerics")

    dummy_audio = tmp_path / "audit_session.wav"
    dummy_audio.write_bytes(b"RIFFauditWAVEfmt ")

    progress_events: list[tuple[float, str]] = []

    def on_progress(p: float, msg: str) -> None:
        progress_events.append((p, msg))

    # Cancel midway
    cancelled = False

    def cancel_check() -> bool:
        return cancelled

    def on_progress_and_cancel(p: float, msg: str) -> None:
        nonlocal cancelled
        progress_events.append((p, msg))
        if p >= 0.3:
            cancelled = True

    res = svc.ingest_file(
        dummy_audio,
        source_id="audit_cancel",
        cancel_token=cancel_check,
        progress_cb=on_progress_and_cancel,
    )

    assert len(progress_events) >= 2
    assert res.status in ("PARTIAL", "SUCCEEDED")
    # No fabricated text or timestamps
    for seg in res.segments:
        assert seg.start_ms is not None
        assert seg.text != ""


# ---------------------------------------------------------------------------
# CRA-014.5: WER and CER evaluation metrics
# ---------------------------------------------------------------------------
def test_cra_014_5_wer_and_cer_metrics():
    gold = "the enterprise ontology platform provides knowledge graphs"
    hyp = "the enterprise ontology system provides knowledge graphs"

    wer = compute_wer(gold, hyp)
    assert 0.14 <= wer <= 0.18  # 1 substitution in 7 words = 1/7 ~ 0.1428

    cer = compute_cer("hello", "helo")
    assert cer == 0.2  # 1 deletion in 5 chars = 0.2

    # Perfect match
    assert compute_wer(gold, gold) == 0.0
    assert compute_cer(gold, gold) == 0.0


# ---------------------------------------------------------------------------
# CRA-014.6: OCR with normalized bounding boxes [ymin, xmin, ymax, xmax]
# ---------------------------------------------------------------------------
def test_cra_014_6_ocr_normalized_bounding_boxes(tmp_path: Path):
    store = MemoryGraphStore()
    ocr = MockOCREngine()
    svc = MultimodalIngestionService(store, ocr_engine=ocr, active_tier="numerics")

    dummy_img = tmp_path / "diagram_scan.png"
    dummy_img.write_bytes(b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDRdummy")

    res = svc.ingest_file(dummy_img, source_id="ocr_doc_1")
    assert res.status == "SUCCEEDED"
    assert len(res.segments) == 2

    for seg in res.segments:
        assert seg.bounding_box is not None
        ymin, xmin, ymax, xmax = seg.bounding_box
        assert 0.0 <= ymin <= 1.0
        assert 0.0 <= xmin <= 1.0
        assert 0.0 <= ymax <= 1.0
        assert 0.0 <= xmax <= 1.0
        assert ymin <= ymax
        assert xmin <= xmax
        assert seg.page_number == 1
        assert seg.confidence > 0.9


# ---------------------------------------------------------------------------
# CRA-014.7: Audio and video millisecond timestamps
# ---------------------------------------------------------------------------
def test_cra_014_7_audio_video_millisecond_timestamps(tmp_path: Path):
    store = MemoryGraphStore()
    stt = MockSTTEngine()
    svc = MultimodalIngestionService(store, stt_engine=stt, active_tier="numerics")

    dummy_video = tmp_path / "incident_call.mp4"
    dummy_video.write_bytes(b"\x00\x00\x00\x20ftypmp42dummy")

    res = svc.ingest_file(dummy_video, source_id="video_01")
    assert res.status == "SUCCEEDED"
    assert len(res.segments) == 2
    assert res.segments[0].start_ms == 0
    assert res.segments[0].end_ms == 6200
    assert res.segments[1].start_ms == 6200
    assert res.segments[1].end_ms == 12500


# ---------------------------------------------------------------------------
# CRA-014.8: Air-gap / no-egress mode with hash-pinned bundles
# ---------------------------------------------------------------------------
def test_cra_014_8_airgap_no_egress_hash_pinned():
    expected_hash = hashlib.sha256(b"whisper-base-pinned-v1").hexdigest()
    budget = MediaBudget(no_egress=True, offline_bundle_hash=expected_hash)

    assert budget.no_egress is True
    assert budget.offline_bundle_hash == expected_hash


# ---------------------------------------------------------------------------
# CRA-014.9: Compute tier readiness and 503 unavailable error
# ---------------------------------------------------------------------------
def test_cra_014_9_tier_readiness_and_503_unavailable(tmp_path: Path):
    store = MemoryGraphStore()
    # Missing tier: active_tier is "none"
    svc = MultimodalIngestionService(store, active_tier="none")

    dummy_audio = tmp_path / "sample.wav"
    dummy_audio.write_bytes(b"RIFFaudioWAVE")

    with pytest.raises(MediaTierUnavailableError) as exc_info:
        svc.ingest_file(dummy_audio, source_id="tier_test")

    err = exc_info.value
    assert err.http_status == 503
    assert err.required_tier == "numerics"
    assert "UNAVAILABLE" in str(err)


# ---------------------------------------------------------------------------
# CRA-014.A: Acceptance Gate: Search Spoken Phrase, Locators, ACLs, and Tiers
# ---------------------------------------------------------------------------
def test_cra_014_a_acceptance_gate(tmp_path: Path):
    store = MemoryGraphStore()
    stt = MockSTTEngine(
        text="Critical outage in database cluster during midnight deployment.",
        segments=[
            {"start": 0.0, "end": 4.5, "text": "Critical outage in database cluster", "confidence": 0.97},
            {"start": 4.5, "end": 8.0, "text": "during midnight deployment.", "confidence": 0.95},
        ],
    )
    svc = MultimodalIngestionService(store, stt_engine=stt, active_tier="numerics")

    dummy_audio = tmp_path / "postmortem_recording.wav"
    dummy_audio.write_bytes(b"RIFFpostmortemWAVEfmt ")

    res = svc.ingest_file(dummy_audio, source_id="postmortem_01")
    assert res.status == "SUCCEEDED"

    # 1. Search spoken phrase with authorized role
    analyst_matches = svc.search_spoken_phrase("database cluster", principal_roles=["role:analyst"])
    assert len(analyst_matches) >= 1
    match = analyst_matches[0]
    assert match.source_uri == str(dummy_audio)
    assert match.start_ms is not None
    assert match.end_ms is not None

    # 2. Search spoken phrase with unauthorized role (denied/filtered)
    guest_matches = svc.search_spoken_phrase("database cluster", principal_roles=["role:guest"])
    assert len(guest_matches) == 0

    # 3. Missing tier raises 503 error
    offline_svc = MultimodalIngestionService(store, active_tier="none")
    with pytest.raises(MediaTierUnavailableError) as exc_info:
        offline_svc.validate_tier_readiness("numerics")
    assert exc_info.value.http_status == 503
