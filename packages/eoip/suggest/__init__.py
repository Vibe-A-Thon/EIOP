"""NL suggestion engine (SR-NLQ-001..005).

Backend for the 'intelligent suggestion engine': deterministic template/semantic
parser tier mapping the §1.2 question taxonomy to ``QueryPlan`` previews, ranked
candidate interpretations with entity bindings, cost tiers, confidence,
data-coverage and permission pre-check notes. Optional LLM-assist is an
External gate and never required.
"""

from eoip.suggest.engine import LLMAssistHook, SuggestionEngine
from eoip.suggest.models import (
    COST_TIERS,
    CandidateInterpretation,
    EntityAlternative,
    EntityBinding,
    PermissionNote,
    SuggestionRequest,
    SuggestionResponse,
    choose_answer_mode,
)
from eoip.suggest.parser import parse_question

__all__ = [
    "COST_TIERS",
    "CandidateInterpretation",
    "EntityAlternative",
    "EntityBinding",
    "LLMAssistHook",
    "PermissionNote",
    "SuggestionEngine",
    "SuggestionRequest",
    "SuggestionResponse",
    "choose_answer_mode",
    "parse_question",
]
