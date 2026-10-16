from _mark_done import mark_done

entries = {}
for i in range(2, 11):
    rid = f"GAP-TRUTH-{i:03d}"
    entries[rid] = {
        "test_file": "tests/unit/test_truth_resolution.py",
        "code_paths": [
            "packages/eoip/truth/engine.py",
            "packages/eoip/truth/models.py",
        ],
    }

mark_done(entries)
