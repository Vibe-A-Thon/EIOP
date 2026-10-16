import React, { useState, useId } from 'react';
import { tokens } from './tokens';

/**
 * Shared Button Component (UI-001)
 */
export function Button({
  children,
  variant = 'primary',
  size = 'md',
  disabled = false,
  loading = false,
  onClick,
  className = '',
  ariaLabel,
  ...props
}) {
  const baseStyles = {
    fontFamily: tokens.typography.fontFamily.sans,
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    borderRadius: tokens.radii.md,
    fontWeight: 600,
    cursor: disabled || loading ? 'not-allowed' : 'pointer',
    transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
    border: 'none',
    opacity: disabled ? 0.6 : 1,
    gap: '8px',
  };

  const sizeStyles = {
    sm: { padding: '6px 12px', fontSize: tokens.typography.fontSize.xs },
    md: { padding: '10px 18px', fontSize: tokens.typography.fontSize.sm },
    lg: { padding: '12px 24px', fontSize: tokens.typography.fontSize.base },
  }[size] || {};

  const variantStyles = {
    primary: {
      background: `linear-gradient(135deg, ${tokens.colors.brand.primary}, ${tokens.colors.brand.secondary})`,
      color: '#ffffff',
      boxShadow: tokens.shadows.glow,
    },
    secondary: {
      background: tokens.colors.bg.tertiary,
      color: tokens.colors.text.primary,
      border: `1px solid ${tokens.colors.border.light}`,
    },
    danger: {
      background: tokens.colors.status.danger,
      color: '#ffffff',
      boxShadow: tokens.shadows.md,
    },
    ghost: {
      background: 'transparent',
      color: tokens.colors.text.secondary,
    },
  }[variant] || {};

  return (
    <button
      style={{ ...baseStyles, ...sizeStyles, ...variantStyles }}
      disabled={disabled || loading}
      onClick={onClick}
      aria-label={ariaLabel}
      aria-busy={loading}
      className={`eoip-btn ${className}`}
      {...props}
    >
      {loading ? <span>⟳ Loading...</span> : children}
    </button>
  );
}

/**
 * Shared Card Component (UI-001)
 */
export function Card({ children, title, subtitle, className = '', style = {}, ...props }) {
  return (
    <div
      style={{
        background: tokens.colors.bg.surface,
        backdropFilter: 'blur(16px)',
        border: `1px solid ${tokens.colors.border.light}`,
        borderRadius: tokens.radii.lg,
        padding: '24px',
        boxShadow: tokens.shadows.glass,
        color: tokens.colors.text.primary,
        ...style,
      }}
      className={`eoip-card ${className}`}
      {...props}
    >
      {(title || subtitle) && (
        <div style={{ marginBottom: '16px' }}>
          {title && <h3 style={{ margin: 0, fontSize: tokens.typography.fontSize.lg, fontWeight: 600 }}>{title}</h3>}
          {subtitle && <p style={{ margin: '4px 0 0 0', color: tokens.colors.text.muted, fontSize: tokens.typography.fontSize.xs }}>{subtitle}</p>}
        </div>
      )}
      {children}
    </div>
  );
}

/**
 * Shared Badge Component (UI-001)
 */
export function Badge({ children, variant = 'info', className = '', ...props }) {
  const colors = {
    success: { bg: 'rgba(16, 185, 129, 0.15)', text: tokens.colors.status.success, border: 'rgba(16, 185, 129, 0.3)' },
    warning: { bg: 'rgba(245, 158, 11, 0.15)', text: tokens.colors.status.warning, border: 'rgba(245, 158, 11, 0.3)' },
    danger: { bg: 'rgba(239, 68, 68, 0.15)', text: tokens.colors.status.danger, border: 'rgba(239, 68, 68, 0.3)' },
    info: { bg: 'rgba(99, 102, 241, 0.15)', text: tokens.colors.brand.primary, border: 'rgba(99, 102, 241, 0.3)' },
  }[variant] || {};

  return (
    <span
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        padding: '2px 8px',
        borderRadius: tokens.radii.full,
        fontSize: tokens.typography.fontSize.xs,
        fontWeight: 600,
        background: colors.bg,
        color: colors.text,
        border: `1px solid ${colors.border}`,
      }}
      className={`eoip-badge ${className}`}
      {...props}
    >
      {children}
    </span>
  );
}

/**
 * Shared Input Component (UI-001)
 */
export function Input({ label, error, id, ariaLabel, style = {}, ...props }) {
  const generatedId = useId();
  const inputId = id || generatedId;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '6px', marginBottom: '12px' }}>
      {label && (
        <label htmlFor={inputId} style={{ color: tokens.colors.text.secondary, fontSize: tokens.typography.fontSize.xs, fontWeight: 500 }}>
          {label}
        </label>
      )}
      <input
        id={inputId}
        aria-label={ariaLabel || label}
        style={{
          background: tokens.colors.bg.tertiary,
          border: `1px solid ${error ? tokens.colors.status.danger : tokens.colors.border.light}`,
          borderRadius: tokens.radii.md,
          padding: '10px 14px',
          color: tokens.colors.text.primary,
          fontSize: tokens.typography.fontSize.sm,
          outline: 'none',
          ...style,
        }}
        {...props}
      />
      {error && <span style={{ color: tokens.colors.status.danger, fontSize: tokens.typography.fontSize.xs }}>{error}</span>}
    </div>
  );
}

