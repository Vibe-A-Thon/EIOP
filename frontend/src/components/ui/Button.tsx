import { forwardRef, type ButtonHTMLAttributes, type ReactNode } from "react";
import { cn } from "../../lib/utils";

type Variant = "primary" | "secondary" | "ghost" | "danger" | "outline";
type Size = "sm" | "md" | "icon";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: Size;
  children?: ReactNode;
}

const variants: Record<Variant, string> = {
  primary:
    "bg-[var(--accent)] text-black font-semibold hover:bg-[var(--accent-strong)] border border-transparent",
  secondary:
    "bg-[var(--bg-panel)] text-[var(--text-primary)] hover:bg-[var(--bg-hover)] border border-[var(--border-subtle)] hover:border-[var(--border-strong)]",
  outline:
    "bg-transparent text-[var(--text-primary)] hover:bg-[var(--bg-hover)] border border-[var(--border-strong)]",
  ghost: "bg-transparent text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-hover)] border border-transparent",
  danger:
    "bg-[var(--danger)] text-white font-semibold hover:brightness-110 border border-transparent",
};

const sizes: Record<Size, string> = {
  sm: "h-7 px-2.5 text-xs gap-1.5",
  md: "h-9 px-3.5 text-sm gap-2",
  icon: "h-9 w-9 justify-center",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "secondary", size = "md", className, children, ...props }, ref) => (
    <button
      ref={ref}
      className={cn(
        "inline-flex items-center rounded-sm font-body transition-colors duration-150 focus-ring disabled:opacity-40 disabled:cursor-not-allowed select-none",
        variants[variant],
        sizes[size],
        className,
      )}
      {...props}
    >
      {children}
    </button>
  ),
);
Button.displayName = "Button";
