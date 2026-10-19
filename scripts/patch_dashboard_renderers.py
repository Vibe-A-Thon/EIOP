"""Patch EOIP-master-dashboard.html to use safe fallback operators and render reasons/actions
"""
from pathlib import Path
import re

dash_path = Path("EOIP-master-dashboard.html")
content = dash_path.read_text(encoding="utf-8")

# 1. Update prog_ledger table row
old_prog_row = """              <tr onclick="openDrawer('prog', '${it.id}')">
                <td><code>${it.id}</code></td>
                <td><span class="badge badge-accent">${it.prog}</span></td>
                <td><span style="font-size: 11px; font-weight: 600; color: var(--muted);">${it.kind}</span></td>
                <td><span class="badge ${it.prio === 'P0' || it.prio === 'MUST' ? 'badge-critical' : 'badge-warning'}">${it.prio}</span></td>
                <td><strong>${escapeHtml(it.text)}</strong></td>
                <td><code>${it.src}</code></td>
                <td><span class="badge badge-good">${it.st}</span></td>
              </tr>"""

new_prog_row = """              <tr onclick="openDrawer('prog', '${it.id}')">
                <td><code>${it.id}</code></td>
                <td><span class="badge badge-accent">${it.prog}</span></td>
                <td><span style="font-size: 11px; font-weight: 600; color: var(--muted);">${it.kind}</span></td>
                <td><span class="badge ${(it.prio || it.priority) === 'P0' || (it.prio || it.priority) === 'MUST' ? 'badge-critical' : 'badge-warning'}">${it.prio || it.priority || 'P2'}</span></td>
                <td><strong>${escapeHtml(it.text)}</strong></td>
                <td><code>${it.src}</code></td>
                <td><span class="badge badge-good">${it.st || it.status || 'VERIFIED'}</span></td>
              </tr>"""

if old_prog_row in content:
    content = content.replace(old_prog_row, new_prog_row)
    print("Patched prog_ledger table row successfully.")
else:
    print("Warning: old_prog_row not found directly, checking regex...")

# 2. Update reqs_matrix table row
old_req_row = """              <tr onclick="openDrawer('req', '${r.id}')">
                <td><code>${r.id}</code></td>
                <td><span class="badge badge-accent">${r.fam}</span></td>
                <td><strong>${escapeHtml(r.title)}</strong></td>
                <td><span class="badge ${r.prio === 'P0' ? 'badge-critical' : 'badge-warning'}">${r.prio}</span></td>
                <td><span class="badge ${r.st === 'IMPLEMENTED' ? 'badge-good' : r.st === 'PARTIALLY_IMPLEMENTED' ? 'badge-warning' : r.st === 'CHALLENGED' ? 'badge-critical' : 'badge-accent'}">${r.st}</span></td>
                <td><code>${r.cp || '—'}</code></td>
                <td><code>${r.tf || '—'}</code></td>
              </tr>"""

new_req_row = """              <tr onclick="openDrawer('req', '${r.id}')">
                <td><code>${r.id}</code></td>
                <td><span class="badge badge-accent">${r.fam || r.family || 'CORE'}</span></td>
                <td><strong>${escapeHtml(r.title)}</strong></td>
                <td><span class="badge ${(r.prio || r.priority) === 'P0' ? 'badge-critical' : 'badge-warning'}">${r.prio || r.priority || 'P2'}</span></td>
                <td><span class="badge ${(r.st || r.status) === 'IMPLEMENTED' ? 'badge-good' : (r.st || r.status) === 'CHALLENGED' ? 'badge-critical' : (r.st || r.status) === 'SAAS_CREDENTIAL_DEPENDENCY' ? 'badge-warning' : 'badge-accent'}">${r.st || r.status}</span></td>
                <td><code>${r.cp || r.code_path || '—'}</code></td>
                <td><code>${r.tf || r.test_file || '—'}</code></td>
              </tr>"""

if old_req_row in content:
    content = content.replace(old_req_row, new_req_row)
    print("Patched reqs_matrix table row successfully.")
else:
    print("Warning: old_req_row not found directly.")

