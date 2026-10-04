"""Real format fixtures, extraction fidelity, limits and citation offsets."""

import hashlib
import io
import json
import sqlite3
import struct
import subprocess
import sys
import zipfile
from email.message import EmailMessage
from pathlib import Path

import pytest
from eoip.fileparse import FileParser
from eoip.fileparse.contracts import ParseError, ParseOptions


def parse(content, name, **options):
    return FileParser(ParseOptions(**options)).parse_bytes(content, name)


@pytest.mark.parametrize("name,content,expected", [
    ("sample.txt", "Actual caf\u00e9".encode(), "Actual caf\u00e9"),
    ("sample.txt", "Actual UTF16".encode("utf-16"), "Actual UTF16"),
    ("sample.txt", b"\xef\xbb\xbfActual BOM", "Actual BOM"),
    ("sample.csv", b'name,value\n"actual, row",42\n', "actual, row"),
    ("sample.json", b'{"actual": [42, true, null]}', "actual"),
    ("sample.html", b'<title>Actual</title><script>secret()</script><p>Visible</p>', "Visible"),
    ("sample.htm", b"<p>Visible</p>", "Visible"),
    ("sample.xhtml", b"<html><body><p>Visible</p></body></html>", "Visible"),
    ("sample.xml", b"<root><item>Actual XML</item>tail</root>", "Actual XML"),
    ("sample.rtf", br"{\rtf1\ansi Actual RTF\par next}", "Actual RTF"),
])
def test_actual_text_formats(name, content, expected):
    if name.endswith(".xml"):
        pytest.importorskip("defusedxml")
    if name.endswith(".rtf"):
        pytest.importorskip("striprtf")
    result = parse(content, name)
    assert result.status == "SUCCEEDED"
    assert expected in "\n".join(chunk.text for chunk in result.chunks)
    assert "secret()" not in "\n".join(chunk.text for chunk in result.chunks)
    assert json.loads(FileParser.to_json(result))["schema_version"] == "1.0"


@pytest.mark.parametrize("content,name,code", [
    (b"\x00\x01", "bad.txt", "invalid_text"),
    (b"\xff", "bad.txt", "invalid_encoding"),
    (b'{"a":NaN}', "bad.json", "invalid_format"),
    (b'{"a":1e999}', "bad.json", "invalid_format"),
    (b'a,b\n1\n', "bad.csv", "invalid_csv"),
    (b'a\n"unterminated', "bad.csv", "invalid_csv"),
    pytest.param(b'a\n' + b'z' * 140000, "large.csv", "invalid_csv", id="oversized-csv-field"),
    (b"not rtf", "bad.rtf", "invalid_format"),
    (b"not sqlite", "bad.db", "unsupported_database"),
    (b"unsupported", "bad.pdf", "unsupported_format"),
])
def test_invalid_inputs_have_explicit_errors(content, name, code):
    with pytest.raises(ParseError) as exc:
        parse(content, name)
    assert exc.value.code == code


def test_xml_entity_and_malformed_xml_are_rejected():
    pytest.importorskip("defusedxml")
    for content in (b"<root>", b'<!DOCTYPE r [<!ENTITY x "secret">]><r>&x;</r>'):
        with pytest.raises(ParseError, match="XML"):
            parse(content, "bad.xml")


def test_chunks_cover_exact_text_and_have_stable_provenance():
    text = "0123456789 " * 30
    result = parse(text.encode(), "body.txt", chunk_chars=64, chunk_overlap=12)
    again = parse(text.encode(), "body.txt", chunk_chars=64, chunk_overlap=12)
    assert result == again
    covered = set()
    for chunk in result.chunks:
        assert chunk.text == text[chunk.start_char:chunk.end_char]
        assert len(chunk.text) <= 64
        assert chunk.citations == [
            f"{chunk.source_uri}#section={chunk.section_index}&chars={chunk.start_char}:{chunk.end_char}"
        ]
        covered.update(range(chunk.start_char, chunk.end_char))
    assert covered == set(range(len(text)))
    assert result.chunks[1].start_char == 52
    assert parse(b"different", "body.txt").documents[0].document_id != result.documents[0].document_id


@pytest.mark.parametrize("options", [
    {"max_file_bytes": 3}, {"max_expanded_bytes": 3}, {"max_text_chars": 3},
])
def test_byte_and_text_limits(options):
    with pytest.raises(ParseError) as exc:
        parse(b"actual input", "body.txt", **options)
    assert exc.value.code.endswith("_limit")


