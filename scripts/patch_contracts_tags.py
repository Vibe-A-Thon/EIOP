"""Patch markers in test_g2_contracts.py and convert CRLF to LF."""

path = "tests/contract/test_g2_contracts.py"
content = open(path, "r", encoding="utf-8").read()
content = content.replace(
    '@pytest.mark.req("G2-T0005")',
    '@pytest.mark.req("G2-T0005", "FR-CONN-001", "G2-EKAF-002")'
)
open(path, "w", encoding="utf-8", newline="\n").write(content)
print("Updated tests/contract/test_g2_contracts.py successfully.")