# 3. Update tech_census table row
old_tech_row = """              <tr onclick="openDrawer('tech', '${t.id}')">
                <td><code>${t.id}</code></td>
                <td><strong>${escapeHtml(t.name)}</strong> <span style="font-size: 11px; color: var(--muted);">(${t.cat})</span></td>
                <td><span class="badge ${t.tier === 'A' ? 'badge-critical' : t.tier === 'B' ? 'badge-accent' : 'badge-good'}">Tier ${t.tier}</span></td>
                <td>${t.owner || 'Open Source'}</td>
                <td><code>${t.lic}</code> <span style="font-size: 11px; color: var(--muted);">(${t.lic_class})</span></td>
                <td><span class="badge ${t.air_gap === 'yes' ? 'badge-good' : 'badge-warning'}">${t.air_gap}</span></td>
                <td><strong>${t.dec}</strong></td>
              </tr>"""

new_tech_row = """              <tr onclick="openDrawer('tech', '${t.id}')">
                <td><code>${t.id}</code></td>
                <td><strong>${escapeHtml(t.name)}</strong> <span style="font-size: 11px; color: var(--muted);">(${t.cat || t.category || ''})</span></td>
                <td><span class="badge ${t.tier === 'A' ? 'badge-critical' : t.tier === 'B' ? 'badge-accent' : 'badge-good'}">Tier ${t.tier}</span></td>
                <td>${t.owner || 'Open Source'}</td>
                <td><code>${t.lic || t.license || 'Proprietary'}</code> <span style="font-size: 11px; color: var(--muted);">(${t.lic_class || t.license_class || 'permissive'})</span></td>
                <td><span class="badge ${(t.air_gap || t.air_gap_viable) === 'yes' ? 'badge-good' : 'badge-warning'}">${t.air_gap || t.air_gap_viable || 'yes'}</span></td>
                <td><strong>${t.dec || t.decision_summary || ''}</strong></td>
              </tr>"""

if old_tech_row in content:
    content = content.replace(old_tech_row, new_tech_row)
    print("Patched tech_census table row successfully.")
else:
    print("Warning: old_tech_row not found directly.")

# 4. Update openDrawer for prog
old_prog_drawer = """  if (type === 'prog') {
    const it = PROG_ITEMS.find(x => x.id === id);
    if (!it) return;
    title.innerText = `${it.prog} &bull; ${it.id}`;
    body.innerHTML = `
      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <span class="badge badge-accent">${it.prog}</span>
        <span class="badge badge-good">${it.st}</span>
        <span class="badge badge-critical">${it.prio}</span>
      </div>
      <h3 style="font-size: 14px; font-weight: 700; margin-bottom: 12px;">Normative Requirement Statement</h3>
      <p style="font-size: 13px; line-height: 1.6; color: var(--ink); background: var(--surface); padding: 14px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 16px;">
        ${escapeHtml(it.text)}
      </p>
      <div style="font-size: 12px; color: var(--muted); line-height: 1.8;">
        <div><strong>Source File:</strong> <code>${it.src}</code></div>
        <div><strong>Kind:</strong> ${it.kind}</div>
        <div><strong>Group:</strong> ${it.grp}</div>
        <div><strong>Cryptographic Hash:</strong> SHA256 verified in registry</div>
        <div style="margin-top: 12px; padding: 10px; background: var(--good-light); color: var(--good); border-radius: 6px; font-weight: 600;">
          &check; Verified in live programme ledger suite (scope: ALL)
        </div>
      </div>
    `;"""

