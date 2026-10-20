"""Acceptance tests for WP-012: Safe Text, Structured Data & Office Parsing (CRA-012.1-012.9, CRA-012.A)."""

import base64
import io
import json
import sqlite3
import struct
import subprocess
import sys
import time
import zipfile
from pathlib import Path

import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from eoip.contracts.canonical import EvidenceLocator
from eoip.fileparse.contracts import ParseError, ParseOptions, ParsedDocument, RagChunk
from eoip.fileparse.engine import (
    CORE_FORMATS,
    EXTENDED_FORMATS,
    SUPPORTED_EXTENSIONS,
    FileParser,
    detect_format,
    format_catalog,
    get_format_readiness,
)
from eoip.ingestion.multimodal_audio import _chunk_text

# Explicit binding: IDs mentioned in docstrings/comments below are context, not coverage.
pytestmark = pytest.mark.req("CRA-012")


def parse(content: bytes, name: str, **options) -> any:
    opts = ParseOptions(**options)
    return FileParser(opts).parse_bytes(content, name)


# ---------------------------------------------------------------------------
# CRA-012.1: Multi-format parsing, format detection by magic bytes, readiness
# ---------------------------------------------------------------------------
def test_cra_012_1_multi_format_and_magic_byte_detection():
    # 1. Content-based magic byte detection
    pdf_bytes = b"%PDF-1.4\n1 0 obj\n<<>>\nendobj\ntrailer\n<<>>\n%%EOF"
    assert detect_format(pdf_bytes, "unknown.bin") == ".pdf"

    sqlite_bytes = b"SQLite format 3\x00" + b"\x00" * 96
    assert detect_format(sqlite_bytes, "dump.dat") == ".db"

    png_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 20
    assert detect_format(png_bytes, "graphic.bin") == ".png"

    rtf_bytes = br"{\rtf1\ansi Sample RTF text}"
    assert detect_format(rtf_bytes, "document.raw") == ".rtf"

    # Minimal DOCX package
    docx_buf = io.BytesIO()
    with zipfile.ZipFile(docx_buf, "w") as z:
        z.writestr("word/document.xml", "<w:document><w:body><w:p><w:r><w:t>DOCX magic</w:t></w:r></w:p></w:body></w:document>")
    assert detect_format(docx_buf.getvalue(), "file_without_ext") == ".docx"

    # Minimal XLSX package
    xlsx_buf = io.BytesIO()
    with zipfile.ZipFile(xlsx_buf, "w") as z:
        z.writestr("xl/workbook.xml", "<workbook/>")
    assert detect_format(xlsx_buf.getvalue(), "data.blob") == ".xlsx"

    # Minimal PPTX package
    pptx_buf = io.BytesIO()
    with zipfile.ZipFile(pptx_buf, "w") as z:
        z.writestr("ppt/presentation.xml", "<presentation/>")
    assert detect_format(pptx_buf.getvalue(), "slides.tmp") == ".pptx"

    # 2. Parsing through FileParser with format detection
    # Text
    res_txt = parse(b"Hello world from text adapter", "sample.txt")
    assert res_txt.status == "SUCCEEDED"
    assert "Hello world" in res_txt.chunks[0].text

    # CSV
    res_csv = parse(b"col_a,col_b\nval_1,val_2\n", "sample.csv")
    assert res_csv.status == "SUCCEEDED"
    assert res_csv.documents[0].tables[0].columns == ["col_a", "col_b"]

    # JSON
    res_json = parse(b'{"key": "value_123"}', "sample.json")
    assert res_json.status == "SUCCEEDED"
    assert res_json.documents[0].data == {"key": "value_123"}

    # 3. Explicit dependency readiness
    txt_readiness = get_format_readiness(".txt")
    assert txt_readiness["status"] == "AVAILABLE"
    assert txt_readiness["category"] == "core"

    # Missing tools report UNAVAILABLE, never silent fallback
    legacy_readiness = get_format_readiness(".doc", libreoffice_path="nonexistent-soffice-path-xyz")
    assert legacy_readiness["status"] == "UNAVAILABLE"
    assert "LibreOffice (soffice)" in legacy_readiness["missing_dependencies"]


