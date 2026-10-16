import { useQuery } from "@tanstack/react-query";
import { useEffect, useMemo, useState } from "react";
import { Palette, Check, X, Lock, RotateCcw, Type, Bot, Tags, Loader2, TriangleAlert } from "lucide-react";
import { motion } from "framer-motion";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Card, Overline } from "../components/ui/Card";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { Page, PageHeader } from "../components/ui/Page";
import { ErrorState, LoadingState } from "../components/ui/States";

const THEMES = [
  { id: "dark", label: "Dark", bg: "#11141a", text: "#f8fafc" },
  { id: "light", label: "Light", bg: "#ffffff", text: "#0f172a" },
  { id: "hc-dark", label: "HC Dark", bg: "#0a0a0a", text: "#ffffff" },
  { id: "hc-light", label: "HC Light", bg: "#ffffff", text: "#000000" },
];

function hexToRgb(hex: string): [number, number, number] | null {
  const m = hex.replace("#", "").match(/^([0-9a-f]{6})$/i);
  if (!m) return null;
  const n = parseInt(m[1], 16);
  return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
}
function relLum([r, g, b]: [number, number, number]) {
  const a = [r, g, b].map((v) => {
    const s = v / 255;
    return s <= 0.03928 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * a[0] + 0.7152 * a[1] + 0.0722 * a[2];
}
function contrast(a: string, b: string) {
  const ra = hexToRgb(a), rb = hexToRgb(b);
  if (!ra || !rb) return 0;
  const la = relLum(ra), lb = relLum(rb);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}
function bestText(bg: string) {
  return contrast(bg, "#ffffff") >= contrast(bg, "#000000") ? "#ffffff" : "#000000";
}

export function Brand() {
  const { session } = useAuth();
  const isAdmin = (session?.principal.roles || []).some((r) => r === "admin" || r === "system");

  const theme = useQuery({
    queryKey: [session?.tenant, "branding-theme"],
    queryFn: () => apiFetch<any>(`/branding/theme?tenant_id=${session?.tenant || "default"}&mode=dark`),
    retry: false,
  });

  const [appName, setAppName] = useState("");
  const [primary, setPrimary] = useState("#06b6d4");
  const [assistant, setAssistant] = useState("");
  const [renameInput, setRenameInput] = useState("WorkItem, Repository, Incident");
  const [renameResult, setRenameResult] = useState<Record<string, string> | null>(null);
  const [renaming, setRenaming] = useState(false);

  useEffect(() => {
    if (theme.data) {
      setAppName(theme.data.app_name || "KnowGridFlow");
      const p = theme.data.colors?.primary;
      if (p && /^#[0-9a-f]{6}$/i.test(p)) setPrimary(p);
      setAssistant(theme.data.assistant?.name || "Assistant");
    }
  }, [theme.data]);

  const contrastResults = useMemo(
    () => THEMES.map((t) => {
      const onPrimary = bestText(primary);
      const chipRatio = contrast(primary, onPrimary); // label legibility on a brand-filled button
      const accentRatio = contrast(primary, t.bg); // brand as accent text/border on the theme surface
      const limiting = Math.min(accentRatio, chipRatio);
      return { ...t, onPrimary, chipRatio, accentRatio, limiting, pass: chipRatio >= 4.5 && accentRatio >= 3 };
    }),
    [primary],
  );
  const allPass = contrastResults.every((r) => r.pass);

  const previewTerminology = async () => {
    const labels = renameInput.split(",").map((s) => s.trim()).filter(Boolean);
    if (!labels.length) return;
    setRenaming(true);
    try {
      const r = await apiFetch<any>("/branding/terminology/canonicalize", { method: "POST", body: { labels } });
      setRenameResult(r.canonical || r);
    } catch {
      setRenameResult(null);
    } finally {
      setRenaming(false);
    }
  };

  if (theme.isLoading) return <LoadingState label="Loading brand pack" />;
  if (theme.error) return <ErrorState problem={theme.error} onRetry={theme.refetch} />;

  return (
    <Page>
      <PageHeader title="Brand" overline="White-label theme · preview · publish" icon={<Palette size={18} />} actions={
        <div className="flex items-center gap-2">
          <Badge tone={allPass ? "success" : "danger"} testId="brand-contrast-status">{allPass ? "Contrast OK" : "Contrast failing"}</Badge>
        </div>
      } />

      {!isAdmin && (
        <Card className="flex items-center gap-2 p-4 text-sm text-amber-300">
          <TriangleAlert size={15} /> Brand management requires the <code className="font-mono">admin</code> or <code className="font-mono">system</code> role. Showing a read-only preview.
        </Card>
      )}

      <div className="grid gap-4 lg:grid-cols-[360px_1fr]">
        {/* Draft editor */}
        <div className="space-y-4">
          <Card className="p-4" data-testid="brand-editor">
            <Overline>Brand pack (draft)</Overline>
            <div className="mt-3 space-y-3">
              <div>
                <label className="mb-1 flex items-center gap-1.5 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]"><Type size={11} /> Product name</label>
                <input data-testid="brand-app-name" value={appName} onChange={(e) => setAppName(e.target.value)} disabled={!isAdmin} className="h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)] disabled:opacity-50" />
              </div>
              <div>
                <label className="mb-1 flex items-center gap-1.5 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]"><Palette size={11} /> Brand / accent colour</label>
                <div className="flex items-center gap-2">
                  <input type="color" data-testid="brand-color-picker" value={primary} onChange={(e) => setPrimary(e.target.value)} disabled={!isAdmin} className="h-9 w-12 cursor-pointer rounded-sm border border-[var(--border-strong)] bg-transparent disabled:opacity-50" />
                  <input value={primary} onChange={(e) => setPrimary(e.target.value)} disabled={!isAdmin} className="h-9 flex-1 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 font-mono text-sm uppercase outline-none focus:border-[var(--accent)] disabled:opacity-50" />
                </div>
              </div>
              <div>
                <label className="mb-1 flex items-center gap-1.5 font-mono text-[9px] uppercase tracking-wider text-[var(--text-muted)]"><Bot size={11} /> Assistant name</label>
                <input data-testid="brand-assistant-name" value={assistant} onChange={(e) => setAssistant(e.target.value)} disabled={!isAdmin} className="h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)] disabled:opacity-50" />
              </div>
            </div>
            <p className="mt-3 text-[11px] text-[var(--text-muted)]">Semantic, fact-class and focus colours are locked by the design system and cannot be rebranded.</p>
          </Card>

          <Card className="p-4">
            <Overline>Publish</Overline>
            <p className="mt-1 text-xs text-[var(--text-muted)]">Theme application is atomic — the pack must pass contrast validation before it can go live.</p>
            <Button className="mt-3 w-full justify-center" variant="primary" data-testid="brand-publish" disabled title="Publish not available in this deployment">
              <Lock size={14} /> Publish brand pack
            </Button>
            <Button className="mt-2 w-full justify-center" variant="outline" data-testid="brand-rollback" disabled title="Rollback not available in this deployment">
              <RotateCcw size={14} /> Rollback to last published
            </Button>
            <div className="mt-3 flex items-start gap-2 rounded-sm border border-amber-500/40 bg-amber-500/10 px-2.5 py-2 text-[11px] text-amber-200" data-testid="brand-publish-contract">
              <TriangleAlert size={13} className="mt-0.5 shrink-0" />
              Publishing is not wired in this deployment (contract <span className="font-mono">BACKEND-MISSING-018</span>). Read and preview are fully live.
            </div>
          </Card>
        </div>

        {/* Preview + validation */}
        <div className="space-y-4">
          <Card className="p-4">
            <Overline>Live preview — all four themes</Overline>
            <div className="mt-3 grid gap-3 sm:grid-cols-2 xl:grid-cols-4" data-testid="brand-theme-previews">
              {contrastResults.map((t) => (
                <motion.div key={t.id} initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} className="overflow-hidden rounded-md border border-[var(--border-subtle)]">
                  <div className="p-3" style={{ backgroundColor: t.bg, color: t.text }}>
                    <div className="flex items-center gap-1.5">
                      <span className="inline-block h-4 w-4 rounded-sm" style={{ backgroundColor: primary }} />
                      <span className="text-xs font-semibold" style={{ fontFamily: "var(--font-heading)" }}>{appName || "KnowGridFlow"}</span>
                    </div>
                    <div className="mt-2 inline-flex items-center rounded-sm px-2 py-1 text-[11px] font-semibold" style={{ backgroundColor: primary, color: t.onPrimary }}>
                      Primary action
                    </div>
                    <p className="mt-2 text-[10px]" style={{ color: primary }}>Accent link · {assistant || "Assistant"}</p>
                  </div>
                  <div className="flex items-center justify-between border-t border-[var(--border-subtle)] bg-[var(--bg-panel)] px-2.5 py-1.5">
                    <span className="font-mono text-[10px] text-[var(--text-muted)]">{t.label}</span>
                    {t.pass
                      ? <span className="flex items-center gap-1 text-[10px] text-emerald-400" data-testid={`brand-contrast-${t.id}`}><Check size={11} /> AA {t.accentRatio.toFixed(1)}:1</span>
                      : <span className="flex items-center gap-1 text-[10px] text-red-400" data-testid={`brand-contrast-${t.id}`}><X size={11} /> {t.accentRatio.toFixed(1)}:1</span>}
                  </div>
                </motion.div>
              ))}
            </div>
            {!allPass && (
              <div className="mt-3 flex items-start gap-2 rounded-sm border border-red-500/40 bg-red-500/10 px-2.5 py-2 text-[11px] text-red-200">
                <TriangleAlert size={13} className="mt-0.5 shrink-0" /> The brand colour fails the WCAG AA 4.5:1 gate on one or more themes. Adjust the colour until every theme passes before publishing.
              </div>
            )}
          </Card>

          <Card className="p-4">
            <div className="flex items-center justify-between">
              <Overline>Terminology rename (preview)</Overline>
              <Button size="sm" variant="outline" data-testid="brand-terminology-preview" onClick={previewTerminology} disabled={renaming}>
                {renaming ? <Loader2 size={12} className="animate-spin" /> : <Tags size={12} />} Preview
              </Button>
            </div>
            <input data-testid="brand-rename-input" value={renameInput} onChange={(e) => setRenameInput(e.target.value)} className="mt-3 h-9 w-full rounded-sm border border-[var(--border-strong)] bg-[var(--bg-void)] px-2.5 text-sm outline-none focus:border-[var(--accent)]" placeholder="WorkItem, Repository, Incident" />
            {renameResult && (
              <div className="mt-3 space-y-1" data-testid="brand-rename-result">
                {Object.entries(renameResult).map(([from, to]) => (
                  <div key={from} className="flex items-center gap-2 rounded-sm bg-[var(--bg-void)] px-2.5 py-1.5 text-xs">
                    <span className="font-mono">{from}</span>
                    <span className="text-[var(--text-muted)]">→</span>
                    <span className="font-mono text-cyan-300">{String(to)}</span>
                  </div>
                ))}
              </div>
            )}
          </Card>
        </div>
      </div>
    </Page>
  );
}
