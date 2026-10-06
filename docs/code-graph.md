# EOIP Code Graph

The code graph links source code symbols to commits, merge requests, work items, and test cases, enabling cross-domain impact analysis and test coverage tracing.

---

## Overview

```
File (path, language)
  ↓ DEFINES
CodeSymbol (qualified_name, symbol_kind, start_line, end_line)
  ↓ CALLS / IMPORTS / INHERITS
CodeSymbol
  ↓ CommitSymbolLink
Commit
  ↓ IMPLEMENTS
WorkItem
```

---

## Code Parser (`packages/eoip/codegraph/parser.py`)

`CodeParser` uses Python's `ast` module for Python files and a tree-sitter-based parser for TypeScript/JavaScript.

### Supported Languages
| Language | File extensions | AST method |
|----------|---------------|------------|
| Python | `.py` | `ast.parse` |
| TypeScript | `.ts`, `.tsx` | tree-sitter |
| JavaScript | `.js` | tree-sitter |

### Symbol Kinds
`FUNCTION`, `CLASS`, `METHOD`, `INTERFACE`, `MODULE`, `VARIABLE`, `CONSTANT`

### `parse(repo_id, path, source) → ParseResult`

Returns:
- `symbols: list[SymbolRange]` — all symbols with location
- `imports: list[str]` — import dependencies
- `parse_errors: list[str]` — parse failures (graceful, never raises)

`PARSER_VERSION` is stored on every `CodeSymbol` vertex for provenance.

---

## SymbolRange (`packages/eoip/codegraph/parser.py`)

```python
@dataclass
class SymbolRange:
    qualified_name: str    # e.g. "PaymentController.processPayment"
    symbol_kind: str       # "function" | "class" | "method" | ...
    start_line: int
    end_line: int
    start_column: int
    end_column: int
    name: str              # short name
```

---

## DiffHunk (`packages/eoip/codegraph/diff_hunk.py`)

`DiffHunk` represents a contiguous changed block from a git diff.

```python
@dataclass
class DiffHunk:
    old_start: int
    old_count: int
    new_start: int
    new_count: int
    lines: list[str]       # diff lines (+/-/ )
```

`DiffHunkParser.parse(diff_text)` splits a unified diff into `DiffHunk` list.

---

## CommitSymbolLink (`packages/eoip/codegraph/link.py`)

`link_commit_to_symbols(commit, symbols, diff_hunks)` — identifies which symbols were modified by a commit.

Algorithm:
1. Parse the commit's diff into `DiffHunk` list
2. For each modified file, find `SymbolRange` records that overlap the changed line range
3. Create a `CommitSymbolLink` edge (Commit → CodeSymbol) with `change_kind` (ADDED/MODIFIED/DELETED)

This link enables "what code changed in issue PAY-123?" queries.

---

## Code Graph JSON Format

Pre-extracted code graphs (from static analysis or export) can be ingested as JSON:

```json
{
  "repo_id": "urn:repo:payment-gateway",
  "files": [
    {"path": "src/payment/controller.py", "language": "python"}
  ],
  "symbols": [
    {
      "qualified_name": "PaymentController.processPayment",
      "kind": "method",
      "file": "src/payment/controller.py",
      "start_line": 42,
      "end_line": 89,
      "name": "processPayment"
    }
  ],
  "edges": [
    {"from": "PaymentController.processPayment", "to": "PaymentValidator.validate", "type": "CALLS"},
    {"from": "PaymentController", "to": "BaseController", "type": "INHERITS"},
    {"from": "src/payment/controller.py", "to": "stripe", "type": "IMPORTS"}
  ],
  "dependencies": [
    {"name": "stripe", "version": "5.4.0", "language": "python"}
  ]
}
```

Ingested via `CodeGraphJsonProcessor` or `POST /api/v1/admin/ingestion/code-graph-json`.

Demo code graphs are in `demo/demodata/code/`.

---

## Code Graph API

### Export
```
GET /api/v1/code/export?repo=urn:repo:payment-gateway
```
Returns the code graph as JSON (same format as ingestion input).

### Search
```
POST /api/v1/search
{"query": "PaymentController", "labels": ["CodeSymbol"]}
```

### Impact from Symbol
```
POST /api/v1/impact
{"canonical_id": "urn:codesymbol:payment-gateway/PaymentController/processPayment", "direction": "DOWNSTREAM"}
```

### Symbol → Test Coverage
```
POST /api/v1/agents/query
{"question": "What tests cover PaymentController.processPayment?"}
```

---

## Cross-Domain Links

The semantic pipeline (`bridge_edges` stage) creates cross-domain edges:

| Link | Source → Target | Created When |
|------|----------------|--------------|
| `CommitSymbolLink` | Commit → CodeSymbol | Commit diff overlaps symbol range |
| `IMPLEMENTS` | Commit → WorkItem | Commit message contains issue key |
| `COVERS` | TestCase → CodeSymbol | Test file imports or calls symbol |
| `REFERENCED_IN` | CodeSymbol → Document | Documentation mentions symbol |
| `DEPLOYED_AS` | CodeSymbol → Deployment | Symbol present in deployment artifact |

---

## MCP Tools for Code Graph

All 17 MCP tools are read-only. Code-specific tools:

| Tool | Description |
|------|-------------|
| `get_code_symbol` | Get symbol details by canonical_id |
| `get_file_symbols` | List all symbols in a file |
| `list_commits` | List commits by repo, branch, or author |
| `get_dependencies` | Get package dependencies for a repo |
| `impact_analysis` | Blast radius from a code symbol |
| `find_path` | Path from symbol to work item or test |

---

## TestCoverageAgent

`packages/eoip/agents/test_coverage.py`

Given a set of `CodeSymbol` canonical IDs, returns:
- `TestCase` vertices that have `COVERS` edges to those symbols
- Symbols with no test coverage (coverage gap)
- Coverage percentage per file

Uses `TraceLineageAgent` to follow the chain: `TestCase → COVERS → CodeSymbol`.
