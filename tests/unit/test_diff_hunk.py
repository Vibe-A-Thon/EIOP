"""Tests for diff hunk parsing and commit-to-symbol linking (FR-CODE-003)."""

from eoip.codegraph.diff_hunk import (
    CommitSymbolLink,
    DiffHunk,
    SymbolRange,
    link_commit_to_symbols,
    parse_unified_diff,
)


SAMPLE_DIFF = """\
diff --git a/src/main.py b/src/main.py
--- a/src/main.py
+++ b/src/main.py
@@ -10,7 +10,9 @@ def helper():
     pass

 def process():
-    old_code()
+    new_code()
+    extra_line()
+    another_line()

@@ -30,3 +32,4 @@ class Handler:
     def handle(self):
         pass
+        self.cleanup()
diff --git a/src/utils.py b/src/utils.py
--- a/src/utils.py
+++ b/src/utils.py
@@ -5,6 +5,8 @@ def format_output():
     return output
+
+def new_utility():
+    pass
"""


def test_parse_unified_diff_extracts_hunks():
    hunks = parse_unified_diff(SAMPLE_DIFF)
    assert len(hunks) == 3
    assert hunks[0].path == "src/main.py"
    assert hunks[0].new_start == 10
    assert hunks[0].new_count == 9
    assert hunks[1].path == "src/main.py"
    assert hunks[1].new_start == 32
    assert hunks[1].new_count == 4
    assert hunks[2].path == "src/utils.py"
    assert hunks[2].new_start == 5
    assert hunks[2].new_count == 8


def test_parse_empty_diff():
    assert parse_unified_diff("") == []


def test_parse_single_line_hunk():
    diff = """\
diff --git a/file.py b/file.py
--- a/file.py
+++ b/file.py
@@ -1 +1 @@
-old
+new
"""
    hunks = parse_unified_diff(diff)
    assert len(hunks) == 1
    assert hunks[0].new_start == 1
    assert hunks[0].new_count == 1
    assert hunks[0].new_end == 1


def test_hunk_new_end():
    hunk = DiffHunk(path="a.py", old_start=1, old_count=5, new_start=10, new_count=7)
    assert hunk.new_end == 16


def test_hunk_new_end_zero_count():
    hunk = DiffHunk(path="a.py", old_start=1, old_count=3, new_start=10, new_count=0)
    assert hunk.new_end == 10


def test_link_commit_to_symbols_overlap():
    hunks = [DiffHunk(path="src/main.py", old_start=10, old_count=5, new_start=10, new_count=8)]
    symbols = {
        "src/main.py": [
            SymbolRange("sym:helper", "helper", 1, 8),
            SymbolRange("sym:process", "process", 10, 20),
            SymbolRange("sym:unrelated", "unrelated", 25, 30),
        ]
    }
    links = link_commit_to_symbols("commit:abc", hunks, symbols)
    assert len(links) == 1
    assert links[0].symbol_id == "sym:process"
    assert links[0].overlap_lines > 0


def test_link_commit_no_overlap():
    hunks = [DiffHunk(path="src/main.py", old_start=50, old_count=3, new_start=50, new_count=3)]
    symbols = {
        "src/main.py": [
            SymbolRange("sym:a", "a", 1, 10),
            SymbolRange("sym:b", "b", 20, 30),
        ]
    }
    links = link_commit_to_symbols("commit:abc", hunks, symbols)
    assert len(links) == 0


def test_link_commit_multiple_symbols():
    hunks = [DiffHunk(path="src/main.py", old_start=1, old_count=50, new_start=1, new_count=50)]
    symbols = {
        "src/main.py": [
            SymbolRange("sym:a", "a", 5, 15),
            SymbolRange("sym:b", "b", 20, 30),
            SymbolRange("sym:c", "c", 40, 50),
        ]
    }
    links = link_commit_to_symbols("commit:abc", hunks, symbols)
    assert len(links) == 3


def test_link_deduplicates_across_hunks():
    hunks = [
        DiffHunk(path="src/main.py", old_start=5, old_count=3, new_start=5, new_count=3),
        DiffHunk(path="src/main.py", old_start=8, old_count=3, new_start=8, new_count=3),
    ]
    symbols = {
        "src/main.py": [SymbolRange("sym:big", "big", 1, 20)]
    }
    links = link_commit_to_symbols("commit:abc", hunks, symbols)
    assert len(links) == 1


def test_link_cross_file():
    hunks = [
        DiffHunk(path="a.py", old_start=1, old_count=3, new_start=1, new_count=3),
        DiffHunk(path="b.py", old_start=1, old_count=3, new_start=1, new_count=3),
    ]
    symbols = {
        "a.py": [SymbolRange("sym:a1", "a1", 1, 10)],
        "b.py": [SymbolRange("sym:b1", "b1", 1, 10)],
    }
    links = link_commit_to_symbols("commit:abc", hunks, symbols)
    assert len(links) == 2
    symbol_ids = {link.symbol_id for link in links}
    assert symbol_ids == {"sym:a1", "sym:b1"}
