"""Real Office containers and read-only SQLite, with structured rows/slide locators."""

from __future__ import annotations

import io
import sqlite3
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree.ElementTree import ParseError as XMLParseError

from eoip.fileparse.common import Extraction, dependency, json_cell
from eoip.fileparse.contracts import ParseError


def parse_office(content: bytes, suffix: str, out: Extraction) -> None:
    if suffix == ".xls":
        errors = (dependency("xlrd").XLRDError,)
    elif suffix == ".pdf":
        errors = (dependency("pypdf.errors").PyPdfError,)
    elif suffix in {".odt", ".ods", ".odp"}:
        errors = (dependency("defusedxml.common").DefusedXmlException, zipfile.BadZipFile)
    else:
        errors = (dependency("lxml.etree").XMLSyntaxError, XMLParseError)
    try:
        _parse_office(content, suffix, out)
    except errors as exc:
        raise ParseError("invalid_format", f"{suffix} contains malformed Office data") from exc


def parse_pdf(content: bytes, out: Extraction) -> None:
    pypdf = dependency("pypdf")
    try:
        reader = pypdf.PdfReader(io.BytesIO(content))
        if reader.is_encrypted:
            raise ParseError("encrypted_document", "PDF is encrypted and cannot be parsed without credentials")
        for index, page in enumerate(reader.pages, 1):
            text = page.extract_text() or ""
            if text.strip():
                out.section("page", text.strip(), page=index)
        out.document.metadata["pages"] = len(reader.pages)
    except ParseError:
        raise
    except Exception as exc:
        raise ParseError("invalid_format", f"PDF decoding failed: {exc}") from exc


def parse_odf(content: bytes, suffix: str, out: Extraction) -> None:
    etree = dependency("defusedxml.ElementTree")
    try:
        with zipfile.ZipFile(io.BytesIO(content)) as archive:
            if "content.xml" not in archive.namelist():
                raise ParseError("invalid_format", "ODF package missing content.xml")
            xml_data = archive.read("content.xml")
            root = etree.fromstring(xml_data)

            if suffix == ".ods":
                sheet_count = 0
                for table_elem in root.iter():
                    if table_elem.tag.endswith("table"):
                        sheet_count += 1
                        sheet_name = table_elem.attrib.get(
                            "{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name", f"sheet_{sheet_count}"
                        )
                        rows = []
                        for row_elem in table_elem.iter():
                            if row_elem.tag.endswith("table-row"):
                                row_cells = []
                                for cell_elem in row_elem.iter():
                                    if cell_elem.tag.endswith("table-cell"):
                                        cell_text = "".join(cell_elem.itertext()).strip()
                                        row_cells.append(json_cell(cell_text if cell_text else None))
                                if any(c is not None for c in row_cells):
                                    rows.append(row_cells)
                        if rows:
                            width = max((len(r) for r in rows), default=0)
                            out.table(sheet_name, [f"column_{i+1}" for i in range(width)], rows, sheet=sheet_name)
            elif suffix == ".odp":
                slide_idx = 0
                for page_elem in root.iter():
                    if page_elem.tag.endswith("page"):
                        slide_idx += 1
                        slide_text = " ".join(page_elem.itertext()).strip()
                        if slide_text:
                            out.section("slide", slide_text, slide=slide_idx)
            else:
                block_idx = 0
                for elem in root.iter():
                    if elem.tag.endswith("p") or elem.tag.endswith("h"):
                        text = "".join(elem.itertext()).strip()
                        if text:
                            block_idx += 1
                            kind = "heading" if elem.tag.endswith("h") else "paragraph"
                            out.section(kind, text, block=block_idx, paragraph=block_idx)
    except ParseError:
        raise
    except Exception as exc:
        raise ParseError("invalid_format", f"{suffix} decoding failed: {exc}") from exc


