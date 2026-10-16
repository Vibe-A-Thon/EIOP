"""Ingestion-side analysis helpers (schema profiling, key and relationship discovery).

SR-ING-010/012/013/016: deterministic, LLM-free analysis of JSON payloads that
feeds the ingestion pipeline stage 6 (profiling & schema inference) and stage 9
(key & relationship discovery). Pure stdlib + pydantic; no I/O.
"""