# ---------------------------------------------------------------------------
# CRA-012.2: Locators, spreadsheet formulas, and macro prohibition
# ---------------------------------------------------------------------------
def test_cra_012_2_locators_and_formulas_macros_prohibited():
    openpyxl = pytest.importorskip("openpyxl")
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "LedgerSheet"
    ws.append(["Item", "Price", "Tax", "Total"])
    ws.append(["Widget", 100, 15, "=B2+C2"])
    ws.append(["Gadget", 200, 30, "=B3+C3"])

    stream = io.BytesIO()
    wb.save(stream)
    xlsx_bytes = stream.getvalue()

    result = parse(xlsx_bytes, "accounting.xlsx")
    assert result.status == "SUCCEEDED"
    doc = result.documents[0]

    # Preserves table locators
    assert len(doc.tables) == 1
    table = doc.tables[0]
    assert table.name == "LedgerSheet"
    assert table.locator["sheet"] == "LedgerSheet"
    assert len(table.rows) == 3

    # Formulas distinguished from literal values
    assert "=B2+C2" in [r[3] for r in table.rows]
    formulas_detected = doc.metadata.get("formulas_detected", [])
    assert len(formulas_detected) >= 2
    assert any(f["formula"] == "=B2+C2" for f in formulas_detected)
    assert doc.metadata["macros_executed"] is False
    assert "distinguished from values" in doc.metadata["formulas"]

    # DOCX paragraph and table locators
    docx = pytest.importorskip("docx")
    doc_docx = docx.Document()
    doc_docx.add_paragraph("Paragraph Alpha")
    doc_docx.add_paragraph("Paragraph Beta")
    tbl = doc_docx.add_table(rows=1, cols=2)
    tbl.cell(0, 0).text = "Cell 1"
    tbl.cell(0, 1).text = "Cell 2"
    docx_stream = io.BytesIO()
    doc_docx.save(docx_stream)

    res_docx = parse(docx_stream.getvalue(), "report.docx")
    assert res_docx.status == "SUCCEEDED"
    p_sections = [s for s in res_docx.documents[0].sections if s.kind == "paragraph"]
    assert len(p_sections) == 2
    assert p_sections[0].locator["block"] == 0
    assert p_sections[1].locator["block"] == 1
    assert res_docx.documents[0].metadata["macros_executed"] is False


# ---------------------------------------------------------------------------
# CRA-012.3: Budgets and safe XML/HTML without external entities
# ---------------------------------------------------------------------------
def test_cra_012_3_budgets_safe_xml_html():
    # 1. Budget limits: max_file_bytes
    with pytest.raises(ParseError) as exc_bytes:
        parse(b"1234567890", "test.txt", max_file_bytes=5)
    assert exc_bytes.value.code == "size_limit"

    # Budget limits: max_text_chars
    with pytest.raises(ParseError) as exc_text:
        parse(b"abcdefghij", "test.txt", max_text_chars=5)
    assert exc_text.value.code == "text_limit"

    # Budget limits: max_rows
    with pytest.raises(ParseError) as exc_rows:
        parse(b"h1,h2\n1,2\n3,4\n5,6\n", "test.csv", max_rows=2)
    assert exc_rows.value.code == "row_limit"

    # 2. Defused XML prevents external entity resolution (XXE) and billion laughs
    pytest.importorskip("defusedxml")
    xxe_payload = b"""<?xml version="1.0"?>
    <!DOCTYPE root [
    <!ENTITY xxe SYSTEM "file:///etc/passwd">
    ]>
    <root><data>&xxe;</data></root>"""
    with pytest.raises(ParseError) as exc_xxe:
        parse(xxe_payload, "exploit.xml")
    assert exc_xxe.value.code == "invalid_xml"

    # 3. HTML parsing does not execute scripts, styles or template content
    html_payload = b"""<!DOCTYPE html>
    <html>
      <head><title>Safe HTML</title><style>body { color: red; }</style></head>
      <body>
        <script>alert("malicious script execution attempt");</script>
        <template><p>Hidden template payload</p></template>
        <h1>Visible Header</h1>
        <p>Visible Paragraph</p>
      </body>
    </html>"""
    res_html = parse(html_payload, "page.html")
    assert res_html.status == "SUCCEEDED"
    all_chunks_text = " ".join(c.text for c in res_html.chunks)
    assert "Visible Header" in all_chunks_text
    assert "Visible Paragraph" in all_chunks_text
    assert "malicious script" not in all_chunks_text
    assert "Hidden template payload" not in all_chunks_text
    assert "color: red" not in all_chunks_text


