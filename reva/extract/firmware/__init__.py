"""
Firmware & Bytecode Carving (Module FM, T-ENH-021..024).
Provides pure-Python firmware carving, secret harvesting, and WASM decoding.
"""

from reva.extract.firmware.carver import FirmwareCarver, CarvedPartition
from reva.extract.firmware.secret_harvester import SecretHarvester, HarvestedSecret
from reva.extract.firmware.wasm_decoder import WASMDecoder, WASMModuleInfo

__all__ = [
    "FirmwareCarver",
    "CarvedPartition",
    "SecretHarvester",
    "HarvestedSecret",
    "WASMDecoder",
    "WASMModuleInfo",
]
