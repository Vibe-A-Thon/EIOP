import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { apiFetch, setActiveTenant, setAuthToken } from "./api";

export interface Principal {
  id: string;
  username: string;
  roles: string[];
  tenant_id?: string | null;
  label: string;
  provider: string;
}

export interface Session {
  token: string;
  principal: Principal;
  tenant: string;
  workspace: string;
}

interface AuthCtx {
  session: Session | null;
  signIn: (username: string, password: string, tenant: string) => Promise<void>;
  signOut: () => void;
  setScope: (tenant: string, workspace: string) => void;
}

const Ctx = createContext<AuthCtx | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);

  // FT-AUTH: login credentials only. The role shown here is whatever the server derives
  // from the authenticated user record; there is no client-side fallback principal.
  const signIn = async (username: string, password: string, tenant: string) => {
    setAuthToken(null);
    const { token } = await apiFetch<{ token: string }>("/auth/login", {
      method: "POST",
      body: { username, password },
      tenant: null,
    });
    setAuthToken(token);
    setActiveTenant(tenant);
    try {
      const me = await apiFetch<any>("/auth/whoami");
      const roles: string[] = me.roles || [];
      const topRole = roles.includes("superadmin")
        ? "Super admin"
        : me.is_admin
          ? "Administrator"
          : roles[0]
            ? roles[0][0].toUpperCase() + roles[0].slice(1)
            : "Member";
      const principal: Principal = {
        id: me.id,
        username: me.username,
        roles,
        tenant_id: me.tenant_id ?? null,
        label: `${topRole}${me.tenant_id ? ` · ${me.tenant_id}` : " · all tenants"}`,
        provider: me.provider,
      };
      setSession({ token, principal, tenant, workspace: "default" });
    } catch (err) {
      setAuthToken(null);
      setActiveTenant(null);
      throw err;
    }
  };

  const signOut = () => {
    apiFetch("/auth/logout", { method: "POST" }).catch(() => {});
    setAuthToken(null);
    setActiveTenant(null);
    setSession(null);
  };

  const setScope = (tenant: string, workspace: string) => {
    setActiveTenant(tenant);
    setSession((prev) => (prev ? { ...prev, tenant, workspace } : prev));
  };

  // On any 401 after sign-in, clear session and return to sign-in.
  useEffect(() => {
    const onUnauthorized = () => {
      setSession((prev) => {
        if (prev) {
          setAuthToken(null);
          setActiveTenant(null);
          return null;
        }
        return prev;
      });
    };
    window.addEventListener("kgf:unauthorized", onUnauthorized);
    return () => window.removeEventListener("kgf:unauthorized", onUnauthorized);
  }, []);

  return (
    <Ctx.Provider value={{ session, signIn, signOut, setScope }}>{children}</Ctx.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
