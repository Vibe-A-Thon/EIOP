import { useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";
import { Plus, SquareStack } from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { EmptyState, ErrorState, LoadingState } from "../components/ui/States";
import { relativeTime } from "../lib/utils";

export function Snapshots() {
  const { session } = useAuth();
  const qc = useQueryClient();
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [confirmId, setConfirmId] = useState<string | null>(null);
  const [confirmText, setConfirmText] = useState("");

  const snaps = useQuery({ queryKey: [session?.tenant, "snapshots"], queryFn: () => apiFetch<any>("/enterprise/snapshots"), retry: false });
  const list: any[] = snaps.data?.snapshots || (Array.isArray(snaps.data) ? snaps.data : []);

  const create = async () => {
    setBusy(true);
    try {
      await apiFetch("/enterprise/snapshots", { method: "POST", body: { name: name.trim() || `snapshot-${Date.now()}`, snapshot_type: "FULL", tags: {} } });
      setName(""); qc.invalidateQueries({ queryKey: [session?.tenant, "snapshots"] });
    } catch { /* refresh shows state */ } finally { setBusy(false); }
  };

  const restore = async (id: string) => {
    await apiFetch("/enterprise/snapshots/restore", { method: "POST", body: { snapshot_id: id } }).catch(() => {});
    setConfirmId(null); setConfirmText("");
    qc.invalidateQueries();
  };

  return (
    <Page>
      <PageHeader title="Snapshots" overline="Point-in-time graph snapshots" icon={<SquareStack size={18} />} />

      <Card className="flex flex-wrap items-center gap-2 p-3">
        <input data-testid="snapshot-name" value={name} onChange={(e) => setName(e.target.value)} placeholder="Snapshot name…" className="h-9 flex-1 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]" />
        <Button variant="primary" data-testid="snapshot-create" onClick={create} disabled={busy}><Plus size={14} /> Create snapshot</Button>
      </Card>

      <Card>
        {snaps.isLoading ? <LoadingState label="Loading snapshots" />
          : snaps.error ? <ErrorState problem={snaps.error} onRetry={snaps.refetch} />
          : list.length === 0 ? <EmptyState title="No snapshots yet" description="Create a snapshot to capture the current graph state." icon={<SquareStack size={22} />} />
          : <div className="divide-y divide-[var(--border-subtle)]">{list.map((s, i) => {
              const id = s.snapshot_id || s.id;
              return (
                <div key={id || i} className="flex items-center gap-3 px-4 py-3">
                  <div className="min-w-0 flex-1"><p className="font-medium">{s.name || id}</p><p className="font-mono text-[10px] text-[var(--text-muted)]">{id} · {relativeTime(s.created_at)}</p></div>
                  <Badge tone="neutral">{s.snapshot_type || "FULL"}</Badge>
                  <Button size="sm" variant="outline" data-testid="snapshot-restore" onClick={() => { setConfirmId(id); setConfirmText(""); }}>Restore</Button>
                </div>
              );
            })}</div>}
      </Card>

      {confirmId && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={() => setConfirmId(null)} />
          <Card className="relative w-full max-w-sm animate-fade-in p-4">
            <h3 className="font-heading text-sm font-semibold text-red-300">Destructive: restore snapshot</h3>
            <p className="mt-1 text-xs text-[var(--text-muted)]">This overwrites the current graph. Type <strong className="font-mono text-[var(--text-primary)]">RESTORE</strong> to confirm.</p>
            <input data-testid="snapshot-confirm-input" value={confirmText} onChange={(e) => setConfirmText(e.target.value)} className="mt-3 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm outline-none focus:border-[var(--danger)]" />
            <div className="mt-3 flex justify-end gap-2">
              <Button variant="ghost" onClick={() => setConfirmId(null)}>Cancel</Button>
              <Button variant="danger" data-testid="snapshot-confirm" disabled={confirmText !== "RESTORE"} onClick={() => restore(confirmId)}>Restore</Button>
            </div>
          </Card>
        </div>
      )}
    </Page>
  );
}
