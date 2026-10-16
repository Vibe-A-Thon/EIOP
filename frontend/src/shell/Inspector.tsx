import { useQuery } from "@tanstack/react-query";
import { useNavigate } from "react-router-dom";
import { Maximize2, X } from "lucide-react";
import { useShell } from "../lib/shellStore";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { FactClassBadge } from "../components/FactClassBadge";
import { LoadingState, ErrorState } from "../components/ui/States";
import { Button } from "../components/ui/Button";
import { shortId } from "../lib/utils";

export function Inspector() {
  const { inspectorOpen, inspectorEntityId, closeInspector } = useShell();
  const { session } = useAuth();
  const navigate = useNavigate();

  const { data, isLoading, error, refetch } = useQuery({
    queryKey: [session?.tenant, "entity", inspectorEntityId],
    queryFn: () => apiFetch<any>(`/entities/${encodeURIComponent(inspectorEntityId!)}`),
    enabled: !!inspectorEntityId && inspectorOpen,
  });

  if (!inspectorOpen) return null;

  const entity = data?.entity;
  const props = entity?.properties || {};
  const name = props.name || props.title || shortId(inspectorEntityId || "");

  return (
    <aside
      data-testid="inspector-panel"
      className="flex w-[340px] shrink-0 flex-col border-l border-[var(--border-subtle)] bg-[var(--bg-surface)] animate-fade-in"
    >
      <div className="flex h-11 shrink-0 items-center justify-between border-b border-[var(--border-subtle)] px-3">
        <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
          Inspector
        </span>
        <button
          data-testid="inspector-close"
          onClick={closeInspector}
          className="grid h-7 w-7 place-items-center rounded-sm text-[var(--text-muted)] transition-colors hover:bg-[var(--bg-hover)] hover:text-[var(--text-primary)]"
        >
          <X size={15} />
        </button>
      </div>

      <div className="flex-1 overflow-y-auto">
        {isLoading && <LoadingState label="Loading entity" />}
        {error && <ErrorState problem={error} onRetry={refetch} />}
        {entity && (
          <div className="space-y-4 p-4">
            <div>
              <div className="mb-1.5 flex flex-wrap items-center gap-2">
                <span className="rounded-full border border-[var(--border-strong)] px-2 py-0.5 font-mono text-[10px] uppercase tracking-wider text-[var(--text-secondary)]">
                  {entity.label}
                </span>
                <FactClassBadge creationStatus={props.creation_status} size="sm" />
              </div>
              <h3 className="break-words font-heading text-base font-semibold leading-tight">
                {name}
              </h3>
              <p className="mt-1 break-all font-mono text-[10px] text-[var(--text-muted)]">
                {inspectorEntityId}
              </p>
            </div>

            <div className="grid grid-cols-2 gap-2">
              <div className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-2.5">
                <p className="font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
                  Outgoing
                </p>
                <p className="font-heading text-lg font-semibold">{data.outgoing?.length ?? 0}</p>
              </div>
              <div className="rounded-sm border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-2.5">
                <p className="font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]">
                  Incoming
                </p>
                <p className="font-heading text-lg font-semibold">{data.incoming?.length ?? 0}</p>
              </div>
            </div>

            <div>
              <p className="mb-1.5 font-mono text-[10px] uppercase tracking-wider text-[var(--text-muted)]">
                Properties
              </p>
              <dl className="space-y-1.5">
                {Object.entries(props)
                  .filter(([, v]) => v !== null && v !== "" && typeof v !== "object")
                  .slice(0, 12)
                  .map(([k, v]) => (
                    <div
                      key={k}
                      className="flex items-start justify-between gap-3 border-b border-[var(--border-subtle)] pb-1.5 text-xs last:border-0"
                    >
                      <dt className="shrink-0 font-mono text-[var(--text-muted)]">{k}</dt>
                      <dd className="break-all text-right text-[var(--text-secondary)]">
                        {String(v)}
                      </dd>
                    </div>
                  ))}
              </dl>
            </div>
          </div>
        )}
      </div>

      {entity && (
        <div className="shrink-0 border-t border-[var(--border-subtle)] p-3">
          <Button
            variant="primary"
            data-testid="inspector-open-full"
            onClick={() => {
              navigate(`/entity/${encodeURIComponent(inspectorEntityId!)}`);
              closeInspector();
            }}
            className="w-full justify-center"
          >
            <Maximize2 size={14} /> Open full view
          </Button>
        </div>
      )}
    </aside>
  );
}
