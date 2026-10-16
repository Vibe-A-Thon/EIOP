import {
  Activity,
  Bot,
  DatabaseZap,
  FileBarChart,
  GitCompareArrows,
  HeartPulse,
  LayoutDashboard,
  LifeBuoy,
  MessagesSquare,
  Network,
  Palette,
  Radar,
  Route as RouteIcon,
  ScrollText,
  Settings,
  Shapes,
  ShieldCheck,
  SlidersHorizontal,
  SquareStack,
  TerminalSquare,
  History,
  Users,
  Waypoints,
  type LucideIcon,
} from "lucide-react";

export interface NavItem {
  id: string;
  label: string;
  to: string;
  icon: LucideIcon;
  adminOnly?: boolean;
}

export interface NavGroup {
  label: string;
  items: NavItem[];
}

export const NAV_GROUPS: NavGroup[] = [
  {
    label: "Workspace",
    items: [
      { id: "overview", label: "Overview", to: "/overview", icon: LayoutDashboard },
      { id: "ask", label: "Ask", to: "/ask", icon: MessagesSquare },
    ],
  },
  {
    label: "Explore",
    items: [
      { id: "graph", label: "Graph Explorer", to: "/graph", icon: Waypoints },
      { id: "meta-graph", label: "Meta-graph", to: "/meta-graph", icon: Shapes },
      { id: "query", label: "Query", to: "/query", icon: TerminalSquare },
      { id: "impact", label: "Impact", to: "/impact", icon: Radar },
      { id: "changes", label: "Changes", to: "/changes", icon: GitCompareArrows },
      { id: "time", label: "Time Travel", to: "/time", icon: History },
      { id: "incidents", label: "Incidents", to: "/incidents", icon: Activity },
    ],
  },
  {
    label: "Knowledge",
    items: [
      { id: "ontology", label: "Ontology", to: "/ontology", icon: Network },
      { id: "quality", label: "Quality", to: "/quality", icon: ShieldCheck },
      { id: "snapshots", label: "Snapshots", to: "/snapshots", icon: SquareStack },
    ],
  },
  {
    label: "Operate",
    items: [
      { id: "ingestion", label: "Ingestion", to: "/ingestion", icon: DatabaseZap },
      { id: "agents", label: "Agents", to: "/agents", icon: Bot },
      { id: "reports", label: "Reports", to: "/reports", icon: FileBarChart },
      { id: "collaboration", label: "Collaboration", to: "/collaboration", icon: Users },
      { id: "health", label: "Health", to: "/health", icon: HeartPulse },
    ],
  },
  {
    label: "Govern",
    items: [
      { id: "governance", label: "Governance", to: "/governance", icon: ScrollText, adminOnly: true },
      { id: "brand", label: "Brand", to: "/brand", icon: Palette, adminOnly: true },
      { id: "tenant", label: "Tenant", to: "/tenant", icon: SlidersHorizontal, adminOnly: true },
    ],
  },
  {
    label: "System",
    items: [
      { id: "settings", label: "Settings", to: "/settings", icon: Settings },
      { id: "help", label: "Help & About", to: "/help", icon: LifeBuoy },
    ],
  },
];

export const NAV_ITEMS: NavItem[] = NAV_GROUPS.flatMap((g) => g.items);
export const _routeIcons = { RouteIcon };
