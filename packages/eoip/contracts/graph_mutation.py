"""GraphMutation v1.

Normative: EOIP-engg-doc-pkg/schemas/graph_mutation.schema.json
"Every graph mutation references a captured event." (FR-INGEST-001)
"""

from typing import Literal

from pydantic import BaseModel


class GraphMutation(BaseModel):
    mutation_id: str
    operation: Literal["UPSERT", "TOMBSTONE"]
    target_kind: Literal["VERTEX", "EDGE"]
    payload: dict
    ingestion_run_id: str