/**
 * Shared Modal Dialog Component (UI-001)
 */
export function Modal({ isOpen, onClose, title, children }) {
  if (!isOpen) return null;

  return (
    <div
      role="dialog"
      aria-modal="true"
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.75)',
        backdropFilter: 'blur(8px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
      }}
      onClick={onClose}
    >
      <div
        style={{
          background: tokens.colors.bg.secondary,
          border: `1px solid ${tokens.colors.border.light}`,
          borderRadius: tokens.radii.lg,
          padding: '24px',
          maxWidth: '560px',
          width: '90%',
          boxShadow: tokens.shadows.glass,
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
          <h2 style={{ margin: 0, fontSize: tokens.typography.fontSize.lg, color: tokens.colors.text.primary }}>{title}</h2>
          <button
            onClick={onClose}
            aria-label="Close dialog"
            style={{ background: 'none', border: 'none', color: tokens.colors.text.muted, cursor: 'pointer', fontSize: '1.25rem' }}
          >
            ✕
          </button>
        </div>
        <div style={{ color: tokens.colors.text.secondary }}>{children}</div>
      </div>
    </div>
  );
}

/**
 * Advanced DataGrid Component (UI-003)
 */
export function DataGrid({ columns, data, pageSize = 10, title }) {
  const [sortKey, setSortKey] = useState(null);
  const [sortOrder, setSortOrder] = useState('asc');
  const [filterText, setFilterText] = useState('');
  const [currentPage, setCurrentPage] = useState(1);

  // Filter
  const filteredData = data.filter((row) =>
    columns.some((col) => {
      const val = row[col.key];
      return val ? String(val).toLowerCase().includes(filterText.toLowerCase()) : false;
    })
  );

  // Sort
  const sortedData = [...filteredData].sort((a, b) => {
    if (!sortKey) return 0;
    const valA = a[sortKey];
    const valB = b[sortKey];
    if (valA === valB) return 0;
    if (valA == null) return 1;
    if (valB == null) return -1;
    const res = valA > valB ? 1 : -1;
    return sortOrder === 'asc' ? res : -res;
  });

  // Paginate
  const totalPages = Math.ceil(sortedData.length / pageSize) || 1;
  const paginatedData = sortedData.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const handleSort = (key) => {
    if (sortKey === key) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortKey(key);
      setSortOrder('asc');
    }
  };

  return (
    <Card title={title}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '12px', alignItems: 'center' }}>
        <Input
          placeholder="Search grid..."
          ariaLabel="Search grid records"
          value={filterText}
          onChange={(e) => {
            setFilterText(e.target.value);
            setCurrentPage(1);
          }}
          style={{ width: '240px', marginBottom: 0 }}
        />
        <span style={{ fontSize: tokens.typography.fontSize.xs, color: tokens.colors.text.muted }}>
          Showing {paginatedData.length} of {filteredData.length} entries
        </span>
      </div>

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: tokens.typography.fontSize.sm }}>
          <thead>
            <tr style={{ borderBottom: `1px solid ${tokens.colors.border.light}` }}>
              {columns.map((col) => (
                <th
                  key={col.key}
                  onClick={() => handleSort(col.key)}
                  style={{
                    padding: '12px 16px',
                    color: tokens.colors.text.secondary,
                    fontWeight: 600,
                    cursor: 'pointer',
                    userSelect: 'none',
                  }}
                >
                  {col.header} {sortKey === col.key ? (sortOrder === 'asc' ? '▲' : '▼') : ''}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {paginatedData.map((row, idx) => (
              <tr
                key={row.id || idx}
                style={{
                  borderBottom: `1px solid ${tokens.colors.border.subtle}`,
                  transition: 'background 0.15s ease',
                }}
              >
                {columns.map((col) => (
                  <td key={col.key} style={{ padding: '12px 16px', color: tokens.colors.text.primary }}>
                    {col.render ? col.render(row[col.key], row) : row[col.key]}
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {totalPages > 1 && (
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '8px', marginTop: '16px', alignItems: 'center' }}>
          <Button
            size="sm"
            variant="secondary"
            disabled={currentPage === 1}
            onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
          >
            Previous
          </Button>
          <span style={{ color: tokens.colors.text.secondary, fontSize: tokens.typography.fontSize.xs }}>
            Page {currentPage} of {totalPages}
          </span>
          <Button
            size="sm"
            variant="secondary"
            disabled={currentPage === totalPages}
            onClick={() => setCurrentPage((p) => Math.min(totalPages, p + 1))}
          >
            Next
          </Button>
        </div>
      )}
    </Card>
  );
}
