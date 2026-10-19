"""
Unit Tests for Module FM: Firmware Carving, Secret Harvesting, and WASM Decoding (T-ENH-021..024).
"""

import pytest

from reva.extract.firmware.carver import FirmwareCarver
from reva.extract.firmware.secret_harvester import SecretHarvester
from reva.extract.firmware.wasm_decoder import WASMDecoder


@pytest.fixture
def mock_firmware_blob():
    # Build a raw blob containing SquashFS and U-Boot headers
    blob = bytearray(2048)
    # Insert U-Boot at offset 128
    blob[128:132] = b"\x27\x05\x19\x56"
    # Insert SquashFS (hsqs) at offset 512
    blob[512:516] = b"hsqs"
    return bytes(blob)


@pytest.fixture
def mock_wasm_bytes():
    # Magic \x00asm\x01\x00\x00\x00
    magic = b"\x00asm\x01\x00\x00\x00"
    # Section 1 (Type), size 4, dummy payload
    sec1 = bytes([1, 4, 1, 0x60, 0, 0])
    # Section 7 (Export), size 2, dummy payload
    sec7 = bytes([7, 2, 0, 0])
    return magic + sec1 + sec7


def test_firmware_carver(mock_firmware_blob):
    carver = FirmwareCarver()
    parts = carver.carve_bytes(mock_firmware_blob)

    assert len(parts) >= 2
    types = [p.partition_type for p in parts]
    assert "U-Boot" in types
    assert "SquashFS" in types

    uboot = [p for p in parts if p.partition_type == "U-Boot"][0]
    assert uboot.offset == 128

    sqsh = [p for p in parts if p.partition_type == "SquashFS"][0]
    assert sqsh.offset == 512


def test_secret_harvester():
    harvester = SecretHarvester()
    payload = b"""
    Config file:
    api_key = "AKIA1234567890ABCDEF"
    db_uri = "postgres://admin:supersecret@db.internal:5432/production"
    """
    secrets = harvester.harvest_bytes(payload)
    assert len(secrets) >= 2

    types = [s.secret_type for s in secrets]
    assert "AWS_ACCESS_KEY" in types
    assert "DB_CONNECTION_STRING" in types

    # Check preview redaction
    aws_secret = [s for s in secrets if s.secret_type == "AWS_ACCESS_KEY"][0]
    assert "..." in aws_secret.redacted_preview
    assert "AKIA" in aws_secret.redacted_preview


def test_wasm_decoder(mock_wasm_bytes):
    decoder = WASMDecoder()
    info = decoder.decode_bytes(mock_wasm_bytes)

    assert info.version == 1
    assert info.has_type_section
    assert info.has_export_section
    assert len(info.sections) == 2
    assert info.sections[0].name == "Type"
    assert info.sections[1].name == "Export"