def _parse_office(content: bytes, suffix: str, out: Extraction) -> None:
    if suffix == ".pdf":
        parse_pdf(content, out)
    elif suffix in {".odt", ".ods", ".odp"}:
        parse_odf(content, suffix, out)
    elif suffix == ".docx":
        docx = dependency("docx")
        document = docx.Document(io.BytesIO(content))
        for index, block in enumerate(document.iter_inner_content()):
            if isinstance(block, docx.text.paragraph.Paragraph):
                out.section("paragraph", block.text, block=index, style=block.style.name)
            else:
                rows = [[cell.text for cell in row.cells] for row in block.rows]
                width = max((len(row) for row in rows), default=0)
                out.table(f"table_{index}", [f"column_{i + 1}" for i in range(width)], rows, block=index)
        for index, section in enumerate(document.sections):
            for kind in ("header", "footer"):
                for paragraph in getattr(section, kind).paragraphs:
                    out.section(kind, paragraph.text, section=index)
        out.document.metadata["author"] = document.core_properties.author or ""
        out.document.metadata["macros_executed"] = False
    elif suffix == ".xlsx":
        openpyxl = dependency("openpyxl")
        workbook = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=False, keep_links=False)
        try:
            for sheet in workbook:
                # Do not trust producer-supplied worksheet dimensions.
                sheet.reset_dimensions()
                rows = []
                formulas_detected = []
                for row_idx, row in enumerate(sheet.iter_rows(values_only=True), 1):
                    if out.rows + len(rows) >= out.options.max_rows:
                        raise ParseError("row_limit", "Workbook exceeds max_rows")
                    if len(row) > 10_000:
                        raise ParseError("column_limit", "Worksheet exceeds 10000 columns")
                    row_cells = []
                    for col_idx, value in enumerate(row, 1):
                        if isinstance(value, str) and value.startswith("="):
                            formulas_detected.append({"sheet": sheet.title, "row": row_idx, "column": col_idx, "formula": value})
                        row_cells.append(json_cell(value))
                    rows.append(row_cells)
                width = max((len(row) for row in rows), default=0)
                out.table(sheet.title, [f"column_{i + 1}" for i in range(width)], rows, sheet=sheet.title)
                if formulas_detected:
                    out.document.metadata.setdefault("formulas_detected", []).extend(formulas_detected)
        finally:
            workbook.close()
        out.document.metadata["formulas"] = "distinguished from values; preserved as text; macros prohibited and never executed"
        out.document.metadata["macros_executed"] = False
    elif suffix == ".xls":
        xlrd = dependency("xlrd")
        workbook = xlrd.open_workbook(file_contents=content, on_demand=True)
        try:
            for sheet in workbook.sheets():
                if out.rows + sheet.nrows > out.options.max_rows or sheet.ncols > 10_000:
                    raise ParseError("row_limit", "XLS sheet exceeds configured row/column limits")
                rows = []
                for index in range(sheet.nrows):
                    values = []
                    for cell in sheet.row(index):
                        value = cell.value
                        if cell.ctype == xlrd.XL_CELL_DATE:
                            value = xlrd.xldate.xldate_as_datetime(value, workbook.datemode)
                        values.append(json_cell(value))
                    rows.append(values)
                out.table(sheet.name, [f"column_{i + 1}" for i in range(sheet.ncols)], rows, sheet=sheet.name)
        finally:
            workbook.release_resources()
        out.document.metadata["macros_executed"] = False
    else:
        pptx = dependency("pptx")
        presentation = pptx.Presentation(io.BytesIO(content))
        for index, slide in enumerate(presentation.slides, 1):
            def shapes(items, slide_index=index):
                for shape in items:
                    if shape.shape_type == 6:
                        shapes(shape.shapes)
                    elif shape.has_text_frame:
                        out.section("slide", shape.text_frame.text, slide=slide_index, shape=shape.shape_id)
                    elif shape.has_table:
                        rows = [[cell.text for cell in row.cells] for row in shape.table.rows]
                        out.table(
                            f"slide_{slide_index}_table_{shape.shape_id}",
                            [f"column_{i + 1}" for i in range(len(shape.table.columns))], rows, slide=slide_index,
                        )
            shapes(slide.shapes)
            if slide.has_notes_slide:
                frame = slide.notes_slide.notes_text_frame
                if frame:
                    out.section("speaker_notes", frame.text, slide=index)
        out.document.metadata["macros_executed"] = False


def parse_database(content: bytes, out: Extraction) -> None:
    if not content.startswith(b"SQLite format 3\x00"):
        raise ParseError("unsupported_database", ".db supports SQLite 3 only; export other databases explicitly")
    with TemporaryDirectory(prefix="eoip-sqlite-") as temporary:
        path = Path(temporary) / "input.db"
        path.write_bytes(content)
        connection = sqlite3.connect(f"{path.as_uri()}?mode=ro&immutable=1", uri=True)
        connection.set_progress_handler(lambda: 1, 1_000_000)
        try:
            connection.execute("PRAGMA query_only=ON")
            connection.execute("PRAGMA trusted_schema=OFF")
            tables = connection.execute(
                "SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
            ).fetchmany(out.options.max_members + 1)
            if len(tables) > out.options.max_members:
                raise ParseError("member_limit", "Database exceeds the table count limit")
            for name, sql in tables:
                if sql and "VIRTUAL TABLE" in sql.upper():
                    raise ParseError("unsupported_database", "SQLite virtual tables require a separate trusted export")
                quoted = '"' + name.replace('"', '""') + '"'
                cursor = connection.execute(f"SELECT * FROM {quoted} LIMIT ?", (out.options.max_rows + 1,))
                rows = cursor.fetchall()
                if len(rows) > out.options.max_rows:
                    raise ParseError("row_limit", "Database exceeds max_rows")
                columns = [item[0] for item in cursor.description]
                out.table(name, columns, [[json_cell(cell) for cell in row] for row in rows], table_name=name)
            out.document.metadata["database_kind"] = "sqlite3"
        finally:
            connection.close()
