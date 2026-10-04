"""python -m eoip.fileparse INPUT --output NEW_DIRECTORY [--ocr] [--vectors]."""

from __future__ import annotations

import argparse
import json
import logging
from pathlib import Path

from eoip.fileparse.contracts import ParseError, ParseOptions
from eoip.fileparse.engine import FileParser, format_catalog
from eoip.fileparse.export import export_bundle


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Convert actual local files into JSON and citation-aware RAG data")
    parser.add_argument("input", nargs="?", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--formats", action="store_true")
    parser.add_argument("--source-id", default="local_files")
    parser.add_argument("--encoding", default="utf-8")
    parser.add_argument("--ocr", action="store_true")
    parser.add_argument("--ocr-language", default="eng")
    parser.add_argument("--tesseract-path")
    parser.add_argument("--libreoffice-path")
    parser.add_argument("--vectors", action="store_true")
    parser.add_argument("--chunk-chars", type=int, default=1200)
    parser.add_argument("--chunk-overlap", type=int, default=150)
    args = parser.parse_args(argv)
    if args.formats:
        print(json.dumps(format_catalog(), indent=2))
        return 0
    if args.input is None or args.output is None:
        parser.error("input and --output are required unless --formats is used")
    logging.basicConfig(level=logging.WARNING)
    try:
        options = ParseOptions(
            encoding=args.encoding, ocr=args.ocr, ocr_language=args.ocr_language,
            tesseract_path=args.tesseract_path, libreoffice_path=args.libreoffice_path,
            chunk_chars=args.chunk_chars, chunk_overlap=args.chunk_overlap,
        )
        result = FileParser(options).parse_path(args.input, source_id=args.source_id)
        manifest = export_bundle(result, args.output, vectors=args.vectors)
        print(json.dumps(manifest, indent=2))
        return 0 if result.status == "SUCCEEDED" else 2
    except (ParseError, OSError, ValueError) as exc:
        print(json.dumps({"status": "FAILED", "code": getattr(exc, "code", "invalid_input"), "message": str(exc)}))
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
