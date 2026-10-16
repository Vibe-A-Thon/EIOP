import type { ReactNode } from "react";
import { cn } from "../../lib/utils";

type Tone = "neutral" | "success" | "info" | "warning" | "danger" | "accent";

const tones: Record<Tone, string> = {
  neutral: "text-[var(--text-secondary)] border-[var(--border-strong)] bg-[var(--bg-panel)]",
  success: "text-emerald-300 border-emerald-500/40 bg-emerald-500/10",
  info: "text-blue-300 border-blue-500/40 bg-blue-500/10",
  warning: "text-amber-300 border-amber-500/40 bg-amber-500/10",
  danger: "text-red-300 border-red-500/40 bg-red-500/10",
  accent: "text-cyan-300 border-cyan-500/40 bg-cyan-500/10",
};

export function Badge({
  tone = "neutral",
  children,
  className,
  icon,
  testId,
}: {
  tone?: Tone;
  children: ReactNode;
  className?: string;
  icon?: ReactNode;
  testId?: string;
}) {
  return (
    <span
      data-testid={testId}
      className={cn(
        "inline-flex items-center gap-1 rounded-full border px-2 py-0.5 text-[10px] font-mono uppercase tracking-wider",
        tones[tone],
        className,
      )}
    >
      {icon}
      {children}
    </span>
  );
}

export function StatusDot({ tone = "neutral", pulse }: { tone?: Tone; pulse?: boolean }) {
  const colors: Record<Tone, string> = {
    neutral: "bg-slate-400",
    success: "bg-emerald-400",
    info: "bg-blue-400",
    warning: "bg-amber-400",
    danger: "bg-red-400",
    accent: "bg-cyan-400",
  };
  return (
    <span className="relative inline-flex h-2 w-2">
      {pulse && (
        <span className={cn("absolute inline-flex h-full w-full animate-ping rounded-full opacity-60", colors[tone])} />
      )}
      <span className={cn("relative inline-flex h-2 w-2 rounded-full", colors[tone])} />
    </span>
  );
}
