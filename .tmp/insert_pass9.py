"""Insert the Pass-9 section into docs/audit-2026-10-06/assessed-gap-report.md
and the pass9_super_requirements block into assessed-gap-report.json."""
import json

data = json.load(open('.tmp/sr_table.json', encoding='utf-8'))
rows, counts = data['rows'], data['counts']

suite = json.load(open('.tmp/suite_result.json', encoding='utf-8'))

# ---- test counts per package (collected via --collect-only, 2026-10-08) ----
PKG_TESTS = [
    ('tenancy', 'tests/unit/test_tenancy.py', 49),
    ('licensing', 'tests/unit/test_licensing.py', 26),
    ('config (layered)', 'tests/unit/test_layered_config.py', 21),
    ('egress gateway', 'tests/unit/test_egress_gateway.py', 41),
    ('branding', 'tests/unit/test_branding.py', 15),
    ('privacy', 'tests/unit/test_privacy.py', 22),
    ('compliance packs', 'tests/unit/test_compliance_packs.py', 30),
    ('report generator', 'tests/unit/test_reports.py', 37),
    ('QA gate integrity', 'tests/unit/test_qa_gate_integrity.py', 21),
    ('NL suggestion engine', 'tests/unit/test_suggestion_engine.py', 13),
    ('schema profiler', 'tests/unit/test_schema_profiler.py', 21),
    ('pack SDK + domain packs', 'tests/unit/test_marketplace.py + test_domain_packs*.py', 34 + 10 + 8),
    ('SR-wave API routes (new)', 'tests/unit/test_sr_wave_api_routes.py', 12),
]
pkg_total = sum(n for _, _, n in PKG_TESTS)

ROUTES = [
    ('tenancy', 12), ('licensing', 6), ('config', 13), ('egress', 12),
    ('branding', 5), ('privacy', 7), ('compliance', 18), ('reports', 8),
    ('qa', 13), ('suggest', 4), ('ingest profile', 4),
]
routes_total = sum(n for _, n in ROUTES)

lines = []
A = lines.append
A('## Pass 9 — Super-Requirements (SR-*) Commercial Baseline Implementation')
A('')
A('**Date**: 2026-10-08')
A('')
A('### (a) What was implemented in this pass')
A('')
A('Eleven `eoip` packages were wired into the API (`apps/api/extended.py`, '
  '`ExtendedState._init_sr_wave` + `build_extended_router`) behind their lazy '
  '`build_router(...)` factories, and exercised end-to-end through FastAPI '
  'routes with a new test module (`tests/unit/test_sr_wave_api_routes.py`, '
  '12 tests). All routes are live under `/api/v1`.')
A('')
A('| Area (SR IDs) | Package(s) | API prefix | Tests (package file) |')
A('|---|---|---|---|')
A('| Tenancy SR-TEN-001/002/003/006/007/009 | `packages/eoip/tenancy/` | `/api/v1/tenancy` | 49 (`test_tenancy.py`) |')
A('| Licensing SR-DEP-007, SR-COM-001, SR-TEN-009 | `packages/eoip/licensing/` | `/api/v1/licensing` | 26 (`test_licensing.py`) |')
A('| Layered config SR-CFG-001..006 | `packages/eoip/config/` | `/api/v1/config` | 21 (`test_layered_config.py`) |')
A('| Egress gateway SR-LLM-010..020 + SR-CON-010/011 (S0-S7 transforms, manifests, canaries, kill switch; no transport by default) | `packages/eoip/egress/` | `/api/v1/egress` | 41 (`test_egress_gateway.py`) |')
A('| Branding SR-WL-001/003/004-partial/006/007 + SR-ONT-007 | `packages/eoip/branding/` | `/api/v1/branding` | 15 (`test_branding.py`) |')
A('| Privacy SR-PRV-001..004, 006 partials | `packages/eoip/privacy/` | `/api/v1/privacy` | 22 (`test_privacy.py`) |')
A('| Compliance packs SR-GOV-001..005 | `packages/eoip/compliance/` | `/api/v1/compliance` | 30 (`test_compliance_packs.py`) |')
A('| Report generator SR-NLQ-008 (HTML/MD/JSON in-product; PDF/DOCX/PPTX External) | `packages/eoip/reports/` | `/api/v1/reports` | 37 (`test_reports.py`) |')
A('| QA gate integrity SR-QA-010..014 (behavioral evidence registry replacing the string-match gate, mutation checks, three-number dashboard, code introspection, policy gate) | `packages/eoip/qa/` | `/api/v1/qa` | 21 (`test_qa_gate_integrity.py`) |')
A('| NL suggestion engine SR-NLQ-002/003/004-partial | `packages/eoip/suggest/` | `/api/v1/suggest` | 13 (`test_suggestion_engine.py`) |')
A('| Schema profiler SR-ING-010/012/013/016-hook | `packages/eoip/ingest/profile.py` | `/api/v1/ingest/profile` | 21 (`test_schema_profiler.py`) |')
A('| Domain packs (healthcare + manufacturing) SR-COM-020/021 | `packages/eoip/marketplace/` + `config/domain-packs/` | (pack metadata APIs) | 52 (`test_marketplace.py`, `test_domain_packs*.py`) |')
A('')
A(f'Routes added this pass: **{routes_total}** across 11 routers '
  f'({", ".join(f"{k} {n}" for k, n in ROUTES)}).')
