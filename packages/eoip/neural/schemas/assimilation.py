"""
Dual-Pathway Brain Schema Assimilation Engine (NS-P1, T-NS-003).
Implements the Tse-Morris cognitive architecture:
- Fast cortical slot-filling pathway (< 50ms latency target)
- Slow hippocampal novelty gap router with REVA Warrant linkage
Strictly guarantees epistemic labeling: epistemic_state="inferred".
"""

from __future__ import annotations

import time
from typing import Any, Dict, List, Optional, Tuple

from packages.eoip.neural.schemas.models import AssimilationResult, NeuralSchema
from reva.core.ids import gap_id


class DualPathwayAssimilator:
    """
    Assimilates incoming entity attributes into active Neural Schemas.
    Routes novelty to knowledge gaps when slot fit is below threshold.
    """

    def __init__(
        self,
        schemas: Optional[Dict[str, NeuralSchema]] = None,
        confidence_threshold: float = 0.85,
        max_fast_latency_ms: float = 50.0,
    ) -> None:
        self.schemas: Dict[str, NeuralSchema] = schemas or {}
        self.confidence_threshold = confidence_threshold
        self.max_fast_latency_ms = max_fast_latency_ms

    def register_schema(self, schema: NeuralSchema) -> None:
        self.schemas[schema.schema_id] = schema

    def assimilate(
        self,
        schema_id: str,
        entity_properties: Dict[str, Any],
        tenant_id: str = "default",
    ) -> AssimilationResult:
        """
        Executes dual-pathway schema assimilation:
        - If required slots are satisfied: fast-path assimilation with epistemic_state='inferred'
        - If novelty or missing required slots: slow-path routing to gap engine
        """
        t0 = time.perf_counter()

        if schema_id not in self.schemas:
            elapsed_ms = (time.perf_counter() - t0) * 1000.0
            return AssimilationResult(
                schema_id=schema_id,
                status="rejected",
                confidence=0.0,
                filled_slots={},
                missing_slots=[],
                latency_ms=elapsed_ms,
                epistemic_state="inferred",
            )

        schema = self.schemas[schema_id]
        filled_slots: Dict[str, Any] = {}
        missing_slots: List[str] = []
        valid_count = 0
        total_required = 0

        for slot_name, constraint in schema.slots.items():
            if constraint.required:
                total_required += 1

            if slot_name in entity_properties:
                val = entity_properties[slot_name]
                if constraint.validate_value(val):
                    filled_slots[slot_name] = {
                        "value": val,
                        "epistemic_state": "inferred",
                    }
                    if constraint.required:
                        valid_count += 1
                else:
                    if constraint.required:
                        missing_slots.append(slot_name)
            else:
                if constraint.required:
                    missing_slots.append(slot_name)

        confidence = (valid_count / total_required) if total_required > 0 else 1.0
        elapsed_ms = (time.perf_counter() - t0) * 1000.0

        # Fast cortical pathway
        if confidence >= self.confidence_threshold and not missing_slots:
            return AssimilationResult(
                schema_id=schema_id,
                status="assimilated",
                confidence=confidence,
                filled_slots=filled_slots,
                missing_slots=[],
                latency_ms=elapsed_ms,
                epistemic_state="inferred",
            )

        # Slow hippocampal novelty gap routing
        g_id = gap_id(
            tenant_id=tenant_id,
            domain=schema.domain,
            question=f"Novelty gap for schema {schema.name}: missing {missing_slots}",
            scope={"schema_id": schema_id, "missing_slots": missing_slots},
        )

        return AssimilationResult(
            schema_id=schema_id,
            status="novel_gap_routed",
            confidence=confidence,
            filled_slots=filled_slots,
            missing_slots=missing_slots,
            latency_ms=elapsed_ms,
            epistemic_state="inferred",
            gap_id=g_id,
        )