def test_real_docx_paragraphs_tables_headers():
    docx = pytest.importorskip("docx")
    document = docx.Document()
    document.add_paragraph("Actual paragraph")
    table = document.add_table(rows=1, cols=2)
    table.cell(0, 0).text, table.cell(0, 1).text = "actual cell", "42"
    document.sections[0].header.paragraphs[0].text = "actual header"
    stream = io.BytesIO()
    document.save(stream)
    result = parse(stream.getvalue(), "actual.docx")
    assert result.documents[0].tables[0].rows == [["actual cell", "42"]]
    assert any(chunk.text == "Actual paragraph" for chunk in result.chunks)
    assert any(chunk.locator == {"section": 0} and chunk.text == "actual header" for chunk in result.chunks)


def test_real_xlsx_preserves_formulas_and_aggregate_row_limit():
    openpyxl = pytest.importorskip("openpyxl")
    workbook = openpyxl.Workbook()
    workbook.active.append(["actual spreadsheet", "=1+2"])
    workbook.create_sheet("Second").append([42, True])
    stream = io.BytesIO()
    workbook.save(stream)
    result = parse(stream.getvalue(), "actual.xlsx")
    assert result.documents[0].tables[0].rows == [["actual spreadsheet", "=1+2"]]
    assert result.documents[0].tables[1].rows == [[42, True]]
    with pytest.raises(ParseError) as exc:
        parse(stream.getvalue(), "actual.xlsx", max_rows=1)
    assert exc.value.code == "row_limit"


def test_actual_biff2_xls_records():
    pytest.importorskip("xlrd")

    def record(code, data):
        return struct.pack("<HH", code, len(data)) + data

    # A minimal original BIFF2 worksheet: BOF, CODEPAGE, LABEL, EOF.
    content = (
        record(9, struct.pack("<HH", 2, 16))
        + record(0x42, struct.pack("<H", 1252))
        + record(4, struct.pack("<HH", 0, 0) + b"\x00\x00\x00\x0bactual cell")
        + record(10, b"")
    )
    assert parse(content, "actual.xls").documents[0].tables[0].rows == [["actual cell"]]


def test_real_pptx_slide_and_notes():
    pptx = pytest.importorskip("pptx")
    presentation = pptx.Presentation()
    slide = presentation.slides.add_slide(presentation.slide_layouts[1])
    slide.shapes.title.text = "Actual slide"
    slide.notes_slide.notes_text_frame.text = "Actual speaker notes"
    stream = io.BytesIO()
    presentation.save(stream)
    result = parse(stream.getvalue(), "actual.pptx")
    assert any(chunk.text == "Actual slide" and chunk.locator["slide"] == 1 for chunk in result.chunks)
    assert any(chunk.text == "Actual speaker notes" for chunk in result.chunks)


def test_real_sqlite_blob_and_read_only_extraction(tmp_path):
    path = tmp_path / "actual.db"
    with sqlite3.connect(path) as connection:
        connection.execute("CREATE TABLE sample (text TEXT, blob BLOB)")
        connection.execute("INSERT INTO sample VALUES (?, ?)", ("actual sqlite", b"\x00\xff"))
    before = path.read_bytes()
    result = FileParser().parse_path(path)
    assert path.read_bytes() == before
    assert result.documents[0].tables[0].rows == [
        ["actual sqlite", {"type": "blob", "encoding": "base64", "value": "AP8="}]
    ]


@pytest.mark.parametrize("suffix,format_name", [
    ("jpg", "JPEG"), ("jpeg", "JPEG"), ("png", "PNG"), ("gif", "GIF"),
    ("tif", "TIFF"), ("tiff", "TIFF"), ("bmp", "BMP"), ("webp", "WEBP"),
])
def test_actual_images_are_decoded_without_inventing_visual_text(suffix, format_name):
    image = pytest.importorskip("PIL.Image")
    stream = io.BytesIO()
    image.new("RGB", (8, 6), color="white").save(stream, format=format_name)
    result = parse(stream.getvalue(), f"image.{suffix}")
    assert result.documents[0].metadata["width"] == 8
    assert result.documents[0].metadata["height"] == 6
    assert result.documents[0].metadata["frames"] == 1
    assert result.chunks == []
    assert result.documents[0].warnings
    with pytest.raises(ParseError) as exc:
        parse(stream.getvalue(), f"image.{suffix}", max_image_pixels=40)
    assert exc.value.code == "image_limit"


def test_actual_email_body_attachment_and_headers():
    message = EmailMessage()
    message["Subject"] = "Actual mail"
    message["From"] = "sender@example.invalid"
    message.set_content("Actual email body")
    message.add_attachment(b"Actual attachment", maintype="text", subtype="plain", filename="attachment.txt")
    result = parse(message.as_bytes(), "message.eml")
    assert len(result.documents) == 2
    parent = next(doc for doc in result.documents if doc.format == "eml")
    child = next(doc for doc in result.documents if doc.format == "txt")
    assert child.parent_id == parent.document_id
    assert parent.title == "Actual mail"
    assert any("Actual email body" in chunk.text for chunk in result.chunks)
    assert any(chunk.text == "Actual attachment" for chunk in result.chunks)


