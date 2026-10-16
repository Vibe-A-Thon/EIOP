"""GraphMutation v1.

Normative: schemas/graph_mutation.schema.json
"Every graph mutation references a captured event." (FR-INGEST-001)
"""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class GraphMutation(BaseModel):
    model_config = ConfigDict(extra="forbid")

    mutation_id: str = Field(min_length=1)
    operation: Literal["UPSERT", "TOMBSTONE"]
    target_kind: Literal["VERTEX", "EDGE"]
    payload: dict
    ingestion_run_id: str = Field(min_length=1)

    @field_validator("mutation_id", "ingestion_run_id")
    @classmethod
    def require_nonblank_identity(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("mutation_id and ingestion_run_id must be nonblank")
        return value
