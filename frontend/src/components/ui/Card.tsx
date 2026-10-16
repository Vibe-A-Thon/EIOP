import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../../lib/utils";

export function Card({ className, children, ...props }: HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "rounded-md border border-[var(--border-subtle)] bg-[var(--bg-surface)]",
        className,
      )}
      {...props}
    >
      {children}
    </div>
  );
}

export function CardHeader({
  title,
  icon,
  action,
  description,
}: {
  title: ReactNode;
  icon?: ReactNode;
  action?: ReactNode;
  description?: ReactNode;
}) {
  return (
    <div className="flex items-start justify-between gap-3 border-b border-[var(--border-subtle)] px-4 py-3">
      <div className="min-w-0">
        <div className="flex items-center gap-2">
          {icon && <span className="text-[var(--text-muted)]">{icon}</span>}
          <h3 className="font-heading text-sm font-semibold tracking-tight text-[var(--text-primary)]">
            {title}
          </h3>
        </div>
        {description && (
          <p className="mt-0.5 text-xs text-[var(--text-muted)]">{description}</p>
        )}
      </div>
      {action}
    </div>
  );
}

export function Overline({ children, className }: { children: ReactNode; className?: string }) {
  return (
    <span
      className={cn(
        "font-mono text-[10px] uppercase tracking-[0.18em] text-[var(--text-muted)]",
        className,
      )}
    >
      {children}
    </span>
  );
}
