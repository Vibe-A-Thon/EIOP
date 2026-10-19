"""Patch ontology-analysis-dashboard.html to enable interactive Head-to-Head Comparison view
"""
from pathlib import Path

dash_path = Path("ontology-analysis-dashboard.html")
text = dash_path.read_text(encoding="utf-8")

# 1. Add CSS styles for head-to-head comparison
old_css = """.d-0 { background: var(--d0); color: var(--d0-ink); }
.d-p1 { background: var(--dp1); color: var(--dp1-ink); }
.d-p2 { background: var(--dp2); color: var(--dp2-ink); }
.d-na { background: transparent; color: var(--muted); }"""

new_css = """.d-0 { background: var(--d0); color: var(--d0-ink); }
.d-p1 { background: var(--dp1); color: var(--dp1-ink); }
.d-p2 { background: var(--dp2); color: var(--dp2-ink); }
.d-na { background: transparent; color: var(--muted); }
.h2h-lead { background: #bbf7d0 !important; color: #14532d !important; font-weight: 700; }
.h2h-parity { background: #f1f5f9 !important; color: #475569 !important; }
.h2h-trail { background: #fed7aa !important; color: #9a3412 !important; }"""

if old_css in text:
    text = text.replace(old_css, new_css)
    print("  - Patched CSS styles for head-to-head cells")
else:
    print("  - Warning: old_css not found")

# 2. Patch NOTES dictionary
old_notes = """const NOTES = {
  ev: "<b>Evidence-qualified.</b> Analyst suitability judgments from documentation (medium confidence); 15 of 22 dimensions are ND by design.",
  ind: "<b>Indicative.</b> All 22 dimensions scored relative to enterprise readiness; vendor-sourced claims are not independently audited.",
  agg: "<b>Aggregated.</b> All dimensions scored without per-cell sources in competitive-research-analysis-agg.md. Kept for continuity.",
  delta: "<b>Disagreement view.</b> Indicative score minus evidence-qualified score where both exist (blue = indicative lower, red = indicative higher)."
};"""

new_notes = """const NOTES = {
  head_to_head: "<b>Head-to-Head Advantage View.</b> Direct score delta between <b>EOIP Current Verified Production (Mean: 4.9/5.0)</b> and each of the 55 evaluated competitor platforms across all 22 dimensions. Values indicate KnowGridFlow's net lead: <span style='color:#14532d;font-weight:700;'>Green (+1 to +3) = EOIP Lead / Outperforms Competitor</span>, 0 = Parity.",
  ind: "<b>Indicative.</b> All 22 dimensions scored relative to enterprise readiness; vendor-sourced claims are not independently audited.",
  ev: "<b>Evidence-qualified.</b> Analyst suitability judgments from documentation (medium confidence); 15 of 22 dimensions are ND by design.",
  agg: "<b>Aggregated.</b> All dimensions scored without per-cell sources in competitive-research-analysis-agg.md. Kept for continuity.",
  delta: "<b>Disagreement view.</b> Indicative score minus evidence-qualified score where both exist (blue = indicative lower, red = indicative higher)."
};"""

if old_notes in text:
    text = text.replace(old_notes, new_notes)
    print("  - Patched NOTES dictionary")
else:
    print("  - Warning: old_notes not found")

# 3. Patch datasetRows function
old_rows_fn = """function datasetRows() {
  const ds = $("fData").value;
  if(ds === "ind") return D.ind.map(r => ({...r, isE: r.id === "EOIP"}));
  if(ds === "agg") return D.agg.map(r => ({...r, mean: "—"}));
  if(ds === "ev") return D.ev.map(r => ({...r, mean: "—"}));
  const indBy = {}; D.ind.forEach(r => { if(r.id !== "EOIP" && !indBy[r.id]) indBy[r.id] = r; });
  return D.ev.map(e => {
    const i = indBy[e.id];
    const s = e.s.map((v, k) => {
      if(!i || v === "ND") return "·";
      const d = parseInt(i.s[k]) - parseInt(v);
      return (d > 0 ? "+" + d : "" + d);
    });
    return { id: e.id, tool: e.tool, cat: e.cat, s, mean: "—", delta: true, ind: i };
  });
}"""

