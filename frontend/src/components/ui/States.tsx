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

/** Polished list skeleton for data-fetching panels. */
export function SkeletonRows({ rows = 5, testId }: { rows?: number; testId?: string }) {
  return (
    <div className="divide-y divide-[var(--border-subtle)]" data-testid={testId}>
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="flex items-center gap-3 px-4 py-3">
          <Skeleton className="h-8 w-8 rounded-full" />
          <div className="flex-1 space-y-1.5">
            <Skeleton className="h-3 w-1/3" />
            <Skeleton className="h-2.5 w-2/3" />
          </div>
          <Skeleton className="h-6 w-16" />
        </div>
      ))}
    </div>
  );
}

export function LoadingState({ label = "Loading", testId }: { label?: string; testId?: string }) {
  return (
    <div
      data-testid={testId}
      className="animate-fade-in flex flex-col items-center justify-center gap-3 py-12 text-sm text-[var(--text-muted)]"
    >
      <span className="relative flex h-10 w-10 items-center justify-center">
        <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-[var(--accent)] opacity-20" />
        <Spinner className="relative" />
      </span>
      <span className="tracking-wide">{label}…</span>
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
      className="animate-fade-in flex flex-col items-center justify-center gap-3 px-6 py-14 text-center"
    >
      <div className="rounded-full border border-[var(--border-subtle)] bg-gradient-to-b from-[var(--bg-panel)] to-[var(--bg-surface)] p-4 text-[var(--text-muted)] shadow-inner ring-1 ring-[var(--border-subtle)]">
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
