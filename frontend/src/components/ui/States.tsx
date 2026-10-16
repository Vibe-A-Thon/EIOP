import type { ReactNode } from "react";
import { AlertTriangle, Inbox, Loader2, TriangleAlert } from "lucide-react";
import type { ApiProblem } from "../../lib/api";
import { cn } from "../../lib/utils";

export function Spinner({ className }: { className?: string }) {
  return <Loader2 className={cn("animate-spin text-[var(--text-muted)]", className)} size={18} />;
}

export function Skeleton({ className }: { className?: string }) {
  return <div className={cn("kgf-skeleton rounded-sm", className)} />;
}

export function LoadingState({ label = "Loading", testId }: { label?: string; testId?: string }) {
  return (
    <div
      data-testid={testId}
      className="flex items-center justify-center gap-2 py-10 text-sm text-[var(--text-muted)]"
    >
      <Spinner />
      {label}…
    </div>
  );
}

export function EmptyState({
  title,
  description,
  icon,
  action,
  testId,
}: {
  title: string;
  description?: string;
  icon?: ReactNode;
  action?: ReactNode;
  testId?: string;
}) {
  return (
    <div
      data-testid={testId}
      className="flex flex-col items-center justify-center gap-3 px-6 py-12 text-center"
    >
      <div className="rounded-full border border-[var(--border-subtle)] bg-[var(--bg-panel)] p-3 text-[var(--text-muted)]">
        {icon || <Inbox size={22} />}
      </div>
      <div>
        <p className="font-heading text-sm font-semibold text-[var(--text-primary)]">{title}</p>
        {description && (
          <p className="mt-1 max-w-sm text-xs text-[var(--text-muted)]">{description}</p>
        )}
      </div>
      {action}
    </div>
  );
}

export function ErrorState({
  problem,
  onRetry,
  testId,
}: {
  problem: ApiProblem | Error | unknown;
  onRetry?: () => void;
  testId?: string;
}) {
  const p = (problem as any)?.problem || problem;
  const status = p?.status;
  const detail = p?.detail || p?.message || "Something went wrong";
  const correlationId = p?.correlationId;
  return (
    <div
      data-testid={testId}
      className="m-4 rounded-md border border-red-500/40 bg-red-500/10 p-4 text-sm"
    >
      <div className="flex items-center gap-2 font-semibold text-red-300">
        <AlertTriangle size={16} />
        {status ? `Error ${status}` : "Error"}
      </div>
      <p className="mt-1 text-[var(--text-secondary)]">{detail}</p>
      {correlationId && (
        <p className="mt-1 font-mono text-[10px] text-[var(--text-muted)]">
          correlation: {correlationId}
        </p>
      )}
      {onRetry && (
        <button
          onClick={onRetry}
          data-testid="error-retry-button"
          className="mt-3 rounded-sm border border-[var(--border-strong)] px-2.5 py-1 text-xs text-[var(--text-primary)] transition-colors hover:bg-[var(--bg-hover)]"
        >
          Retry
        </button>
      )}
    </div>
  );
}

/** Renders partial/warnings on GraphResult responses (GUI-COMP-19). */
export function ResultBanner({
  partial,
  warnings,
}: {
  partial?: boolean;
  warnings?: string[];
}) {
  if (!partial && (!warnings || warnings.length === 0)) return null;
  return (
    <div className="flex items-start gap-2 rounded-sm border border-amber-500/40 bg-amber-500/10 px-3 py-2 text-xs text-amber-200">
      <TriangleAlert size={14} className="mt-0.5 shrink-0" />
      <div className="space-y-0.5">
        {partial && <div className="font-medium">Partial result — not all data was returned.</div>}
        {warnings?.map((w, i) => (
          <div key={i}>{w}</div>
        ))}
      </div>
    </div>
  );
}
