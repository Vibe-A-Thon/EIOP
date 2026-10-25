import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import {
  Activity,
  ArrowRight,
  Boxes,
  KeyRound,
  Loader2,
  ShieldCheck,
  UserRound,
  Waypoints,
} from "lucide-react";
import { useAuth } from "../lib/auth";
import { apiFetch } from "../lib/api";
import { Button } from "../components/ui/Button";
import { StatusDot } from "../components/ui/Badge";

// FT-AUTH: sign in with login credentials (username + password). Nothing is prefilled
// and no tokens or demo identities are embedded in the bundle; roles come from the
// server-side user record. SSO providers are listed by the API but are placeholders.

export function SignIn() {
  const { signIn } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [tenant, setTenant] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [provider, setProvider] = useState<{ ok: boolean; label: string }>({
    ok: false,
    label: "Checking…",
  });

  useEffect(() => {
    apiFetch<any>("/auth/health", { tenant: null })
      .then((r) =>
        setProvider({
          ok: true,
          label: r?.status ? `Identity provider: ${r.status}` : "Identity provider: reachable",
        }),
      )
      .catch(() => setProvider({ ok: false, label: "Identity provider: unavailable" }));
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setError(null);
    try {
      await signIn(username.trim(), password, tenant.trim() || "default");
      navigate("/overview", { replace: true });
    } catch (err: any) {
      setError(err?.problem?.status === 401 ? "Invalid username or password" : err?.problem?.detail || err?.message || "Sign-in failed");
      setPassword("");
      setSubmitting(false);
    }
  };

  return (
    <div className="grid min-h-screen grid-cols-1 lg:grid-cols-[1.1fr_0.9fr]">
      {/* Left — telemetry panel */}
      <div className="relative hidden flex-col justify-between overflow-hidden border-r border-[var(--border-subtle)] bg-[var(--bg-surface)] p-10 lg:flex">
        <div
          className="pointer-events-none absolute inset-0 opacity-[0.12]"
          style={{
            backgroundImage:
              "linear-gradient(var(--border-strong) 1px, transparent 1px), linear-gradient(90deg, var(--border-strong) 1px, transparent 1px)",
            backgroundSize: "44px 44px",
          }}
        />
        <div className="relative flex items-center gap-2.5">
          <div className="grid h-9 w-9 place-items-center rounded-md border border-cyan-500/40 bg-cyan-500/10 text-cyan-300">
            <Waypoints size={18} />
          </div>
          <div>
            <p className="font-heading text-sm font-bold tracking-tight">KnowGridFlow</p>
            <p className="font-mono text-[10px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
              Enterprise Ontology & Intelligence
            </p>
          </div>
        </div>

        <div className="relative space-y-6">
          <h1 className="max-w-md font-heading text-3xl font-bold leading-tight tracking-tight">
            The graph is the work surface. Every answer carries its evidence.
          </h1>
          <div className="grid max-w-md grid-cols-1 gap-3">
            {[
              { icon: Waypoints, t: "Traceability", d: "What implements this requirement?" },
              { icon: Activity, t: "Impact", d: "What changes if this changes?" },
              { icon: ShieldCheck, t: "Evidence", d: "Why do we believe this is true?" },
            ].map((f) => (
              <div
                key={f.t}
                className="flex items-start gap-3 rounded-md border border-[var(--border-subtle)] bg-[var(--bg-panel)] px-4 py-3"
              >
                <f.icon size={18} className="mt-0.5 text-cyan-300" />
                <div>
                  <p className="text-sm font-semibold">{f.t}</p>
                  <p className="text-xs text-[var(--text-muted)]">{f.d}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="relative flex items-center gap-2 font-mono text-[11px] text-[var(--text-muted)]">
          <StatusDot tone={provider.ok ? "success" : "warning"} pulse={provider.ok} />
          {provider.label}
        </div>
      </div>

      {/* Right — form */}
      <div className="flex items-center justify-center p-6 sm:p-10">
        <form onSubmit={submit} className="w-full max-w-sm animate-fade-in" data-testid="signin-form">
          <div className="mb-8 flex items-center gap-2.5 lg:hidden">
            <div className="grid h-9 w-9 place-items-center rounded-md border border-cyan-500/40 bg-cyan-500/10 text-cyan-300">
              <Waypoints size={18} />
            </div>
            <p className="font-heading text-base font-bold">KnowGridFlow</p>
          </div>

          <h2 className="font-heading text-xl font-semibold tracking-tight">Sign in</h2>
          <p className="mt-1 text-sm text-[var(--text-muted)]">
            Sign in with the username and password provisioned for you by an administrator.
          </p>

          <label className="mt-7 block">
            <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
              Username
            </span>
            <div className="mt-1.5 flex items-center gap-2 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-surface)] px-3 focus-within:border-[var(--accent)]">
              <UserRound size={15} className="text-[var(--text-muted)]" />
              <input
                data-testid="signin-username-input"
                name="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="h-10 w-full bg-transparent font-mono text-sm outline-none placeholder:text-[var(--text-muted)]"
                autoComplete="username"
                required
              />
            </div>
          </label>

          <label className="mt-4 block">
            <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
              Password
            </span>
            <div className="mt-1.5 flex items-center gap-2 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-surface)] px-3 focus-within:border-[var(--accent)]">
              <KeyRound size={15} className="text-[var(--text-muted)]" />
              <input
                data-testid="signin-password-input"
                name="password"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="h-10 w-full bg-transparent font-mono text-sm outline-none placeholder:text-[var(--text-muted)]"
                autoComplete="current-password"
                required
              />
            </div>
          </label>

          <label className="mt-4 block">
            <span className="font-mono text-[10px] uppercase tracking-[0.18em] text-[var(--text-muted)]">
              Tenant
            </span>
            <div className="mt-1.5 flex items-center gap-2 rounded-sm border border-[var(--border-strong)] bg-[var(--bg-surface)] px-3 focus-within:border-[var(--accent)]">
              <Boxes size={15} className="text-[var(--text-muted)]" />
              <input
                data-testid="signin-tenant-input"
                value={tenant}
                onChange={(e) => setTenant(e.target.value)}
                className="h-10 w-full bg-transparent font-mono text-sm outline-none"
                placeholder="default"
                autoComplete="off"
              />
            </div>
          </label>

          {error && (
            <p
              data-testid="signin-error"
              className="mt-4 rounded-sm border border-red-500/40 bg-red-500/10 px-3 py-2 text-xs text-red-300"
            >
              {error}
            </p>
          )}

          <Button
            type="submit"
            variant="primary"
            data-testid="signin-submit-button"
            disabled={submitting || !username.trim() || !password}
            className="mt-6 w-full justify-center"
          >
            {submitting ? <Loader2 size={16} className="animate-spin" /> : <>Continue <ArrowRight size={16} /></>}
          </Button>

          <p className="mt-5 text-center font-mono text-[10px] leading-relaxed text-[var(--text-muted)]">
            Your session token is held in memory only and never persisted to storage.
            Single sign-on (OIDC/SAML) is not available yet.
          </p>

        </form>
      </div>
    </div>
  );
}
