"""
Mobile Package Triage & JNI Native Bridge Mapper (Module MB, T-ENH-015..020).
Provides pure-Python APK, DEX, and JNI boundary analysis.
"""

from reva.extract.mobile.apk_parser import APKParser, APKMetadata
from reva.extract.mobile.dex_parser import DEXParser, DEXHeader
from reva.extract.mobile.jni_mapper import JNIBoundaryMapper, JNIBridgeMapping

__all__ = [
    "APKParser",
    "APKMetadata",
    "DEXParser",
    "DEXHeader",
    "JNIBoundaryMapper",
    "JNIBridgeMapping",
]
