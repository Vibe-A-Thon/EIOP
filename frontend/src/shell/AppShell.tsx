import type { ReactNode } from "react";
import { NavRail } from "./NavRail";
import { TopBar } from "./TopBar";
import { Inspector } from "./Inspector";
import { Dock } from "./Dock";
import { CommandPalette } from "./CommandPalette";

export function AppShell({ children }: { children: ReactNode }) {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-[var(--bg-void)]">
      <NavRail />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar />
        <div className="flex min-h-0 flex-1">
          <main className="min-w-0 flex-1 overflow-y-auto">{children}</main>
          <Inspector />
        </div>
        <Dock />
      </div>
      <CommandPalette />
    </div>
  );
}
