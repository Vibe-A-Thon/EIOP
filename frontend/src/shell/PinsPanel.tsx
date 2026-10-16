import { Copy, Download, FileText, Pin, Trash2, X } from "lucide-react";
import { usePins } from "../lib/pinsStore";
import { EmptyState } from "../components/ui/States";
import { relativeTime } from "../lib/utils";

export function PinsPanel() {
  const { pins, open, setOpen, removePin, clear } = usePins();
  if (!open) return null;

  const copyAll = () => {
    const text = pins
      .map((p, i) => `${i + 1}. ${p.text}${p.source ? `\n   source: ${p.source}` : ""}${p.question ? `\n   from: ${p.question}` : ""}`)
      .join("\n\n");
    navigator.clipboard?.writeText(text).catch(() => {});
  };

  const exportJson = () => {
    const blob = new Blob([JSON.stringify({ kind: "kgf.evidence", version: 1, pins }, null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `kgf-evidence-${new Date().toISOString().slice(0, 10)}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const exportReport = () => {
    const byQuestion = new Map<string, typeof pins>();
    pins.forEach((p) => {
      const q = p.question || "Unattributed evidence";
      if (!byQuestion.has(q)) byQuestion.set(q, []);
      byQuestion.get(q)!.push(p);
    });
    let md = `# Evidence Case Report\n\n_Generated ${new Date().toLocaleString()} · KnowGridFlow_\n\n`;
    md += `**${pins.length} pinned fact${pins.length === 1 ? "" : "s"}** across ${byQuestion.size} question${byQuestion.size === 1 ? "" : "s"}.\n\n`;
    let n = 1;
    for (const [q, items] of byQuestion) {
      md += `## ${q}\n\n`;
      for (const p of items) {
        md += `${n}. ${p.text}\n`;
        if (p.source) md += `   - Source: \`${p.source}\`\n`;
        n++;
      }
      md += `\n`;
    }
    md += `---\n_All facts are drawn from the local knowledge graph. Fact classes and provenance are available in the entity views._\n`;
    const blob = new Blob([md], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `kgf-case-report-${new Date().toISOString().slice(0, 10)}.md`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <aside
      data-testid="pins-panel"
      className="flex w-[340px] shrink-0 flex-col border-l border-[var(--border-subtle)] bg-[var(--bg-surface)] kgf-slide-right"
    >
      <div className="flex h-11 shrink-0 items-center justify-between border-b border-[var(--border-subtle)] px-3">
        <span className="flex items-center gap-1.5 font-mono text-[10px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
          <Pin size={12} /> Evidence board ({pins.length})
        </span>
        <button
          data-testid="pins-close"
          onClick={() => setOpen(false)}
          className="grid h-7 w-7 place-items-center rounded-sm text-[var(--text-muted)] transition-colors hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
        >
          <X size={15} />
        </button>
      </div>

      {pins.length > 0 && (
        <div className="flex items-center gap-1.5 border-b border-[var(--border-subtle)] px-3 py-2">
          <button
            data-testid="pins-copy"
            onClick={copyAll}
            className="flex items-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2 py-1 text-xs transition-colors hover:border-[var(--border-strong)]"
          >
            <Copy size={12} /> Copy
          </button>
          <button
            data-testid="pins-export"
            onClick={exportJson}
            className="flex items-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2 py-1 text-xs transition-colors hover:border-[var(--border-strong)]"
          >
            <Download size={12} /> Export
          </button>
          <button
            data-testid="pins-report"
            onClick={exportReport}
            className="flex items-center gap-1.5 rounded-sm border border-[var(--border-subtle)] px-2 py-1 text-xs transition-colors hover:border-[var(--border-strong)]"
          >
            <FileText size={12} /> Report
          </button>
          <button
            data-testid="pins-clear"
            onClick={clear}
            className="ml-auto flex items-center gap-1.5 rounded-sm px-2 py-1 text-xs text-[var(--text-muted)] transition-colors hover:text-red-400"
          >
            <Trash2 size={12} /> Clear
          </button>
        </div>
      )}

      <div className="flex-1 overflow-y-auto p-3">
        {pins.length === 0 ? (
          <EmptyState
            title="No pinned evidence"
            description="Pin evidence snippets from an answer in Ask to build your case here."
            icon={<Pin size={20} />}
          />
        ) : (
          <ul className="space-y-2">
            {pins.map((p, i) => (
              <li
                key={p.id}
                className="group rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3 text-xs"
              >
                <div className="flex items-start gap-2">
                  <span className="mt-0.5 grid h-4 w-4 shrink-0 place-items-center rounded-full bg-cyan-500/20 font-mono text-[9px] text-cyan-300">
                    {i + 1}
                  </span>
                  <p className="flex-1 text-[var(--text-secondary)]">{p.text}</p>
                  <button
                    onClick={() => removePin(p.id)}
                    className="shrink-0 text-[var(--text-muted)] opacity-0 transition-opacity hover:text-red-400 group-hover:opacity-100"
                  >
                    <X size={13} />
                  </button>
                </div>
                {p.source && (
                  <p className="mt-1 break-all pl-6 font-mono text-[10px] text-[var(--text-muted)]">{p.source}</p>
                )}
                {p.question && (
                  <p className="mt-0.5 pl-6 font-mono text-[9px] italic text-[var(--text-muted)]">
                    from: {p.question} · {relativeTime(p.at)}
                  </p>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </aside>
  );
}
