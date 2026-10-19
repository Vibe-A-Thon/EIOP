"""
JNI Native Bridge Symbol Mapper (REVA-MB-004, T-ENH-018).
Bridges Java/Kotlin native method calls to compiled native C/C++ symbol exports in .so files.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set, Tuple


@dataclass
class JNIBridgeMapping:
    java_class: str
    java_method: str
    expected_c_symbol: str
    matched_native_lib: Optional[str] = None
    is_resolved: bool = False


class JNIBoundaryMapper:
    """
    Computes standard JNI symbol signatures according to Oracle JVM / Android ART spec:
    Java_<fully_qualified_class_with_underscores>_<method_name>
    """

    def compute_jni_symbol(self, package_name: str, class_name: str, method_name: str) -> str:
        """
        Derives the canonical exported JNI symbol name.
        """
        full_class = f"{package_name}.{class_name}" if package_name else class_name
        sanitized_class = full_class.replace("_", "_1").replace(".", "_")
        sanitized_method = method_name.replace("_", "_1")
        return f"Java_{sanitized_class}_{sanitized_method}"

    def extract_native_methods_from_java(self, java_source: str, package_name: str = "") -> List[Tuple[str, str]]:
        """
        Finds 'native' method declarations in Java/Kotlin source code using regex.
        Returns List of (class_name, method_name).
        """
        # Find class name
        class_match = re.search(r"\bclass\s+([A-Za-z0-9_]+)", java_source)
        class_name = class_match.group(1) if class_match else "UnknownClass"

        # Find package if not provided
        if not package_name:
            pkg_match = re.search(r"\bpackage\s+([A-Za-z0-9_\.]+);", java_source)
            if pkg_match:
                package_name = pkg_match.group(1)

        # Find native methods
        results = []
        for match in re.finditer(r"\bnative\s+[A-Za-z0-9_<>\[\]]+\s+([A-Za-z0-9_]+)\s*\(", java_source):
            method_name = match.group(1)
            results.append((f"{package_name}.{class_name}" if package_name else class_name, method_name))

        return results

    def map_boundaries(
        self,
        java_native_declarations: List[Tuple[str, str]], # (class_name, method_name)
        native_so_exported_symbols: Dict[str, List[str]], # so_name -> list of exported symbols
    ) -> List[JNIBridgeMapping]:
        """
        Resolves Java native declarations against native library symbol tables.
        """
        mappings: List[JNIBridgeMapping] = []

        for full_class, method in java_native_declarations:
            parts = full_class.rsplit(".", 1)
            pkg = parts[0] if len(parts) > 1 else ""
            cls = parts[-1]
            c_sym = self.compute_jni_symbol(pkg, cls, method)

            matched_lib = None
            for so_name, symbols in native_so_exported_symbols.items():
                if c_sym in symbols:
                    matched_lib = so_name
                    break

            mappings.append(JNIBridgeMapping(
                java_class=full_class,
                java_method=method,
                expected_c_symbol=c_sym,
                matched_native_lib=matched_lib,
                is_resolved=matched_lib is not None,
            ))

        return mappings
