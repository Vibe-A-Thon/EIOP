"""Real recursive archives, member rejection and atomic artifact persistence."""

import gzip
import hashlib
import io
import json
import math
import stat
import struct
import tarfile
import zipfile
import zlib

import pytest
from eoip.fileparse import FileParser
from eoip.fileparse.contracts import ParseError, ParseOptions
from eoip.fileparse.export import export_bundle


def zip_bytes(members):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for name, content in members:
            archive.writestr(name, content)
    return stream.getvalue()


def tar_bytes():
    stream = io.BytesIO()
    with tarfile.open(fileobj=stream, mode="w") as archive:
        content = b"actual tar member"
        item = tarfile.TarInfo("folder/body.txt")
        item.size = len(content)
        archive.addfile(item, io.BytesIO(content))
    return stream.getvalue()


@pytest.mark.parametrize("name,content", [
    ("actual.zip", zip_bytes([("folder/body.txt", b"actual zip member")])),
    ("actual.tar", tar_bytes()),
    ("actual.tar.gz", gzip.compress(tar_bytes())),
    ("actual.tgz", gzip.compress(tar_bytes())),
    ("actual.txt.gz", gzip.compress(b"actual gzip member")),
], ids=["zip", "tar", "tar-gzip", "tgz", "gzip"])
def test_actual_archives_retain_nested_provenance(name, content):
    result = FileParser().parse_bytes(content, name)
    assert result.status == "SUCCEEDED"
    assert len(result.chunks) == 1
    assert "actual" in result.chunks[0].text
    assert "!/" in result.chunks[0].source_uri
    identities = {document.document_id for document in result.documents}
    assert all(document.parent_id in identities for document in result.documents if document.parent_id)


def test_actual_7z_memory_extraction():
    py7zr = pytest.importorskip("py7zr")
    stream = io.BytesIO()
    with py7zr.SevenZipFile(stream, "w") as archive:
        archive.writestr(b"actual seven zip", "folder/body.txt")
    result = FileParser().parse_bytes(stream.getvalue(), "actual.7z")
    assert result.chunks[0].text == "actual seven zip"


def test_actual_original_stored_rar_without_external_tool():
    pytest.importorskip("rarfile")

    def header(payload):
        return struct.pack("<H", zlib.crc32(payload) & 0xFFFF) + payload

    name, data = b"body.txt", b"Actual original RAR member"
    main = header(struct.pack("<BHHHI", 0x73, 0, 13, 0, 0))
    file_header = header(struct.pack(
        "<BHHIIBIIBBHI", 0x74, 0x8000, 32 + len(name), len(data), len(data),
        3, zlib.crc32(data), 0, 20, 0x30, len(name), 0x20,
    ) + name)
    end = header(struct.pack("<BHH", 0x7B, 0, 7))
    result = FileParser().parse_bytes(b"Rar!\x1a\x07\x00" + main + file_header + data + end, "original.rar")
    assert result.status == "SUCCEEDED"
    assert result.chunks[0].text == data.decode()


@pytest.mark.parametrize("name", ["../escape.txt", "/absolute.txt", "C:\\escape.txt", "a/../b.txt"])
def test_archive_paths_never_escape(name):
    with pytest.raises(ParseError) as exc:
        FileParser().parse_bytes(zip_bytes([(name, b"bad")]), "unsafe.zip")
    assert exc.value.code == "unsafe_member"


def test_duplicate_and_symlink_members_rejected():
    with pytest.warns(UserWarning, match="Duplicate"):
        duplicate = zip_bytes([("a.txt", b"one"), ("a.txt", b"two")])
    with pytest.raises(ParseError) as exc:
        FileParser().parse_bytes(duplicate, "duplicate.zip")
    assert exc.value.code == "duplicate_member"
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w") as archive:
        link = zipfile.ZipInfo("link.txt")
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        archive.writestr(link, b"target")
    with pytest.raises(ParseError) as exc:
        FileParser().parse_bytes(stream.getvalue(), "link.zip")
    assert exc.value.code == "unsafe_member"


def test_partial_members_and_failed_containers_remain_explicit():
    result = FileParser().parse_bytes(
        zip_bytes([("good.txt", b"actual content"), ("bad.bin", b"bad")]), "partial.zip"
    )
    assert result.status == "PARTIAL"
    assert result.errors[0].code == "unsupported_format"
    assert result.chunks[0].text == "actual content"
    result = FileParser().parse_bytes(zip_bytes([("bad.bin", b"bad")]), "failed.zip")
    assert result.status == "FAILED"
    assert not result.chunks


def test_failed_nested_email_rolls_back_earlier_attachments():
    email = (
        b"Subject: Actual message\r\nContent-Type: multipart/mixed; boundary=x\r\n\r\n"
        b"--x\r\nContent-Type: text/plain\r\n"
        b"Content-Disposition: attachment; filename=child.txt\r\n\r\nnested content\r\n"
        b"--x\r\nContent-Type: text/plain; charset=unknown-charset\r\n\r\nbad\r\n--x--\r\n"
    )
    result = FileParser().parse_bytes(zip_bytes([("bad.eml", email), ("good.txt", b"good")]), "actual.zip")
    assert result.status == "PARTIAL"
    assert {doc.source_name for doc in result.documents} == {"actual.zip", "good.txt"}
    assert [chunk.text for chunk in result.chunks] == ["good"]
    assert result.errors[0].code == "invalid_encoding"


@pytest.mark.parametrize("options,code", [
    ({"max_members": 1}, "member_limit"),
    ({"max_depth": 0}, "depth_limit"),
    ({"max_expanded_bytes": 10}, "size_limit"),
    ({"max_text_chars": 8}, "text_limit"),
    ({"max_sections": 1}, "sections_limit"),
    ({"max_rows": 1}, "rows_limit"),
])
def test_global_container_budgets(options, code):
    content = zip_bytes([("a.csv", b"a\n1234\n"), ("b.csv", b"b\n5678\n")])
    with pytest.raises(ParseError) as exc:
        FileParser(ParseOptions(**options)).parse_bytes(content, "limits.zip")
    assert exc.value.code == code


@pytest.mark.parametrize("name", ["broken.zip", "broken.tar", "broken.gz", "broken.7z", "broken.rar"])
def test_corrupt_archive_has_parser_error(name):
    if name.endswith(".7z"):
        pytest.importorskip("py7zr")
    if name.endswith(".rar"):
        pytest.importorskip("rarfile")
    with pytest.raises(ParseError):
        FileParser().parse_bytes(b"not an archive", name)


def test_atomic_bundle_json_checksums_and_vectors(tmp_path):
    result = FileParser().parse_bytes(b"Actual searchable provenance", "body.txt")
    destination = tmp_path / "bundle"
    manifest = export_bundle(result, destination, vectors=True)
    assert json.loads((destination / "parsed.json").read_text(encoding="utf-8")) == result.model_dump(mode="json")
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((destination / name).read_bytes()).hexdigest() == digest
    chunk = json.loads((destination / "chunks.jsonl").read_text(encoding="utf-8"))
    assert chunk["citations"] == result.chunks[0].citations
    vector = json.loads((destination / "vectors.jsonl").read_text(encoding="utf-8"))["vector"]
    assert len(vector) == 256
    assert math.isclose(sum(value * value for value in vector), 1)
    graph = json.loads((destination / "graph.json").read_text(encoding="utf-8"))
    assert graph["relationships"][0]["type"] == "CONTAINS"
    with pytest.raises(FileExistsError):
        export_bundle(result, destination)