def test_actual_original_outlook_compound_file():
    pytest.importorskip("extract_msg")
    free, end, fat_sector = 0xFFFFFFFF, 0xFFFFFFFE, 0xFFFFFFFD
    header = (
        bytes.fromhex("d0cf11e0a1b11ae1") + bytes(16)
        + struct.pack("<HHHHH", 62, 3, 0xFFFE, 9, 6) + bytes(6)
        + struct.pack("<9I", 0, 1, 1, 0, 4096, 3, 1, end, 0)
        + struct.pack("<109I", 0, *([free] * 108))
    )

    def directory_entry(name, kind, *, left=free, right=free, child=free, start=end, size=0):
        label = (name + "\0").encode("utf-16le")
        return struct.pack(
            "<64sHBBIII16sIQQIQ", label, len(label), kind, 1, left, right, child,
            bytes(16), 0, 0, 0, start, size,
        )

    subject = "Actual MSG subject".encode("utf-16le")
    body = "Actual MSG body".encode("utf-16le")
    properties = (
        bytes(32) + struct.pack("<4I", 0x340D0003, 6, 0x40000, 0)
        + struct.pack("<4I", 0x0037001F, 6, len(subject) + 2, 0)
        + struct.pack("<4I", 0x1000001F, 6, len(body) + 2, 0)
    )
    # Original CFB v3 with FAT, directory, mini-stream and mini-FAT sectors.
    directory = (
        directory_entry("Root Entry", 5, child=2, start=2, size=256)
        + directory_entry("__properties_version1.0", 2, start=2, size=len(properties))
        + directory_entry("__substg1.0_0037001F", 2, left=1, right=3, start=0, size=len(subject))
        + directory_entry("__substg1.0_1000001F", 2, start=1, size=len(body))
    )
    fat = struct.pack("<128I", fat_sector, end, end, end, *([free] * 124))
    mini_fat = struct.pack("<128I", end, end, 3, end, *([free] * 124))
    mini_stream = (
        subject.ljust(64, b"\0") + body.ljust(64, b"\0") + properties.ljust(128, b"\0")
    ).ljust(512, b"\0")
    result = parse(header + fat + directory + mini_stream + mini_fat, "original.msg")
    assert result.documents[0].title == "Actual MSG subject"
    assert result.documents[0].metadata["date"] is None
    assert [chunk.text for chunk in result.chunks] == ["Actual MSG body"]


@pytest.mark.parametrize("extension,part", [
    ("docx", "word/document.xml"),
    ("xlsx", "xl/worksheets/sheet1.xml"),
    ("pptx", "ppt/presentation.xml"),
])
def test_malformed_office_xml_is_normalized(extension, part):
    buffer = io.BytesIO()
    if extension == "docx":
        pytest.importorskip("docx").Document().save(buffer)
    elif extension == "xlsx":
        pytest.importorskip("openpyxl").Workbook().save(buffer)
    else:
        pytest.importorskip("pptx").Presentation().save(buffer)
    malformed = io.BytesIO()
    with zipfile.ZipFile(buffer) as original, zipfile.ZipFile(malformed, "w") as archive:
        for entry in original.infolist():
            archive.writestr(entry.filename, b"<broken" if entry.filename == part else original.read(entry))
    with pytest.raises(ParseError) as failure:
        parse(malformed.getvalue(), f"malformed.{extension}")
    assert failure.value.code == "invalid_format"


@pytest.mark.parametrize("case,exit_code,status", [
    ("success", 0, "SUCCEEDED"),
    ("invalid", 1, "FAILED"),
    ("partial", 2, "PARTIAL"),
    ("failed-container", 2, "FAILED"),
])
def test_cli_persistent_outputs_and_exit_codes(tmp_path, case, exit_code, status):
    source = tmp_path / ("input.zip" if case in {"partial", "failed-container"} else "input.txt")
    if source.suffix == ".zip":
        with zipfile.ZipFile(source, "w") as archive:
            archive.writestr("unsupported.bin", b"binary")
            if case == "partial":
                archive.writestr("actual.txt", "Actual CLI extraction")
    else:
        source.write_bytes(b"\xff" if case == "invalid" else b"Actual CLI extraction")
    destination = tmp_path / "bundle"
    command = [sys.executable, "-m", "eoip.fileparse", str(source), "--output", str(destination), "--vectors"]
    process = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    assert process.returncode == exit_code, process.stderr
    assert json.loads(process.stdout)["status"] == status
    if case == "invalid":
        assert not destination.exists()
        return
    manifest = destination / "manifest.json"
    original_manifest = manifest.read_bytes()
    exported = json.loads((destination / "parsed.json").read_text(encoding="utf-8"))
    assert exported["status"] == status
    assert (destination / "vectors.jsonl").is_file()
    assert len(list((destination / "documents").glob("*.json"))) == len(exported["documents"])
    for name, digest in json.loads(original_manifest)["files"].items():
        assert hashlib.sha256((destination / name).read_bytes()).hexdigest() == digest
    duplicate = subprocess.run(command, capture_output=True, text=True, timeout=30, check=False)
    assert duplicate.returncode == 1
    assert manifest.read_bytes() == original_manifest


