import { createContext, useContext, useEffect, useState, type ReactNode } from "react";

export type ThemeName = "dark" | "light" | "hc-dark" | "hc-light";

export const THEMES: { id: ThemeName; label: string }[] = [
  { id: "dark", label: "Dark" },
  { id: "light", label: "Light" },
  { id: "hc-dark", label: "High-contrast dark" },
  { id: "hc-light", label: "High-contrast light" },
];

interface ThemeCtx {
  theme: ThemeName;
  setTheme: (t: ThemeName) => void;
  cycle: () => void;
}

const Ctx = createContext<ThemeCtx | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [theme, setThemeState] = useState<ThemeName>("dark");

  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const setTheme = (t: ThemeName) => setThemeState(t);
  const cycle = () => {
    const order: ThemeName[] = ["dark", "light", "hc-dark", "hc-light"];
    setThemeState((prev) => order[(order.indexOf(prev) + 1) % order.length]);
  };

  return <Ctx.Provider value={{ theme, setTheme, cycle }}>{children}</Ctx.Provider>;
}

export function useTheme() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}
