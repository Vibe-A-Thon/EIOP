import { create } from "zustand";

export interface Pin {
  id: string;
  text: string;
  source?: string;
  question?: string;
  at: string;
}

interface PinsState {
  pins: Pin[];
  open: boolean;
  addPin: (pin: Omit<Pin, "id" | "at">) => void;
  removePin: (id: string) => void;
  clear: () => void;
  setOpen: (open: boolean) => void;
}

export const usePins = create<PinsState>((set, get) => ({
  pins: [],
  open: false,
  addPin: (pin) => {
    const key = `${pin.text}|${pin.source || ""}`;
    if (get().pins.some((p) => `${p.text}|${p.source || ""}` === key)) {
      set({ open: true });
      return;
    }
    set((s) => ({
      open: true,
      pins: [
        { ...pin, id: `${Date.now()}-${Math.random().toString(36).slice(2, 6)}`, at: new Date().toISOString() },
        ...s.pins,
      ],
    }));
  },
  removePin: (id) => set((s) => ({ pins: s.pins.filter((p) => p.id !== id) })),
  clear: () => set({ pins: [] }),
  setOpen: (open) => set({ open }),
}));
