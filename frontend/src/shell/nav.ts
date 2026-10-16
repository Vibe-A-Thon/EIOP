import {
  LayoutDashboard,
  MessagesSquare,
  Waypoints,
  Network,
  type LucideIcon,
} from "lucide-react";

export interface NavItem {
  id: string;
  label: string;
  to: string;
  icon: LucideIcon;
  hint: string;
}

export const NAV_ITEMS: NavItem[] = [
  { id: "overview", label: "Overview", to: "/overview", icon: LayoutDashboard, hint: "Dashboard" },
  { id: "ask", label: "Ask", to: "/ask", icon: MessagesSquare, hint: "Natural-language query" },
  { id: "graph", label: "Graph Explorer", to: "/graph", icon: Waypoints, hint: "Primary work surface" },
  { id: "schema", label: "Schema", to: "/schema", icon: Network, hint: "Ontology & labels" },
];
