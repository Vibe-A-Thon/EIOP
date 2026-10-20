import pytest
from reva.core.egress_gate import EgressSecurityGate, RevaEgressViolationError
from reva.core.pseudonymizer import CodePseudonymizer

pytestmark = pytest.mark.reva_depth("unit")

def test_code_pseudonymizer():
    pseudonymizer = CodePseudonymizer()
    code = """
def internal_calculator(api_key, account_id):
    endpoint = "https://vault.internal.example/api/v1/rotate"
    secret_token = "some_secret"
    return api_key + account_id
"""
    result = pseudonymizer.pseudonymize_code(code)
    assert "[FUNC_1]" in result
    assert "[DOMAIN_1]" in result
    assert "https://[DOMAIN_1]/api/v1/rotate" in result
    assert "internal_calculator" not in result

    # Test reverse mapping
    restored = pseudonymizer.restore_tokens(result)
    assert "internal_calculator" in restored
    assert "vault.internal.example" in restored

def test_egress_gate_scrubs_secrets():
    gate = EgressSecurityGate()
    payload = {
        "user_input": "Here is my AWS key: AKIAIOSFODNN7EXAMPLE and JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.doNotLeakThisToken",
    }
    sanitized = gate.inspect_and_sanitize(payload)
    assert "AKIAIOSFODNN7EXAMPLE" not in sanitized["user_input"]
    assert "[REDACTED_AWS_KEY]" in sanitized["user_input"]
    assert "[REDACTED_JWT]" in sanitized["user_input"]
    assert "<<<UNTRUSTED_CONTENT_START:" in sanitized["user_input"]
    assert sanitized["_egress_gate"]["verified"] is True

def test_egress_gate_fences_content():
    gate = EgressSecurityGate()
    payload = {"prompt": "Analyze this code structure"}
    sanitized = gate.inspect_and_sanitize(payload)
    assert "<<<UNTRUSTED_CONTENT_START:" in sanitized["prompt"]
    assert "<<<UNTRUSTED_CONTENT_END>>>" in sanitized["prompt"]
