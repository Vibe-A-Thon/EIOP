/**
 * Phase 12.2 — Automated Graph Intelligence Report.
 * Generates a comprehensive Markdown report with 7 sections.
 */

function generateOverviewSection(nodes, edges) {
  const nodeCount = nodes.length;
  const edgeCount = edges.length;
  const density = nodeCount > 1 ? (2 * edgeCount) / (nodeCount * (nodeCount - 1)) : 0;
  const labels = {};
  for (const n of nodes) labels[n.label] = (labels[n.label] || 0) + 1;
  const domains = {};
  for (const n of nodes) if (n.domain) domains[n.domain] = (domains[n.domain] || 0) + 1;

  return `## 1. Executive Summary

| Metric | Value |
|---|---|
| Total Nodes | ${nodeCount} |
| Total Edges | ${edgeCount} |
| Graph Density | ${density.toFixed(4)} |
| Entity Types | ${Object.keys(labels).length} |
| Domains | ${Object.keys(domains).length} |

**Entity type breakdown:**
${Object.entries(labels).sort((a, b) => b[1] - a[1]).map(([l, c]) => `- ${l}: ${c}`).join('\n')}

**Domain breakdown:**
${Object.entries(domains).sort((a, b) => b[1] - a[1]).map(([d, c]) => `- ${d}: ${c}`).join('\n') || '- No domain data available'}`;
}

function generateTopologySection(nodes, edges) {
  const adj = {};
  for (const n of nodes) adj[n.id] = {in: 0, out: 0};
  for (const e of edges) {
    if (adj[e.from_id]) adj[e.from_id].out++;
    if (adj[e.to_id]) adj[e.to_id].in++;
  }
  const degrees = Object.values(adj).map(d => d.in + d.out);
  const avgDeg = degrees.length ? degrees.reduce((s, d) => s + d, 0) / degrees.length : 0;
  const maxDeg = Math.max(0, ...degrees);
  const minDeg = Math.min(Infinity, ...degrees);
  const degDist = {};
  for (const d of degrees) degDist[d] = (degDist[d] || 0) + 1;

  return `## 2. Topology Statistics

| Metric | Value |
|---|---|
| Average Degree | ${avgDeg.toFixed(2)} |
| Max Degree | ${maxDeg} |
| Min Degree | ${minDeg === Infinity ? 0 : minDeg} |
| Isolated Nodes | ${degrees.filter(d => d === 0).length} |

**Degree distribution (top 10):**
${Object.entries(degDist).sort((a, b) => Number(a[0]) - Number(b[0])).slice(0, 10).map(([d, c]) => `- Degree ${d}: ${c} nodes`).join('\n')}`;
}

function generateCentralitySection(metrics) {
  if (!metrics || !Object.keys(metrics).length) return '## 3. Centrality Analysis\n\nNo centrality data available. Compute centrality from the Impact tab.';
  const entries = Object.entries(metrics);
  const byDegree = [...entries].sort((a, b) => (b[1].degree || 0) - (a[1].degree || 0)).slice(0, 10);
  const byBetweenness = [...entries].sort((a, b) => (b[1].betweenness || 0) - (a[1].betweenness || 0)).slice(0, 10);
  const byPageRank = [...entries].sort((a, b) => (b[1].page_rank || 0) - (a[1].page_rank || 0)).slice(0, 10);

  return `## 3. Centrality Analysis

**Top 10 by Degree:**
${byDegree.map(([id, m], i) => `${i + 1}. \`${id}\` — degree ${m.degree || 0}`).join('\n')}

**Top 10 by Betweenness:**
${byBetweenness.map(([id, m], i) => `${i + 1}. \`${id}\` — betweenness ${(m.betweenness || 0).toFixed(4)}`).join('\n')}

**Top 10 by PageRank:**
${byPageRank.map(([id, m], i) => `${i + 1}. \`${id}\` — PageRank ${(m.page_rank || 0).toFixed(4)}`).join('\n')}`;
}

function generateCommunitySection(communities) {
  if (!communities || !communities.length) return '## 4. Community Breakdown\n\nNo community data. Run community detection from the Similarity view.';
  return `## 4. Community Breakdown