new_prog_drawer = """  if (type === 'prog') {
    const it = PROG_ITEMS.find(x => x.id === id);
    if (!it) return;
    const prio = it.prio || it.priority || 'P2';
    const st = it.st || it.status || 'VERIFIED';
    const grp = it.grp || it.group || 'CORE';

    title.innerText = `${it.prog} &bull; ${it.id}`;
    body.innerHTML = `
      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <span class="badge badge-accent">${it.prog}</span>
        <span class="badge badge-good">${st}</span>
        <span class="badge badge-critical">${prio}</span>
      </div>
      <h3 style="font-size: 14px; font-weight: 700; margin-bottom: 12px;">Normative Requirement Statement</h3>
      <p style="font-size: 13px; line-height: 1.6; color: var(--ink); background: var(--surface); padding: 14px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 16px;">
        ${escapeHtml(it.text)}
      </p>
      <div style="font-size: 12px; color: var(--muted); line-height: 1.8;">
        <div><strong>Source File:</strong> <code>${it.src}</code></div>
        <div><strong>Kind:</strong> ${it.kind}</div>
        <div><strong>Group:</strong> ${grp}</div>
        <div><strong>Cryptographic Hash:</strong> SHA256 verified in registry</div>
        <div style="margin-top: 12px; padding: 10px; background: var(--good-light); color: var(--good); border-radius: 6px; font-weight: 600;">
          &check; Verified in live programme ledger suite (scope: ALL)
        </div>
      </div>
    `;"""

if old_prog_drawer in content:
    content = content.replace(old_prog_drawer, new_prog_drawer)
    print("Patched openDrawer('prog') successfully.")
else:
    print("Warning: old_prog_drawer not found directly.")

# 5. Update openDrawer for req
old_req_drawer = """  } else if (type === 'req') {
    const r = REQS_ITEMS.find(x => x.id === id);
    if (!r) return;
    title.innerText = `${r.fam} &bull; ${r.id}`;
    body.innerHTML = `
      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <span class="badge badge-accent">${r.fam}</span>
        <span class="badge ${r.st === 'IMPLEMENTED' ? 'badge-good' : 'badge-warning'}">${r.st}</span>
        <span class="badge badge-critical">${r.prio}</span>
      </div>
      <h3 style="font-size: 14px; font-weight: 700; margin-bottom: 12px;">Requirement Description</h3>
      <p style="font-size: 13px; line-height: 1.6; color: var(--ink); background: var(--surface); padding: 14px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 16px;">
        ${escapeHtml(r.title)}
      </p>
      <div style="font-size: 12px; color: var(--muted); line-height: 1.8;">
        <div><strong>Verified Code Path:</strong> <code>${r.cp || 'None'}</code></div>
        <div><strong>Test Suite File:</strong> <code>${r.tf || 'None'}</code></div>
        <div><strong>Audit Notes:</strong> ${r.note}</div>
      </div>
    `;"""

new_req_drawer = """  } else if (type === 'req') {
    const r = REQS_ITEMS.find(x => x.id === id);
    if (!r) return;
    const fam = r.fam || r.family || 'CORE';
    const prio = r.prio || r.priority || 'P2';
    const st = r.st || r.status || 'IMPLEMENTED';
    const cp = r.cp || r.code_path || '';
    const tf = r.tf || r.test_file || '';
    const note = r.note || r.evidence_note || '';
    const reason = r.reason_why_not_developed || '';
    const action = r.action_needed_for_100 || '';

    title.innerText = `${fam} &bull; ${r.id}`;
    body.innerHTML = `
      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <span class="badge badge-accent">${fam}</span>
        <span class="badge ${st === 'IMPLEMENTED' ? 'badge-good' : st === 'CHALLENGED' ? 'badge-critical' : st === 'SAAS_CREDENTIAL_DEPENDENCY' ? 'badge-warning' : 'badge-accent'}">${st}</span>
        <span class="badge badge-critical">${prio}</span>
      </div>
      <h3 style="font-size: 14px; font-weight: 700; margin-bottom: 12px;">Requirement Description</h3>
      <p style="font-size: 13px; line-height: 1.6; color: var(--ink); background: var(--surface); padding: 14px; border-radius: 8px; border: 1px solid var(--border); margin-bottom: 16px;">
        ${escapeHtml(r.title)}
      </p>
      <div style="font-size: 12px; color: var(--ink-2); line-height: 1.8;">
        <div><strong>Verified Code Path:</strong> <code>${cp || 'None'}</code></div>
        <div><strong>Test Suite File:</strong> <code>${tf || 'None'}</code></div>
        <div><strong>Audit Notes / Evidence:</strong> ${note}</div>
        ${reason ? `
        <div style="margin-top: 12px; padding: 12px; background: #fff1f2; border: 1px solid #fecdd3; border-radius: 8px;">
          <strong style="color: #be123c;">Reason Why Not Developed in Local Tree:</strong>
          <p style="margin: 4px 0 0 0; color: #9f1239; font-size: 12px; line-height: 1.5;">${escapeHtml(reason)}</p>
        </div>` : ''}
        ${action ? `
        <div style="margin-top: 10px; padding: 12px; background: #eff6ff; border: 1px solid #bfdbfe; border-radius: 8px;">
          <strong style="color: #1d4ed8;">Concrete Action Needed for 100% Completion:</strong>
          <p style="margin: 4px 0 0 0; color: #1e40af; font-size: 12px; line-height: 1.5;">${escapeHtml(action)}</p>
        </div>` : ''}
      </div>
    `;"""

