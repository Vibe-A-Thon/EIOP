"""Unit tests for Model Runtime Truthfulness (CP-19).

Verifies:
- Explicit simulation mode labeling on SelfLLMEngine (is_simulation=True, execution_mode="simulation")
- Progressive streaming emission without blocking
- Provider delegation when a live model provider is available (is_simulation=False, execution_mode="live")
- Resilient fallback to deterministic simulation when provider errors
"""

from __future__ import annotations

from unittest.mock import MagicMock

from eoip.models.provider import ModelResponse
from eoip.models.self_llm import SelfLLMEngine


def test_self_llm_simulation_mode_truthfulness():
    engine = SelfLLMEngine()
    assert engine.is_simulation is True

    res = engine.generate("Explain the graph schema")
    assert res.content
    assert res.metadata.get("is_simulation") is True
    assert res.metadata.get("execution_mode") == "simulation"

    # Streaming chunks must expose simulation status and progress
    chunks = list(engine.generate_stream("Explain the graph schema"))
    assert len(chunks) > 0
    assert chunks[0].usage.get("is_simulation") is True
    assert chunks[0].usage.get("execution_mode") == "simulation"
    assert chunks[-1].is_final is True
    assert " ".join(c.delta.strip() for c in chunks) == chunks[-1].accumulated_content


def test_self_llm_live_provider_delegation():
    mock_provider = MagicMock()
    mock_provider.available = True
    mock_provider.model_name = "llama3:8b"
    mock_provider.generate.return_value = ModelResponse(
        content="Grounded answer from live local model.",
        model="llama3:8b",
        generation="local_model",
        tokens_used=12,
    )

    engine = SelfLLMEngine(provider=mock_provider)
    assert engine.is_simulation is False

    res = engine.generate("What services depend on the payment db?")
    assert res.content == "Grounded answer from live local model."
    assert res.metadata.get("is_simulation") is False
    assert res.metadata.get("execution_mode") == "live"
    assert res.metadata.get("provider_model") == "llama3:8b"
    mock_provider.generate.assert_called_once()


def test_self_llm_provider_fallback_to_simulation():
    mock_provider = MagicMock()
    mock_provider.available = True
    mock_provider.model_name = "flaky-model"
    mock_provider.generate.side_effect = RuntimeError("Connection refused to inference server")

    engine = SelfLLMEngine(provider=mock_provider)
    # When provider fails, engine falls back to simulation mode
    res = engine.generate("Analyze topology")
    assert res.content
    assert res.metadata.get("is_simulation") is True
    assert res.metadata.get("execution_mode") == "simulation"
