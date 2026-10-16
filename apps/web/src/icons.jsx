import React, {useEffect, useId, useRef, useState} from 'react';
import {createPortal} from 'react-dom';
import {
  Activity, ArrowRight, ChartNoAxesCombined, Check, ChevronRight, Clock, Code,
  Copy, Cpu, Database, Download, Eye, EyeOff, FileText, Filter, Focus, GitBranch,
  Info, KeyRound, Layers, Link, Lock, LogOut, Menu, Minus, Network, Play,
  Plus, Radar, RefreshCw, Search, Settings, Shield, ShieldCheck, SlidersHorizontal,
  Sparkles, TriangleAlert, Upload, Users, X, Zap,
} from 'lucide-react';

const registry = {
  activity: Activity, arrow: ArrowRight, chart: ChartNoAxesCombined, check: Check,
  chevron: ChevronRight, clock: Clock, code: Code, copy: Copy, cpu: Cpu,
  database: Database, document: FileText, download: Download, eye: Eye, eyeOff: EyeOff,
  filter: Filter, focus: Focus, gitBranch: GitBranch, graph: Network, info: Info,
  key: KeyRound, layers: Layers, link: Link, lock: Lock, logout: LogOut,
  menu: Menu, minus: Minus, play: Play, plus: Plus, radar: Radar, refresh: RefreshCw,
  search: Search, settings: Settings, shield: Shield, shieldCheck: ShieldCheck,
  sliders: SlidersHorizontal, spark: Sparkles, upload: Upload, users: Users, warning: TriangleAlert, close: X, zap: Zap,
};

export function Icon({name, size = 18, className = ''}) {
  const Component = registry[name] || Info;
  return <Component className={`icon ${className}`} size={size} strokeWidth={1.75} aria-hidden="true"/>;
}

export function Tip({text, children, className = ''}) {
  const id = useId();
  const ref = useRef(null);
  const [position, setPosition] = useState(null);
  const show = () => {
    const rect = ref.current?.getBoundingClientRect();
    if (rect) setPosition({left: Math.max(128, Math.min(window.innerWidth - 128, rect.left + rect.width / 2)),
      top: rect.top > 70 ? rect.top - 8 : rect.bottom + 8, above: rect.top > 70});
  };
  useEffect(() => {
    if (!position) return;
    const close = event => {if (event.type !== 'keydown' || event.key === 'Escape') setPosition(null);};
    window.addEventListener('keydown', close);
    window.addEventListener('scroll', close, true);
    window.addEventListener('resize', close);
    return () => {window.removeEventListener('keydown', close); window.removeEventListener('scroll', close, true); window.removeEventListener('resize', close);};
  }, [position]);
  const described = React.isValidElement(children) ? React.cloneElement(children, {
    'aria-describedby': [children.props['aria-describedby'], position && id].filter(Boolean).join(' ') || undefined,
  }) : children;
  return <span ref={ref} className={`tip ${className}`} onMouseEnter={show} onMouseLeave={() => setPosition(null)}
    onFocus={show} onBlur={() => setPosition(null)}>{described}
    {position && text && createPortal(<span id={id} role="tooltip" className="atlas-tooltip"
      style={{left: position.left, top: position.top, transform: `translate(-50%, ${position.above ? '-100%' : '0'})`}}>{text}</span>, document.body)}
  </span>;
}
