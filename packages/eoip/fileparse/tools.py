"""Opt-in local conversion/OCR; no shell, network service or remote model."""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

from eoip.fileparse.contracts import ParseError, ParseOptions


def executable(configured: str | None, name: str) -> str:
    resolved = shutil.which(configured or name)
    if not resolved:
        raise ParseError("tool_unavailable", f"Local {name} executable is required; configure its path")
    return resolved


def run_tool(arguments: list[str], options: ParseOptions, directory: Path) -> None:
    try:
        # Tool diagnostics stay local, not in responses containing source text.
        with (directory / "tool.log").open("wb") as log:
            result = subprocess.run(
                arguments, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                timeout=options.tool_timeout_seconds, check=False, cwd=directory,
            )
    except subprocess.TimeoutExpired as exc:
        raise ParseError("tool_timeout", "Local conversion/OCR exceeded its execution timeout") from exc
    except OSError as exc:
        raise ParseError("tool_failed", "Cannot start the configured local conversion/OCR tool") from exc
    if result.returncode != 0:
        raise ParseError("tool_failed", f"Local conversion/OCR exited with code {result.returncode}")


def convert_legacy(content: bytes, suffix: str, options: ParseOptions) -> tuple[bytes, str]:
    tool = executable(options.libreoffice_path, "soffice")
    target = ".pptx" if suffix == ".ppt" else ".docx"
    with TemporaryDirectory(prefix="eoip-office-") as temporary:
        directory = Path(temporary)
        source = directory / f"input{suffix}"
        source.write_bytes(content)
        profile = (directory / "profile").as_uri()
        run_tool(
            [tool, f"-env:UserInstallation={profile}", "--headless", "--nologo", "--nodefault",
             "--norestore", "--convert-to", target[1:], "--outdir", str(directory), str(source)],
            options, directory,
        )
        destination = directory / f"input{target}"
        if not destination.is_file():
            raise ParseError("conversion_failed", "LibreOffice did not produce the requested modern Office file")
        if destination.stat().st_size > options.max_file_bytes:
            raise ParseError("size_limit", "Converted Office file exceeds max_file_bytes")
        return destination.read_bytes(), target


def image_ocr(png: bytes, options: ParseOptions) -> str:
    tool = executable(options.tesseract_path, "tesseract")
    with TemporaryDirectory(prefix="eoip-ocr-") as temporary:
        directory = Path(temporary)
        source = directory / "frame.png"
        source.write_bytes(png)
        run_tool(
            [tool, str(source), str(directory / "ocr"), "-l", options.ocr_language],
            options, directory,
        )
        output = directory / "ocr.txt"
        if not output.is_file():
            raise ParseError("ocr_failed", "Tesseract did not produce a text output")
        if output.stat().st_size > options.max_text_chars * 4:
            raise ParseError("text_limit", "OCR output exceeds configured text limits")
        return output.read_text(encoding="utf-8")