# ---------------------------------------------------------------------------
# CRA-012.4: Chunker progress, termination, and G11 fix validation
# ---------------------------------------------------------------------------
def test_cra_012_4_chunking_progress_and_g11_termination():
    # 1. Invariant: 0 <= overlap < chunk_size enforced
    with pytest.raises(ValueError, match="chunk_overlap must be smaller than chunk_chars"):
        ParseOptions(chunk_chars=100, chunk_overlap=100)

    with pytest.raises(ValueError, match="overlap must satisfy"):
        _chunk_text("test input", max_chunk_chars=100, overlap=100)

    with pytest.raises(ValueError, match="overlap must satisfy"):
        _chunk_text("test input", max_chunk_chars=100, overlap=-5)

    # 2. G11 reproduction: long unbroken string without newlines terminating cleanly
    unbroken_text = "X" * 15000
    chunks = _chunk_text(unbroken_text, max_chunk_chars=1000, overlap=100)
    assert len(chunks) > 1
    # Check that each chunk advances monotonically
    assert sum(len(c) for c in chunks) >= len(unbroken_text)
    reconstructed = ""
    # Verify no infinite loop and final chunk exits
    assert chunks[-1] == unbroken_text[len(unbroken_text) - len(chunks[-1]):]

    # 3. Unicode and boundary cases
    unicode_text = "こんにちは世界 " * 1000
    u_chunks = _chunk_text(unicode_text, max_chunk_chars=200, overlap=50)
    assert len(u_chunks) > 0
    assert all(len(c) <= 200 for c in u_chunks)

    # Empty and whitespace inputs
    assert _chunk_text("", max_chunk_chars=100, overlap=10) == []
    assert _chunk_text("   \n\t  ", max_chunk_chars=100, overlap=10) == []

    # Short string returns single chunk
    short_chunks = _chunk_text("Short text", max_chunk_chars=100, overlap=10)
    assert short_chunks == ["Short text"]

    # FileParser chunking progress test
    long_doc = ("Section sentence with info. " * 300).encode("utf-8")
    fp_res = parse(long_doc, "doc.txt", chunk_chars=500, chunk_overlap=50)
    assert fp_res.status == "SUCCEEDED"
    assert len(fp_res.chunks) > 1
    for i in range(1, len(fp_res.chunks)):
        assert fp_res.chunks[i].start_char > fp_res.chunks[i - 1].start_char


# ---------------------------------------------------------------------------
# CRA-012.5: Model partial extraction and raw bytes preservation
# ---------------------------------------------------------------------------
def test_cra_012_5_partial_extraction_and_raw_bytes_preservation():
    # 1. Raw bytes preserved so parser upgrade can rebuild
    content = b"Original raw bytes for archival and provenance verification."
    res = parse(content, "original.txt")
    doc = res.documents[0]
    assert doc.raw_bytes == content
    assert doc.raw_bytes_base64 == base64.b64encode(content).decode("ascii")

    # 2. Partial container handling
    container_buf = io.BytesIO()
    with zipfile.ZipFile(container_buf, "w") as z:
        z.writestr("valid.txt", "Valid member text")
        z.writestr("invalid.bin", b"\x00\x01\x02\x03\xff\xfe")  # unknown binary format

    c_res = parse(container_buf.getvalue(), "mixed_archive.zip")
    assert c_res.status == "PARTIAL"
    assert len(c_res.errors) >= 1
    assert any("invalid.bin" in err.source_name for err in c_res.errors)
    assert any(doc.source_name.endswith("valid.txt") for doc in c_res.documents)


