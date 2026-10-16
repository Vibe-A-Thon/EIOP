import React, {useState, useEffect, useCallback} from 'react';
import {Icon} from '../icons.jsx';

const DOMAINS = [
  {id: 'bfsi', name: 'Banking & Financial Services (BFSI)', icon: 'shield', desc: 'Accounts, Transactions, AML, KYC, Risk Exposures'},
  {id: 'cybersecurity', name: 'Cybersecurity & Threat Mesh', icon: 'shield', desc: 'Assets, CVEs, Attack Vectors, Threat Actors, Mitigations'},
  {id: 'healthcare', name: 'Healthcare & Life Sciences', icon: 'activity', desc: 'Patients, Providers, Clinical Encounters, HIPAA Compliance'},
  {id: 'compliance', name: 'Regulatory & Audit Compliance', icon: 'document', desc: 'SOC2, ISO27001, GDPR, Policies, Evidence Ledgers'},
  {id: 'data-governance', name: 'Enterprise Data Governance', icon: 'database', desc: 'Data Lineage, Catalogs, Quality Rules, Schemas'},
  {id: 'itsm', name: 'IT Service Management (ITSM)', icon: 'activity', desc: 'CMDB, Incidents, Change Requests, Service Catalogs'},
  {id: 'manufacturing', name: 'Manufacturing & Supply Chain', icon: 'layers', desc: 'BOM, Suppliers, IoT Telemetry, Inventory Assets'},
  {id: 'software-engineering', name: 'Software Delivery & DevOps', icon: 'code', desc: 'Repos, Commits, Pipelines, Deployments, Test Runs'},
];

export default function DomainPackDashboard({api}) {
  const [packStatus, setPackStatus] = useState({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [seedTopology, setSeedTopology] = useState(true);
  const [activeMessage, setActiveMessage] = useState(null);

  const fetchDomainPacks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api('/api/v1/domain-packs', undefined, 'GET').catch(() => null);
      if (res && res.packs) {
        setPackStatus(res.packs);
      } else {
        // Fallback initialized map
        const initial = {};
        DOMAINS.forEach(d => { initial[d.id] = {active: false, entity_count: 0}; });
        setPackStatus(initial);
      }
    } catch (err) {
      setError(err.message || 'Failed to fetch domain packs');
    } finally {
      setLoading(false);
    }
  }, [api]);

  useEffect(() => {
    fetchDomainPacks();
  }, [fetchDomainPacks]);

  const activatePack = async (domainId) => {
    setLoading(true);
    setError(null);
    setActiveMessage(null);
    try {
      const res = await api(`/api/v1/domain-packs/${domainId}/activate`, {
        seed_live_topology: seedTopology,
      }, 'POST');
      setActiveMessage(`Successfully activated ${domainId.toUpperCase()} domain pack!`);
      setPackStatus(prev => ({
        ...prev,
        [domainId]: {...(prev[domainId] || {}), active: true, activated_at: new Date().toISOString()},
      }));
    } catch (err) {
      setError(`Failed to activate ${domainId}: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="domainpack-dashboard" style={{padding: '1.5rem', display: 'flex', flexDirection: 'column', gap: '1.5rem'}}>
      <header style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color, #333)', paddingBottom: '1rem'}}>
        <div>
          <h2 style={{margin: 0, display: 'flex', alignItems: 'center', gap: '0.5rem'}}>
            <Icon name="layers" /> Industry Domain Pack Lifecycle Manager
          </h2>
          <p style={{margin: '0.25rem 0 0 0', color: 'var(--text-muted, #888)'}}>
            UI-03 · Turnkey domain packs for enterprise ontologies, pre-seeded schemas, and automated digital twins
          </p>
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: '1rem'}}>
          <label style={{display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.85rem', color: '#ccc', cursor: 'pointer'}}>
            <input
              type="checkbox"
              checked={seedTopology}
              onChange={e => setSeedTopology(e.target.checked)}
            />
            Seed Live Topology on Activation
          </label>
          <button
            onClick={fetchDomainPacks}
            disabled={loading}
            style={{padding: '0.5rem 1rem', background: '#333', color: '#fff', border: '1px solid #555', borderRadius: '4px', cursor: 'pointer'}}
          >
            Refresh Status
          </button>
        </div>
      </header>

      {error && (
        <div style={{padding: '1rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid #ef4444', borderRadius: '6px', color: '#f87171'}}>
          {error}
        </div>
      )}

      {activeMessage && (
        <div style={{padding: '1rem', background: 'rgba(16, 185, 129, 0.1)', border: '1px solid #10b981', borderRadius: '6px', color: '#34d399'}}>
          {activeMessage}
        </div>
      )}

      <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.25rem'}}>
        {DOMAINS.map(d => {
          const status = packStatus[d.id] || {};
          const isActive = status.active || false;
          return (
            <div
              key={d.id}
              className="domain-card"
              style={{
                background: '#1a1a22',
                border: isActive ? '1px solid #10b981' : '1px solid #333',
                borderRadius: '8px',
                padding: '1.25rem',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-between',
                gap: '1rem',
              }}
            >
              <div>
                <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start'}}>
                  <h3 style={{margin: '0 0 0.5rem 0', fontSize: '1.1rem', color: '#fff', display: 'flex', alignItems: 'center', gap: '0.4rem'}}>
                    <Icon name={d.icon} size={18} /> {d.name}
                  </h3>
                  <span
                    style={{
                      fontSize: '0.75rem',
                      padding: '0.2rem 0.5rem',
                      borderRadius: '12px',
                      background: isActive ? 'rgba(16, 185, 129, 0.2)' : 'rgba(255, 255, 255, 0.1)',
                      color: isActive ? '#34d399' : '#888',
                      fontWeight: 600,
                    }}
                  >
                    {isActive ? 'ACTIVE' : 'READY'}
                  </span>
                </div>
                <p style={{fontSize: '0.85rem', color: '#aaa', margin: 0, lineHeight: 1.4}}>
                  {d.desc}
                </p>
              </div>

              <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid #2a2a35', paddingTop: '0.75rem'}}>
                <span style={{fontSize: '0.8rem', color: '#666'}}>ID: {d.id}</span>
                <button
                  onClick={() => activatePack(d.id)}
                  disabled={loading}
                  style={{
                    padding: '0.4rem 0.9rem',
                    background: isActive ? '#059669' : '#6366f1',
                    color: '#fff',
                    border: 'none',
                    borderRadius: '4px',
                    cursor: 'pointer',
                    fontWeight: 600,
                    fontSize: '0.85rem',
                  }}
                >
                  {isActive ? 'Re-Activate / Seed' : 'Activate Pack'}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