A('')
A('### (b) SR status table (all 290 SR IDs from `super-requirements.md`)')
A('')
A('Statuses: **Done-behavioral** = implemented this pass with executable behavioral '
  'evidence; **Exists** = implemented before this pass per prior audit policy; '
  '**Exists-partial** = implementation exists but acceptance is not complete; '
  '**External gate** = genuinely deferred pending external systems/certifications; '
  '**ADR-gated** = deferred pending an architecture/business decision.')
A('')
A('| SR ID | Priority | Status | Evidence |')
A('|---|---|---|---|')
for rid, pri, status, evnote in rows:
    A(f'| {rid} | {pri} | {status} | {evnote} |')
A('')
A(f'Status counts: Done-behavioral {counts.get("Done-behavioral", 0)}, '
  f'Exists {counts.get("Exists", 0)}, Exists-partial {counts.get("Exists-partial", 0)}, '
  f'External gate {counts.get("External gate", 0)}, ADR-gated {counts.get("ADR-gated", 0)}.')
A('')
A('### (c) Test totals for this pass')
A('')
A('| Package tests | File | Tests |')
A('|---|---|---|')
for name, path, n in PKG_TESTS:
    A(f'| {name} | `{path}` | {n} |')
A(f'| **Total pass-9 package tests** | | **{pkg_total}** |')
A('')
A(f'Full unit suite ({suite["label"]}): **{suite["summary"]}**.')
A('')
section = '\n'.join(lines) + '\n'

# ---- insert into .md before the final signature line ----
p = 'docs/audit-2026-10-06/assessed-gap-report.md'
s = open(p, 'r', encoding='utf-8', newline='').read()
sig = '*Pass 8 final - 2026-10-07.'
idx = s.rfind(sig)
assert idx != -1, 'signature line not found'
insert_at = s.rfind('\n', 0, idx) + 1
new = s[:insert_at] + '\n' + section + '\n' + s[insert_at:]
new = new.replace(
    '**Updated**: 2026-10-07 (Pass 8 full GAP gate closure - enterprise completion contracts and focused verification)',
    '**Updated**: 2026-10-08 (Pass 9 SR-* commercial baseline - 11 packages wired into the API, 290-SR status table)',
    1)
open(p, 'w', encoding='utf-8', newline='').write(new)
print('md updated')

# ---- json block ----
pj = 'docs/audit-2026-10-06/assessed-gap-report.json'
doc = json.load(open(pj, encoding='utf-8'))
doc['pass9_super_requirements'] = {
    'date': '2026-10-08',
    'packages_implemented': [
        'eoip.tenancy (SR-TEN-001/002/003/006/007/009)',
        'eoip.licensing (SR-DEP-007, SR-COM-001, SR-TEN-009)',
        'eoip.config (SR-CFG-001..006)',
        'eoip.egress (SR-LLM-010..020, SR-CON-010/011)',
        'eoip.branding (SR-WL-001/003/004-partial/006/007, SR-ONT-007)',
        'eoip.privacy (SR-PRV-001..004, 006 partials)',
        'eoip.compliance (SR-GOV-001..005)',
        'eoip.reports (SR-NLQ-008, HTML/MD/JSON in-product)',
        'eoip.qa (SR-QA-010..014)',
        'eoip.suggest (SR-NLQ-002/003/004-partial)',
        'eoip.ingest.profile (SR-ING-010/012/013/016-hook)',
        'eoip marketplace + config/domain-packs healthcare/manufacturing (SR-COM-020/021)',
    ],
    'wiring': 'apps/api/extended.py ExtendedState._init_sr_wave + build_extended_router',
    'routes_added': {'total': routes_total, 'by_area': dict(ROUTES)},
    'new_test_file': 'tests/unit/test_sr_wave_api_routes.py',
    'package_test_total': pkg_total,
    'sr_status_summary': {
        'total_sr_ids': len(rows),
        'by_status': counts,
    },
    'test_receipt': {
        'command': '.venv/Scripts/python -m pytest tests/unit -q -p no:cacheprovider',
        'passed': suite['passed'],
        'skipped': suite.get('skipped', 0),
        'failed': suite['failed'],
        'summary': suite['summary'],
        'date': '2026-10-08',
    },
}
json.dump(doc, open(pj, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
print('json updated')