| Community | Members | Label |
|---|---|---|
${communities.map((c, i) => `| ${i + 1} | ${c.size || c.members?.length || 0} | ${c.label || 'Unlabeled'} |`).join('\n')}

Total communities: ${communities.length}`;
}

function generateEvidenceSection(nodes, edges) {
  const total = edges.length;
  const evidenced = edges.filter(e => e.properties?.source_ref || e.properties?.evidence_key).length;
  const byStatus = {};
  for (const e of edges) {
    const s = e.creation_status || 'UNKNOWN';
    byStatus[s] = (byStatus[s] || 0) + 1;
  }

  return `## 5. Evidence Coverage

| Metric | Value |
|---|---|
| Total Edges | ${total} |
| Evidenced | ${evidenced} (${total ? ((evidenced / total) * 100).toFixed(1) : 0}%) |
| Unevidenced | ${total - evidenced} |

**Creation status distribution:**
${Object.entries(byStatus).sort((a, b) => b[1] - a[1]).map(([s, c]) => `- ${s}: ${c}`).join('\n')}`;
}

function generateHealthSection(nodes, edges) {
  const adj = {};
  for (const n of nodes) adj[n.id] = 0;
  for (const e of edges) {
    if (e.to_id in adj) adj[e.to_id]++;
  }
  const orphaned = Object.entries(adj).filter(([, v]) => v === 0).length;
  const completeness = nodes.length ? ((nodes.length - orphaned) / nodes.length * 100).toFixed(1) : 0;

  return `## 6. Health Assessment

| Metric | Value |
|---|---|
| Completeness | ${completeness}% |
| Orphaned Entities | ${orphaned} |
| Total Nodes | ${nodes.length} |

${orphaned > 0 ? `**Warning:** ${orphaned} orphaned entities detected with zero incoming edges.` : '**Status:** No orphaned entities. Graph connectivity is healthy.'}`;
}

function generateRecommendationsSection(nodes, edges) {
  const recommendations = [];
  const adj = {};
  for (const n of nodes) adj[n.id] = {in: 0, out: 0};
  for (const e of edges) {
    if (adj[e.from_id]) adj[e.from_id].out++;
    if (adj[e.to_id]) adj[e.to_id].in++;
  }
  const orphaned = Object.entries(adj).filter(([, v]) => v.in === 0);
  if (orphaned.length > 0) {
    recommendations.push(`- **Investigate ${orphaned.length} orphaned entities** with zero incoming edges — they may represent dead code or uncovered functionality`);
  }
  const hubs = Object.entries(adj).filter(([, v]) => v.in + v.out > 20).sort((a, b) => (b[1].in + b[1].out) - (a[1].in + a[1].out));
  if (hubs.length > 0) {
    recommendations.push(`- **Review ${hubs.length} high-degree hub nodes** that may be single points of failure: ${hubs.slice(0, 3).map(([id]) => '`' + id + '`').join(', ')}`);
  }
  const unevidenced = edges.filter(e => !e.properties?.source_ref && !e.properties?.evidence_key);
  if (unevidenced.length > edges.length * 0.2) {
    recommendations.push(`- **Improve evidence coverage:** ${unevidenced.length}/${edges.length} edges (${((unevidenced.length / Math.max(edges.length, 1)) * 100).toFixed(0)}%) lack source references`);
  }
  if (!recommendations.length) recommendations.push('- No immediate recommendations. Graph health is good.');

  return `## 7. Actionable Recommendations\n\n${recommendations.join('\n')}`;
}

export function generateGraphReport(nodes, edges, options = {}) {
  const {metrics = {}, communities = []} = options;
  const sections = [
    generateOverviewSection(nodes, edges),
    generateTopologySection(nodes, edges),
    generateCentralitySection(metrics),
    generateCommunitySection(communities),
    generateEvidenceSection(nodes, edges),
    generateHealthSection(nodes, edges),
    generateRecommendationsSection(nodes, edges),
  ];
  const date = new Date().toISOString().slice(0, 10);
  return `# KGR Graph Intelligence Report\n\n**Generated:** ${date}  \n**Nodes:** ${nodes.length} | **Edges:** ${edges.length}\n\n---\n\n${sections.join('\n\n---\n\n')}`;
}
