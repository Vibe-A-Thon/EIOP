const {test} = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..', '..', '..');
const folder = path.join(root, 'EOIP-engg-doc-pkg', 'roles');
const html = fs.readFileSync(path.join(folder, 'roles_dashboard.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

function dashboard(saved = '{}', storageError = false) {
  const elements = new Map();
  const downloads = [];
  let persisted = saved;
  const element = id => {
    if (!elements.has(id)) elements.set(id, {
      innerHTML: '', textContent: '', style: {}, attributes: {},
      setAttribute(name, value) { this.attributes[name] = value; },
      addEventListener() {},
      insertAdjacentHTML(_position, value) { this.innerHTML += value; },
    });
    return elements.get(id);
  };
  const context = vm.createContext({
    document: {
      getElementById: element,
      body: {appendChild() {}},
      createElement: () => ({
        click() { downloads.push(this.download); },
        remove() {},
      }),
    },
    localStorage: {
      getItem() { if (storageError) throw new Error('storage denied'); return persisted; },
      setItem(_key, value) { if (storageError) throw new Error('storage denied'); persisted = value; },
    },
    Blob,
    URL: {createObjectURL: () => 'blob:test', revokeObjectURL() {}},
    setTimeout: callback => callback(),
  });
  vm.runInContext(script, context);
  return {
    read: expression => JSON.parse(JSON.stringify(vm.runInContext(expression, context))),
    run: code => vm.runInContext(code, context),
    elements, downloads, saved: () => persisted,
  };
}

test('roles dashboard covers every source task and range without invented engine assignments', () => {
  const page = dashboard();
  const tasks = page.read('TASKS');
  const expected = new Set();
  for (const file of fs.readdirSync(folder).filter(name => name.endsWith('_tasks.md'))) {
    const lines = fs.readFileSync(path.join(folder, file), 'utf8').split(/\r?\n/);
    for (let i = 0; i < lines.length; i++) {
      if (!lines[i].startsWith('- **TASK-')) continue;
      const ids = lines[i].match(/TASK-[A-Z]+-\d+/g);
      const first = Number(ids[0].slice(-3));
      const last = Number(ids.at(-1).slice(-3));
      const prefix = ids[0].slice(0, -3);
      for (let n = first; n <= last; n++) {
        const id = prefix + String(n).padStart(3, '0');
        expected.add(id);
        const task = tasks.find(item => item.id === id);
        assert.ok(task, `Missing ${id}`);
        assert.equal(task.source.path, file);
        assert.equal(task.source.line, i + 1, `Stale source line for ${id}`);
        if (first !== last) {
          assert.equal(task.grouped, true);
          assert.equal(task.status, 'Blocked');
          assert.equal(task.pri, 'Unspecified');
        }
      }
    }
  }
  assert.equal(expected.size, 244);
  assert.equal(tasks.length, expected.size);
  assert.deepEqual(new Set(tasks.map(t => t.id)), expected);
  assert.equal(tasks.filter(t => t.grouped).length, 28);
  assert.equal(page.read('ROLES.length'), 15);
  assert.ok(page.read('Object.keys(ASSESSMENTS)').every(id => expected.has(id)));
});

test('every assessed task has concrete remaining work and valid evidence paths and line references', () => {
  const page = dashboard();
  for (const [key, evidence] of Object.entries(page.read('EVIDENCE'))) {
    const target = path.join(root, ...evidence.path.split('/'));
    if (!fs.existsSync(target) && /^(audit-output|test-results)\//.test(evidence.path)) continue;
    assert.ok(fs.existsSync(target), `${key}: ${target}`);
    assert.ok(evidence.line > 0 && evidence.line <= fs.readFileSync(target, 'utf8').split(/\r?\n/).length);
  }
  for (const task of page.read('TASKS')) {
    assert.ok(task.observed.length > 20, task.id);
    assert.ok(task.remaining.length > 30, task.id);
    if (task.status === 'Completed') assert.ok(task.evidence.length, task.id);
  }
  assert.equal(page.read('gs("TASK-DEV-031")'), 'Failed');
  assert.equal(page.read('gs("TASK-DEV-032")'), 'Partial');
  assert.equal(page.read('gs("TASK-QA-005")'), 'Failed');
  assert.equal(page.read('REVIEW.unitSnapshot.passed + REVIEW.unitSnapshot.failed + REVIEW.unitSnapshot.skipped'), 3521);
});

test('legacy planning states never inflate audited progress and remain persistable', () => {
  const page = dashboard(JSON.stringify({'TASK-CEO-001': 'Completed', 'TASK-DEV-031': 'Completed'}));
  assert.equal(page.read('gs("TASK-CEO-001")'), 'Partial');
  assert.equal(page.read('gs("TASK-DEV-031")'), 'Failed');
  const before = page.read('counts(TASKS)');
  page.run('setLocal("TASK-DEV-031", "Completed")');
  assert.deepEqual(page.read('counts(TASKS)'), before);
  const data = page.read('reportData()');
  const task = data.roles.flatMap(r => r.tasks).find(t => t.id === 'TASK-DEV-031');
  assert.equal(task.status, 'Failed');
  assert.equal(task.localTracking, 'Completed');
  assert.equal(JSON.parse(page.saved())['TASK-CEO-001'], 'Completed');
});

test('invalid or unavailable local storage surfaces an error instead of a false success', () => {
  for (const saved of ['{broken', 'null', '[]']) {
    const page = dashboard(saved);
    assert.match(page.elements.get('notice').textContent, /could not be loaded/);
    assert.equal(page.saved(), saved);
    assert.equal(page.read('TASKS.length'), 244);
  }
  const page = dashboard('{}', true);
  page.run('setLocal("TASK-CEO-001", "In Progress")');
  assert.match(page.elements.get('notice').textContent, /could not be saved/);
  assert.equal(page.read('gs("TASK-CEO-001")'), 'Partial');
});

test('combined search, role, audited-status and priority filters preserve global totals', () => {
  const page = dashboard();
  const before = page.read('counts(TASKS)');
  page.run('curRole="DEV"; statusFilter="Failed"; priorityFilter="P1"; q="catalog"; render()');
  assert.deepEqual(page.read('filteredTasks().map(t => t.id)'), ['TASK-DEV-031']);
  assert.match(page.elements.get('visibleCount').textContent, /Showing 1 of 244/);
  page.run('curRole="ALL"; statusFilter="Completed"; priorityFilter="ALL"; q=""; render()');
  assert.equal(page.read('filteredTasks().length'), before.Completed);
  page.run('statusFilter="REMAINING"; render()');
  assert.equal(page.read('filteredTasks().length'), 244 - before.Completed);
  assert.deepEqual(page.read('counts(TASKS)'), before);
});

test('JSON and weekly exports download all statuses, source evidence and remaining actions', () => {
  const page = dashboard();
  page.run('exportJSON(); exportReport()');
  assert.deepEqual(page.downloads, ['eoip-roles-2026-10-21.json', 'eoip-roles-report-2026-10-21.txt']);
  const data = page.read('reportData()');
  assert.equal(data.roles.flatMap(r => r.tasks).length, 244);
  const report = page.read('weeklyReport()');
  for (const task of page.read('TASKS')) {
    assert.ok(report.includes(`[${task.id}]`));
    assert.ok(report.includes(task.remaining));
  }
  assert.match(report, /NOT VERIFIED/);
  assert.match(report, /17 fail/);
  assert.doesNotMatch(html, /fonts\.googleapis/);
});
