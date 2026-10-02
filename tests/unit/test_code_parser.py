from eoip.codegraph.parser import CodeParser


def test_python_parser_returns_stable_symbols_ranges_imports_and_static_calls() -> None:
    source = "from helpers import normalize\n\ndef run():\n    return normalize()\n\ndef normalize():\n    return 'ok'\n"
    parser = CodeParser()

    parsed = parser.parse("demo", "src/service.py", source)
    repeated = parser.parse("demo", "src/service.py", source)

    assert parsed.language == "python"
    assert parsed.imports == ["helpers"]
    assert [symbol.name for symbol in parsed.symbols] == ["run", "normalize"]
    assert parsed.symbols[0].start_line == 3
    assert parsed.symbols[0].end_line == 4
    assert parsed.calls[0].callee_name == "normalize"
    assert parsed.calls[0].target_id == parsed.symbols[1].canonical_id
    assert [symbol.canonical_id for symbol in parsed.symbols] == [symbol.canonical_id for symbol in repeated.symbols]


def test_typescript_parser_extracts_function_variable_import_and_call() -> None:
    source = 'import { parse } from "./parser";\nexport function run() { return parse(); }\nexport const parse = () => 1;\n'

    parsed = CodeParser().parse("demo", "src/client.ts", source)

    assert parsed.language == "typescript"
    assert parsed.imports == ["./parser"]
    assert {symbol.name for symbol in parsed.symbols} == {"run", "parse"}
    assert any(call.callee_name == "parse" for call in parsed.calls)


def test_python_syntax_errors_are_explicit_and_not_partially_mapped() -> None:
    parsed = CodeParser().parse("demo", "src/broken.py", "def broken(:\n  pass\n")

    assert parsed.parse_errors
    assert not parsed.symbols
    assert not parsed.calls