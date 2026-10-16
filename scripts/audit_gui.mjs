import {createHash} from 'node:crypto';
import {mkdir, readFile, readdir, writeFile} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath, pathToFileURL} from 'node:url';

export function markdownCells(line) {
  const result = [];
  let current = '', code = false, escaped = false;
  for (const char of line.trim()) {
    if (escaped) {current += char; escaped = false;}
    else if (char === '\\') {current += char; escaped = true;}
    else if (char === '`') {current += char; code = !code;}
    else if (char === '|' && !code) {result.push(current.trim()); current = '';}
    else current += char;
  }
  result.push(current.trim());
  return result.slice(1, -1);
}

const sha = value => createHash('sha256').update(value).digest('hex');

export function sourceRegistry(buffer) {
  const text = buffer.toString('utf8').replaceAll('\r\n', '\n');
  const lines = text.split('\n');
  if (lines.at(-1) === '') lines.pop();
  const intake = [], sections = [], screens = [], integrations = [], backends = [];
  for (let index = 0; index < lines.length; index++) {
    const line = index + 1, content = lines[index];
    if (content.trim()) intake.push({id: `GUI-SOURCE-L${String(line).padStart(4, '0')}`, line, text: content,
      classification: 'UNTRIAGED', acceptance_status: 'NOT_EVALUATED'});
    if (/^## \d+\./.test(content)) sections.push({line, title: content.slice(3)});
    if (/^### SCR-\d{3} - /.test(content)) screens.push({id: content.match(/SCR-\d{3}/)[0], line, title: content.slice(4)});
    if (!content.startsWith('|')) continue;
    const cells = markdownCells(content);
    if (/^`INT-\d{3}`$/.test(cells[0] || '')) {
      if (cells.length !== 12) throw new Error(`Integration row ${line} has ${cells.length} cells`);
      integrations.push({id: cells[0].replaceAll('`', ''), line, method_path: cells[2],
        source_screens: cells[11], disposition: 'OPEN_CONTRACT_REVIEW'});
    }
    if (/^`BACKEND-MISSING-\d{3}`$/.test(cells[0] || '')) backends.push({id: cells[0].replaceAll('`', ''), line,
      proposed_contract: cells[1], screens: cells[3], status: 'NOT_EVALUATED'});
  }
  for (const [records, prefix, count] of [[screens, 'SCR-', 27], [integrations, 'INT-', 735], [backends, 'BACKEND-MISSING-', 20]]) {
    const ids = new Set(records.map(item => item.id));
    if (records.length !== count || ids.size !== count || Array.from({length: count}, (_, index) => `${prefix}${String(index + 1).padStart(3, '0')}`).some(id => !ids.has(id))) {
      throw new Error(`${prefix} baseline changed; review source scope before regenerating`);
    }
  }
  if (sections.length !== 23) throw new Error('Source section count changed');
  return {schema_version: 'gui-source-intake-v1', source: 'GUI-UIX-requirements.md',
    source_sha256_lf: sha(text), source_lines: lines.length,
    notice: 'Structural intake only. Source lines are not decomposed acceptance clauses; no behavior or completion is inferred.',
    sections, screens, integrations, backends, intake};
}

async function filesUnder(directory) {
  const entries = await readdir(directory, {withFileTypes: true});
  const nested = await Promise.all(entries.map(entry => entry.isDirectory()
    ? filesUnder(path.join(directory, entry.name)) : [path.join(directory, entry.name)]));
  return nested.flat().sort();
}

export async function frontendInventory(root) {
  const files = await filesUnder(path.join(root, 'apps/web/src'));
  const patterns = {
    persistent_browser_data: /(?:localStorage|sessionStorage)\./,
    direct_transport: /(?:\bfetch\(|new WebSocket\()/,
    raw_html: /dangerouslySetInnerHTML|\.innerHTML\s*=|document\.write\(/,
    discarded_error: /\.catch\(\(\) => (?:null|\(\{\}\))\)/,
    nondeterminism: /Math\.random\(/,
  };
  const inventory = [];
  for (const file of files) {
    const bytes = await readFile(file), text = bytes.toString('utf8');
    const lines = text.split(/\r?\n/);
    const observations = [];
    for (const [kind, pattern] of Object.entries(patterns)) {
      lines.forEach((line, index) => {if (pattern.test(line)) observations.push({kind, line: index + 1});});
    }
    inventory.push({path: path.relative(root, file).replaceAll('\\', '/'), bytes: bytes.length,
      lines: lines.length - (text.endsWith('\n') ? 1 : 0), sha256: sha(bytes), observations});
  }
  return {schema_version: 'gui-source-inventory-v1', notice: 'Pattern observations require human review; they are neither defects nor execution evidence by themselves.', files: inventory};
}

async function main() {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const registryPath = path.join(root, 'config/verification/gui-source-registry.json');
  const registry = sourceRegistry(await readFile(path.join(root, 'GUI-UIX-requirements.md')));
  const serialized = JSON.stringify(registry, null, 2) + '\n';
  if (process.argv.includes('--check')) {
    if ((await readFile(registryPath, 'utf8')).replaceAll('\r\n', '\n') !== serialized) throw new Error('GUI source registry is stale');
  } else {
    await mkdir(path.dirname(registryPath), {recursive: true});
    await writeFile(registryPath, serialized);
  }
  const output = path.join(root, 'test-results/gui-source-inventory.json');
  await mkdir(path.dirname(output), {recursive: true});
  const inventory = await frontendInventory(root);
  await writeFile(output, JSON.stringify(inventory, null, 2) + '\n');
  console.log(JSON.stringify({source_lines: registry.source_lines, screens: registry.screens.length,
    integrations: registry.integrations.length, missing_contracts: registry.backends.length,
    unmapped_integrations: registry.integrations.filter(item => item.source_screens === 'No primary screen assigned').length,
    intake_units: registry.intake.length, frontend_files: inventory.files.length,
    frontend_lines: inventory.files.reduce((total, file) => total + file.lines, 0),
    registry: path.relative(root, registryPath), inventory: path.relative(root, output)}, null, 2));
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch(error => {console.error(error.message); process.exitCode = 1;});
}
