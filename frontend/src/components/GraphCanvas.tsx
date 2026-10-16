import { useEffect, useRef } from "react";
import Graph from "graphology";
import Sigma from "sigma";
import forceAtlas2 from "graphology-layout-forceatlas2";

export interface GNode {
  id: string;
  label: string;
  domain?: string;
  properties?: Record<string, any>;
}
export interface GEdge {
  id: string;
  from_id: string;
  to_id: string;
  type: string;
  creation_status?: string;
}

interface Props {
  nodes: GNode[];
  edges: GEdge[];
  colorOf: (n: GNode) => string;
  edgeColorOf: (e: GEdge) => string;
  selectedId?: string | null;
  highlightNodes?: Set<string>;
  highlightEdges?: Set<string>;
  onSelect: (id: string) => void;
}

const DIM_NODE = "#2b3442";
const DIM_EDGE = "#1b2430";
const PATH_EDGE = "#22d3ee";

export function GraphCanvas({
  nodes,
  edges,
  colorOf,
  edgeColorOf,
  selectedId,
  highlightNodes,
  highlightEdges,
  onSelect,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const sigmaRef = useRef<Sigma | null>(null);
  const graphRef = useRef<any>(null);

  useEffect(() => {
    if (!containerRef.current) return;
    const GraphCtor = Graph as unknown as new (opts?: any) => any;
    const graph: any = new GraphCtor({ multi: true, type: "directed" });

    const present = new Set(nodes.map((n) => n.id));
    nodes.forEach((n, i) => {
      const angle = (i / Math.max(nodes.length, 1)) * Math.PI * 2;
      const color = colorOf(n);
      graph.addNode(n.id, {
        label: n.properties?.name || n.properties?.title || n.label,
        x: Math.cos(angle) * 10 + Math.random(),
        y: Math.sin(angle) * 10 + Math.random(),
        size: 6,
        color,
        _baseColor: color,
      });
    });
    edges.forEach((e) => {
      if (!present.has(e.from_id) || !present.has(e.to_id)) return;
      try {
        const color = edgeColorOf(e);
        graph.addEdgeWithKey(e.id, e.from_id, e.to_id, {
          color,
          _baseColor: color,
          size: 1,
          type: "arrow",
        });
      } catch {
        /* duplicate key */
      }
    });

    graph.forEachNode((node: string) => {
      const deg = graph.degree(node);
      const size = Math.min(4 + deg * 1.1, 16);
      graph.setNodeAttribute(node, "size", size);
      graph.setNodeAttribute(node, "_baseSize", size);
    });

    const reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (nodes.length > 1) {
      forceAtlas2.assign(graph, {
        iterations: reduce ? 60 : 220,
        settings: { gravity: 1.2, scalingRatio: 12, slowDown: 2, barnesHutOptimize: nodes.length > 200 },
      });
    }

    const renderer = new Sigma(graph, containerRef.current, {
      allowInvalidContainer: true,
      renderEdgeLabels: false,
      defaultEdgeColor: "#334155",
      labelColor: { color: getComputedStyle(document.documentElement).getPropertyValue("--text-secondary") || "#94a3b8" },
      labelSize: 11,
      labelFont: "IBM Plex Sans, sans-serif",
      labelRenderedSizeThreshold: 8,
      minCameraRatio: 0.05,
      maxCameraRatio: 12,
    });

    renderer.on("clickNode", ({ node }) => onSelect(node));
    renderer.on("enterNode", () => {
      if (containerRef.current) containerRef.current.style.cursor = "pointer";
    });
    renderer.on("leaveNode", () => {
      if (containerRef.current) containerRef.current.style.cursor = "default";
    });

    sigmaRef.current = renderer;
    graphRef.current = graph;

    return () => {
      renderer.kill();
      sigmaRef.current = null;
      graphRef.current = null;
    };
  }, [nodes, edges, colorOf, edgeColorOf, onSelect]);

  // Decoration: selection + path highlight (dim everything else). No relayout.
  useEffect(() => {
    const graph = graphRef.current;
    const renderer = sigmaRef.current;
    if (!graph || !renderer) return;
    const hasHighlight = !!highlightNodes && highlightNodes.size > 0;

    graph.forEachNode((node: string) => {
      const base = graph.getNodeAttribute(node, "_baseColor");
      const baseSize = graph.getNodeAttribute(node, "_baseSize") || 6;
      if (hasHighlight) {
        const on = highlightNodes!.has(node);
        graph.setNodeAttribute(node, "color", on ? base : DIM_NODE);
        graph.setNodeAttribute(node, "size", on ? baseSize * 1.5 : baseSize * 0.75);
        graph.setNodeAttribute(node, "highlighted", on || node === selectedId);
        graph.setNodeAttribute(node, "zIndex", on ? 2 : 0);
      } else {
        graph.setNodeAttribute(node, "color", base);
        graph.setNodeAttribute(node, "size", baseSize);
        graph.setNodeAttribute(node, "highlighted", node === selectedId);
        graph.setNodeAttribute(node, "zIndex", node === selectedId ? 1 : 0);
      }
    });

    graph.forEachEdge((edge: string) => {
      const base = graph.getEdgeAttribute(edge, "_baseColor");
      if (hasHighlight && highlightEdges) {
        const on = highlightEdges.has(edge);
        graph.setEdgeAttribute(edge, "color", on ? PATH_EDGE : DIM_EDGE);
        graph.setEdgeAttribute(edge, "size", on ? 2.5 : 0.6);
        graph.setEdgeAttribute(edge, "zIndex", on ? 2 : 0);
      } else {
        graph.setEdgeAttribute(edge, "color", base);
        graph.setEdgeAttribute(edge, "size", 1);
        graph.setEdgeAttribute(edge, "zIndex", 0);
      }
    });

    renderer.refresh();
  }, [selectedId, highlightNodes, highlightEdges]);

  return <div ref={containerRef} className="h-full w-full" data-testid="graph-canvas" />;
}
