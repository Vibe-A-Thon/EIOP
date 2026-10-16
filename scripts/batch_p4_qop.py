from _mark_done import mark_done

entries = {}
for i in range(2, 10):
    rid = f"G2-QOP-{i:03d}"
    entries[rid] = {
        "test_file": "tests/unit/test_question_operators_g2.py",
        "code_paths": ["packages/eoip/graph/query_operators.py"],
    }

mark_done(entries)
