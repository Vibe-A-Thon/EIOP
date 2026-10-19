"""Self-contained offline HTML ledger export with interactive filtering (T-212 / REVA-PD-011)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from reva.pd.ledger import LedgerRecord


def render_ledger_html(ledger: LedgerRecord) -> str:
    """Generate self-contained HTML report with embedded JSON and zero network calls."""
    ledger_data = ledger.canonical_dict()
    ledger_json = json.dumps(ledger_data, indent=2, default=str)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline';">
  <title>REVA Proof-of-Done Ledger — {ledger.ledger_id}</title>
  <style>
    :root {{
      --bg: #0d1117;
      --card-bg: #161b22;
      --border: #30363d;
      --text: #c9d1d9;
      --text-heading: #f0f6fc;
      --accent: #58a6ff;
      --green: #238636;
      --red: #da3633;
      --orange: #d29922;
      --purple: #8957e5;
    }}
    @media (prefers-color-scheme: light) {{
      :root {{
        --bg: #f6f8fa;
        --card-bg: #ffffff;
        --border: #d0d7de;
        --text: #24292f;
        --text-heading: #1f2328;
        --accent: #0969da;
        --green: #1a7f37;
        --red: #cf222e;
        --orange: #9a6700;
        --purple: #8250df;
      }}
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
    body {{ background: var(--bg); color: var(--text); padding: 24px; line-height: 1.5; }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    header {{ margin-bottom: 24px; border-bottom: 1px solid var(--border); padding-bottom: 16px; }}
    h1 {{ color: var(--text-heading); font-size: 24px; display: flex; align-items: center; gap: 12px; }}
    .ledger-badge {{ font-size: 13px; font-weight: normal; background: var(--card-bg); border: 1px solid var(--border); padding: 4px 8px; border-radius: 6px; }}
    .meta-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; margin-top: 16px; font-size: 13px; }}
    .meta-item {{ background: var(--card-bg); padding: 12px; border-radius: 6px; border: 1px solid var(--border); }}
    .meta-label {{ color: #8b949e; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }}
    .meta-val {{ font-weight: 600; color: var(--text-heading); margin-top: 4px; font-family: monospace; word-break: break-all; }}
    .stats-row {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(130px, 1fr)); gap: 12px; margin: 24px 0; }}
    .stat-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 6px; padding: 16px; text-align: center; cursor: pointer; transition: transform 0.1s; }}
    .stat-card:hover {{ transform: translateY(-2px); }}
    .stat-card.active {{ border-color: var(--accent); }}
    .stat-num {{ font-size: 28px; font-weight: bold; color: var(--text-heading); }}
    .stat-closed .stat-num {{ color: var(--green); }}
    .stat-failed .stat-num {{ color: var(--red); }}
    .stat-blocked .stat-num {{ color: var(--orange); }}
    .stat-open .stat-num {{ color: var(--accent); }}
    .toolbar {{ display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }}
    .search-input {{ background: var(--card-bg); border: 1px solid var(--border); color: var(--text); padding: 8px 12px; border-radius: 6px; flex: 1; min-width: 200px; }}
    table {{ width: 100%; border-collapse: collapse; background: var(--card-bg); border: 1px solid var(--border); border-radius: 6px; overflow: hidden; }}
    th, td {{ padding: 12px 16px; text-align: left; border-bottom: 1px solid var(--border); font-size: 14px; }}
    th {{ background: rgba(0,0,0,0.1); color: var(--text-heading); font-weight: 600; }}
    .badge {{ display: inline-block; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 700; text-transform: uppercase; }}
    .badge-closed {{ background: rgba(35, 134, 54, 0.2); color: var(--green); border: 1px solid var(--green); }}
    .badge-open {{ background: rgba(88, 166, 255, 0.2); color: var(--accent); border: 1px solid var(--accent); }}
    .badge-failed {{ background: rgba(218, 54, 51, 0.2); color: var(--red); border: 1px solid var(--red); }}
    .badge-blocked {{ background: rgba(210, 153, 34, 0.2); color: var(--orange); border: 1px solid var(--orange); }}
    .badge-stale, .badge-flaky, .badge-unknown {{ background: rgba(137, 87, 229, 0.2); color: var(--purple); border: 1px solid var(--purple); }}
    .row-clickable {{ cursor: pointer; }}
    .row-clickable:hover {{ background: rgba(255,255,255,0.03); }}
    .drawer {{ display: none; background: rgba(0,0,0,0.2); padding: 16px; border-top: 1px dashed var(--border); }}
    .drawer-active {{ display: table-row; }}
    .checks-list {{ margin-top: 8px; display: grid; gap: 6px; font-size: 13px; }}
    .check-item {{ display: flex; align-items: center; gap: 8px; }}
    .check-pass {{ color: var(--green); }}
    .check-fail {{ color: var(--red); }}
  </style>
</head>
<body>
  <div class="container">
    <header>
      <h1>
        REVA Proof-of-Done Ledger
        <span class="ledger-badge">{ledger.ledger_id}</span>
      </h1>
      <div class="meta-grid">
        <div class="meta-item">
          <div class="meta-label">Scope</div>
          <div class="meta-val">{ledger.scope}</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Commit</div>
          <div class="meta-val">{ledger.commit[:12] if len(ledger.commit) >= 12 else ledger.commit}</div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Completion Status</div>
          <div class="meta-val" style="color: {'var(--green)' if ledger.complete else 'var(--orange)'}">
            {'COMPLETE (100%)' if ledger.complete else 'INCOMPLETE'}
          </div>
        </div>
        <div class="meta-item">
          <div class="meta-label">Timestamp</div>
          <div class="meta-val">{ledger.created_at}</div>
        </div>
      </div>
    </header>

    <div class="stats-row">
      <div class="stat-card" data-filter="all">
        <div class="stat-num">{len(ledger.closures)}</div>
        <div class="meta-label">Total Obligations</div>
      </div>
      <div class="stat-card stat-closed active" data-filter="closed">
        <div class="stat-num">{ledger.summary.get('closed', 0)}</div>
        <div class="meta-label">Closed</div>
      </div>
      <div class="stat-card stat-open" data-filter="open">
        <div class="stat-num">{ledger.summary.get('open', 0)}</div>
        <div class="meta-label">Open</div>
      </div>
      <div class="stat-card stat-blocked" data-filter="blocked">
        <div class="stat-num">{ledger.summary.get('blocked', 0)}</div>
        <div class="meta-label">Blocked</div>
      </div>
      <div class="stat-card stat-failed" data-filter="failed">
        <div class="stat-num">{ledger.summary.get('failed', 0)}</div>
        <div class="meta-label">Failed</div>
      </div>
    </div>

    <div class="toolbar">
      <input type="text" id="searchInput" class="search-input" placeholder="Filter by obligation key or reasons...">
    </div>

    <table id="ledgerTable">
      <thead>
        <tr>
          <th>Obligation Key</th>
          <th>Version</th>
          <th>Outcome</th>
          <th>Reason Codes</th>
          <th>Closure ID</th>
        </tr>
      </thead>
      <tbody id="tableBody"></tbody>
    </table>
  </div>

  <script type="application/json" id="reva-ledger">
{ledger_json}
  </script>

  <script>
    (function() {{
      const raw = document.getElementById("reva-ledger").textContent;
      const data = JSON.parse(raw);
      const closures = data.closures || [];
      let currentFilter = "all";
      let searchQuery = "";

      const tbody = document.getElementById("tableBody");
      const searchInput = document.getElementById("searchInput");
      const statCards = document.querySelectorAll(".stat-card");

      function render() {{
        tbody.innerHTML = "";
        const filtered = closures.filter(c => {{
          const matchesFilter = (currentFilter === "all") || (c.outcome === currentFilter);
          const text = (c.obligation_key + " " + (c.reasons || []).join(" ")).toLowerCase();
          const matchesSearch = !searchQuery || text.includes(searchQuery);
          return matchesFilter && matchesSearch;
        }});

        filtered.forEach((c, idx) => {{
          const tr = document.createElement("tr");
          tr.className = "row-clickable";
          const reasons = (c.reasons && c.reasons.length) ? c.reasons.join(", ") : "—";
          tr.innerHTML = `
            <td><code>${{c.obligation_key}}</code></td>
            <td>v${{c.obligation_version}}</td>
            <td><span class="badge badge-${{c.outcome}}">${{c.outcome}}</span></td>
            <td>${{reasons}}</td>
            <td><small><code>${{c.closure_id || "—"}}</code></small></td>
          `;

          const drawerTr = document.createElement("tr");
          drawerTr.className = "drawer";
          const checks = c.checks || [];
          const checksHtml = checks.map(ck => `
            <div class="check-item">
              <span class="${{ck.status === 'pass' ? 'check-pass' : 'check-fail'}}">●</span>
              <strong>${{ck.check}}</strong>: ${{ck.details || ck.status}}
            </div>
          `).join("");

          drawerTr.innerHTML = `
            <td colspan="5">
              <strong>Evaluation Checks:</strong>
              <div class="checks-list">${{checksHtml || "No check details recorded"}}</div>
            </td>
          `;

          tr.addEventListener("click", () => {{
            drawerTr.classList.toggle("drawer-active");
          }});

          tbody.appendChild(tr);
          tbody.appendChild(drawerTr);
        }});
      }}

      statCards.forEach(card => {{
        card.addEventListener("click", () => {{
          statCards.forEach(c => c.classList.remove("active"));
          card.classList.add("active");
          currentFilter = card.getAttribute("data-filter");
          render();
        }});
      }});

      searchInput.addEventListener("input", (e) => {{
        searchQuery = e.target.value.toLowerCase().trim();
        render();
      }});

      render();
    }})();
  </script>
</body>
</html>
"""


def export_ledger_html(ledger: LedgerRecord, output_path: Union[str, Path]) -> None:
    """Write self-contained HTML ledger file to destination path."""
    html_content = render_ledger_html(ledger)
    Path(output_path).write_text(html_content, encoding="utf-8")
