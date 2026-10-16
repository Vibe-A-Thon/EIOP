import type { HTMLAttributes, ReactNode } from "react";
import { cn } from "../../lib/utils";

interface CardProps extends HTMLAttributes<HTMLDivElement> {
  hover?: boolean;
  glass?: boolean;
}

export function Card({ className, children, hover, glass, ...props }: CardProps) {
  return (
    <div
      className={cn(
        "rounded-md border border-[var(--border-subtle)] shadow-[0_1px_2px_-1px_hsl(var(--shadow-color)/0.4)]",
        glass ? "bg-[var(--bg-surface)]/80 backdrop-blur-xl" : "bg-[var(--bg-surface)]",
        hover &&
          "transition-[transform,box-shadow,border-color] duration-200 ease-out hover:-translate-y-0.5 hover:border-[var(--border-strong)] hover:shadow-[0_8px_24px_-8px_hsl(var(--shadow-color)/0.6)]",
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
