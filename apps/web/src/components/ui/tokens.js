/**
 * Design Tokens & Theme System for EOIP (UI-001).
 * Supports dark/light modes, vibrant accents, glassmorphic blurs, and typography.
 */

export const tokens = {
  colors: {
    // Dark Theme Palette
    bg: {
      primary: '#090d16',
      secondary: '#0f172a',
      tertiary: '#1e293b',
      surface: 'rgba(30, 41, 59, 0.7)',
      glass: 'rgba(15, 23, 42, 0.75)',
    },
    // Vibrant Accents
    brand: {
      primary: '#6366f1',    // Indigo
      primaryHover: '#4f46e5',
      secondary: '#06b6d4',  // Cyan
      accent: '#ec4899',     // Pink
      glow: 'rgba(99, 102, 241, 0.35)',
    },
    // Text Hierarchy
    text: {
      primary: '#f8fafc',
      secondary: '#94a3b8',
      muted: '#64748b',
      inverse: '#0f172a',
    },
    // Status & Semantic Colors
    status: {
      success: '#10b981',
      successGlow: 'rgba(16, 185, 129, 0.25)',
      warning: '#f59e0b',
      warningGlow: 'rgba(245, 158, 11, 0.25)',
      danger: '#ef4444',
      dangerGlow: 'rgba(239, 68, 68, 0.25)',
      info: '#3b82f6',
    },
    // Borders & Dividers
    border: {
      light: 'rgba(255, 255, 255, 0.1)',
      subtle: 'rgba(255, 255, 255, 0.05)',
      focus: '#6366f1',
    },
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
    xxl: '48px',
  },
  radii: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '9999px',
  },
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.2), 0 2px 4px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.3), 0 4px 6px -2px rgba(0, 0, 0, 0.15)',
    glow: '0 0 20px rgba(99, 102, 241, 0.4)',
    glass: '0 8px 32px 0 rgba(0, 0, 0, 0.37)',
  },
  typography: {
    fontFamily: {
      sans: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif",
      mono: "'JetBrains Mono', 'Fira Code', monospace",
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      xxl: '1.5rem',
    },
  },
};