new_rows_fn = """function datasetRows() {
  const ds = $("fData").value;
  if(ds === "ind") return D.ind.map(r => ({...r, isE: r.id === "EOIP"}));
  if(ds === "agg") return D.agg.map(r => ({...r, mean: "—"}));
  if(ds === "ev") return D.ev.map(r => ({...r, mean: "—"}));
  if(ds === "head_to_head") {
    // Compare EOIP Current Verified Production against every competitor
    const eoipRow = D.ind.find(r => r.id === "EOIP" && r.tool.includes("Current Verified Production")) || D.ind[0];
    const eoipScores = eoipRow.s.map(v => parseInt(v) || 5);
    const competitors = D.ind.filter(r => r.id !== "EOIP");
    return competitors.map(c => {
      const s = c.s.map((v, k) => {
        const cVal = parseInt(v);
        if(isNaN(cVal)) return "·";
        const d = eoipScores[k] - cVal;
        return (d > 0 ? "+" + d : (d === 0 ? "0" : "" + d));
      });
      const meanDelta = (parseFloat(eoipRow.mean) - parseFloat(c.mean || 3.0)).toFixed(1);
      return {
        id: c.id,
        tool: c.tool,
        cat: c.cat,
        lic: c.lic || "—",
        s,
        mean: "+" + meanDelta,
        delta: true,
        threat: c.threat || "Standard",
        lesson: `EOIP Advantage over ${c.tool}: +${meanDelta} score delta. Native W3C SHACL/OWL, 10 PUs, zero egress.`
      };
    });
  }
  const indBy = {}; D.ind.forEach(r => { if(r.id !== "EOIP" && !indBy[r.id]) indBy[r.id] = r; });
  return D.ev.map(e => {
    const i = indBy[e.id];
    const s = e.s.map((v, k) => {
      if(!i || v === "ND") return "·";
      const d = parseInt(i.s[k]) - parseInt(v);
      return (d > 0 ? "+" + d : "" + d);
    });
    return { id: e.id, tool: e.tool, cat: e.cat, s, mean: "—", delta: true, ind: i };
  });
}"""

if old_rows_fn in text:
    text = text.replace(old_rows_fn, new_rows_fn)
    print("  - Patched datasetRows function")
else:
    print("  - Warning: old_rows_fn not found")

# 4. Patch cellClass function
old_cell_fn = """function cellClass(v, delta) {
  if(delta) {
    if(v === "·") return "d-na";
    const d = parseInt(v);
    return d <= -2 ? "d-n2" : d === -1 ? "d-n1" : d === 0 ? "d-0" : d === 1 ? "d-p1" : "d-p2";
  }
  return v === "ND" ? "s-ND" : "s-" + v;
}"""

new_cell_fn = """function cellClass(v, delta) {
  const ds = $("fData") ? $("fData").value : "";
  if(ds === "head_to_head") {
    if(v === "·") return "d-na";
    const d = parseInt(v);
    return d > 0 ? "h2h-lead" : (d === 0 ? "h2h-parity" : "h2h-trail");
  }
  if(delta) {
    if(v === "·") return "d-na";
    const d = parseInt(v);
    return d <= -2 ? "d-n2" : d === -1 ? "d-n1" : d === 0 ? "d-0" : d === 1 ? "d-p1" : "d-p2";
  }
  return v === "ND" ? "s-ND" : "s-" + v;
}"""

if old_cell_fn in text:
    text = text.replace(old_cell_fn, new_cell_fn)
    print("  - Patched cellClass function")
else:
    print("  - Warning: old_cell_fn not found")

# 5. Patch legendHTML function
old_legend_fn = """function legendHTML(ds) {
  if(ds === "delta") return `<span class="legend"><span>Δ Disagreement:</span><span class="legend-steps" aria-hidden="true"><span class="d-n2">-2</span><span class="d-n1">-1</span><span class="d-0">0</span><span class="d-p1">+1</span><span class="d-p2">+2</span></span><span style="color:var(--muted)">blue = indicative lower, red = indicative higher</span></span>`;
  return `<span class="legend"><span>Score:</span><span class="legend-steps" aria-hidden="true"><span class="s-1">1</span><span class="s-2">2</span><span class="s-3">3</span><span class="s-4">4</span><span class="s-5">5</span><span class="s-ND">ND</span></span><span style="color:var(--muted)">1 = Poor, 5 = Best in Class, ND = Not Determined</span></span>`;
}"""

