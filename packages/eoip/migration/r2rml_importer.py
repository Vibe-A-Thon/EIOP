"""R2RML / RML import translator for Ontop, Morph-KGC, and RMLStreamer (CRA-034.8, ONT-017).

Translates R2RML and RML mapping files into CML / MappingIR.
Explicitly detects and flags unsupported constructs (custom SQL functions, non-standard joins,
unsupported logical source formats) and records them in a LossReport.
"""

from __future__ import annotations

from typing import Any

from eoip.mapping.ir import (
    MappingIR,
    PropertyMapIR,
    ProvenanceConfigIR,
    RelationMapIR,
    SubjectMapIR,
)
from eoip.mapping.r2rml import LossReport, R2RMLAdapter, UnsupportedConstruct


class ThirdPartyRMLImporter:
    """Imports R2RML/RML configurations from Ontop, Morph-KGC, and RMLStreamer."""

    def __init__(self, engine_origin: str = "ontop") -> None:
        self.engine_origin = engine_origin.lower()
        self.adapter = R2RMLAdapter()

    def translate_to_cml_ir(
        self,
        rml_content: dict[str, Any],
    ) -> tuple[MappingIR, LossReport]:
        """Translate RML dictionary into MappingIR and generate a LossReport."""
        # Check engine-specific constructs
        unsupported: list[UnsupportedConstruct] = []
        coercions: list[str] = []

        logical_source = rml_content.get("logicalSource") or rml_content.get("logicalTable", {})

        # RMLStreamer specific: stream connectors (Kafka, WebSockets)
        if self.engine_origin == "rmlstreamer":
            if "sourceType" in logical_source and logical_source["sourceType"] not in ("file", "table", "rest"):
                unsupported.append(
                    UnsupportedConstruct(
                        construct_type="RMLStreamer_StreamSource",
                        identifier=logical_source.get("sourceType", "unknown"),
                        detail="Real-time streaming RML sources must be bridged via EOIP SourceConnector",
                    )
                )

        # Ontop specific: proprietary SQL expressions
        if self.engine_origin == "ontop":
            query = str(logical_source.get("sqlQuery", ""))
            if "regexp_replace" in query.lower() or "sysdate" in query.lower():
                coercions.append("Vendor-specific SQL dialect expressions coerced to standard SQL-92")

        # Morph-KGC specific: tabular file extensions
        if self.engine_origin == "morph-kgc":
            if logical_source.get("format") == "excel":
                unsupported.append(
                    UnsupportedConstruct(
                        construct_type="MorphKGC_BinaryExcel",
                        identifier="excel_format",
                        detail="Binary Excel spreadsheets must be pre-extracted to CSV/Parquet",
                    )
                )

        mapping_ir, loss_report = self.adapter.import_r2rml_dict(rml_content)

        # Merge findings
        for u in unsupported:
            loss_report.unsupported_constructs.append(u)
        for c in coercions:
            loss_report.lossy_coercions.append(c)

        return mapping_ir, loss_report