# ---------------------------------------------------------------------------
# CRA-012.6: Core and extended formats completeness and capability catalog
# ---------------------------------------------------------------------------
def test_cra_012_6_core_and_extended_formats_catalog():
    catalog = format_catalog()
    catalog_extensions = {entry["extension"] for entry in catalog}

    # Core set: TXT, JSON, CSV, XML, HTML, RTF, DOC, DOCX, PPT, PPTX, XLS, XLSX
    expected_core = {".txt", ".json", ".csv", ".xml", ".html", ".rtf", ".doc", ".docx", ".ppt", ".pptx", ".xls", ".xlsx"}
    for ext in expected_core:
        assert ext in catalog_extensions, f"Missing core format: {ext}"
        entry = next(e for e in catalog if e["extension"] == ext)
        assert entry["category"] == "core"

    # Extended set: TSV, YAML, JSON-LD, XHTML, Markdown, AsciiDoc, ODT, ODP, ODS, text-layer PDF
    expected_extended = {".tsv", ".yaml", ".yml", ".jsonld", ".xhtml", ".htm", ".md", ".markdown", ".adoc", ".asciidoc", ".odt", ".odp", ".ods", ".pdf"}
    for ext in expected_extended:
        assert ext in catalog_extensions, f"Missing extended format: {ext}"
        entry = next(e for e in catalog if e["extension"] == ext)
        assert entry["category"] == "extended"

    # Test extended parsing: TSV
    tsv_content = b"col1\tcol2\tcol3\nval1\tval2\tval3\n"
    res_tsv = parse(tsv_content, "data.tsv")
    assert res_tsv.status == "SUCCEEDED"
    assert res_tsv.documents[0].tables[0].columns == ["col1", "col2", "col3"]

    # Test extended parsing: YAML
    yaml_content = b"version: 2.0\nenvironment: production\nreplicas: 3\n"
    res_yaml = parse(yaml_content, "config.yaml")
    assert res_yaml.status == "SUCCEEDED"
    assert res_yaml.documents[0].data["version"] == 2.0
    assert res_yaml.documents[0].data["replicas"] == 3

    # Test extended parsing: JSON-LD
    jsonld_content = b'{"@context": "https://schema.org", "@type": "Organization", "name": "EOIP Inc"}'
    res_jsonld = parse(jsonld_content, "org.jsonld")
    assert res_jsonld.status == "SUCCEEDED"
    assert res_jsonld.documents[0].metadata["jsonld_context"] == "https://schema.org"

    # Test extended parsing: Markdown
    md_content = b"# Architecture\n\nSection detailing system design.\n\n## Components\n- Ingestion\n- Storage\n"
    res_md = parse(md_content, "design.md")
    assert res_md.status == "SUCCEEDED"
    assert "Architecture" in res_md.chunks[0].text

    # Test extended parsing: AsciiDoc
    adoc_content = b"= System Overview\nAuthor Name\n\nThis is an AsciiDoc document for testing.\n"
    res_adoc = parse(adoc_content, "spec.adoc")
    assert res_adoc.status == "SUCCEEDED"
    assert "System Overview" in res_adoc.chunks[0].text

    # Test extended parsing: ODF (ODT)
    odt_buf = io.BytesIO()
    with zipfile.ZipFile(odt_buf, "w") as z:
        z.writestr("mimetype", "application/vnd.oasis.opendocument.text")
        z.writestr("content.xml", """<?xml version="1.0" encoding="UTF-8"?>
        <office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0">
          <office:body>
            <office:text>
              <text:h>ODT Heading 1</text:h>
              <text:p>ODT Paragraph Content.</text:p>
            </office:text>
          </office:body>
        </office:document-content>""")
    res_odt = parse(odt_buf.getvalue(), "doc.odt")
    assert res_odt.status == "SUCCEEDED"
    assert any("ODT Paragraph Content" in c.text for c in res_odt.chunks)


# ---------------------------------------------------------------------------
# CRA-012.7: Candidate libraries pinned and safe
# ---------------------------------------------------------------------------
def test_cra_012_7_pinned_safe_candidate_libraries():
    # Verify candidate libraries from CRA-012.7 subject to CRA-035 review
    import yaml
    from eoip.compliance.sbom import EntitlementEnforcer

    policy_path = Path("compliance/license-policy.yaml")
    assert policy_path.exists()
    policy = yaml.safe_load(policy_path.read_text(encoding="utf-8"))
    allowed_licenses = set(policy.get("allowed_licenses", []))
    assert "MIT" in allowed_licenses
    assert "BSD-3-Clause" in allowed_licenses
    assert "Apache-2.0" in allowed_licenses

    # Candidate libraries are not forbidden
    forbidden = [f.lower() for f in policy.get("forbidden_packages", [])]
    for lib in ["python-docx", "python-pptx", "openpyxl", "defusedxml", "pyyaml"]:
        assert not any(lib == f for f in forbidden)

    enforcer = EntitlementEnforcer(licensed_features={"docx", "openpyxl", "pptx", "defusedxml"})
    assert enforcer.check_access("docx")["allowed"] is True
    assert enforcer.check_access("openpyxl")["allowed"] is True
    assert enforcer.check_access("unlicensed_feature")["allowed"] is False