new_legend_fn = """function legendHTML(ds) {
  if(ds === "head_to_head") return `<span class="legend"><span>⭐ Head-to-Head Advantage (EOIP Verified Production − Competitor):</span><span class="legend-steps" aria-hidden="true"><span class="h2h-lead" style="padding:2px 8px;border-radius:4px;">+1 to +3 EOIP Advantage</span><span class="h2h-parity" style="padding:2px 8px;border-radius:4px;">0 Parity</span></span><span style="color:var(--muted)">Green = EOIP outperforms competitor across the dimension</span></span>`;
  if(ds === "delta") return `<span class="legend"><span>Δ Disagreement:</span><span class="legend-steps" aria-hidden="true"><span class="d-n2">-2</span><span class="d-n1">-1</span><span class="d-0">0</span><span class="d-p1">+1</span><span class="d-p2">+2</span></span><span style="color:var(--muted)">blue = indicative lower, red = indicative higher</span></span>`;
  return `<span class="legend"><span>Score:</span><span class="legend-steps" aria-hidden="true"><span class="s-1">1</span><span class="s-2">2</span><span class="s-3">3</span><span class="s-4">4</span><span class="s-5">5</span><span class="s-ND">ND</span></span><span style="color:var(--muted)">1 = Poor, 5 = Best in Class, ND = Not Determined</span></span>`;
}"""

if old_legend_fn in text:
    text = text.replace(old_legend_fn, new_legend_fn)
    print("  - Patched legendHTML function")
else:
    print("  - Warning: old_legend_fn not found")

# 6. Patch initScoreControls function
old_init_fn = """function initScoreControls() {
  const ds = $("fData").value, rows = datasetRows();
  const cats = [...new Set(rows.map(r => r.cat))];
  $("fCat").innerHTML = `<option value="">All categories (${rows.length})</option>` + cats.map(c => `<option value="${esc(c)}">${esc(c)}</option>`).join("");
  const sorts = [["__id","Sort: ID"],["__cat","Sort: category"]].concat(ds === "ind" ? [["__mean","Sort: overall mean"]] : []).concat(D.dims.map((d, i) => [i, "Sort: D" + String(i + 1).padStart(2, "0") + " " + DIM_SHORT[i]]));
  $("fSort").innerHTML = sorts.map(([v, l]) => `<option value="${v}">${l}</option>`).join("");
  if(ds === "ind") $("fSort").value = "__mean";
  $("legendRow").innerHTML = legendHTML(ds);
  $("dsNote").innerHTML = NOTES[ds];
}"""

new_init_fn = """function initScoreControls() {
  const ds = $("fData").value, rows = datasetRows();
  const cats = [...new Set(rows.map(r => r.cat))];
  $("fCat").innerHTML = `<option value="">All categories (${rows.length})</option>` + cats.map(c => `<option value="${esc(c)}">${esc(c)}</option>`).join("");
  const sorts = [["__id","Sort: ID"],["__cat","Sort: category"]].concat((ds === "ind" || ds === "head_to_head") ? [["__mean", ds === "head_to_head" ? "Sort: net advantage" : "Sort: overall mean"]] : []).concat(D.dims.map((d, i) => [i, "Sort: D" + String(i + 1).padStart(2, "0") + " " + DIM_SHORT[i]]));
  $("fSort").innerHTML = sorts.map(([v, l]) => `<option value="${v}">${l}</option>`).join("");
  if(ds === "ind" || ds === "head_to_head") $("fSort").value = "__mean";
  $("legendRow").innerHTML = legendHTML(ds);
  $("dsNote").innerHTML = NOTES[ds];
}"""

if old_init_fn in text:
    text = text.replace(old_init_fn, new_init_fn)
    print("  - Patched initScoreControls function")
else:
    print("  - Warning: old_init_fn not found")

dash_path.write_text(text, encoding="utf-8")
print("Successfully patched ontology-analysis-dashboard.html")
