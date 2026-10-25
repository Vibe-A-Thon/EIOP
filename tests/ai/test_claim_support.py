"""CRA-026.7/.8: every answer sentence is backed by a cited evidence span; unsupported claims are removed."""
from __future__ import annotations

import pytest
from eoip.ai.claim_support import check_claim, extractive_sentences

pytestmark = pytest.mark.req("CRA-026")

EV = [
    {"assertion_id": "a1", "snippet": "The payments service is owned by team red. It was migrated in 2024."},
    {"assertion_id": "a2", "snippet": "Checkout depends on the payments service."},
]


@pytest.mark.parametrize("claim,ok,reason", [
    ("The payments service is owned by team red [a1].", True, ""),
    ("Payments was migrated in 2024 [a1].", True, ""),
    ("Payments was migrated in 2023 [a1].", False, "numbers not in evidence"),          # hallucinated number
    ("The payments service is not owned by team red [a1].", False, "negation"),          # flipped polarity
    ("The payments service is owned by team red [a9].", False, "not in the context"),     # fabricated citation
    ("Checkout depends on the payments service [a1].", False, "coverage"),               # wrong cited source
    ("Checkout depends on the payments service.", True, ""),                              # uncited, but backed
    ("Revenue grew strongly across Europe.", False, "no overlapping"),                    # unbacked
])
def test_claim_support_cases(claim, ok, reason):
    v = check_claim(claim, EV)
    assert v.supported is ok and reason in v.reason
    if ok:
        src = next(e["snippet"] for e in EV if e["assertion_id"] == v.assertion_id)
        assert src[v.span["start"]:v.span["end"]] == v.span["text"]  # exact span offsets


def test_extractive_answer_is_verbatim_cited_spans():
    out = extractive_sentences("when was it migrated?", EV)
    assert out[0].sentence == "It was migrated in 2024. [a1]" and out[0].span["text"] == "It was migrated in 2024."
    assert all(check_claim(c.sentence, EV).supported for c in out)