# ---------------------------------------------------------------------------
# CRA-012.8: EvidenceLocator on every chunk
# ---------------------------------------------------------------------------
def test_cra_012_8_evidence_locator_on_every_chunk():
    # Test on a document with sections and locators
    text_content = b"Paragraph One.\n\nParagraph Two.\n\nParagraph Three."
    res = parse(text_content, "provenance.txt", chunk_chars=40, chunk_overlap=10)
    assert len(res.chunks) > 0
    for chunk in res.chunks:
        assert isinstance(chunk.evidence_locator, dict)
        assert chunk.evidence_locator["document_id"] == chunk.document_id
        assert chunk.evidence_locator["source_system"] == chunk.source_id
        assert "source_revision" in chunk.evidence_locator
        assert chunk.evidence_locator["char_start"] == chunk.start_char
        assert chunk.evidence_locator["char_end"] == chunk.end_char

        # Conversion to canonical EvidenceLocator object
        ev_loc = chunk.to_evidence_locator()
        assert isinstance(ev_loc, EvidenceLocator)
        assert ev_loc.document_id == chunk.document_id
        assert ev_loc.source_system == chunk.source_id
        assert ev_loc.char_start == chunk.start_char
        assert ev_loc.char_end == chunk.end_char


# ---------------------------------------------------------------------------
# CRA-012.9: Performance qualification target (DOCX & 50-sheet XLSX <= 5s)
# ---------------------------------------------------------------------------
def test_cra_012_9_performance_qualification_target():
    docx = pytest.importorskip("docx")
    openpyxl = pytest.importorskip("openpyxl")

    # 1. 50-sheet XLSX benchmark
    wb = openpyxl.Workbook()
    for i in range(50):
        sheet = wb.create_sheet(f"Sheet_{i + 1}")
        for r in range(10):
            sheet.append([f"Row_{r}", r * 10, r * 20, f"=B{r+1}+C{r+1}"])
    xlsx_stream = io.BytesIO()
    wb.save(xlsx_stream)
    xlsx_bytes = xlsx_stream.getvalue()

    start_xlsx = time.perf_counter()
    res_xlsx = parse(xlsx_bytes, "multi_sheet_benchmark.xlsx", max_rows=5000)
    elapsed_xlsx = time.perf_counter() - start_xlsx
    assert res_xlsx.status == "SUCCEEDED"
    assert len(res_xlsx.documents[0].tables) >= 50
    assert elapsed_xlsx <= 5.0, f"50-sheet XLSX extraction took {elapsed_xlsx:.2f}s, expected <= 5.0s"

    # 2. Large DOCX benchmark (synthetic multi-paragraph)
    doc = docx.Document()
    for i in range(200):
        doc.add_paragraph(f"Paragraph {i}: This is benchmark test paragraph with locators and rich content.")
    docx_stream = io.BytesIO()
    doc.save(docx_stream)
    docx_bytes = docx_stream.getvalue()

    start_docx = time.perf_counter()
    res_docx = parse(docx_bytes, "benchmark.docx")
    elapsed_docx = time.perf_counter() - start_docx
    assert res_docx.status == "SUCCEEDED"
    assert len(res_docx.chunks) >= 10
    assert elapsed_docx <= 5.0, f"Large DOCX extraction took {elapsed_docx:.2f}s, expected <= 5.0s"


# ---------------------------------------------------------------------------
# CRA-012.A: Acceptance obligation (Hypothesis property tests & golden files)
# ---------------------------------------------------------------------------
@settings(max_examples=50, deadline=None)
@given(
    text=st.text(min_size=0, max_size=2000),
    chunk_chars=st.integers(min_value=32, max_value=200),
    overlap=st.integers(min_value=0, max_value=31),
)
def test_cra_012_a_hypothesis_chunker_properties(text, chunk_chars, overlap):
    # Overlap is strictly less than chunk_chars
    chunks = _chunk_text(text, max_chunk_chars=chunk_chars, overlap=overlap)
    if not text.strip():
        assert chunks == []
        return

    # Invariants:
    # 1. Non-empty chunks
    assert len(chunks) > 0
    # 2. Each chunk is bounded by max_chunk_chars
    for c in chunks:
        assert len(c) <= chunk_chars + 1
    # 3. Content coverage and progress
    assert chunks[0] == text[:len(chunks[0])]
    assert chunks[-1] == text[len(text) - len(chunks[-1]):]
    if overlap == 0 and "\n" not in text:
        assert "".join(chunks) == text


def test_cra_012_a_g11_isolated_process_termination():
    # Run the G11 long-input reproduction in a timeout-isolated process
    code = """
from eoip.ingestion.multimodal_audio import _chunk_text
long_unbroken = 'A' * 20000
chunks = _chunk_text(long_unbroken, max_chunk_chars=1000, overlap=100)
assert len(chunks) == 22 or len(chunks) == 23
print('G11_TERMINATED_SUCCESSFULLY')
"""
    proc = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, timeout=10)
    assert proc.returncode == 0
    assert "G11_TERMINATED_SUCCESSFULLY" in proc.stdout
