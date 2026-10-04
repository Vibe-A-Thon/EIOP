"""Versioned file parsing artifacts; offsets refer to extracted section text."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

PARSER_VERSION = "fileparse/1.0"


class ParseError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        self.code = code
        super().__init__(message)


class ParseOptions(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    max_file_bytes: int = Field(default=20_000_000, ge=1, le=100_000_000)
    max_expanded_bytes: int = Field(default=100_000_000, ge=1, le=500_000_000)
    max_members: int = Field(default=500, ge=1, le=10_000)
    max_depth: int = Field(default=3, ge=0, le=8)
    max_rows: int = Field(default=10_000, ge=1, le=100_000)
    max_sections: int = Field(default=10_000, ge=1, le=100_000)
    max_text_chars: int = Field(default=5_000_000, ge=1, le=20_000_000)
    max_image_pixels: int = Field(default=25_000_000, ge=1, le=100_000_000)
    chunk_chars: int = Field(default=1200, ge=32, le=8000)
    chunk_overlap: int = Field(default=150, ge=0, le=2000)
    encoding: str = Field(default="utf-8", min_length=1, max_length=64)
    ocr: bool = False
    ocr_language: str = Field(default="eng", pattern=r"^[A-Za-z0-9_+]+$", max_length=64)
    tesseract_path: str | None = None
    libreoffice_path: str | None = None
    tool_timeout_seconds: int = Field(default=60, ge=1, le=300)

    @model_validator(mode="after")
    def validate_overlap(self) -> ParseOptions:
        if self.chunk_overlap >= self.chunk_chars:
            raise ValueError("chunk_overlap must be smaller than chunk_chars")
        return self


class Section(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int
    kind: str
    text: str
    locator: dict[str, JsonValue] = Field(default_factory=dict)


class Table(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    columns: list[str]
    rows: list[list[JsonValue]]
    locator: dict[str, JsonValue] = Field(default_factory=dict)


class ParsedDocument(BaseModel):
    model_config = ConfigDict(extra="forbid")

    document_id: str
    source_id: str
    source_name: str
    source_uri: str
    parent_id: str | None = None
    content_hash: str
    size_bytes: int
    format: str
    media_type: str
    parser_version: str = PARSER_VERSION
    title: str
    sections: list[Section] = Field(default_factory=list)
    tables: list[Table] = Field(default_factory=list)
    data: JsonValue = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)


class RagChunk(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chunk_id: str
    document_id: str
    source_id: str
    source_uri: str
    content_hash: str
    section_index: int
    start_char: int
    end_char: int
    text: str
    locator: dict[str, JsonValue]
    citations: list[str]


class FileIssue(BaseModel):
    source_name: str
    code: str
    message: str


class ParseResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    schema_version: Literal["1.0"] = "1.0"
    parser_version: str = PARSER_VERSION
    status: Literal["SUCCEEDED", "PARTIAL", "FAILED"] = "SUCCEEDED"
    documents: list[ParsedDocument] = Field(default_factory=list)
    chunks: list[RagChunk] = Field(default_factory=list)
    errors: list[FileIssue] = Field(default_factory=list)
