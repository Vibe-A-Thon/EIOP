import assert from 'node:assert/strict';
import {test} from 'node:test';
import {graphToPdf, graphPdfLines} from '../../src/kgr/export/GraphPdf.ts';

const decode = bytes => new TextDecoder().decode(bytes);

test('graphToPdf produces a structurally valid PDF with a correct xref table', () => {
  const graph = {nodes: [{id: 'urn:a', label: 'Service', domain: 'ENG'}, {id: 'urn:b', label: 'Team'}],
    edges: [{from_id: 'urn:a', to_id: 'urn:b', type: 'OWNED_BY'}]};
  const pdf = decode(graphToPdf(graph));
  assert.ok(pdf.startsWith('%PDF-1.4\n'));
  assert.ok(pdf.endsWith('%%EOF\n'));
  const startxref = Number(pdf.match(/startxref\n(\d+)/)[1]);
  assert.equal(pdf.slice(startxref, startxref + 4), 'xref');
  const offsets = [...pdf.matchAll(/^(\d{10}) 00000 n $/gm)].map(m => Number(m[1]));
  offsets.forEach((offset, index) => assert.ok(pdf.startsWith(`${index + 1} 0 obj`, offset)));
  assert.match(pdf, /\(urn:a \| Service \| ENG\) Tj/);
  assert.match(pdf, /\(urn:a -> urn:b : OWNED_BY\) Tj/);
});

test('graph strings cannot break out of PDF string literals', () => {
  const pdf = decode(graphToPdf({nodes: [{id: 'x) Tj /Evil (y\\', label: 'L'}], edges: []}));
  assert.match(pdf, /\(x\\\) Tj \/Evil \\\(y\\\\ \| L \| \) Tj/);
});

test('large graphs paginate', () => {
  const nodes = Array.from({length: 200}, (_, i) => ({id: `urn:n${i}`, label: 'N'}));
  const pdf = decode(graphToPdf({nodes, edges: []}));
  const pages = Number(pdf.match(/\/Count (\d+)/)[1]);
  assert.ok(pages >= 4, `expected several pages, got ${pages}`);
  assert.equal(graphPdfLines({nodes, edges: []}).length, 206);
});
