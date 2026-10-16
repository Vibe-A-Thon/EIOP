import { useEffect, useState } from "react";
import { Monitor, Settings as SettingsIcon } from "lucide-react";
import { useTheme, THEMES, type ThemeName } from "../lib/theme";
import { Card, Overline } from "../components/ui/Card";
import { Page, PageHeader } from "../components/ui/Page";
import { cn } from "../lib/utils";

const DENSITIES = ["comfortable", "compact"] as const;
const LOCALES = ["en", "en-GB", "de", "fr", "ja"];

export function Settings() {
  const { theme, setTheme } = useTheme();
  const [density, setDensity] = useState<string>(() => localStorage.getItem("kgf.density") || "comfortable");
  const [reduceMotion, setReduceMotion] = useState<boolean>(() => localStorage.getItem("kgf.reduceMotion") === "1");
  const [locale, setLocale] = useState<string>(() => localStorage.getItem("kgf.locale") || "en");

  useEffect(() => {
    document.documentElement.setAttribute("data-density", density);
    localStorage.setItem("kgf.density", density);
  }, [density]);
  useEffect(() => {
    document.documentElement.classList.toggle("kgf-reduce-motion", reduceMotion);
    localStorage.setItem("kgf.reduceMotion", reduceMotion ? "1" : "0");
  }, [reduceMotion]);
  useEffect(() => { localStorage.setItem("kgf.locale", locale); }, [locale]);

  return (
    <Page>
      <PageHeader title="Settings" overline="Appearance, density & locale" icon={<SettingsIcon size={18} />} />

      <Card className="p-5">
        <Overline>Theme</Overline>
        <div className="mt-3 grid grid-cols-2 gap-2 sm:grid-cols-4">
          {THEMES.map((t) => (
            <button
              key={t.id}
              data-testid={`settings-theme-${t.id}`}
              onClick={() => setTheme(t.id as ThemeName)}
              className={cn("flex items-center gap-2 rounded-sm border px-3 py-2.5 text-sm transition-colors", theme === t.id ? "border-[var(--accent)] text-[var(--accent)]" : "border-[var(--border-subtle)] text-[var(--text-secondary)] hover:border-[var(--border-strong)]")}
            >
              <Monitor size={14} /> {t.label}
            </button>
          ))}
        </div>
      </Card>

      <Card className="p-5">
        <Overline>Density</Overline>
        <div className="mt-3 flex gap-2">
          {DENSITIES.map((d) => (
            <button key={d} data-testid={`settings-density-${d}`} onClick={() => setDensity(d)}
              className={cn("rounded-sm border px-3.5 py-2 text-sm capitalize transition-colors", density === d ? "border-[var(--accent)] text-[var(--accent)]" : "border-[var(--border-subtle)] text-[var(--text-secondary)] hover:border-[var(--border-strong)]")}>
              {d}
            </button>
          ))}
        </div>
      </Card>

      <Card className="flex items-center justify-between p-5">
        <div><Overline>Reduce motion</Overline><p className="mt-1 text-sm text-[var(--text-muted)]">Minimize animations and transitions.</p></div>
        <button
          data-testid="settings-reduce-motion"
          role="switch"
          aria-checked={reduceMotion}
          onClick={() => setReduceMotion((v) => !v)}
          className={cn("relative h-6 w-11 rounded-full transition-colors", reduceMotion ? "bg-[var(--accent)]" : "bg-[var(--bg-hover)]")}
        >
          <span className={cn("absolute top-0.5 h-5 w-5 rounded-full bg-white transition-transform", reduceMotion ? "translate-x-5" : "translate-x-0.5")} />
        </button>
      </Card>

      <Card className="p-5">
        <Overline>Locale</Overline>
        <select data-testid="settings-locale" value={locale} onChange={(e) => setLocale(e.target.value)} className="mt-3 h-9 w-48 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none">
          {LOCALES.map((l) => <option key={l} value={l}>{l}</option>)}
        </select>
        <p className="mt-2 font-mono text-[10px] text-[var(--text-muted)]">Locale preference is stored on this device.</p>
      </Card>
    </Page>
  );
}
