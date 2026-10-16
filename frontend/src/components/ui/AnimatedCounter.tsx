import { useEffect, useRef, useState } from "react";

interface Props {
  value: number | null | undefined;
  decimals?: number;
  duration?: number;
  className?: string;
  format?: (n: number) => string;
}

// Animated number that eases from its previous value to the new one.
// Respects prefers-reduced-motion (snaps instantly).
export function AnimatedCounter({ value, decimals = 0, duration = 900, className, format }: Props) {
  const target = typeof value === "number" && Number.isFinite(value) ? value : null;
  const [display, setDisplay] = useState(target ?? 0);
  const fromRef = useRef(0);
  const rafRef = useRef<number | null>(null);

  useEffect(() => {
    if (target === null) return;
    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (reduce) { setDisplay(target); return; }
    const from = fromRef.current;
    const start = performance.now();
    const tick = (now: number) => {
      const t = Math.min(1, (now - start) / duration);
      const eased = 1 - Math.pow(1 - t, 3); // easeOutCubic
      setDisplay(from + (target - from) * eased);
      if (t < 1) rafRef.current = requestAnimationFrame(tick);
      else fromRef.current = target;
    };
    rafRef.current = requestAnimationFrame(tick);
    return () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); };
  }, [target, duration]);

  if (target === null) return <span className={className}>N/A</span>;
  const fmt = format || ((n: number) => new Intl.NumberFormat("en-US", { minimumFractionDigits: decimals, maximumFractionDigits: decimals }).format(n));
  return <span className={className} style={{ fontVariantNumeric: "tabular-nums" }}>{fmt(display)}</span>;
}
