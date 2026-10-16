"""Optional OpenTelemetry tracing integration (G2-SRC-OTEL-LIB).

Instruments a FastAPI application and exports spans to an OTLP endpoint taken
from ``EOIP_OTEL_ENDPOINT`` (OTLP/HTTP preferred so no gRPC dependency is
required). Every span is enriched with the inbound ``X-Correlation-ID`` header
so traces line up with the platform's audit/correlation logs.

The module is a documented no-op when the optional ``opentelemetry-sdk`` (and
friends) are not installed: :func:`setup_tracing` logs a one-line warning and
returns ``False`` so callers can treat tracing as strictly best-effort.
"""

from __future__ import annotations

import logging
import os
from typing import Any

logger = logging.getLogger(__name__)

CORRELATION_HEADER = "x-correlation-id"
_warned = False


def _import_otel() -> dict[str, Any] | None:
    """Import the optional OpenTelemetry stack lazily; None when absent."""
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        return None
    try:  # instrumentation is a separate distribution; degrade without it
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except ImportError:
        FastAPIInstrumentor = None
    return {
        "trace": trace,
        "OTLPSpanExporter": OTLPSpanExporter,
        "TracerProvider": TracerProvider,
        "BatchSpanProcessor": BatchSpanProcessor,
        "FastAPIInstrumentor": FastAPIInstrumentor,
    }


def otel_available() -> bool:
    return _import_otel() is not None


def _correlation_id_middleware(trace_module: Any):
    async def middleware(request, call_next):
        correlation_id = request.headers.get(CORRELATION_HEADER)
        if correlation_id:
            span = trace_module.get_current_span()
            if span is not None and span.is_recording():
                span.set_attribute("eoip.correlation_id", correlation_id)
        return await call_next(request)

    return middleware


def setup_tracing(app: Any, service_name: str, *, endpoint: str | None = None) -> bool:
    """Instrument ``app`` (FastAPI) with OTLP tracing; no-op without the extra.

    Returns ``True`` when tracing was configured, ``False`` otherwise.
    (G2-SRC-OTEL-LIB)
    """
    global _warned
    otel = _import_otel()
    if otel is None:
        if not _warned:
            logger.warning(
                "OpenTelemetry not installed; tracing disabled "
                "(pip install eoip[otel] to enable, G2-SRC-OTEL-LIB)"
            )
            _warned = True
        return False

    endpoint = endpoint or os.environ.get("EOIP_OTEL_ENDPOINT")
    provider = otel["TracerProvider"]()
    if endpoint:
        exporter = otel["OTLPSpanExporter"](endpoint=endpoint)
        provider.add_span_processor(otel["BatchSpanProcessor"](exporter))
    otel["trace"].set_tracer_provider(provider)

    instrumentor = otel["FastAPIInstrumentor"]
    if instrumentor is not None:
        instrumentor.instrument_app(app)
    app.middleware("http")(_correlation_id_middleware(otel["trace"]))
    return True


def get_tracer(name: str) -> Any:
    """Return a named tracer, or a recording-free null object when OTel is absent."""
    otel = _import_otel()
    if otel is None:
        class _NoopTracer:
            def start_span(self, *_args, **_kwargs):
                return None

            def start_as_current_span(self, *_args, **_kwargs):
                from contextlib import nullcontext

                return nullcontext()

        return _NoopTracer()
    return otel["trace"].get_tracer(name)
