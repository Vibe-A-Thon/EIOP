"""
Unit Tests for Module MB: Mobile Package Triage, DEX Parsing, and JNI Bridge Mapping (T-ENH-015..020).
"""

import io
import struct
import zipfile
import pytest

from reva.extract.mobile.apk_parser import APKParser
from reva.extract.mobile.dex_parser import DEXParser
from reva.extract.mobile.jni_mapper import JNIBoundaryMapper
from reva.core.errors import RevaResourceLimitError

pytestmark = pytest.mark.reva_depth("unit")


@pytest.fixture
def mock_apk_bytes():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("AndroidManifest.xml", b"<manifest package='com.example.app'/>")
        zf.writestr("classes.dex", b"dex\n035\x00" + b"\x00" * 110)
        zf.writestr("lib/arm64-v8a/libnative.so", b"\x7fELF" + b"\x00" * 60)
    return buf.getvalue()


@pytest.fixture
def mock_dex_bytes():
    buf = bytearray(120)
    buf[0:8] = b"dex\n035\x00"
    struct.pack_into("<I", buf, 8, 0x12345678)  # checksum
    buf[12:32] = b"\xaa" * 20                   # SHA-1 signature
    struct.pack_into("<I", buf, 32, 120)        # file size
    struct.pack_into("<I", buf, 56, 10)         # string_ids_size
    struct.pack_into("<I", buf, 88, 5)          # method_ids_size
    struct.pack_into("<I", buf, 96, 2)          # class_defs_size
    return bytes(buf)


def test_apk_parser(mock_apk_bytes):
    parser = APKParser()
    meta = parser.parse_bytes(mock_apk_bytes)

    assert meta.has_manifest
    assert "classes.dex" in meta.dex_files
    assert "arm64-v8a" in meta.native_libraries
    assert "libnative.so" in meta.native_libraries["arm64-v8a"]
    assert meta.member_count == 3


def test_dex_parser(mock_dex_bytes):
    parser = DEXParser()
    hdr = parser.parse_bytes(mock_dex_bytes)

    assert hdr.version == "035"
    assert hdr.checksum == 0x12345678
    assert hdr.string_ids_count == 10
    assert hdr.method_ids_count == 5
    assert hdr.class_defs_count == 2


def test_jni_boundary_mapper():
    mapper = JNIBoundaryMapper()
    sym = mapper.compute_jni_symbol("com.example.crypto", "KeyStore", "signPayload")
    assert sym == "Java_com_example_crypto_KeyStore_signPayload"

    java_code = """
    package com.example.crypto;
    public class KeyStore {
        public native byte[] signPayload(byte[] data);
        public native int getVersion();
    }
    """
    native_decs = mapper.extract_native_methods_from_java(java_code)
    assert len(native_decs) == 2

    # Match against native so exports
    so_exports = {
        "libcrypto.so": [
            "Java_com_example_crypto_KeyStore_signPayload",
            "other_c_func",
        ]
    }
    mappings = mapper.map_boundaries(native_decs, so_exports)
    assert len(mappings) == 2

    # First one should be resolved
    assert mappings[0].is_resolved
    assert mappings[0].matched_native_lib == "libcrypto.so"

    # Second one is not in the so
    assert not mappings[1].is_resolved