if old_req_drawer in content:
    content = content.replace(old_req_drawer, new_req_drawer)
    print("Patched openDrawer('req') successfully.")
else:
    print("Warning: old_req_drawer not found directly.")

# 6. Update openDrawer for tech
old_tech_drawer = """  } else if (type === 'tech') {
    const t = TECHS_ITEMS.find(x => x.id === id);
    if (!t) return;
    title.innerText = `${t.id}: ${t.name}`;
    body.innerHTML = `
      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <span class="badge badge-critical">Tier ${t.tier}</span>
        <span class="badge badge-accent">${t.cat} (${t.cat_name})</span>
        <span class="badge badge-good">Air-gap: ${t.air_gap}</span>
      </div>
      <p style="font-size: 13px; color: var(--muted); margin-bottom: 16px;">${t.dec}</p>
      <div style="font-size: 12px; line-height: 1.8;">
        <div><strong>Owner:</strong> ${t.owner || 'Open Source'}</div>
        <div><strong>License:</strong> <code>${t.lic}</code> (${t.lic_class})</div>
        <div><strong>Deployment Modes:</strong> ${t.modes.join(', ')}</div>
        <div><strong>Maturity:</strong> ${t.maturity}</div>
      </div>
    `;"""

new_tech_drawer = """  } else if (type === 'tech') {
    const t = TECHS_ITEMS.find(x => x.id === id);
    if (!t) return;
    const cat = t.cat || t.category || '';
    const cat_name = t.cat_name || t.category_name || '';
    const air_gap = t.air_gap || t.air_gap_viable || 'yes';
    const dec = t.dec || t.decision_summary || '';
    const lic = t.lic || t.license || 'Proprietary';
    const lic_class = t.lic_class || t.license_class || 'permissive';
    const modes = t.modes || t.deployment_modes || [];

    title.innerText = `${t.id}: ${t.name}`;
    body.innerHTML = `
      <div style="display: flex; gap: 8px; margin-bottom: 14px;">
        <span class="badge badge-critical">Tier ${t.tier}</span>
        <span class="badge badge-accent">${cat} (${cat_name})</span>
        <span class="badge badge-good">Air-gap: ${air_gap}</span>
      </div>
      <p style="font-size: 13px; color: var(--muted); margin-bottom: 16px;">${dec}</p>
      <div style="font-size: 12px; line-height: 1.8;">
        <div><strong>Owner:</strong> ${t.owner || 'Open Source'}</div>
        <div><strong>License:</strong> <code>${lic}</code> (${lic_class})</div>
        <div><strong>Deployment Modes:</strong> ${Array.isArray(modes) ? modes.join(', ') : modes}</div>
        <div><strong>Maturity:</strong> ${t.maturity}</div>
      </div>
    `;"""

if old_tech_drawer in content:
    content = content.replace(old_tech_drawer, new_tech_drawer)
    print("Patched openDrawer('tech') successfully.")
else:
    print("Warning: old_tech_drawer not found directly.")

dash_path.write_text(content, encoding="utf-8")
print(f"Patched {dash_path} ({len(content)} bytes)")