@pytest.mark.parametrize("suffix", ["doc", "ppt", "wps", "wpd"])
def test_missing_legacy_tool_is_explicit(suffix):
    with pytest.raises(ParseError) as exc:
        parse(b"binary content", f"actual.{suffix}", libreoffice_path="eoip-nonexistent-soffice")
    assert exc.value.code == "tool_unavailable"


@pytest.mark.parametrize("name", ["bad.xls", "bad.msg"])
def test_corrupt_binary_library_errors_are_normalized(name):
    pytest.importorskip("xlrd" if name.endswith(".xls") else "extract_msg")
    with pytest.raises(ParseError) as exc:
        parse(b"not binary Office data", name)
    assert exc.value.code in {"invalid_format", "invalid_email"}


def test_live_sqlite_wal_requires_consistent_snapshot(tmp_path):
    path = tmp_path / "live.db"
    with sqlite3.connect(path) as connection:
        connection.execute("PRAGMA journal_mode=WAL")
        connection.execute("CREATE TABLE sample (text TEXT)")
        connection.execute("INSERT INTO sample VALUES ('not yet checkpointed')")
        connection.commit()
        with pytest.raises(ParseError, match="consistent backup"):
            FileParser().parse_path(path)


@pytest.mark.parametrize("suffix", ["doc", "ppt", "wps", "wpd"])
def test_legacy_adapter_decodes_real_converted_output_with_mocked_tool(suffix, monkeypatch):
    from eoip.fileparse import tools

    stream = io.BytesIO()
    if suffix == "ppt":
        pptx = pytest.importorskip("pptx")
        document = pptx.Presentation()
        document.slides.add_slide(document.slide_layouts[1]).shapes.title.text = "Converted actual text"
    else:
        docx = pytest.importorskip("docx")
        document = docx.Document()
        document.add_paragraph("Converted actual text")
    document.save(stream)
    monkeypatch.setattr(tools, "executable", lambda *_: "mock-soffice")

    def convert(arguments, options, directory):
        assert "--headless" in arguments
        assert (directory / f"input.{suffix}").read_bytes() == b"original binary bytes"
        target = "pptx" if suffix == "ppt" else "docx"
        (directory / f"input.{target}").write_bytes(stream.getvalue())

    monkeypatch.setattr(tools, "run_tool", convert)
    result = parse(b"original binary bytes", f"input.{suffix}")
    assert any(chunk.text == "Converted actual text" for chunk in result.chunks)
    assert result.documents[0].content_hash != hashlib.sha256(stream.getvalue()).hexdigest()
    assert result.documents[0].metadata["conversion_tool"] == "LibreOffice"


def test_ocr_adapter_real_png_with_mocked_tool_output(monkeypatch):
    from eoip.fileparse import tools

    image = pytest.importorskip("PIL.Image")
    stream = io.BytesIO()
    image.new("RGB", (8, 6), color="white").save(stream, format="PNG")
    monkeypatch.setattr(tools, "executable", lambda *_: "mock-tesseract")

    def recognize(arguments, options, directory):
        assert Path(arguments[1]).read_bytes().startswith(b"\x89PNG")
        (directory / "ocr.txt").write_text("Recognized local text", encoding="utf-8")

    monkeypatch.setattr(tools, "run_tool", recognize)
    result = parse(stream.getvalue(), "actual.png", ocr=True)
    assert result.chunks[0].text == "Recognized local text"
    assert result.chunks[0].locator == {"frame": 1, "method": "tesseract"}


@pytest.mark.parametrize("failure,code", [
    ("timeout", "tool_timeout"), ("nonzero", "tool_failed"), ("launch", "tool_failed"),
])
def test_local_tool_failures_are_explicit(tmp_path, monkeypatch, failure, code):
    from eoip.fileparse import tools

    def run(*args, **kwargs):
        assert kwargs["timeout"] == 60
        if failure == "timeout":
            raise subprocess.TimeoutExpired("local-tool", 60)
        if failure == "launch":
            raise OSError("cannot start")
        return subprocess.CompletedProcess(args[0], 7)

    monkeypatch.setattr(tools.subprocess, "run", run)
    with pytest.raises(ParseError) as exc:
        tools.run_tool(["local-tool"], ParseOptions(), tmp_path)
    assert exc.value.code == code
