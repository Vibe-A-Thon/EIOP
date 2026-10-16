import { useState } from "react";
import { ArrowRight, CheckCircle2, Loader2, Play, Plug, X } from "lucide-react";
import { apiFetch } from "../lib/api";
import { Button } from "./ui/Button";
import { JobStatusBadge } from "./ModeBadges";

interface Connector {
  id: string;
  name?: string;
  type?: string;
}

export function SourceOnboarding({
  connector,
  onClose,
  onDone,
}: {
  connector: Connector;
  onClose: () => void;
  onDone: () => void;
}) {
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [sourceId, setSourceId] = useState(`${connector.id}-1`);
  const [name, setName] = useState(`${(connector.name || connector.id).replace(/\b\w/g, (c) => c.toUpperCase())} Source`);
  const [baseUrl, setBaseUrl] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [job, setJob] = useState<any>(null);

  const create = async () => {
    setBusy(true);
    setError(null);
    try {
      await apiFetch("/sources", {
        method: "POST",
        body: {
          source_id: sourceId.trim(),
          source_type: connector.id,
          name: name.trim(),
          base_url: baseUrl.trim() || undefined,
          capabilities: { baseline: true, discovery: true, replay: true },
        },
      });
      onDone();
      setStep(3);
    } catch (err: any) {
      setError(err?.problem?.detail || err?.message || "Could not create source");
    } finally {
      setBusy(false);
    }
  };

  const runBaseline = async () => {
    setBusy(true);
    setError(null);
    try {
      const j = await apiFetch<any>(`/sources/${encodeURIComponent(sourceId.trim())}/baseline`, {
        method: "POST",
        body: { dry_run: false },
      });
      setJob(j);
      onDone();
    } catch (err: any) {
      setError(err?.problem?.detail || err?.message || "Baseline failed to start");
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" data-testid="source-onboarding">
      <div className="absolute inset-0 bg-black/60 backdrop-blur-sm" onClick={onClose} />
      <div className="relative w-full max-w-lg animate-fade-in overflow-hidden rounded-lg border border-[var(--border-strong)] bg-[var(--bg-surface)] shadow-2xl">
        <div className="flex items-center justify-between border-b border-[var(--border-subtle)] px-4 py-3">
          <div className="flex items-center gap-2.5">
            <div className="grid h-8 w-8 place-items-center rounded-sm border border-cyan-500/40 bg-cyan-500/10 text-cyan-300">
              <Plug size={15} />
            </div>
            <div>
              <h3 className="font-heading text-sm font-semibold capitalize">Connect {connector.name || connector.id}</h3>
              <p className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
                Step {step} of 3
              </p>
            </div>
          </div>
          <button onClick={onClose} className="grid h-7 w-7 place-items-center rounded-sm text-[var(--text-muted)] transition-colors hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]">
            <X size={15} />
          </button>
        </div>

        {/* Stepper */}
        <div className="flex gap-1 px-4 pt-3">
          {[1, 2, 3].map((s) => (
            <div key={s} className={`h-1 flex-1 rounded-full ${s <= step ? "bg-[var(--accent)]" : "bg-[var(--bg-hover)]"}`} />
          ))}
        </div>

        <div className="p-4">
          {step === 1 && (
            <div className="space-y-3">
              <label className="block">
                <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">Source ID</span>
                <input
                  data-testid="onboard-source-id"
                  value={sourceId}
                  onChange={(e) => setSourceId(e.target.value)}
                  className="mt-1 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm outline-none focus:border-[var(--accent)]"
                />
              </label>
              <label className="block">
                <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">Display name</span>
                <input
                  data-testid="onboard-name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="mt-1 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]"
                />
              </label>
              <label className="block">
                <span className="font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">Base URL (optional)</span>
                <input
                  data-testid="onboard-base-url"
                  value={baseUrl}
                  onChange={(e) => setBaseUrl(e.target.value)}
                  placeholder="https://…"
                  className="mt-1 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm outline-none focus:border-[var(--accent)]"
                />
              </label>
              <p className="font-mono text-[10px] leading-relaxed text-[var(--text-muted)]">
                Credentials are never entered here — they are referenced from the deployment's secret store.
              </p>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-2 text-sm">
              <p className="text-[var(--text-muted)]">Review and register this source:</p>
              {[
                ["Connector", connector.id],
                ["Source ID", sourceId],
                ["Name", name],
                ["Base URL", baseUrl || "—"],
              ].map(([k, v]) => (
                <div key={k} className="flex justify-between border-b border-[var(--border-subtle)] py-1.5 last:border-0">
                  <span className="font-mono text-xs text-[var(--text-muted)]">{k}</span>
                  <span className="font-mono text-xs">{v}</span>
                </div>
              ))}
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <div className="flex items-center gap-2 text-sm text-emerald-300">
                <CheckCircle2 size={18} /> Source <strong className="font-mono">{sourceId}</strong> registered.
              </div>
              {job ? (
                <div className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3">
                  <div className="flex items-center gap-2">
                    <JobStatusBadge status={job.status} />
                    <span className="font-mono text-[10px] text-[var(--text-muted)]">{job.kind}</span>
                  </div>
                  <p className="mt-1 break-all font-mono text-[10px] text-[var(--text-muted)]">job: {job.job_id}</p>
                  <p className="mt-2 text-xs text-[var(--text-secondary)]">
                    Baseline started. Track progress in the Jobs tab.
                  </p>
                </div>
              ) : (
                <p className="text-sm text-[var(--text-muted)]">
                  Run a baseline ingestion to pull this source's data into the graph.
                </p>
              )}
            </div>
          )}

          {error && <p className="mt-3 rounded-sm border border-red-500/40 bg-red-500/10 px-3 py-2 text-xs text-red-300">{error}</p>}
        </div>

        <div className="flex items-center justify-between border-t border-[var(--border-subtle)] px-4 py-3">
          <button onClick={onClose} className="text-xs text-[var(--text-muted)] transition-colors hover:text-[var(--text-primary)]">
            {step === 3 ? "Close" : "Cancel"}
          </button>
          <div className="flex gap-2">
            {step === 1 && (
              <Button variant="primary" data-testid="onboard-next" onClick={() => setStep(2)} disabled={!sourceId.trim() || !name.trim()}>
                Review <ArrowRight size={14} />
              </Button>
            )}
            {step === 2 && (
              <>
                <Button variant="ghost" onClick={() => setStep(1)}>Back</Button>
                <Button variant="primary" data-testid="onboard-create" onClick={create} disabled={busy}>
                  {busy ? <Loader2 size={14} className="animate-spin" /> : null} Register source
                </Button>
              </>
            )}
            {step === 3 && !job && (
              <Button variant="primary" data-testid="onboard-baseline" onClick={runBaseline} disabled={busy}>
                {busy ? <Loader2 size={14} className="animate-spin" /> : <Play size={14} />} Run baseline
              </Button>
            )}
            {step === 3 && job && (
              <Button variant="primary" data-testid="onboard-done" onClick={onClose}>Done</Button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
