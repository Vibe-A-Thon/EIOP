import { create } from "zustand";

interface ShellState {
  inspectorEntityId: string | null;
  inspectorOpen: boolean;
  dockOpen: boolean;
  paletteOpen: boolean;
  railCollapsed: boolean;
  openInspector: (entityId: string) => void;
  closeInspector: () => void;
  setDockOpen: (open: boolean) => void;
  togglePalette: (open?: boolean) => void;
  toggleRail: () => void;
}

export const useShell = create<ShellState>((set) => ({
  inspectorEntityId: null,
  inspectorOpen: false,
  dockOpen: false,
  paletteOpen: false,
  railCollapsed: false,
  openInspector: (entityId) => set({ inspectorEntityId: entityId, inspectorOpen: true }),
  closeInspector: () => set({ inspectorOpen: false }),
  setDockOpen: (open) => set({ dockOpen: open }),
  togglePalette: (open) => set((s) => ({ paletteOpen: open ?? !s.paletteOpen })),
  toggleRail: () => set((s) => ({ railCollapsed: !s.railCollapsed })),
}));
