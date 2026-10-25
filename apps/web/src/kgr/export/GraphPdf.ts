// FT-D11: real PDF export of the loaded graph (summary, entity table, relationship
// table). Pure TypeScript, no dependency and no HTML, so graph content cannot
// inject markup: every string is escaped as a PDF literal and limited to WinAnsi.
import type {ExportGraph} from './GraphFormats.ts';

const PAGE_WIDTH = 612; // US Letter, points
const PAGE_HEIGHT = 792;
const MARGIN = 48;
const LINE = 13;
const MAX_CHARS = 95;

function pdfText(value: unknown): string {
  const text = String(value ?? '')
    .replace(/[^\x20-\x7e]/g, '?')
    .slice(0, MAX_CHARS);
  return text.replace(/\\/g, '\\\\').replace(/\(/g, '\\(').replace(/\)/g, '\\)');
}

export function graphPdfLines(graph: ExportGraph): {text: string; bold?: boolean}[] {
  const nodes = graph.nodes || [];
  const edges = graph.edges || [];
  const lines: {text: string; bold?: boolean}[] = [
    {text: 'EOIP graph report', bold: true},
    {text: `${nodes.length} entities, ${edges.length} relationships`},
    {text: ''},
    {text: 'Entities (ID | Type | Domain)', bold: true},
  ];
  for (const node of nodes) lines.push({text: `${node.id} | ${node.label ?? ''} | ${node.domain ?? ''}`});
  lines.push({text: ''}, {text: 'Relationships (From -> To : Type)', bold: true});
  for (const edge of edges) lines.push({text: `${edge.from_id} -> ${edge.to_id} : ${edge.type}`});
  return lines;
}

export function graphToPdf(graph: ExportGraph): Uint8Array {
  const lines = graphPdfLines(graph);
  const perPage = Math.floor((PAGE_HEIGHT - 2 * MARGIN) / LINE);
  const pages: {text: string; bold?: boolean}[][] = [];
  for (let i = 0; i < lines.length; i += perPage) pages.push(lines.slice(i, i + perPage));
  if (!pages.length) pages.push([]);

  // Objects: 1 catalog, 2 pages, 3 Helvetica, 4 Helvetica-Bold, then (page, content) pairs.
  const objects: string[] = [];
  const pageIds = pages.map((_, index) => 5 + index * 2);
  objects[1] = '<< /Type /Catalog /Pages 2 0 R >>';
  objects[2] = `<< /Type /Pages /Kids [${pageIds.map(id => `${id} 0 R`).join(' ')}] /Count ${pages.length} >>`;
  objects[3] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>';
  objects[4] = '<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>';
  pages.forEach((pageLines, index) => {
    const pageId = pageIds[index];
    let stream = 'BT\n';
    let y = PAGE_HEIGHT - MARGIN;
    for (const line of pageLines) {
      stream += `/${line.bold ? 'F2' : 'F1'} ${line.bold ? 12 : 9} Tf 1 0 0 1 ${MARGIN} ${y} Tm (${pdfText(line.text)}) Tj\n`;
      y -= LINE;
    }
    stream += `/F1 8 Tf 1 0 0 1 ${MARGIN} ${MARGIN / 2} Tm (Page ${index + 1} of ${pages.length}) Tj\nET`;
    objects[pageId] = `<< /Type /Page /Parent 2 0 R /MediaBox [0 0 ${PAGE_WIDTH} ${PAGE_HEIGHT}] ` +
      `/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents ${pageId + 1} 0 R >>`;
    objects[pageId + 1] = `<< /Length ${stream.length} >>\nstream\n${stream}\nendstream`;
  });

  let out = '%PDF-1.4\n';
  const offsets: number[] = [];
  for (let id = 1; id < objects.length; id++) {
    offsets[id] = out.length;
    out += `${id} 0 obj\n${objects[id]}\nendobj\n`;
  }
  const xref = out.length;
  out += `xref\n0 ${objects.length}\n0000000000 65535 f \n`;
  for (let id = 1; id < objects.length; id++) out += `${String(offsets[id]).padStart(10, '0')} 00000 n \n`;
  out += `trailer\n<< /Size ${objects.length} /Root 1 0 R >>\nstartxref\n${xref}\n%%EOF\n`;
  return new TextEncoder().encode(out); // ASCII only, so byte offsets equal string offsets
}
