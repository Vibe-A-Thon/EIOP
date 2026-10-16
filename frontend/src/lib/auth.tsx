import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { apiFetch, setActiveTenant, setAuthToken } from "./api";

export interface Principal {
  id: string;
  username: string;
  roles: string[];
  tenant_id?: string | null;
  label: string;
  bootstrap: boolean;
}

export interface Session {
  token: string;
  principal: Principal;
  tenant: string;
  workspace: string;
}

interface AuthCtx {
  session: Session | null;
  signIn: (token: string, tenant: string) => Promise<void>;
  signOut: () => void;
  setScope: (tenant: string, workspace: string) => void;
}

const Ctx = createContext<AuthCtx | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<Session | null>(null);

  const signIn = async (token: string, tenant: string) => {
    setAuthToken(token);
    setActiveTenant(tenant);
    let principal: Principal;
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
      principal = {
        id: me.id || "principal",
        username: me.username || "user",
        roles,
        tenant_id: me.tenant_id ?? null,
        label: `${topRole}${me.tenant_id ? ` · ${me.tenant_id}` : " · all tenants"}`,
        bootstrap: me.provider === "asg" && me.username?.startsWith("bootstrap"),
      };
    } catch {
      principal = {
        id: "urn:eoip:authn:principal:bootstrap",
        username: "bootstrap-admin",
        roles: ["admin", "system"],
        tenant_id: null,
        label: "Deployment access (bootstrap token)",
        bootstrap: true,
      };
    }
    setSession({ token, principal, tenant, workspace: "default" });
  };

  const signOut = () => {
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
